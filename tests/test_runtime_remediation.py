"""PR #242 remediation regressions (directive #28).

Covers:
- #1 phase order: execute_step runs producer -> validation -> MODEL_WARRANT eval
  (warrant consumes the NEWLY produced validated brief, not a stale/nonexistent one).
- #2 target-revision identity: warrant target_revision is the exact target-checkout
  SHA (git -C <target> rev-parse HEAD), never a framework branch name; fails closed.
- #3 PARTIAL materialization is scoped to the producer-declared needed_representation
  (not all diagnostic probes).
- Fail-closed on applicable enabled warrant-seam operational failure (directive #29):
  -> INCONCLUSIVE-equivalent record / safe stop; ACTION does not route; explicit
  NO_CHANGE does not terminalize; no representation materialized; warrant_enabled=false
  legacy unchanged; non-applicable step unchanged.
"""
import os
import unittest
from unittest.mock import MagicMock, patch

from sensemaking_skills.reasoning.evidence_probes import EvidenceInput
from sensemaking_skills.reasoning.warrant_gate import run_seam_warrant

import importlib.util
import sys
_scripts = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if _scripts not in sys.path:
    sys.path.insert(0, _scripts)
if "workflow_runtime" not in sys.modules:
    _spec = importlib.util.spec_from_file_location(
        "workflow_runtime", os.path.join(_scripts, "workflow-runtime.py"))
    _wr = importlib.util.module_from_spec(_spec)
    sys.modules["workflow_runtime"] = _wr
    _spec.loader.exec_module(_wr)
else:
    _wr = sys.modules["workflow_runtime"]
OrchestrationRunner = _wr.OrchestrationRunner

import skill_executor  # scripts/ on sys.path
SkillExecutionResult = skill_executor.SkillExecutionResult
SkillExecutionStatus = skill_executor.SkillExecutionStatus

import yaml


VALID_BRIEF = """# Repository Sensemaking Brief

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: docs_fog
primary_fog_type: docs_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "a.py (lines L10-L15): a"
recommended_workflow_id: docs-implementation-workflow
recommended_execution_mode: plan_only
weakest_boundary: some-boundary
weakness_type: Other
weakness_type_explanation: test
required_inputs:
  - user_intent
created_at: "2026-08-29T00:00:00Z"
immutable: true
representation_sufficiency:
  status: sufficient
  rationale: native evidence suffices for this consequential problem
  needed_representation: null
```
"""


class FakeRealExecutor:
    supports_real_execution = True

    def __init__(self, brief_text):
        self.brief_text = brief_text
        self.invoked = False
        self.saw_probe_path = None
        self.wrote_path = None

    def invoke_skill(self, skill_id, invocation_command, input_artifacts, expected_output_artifact, context):
        self.invoked = True
        path = context.get("expected_output_path")
        self.saw_probe_path = context.get("expected_probe_report_path")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.brief_text)
            self.wrote_path = path
        return SkillExecutionResult(
            skill_id=skill_id,
            status=SkillExecutionStatus.EXECUTED,
            command=invocation_command,
            output_artifact=expected_output_artifact,
        )


