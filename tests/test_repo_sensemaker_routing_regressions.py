"""Commit 5 - workflow routing regressions.

- Registry authority: only canonical-registry IDs route; skill IDs are not
  workflow IDs; target-repo registries must not ground routing.
- GAP-7: recommended_execution_mode must come from the workflow's allowed
  modes; plan_only is not invented where the registry does not list it.
- Negative routing (validator-level): skill ID, near-match ID, stale
  target-repo registry IDs are all rejected.
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
REGISTRY = REPO_ROOT / "skills" / "workflow-planner" / "references" / "workflow-registry.yaml"
CORPUS = REPO_ROOT / "experiments" / "repository-sensemaking-skill-hardening-v1" / "corpus"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("validate_brief", str(REPO_ROOT / "scripts" / "validate-brief.py"))
validate_brief_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_brief_module)
validate_brief = validate_brief_module.validate_brief

ALL_MODES = {"plan_only", "prompt_chain", "guided_execution", "autonomous_execution", "yolo_execution"}


def skill_text() -> str:
    return re.sub(r"\s+", " ", SKILL.read_text(encoding="utf-8"))


def registry() -> list[dict]:
    return yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))["workflows"]


def make_brief(workflow_id: str, mode: str = "guided_execution") -> str:
    return f"""# Repository Sensemaking Brief: routing regression fixture

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

Based on the evidence, the primary fog type is **product_fog**.

The recommended workflow is: {workflow_id}

---

## Machine-readable Handoff

```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: product_fog
evidence:
  - "README.md (L1-L2): fixture evidence"
recommended_workflow_id: {workflow_id}
recommended_execution_mode: {mode}
weakness_type: Zero Validation
created_at: "2026-08-07T00:00:00Z"
immutable: true
```
"""


class TestSkillRoutingContent(unittest.TestCase):
    def test_registry_authority_documented(self):
        text = skill_text()
        self.assertIn("Never substitute a skill ID", text)
        self.assertIn("Never infer an ID from naming conventions", text)
        self.assertIn("target-repo registries are untrusted", text)

    def test_routing_rationale_documented(self):
        text = skill_text()
        self.assertIn("why this workflow", text)
        self.assertIn("why not the closest alternatives", text)
        self.assertIn("preconditions are missing", text)

    def test_gap7_no_invented_modes_documented(self):
        text = skill_text()
        self.assertIn("Never invent a mode", text)
        self.assertIn("architecture-implementation-workflow", text)
        self.assertIn("Recommending a workflow", text)
        self.assertIn("No Implementation boundary is unaffected", text)

    def test_template_mode_guidance_is_registry_based(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        line = next(l for l in text.splitlines() if "recommended_execution_mode:" in l)
        self.assertIn("allowed_execution_modes", line)
        self.assertNotIn("plan_only | guided_execution", line)


class TestRegistryInvariants(unittest.TestCase):
    def test_all_ids_unique(self):
        ws = registry()
        ids = [w["id"] for w in ws]
        self.assertEqual(len(ids), len(set(ids)))

    def test_all_modes_are_known(self):
        for w in registry():
            for mode in w.get("allowed_execution_modes", []):
                self.assertIn(mode, ALL_MODES, f"{w['id']}: unknown mode {mode}")

    def test_gap7_architecture_workflow_has_no_plan_only(self):
        ws = {w["id"]: w for w in registry()}
        self.assertNotIn("plan_only", ws["architecture-implementation-workflow"]["allowed_execution_modes"])

    def test_skill_ids_are_not_workflow_ids(self):
        ids = {w["id"] for w in registry()}
        self.assertNotIn("docs-aligner", ids)

    def test_stale_target_registry_ids_not_canonical(self):
        """adv-multi-registry fixture: its stale registry IDs must not exist
        in the canonical registry (routing must never ground on them)."""
        ids = {w["id"] for w in registry()}
        stale = yaml.safe_load(
            (CORPUS / "adv-multi-registry" / "docs" / "workflow-registry.yaml").read_text(encoding="utf-8"))
        for w in stale["workflows"]:
            self.assertNotIn(w["id"], ids, f"stale ID {w['id']} must not be canonical")


class TestNegativeRouting(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "README.md").write_text("line one\nline two\n", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _errors(self, brief_text: str):
        brief = self.tmp / "brief.md"
        brief.write_text(brief_text, encoding="utf-8")
        return validate_brief(str(brief), str(REPO_ROOT), target_repo=str(self.tmp))

    def test_skill_id_rejected(self):
        """docs-aligner is a skill, not a workflow - must be hallucinated."""
        errors = self._errors(make_brief("docs-aligner"))
        messages = " ".join(e.get("message", "") for e in errors)
        self.assertIn("HALLUCINATED_WORKFLOW_ID", messages)

    def test_near_match_id_rejected(self):
        """arch-implementation-workflow (missing 'itecture') is not canonical."""
        errors = self._errors(make_brief("arch-implementation-workflow"))
        messages = " ".join(e.get("message", "") for e in errors)
        self.assertIn("HALLUCINATED_WORKFLOW_ID", messages)

    def test_valid_workflow_accepted(self):
        errors = self._errors(make_brief("product-implementation-workflow"))
        self.assertEqual([e for e in errors if e.get("severity") == "error"], [],
                         f"valid workflow must have no errors: {errors}")


if __name__ == "__main__":
    unittest.main()
