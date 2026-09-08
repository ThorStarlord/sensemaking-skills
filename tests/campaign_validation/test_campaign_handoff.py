"""P7 qualification for durable, integrity-bound fresh-context handoff/resume."""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest
import yaml
from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import (
    Authority,
    CampaignPolicy,
    CampaignState,
    Responsibility,
    TerminalState,
    TransitionRecord,
)
from sensemaking_skills.campaigns import (
    AdvanceDecision,
    CampaignDecisionService,
    CampaignIntegrityError,
    CampaignService,
    CampaignTransactionError,
)
from sensemaking_skills.campaigns.handoff import CampaignHandoffService
from sensemaking_skills.cli import CAMPAIGN_INVALID_EXIT, CAMPAIGN_WORKSPACE_EXIT, cli


def _responsibility(responsibility_id: str = "R-P7") -> Responsibility:
    return Responsibility(
        id=responsibility_id,
        statement="continue the explicitly warranted bounded responsibility",
        trigger_evidence=(),
        decision_blocked="whether the bounded responsibility is complete",
        scope="P7 handoff/resume qualification",
        authority=Authority.AUTHORIZED_AUTONOMOUSLY,
        success_conditions=("fresh context reconstructs durable campaign facts",),
    )


def _active_campaign(workspace: Path, *, with_policy: bool = True) -> CampaignService:
    service = CampaignService(workspace)
    policy = (
        CampaignPolicy(
            campaign_id="CMP-P7",
            mission="prove fresh-context reconstruction without chat memory",
            stop_conditions=(TerminalState.OWNER_DECISION_REQUIRED,),
        )
        if with_policy
        else None
    )
    service.initialize(
        CampaignState(
            campaign_id="CMP-P7",
            mission="prove fresh-context reconstruction without chat memory",
            status="active",
            current_state="initialized",
        ),
        policy=policy,
    )
    (service.store.workspace.evidence_dir / "brief.md").write_text(
        "durable P7 evidence",
        encoding="utf-8",
    )
    CampaignDecisionService(workspace).advance(
        AdvanceDecision(
            transition_id="TR-P7-ACTIVE",
            to_state="responsibility_active",
            decision="the agent explicitly authored the responsibility before handoff",
            next_responsibility=_responsibility(),
            evidence=("evidence/brief.md",),
        )
    )
    return CampaignService(workspace)


