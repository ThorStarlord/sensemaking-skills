"""Uncertainty History v0 append-only companion qualification."""

from __future__ import annotations

import json
from dataclasses import replace

from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import CampaignState, TransitionRecord, Uncertainty
from sensemaking_skills.campaigns import CampaignService
from sensemaking_skills.campaigns.uncertainty_history import UncertaintyHistoryService
from sensemaking_skills.cli import cli


def _workspace(tmp_path):
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-UNCERTAINTY-HISTORY",
            mission="preserve uncertainty lifecycle without ranking it",
            status="active",
            current_state="investigate",
            active_uncertainty=Uncertainty(
                id="U-1",
                question="Which bounded fact changes the current decision?",
                consequences=("the next responsibility may change",),
            ),
        )
    )
    return workspace


def test_active_event_must_match_campaign_state_active_uncertainty(tmp_path):
    workspace = _workspace(tmp_path)
    runner = CliRunner()
    rejected = runner.invoke(
        cli,
        [
            "campaign",
            "uncertainty-record",
            "--workspace",
            str(workspace),
            "--event-id",
            "UE-1",
            "--uncertainty-id",
            "U-OTHER",
            "--status",
            "active",
            "--json",
        ],
    )
    assert rejected.exit_code != 0
    assert "does not select active uncertainty" in rejected.output

    accepted = runner.invoke(
        cli,
        [
            "campaign",
            "uncertainty-record",
            "--workspace",
            str(workspace),
            "--event-id",
            "UE-1",
            "--uncertainty-id",
            "U-1",
            "--status",
            "active",
            "--json",
        ],
    )
    assert accepted.exit_code == 0, accepted.output
    payload = json.loads(accepted.output)
    assert payload["campaign_schema_changed"] is False
    assert payload["semantic_recommendation_included"] is False
    assert "rank" in payload["explicit_limit"]


def test_history_preserves_resolution_after_campaign_transition(tmp_path):
    workspace = _workspace(tmp_path)
    service = UncertaintyHistoryService(workspace)
    first_digest = service.append(
        event_id="UE-1",
        uncertainty_id="U-1",
        status="active",
    )

    lifecycle = CampaignService(workspace)
    current = lifecycle.resume().state
    lifecycle.record_transition(
        new_state=replace(current, current_state="resolved", active_uncertainty=None),
        transition=TransitionRecord(
            id="T-RESOLVE",
            from_state="investigate",
            to_state="resolved",
            evidence=(),
            decision="record uncertainty resolution",
            authority=None,
        ),
    )
    second_digest = service.append(
        event_id="UE-2",
        uncertainty_id="U-1",
        status="resolved",
        transition_id="T-RESOLVE",
        note="agent recorded that this uncertainty no longer governs the decision",
    )
    assert first_digest != second_digest

    result = service.load()
    assert result.valid
    assert len(result.records) == 2
    assert result.records[1]["previous_digest"] == result.records[0]["event_digest"]
    assert result.latest_statuses == {"U-1": "resolved"}
    assert CampaignService(workspace).resume().state.active_uncertainty is None


def test_history_rejects_evidence_outside_campaign_authority(tmp_path):
    workspace = _workspace(tmp_path)
    result = CliRunner().invoke(
        cli,
        [
            "campaign",
            "uncertainty-record",
            "--workspace",
            str(workspace),
            "--event-id",
            "UE-1",
            "--uncertainty-id",
            "U-1",
            "--status",
            "active",
            "--evidence-ref",
            "evidence/not-present.md",
        ],
    )
    assert result.exit_code != 0
    assert "not exposed by Campaign evidence authority" in result.output


def test_uncertainty_history_fails_closed_after_tamper(tmp_path):
    workspace = _workspace(tmp_path)
    service = UncertaintyHistoryService(workspace)
    service.append(event_id="UE-1", uncertainty_id="U-1", status="active")
    path = workspace / "uncertainty-history.jsonl"
    record = json.loads(path.read_text(encoding="utf-8"))
    record["event"]["status"] = "resolved"
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")

    result = CliRunner().invoke(
        cli,
        ["campaign", "uncertainty-history", "--workspace", str(workspace), "--json"],
    )
    assert result.exit_code == 3, result.output
    payload = json.loads(result.output)
    codes = {item["code"] for item in payload["diagnostics"]}
    assert "UNCERTAINTY_HISTORY_DIGEST_MISMATCH" in codes
    assert payload["semantic_recommendation_included"] is False


def test_resume_capsule_surfaces_history_as_non_authoritative_companion(tmp_path):
    workspace = _workspace(tmp_path)
    UncertaintyHistoryService(workspace).append(
        event_id="UE-1",
        uncertainty_id="U-1",
        status="active",
    )
    result = CliRunner().invoke(
        cli,
        [
            "campaign",
            "resume-context",
            "--workspace",
            str(workspace),
            "--compact",
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    history = payload["uncertainty_history"]
    assert history["present"] is True
    assert history["valid"] is True
    assert history["latest_statuses"] == {"U-1": "active"}
    assert history["semantic_recommendation_included"] is False
    assert payload["active_uncertainty"]["id"] == "U-1"
    assert "selected_uncertainty" not in payload


def test_superseded_event_requires_distinct_replacement_id(tmp_path):
    workspace = _workspace(tmp_path)
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "campaign",
            "uncertainty-record",
            "--workspace",
            str(workspace),
            "--event-id",
            "UE-1",
            "--uncertainty-id",
            "U-1",
            "--status",
            "superseded",
            "--superseded-by",
            "U-1",
        ],
    )
    assert result.exit_code != 0
    assert "must differ" in result.output
