"""Focused P5 contract-regression tests discovered during bounded review."""

from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import Authority, CampaignState, Responsibility
from sensemaking_skills.campaigns import (
    AdvanceDecision,
    CampaignDecisionService,
    CampaignService,
    DeferDecision,
)
from sensemaking_skills.cli import cli


def _initialize_with_active_responsibility(workspace: Path) -> None:
    service = CampaignService(workspace)
    service.initialize(
        CampaignState(
            campaign_id="CMP-P5-BOUNDARY",
            mission="preserve canonical P5 decision semantics",
            status="active",
            current_state="initialized",
        )
    )
    CampaignDecisionService(workspace).advance(
        AdvanceDecision(
            transition_id="TR-P5-BOUNDARY-ADVANCE",
            to_state="bounded_work",
            decision="the agent explicitly selected one bounded responsibility",
            next_responsibility=Responsibility(
                id="R-P5-BOUNDARY",
                statement="exercise the canonical defer contract",
                trigger_evidence=(),
                decision_blocked="whether deferred work can proceed",
                scope="P5 contract boundary only",
                authority=Authority.AUTHORIZED_AUTONOMOUSLY,
                success_conditions=("defer semantics remain canonical",),
            ),
        )
    )


def test_defer_without_reopen_condition_preserves_canonical_optional_semantics(tmp_path):
    workspace = tmp_path / "campaign"
    _initialize_with_active_responsibility(workspace)

    snapshot = CampaignDecisionService(workspace).defer(
        DeferDecision(
            transition_id="TR-P5-BOUNDARY-DEFER",
            to_state="deferred_unknown_reopen",
            decision="defer without inventing an unknown reopening condition",
            reason="no evidence currently establishes a concrete reopen trigger",
        )
    )

    deferred = snapshot.state.deferred_responsibilities[-1]
    assert deferred.responsibility_id == "R-P5-BOUNDARY"
    assert deferred.reason == (
        "no evidence currently establishes a concrete reopen trigger"
    )
    assert deferred.reopen_when == ()
    assert deferred.not_reopened_by == ()
    assert snapshot.state.active_responsibility is None
    assert snapshot.state.authority is None
    assert CampaignService(workspace).validate().valid


def test_defer_json_exposes_exact_replacement_state_and_optional_reopen_contract(tmp_path):
    workspace = tmp_path / "campaign"
    _initialize_with_active_responsibility(workspace)
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "campaign",
            "defer",
            "--workspace",
            str(workspace),
            "--transition-id",
            "TR-P5-BOUNDARY-CLI-DEFER",
            "--to-state",
            "deferred_unknown_reopen",
            "--decision",
            "defer without fabricating a reopening condition",
            "--reason",
            "reopening evidence is not yet known",
            "--json",
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_DEFERRED"
    assert payload["transition"]["id"] == "TR-P5-BOUNDARY-CLI-DEFER"
    assert payload["state"]["current_state"] == "deferred_unknown_reopen"
    deferred = payload["state"]["deferred_responsibilities"][-1]
    assert deferred["responsibility_id"] == "R-P5-BOUNDARY"
    assert deferred["reason"] == "reopening evidence is not yet known"
    assert deferred["reopen_when"] == []
    assert deferred["not_reopened_by"] == []
