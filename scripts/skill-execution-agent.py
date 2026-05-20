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

from _validator_utils import (
    format_error,
    load_yaml,
    resolve_repo_root,
    load_artifact_contracts,
)
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

    def _run_validators(self, artifact_id: str, artifact_path: str) -> Tuple[bool, List[dict]]:
        """Run validators on an artifact. Returns (all_passed, validator_results)."""
        if not os.path.exists(artifact_path):
            return False, [{"name": "file_exists", "result": "FAILED", "reason": "Artifact file not found"}]

        # Load artifact contracts
        contracts = load_artifact_contracts(self.repo_root)
        if not contracts:
            return False, [{"name": "contracts_load", "result": "FAILED", "reason": "Could not load artifact contracts"}]

        # Find contract for this artifact
        artifact_contract = None
        for artifact in contracts.get("artifacts", []):
            if artifact.get("id") == artifact_id:
                artifact_contract = artifact
                break

        if not artifact_contract:
            return True, [{"name": "contract_lookup", "result": "SKIPPED", "reason": f"No contract found for {artifact_id}"}]

        # Get validation commands
        verification = artifact_contract.get("verification", {})
        if not verification:
            return True, [{"name": "verification", "result": "SKIPPED", "reason": "No verification defined"}]

        validator_results = []
        all_passed = True

        # Run generic validator
        generic_cmd = verification.get("generic_validator")
        if generic_cmd:
            cmd = generic_cmd.format(artifact_path=artifact_path)
            try:
                exit_code = os.system(cmd + " > /dev/null 2>&1")
                result = "PASSED" if exit_code == 0 else "FAILED"
                if result == "FAILED":
                    all_passed = False
                validator_results.append({
                    "name": "generic_validator",
                    "command": generic_cmd,
                    "result": result,
                    "exit_code": exit_code,
                })
            except Exception as e:
                validator_results.append({
                    "name": "generic_validator",
                    "command": generic_cmd,
                    "result": "FAILED",
                    "error": str(e),
                })
                all_passed = False

        # Run specialized validators
        for spec_cmd in verification.get("specialized_validators", []):
            cmd = spec_cmd.format(artifact_path=artifact_path)
            try:
                exit_code = os.system(cmd + " > /dev/null 2>&1")
                result = "PASSED" if exit_code == 0 else "FAILED"
                if result == "FAILED":
                    all_passed = False
                validator_results.append({
                    "name": spec_cmd.split("/")[-1].replace(".py", ""),
                    "command": spec_cmd,
                    "result": result,
                    "exit_code": exit_code,
                })
            except Exception as e:
                validator_results.append({
                    "name": spec_cmd.split("/")[-1].replace(".py", ""),
                    "command": spec_cmd,
                    "result": "FAILED",
                    "error": str(e),
                })
                all_passed = False

        return all_passed, validator_results

    def _resolve_step_inputs(self, step: dict, step_index: int) -> dict:
        """Resolve a step's input_source/input_artifact into actual values/paths.

        Returns a dict of resolved inputs.
        """
        resolved = {}
        external_context = self.plan_data.get("external_context", {})

        # Resolve input_artifact (produced by previous step)
        if step.get("input_artifact"):
            artifact_name = step["input_artifact"]
            # For now, assume artifacts are in artifacts/ directory
            artifact_path = os.path.join(self.repo_root, "artifacts", f"{artifact_name}.md")
            resolved[artifact_name] = {
                "type": "artifact_path",
                "path": artifact_path,
            }

        # Resolve input_source (external context or repository)
        if step.get("input_source"):
            source_name = step["input_source"]
            if source_name in external_context:
                source_data = external_context[source_name]
                resolved[source_name] = {
                    "type": "external_context",
                    "data": source_data,
                }
            else:
                # Assume it's repository_state
                resolved[source_name] = {
                    "type": "repository_state",
                    "data": {
                        "type": "repo_root",
                        "path": self.repo_root,
                    },
                }

        return resolved

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

            # Resolve step inputs
            resolved_inputs = self._resolve_step_inputs(step, i)

            # Gather input artifacts (for backward compatibility)
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
                    "resolved_inputs": resolved_inputs,
                },
            )

            self.execution_log.append(result)

            # If skill execution succeeded and artifact exists, run validators
            if result.status == SkillExecutionStatus.EXECUTED and result.output_artifact:
                artifact_path = os.path.join(self.repo_root, "artifacts", f"{result.output_artifact}.md")
                if os.path.exists(artifact_path):
                    validation_passed, validator_results = self._run_validators(
                        result.output_artifact,
                        artifact_path
                    )

                    # Store validator results in the execution result
                    result.validator_results = validator_results
                    result.validation_passed = validation_passed

                    # Update status based on validation
                    if not validation_passed:
                        result.status = SkillExecutionStatus.FAILED
                        result.error = f"Artifact validation failed: {len([v for v in validator_results if v.get('result') == 'FAILED'])} validator(s) failed"
                        self.error_messages.append(f"Step {step_id}: Artifact validation failed")
                        self.failed = True
                        failures += 1
                    else:
                        result.status = SkillExecutionStatus.EXECUTED  # Mark as fully executed and validated

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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = resolve_repo_root(args.repo_root, script_dir)

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
        if hasattr(result, 'validator_results') and result.validator_results:
            print(f"    Validators:")
            for v in result.validator_results:
                v_result = v.get('result', 'UNKNOWN')
                v_name = v.get('name', 'unknown')
                print(f"      - {v_name}: {v_result}")
        if result.error:
            print(f"    ERROR: {result.error}")

    # Output structured results as JSON for orchestrator parsing
    results = {
        "success": success,
        "workflow_id": agent.workflow_id,
        "session_id": agent.session_id,
        "executor": args.executor,
        "step_results": [
            {
                "skill": r.skill_id,
                "status": r.status.value,
                "output_artifact": r.output_artifact,
                "message": r.message,
                "error": r.error,
                "validation_passed": r.validation_passed,
                "validator_results": r.validator_results,
            }
            for r in agent.execution_log
        ],
        "errors": agent.error_messages,
    }

    # Output JSON to stdout (can be parsed by orchestrator)
    print(f"\n{json.dumps(results, indent=2)}")

    if not success:
        for err in agent.error_messages:
            print(err, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
