import os

import pytest
import yaml

from sensemaking_skills.campaign_semantics import (
    Authority,
    CampaignHandoff,
    CampaignPolicy,
    CampaignState,
    TransitionRecord,
)
from sensemaking_skills.campaign_semantics.io import ContractError
from sensemaking_skills.campaigns import (
    CampaignAlreadyExistsError,
    CampaignIdentityError,
    CampaignStore,
    CampaignWorkspaceError,
)


def _state(*, campaign_id="CMP-1", current_state="initialized"):
    return CampaignState(
        campaign_id=campaign_id,
        mission="build a durable productization campaign",
        status="active",
        current_state=current_state,
        authority=Authority.AUTHORIZED_AUTONOMOUSLY,
    )


def _symlink_or_skip(link, target, *, target_is_directory=False):
    try:
        link.symlink_to(target, target_is_directory=target_is_directory)
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f"symlink capability unavailable: {exc}")


def test_initialize_creates_isolated_roundtrippable_workspace(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    (target / "marker.txt").write_text("target", encoding="utf-8")
    workspace = tmp_path / "campaigns" / "CMP-1"

    store = CampaignStore(workspace, target_repo=target)
    state = _state()
    policy = CampaignPolicy(campaign_id=state.campaign_id, mission=state.mission)
    store.initialize(state, policy=policy)

    assert store.load_state() == state
    assert store.load_policy() == policy
    assert store.load_trace().initial_state == "initialized"
    assert store.workspace.transitions_dir.is_dir()
    assert store.workspace.artifacts_dir.is_dir()
    assert store.workspace.evidence_dir.is_dir()
    assert (target / "marker.txt").read_text(encoding="utf-8") == "target"
    assert sorted(path.name for path in target.iterdir()) == ["marker.txt"]


def test_initialize_refuses_workspace_inside_target_repository(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    store = CampaignStore(target / ".sensemaking" / "CMP-1", target_repo=target)

    with pytest.raises(CampaignWorkspaceError, match="outside the target repository"):
        store.initialize(_state())

    assert not (target / ".sensemaking").exists()


def test_initialize_refuses_existing_workspace_without_overwriting(tmp_path):
    workspace = tmp_path / "CMP-1"
    workspace.mkdir()
    marker = workspace / "owner-data.txt"
    marker.write_text("preserve", encoding="utf-8")

    with pytest.raises(CampaignAlreadyExistsError):
        CampaignStore(workspace).initialize(_state())

    assert marker.read_text(encoding="utf-8") == "preserve"


def test_initialize_refuses_broken_symlink_workspace_entry(tmp_path):
    workspace = tmp_path / "CMP-1"
    missing_target = tmp_path / "missing-workspace-target"
    _symlink_or_skip(workspace, missing_target, target_is_directory=True)

    store = CampaignStore(workspace)
    with pytest.raises(CampaignAlreadyExistsError):
        store.initialize(_state())

    assert workspace.is_symlink()
    assert not missing_target.exists()


def test_replacement_state_preserves_campaign_identity(tmp_path):
    store = CampaignStore(tmp_path / "CMP-1")
    store.initialize(_state())

    with pytest.raises(CampaignIdentityError):
        store.save_state(_state(campaign_id="CMP-OTHER", current_state="next"))

    assert store.load_state().campaign_id == "CMP-1"
    assert store.load_state().current_state == "initialized"


def test_failed_atomic_state_replace_leaves_previous_state_intact(tmp_path, monkeypatch):
    store = CampaignStore(tmp_path / "CMP-1")
    store.initialize(_state())

    def fail_replace(src, dst):
        raise OSError("simulated replace failure")

    monkeypatch.setattr(os, "replace", fail_replace)
    with pytest.raises(OSError, match="simulated replace failure"):
        store.save_state(_state(current_state="next"))

    assert store.load_state().current_state == "initialized"


def test_transition_records_are_append_only(tmp_path):
    store = CampaignStore(tmp_path / "CMP-1")
    store.initialize(_state())
    transition = TransitionRecord(
        id="TR-0001",
        from_state="initialized",
        to_state="sensemaking",
        evidence=(),
        decision="begin agent-led repository sensemaking",
        authority=Authority.AUTHORIZED_AUTONOMOUSLY,
    )

    store.append_transition(transition)
    with pytest.raises(CampaignWorkspaceError, match="already exists"):
        store.append_transition(transition)

    assert store.load_transitions() == (transition,)


def test_trace_events_append_without_replacing_prior_events(tmp_path):
    store = CampaignStore(tmp_path / "CMP-1")
    store.initialize(_state())

    store.append_trace_event({"event": "created"})
    store.append_trace_event({"event": "artifact_validated", "artifact": "brief.md"})

    assert store.load_trace().events == (
        {"event": "created"},
        {"event": "artifact_validated", "artifact": "brief.md"},
    )


def test_handoff_snapshot_must_equal_current_campaign_state(tmp_path):
    store = CampaignStore(tmp_path / "CMP-1")
    store.initialize(_state())
    current = store.load_state()
    handoff = CampaignHandoff(
        campaign_id=current.campaign_id,
        current_state=current,
        canonical_artifacts=(),
        allowed_next_actions=("inspect_repository",),
        stop_conditions=(),
    )

    store.write_handoff(handoff)
    assert store.load_handoff() == handoff

    stale_handoff = CampaignHandoff(
        campaign_id=current.campaign_id,
        current_state=_state(current_state="stale"),
        canonical_artifacts=(),
        allowed_next_actions=("inspect_repository",),
        stop_conditions=(),
    )
    with pytest.raises(CampaignIdentityError, match="current_state"):
        store.write_handoff(stale_handoff)

    assert store.load_handoff() == handoff


def test_evidence_refs_are_workspace_relative_and_stable(tmp_path):
    store = CampaignStore(tmp_path / "CMP-1")
    store.initialize(_state())
    (store.workspace.artifacts_dir / "brief.md").write_text("brief", encoding="utf-8")
    nested = store.workspace.evidence_dir / "probe"
    nested.mkdir()
    (nested / "report.yaml").write_text("ok: true\n", encoding="utf-8")

    assert store.evidence_refs() == (
        "artifacts/brief.md",
        "evidence/probe/report.yaml",
    )


def test_evidence_refs_reject_symlinked_file_escape(tmp_path):
    store = CampaignStore(tmp_path / "CMP-1")
    store.initialize(_state())
    outside = tmp_path / "outside-secret.txt"
    outside.write_text("secret", encoding="utf-8")
    link = store.workspace.artifacts_dir / "leaked.txt"
    _symlink_or_skip(link, outside)

    with pytest.raises(CampaignWorkspaceError, match="physically contained"):
        store.evidence_refs()


def test_evidence_refs_reject_symlinked_directory_escape(tmp_path):
    store = CampaignStore(tmp_path / "CMP-1")
    store.initialize(_state())
    outside = tmp_path / "outside-evidence"
    outside.mkdir()
    (outside / "secret.txt").write_text("secret", encoding="utf-8")
    link = store.workspace.evidence_dir / "linked"
    _symlink_or_skip(link, outside, target_is_directory=True)

    with pytest.raises(CampaignWorkspaceError, match="physically contained"):
        store.evidence_refs()


def test_contract_corruption_fails_closed_on_load(tmp_path):
    store = CampaignStore(tmp_path / "CMP-1")
    store.initialize(_state())
    payload = yaml.safe_load(store.workspace.state_path.read_text(encoding="utf-8"))
    payload["unexpected_semantic_field"] = "must not be silently discarded"
    store.workspace.state_path.write_text(
        yaml.safe_dump(payload, sort_keys=False),
        encoding="utf-8",
    )

    with pytest.raises(ContractError, match="unknown decision-relevant field"):
        store.load_state()
