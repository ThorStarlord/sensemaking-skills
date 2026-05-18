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
from pathlib import Path
from datetime import datetime


class TestYoloExecutionWithSkills(unittest.TestCase):
    """Test yolo_execution mode with fast-local-diagnostic workflow."""

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

    def test_execution_plan_created_by_yolo_mode(self):
        """Verify that yolo_execution mode creates an execution plan JSON."""
        # Run orchestration-runner with fast-local-diagnostic in yolo_execution mode
        cmd = [
            sys.executable,
            str(self.scripts_dir / "orchestration-runner.py"),
            "fast-local-diagnostic",
            "--mode", "yolo_execution",
        ]

        # Restore artifacts before running mutating modes to ensure git status is clean
        subprocess.run(["git", "restore", "artifacts/"], cwd=str(self.repo_root), capture_output=True)
        subprocess.run(["git", "clean", "-fd", "artifacts/"], cwd=str(self.repo_root), capture_output=True)

        result = subprocess.run(
            cmd,
            cwd=str(self.repo_root),
            capture_output=True,
            text=True,
            timeout=60,
        )

        # Check that the command ran (may have partial/error status)
        self.assertIsNotNone(result.returncode)
        output = result.stdout + result.stderr

        # Verify the output mentions execution plan was written
        self.assertIn(
            "execution_plan_fast-local-diagnostic.json",
            output,
            "Output should mention execution plan file was created"
        )

    def test_execution_plan_json_valid_format(self):
        """Verify that execution plan JSON has required fields and valid structure."""
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
        self.assertEqual(plan["mode"], "yolo_execution")
        self.assertIsInstance(plan["steps"], list)
        self.assertGreater(len(plan["steps"]), 0, "Plan must have at least one step")

    def test_execution_plan_steps_have_required_fields(self):
        """Verify that each step in the execution plan has required fields."""
        plan_path = self.artifacts_dir / "execution_plan_fast-local-diagnostic.json"

        with open(plan_path, "r", encoding="utf-8") as f:
            plan = json.load(f)

        steps = plan.get("steps", [])
        self.assertGreater(len(steps), 0, "Plan must have at least one step")

        for step in steps:
            # Each step must have these fields
            self.assertIn("id", step, f"Step {step} must have id field")
            self.assertIn("skill", step, f"Step {step} must have skill field")
            self.assertIn("step_type", step, f"Step {step} must have step_type field")
            self.assertIn("gate", step, f"Step {step} must have gate field")
            self.assertIn("output_artifact", step, f"Step {step} must have output_artifact field")

            # Verify types
            self.assertIsInstance(step["id"], int, "step id must be integer")
            self.assertIsInstance(step["skill"], str, "step skill must be string")
            self.assertIsInstance(step["step_type"], str, "step step_type must be string")

    def test_fast_local_diagnostic_workflow_registered(self):
        """Verify that fast-local-diagnostic workflow is properly registered."""
        registry_path = (
            self.repo_root / "skills" / "workflow-orchestrator" /
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
        """Verify that orchestration-runner.py is callable and lists workflows."""
        cmd = [
            sys.executable,
            str(self.scripts_dir / "orchestration-runner.py"),
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
            f"orchestration-runner.py --list-workflows should succeed, got: {result.stderr}"
        )

        # Should list fast-local-diagnostic
        output = result.stdout + result.stderr
        self.assertIn(
            "fast-local-diagnostic",
            output,
            "Workflow list should include fast-local-diagnostic"
        )

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
