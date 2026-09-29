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
import tempfile
import shutil
from pathlib import Path
from datetime import datetime


class TestAutonomousExecutionIntegration(unittest.TestCase):
    """Test autonomous_execution mode with fast-local-diagnostic workflow."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures by running the workflow in autonomous_execution mode once."""
        # Resolve repo root
        test_dir = Path(__file__).parent
        cls.repo_root = test_dir.parent.parent
        cls.scripts_dir = cls.repo_root / "scripts"

        # Session artifacts must never land in the real, committed artifacts/
        # tree (see issue #42) — use --from-session with an isolated tempdir,
        # the same confinement mechanism ADR 0010 established, instead of
        # letting the runtime create its own numbered folder under repo_root.
        cls._session_tempdir = tempfile.mkdtemp(
            prefix="orchestration-autonomous-execution-integration-", dir=str(cls.repo_root.parent)
        )
        cls.session_dir = Path(cls._session_tempdir)
        intent_path = cls.session_dir / "00-user-intent.md"
        intent_path.write_text(
            '# User Intent\n\n'
            '## Machine-readable intent\n\n'
            '```yaml\n'
            'artifact_id: user_intent\n'
            'intent_source: integration-test\n'
            'scope_mode: focused\n'
            'raw_problem_statement: "Test autonomous_execution mode integration"\n'
            'created_at: "2026-07-25T00:00:00Z"\n'
            'created_by: "autonomous-execution-integration-test"\n'
            'immutable: false\n'
            '```\n',
            encoding="utf-8",
        )

        # Set environment for autonomous execution
        os.environ["SENSEMAKING_EXECUTION_MODE"] = "autonomous"

        cmd = [
            sys.executable,
            str(cls.scripts_dir / "workflow-runtime.py"),
            "--workflow", "fast-local-diagnostic",
            "--mode", "autonomous_execution",
            "--gate-decision", "auto-approve",
            "--repo-root", str(cls.repo_root),
            "--from-session", str(cls.session_dir),
            "--executor", "dry-run",
            "--use-fixtures",
        ]

        cls.result = subprocess.run(
            cmd,
            cwd=str(cls.repo_root),
            capture_output=True,
            text=True,
            timeout=120,
        )

        cls.output = cls.result.stdout + cls.result.stderr
        cls.summary_path = cls.session_dir / "workflow_summary.json"

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls._session_tempdir, ignore_errors=True)

    def test_autonomous_execution_completes_full_workflow(self):
        """Verify that autonomous_execution mode completes full workflow with auto-approved gates."""
        self.assertIsNotNone(self.session_dir, "Session directory should have been created")
        self.assertEqual(self.result.returncode, 0, f"Runtime execution failed: {self.output}")

        # Verify the output shows autonomous_execution mode was invoked
        self.assertIn(
            "autonomous_execution",
            self.output,
            "Output should mention autonomous_execution mode"
        )

        # Verify the plan was written
        self.assertIn(
            "Plan written",
            self.output,
            "Output should show execution plan was created"
        )

    def test_execution_plan_json_is_valid(self):
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
        self.assertEqual(plan["mode"], "autonomous_execution")
        self.assertIsInstance(plan["steps"], list)
        self.assertGreater(len(plan["steps"]), 0, "Plan must have at least one step")

    def test_run_log_records_skill_execution(self):
        """Verify that run log is created and records skill execution details."""
        self.assertIsNotNone(self.session_dir, "Session directory should have been created")
        run_log_path = self.session_dir / "run_log_fast-local-diagnostic_autonomous_execution.md"

        self.assertTrue(
            run_log_path.exists(),
            f"Run log should exist at {run_log_path}"
        )

        # Read and validate content
        with open(run_log_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Should contain key sections
        self.assertIn("Workflow Run Log", content, "Run log should have workflow header")
        self.assertIn("fast-local-diagnostic", content, "Run log should mention workflow ID")
        self.assertIn("autonomous_execution", content, "Run log should mention execution mode")

        # Should contain status information
        self.assertIn("Status", content, "Run log should record status")
        self.assertIn("completed", content.lower(), "Run log should indicate successful completion")

    def test_execution_plan_steps_have_required_fields(self):
        """Verify that each step in the summary has required fields."""
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
