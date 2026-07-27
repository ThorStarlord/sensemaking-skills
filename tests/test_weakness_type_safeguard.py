"""Tests for scripts/weakness_type_safeguard.py (issue #90).

Covers the section-aware, duplicate-key-safe weakness_type safeguard that
replaces the document-wide regex safeguard Evidence 0013
(experiments/evidence/0013-stage1-auteur-run-model-enforcement/) found
grabbed the wrong yaml fence. No real model/network call.
"""

import os
import sys
import unittest

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, SCRIPTS_DIR)

import weakness_type_safeguard as wts  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "weakness-type-safeguard")
EVIDENCE_0013_BRIEF = os.path.join(
    REPO_ROOT,
    "experiments",
    "evidence",
    "0013-stage1-auteur-run-model-enforcement",
    "repository_sensemaking_brief.md",
)


def _canonical_valid_brief(weakness_type_block: str = "weakness_type: Vocabulary Drift") -> str:
    return f"""# Repository Sensemaking Brief

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: a.py
    lines: L1
    quote: "x"
    supports_claim: "y"
```

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
{weakness_type_block}
required_inputs:
  - user_intent
immutable: true
```
"""


class TestSectionScopedExtraction(unittest.TestCase):
    def test_multiple_fences_only_section_13_authoritative(self):
        text = _canonical_valid_brief()
        result = wts.check(text)
        self.assertEqual(result.outcome, wts.EXACTLY_ONE_WEAKNESS_TYPE_KEY)
        self.assertEqual(result.weakness_type_value, "Vocabulary Drift")
        self.assertEqual(result.exit_code, 0)

    def test_missing_section_13(self):
        text = "# Brief\n\n## 8. Evidence excerpts\n\n```yaml\nweakness_type: X\n```\n"
        result = wts.check(text)
        self.assertEqual(result.outcome, wts.NO_AUTHORITATIVE_SECTION)
        self.assertEqual(result.exit_code, 2)

    def test_section_13_with_no_yaml_block(self):
        text = "# Brief\n\n## 13. Machine-readable handoff\n\nNo fence here at all.\n"
        result = wts.check(text)
        self.assertEqual(result.outcome, wts.NO_AUTHORITATIVE_BLOCK)
        self.assertEqual(result.exit_code, 2)

    def test_unterminated_fence(self):
        text = "# Brief\n\n## 13. Machine-readable handoff\n\n```yaml\nweakness_type: X\n"
        result = wts.check(text)
        self.assertEqual(result.outcome, wts.MALFORMED_FENCE)
        self.assertEqual(result.exit_code, 3)

    def test_nested_opening_fence_inside_section_13(self):
        text = (
            "# Brief\n\n## 13. Machine-readable handoff\n\n"
            "```yaml\n<!-- comment -->\n\n```yaml\nweakness_type: X\n```\n```\n"
        )
        result = wts.check(text)
        self.assertEqual(result.outcome, wts.MALFORMED_FENCE)
        self.assertEqual(result.exit_code, 3)

    def test_multiple_independent_blocks_in_section_ambiguous(self):
        text = (
            "# Brief\n\n## 13. Machine-readable handoff\n\n"
            "```yaml\nweakness_type: X\n```\n\nSome text.\n\n```yaml\nweakness_type: Y\n```\n"
        )
        result = wts.check(text)
        self.assertEqual(result.outcome, wts.MALFORMED_FENCE)
        self.assertEqual(result.exit_code, 3)

    def test_section_13_bounded_by_next_heading_of_same_level(self):
        text = (
            "# Brief\n\n## 13. Machine-readable handoff\n\n"
            "```yaml\nweakness_type: X\n```\n\n"
            "## 14. Ready-to-copy prompt\n\n```yaml\nweakness_type: SHOULD_NOT_COUNT\n```\n"
        )
        result = wts.check(text)
        self.assertEqual(result.outcome, wts.EXACTLY_ONE_WEAKNESS_TYPE_KEY)
        self.assertEqual(result.weakness_type_value, "X")


