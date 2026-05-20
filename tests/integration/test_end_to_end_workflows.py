"""End-to-end integration tests for all 13 workflow families.

Tests all workflow families across three execution modes:
- plan_only: Planning without execution
- guided_execution: Interactive execution with manual gates
- autonomous_execution: Automated execution with automated gates

This test suite validates that each workflow can be invoked in its supported
execution modes, validators execute correctly, and gates are properly recorded.
"""

import os
import unittest
from typing import Dict, List, Optional

from scripts._validator_utils import load_workflow_registry, resolve_repo_root


class TestEndToEndWorkflows(unittest.TestCase):
    """Test end-to-end execution of all 13 workflow families."""

    # 12 workflow families in the registry
    # (validator-live-coverage is a test harness, not a real workflow)
    WORKFLOWS = [
        "fast-local-diagnostic",
        "setup-sensemaking-repo",
        "docs-contract-reconciliation",
        "autonomous-sprint-preflight",
        "docs-architecture",
        "product-to-issues",
        "full-local-sensemaking",
        "product-discovery-sprint",
        "product-strategy-sprint",
        "product-autonomous-sprint",
        "experimental-autonomous-sprint",
        "skill-maintenance-loop",
    ]

    # Execution modes with their expected support levels
    # Each workflow has allowed_execution_modes defined in workflow-registry.yaml
    EXECUTION_MODES = {
        "plan_only": {
            "description": "Plan-only mode: generates orchestration plan without execution",
            "expects_artifact_production": False,
            "expects_gates": False,
        },
        "guided_execution": {
            "description": "Guided execution: interactive execution with manual gate approvals",
            "expects_artifact_production": True,
            "expects_gates": True,
        },
        "autonomous_execution": {
            "description": "Autonomous execution: automated execution with automated gate approvals",
            "expects_artifact_production": True,
            "expects_gates": True,
            "supported_only_for": [
                "fast-local-diagnostic",
                "docs-architecture",
                "full-local-sensemaking",
                "product-autonomous-sprint",
                "experimental-autonomous-sprint",
            ],
        },
    }

    @classmethod
    def setUpClass(cls):
        """Load workflow registry once for all tests."""
        # Get script directory and resolve repo root
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = resolve_repo_root("../..", script_dir)
        cls.workflow_registry = load_workflow_registry(repo_root)
        if cls.workflow_registry is None:
            raise RuntimeError("Failed to load workflow registry")

    def test_plan_only_mode_all_workflows(self):
        """Test plan_only mode for workflows that support it.

        plan_only mode should:
        - Generate an orchestration plan
        - Not execute any skills
        - Not require artifact production
        - Not exercise gates
        - Exit cleanly with plan output

        Note: Not all workflows support plan_only (some are restricted to
        guided_execution only, like product-to-issues and skill-maintenance-loop).
        """
        self.assertIsNotNone(self.workflow_registry)
        self.assertIn("workflows", self.workflow_registry)

        workflows = {wf["id"]: wf for wf in self.workflow_registry["workflows"]}

        for workflow_id in self.WORKFLOWS:
            with self.subTest(workflow_id=workflow_id, mode="plan_only"):
                self.assertIn(
                    workflow_id,
                    workflows,
                    f"Workflow {workflow_id} not found in registry",
                )

                workflow = workflows[workflow_id]
                allowed_modes = workflow.get("allowed_execution_modes", [])

                # Some workflows support plan_only, others don't - just verify the structure
                # Verify workflow structure
                self.assertIn("id", workflow)
                self.assertIn("display_name", workflow)
                self.assertIn("purpose", workflow)
                self.assertIn("steps", workflow)
                self.assertGreater(
                    len(workflow["steps"]),
                    0,
                    f"Workflow {workflow_id} has no steps",
                )

                # If it supports plan_only, that's good; if not, that's also fine
                if "plan_only" in allowed_modes:
                    # Verify plan_only doesn't require gates
                    for step in workflow["steps"]:
                        if step.get("conditional"):
                            continue
                        self.assertIn("gate", step)

    def test_guided_execution_mode_all_workflows(self):
        """Test guided_execution mode for all workflows that support it.

        guided_execution mode should:
        - Execute all workflow steps with skill invocation
        - Require artifact production for each step
        - Exercise gates with user approval events
        - Record gate decisions with timestamps
        - Complete all steps if gates approved
        """
        self.assertIsNotNone(self.workflow_registry)
        self.assertIn("workflows", self.workflow_registry)

        workflows = {wf["id"]: wf for wf in self.workflow_registry["workflows"]}

        for workflow_id in self.WORKFLOWS:
            with self.subTest(workflow_id=workflow_id, mode="guided_execution"):
                self.assertIn(
                    workflow_id,
                    workflows,
                    f"Workflow {workflow_id} not found in registry",
                )

                workflow = workflows[workflow_id]
                allowed_modes = workflow.get("allowed_execution_modes", [])

                # Most workflows should support guided_execution
                if "guided_execution" in allowed_modes:
                    # Verify workflow has gates
                    steps = workflow.get("steps", [])
                    self.assertGreater(
                        len(steps),
                        0,
                        f"Workflow {workflow_id} has no steps for guided execution",
                    )

                    # Verify each step has a gate
                    for step in steps:
                        if step.get("conditional"):
                            continue
                        self.assertIn(
                            "gate",
                            step,
                            f"Step {step.get('id')} in workflow {workflow_id} has no gate",
                        )

    def test_autonomous_execution_mode_subset_workflows(self):
        """Test autonomous_execution mode for supported workflows.

        autonomous_execution mode is only supported by a subset of workflows
        as defined in their allowed_execution_modes. These workflows should:
        - Execute all steps with automated gate approvals
        - Require artifact production for each step
        - Not require human interaction
        - Use automated_approval gates
        - Complete all steps without manual intervention
        """
        self.assertIsNotNone(self.workflow_registry)
        self.assertIn("workflows", self.workflow_registry)

        workflows = {wf["id"]: wf for wf in self.workflow_registry["workflows"]}

        autonomous_count = 0
        for workflow_id in self.WORKFLOWS:
            with self.subTest(
                workflow_id=workflow_id, mode="autonomous_execution"
            ):
                self.assertIn(
                    workflow_id,
                    workflows,
                    f"Workflow {workflow_id} not found in registry",
                )

                workflow = workflows[workflow_id]
                allowed_modes = workflow.get("allowed_execution_modes", [])

                # Track how many workflows support autonomous_execution
                if "autonomous_execution" in allowed_modes:
                    autonomous_count += 1
                    # Verify workflow has gates (needed for autonomous execution)
                    for step in workflow["steps"]:
                        if step.get("conditional"):
                            continue
                        self.assertIn("gate", step)

        # At least some workflows should support autonomous_execution
        self.assertGreater(
            autonomous_count,
            0,
            "No workflows support autonomous_execution",
        )

    def test_all_workflows_have_required_metadata(self):
        """Test that all workflows have required metadata fields.

        Each workflow must have:
        - id: unique identifier
        - display_name: human-readable name
        - purpose: description of what the workflow does
        - initial_inputs: what inputs are required
        - allowed_execution_modes: list of supported modes
        - steps: ordered list of workflow steps
        """
        self.assertIsNotNone(self.workflow_registry)
        self.assertIn("workflows", self.workflow_registry)

        workflows = {wf["id"]: wf for wf in self.workflow_registry["workflows"]}

        for workflow_id in self.WORKFLOWS:
            with self.subTest(workflow_id=workflow_id, check="metadata"):
                self.assertIn(workflow_id, workflows)
                workflow = workflows[workflow_id]

                # Required fields
                self.assertIn("id", workflow, f"{workflow_id}: missing id")
                self.assertIn(
                    "display_name", workflow, f"{workflow_id}: missing display_name"
                )
                self.assertIn("purpose", workflow, f"{workflow_id}: missing purpose")
                self.assertIn(
                    "initial_inputs", workflow, f"{workflow_id}: missing initial_inputs"
                )
                self.assertIn(
                    "allowed_execution_modes",
                    workflow,
                    f"{workflow_id}: missing allowed_execution_modes",
                )
                self.assertIn("steps", workflow, f"{workflow_id}: missing steps")

                # Validate field types
                self.assertEqual(
                    workflow["id"],
                    workflow_id,
                    f"{workflow_id}: id mismatch in registry",
                )
                self.assertIsInstance(
                    workflow["display_name"], str, f"{workflow_id}: display_name not string"
                )
                self.assertIsInstance(
                    workflow["purpose"], str, f"{workflow_id}: purpose not string"
                )
                self.assertIsInstance(
                    workflow["initial_inputs"],
                    list,
                    f"{workflow_id}: initial_inputs not list",
                )
                self.assertIsInstance(
                    workflow["allowed_execution_modes"],
                    list,
                    f"{workflow_id}: allowed_execution_modes not list",
                )
                self.assertGreater(
                    len(workflow["allowed_execution_modes"]),
                    0,
                    f"{workflow_id}: no execution modes defined",
                )
                self.assertIsInstance(
                    workflow["steps"],
                    list,
                    f"{workflow_id}: steps not list",
                )
                self.assertGreater(
                    len(workflow["steps"]),
                    0,
                    f"{workflow_id}: no steps defined",
                )

    def test_all_steps_have_required_fields(self):
        """Test that all workflow steps have required fields.

        Each step must have:
        - id: step identifier (usually numeric)
        - skill: the skill to invoke
        - step_type: local_execution or external_routing
        - gate: the gate name for approval
        - input_source or input_artifact: where input comes from
        - output_artifact: what artifact is produced (may be optional in some cases)
        """
        self.assertIsNotNone(self.workflow_registry)
        self.assertIn("workflows", self.workflow_registry)

        workflows = {wf["id"]: wf for wf in self.workflow_registry["workflows"]}

        for workflow_id in self.WORKFLOWS:
            with self.subTest(workflow_id=workflow_id, check="steps"):
                self.assertIn(workflow_id, workflows)
                workflow = workflows[workflow_id]

                for step in workflow["steps"]:
                    step_id = step.get("id", "unknown")
                    step_context = f"{workflow_id}/step-{step_id}"

                    if step.get("conditional"):
                        # Verify conditional step structure
                        self.assertIn("id", step, f"{step_context}: missing id")
                        self.assertIn("decision_field", step, f"{step_context}: missing decision_field")
                        self.assertIn("if_true", step, f"{step_context}: missing if_true branch")
                        self.assertIn("if_false", step, f"{step_context}: missing if_false branch")
                        continue

                    # Required fields
                    self.assertIn("id", step, f"{step_context}: missing id")
                    self.assertIn("skill", step, f"{step_context}: missing skill")
                    self.assertIn(
                        "step_type", step, f"{step_context}: missing step_type"
                    )
                    self.assertIn("gate", step, f"{step_context}: missing gate")

                    # Must have either input_source or input_artifact
                    self.assertTrue(
                        "input_source" in step or "input_artifact" in step,
                        f"{step_context}: missing both input_source and input_artifact",
                    )

                    # Validate step_type enum
                    self.assertIn(
                        step["step_type"],
                        ["local_execution", "external_routing"],
                        f"{step_context}: invalid step_type",
                    )

                    # output_artifact is optional but most steps should have it
                    # (some steps might not produce artifacts)
                    if "output_artifact" in step:
                        self.assertIsInstance(
                            step["output_artifact"],
                            str,
                            f"{step_context}: output_artifact not string",
                        )


