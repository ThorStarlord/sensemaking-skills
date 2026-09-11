"""Campaign Preflight v0 repository/hermetic qualification."""

from __future__ import annotations

import json

from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import (
    Authority,
    CampaignState,
    Responsibility,
)
from sensemaking_skills.campaigns import CampaignService
from sensemaking_skills.cli import cli


def _check(payload: dict, check_id: str) -> dict:
    return next(item for item in payload["checks"] if item["id"] == check_id)


def test_preflight_passes_valid_targetless_campaign_without_semantic_decision(tmp_path):
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-PREFLIGHT",
            mission="verify declared mechanical readiness",
            status="active",
            current_state="initialized",
        )
    )

    result = CliRunner().invoke(
        cli,
        ["campaign", "preflight", "--workspace", str(workspace), "--json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_PREFLIGHT_PASS"
    assert payload["ready"] is True
    assert payload["semantic_recommendation_included"] is False
    assert payload["semantic_truth_established"] is False
    assert "recommended_next_action" not in payload
    assert _check(payload, "campaign_integrity")["status"] == "pass"
    assert _check(payload, "target_binding")["status"] == "not_applicable"
    assert _check(payload, "capability_catalog")["status"] == "not_evaluated"
    assert "does not decide whether the agent should proceed" in payload["explicit_limit"]


def test_preflight_enumerates_unranked_agent_supplied_capability_type(tmp_path):
    workspace = tmp_path / "campaign"
    responsibility = Responsibility(
        id="R-1",
        statement="diagnose the repository",
        trigger_evidence=(),
        decision_blocked="which repository boundary matters",
        scope="repository",
        authority=Authority.AUTHORIZED_AUTONOMOUSLY,
        success_conditions=("diagnosis returned",),
    )
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-PREFLIGHT-CAP",
            mission="inspect declared capability compatibility",
            status="active",
            current_state="diagnosis",
            active_responsibility=responsibility,
            authority=Authority.AUTHORIZED_AUTONOMOUSLY,
        )
    )

    result = CliRunner().invoke(
        cli,
        [
            "campaign",
            "preflight",
            "--workspace",
            str(workspace),
            "--responsibility-type",
            "repository_diagnosis",
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    capability = _check(payload, "capability_catalog")
    assert capability["status"] == "pass"
    assert "repo-sensemaker" in capability["data"]["candidate_ids"]
    assert capability["data"]["availability_counts"]["external"] >= 1
    assert payload["ready"] is True
    assert "selected_capability" not in payload


def test_preflight_fails_closed_on_corrupt_semantic_companion(tmp_path):
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-PREFLIGHT-BAD-SEMANTIC",
            mission="surface companion corruption",
            status="active",
            current_state="initialized",
        )
    )
    (workspace / "semantic-state.jsonl").write_text("{not-json}\n", encoding="utf-8")

    result = CliRunner().invoke(
        cli,
        ["campaign", "preflight", "--workspace", str(workspace), "--json"],
    )
    assert result.exit_code == 3, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_PREFLIGHT_FAIL"
    assert payload["ready"] is False
    semantic = _check(payload, "semantic_reference_integrity")
    assert semantic["status"] == "fail"
    assert "SEMANTIC_STATE_INVALID_JSON" in semantic["diagnostics"]


def test_preflight_does_not_infer_capability_type_from_responsibility_prose(tmp_path):
    workspace = tmp_path / "campaign"
    responsibility = Responsibility(
        id="R-2",
        statement="repository diagnosis",
        trigger_evidence=(),
        decision_blocked="what matters next",
        scope="repository",
        authority=Authority.AUTHORIZED_AUTONOMOUSLY,
        success_conditions=("bounded result",),
    )
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-PREFLIGHT-NO-INFER",
            mission="preserve semantic ownership",
            status="active",
            current_state="diagnosis",
            active_responsibility=responsibility,
            authority=Authority.AUTHORIZED_AUTONOMOUSLY,
        )
    )

    result = CliRunner().invoke(
        cli,
        ["campaign", "preflight", "--workspace", str(workspace), "--json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    capability = _check(payload, "capability_catalog")
    assert capability["status"] == "not_evaluated"
    assert capability["data"] == {}


def test_preflight_rejects_blank_explicit_responsibility_type(tmp_path):
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-PREFLIGHT-BLANK",
            mission="reject ambiguous explicit input",
            status="active",
            current_state="initialized",
        )
    )
    result = CliRunner().invoke(
        cli,
        [
            "campaign",
            "preflight",
            "--workspace",
            str(workspace),
            "--responsibility-type",
            "   ",
            "--json",
        ],
    )
    assert result.exit_code != 0
    assert "must be non-empty" in result.output
