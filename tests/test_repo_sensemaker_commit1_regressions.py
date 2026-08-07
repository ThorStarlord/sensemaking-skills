"""Commit 1 regressions: deterministic exploration + evidence authority + GAP-1/GAP-3.

Covers:
- GAP-1: standalone briefs must contain validator-valid verbatim quotes
  (placeholder -> blocking EVIDENCE_QUOTE_NOT_FOUND); skill/template must
  document both invocation modes.
- GAP-3: citation grammar supports js/jsx/ts/tsx/json/html/css/go/rs/java/rb/sh
  (validator FILE_CITATION_RE), without accepting arbitrary extensions.
- Skill content: exploration protocol (Pass A-E), evidence authority
  (OBSERVED/DERIVED/INFERRED/UNKNOWN), low-value content rules.
"""

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import importlib.util

spec = importlib.util.spec_from_file_location(
    "validate_brief", str(REPO_ROOT / "scripts" / "validate-brief.py")
)
validate_brief_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_brief_module)
validate_brief = validate_brief_module.validate_brief

SKILL = REPO_ROOT / "skills" / "repo-sensemaker" / "SKILL.md"
TEMPLATE = REPO_ROOT / "skills" / "repo-sensemaker" / "references" / "repo-analysis-template.md"


def make_target(tmp: Path, files: dict[str, str]) -> None:
    for rel, content in files.items():
        p = tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")


def make_brief(quote: str, cited_file: str = "README.md", lines: str = "L1-L2") -> str:
    """Minimal standalone brief modeled on tests/fixtures/brief-valid.md."""
    return f"""# Repository Sensemaking Brief: regression fixture

## Evidence

- {cited_file} ({lines}): fixture evidence line
- Logic trace: the cited fixture evidence supports the boundary conclusion.

## Evidence excerpts

```yaml
evidence_excerpts:
  - file: "{cited_file}"
    lines: "{lines}"
    quote: "{quote}"
    supports_claim: "fixture claim"
```

## Recommended Workflow

Logic trace: the evidence shows the fixture boundary, so the fog is product
scope rather than UI, docs, or architecture; this points to product_fog.

Based on the evidence, the primary fog type is **product_fog**.

The recommended workflow is: product-implementation-workflow

---

## Machine-readable Handoff

```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: product_fog
evidence:
  - "{cited_file} ({lines}): fixture evidence"
recommended_workflow_id: product-implementation-workflow
weakness_type: Zero Validation
created_at: "2026-08-07T00:00:00Z"
immutable: true
```
"""


def error_ids(errors):
    ids = set()
    for e in errors:
        ids.add(e.get("error_id", ""))
        msg = e.get("message", "")
        if ":" in msg:
            ids.add(msg.split(":", 1)[0])
    return ids


class TestGap1QuoteHandling(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        make_target(self.tmp, {"README.md": "line one\nline two\n"})

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_placeholder_quote_fails_standalone(self):
        """GAP-1 regression: a placeholder quote must be a blocking
        EVIDENCE_QUOTE_NOT_FOUND in standalone (no-runtime) validation."""
        brief = self.tmp / "brief.md"
        brief.write_text(make_brief(quote="see file/lines"), encoding="utf-8")
        errors = validate_brief(str(brief), str(REPO_ROOT), target_repo=str(self.tmp))
        ids = error_ids(errors)
        self.assertTrue(
            any("EVIDENCE_QUOTE_NOT_FOUND" in e for e in ids),
            f"expected EVIDENCE_QUOTE_NOT_FOUND, got {ids}",
        )

    def test_verbatim_quote_passes_standalone(self):
        """A verbatim quote must validate cleanly in standalone mode."""
        brief = self.tmp / "brief.md"
        brief.write_text(make_brief(quote="line one"), encoding="utf-8")
        errors = validate_brief(str(brief), str(REPO_ROOT), target_repo=str(self.tmp))
        self.assertEqual(errors, [], f"expected no errors, got {errors}")

    def test_skill_documents_both_invocation_modes(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("Runtime invocation", text)
        self.assertIn("Standalone invocation", text)
        self.assertIn("EVIDENCE_QUOTE_NOT_FOUND", text)

    def test_template_quote_guidance_is_mode_conditional(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("Runtime invocation", text)
        self.assertIn("Standalone invocation", text)
        self.assertIn("verbatim", text)


class TestGap3CitationExtensions(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_js_citation_accepted(self):
        """GAP-3 regression: .js citations must satisfy the evidence-citation
        check (previously rejected by FILE_CITATION_RE)."""
        make_target(self.tmp, {"app.js": "export const x = 1;\n"})
        brief = self.tmp / "brief.md"
        brief.write_text(make_brief(quote="export const x = 1;", cited_file="app.js", lines="L1"), encoding="utf-8")
        errors = validate_brief(str(brief), str(REPO_ROOT), target_repo=str(self.tmp))
        ids = error_ids(errors)
        self.assertNotIn("repository_sensemaking_brief.evidence.no_file_citations", ids)
        self.assertEqual(errors, [], f"expected no errors, got {errors}")

    def test_supported_extensions_present_in_validator(self):
        pattern = validate_brief_module.FILE_CITATION_RE.pattern
        for ext in ("js", "jsx", "ts", "tsx", "json", "html", "css", "go", "rs", "java", "rb", "sh"):
            self.assertIn(ext, pattern, f"FILE_CITATION_RE missing {ext}")

    def test_unknown_extension_still_rejected(self):
        """The citation grammar must stay restrictive: .xyz must not cite."""
        pattern = validate_brief_module.FILE_CITATION_RE.pattern
        self.assertNotIn("xyz", pattern)


class TestSkillDiscoveryContent(unittest.TestCase):
    def test_exploration_protocol_passes_a_to_e(self):
        text = SKILL.read_text(encoding="utf-8")
        for marker in ("Pass A", "Pass B", "Pass C", "Pass D", "Pass E"):
            self.assertIn(marker, text)
        self.assertIn("Contradiction search", text)

    def test_low_value_content_rules_present(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("Low-value content", text)
        self.assertIn("vendor", text)

    def test_evidence_authority_classes_present(self):
        text = SKILL.read_text(encoding="utf-8")
        for cls in ("OBSERVED", "DERIVED", "INFERRED", "UNKNOWN"):
            self.assertIn(cls, text)
        self.assertIn("never invent a path", text)


if __name__ == "__main__":
    unittest.main()
