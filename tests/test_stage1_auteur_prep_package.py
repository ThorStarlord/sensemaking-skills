"""Deterministic validation of the Stage 1 auteur post-remediation preparation package.

These tests verify that the preparation package is internally consistent and
that it cannot silently drift into something that looks like a completed run.

They are deliberately offline and side-effect free: they read repository files
only. They never invoke a model, never run the Stage 1 workflow, and never
create an evidence directory.
"""

import re
import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_PATH = REPO_ROOT / "docs" / "experiments" / "STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md"
CHECKLIST_PATH = REPO_ROOT / "docs" / "experiments" / "GATE-D-STALE-DIAGNOSIS-CHECKLIST.md"

EVIDENCE_0015_DIR = "experiments/evidence/0015-stage1-auteur-controlled-learning-attempt"
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")

REQUIRED_GATES = [
    "Gate A - Invocation integrity",
    "Gate B - Structural validation",
    "Gate C - Safety",
    "Gate D - Substantive audit",
    "Gate E - Human usefulness",
    "Gate F - Campaign interpretation",
]

REQUIRED_RESULTS = [
    "SUCCESSFUL_CONTROLLED_EVIDENCE",
    "STRUCTURAL_FAILURE",
    "SUBSTANTIVE_FAILURE",
    "SAFETY_FAILURE",
    "INCONCLUSIVE",
]


def _load_contract():
    text = PACKAGE_PATH.read_text(encoding="utf-8")
    blocks = re.findall(r"```yaml\n(.*?)```", text, re.DOTALL)
    if not blocks:
        raise AssertionError("no ```yaml contract block found in the preparation package")
    return yaml.safe_load(blocks[0]), text


class PreparationPackageStructure(unittest.TestCase):
    def setUp(self):
        self.contract, self.text = _load_contract()

    def test_package_and_checklist_exist(self):
        self.assertTrue(PACKAGE_PATH.is_file())
        self.assertTrue(CHECKLIST_PATH.is_file())

    def test_status_is_prepared_not_run(self):
        self.assertEqual(self.contract["package_status"], "PREPARED_NOT_RUN")
        self.assertIn("PREPARED_NOT_RUN", self.text)

    def test_framework_sha_present_and_full_length(self):
        self.assertTrue(FULL_SHA.match(str(self.contract["framework_sha"])))

    def test_target_sha_present_and_full_length(self):
        self.assertTrue(FULL_SHA.match(str(self.contract["target_sha"])))

    def test_artifact_type_is_repository_sensemaking_brief(self):
        self.assertEqual(self.contract["artifact_type"], "repository_sensemaking_brief")

    def test_exact_model_specified(self):
        self.assertEqual(self.contract["exact_model"], "claude-sonnet-5")


class EvidenceNumbering(unittest.TestCase):
    def setUp(self):
        self.contract, self.text = _load_contract()

    def test_evidence_number_is_unused_on_disk(self):
        number = self.contract["evidence_number"]
        existing = [p.name for p in (REPO_ROOT / "experiments" / "evidence").iterdir() if p.is_dir()]
        for name in existing:
            self.assertFalse(
                name.startswith(f"{number}-"),
                f"evidence number {number} is already used by {name}",
            )

    def test_planned_evidence_directory_was_not_created(self):
        planned = REPO_ROOT / self.contract["evidence_directory_planned"]
        self.assertFalse(
            planned.exists(),
            "preparation must not create the live evidence directory",
        )
        self.assertFalse(self.contract["evidence_directory_created"])

    def test_slug_matches_number(self):
        self.assertTrue(
            self.contract["evidence_slug"].startswith(self.contract["evidence_number"] + "-")
        )


class HistoricalEvidenceImmutability(unittest.TestCase):
    def setUp(self):
        self.contract, self.text = _load_contract()

    def test_evidence_0015_not_used_as_new_output_path(self):
        for key in ("expected_output_path", "expected_run_log_path", "evidence_directory_planned"):
            value = str(self.contract[key]).replace("\\", "/")
            self.assertNotIn(
                EVIDENCE_0015_DIR,
                value,
                f"{key} must not point into historical Evidence 0015",
            )
            self.assertNotIn("0015", value, f"{key} must not reference evidence 0015")

    def test_evidence_0015_declared_immutable_and_not_reclassified(self):
        hist = self.contract["historical_evidence_0015"]
        self.assertTrue(hist["immutable"])
        self.assertFalse(hist["usable_as_new_output_path"])
        self.assertFalse(hist["usable_as_input_artifact"])
        self.assertFalse(hist["reclassified_by_this_package"])
        self.assertEqual(hist["classification"], "STAGE 1 FAIL")

    def test_evidence_0015_directory_still_present(self):
        self.assertTrue((REPO_ROOT / EVIDENCE_0015_DIR).is_dir())


