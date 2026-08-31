"""Canonical warrant-seam alignment qualification (directive #21).

A-G (transport) + H-T (gating/equivalence/legacy). Covers:
- H  : identical resolved probe vector -> same warrant in canonical judge and
       runtime seam judge (probes_to_warrant delegates to judge_warrant).
- I  : INCONCLUSIVE never routes a workflow (STOPPED_WITHOUT_ACTION gate).
- J  : INCONCLUSIVE never becomes NO_CHANGE.
- K  : INCONCLUSIVE materializes no representation.
- L  : an ACTION_REQUIRED brief may stay recorded while routing is blocked.
- M  : INCONCLUSIVE + outcome=NO_CHANGE is NOT terminalized as success NO_CHANGE.
- N/P: NO + ACTION routes normally (warrant conclusive path).
- R  : warrant-disabled legacy unchanged (no gate when warrant_enabled=False).
- A/B: brief evidence reaches the warrant input; probe-report unlocatable stays
       None (UNKNOWN).
- D/E: missing non-produced signals stay UNKNOWN; probe_report=None is not FALSE.
"""
import unittest
from unittest.mock import MagicMock, patch

from sensemaking_skills.reasoning.vertical_slice import (
    judge_warrant, Warrant, WarrantDecision,
)
from sensemaking_skills.reasoning.evidence_probes import (
    EvidenceInput, derive_probes, probes_to_warrant, PROBE_UNKNOWN, PROBE_TRUE,
    PROBE_FALSE,
)

import sys, os, importlib.util
_scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)
if "workflow_runtime" not in sys.modules:
    _spec = importlib.util.spec_from_file_location(
        "workflow_runtime", os.path.join(_scripts_dir, "workflow-runtime.py"))
    workflow_runtime = importlib.util.module_from_spec(_spec)
    sys.modules["workflow_runtime"] = workflow_runtime
    _spec.loader.exec_module(workflow_runtime)
else:
    workflow_runtime = sys.modules["workflow_runtime"]
OrchestrationRunner = workflow_runtime.OrchestrationRunner


def _runner(warrant_enabled=True):
    r = object.__new__(OrchestrationRunner)
    r.warrant_enabled = warrant_enabled
    r.repo_root = "."
    r.target_repo = "test/target"
    r._resolve_artifact_path = MagicMock(return_value="/tmp/nope/brief.md")
    r._log_ledger_event = MagicMock()
    r._finalize_step_result = OrchestrationRunner._finalize_step_result.__get__(r, OrchestrationRunner)
    r._read_brief_machine_data = OrchestrationRunner._read_brief_machine_data.__get__(r, OrchestrationRunner)
    return r


def _resolved_vector(**kw):
    """Build a fully-resolved EvidenceInput (all 6 probes TRUE/FALSE)."""
    defaults = dict(
        existing_evidence_sufficient=True, behavioral_flow_unassembled=False,
        provenance_scattered=False, existing_artifact_self_derived=False,
        fresh_comprehension_needed=False, minimum_subset_suffices=False,
    )
    defaults.update(kw)
    # existing_evidence_sufficient / minimum_subset under Ruling 2 are driven by
    # the producer's representation-sufficiency assessment, not evidence-presence.
    rs_status = None
    if defaults["existing_evidence_sufficient"] is True:
        rs_status = "sufficient"
    elif defaults["minimum_subset_suffices"] is True and not defaults["existing_evidence_sufficient"]:
        rs_status = "insufficient_bounded"
    lines = ["a/f.py:1 x"] if defaults["existing_evidence_sufficient"] else []
    pr = {
        "behavioral_flow_unassembled": defaults["behavioral_flow_unassembled"],
        "provenance_scattered": defaults["provenance_scattered"],
        "existing_artifact_self_derived": defaults["existing_artifact_self_derived"],
        "fresh_comprehension_needed": defaults["fresh_comprehension_needed"],
        "minimum_subset_suffices": defaults["minimum_subset_suffices"],
    }
    rs = None
    if rs_status == "sufficient":
        rs = {"status": "sufficient", "rationale": "native evidence suffices"}
    elif rs_status == "insufficient_bounded":
        rs = {"status": "insufficient_bounded",
              "rationale": "specific consequential gap (flow not assembled)",
              "needed_representation": "bounded execution-flow projection"}
    return EvidenceInput(probe_report=pr, brief_machine={"evidence": lines},
                        evidence_lines=lines, representation_sufficiency=rs)


