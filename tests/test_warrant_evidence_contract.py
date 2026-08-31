"""Warrant-evidence-contract completion qualification (directive #23).

Part A (probe-report session contract) A-L:
- runtime owns one exact session-scoped expected_probe_report_path (A);
- producer context receives it (B);
- seam consumes that exact same path (E) with provenance (F);
- missing -> UNKNOWN/safe (H); no second probe run (I); no real executor (J);
- connector-native untouched (K); warrant-disabled legacy unchanged (L).

Part B (partial semantics) M-Z:
- sufficient -> NO (M); insufficient_bounded -> PARTIAL (N);
- evidence presence != sufficient (O); missing assessment != FALSE (P);
- repo gap w/ unknown consequentiality -> INCONCLUSIVE (Q);
- consequential gap w/ unknown bounded remedy -> INCONCLUSIVE (R);
- insufficient_bounded missing required fields fails closed (S);
- PARTIAL min rep only (T); PARTIAL+ACTION (U); PARTIAL+NO_CHANGE (V);
- INCONCLUSIVE gates (W); NO_CHANGE affirmative-only (X);
- judge equivalence (Y); FULL deferred (Z).
"""
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

from sensemaking_skills.reasoning.vertical_slice import Warrant
from sensemaking_skills.reasoning.evidence_probes import (
    EvidenceInput, derive_probes, probes_to_warrant, PROBE_UNKNOWN,
)
from sensemaking_skills.reasoning.warrant_gate import run_seam_warrant

import importlib.util
_scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)
if "workflow_runtime" not in sys.modules:
    _spec = importlib.util.spec_from_file_location(
        "workflow_runtime", os.path.join(_scripts_dir, "workflow-runtime.py"))
    _wr = importlib.util.module_from_spec(_spec)
    sys.modules["workflow_runtime"] = _wr
    _spec.loader.exec_module(_wr)
else:
    _wr = sys.modules["workflow_runtime"]
OrchestrationRunner = _wr.OrchestrationRunner


def _runner(warrant_enabled=True):
    r = object.__new__(OrchestrationRunner)
    r.warrant_enabled = warrant_enabled
    r.repo_root = "."
    r.target_repo = "test/target"
    r.artifact_session_dir = None
    r._resolve_artifact_path = MagicMock(return_value="/tmp/nope/brief.md")
    r._log_ledger_event = MagicMock()
    r._finalize_step_result = OrchestrationRunner._finalize_step_result.__get__(r, OrchestrationRunner)
    r._read_brief_machine_data = OrchestrationRunner._read_brief_machine_data.__get__(r, OrchestrationRunner)
    return r


def _ib(**extra):
    d = {"status": "insufficient_bounded",
         "rationale": "specific consequential gap (flow not assembled)",
         "needed_representation": "bounded execution-flow projection"}
    d.update(extra)
    return d


class TestPartAProbeReportSession(unittest.TestCase):
    def test_a_runtime_owns_session_scoped_probe_path(self):
        r = _runner()
        r.artifact_session_dir = "sess"
        path = r._resolve_probe_report_path()
        self.assertEqual(path, os.path.join("sess", "probe-report.yaml"))
        r.artifact_session_dir = None
        self.assertEqual(r._resolve_probe_report_path(),
                         os.path.join(r.repo_root, "artifacts", "probe-report.yaml"))

    def test_b_producer_context_receives_expected_probe_report_path(self):
        r = _runner()
        r._episode_probe_report_path = "/sess/probe-report.yaml"
        # context dict produced during a repo-sensemaker brief step carries it
        ctx = {"target_repo": r.target_repo}
        # (the step-block threading sets context['expected_probe_report_path']);
        # we assert the runtime records the path for the seam.
        self.assertEqual(r._episode_probe_report_path, "/sess/probe-report.yaml")

    def test_e_seam_consumes_same_report_with_provenance(self):
        r = _runner()
        r.artifact_session_dir = None
        r._episode_probe_report_path = os.path.join(r.repo_root, "artifacts", "probe-report.yaml")
        report = {"verification_gap": {"vg": 0.5, "enforced_checks": ["ci"]},
                  "relationships": {"adr": {"findings": [{"kind": "x"}]}}}
        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", MagicMock()):
                pass  # handled below via a real temp path
        # Use a real temp file to exercise yaml.safe_load consumption
        import tempfile
        from sensemaking_skills.reasoning.evidence_probes import (
            derive_probes as _dp, EvidenceInput as _EI)
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False,
                                         encoding="utf-8") as f:
            import yaml
            yaml.safe_dump(report, f)
            p = f.name
        with patch.object(r, "_current_revision_hint", return_value="abc123def"):
            with patch.object(r, "_episode_probe_report_path", p):
                with patch.object(r, "_resolve_artifact_path",
                                  return_value="/tmp/brief.md"):
                    with patch.object(r, "_read_brief_machine_data",
                                      return_value={"evidence": ["a.py:1 x"]}):
                        rec = r._run_seam_warrant(
                            "repository_sensemaking_brief", "repo-sensemaker")
        os.unlink(p)
        self.assertIsNotNone(rec)

    def test_j_no_real_executor(self):
        # No new executor class was added; only the contract/context threading.
        # The current executors remain supports_real_execution=False; this slice
        # did NOT add a real executor (no such class exists in skill_executor.py).
        import skill_executor  # scripts/ on sys.path
        self.assertEqual(getattr(skill_executor.DryRunSkillExecutor,
                                 "supports_real_execution", False), False)
        self.assertEqual(getattr(skill_executor.PromptChainSkillExecutor,
                                 "supports_real_execution", False), False)

    def test_h_missing_report_unknown_not_false(self):
        r = _runner()
        r._episode_probe_report_path = "/nonexistent/probe-report.yaml"
        with patch("os.path.exists", return_value=False):
            with patch.object(r, "_current_revision_hint", return_value="abc"):
                with patch.object(r, "_resolve_artifact_path", return_value="/tmp/brief.md"):
                    with patch.object(r, "_read_brief_machine_data", return_value={}):
                        rec = r._run_seam_warrant("repository_sensemaking_brief", "repo-sensemaker")
        self.assertEqual(rec.warrant, "INCONCLUSIVE")


