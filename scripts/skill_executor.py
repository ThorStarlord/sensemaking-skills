"""
Skill Executor — interface and implementations for invoking skills.

Defines the boundary between "the runtime prepared skill invocation" and
"the skill was actually invoked." This prevents dry-run logging from being
reported as real skill execution.

Usage:
    from skill_executor import create_executor

    executor = create_executor("dry-run", repo_root)
    result = executor.invoke_skill(skill_id, command, input_artifacts, expected_output, context)
    print(result.status)  # PREPARED, PROMPT_GENERATED, EXECUTED, FAILED, UNSUPPORTED
"""

import os
import sys
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

# SDK type imports for error classification
from claude_agent_sdk import ResultMessage


# ============================================================================
# Output path resolution (shared by real executors)
# ============================================================================

def resolve_output_path(repo_root: str, expected_output_artifact: str, context: Optional[dict]) -> str:
    """Resolve the absolute path where a skill's output artifact must be written.

    The runtime owns artifact path resolution (contracts + session scoping via
    OrchestrationRunner._resolve_artifact_path). When it invokes a skill it passes
    the already-resolved, session-scoped path as context['expected_output_path'].
    Executors MUST honor that path so the producer (executor) and consumer
    (runtime) agree on where the artifact lives.

    Only when no path is provided (e.g. an executor used standalone, outside the
    runtime) do we fall back to the flat artifacts/<id>.md path.
    """
    provided = (context or {}).get("expected_output_path")
    if provided:
        return provided
    return os.path.join(repo_root, "artifacts", expected_output_artifact + ".md")


# ============================================================================
# Session-root artifact-write confinement (issue #43)
# ============================================================================
#
# create-artifact.py's own overwrite guard (PR #41 / issue #40) only stops a
# collision with an EXISTING tracked file. A fresh path outside the active
# session is not caught by anything: nothing checks WHERE expected_output_path
# is honored, only whether it exists once written. This section closes that
# gap for the Claude Agent SDK executor by making runtime artifact writes
# structurally confined, not just contract-conformant.
#
# Mechanism: a `PreToolUse` hook, not `can_use_tool`. The SDK's own contract
# (claude_agent_sdk.types.ClaudeAgentOptions.can_use_tool docstring) states
# can_use_tool is only invoked for tool calls that would otherwise prompt the
# user -- it is never invoked for a tool already permitted by allowed_tools.
# Since Write/Bash/etc. are named in allowed_tools below, can_use_tool would
# never fire for them and would be a fake gate. A PreToolUse hook with
# matcher=None is documented to observe/gate every tool call regardless of
# allowed_tools/permission_mode, which is what "structural confinement"
# requires.


def canonicalize_path(path: str) -> str:
    """Canonicalize a path for authorization comparison.

    Resolves to an absolute, symlink/junction-resolved, case-normalized form
    so that two different spellings of the same on-disk location (relative
    vs. absolute, mixed drive-letter case, a symlinked ancestor, a `..`
    traversal) compare equal, while genuinely different locations never do.

    Deliberately NOT a string-prefix check: a prefix match would treat
    "artifacts/100-run-2" as inside "artifacts/100-run" and is defeated by
    ".." components without normalization first.

    `os.path.realpath` resolves symlinks/junctions for whatever prefix of the
    path currently exists on disk; for a not-yet-created final path
    component (the common case -- the artifact doesn't exist yet) there is
    nothing to resolve for that component, so it is carried through
    unchanged. That is correct here: authorization is about *where* the
    write will land, and only existing ancestor directories can be
    symlinked into another location.
    """
    resolved = os.path.realpath(os.path.abspath(os.path.normpath(path)))
    return os.path.normcase(resolved)


# Tools this executor ever grants to the model. Anything not read-only or not
# the single artifact-writing tool is denied by the hook below, whether or
# not it is also excluded from allowed_tools -- the hook is the authority,
# allowed_tools is defense-in-depth on top of it.
_READ_ONLY_TOOLS = frozenset({"Read", "Glob", "Grep"})
_ARTIFACT_WRITE_TOOL = "Write"


def _deny(message: str) -> dict:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": message,
        }
    }


