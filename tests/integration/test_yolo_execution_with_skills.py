"""Integration test for yolo_execution mode with skill invocation.

Tests the full orchestration workflow: plan generation, skill execution dispatch,
execution plan creation, and verification that the orchestration pipeline produces
expected artifacts and execution plans.
"""

import unittest
import json
import sys
import os
import subprocess
import shutil
from pathlib import Path
from datetime import datetime


class TestYoloExecutionWithSkills(unittest.TestCase):
    """Test yolo_execution mode with fast-local-diagnostic workflow."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures by running the workflow in yolo_execution mode once."""
        # Resolve repo root
        test_dir = Path(__file__).parent
        cls.repo_root = test_dir.parent.parent
        cls.artifacts_dir = cls.repo_root / "artifacts"
        cls.scripts_dir = cls.repo_root / "scripts"

        # Clean artifacts dir of stale runs
        shutil.rmtree(cls.artifacts_dir, ignore_errors=True)
        cls.artifacts_dir.mkdir(exist_ok=True)

        # Set environment for yolo execution
        os.environ["SENSEMAKING_EXECUTION_MODE"] = "yolo"

        cmd = [
            sys.executable,
            str(cls.scripts_dir / "workflow-runtime.py"),
            "--workflow", "fast-local-diagnostic",
            "--mode", "yolo_execution",
            "--executor", "dry-run",
            "--use-fixtures",
        ]

        cls.result = subprocess.run(
            cmd,
            cwd=str(cls.repo_root),
            capture_output=True,
            text=True,
            timeout=60,
        )

        cls.output = cls.result.stdout + cls.result.stderr

        # Locate the session directory
        session_dirs = [d for d in cls.artifacts_dir.iterdir() if d.is_dir() and d.name.endswith("-orchestration-run")]
        if session_dirs:
            cls.session_dir = session_dirs[0]
            cls.summary_path = cls.session_dir / "workflow_summary.json"
        else:
            cls.session_dir = None
            cls.summary_path = None

    def test_execution_plan_created_by_yolo_mode(self):
        """Verify that yolo_execution mode creates a plan and summary."""
        self.assertIsNotNone(self.session_dir, "Session directory should have been created")
        self.assertEqual(self.result.returncode, 0, f"Runtime execution failed: {self.output}")

        # Verify the output mentions plan and summary paths
        self.assertIn(
            "Plan written to",
            self.output,
            "Output should mention plan was written"
        )
        self.assertIn(
            "workflow_summary.json",
            self.output,
            "Output should mention workflow summary JSON"
        )

    def test_execution_plan_json_valid_format(self):
        """Verify that workflow summary JSON has required fields and valid structure."""
        self.assertIsNotNone(self.summary_path, "Summary path should be set")
        self.assertTrue(
            self.summary_path.exists(),
            f"Execution summary file should exist at {self.summary_path}"
        )

        # Parse JSON
        with open(self.summary_path, "r", encoding="utf-8") as f:
            plan = json.load(f)

        # Verify required top-level fields
        self.assertIn("workflow_id", plan, "Plan must have workflow_id")
        self.assertIn("session_id", plan, "Plan must have session_id")
        self.assertIn("mode", plan, "Plan must have mode")
        self.assertIn("steps", plan, "Plan must have steps")
        self.assertIn("executed_at", plan, "Plan must have executed_at timestamp")

        # Verify values
        self.assertEqual(plan["workflow_id"], "fast-local-diagnostic")
        self.assertEqual(plan["mode"], "yolo_execution")
        self.assertIsInstance(plan["steps"], list)
        self.assertGreater(len(plan["steps"]), 0, "Plan must have at least one step")

    def test_execution_plan_steps_have_required_fields(self):
        """Verify that each step in the workflow summary has required fields."""
        self.assertIsNotNone(self.summary_path)
        with open(self.summary_path, "r", encoding="utf-8") as f:
            plan = json.load(f)

        steps = plan.get("steps", [])
        self.assertGreater(len(steps), 0, "Plan must have at least one step")

        for step in steps:
            # Each step must have these fields
            self.assertIn("step_id", step, f"Step {step} must have step_id field")
            self.assertIn("skill", step, f"Step {step} must have skill field")
            self.assertIn("status", step, f"Step {step} must have status field")
            self.assertIn("output_artifact", step, f"Step {step} must have output_artifact field")

            # Verify types
            self.assertIsInstance(step["step_id"], str, "step id must be string")
            self.assertIsInstance(step["skill"], str, "step skill must be string")

    def test_fast_local_diagnostic_workflow_registered(self):
        """Verify that fast-local-diagnostic workflow is properly registered."""
        registry_path = (
            self.repo_root / "skills" / "workflow-planner" /
            "references" / "workflow-registry.yaml"
        )

        self.assertTrue(
            registry_path.exists(),
            f"Workflow registry should exist at {registry_path}"
        )

        # Read and check for fast-local-diagnostic
        with open(registry_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn(
            "fast-local-diagnostic",
            content,
            "Workflow registry must contain fast-local-diagnostic"
        )
        self.assertIn(
            "yolo_execution",
            content,
            "fast-local-diagnostic must have yolo_execution in allowed_execution_modes"
        )

    def test_orchestration_runner_callable(self):
        """Verify that workflow-runtime.py is callable and lists workflows."""
        cmd = [
            sys.executable,
            str(self.scripts_dir / "workflow-runtime.py"),
            "--list-workflows",
        ]

        result = subprocess.run(
            cmd,
            cwd=str(self.repo_root),
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Should succeed
        self.assertEqual(
            result.returncode,
            0,
            f"workflow-runtime.py --list-workflows should succeed, got: {result.stderr}"
        )

        # Should list fast-local-diagnostic
        output = result.stdout + result.stderr
        self.assertIn(
            "fast-local-diagnostic",
            output,
            "Workflow list should include fast-local-diagnostic"
        )

    def test_execution_plan_timestamp_valid(self):
        """Verify that executed_at timestamp in summary is valid ISO format."""
        self.assertIsNotNone(self.summary_path)
        with open(self.summary_path, "r", encoding="utf-8") as f:
            plan = json.load(f)

        executed_at = plan.get("executed_at")
        self.assertIsNotNone(executed_at, "Plan must have executed_at field")

        # Try to parse as ISO datetime
        try:
            dt = datetime.fromisoformat(executed_at)
            self.assertIsInstance(dt, datetime, "executed_at must be valid ISO datetime")
        except (ValueError, TypeError) as e:
            self.fail(f"executed_at is not valid ISO format: {e}")

    def test_execution_plan_session_id_format(self):
        """Verify that session_id in summary has expected format."""
        self.assertIsNotNone(self.summary_path)
        with open(self.summary_path, "r", encoding="utf-8") as f:
            plan = json.load(f)

        session_id = plan.get("session_id")
        self.assertIsNotNone(session_id, "Plan must have session_id")
        self.assertIsInstance(session_id, str, "session_id must be string")

        # Session ID should start with 'orchestration-'
        self.assertTrue(
            session_id.startswith("orchestration-"),
            f"session_id should start with 'orchestration-', got: {session_id}"
        )

    def test_ledger_audit_passes(self):
        """Verify that workflow-runtime.py audit-run passes successfully on the generated ledger."""
        self.assertIsNotNone(self.session_dir)
        ledger_path = self.session_dir / "run-ledger.jsonl"
        self.assertTrue(ledger_path.exists(), f"Ledger file should exist at {ledger_path}")

        cmd = [
            sys.executable,
            str(self.scripts_dir / "workflow-runtime.py"),
            "audit-run",
            "--ledger-path", str(ledger_path),
            "--repo-root", str(self.repo_root)
        ]
        audit_res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(
            audit_res.returncode,
            0,
            f"Ledger audit failed: {audit_res.stdout}\n{audit_res.stderr}"
        )


if __name__ == "__main__":
    unittest.main()
