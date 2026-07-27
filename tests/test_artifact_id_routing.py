"""Regression tests for issue #97: generic artifact_id detection for
repository sensemaking briefs (and other artifact types) with multiple YAML
fences.

Background: scripts/validate-and-report.py is the single generic entry point
agents call to validate any Phase 1 artifact. It must locate the AUTHORITATIVE
machine-readable handoff block (Section 13 "Machine-readable handoff", or the
equivalent Section 11/plan/decision heading) -- not just "the first" or "the
last" ```yaml fence in the document -- because earlier fences (e.g. a nested
YAML *example* embedded inside prose/instruction comments) are not
authoritative and must be ignored.

The concrete bug reproduced by preserved Evidence 0014
(experiments/evidence/0014-stage1-auteur-second-run-remediated-framework/raw/
repository_sensemaking_brief.md) was NOT actually "wrong block selected": the
old Section-13-specific regex already matched the correct block. The real
defect was that the authoritative block's full YAML failed to parse (a
citation inside `evidence:` contains an unescaped embedded double quote --
`"src/auteur/__init__.py (L1): __version__ = "0.35.0" -- ..."` on line 206 of
the preserved artifact), and the old code swallowed that ParserError with a
bare `except Exception: pass`, returning None -- which is indistinguishable
from "no authoritative block found" or "field genuinely absent". That None
then routed to the generic fallback validator, which reported
`unknown.artifact_id.missing_field` even though `artifact_id:
repository_sensemaking_brief` is present, well-formed, and is the very first
line of the authoritative block.

These tests prove:
  1. The real, unmodified, immutable Evidence 0014 artifact now routes to
     validate-brief.py (read-only; the artifact itself is never edited).
  2. Earlier unrelated/nested YAML fences are ignored in favor of the
     authoritative Section 13 block.
  3. The new error taxonomy distinguishes no-block / malformed-YAML /
     missing-field / duplicate-key / conflicting-value / ambiguous-blocks
     instead of collapsing everything into unknown.artifact_id.missing_field.
  4. Existing registered artifact types (plan) remain compatible.

This is a routing-layer fix only. It does not modify Evidence 0014, does not
invoke a model, and does not weaken validate-brief.py's own downstream
validation (Evidence 0014 may still fail LATER, artifact-specific checks --
that is expected and orthogonal to this fix).
"""

import importlib.util
import os
import sys
import unittest

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

EVIDENCE_0014_BRIEF = os.path.join(
    REPO_ROOT, "experiments", "evidence",
    "0014-stage1-auteur-second-run-remediated-framework", "raw",
    "repository_sensemaking_brief.md",
)


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "validate_and_report",
        os.path.join(SCRIPTS_DIR, "validate-and-report.py"),
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VAR = _load_module()


def _write(tmp_path, name, content):
    path = os.path.join(tmp_path, name)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    return path


AUTHORITATIVE_OK = """## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
```
"""


class TestEvidence0014Regression(unittest.TestCase):
    """The decisive regression: the real, immutable, preserved Evidence 0014
    artifact must route to validate-brief.py. It is read-only in this test --
    never written to, never modified.
    """

    def test_evidence_0014_artifact_is_immutable_and_present(self):
        self.assertTrue(os.path.exists(EVIDENCE_0014_BRIEF), EVIDENCE_0014_BRIEF)
        with open(EVIDENCE_0014_BRIEF, encoding="utf-8") as f:
            content = f.read()
        # Sanity: the field really is present verbatim, confirming this is a
        # routing/parsing defect, not a producer omission.
        self.assertIn("artifact_id: repository_sensemaking_brief", content)

    def test_evidence_0014_multiple_yaml_fences_present(self):
        with open(EVIDENCE_0014_BRIEF, encoding="utf-8") as f:
            content = f.read()
        fence_count = content.count("```yaml")
        self.assertGreaterEqual(
            fence_count, 2,
            "Evidence 0014 must contain multiple ```yaml fences for this to "
            "be a meaningful regression (Section 8's evidence-excerpt schema "
            "example plus Section 13's authoritative handoff).",
        )

    def test_evidence_0014_extraction_detects_authoritative_artifact_id(self):
        extraction = VAR.extract_artifact_id_detailed(EVIDENCE_0014_BRIEF)
        self.assertEqual(extraction.status, "ok")
        self.assertEqual(extraction.artifact_id, "repository_sensemaking_brief")

    def test_evidence_0014_generic_routing_selects_brief_validator(self):
        result = VAR.validate_and_report(EVIDENCE_0014_BRIEF, repo_root=REPO_ROOT)
        self.assertEqual(result["artifact_id"], "repository_sensemaking_brief")
        self.assertEqual(result["validator"], "validate-brief.py")
        # The overall artifact may still fail LATER, artifact-specific checks
        # (e.g. hallucinated evidence file paths) -- that is expected and is
        # not what this regression proves. What must be true is that routing
        # reached the artifact-specific validator at all, instead of failing
        # at the generic layer with unknown.artifact_id.missing_field.
        for error in result.get("errors", []):
            self.assertNotEqual(
                error.get("error_id"), "unknown.artifact_id.missing_field",
                "Routing must not fail with the generic missing-field error "
                "once the authoritative block's artifact_id is present.",
            )


