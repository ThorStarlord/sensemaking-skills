"""Resume Capsule v1 deterministic projection contracts."""

from __future__ import annotations

import json
from dataclasses import replace

from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import CampaignState, TransitionRecord
from sensemaking_skills.campaigns import CampaignService
from sensemaking_skills.cli import cli


def _workspace(tmp_path):
    workspace = tmp_path / "campaign"
    service = CampaignService(workspace)
    service.initialize(
        CampaignState(
            campaign_id="CMP-RESUME-V1",
            mission="reconstruct bounded durable context",
            status="active",
            current_state="initialized",
            established_facts=("fact-a", "fact-b"),
            resolved_questions=("question-a",),
        )
    )
    current = service.resume().state
    service.record_transition(
        new_state=replace(current, current_state="review"),
        transition=TransitionRecord(
            id="T1",
            from_state="initialized",
            to_state="review",
            evidence=(),
            decision="enter review",
            authority=None,
        ),
    )
    current = service.resume().state
    service.record_transition(
        new_state=replace(current, current_state="verify"),
        transition=TransitionRecord(
            id="T2",
            from_state="review",
            to_state="verify",
            evidence=(),
            decision="enter verification",
            authority=None,
        ),
    )
    return workspace


def test_full_resume_capsule_remains_backward_compatible_and_versioned(tmp_path):
    workspace = _workspace(tmp_path)
    result = CliRunner().invoke(
        cli,
        ["campaign", "resume-context", "--workspace", str(workspace), "--json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_RESUME_CONTEXT"
    assert payload["capsule_version"] == "1"
    assert payload["projection"] == "full"
    assert payload["current_state"] == "verify"
    assert payload["established_facts"] == ["fact-a", "fact-b"]
    assert payload["resolved_questions"] == ["question-a"]
    assert payload["recent_transitions"][-1]["id"] == "T2"
    assert payload["semantic_recommendation_included"] is False
    assert payload["semantic_truth_established"] is False
    assert "recommended_next_action" not in payload


def test_compact_resume_capsule_uses_counts_ids_and_bounded_recent_history(tmp_path):
    workspace = _workspace(tmp_path)
    runner = CliRunner()
    full_result = runner.invoke(
        cli,
        ["campaign", "resume-context", "--workspace", str(workspace), "--json"],
    )
    compact_result = runner.invoke(
        cli,
        [
            "campaign",
            "resume-context",
            "--workspace",
            str(workspace),
            "--recent-transitions",
            "1",
            "--compact",
            "--json",
        ],
    )
    assert compact_result.exit_code == 0, compact_result.output
    payload = json.loads(compact_result.output)
    assert payload["projection"] == "compact"
    assert payload["counts"]["established_facts"] == 2
    assert payload["counts"]["resolved_questions"] == 1
    assert payload["counts"]["transitions"] == 2
    assert [item["id"] for item in payload["recent_transitions"]] == ["T2"]
    assert "target_snapshot" not in payload
    assert "evidence_refs" not in payload
    assert payload["handoff_present"] is False
    assert len(compact_result.output) < len(full_result.output)


def test_resume_capsule_can_include_preflight_without_turning_it_into_advice(tmp_path):
    workspace = _workspace(tmp_path)
    result = CliRunner().invoke(
        cli,
        [
            "campaign",
            "resume-context",
            "--workspace",
            str(workspace),
            "--compact",
            "--include-preflight",
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    preflight = payload["preflight"]
    assert preflight["ready"] is True
    assert preflight["semantic_recommendation_included"] is False
    assert preflight["semantic_truth_established"] is False
    assert all("detail" not in item for item in preflight["checks"])
    assert "recommended_next_action" not in payload


def test_resume_capsule_surfaces_failed_preflight_without_changing_resume_exit_semantics(tmp_path):
    workspace = _workspace(tmp_path)
    (workspace / "semantic-state.jsonl").write_text("{broken-json}\n", encoding="utf-8")
    result = CliRunner().invoke(
        cli,
        [
            "campaign",
            "resume-context",
            "--workspace",
            str(workspace),
            "--include-preflight",
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["semantic_companion"]["valid"] is False
    assert payload["preflight"]["ready"] is False
    failed = [item for item in payload["preflight"]["checks"] if item["status"] == "fail"]
    assert failed
    assert "SEMANTIC_STATE_INVALID_JSON" in failed[0]["diagnostics"]