class TestPhaseOrder(unittest.TestCase):
    """#1: producer executes before MODEL_WARRANT evaluation over the produced brief."""

    def _runner(self, executor, brief_path):
        r = object.__new__(OrchestrationRunner)
        r.mode = "guided_execution"
        r.warrant_enabled = True
        r.use_fixtures = False
        r.repo_root = "."
        r.target_repo = "."
        r.workflow_id = "phb-remediation-test"
        r.log_dir = "."
        r.skill_executor = executor
        r.errors = []
        r.step_results = []
        r.gate_decisions = []
        r.session_id = "test-phaseseq"
        r.artifact_session_dir = None
        r._episode_probe_report_path = None
        r.contracts = None
        r._resolve_artifact_path = MagicMock(return_value=brief_path)
        r._resolve_step_inputs = MagicMock(return_value=([], {}))
        r._log_ledger_event = MagicMock()
        r._ensure_intent_ref = MagicMock()
        r._compute_file_hash = MagicMock(return_value="abc")
        r._run_validator_stack = MagicMock(
            return_value=[{"command": "x", "result": "PASSED"}])
        r._manage_gate = MagicMock(side_effect=lambda g, s, sk: "approved")
        r._finalize_step_result = OrchestrationRunner._finalize_step_result.__get__(r, OrchestrationRunner)
        r._read_brief_machine_data = OrchestrationRunner._read_brief_machine_data.__get__(r, OrchestrationRunner)
        r._read_brief_outcome = OrchestrationRunner._read_brief_outcome.__get__(r, OrchestrationRunner)
        r._current_target_revision = MagicMock(return_value="3a8bfc4d")
        return r

    def test_producer_runs_before_warrant_and_consumes_produced_brief(self):
        # brief lives under repo_root so os.path.relpath (same drive) works.
        brief_path = os.path.abspath(os.path.join(
            "artifacts-test-phaseseq", "repository_sensemaking_brief.md"))
        os.makedirs(os.path.dirname(brief_path), exist_ok=True)
        executor = FakeRealExecutor(VALID_BRIEF)
        runner = self._runner(executor, brief_path)
        # The producer has NOT run yet; before execute_step the brief must NOT exist
        # (so a pre-executor warrant could only see a stale/nonexistent brief).
        if os.path.exists(brief_path):
            os.remove(brief_path)
        self.assertFalse(os.path.exists(brief_path),
                         "brief should not pre-exist before producer runs")
        step = {"skill": "repo-sensemaker",
                "output_artifact": "repository_sensemaking_brief",
                "step_type": "local_execution"}
        result = runner.execute_step(step, 1, 1)
        # Producer executed FIRST: executor.invoke_skill was called and wrote the brief.
        self.assertTrue(executor.invoked, "producer executor must be invoked")
        self.assertTrue(os.path.exists(brief_path), "producer must write the brief")
        # The produced brief carried a 'sufficient' assessment -> the REAL warrant seam
        # (not mocked) must yield NO, proving it consumed the produced brief, not a stale one.
        self.assertEqual(result.get("warrant"), "NO",
                         f"warrant must consume the produced sufficient brief, got {result.get('warrant')}")
        # NOT gated (conclusive NO) -> no STOPPED_WITHOUT_ACTION
        self.assertNotEqual(result.get("terminal_outcome"), "STOPPED_WITHOUT_ACTION")
        self.assertNotEqual(result.get("gate_result"), "blocked_inconclusive")
        # clean up the produced brief
        import shutil
        shutil.rmtree(os.path.dirname(brief_path), ignore_errors=True)


class TestTargetRevisionIdentity(unittest.TestCase):
    """#2: warrant target_revision is the exact TARGET-checkout SHA, never framework branch."""

    def test_target_revision_uses_exact_target_sha(self):
        runner = object.__new__(OrchestrationRunner)
        runner.repo_root = "/nonexistent-framework-repo"  # DIFFERENT from target
        runner.target_repo = "."
        # The target repo (".") has a real exact HEAD SHA; the framework repo is different.
        rev = OrchestrationRunner._current_target_revision.__get__(runner, OrchestrationRunner)()
        self.assertRegex(rev, r"^[0-9a-f]{40}$",
                         f"expected exact 40-char target SHA, got {rev!r}")
        # It must NOT be a branch name of the framework repo.
        self.assertNotEqual(rev, "phb-conditional-representation-candidate")

    def test_target_revision_fails_closed_when_unestablishable(self):
        runner = object.__new__(OrchestrationRunner)
        runner.repo_root = "."
        runner.target_repo = "/definitely/not/a/git/repo/xyz"
        rev = OrchestrationRunner._current_target_revision.__get__(runner, OrchestrationRunner)()
        self.assertEqual(rev, "unknown")

    def test_probe_report_not_consumed_when_revision_unknown(self):
        # Constructor path: _run_seam_warrant must NOT consume a probe-report when the
        # target revision is not authoritative (fail closed -> probe stays UNKNOWN).
        runner = object.__new__(OrchestrationRunner)
        runner.repo_root = "."
        runner.target_repo = "/not/a/git/repo"
        runner._resolve_artifact_path = MagicMock(return_value="/tmp/nonexistent-brief.md")
        runner._read_brief_machine_data = MagicMock(return_value={})
        runner._episode_probe_report_path = "/some/stale/probe-report.yaml"
        runner._current_target_revision = MagicMock(return_value="unknown")
        runner.user_goal_hint = MagicMock(return_value="g")
        with patch("os.path.exists", return_value=True), \
             patch("builtins.open", return_value=MagicMock()):
            rec = OrchestrationRunner._run_seam_warrant.__get__(runner, OrchestrationRunner)(
                "repository_sensemaking_brief", "repo-sensemaker")
        # Even though a stale probe-report "exists" at the path, revision-unknown means
        # it must NOT be consumed -> INCONCLUSIVE (safe), not revision-bound evidence.
        self.assertIsNotNone(rec)
        self.assertEqual(rec.warrant, "INCONCLUSIVE")
        self.assertFalse(rec.representation_materialized)