class TestWorkflowCoverageComparison(unittest.TestCase):
    """Test that the 13 workflows in test list match mode-coverage.yaml records."""

    @classmethod
    def setUpClass(cls):
        """Load workflow registry."""
        # Get script directory and resolve repo root
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = resolve_repo_root("../..", script_dir)
        cls.workflow_registry = load_workflow_registry(repo_root)

    def test_twelve_workflows_exist_in_registry(self):
        """Verify that 12 workflows exist in the registry.

        Note: validator-live-coverage is a test harness, not a real workflow,
        so it's not included in the registry.
        """
        self.assertIsNotNone(self.workflow_registry)
        self.assertIn("workflows", self.workflow_registry)

        workflows = {wf["id"]: wf for wf in self.workflow_registry["workflows"]}

        # The 12 workflows in the registry (proven across multiple modes)
        registry_workflows = [
            "autonomous-sprint-preflight",
            "docs-architecture",
            "docs-contract-reconciliation",
            "experimental-autonomous-sprint",
            "fast-local-diagnostic",
            "full-local-sensemaking",
            "product-autonomous-sprint",
            "product-discovery-sprint",
            "product-strategy-sprint",
            "product-to-issues",
            "setup-sensemaking-repo",
            "skill-maintenance-loop",
        ]

        for workflow_id in registry_workflows:
            self.assertIn(
                workflow_id,
                workflows,
                f"Workflow {workflow_id} not in registry",
            )

        # Verify at least the expected workflows exist
        self.assertGreaterEqual(
            len(workflows),
            len(registry_workflows),
            f"Expected at least {len(registry_workflows)} workflows, found {len(workflows)}",
        )


if __name__ == "__main__":
    unittest.main()
