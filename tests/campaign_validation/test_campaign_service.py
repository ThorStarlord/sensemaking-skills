import os
from dataclasses import replace
from pathlib import Path

import pytest

import sensemaking_skills.campaigns.store as store_module
from sensemaking_skills.campaign_semantics import (
    Authority,
    CampaignPolicy,
    CampaignState,
    Responsibility,
    TerminalState,
    TransitionRecord,
)
from sensemaking_skills.campaigns import (
    CampaignIntegrityError,
    CampaignService,
    CampaignTransactionError,
)


def _state(
    *,
    current_state="initialized",
    authority=Authority.AUTHORIZED_AUTONOMOUSLY,
    active_responsibility=None,
):
    return CampaignState(
        campaign_id="CMP-P2",
        mission="prove durable lifecycle service",
        status="active",
        current_state=current_state,
        authority=authority,
        active_responsibility=active_responsibility,
    )


def _responsibility(
    *,
    authority=Authority.AUTHORIZED_AUTONOMOUSLY,
    responsibility_id="R-1",
):
    return Responsibility(
        id=responsibility_id,
        statement="perform the explicitly chosen bounded responsibility",
        trigger_evidence=(),
        decision_blocked="whether the bounded responsibility is complete",
        scope="P2 qualification",
        authority=authority,
        success_conditions=("durable transition recorded",),
    )


def _transition(
    *,
    transition_id="TR-0001",
    from_state="initialized",
    to_state="sensemaking",
    evidence=(),
    authority=Authority.AUTHORIZED_AUTONOMOUSLY,
    next_responsibility=None,
    terminal_state=None,
):
    return TransitionRecord(
        id=transition_id,
        from_state=from_state,
        to_state=to_state,
        evidence=evidence,
        decision="record the agent-authored lifecycle decision",
        next_responsibility=next_responsibility,
        terminal_state=terminal_state,
        authority=authority,
    )


def test_initialize_validate_and_fresh_service_resume_roundtrip(tmp_path):
    workspace = tmp_path / "CMP-P2"
    service = CampaignService(workspace)
    policy = CampaignPolicy(
        campaign_id="CMP-P2",
        mission="prove durable lifecycle service",
    )

    created = service.initialize(_state(), policy=policy)

    assert created.state.current_state == "initialized"
    assert created.transitions == ()
    assert created.trace.initial_state == "initialized"
    assert service.validate().valid
    assert service.store.workspace.transactions_dir.is_dir()

    fresh = CampaignService(workspace).resume()
    assert fresh == created


def test_initialize_rejects_authority_metadata_mismatch_before_writing(tmp_path):
    responsibility = _responsibility(
        authority=Authority.OWNER_AUTHORIZATION_REQUIRED,
    )
    state = _state(
        authority=Authority.AUTHORIZED_AUTONOMOUSLY,
        active_responsibility=responsibility,
    )

    with pytest.raises(CampaignIntegrityError) as exc_info:
        CampaignService(tmp_path / "CMP-P2").initialize(state)

    assert "AUTHORITY_METADATA_MISMATCH" in exc_info.value.diagnostic_codes
    assert not (tmp_path / "CMP-P2").exists()


def test_record_transition_persists_reconstructible_state_history_and_trace(tmp_path):
    service = CampaignService(tmp_path / "CMP-P2")
    service.initialize(_state())
    evidence_path = service.store.workspace.evidence_dir / "brief.md"
    evidence_path.write_text("validated brief", encoding="utf-8")

    new_state = _state(current_state="sensemaking")
    snapshot = service.record_transition(
        new_state=new_state,
        transition=_transition(evidence=("evidence/brief.md",)),
    )

    assert snapshot.state == new_state
    assert [record.id for record in snapshot.transitions] == ["TR-0001"]
    assert snapshot.trace.events[-1] == {
        "event": "transition_committed",
        "transition_id": "TR-0001",
        "from_state": "initialized",
        "to_state": "sensemaking",
    }
    assert service.validate().valid
    assert not any(service.store.workspace.transactions_dir.iterdir())


