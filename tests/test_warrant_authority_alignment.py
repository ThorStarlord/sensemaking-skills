"""Warrant-authority alignment qualification (directive #25).

A-V: representation_sufficiency is the PRIMARY task-relative MODEL_WARRANT
authority; mechanical probes are supporting/diagnostic signals that do NOT gate.
Frozen jtbl P+C re-evaluates to NO without changing the historical SAFE_INCONCLUSIVE.
"""
import os
import sys
import unittest

from sensemaking_skills.reasoning.vertical_slice import Warrant
from sensemaking_skills.reasoning.evidence_probes import (
    EvidenceInput, derive_probes, probes_to_warrant, PROBE_UNKNOWN,
)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
import brief_skeleton


def _ib(**extra):
    d = {"status": "insufficient_bounded",
         "rationale": "specific consequential gap (flow not assembled)",
         "needed_representation": "bounded execution-flow projection"}
    d.update(extra)
    return d


class TestAutowiredMapping(unittest.TestCase):
    def test_a_sufficient_to_no(self):
        ev = EvidenceInput(representation_sufficiency={"status": "sufficient", "rationale": "ok"})
        self.assertEqual(probes_to_warrant(derive_probes(ev)), Warrant.NO)

    def test_b_insufficient_bounded_to_partial(self):
        ev = EvidenceInput(representation_sufficiency=_ib())
        self.assertEqual(probes_to_warrant(derive_probes(ev)), Warrant.PARTIAL)

    def test_c_inconclusive_to_inconclusive(self):
        ev = EvidenceInput(representation_sufficiency={"status": "inconclusive", "rationale": "?"})
        self.assertEqual(probes_to_warrant(derive_probes(ev)), Warrant.INCONCLUSIVE)

    def test_d_missing_malformed_to_inconclusive(self):
        for rs in [None, {}, "garbage",
                   {"status": "bogus"},
                   {"status": "insufficient_bounded"},   # missing rationale/needed_rep
                   ]:
            with self.subTest(rs=rs):
                ev = EvidenceInput(representation_sufficiency=rs,
                                   brief_machine={"evidence": ["a.py:1 x"]},
                                   evidence_lines=["a.py:1 x"])
                self.assertEqual(probes_to_warrant(derive_probes(ev)), Warrant.INCONCLUSIVE)
        # Note: {'status':'sufficient'} is valid even with an empty/non-string
        # rationale (only insufficient_bounded requires a non-empty rationale +
        # needed_representation per contract).
        ev_suf = EvidenceInput(representation_sufficiency={"status": "sufficient", "rationale": 123})
        self.assertEqual(probes_to_warrant(derive_probes(ev_suf)), Warrant.NO)


class TestMechanicalProbesDoNotVeto(unittest.TestCase):
    def test_e_unknown_diagnostics_do_not_veto_sufficient(self):
        # sufficient + all other probes UNKNOWN (common production case).
        ev = EvidenceInput(representation_sufficiency={"status": "sufficient", "rationale": "ok"},
                           probe_report={"behavioral_flow_unassembled": None},
                           brief_machine={"evidence": ["a.py:1 x", "b.py:2 y", "c.py:3 z"]},
                           evidence_lines=["a.py:1 x", "b.py:2 y", "c.py:3 z"])
        d = derive_probes(ev)
        self.assertEqual(probes_to_warrant(d), Warrant.NO)
        # diagnostics are still reported (telemetry), not dropped
        names = {p.probe for p in d.probes}
        self.assertIn("behavioral_flow_unassembled", names)

    def test_f_provenance_scattered_true_alone_not_force(self):
        ev = EvidenceInput(representation_sufficiency={"status": "sufficient", "rationale": "ok"},
                           brief_machine={"evidence": ["a.py:1 x", "b.py:2 y"]},
                           evidence_lines=["a.py:1 x", "b.py:2 y"])
        self.assertEqual(probes_to_warrant(derive_probes(ev)), Warrant.NO)

    def test_g_behavioral_flow_true_alone_not_force_partial(self):
        # A mechanical flow signal with a valid 'sufficient' does not force PARTIAL.
        ev = EvidenceInput(representation_sufficiency={"status": "sufficient", "rationale": "ok"},
                           probe_report={"behavioral_flow_unassembled": True},
                           brief_machine={"evidence": ["a.py:1 x"]}, evidence_lines=["a.py:1 x"])
        self.assertEqual(probes_to_warrant(derive_probes(ev)), Warrant.NO)

    def test_h_fresh_comprehension_not_gate(self):
        # fresh_comprehension_needed does not gate production warrant (sufficient -> NO).
        ev = EvidenceInput(representation_sufficiency={"status": "sufficient", "rationale": "ok"},
                           probe_report={"fresh_comprehension_needed": True},
                           brief_machine={"evidence": ["a.py:1 x"]}, evidence_lines=["a.py:1 x"])
        self.assertEqual(probes_to_warrant(derive_probes(ev)), Warrant.NO)

    def test_i_minimum_subset_not_duplicate_authority(self):
        # minimum_subset_suffices no longer independently re-decides boundedness.
        # insufficient_bounded contract alone reaches PARTIAL.
        ev = EvidenceInput(representation_sufficiency=_ib(),
                           probe_report={"minimum_subset_suffices": False})
        self.assertEqual(probes_to_warrant(derive_probes(ev)), Warrant.PARTIAL)

    def test_j_partial_requires_bounded_needed_representation(self):
        ev = EvidenceInput(representation_sufficiency=_ib(needed_representation=""))
        self.assertEqual(probes_to_warrant(derive_probes(ev)), Warrant.INCONCLUSIVE)


