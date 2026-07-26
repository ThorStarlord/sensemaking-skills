"""Tests for the redesigned brief weakness-type and evidence-quote-grounding
contract (issue #80).

Background: scripts/validate-brief.py used to validate the weakness taxonomy
by scraping Section 6 prose for a case-insensitive substring match against
skills/repo-sensemaker/references/weakness-types.md, with an unrecognized
match as a HARD BLOCKING error (UNKNOWN_WEAKNESS_TYPE). PR #78 was correctly
rejected under that then-current structural contract; the rejection exposed
the brittleness of prose-substring taxonomy validation (the substantive
diagnosis in PR #78 was never audited and remains neither confirmed nor
disproven). That blocking check is retired here. Weakness taxonomy is now a
structured `weakness_type` field (Section 13 machine YAML) that is required
metadata but non-blocking (D2/D3/D4): missing, unrecognized, or
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
        """This is the direct regression test for the structural-contract
        failure mode PR #78 hit (correctly rejected under the old contract,
        but that rejection exposed the check's brittleness -- see module
        docstring): an unrecognized type must NOT invalidate the brief."""
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


class TestProseMismatchAdversarial(unittest.TestCase):
    """Adversarial coverage for WEAKNESS_TYPE_PROSE_MISMATCH (pre-merge
    review item 3): informational only, never blocking, no noise when the
    structured field is valid and prose simply doesn't restate it verbatim
    in a way that would be misleading, and predictable for `Other`."""

    def test_valid_structured_type_absent_from_prose_still_warns_but_never_blocks(self):
        # The check is deliberately not silent here -- Section 6's prose is
        # supposed to restate the type per the template -- but it must never
        # affect validity.
        content = _brief("weakness_type: Zero Validation", weakness_label="Something else entirely")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT)
            matches = _by_code(errors, vb.WEAKNESS_TYPE_PROSE_MISMATCH)
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["severity"], "warning")
            import json
            self.assertTrue(json.loads(vb.validation_result_to_json(path, errors))["valid"])
        finally:
            os.remove(path)

    def test_valid_structured_type_different_term_in_prose_warns_nonblocking(self):
        content = _brief("weakness_type: Zero Validation", weakness_label="Contract Mismatch")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT)
            matches = _by_code(errors, vb.WEAKNESS_TYPE_PROSE_MISMATCH)
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["severity"], "warning")
        finally:
            os.remove(path)

    def test_prose_with_multiple_registered_terms_including_structured_value_is_not_misleading(self):
        # Prose names several terms, but one of them IS the structured
        # value -- the substring check finds it, so no mismatch warning
        # (not misled by the extra terms present).
        content = _brief(
            "weakness_type: Zero Validation",
            weakness_label="Zero Validation (related to Contract Mismatch and Vocabulary Drift)",
        )
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT)
            self.assertEqual(_by_code(errors, vb.WEAKNESS_TYPE_PROSE_MISMATCH), [])
        finally:
            os.remove(path)

    def test_other_with_explanation_never_triggers_prose_mismatch(self):
        # "Other" is exempt from this check entirely (common English word;
        # substring matching against it is unpredictable in either
        # direction) -- must behave predictably: never warns, regardless of
        # what Section 6 prose says.
        content = _brief(
            'weakness_type: Other\nweakness_type_explanation: "no registered type fits"',
            weakness_label="Something with no taxonomy term at all",
        )
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT)
            self.assertEqual(_by_code(errors, vb.WEAKNESS_TYPE_PROSE_MISMATCH), [])
        finally:
            os.remove(path)

    def test_other_with_prose_mentioning_a_registered_term_still_no_prose_mismatch(self):
        content = _brief(
            'weakness_type: Other\nweakness_type_explanation: "closest to Ghost Features but not quite"',
            weakness_label="Closest to Ghost Features but not quite",
        )
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT)
            self.assertEqual(_by_code(errors, vb.WEAKNESS_TYPE_PROSE_MISMATCH), [])
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
    """Adversarial coverage for the QUOTE_GROUNDING_WINDOW=3 quote-grounding
    behavior (issue #80 pre-merge review). See scripts/validate-brief.py's
    _quote_found_near() docstring for the design rationale: a small, fixed,
    exact-text (not semantic) window absorbs off-by-a-few-lines citation
    drift without allowing fabricated quotes to pass. Every success case
    here also asserts on the *exact* matched-location detail the validator
    reports, not just pass/fail -- this proves the report states where the
    match actually occurred, not merely "somewhere in the window.\""""

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.target_repo = self._tmpdir.name
        with open(os.path.join(self.target_repo, "example.py"), "w", encoding="utf-8") as f:
            f.write(
                "line one\nline two\nline three\nline four\nline five\n"
                "line six\nline seven\nline eight\nline nine\nline ten\n"
                "line eleven\nline twelve\n"
            )

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
            "primary_fog_type: architecture_fog\n"
            "evidence:\n  - \"example.py: cited for grounding\"\n"
            "recommended_workflow_id: full-local-sensemaking\n"
            "weakest_boundary: fixture\nweakness_type: Zero Validation\n"
            "required_inputs:\n  - repository_sensemaking_brief\n```\n"
        )

    def test_quote_found_exactly_in_cited_range_passes_with_no_window_warning(self):
        """Exact-range match: must pass cleanly, with NO
        EVIDENCE_QUOTE_WINDOW_MATCH warning (that warning is reserved for
        window-only or ambiguous matches)."""
        path = _write_tmp(self._brief_citing("2", "line two"))
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND), [])
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_WINDOW_MATCH), [])
        finally:
            os.remove(path)

    def test_quote_one_line_outside_cited_range_passes_with_reported_location(self):
        # Cited at line 2, quote actually on line 3 -- inside the window,
        # outside the exact cited range. Must pass, but with a non-blocking
        # warning that states the exact matched line.
        path = _write_tmp(self._brief_citing("2", "line three"))
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND), [])
            matches = _by_code(errors, vb.EVIDENCE_QUOTE_WINDOW_MATCH)
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["severity"], "warning")
            self.assertIn("matched at line 3", matches[0]["message"])
            self.assertIn("OUTSIDE the cited range 2-2", matches[0]["message"])
            import json
            self.assertTrue(json.loads(vb.validation_result_to_json(path, errors))["valid"])
        finally:
            os.remove(path)

    def test_quote_three_lines_outside_cited_range_passes_at_window_edge(self):
        # Cited at line 1, quote actually on line 4 -- exactly at the edge
        # of the +/-3 window. Must pass, with the exact matched line reported.
        path = _write_tmp(self._brief_citing("1", "line four"))
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND), [])
            matches = _by_code(errors, vb.EVIDENCE_QUOTE_WINDOW_MATCH)
            self.assertEqual(len(matches), 1)
            self.assertIn("matched at line 4", matches[0]["message"])
        finally:
            os.remove(path)

    def test_quote_four_lines_outside_cited_range_fails(self):
        # Cited at line 1, quote actually on line 5 -- one line beyond the
        # +/-3 window. Must fail (blocking), not silently expand the window.
        path = _write_tmp(self._brief_citing("1", "line five"))
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            matches = _by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND)
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["severity"], "error")
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_WINDOW_MATCH), [])
        finally:
            os.remove(path)

    def test_quote_appearing_twice_in_window_is_ambiguous_but_deterministic(self):
        # "line six" and a second, deliberately duplicated "line six" a few
        # lines later both fall inside the window for a citation of line 6.
        with open(os.path.join(self.target_repo, "dup.py"), "w", encoding="utf-8") as f:
            f.write("alpha\nline six\nbeta\ngamma\nline six\ndelta\n")
        content = self._brief_citing("2", "line six").replace("example.py", "dup.py")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            # Grounded (found), never a hard failure just for being ambiguous.
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND), [])
            matches = _by_code(errors, vb.EVIDENCE_QUOTE_WINDOW_MATCH)
            self.assertEqual(len(matches), 1)
            message = matches[0]["message"]
            # Deterministic tie-break: closest to the cited start line (2) wins -> line 2.
            self.assertIn("matched at line 2", message)
            self.assertIn("AMBIGUOUS", message)
            self.assertIn("also matched at line(s) 5", message)
        finally:
            os.remove(path)

    def test_quote_only_in_a_neighboring_code_block_outside_window_fails(self):
        # The quote genuinely exists in the file, but only far outside the
        # +/-3 window around the citation -- must fail, no whole-file/repo
        # fallback search.
        with open(os.path.join(self.target_repo, "neighbor.py"), "w", encoding="utf-8") as f:
            f.write(
                "def block_one():\n    pass\n\n\n\n\n\n\n\n\n"
                "def block_two():\n    return 'only found here'\n"
            )
        content = self._brief_citing("1", "return 'only found here'").replace("example.py", "neighbor.py")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            matches = _by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND)
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["severity"], "error")
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


