"""Commit 3 - weakest-boundary reasoning regressions.

- Skill content: candidate generation + scoring dimensions, selection rule,
  mandatory selection structure (incl. Alternatives considered + Confidence),
  no-manufactured-boundary rule, GAP-5 substantive-audit documentation,
  GAP-6 taxonomy mapping guidance.
- Deterministic candidate ranking (mirror of the skill's selection rule).
- Taxonomy invariants: all corpus ground-truth weaknesses and all baseline
  brief weakness_type values are within the seven canonical types.
- GAP-5 validator behavior: Ghost Features triggers the D5
  HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT warning (severity warning, not error).
"""

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import re
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CORPUS = REPO_ROOT / "experiments" / "repository-sensemaking-skill-hardening-v1" / "corpus"
SKILL = REPO_ROOT / "skills" / "repo-sensemaker" / "SKILL.md"
TEMPLATE = REPO_ROOT / "skills" / "repo-sensemaker" / "references" / "repo-analysis-template.md"

CANONICAL_TYPES = {
    "Vocabulary Drift", "Contract Mismatch", "Ghost Features", "Safety Gaps",
    "Implicit Dependencies", "Zero Validation", "Orphaned Examples",
}

sys.path.insert(0, str(REPO_ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("validate_brief", str(REPO_ROOT / "scripts" / "validate-brief.py"))
validate_brief_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_brief_module)
validate_brief = validate_brief_module.validate_brief


def score_candidate(evidence_strength, severity, blast_radius, goal_relevance,
                    downstream_blocking, uncertainty):
    """Deterministic mirror of the skill's selection rule.

    Higher is better; uncertainty is inverted (lower uncertainty is better).
    Values: high=3, medium=2, low=1.
    """
    v = {"high": 3, "medium": 2, "low": 1, "strong": 3, "weak": 1}
    return (
        v[evidence_strength] + v[severity] + v[blast_radius]
        + v[goal_relevance] + v[downstream_blocking] + (4 - v[uncertainty])
    )


def make_brief(weakness_type: str) -> str:
    return f"""# Repository Sensemaking Brief: boundary regression fixture

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

The recommended workflow is: product-implementation-workflow

---

## Machine-readable Handoff

```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: product_fog
evidence:
  - "README.md (L1-L2): fixture evidence"
recommended_workflow_id: product-implementation-workflow
weakness_type: {weakness_type}
created_at: "2026-08-07T00:00:00Z"
immutable: true
```
"""


def skill_text() -> str:
    import re as _re
    return _re.sub(r"\s+", " ", SKILL.read_text(encoding="utf-8"))


class TestSkillBoundaryContent(unittest.TestCase):
    def test_candidate_generation_documented(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("2-5 candidate boundaries", text)
        for dim in ("evidence_strength", "severity", "blast_radius",
                    "goal_relevance", "downstream_blocking_effect", "uncertainty"):
            self.assertIn(dim, text)

    def test_selection_rule_documented(self):
        text = skill_text()
        self.assertIn("Do NOT select merely the easiest problem to describe", text)

    def test_mandatory_structure_documented(self):
        text = SKILL.read_text(encoding="utf-8")
        for field in ("Boundary:", "Observed contract:", "Observed violation or uncertainty:",
                      "Evidence:", "Weakness type:", "Logic trace:", "Failure consequence:",
                      "Confidence:", "Alternatives considered:"):
            self.assertIn(field, text)
        template = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("Alternatives considered:", template)

    def test_no_manufactured_boundary_rule(self):
        self.assertIn("Do not manufacture a boundary", SKILL.read_text(encoding="utf-8"))

    def test_gap5_substantive_audit_documented(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT", text)
        self.assertIn("substantive human audit", text)

    def test_gap6_mapping_guidance_documented(self):
        text = SKILL.read_text(encoding="utf-8")
        for phrase in ("dead/unreachable code", "declared-but-unused dependency",
                       "exec()", "never-imported module"):
            self.assertIn(phrase, text)


class TestCandidateRanking(unittest.TestCase):
    def test_high_consequence_strong_evidence_wins(self):
        """The skill rule: consequence + evidence + centrality beat
        easy-to-describe candidates."""
        easy = score_candidate("medium", "low", "low", "low", "low", "low")   # easy to describe, unimportant
        hard = score_candidate("strong", "high", "high", "high", "high", "medium")  # consequential, evidenced
        self.assertGreater(hard, easy)

    def test_uncertainty_penalizes(self):
        a = score_candidate("strong", "high", "high", "high", "high", "low")
        b = score_candidate("strong", "high", "high", "high", "high", "high")
        self.assertGreater(a, b, "lower uncertainty should rank higher")


class TestTaxonomyInvariants(unittest.TestCase):
    def test_all_ground_truth_types_are_canonical(self):
        gt = yaml.safe_load((CORPUS / "ground-truth.yaml").read_text(encoding="utf-8"))["repositories"]
        for entry in gt:
            t = entry["known_weak_boundaries"][0]["type"]
            self.assertIn(t, CANONICAL_TYPES, f"{entry['repository_id']}: {t}")

    def test_all_baseline_brief_types_are_canonical(self):
        scored = yaml.safe_load(
            (REPO_ROOT / "experiments" / "repository-sensemaking-skill-hardening-v1" / "baseline-scored.yaml")
            .read_text(encoding="utf-8"))["rows"]
        for r in scored:
            t = r.get("weakness_type")
            self.assertIsNotNone(t, f"{r['repository_id']} has no weakness_type")
            self.assertIn(t, CANONICAL_TYPES, f"{r['repository_id']}: {t}")


def mapping_guard(case: str) -> str:
    """Deterministic mirror of the REPAIR-2 GAP-6 mapping guidance."""
    return {
        "declared_but_unused_dependency": "Implicit Dependencies",
        "packaging_metadata_gap": "Zero Validation",
        "unwired_module_undocumented": "Implicit Dependencies",
        "unwired_module_documented": "Ghost Features",
        "docs_misdescribing_existing_code": "Vocabulary Drift",
        "exec_loading_without_validation": "Zero Validation",
        "dead_code_documented_as_live": "Ghost Features",
        "dead_code_not_documented": "Orphaned Examples",
    }[case]


class TestGap6MappingGuard(unittest.TestCase):
    """REPAIR-2: pin the corrected mapping directions so Ghost Features
    cannot become the default bucket again."""

    def test_unused_dependency_maps_to_implicit_dependencies(self):
        self.assertEqual(mapping_guard("declared_but_unused_dependency"), "Implicit Dependencies")

    def test_packaging_gap_maps_to_zero_validation(self):
        self.assertEqual(mapping_guard("packaging_metadata_gap"), "Zero Validation")

    def test_docs_misdescribing_existing_code_maps_to_vocabulary_drift(self):
        self.assertEqual(mapping_guard("docs_misdescribing_existing_code"), "Vocabulary Drift")

    def test_unwired_module_undocumented_maps_to_implicit_dependencies(self):
        self.assertEqual(mapping_guard("unwired_module_undocumented"), "Implicit Dependencies")

    def test_unwired_module_documented_maps_to_ghost_features(self):
        self.assertEqual(mapping_guard("unwired_module_documented"), "Ghost Features")

    def test_skill_documents_unused_dep_is_not_ghost_features(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("declared-but-unused dependency", text)
        self.assertIn("NOT Ghost Features", text)
        self.assertIn("docs misdescribing EXISTING code", text)

    def test_skill_documents_ui_fog_tie_break(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("ui_fog precedence", text)
        self.assertIn("specialized decision procedure", text)

    def test_skill_documents_entry_point_stub_qualification(self):
        text = re.sub(r"\s+", " ", SKILL.read_text(encoding="utf-8"))
        self.assertIn("Entry-point stubs", text)
        self.assertIn("architecture_fog", text)
        self.assertIn("no implementation at all are product", text)


class TestGap5ValidatorBehavior(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "README.md").write_text("line one\nline two\n", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_ghost_features_triggers_substantive_audit_warning(self):
        brief = self.tmp / "brief.md"
        brief.write_text(make_brief("Ghost Features"), encoding="utf-8")
        errors = validate_brief(str(brief), str(REPO_ROOT), target_repo=str(self.tmp))
        messages = " ".join(e.get("message", "") for e in errors)
        self.assertIn("HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT", messages)
        self.assertFalse(any(e.get("severity") == "error" for e in errors),
                         "the D5 warning must not invalidate the artifact")

    def test_zero_validation_no_substantive_audit_warning(self):
        brief = self.tmp / "brief.md"
        brief.write_text(make_brief("Zero Validation"), encoding="utf-8")
        errors = validate_brief(str(brief), str(REPO_ROOT), target_repo=str(self.tmp))
        messages = " ".join(e.get("message", "") for e in errors)
        self.assertNotIn("HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT", messages)


if __name__ == "__main__":
    unittest.main()
