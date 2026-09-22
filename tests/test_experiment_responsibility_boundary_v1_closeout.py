"""Terminal qualification checks for Issue #441 Experiment Responsibility Boundary v1."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "STATUS.md"
HANDOFF = ROOT / "docs" / "experiment-responsibility-boundary-v1-handoff.md"
BOUNDARY = ROOT / "docs" / "experiment-responsibility-boundary-v1.md"
EXPERIMENT_DESIGN = ROOT / "skills" / "experiment-design" / "SKILL.md"
EXPERIMENT_CONTRACT = (
    ROOT / "skills" / "experiment-design" / "references" / "contract.md"
)


def test_handoff_records_exact_feature_qualification_and_merge() -> None:
    text = HANDOFF.read_text(encoding="utf-8")

    for value in (
        "#441",
        "#442",
        "005aa2d41e7dd89d1af186473c8cc3e18845385f",
        "7d15024226022bdd47a82da99241c7989a8e3f4d",
        "35548589418",
        "35548589414",
        "35548589416",
    ):
        assert value in text

    assert "zero file differences" in text
    assert "COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF" in text
    assert "does **not** establish" in text
    assert "not a validation experiment" in text


def test_status_returns_to_normal_use_after_issue_441() -> None:
    status = STATUS.read_text(encoding="utf-8")

    assert "Experiment Responsibility Boundary v1 — COMPLETE / INTEGRATED / NORMAL_USE_HANDOFF" in status
    assert (
        "Issue #438 Experiment Economy & Proportional Rigor v1 "
        "is complete/integrated and in normal-use handoff"
    ) in status
    assert (
        "ISSUE_441_EXPERIMENT_RESPONSIBILITY_BOUNDARY_V1 "
        "= COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF"
    ) in status
    assert (
        "ISSUE_438_EXPERIMENT_ECONOMY_PROPORTIONAL_RIGOR_V1 "
        "= COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF"
    ) in status
    assert "EXPERIMENT PREREQUISITE = NONE" in status
    assert "SYNTHETIC_STRATEGICPLANNER_TESTING = STOPPED" in status
    assert "NO ACTIVE ISSUE #441 CONSTRUCTION PACKAGE" in status


def test_terminal_boundary_preserves_warrant_ownership_and_v1_compatibility() -> None:
    boundary = BOUNDARY.read_text(encoding="utf-8")
    skill = EXPERIMENT_DESIGN.read_text(encoding="utf-8")
    contract = EXPERIMENT_CONTRACT.read_text(encoding="utf-8")

    assert "diagnostic uncertainty\n!= experimentation responsibility" in boundary
    assert "experiment-design\n!= experiment-warrant selector" in skill
    assert 'experiment_plan schema_version: "2"' in skill
    assert 'Historical `schema_version: "1"` plans remain valid' in contract
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