def _mapping_keys(value: Any) -> tuple[str, ...]:
    keys: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.append(str(key))
            keys.extend(_mapping_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            keys.extend(_mapping_keys(nested))
    return tuple(keys)


def test_create_binds_exact_reconstructible_context_without_mutating_semantic_state(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "campaign"
    lifecycle = _active_campaign(workspace)
    before = lifecycle.resume()

    result = CampaignHandoffService(workspace).create(
        allowed_next_actions=("continue_agent_judgment",),
        stop_conditions=(TerminalState.OWNER_DECISION_REQUIRED,),
    )

    after = lifecycle.resume()
    assert after.state == before.state
    assert after.transitions == before.transitions
    assert after.trace == before.trace
    assert after.evidence_refs == before.evidence_refs
    assert after.policy == before.policy
    assert after.handoff == result.handoff

    assert result.reconstruction_sha256
    assert len(result.reconstruction_sha256) == 64
    assert result.handoff.current_state == before.state
    assert result.handoff.allowed_next_actions == ("continue_agent_judgment",)
    assert result.handoff.stop_conditions == (
        TerminalState.OWNER_DECISION_REQUIRED,
    )
    assert result.handoff.canonical_artifacts == tuple(
        sorted(
            {
                "campaign-state.yaml",
                "campaign-policy.yaml",
                "trace.yaml",
                "transitions/TR-P7-ACTIVE.yaml",
                "evidence/brief.md",
            }
        )
    )

    first_line = lifecycle.store.workspace.handoff_path.read_text(
        encoding="utf-8"
    ).splitlines()[0]
    assert first_line == f"# p7_reconstruction_sha256: {result.reconstruction_sha256}"


def test_fresh_service_instance_resumes_exact_bound_handoff(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    _active_campaign(workspace)
    created = CampaignHandoffService(workspace).create(
        allowed_next_actions=("inspect_current_responsibility",),
    )

    fresh = CampaignHandoffService(workspace).resume()

    assert fresh == created
    assert fresh.snapshot.state.active_responsibility is not None
    assert fresh.snapshot.state.active_responsibility.id == "R-P7"
    assert fresh.snapshot.state.authority is Authority.AUTHORIZED_AUTONOMOUSLY
    assert fresh.snapshot.evidence_refs == ("evidence/brief.md",)
    assert [item.id for item in fresh.snapshot.transitions] == ["TR-P7-ACTIVE"]


def test_cli_handoff_and_resume_emit_complete_unranked_reconstruction_envelope(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "campaign"
    _active_campaign(workspace)
    runner = CliRunner()

    handoff_result = runner.invoke(
        cli,
        [
            "campaign",
            "handoff",
            "--workspace",
            str(workspace),
            "--allowed-next-action",
            "continue_agent_judgment",
            "--stop-condition",
            "owner_decision_required",
            "--json",
        ],
    )
    assert handoff_result.exit_code == 0, handoff_result.output
    handoff_payload = json.loads(handoff_result.output)
    assert handoff_payload["code"] == "CAMPAIGN_HANDOFF_WRITTEN"
    assert handoff_payload["campaign_id"] == "CMP-P7"
    assert handoff_payload["state"]["active_responsibility"]["id"] == "R-P7"
    assert handoff_payload["handoff"]["allowed_next_actions"] == [
        "continue_agent_judgment"
    ]
    assert handoff_payload["handoff"]["stop_conditions"] == [
        "owner_decision_required"
    ]
    assert len(handoff_payload["reconstruction_sha256"]) == 64

    resume_result = runner.invoke(
        cli,
        ["campaign", "resume", "--workspace", str(workspace), "--json"],
    )
    assert resume_result.exit_code == 0, resume_result.output
    resume_payload = json.loads(resume_result.output)
    assert resume_payload["code"] == "CAMPAIGN_RESUMED"
    assert resume_payload["reconstruction_sha256"] == handoff_payload[
        "reconstruction_sha256"
    ]
    assert resume_payload["state"] == handoff_payload["state"]
    assert resume_payload["transitions"] == handoff_payload["transitions"]
    assert resume_payload["trace"] == handoff_payload["trace"]
    assert resume_payload["evidence_refs"] == ["evidence/brief.md"]

    forbidden_key_markers = ("recommend", "rank", "score", "selected")
    for key in _mapping_keys(resume_payload):
        lowered = key.lower()
        assert all(marker not in lowered for marker in forbidden_key_markers), key


def test_cli_handoff_without_guidance_infers_no_next_action_or_stop_condition(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "campaign"
    _active_campaign(workspace)
    result = CliRunner().invoke(
        cli,
        ["campaign", "handoff", "--workspace", str(workspace), "--json"],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["handoff"]["allowed_next_actions"] == []
    assert payload["handoff"]["stop_conditions"] == []
    # Policy stop conditions remain visible in policy but are not silently copied
    # into agent-authored handoff guidance.
    assert payload["policy"]["stop_conditions"] == ["owner_decision_required"]


def test_fresh_python_process_resumes_without_prior_conversation_memory(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "campaign"
    _active_campaign(workspace)
    CampaignHandoffService(workspace).create(
        allowed_next_actions=("fresh_agent_decides",),
    )

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "sensemaking_skills.cli",
            "campaign",
            "resume",
            "--workspace",
            str(workspace),
            "--json",
        ],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr or completed.stdout
    payload = json.loads(completed.stdout)
    assert payload["code"] == "CAMPAIGN_RESUMED"
    assert payload["campaign_id"] == "CMP-P7"
    assert payload["state"]["current_state"] == "responsibility_active"
    assert payload["state"]["active_responsibility"]["id"] == "R-P7"
    assert payload["handoff"]["allowed_next_actions"] == ["fresh_agent_decides"]


def test_editing_handoff_guidance_without_rebinding_fails_closed(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    lifecycle = _active_campaign(workspace)
    CampaignHandoffService(workspace).create(
        allowed_next_actions=("continue_agent_judgment",),
    )

    path = lifecycle.store.workspace.handoff_path
    lines = path.read_text(encoding="utf-8").splitlines()
    marker = lines[0]
    payload = yaml.safe_load("\n".join(lines[1:]))
    payload["allowed_next_actions"] = ["silently_changed_after_handoff"]
    path.write_text(
        marker + "\n" + yaml.safe_dump(payload, sort_keys=False),
        encoding="utf-8",
    )

    with pytest.raises(CampaignIntegrityError) as exc_info:
        CampaignHandoffService(workspace).resume()
    assert "HANDOFF_RECONSTRUCTION_BINDING_MISMATCH" in exc_info.value.diagnostic_codes


def test_legacy_unbound_handoff_is_not_accepted_as_p7_fresh_context(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    lifecycle = _active_campaign(workspace)
    snapshot = lifecycle.resume()
    lifecycle.generate_handoff(
        canonical_artifacts=("campaign-state.yaml", "trace.yaml"),
        allowed_next_actions=(),
        stop_conditions=(),
    )
    assert snapshot.state == lifecycle.store.load_state()

    with pytest.raises(CampaignIntegrityError) as exc_info:
        CampaignHandoffService(workspace).resume()
    assert "HANDOFF_RECONSTRUCTION_BINDING_MISSING" in exc_info.value.diagnostic_codes


def test_next_lifecycle_transition_invalidates_handoff_and_fresh_resume_fails_closed(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "campaign"
    lifecycle = _active_campaign(workspace)
    CampaignHandoffService(workspace).create()
    current = lifecycle.resume()
    assert current.handoff is not None

    lifecycle.record_transition(
        new_state=replace(current.state, current_state="post_handoff_transition"),
        transition=TransitionRecord(
            id="TR-P7-NEXT",
            from_state=current.state.current_state,
            to_state="post_handoff_transition",
            evidence=(),
            decision="advance after the old handoff was generated",
            next_responsibility="R-P7",
            authority=current.state.authority,
        ),
    )

    assert not lifecycle.store.workspace.handoff_path.exists()
    with pytest.raises(CampaignTransactionError, match="requires a current campaign handoff"):
        CampaignHandoffService(workspace).resume()


def test_terminal_campaign_handoff_resumes_terminal_state_honestly(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    lifecycle = CampaignService(workspace)
    lifecycle.initialize(
        CampaignState(
            campaign_id="CMP-P7-TERM",
            mission="preserve a terminal campaign honestly",
            status="active",
            current_state="initialized",
        )
    )
    lifecycle.terminate(
        transition_id="TR-P7-DONE",
        to_state="done",
        terminal_state=TerminalState.GOAL_ACHIEVED,
        decision="the explicit campaign goal is achieved",
    )

    result = CampaignHandoffService(workspace).create()
    fresh = CampaignHandoffService(workspace).resume()

    assert result.snapshot.state.status == "terminal"
    assert fresh.snapshot.state.terminal_state is TerminalState.GOAL_ACHIEVED
    assert fresh.snapshot.state.active_responsibility is None
    assert fresh.handoff.allowed_next_actions == ()


def test_duplicate_or_blank_agent_guidance_is_rejected_before_handoff_write(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "campaign"
    lifecycle = _active_campaign(workspace)

    with pytest.raises(CampaignTransactionError, match="non-empty"):
        CampaignHandoffService(workspace).create(allowed_next_actions=("   ",))
    assert not lifecycle.store.workspace.handoff_path.exists()

    with pytest.raises(CampaignTransactionError, match="duplicates"):
        CampaignHandoffService(workspace).create(
            allowed_next_actions=("inspect", "inspect")
        )
    assert not lifecycle.store.workspace.handoff_path.exists()


def test_cli_resume_without_handoff_uses_existing_workspace_failure_class(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "campaign"
    _active_campaign(workspace)

    result = CliRunner().invoke(
        cli,
        ["campaign", "resume", "--workspace", str(workspace), "--json"],
    )

    assert result.exit_code == CAMPAIGN_WORKSPACE_EXIT
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_TRANSACTION_ERROR"
    assert "requires a current campaign handoff" in payload["message"]


def test_cli_tampered_bound_handoff_uses_integrity_failure_class(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    lifecycle = _active_campaign(workspace)
    CampaignHandoffService(workspace).create()

    path = lifecycle.store.workspace.handoff_path
    raw = path.read_text(encoding="utf-8")
    path.write_text(
        raw.replace(
            "allowed_next_actions: []",
            "allowed_next_actions:\n- silently_changed",
        ),
        encoding="utf-8",
    )

    result = CliRunner().invoke(
        cli,
        ["campaign", "resume", "--workspace", str(workspace), "--json"],
    )

    assert result.exit_code == CAMPAIGN_INVALID_EXIT
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_INTEGRITY_ERROR"
    assert "HANDOFF_RECONSTRUCTION_BINDING_MISMATCH" in payload["diagnostics"]