def test_transition_requires_existing_evidence_before_commit_intent(tmp_path):
    service = CampaignService(tmp_path / "CMP-P2")
    service.initialize(_state())

    with pytest.raises(CampaignTransactionError, match="missing evidence"):
        service.record_transition(
            new_state=_state(current_state="sensemaking"),
            transition=_transition(evidence=("evidence/missing.md",)),
        )

    assert service.store.load_state().current_state == "initialized"
    assert service.store.load_transitions() == ()
    assert not any(service.store.workspace.transactions_dir.iterdir())


def test_transition_source_and_target_must_match_state_snapshots(tmp_path):
    service = CampaignService(tmp_path / "CMP-P2")
    service.initialize(_state())

    with pytest.raises(CampaignTransactionError, match="from_state"):
        service.record_transition(
            new_state=_state(current_state="sensemaking"),
            transition=_transition(from_state="wrong"),
        )

    with pytest.raises(CampaignTransactionError, match="to_state"):
        service.record_transition(
            new_state=_state(current_state="different"),
            transition=_transition(to_state="sensemaking"),
        )

    assert service.store.load_transitions() == ()


def test_publish_failure_has_no_live_lifecycle_effect(tmp_path, monkeypatch):
    service = CampaignService(tmp_path / "CMP-P2")
    service.initialize(_state())
    real_replace = store_module.os.replace
    transaction_dir = service.store.workspace.transactions_dir / "TR-0001"

    def fail_commit_intent(src, dst):
        if Path(dst) == transaction_dir and Path(src).name.startswith(".TR-0001.staging-"):
            raise OSError("simulated journal publish failure")
        return real_replace(src, dst)

    monkeypatch.setattr(store_module.os, "replace", fail_commit_intent)

    with pytest.raises(CampaignTransactionError, match="publish lifecycle commit intent"):
        service.record_transition(
            new_state=_state(current_state="sensemaking"),
            transition=_transition(),
        )

    assert service.store.load_state().current_state == "initialized"
    assert service.store.load_transitions() == ()
    assert service.store.load_trace().events == ()
    assert not transaction_dir.exists()


def test_crash_after_commit_intent_recovers_exact_transition(tmp_path, monkeypatch):
    workspace = tmp_path / "CMP-P2"
    service = CampaignService(workspace)
    service.initialize(_state())
    real_atomic_write = store_module._atomic_write_yaml
    failed = {"trace": False}

    def fail_first_trace_materialization(path, payload):
        if Path(path) == service.store.workspace.trace_path and not failed["trace"]:
            failed["trace"] = True
            raise OSError("simulated crash after durable intent")
        return real_atomic_write(path, payload)

    monkeypatch.setattr(store_module, "_atomic_write_yaml", fail_first_trace_materialization)

    with pytest.raises(CampaignTransactionError, match="materialization is pending"):
        service.record_transition(
            new_state=_state(current_state="sensemaking"),
            transition=_transition(),
        )

    # State is deliberately last: it never advertises an advance before history.
    assert service.store.load_state().current_state == "initialized"
    assert [record.id for record in service.store.load_transitions()] == ["TR-0001"]
    journal = service.store.workspace.transactions_dir / "TR-0001"
    assert journal.is_dir()

    monkeypatch.setattr(store_module, "_atomic_write_yaml", real_atomic_write)
    recovered = CampaignService(workspace).resume()

    assert recovered.state.current_state == "sensemaking"
    assert [record.id for record in recovered.transitions] == ["TR-0001"]
    assert recovered.trace.events[-1]["transition_id"] == "TR-0001"
    assert not journal.exists()


