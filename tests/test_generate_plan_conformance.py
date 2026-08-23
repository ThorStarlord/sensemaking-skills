"""The runtime's two-stage workflow_orchestration_plan lifecycle must conform to
ADR 0025.

Governing authority: ADR 0025 (two-stage plan lifecycle). The runtime authors a
PROVISIONAL execution skeleton at Phase 2 (generate_plan), which must NOT fabricate
diagnosis-dependent fields and must NOT treat the executing workflow as the final
routing decision. Once a valid repository_sensemaking_brief exists, finalize_plan()
consumes the real primary_fog_type evidence and produces the canonical contract-valid
plan (workflow_steps, created_at, routing audit, contract-valid chosen_workflow_id).

Only the FINALIZED artifact is required to pass validate-plan.py / validate-artifact.py.
The provisional skeleton is a different, pre-diagnosis knowledge state.

These tests exercise the real producer/finalization path (OrchestrationRunner
generate_plan -> finalize_plan), not a parallel test-only class.
"""

import os
import sys
import tempfile
import shutil
import subprocess
import importlib.util
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
scripts_dir = os.path.join(REPO_ROOT, "scripts")
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

if "workflow_runtime" in sys.modules:
    workflow_runtime = sys.modules["workflow_runtime"]
else:
    spec = importlib.util.spec_from_file_location(
        "workflow_runtime", os.path.join(scripts_dir, "workflow-runtime.py")
    )
    workflow_runtime = importlib.util.module_from_spec(spec)
    sys.modules["workflow_runtime"] = workflow_runtime
    spec.loader.exec_module(workflow_runtime)

OrchestrationRunner = workflow_runtime.OrchestrationRunner

# Fog type -> the contract-valid implementation workflow it selects (mirrors both
# validate-plan.py fog_to_workflow and OrchestrationRunner._FOG_TO_WORKFLOW).
FOG_TO_WORKFLOW = {
    "product_fog": "product-implementation-workflow",
    "ui_fog": "ui-implementation-workflow",
    "docs_fog": "docs-implementation-workflow",
    "architecture_fog": "architecture-implementation-workflow",
}


def _run(validator, artifact_id, plan_path):
    """Run a validator script; return (ok, combined_output)."""
    if validator == "validate-artifact.py":
        cmd = [sys.executable, os.path.join(scripts_dir, validator), artifact_id,
               plan_path, "--repo-root", REPO_ROOT]
    else:
        cmd = [sys.executable, os.path.join(scripts_dir, validator), plan_path,
               "--repo-root", REPO_ROOT]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode == 0, (res.stdout + res.stderr)


def _read_machine_block(path):
    """Parse the first fenced ```yaml machine block from an artifact."""
    import re
    import yaml
    with open(path, encoding="utf-8") as f:
        content = f.read()
    m = re.search(r"```yaml\n(.*?)\n```", content, re.DOTALL)
    if not m:
        return {}
    return (yaml.safe_load(m.group(1)) or {})


def _write_controlled_brief(fog_type):
    """Write a valid controlled repository_sensemaking_brief to a temp file."""
    tmp = tempfile.mkdtemp()
    brief_path = os.path.join(tmp, "repository_sensemaking_brief.md")
    impl = FOG_TO_WORKFLOW[fog_type]
    with open(brief_path, "w", encoding="utf-8") as f:
        f.write(
            "# Repository Sensemaking Brief\n\n"
            "## 1. Diagnosis summary\n\n"
            f"{fog_type} detected.\n\n"
            "```yaml\n"
            "artifact_id: repository_sensemaking_brief\n"
            f"primary_fog_type: {fog_type}\n"
            f"recommended_workflow_id: {impl}\n"
            "escalation_recommended: false\n"
            "```\n"
        )
    return brief_path


