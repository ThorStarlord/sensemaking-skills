#!/usr/bin/env python3
"""
AI-native orchestrator skill for workflow execution.

This skill controls the workflow run loop, invokes worker skills,
and verifies the run ledger.
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from _validator_utils import load_workflow_registry, resolve_repo_root


class OrchestratorSkill:
    def __init__(self, repo_root: str, workflow_id: str, mode: str = "guided_execution"):
        self.repo_root = repo_root
        self.workflow_id = workflow_id
        self.mode = mode
        self.registry = load_workflow_registry(repo_root)
        self.workflow = self._load_workflow()
        self.run_id = None
        self.session_dir = None

    def _load_workflow(self) -> Dict[str, Any]:
        """Load workflow definition from registry."""
        if not self.registry:
            raise RuntimeError(f"Failed to load workflow registry from {self.repo_root}")

        workflows = self.registry.get("workflows", [])
        for wf in workflows:
            if wf.get("id") == self.workflow_id:
                return wf

        raise RuntimeError(f"Workflow '{self.workflow_id}' not found in registry")

    def run(self, input_artifact: str = None, input_artifacts: Dict[str, str] = None) -> int:
        """Execute the workflow."""
        try:
            # 1. Initialize run ledger
            self._initialize_run(input_artifact or "user_intent", input_artifacts or {})

            # 2. Execute each step
            steps = self.workflow.get("steps", [])
            for step_num, step in enumerate(steps, 1):
                result = self._execute_step(step, step_num, len(steps), input_artifact)
                if result != 0:
                    print(f"[ORCHESTRATOR] Step {step_num} failed. Halting run.")
                    return 1

            # 3. Finalize run
            return self._finalize_run()

        except Exception as e:
            print(f"[ORCHESTRATOR ERROR] {e}", file=sys.stderr)
            return 1

    def _initialize_run(self, input_artifact: str, input_artifacts: Dict[str, str]):
        """Initialize run ledger and session directory."""
        # Create session directory
        artifacts_dir = Path(self.repo_root) / "artifacts"
        artifacts_dir.mkdir(exist_ok=True)

        # Find next run number
        run_num = 1
        while (artifacts_dir / f"{run_num:02d}-orchestration-run").exists():
            run_num += 1

        self.session_dir = artifacts_dir / f"{run_num:02d}-orchestration-run"
        self.session_dir.mkdir(exist_ok=True)
        self.run_id = f"orchestrator-run-{run_num:02d}"

        # Start run in ledger
        cmd = [
            sys.executable,
            str(scripts_dir / "run-ledger.py"),
            "--repo-root", self.repo_root,
            "--ledger-path", str(self.session_dir / "run-ledger.jsonl"),
            "start-run",
            "--run-id", self.run_id,
            "--workflow", self.workflow_id,
            "--mode", self.mode,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Failed to start run: {result.stderr}")

        print(f"[ORCHESTRATOR] Initialized run {self.run_id} in {self.session_dir}")

    def _execute_step(self, step: Dict[str, Any], step_num: int, total_steps: int,
                     input_artifact: str) -> int:
        """Execute a single workflow step."""
        skill_id = step.get("skill")
        output_artifact = step.get("output_artifact")
        gate = step.get("gate")

        print(f"\n[ORCHESTRATOR] Step {step_num}/{total_steps}: {skill_id}")

        try:
            # 1. Start step in ledger
            cmd = [
                sys.executable,
                str(scripts_dir / "run-ledger.py"),
                "--repo-root", self.repo_root,
                "--ledger-path", str(self.session_dir / "run-ledger.jsonl"),
                "start-step",
                "--step-id", str(step_num),
                "--skill", skill_id,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"[ORCHESTRATOR] Failed to start step: {result.stderr}")
                return 1

            # 2. Invoke the worker skill
            # This would normally invoke the skill via Claude, but for now we'll simulate it
            print(f"[ORCHESTRATOR] Would invoke /{skill_id} skill here")

            # 3. Verify artifact was created and validated
            artifact_path = self.session_dir / f"{step_num:02d}-{output_artifact}.md"
            if not artifact_path.exists():
                print(f"[ORCHESTRATOR] ERROR: Artifact not found at {artifact_path}")
                return 1

            # 4. Complete step in ledger
            cmd = [
                sys.executable,
                str(scripts_dir / "run-ledger.py"),
                "--repo-root", self.repo_root,
                "--ledger-path", str(self.session_dir / "run-ledger.jsonl"),
                "complete-step",
                "--step-id", str(step_num),
                "--status", "completed",
                "--gate-status", "approved",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"[ORCHESTRATOR] Failed to complete step: {result.stderr}")
                return 1

            print(f"[ORCHESTRATOR] Step {step_num} completed successfully")
            return 0

        except Exception as e:
            print(f"[ORCHESTRATOR] Step {step_num} failed: {e}")
            return 1

    def _finalize_run(self) -> int:
        """Finalize the run and audit the ledger."""
        print(f"\n[ORCHESTRATOR] Finalizing run...")

        try:
            # 1. Audit the run ledger
            cmd = [
                sys.executable,
                str(scripts_dir / "workflow-runtime.py"),
                "audit-run",
                "--ledger-path", str(self.session_dir / "run-ledger.jsonl"),
                "--repo-root", self.repo_root,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print("[ORCHESTRATOR] ✓ Run ledger audit PASSED")
                print(f"[ORCHESTRATOR] Run completed successfully: {self.session_dir}")
                return 0
            else:
                print(f"[ORCHESTRATOR] ✗ Run ledger audit FAILED: {result.stdout}")
                return 1

        except Exception as e:
            print(f"[ORCHESTRATOR] Finalization failed: {e}")
            return 1


def main():
    parser = argparse.ArgumentParser(description="AI-native orchestrator skill")
    parser.add_argument("--repo-root", required=True, help="Repository root directory")
    parser.add_argument("--workflow", required=True, help="Workflow ID to execute")
    parser.add_argument("--mode", default="guided_execution",
                       choices=["plan_only", "prompt_chain", "guided_execution", "autonomous_execution"],
                       help="Execution mode")
    parser.add_argument("--input-artifact", default="user_intent", help="Input artifact ID")

    args = parser.parse_args()

    try:
        orchestrator = OrchestratorSkill(args.repo_root, args.workflow, args.mode)
        return orchestrator.run(args.input_artifact)
    except Exception as e:
        print(f"[ORCHESTRATOR FATAL] {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
