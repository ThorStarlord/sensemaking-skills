"""Commit 7 - baseline-gap coverage traceability (12.1).

Every baseline gap (GAP-1..GAP-9) must have at least one permanent
regression test. This file pins that traceability so a future change cannot
silently drop gap coverage.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TESTS = REPO_ROOT / "tests"

GAP_COVERAGE = {
    "GAP-1": ("standalone quote handling", ["EVIDENCE_QUOTE_NOT_FOUND", "placeholder"]),
    "GAP-2": ("vocabulary drift", ["escalation_recommended", "artifact-vocabulary-map"]),
    "GAP-3": ("citation extensions", ["FILE_CITATION_RE", "js_citation", "test_supported_extensions"]),
    "GAP-4": ("fog enum agreement", ["mixed", "unknown_value"]),
    "GAP-5": ("substantive audit visibility", ["HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT"]),
    "GAP-6": ("taxonomy fit", ["CANONICAL_TYPES", "Ghost Features", "taxonomy"]),
    "GAP-7": ("execution-mode mismatch", ["plan_only", "allowed_execution_modes", "architecture-implementation-workflow"]),
    "GAP-8": ("absent user intent", ["user_implied_fog_type: unknown", "diagnosis_conflict: false"]),
    "GAP-9": ("standalone validation path", ["validate-brief.py", "COMPLETE artifact"]),
}

GAP_TEST_FILES = [
    "test_repo_sensemaker_commit1_regressions.py",
    "test_repo_sensemaker_architecture_fixtures.py",
    "test_repo_sensemaker_boundary_regressions.py",
    "test_repo_sensemaker_fog_regressions.py",
    "test_repo_sensemaker_routing_regressions.py",
    "test_repo_sensemaker_contract_regressions.py",
]


class TestGapCoverageTraceability(unittest.TestCase):
    def test_every_gap_has_regression_markers_in_the_suite(self):
        all_test_text = ""
        for name in GAP_TEST_FILES:
            all_test_text += (TESTS / name).read_text(encoding="utf-8")
        for gap, (what, markers) in GAP_COVERAGE.items():
            for marker in markers:
                self.assertIn(marker, all_test_text,
                              f"{gap} ({what}): marker '{marker}' missing from regression suite")

    def test_gap_markers_also_in_skill_or_template(self):
        """Producer-side guidance must carry the same markers (no test-only
        vocabulary)."""
        skill = (REPO_ROOT / "skills" / "repo-sensemaker" / "SKILL.md").read_text(encoding="utf-8")
        template = (REPO_ROOT / "skills" / "repo-sensemaker" / "references" / "repo-analysis-template.md").read_text(encoding="utf-8")
        guidance = skill + template
        for marker in ("EVIDENCE_QUOTE_NOT_FOUND", "user_implied_fog_type: unknown",
                       "HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT", "allowed_execution_modes"):
            self.assertIn(marker, guidance)


if __name__ == "__main__":
    unittest.main()
