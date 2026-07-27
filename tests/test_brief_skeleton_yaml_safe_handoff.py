"""Regression tests for the Evidence 0014 HANDOFF_YAML_PARSE_ERROR defect.

Root cause (see scripts/brief_skeleton.py `reconcile()`): the `evidence` and
`required_inputs` Section 13 fields used to be built by hand with an f-string
(`f'  - "{v}"'`) that wrapped a raw model/harvested string value in a fresh
pair of double quotes with no escaping. Any embedded, unescaped double quote
in that string produced syntactically invalid YAML -- exactly what Evidence
0014's preserved artifact contains:

    - "src/auteur/__init__.py (L1): __version__ = "0.35.0" -- ..."

`reconcile()` now serializes these fields through a real YAML dumper
(`yaml.dump` with the existing `_QuotedStr`/`_EvidenceExcerptDumper`
machinery already used for evidence_excerpts quotes), so pyyaml -- not
hand-rolled string interpolation -- owns escaping.

These tests do NOT modify or re-run Evidence 0014; they exercise the
corrected runtime function against synthetic input isolating the same
defect, per task authorization (no historical evidence may be edited or
reprocessed).
"""

import os
import sys
import unittest

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, SCRIPTS_DIR)

import yaml  # noqa: E402

import brief_skeleton as bs  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))

# The exact Evidence 0014 evidence string (single-quoted here purely so this
# Python source file stays syntactically valid; brief_skeleton.reconcile()
# never sees Python quoting, only the YAML text below).
EVIDENCE_0014_STRING = (
    'src/auteur/__init__.py (L1): __version__ = "0.35.0" -- '
    "ground-truth current version"
)


def _model_output_with_evidence(evidence_yaml_list_item: str) -> str:
    return f"""
```yaml
primary_fog_type: architecture_fog
user_implied_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - {evidence_yaml_list_item}
recommended_workflow_id: docs-aligner
recommended_execution_mode: plan_only
weakest_boundary: version-drift
weakness_type: Other
weakness_type_explanation: test
```
"""


class TestHandoffYamlRoundTrips(unittest.TestCase):
    """`handoff_yaml_round_trips()` is the new explicit parseability check
    (distinct from `skeleton_integrity_ok`, which is structural only)."""

    def test_fresh_skeleton_round_trips(self):
        ok, reason = bs.handoff_yaml_round_trips(bs.build_skeleton())
        self.assertTrue(ok, reason)

    def test_structural_integrity_does_not_imply_yaml_validity(self):
        # Documents the exact Evidence 0014 gap: integrity_ok can be True
        # (markers/headings present) while the YAML itself is broken.
        # Hand-build a document that passes skeleton_integrity_ok's string
        # checks but has an invalid Section 13 fence.
        base = bs.build_skeleton()
        broken = base.replace(
            'evidence: []  # model fills: list of "path/to/file (lines Lx-Ly): citation"',
            f'evidence:\n  - "{EVIDENCE_0014_STRING}"',
        )
        self.assertTrue(bs.skeleton_integrity_ok(broken))
        ok, reason = bs.handoff_yaml_round_trips(broken)
        self.assertFalse(ok)
        self.assertIn("YAML_PARSE_ERROR", reason)