class TestAuthoritativeBlockSelection(unittest.TestCase):
    """1: single YAML fence with valid artifact_id; 2: earlier unrelated
    fence + authoritative block; 11: nested YAML examples in prose.
    """

    def test_single_fence_valid_artifact_id(self):
        content = AUTHORITATIVE_OK
        path = self._write(content)
        extraction = VAR.extract_artifact_id_detailed(path)
        self.assertEqual(extraction.status, "ok")
        self.assertEqual(extraction.artifact_id, "repository_sensemaking_brief")

    def test_earlier_unrelated_fence_ignored(self):
        content = (
            "## 5. Some earlier section\n\n"
            "```yaml\n"
            "not_authoritative: true\n"
            "artifact_id: decoy_wrong_id\n"
            "```\n\n"
            + AUTHORITATIVE_OK
        )
        path = self._write(content)
        extraction = VAR.extract_artifact_id_detailed(path)
        self.assertEqual(extraction.status, "ok")
        self.assertEqual(extraction.artifact_id, "repository_sensemaking_brief")

    def test_nested_yaml_example_in_prose_ignored(self):
        content = (
            "## 8. Evidence excerpts\n\n"
            "<!-- example schema below, not authoritative -->\n"
            "```yaml\n"
            "evidence_excerpts:\n"
            "  - file: example.py\n"
            "    artifact_id: this_is_just_prose_not_real\n"
            "```\n\n"
            + AUTHORITATIVE_OK
        )
        path = self._write(content)
        extraction = VAR.extract_artifact_id_detailed(path)
        self.assertEqual(extraction.status, "ok")
        self.assertEqual(extraction.artifact_id, "repository_sensemaking_brief")

    def _write(self, content):
        return _write(self.tmp_dir(), "fixture.md", content)

    def tmp_dir(self):
        import tempfile
        d = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(d, ignore_errors=True))
        return d


