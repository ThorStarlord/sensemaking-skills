"""Deterministic contract tests: the repo-sensemaker state-currency discipline.

Pins the durable learning codified after experiment S2 and the Auteur
authentic-reuse run: documented state is not automatically verified current
state; a recommendation that depends on a decision-changing current-state
claim must distinguish verified current state from merely documented state
(probe cited when verified, clearly identified when not); and clarification is
reserved for genuinely decision-changing owner intent, with empirical
uncertainty resolved through probes rather than by asking the owner to guess.

Like ``test_repo_sensemaker_evidence_contract.py``, this module is fully
deterministic and pins the *codified contract* — the skill text, the template
guidance, and one demonstration fixture validated through the real
``validate-brief.py`` CLI — not model behavior.
"""

import json
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_PATH = os.path.join(REPO_ROOT, "skills", "repo-sensemaker", "SKILL.md")
TEMPLATE_PATH = os.path.join(
    REPO_ROOT, "skills", "repo-sensemaker", "references", "repo-analysis-template.md"
)
VALIDATE_BRIEF = os.path.join(REPO_ROOT, "scripts", "validate-brief.py")
DISCIPLINE_FIXTURE = os.path.join(
    REPO_ROOT, "tests", "fixtures", "repo-sensemaker-state-currency-good.md"
)


def read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        # Normalize whitespace: guidance prose is markdown-wrapped across
        # lines, and the tests pin semantics, not line wrapping.
        return " ".join(f.read().split())


def run_validate_brief(path: str) -> dict:
    result = subprocess.run(
        [sys.executable, VALIDATE_BRIEF, path, "--json"],
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


class TestSkillCodifiesStateCurrency:
    """The workflow codifies the S2 boundary: documented state != current state."""

    def test_evidence_gathering_requires_state_currency_verification(self):
        text = read(SKILL_PATH)
        assert "documented state is not automatically verified current state" in text
        assert "cheapest repository probe" in text
        assert "documented but not independently verified" in text
        # The specific S2 failure mode: documentation of unfinished work is not
        # proof that work remains unfinished.
        assert "unfinished documentation as proof that work remains unfinished" in text

    def test_synthesis_requires_claim_provenance_separation(self):
        text = read(SKILL_PATH)
        assert "observed evidence, documented claims, inference" in text
        assert "owner-supplied judgment/context" in text
        assert "distinguishable" in text
        assert "verified current state from merely documented state" in text

    def test_clarification_policy_is_durable_not_numeric(self):
        """The durable rule is 'no unnecessary questions; neutral clarification
        when genuinely needed' — deliberately NOT the experimental 'at most one
        question' constraint, which was an S1/S2 probe constraint, not a
        product rule."""
        text = read(SKILL_PATH)
        assert "Ask no questions when repository evidence is sufficient" in text
        assert "materially change the recommendation" in text
        assert "neutral, high-information" in text
        assert "probes rather than asking the owner to guess" in text
        assert "at most one" not in text


class TestTemplateCodifiesGuidance:
    """The brief template carries the same discipline as producer guidance."""

    def test_section7_codifies_state_currency_and_provenance(self):
        text = read(TEMPLATE_PATH)
        assert "State currency and claim provenance (required)" in text
        assert "verified current state from merely documented state" in text
        assert "cite the probe used" in text
        assert "documented but not independently verified" in text
        assert "Never treat documented state as automatically current" in text

    def test_section11_requires_probe_or_unverified_identification(self):
        text = read(TEMPLATE_PATH)
        assert "cite the probe that verified it" in text
        assert "documented but not independently verified" in text


class TestDisciplineFixture:
    """The demonstration fixture shows one good representation and stays
    compatible with the real validator (no contract breakage)."""

    def test_fixture_demonstrates_the_distinction_without_literal_tokens(self):
        text = read(DISCIPLINE_FIXTURE)
        # Verified claim: probe cited in prose.
        assert "git history" in text
        assert "probe" in text
        # Unverified documented claim: clearly identified.
        assert "documented but not independently verified" in text
        # The distinction is semantic, not a serialization format: the fixture
        # must not rely on literal label tokens.
        assert "verified:" not in text
        assert "documented-not-verified:" not in text

    def test_fixture_passes_the_real_validator(self):
        result = run_validate_brief(DISCIPLINE_FIXTURE)
        assert result["valid"] is True, result["errors"]
        assert result["errors"] == []