class InvocationAndSafetyRules(unittest.TestCase):
    def setUp(self):
        self.contract, self.text = _load_contract()

    def test_one_invocation_rule(self):
        self.assertEqual(self.contract["invocation_count_allowed"], 1)

    def test_no_fallback_or_substitution(self):
        self.assertFalse(self.contract["model_fallback_allowed"])
        self.assertFalse(self.contract["model_substitution_allowed"])

    def test_no_automatic_retry_or_repair(self):
        self.assertFalse(self.contract["automatic_retry_allowed"])
        self.assertFalse(self.contract["automatic_repair_allowed"])
        self.assertFalse(self.contract["manual_artifact_repair_allowed"])

    def test_no_target_mutation(self):
        self.assertFalse(self.contract["target_mutation_allowed"])

    def test_second_attempt_requires_owner_decision(self):
        self.assertTrue(self.contract["second_attempt_requires_new_owner_decision"])

    def test_stop_on_first_failed_gate(self):
        self.assertTrue(self.contract["stop_on_first_failed_gate"])


class RootsAndPaths(unittest.TestCase):
    def setUp(self):
        self.contract, self.text = _load_contract()

    def _norm(self, value):
        return str(value).replace("\\", "/").rstrip("/")

    def test_framework_and_target_roots_differ(self):
        self.assertNotEqual(
            self._norm(self.contract["framework_root"]),
            self._norm(self.contract["target_root"]),
        )

    def test_output_and_log_paths_are_not_under_target_root(self):
        target = self._norm(self.contract["target_root"]) + "/"
        for key in ("expected_output_path", "expected_run_log_path"):
            self.assertFalse(
                self._norm(self.contract[key]).startswith(target),
                f"{key} must not live under the target root",
            )

    def test_output_path_is_under_an_authorized_location(self):
        out = self._norm(self.contract["expected_output_path"])
        framework = self._norm(self.contract["framework_root"]) + "/"
        self.assertTrue(out.startswith(framework))
        self.assertTrue(out.endswith("repository_sensemaking_brief.md"))

    def test_log_path_is_outside_both_repositories_or_under_framework(self):
        log = self._norm(self.contract["expected_run_log_path"])
        self.assertNotIn("/target-auteur/", log)
        self.assertTrue(log.endswith(".md"))


class GatesAndTripwires(unittest.TestCase):
    def setUp(self):
        self.contract, self.text = _load_contract()

    def test_all_six_gates_present(self):
        self.assertEqual(self.contract["gates"], REQUIRED_GATES)

    def test_all_eight_tripwires_present(self):
        tripwires = self.contract["stale_diagnosis_tripwires"]
        self.assertEqual(len(tripwires), 8)
        for index in range(1, 9):
            self.assertTrue(
                any(t.startswith(f"T{index} ") for t in tripwires),
                f"tripwire T{index} missing",
            )

    def test_tripwires_also_present_in_reviewer_checklist(self):
        checklist = CHECKLIST_PATH.read_text(encoding="utf-8")
        for index in range(1, 9):
            self.assertIn(f"| T{index} |", checklist)

    def test_checklist_is_marked_prepared_not_run(self):
        self.assertIn("PREPARED_NOT_RUN", CHECKLIST_PATH.read_text(encoding="utf-8"))

    def test_contradiction_search_paths_declared(self):
        paths = self.contract["contradiction_search_paths"]
        for expected in (
            "src/auteur/series/universe_advisory.py",
            "src/auteur/series/handlers.py",
            "src/auteur/universe/models.py",
            "tests/test_series_universe_integration.py",
        ):
            self.assertIn(expected, paths)

    def test_campaign_results_are_exactly_the_permitted_five(self):
        self.assertEqual(self.contract["campaign_results_permitted"], REQUIRED_RESULTS)


class ReadinessAndCampaignBoundaries(unittest.TestCase):
    def setUp(self):
        self.contract, self.text = _load_contract()

    def test_readiness_cannot_be_auto_promoted(self):
        self.assertFalse(self.contract["readiness_auto_promotion_allowed"])
        self.assertEqual(self.contract["readiness_classification_before"], "Externally exercised")

    def test_second_structurally_different_target_still_required(self):
        self.assertTrue(self.contract["second_structurally_different_target_required"])


class NoFabricatedRunOutput(unittest.TestCase):
    """The package must not look like, or contain, a completed run."""

    def setUp(self):
        self.contract, self.text = _load_contract()

    def test_no_completed_gate_verdicts(self):
        forbidden = [
            "Gate A result: PASS",
            "Gate B result: PASS",
            "Gate C result: PASS",
            "Gate D result: PASS",
            "Gate E result: PASS",
            "Gate F result: PASS",
        ]
        for phrase in forbidden:
            self.assertNotIn(phrase, self.text)
            self.assertNotIn(phrase, CHECKLIST_PATH.read_text(encoding="utf-8"))

    def test_no_run_classification_claimed(self):
        for phrase in ("STAGE 1 PASS", "Stage 1 was invoked", "run completed"):
            self.assertNotIn(phrase, self.text)

    def test_owner_authorization_block_is_blank(self):
        self.assertIn("Authorized by:\n", self.text)
        self.assertIn("NOT AUTHORIZED", self.text)

    def test_no_live_evidence_files_produced(self):
        planned = REPO_ROOT / self.contract["evidence_directory_planned"]
        self.assertFalse(planned.exists())
        for name in ("repository_sensemaking_brief.md", "workflow_summary.json", "tool-call-trace.jsonl"):
            self.assertFalse(
                (PACKAGE_PATH.parent / name).exists(),
                f"preparation must not emit {name}",
            )


if __name__ == "__main__":
    unittest.main()