def _allow() -> dict:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
        }
    }


def build_artifact_permission_gate(expected_output_path: Optional[str]):
    """Build a PreToolUse hook callback confining writes to expected_output_path.

    Closed over the runtime-resolved expected_output_path for one invocation
    (never supplied by the model). Missing/empty expected_output_path fails
    closed: every mutating tool call is denied, since there is nothing to
    authorize against.

    Returned callable matches the SDK's HookCallback signature:
    (input_data: dict, tool_use_id: str | None, context: HookContext) -> Awaitable[dict]
    """
    authorized_canonical = canonicalize_path(expected_output_path) if expected_output_path else None

    async def artifact_permission_gate(input_data, tool_use_id, context):
        tool_name = input_data.get("tool_name")
        tool_input = input_data.get("tool_input") or {}

        if tool_name in _READ_ONLY_TOOLS:
            return _allow()

        if tool_name == _ARTIFACT_WRITE_TOOL:
            if authorized_canonical is None:
                return _deny(
                    "No expected_output_path was authorized for this invocation; "
                    "refusing all writes (fail-closed)."
                )
            file_path = tool_input.get("file_path")
            if not isinstance(file_path, str) or not file_path.strip():
                return _deny(
                    "Write call is missing a valid file_path; refusing (fail-closed)."
                )
            if canonicalize_path(file_path) != authorized_canonical:
                return _deny(
                    f"Write to '{file_path}' is not the runtime-authorized artifact "
                    f"path. This invocation may only write to: {expected_output_path}"
                )
            return _allow()

        return _deny(
            f"Tool '{tool_name}' is not permitted during runtime-owned artifact "
            f"writes. Only {sorted(_READ_ONLY_TOOLS)} and "
            f"'{_ARTIFACT_WRITE_TOOL}' (to the authorized path) are allowed."
        )

    return artifact_permission_gate


# ============================================================================
# Status Enum
# ============================================================================

class SkillExecutionStatus(Enum):
    """Honest status values that distinguish preparation from real execution."""
    PREPARED = "prepared"          # dry-run: invocation was prepared/logged
    PROMPT_GENERATED = "prompt_generated"  # prompt-chain: human/agent prompt created
    EXECUTED = "executed"          # real skill execution happened
    FAILED = "failed"              # attempted and failed
    UNSUPPORTED = "unsupported"    # selected executor is not implemented


# ============================================================================
# Result Object
# ============================================================================

@dataclass
class SkillExecutionResult:
    """Result of a single skill invocation attempt."""
    skill_id: str
    status: SkillExecutionStatus
    command: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    output_artifact: Optional[str] = None
    message: str = ""
    error: str = ""
    validator_results: Optional[list] = None
    validation_passed: Optional[bool] = None

    def to_dict(self) -> dict:
        return {
            "skill_id": self.skill_id,
            "status": self.status.value,
            "command": self.command,
            "timestamp": self.timestamp,
            "output_artifact": self.output_artifact,
            "message": self.message,
            "error": self.error,
            "validator_results": self.validator_results,
            "validation_passed": self.validation_passed,
        }


# ============================================================================
# Abstract Base Class
# ============================================================================

class SkillExecutor(ABC):
    """Interface for skill invocation.

    Each executor implementation determines how a skill is actually invoked.
    The runtime selects an executor based on the execution mode and passes
    it to the skill-execution-agent.
    """

    supports_real_execution: bool = False
    """Whether this executor actually runs skills (not just dry-run/prompt)."""

    @abstractmethod
    def invoke_skill(
        self,
        skill_id: str,
        invocation_command: str,
        input_artifacts: list[str],
        expected_output_artifact: str,
        context: dict,
    ) -> SkillExecutionResult:
        ...

    def validate_mode(self, mode: str) -> Optional[str]:
        """Return an error message if this executor cannot honestly run in the given mode."""
        if mode in ("autonomous_execution", "yolo_execution") and not self.supports_real_execution:
            return (
                f"{mode} requires a real SkillExecutor with supports_real_execution=True.\n"
                f"Current executor: {self.__class__.__name__} "
                f"(supports_real_execution={self.supports_real_execution}).\n"
                f"This mode cannot honestly execute skills yet."
            )
        return None


