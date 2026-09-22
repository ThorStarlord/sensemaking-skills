"""Terminal qualification checks for Issue #435 semantic grounding refinement."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "STATUS.md"
HANDOFF = ROOT / "docs" / "strategic-repository-analysis-semantic-grounding-v1-handoff.md"
CONTRACT = ROOT / "docs" / "strategic-repository-sensemaking-v1.md"
SKILL = ROOT / "skills" / "strategic-repository-analysis" / "SKILL.md"
TEMPLATE = (
    ROOT
    / "skills"
    / "strategic-repository-analysis"
    / "references"
    / "strategic-repository-analysis-template.md"
)


def test_handoff_records_exact_feature_qualification_and_merge() -> None:
    text = HANDOFF.read_text(encoding="utf-8")
    for value in (
        "#435",
        "#436",
        "9dde64875ed12afdc1fc16b41e043c86435cce74",
        "bcb1d6cae1690463b63389d3d546fbb81f0acb27",
        "35536764090",
        "35536764096",
    ):
        assert value in text
    assert "zero file differences" in text
    assert "COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF" in text
    assert "semantic correctness" in text


def test_status_returns_to_normal_use_after_issue_435() -> None:
    status = STATUS.read_text(encoding="utf-8")
    assert (
        "ISSUE_435_STRATEGIC_REPOSITORY_ANALYSIS_SEMANTIC_GROUNDING_V1 "
        "= COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF"
    ) in status
    assert "EXPERIMENT PREREQUISITE = NONE" in status
    assert "SYNTHETIC STRATEGICPLANNER TESTING = STOPPED" in status


def test_current_contract_exposes_grounding_without_planner_authority() -> None:
    contract = CONTRACT.read_text(encoding="utf-8")
    skill = SKILL.read_text(encoding="utf-8")
    template = TEMPLATE.read_text(encoding="utf-8")

    for phrase in (
        "Strategicity Gate",
        "repository issue exists != strategic frontier",
        "bounded repair != construction path",
        "schema_version: 2",
        "frontier_refs",
        "why_plausible",
        "builds_on_capability_ids",
        "required_capability_ids",
    ):
        assert phrase in contract or phrase in skill or phrase in template

    assert "small intervention\n!= strategically preferable future" in contract
    assert "semantic truth" in contract.lower()
    assert "StrategicPlanner" not in (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "OuterLoopEngine" not in (ROOT / "pyproject.toml").read_text(encoding="utf-8")
