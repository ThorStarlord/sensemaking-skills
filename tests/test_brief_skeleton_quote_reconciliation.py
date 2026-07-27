"""Tests for the issue #89 quote-reconciliation wiring in
scripts/brief_skeleton.py: reconcile() must overwrite
evidence_excerpts[].quote with deterministically-extracted text (never the
model's own transcription), scoped to the correct root, and must never
silently keep an unverified quote when extraction fails.

No real model/network call. No repository outside a temp dir /
tests/fixtures is touched.
"""

import importlib.util
import os
import sys
import tempfile
import unittest

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, SCRIPTS_DIR)

import brief_skeleton as bs  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "validate_brief", os.path.join(SCRIPTS_DIR, "validate-brief.py")
)
validate_brief_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_brief_module)
validate_brief = validate_brief_module.validate_brief

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))


def _write_tmp(content: str) -> str:
    fd, path = tempfile.mkstemp(suffix=".md")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def _model_output(evidence_yaml_block: str) -> str:
    return f"""
<!-- MODEL_SECTION:repository_goal:BEGIN -->
Goal prose.
<!-- MODEL_SECTION:repository_goal:END -->

<!-- MODEL_SECTION:weakest_boundary_prose:BEGIN -->
Weakness prose.
<!-- MODEL_SECTION:weakest_boundary_prose:END -->

<!-- MODEL_SECTION:evidence_prose:BEGIN -->
Logic trace: connects evidence to conclusion.
<!-- MODEL_SECTION:evidence_prose:END -->

<!-- MODEL_SECTION:evidence_excerpts:BEGIN -->
{evidence_yaml_block}
<!-- MODEL_SECTION:evidence_excerpts:END -->

```yaml
primary_fog_type: architecture_fog
recommended_workflow_id: architecture-implementation-workflow
escalation_recommended: false
weakness_type: Zero Validation
evidence:
  - "target_file.py (lines L1): weak boundary"
```
"""


class TmpTargetRepoMixin:
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.target_root = self._tmpdir.name

    def tearDown(self):
        self._tmpdir.cleanup()

    def write_target(self, relpath: str, content: str) -> None:
        full = os.path.join(self.target_root, relpath)
        os.makedirs(os.path.dirname(full) or self.target_root, exist_ok=True)
        with open(full, "w", encoding="utf-8", newline="") as f:
            f.write(content)


