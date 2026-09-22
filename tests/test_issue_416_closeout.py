"""Terminal currentness checks for Issue #416 strategic construction closeout."""

from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs" / "strategic-continuity-reconciliation-multi-repository-v1-handoff.md"


def test_issue_416_handoff_records_all_qualified_package_receipts() -> None:
    text = HANDOFF.read_text(encoding="utf-8")

    for pr in ("#417", "#420", "#422", "#424"):
        assert pr in text

    for run_id in (
        "35489999196",
        "35489999194",
        "35490477569",
        "35490477546",
        "35492229134",
        "35492229187",
        "35492405535",
        "35492405571",
    ):
        assert run_id in text

    for merge_sha in (
        "4ff09d71948bd967e2d7bb02855628fc71f7bd56",
        "37f0c180af4dc4b741e490ba4e4c54980109a13f",
        "08787aaff58c671edaf4ee7109659d8443ea7e45",
        "6afe8ce1eb8642ed412fa12f49e3bf116861ced0",
    ):
        assert merge_sha in text

    assert "NO_CHANGE / NORMAL_USE_HANDOFF" in text
    assert "Campaign schema v3" in text
    assert "automatic repository discovery or scope expansion" in text
    assert "StrategicPlanner v0" in text


def test_status_is_terminal_for_issue_416_and_preserves_prior_baselines() -> None:
    status = (ROOT / "STATUS.md").read_text(encoding="utf-8")

    assert "Issue #416" in status
    assert "Strategic Continuity, Reconciliation & Multi-Repository Sensemaking v1 — COMPLETE / INTEGRATED / NORMAL_USE_HANDOFF" in status
    assert (
        "ISSUE_416_STRATEGIC_CONTINUITY_RECONCILIATION_MULTI_REPO_V1 = "
        "COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF"
    ) in status
    assert "STRATEGY_VIEWER_CLI = IMPLEMENTED" in status
    assert "STRATEGIC_REPOSITORY_SENSEMAKING_V1 = COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF" in status
    assert "POLICY_HIERARCHY_COMPLETION_V0 = COMPLETE_INTEGRATED_COMPOSABLE" in status
    assert "SYNTHETIC STRATEGICPLANNER TESTING = STOPPED" in status
    assert "Issue #384" in status


def test_candidate_directions_reconcile_issue_416_surfaces_as_implemented() -> None:
    text = (ROOT / "docs" / "strategic-candidate-directions.md").read_text(encoding="utf-8")

    multi = text.split("### 6.4 Multi-Repository Strategic Sensemaking v1", 1)[1].split(
        "## 7.", 1
    )[0]
    continuity = text.split(
        "### 9.5 Strategic Continuity, Reconciliation, and Reserved Decisions v1", 1
    )[1].split("## 10.", 1)[0]
    impact = text.split("### 10.5 Change-Impact Sensemaking v1", 1)[1].split(
        "## 11.", 1
    )[0]

    for section in (multi, continuity, impact):
        assert "IMPLEMENTED_BASELINE" in section

    assert "automatic discovery" in multi
    assert "drift detected != strategy invalid" in continuity
    assert "follow-up responsibility != backlog item" in impact


def test_release_inventory_contains_all_issue_416_skills_without_runtime_planner() -> None:
    release = yaml.safe_load((ROOT / "release-v1.0.yaml").read_text(encoding="utf-8"))
    supported = set(release["skill_inventory"]["supported"])

    expected = {
        "strategic-repository-analysis",
        "strategic-repository-reconciliation",
        "owner-decision-capsule",
        "thesis-review-packet",
        "external-evidence-packet",
        "multi-repository-strategic-analysis",
        "change-impact-analysis",
    }
    assert expected <= supported

    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "StrategicPlanner" not in pyproject
    assert "OuterLoopEngine" not in pyproject


def test_terminal_handoff_does_not_claim_release_or_external_admin_authority() -> None:
    handoff = HANDOFF.read_text(encoding="utf-8")

    assert "Issue #384 remains a separate GitHub-hosting/admin" in handoff
    assert "freeze RC3" in handoff
    assert "publish a package" in handoff
    assert "final `1.0.0`" in handoff
