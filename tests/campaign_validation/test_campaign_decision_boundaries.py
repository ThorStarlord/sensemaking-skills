"""Focused P5 contract-regression tests discovered during bounded review."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import Authority, CampaignState, Responsibility
from sensemaking_skills.campaigns import (
    AdvanceDecision,
    CampaignDecisionService,
    CampaignService,
    CampaignTransactionError,
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


def test_advance_rejects_trigger_evidence_omitted_from_transition_record(tmp_path):
    workspace = tmp_path / "campaign"
    service = CampaignService(workspace)
    service.initialize(
        CampaignState(
            campaign_id="CMP-P5-EVIDENCE-BINDING",
            mission="bind responsibility trigger evidence to its advance decision",
            status="active",
            current_state="initialized",
        )
    )
    evidence = service.store.workspace.evidence_dir / "brief.md"
    evidence.write_text("durable trigger evidence", encoding="utf-8")

    with pytest.raises(CampaignTransactionError, match="recorded on the advance transition"):
        CampaignDecisionService(workspace).advance(
            AdvanceDecision(
                transition_id="TR-P5-UNBOUND-EVIDENCE",
                to_state="bounded_work",
                decision="this decision record is mechanically incomplete",
                evidence=(),
                next_responsibility=Responsibility(
                    id="R-P5-EVIDENCE",
                    statement="perform work triggered by durable evidence",
                    trigger_evidence=("evidence/brief.md",),
                    decision_blocked="whether the triggered work is complete",
                    scope="P5 evidence-binding proof",
                    authority=Authority.AUTHORIZED_AUTONOMOUSLY,
                    success_conditions=("trigger evidence is auditable",),
                ),
            )
        )

    fresh = CampaignService(workspace).resume()
    assert fresh.state.current_state == "initialized"
    assert fresh.transitions == ()