class TestDeterministicQuoteOverwrite(TmpTargetRepoMixin, unittest.TestCase):
    def test_model_quote_is_discarded_and_replaced(self):
        self.write_target("target_file.py", '"""Decision workspace service — real state."""\n')
        model_output = _model_output(
            "```yaml\n"
            "evidence_excerpts:\n"
            "  - file: target_file.py\n"
            "    lines: L1\n"
            '    quote: "Decision workspace service -- real state (WRONG, model paraphrased)"\n'
            '    supports_claim: "supports diagnosis"\n'
            "```"
        )
        out = bs.reconcile(model_output, target_root=self.target_root, framework_root=REPO_ROOT)
        self.assertNotIn("WRONG, model paraphrased", out)
        # The extracted quote is YAML double-quoted, so literal `"` chars in
        # the source text (the docstring's triple-quotes) are backslash-
        # escaped in the serialized artifact -- check the unescaped content
        # instead of the raw source bytes.
        self.assertIn("Decision workspace service — real state", out)

    def test_em_dash_survives_full_reconcile_and_validator(self):
        self.write_target("target_file.py", '"""Decision workspace service — real state."""\n')
        model_output = _model_output(
            "```yaml\n"
            "evidence_excerpts:\n"
            "  - file: target_file.py\n"
            "    lines: L1\n"
            '    quote: "placeholder"\n'
            '    supports_claim: "supports diagnosis"\n'
            "```"
        )
        out = bs.reconcile(model_output, target_root=self.target_root, framework_root=REPO_ROOT)
        path = _write_tmp(out)
        try:
            errors = validate_brief(path, REPO_ROOT, target_repo=self.target_root)
            blocking = [e for e in errors if e.get("severity", "error") == "error"]
            self.assertEqual(blocking, [], f"expected no blocking errors, got {blocking}")
        finally:
            os.remove(path)

    def test_indentation_survives_full_reconcile_and_validator(self):
        self.write_target("target_file.py", "def f():\n    x = 1\n    return x\n")
        model_output = _model_output(
            "```yaml\n"
            "evidence_excerpts:\n"
            "  - file: target_file.py\n"
            "    lines: L2\n"
            '    quote: "x = 1"\n'
            '    supports_claim: "supports diagnosis"\n'
            "```"
        )
        out = bs.reconcile(model_output, target_root=self.target_root, framework_root=REPO_ROOT)
        self.assertIn("    x = 1", out)
        path = _write_tmp(out)
        try:
            errors = validate_brief(path, REPO_ROOT, target_repo=self.target_root)
            blocking = [e for e in errors if e.get("severity", "error") == "error"]
            self.assertEqual(blocking, [], f"expected no blocking errors, got {blocking}")
        finally:
            os.remove(path)

    def test_extraction_failure_produces_sentinel_that_fails_validator(self):
        # File does not exist in target_root -- extraction cannot complete.
        model_output = _model_output(
            "```yaml\n"
            "evidence_excerpts:\n"
            "  - file: does_not_exist.py\n"
            "    lines: L1\n"
            '    quote: "placeholder"\n'
            '    supports_claim: "supports diagnosis"\n'
            "```"
        )
        out = bs.reconcile(model_output, target_root=self.target_root, framework_root=REPO_ROOT)
        self.assertIn("QUOTE_EXTRACTION_FAILED", out)
        # HALLUCINATED_FILE already covers the missing-file case in
        # validate-brief.py (the file itself doesn't exist), which is the
        # correct, pre-existing signal -- the sentinel additionally
        # guarantees the quote itself could never accidentally validate.
        path = _write_tmp(out)
        try:
            errors = validate_brief(path, REPO_ROOT, target_repo=self.target_root)
            blocking_codes = [e["message"] for e in errors if e.get("severity", "error") == "error"]
            self.assertTrue(
                any("HALLUCINATED_FILE" in m for m in blocking_codes),
                f"expected a blocking error, got {blocking_codes}",
            )
        finally:
            os.remove(path)

    def test_target_root_vs_framework_root_distinguished(self):
        # A file that exists in the framework root but NOT in target_root
        # must not be silently read from the framework root.
        self.write_target("only_in_target.py", "irrelevant\n")
        model_output = _model_output(
            "```yaml\n"
            "evidence_excerpts:\n"
            "  - file: scripts/validate-brief.py\n"  # exists in framework root, not target_root
            "    lines: L1\n"
            '    quote: "placeholder"\n'
            '    supports_claim: "supports diagnosis"\n'
            "```"
        )
        out = bs.reconcile(model_output, target_root=self.target_root, framework_root=REPO_ROOT)
        self.assertIn("QUOTE_EXTRACTION_FAILED", out)

    def test_no_target_file_written_during_reconcile(self):
        self.write_target("target_file.py", "a\nb\n")
        before = os.listdir(self.target_root)
        model_output = _model_output(
            "```yaml\n"
            "evidence_excerpts:\n"
            "  - file: target_file.py\n"
            "    lines: L1\n"
            '    quote: "placeholder"\n'
            '    supports_claim: "supports diagnosis"\n'
            "```"
        )
        bs.reconcile(model_output, target_root=self.target_root, framework_root=REPO_ROOT)
        after = os.listdir(self.target_root)
        self.assertEqual(before, after)

    def test_validator_rejects_hand_edited_quote(self):
        """Regression: even after runtime overwrite, if someone were to
        hand-edit the reconciled artifact's quote afterward, the validator
        (independently re-deriving/checking grounding) must reject it. This
        proves the validator is still the authority, not just the runtime."""
        self.write_target("target_file.py", '"""Decision workspace service — real state."""\n')
        model_output = _model_output(
            "```yaml\n"
            "evidence_excerpts:\n"
            "  - file: target_file.py\n"
            "    lines: L1\n"
            '    quote: "placeholder"\n'
            '    supports_claim: "supports diagnosis"\n'
            "```"
        )
        out = bs.reconcile(model_output, target_root=self.target_root, framework_root=REPO_ROOT)
        tampered = out.replace(
            "Decision workspace service — real state",
            "this text was never in the source file at all",
        )
        path = _write_tmp(tampered)
        try:
            errors = validate_brief(path, REPO_ROOT, target_repo=self.target_root)
            blocking_codes = [e["message"] for e in errors if e.get("severity", "error") == "error"]
            self.assertTrue(any("EVIDENCE_QUOTE_NOT_FOUND" in m for m in blocking_codes))
        finally:
            os.remove(path)


class TestNonEvidenceProseUnaffected(TmpTargetRepoMixin, unittest.TestCase):
    """Regression: ordinary non-evidence prose sections must not be
    rewritten by the quote-reconciliation logic -- it only touches the
    evidence_excerpts block."""

    def test_prose_sections_untouched(self):
        self.write_target("target_file.py", "a\nb\n")
        model_output = _model_output(
            "```yaml\n"
            "evidence_excerpts:\n"
            "  - file: target_file.py\n"
            "    lines: L1\n"
            '    quote: "placeholder"\n'
            '    supports_claim: "supports diagnosis"\n'
            "```"
        )
        out = bs.reconcile(model_output, target_root=self.target_root, framework_root=REPO_ROOT)
        self.assertIn("Goal prose.", out)
        self.assertIn("Weakness prose.", out)
        self.assertIn("Logic trace: connects evidence to conclusion.", out)


class TestDefaultRootFallback(unittest.TestCase):
    """When target_root is not supplied, extraction falls back to
    framework_root, mirroring validate-brief.py's citation_root fallback --
    single-repo/internal-proof runs are unaffected."""

    def test_falls_back_to_framework_root(self):
        model_output = _model_output(
            "```yaml\n"
            "evidence_excerpts:\n"
            "  - file: skills/repo-sensemaker/references/weakness-types.md\n"
            "    lines: L5\n"
            '    quote: "placeholder"\n'
            '    supports_claim: "supports diagnosis"\n'
            "```"
        )
        out = bs.reconcile(model_output, framework_root=REPO_ROOT)
        self.assertNotIn("QUOTE_EXTRACTION_FAILED", out)
        self.assertIn("Vocabulary Drift", out)


if __name__ == "__main__":
    unittest.main()
