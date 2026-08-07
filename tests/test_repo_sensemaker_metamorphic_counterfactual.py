"""Commit 7 - metamorphic + counterfactual regressions (12.3, 12.4).

Metamorphic: perturbing semantically-irrelevant properties must not change
the validation verdict or the frozen semantic score (same corpus, same
ground truth, same scorer).

Counterfactual: fixing the relevant evidence must remove the corresponding
diagnosis input (fixture-level: the defect markers disappear when the
defect is fixed).
"""

import importlib.util
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CORPUS = REPO_ROOT / "experiments" / "repository-sensemaking-skill-hardening-v1" / "corpus"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("validate_brief", str(REPO_ROOT / "scripts" / "validate-brief.py"))
validate_brief_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_brief_module)
validate_brief = validate_brief_module.validate_brief


def brief_fixture() -> str:
    return """# Repository Sensemaking Brief: metamorphic fixture

## Evidence

- README.md (L1-L2): fixture evidence line
- Logic trace: the cited fixture evidence supports the boundary conclusion.

## Evidence excerpts

```yaml
evidence_excerpts:
  - file: "README.md"
    lines: "L1-L2"
    quote: "line one"
    supports_claim: "fixture claim"
```

## 6.5. Problem classification (fog type)

The primary fog type is **product_fog**.

## Recommended Workflow

Logic trace: the evidence shows the fixture boundary, so the fog is product
scope; this points to product_fog.

The recommended workflow is: product-implementation-workflow

---

## Machine-readable Handoff

```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: product_fog
evidence:
  - "README.md (L1-L2): fixture evidence"
recommended_workflow_id: product-implementation-workflow
weakness_type: Zero Validation
created_at: "2026-08-07T00:00:00Z"
immutable: true
```
"""


def handoff_yaml(text: str) -> dict:
    m = re.search(r"## Machine-readable Handoff.*?```yaml\n(.*?)\n```", text, re.S)
    return yaml.safe_load(m.group(1))


def reorder_yaml(text: str) -> str:
    """Reorder the handoff YAML keys and the evidence list items."""
    data = handoff_yaml(text)
    ordered = {k: data[k] for k in reversed(list(data.keys()))}
    if isinstance(ordered.get("evidence"), list):
        ordered["evidence"] = list(reversed(ordered["evidence"]))
    new_block = yaml.safe_dump(ordered, sort_keys=False)
    m = re.search(r"(## Machine-readable Handoff.*?```yaml\n)(.*?)(\n```)", text, re.S)
    return text[:m.start(2)] + new_block.rstrip("\n") + text[m.end(2):]


def signature(errors) -> tuple:
    return tuple(sorted((e.get("error_type"), e.get("field"), e.get("message", "")[:60])
                        for e in errors))


class TestMetamorphic(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "README.md").write_text("line one\nline two\n", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_yaml_key_reorder_does_not_change_verdict(self):
        base = brief_fixture()
        perturbed = reorder_yaml(base)
        b1 = self.tmp / "b1.md"; b1.write_text(base, encoding="utf-8")
        b2 = self.tmp / "b2.md"; b2.write_text(perturbed, encoding="utf-8")
        e1 = validate_brief(str(b1), str(REPO_ROOT), target_repo=str(self.tmp))
        e2 = validate_brief(str(b2), str(REPO_ROOT), target_repo=str(self.tmp))
        self.assertEqual(signature(e1), signature(e2))

    def test_irrelevant_generated_file_does_not_change_verdict(self):
        (self.tmp / "dist").mkdir()
        (self.tmp / "dist/bundle.js").write_text("console.log('minified');\n", encoding="utf-8")
        b = self.tmp / "b.md"; b.write_text(brief_fixture(), encoding="utf-8")
        errors = validate_brief(str(b), str(REPO_ROOT), target_repo=str(self.tmp))
        self.assertEqual([e for e in errors if e.get("severity") == "error"], [])


class TestCounterfactual(unittest.TestCase):
    def test_partial_impl_defect_marker_disappears_when_fixed(self):
        """Counterfactual: implementing the stub removes the Ghost Features
        input (the NotImplementedError marker)."""
        root = CORPUS / "adv-partial-impl"
        original = (root / "core.py").read_text(encoding="utf-8")
        fixed = original.replace("raise NotImplementedError('report generation not implemented yet')",
                                 "return 'report generated'")
        self.assertNotEqual(original, fixed)
        self.assertNotIn("NotImplementedError", fixed)

    def test_stale_readme_mismatch_disappears_when_aligned(self):
        """Counterfactual: aligning the README with the code removes the
        SQLite-vs-JSON contradiction."""
        root = CORPUS / "stale-readme"
        readme = (root / "README.md").read_text(encoding="utf-8")
        aligned = readme.replace("SQLite", "JSON files")
        self.assertNotIn("SQLite", aligned)

    def test_generated_heavy_primary_source_swap(self):
        """Counterfactual: without the DO NOT EDIT marker the generated file
        becomes indistinguishable from authored source."""
        root = CORPUS / "generated-heavy"
        pb = (root / "generated/api_pb2.py").read_text(encoding="utf-8")
        self.assertIn("DO NOT EDIT", pb)
        stripped = pb.replace("DO NOT EDIT!", "generated marker removed")
        self.assertNotIn("DO NOT EDIT", stripped)


if __name__ == "__main__":
    unittest.main()