class TestWeaknessTypeCounts(unittest.TestCase):
    def test_zero_weakness_type_keys(self):
        text = _canonical_valid_brief(weakness_type_block="other_field: 1")
        result = wts.check(text)
        self.assertEqual(result.outcome, wts.ZERO_WEAKNESS_TYPE_KEYS)
        self.assertEqual(result.exit_code, 2)

    def test_exactly_one_weakness_type_key(self):
        text = _canonical_valid_brief()
        result = wts.check(text)
        self.assertEqual(result.outcome, wts.EXACTLY_ONE_WEAKNESS_TYPE_KEY)
        self.assertEqual(result.exit_code, 0)

    def test_two_top_level_duplicates(self):
        text = _canonical_valid_brief(
            weakness_type_block="weakness_type: Vocabulary Drift\nweakness_type: Contract Mismatch"
        )
        result = wts.check(text)
        self.assertEqual(result.outcome, wts.DUPLICATE_WEAKNESS_TYPE_KEYS)
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.duplicate_count, 2)

    def test_duplicates_separated_by_comments_and_blank_lines(self):
        text = _canonical_valid_brief(
            weakness_type_block=(
                "weakness_type: Vocabulary Drift\n"
                "# a comment\n\n"
                "other_field: 1\n"
                "weakness_type: Contract Mismatch"
            )
        )
        result = wts.check(text)
        self.assertEqual(result.outcome, wts.DUPLICATE_WEAKNESS_TYPE_KEYS)

    def test_nested_non_authoritative_plus_one_authoritative_is_not_duplicate(self):
        text = _canonical_valid_brief(
            weakness_type_block=(
                "weakness_type: Vocabulary Drift\n"
                "metadata:\n"
                "  weakness_type: nested_should_not_count\n"
            )
        )
        result = wts.check(text)
        self.assertEqual(result.outcome, wts.EXACTLY_ONE_WEAKNESS_TYPE_KEY)
        self.assertEqual(result.weakness_type_value, "Vocabulary Drift")

    def test_other_plus_explanation_is_valid(self):
        text = _canonical_valid_brief(
            weakness_type_block=(
                'weakness_type: Other\n'
                'weakness_type_explanation: "a custom category"'
            )
        )
        result = wts.check(text)
        self.assertEqual(result.outcome, wts.EXACTLY_ONE_WEAKNESS_TYPE_KEY)
        self.assertEqual(result.weakness_type_value, "Other")

    def test_last_value_wins_never_silently_accepted(self):
        # A plain yaml.safe_load of this block would silently return
        # "Contract Mismatch" (last value wins) with no error at all.
        # The safeguard must not do that -- it must classify this as a
        # hard-stop duplicate, never as EXACTLY_ONE with the last value.
        text = _canonical_valid_brief(
            weakness_type_block="weakness_type: Vocabulary Drift\nweakness_type: Contract Mismatch"
        )
        result = wts.check(text)
        self.assertNotEqual(result.outcome, wts.EXACTLY_ONE_WEAKNESS_TYPE_KEY)
        self.assertEqual(result.outcome, wts.DUPLICATE_WEAKNESS_TYPE_KEYS)

    def test_unrelated_invalid_yaml(self):
        text = _canonical_valid_brief(weakness_type_block="weakness_type: [unterminated")
        result = wts.check(text)
        self.assertEqual(result.outcome, wts.YAML_PARSE_ERROR)
        self.assertEqual(result.exit_code, 4)

    def test_duplicate_key_unrelated_to_weakness_type(self):
        text = _canonical_valid_brief(
            weakness_type_block="weakness_type: Vocabulary Drift\nother_field: 1\nother_field: 2"
        )
        result = wts.check(text)
        self.assertEqual(result.outcome, wts.YAML_PARSE_ERROR)


