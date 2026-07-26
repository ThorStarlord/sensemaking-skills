"""Regression tests for the evidence-excerpt quote/supports_claim and
logic-trace bug exposed by PR #70 (external auteur rerun, issue tracked
separately from #68/PR #69's target_repo citation-path fix -- this is a
DIFFERENT bug).

Background: PR #70 preserved a live repo-sensemaker run against a disposable
clone of an external repo. The citation-path bug (issue #68) did not
reproduce (PR #69's fix held), but validate-brief.py still failed with
NO_LOGIC_TRACE and EVIDENCE_EXCERPT_FIELD (missing quote/supports_claim) on
all 5 evidence excerpts. Root cause: the live execution instruction built by
ClaudeAgentSdkSkillExecutor.build_skeleton_prompt (via
build_semantic_authorities_block) told the model to "fill in ... the
evidence_excerpts YAML block under Section 8" but never named the four
required per-excerpt fields or explained what `quote` / `supports_claim`
mean, and never mentioned the "Logic trace:" phrase requirement at all --
even though the static template
(skills/repo-sensemaker/references/repo-analysis-template.md) documents both
correctly. The model produced a `citation` field instead of `quote`/
`supports_claim` and never wrote a "Logic trace:" paragraph, exactly as this
suite reproduces.

This suite proves:
  1. The live prompt now explicitly names quote/supports_claim/logic trace.
  2. The runtime-owned skeleton (brief_skeleton.py) now scaffolds a reminder
     for both requirements.
  3. reconcile() preserves model-populated quote/supports_claim unchanged.
  4/5. Negative regressions: missing quote/supports_claim, and missing logic
     trace, both still fail validate-brief.py (validator strictness is
     unchanged).
  6. A correctly-shaped fixture (quote, supports_claim, logic trace all
     present) passes the real validator.
"""

import importlib.util
import os
import sys
import tempfile
import unittest

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, SCRIPTS_DIR)

import skill_executor as se  # noqa: E402
import brief_skeleton as bs  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "validate_brief", os.path.join(SCRIPTS_DIR, "validate-brief.py")
)
validate_brief_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_brief_module)
validate_brief = validate_brief_module.validate_brief
NO_LOGIC_TRACE = validate_brief_module.NO_LOGIC_TRACE
EVIDENCE_EXCERPT_FIELD = validate_brief_module.EVIDENCE_EXCERPT_FIELD


def _codes(errors):
    return [e["message"] for e in errors]


def _write_tmp(content: str) -> str:
    fd, path = tempfile.mkstemp(suffix=".md")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(content)
    return path


class TestLivePromptGuidance(unittest.TestCase):
    """The actual constructed prompt (build_skeleton_prompt), not just static
    file content -- same discipline as test_semantic_authorities.py."""

    @classmethod
    def setUpClass(cls):
        executor = se.ClaudeAgentSdkSkillExecutor.__new__(se.ClaudeAgentSdkSkillExecutor)
        executor.repo_root = REPO_ROOT
        cls.prompt = executor.build_skeleton_prompt(
            "repo-sensemaker", "", "artifacts/repository_sensemaking_brief.md"
        )

    def test_prompt_names_all_four_evidence_excerpt_fields(self):
        for field in ("file", "lines", "quote", "supports_claim"):
            self.assertIn(f"`{field}`", self.prompt, f"required field '{field}' not named in prompt")

    def test_prompt_explains_quote_and_supports_claim_semantics(self):
        low = self.prompt.lower()
        self.assertIn("verbatim", low)
        self.assertIn("supports_claim", low)
        self.assertIn("claim", low)

    def test_prompt_warns_against_wrong_field_name(self):
        # The reproducing PR #70 brief used `citation` instead of quote/
        # supports_claim -- the prompt must call this out as insufficient.
        self.assertIn("citation", self.prompt)

    def test_prompt_states_logic_trace_requirement_with_literal_marker_words(self):
        self.assertIn("Logic trace:", self.prompt)
        self.assertIn("NO_LOGIC_TRACE", self.prompt)

    def test_prompt_is_not_hardcoded_duplicate(self):
        # Sanity: the guidance is a static block appended to the function,
        # not accidentally omitted by some conditional.
        with open(os.path.join(SCRIPTS_DIR, "skill_executor.py"), encoding="utf-8") as f:
            source = f.read()
        self.assertIn("EVIDENCE_EXCERPT_FIELD", source)


class TestSkeletonScaffolding(unittest.TestCase):
    """The runtime-owned skeleton itself carries a reminder for both
    requirements, independent of the prompt."""

    @classmethod
    def setUpClass(cls):
        cls.skeleton = bs.build_skeleton()

    def test_skeleton_reminds_about_logic_trace(self):
        # The skeleton must NOT contain the literal "logic trace" phrase
        # itself (that would trivially satisfy validate-brief.py's
        # NO_LOGIC_TRACE substring check regardless of what the model
        # writes, silently defeating the validator). It must still mention
        # the error code so the requirement is discoverable.
        self.assertNotIn("logic trace", self.skeleton.lower())
        self.assertIn("NO_LOGIC_TRACE", self.skeleton)
        self.assertIn("diagnostic reasoning", self.skeleton.lower())

    def test_skeleton_reminds_about_required_excerpt_fields(self):
        self.assertIn("quote", self.skeleton)
        self.assertIn("supports_claim", self.skeleton)
        self.assertIn("EVIDENCE_EXCERPT_FIELD", self.skeleton)

    def test_skeleton_still_passes_integrity_check(self):
        self.assertTrue(bs.skeleton_integrity_ok(self.skeleton))