class TestTwoStagePlanLifecycle(unittest.TestCase):
    """Prove BOTH states of the ADR 0025 two-stage lifecycle."""

    def _runner(self, workflow_id, mode="guided_execution", tmpdir=None):
        runner = OrchestrationRunner(
            workflow_id=workflow_id, mode=mode, repo_root=REPO_ROOT, executor="dry-run"
        )
        self.assertTrue(runner.workflow, f"workflow '{workflow_id}' not loaded: {runner.errors}")
        runner.session_id = "test-session-0001"
        runner.plan_out = os.path.join(tmpdir or tempfile.mkdtemp(), f"plan_{workflow_id}.md")
        return runner

    def _assert_provisional(self, runner, workflow_id):
        """Provisional-state assertions (ADR 0025 stage 1)."""
        machine = _read_machine_block(runner.plan_out)
        # No fabricated diagnosis-dependent field.
        self.assertNotIn("primary_fog_type", machine,
                         "provisional skeleton must NOT emit primary_fog_type before diagnosis")
        # No finalized-canonical fields.
        self.assertNotIn("workflow_steps", machine,
                         "provisional skeleton must NOT emit workflow_steps (finalized field)")
        self.assertNotIn("created_at", machine,
                         "provisional skeleton must NOT emit created_at (finalized field)")
        # Explicitly flagged provisional, so it is never mistaken for a finalized plan.
        self.assertEqual(machine.get("plan_stage"), "provisional",
                         "provisional skeleton must be flagged plan_stage: provisional")
        # The executing workflow identity is recorded, but NOT as a final routing claim.
        self.assertEqual(machine.get("chosen_workflow_id"), workflow_id,
                         "provisional skeleton records the currently-executing workflow")
        # It must be a different knowledge state from a final routing decision: there is
        # no final fog-aligned workflow asserted anywhere.
        with open(runner.plan_out, encoding="utf-8") as f:
            provisional_content = f.read()
        self.assertFalse(
            any(w in provisional_content for w in FOG_TO_WORKFLOW.values()),
            "provisional skeleton must not assert a final implementation workflow",
        )

    def _assert_finalized(self, runner, fog_type):
        """Finalized-state assertions (ADR 0025 stage 2)."""
        machine = _read_machine_block(runner.plan_out)
        # Real brief evidence consumed.
        self.assertEqual(machine.get("primary_fog_type"), fog_type)
        # Final routing state derived from the evidence, distinct from the
        # provisional execution identity.
        self.assertEqual(machine.get("chosen_workflow_id"), FOG_TO_WORKFLOW[fog_type])
        self.assertEqual(machine.get("selected_workflow"), FOG_TO_WORKFLOW[fog_type])
        self.assertEqual(machine.get("system_recommended_workflow"), FOG_TO_WORKFLOW[fog_type])
        self.assertIn("routing_decision_method", machine)
        # workflow_steps present and populated.
        self.assertTrue(machine.get("workflow_steps"),
                        "finalized plan must carry a non-empty workflow_steps array")
        # created_at present.
        self.assertTrue(machine.get("created_at"), "finalized plan must carry created_at")
        # No stale auto-invocation authority language on the plan.
        self.assertNotIn("recommended_workflow_id", machine,
                         "the plan's authoritative selection field is chosen_workflow_id")
        # No fabricated/additional divergence when selection matches recommendation.
        self.assertIs(machine.get("routing_divergence"), False)

    def test_provisional_generation_produces_valid_placeholder_no_fabrication(self):
        """Provisional skeleton: no fabricated diagnosis; runtime can proceed."""
        tmp = tempfile.mkdtemp()
        try:
            for workflow_id in ("full-local-sensemaking", "fast-local-diagnostic"):
                with self.subTest(workflow_id=workflow_id):
                    runner = self._runner(workflow_id, tmpdir=tmp)
                    runner.generate_plan()
                    # The runtime's execution responsibilities remain unaffected: the
                    # skeleton still resolves the steps it needs to execute.
                    self.assertEqual(runner.workflow_id, workflow_id)
                    self.assertTrue(os.path.exists(runner.plan_out))
                    self._assert_provisional(runner, workflow_id)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_finalization_produces_contract_valid_plan_each_fog(self):
        """After a valid brief, finalize_plan() yields a contract-valid canonical plan."""
        tmp = tempfile.mkdtemp()
        try:
            for fog_type, impl in FOG_TO_WORKFLOW.items():
                with self.subTest(fog_type=fog_type):
                    runner = self._runner("fast-local-diagnostic", tmpdir=tmp)
                    runner.generate_plan()
                    brief = _write_controlled_brief(fog_type)
                    result = runner.finalize_plan(brief)
                    self.assertIsNotNone(result,
                                         f"finalize_plan returned None for fog_type={fog_type}")
                    self._assert_finalized(runner, fog_type)

                    ok_generic, out_generic = _run(
                        "validate-artifact.py", "workflow_orchestration_plan", runner.plan_out)
                    self.assertTrue(ok_generic,
                                    f"validate-artifact.py failed for {fog_type}:\n{out_generic}")
                    ok_plan, out_plan = _run(
                        "validate-plan.py", "workflow_orchestration_plan", runner.plan_out)
                    self.assertTrue(ok_plan,
                                    f"validate-plan.py failed for {fog_type}:\n{out_plan}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_finalization_honors_brief_evidence_and_rejects_no_diagnosis(self):
        """Finalization consumes real brief evidence and no-ops without a diagnosis."""
        tmp = tempfile.mkdtemp()
        try:
            runner = self._runner("full-local-sensemaking", tmpdir=tmp)
            runner.generate_plan()
            brief = _write_controlled_brief("product_fog")
            runner.finalize_plan(brief)
            machine = _read_machine_block(runner.plan_out)
            self.assertEqual(machine.get("primary_fog_type"), "product_fog")
            self.assertEqual(machine.get("chosen_workflow_id"), "product-implementation-workflow")

            # Fresh provisional state: a brief without primary_fog_type must leave the
            # plan provisional (no fabricated diagnosis, no false finalization).
            runner2 = self._runner("fast-local-diagnostic", tmpdir=tmp)
            runner2.generate_plan()
            blank_brief = os.path.join(tmp, "blank-brief.md")
            with open(blank_brief, "w", encoding="utf-8") as f:
                f.write("# Brief\n\n```yaml\nartifact_id: repository_sensemaking_brief\n```\n")
            res = runner2.finalize_plan(blank_brief)
            self.assertIsNone(res, "finalize_plan must no-op when the brief has no fog type")
            self._assert_provisional(runner2, "fast-local-diagnostic")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def _write_brief_with_fog(self, fog_type, escalation):
        """Write a brief with a given fog_type and escalation flag; return path."""
        brief = os.path.join(tempfile.mkdtemp(), "edge-brief.md")
        with open(brief, "w", encoding="utf-8") as f:
            f.write("# Brief\n\n```yaml\nartifact_id: repository_sensemaking_brief\n"
                    f"primary_fog_type: {fog_type}\n"
                    f"escalation_recommended: {str(escalation).lower()}\n```\n")
        return brief

    def test_finalization_noops_on_unknown_fog_and_escalation(self):
        """A plan must not be finalized from evidence that yields no contract-valid routing."""
        tmp = tempfile.mkdtemp()
        try:
            # Unrecognized fog type: not a ratified canonical fog, so no valid selection.
            runner = self._runner("fast-local-diagnostic", tmpdir=tmp)
            runner.generate_plan()
            unknown = self._write_brief_with_fog("integration_fog", escalation=False)
            self.assertIsNone(runner.finalize_plan(unknown),
                              "finalize_plan must no-op on an unratified fog type")
            self._assert_provisional(runner, "fast-local-diagnostic")

            # Escalation recommended: the correct routing state is not a plain
            # fog-aligned selection, so the plan stays provisional.
            runner2 = self._runner("fast-local-diagnostic", tmpdir=tmp)
            runner2.generate_plan()
            esc = self._write_brief_with_fog("product_fog", escalation=True)
            self.assertIsNone(runner2.finalize_plan(esc),
                              "finalize_plan must no-op when the brief recommends escalation")
            self._assert_provisional(runner2, "fast-local-diagnostic")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_provisional_state_does_not_assert_final_workflow(self):
        """The conditional workflow's plan must not claim a final routing decision."""
        tmp = tempfile.mkdtemp()
        try:
            runner = self._runner("full-local-sensemaking", tmpdir=tmp)
            runner.generate_plan()
            with open(runner.plan_out, encoding="utf-8") as f:
                content = f.read()
            # The executing workflow is present as execution identity...
            self.assertIn("full-local-sensemaking", content)
            # ...but no implementation workflow is asserted as the final routing target.
            for impl in FOG_TO_WORKFLOW.values():
                self.assertNotIn(impl, content,
                                 f"provisional skeleton must not reference final routing target {impl}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