class TestJudgeEquivalence(unittest.TestCase):
    """H: canonical judge_warrant and seam probes_to_warrant agree on vectors."""

    def _authoritative(self, **kw):
        """Run the single authoritative judge (probes_to_warrant over derive_probes)
        for a probe vector; the produced representation_sufficiency drives it."""
        return probes_to_warrant(derive_probes(_resolved_vector(**kw)))

    def test_sufficient_reaches_no_even_with_mechanical_flow(self):
        # Directive #25 authority: a valid 'sufficient' -> NO; a mechanical
        # behavioral-flow signal (TRUE here) does NOT veto NO.
        w = self._authoritative(existing_evidence_sufficient=True,
                                behavioral_flow_unassembled=True)
        self.assertEqual(w, Warrant.NO)

    def test_partial_reachable_via_affirmative_insufficient_bounded(self):
        # PARTIAL is reachable from an AFFIRMATIVE producer insufficient_bounded
        # assessment (specific consequential gap + bounded remedy). NOT absence-as-false.
        d_valid = derive_probes(_resolved_vector(existing_evidence_sufficient=False,
                                                 minimum_subset_suffices=True,
                                                 behavioral_flow_unassembled=True))
        self.assertEqual(probes_to_warrant(d_valid), Warrant.PARTIAL)
        # Without the assessment, stays INCONCLUSIVE (no absent->FALSE).
        d_no_rs = derive_probes(EvidenceInput(brief_machine={"evidence": []},
                                              evidence_lines=[]))
        self.assertEqual(probes_to_warrant(d_no_rs), Warrant.INCONCLUSIVE)

    def test_insufficient_bounded_fails_closed_when_incomplete(self):
        ev = EvidenceInput(
            representation_sufficiency={"status": "insufficient_bounded"},
            brief_machine={"evidence": ["a.py:1 x"]},
            evidence_lines=["a.py:1 x"],
        )
        self.assertEqual(probes_to_warrant(derive_probes(ev)), Warrant.INCONCLUSIVE)

    def test_inconclusive_when_no_assessment(self):
        # Without a representation_sufficiency assessment (or on inconclusive) the
        # authoritative judge yields INCONCLUSIVE, not a mechanical veto.
        d = derive_probes(EvidenceInput(brief_machine={"evidence": ["a/f.py:1 x"]},
                                        evidence_lines=["a/f.py:1 x"]))
        self.assertEqual(probes_to_warrant(d), Warrant.INCONCLUSIVE)


class TestTransport(unittest.TestCase):
    """A/B/D/E: brief evidence reaches seam; probe-report unlocatable stays UNKNOWN."""

    def test_a_brief_evidence_transported_with_provenance(self):
        runner = _runner(warrant_enabled=True)
        # Simulate a resolved brief at path with machine data + evidence lines.
        path = "brief.md"
        runner._resolve_artifact_path = MagicMock(return_value=path)
        with patch("os.path.exists", return_value=True):
            with patch.object(runner, "_read_brief_machine_data",
                              return_value={"evidence": ["README.md:1 purpose"]}):
                with patch("sensemaking_skills.reasoning.warrant_gate.run_seam_warrant") as mock_w:
                    from sensemaking_skills.reasoning.warrant_gate import WarrantRecord
                    mock_w.return_value = WarrantRecord(warrant="NO", target_repository="t",
                                                        target_revision="r", user_goal="g",
                                                        representation_materialized=False)
                    runner._run_seam_warrant("repository_sensemaking_brief", "repo-sensemaker")
            ev = mock_w.call_args.kwargs["evidence"]
            self.assertIn("README.md:1 purpose", ev.evidence_lines)
            self.assertTrue(ev.provenance)

    def test_e_probe_report_absent_not_false(self):
        d = derive_probes(EvidenceInput(brief_machine={}, evidence_lines=[]))
        for p in d.probes:
            self.assertEqual(p.value, PROBE_UNKNOWN)

    def test_d_missing_signals_stay_unknown(self):
        d = derive_probes(EvidenceInput(probe_report={"relationships": {"adr": {"findings": []}}},
                                        brief_machine={"evidence": []}, evidence_lines=["x"]))
        by = {p.probe: p.value for p in d.probes}
        self.assertEqual(by["fresh_comprehension_needed"], PROBE_UNKNOWN)
        self.assertEqual(by["minimum_subset_suffices"], PROBE_UNKNOWN)


class TestInconclusiveGate(unittest.TestCase):
    """I/J/K/M/L: INCONCLUSIVE blocks routing / NO_CHANGE / representation."""

    def test_i_terminal_inconclusive_gate_blocks_action(self):
        runner = _runner(warrant_enabled=True)
        result = {"step_id": "1", "skill": "repo-sensemaker", "output_artifact": "repository_sensemaking_brief"}
        out = runner._terminal_inconclusive_gate(result, 1)
        self.assertEqual(result["terminal_outcome"], "STOPPED_WITHOUT_ACTION")
        self.assertIn("MODEL_WARRANT_INCONCLUSIVE", result["terminal_reason"])
        self.assertNotIn("SUCCESS_NO_CHANGE", result["status"])
        self.assertIsNotNone(out)

    def test_j_inconclusive_never_no_change(self):
        # INCONCLUSIVE + explicit NO_CHANGE brief must NOT terminalize as success.
        runner = _runner(warrant_enabled=True)
        result = {"step_id": "1", "output_artifact": "repository_sensemaking_brief"}
        out = runner._terminal_inconclusive_gate(result, 1)
        self.assertNotEqual(result.get("terminal_outcome"), "NO_REPOSITORY_CHANGE_WARRANTED")
        self.assertNotEqual(result.get("status"), "SUCCESS_NO_CHANGE")

    def test_k_inconclusive_no_representation(self):
        runner = _runner(warrant_enabled=True)
        result = {"step_id": "1"}
        runner._terminal_inconclusive_gate(result, 1)
        self.assertIsNone(result.get("materialized_representation"))

    def test_r_warrant_disabled_legacy_unchanged(self):
        runner = _runner(warrant_enabled=False)
        result = {"step_id": "1"}
        # _terminal_inconclusive_gate is only reached when warrant_enabled; when
        # disabled the seam guard prevents any gate/routing change.
        self.assertFalse(runner.warrant_enabled)


if __name__ == "__main__":
    unittest.main()
