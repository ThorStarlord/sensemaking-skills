"""Commit 6 - artifact contract + semantic validator regressions.

- GAP-2: vocabulary map exists and canonicalizes escalation_recommended
  (not escalation_required); contract required fields are present in the
  template's Section-13 block (producer/consumer agreement).
- GAP-9: skill documents both invocation pipelines (runtime skeleton ->
  reconcile -> validate-and-record; standalone complete artifact ->
  validate-brief.py).
- New semantic checks: FOG_PROSE_MISMATCH and WORKFLOW_PROSE_MISMATCH fire
  as warnings (never invalidate) when handoff and prose disagree; silence
  when they agree.
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
SKILL = REPO_ROOT / "skills" / "repo-sensemaker" / "SKILL.md"
TEMPLATE = REPO_ROOT / "skills" / "repo-sensemaker" / "references" / "repo-analysis-template.md"
CONTRACTS = REPO_ROOT / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"
WORK = REPO_ROOT / "experiments" / "repository-sensemaking-skill-hardening-v1"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("validate_brief", str(REPO_ROOT / "scripts" / "validate-brief.py"))
validate_brief_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_brief_module)
validate_brief = validate_brief_module.validate_brief


def skill_text() -> str:
    return re.sub(r"\s+", " ", SKILL.read_text(encoding="utf-8"))


def template_section13_fields() -> set[str]:
    text = TEMPLATE.read_text(encoding="utf-8")
    m = re.search(r"## 13\..*?```yaml\n(.*?)\n```", text, re.S)
    assert m, "template Section-13 yaml block not found"
    data = yaml.safe_load(m.group(1)) or {}
    return set(data.keys())


def make_brief(primary_fog_type: str, workflow_id: str, fog_prose: str | None = None,
               workflow_prose: str | None = None) -> str:
    fog_prose = fog_prose if fog_prose is not None else primary_fog_type
    workflow_prose = workflow_prose if workflow_prose is not None else workflow_id
    return f"""# Repository Sensemaking Brief: contract regression fixture

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

The primary fog type is **{fog_prose}**.

## Recommended Workflow

Logic trace: the evidence shows the fixture boundary, so the fog is product
scope; this points to product_fog.

The recommended workflow is: {workflow_prose}

---

## Machine-readable Handoff

```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: {primary_fog_type}
evidence:
  - "README.md (L1-L2): fixture evidence"
recommended_workflow_id: {workflow_id}
weakness_type: Zero Validation
created_at: "2026-08-07T00:00:00Z"
immutable: true
```
"""


class TestGap2Vocabulary(unittest.TestCase):
    def test_vocabulary_map_exists_and_canonicalizes_escalation(self):
        m = yaml.safe_load((WORK / "artifact-vocabulary-map-v1.yaml").read_text(encoding="utf-8"))
        self.assertEqual(m["vocabulary_decisions"]["escalation_field"]["canonical"], "escalation_recommended")
        self.assertEqual(m["vocabulary_decisions"]["timestamps_field"]["canonical"], "created_at")

    def test_contract_required_fields_present_in_template(self):
        contracts = yaml.safe_load(CONTRACTS.read_text(encoding="utf-8"))
        brief_contract = next(
            a for a in contracts["artifacts"] if a["id"] == "repository_sensemaking_brief")
        template_fields = template_section13_fields()
        for field in brief_contract["required_machine_fields"]:
            self.assertIn(field, template_fields, f"template Section-13 missing {field}")

    def test_escalation_required_not_canonical_for_brief(self):
        contracts = yaml.safe_load(CONTRACTS.read_text(encoding="utf-8"))
        brief_contract = next(
            a for a in contracts["artifacts"] if a["id"] == "repository_sensemaking_brief")
        all_fields = (brief_contract["required_machine_fields"]
                      + brief_contract["recommended_machine_fields"])
        self.assertIn("escalation_recommended", all_fields)
        self.assertNotIn("escalation_required", all_fields)


class TestGap9Pipelines(unittest.TestCase):
    def test_skill_documents_runtime_pipeline(self):
        text = skill_text()
        self.assertIn("runtime reconciles model output into the canonical skeleton", text)
        self.assertIn("validate-and-record.py", text)

    def test_skill_documents_standalone_pipeline(self):
        text = skill_text()
        self.assertIn("model authors the COMPLETE artifact", text)
        self.assertIn("validate-brief.py", text)


class TestSemanticAgreementChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "README.md").write_text("line one\nline two\n", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _errors(self, text: str):
        brief = self.tmp / "brief.md"
        brief.write_text(text, encoding="utf-8")
        return validate_brief(str(brief), str(REPO_ROOT), target_repo=str(self.tmp))

    def test_fog_mismatch_warns(self):
        errors = self._errors(make_brief("product_fog", "product-implementation-workflow",
                                         fog_prose="architecture_fog"))
        messages = " ".join(e.get("message", "") for e in errors)
        self.assertIn("FOG_PROSE_MISMATCH", messages)
        self.assertTrue(all(e.get("severity") != "error" for e in errors),
                        "agreement mismatch must be a warning, not an error")

    def test_workflow_mismatch_warns(self):
        errors = self._errors(make_brief("product_fog", "product-implementation-workflow",
                                         workflow_prose="docs-implementation-workflow"))
        messages = " ".join(e.get("message", "") for e in errors)
        self.assertIn("WORKFLOW_PROSE_MISMATCH", messages)

    def test_agreement_is_silent(self):
        errors = self._errors(make_brief("product_fog", "product-implementation-workflow"))
        messages = " ".join(e.get("message", "") for e in errors)
        self.assertNotIn("FOG_PROSE_MISMATCH", messages)
        self.assertNotIn("WORKFLOW_PROSE_MISMATCH", messages)

    def test_mismatched_brief_still_valid(self):
        """Semantic agreement warnings must never flip validity."""
        errors = self._errors(make_brief("product_fog", "product-implementation-workflow",
                                         fog_prose="docs_fog"))
        self.assertTrue(all(e.get("severity") != "error" for e in errors))


if __name__ == "__main__":
    unittest.main()
