"""P3 integration tests for the durable campaign CLI."""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import replace

import pytest
from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import TransitionRecord
from sensemaking_skills.campaigns import CampaignService, CampaignStore
from sensemaking_skills.cli import (
    CAMPAIGN_INVALID_EXIT,
    CAMPAIGN_WORKSPACE_EXIT,
    cli,
)


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def _init_args(workspace, *, json_output: bool = False):
    args = [
        "campaign",
        "init",
        "--workspace",
        str(workspace),
        "--campaign-id",
        "CMP-CLI-1",
        "--mission",
        "Preserve explicit agent-authored campaign decisions",
    ]
    if json_output:
        args.append("--json")
    return args


def test_campaign_init_status_validate_and_empty_history_json(runner, tmp_path):
    workspace = tmp_path / "campaign"

    created = runner.invoke(cli, _init_args(workspace, json_output=True))
    assert created.exit_code == 0, created.output
    created_payload = json.loads(created.output)
    assert created_payload["code"] == "CAMPAIGN_INITIALIZED"
    assert created_payload["campaign_id"] == "CMP-CLI-1"
    assert created_payload["current_state"] == "initialized"
    assert created_payload["transition_count"] == 0

    status = runner.invoke(
        cli, ["campaign", "status", "--workspace", str(workspace), "--json"]
    )
    assert status.exit_code == 0, status.output
    status_payload = json.loads(status.output)
    assert status_payload["code"] == "CAMPAIGN_STATUS"
    assert status_payload["campaign_id"] == "CMP-CLI-1"
    assert status_payload["active_responsibility"] is None

    validation = runner.invoke(
        cli, ["campaign", "validate", "--workspace", str(workspace), "--json"]
    )
    assert validation.exit_code == 0, validation.output
    validation_payload = json.loads(validation.output)
    assert validation_payload == {
        "code": "CAMPAIGN_VALID",
        "diagnostics": [],
        "ok": True,
        "valid": True,
    }

    history = runner.invoke(
        cli, ["campaign", "history", "--workspace", str(workspace), "--json"]
    )
    assert history.exit_code == 0, history.output
    history_payload = json.loads(history.output)
    assert history_payload["code"] == "CAMPAIGN_HISTORY"
    assert history_payload["initial_state"] == "initialized"
    assert history_payload["transitions"] == []


def test_campaign_history_uses_trace_defined_service_order(runner, tmp_path):
    workspace = tmp_path / "campaign"
    assert runner.invoke(cli, _init_args(workspace)).exit_code == 0

    service = CampaignService(workspace)
    current = service.resume().state
    next_state = replace(current, current_state="review")
    transition = TransitionRecord(
        id="T-10",
        from_state="initialized",
        to_state="review",
        evidence=(),
        decision="agent-authored decision to enter review",
        authority=None,
    )
    service.record_transition(new_state=next_state, transition=transition)

    history = runner.invoke(
        cli, ["campaign", "history", "--workspace", str(workspace), "--json"]
    )
    assert history.exit_code == 0, history.output
    payload = json.loads(history.output)
    assert payload["transition_count"] == 1
    assert payload["transitions"][0]["id"] == "T-10"
    assert payload["transitions"][0]["decision"] == (
        "agent-authored decision to enter review"
    )


def test_campaign_validate_returns_stable_invalid_exit_for_untraced_record(
    runner, tmp_path
):
    workspace = tmp_path / "campaign"
    assert runner.invoke(cli, _init_args(workspace)).exit_code == 0

    CampaignStore(workspace).append_transition(
        TransitionRecord(
            id="T-UNTRACED",
            from_state="initialized",
            to_state="ghost",
            evidence=(),
            decision="manual corruption",
            authority=None,
        )
    )

    result = runner.invoke(
        cli, ["campaign", "validate", "--workspace", str(workspace), "--json"]
    )
    assert result.exit_code == CAMPAIGN_INVALID_EXIT
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_INVALID"
    assert payload["valid"] is False
    assert "UNTRACED_TRANSITION" in {
        diagnostic["code"] for diagnostic in payload["diagnostics"]
    }


def test_campaign_status_maps_contract_corruption_to_integrity_error(runner, tmp_path):
    workspace = tmp_path / "campaign"
    assert runner.invoke(cli, _init_args(workspace)).exit_code == 0
    state_path = workspace / "campaign-state.yaml"
    state_path.write_text(
        state_path.read_text(encoding="utf-8") + "unknown_field: true\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        cli, ["campaign", "status", "--workspace", str(workspace), "--json"]
    )
    assert result.exit_code == CAMPAIGN_INVALID_EXIT
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_INTEGRITY_ERROR"
    assert payload["ok"] is False


def test_campaign_init_existing_workspace_has_stable_workspace_exit(runner, tmp_path):
    workspace = tmp_path / "campaign"
    assert runner.invoke(cli, _init_args(workspace)).exit_code == 0

    result = runner.invoke(cli, _init_args(workspace, json_output=True))
    assert result.exit_code == CAMPAIGN_WORKSPACE_EXIT
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_ALREADY_EXISTS"


def test_campaign_init_refuses_workspace_inside_target_repository(runner, tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    workspace = target / "campaign"
    args = [
        *_init_args(workspace, json_output=True),
        "--target-repo",
        str(target),
    ]

    result = runner.invoke(cli, args)
    assert result.exit_code == CAMPAIGN_WORKSPACE_EXIT
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_WORKSPACE_ERROR"
    assert not workspace.exists()


def test_campaign_status_reports_state_without_semantic_recommendation(runner, tmp_path):
    workspace = tmp_path / "campaign"
    assert runner.invoke(cli, _init_args(workspace)).exit_code == 0

    result = runner.invoke(cli, ["campaign", "status", "--workspace", str(workspace)])
    assert result.exit_code == 0
    lowered = result.output.lower()
    assert "campaign_status" in lowered
    assert "suggested next" not in lowered
    assert "should do next" not in lowered


def test_campaign_cli_survives_fresh_process_boundary(tmp_path):
    workspace = tmp_path / "campaign"
    base = [sys.executable, "-m", "sensemaking_skills.cli", "campaign"]

    init = subprocess.run(
        [
            *base,
            "init",
            "--workspace",
            str(workspace),
            "--campaign-id",
            "CMP-SUBPROCESS",
            "--mission",
            "Prove durable fresh-process reconstruction",
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert init.returncode == 0, init.stderr or init.stdout
    assert json.loads(init.stdout)["code"] == "CAMPAIGN_INITIALIZED"

    status = subprocess.run(
        [*base, "status", "--workspace", str(workspace), "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert status.returncode == 0, status.stderr or status.stdout
    status_payload = json.loads(status.stdout)
    assert status_payload["campaign_id"] == "CMP-SUBPROCESS"
    assert status_payload["current_state"] == "initialized"

    validation = subprocess.run(
        [*base, "validate", "--workspace", str(workspace), "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert validation.returncode == 0, validation.stderr or validation.stdout
    assert json.loads(validation.stdout)["code"] == "CAMPAIGN_VALID"

    history = subprocess.run(
        [*base, "history", "--workspace", str(workspace), "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert history.returncode == 0, history.stderr or history.stdout
    history_payload = json.loads(history.stdout)
    assert history_payload["campaign_id"] == "CMP-SUBPROCESS"
    assert history_payload["transition_count"] == 0