def test_defer_responsibility_moves_explicit_active_record_to_deferred(tmp_path):
    responsibility = _responsibility()
    service = CampaignService(tmp_path / "CMP-P2")
    service.initialize(_state(active_responsibility=responsibility))

    snapshot = service.defer_responsibility(
        transition_id="TR-DEFER",
        to_state="deferred_boundary",
        reason="the agent reached an external dependency",
        reopen_when=("dependency becomes available",),
        not_reopened_by=("elapsed time alone",),
        decision="defer rather than fabricate progress",
    )

    assert snapshot.state.active_responsibility is None
    assert snapshot.state.authority is None
    assert snapshot.state.deferred_responsibilities[0].responsibility_id == "R-1"
    assert snapshot.state.deferred_responsibilities[0].reopen_when == (
        "dependency becomes available",
    )
    assert snapshot.transitions[-1].id == "TR-DEFER"


def test_terminate_records_terminal_state_and_clears_executable_work(tmp_path):
    responsibility = _responsibility()
    service = CampaignService(tmp_path / "CMP-P2")
    service.initialize(_state(active_responsibility=responsibility))

    snapshot = service.terminate(
        transition_id="TR-DONE",
        to_state="done",
        terminal_state=TerminalState.GOAL_ACHIEVED,
        decision="the explicitly defined campaign goal is achieved",
    )

    assert snapshot.state.status == "terminal"
    assert snapshot.state.current_state == "done"
    assert snapshot.state.active_responsibility is None
    assert snapshot.state.terminal_state is TerminalState.GOAL_ACHIEVED
    assert snapshot.trace.terminal_state == TerminalState.GOAL_ACHIEVED.value
    assert snapshot.transitions[-1].terminal_state is TerminalState.GOAL_ACHIEVED
    assert service.validate().valid

    with pytest.raises(CampaignTransactionError, match="terminal campaigns"):
        service.record_transition(
            new_state=replace(snapshot.state, current_state="illegal"),
            transition=_transition(
                transition_id="TR-ILLEGAL",
                from_state="done",
                to_state="illegal",
                authority=snapshot.state.authority,
                terminal_state=TerminalState.GOAL_ACHIEVED,
            ),
        )


def test_generate_handoff_is_exact_and_next_transition_invalidates_it(tmp_path):
    service = CampaignService(tmp_path / "CMP-P2")
    service.initialize(_state())
    evidence_path = service.store.workspace.evidence_dir / "brief.md"
    evidence_path.write_text("brief", encoding="utf-8")

    handoff = service.generate_handoff(
        canonical_artifacts=("campaign-state.yaml", "evidence/brief.md"),
        allowed_next_actions=("continue_agent_judgment",),
        stop_conditions=(TerminalState.OWNER_DECISION_REQUIRED,),
    )
    assert handoff.current_state == service.store.load_state()

    snapshot = service.record_transition(
        new_state=_state(current_state="sensemaking"),
        transition=_transition(evidence=("evidence/brief.md",)),
    )
    assert snapshot.handoff is None
    assert not os.path.lexists(service.store.workspace.handoff_path)


def test_generate_handoff_rejects_non_durable_canonical_artifact(tmp_path):
    service = CampaignService(tmp_path / "CMP-P2")
    service.initialize(_state())

    with pytest.raises(CampaignTransactionError, match="non-durable"):
        service.generate_handoff(
            canonical_artifacts=("some/external/chat-memory",),
            allowed_next_actions=(),
            stop_conditions=(),
        )


def test_validate_reports_transition_not_ordered_by_trace(tmp_path):
    service = CampaignService(tmp_path / "CMP-P2")
    service.initialize(_state())
    service.store.append_transition(_transition())

    result = service.validate()

    assert not result.valid
    assert "UNTRACED_TRANSITION" in result.diagnostic_codes
    with pytest.raises(CampaignIntegrityError) as exc_info:
        service.resume()
    assert "UNTRACED_TRANSITION" in exc_info.value.diagnostic_codes


def test_policy_mission_mismatch_is_rejected_before_initialization(tmp_path):
    service = CampaignService(tmp_path / "CMP-P2")
    policy = CampaignPolicy(campaign_id="CMP-P2", mission="different mission")

    with pytest.raises(CampaignIntegrityError) as exc_info:
        service.initialize(_state(), policy=policy)

    assert "POLICY_MISSION_MISMATCH" in exc_info.value.diagnostic_codes
    assert not service.store.root.exists()
