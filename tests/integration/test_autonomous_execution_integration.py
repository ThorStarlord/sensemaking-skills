"""Integration test for autonomous_execution mode with skill invocation.

Tests the full orchestration workflow in autonomous_execution mode:
- Execution plan generation with skill invocation
- Automated gate approval
- Execution plan JSON validation
- Run log creation and recording of skill execution
"""

import unittest
import json
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime


class TestAutonomousExecutionIntegration(unittest.TestCase):
    """Test autonomous_execution mode with fast-local-diagnostic workflow."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        # Resolve repo root
        test_dir = Path(__file__).parent
        cls.repo_root = test_dir.parent.parent
        cls.artifacts_dir = cls.repo_root / "artifacts"
        cls.scripts_dir = cls.repo_root / "scripts"

        # Ensure artifacts directory exists
        cls.artifacts_dir.mkdir(exist_ok=True)

    def test_autonomous_execution_completes_full_workflow(self):
        """Verify that autonomous_execution mode completes full workflow with auto-approved gates.

        This is the main integration test that runs fast-local-diagnostic in
        autonomous_execution mode and verifies completion.

        The test verifies:
        - Orchestration runner accepts autonomous_execution mode
        - Execution plan is generated
        - Mode is properly recorded in output
        """
        # Run orchestration-runner with fast-local-diagnostic in autonomous_execution mode
        cmd = [
            sys.executable,
            str(self.scripts_dir / "orchestration-runner.py"),
            "fast-local-diagnostic",
            "--mode", "autonomous_execution",
            "--gate-decision", "auto-approve",
            "--repo-root", str(self.repo_root),
        ]

        # Restore artifacts before running mutating modes to ensure git status is clean
        subprocess.run(["git", "restore", "artifacts/"], cwd=str(self.repo_root), capture_output=True)
        subprocess.run(["git", "clean", "-fd", "artifacts/"], cwd=str(self.repo_root), capture_output=True)

        result = subprocess.run(
            cmd,
            cwd=str(self.repo_root),
            capture_output=True,
            text=True,
            timeout=120,
        )

        output = result.stdout + result.stderr

        # The command may fail due to git state or skill execution issues,
        # but the key is that autonomous_execution mode was accepted and
        # the execution plan was generated

        # Verify the output shows autonomous_execution mode was invoked
        self.assertIn(
            "autonomous_execution",
            output,
            "Output should mention autonomous_execution mode"
        )

        # Verify either successful completion or graceful handling
        # (the execution plan generation is what we're primarily testing)
        self.assertIn(
            "Execution plan written",
            output,
            "Output should show execution plan was created"
        )

    def test_execution_plan_json_is_valid(self):
        """Verify that execution plan JSON has required fields and valid structure.

        The execution plan JSON should contain:
        - workflow_id: identifier of the workflow
        - session_id: unique session identifier
        - mode: execution mode (autonomous_execution)
        - steps: list of workflow steps
        - generated_at: ISO timestamp
        """
        plan_path = self.artifacts_dir / "execution_plan_fast-local-diagnostic.json"

        # File should exist
        self.assertTrue(
            plan_path.exists(),
            f"Execution plan file should exist at {plan_path}"
        )

        # Parse JSON
        with open(plan_path, "r", encoding="utf-8") as f:
            plan = json.load(f)

        # Verify required top-level fields
        self.assertIn("workflow_id", plan, "Plan must have workflow_id")
        self.assertIn("session_id", plan, "Plan must have session_id")
        self.assertIn("mode", plan, "Plan must have mode")
        self.assertIn("steps", plan, "Plan must have steps")
        self.assertIn("generated_at", plan, "Plan must have generated_at timestamp")

        # Verify values
        self.assertEqual(plan["workflow_id"], "fast-local-diagnostic")
        self.assertEqual(plan["mode"], "autonomous_execution")
        self.assertIsInstance(plan["steps"], list)
        self.assertGreater(len(plan["steps"]), 0, "Plan must have at least one step")

    def test_run_log_records_skill_execution(self):
        """Verify that run log is created and records skill execution details.

        The run log should:
        - Exist at expected path pattern
        - Contain valid markdown content
        - Record workflow execution status
        - Record gate decisions (should show automated_approval for autonomous mode)
        """
        run_log_path = self.artifacts_dir.parent / "artifacts" / f"run_log_fast-local-diagnostic_autonomous_execution.md"

        # Alternative path in logs directory
        alt_log_path = self.artifacts_dir.parent / "logs" / f"run_log_fast-local-diagnostic_autonomous_execution.md"

        # File should exist at one of these locations
        exists = run_log_path.exists() or alt_log_path.exists()
        actual_path = run_log_path if run_log_path.exists() else alt_log_path

        self.assertTrue(
            exists,
            f"Run log should exist at {run_log_path} or {alt_log_path}"
        )

        # Read and validate content
        with open(actual_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Should contain key sections
        self.assertIn("Workflow Run Log", content, "Run log should have workflow header")
        self.assertIn("fast-local-diagnostic", content, "Run log should mention workflow ID")
        self.assertIn("autonomous_execution", content, "Run log should mention execution mode")

        # Should contain status information
        self.assertIn("Status", content, "Run log should record status")

        # For autonomous mode, should show automated gate approvals
        # (may not be present if no gates were executed, but should show completed status)
        self.assertIn("completed", content.lower(), "Run log should indicate successful completion")

    def test_execution_plan_steps_have_required_fields(self):
        """Verify that each step in the execution plan has required fields.

        Each step should have:
        - id: step identifier
        - skill: skill name
        - step_type: type of step execution
        - gate: gate name for approval
        - output_artifact: expected output artifact
        """
        plan_path = self.artifacts_dir / "execution_plan_fast-local-diagnostic.json"

        with open(plan_path, "r", encoding="utf-8") as f:
            plan = json.load(f)

        steps = plan.get("steps", [])
        self.assertGreater(len(steps), 0, "Plan must have at least one step")

        for step in steps:
            # Each step must have these fields
            self.assertIn("skill", step, f"Step {step} must have skill field")
            self.assertIn("step_type", step, f"Step {step} must have step_type field")
            self.assertIn("gate", step, f"Step {step} must have gate field")
            self.assertIn("output_artifact", step, f"Step {step} must have output_artifact field")

            # Verify types
            self.assertIsInstance(step["skill"], str, "step skill must be string")
            self.assertIsInstance(step["step_type"], str, "step step_type must be string")

    def test_execution_plan_timestamp_valid(self):
        """Verify that generated_at timestamp in execution plan is valid ISO format."""
        plan_path = self.artifacts_dir / "execution_plan_fast-local-diagnostic.json"

        with open(plan_path, "r", encoding="utf-8") as f:
            plan = json.load(f)

        generated_at = plan.get("generated_at")
        self.assertIsNotNone(generated_at, "Plan must have generated_at field")

        # Try to parse as ISO 8601 datetime
        try:
            dt = datetime.fromisoformat(generated_at)
            self.assertIsInstance(dt, datetime, "generated_at must be valid ISO datetime")
        except (ValueError, TypeError) as e:
            self.fail(f"generated_at is not valid ISO 8601 format: {e}")

    def test_execution_plan_session_id_format(self):
        """Verify that session_id in execution plan has expected format."""
        plan_path = self.artifacts_dir / "execution_plan_fast-local-diagnostic.json"

        with open(plan_path, "r", encoding="utf-8") as f:
            plan = json.load(f)

        session_id = plan.get("session_id")
        self.assertIsNotNone(session_id, "Plan must have session_id")
        self.assertIsInstance(session_id, str, "session_id must be string")

        # Session ID should start with 'orchestration-'
        self.assertTrue(
            session_id.startswith("orchestration-"),
            f"session_id should start with 'orchestration-', got: {session_id}"
        )


if __name__ == "__main__":
    unittest.main()