# ============================================================================
# Dry-Run Executor
# ============================================================================

class DryRunSkillExecutor(SkillExecutor):
    """Validates that a skill exists in the registry and logs the intended invocation.

    This is the current behavior — the skill is never actually invoked.
    The result status is PREPARED, not EXECUTED.
    """

    supports_real_execution: bool = False

    def invoke_skill(
        self,
        skill_id: str,
        invocation_command: str,
        input_artifacts: list[str],
        expected_output_artifact: str,
        context: dict,
    ) -> SkillExecutionResult:
        return SkillExecutionResult(
            skill_id=skill_id,
            status=SkillExecutionStatus.PREPARED,
            command=invocation_command,
            output_artifact=expected_output_artifact,
            message=f"Dry run: invocation of '{invocation_command}' prepared. "
                    f"Skill was NOT actually invoked.",
        )


# ============================================================================
# Prompt Chain Executor
# ============================================================================

class PromptChainSkillExecutor(SkillExecutor):
    """Generates copy-paste prompts for manual or coding-agent skill execution.

    The prompts are written to a file and returned. No actual skill invocation
    happens — the output is intended for a human or coding agent to run.
    """

    supports_real_execution: bool = False

    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def invoke_skill(
        self,
        skill_id: str,
        invocation_command: str,
        input_artifacts: list[str],
        expected_output_artifact: str,
        context: dict,
    ) -> SkillExecutionResult:
        # Build a prompt for the skill
        prompt_lines = [
            f"# Skill: {skill_id}",
            f"## Command: {invocation_command}",
            f"## Expected Output: {expected_output_artifact}",
            "",
            "### Input Context",
        ]
        for artifact in input_artifacts:
            prompt_lines.append(f"- {artifact}")
        prompt_lines.extend([
            "",
            "### Instructions",
            f"Run {invocation_command} with the context above.",
            f"Produce the output artifact at: {expected_output_artifact}",
            "",
            "---",
            f"Prompt generated by PromptChainSkillExecutor at {datetime.now().isoformat()}",
        ])
        prompt_text = "\n".join(prompt_lines)

        # Write prompt to file
        os.makedirs(self.output_dir, exist_ok=True)
        prompt_path = os.path.join(self.output_dir, f"prompt_{skill_id}.md")
        with open(prompt_path, 'w', encoding='utf-8') as f:
            f.write(prompt_text)

        return SkillExecutionResult(
            skill_id=skill_id,
            status=SkillExecutionStatus.PROMPT_GENERATED,
            command=invocation_command,
            output_artifact=expected_output_artifact,
            message=f"Prompt chain: prompt for '{invocation_command}' written to {prompt_path}. "
                    f"Skill was NOT actually invoked.",
        )


# ============================================================================
# Unsupported / Future Executors
# ============================================================================