VALID_MODEL_OUTPUT = """
<!-- MODEL_SECTION:repository_goal:BEGIN -->
This repo builds sensemaking skills for repository diagnosis.
<!-- MODEL_SECTION:repository_goal:END -->

<!-- MODEL_SECTION:weakest_boundary_prose:BEGIN -->
**Weakness type:** Zero Validation
<!-- MODEL_SECTION:weakest_boundary_prose:END -->

<!-- MODEL_SECTION:evidence_prose:BEGIN -->
Logic trace: scripts/validate-brief.py:312 requires quote and supports_claim
on every excerpt, which is the chain from that check to the weakest-boundary
conclusion here.
<!-- MODEL_SECTION:evidence_prose:END -->

<!-- MODEL_SECTION:evidence_excerpts:BEGIN -->
```yaml
evidence_excerpts:
  - file: scripts/validate-brief.py
    lines: L312-L314
    quote: "for field in [\\"file\\", \\"lines\\", \\"quote\\", \\"supports_claim\\"]:"
    supports_claim: "Confirms the validator requires all four named fields per excerpt."
```
<!-- MODEL_SECTION:evidence_excerpts:END -->

```yaml
primary_fog_type: architecture_fog
recommended_workflow_id: architecture-implementation-workflow
escalation_recommended: false
evidence:
  - "scripts/validate-brief.py (lines L312-L314): weak boundary"
```
"""


class TestReconciliationPreservesFields(unittest.TestCase):
    def test_reconcile_preserves_quote_and_supports_claim_unchanged(self):
        reconciled = bs.reconcile(VALID_MODEL_OUTPUT)
        self.assertIn(
            'quote: "for field in [\\"file\\", \\"lines\\", \\"quote\\", \\"supports_claim\\"]:"',
            reconciled,
        )
        self.assertIn(
            'supports_claim: "Confirms the validator requires all four named fields per excerpt."',
            reconciled,
        )

    def test_reconcile_preserves_logic_trace_paragraph(self):
        reconciled = bs.reconcile(VALID_MODEL_OUTPUT)
        self.assertIn("Logic trace:", reconciled)


class TestValidatorNegativeRegressions(unittest.TestCase):
    """Validator strictness must NOT be weakened by this fix."""

    def test_missing_quote_and_supports_claim_still_fails(self):
        broken = VALID_MODEL_OUTPUT.replace(
            '    quote: "for field in [\\"file\\", \\"lines\\", \\"quote\\", \\"supports_claim\\"]:"\n'
            '    supports_claim: "Confirms the validator requires all four named fields per excerpt."\n',
            '    citation: "wrong field name, like the PR #70 reproduction"\n',
        )
        reconciled = bs.reconcile(broken)
        path = _write_tmp(reconciled)
        try:
            errors = validate_brief(path, REPO_ROOT)
            codes = _codes(errors)
            self.assertTrue(
                any(EVIDENCE_EXCERPT_FIELD in c for c in codes),
                f"expected {EVIDENCE_EXCERPT_FIELD} in errors, got {codes}",
            )
        finally:
            os.remove(path)

    def test_missing_logic_trace_still_fails(self):
        broken = VALID_MODEL_OUTPUT.replace(
            "Logic trace: scripts/validate-brief.py:312 requires quote and supports_claim\n"
            "on every excerpt, which is the chain from that check to the weakest-boundary\n"
            "conclusion here.",
            "This paragraph cites scripts/validate-brief.py:312 but never states its reasoning chain.",
        )
        reconciled = bs.reconcile(broken)
        # bs.build_skeleton() itself also carries the reminder text
        # containing "Logic trace:" as an HTML comment placeholder if the
        # model section wasn't filled -- here it WAS filled (overwriting the
        # placeholder), so the literal phrase must be genuinely absent.
        self.assertNotIn("Logic trace:", reconciled)
        path = _write_tmp(reconciled)
        try:
            errors = validate_brief(path, REPO_ROOT)
            codes = _codes(errors)
            self.assertTrue(
                any(NO_LOGIC_TRACE in c for c in codes),
                f"expected {NO_LOGIC_TRACE} in errors, got {codes}",
            )
        finally:
            os.remove(path)


class TestValidatorPositiveRegression(unittest.TestCase):
    def test_correctly_shaped_fixture_passes_real_validator(self):
        reconciled = bs.reconcile(VALID_MODEL_OUTPUT)
        path = _write_tmp(reconciled)
        try:
            errors = validate_brief(path, REPO_ROOT)
            self.assertEqual(errors, [], f"expected no errors, got {errors}")
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
