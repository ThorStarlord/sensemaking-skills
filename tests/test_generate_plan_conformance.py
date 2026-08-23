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

The closure proof is:

    valid repository_sensemaking_brief
        -> PASS its real validator (validate-brief.py)
        -> finalize_plan(...)
        -> finalized workflow_orchestration_plan
        -> validate-artifact.py PASS
        -> validate-plan.py PASS

so the input brief is proven valid through the repository's real brief validator
before any finalization is exercised. These tests exercise the real
producer/finalization/validator path, not a parallel test-only implementation. The
test does not copy the runtime's private fog->workflow mapping: routing correctness
is proven by the real validate-plan.py contract gate, and preference for the brief's
`recommended_workflow_id` is asserted directly against the brief's own field value.
"""

import os
import sys
import tempfile
import re
import shutil
import subprocess
import importlib.util
import unittest

import yaml

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
scripts_dir = os.path.join(REPO_ROOT, "scripts")
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

# The canonical valid brief fixture (known to pass validate-brief.py) is adapted for
# each case so the input brief is a genuine contract-valid brief, not a YAML stub.
VALID_BRIEF_FIXTURE = os.path.join(
    REPO_ROOT, "tests", "fixtures", "validate-brief", "valid", "valid-brief.md"
)

# A canonical VALID escalated brief (escalation_recommended: true, recommended_workflow_id:
# null, ratified primary_fog_type: architecture_fog), known to pass validate-brief.py.
VALID_ESCALATED_BRIEF_FIXTURE = os.path.join(
    REPO_ROOT, "tests", "fixtures", "validate-brief", "valid", "no-match-with-escalation.md"
)

# A real, distinct, non-fog-default registry workflow with a contract-valid plan. It
# must differ from every fog-aligned default so the test proves a brief recommendation
# that is NOT merely reconstructed from a fog map is honored. product-discovery-sprint
# is a product-family workflow that differs from product-implementation-workflow.
DISTINCT_RECOMMENDED_WORKFLOW = "product-discovery-sprint"

# The fog -> default implementation workflow mapping, taken from validate-plan.py's OWN
# fog_to_workflow (the consumer/routing authority), NOT from the runtime's private
# _FOG_TO_WORKFLOW. The test uses it only to construct realistic valid briefs whose
# recommendation the producer must honor; it never asserts the producer "should" have
# produced a value from the runtime's private map.
VALIDATOR_FOG_TO_DEFAULT_WORKFLOW = {
    "product_fog": "product-implementation-workflow",
    "ui_fog": "ui-implementation-workflow",
    "docs_fog": "docs-implementation-workflow",
    "architecture_fog": "architecture-implementation-workflow",
}

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
    """Parse the LAST fenced ```yaml machine block from an artifact.

    The plan has its single machine block (Section 11); a brief's authoritative machine
    block is the Section 13 handoff, which is the last yaml fence in the canonical valid
    fixtures (Section 8 "Evidence excerpts" is an earlier fence). Reading the last fence
    is therefore correct for both the finalized plan and the brief.
    """
    with open(path, encoding="utf-8") as f:
        content = f.read()
    blocks = re.findall(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)
    if not blocks:
        return {}
    return (yaml.safe_load(blocks[-1]) or {})


def _write_valid_brief(fog_type, recommended_workflow_id):
    """Adapt the canonical valid brief to a given fog type + recommendation.

    Only the machine fields and the Section 11/12 recommendation references are
    changed; every evidence/prose section is carried over verbatim from the canonical
    valid fixture so quote-grounding and required sections remain intact.
    """
    with open(VALID_BRIEF_FIXTURE, encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r"primary_fog_type: [a-z_]+",
                     f"primary_fog_type: {fog_type}", content)
    content = re.sub(r"recommended_workflow_id: [a-z\-]+",
                     f"recommended_workflow_id: {recommended_workflow_id}", content)
    content = re.sub(
        r"## 12\. Recommended workflow\n[a-z\-]+",
        f"## 12. Recommended workflow\n{recommended_workflow_id}", content)
    tmp = tempfile.mkdtemp()
    brief_path = os.path.join(tmp, "repository_sensemaking_brief.md")
    with open(brief_path, "w", encoding="utf-8") as f:
        f.write(content)
    return brief_path


def _copy_brief_fixture(fixture_path):
    """Copy a canonical brief fixture verbatim to a writable temp path."""
    tmp = tempfile.mkdtemp()
    brief_path = os.path.join(tmp, "repository_sensemaking_brief.md")
    with open(fixture_path, encoding="utf-8") as src:
        content = src.read()
    with open(brief_path, "w", encoding="utf-8") as f:
        f.write(content)
    return brief_path


def _assert_valid_brief(self, brief_path):
    """Prove the input brief passes the repository's real brief validator."""
    ok, out = _run("validate-brief.py", "repository_sensemaking_brief", brief_path)
    self.assertTrue(ok, f"controlled brief must pass validate-brief.py:\n{out}")


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

    def _assert_doubly_valid(self, runner, machine):
        """Finalized plan must carry the required contract fields and pass BOTH validators.

        This is the closure proof for the common fog-aligned finalization path: the
        finalized canonical plan passes validate-artifact.py and validate-plan.py with no
        manual repair.
        """
        # Required machine fields (artifact-contracts.yaml).
        self.assertEqual(machine.get("artifact_id"), "workflow_orchestration_plan")
        self.assertIn("primary_fog_type", machine)
        self.assertIn("chosen_workflow_id", machine)
        self.assertIn("routing_decision_method", machine)
        self.assertTrue(machine.get("workflow_steps"),
                        "finalized plan must carry a non-empty workflow_steps array")
        self.assertTrue(machine.get("created_at"), "finalized plan must carry created_at")
        # No stale plan-level recommendation field; selection is chosen_workflow_id.
        self.assertNotIn("recommended_workflow_id", machine,
                         "the plan's authoritative selection field is chosen_workflow_id")
        # Pass the real validators, no manual repair.
        ok_generic, out_generic = _run(
            "validate-artifact.py", "workflow_orchestration_plan", runner.plan_out)
        self.assertTrue(ok_generic,
                        f"validate-artifact.py failed:\n{out_generic}")
        ok_plan, out_plan = _run(
            "validate-plan.py", "workflow_orchestration_plan", runner.plan_out)
        self.assertTrue(ok_plan,
                        f"validate-plan.py failed:\n{out_plan}")

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
        """After a VALID brief, finalize_plan() yields a doubly-valid canonical plan.

        For each fog the brief recommends the fog-aligned default (repo-sensemaker's
        natural output). The finalized plan then represents a recommendation that equals
        the selection, recorded as `diagnosis_primary_soft_context`, and must pass both
        validate-artifact.py AND validate-plan.py (the closure proof).
        """
        tmp = tempfile.mkdtemp()
        try:
            for fog_type, recommended in VALIDATOR_FOG_TO_DEFAULT_WORKFLOW.items():
                with self.subTest(fog_type=fog_type):
                    brief = _write_valid_brief(fog_type, recommended)
                    _assert_valid_brief(self, brief)

                    runner = self._runner("fast-local-diagnostic", tmpdir=tmp)
                    runner.generate_plan()
                    result = runner.finalize_plan(brief)
                    self.assertIsNotNone(result,
                                         f"finalize_plan returned None for fog_type={fog_type}")
                    machine = _read_machine_block(runner.plan_out)
                    # Evidence consumed: brief's primary_fog_type is present.
                    self.assertEqual(machine.get("primary_fog_type"), fog_type)
                    # The brief's recommendation is reflected as the system recommendation.
                    self.assertEqual(machine.get("system_recommended_workflow"), recommended)
                    # Selection defaults to the recommendation (no divergence).
                    self.assertEqual(machine.get("selected_workflow"), recommended)
                    self.assertIs(machine.get("routing_divergence"), False)
                    self.assertEqual(machine.get("chosen_workflow_id"), recommended)
                    self.assertEqual(machine.get("routing_decision_method"),
                                     "diagnosis_primary_soft_context")
                    self._assert_doubly_valid(runner, machine)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_finalization_honors_distinct_brief_recommendation(self):
        """A distinct valid brief recommendation is followed, with an honest audit.

        The brief recommends a distinct valid workflow (product-discovery-sprint) that
        differs from the fog-aligned default. The producer must consume THAT
        recommendation as the system recommendation, not silently derive the selection
        from a hard-coded fog map. The selection defaults to the recommendation, so
        routing_divergence is truthfully false and the method is the ordinary
        diagnosis method - NOT `user_explicit_override` (a deviation from the fog
        default is NOT an override). The plan must pass both validators.
        """
        tmp = tempfile.mkdtemp()
        try:
            brief = _write_valid_brief("product_fog", DISTINCT_RECOMMENDED_WORKFLOW)
            _assert_valid_brief(self, brief)

            runner = self._runner("fast-local-diagnostic", tmpdir=tmp)
            runner.generate_plan()
            result = runner.finalize_plan(brief)
            self.assertIsNotNone(result)
            machine = _read_machine_block(runner.plan_out)
            # The distinct recommendation is preserved as the system recommendation.
            self.assertEqual(machine.get("system_recommended_workflow"),
                             DISTINCT_RECOMMENDED_WORKFLOW)
            # Selection defaults to the recommendation and matches it.
            self.assertEqual(machine.get("selected_workflow"), DISTINCT_RECOMMENDED_WORKFLOW)
            self.assertEqual(machine.get("chosen_workflow_id"), DISTINCT_RECOMMENDED_WORKFLOW)
            self.assertIs(machine.get("routing_divergence"), False,
                          "selection equals recommendation, so divergence must be false")
            # Following a (possibly non-fog-default) system recommendation is NOT an
            # override; the ordinary diagnosis method is used, and the plan still passes
            # both validators because the validator audit compares selection against the
            # system recommendation (fog map is only a fallback recommendation).
            self.assertEqual(machine.get("routing_decision_method"),
                             "diagnosis_primary_soft_context")
            self._assert_doubly_valid(runner, machine)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_explicit_authorized_selection_sets_truthful_divergence(self):
        """An explicit selected_workflow_id override is preserved with truthful audit.

        The explicit selection differs from the brief's recommendation, so
        routing_divergence must be truthfully True, and a non-default selection with an
        explicit override must pass both validators.
        """
        tmp = tempfile.mkdtemp()
        try:
            brief = _write_valid_brief("product_fog", "product-implementation-workflow")
            _assert_valid_brief(self, brief)

            runner = self._runner("fast-local-diagnostic", tmpdir=tmp)
            runner.generate_plan()
            result = runner.finalize_plan(
                brief, selected_workflow_id=DISTINCT_RECOMMENDED_WORKFLOW)
            self.assertIsNotNone(result)
            machine = _read_machine_block(runner.plan_out)
            # The explicit selection is preserved.
            self.assertEqual(machine.get("chosen_workflow_id"), DISTINCT_RECOMMENDED_WORKFLOW)
            self.assertEqual(machine.get("selected_workflow"), DISTINCT_RECOMMENDED_WORKFLOW)
            # The brief's recommendation is the system recommendation.
            self.assertEqual(machine.get("system_recommended_workflow"),
                             "product-implementation-workflow")
            # Selection differs from recommendation -> truthful divergence.
            self.assertIs(machine.get("routing_divergence"), True)
            self.assertEqual(machine.get("routing_decision_method"), "user_explicit_override")
            self._assert_doubly_valid(runner, machine)

            # An invalid explicit selection must not fabricate a plan.
            runner2 = self._runner("fast-local-diagnostic", tmpdir=tmp)
            runner2.generate_plan()
            res2 = runner2.finalize_plan(brief, selected_workflow_id="not-a-real-workflow")
            self.assertIsNone(res2,
                              "finalize_plan must no-op when the explicit selection is invalid")
            self._assert_provisional(runner2, "fast-local-diagnostic")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_selection_diverges_from_recommendation_without_override_fails(self):
        """A selection diverging from the system recommendation needs an authorized method.

        The routing-audit gate must not be weakened: when the selection differs from the
        system recommendation and routing_decision_method is NOT an authorized divergence
        method (here the ordinary soft-context method), validate-plan.py must fail with a
        semantic_conflict. Following the system recommendation is fine even when it is a
        non-fog-default workflow; DIVERGING from it without an override is not.
        """
        tmp = tempfile.mkdtemp()
        try:
            # Brief recommends the fog-default; a finalized (non-override) plan selects it.
            brief = _write_valid_brief("product_fog", "product-implementation-workflow")
            _assert_valid_brief(self, brief)
            runner = self._runner("fast-local-diagnostic", tmpdir=tmp)
            runner.generate_plan()
            self.assertIsNotNone(runner.finalize_plan(brief))
            # Force the SELECTION to diverge from the system recommendation with the
            # ordinary (non-override) diagnosis method.
            with open(runner.plan_out, encoding="utf-8") as f:
                content = f.read()
            content = content.replace(
                "selected_workflow: product-implementation-workflow",
                f"selected_workflow: {DISTINCT_RECOMMENDED_WORKFLOW}")
            content = content.replace(
                "chosen_workflow_id: product-implementation-workflow",
                f"chosen_workflow_id: {DISTINCT_RECOMMENDED_WORKFLOW}")
            with open(runner.plan_out, "w", encoding="utf-8") as f:
                f.write(content)
            ok_generic, _ = _run(
                "validate-artifact.py", "workflow_orchestration_plan", runner.plan_out)
            self.assertTrue(ok_generic,
                            "validate-artifact.py still passes (method is a canonical value)")
            ok_plan, out_plan = _run(
                "validate-plan.py", "workflow_orchestration_plan", runner.plan_out)
            self.assertFalse(ok_plan,
                             "selection diverging from the system recommendation without an "
                             "authorized override method must fail validate-plan.py")
            self.assertIn("semantic_conflict", out_plan)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_finalization_rejects_no_diagnosis(self):
        """Finalization no-ops (stays provisional) when the brief has no fog type."""
        tmp = tempfile.mkdtemp()
        try:
            runner = self._runner("fast-local-diagnostic", tmpdir=tmp)
            runner.generate_plan()
            blank_brief = os.path.join(tmp, "blank-brief.md")
            with open(blank_brief, "w", encoding="utf-8") as f:
                f.write("# Brief\n\n```yaml\nartifact_id: repository_sensemaking_brief\n```\n")
            res = runner.finalize_plan(blank_brief)
            self.assertIsNone(res, "finalize_plan must no-op when the brief has no fog type")
            self._assert_provisional(runner, "fast-local-diagnostic")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_finalization_noops_on_unknown_fog_and_escalation(self):
        """A plan must not be finalized from evidence that yields no contract-valid routing."""
        tmp = tempfile.mkdtemp()
        try:
            # Unrecognized fog type: not a ratified canonical fog, so no valid selection.
            runner = self._runner("fast-local-diagnostic", tmpdir=tmp)
            runner.generate_plan()
            unknown = _write_valid_brief("architecture_fog", "product-implementation-workflow")
            # Override the machine block's fog to an unratified value so we can reach the
            # producer's unratified-fog guard deterministically.
            with open(unknown, encoding="utf-8") as f:
                content = f.read()
            content = content.replace("primary_fog_type: architecture_fog",
                                      "primary_fog_type: integration_fog")
            with open(unknown, "w", encoding="utf-8") as f:
                f.write(content)
            self.assertIsNone(runner.finalize_plan(unknown),
                              "finalize_plan must no-op on an unratified fog type")
            self._assert_provisional(runner, "fast-local-diagnostic")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_finalization_noops_on_escalated_brief(self):
        """An escalated valid brief must not be finalized (no fabricated selection).

        Start from a VALID repository_sensemaking_brief with a ratified primary_fog_type
        and escalation_recommended: true. finalize_plan() must return None, leave the
        Phase-2 plan provisional, and fabricate no final routing selection, because
        escalation routing is outside this fog-aligned finalization (ADR 0014).
        """
        tmp = tempfile.mkdtemp()
        try:
            escalation_brief = _copy_brief_fixture(VALID_ESCALATED_BRIEF_FIXTURE)
            _assert_valid_brief(self, escalation_brief)
            # Sanity: this is a ratified fog with escalation recommended.
            machine = _read_machine_block(escalation_brief)
            self.assertEqual(machine.get("primary_fog_type"), "architecture_fog")
            self.assertIs(machine.get("escalation_recommended"), True)

            runner = self._runner("fast-local-diagnostic", tmpdir=tmp)
            runner.generate_plan()
            result = runner.finalize_plan(escalation_brief)
            self.assertIsNone(result,
                              "finalize_plan must no-op when the brief recommends escalation")
            self._assert_provisional(runner, "fast-local-diagnostic")
            # No final routing selection is fabricated.
            with open(runner.plan_out, encoding="utf-8") as f:
                provisional_content = f.read()
            self.assertNotIn("product-implementation-workflow", provisional_content)
            self.assertNotIn("primary_fog_type", _read_machine_block(runner.plan_out))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_provisional_state_does_not_assert_final_workflow(self):
        """The conditional workflow's plan must not claim a final routing decision."""
        tmp = tempfile.mkdtemp()
        try:
            runner = self._runner("full-local-sensemaking", tmpdir=tmp)
            runner.generate_plan()
            # The executing workflow is present as execution identity...
            self.assertEqual(runner.workflow_id, "full-local-sensemaking")
            machine = _read_machine_block(runner.plan_out)
            self.assertEqual(machine.get("chosen_workflow_id"), "full-local-sensemaking")
            # ...and no primary_fog_type is asserted (the plan pre-dates diagnosis).
            self.assertNotIn("primary_fog_type", machine)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