class ClaudeAgentSdkSkillExecutor(SkillExecutor):
    """Invoke skills via Claude Agent SDK.

    Uses the Claude Agent SDK's query() API to invoke skills with autonomous
    tool use. The SDK handles skill discovery from filesystem, tool loops,
    file management, and permissions.

    The executor bridges the synchronous SkillExecutor interface to the
    async Claude Agent SDK using anyio.run().
    """

    supports_real_execution: bool = True

    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self._check_dependencies()

    def _check_dependencies(self) -> tuple[bool, str]:
        """Check if required dependencies are installed."""
        missing = []
        try:
            import anyio
        except ImportError:
            missing.append("anyio")

        try:
            from claude_agent_sdk import query, ClaudeAgentOptions
        except ImportError:
            missing.append("claude-agent-sdk")

        return len(missing) == 0, missing

    def invoke_skill(
        self,
        skill_id: str,
        invocation_command: str,
        input_artifacts: list[str],
        expected_output_artifact: str,
        context: dict,
    ) -> SkillExecutionResult:
        """Invoke a skill via Claude Agent SDK.

        Returns EXECUTED only if the expected artifact file exists after execution.
        Returns UNSUPPORTED if dependencies are missing.
        """
        deps_ok, missing_deps = self._check_dependencies()
        if not deps_ok:
            return SkillExecutionResult(
                skill_id=skill_id,
                status=SkillExecutionStatus.UNSUPPORTED,
                command=invocation_command,
                output_artifact=expected_output_artifact,
                error=f"Missing dependencies: {', '.join(missing_deps)}. "
                      f"Install with: pip install {' '.join(missing_deps)}",
            )

        # Bridge to async SDK using anyio
        try:
            import anyio
            result = anyio.run(
                self._invoke_skill_async,
                skill_id,
                invocation_command,
                input_artifacts,
                expected_output_artifact,
                context,
            )
            return result
        except Exception as e:
            return SkillExecutionResult(
                skill_id=skill_id,
                status=SkillExecutionStatus.FAILED,
                command=invocation_command,
                output_artifact=expected_output_artifact,
                error=f"Skill execution failed: {str(e)}",
            )

    async def _invoke_skill_async(
        self,
        skill_id: str,
        invocation_command: str,
        input_artifacts: list[str],
        expected_output_artifact: str,
        context: dict,
    ) -> SkillExecutionResult:
        """Async implementation of skill invocation via Claude Agent SDK."""
        from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher

        # Build prompt that instructs Claude to run the skill
        resolved_inputs = context.get("resolved_inputs", {})

        # Format input information for the prompt
        input_section = ""
        if resolved_inputs:
            input_section = "## Input Data\n"
            for input_name, input_data in resolved_inputs.items():
                if input_data["type"] == "external_context":
                    input_section += f"\n**{input_name}:**\n```\n{input_data['data']}\n```\n"
                elif input_data["type"] == "artifact_path":
                    input_section += f"\n**{input_name}** (artifact file):\n{input_data['path']}\n"
                elif input_data["type"] == "repository_state":
                    input_section += f"\n**{input_name}:**\nRepository root: {input_data['data'].get('path', '.')}\n"
            input_section += "\n"

        # Expected output path — use the runtime-resolved (session-scoped) path so
        # the artifact lands where the runtime will look for it.
        expected_output_path = resolve_output_path(self.repo_root, expected_output_artifact, context)
        relative_output_path = os.path.relpath(expected_output_path, self.repo_root)

        prompt = (
            f"You are executing the '{skill_id}' skill as part of a structured workflow.\n\n"
            f"{input_section}"
            f"## Your Task\n"
            f"Use the/{skill_id} slash command or the skill definition to produce the required output.\n\n"
            f"## Output Artifact (REQUIRED)\n"
            f"You MUST write the final artifact to this exact path:\n"
            f"```\n{relative_output_path}\n```\n\n"
            f"Use the Write tool to create this file. The artifact must be markdown format (.md) "
            f"and must match the expected output format for this skill.\n\n"
            f"Do not stop until the artifact file exists at the specified path."
        )

        # Capture SDK result and error info for diagnostic classification
        sdk_last_result_info: str | None = None

        # Runtime artifact-write confinement (issue #43): the PreToolUse hook below
        # is the authoritative enforcement point (see build_artifact_permission_gate).
        # allowed_tools is narrowed too, as defense-in-depth on top of the hook, not
        # as the enforcement mechanism itself -- can_use_tool would have been a fake
        # gate here since Write/Bash would already be pre-permitted by allowed_tools.
        artifact_permission_gate = build_artifact_permission_gate(expected_output_path)

        try:
            # Query the Claude Agent SDK
            async for message in query(
                prompt=prompt,
                options=ClaudeAgentOptions(
                    cwd=self.repo_root,
                    setting_sources=["project", "user"],
                    skills=[skill_id],
                    allowed_tools=["Read", "Write", "Glob", "Grep"],
                    hooks={
                        "PreToolUse": [
                            HookMatcher(matcher=None, hooks=[artifact_permission_gate]),
                        ],
                    },
                ),
            ):
                # Capture ResultMessage error info for classification
                if isinstance(message, ResultMessage):
                    if message.is_error:
                        errors_text = "; ".join(str(e) for e in (message.errors or []))
                        sdk_last_result_info = errors_text or str(message.subtype)

            # Check if the expected artifact was produced
            if os.path.exists(expected_output_path):
                return SkillExecutionResult(
                    skill_id=skill_id,
                    status=SkillExecutionStatus.EXECUTED,
                    command=invocation_command,
                    output_artifact=expected_output_artifact,
                    message=f"Artifact produced at {expected_output_path}",
                )
            else:
                # Build categorized error: include SDK error info if available
                category = "sdk_result_error" if sdk_last_result_info else "no_artifact"
                detail = ""
                if sdk_last_result_info:
                    detail = f" SDK reported: {sdk_last_result_info}."
                return SkillExecutionResult(
                    skill_id=skill_id,
                    status=SkillExecutionStatus.FAILED,
                    command=invocation_command,
                    output_artifact=expected_output_artifact,
                    error=f"[{category}] Expected artifact '{expected_output_artifact}' not produced.{detail} "
                          f"Artifact not found at {expected_output_path}",
                )

        except Exception as e:
            detail = ""
            if sdk_last_result_info:
                detail = f" SDK result: {sdk_last_result_info}."
            return SkillExecutionResult(
                skill_id=skill_id,
                status=SkillExecutionStatus.FAILED,
                command=invocation_command,
                output_artifact=expected_output_artifact,
                error=f"SDK execution failed: {e}.{detail}",
            )