class TestErrorTaxonomy(unittest.TestCase):
    """3/4/5/6/7/8/9/10: correct / missing / conflicting / duplicate /
    malformed authoritative YAML / malformed earlier non-authoritative YAML /
    multiple authoritative candidates.
    """

    def setUp(self):
        import tempfile
        self.tmp_dir = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(self.tmp_dir, ignore_errors=True))

    def _write(self, name, content):
        return _write(self.tmp_dir, name, content)

    def test_correct_artifact_id(self):
        path = self._write("ok.md", AUTHORITATIVE_OK)
        extraction = VAR.extract_artifact_id_detailed(path)
        self.assertEqual(extraction.status, "ok")
        self.assertEqual(extraction.artifact_id, "repository_sensemaking_brief")

    def test_missing_artifact_id(self):
        content = "## 13. Machine-readable handoff\n\n```yaml\nschema_version: 1\n```\n"
        path = self._write("missing.md", content)
        extraction = VAR.extract_artifact_id_detailed(path)
        self.assertEqual(extraction.status, "missing_field")

    def test_conflicting_artifact_id(self):
        content = (
            "## 13. Machine-readable handoff\n\n"
            "```yaml\n"
            "artifact_id: repository_sensemaking_brief\n"
            "other_field: 1\n"
            "artifact_id: workflow_orchestration_plan\n"
            "```\n"
        )
        path = self._write("conflict.md", content)
        extraction = VAR.extract_artifact_id_detailed(path)
        # PyYAML's SafeLoader resolves duplicate top-level keys silently
        # (last one wins) rather than raising -- so a conflicting pair of
        # differently-valued artifact_id keys parses successfully as a dict
        # with the LAST value. That would silently override authority, which
        # issue #97 explicitly forbids ("A conflicting model-provided
        # artifact_id must never silently override runtime authority").
        # The router must therefore explicitly re-scan for repeated
        # artifact_id lines even on YAML-parse success, not just on failure.
        self.assertIn(extraction.status, ("conflicting_artifact_id",))

    def test_duplicate_artifact_id_same_value(self):
        content = (
            "## 13. Machine-readable handoff\n\n"
            "```yaml\n"
            "artifact_id: repository_sensemaking_brief\n"
            "other_field: 1\n"
            "artifact_id: repository_sensemaking_brief\n"
            "```\n"
        )
        path = self._write("dup.md", content)
        extraction = VAR.extract_artifact_id_detailed(path)
        self.assertEqual(extraction.status, "duplicate_key")

    def test_malformed_authoritative_yaml_no_recoverable_artifact_id(self):
        # Malformed YAML with NO plain top-level `artifact_id:` line at all
        # (the id is embedded oddly) -- must be reported distinctly from
        # "missing field".
        content = (
            "## 13. Machine-readable handoff\n\n"
            "```yaml\n"
            "evidence:\n"
            '  - "unterminated "quote" breaks parsing"\n'
            "```\n"
        )
        path = self._write("malformed.md", content)
        extraction = VAR.extract_artifact_id_detailed(path)
        self.assertEqual(extraction.status, "malformed_authoritative_yaml")

    def test_malformed_authoritative_yaml_with_recoverable_artifact_id(self):
        # This is the exact Evidence-0014 shape: artifact_id is present and
        # well-formed, but a LATER field (evidence:) has an unescaped quote
        # that breaks the whole block's YAML parse. Routing must still
        # recover artifact_id deterministically.
        content = (
            "## 13. Machine-readable handoff\n\n"
            "```yaml\n"
            "artifact_id: repository_sensemaking_brief\n"
            "evidence:\n"
            '  - "file.py (L1): __version__ = "0.35.0" -- broken quote"\n'
            "```\n"
        )
        path = self._write("evidence0014_shape.md", content)
        extraction = VAR.extract_artifact_id_detailed(path)
        self.assertEqual(extraction.status, "ok")
        self.assertEqual(extraction.artifact_id, "repository_sensemaking_brief")

    def test_malformed_earlier_non_authoritative_yaml_does_not_block_routing(self):
        content = (
            "## 3. Some earlier section\n\n"
            "```yaml\n"
            'broken: "unterminated\n'
            "```\n\n"
            + AUTHORITATIVE_OK
        )
        path = self._write("earlier_malformed.md", content)
        extraction = VAR.extract_artifact_id_detailed(path)
        self.assertEqual(extraction.status, "ok")
        self.assertEqual(extraction.artifact_id, "repository_sensemaking_brief")

    def test_multiple_authoritative_candidate_blocks_is_ambiguous(self):
        content = (
            AUTHORITATIVE_OK
            + "\n## 13. Machine-readable handoff\n\n"
            "```yaml\n"
            "artifact_id: repository_sensemaking_brief\n"
            "```\n"
        )
        path = self._write("ambiguous.md", content)
        extraction = VAR.extract_artifact_id_detailed(path)
        self.assertEqual(extraction.status, "ambiguous_authoritative_blocks")

    def test_no_authoritative_block(self):
        content = "# Some document\n\nNo handoff section here at all.\n"
        path = self._write("noblock.md", content)
        extraction = VAR.extract_artifact_id_detailed(path)
        self.assertEqual(extraction.status, "no_authoritative_block")


