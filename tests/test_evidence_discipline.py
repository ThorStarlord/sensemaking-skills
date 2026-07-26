"""Tests for the issue #74 evidence-discipline safeguard.

Background: an independent evidence-quality audit of a live repo-sensemaker
run (experiments/evidence/0011-external-repo-auteur-rerun2/EVIDENCE.md) found
the model asserted a "ghost feature" absence claim based on a stale
docstring, while the function body it cited already implemented the claimed-
absent capability a few hundred lines further down in the same function.
The model never searched for evidence that would falsify its own claim.
Direct code inspection of scripts/skill_executor.py's
build_semantic_authorities_block (issue #58 / PR #72) confirmed it covered
workflow-ID/weakness-type vocabulary and evidence-excerpt shape, but said
nothing about contradiction search or authority ordering for absence claims.
This suite proves the fix (build_evidence_discipline_block, called from
build_semantic_authorities_block) closes that gap.

HONEST SCOPE STATEMENT (same discipline as PR #59/#72's precedent):
  - TestLivePromptContainsEvidenceDiscipline proves the actual constructed
    live prompt (not just static file content) contains the required
    instruction text.
  - TestAdversarialFixtureContradictionIsFindable proves a deterministic
    fixture is constructed such that the exact contradiction pattern from
    the real auteur incident (stale docstring vs. real implementation) is
    findable by bounded, targeted search -- NOT that a live model would
    actually perform that search.
  - TestNoTrivialSatisfactionMarkers guards against repeating the PR #72
    near-miss (a runtime-owned skeleton/prompt containing a literal marker
    phrase that would trivially satisfy a validator regardless of genuine
    model reasoning).
  - NEITHER prompt-construction tests nor fixture tests prove live model
    obedience. The independent post-run evidence-quality audit (as
    performed manually for PR #73/EVIDENCE.md) remains mandatory regardless
    of this fix -- this fix reduces the odds of the failure, it does not
    eliminate the need to check for it.
"""

import os
import sys
import unittest

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "evidence_discipline_adversarial")
sys.path.insert(0, SCRIPTS_DIR)

import skill_executor as se  # noqa: E402
import brief_skeleton as bs  # noqa: E402


class TestLivePromptContainsEvidenceDiscipline(unittest.TestCase):
    """Proves the actual constructed prompt (build_skeleton_prompt via
    build_semantic_authorities_block), not just the static block's source
    text, contains the required instruction content."""

    @classmethod
    def setUpClass(cls):
        executor = se.ClaudeAgentSdkSkillExecutor.__new__(se.ClaudeAgentSdkSkillExecutor)
        executor.repo_root = REPO_ROOT
        cls.prompt = executor.build_skeleton_prompt(
            "repo-sensemaker", "", "artifacts/repository_sensemaking_brief.md"
        )

    def test_prompt_requires_contradiction_search_for_absence_claims(self):
        low = self.prompt.lower()
        self.assertIn("absence", low)
        self.assertIn("contradiction search", low)
        self.assertIn("falsify", low)

    def test_prompt_requires_symbol_and_callee_inspection(self):
        low = self.prompt.lower()
        self.assertIn("usages", low)
        self.assertIn("callees", low)
        self.assertIn("entry point", low)

    def test_prompt_states_authority_ordering(self):
        low = self.prompt.lower()
        self.assertIn("authority ordering", low)
        # executable code/config must outrank comments/docstrings and
        # historical/status notes, in that direction
        self.assertIn("executable code", low)
        self.assertIn("comments and docstrings", low)
        self.assertIn("status files", low)

    def test_prompt_requires_uncertainty_downgrade_when_incomplete(self):
        low = self.prompt.lower()
        self.assertIn("downgrade", low)
        self.assertIn("uncertainty", low)

    def test_prompt_requires_disconfirmation_recorded_in_reasoning(self):
        low = self.prompt.lower()
        self.assertIn("disconfirmation", low)

    def test_prompt_does_not_require_exhaustive_line_by_line_reading(self):
        low = self.prompt.lower()
        self.assertIn("targeted searches", low)
        self.assertIn("not required", low)

    def test_prompt_contains_no_auteur_specific_language(self):
        # This fix must be generic -- no hardcoded auteur names, layers,
        # paths, or symbols anywhere in the live prompt.
        low = self.prompt.lower()
        for forbidden in (
            "auteur",
            "diagnosticlayer",
            "_analyze_structure",
            "run_all_diagnostics",
            "9-layer",
            "resonance",
        ):
            self.assertNotIn(forbidden, low, f"prompt leaked repo-specific term: {forbidden!r}")

    def test_evidence_discipline_does_not_weaken_existing_requirements(self):
        # Sanity: the pre-existing quote/supports_claim/logic-trace guidance
        # (PR #72) must still be present alongside the new block.
        for field in ("quote", "supports_claim"):
            self.assertIn(f"`{field}`", self.prompt)
        self.assertIn("Logic trace:", self.prompt)