class TestEvidenceSerializationEvidence0014(unittest.TestCase):
    """Decisive regression: the exact malformed Evidence 0014 evidence
    string, supplied as a properly single-quoted YAML scalar by the model
    (the model's own YAML is valid -- the runtime's re-serialization step
    was the defect), must survive reconcile() as parseable YAML with the
    semantic string preserved exactly.
    """

    def _reconcile_with_evidence(self, item: str):
        model_output = _model_output_with_evidence(item)
        out = bs.reconcile(model_output)
        ok, reason = bs.handoff_yaml_round_trips(out)
        self.assertTrue(ok, f"handoff did not round-trip: {reason}\n---\n{out}")
        block = bs.extract_handoff_yaml_block(out)
        data = yaml.safe_load(block)
        return out, data

    def test_evidence_0014_embedded_double_quotes(self):
        out, data = self._reconcile_with_evidence(f"'{EVIDENCE_0014_STRING}'")
        self.assertEqual(data["evidence"], [EVIDENCE_0014_STRING])

    def test_embedded_single_quotes(self):
        value = "it's the auteur module's __init__"
        out, data = self._reconcile_with_evidence(f'"{value}"')
        self.assertEqual(data["evidence"], [value])

    def test_mixed_quotes(self):
        value = 'he said "it\'s fine" -- verbatim'
        out, data = self._reconcile_with_evidence(f"'{value.replace(chr(39), chr(39)*2)}'")
        self.assertEqual(data["evidence"], [value])

    def test_colon_inside_string(self):
        value = "src/foo.py (L1): a key: value looking string"
        out, data = self._reconcile_with_evidence(f"'{value}'")
        self.assertEqual(data["evidence"], [value])

    def test_hash_character(self):
        value = "src/foo.py (L1): comment marker # not a real comment"
        out, data = self._reconcile_with_evidence(f"'{value}'")
        self.assertEqual(data["evidence"], [value])

    def test_backslash_windows_path(self):
        value = r"C:\repo\src\foo.py (L1): windows path evidence"
        out, data = self._reconcile_with_evidence(f"'{value}'")
        self.assertEqual(data["evidence"], [value])

    def test_markdown_formatting(self):
        value = "**bold** and _italic_ and [link](http://example.com)"
        out, data = self._reconcile_with_evidence(f"'{value}'")
        self.assertEqual(data["evidence"], [value])

    def test_backticks(self):
        value = "uses `__version__` attribute"
        out, data = self._reconcile_with_evidence(f"'{value}'")
        self.assertEqual(data["evidence"], [value])

    def test_unicode(self):
        value = "src/foo.py (L1): caf\u00e9 na\u00efve \u2014 unicode dash"
        out, data = self._reconcile_with_evidence(f"'{value}'")
        self.assertEqual(data["evidence"], [value])

    def test_multiline_string(self):
        value = "line one\nline two"
        out = bs.reconcile(_model_output_with_evidence('"line one\\nline two"'))
        ok, reason = bs.handoff_yaml_round_trips(out)
        self.assertTrue(ok, reason)
        block = bs.extract_handoff_yaml_block(out)
        data = yaml.safe_load(block)
        self.assertEqual(data["evidence"], [value])

    def test_yaml_looking_text(self):
        value = "key: value\n- list item"
        out, data = self._reconcile_with_evidence('"key: value\\n- list item"')
        self.assertEqual(data["evidence"], [value])

    def test_code_fence_looking_text(self):
        # A literal ``` inside the model's raw text breaks the OUTER
        # ```yaml ... ``` fence the model is instructed to wrap Section 13
        # in (a pre-existing markdown-fence-extraction limitation of
        # `_YAML_BLOCK_RE`, orthogonal to the reconcile()-level escaping
        # bug this test suite targets) -- the harvester's regex closes on
        # the first ``` it sees, so this field is not harvested at all.
        # That is a safe failure mode (no field harvested -> the runtime's
        # own placeholder/empty value survives, still valid YAML; the real
        # validator flags the resulting missing/empty evidence field) as
        # opposed to Evidence 0014's failure mode (a field IS harvested,
        # but the runtime's OWN re-serialization step then emits invalid
        # YAML). This test pins that safe-failure behavior: the reconciled
        # artifact still round-trips as valid YAML even when the model's
        # raw text contains a nested code fence.
        out = bs.reconcile(_model_output_with_evidence('"```python\\nprint(1)\\n```"'))
        ok, reason = bs.handoff_yaml_round_trips(out)
        self.assertTrue(ok, reason)

    def test_empty_string(self):
        out, data = self._reconcile_with_evidence('""')
        self.assertEqual(data["evidence"], [""])

    def test_null_looking_text(self):
        out, data = self._reconcile_with_evidence('"null"')
        self.assertEqual(data["evidence"], ["null"])

    def test_boolean_looking_text(self):
        for word in ("yes", "no", "true"):
            with self.subTest(word=word):
                out, data = self._reconcile_with_evidence(f'"{word}"')
                self.assertEqual(data["evidence"], [word])

    def test_numeric_looking_text(self):
        out, data = self._reconcile_with_evidence('"12345"')
        self.assertEqual(data["evidence"], ["12345"])

    def test_crlf_input(self):
        model_output = _model_output_with_evidence(f"'{EVIDENCE_0014_STRING}'").replace("\n", "\r\n")
        out = bs.reconcile(model_output)
        ok, reason = bs.handoff_yaml_round_trips(out)
        self.assertTrue(ok, reason)

    def test_lf_input(self):
        model_output = _model_output_with_evidence(f"'{EVIDENCE_0014_STRING}'")
        self.assertNotIn("\r\n", model_output)
        out = bs.reconcile(model_output)
        ok, reason = bs.handoff_yaml_round_trips(out)
        self.assertTrue(ok, reason)

    def test_multiple_evidence_entries(self):
        model_output = f"""
```yaml
primary_fog_type: architecture_fog
user_implied_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - '{EVIDENCE_0014_STRING}'
  - 'second entry with "quotes" too'
  - plain unquoted entry
recommended_workflow_id: docs-aligner
recommended_execution_mode: plan_only
weakest_boundary: version-drift
weakness_type: Other
weakness_type_explanation: test
```
"""
        out = bs.reconcile(model_output)
        ok, reason = bs.handoff_yaml_round_trips(out)
        self.assertTrue(ok, reason)
        data = yaml.safe_load(bs.extract_handoff_yaml_block(out))
        self.assertEqual(
            data["evidence"],
            [EVIDENCE_0014_STRING, 'second entry with "quotes" too', "plain unquoted entry"],
        )


