"""Contract checks for Experiment Responsibility Boundary v1.

These checks verify responsibility ownership and experiment-plan representation.
They do not establish that a particular experiment is semantically warranted,
optimal, or worth running.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOUNDARY = ROOT / "docs" / "experiment-responsibility-boundary-v1.md"
DISCOVERY = ROOT / "skills" / "discovery" / "SKILL.md"
HYPOTHESIS = ROOT / "skills" / "hypothesis" / "SKILL.md"
LEAN_CANVAS = ROOT / "skills" / "lean-canvas" / "SKILL.md"
EXPERIMENT_DESIGN = ROOT / "skills" / "experiment-design" / "SKILL.md"
EXPERIMENT_CONTRACT = (
    ROOT / "skills" / "experiment-design" / "references" / "contract.md"
)
PM_ARTIFACTS = ROOT / "docs" / "product-management" / "artifact-contracts.md"
CAPABILITY_REGISTRY = (
    ROOT / "src" / "sensemaking_skills" / "defaults" / "capability-registry.yaml"
)


def test_boundary_names_experiment_design_skill() -> None:
    text = BOUNDARY.read_text(encoding="utf-8")

    assert "experiment-design" in text


def test_diagnostic_skills_link_experiment_economy_reference() -> None:
    discovery = DISCOVERY.read_text(encoding="utf-8")
    hypothesis = HYPOTHESIS.read_text(encoding="utf-8")
    lean = LEAN_CANVAS.read_text(encoding="utf-8")

    assert "experiment-economy-v1.md" in discovery
    assert "experiment-economy-v1.md" in hypothesis
    assert "experiment-economy-v1.md" in lean


def test_experiment_design_names_v2_plan_contract_fields() -> None:
    skill = EXPERIMENT_DESIGN.read_text(encoding="utf-8")
    contract = EXPERIMENT_CONTRACT.read_text(encoding="utf-8")

    assert 'experiment_plan schema_version: "2"' in skill

    assert "decision_to_support" in contract
    assert "decision_changing_uncertainty" in contract
    assert "cheaper_evidence_sources_considered" in contract
    assert "decision_branches" in contract
    assert "total_experiment_cost" in contract
    assert "minimum_required_controls" in contract
    assert "controls_rejected_as_unnecessary" in contract
    assert "claim_ceiling" in contract


def test_pm_contract_and_registry_expose_v2_without_runtime_authority() -> None:
    artifacts = PM_ARTIFACTS.read_text(encoding="utf-8")
    registry = CAPABILITY_REGISTRY.read_text(encoding="utf-8")
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert 'schema_version: "1"' in artifacts
    assert 'schema_version: "2"' in artifacts

    assert "experiment warrant must already exist" in registry
    assert "decision discrimination, proportional rigor" in registry

    for forbidden in (
        "ExperimentEngine",
        "ExperimentRouter",
        "ValueOfInformationScore",
        "ExperimentWarrantSelector",
    ):
        assert forbidden not in pyproject