# Keep old name as alias for backwards compatibility
ClaudeCodeSkillExecutor = ClaudeAgentSdkSkillExecutor


class ApiSkillExecutor(SkillExecutor):
    """Invoke skills by calling Claude API directly with skill instructions.

    Loads the skill definition from SKILL.md, builds a prompt with input artifacts,
    calls Claude API, and saves the output to the expected artifact path.

    Requires ANTHROPIC_API_KEY environment variable.
    """

    supports_real_execution: bool = True

    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self._check_dependencies()

    def _check_dependencies(self) -> tuple[bool, list[str]]:
        """Check if required dependencies are installed."""
        missing = []
        try:
            import anthropic
        except ImportError:
            missing.append("anthropic")

        import os
        if not os.environ.get("ANTHROPIC_API_KEY"):
            missing.append("ANTHROPIC_API_KEY environment variable")

        return len(missing) == 0, missing

    def _load_skill_content(self, skill_id: str) -> str | None:
        """Load skill definition from SKILL.md."""
        skill_path = os.path.join(self.repo_root, "skills", skill_id, "SKILL.md")
        if not os.path.exists(skill_path):
            return None
        try:
            with open(skill_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None

    def _read_artifact_content(self, artifact_path: str) -> str | None:
        """Read artifact content if it exists."""
        if not artifact_path or not os.path.exists(artifact_path):
            return None
        try:
            with open(artifact_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None

    def invoke_skill(
        self,
        skill_id: str,
        invocation_command: str,
        input_artifacts: list[str],
        expected_output_artifact: str,
        context: dict,
    ) -> SkillExecutionResult:
        """Invoke a skill via Claude API.

        Returns EXECUTED if artifact is produced and saved.
        Returns FAILED if API call fails or artifact not produced.
        Returns UNSUPPORTED if dependencies missing.
        """
        deps_ok, missing = self._check_dependencies()
        if not deps_ok:
            return SkillExecutionResult(
                skill_id=skill_id,
                status=SkillExecutionStatus.UNSUPPORTED,
                command=invocation_command,
                output_artifact=expected_output_artifact,
                error=f"Missing dependencies: {', '.join(missing)}. "
                      f"Install with: pip install anthropic",
            )

        # Load skill definition
        skill_content = self._load_skill_content(skill_id)
        if not skill_content:
            return SkillExecutionResult(
                skill_id=skill_id,
                status=SkillExecutionStatus.FAILED,
                command=invocation_command,
                output_artifact=expected_output_artifact,
                error=f"Skill '{skill_id}' not found in skills/{skill_id}/SKILL.md",
            )

        # Build prompt with skill definition and context
        prompt_parts = [
            f"You are executing the '{skill_id}' skill as part of a structured workflow.",
            "",
            "## Skill Definition",
            skill_content,
            "",
        ]

        # Add input context if available
        resolved_inputs = context.get("resolved_inputs", {})
        if resolved_inputs:
            prompt_parts.append("## Input Context")
            for input_name, input_data in resolved_inputs.items():
                if input_data.get("type") == "artifact_content":
                    prompt_parts.append(f"\n### {input_name}")
                    prompt_parts.append(f"```\n{input_data.get('content', '')}\n```")

        # Add output instruction — use the runtime-resolved (session-scoped) path.
        expected_path = resolve_output_path(self.repo_root, expected_output_artifact, context)
        relative_expected_path = os.path.relpath(expected_path, self.repo_root).replace("\\", "/")
        prompt_parts.extend([
            "",
            "## Required Output",
            f"Write the final artifact to this path (relative to repo root):",
            f"`{relative_expected_path}`",
            "",
            "Produce valid markdown that matches the expected artifact format. "
            "Include all required sections and machine-readable fields.",
        ])

        prompt = "\n".join(prompt_parts)

        try:
            from anthropic import Anthropic

            client = Anthropic()

            # Call Claude API
            message = client.messages.create(
                model="claude-opus-4-7",
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )

            artifact_content = message.content[0].text if message.content else ""

            # Try to extract markdown artifact from response
            # Claude might wrap it in code blocks or explain it
            import re
            match = re.search(r"^#\s+", artifact_content, re.MULTILINE)
            if match:
                # Response starts with markdown heading, use as-is
                artifact_text = artifact_content
            elif "```markdown" in artifact_content:
                # Response has code block, extract it
                m = re.search(r"```markdown\n(.*?)\n```", artifact_content, re.DOTALL)
                artifact_text = m.group(1) if m else artifact_content
            else:
                artifact_text = artifact_content

            # Create artifacts directory if needed
            os.makedirs(os.path.dirname(expected_path), exist_ok=True)

            # Write artifact to expected path
            with open(expected_path, "w", encoding="utf-8") as f:
                f.write(artifact_text)

            # Verify artifact was created
            if os.path.exists(expected_path):
                return SkillExecutionResult(
                    skill_id=skill_id,
                    status=SkillExecutionStatus.EXECUTED,
                    command=invocation_command,
                    output_artifact=expected_output_artifact,
                    message=f"Artifact produced at {expected_path} via Claude API",
                )
            else:
                return SkillExecutionResult(
                    skill_id=skill_id,
                    status=SkillExecutionStatus.FAILED,
                    command=invocation_command,
                    output_artifact=expected_output_artifact,
                    error=f"Artifact file not created at {expected_path}",
                )

        except Exception as e:
            return SkillExecutionResult(
                skill_id=skill_id,
                status=SkillExecutionStatus.FAILED,
                command=invocation_command,
                output_artifact=expected_output_artifact,
                error=f"API execution failed: {str(e)}",
            )


# ============================================================================
# Factory
# ============================================================================

EXECUTOR_REGISTRY = {
    "dry-run": DryRunSkillExecutor,
    "prompt-chain": PromptChainSkillExecutor,
    "claude-code": ClaudeCodeSkillExecutor,
    "api": ApiSkillExecutor,
}


def create_executor(
    executor_id: str,
    repo_root: str,
    prompt_output_dir: Optional[str] = None,
) -> SkillExecutor:
    """Create a SkillExecutor instance by id.

    Args:
        executor_id: One of "dry-run", "prompt-chain", "claude-code", "api".
        repo_root: Repository root path.
        prompt_output_dir: Directory for prompt files (prompt-chain only).

    Returns:
        A SkillExecutor instance.

    Raises:
        ValueError: If executor_id is unknown.
    """
    if executor_id not in EXECUTOR_REGISTRY:
        known = ", ".join(EXECUTOR_REGISTRY.keys())
        raise ValueError(f"Unknown executor '{executor_id}'. Known: {known}")

    executor_cls = EXECUTOR_REGISTRY[executor_id]

    if executor_id == "prompt-chain":
        output_dir = prompt_output_dir or os.path.join(repo_root, "prompts")
        return executor_cls(output_dir=output_dir)

    if executor_id in ("claude-code", "api"):
        return executor_cls(repo_root=repo_root)

    return executor_cls()
