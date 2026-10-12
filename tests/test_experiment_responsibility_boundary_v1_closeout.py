"""Terminal qualification checks for Issue #441 Experiment Responsibility Boundary v1."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_DESIGN = ROOT / "skills" / "experiment-design" / "SKILL.md"
EXPERIMENT_CONTRACT = (
    ROOT / "skills" / "experiment-design" / "references" / "contract.md"
)


def test_terminal_boundary_preserves_v2_plan_contract_fields() -> None:
    skill = EXPERIMENT_DESIGN.read_text(encoding="utf-8")
    contract = EXPERIMENT_CONTRACT.read_text(encoding="utf-8")

    assert 'experiment_plan schema_version: "2"' in skill
    assert 'schema_version: "2"' in contract
    assert "decision_branches" in contract
    assert "total_experiment_cost" in contract


def test_closeout_adds_no_experiment_runtime_or_scoring_surface() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    for forbidden in (
        "ExperimentEngine",
        "ExperimentRouter",
        "ValueOfInformationScore",
        "ExperimentWarrantSelector",
    ):
        assert forbidden not in pyproject
