"""Terminal currentness checks for Strategic Repository Sensemaking v1."""

from __future__ import annotations

from pathlib import Path

import tomllib
import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_handoff_records_qualified_functional_packages_and_later_integrations() -> None:
    handoff = (ROOT / "docs" / "strategic-repository-sensemaking-v1-handoff.md").read_text(
        encoding="utf-8"
    )

    for pr in ("#403", "#404", "#409", "#411"):
        assert pr in handoff

    for run_id in (
        "35481010243",
        "35481010191",
        "35481081176",
        "35481081179",
        "35481237943",
        "35481237897",
        "35481312550",
        "35481312659",
    ):
        assert run_id in handoff

    assert "no synthetic/model-comparison experiment was required or performed" in handoff
    assert "construction path\n!= feature list" in handoff
    assert "candidate responsibility\n!= implementation authorization" in handoff
    assert "does not promote StrategicPlanner v0" in handoff
    assert "Policy Hierarchy Completion v0 is complete/integrated/composable" in handoff


def test_candidate_reservoir_marks_strategic_repository_sensemaking_implemented() -> None:
    text = (ROOT / "docs" / "strategic-candidate-directions.md").read_text(
        encoding="utf-8"
    )
    section = text.split("### 9.4 Strategic Repository Sensemaking v1", 1)[1].split(
        "## 10.", 1
    )[0]

    assert "IMPLEMENTED_BASELINE" in section
    assert "strategic-repository-analysis" in section
    assert "strategic_repository_analysis" in section
    assert "0–5 materially real construction paths" in section
    assert "construction path != backlog" in section
    assert "path comparison != numeric ranking" in section
    assert "does not promote StrategicPlanner v0" in section


def test_current_public_surface_and_changelog_record_the_capability() -> None:
    public = (ROOT / "docs" / "public-surface-v1.0.md").read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    assert "strategic-repository-analysis" in public
    assert "strategic_repository_analysis" in public
    assert "strategic analysis != implementation authorization" in public
    assert "Skill is a semantic-agent capability, not a CLI planner" in public

    rc3 = changelog.split("## [1.0.0-rc.3] - UNRELEASED", 1)[1].split(
        "## [1.0.0-rc.2]", 1
    )[0]
    assert "Strategic Repository Sensemaking v1" in rc3
    assert "Repository evolution routing" in rc3
    assert "deterministic path ranking" in rc3
    assert "Adaptive Policy Coordinator" in rc3


def test_status_is_terminal_for_issue_401_and_preserves_completed_policy_hierarchy() -> None:
    status = (ROOT / "STATUS.md").read_text(encoding="utf-8")

    assert "Strategic Repository Sensemaking v1 — COMPLETE / INTEGRATED / NORMAL_USE_HANDOFF" in status
    assert "CURRENT CONSTRUCTION RESPONSIBILITY = NONE" in status
    assert "PRIMARY CONSTRUCTION PROGRAM = NONE" in status
    assert "OPERATING MODE = NORMAL_USE_VALIDATION" in status
    assert "STRATEGIC_REPOSITORY_SENSEMAKING_V1 = COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF" in status
    assert "POLICY_HIERARCHY_COMPLETION_V0 = COMPLETE_INTEGRATED_COMPOSABLE" in status
    assert "SUPPORTING EVIDENCE MODE = NORMAL_USE_VALIDATION" in status
    assert "EXPERIMENT PREREQUISITE = NONE" in status
    assert "SYNTHETIC STRATEGICPLANNER TESTING = STOPPED" in status
    assert "Adaptive Policy Coordinator v0" in status
    assert "Policy Hierarchy Completion v0 is complete/integrated/composable" in status
    assert "CURRENT CONSTRUCTION RESPONSIBILITY = STRATEGIC_PATH_SYNTHESIS_INTEGRATION" not in status
    assert "QUALIFY AND INTEGRATE THE TERMINAL STRATEGIC REPOSITORY SENSEMAKING V1 CLOSEOUT" not in status


def test_release_remains_rc3_development_and_no_runtime_planner_is_promoted() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    release_text = (ROOT / "release-v1.0.yaml").read_text(encoding="utf-8")
    release = yaml.safe_load(release_text)

    assert pyproject["project"]["version"] == "1.0.0rc3.dev0"
    assert release["release"]["version"] == "1.0.0rc3"
    assert release["release"]["status"] == "development"
    assert 'schema_version: "2"' in release_text
    assert "StrategicPlanner" not in (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "OuterLoopEngine" not in (ROOT / "pyproject.toml").read_text(encoding="utf-8")


def test_closeout_does_not_reopen_or_extend_policy_hierarchy() -> None:
    status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
    handoff = (ROOT / "docs" / "strategic-repository-sensemaking-v1-handoff.md").read_text(
        encoding="utf-8"
    )

    assert "No additional Issue #399 construction package is selected by this closeout." in handoff
    assert "Policy Hierarchy Completion v0 is complete/integrated/composable" in handoff
    assert "Policy Hierarchy Completion v0 is complete/integrated/composable" in status
    assert "this closeout does not reopen or extend it" in status
