"""Commit 4 - fog classification regressions.

- GAP-4: producer guidance and validator agree on the fog enum
  (template no longer lists mixed/unknown; validator rejects mixed).
- GAP-8: no-user-intent semantics are canonical (user_implied_fog_type:
  unknown, diagnosis_conflict: false) in skill + template, and the
  validator accepts them.
- Ghost-feature reasoning: deterministic 3-way classifier mirrors the
  skill's decision table (stale docs -> docs_fog, product promise ->
  product_fog, architecture constraint -> architecture_fog).
- Skill content: evidence signals for all four fogs, no auto-default to
  architecture, primary vs secondary fog.
"""

import importlib.util
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL = REPO_ROOT / "skills" / "repo-sensemaker" / "SKILL.md"
TEMPLATE = REPO_ROOT / "skills" / "repo-sensemaker" / "references" / "repo-analysis-template.md"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("validate_brief", str(REPO_ROOT / "scripts" / "validate-brief.py"))
validate_brief_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_brief_module)
validate_brief = validate_brief_module.validate_brief

ALLOWED_FOG = {"product_fog", "ui_fog", "docs_fog", "architecture_fog"}


def skill_text() -> str:
    return re.sub(r"\s+", " ", SKILL.read_text(encoding="utf-8"))


def classify_ghost(docs_stale: bool, product_promise: bool, architecture_constraint: bool) -> str:
    """Deterministic mirror of the skill's ghost-feature decision table.

    product promise dominates (the defect is the promise); then
    architecture constraint; then stale docs.
    """
    if product_promise:
        return "product_fog"
    if architecture_constraint:
        return "architecture_fog"
    if docs_stale:
        return "docs_fog"
    return "no_fog"


def make_brief(primary_fog_type: str, user_implied: str = "unknown", conflict: str = "false") -> str:
    return f"""# Repository Sensemaking Brief: fog regression fixture

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

## Recommended Workflow

Logic trace: the evidence shows the fixture boundary, so the fog is product
scope; this points to product_fog.

Based on the evidence, the primary fog type is **{primary_fog_type}**.

The recommended workflow is: product-implementation-workflow

---

## Machine-readable Handoff

```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: {primary_fog_type}
user_implied_fog_type: {user_implied}
diagnosis_conflict: {conflict}
evidence:
  - "README.md (L1-L2): fixture evidence"
recommended_workflow_id: product-implementation-workflow
weakness_type: Zero Validation
created_at: "2026-08-07T00:00:00Z"
immutable: true
```
"""


class TestSkillFogContent(unittest.TestCase):
    def test_all_four_fog_signal_sets_documented(self):
        text = skill_text()
        for fog in ("product_fog", "ui_fog", "docs_fog", "architecture_fog"):
            self.assertIn(f"**{fog}**", text)
        self.assertIn("promised feature absent", text)

    def test_ghost_feature_three_way_documented(self):
        text = skill_text()
        self.assertIn("product_fog candidate", text)
        self.assertIn("docs_fog candidate", text)
        self.assertIn("architecture_fog candidate", text)
        self.assertIn("the defect is the promise, not the docs", text)

    def test_no_auto_architecture_default(self):
        text = skill_text()
        self.assertIn("Do NOT default to architecture_fog merely because classification is hard", text)

    def test_primary_secondary_fog_documented(self):
        text = skill_text()
        self.assertIn("Separate primary from secondary fog", text)

    def test_gap8_canonical_no_intent_values_in_skill(self):
        text = skill_text()
        self.assertIn("user_implied_fog_type: unknown", text)
        self.assertIn("diagnosis_conflict: false", text)

    def test_gap8_canonical_no_intent_values_in_template(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("user_implied_fog_type: unknown", text)
        self.assertIn("diagnosis_conflict: false", text)


class TestGap4EnumAgreement(unittest.TestCase):
    def test_template_no_longer_lists_mixed_or_unknown_as_valid_primary(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        line = next(l for l in text.splitlines() if "primary_fog_type:" in l and "|" in l)
        enum_part = line.split("#", 1)[0].split(":", 1)[1]
        values = {v.strip() for v in enum_part.split("|")}
        self.assertEqual(values, ALLOWED_FOG)
        self.assertNotIn("mixed", values)
        self.assertNotIn("unknown", values)

    def test_validator_rejects_mixed(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / "README.md").write_text("line one\nline two\n", encoding="utf-8")
            brief = tmp / "brief.md"
            brief.write_text(make_brief("mixed"), encoding="utf-8")
            errors = validate_brief(str(brief), str(REPO_ROOT), target_repo=str(tmp))
            types = [e.get("error_type") for e in errors]
            self.assertIn("unknown_value", types)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_validator_accepts_all_four(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / "README.md").write_text("line one\nline two\n", encoding="utf-8")
            for fog in sorted(ALLOWED_FOG):
                brief = tmp / f"brief-{fog}.md"
                brief.write_text(make_brief(fog), encoding="utf-8")
                errors = validate_brief(str(brief), str(REPO_ROOT), target_repo=str(tmp))
                msgs = " ".join(e.get("message", "") for e in errors)
                self.assertNotIn("unknown_value", msgs, f"{fog} must be accepted: {msgs}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestGap8ValidatorAcceptance(unittest.TestCase):
    def test_no_intent_values_accepted_by_validator(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / "README.md").write_text("line one\nline two\n", encoding="utf-8")
            brief = tmp / "brief.md"
            brief.write_text(make_brief("product_fog", user_implied="unknown", conflict="false"),
                             encoding="utf-8")
            errors = validate_brief(str(brief), str(REPO_ROOT), target_repo=str(tmp))
            self.assertEqual([e for e in errors if e.get("severity") == "error"], [],
                             f"no-intent brief must have no errors: {errors}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestGhostFeatureClassifier(unittest.TestCase):
    def test_stale_docs_only(self):
        self.assertEqual(classify_ghost(docs_stale=True, product_promise=False, architecture_constraint=False),
                         "docs_fog")

    def test_product_promise_dominates(self):
        self.assertEqual(classify_ghost(docs_stale=True, product_promise=True, architecture_constraint=False),
                         "product_fog")

    def test_architecture_constraint(self):
        self.assertEqual(classify_ghost(docs_stale=False, product_promise=False, architecture_constraint=True),
                         "architecture_fog")

    def test_none(self):
        self.assertEqual(classify_ghost(False, False, False), "no_fog")


if __name__ == "__main__":
    unittest.main()
