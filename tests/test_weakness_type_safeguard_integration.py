"""Integration tests for issue #93: scripts/weakness_type_safeguard.py wired
into scripts/validate-brief.py's validate_brief().

PR #92 added the section-aware, duplicate-key-safe safeguard as a standalone
tested module (issue #90) but, per its scope boundary, did NOT wire it into
validate-brief.py. This suite covers that integration: the safeguard's
outcomes must surface as blocking validate_brief() errors with their own
stable error codes, while all pre-existing validate-brief.py behavior
(weakness_type enum/"Other"/explanation checks, evidence-quote grounding,
etc.) continues to work unchanged.
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

EVIDENCE_0013_BRIEF = os.path.join(
    REPO_ROOT,
    "experiments",
    "evidence",
    "0013-stage1-auteur-run-model-enforcement",
    "repository_sensemaking_brief.md",
)


def _by_code(errors, code):
    return [e for e in errors if e["message"].startswith(f"{code}:")]


def _is_blocking(errors, code):
    matches = _by_code(errors, code)
    return bool(matches) and all(vb._is_blocking(e) for e in matches)


def _write_tmp(content: str) -> str:
    fd, path = tempfile.mkstemp(suffix=".md")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(content)
    return path


# Minimal brief bodies. Section 8 is included (and sometimes deliberately
# malformed) to reproduce the exact Evidence 0013 regression shape; Section
# 13 is the authoritative block under test.
def _brief(section13_yaml: str, section8_block: str | None = None) -> str:
    section8 = section8_block if section8_block is not None else (
        "```yaml\n"
        "evidence_excerpts:\n"
        "  - file: skills/repo-sensemaker/references/weakness-types.md\n"
        "    lines: L1\n"
        '    quote: "# Weakness Types in Repositories"\n'
        '    supports_claim: "Confirms the taxonomy reference file exists."\n'
        "```\n"
    )
    return f"""# Repository Sensemaking Brief (safeguard-integration fixture)

## 1. Repository goal
Fixture.

## 6. Weakest boundary
Fixture weakest-boundary prose.

## 7. Evidence
- `skills/repo-sensemaker/references/weakness-types.md:1` supports this fixture.

Logic trace: fixture chain from evidence to conclusion.

## 8. Evidence excerpts
{section8}

## 12. Recommended workflow
full-local-sensemaking

## 13. Machine-readable handoff
```yaml
{section13_yaml}
```

## 14. Ready-to-copy prompt
N/A -- test fixture.
"""


VALID_S13 = """artifact_id: repository_sensemaking_brief
primary_fog_type: architecture_fog
evidence:
  - "skills/repo-sensemaker/references/weakness-types.md: taxonomy reference"
recommended_workflow_id: full-local-sensemaking
recommended_execution_mode: plan_only
weakest_boundary: fixture-boundary
weakness_type: Zero Validation
required_inputs:
  - repository_sensemaking_brief