class TestNoTrivialSatisfactionMarkers(unittest.TestCase):
    """Guards against repeating the exact PR #72 near-miss: a runtime-owned
    skeleton containing a literal marker phrase a validator scans for, which
    would trivially satisfy that check regardless of genuine model output.

    This fix introduces no NEW validator and no new literal marker phrase
    for validate-brief.py to scan for (see build_evidence_discipline_block's
    docstring) -- so this test is a forward-looking guard: it asserts the
    runtime-owned skeleton (which IS partially injected into every brief
    regardless of model behavior) does not contain the new instructional
    vocabulary this fix adds, since if a future validator started scanning
    for e.g. "contradiction search" or "authority ordering", a skeleton
    that already contained those words would trivially pass without any
    genuine model reasoning -- exactly PR #72's mistake, generalized.
    """

    @classmethod
    def setUpClass(cls):
        cls.skeleton = bs.build_skeleton()

    def test_skeleton_does_not_contain_new_marker_vocabulary(self):
        low = self.skeleton.lower()
        for marker in ("contradiction search", "authority ordering", "disconfirmation"):
            self.assertNotIn(
                marker,
                low,
                f"skeleton contains new evidence-discipline marker phrase {marker!r} -- "
                "this would let a future validator be trivially satisfied by the "
                "runtime skeleton alone, regardless of genuine model reasoning "
                "(the exact PR #72 near-miss, generalized).",
            )

    def test_skeleton_still_passes_integrity_check(self):
        self.assertTrue(bs.skeleton_integrity_ok(self.skeleton))


class TestAdversarialFixtureContradictionIsFindable(unittest.TestCase):
    """Proves the deterministic fixture at
    tests/fixtures/evidence_discipline_adversarial/ contains a findable
    contradiction of the exact shape the real auteur incident exhibited:
    a stale docstring claiming absence, an entry point calling a helper
    that implements the claimed-absent capability, and enum/member usages
    proving the capability exists.

    Scope: this proves the CONTRADICTION IS DISCOVERABLE by the bounded
    search steps the prompt now requires (grep for symbol usage; read the
    cited function's full body) -- it does not run a live model against
    this fixture and does not prove any model would actually perform the
    search. It exists so the policy this fix encodes is testable
    deterministically, independent of live model behavior.
    """

    @classmethod
    def setUpClass(cls):
        path = os.path.join(FIXTURE_DIR, "module_under_test.py")
        with open(path, encoding="utf-8") as f:
            cls.source = f.read()

    def test_fixture_contains_stale_docstring_claiming_absence(self):
        self.assertIn("Currently runs: STRUCTURE only", self.source)

    def test_fixture_entry_point_calls_helper_implementing_the_feature(self):
        self.assertIn("def run_all_diagnostics(document):", self.source)
        self.assertIn("_analyze_structure(document)", self.source)

    def test_fixture_helper_actually_implements_claimed_absent_capability(self):
        # Symbol/member usages proving THEME and MODULATION diagnostics are
        # real, reachable code -- exactly what a step-2/step-3 search
        # (symbol usage + callee inspection) would surface.
        self.assertIn("DiagnosticLayer.THEME", self.source)
        self.assertIn("DiagnosticLayer.MODULATION", self.source)
        self.assertIn('"theme.thesis_unrepresented"', self.source)
        self.assertIn('"modulation.pov_underutilized"', self.source)

    def test_tempting_false_claim_document_describes_the_trap(self):
        claim_path = os.path.join(FIXTURE_DIR, "tempting_false_claim.md")
        with open(claim_path, encoding="utf-8") as f:
            claim_text = f.read()
        self.assertIn("Ghost Features", claim_text)
        self.assertIn("FALSE", claim_text)

    def test_grep_for_symbol_usage_falsifies_the_absence_claim(self):
        # Simulates prompt requirement #2 (search for symbol/enum/member
        # usages) and #4 (deliberately search for falsifying evidence):
        # a simple substring search for the enum members the false claim
        # says have "no active diagnostic rules" immediately finds
        # contradicting, reachable code.
        for member, usage in (
            ("THEME = ", "DiagnosticLayer.THEME"),
            ("MODULATION = ", "DiagnosticLayer.MODULATION"),
        ):
            self.assertIn(member, self.source, f"expected enum member declaration {member!r}")
            self.assertIn(usage, self.source, f"expected real usage site {usage!r}")


if __name__ == "__main__":
    unittest.main()
