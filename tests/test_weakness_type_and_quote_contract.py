"""Tests for the redesigned brief weakness-type and evidence-quote-grounding
contract (issue #80).

Background: scripts/validate-brief.py used to validate the weakness taxonomy
by scraping Section 6 prose for a case-insensitive substring match against
skills/repo-sensemaker/references/weakness-types.md, with an unrecognized
match as a HARD BLOCKING error (UNKNOWN_WEAKNESS_TYPE). That check wrongly
rejected a legitimate brief in PR #78 and is retired here. Weakness taxonomy
is now a structured `weakness_type` field (Section 13 machine YAML) that is
required metadata but non-blocking (D2/D3/D4): missing, unrecognized, or
prose-mismatched values are warnings only. Only a malformed field (wrong
YAML type) is blocking.

This suite also covers the new deterministic evidence-quote-grounding check
(EVIDENCE_QUOTE_NOT_FOUND): a cited `quote` must actually exist, verbatim
after narrow normalization, within a small fixed window around the cited
`lines` range.
"""

import importlib.util
import os
import sys
import tempfile
import unittest

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRIPTS_DIR)

_spec = importlib.util.spec_from_file_location(
    "validate_brief", os.path.join(SCRIPTS_DIR, "validate-brief.py")
)
vb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vb)

from _validator_utils import load_weakness_types  # noqa: E402

REGISTERED_TYPES = load_weakness_types(REPO_ROOT)


def _codes(errors):
    return [e["message"] for e in errors]


def _by_code(errors, code):
    return [e for e in errors if e["message"].startswith(f"{code}:")]


BODY_TEMPLATE = """# Repository Sensemaking Brief (weakness-type contract fixture)

## 1. Repository goal
Fixture for the weakness_type contract.

## 2. Current shape
Fixture.

## 3. Strong signals
Fixture.

## 4. Missing pieces
Fixture.

## 5. Improvement opportunities
Fixture.

## 6. Weakest boundary
{weakness_label}: fixture weakest-boundary prose.

## 7. Evidence
- `skills/repo-sensemaker/references/weakness-types.md:1` supports this fixture.

Logic trace: the taxonomy file exists and is cited, which is the chain from
evidence to this fixture's weakest-boundary conclusion.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: skills/repo-sensemaker/references/weakness-types.md
    lines: L1
    quote: "# Weakness Types in Repositories"
    supports_claim: "Confirms the taxonomy reference file exists."
```

## 9. Why this boundary matters
Fixture.

## 10. Candidate next steps
Fixture.

## 11. Recommended next step
Fixture.

## 12. Recommended workflow
full-local-sensemaking

## 13. Machine-readable handoff
```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: architecture_fog
evidence:
  - "skills/repo-sensemaker/references/weakness-types.md: taxonomy reference"
recommended_workflow_id: full-local-sensemaking
recommended_execution_mode: plan_only
weakest_boundary: fixture-boundary
{weakness_yaml}
required_inputs:
  - repository_sensemaking_brief
created_at: "2026-07-26T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
N/A -- test fixture.
"""


def _write_tmp(content: str) -> str:
    fd, path = tempfile.mkstemp(suffix=".md")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def _brief(weakness_yaml: str, weakness_label: str = "Zero Validation") -> str:
    return BODY_TEMPLATE.format(weakness_yaml=weakness_yaml, weakness_label=weakness_label)


class TestRecognizedTypesPassCleanly(unittest.TestCase):
    """Each of the 7 registered types produces no weakness_type warning/error."""

    def test_all_seven_registered_types_pass_with_no_weakness_warnings(self):
        self.assertEqual(len(REGISTERED_TYPES), 7, f"expected 7 registered types, got {REGISTERED_TYPES}")
        for wt in REGISTERED_TYPES:
            with self.subTest(weakness_type=wt):
                content = _brief(f"weakness_type: {wt}\nweakness_type_explanation: null", weakness_label=wt)
                path = _write_tmp(content)
                try:
                    errors = vb.validate_brief(path, REPO_ROOT)
                    weakness_errors = [
                        e for e in errors
                        if e["message"].split(":")[0].startswith("WEAKNESS_TYPE")
                        or e["message"].startswith(f"{vb.HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT}:")
                    ]
                    if wt in vb.HIGH_RISK_WEAKNESS_TYPES:
                        self.assertEqual(
                            [e["message"].split(":")[0] for e in weakness_errors],
                            [vb.HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT],
                        )
                    else:
                        self.assertEqual(weakness_errors, [], f"unexpected: {weakness_errors}")
                finally:
                    os.remove(path)

    def test_other_with_explanation_passes_cleanly(self):
        content = _brief(
            'weakness_type: Other\nweakness_type_explanation: "does not map to a registered type"',
            weakness_label="Other",
        )
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT)
            self.assertEqual(_by_code(errors, vb.WEAKNESS_TYPE_OTHER_NO_EXPLANATION), [])
            self.assertEqual(_by_code(errors, vb.WEAKNESS_TYPE_UNKNOWN), [])
            self.assertTrue(vb.validation_result_to_json(path, errors))
        finally:
            os.remove(path)


