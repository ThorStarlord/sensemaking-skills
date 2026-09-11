"""Hermetic qualification for Campaign completion receipts and archive markers."""

from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import CampaignState
from sensemaking_skills.campaigns import CampaignService
from sensemaking_skills.cli import cli


def _campaign(root: Path, campaign_id: str) -> Path:
    workspace = root / campaign_id
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id=campaign_id,
            mission="finish and preserve a bounded Campaign",
            status="active",
            current_state="scoped",
        )
    )
    return workspace


def _close(runner: CliRunner, workspace: Path, terminal_state: str = "no_further_work_warranted"):
    return runner.invoke(
        cli,
        [
            "campaign", "close",
            "--workspace", str(workspace),
            "--transition-id", "T-CLOSE",
            "--to-state", "closed",
            "--decision", "caller explicitly closes this Campaign",
            "--terminal-state", terminal_state,
            "--json",
        ],
    )


def test_closeout_requires_existing_terminal_decision_and_is_recalculable(tmp_path: Path) -> None:
    workspace = _campaign(tmp_path, "CMP-CLOSEOUT")
    runner = CliRunner()

    premature = runner.invoke(cli, ["campaign", "closeout", "--workspace", str(workspace), "--json"])
    assert premature.exit_code != 0
    assert "already-terminal Campaign" in premature.output

    closed = _close(runner, workspace)
    assert closed.exit_code == 0, closed.output
    recorded = runner.invoke(cli, ["campaign", "closeout", "--workspace", str(workspace), "--json"])
    assert recorded.exit_code == 0, recorded.output
    payload = json.loads(recorded.output)
    receipt = payload["receipt"]
    assert receipt["terminal_state"] == "no_further_work_warranted"
    assert receipt["semantic_success_established"] is False
    assert receipt["semantic_truth_established"] is False
    assert receipt["final_transition_id"] == "T-CLOSE"
    assert receipt["workspace_manifest_sha256"]
    assert (workspace / "completion-receipt.json").is_file()

    verified = runner.invoke(cli, ["campaign", "completion-receipt", "--workspace", str(workspace), "--json"])
    assert verified.exit_code == 0, verified.output
    assert json.loads(verified.output)["ok"] is True

    # Any new durable workspace byte makes the existing receipt stale until an
    # explicit closeout refresh is requested.
    (workspace / "post-close-note.txt").write_text("new durable byte\n", encoding="utf-8")
    stale = runner.invoke(cli, ["campaign", "completion-receipt", "--workspace", str(workspace), "--json"])
    assert stale.exit_code == 3, stale.output
    assert "COMPLETION_RECEIPT_CURRENT_STATE_MISMATCH" in stale.output
    refreshed = runner.invoke(cli, ["campaign", "closeout", "--workspace", str(workspace), "--json"])
    assert refreshed.exit_code == 0, refreshed.output


def test_archive_is_nondestructive_and_does_not_mean_success(tmp_path: Path) -> None:
    workspace = _campaign(tmp_path, "CMP-BLOCKED")
    runner = CliRunner()
    assert _close(runner, workspace, "external_blocker").exit_code == 0

    no_receipt = runner.invoke(cli, ["campaign", "archive", "--workspace", str(workspace), "--json"])
    assert no_receipt.exit_code != 0
    assert "valid completion receipt" in no_receipt.output

    assert runner.invoke(cli, ["campaign", "closeout", "--workspace", str(workspace), "--json"]).exit_code == 0
    archived = runner.invoke(cli, ["campaign", "archive", "--workspace", str(workspace), "--json"])
    assert archived.exit_code == 0, archived.output
    payload = json.loads(archived.output)
    assert payload["semantic_success_established"] is False
    assert payload["workspace_moved"] is False
    assert payload["workspace_deleted"] is False
    assert workspace.is_dir()
    assert (workspace / "archive-receipt.json").is_file()
    assert CampaignService(workspace).resume().state.terminal_state.value == "external_blocker"


def test_inventory_hides_archived_by_default_and_can_include_them(tmp_path: Path) -> None:
    active = _campaign(tmp_path, "CMP-ACTIVE")
    archived = _campaign(tmp_path, "CMP-ARCHIVED")
    runner = CliRunner()
    assert _close(runner, archived).exit_code == 0
    assert runner.invoke(cli, ["campaign", "closeout", "--workspace", str(archived), "--json"]).exit_code == 0
    assert runner.invoke(cli, ["campaign", "archive", "--workspace", str(archived), "--json"]).exit_code == 0

    default = runner.invoke(cli, ["campaign", "inventory", "--root", str(tmp_path), "--json"])
    assert default.exit_code == 0, default.output
    default_payload = json.loads(default.output)
    assert [item["campaign_id"] for item in default_payload["entries"]] == ["CMP-ACTIVE"]
    assert default_payload["include_archived"] is False

    included = runner.invoke(cli, ["campaign", "inventory", "--root", str(tmp_path), "--include-archived", "--json"])
    assert included.exit_code == 0, included.output
    included_payload = json.loads(included.output)
    by_id = {item["campaign_id"]: item for item in included_payload["entries"]}
    assert set(by_id) == {"CMP-ACTIVE", "CMP-ARCHIVED"}
    assert by_id["CMP-ARCHIVED"]["archived"] is True
    assert by_id["CMP-ARCHIVED"]["archive_integrity"] == "PASS"
    assert by_id["CMP-ACTIVE"]["archived"] is False
    assert active.is_dir() and archived.is_dir()