class TestWarningErrorSemanticsEndToEnd(unittest.TestCase):
    """Pre-merge review item 5: prove warning/error semantics hold through
    the REAL CLI entrypoint (subprocess against scripts/validate-brief.py),
    not just the in-process validate_brief()/validation_result_to_json()
    helpers -- both --json and the human-readable text mode, for every
    warning code and a representative blocking code."""

    VALIDATOR = os.path.join(SCRIPTS_DIR, "validate-brief.py")

    def _run(self, path, *, target_repo=None, as_json=True):
        import subprocess
        cmd = [sys.executable, self.VALIDATOR, path, "--repo-root", REPO_ROOT]
        if target_repo:
            cmd += ["--target-repo", target_repo]
        if as_json:
            cmd.append("--json")
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode, result.stdout

    def _assert_warning_only(self, content, code):
        path = _write_tmp(content)
        try:
            code_json, stdout_json = self._run(path, as_json=True)
            self.assertEqual(code_json, 0, stdout_json)
            import json
            result = json.loads(stdout_json)
            self.assertTrue(result["valid"])
            self.assertTrue(any(e["message"].startswith(f"{code}:") for e in result["errors"]), stdout_json)
            matching = [e for e in result["errors"] if e["message"].startswith(f"{code}:")]
            self.assertTrue(all(e["severity"] == "warning" for e in matching))

            code_text, stdout_text = self._run(path, as_json=False)
            self.assertEqual(code_text, 0, stdout_text)
            self.assertIn(code, stdout_text)
            self.assertIn("WARNING", stdout_text)
        finally:
            os.remove(path)

    def _assert_blocking(self, content, code, target_repo=None):
        path = _write_tmp(content)
        try:
            code_json, stdout_json = self._run(path, target_repo=target_repo, as_json=True)
            self.assertEqual(code_json, 1, stdout_json)
            import json
            result = json.loads(stdout_json)
            self.assertFalse(result["valid"])
            matching = [e for e in result["errors"] if e["message"].startswith(f"{code}:")]
            self.assertTrue(matching, stdout_json)
            self.assertTrue(all(e["severity"] == "error" for e in matching))

            code_text, stdout_text = self._run(path, target_repo=target_repo, as_json=False)
            self.assertEqual(code_text, 1, stdout_text)
            self.assertIn(code, stdout_text)
            self.assertIn("ERROR", stdout_text)
        finally:
            os.remove(path)

    def test_weakness_type_missing_end_to_end(self):
        self._assert_warning_only(_brief(""), vb.WEAKNESS_TYPE_MISSING)

    def test_weakness_type_unknown_end_to_end(self):
        self._assert_warning_only(
            _brief("weakness_type: Not A Real Type", weakness_label="Not A Real Type"),
            vb.WEAKNESS_TYPE_UNKNOWN,
        )

    def test_weakness_type_other_no_explanation_end_to_end(self):
        self._assert_warning_only(
            _brief("weakness_type: Other", weakness_label="Other"),
            vb.WEAKNESS_TYPE_OTHER_NO_EXPLANATION,
        )

    def test_weakness_type_malformed_end_to_end(self):
        self._assert_blocking(
            _brief("weakness_type:\n  - Zero Validation\n  - Safety Gaps"),
            vb.WEAKNESS_TYPE_MALFORMED,
        )

    def test_high_risk_claim_needs_substantive_audit_end_to_end(self):
        self._assert_warning_only(
            _brief("weakness_type: Safety Gaps", weakness_label="Safety Gaps"),
            vb.HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT,
        )

    def test_evidence_quote_not_found_end_to_end(self):
        with tempfile.TemporaryDirectory() as target_repo:
            with open(os.path.join(target_repo, "example.py"), "w", encoding="utf-8") as f:
                f.write("alpha\nbeta\ngamma\n")
            content = (
                "# Brief\n\n## 6. Weakest boundary\nZero Validation: fixture.\n\n"
                "## 7. Evidence\n- example.py cited.\n\nLogic trace: example.py "
                "supports this fixture's weakest-boundary claim.\n\n"
                "## 8. Evidence excerpts\n```yaml\nevidence_excerpts:\n"
                "  - file: example.py\n    lines: 2\n    quote: \"this text is not in the file\"\n"
                "    supports_claim: \"demonstrates grounding\"\n```\n\n"
                "## 13. Machine-readable handoff\n```yaml\n"
                "primary_fog_type: architecture_fog\n"
                "evidence:\n  - \"example.py: cited\"\n"
                "recommended_workflow_id: full-local-sensemaking\n"
                "weakest_boundary: fixture\nweakness_type: Zero Validation\n"
                "required_inputs:\n  - repository_sensemaking_brief\n```\n"
            )
            self._assert_blocking(content, vb.EVIDENCE_QUOTE_NOT_FOUND, target_repo=target_repo)


if __name__ == "__main__":
    unittest.main()