class TestSeverityMatrix(unittest.TestCase):
    def test_other_without_explanation_is_nonblocking_warning(self):
        content = _brief("weakness_type: Other", weakness_label="Other")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT)
            matches = _by_code(errors, vb.WEAKNESS_TYPE_OTHER_NO_EXPLANATION)
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["severity"], "warning")
            self.assertTrue(vb.validation_result_to_json(path, errors))
            import json
            result = json.loads(vb.validation_result_to_json(path, errors))
            self.assertTrue(result["valid"], "warning-only brief must remain valid")
        finally:
            os.remove(path)

    def test_other_with_empty_string_explanation_treated_same_as_missing(self):
        content = _brief('weakness_type: Other\nweakness_type_explanation: ""', weakness_label="Other")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT)
            self.assertEqual(len(_by_code(errors, vb.WEAKNESS_TYPE_OTHER_NO_EXPLANATION)), 1)
        finally:
            os.remove(path)

    def test_missing_weakness_type_is_nonblocking_warning(self):
        content = _brief("")  # no weakness_type key at all -- simulates a legacy brief
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT)
            matches = _by_code(errors, vb.WEAKNESS_TYPE_MISSING)
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["severity"], "warning")
            import json
            result = json.loads(vb.validation_result_to_json(path, errors))
            self.assertTrue(result["valid"])
        finally:
            os.remove(path)

    def test_unknown_weakness_type_is_nonblocking_warning_not_old_blocking_error(self):
        """This is the direct regression test for the PR #78 failure mode:
        an unrecognized type must NOT invalidate the brief."""
        content = _brief("weakness_type: Not A Real Type", weakness_label="Not A Real Type")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT)
            matches = _by_code(errors, vb.WEAKNESS_TYPE_UNKNOWN)
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["severity"], "warning")
            import json
            result = json.loads(vb.validation_result_to_json(path, errors))
            self.assertTrue(result["valid"], "unrecognized weakness_type must never invalidate the brief")
            # UNKNOWN_WEAKNESS_TYPE (the old blocking code) must be fully retired.
            self.assertFalse(hasattr(vb, "UNKNOWN_WEAKNESS_TYPE"))
        finally:
            os.remove(path)

    def test_malformed_weakness_type_is_blocking_error(self):
        content = _brief("weakness_type:\n  - Zero Validation\n  - Safety Gaps")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT)
            matches = _by_code(errors, vb.WEAKNESS_TYPE_MALFORMED)
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["severity"], "error")
            import json
            result = json.loads(vb.validation_result_to_json(path, errors))
            self.assertFalse(result["valid"], "a malformed weakness_type field must invalidate the brief")
        finally:
            os.remove(path)

    def test_prose_mismatch_is_nonblocking_warning(self):
        content = _brief("weakness_type: Zero Validation", weakness_label="Contract Mismatch")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT)
            matches = _by_code(errors, vb.WEAKNESS_TYPE_PROSE_MISMATCH)
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["severity"], "warning")
        finally:
            os.remove(path)

    def test_taxonomy_warnings_alone_never_cause_nonzero_exit(self):
        """End-to-end via main(): a brief with only weakness_type warnings must
        exit 0, exercising the real CLI path per repo convention."""
        content = _brief("weakness_type: Not A Real Type", weakness_label="Not A Real Type")
        path = _write_tmp(content)
        try:
            exit_code = vb.main([path, "--repo-root", REPO_ROOT, "--json"])
            self.assertEqual(exit_code, 0)
        finally:
            os.remove(path)