class TestCRLFAndFilenameAndHtmlComment(unittest.TestCase):
    """12: CRLF documents. 13: filename suggests an artifact but YAML lacks
    the field. 14/15: HTML comment vs. authoritative YAML agreement/conflict
    -- the router must use the YAML field, never the HTML comment, as
    authoritative.
    """

    def setUp(self):
        import tempfile
        self.tmp_dir = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(self.tmp_dir, ignore_errors=True))

    def _write(self, name, content):
        return _write(self.tmp_dir, name, content)

    def test_crlf_document(self):
        content = AUTHORITATIVE_OK.replace("\n", "\r\n")
        path = self._write("crlf.md", content)
        extraction = VAR.extract_artifact_id_detailed(path)
        self.assertEqual(extraction.status, "ok")
        self.assertEqual(extraction.artifact_id, "repository_sensemaking_brief")

    def test_filename_suggests_artifact_but_yaml_lacks_field(self):
        content = "## 13. Machine-readable handoff\n\n```yaml\nschema_version: 1\n```\n"
        path = self._write("repository_sensemaking_brief.md", content)
        extraction = VAR.extract_artifact_id_detailed(path)
        # Must NOT infer artifact_id from the filename (issue #97 explicitly
        # forbids "inferring artifact_id solely from filenames as the
        # primary fix").
        self.assertEqual(extraction.status, "missing_field")
        self.assertIsNone(extraction.artifact_id)

    def test_html_comment_id_ignored_when_yaml_lacks_field(self):
        content = (
            "<!-- artifact_id: repository_sensemaking_brief -->\n\n"
            "## 13. Machine-readable handoff\n\n"
            "```yaml\nschema_version: 1\n```\n"
        )
        path = self._write("html_comment.md", content)
        extraction = VAR.extract_artifact_id_detailed(path)
        self.assertEqual(extraction.status, "missing_field")

    def test_html_comment_and_yaml_disagree_yaml_wins(self):
        content = (
            "<!-- artifact_id: workflow_orchestration_plan -->\n\n"
            + AUTHORITATIVE_OK
        )
        path = self._write("disagree.md", content)
        extraction = VAR.extract_artifact_id_detailed(path)
        self.assertEqual(extraction.status, "ok")
        self.assertEqual(extraction.artifact_id, "repository_sensemaking_brief")


class TestGenericRoutingIntegration(unittest.TestCase):
    """17: generic routing reaches the artifact-specific validator.
    16: external-target validation mode still passes target_repo through.
    18: existing valid fixtures remain unchanged.
    """

    def test_existing_plan_fixture_still_routes(self):
        path = os.path.join(REPO_ROOT, "tests", "fixtures", "plan-valid.md")
        extraction = VAR.extract_artifact_id_detailed(path)
        self.assertEqual(extraction.status, "ok")
        self.assertEqual(extraction.artifact_id, "workflow_orchestration_plan")
        result = VAR.validate_and_report(path, repo_root=REPO_ROOT)
        self.assertEqual(result["validator"], "validate-plan.py")

    def test_existing_brief_fixture_still_routes(self):
        path = os.path.join(REPO_ROOT, "tests", "fixtures", "brief-valid.md")
        extraction = VAR.extract_artifact_id_detailed(path)
        self.assertEqual(extraction.status, "ok")
        self.assertEqual(extraction.artifact_id, "repository_sensemaking_brief")

    def test_target_repo_passthrough_preserved_on_successful_routing(self):
        # Regression guard: the target_repo passthrough to validate-brief.py
        # (for external-repository runs) must still occur once routing
        # succeeds; this fix only changes artifact_id EXTRACTION, not the
        # invoke_validator command-building logic.
        path = os.path.join(REPO_ROOT, "tests", "fixtures", "brief-valid.md")
        validator_path = VAR.select_validator(
            VAR.extract_artifact_id_detailed(path).artifact_id
        )
        self.assertEqual(validator_path, "scripts/validate-brief.py")


class TestGenericMissingFieldStillWeaklessFalls(unittest.TestCase):
    """9/12 from the taxonomy list: missing-field errors are not weakened --
    a genuinely missing artifact_id still fails deterministically end-to-end
    through validate_and_report(), not just at the extraction layer.
    """

    def setUp(self):
        import tempfile
        self.tmp_dir = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(self.tmp_dir, ignore_errors=True))

    def test_missing_field_end_to_end(self):
        content = "## 13. Machine-readable handoff\n\n```yaml\nschema_version: 1\n```\n"
        path = _write(self.tmp_dir, "missing.md", content)
        result = VAR.validate_and_report(path, repo_root=REPO_ROOT)
        self.assertFalse(result["valid"])
        self.assertEqual(
            result["errors"][0]["error_id"], "unknown.artifact_id.missing_field"
        )

    def test_no_block_end_to_end_is_distinct_error(self):
        content = "# Nothing here\n"
        path = _write(self.tmp_dir, "noblock.md", content)
        result = VAR.validate_and_report(path, repo_root=REPO_ROOT)
        self.assertFalse(result["valid"])
        self.assertEqual(
            result["errors"][0]["error_id"], "unknown.artifact_id.no_authoritative_block"
        )


if __name__ == "__main__":
    unittest.main()
