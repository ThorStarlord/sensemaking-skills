"""Contract checks for Experiment Economy & Proportional Rigor v1.

These tests establish that the guidance surfaces and non-identities remain
present. They do not establish that an experiment is semantically warranted or
that a chosen rigor level is empirically optimal.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "skills" / "using-sensemaking" / "SKILL.md"
INQUIRY = ROOT / "skills" / "using-sensemaking" / "references" / "inquiry-policy-v0.md"
METAREASONING = (
    ROOT / "skills" / "using-sensemaking" / "references" / "metareasoning-policy-v0.md"
)
ECONOMY = (
    ROOT / "skills" / "using-sensemaking" / "references" / "experiment-economy-v1.md"
)
STRATEGIC_SKILL = ROOT / "skills" / "strategic-repository-analysis" / "SKILL.md"


def test_inquiry_policy_links_experiment_economy_reference() -> None:
    text = INQUIRY.read_text(encoding="utf-8")

    assert "experiment-economy-v1.md" in text


def test_metareasoning_links_experiment_economy_reference() -> None:
    text = METAREASONING.read_text(encoding="utf-8")

    assert "experiment-economy-v1.md" in text


def test_using_sensemaking_links_experiment_economy_reference() -> None:
    text = BOOTSTRAP.read_text(encoding="utf-8")

    assert ECONOMY.exists()
    assert "experiment-economy-v1.md" in text


def test_strategic_analysis_links_experiment_economy_reference() -> None:
    skill = STRATEGIC_SKILL.read_text(encoding="utf-8")

    assert "experiment-economy-v1.md" in skill


def test_experiment_economy_adds_no_runtime_or_scoring_authority() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    for forbidden in (
        "ExperimentEngine",
        "ExperimentRouter",
        "EvidenceGradeSelector",
    ):
        assert forbidden not in pyproject