created_at: "2026-07-26T00:00:00Z"
immutable: true"""


class TestValidSingleWeaknessType(unittest.TestCase):
    def test_valid_single_weakness_type_no_safeguard_error(self):
        path = _write_tmp(_brief(VALID_S13))
        errors = vb.validate_brief(path, REPO_ROOT)
        for code in (
            vb.DUPLICATE_WEAKNESS_TYPE_KEYS,
            vb.MALFORMED_HANDOFF_FENCE,
            vb.MISSING_HANDOFF_SECTION,
            vb.MISSING_HANDOFF_BLOCK,
            vb.MISSING_WEAKNESS_TYPE,
            vb.HANDOFF_YAML_PARSE_ERROR,
        ):
            self.assertEqual(_by_code(errors, code), [], f"unexpected {code}")


class TestDuplicateTopLevelWeaknessType(unittest.TestCase):
    def _assert_duplicate_blocks(self, section13_yaml):
        path = _write_tmp(_brief(section13_yaml))
        errors = vb.validate_brief(path, REPO_ROOT)
        dup = _by_code(errors, vb.DUPLICATE_WEAKNESS_TYPE_KEYS)
        self.assertTrue(dup, "expected DUPLICATE_WEAKNESS_TYPE_KEYS error")
        self.assertTrue(all(vb._is_blocking(e) for e in dup))
        # Must not be mislabeled as a generic YAML parse failure.
        self.assertEqual(_by_code(errors, vb.HANDOFF_YAML_PARSE_ERROR), [])
        return errors

    def test_duplicate_top_level_weakness_type_blocks(self):
        self._assert_duplicate_blocks(
            "artifact_id: repository_sensemaking_brief\n"
            "weakness_type: Vocabulary Drift\n"
            "weakness_type: Contract Mismatch\n"
            "required_inputs:\n  - repository_sensemaking_brief\n"
            "immutable: true"
        )

    def test_duplicate_separated_by_comments_and_blank_lines_blocks(self):
        self._assert_duplicate_blocks(
            "artifact_id: repository_sensemaking_brief\n"
            "weakness_type: Vocabulary Drift\n"
            "# a comment\n\n"
            "other_field: 1\n"
            "weakness_type: Contract Mismatch\n"
            "required_inputs:\n  - repository_sensemaking_brief\n"
            "immutable: true"
        )


class TestDuplicateUnrelatedKey(unittest.TestCase):
    def test_duplicate_unrelated_top_level_key_is_yaml_parse_error_not_duplicate_weakness(self):
        path = _write_tmp(_brief(
            "artifact_id: repository_sensemaking_brief\n"
            "weakness_type: Vocabulary Drift\n"
            "other_field: 1\n"
            "other_field: 2\n"
            "immutable: true"
        ))
        errors = vb.validate_brief(path, REPO_ROOT)
        self.assertTrue(_by_code(errors, vb.HANDOFF_YAML_PARSE_ERROR))
        self.assertEqual(_by_code(errors, vb.DUPLICATE_WEAKNESS_TYPE_KEYS), [])


class TestNestedPlusTopLevelIsNotDuplicate(unittest.TestCase):
    def test_nested_weakness_type_under_metadata_plus_one_top_level_passes(self):
        path = _write_tmp(_brief(
            "artifact_id: repository_sensemaking_brief\n"
            "weakness_type: Vocabulary Drift\n"
            "metadata:\n"
            "  weakness_type: nested_should_not_count\n"
            "immutable: true"
        ))
        errors = vb.validate_brief(path, REPO_ROOT)
        for code in (vb.DUPLICATE_WEAKNESS_TYPE_KEYS, vb.HANDOFF_YAML_PARSE_ERROR, vb.MISSING_WEAKNESS_TYPE):
            self.assertEqual(_by_code(errors, code), [])


class TestMissingSection13(unittest.TestCase):
    def test_missing_section_13_heading_blocks(self):
        content = _brief(VALID_S13).replace("## 13. Machine-readable handoff", "## 13x. Not the real heading")
        path = _write_tmp(content)
        errors = vb.validate_brief(path, REPO_ROOT)
        self.assertTrue(_by_code(errors, vb.MISSING_HANDOFF_SECTION))


class TestSection13NoYamlFence(unittest.TestCase):
    def test_section_13_present_no_yaml_fence_blocks(self):
        content = """# Repository Sensemaking Brief

## 13. Machine-readable handoff
No fenced block here at all.