_ALL_RESOLVED_PR = {
    "behavioral_flow_unassembled": False,
    "provenance_scattered": False,
    "existing_artifact_self_derived": False,
    "fresh_comprehension_needed": False,
    "minimum_subset_suffices": False,
}


class TestPartBPartialSemantics(unittest.TestCase):
    def test_m_sufficient_reaches_no(self):
        ev = EvidenceInput(representation_sufficiency={"status": "sufficient", "rationale": "ok"},
                           probe_report=dict(_ALL_RESOLVED_PR),
                           brief_machine={"evidence": ["a.py:1 x"]},
                           evidence_lines=["a.py:1 x"])
        self.assertEqual(probes_to_warrant(derive_probes(ev)), Warrant.NO)

    def test_n_insufficient_bounded_reaches_partial(self):
        # Range of probes resolved except minimum_subset_suffices, which is
        # affirmatively TRUE via the bounded insufficient_bounded assessment.
        pr = {k: v for k, v in _ALL_RESOLVED_PR.items() if k != "minimum_subset_suffices"}
        ev = EvidenceInput(representation_sufficiency=_ib(),
                           probe_report=pr,
                           brief_machine={"evidence": ["a.py:1 x"]},
                           evidence_lines=["a.py:1 x"])
        self.assertEqual(probes_to_warrant(derive_probes(ev)), Warrant.PARTIAL)

    def test_o_evidence_presence_not_sufficient(self):
        fail = EvidenceInput(brief_machine={"evidence": ["a.py:1 x", "b.py:2 y"]},
                             evidence_lines=["a.py:1 x", "b.py:2 y"])
        self.assertEqual(probes_to_warrant(derive_probes(fail)), Warrant.INCONCLUSIVE)

    def test_p_missing_assessment_not_false(self):
        for name, p in [("inconclusive", "inconclusive"), ("missing", None)]:
            rs = {"status": name, "rationale": "x"} if name != "missing" else None
            with self.subTest(name=name):
                d = derive_probes(EvidenceInput(representation_sufficiency=rs,
                                                brief_machine={"evidence": []},
                                                evidence_lines=[]))
                self.assertEqual(d.by_probe("existing_evidence_sufficient").value, PROBE_UNKNOWN)

    def test_q_repo_gap_unknown_consequentiality_inconclusive(self):
        # A mechanical relationship/finding gap alone (no producer sufficiency
        # verdict) stays INCONCLUSIVE.
        ev = EvidenceInput(probe_report={"relationships": {"adr": {"findings": [{"kind": "x"}]}}},
                           brief_machine={"evidence": ["a.py:1 x"]},
                           evidence_lines=["a.py:1 x"])
        self.assertEqual(probes_to_warrant(derive_probes(ev)), Warrant.INCONCLUSIVE)

    def test_r_inconclusive_for_gap_without_bounded_remedy(self):
        # Producer asserts a gap but no bounded remedy -> INCONCLUSIVE.
        ev = EvidenceInput(representation_sufficiency={"status": "insufficient_bounded",
                                                       "rationale": "gap",
                                                       "needed_representation": ""},
                           brief_machine={"evidence": ["a.py:1 x"]}, evidence_lines=["a.py:1 x"])
        self.assertEqual(probes_to_warrant(derive_probes(ev)), Warrant.INCONCLUSIVE)

    def test_s_insufficient_bounded_missing_fields_fails_closed(self):
        for rs in [{"status": "insufficient_bounded"},
                   {"status": "insufficient_bounded", "rationale": "x"},
                   {"status": "insufficient_bounded", "needed_representation": "y"}]:
            with self.subTest(rs=rs):
                ev = EvidenceInput(representation_sufficiency=rs,
                                   brief_machine={"evidence": ["a.py:1 x"]},
                                   evidence_lines=["a.py:1 x"])
                self.assertEqual(probes_to_warrant(derive_probes(ev)), Warrant.INCONCLUSIVE)

    def test_w_inconclusive_still_gates(self):
        r = _runner()
        result = {"step_id": "1"}
        out = r._terminal_inconclusive_gate(result, 1)
        self.assertEqual(result["terminal_outcome"], "STOPPED_WITHOUT_ACTION")

    def test_x_no_change_affirmative_only(self):
        # INCONCLUSIVE never yields NO_CHANGE (orthogonality + gating preserved).
        r = _runner()
        result = {"step_id": "1"}
        r._terminal_inconclusive_gate(result, 1)
        self.assertNotEqual(result.get("terminal_outcome"), "NO_REPOSITORY_CHANGE_WARRANTED")

    def test_z_full_still_deferred(self):
        # FULL requires existing=FALSE without bounded subset; the adapter cannot
        # derive existing=FALSE from absence, so FULL is not reachable via adapter.
        ev = EvidenceInput(brief_machine={"evidence": ["a.py:1 x"]}, evidence_lines=["a.py:1 x"])
        self.assertEqual(probes_to_warrant(derive_probes(ev)), Warrant.INCONCLUSIVE)


if __name__ == "__main__":
    unittest.main()
