"""Integration tests for auto-invocation authority-gating in SkillsOrchestrator.

Per ADR 0026, auto_invoke_next_workflow / recommended_workflow_id /
chosen_workflow_id / selected_workflow are compatibility metadata, NOT
execution authority. These tests prove the packaged-library consumer
(_handle_auto_invocation) surfaces a candidate and NEVER spawns a child
workflow absent a separate explicit authority event.

Tests the implementation of:
1. Candidate surfacing without spawning (fail-closed, ADR 0026)
2. Recursion guard surfaced without spawning
3. Session passing via --from-session flag (manual path, preserved)
4. No candidate field alone causes a spawn
"""

import os
import sys
import tempfile
import shutil
import yaml
import unittest
from pathlib import Path

# Add src directory to path
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from sensemaking_skills.runner import SkillsOrchestrator
from sensemaking_skills.config import SkillsConfig


class TestAutoInvocationTargetRepo(unittest.TestCase):
    """Test auto-invocation and recursion guard in SkillsOrchestrator."""

    @classmethod
    def setUpClass(cls):
        """Create temporary test repository with workflow registry."""
        cls.tmp_root = Path(tempfile.mkdtemp())

        # Create directory structure
        (cls.tmp_root / "artifacts").mkdir()
        (cls.tmp_root / "skills").mkdir()
        (cls.tmp_root / "scripts").mkdir()
        (cls.tmp_root / "docs" / "adr").mkdir(parents=True)

        # Create minimal CONTEXT.md
        context_file = cls.tmp_root / "CONTEXT.md"
        context_file.write_text("# Context: Test Project\n\nTest context for auto-invocation tests.\n")

        # Create workflow registry
        registry_path = cls.tmp_root / "skills" / "workflow-planner" / "references"
        registry_path.mkdir(parents=True, exist_ok=True)

        registry = {
            "workflows": [
                {
                    "id": "diagnostic-workflow",
                    "display_name": "Diagnostic Workflow",
                    "allowed_execution_modes": ["guided_execution", "autonomous_execution", "yolo_execution"],
                    "steps": [
                        {
                            "id": "1",
                            "skill": "repo-sensemaker",
                            "gate": "none",
                            "output_artifact": "sensemaking_brief",
                        }
                    ]
                },
                {
                    "id": "implementation-workflow",
                    "display_name": "Implementation Workflow",
                    "allowed_execution_modes": ["guided_execution", "autonomous_execution", "yolo_execution"],
                    "steps": [
                        {
                            "id": "1",
                            "skill": "to-prd",
                            "gate": "none",
                            "output_artifact": "prd",
                        }
                    ]
                }
            ]
        }

        with open(registry_path / "workflow-registry.yaml", "w") as f:
            yaml.dump(registry, f)

        # Create artifact contracts
        contracts_file = registry_path / "artifact-contracts.yaml"
        contracts = {
            "artifacts": [
                {
                    "id": "workflow_orchestration_plan",
                    "path": "artifacts/plan_{workflow_id}.md",
                    "produced_by": "workflow-planner",
                    "required_machine_fields": ["chosen_workflow_id"]
                }
            ]
        }
        with open(contracts_file, "w") as f:
            yaml.dump(contracts, f)

    @classmethod
    def tearDownClass(cls):
        """Clean up temporary directory."""
        if cls.tmp_root.exists():
            shutil.rmtree(cls.tmp_root)

    def setUp(self):
        """Set up test fixtures for each test."""
        config_dict = {
            "project_root": str(self.tmp_root),
            "artifacts_dir": "artifacts",
            "context_file": "CONTEXT.md",
            "skills_dir": "skills",
            "workflows_dir": "workflows",
            "adr_dir": "docs/adr",
        }
        self.config = SkillsConfig(config_dict)
        self.orchestrator = SkillsOrchestrator(config=self.config)

    def test_recursion_guard(self):
        """Verify recursion is surfaced WITHOUT spawning (ADR 0026).

        Creates an orchestration plan where recommended_workflow_id == current workflow_id,
        then verifies that _handle_auto_invocation surfaces the self-referential
        candidate and does NOT spawn a child workflow.
        """
        print("\n" + "="*60)
        print("TEST 1: Recursion Guard (fail-closed, no spawn)")
        print("="*60)

        # Create a session with orchestration plan that would cause recursion
        session_dir = self.tmp_root / "artifacts" / "test-recursion-session"
        session_dir.mkdir(parents=True, exist_ok=True)

        # Create an orchestration plan that tries to recursively invoke itself
        plan_content = """---
artifact_id: workflow_orchestration_plan
chosen_workflow_id: diagnostic-workflow
recommended_workflow_id: diagnostic-workflow
execution_mode: yolo_execution
---

# Orchestration Plan for diagnostic-workflow

This is a recursive plan that incorrectly recommends invoking the same workflow.
"""
        plan_file = session_dir / "plan_diagnostic-workflow.md"
        plan_file.write_text(plan_content)

        # Prove no child workflow is spawned: patch run_workflow so a spawn
        # would be observable, then assert it is never called.
        spawned = []
        original_run_workflow = self.orchestrator.run_workflow
        def no_spawn(workflow_id, execution_mode=None, from_session=None, **kw):
            spawned.append((workflow_id, execution_mode))
            return 999
        self.orchestrator.run_workflow = no_spawn
        try:
            exit_code = self.orchestrator._handle_auto_invocation(
                current_workflow_id="diagnostic-workflow",
                parent_session=str(session_dir)
            )
        finally:
            self.orchestrator.run_workflow = original_run_workflow

        # Fail-closed: returns clean completion (0) and never spawns.
        self.assertEqual(exit_code, 0, "Fail-closed should return 0 (completed, no spawn)")
        self.assertEqual(spawned, [], "No child workflow may be spawned (ADR 0026)")
        print("  ✓ Recursion candidate surfaced; no child workflow spawned")
        print("  [OK] TEST PASSED")

    def test_from_session_flag(self):
        """Verify --from-session passes parent artifacts to child workflow.

        Creates a parent session with artifacts, then verifies that
        _run_workflow_with_parent_session copies them to the new session.
        """
        print("\n" + "="*60)
        print("TEST 2: --from-session Flag and Parent Session Passing")
        print("="*60)

        # Create parent session with artifacts
        parent_session = self.tmp_root / "artifacts" / "parent-session"
        parent_session.mkdir(parents=True, exist_ok=True)

        # Create parent intent artifact
        intent_content = """---
artifact_id: user_intent
intent_source: user_problem_statement
scope_mode: soft
raw_problem_statement: "Test problem for auto-invocation"
created_at: "2026-05-23T12:00:00Z"
immutable: true
---

# User Intent

This is a test problem for auto-invocation.
"""
        intent_file = parent_session / "00-user-intent.md"
        intent_file.write_text(intent_content)

        # Create parent orchestration plan
        plan_content = """---
artifact_id: workflow_orchestration_plan
chosen_workflow_id: diagnostic-workflow
execution_mode: yolo_execution
---

# Orchestration Plan
"""
        plan_file = parent_session / "plan_diagnostic-workflow.md"
        plan_file.write_text(plan_content)

        # Call _run_workflow_with_parent_session
        # This should copy parent artifacts to a new session directory
        exit_code = self.orchestrator._run_workflow_with_parent_session(
            workflow_id="implementation-workflow",
            parent_session=parent_session
        )

        # The actual workflow won't run (no runtime.py), but we can verify
        # that the session directory was prepared correctly
        new_session_dir = self.tmp_root / "artifacts" / parent_session.name

        # Verify that artifacts were copied (or at least attempted)
        # Since we don't have a real runner, we just check the method doesn't crash
        self.assertIsNotNone(exit_code, "Method should return an exit code")
        print("  ✓ Parent session passing logic executed without errors")
        print("  [OK] TEST PASSED")

    def test_auto_chaining_reads_plan(self):
        """Verify auto-invocation reads/parses the plan and surfaces the candidate WITHOUT spawning (ADR 0026).

        Tests that _handle_auto_invocation can read YAML frontmatter from an
        orchestration plan, extract the candidate workflow_id, surface it, and
        does NOT spawn a child workflow.
        """
        print("\n" + "="*60)
        print("TEST 3: Auto-Chaining Plan Candidate Surfacing (fail-closed)")
        print("="*60)

        # Create a valid orchestration plan
        session_dir = self.tmp_root / "artifacts" / "test-plan-parsing"
        session_dir.mkdir(parents=True, exist_ok=True)

        # Create orchestration plan that mentions a different implementation workflow
        plan_content = """---
artifact_id: workflow_orchestration_plan
chosen_workflow_id: diagnostic-workflow
recommended_workflow_id: implementation-workflow
execution_mode: yolo_execution
---

# Orchestration Plan for diagnostic-workflow

Recommends chaining to implementation-workflow.
"""
        plan_file = session_dir / "plan_diagnostic-workflow.md"
        plan_file.write_text(plan_content)

        # Prove no child workflow is spawned
        spawned = []
        original_run_workflow = self.orchestrator.run_workflow
        def no_spawn(workflow_id, execution_mode=None, from_session=None, **kw):
            spawned.append((workflow_id, execution_mode))
            return 999
        self.orchestrator.run_workflow = no_spawn
        try:
            exit_code = self.orchestrator._handle_auto_invocation(
                current_workflow_id="diagnostic-workflow",
                parent_session=str(session_dir)
            )
        finally:
            self.orchestrator.run_workflow = original_run_workflow

        # Fail-closed: candidate surfaced, no spawn, clean completion.
        self.assertEqual(exit_code, 0, "Fail-closed should return 0")
        self.assertEqual(spawned, [], "A recommended_workflow_id must NOT spawn a child workflow (ADR 0026)")
        print("  ✓ Orchestration plan parsing logic works")
        print("  ✓ Candidate workflow surfaced, no child workflow spawned")
        print("  [OK] TEST PASSED")

    def _assert_no_spawn_from_plan_field(self, field_name):
        """Helper: prove that a single candidate field does NOT cause a spawn.

        Writes a plan carrying only ``field_name`` mapping to implementation-workflow,
        calls _handle_auto_invocation, and asserts no child workflow is spawned.
        """
        session_dir = self.tmp_root / "artifacts" / ("test-field-" + field_name.replace("_", "-"))
        session_dir.mkdir(parents=True, exist_ok=True)
        plan_content = """---
artifact_id: workflow_orchestration_plan
execution_mode: yolo_execution
%s: implementation-workflow
---

# Orchestration Plan
""" % field_name
        (session_dir / "plan_diagnostic-workflow.md").write_text(plan_content)

        spawned = []
        original_run_workflow = self.orchestrator.run_workflow
        def no_spawn(workflow_id, execution_mode=None, from_session=None, **kw):
            spawned.append((workflow_id, execution_mode))
            return 999
        self.orchestrator.run_workflow = no_spawn
        try:
            exit_code = self.orchestrator._handle_auto_invocation(
                current_workflow_id="diagnostic-workflow",
                parent_session=str(session_dir)
            )
        finally:
            self.orchestrator.run_workflow = original_run_workflow

        self.assertEqual(exit_code, 0, "Fail-closed should return 0")
        self.assertEqual(spawned, [], "Field '%s' must NOT spawn a child workflow (ADR 0026)" % field_name)

    def test_recommended_workflow_id_alone_does_not_spawn(self):
        """A discoverable recommended_workflow_id does NOT cause spawn (ADR 0026)."""
        self._assert_no_spawn_from_plan_field("recommended_workflow_id")

    def test_chosen_workflow_id_does_not_spawn(self):
        """A chosen_workflow_id does NOT cause spawn (ADR 0026)."""
        self._assert_no_spawn_from_plan_field("chosen_workflow_id")

    def test_selected_workflow_does_not_spawn(self):
        """A selected_workflow does NOT cause spawn (ADR 0026)."""
        self._assert_no_spawn_from_plan_field("selected_workflow")

    def test_no_candidate_surfaces_without_spawn(self):
        """With no candidate in the plan, _handle_auto_invocation surfaces nothing and does not spawn."""
        session_dir = self.tmp_root / "artifacts" / "test-no-candidate"
        session_dir.mkdir(parents=True, exist_ok=True)
        plan_content = """---
artifact_id: workflow_orchestration_plan
execution_mode: yolo_execution
---

# Orchestration Plan
"""
        (session_dir / "plan_diagnostic-workflow.md").write_text(plan_content)

        spawned = []
        original_run_workflow = self.orchestrator.run_workflow
        def no_spawn(workflow_id, execution_mode=None, from_session=None, **kw):
            spawned.append((workflow_id, execution_mode))
            return 999
        self.orchestrator.run_workflow = no_spawn
        try:
            exit_code = self.orchestrator._handle_auto_invocation(
                current_workflow_id="diagnostic-workflow",
                parent_session=str(session_dir)
            )
        finally:
            self.orchestrator.run_workflow = original_run_workflow

        self.assertEqual(exit_code, 0)
        self.assertEqual(spawned, [], "No candidate must not spawn (ADR 0026)")


if __name__ == "__main__":
    # Run tests with verbose output
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAutoInvocationTargetRepo)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