## 14. Ready-to-copy prompt
N/A
"""
        path = _write_tmp(content)
        errors = vb.validate_brief(path, REPO_ROOT)
        self.assertTrue(_by_code(errors, vb.MISSING_HANDOFF_BLOCK))


_EVIDENCE_EXCERPTS_BLOCK = (
    "```yaml\n"
    "evidence_excerpts:\n"
    "  - file: skills/repo-sensemaker/references/weakness-types.md\n"
    "    lines: L1\n"
    '    quote: "# Weakness Types in Repositories"\n'
    '    supports_claim: "Confirms the taxonomy reference file exists."\n'
    "```\n"
)


class TestMalformedFence(unittest.TestCase):
    """The fallback ``_parse_artifact_data`` path (last yaml block in the
    document) needs a well-formed dict-shaped yaml block elsewhere (Section
    8's evidence_excerpts) present in these fixtures so legacy parsing has
    something sane to fall back to -- the malformed-fence assertion here is
    about the NEW safeguard's Section 13 check, not the legacy fallback."""

    def test_unterminated_fence_blocks(self):
        content = f"""# Repository Sensemaking Brief

## 8. Evidence excerpts
{_EVIDENCE_EXCERPTS_BLOCK}

## 13. Machine-readable handoff
```yaml
weakness_type: Vocabulary Drift
"""
        path = _write_tmp(content)
        errors = vb.validate_brief(path, REPO_ROOT)
        self.assertTrue(_by_code(errors, vb.MALFORMED_HANDOFF_FENCE))

    def test_doubled_nested_opening_fence_blocks(self):
        content = (
            "# Repository Sensemaking Brief\n\n"
            f"## 8. Evidence excerpts\n{_EVIDENCE_EXCERPTS_BLOCK}\n"
            "## 13. Machine-readable handoff\n\n"
            "```yaml\n<!-- comment -->\n\n```yaml\nweakness_type: X\n```\n```\n"
        )
        path = _write_tmp(content)
        errors = vb.validate_brief(path, REPO_ROOT)
        self.assertTrue(_by_code(errors, vb.MALFORMED_HANDOFF_FENCE))

    def test_multiple_candidate_blocks_in_section_13_blocks(self):
        content = (
            "# Repository Sensemaking Brief\n\n"
            f"## 8. Evidence excerpts\n{_EVIDENCE_EXCERPTS_BLOCK}\n"
            "## 13. Machine-readable handoff\n\n"
            "```yaml\nweakness_type: X\n```\n\nSome text.\n\n```yaml\nweakness_type: Y\n```\n"
        )
        path = _write_tmp(content)
        errors = vb.validate_brief(path, REPO_ROOT)
        self.assertTrue(_by_code(errors, vb.MALFORMED_HANDOFF_FENCE))


class TestEvidence0013RegressionScenario(unittest.TestCase):
    """The exact Evidence 0013 regression: a malformed doubled fence in an
    earlier section (reconstructed here, not the real evidence file) must
    not cause the validator to inspect the wrong block or falsely fail a
    valid Section 13."""

    def test_malformed_earlier_section_does_not_break_valid_section_13(self):
        malformed_section8 = "```yaml\n<!-- comment -->\n\n```yaml\nweakness_type: WRONG\n```\n```\n"
        content = _brief(VALID_S13, section8_block=malformed_section8)
        path = _write_tmp(content)
        errors = vb.validate_brief(path, REPO_ROOT)
        for code in (
            vb.DUPLICATE_WEAKNESS_TYPE_KEYS,
            vb.MALFORMED_HANDOFF_FENCE,
            vb.MISSING_HANDOFF_SECTION,
            vb.MISSING_HANDOFF_BLOCK,
            vb.MISSING_WEAKNESS_TYPE,
            vb.HANDOFF_YAML_PARSE_ERROR,
        ):
            self.assertEqual(_by_code(errors, code), [], f"unexpected {code}")


class TestZeroWeaknessTypeKeys(unittest.TestCase):
    def test_zero_weakness_type_keys_reported_but_non_blocking(self):
        # Deliberately non-blocking: preserves the ratified D2 decision that
        # missing weakness_type metadata never invalidates the brief.
        path = _write_tmp(_brief(
            "artifact_id: repository_sensemaking_brief\n"
            "other_field: 1\n"
            "immutable: true"
        ))
        errors = vb.validate_brief(path, REPO_ROOT)
        matches = _by_code(errors, vb.MISSING_WEAKNESS_TYPE)
        self.assertTrue(matches)
        self.assertFalse(vb._is_blocking(matches[0]))


class TestOtherWithAndWithoutExplanation(unittest.TestCase):
    def test_other_with_explanation_passes_existing_behavior(self):
        path = _write_tmp(_brief(
            "artifact_id: repository_sensemaking_brief\n"
            'weakness_type: Other\n'
            'weakness_type_explanation: "a custom category"\n'
            "immutable: true"
        ))
        errors = vb.validate_brief(path, REPO_ROOT)
        self.assertEqual(_by_code(errors, vb.WEAKNESS_TYPE_OTHER_NO_EXPLANATION), [])
        self.assertEqual(_by_code(errors, vb.DUPLICATE_WEAKNESS_TYPE_KEYS), [])

    def test_other_without_explanation_still_warns_existing_behavior(self):
        path = _write_tmp(_brief(
            "artifact_id: repository_sensemaking_brief\n"
            "weakness_type: Other\n"
            "immutable: true"
        ))
        errors = vb.validate_brief(path, REPO_ROOT)
        matches = _by_code(errors, vb.WEAKNESS_TYPE_OTHER_NO_EXPLANATION)
        self.assertTrue(matches)
        self.assertFalse(vb._is_blocking(matches[0]), "existing behavior: this is a warning, not blocking")


class TestNonStringWeaknessTypeValue(unittest.TestCase):
    def test_list_valued_weakness_type_still_hits_existing_malformed_check(self):
        path = _write_tmp(_brief(
            "artifact_id: repository_sensemaking_brief\n"
            "weakness_type:\n  - Zero Validation\n  - Safety Gaps\n"
            "immutable: true"
        ))
        errors = vb.validate_brief(path, REPO_ROOT)
        self.assertTrue(_by_code(errors, vb.WEAKNESS_TYPE_MALFORMED))
        # The safeguard only checks key structure, not value type -- a
        # single top-level key (even list-valued) is not a duplicate.
        self.assertEqual(_by_code(errors, vb.DUPLICATE_WEAKNESS_TYPE_KEYS), [])


class TestGeneralInvalidYaml(unittest.TestCase):
    def test_bad_indentation_yaml_syntax_error_blocks_with_handoff_parse_error(self):
        content = (
            "# Repository Sensemaking Brief\n\n"
            "## 13. Machine-readable handoff\n\n"
            "```yaml\n"
            "artifact_id: repository_sensemaking_brief\n"
            "weakness_type: Vocabulary Drift\n"
            "  bad_indent: [oops\n"
            "```\n"
        )
        path = _write_tmp(content)
        errors = vb.validate_brief(path, REPO_ROOT)
        self.assertTrue(_by_code(errors, vb.HANDOFF_YAML_PARSE_ERROR))


class TestAnchorsAndAliases(unittest.TestCase):
    def test_yaml_anchor_alias_single_weakness_type_passes(self):
        content = (
            "# Repository Sensemaking Brief\n\n"
            "## 13. Machine-readable handoff\n\n"
            "```yaml\n"
            "artifact_id: repository_sensemaking_brief\n"
            "canonical_type: &wt_anchor Vocabulary Drift\n"
            "weakness_type: *wt_anchor\n"
            "immutable: true\n"
            "```\n"
        )
        path = _write_tmp(content)
        errors = vb.validate_brief(path, REPO_ROOT)
        for code in (vb.DUPLICATE_WEAKNESS_TYPE_KEYS, vb.MALFORMED_HANDOFF_FENCE, vb.HANDOFF_YAML_PARSE_ERROR):
            self.assertEqual(_by_code(errors, code), [])


class TestRealEvidence0013IntegratedValidation(unittest.TestCase):
    """Read-only: runs the INTEGRATED validate_brief() against the real,
    unmodified Evidence 0013 brief file. Confirms the safeguard-specific
    outcome is clean (no DUPLICATE/MALFORMED/MISSING blocking error) but the
    overall validate_brief() result is still FAIL due to Evidence 0013's
    pre-existing, unrelated failures (this integration must not paper over
    those or claim the brief is newly valid)."""

    def test_evidence_0013_safeguard_clean_but_overall_result_still_fails(self):
        self.assertTrue(
            os.path.isfile(EVIDENCE_0013_BRIEF),
            f"expected evidence file at {EVIDENCE_0013_BRIEF}",
        )
        errors = vb.validate_brief(EVIDENCE_0013_BRIEF, REPO_ROOT)

        for code in (
            vb.DUPLICATE_WEAKNESS_TYPE_KEYS,
            vb.MALFORMED_HANDOFF_FENCE,
            vb.MISSING_HANDOFF_SECTION,
            vb.MISSING_HANDOFF_BLOCK,
            vb.MISSING_WEAKNESS_TYPE,
            vb.HANDOFF_YAML_PARSE_ERROR,
        ):
            self.assertEqual(
                _by_code(errors, code), [],
                f"Evidence 0013's real Section 13 should be structurally clean; got {code}",
            )

        blocking = [e for e in errors if vb._is_blocking(e)]
        self.assertTrue(
            blocking,
            "Evidence 0013 is expected to still FAIL overall due to pre-existing "
            "unrelated failures (e.g. quote-fidelity); this integration must not "
            "make it newly pass.",
        )


if __name__ == "__main__":
    unittest.main()