class TestPartialBoundedMaterialization(unittest.TestCase):
    """#3: PARTIAL representation is scoped to the producer-declared needed_representation."""

    def test_partial_scoped_to_needed_representation(self):
        ev = EvidenceInput(
            representation_sufficiency={
                "status": "insufficient_bounded",
                "rationale": "specific consequential gap: execution relationship A->B absent",
                "needed_representation": "bounded execution-flow projection A -> B -> C",
            },
            brief_machine={"evidence": ["a.py:1 x"]},
            evidence_lines=["a.py:1 x"],
        )
        rec = run_seam_warrant(target_repository="t", target_revision="r",
                               user_goal="g", evidence=ev)
        self.assertEqual(rec.warrant, "PARTIAL")
        self.assertTrue(rec.representation_materialized)
        rep = rec.representation or {}
        self.assertEqual(rep.get("warranted_representation"),
                         "bounded execution-flow projection A -> B -> C")
        self.assertIn("rationale", rep)
        # Diagnostics are telemetry, NOT the warranted scope.
        self.assertIn("diagnostic_probes", rep)
        self.assertNotIn("behavioral_flow_unassembled", rep.get("scope", {}))
        self.assertNotIn("scope", rep)

    def test_partial_default_when_needed_representation_missing(self):
        ev = EvidenceInput(
            representation_sufficiency={
                "status": "insufficient_bounded",
                "rationale": "gap",
                "needed_representation": "",
            },
            brief_machine={"evidence": ["a.py:1 x"]}, evidence_lines=["a.py:1 x"],
        )
        # fail-closed: no bounded needed_representation -> INCONCLUSIVE (not PARTIAL).
        rec = run_seam_warrant(target_repository="t", target_revision="r",
                               user_goal="g", evidence=ev)
        self.assertEqual(rec.warrant, "INCONCLUSIVE")


