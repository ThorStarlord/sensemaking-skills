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
STRATEGIC_CONTRACT = ROOT / "docs" / "strategic-repository-sensemaking-v1.md"
POLICY = ROOT / "docs" / "policy-hierarchy-v0.md"


def test_experiment_economy_defines_warrant_before_rigor() -> None:
    text = ECONOMY.read_text(encoding="utf-8")

    for phrase in (
        "Experiment Warrant Gate",
        "Minimum Sufficient Experimental Rigor",
        "Confounder Warrant",
        "TOTAL EXPERIMENT COST",
        "INVESTIGATE\n!= EXPERIMENT",
        "possible confounder\n!= required control",
        "research-grade evidence\n!= default product-development evidence",
        "cheap reversible construction\ncan be the cheapest sufficient inquiry",
    ):
        assert phrase in text

    assert "do not create a numeric expected-value score" in text
    assert "not an engine, scorer, router, or experiment framework" in text


def test_inquiry_policy_does_not_equate_investigation_with_experiment() -> None:
    text = INQUIRY.read_text(encoding="utf-8")

    for phrase in (
        "INVESTIGATE\n!= EXPERIMENT",
        "experiment possible\n!= experiment warranted",
        "experiment-economy-v1.md",
        "cheap reversible construction",
        "total experiment cost",
    ):
        assert phrase in text

    assert "treating coding-agent participation as contamination" in text


def test_metareasoning_allows_reversible_act_to_dominate_separate_inquiry() -> None:
    text = METAREASONING.read_text(encoding="utf-8")

    assert "`ACT` may still dominate" in text
    assert "cheap reversible build" in text
    assert "INQUIRE` does not mean experiment" in text
    assert "experiment-economy-v1.md" in text
    assert "separate inquiry beats acting as the evidence source" in text


def test_using_sensemaking_loads_experiment_economy_only_when_material() -> None:
    text = BOOTSTRAP.read_text(encoding="utf-8")

    assert "Experiment Economy & Proportional Rigor v1" in text
    assert "uncertainty\n!= experiment" in text
    assert "INVESTIGATE\n!= EXPERIMENT" in text
    assert "experiment-economy-v1.md" in text
    assert (
        "when experimentation, experimental\nisolation, fresh-agent setup, or "
        "contamination control is materially under\nconsideration"
    ) in text


def test_strategic_analysis_requires_cheapest_sufficient_evidence_before_experiment() -> None:
    skill = STRATEGIC_SKILL.read_text(encoding="utf-8")
    contract = STRATEGIC_CONTRACT.read_text(encoding="utf-8")

    assert "INVESTIGATE` does not imply an experiment" in skill
    assert "experiment-economy-v1.md" in skill
    assert "plausible experimental outcomes" in skill
    assert "INVESTIGATE != EXPERIMENT" in contract
    assert "research-grade evidence != default product-development evidence" in contract
    assert "Cheap reversible construction may be the evidence-producing action" in contract


def test_policy_hierarchy_preserves_non_experiment_default() -> None:
    text = POLICY.read_text(encoding="utf-8")

    assert "Inquiry does not privilege experimentation" in text
    assert "INVESTIGATE != EXPERIMENT" in text
    assert "experiment possible != experiment warranted" in text
    assert "cheap reversible `ACT` still" in text


def test_experiment_economy_adds_no_runtime_or_scoring_authority() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    reference = ECONOMY.read_text(encoding="utf-8")

    for forbidden in (
        "ExperimentEngine",
        "ExperimentRouter",
        "EvidenceGradeSelector",
    ):
        assert forbidden not in pyproject

    assert "not an engine, scorer, router, or experiment framework" in reference
    assert "must not calculate whether an experiment is strategically warranted" in reference
