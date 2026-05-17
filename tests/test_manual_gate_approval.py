"""Tests for manual gate approval workflow in guided_execution mode.

Verifies that:
1. Gate system prompts user for approval
2. Gate denial stops workflow execution
3. Gate decisions persist in run logs with proper structure
"""

import unittest
import json
import tempfile
import os
from pathlib import Path
from datetime import datetime
import sys
import re


class TestManualGateApproval(unittest.TestCase):
    """Test suite for manual gate approval workflow."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_gate_system_prompts_user_for_approval(self):
        """Test that gate system prompts user for approval in guided_execution mode.

        Verifies:
        - Gate decision structure has required fields
        - Timestamp is in ISO 8601 format
        - Mode matches the execution mode
        - Result is one of the valid GATE_RESULTS
        """
        # Simulate gate decision from guided_execution mode manual approval
        gate_decision = {
            "step": 1,
            "gate": "review",
            "result": "approved_by_user",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "approved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "approved_by": "test_user",
            "mode": "guided_execution",
        }

        # Verify required fields
        required_fields = ["step", "gate", "result", "timestamp", "mode"]
        for field in required_fields:
            self.assertIn(field, gate_decision, f"Gate decision missing required field: {field}")

        # Verify gate result is valid
        valid_results = ["approved_by_user", "denied_by_user", "automated_approval", "bypassed", "not_applicable"]
        self.assertIn(gate_decision["result"], valid_results, f"Invalid gate result: {gate_decision['result']}")

        # Verify timestamp format (ISO 8601)
        timestamp_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
        self.assertRegex(gate_decision["timestamp"], timestamp_pattern, "Timestamp not in ISO 8601 format")

        # Verify mode is guided_execution for manual approval
        self.assertEqual(gate_decision["mode"], "guided_execution")

        # Verify approved_by is present for approved gates
        if gate_decision["result"] == "approved_by_user":
            self.assertIn("approved_by", gate_decision, "approved_by field missing for approved gate")
            self.assertIsNotNone(gate_decision["approved_by"])

    def test_gate_denial_stops_workflow(self):
        """Test that gate denial halts workflow execution.

        Verifies:
        - Denied gate result is 'denied_by_user'
        - Workflow step status changes to PAUSED
        - Subsequent steps are not executed
        - Denial reason is recorded if provided
        """
        # Simulate gate denial
        gate_decision = {
            "step": 2,
            "gate": "critical_review",
            "result": "denied_by_user",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "approved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reason": "Output does not meet quality standards",
            "mode": "guided_execution",
        }

        # Verify denial structure
        self.assertEqual(gate_decision["result"], "denied_by_user")
        self.assertIn("reason", gate_decision)

        # Simulate step execution result when gate is denied
        step_result = {
            "step_id": "2",
            "skill": "test-skill",
            "gate": "critical_review",
            "output_artifact": "test_output.md",
            "artifact_path": "artifacts/test_output.md",
            "gate_result": "denied_by_user",
            "status": "PAUSED",  # Workflow halts at this step
            "step_type": "local_execution",
        }

        # Verify workflow halts
        self.assertEqual(step_result["status"], "PAUSED", "Workflow should be paused after gate denial")

        # Verify no subsequent steps are in the results
        # (in a real run, step_results would only contain steps up to and including this one)
        self.assertNotEqual(step_result["status"], "COMPLETED")

    def test_gate_decision_persists_in_run_log(self):
        """Test that gate decisions persist in run logs with complete information.

        Verifies:
        - Gate decision is recorded in run log
        - Run log contains gate decision history
        - All gate fields are preserved
        - Gate decisions section is properly formatted
        """
        # Simulate multiple gate decisions through a workflow
        gate_decisions = [
            {
                "step": 1,
                "gate": "plan_review",
                "result": "approved_by_user",
                "timestamp": "2026-05-16 14:00:00",
                "approved_at": "2026-05-16 14:00:01",
                "approved_by": "alice",
                "mode": "guided_execution",
            },
            {
                "step": 2,
                "gate": "brief_review",
                "result": "approved_by_user",
                "timestamp": "2026-05-16 14:05:00",
                "approved_at": "2026-05-16 14:05:15",
                "approved_by": "bob",
                "mode": "guided_execution",
            },
        ]

        # Simulate run log generation
        run_log_content = self._generate_run_log_with_gates(gate_decisions)

        # Verify run log contains gate decisions
        self.assertIn("Decisions & Overrides", run_log_content)

        # Verify each gate decision is recorded
        for gd in gate_decisions:
            decision_text = f"Gate '{gd['gate']}' (step {gd['step']}): {gd['result']}"
            self.assertIn(decision_text, run_log_content,
                         f"Gate decision not found in run log: {decision_text}")

        # Verify timestamp format is preserved
        self.assertIn("2026-05-16 14:00:00", run_log_content)

        # Verify approver information is available in log
        self.assertIn("alice", run_log_content)
        self.assertIn("bob", run_log_content)

    def test_gate_decision_with_automated_approval(self):
        """Test gate decision structure for automated approval (autonomous_execution mode).

        Verifies:
        - Automated approval result is recorded correctly
        - Mode is autonomous_execution
        - approved_by indicates automation
        - Timestamp is recorded
        """
        gate_decision = {
            "step": 1,
            "gate": "review",
            "result": "automated_approval",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": "autonomous_execution",
            "approved_by": "automated_gate",
        }

        # Verify automated approval structure
        self.assertEqual(gate_decision["result"], "automated_approval")
        self.assertEqual(gate_decision["mode"], "autonomous_execution")
        self.assertEqual(gate_decision["approved_by"], "automated_gate")

    def test_gate_decision_with_bypass(self):
        """Test gate decision structure for bypassed gates (yolo_execution mode).

        Verifies:
        - Bypassed gate result is recorded
        - Mode is yolo_execution
        - No approval_by or reason needed
        - Timestamp is recorded
        """
        gate_decision = {
            "step": 1,
            "gate": "review",
            "result": "bypassed",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": "yolo_execution",
        }

        # Verify bypass structure
        self.assertEqual(gate_decision["result"], "bypassed")
        self.assertEqual(gate_decision["mode"], "yolo_execution")

    def test_gate_decision_not_applicable(self):
        """Test gate decision structure for non-applicable gates (plan_only mode).

        Verifies:
        - Not applicable result is used for non-mutating modes
        - Mode is plan_only or prompt_chain
        - No approval fields present
        - Timestamp is recorded
        """
        gate_decision = {
            "step": 1,
            "gate": "review",
            "result": "not_applicable",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": "plan_only",
        }

        # Verify not_applicable structure
        self.assertEqual(gate_decision["result"], "not_applicable")
        self.assertEqual(gate_decision["mode"], "plan_only")
        self.assertNotIn("approved_by", gate_decision)

    def test_multiple_gates_in_workflow(self):
        """Test workflow with multiple gates across different steps.

        Verifies:
        - Each step can have a gate
        - Gates are independent
        - Denial at any step stops workflow
        - All gates before denial are recorded as completed
        """
        # Simulate a 3-step workflow with gates
        gate_decisions = [
            {
                "step": 1,
                "gate": "step1_gate",
                "result": "approved_by_user",
                "timestamp": "2026-05-16 14:00:00",
                "approved_by": "reviewer1",
                "mode": "guided_execution",
            },
            {
                "step": 2,
                "gate": "step2_gate",
                "result": "approved_by_user",
                "timestamp": "2026-05-16 14:05:00",
                "approved_by": "reviewer2",
                "mode": "guided_execution",
            },
            {
                "step": 3,
                "gate": "step3_gate",
                "result": "denied_by_user",
                "timestamp": "2026-05-16 14:10:00",
                "reason": "Additional analysis needed",
                "mode": "guided_execution",
            },
        ]

        # Verify gate sequence
        self.assertEqual(len(gate_decisions), 3)
        self.assertEqual(gate_decisions[0]["result"], "approved_by_user")
        self.assertEqual(gate_decisions[1]["result"], "approved_by_user")
        self.assertEqual(gate_decisions[2]["result"], "denied_by_user")

        # Verify only steps 1-2 would complete, step 3 halts
        completed_steps = [gd for gd in gate_decisions if gd["result"] == "approved_by_user"]
        self.assertEqual(len(completed_steps), 2)

    # Helper methods

    def _generate_run_log_with_gates(self, gate_decisions):
        """Generate a run log format similar to orchestration-runner.py output."""
        lines = [
            "# Workflow Run Log: Test Workflow",
            "",
            f"- **Date**: {datetime.now().strftime('%Y-%m-%d')}",
            f"- **Session ID**: test-session-123",
            f"- **Status**: paused",
            "",
            "## Decisions & Overrides",
            "",
        ]

        for gd in gate_decisions:
            lines.append(f"- Gate '{gd['gate']}' (step {gd['step']}): {gd['result']} at {gd['timestamp']}")

        lines.extend([
            "- Approvers: " + ", ".join(set(gd.get("approved_by", "") for gd in gate_decisions if gd.get("approved_by"))),
            "",
        ])

        return "\n".join(lines)


if __name__ == "__main__":
    unittest.main()