class TestFailClosedWarrantFailure(unittest.TestCase):
    """Directive #29: an applicable enabled warrant-seam operational failure must
    FAIL CLOSED to an INCONCLUSIVE-equivalent safe stop (never route ACTION,
    never terminalize NO_CHANGE, never materialize representation)."""

    def _runner(self, executor, brief_path, brief_text):
        r = object.__new__(OrchestrationRunner)
        r.mode = "guided_execution"
        r.warrant_enabled = True
        r.use_fixtures = False
        r.repo_root = "."
        r.target_repo = "."
        r.workflow_id = "phb-failclosed-test"
        r.log_dir = "."
        r.skill_executor = executor
        r.errors = []
        r.step_results = []
        r.gate_decisions = []
        r.session_id = "test-failclosed"
        r.artifact_session_dir = None
        r._episode_probe_report_path = None
        r.contracts = None
        r._resolve_artifact_path = MagicMock(return_value=brief_path)
        r._resolve_step_inputs = MagicMock(return_value=([], {}))
        r._log_ledger_event = MagicMock()
        r._ensure_intent_ref = MagicMock()
        r._compute_file_hash = MagicMock(return_value="abc")
        r._run_validator_stack = MagicMock(return_value=[{"command": "x", "result": "PASSED"}])
        r._manage_gate = MagicMock(side_effect=lambda g, s, sk: "approved")
        r._finalize_step_result = OrchestrationRunner._finalize_step_result.__get__(r, OrchestrationRunner)
        r._read_brief_machine_data = OrchestrationRunner._read_brief_machine_data.__get__(r, OrchestrationRunner)
        r._read_brief_outcome = OrchestrationRunner._read_brief_outcome.__get__(r, OrchestrationRunner)
        r._current_target_revision = MagicMock(return_value="3a8bfc4d")
        r.user_goal_hint = MagicMock(return_value="g")
        return r

    def _run_with_failing_seam(self, brief_text):
        brief_path = os.path.abspath(os.path.join("artifacts-test-failclosed",
                                                  "repository_sensemaking_brief.md"))
        os.makedirs(os.path.dirname(brief_path), exist_ok=True)
        if os.path.exists(brief_path):
            os.remove(brief_path)
        executor = FakeRealExecutor(brief_text)
        runner = self._runner(executor, brief_path, brief_text)
        step = {"skill": "repo-sensemaker",
                "output_artifact": "repository_sensemaking_brief",
                "step_type": "local_execution"}
        # Make the REAL warrant seam fail operationally at the applicable step.
        with patch("sensemaking_skills.reasoning.warrant_gate.run_seam_warrant",
                   side_effect=RuntimeError("boom")):
            result = runner.execute_step(step, 1, 1)
        import shutil
        shutil.rmtree(os.path.dirname(brief_path), ignore_errors=True)
        return result

    def test_fail_closed_safe_stop_on_operational_failure(self):
        result = self._run_with_failing_seam(VALID_BRIEF)
        self.assertEqual(result.get("warrant"), "INCONCLUSIVE")
        self.assertEqual(result.get("terminal_outcome"), "STOPPED_WITHOUT_ACTION")
        self.assertIn("MODEL_WARRANT_INCONCLUSIVE", result.get("terminal_reason", ""))
        self.assertEqual(result.get("gate_result"), "blocked_inconclusive")

    def test_fail_closed_never_routes_action(self):
        # An explicit ACTION brief + operational failure must NOT proceed to action/routing.
        result = self._run_with_failing_seam(VALID_BRIEF)  # VALID_BRIEF is ACTION (docs workflow)
        self.assertEqual(result.get("terminal_outcome"), "STOPPED_WITHOUT_ACTION")
        self.assertNotEqual(result.get("status"), "APPROVED")
        self.assertNotEqual(result.get("status"), "VALIDATED")

    def test_fail_closed_never_terminalizes_no_change(self):
        # An explicit NO_CHANGE brief + operational failure must NOT terminalize NO_CHANGE.
        no_change_brief = VALID_BRIEF.replace(
            "outcome: null", "outcome: NO_REPOSITORY_CHANGE_WARRANTED")
        # Build a NO_CHANGE brief by replacing the outcome + nulling workflow.
        nc = VALID_BRIEF.replace(
            "recommended_workflow_id: docs-implementation-workflow",
            "recommended_workflow_id: null")
        result = self._run_with_failing_seam(nc)
        self.assertEqual(result.get("terminal_outcome"), "STOPPED_WITHOUT_ACTION")
        self.assertNotEqual(result.get("terminal_outcome"), "NO_REPOSITORY_CHANGE_WARRANTED")
        self.assertNotEqual(result.get("status"), "SUCCESS_NO_CHANGE")

    def test_fail_closed_no_representation(self):
        result = self._run_with_failing_seam(VALID_BRIEF)
        wrec = result.get("warrant_record", {})
        self.assertFalse(wrec.get("representation_materialized", False))

    def test_warrant_disabled_legacy_unchanged(self):
        # warrant_enabled=false: the seam block is skipped entirely (no fail-closed gate).
        executor = FakeRealExecutor(VALID_BRIEF)
        brief_path = os.path.abspath(os.path.join("artifacts-test-failclosed",
                                                  "repository_sensemaking_brief.md"))
        os.makedirs(os.path.dirname(brief_path), exist_ok=True)
        if os.path.exists(brief_path):
            os.remove(brief_path)
        r = self._runner(executor, brief_path, VALID_BRIEF)
        r.warrant_enabled = False
        step = {"skill": "repo-sensemaker",
                "output_artifact": "repository_sensemaking_brief",
                "step_type": "local_execution"}
        result = r.execute_step(step, 1, 1)
        import shutil
        shutil.rmtree(os.path.dirname(brief_path), ignore_errors=True)
        self.assertNotIn("warrant", result)

    def test_non_applicable_still_none(self):
        # A non-applicable skill/artifact still yields None (fail-closed is scoped
        # to the applicable repo-sensemaker brief step; None is NOT globally redefined).
        runner = object.__new__(OrchestrationRunner)
        runner.repo_root = "."
        runner.target_repo = "."
        runner._resolve_artifact_path = MagicMock(return_value="/tmp/x.md")
        rec = OrchestrationRunner._run_seam_warrant.__get__(runner, OrchestrationRunner)(
            "workflow_orchestration_plan", "workflow-planner")
        self.assertIsNone(rec)


if __name__ == "__main__":
    unittest.main()
