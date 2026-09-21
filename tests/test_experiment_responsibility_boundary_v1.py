"""Contract checks for Experiment Responsibility Boundary v1.

These checks verify responsibility ownership and experiment-plan representation.
They do not establish that a particular experiment is semantically warranted,
optimal, or worth running.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOUNDARY = ROOT / "docs" / "experiment-responsibility-boundary-v1.md"
USING = ROOT / "skills" / "using-sensemaking" / "SKILL.md"
ECONOMY = (
    ROOT / "skills" / "using-sensemaking" / "references" / "experiment-economy-v1.md"
)
REPO_SENSEMAKER = ROOT / "skills" / "repo-sensemaker" / "SKILL.md"
DISCOVERY = ROOT / "skills" / "discovery" / "SKILL.md"
HYPOTHESIS = ROOT / "skills" / "hypothesis" / "SKILL.md"
LEAN_CANVAS = ROOT / "skills" / "lean-canvas" / "SKILL.md"
PRICING = ROOT / "skills" / "pricing" / "SKILL.md"
EXPERIMENT_DESIGN = ROOT / "skills" / "experiment-design" / "SKILL.md"
EXPERIMENT_CONTRACT = (
    ROOT / "skills" / "experiment-design" / "references" / "contract.md"
)
AB_ANALYSIS = ROOT / "skills" / "ab-test-analysis" / "SKILL.md"
USAGE_RESEARCHER = ROOT / "skills" / "usage-researcher" / "SKILL.md"
PM_DOMAIN = ROOT / "docs" / "product-management" / "domain-model.md"
PM_ARTIFACTS = ROOT / "docs" / "product-management" / "artifact-contracts.md"
CAPABILITY_REGISTRY = (
    ROOT / "src" / "sensemaking_skills" / "defaults" / "capability-registry.yaml"
)


def test_boundary_separates_diagnostic_inquiry_and_experiment_design_roles() -> None:
    text = BOUNDARY.read_text(encoding="utf-8")

    for phrase in (
        "diagnostic Skill",
        "do not manufacture experimentation responsibility",
        "Inquiry Policy / Experiment Economy",
        "experiment-design",
        "decision discrimination",
        "Experimental quality",
        "Experimental efficiency",
        "diagnostic uncertainty\n!= experimentation responsibility",
    ):
        assert phrase in text

    assert "Historical `experiment_plan schema_version: \"1\"` remains valid" in text
    assert "Canonical new plans use `schema_version: \"2\"`" in text


def test_diagnostic_skills_do_not_promote_missing_evidence_directly_to_experiment() -> None:
    repo = REPO_SENSEMAKER.read_text(encoding="utf-8")
    discovery = DISCOVERY.read_text(encoding="utf-8")
    hypothesis = HYPOTHESIS.read_text(encoding="utf-8")
    lean = LEAN_CANVAS.read_text(encoding="utf-8")
    pricing = PRICING.read_text(encoding="utf-8")

    assert "diagnostic recommendation != experimentation responsibility" in repo
    assert "apply Experiment Economy before" in repo
    assert "formulate a bounded probe and recommend" not in repo

    assert "uncertainty != experiment" in discovery
    assert "experiment-economy-v1.md" in discovery

    assert "hypothesis != experiment warrant" in hypothesis
    assert "experiment-economy-v1.md" in hypothesis

    assert "critical assumption != experiment requirement" in lean
    assert "experiment-economy-v1.md" in lean

    assert "high-risk assumption != experiment requirement" in pricing
    assert "Populate experiment proposals only when Experiment Economy establishes" in pricing


def test_experiment_design_consumes_warrant_instead_of_manufacturing_it() -> None:
    skill = EXPERIMENT_DESIGN.read_text(encoding="utf-8")
    contract = EXPERIMENT_CONTRACT.read_text(encoding="utf-8")

    for phrase in (
        "experiment-design\n!= experiment-warrant selector",
        "do **not** manufacture the warrant",
        "cheaper evidence sources considered",
        "decision discrimination",
        "total experiment cost",
        "Minimum Sufficient Experimental Rigor",
        'experiment_plan schema_version: "2"',
    ):
        assert phrase in skill

    assert "return control rather than manufacturing an" in contract
    assert "decision_to_support" in contract
    assert "decision_changing_uncertainty" in contract
    assert "cheaper_evidence_sources_considered" in contract
    assert "decision_branches" in contract
    assert "total_experiment_cost" in contract
    assert "minimum_required_controls" in contract
    assert "controls_rejected_as_unnecessary" in contract
    assert "claim_ceiling" in contract


def test_experiment_analysis_and_usage_research_do_not_self_authorize_more_research() -> None:
    ab = AB_ANALYSIS.read_text(encoding="utf-8")
    usage = USAGE_RESEARCHER.read_text(encoding="utf-8")

    assert "extend recommendation != experiment warrant" in ab
    assert "investigate recommendation != experiment warrant" in ab
    assert "continuation experiment must pass Experiment Economy again" in ab

    assert "usage-researcher\n!= usage-research warrant selector" in usage
    assert "Existing run logs or\nnormal-use evidence may be cheaper and sufficient" in usage


def test_control_loop_retains_experiment_warrant_before_capability_selection() -> None:
    using = USING.read_text(encoding="utf-8")
    economy = ECONOMY.read_text(encoding="utf-8")

    assert "diagnostic recommendation\n!= experimentation responsibility" in using
    assert "experiment warrant\n-> then experiment-design" in using
    assert "Do not select `experiment-design` merely because" in using

    assert "diagnostic uncertainty\n!= experiment warrant" in economy
    assert "experiment-design\n= downstream of experiment warrant" in economy


def test_pm_contract_and_registry_expose_v2_without_runtime_authority() -> None:
    domain = PM_DOMAIN.read_text(encoding="utf-8")
    artifacts = PM_ARTIFACTS.read_text(encoding="utf-8")
    registry = CAPABILITY_REGISTRY.read_text(encoding="utf-8")
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert "experiment-design consumes experiment warrant" in domain
    assert "experiment-analysis continuation recommendation\n!= fresh experiment warrant" in domain

    assert 'schema_version: "1"' in artifacts
    assert 'schema_version: "2"' in artifacts
    assert "qualitative total experiment cost" in artifacts
    assert "direct duplicate decision effects" in artifacts

    assert "experiment warrant must already exist" in registry
    assert "decision discrimination, proportional rigor" in registry

    for forbidden in (
        "ExperimentEngine",
        "ExperimentRouter",
        "ValueOfInformationScore",
        "ExperimentWarrantSelector",
    ):
        assert forbidden not in pyproject
