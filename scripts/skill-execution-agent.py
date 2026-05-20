"""
Skill Execution Agent: Reads orchestration plans and invokes skills via a SkillExecutor.

Usage:
    python scripts/skill-execution-agent.py <plan_json_path> --repo-root <root>
    python scripts/skill-execution-agent.py <plan_json_path> --repo-root <root> --executor prompt-chain
"""

import os
import sys
import json
import argparse
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Tuple

from _validator_utils import format_error, load_yaml, resolve_repo_root
from skill_executor import (
    SkillExecutor,
    SkillExecutionResult,
    SkillExecutionStatus,
    create_executor,
)

# ============================================================================
# Error Codes
# ============================================================================
SKILL_NOT_FOUND = "SKILL_NOT_FOUND"
SKILL_INVOCATION_FAILED = "SKILL_INVOCATION_FAILED"
PLAN_LOAD_FAILED = "PLAN_LOAD_FAILED"
ARTIFACT_VERIFICATION_FAILED = "ARTIFACT_VERIFICATION_FAILED"
EXECUTION_TIMEOUT = "EXECUTION_TIMEOUT"
INVALID_PLAN_FORMAT = "INVALID_PLAN_FORMAT"
EXECUTOR_BLOCKED = "EXECUTOR_BLOCKED"


def load_orchestration_plan(plan_path: str) -> Tuple[bool, dict, str]:
    """Load and validate an orchestration plan JSON file."""
    if not os.path.exists(plan_path):
        return False, {}, format_error(PLAN_LOAD_FAILED, f"Plan file not found: {plan_path}")

    try:
        with open(plan_path, 'r', encoding='utf-8') as f:
            plan_data = json.load(f)
    except json.JSONDecodeError as e:
        return False, {}, format_error(INVALID_PLAN_FORMAT, f"Invalid JSON: {str(e)}")

    if "workflow_id" not in plan_data:
        return False, {}, format_error(INVALID_PLAN_FORMAT, "Plan missing 'workflow_id'")
    if "steps" not in plan_data or not isinstance(plan_data["steps"], list):
        return False, {}, format_error(INVALID_PLAN_FORMAT, "Plan missing 'steps' array")

    return True, plan_data, ""


def get_skill_invocation_command(skill_id: str, repo_root: str) -> Optional[str]:
    """Get the invocation command for a skill from the skill registry."""
    skill_registry_path = os.path.join(repo_root, "skills", "workflow-planner", "references", "skill-registry.yaml")
    if not os.path.exists(skill_registry_path):
        return None

    registry = load_yaml(skill_registry_path)
    if not registry:
        return None

    for ecosystem_name, ecosystem_data in registry.get("ecosystems", {}).items():
        for skill in ecosystem_data.get("skills", []):
            if skill.get("id") == skill_id:
                invocation = skill.get("invocation", {})
                if invocation.get("runtime") == "claude_code":
                    return invocation.get("command")

    return None


