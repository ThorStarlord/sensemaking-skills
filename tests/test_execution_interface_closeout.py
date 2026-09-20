"""Currentness checks for Execution Interface & Agent-Factorization v1 closeout."""

from __future__ import annotations

from pathlib import Path

import tomllib
import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_execution_interface_v1_handoff_covers_all_owner_directed_packages() -> None:
    handoff = (
        ROOT / "docs" / "execution-interface-agent-factorization-v1-handoff.md"
    ).read_text(encoding="utf-8")

    for pr in ("#387", "#388", "#389", "#390", "#391", "#392"):
        assert pr in handoff
    for run_id in ("35408048842", "35408048855", "35408048919"):
        assert run_id in handoff

    assert "Campaign schema v3" in handoff
    assert "worker success != global closure" in handoff
    assert "precedence projection != execution plan" in handoff
    assert "NEXT MODE = NORMAL_USE_VALIDATION" in handoff
    assert "Issue #393" in handoff
    assert "Issue #384" in handoff


def test_status_preserves_execution_interface_closeout_without_freezing_rc3() -> None:
    status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    contract = yaml.safe_load((ROOT / "release-v1.0.yaml").read_text(encoding="utf-8"))

    assert pyproject["project"]["version"] == "1.0.0rc3.dev0"
    assert contract["release"]["version"] == "1.0.0rc3"
    assert contract["release"]["status"] == "development"
    assert "Execution Interface & Agent-Factorization v1 — COMPLETE" in status
    assert "NORMAL_USE_VALIDATION" in status
    assert "EXECUTION_INTERFACE_V1_CLOSEOUT" not in status
    assert "Policy Hierarchy Completion v0" in status
    assert "PRIMARY CONSTRUCTION PROGRAM = POLICY_HIERARCHY_COMPLETION_V0" in status
    assert "POST_RC2_DEVELOPMENT_ACTIVE" not in status
    assert "Do **not** freeze RC3" in status


def test_strategic_candidate_reservoir_marks_new_baselines_as_implemented() -> None:
    candidates = (ROOT / "docs" / "strategic-candidate-directions.md").read_text(
        encoding="utf-8"
    )

    publication = candidates.split(
        "### 10.1 GitHub-native Campaign provenance publication", 1
    )[1].split("### 10.2", 1)[0]
    assert "IMPLEMENTED_BASELINE" in publication
    assert "preview-by-default" in publication
    assert "--publish" in publication

    bridge = candidates.split(
        "### 10.4 External execution interchange / AI Software Factory bridge", 1
    )[1].split("## 11.", 1)[0]
    assert "IMPLEMENTED_BASELINE" in bridge
    assert "worker success != global closure" in bridge
    assert "factory bridge != factory runtime" in bridge

    multi = candidates.split(
        "### 6.1 Target sets and explicit cross-repository relationships", 1
    )[1].split("### 6.2", 1)[0]
    assert "multi-target execution-view" in multi
    assert "precedence projection != execution plan" in multi


def test_changelog_records_post_rc2_execution_interface_capabilities() -> None:
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    rc3 = changelog.split("## [1.0.0-rc.3] - UNRELEASED", 1)[1].split(
        "## [1.0.0-rc.2]", 1
    )[0]

    for phrase in (
        "Release Authority Auditor",
        "Execution Interface v1",
        "External executor interchange",
        "Explicit GitHub provenance publication",
        "Cross-repository execution projection",
        "Execution Interface & Agent-Factorization v1 closeout",
    ):
        assert phrase in rc3