class TestInvariants(unittest.TestCase):
    def test_q_absence_never_false(self):
        d = derive_probes(EvidenceInput())
        by = {p.probe: p.value for p in d.probes}
        for v in by.values():
            self.assertNotEqual(v, "FALSE")
        # no assessment -> INCONCLUSIVE (not NO/PARTIAL)
        self.assertEqual(probes_to_warrant(d), Warrant.INCONCLUSIVE)

    def test_z_full_never_inferred(self):
        ev = EvidenceInput(representation_sufficiency=None)
        self.assertEqual(probes_to_warrant(derive_probes(ev)), Warrant.INCONCLUSIVE)

    def test_legacy_probes_still_reported_as_telemetry(self):
        d = derive_probes(EvidenceInput(
            representation_sufficiency={"status": "inconclusive", "rationale": "?"},
            brief_machine={"evidence": ["a.py:1 x"]}, evidence_lines=["a.py:1 x"]))
        names = {p.probe for p in d.probes}
        self.assertTrue({"existing_evidence_sufficient", "behavioral_flow_unassembled",
                         "provenance_scattered", "existing_artifact_self_derived",
                         "fresh_comprehension_needed", "minimum_subset_suffices"}
                        <= names)


class TestFrozenJtblFreevaluation(unittest.TestCase):
    """U: frozen jtbl P+C (representation_sufficiency=sufficient) -> NO, without
    changing the historical SAFE_INCONCLUSIVE record."""

    def test_frozen_jtbl_C_reevaluates_to_no(self):
        dogfood_dir = os.path.join("experiments", "product-hypothesis-b",
                                   "implementation", "dogfood-jtbl")
        c = os.path.join(dogfood_dir, "C_post_reconcile_final_brief.md")
        if not os.path.exists(c):
            self.skipTest("frozen jtbl C not present")
        with open(c, encoding="utf-8") as f:
            text = f.read()
        block = brief_skeleton.extract_handoff_yaml_block(text)
        import yaml
        machine = yaml.safe_load(block)
        rs = machine.get("representation_sufficiency")
        self.assertEqual(rs.get("status"), "sufficient")
        P = os.path.join(dogfood_dir, "P_same_episode_probe_report.yaml")
        probe = None
        if os.path.exists(P):
            with open(P, encoding="utf-8") as f:
                probe = yaml.safe_load(f)
        ev = EvidenceInput(probe_report=probe, brief_machine=machine,
                           evidence_lines=list(machine.get("evidence") or []),
                           representation_sufficiency=rs)
        from sensemaking_skills.reasoning.warrant_gate import run_seam_warrant
        rec = run_seam_warrant(
            target_repository="kellyjonbrazil/jtbl",
            target_revision="0018aaddf5a76cc03a761ef01b065ff2183f9d17",
            user_goal="goal", evidence=ev,
        )
        self.assertEqual(rec.warrant, "NO")
        self.assertFalse(rec.representation_materialized)


if __name__ == "__main__":
    unittest.main()
