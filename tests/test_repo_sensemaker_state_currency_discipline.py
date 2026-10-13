"""Deterministic contract tests: the repo-sensemaker state-currency discipline.

Pins the durable learning codified after experiment S2 and the Auteur
authentic-reuse run: documented state is not automatically verified current
state; a recommendation that depends on a decision-changing current-state
claim must distinguish verified current state from merely documented state
(probe cited when verified, clearly identified when not); and clarification is
reserved for genuinely decision-changing owner intent, with empirical
uncertainty resolved through probes rather than by asking the owner to guess.

Like ``test_repo_sensemaker_evidence_contract.py``, this module is fully
deterministic and pins one demonstration fixture validated through the real
``validate-brief.py`` CLI — not model behavior.
"""

import json
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