class TestRuntimeOwnedFieldsUnaffected(unittest.TestCase):
    """The fix must not disturb runtime-owned fields, duplicate-key
    safeguards, or PR #99's generic artifact_id routing."""

    def test_missing_runtime_owned_field_still_supplied_by_skeleton(self):
        # reconcile() always rebuilds from a fresh skeleton -- runtime-owned
        # fields can never be omitted regardless of model output.
        out = bs.reconcile("no yaml at all")
        self.assertIn(f"artifact_id: {bs.ARTIFACT_ID}", out)
        ok, reason = bs.handoff_yaml_round_trips(out)
        self.assertTrue(ok, reason)

    def test_conflicting_runtime_owned_artifact_id_ignored(self):
        model_output = """
```yaml
artifact_id: something_else
primary_fog_type: architecture_fog
```
"""
        out = bs.reconcile(model_output)
        self.assertIn(f"artifact_id: {bs.ARTIFACT_ID}", out)
        self.assertNotIn("artifact_id: something_else", out)
        ok, reason = bs.handoff_yaml_round_trips(out)
        self.assertTrue(ok, reason)

    def test_duplicate_runtime_owned_key_not_introduced(self):
        out = bs.reconcile(_model_output_with_evidence(f"'{EVIDENCE_0014_STRING}'"))
        block = bs.extract_handoff_yaml_block(out)
        self.assertEqual(block.count("artifact_id:"), 1)
        self.assertEqual(block.count("\nevidence:"), 1)

    def test_malformed_model_handoff_does_not_crash_reconcile(self):
        # No fence, garbage text -- reconcile() must never raise.
        out = bs.reconcile(': : : not yaml {{{')
        ok, reason = bs.handoff_yaml_round_trips(out)
        self.assertTrue(ok, reason)

    def test_generic_artifact_id_routing_regression(self):
        # PR #99: generic routing keys off `artifact_id: repository_sensemaking_brief`
        # in Section 13. Confirm the reconciled output still carries it verbatim.
        out = bs.reconcile(_model_output_with_evidence(f"'{EVIDENCE_0014_STRING}'"))
        self.assertIn(f"artifact_id: {bs.ARTIFACT_ID}", out)


class TestValidateBriefIntegration(unittest.TestCase):
    """The real downstream consumer: validate-brief.py must get past YAML
    parsing (Section 13) for a reconciled artifact carrying the exact
    Evidence 0014 evidence string. This does NOT assert full validate-brief
    success (evidence excerpts still need real grounding, logic-trace prose,
    etc.) -- only that HANDOFF_YAML_PARSE_ERROR no longer occurs.
    """

    @classmethod
    def setUpClass(cls):
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "validate_brief", os.path.join(SCRIPTS_DIR, "validate-brief.py")
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls.validate_brief = staticmethod(module.validate_brief)

    def test_no_handoff_yaml_parse_error_for_reconciled_evidence_0014_string(self):
        import tempfile

        out = bs.reconcile(_model_output_with_evidence(f"'{EVIDENCE_0014_STRING}'"))
        fd, path = tempfile.mkstemp(suffix=".md")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(out)
            errors = self.validate_brief(path, repo_root=REPO_ROOT)
        finally:
            os.remove(path)
        combined = " ".join(str(e) for e in errors)
        self.assertNotIn("HANDOFF_YAML_PARSE_ERROR", combined)


if __name__ == "__main__":
    unittest.main()
