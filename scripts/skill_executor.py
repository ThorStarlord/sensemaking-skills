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

    def to_dict(self) -> dict:
        return {
            "skill_id": self.skill_id,
            "status": self.status.value,
            "command": self.command,
            "timestamp": self.timestamp,
            "output_artifact": self.output_artifact,
            "message": self.message,
            "error": self.error,
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

class ClaudeCodeSkillExecutor(SkillExecutor):
    """Future: invoke skills via Claude Code slash-command or SDK.

    Not yet implemented. Returns UNSUPPORTED if selected.
    """

    supports_real_execution: bool = True

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
            status=SkillExecutionStatus.UNSUPPORTED,
            command=invocation_command,
            output_artifact=expected_output_artifact,
            error=(
                f"ClaudeCodeSkillExecutor is declared but not implemented. "
                f"Cannot invoke '{invocation_command}' for skill '{skill_id}'."
            ),
        )


class ApiSkillExecutor(SkillExecutor):
    """Future: invoke skills by calling an LLM API directly with skill instructions.

    Not yet implemented. Returns UNSUPPORTED if selected.
    """

    supports_real_execution: bool = True

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
            status=SkillExecutionStatus.UNSUPPORTED,
            command=invocation_command,
            output_artifact=expected_output_artifact,
            error=(
                f"ApiSkillExecutor is declared but not implemented. "
                f"Cannot invoke '{invocation_command}' for skill '{skill_id}'."
            ),
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

    return executor_cls()