class TestLineEndings(unittest.TestCase):
    def test_crlf_input(self):
        text = _canonical_valid_brief().replace("\n", "\r\n")
        result = wts.check(text)
        self.assertEqual(result.outcome, wts.EXACTLY_ONE_WEAKNESS_TYPE_KEY)

    def test_lf_input(self):
        text = _canonical_valid_brief()
        result = wts.check(text)
        self.assertEqual(result.outcome, wts.EXACTLY_ONE_WEAKNESS_TYPE_KEY)


class TestDeterminism(unittest.TestCase):
    def test_deterministic_output_reproducible(self):
        text = _canonical_valid_brief()
        r1 = wts.check(text)
        r2 = wts.check(text)
        self.assertEqual(r1.outcome, r2.outcome)
        self.assertEqual(r1.exit_code, r2.exit_code)
        self.assertEqual(r1.weakness_type_value, r2.weakness_type_value)


class TestEvidence0013Reconstruction(unittest.TestCase):
    """Reconstructs Evidence 0013's real Section 8 malformed doubled/nested
    fence via a fixture copy (tests/fixtures/weakness-type-safeguard/), never
    by editing the evidence directory itself, and proves Section 13 is still
    correctly classified despite it."""

    def test_reconstructed_doubled_section8_fence_does_not_break_section_13(self):
        path = os.path.join(FIXTURES_DIR, "reconstructed_doubled_section8_fence.md")
        with open(path, encoding="utf-8") as f:
            text = f.read()
        result = wts.check(text)
        self.assertEqual(result.outcome, wts.EXACTLY_ONE_WEAKNESS_TYPE_KEY)
        self.assertEqual(result.weakness_type_value, "Vocabulary Drift")


class TestRealEvidence0013Brief(unittest.TestCase):
    """Runs against the real, unmodified Evidence 0013 brief file
    (read-only) and proves the corrected safeguard reports the true
    structural state (exactly one weakness_type key in Section 13),
    unlike the old regex safeguard which reported "no weakness_type key
    found" because it grabbed Section 8's malformed fence instead."""

    def test_real_evidence_0013_brief_classifies_correctly(self):
        self.assertTrue(
            os.path.isfile(EVIDENCE_0013_BRIEF),
            f"expected evidence file at {EVIDENCE_0013_BRIEF}",
        )
        with open(EVIDENCE_0013_BRIEF, encoding="utf-8") as f:
            text = f.read()
        result = wts.check(text)
        self.assertEqual(
            result.outcome,
            wts.EXACTLY_ONE_WEAKNESS_TYPE_KEY,
            f"expected EXACTLY_ONE_WEAKNESS_TYPE_KEY, got {result.outcome}: {result.detail}",
        )
        self.assertEqual(result.weakness_type_value, "Vocabulary Drift")


class TestCanonicalBriefPasses(unittest.TestCase):
    def test_canonical_skeleton_with_weakness_type_passes(self):
        import brief_skeleton as bs

        skel = bs.build_skeleton()
        filled = skel.replace(
            "weakness_type:  # model fills: one of the registered types in "
            "skills/repo-sensemaker/references/weakness-types.md, or 'Other'",
            "weakness_type: Zero Validation",
        )
        result = wts.check(filled)
        self.assertEqual(result.outcome, wts.EXACTLY_ONE_WEAKNESS_TYPE_KEY)
        self.assertEqual(result.weakness_type_value, "Zero Validation")


class TestCLI(unittest.TestCase):
    def test_cli_exit_code_zero_on_pass(self):
        import subprocess

        path = os.path.join(FIXTURES_DIR, "reconstructed_doubled_section8_fence.md")
        proc = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS_DIR, "weakness_type_safeguard.py"), path],
            capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("EXACTLY_ONE_WEAKNESS_TYPE_KEY", proc.stdout)

    def test_cli_ascii_only_output(self):
        import subprocess

        path = os.path.join(FIXTURES_DIR, "reconstructed_doubled_section8_fence.md")
        proc = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS_DIR, "weakness_type_safeguard.py"), path],
            capture_output=True, text=True,
        )
        combined = proc.stdout + proc.stderr
        combined.encode("ascii")  # raises UnicodeEncodeError if non-ASCII present


if __name__ == "__main__":
    unittest.main()