class SkillExecutionAgent:
    """Manages sequential skill execution using a pluggable SkillExecutor."""

    def __init__(self, plan_data: dict, repo_root: str, executor: SkillExecutor):
        self.plan_data = plan_data
        self.repo_root = os.path.abspath(repo_root)
        self.executor = executor
        self.workflow_id = plan_data.get("workflow_id", "unknown")
        self.session_id = plan_data.get("session_id", "unknown")
        self.execution_log: list[SkillExecutionResult] = []
        self.failed = False
        self.error_messages = []

    def execute(self, timeout_per_skill: int = 600) -> Tuple[bool, str]:
        """Execute all steps in the plan sequentially using the configured executor.

        Returns (success: bool, summary_message: str)
        """
        steps = self.plan_data.get("steps", [])
        if not steps:
            return False, "Plan has no steps to execute"

        step_count = 0
        failures = 0

        for i, step in enumerate(steps, start=1):
            step_id = step.get("step_id", i)
            skill_id = step.get("skill")

            # Get the skill invocation command
            command = get_skill_invocation_command(skill_id, self.repo_root)
            if not command:
                msg = format_error(SKILL_NOT_FOUND, f"Step {step_id}: Skill '{skill_id}' not in registry")
                self.execution_log.append(
                    SkillExecutionResult(
                        skill_id=skill_id or "?",
                        status=SkillExecutionStatus.FAILED,
                        command="?",
                        error=msg,
                    )
                )
                self.error_messages.append(msg)
                self.failed = True
                failures += 1
                continue

            # Gather input artifacts
            input_artifacts = []
            if step.get("input_artifact"):
                input_artifacts.append(step["input_artifact"])
            if step.get("input_source"):
                input_artifacts.append(step["input_source"])

            # Invoke the skill via the configured executor
            result = self.executor.invoke_skill(
                skill_id=skill_id,
                invocation_command=command,
                input_artifacts=input_artifacts,
                expected_output_artifact=step.get("output_artifact", ""),
                context={
                    "step_id": step_id,
                    "gate": step.get("gate"),
                    "input_artifact": step.get("input_artifact"),
                    "input_source": step.get("input_source"),
                    "output_artifact": step.get("output_artifact"),
                    "step_type": step.get("step_type", "local_execution"),
                },
            )

            self.execution_log.append(result)

            if result.status == SkillExecutionStatus.FAILED:
                self.error_messages.append(f"Step {step_id}: {result.error}")
                self.failed = True
                failures += 1
            elif result.status == SkillExecutionStatus.UNSUPPORTED:
                self.error_messages.append(f"Step {step_id}: {result.error}")
                self.failed = True
                failures += 1

            step_count += 1

        # Build summary
        if self.failed:
            summary = (
                f"Execution failed with {len(self.error_messages)} errors "
                f"after {step_count} steps. "
                f"Last executor: {self.executor.__class__.__name__} "
                f"(supports_real_execution={self.executor.supports_real_execution})."
            )
            return False, summary

        executor_name = self.executor.__class__.__name__
        summary = (
            f"All {step_count} steps completed via {executor_name}. "
            f"supports_real_execution={self.executor.supports_real_execution}. "
            f"No skills were actually invoked."
        )
        return True, summary


def main():
    parser = argparse.ArgumentParser(description="Execute skills from an orchestration plan")
    parser.add_argument("plan_path", help="Path to orchestration plan JSON")
    parser.add_argument("--repo-root", default=".", help="Repository root directory")
    parser.add_argument("--timeout", type=int, default=600, help="Timeout per skill in seconds")
    parser.add_argument(
        "--executor",
        default="dry-run",
        choices=["dry-run", "prompt-chain", "claude-code", "api"],
        help="Skill executor to use (default: dry-run)",
    )
    parser.add_argument(
        "--prompt-dir",
        default=None,
        help="Output directory for prompt files (prompt-chain executor only)",
    )

    args = parser.parse_args()
    repo_root = resolve_repo_root(args.repo_root)

    # Load plan
    success, plan_data, error_msg = load_orchestration_plan(args.plan_path)
    if not success:
        print(error_msg)
        sys.exit(1)

    # Create executor
    try:
        executor = create_executor(
            args.executor,
            repo_root,
            prompt_output_dir=args.prompt_dir,
        )
    except ValueError as e:
        print(str(e))
        sys.exit(1)

    # Validate executor against mode (if mode is in plan data)
    mode = plan_data.get("mode", "plan_only")
    validation_error = executor.validate_mode(mode)
    if validation_error:
        error_msg = format_error(EXECUTOR_BLOCKED, validation_error)
        print(error_msg)
        sys.exit(1)

    # Execute plan
    agent = SkillExecutionAgent(plan_data, repo_root, executor)
    success, summary = agent.execute(timeout_per_skill=args.timeout)

    print(f"\n{'='*60}")
    print(f"SKILL EXECUTION COMPLETE")
    print(f"Workflow: {agent.workflow_id}")
    print(f"Session: {agent.session_id}")
    print(f"Executor: {args.executor} ({executor.__class__.__name__})")
    print(f"Result: {summary}")
    print(f"{'='*60}\n")

    # Print step results
    for i, result in enumerate(agent.execution_log, 1):
        print(f"  Step {i}: {result.skill_id} -> {result.status.value}")
        if result.message:
            print(f"    {result.message}")
        if result.error:
            print(f"    ERROR: {result.error}")

    if not success:
        for err in agent.error_messages:
            print(err)
        sys.exit(1)


if __name__ == "__main__":
    main()
