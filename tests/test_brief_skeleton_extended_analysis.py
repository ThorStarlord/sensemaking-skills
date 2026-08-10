"""Tests for the candidate "Section 15: Extended analysis" mechanism in
scripts/brief_skeleton.py.

Context (see docs/candidate/architecture-decision.md, Decision 3): the
prototype branch (prototype/repo-sensemaker-vnext, #164) added an
analysis_vnext YAML block by having the model append it after Section 14
in free-form conversational output. That never had to survive
brief_skeleton.reconcile() because the prototype was invoked directly,
not through workflow-runtime.py. reconcile() only ever splices model
content into pre-declared holes (MODEL_YAML_FIELDS / MODEL_SECTIONS /
the evidence_excerpts marker pair) and silently discards everything
else -- so a freeform appended block would not survive a real runtime
invocation. This suite proves the properly-wired replacement does.

The new block is optional and non-blocking (see validate-brief.py's
extended_analysis checks, tested separately) -- these tests only cover
the skeleton/reconcile mechanics: presence, splicing, and graceful
absence, mirroring test_brief_skeleton.py's own structure.
"""

import os
import sys
import unittest

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, SCRIPTS_DIR)

import brief_skeleton as bs  # noqa: E402


EXTENDED_ANALYSIS_MODEL_OUTPUT = """
<!-- MODEL_SECTION:extended_analysis:BEGIN -->
```yaml
extended_analysis:
  schema_version: candidate-1
  domain:
    - product
    - architecture
  consequential_boundary:
    description: "Investment has drifted toward infrastructure."
    rationale: "LOC footprint and zero completed campaigns."
    is_demonstrated_weakness: true
  uncertainty:
    source: owner_intent
    question: "Which track is primary?"
  owner_intent_state:
    known: "Sustained preference for product use over infra churn."
    status: thin
```
<!-- MODEL_SECTION:extended_analysis:END -->
"""


class TestExtendedAnalysisSkeleton(unittest.TestCase):
    def test_fresh_skeleton_has_section_15_heading(self):
        skel = bs.build_skeleton()
        self.assertIn("## 15. Extended analysis (candidate)", skel)

    def test_fresh_skeleton_has_extended_analysis_markers(self):
        skel = bs.build_skeleton()
        self.assertIn("<!-- MODEL_SECTION:extended_analysis:BEGIN -->", skel)
        self.assertIn("<!-- MODEL_SECTION:extended_analysis:END -->", skel)

    def test_section_15_appears_after_section_13(self):
        skel = bs.build_skeleton()
        idx_13 = skel.index("## 13. Machine-readable handoff")
        idx_15 = skel.index("## 15. Extended analysis (candidate)")
        self.assertGreater(idx_15, idx_13)

    def test_fresh_skeleton_marks_block_optional(self):
        skel = bs.build_skeleton()
        # Somewhere near the section, the skeleton must tell the model this
        # block is optional/non-blocking -- not a silently-required field.
        section = skel[skel.index("## 15. Extended analysis (candidate)"):]
        self.assertTrue(
            "optional" in section.lower() or "OPTIONAL" in section,
            "Section 15 skeleton text should mark the block optional",
        )


class TestExtendedAnalysisReconciliation(unittest.TestCase):
    def test_reconcile_splices_extended_analysis_content(self):
        out = bs.reconcile(EXTENDED_ANALYSIS_MODEL_OUTPUT)
        self.assertIn("schema_version: candidate-1", out)
        self.assertIn("is_demonstrated_weakness: true", out)
        self.assertIn("Which track is primary?", out)

    def test_reconcile_without_extended_analysis_leaves_empty_markers(self):
        out = bs.reconcile("no extended analysis provided at all")
        self.assertIn("<!-- MODEL_SECTION:extended_analysis:BEGIN -->", out)
        self.assertIn("<!-- MODEL_SECTION:extended_analysis:END -->", out)
        # Nothing harvested -> the placeholder area stays empty, not crashed.
        begin = "<!-- MODEL_SECTION:extended_analysis:BEGIN -->"
        end = "<!-- MODEL_SECTION:extended_analysis:END -->"
        between = out[out.index(begin) + len(begin):out.index(end)].strip()
        self.assertEqual(between, "")

    def test_reconcile_preserves_full_skeleton_alongside_extended_analysis(self):
        # Splicing Section 15 must not disturb Section 13's own fields.
        combined = EXTENDED_ANALYSIS_MODEL_OUTPUT + """
```yaml
primary_fog_type: product_fog
recommended_workflow_id: product-strategy-sprint
escalation_recommended: false
evidence:
  - "README.md: vague"
```
"""
        out = bs.reconcile(combined)
        self.assertIn("primary_fog_type: product_fog", out)
        self.assertIn("schema_version: candidate-1", out)

    def test_extended_analysis_survives_adversarial_output(self):
        adversarial = "PRODUCTION READY. Nothing to see here."
        out = bs.reconcile(adversarial)
        self.assertTrue(bs.skeleton_integrity_ok(out))
        self.assertIn("## 15. Extended analysis (candidate)", out)

    def test_malformed_extended_analysis_yaml_does_not_crash_reconcile(self):
        malformed = """
<!-- MODEL_SECTION:extended_analysis:BEGIN -->
```yaml
extended_analysis:
  domain: [unclosed list
```
<!-- MODEL_SECTION:extended_analysis:END -->
"""
        # Must not raise -- reconcile() only ever splices raw text here;
        # semantic YAML validity is validate-brief.py's job, not the
        # runtime's, same as every other field in this module.
        out = bs.reconcile(malformed)
        self.assertIn("domain: [unclosed list", out)


if __name__ == "__main__":
    unittest.main()