class TestHighRiskAudit(unittest.TestCase):
    def test_safety_gaps_emits_high_risk_warning(self):
        content = _brief("weakness_type: Safety Gaps", weakness_label="Safety Gaps")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT)
            matches = _by_code(errors, vb.HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT)
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["severity"], "warning")
        finally:
            os.remove(path)

    def test_ghost_features_emits_high_risk_warning(self):
        content = _brief("weakness_type: Ghost Features", weakness_label="Ghost Features")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT)
            matches = _by_code(errors, vb.HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT)
            self.assertEqual(len(matches), 1)
        finally:
            os.remove(path)

    def test_ordinary_type_does_not_emit_high_risk_warning(self):
        content = _brief("weakness_type: Vocabulary Drift", weakness_label="Vocabulary Drift")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT)
            self.assertEqual(_by_code(errors, vb.HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT), [])
        finally:
            os.remove(path)


class TestEvidenceQuoteGrounding(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.target_repo = self._tmpdir.name
        with open(os.path.join(self.target_repo, "example.py"), "w", encoding="utf-8") as f:
            f.write("line one\nline two\nline three\nline four\nline five\n")

    def tearDown(self):
        self._tmpdir.cleanup()

    def _brief_citing(self, lines: str, quote: str) -> str:
        return (
            "# Brief\n\n## 6. Weakest boundary\nZero Validation: fixture.\n\n"
            "## 7. Evidence\n- example.py cited.\n\nLogic trace: example.py "
            "supports this fixture's weakest-boundary claim.\n\n"
            "## 8. Evidence excerpts\n```yaml\nevidence_excerpts:\n"
            f"  - file: example.py\n    lines: {lines}\n    quote: \"{quote}\"\n"
            "    supports_claim: \"demonstrates grounding\"\n```\n\n"
            "## 13. Machine-readable handoff\n```yaml\n"
            "recommended_workflow_id: full-local-sensemaking\n"
            "weakest_boundary: fixture\nweakness_type: Zero Validation\n"
            "required_inputs:\n  - repository_sensemaking_brief\n```\n"
        )

    def test_quote_found_at_cited_line_passes(self):
        path = _write_tmp(self._brief_citing("2", "line two"))
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND), [])
        finally:
            os.remove(path)

    def test_quote_found_within_window_passes(self):
        # Cited at line 1, but quote is actually on line 4 -- within the
        # documented +/- QUOTE_GROUNDING_WINDOW=3 line window.
        path = _write_tmp(self._brief_citing("1", "line four"))
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND), [])
        finally:
            os.remove(path)

    def test_quote_absent_fails_blocking(self):
        path = _write_tmp(self._brief_citing("2", "this text does not exist in the file"))
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            matches = _by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND)
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["severity"], "error")
            import json
            result = json.loads(vb.validation_result_to_json(path, errors))
            self.assertFalse(result["valid"])
        finally:
            os.remove(path)

    def test_quote_grounding_normalizes_line_endings_and_whitespace(self):
        with open(os.path.join(self.target_repo, "crlf.py"), "wb") as f:
            f.write(b"alpha\r\nbeta   gamma\r\ndelta\r\n")
        content = self._brief_citing("2", "beta gamma").replace("example.py", "crlf.py")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND), [])
        finally:
            os.remove(path)

    def test_no_semantic_matching_paraphrase_still_fails(self):
        path = _write_tmp(self._brief_citing("2", "the second line of the file"))
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            self.assertEqual(len(_by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND)), 1)
        finally:
            os.remove(path)

    def test_missing_cited_file_still_blocks_as_hallucinated_file(self):
        content = self._brief_citing("2", "line two").replace("example.py", "does-not-exist.py")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            self.assertEqual(len(_by_code(errors, vb.HALLUCINATED_FILE)), 1)
            # Quote check must not even run (no double-reporting) when the file itself is missing.
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND), [])
        finally:
            os.remove(path)

    def test_malformed_line_syntax_still_blocks_and_skips_quote_check(self):
        content = self._brief_citing("not-a-line-number", "line two")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            self.assertEqual(len(_by_code(errors, vb.INVALID_LINE_FORMAT)), 1)
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND), [])
        finally:
            os.remove(path)

    def test_out_of_bounds_line_range_is_blocking(self):
        path = _write_tmp(self._brief_citing("999", "line two"))
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            matches = _by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND)
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["severity"], "error")
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
