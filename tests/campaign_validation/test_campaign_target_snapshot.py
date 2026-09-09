from __future__ import annotations

import json
import subprocess
from dataclasses import replace
from pathlib import Path

import pytest
from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import (
    CampaignState,
    TransitionRecord,
    dump_campaign_state,
    dump_transition_record,
    target_snapshot_sha256,
)
from sensemaking_skills.campaigns import (
    CampaignIntegrityError,
    CampaignService,
    capture_target_snapshot,
)
from sensemaking_skills.campaigns.handoff import CampaignHandoffService
from sensemaking_skills.cli import cli


def _git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return completed.stdout.strip()


def _repo(tmp_path: Path, name: str = "target") -> Path:
    repo = tmp_path / name
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "target@example.invalid")
    _git(repo, "config", "user.name", "Target Fixture")
    (repo / "tracked.txt").write_text("initial\n", encoding="utf-8")
    _git(repo, "add", "tracked.txt")
    _git(repo, "commit", "-m", "initial")
    return repo


def _state(campaign_id: str = "CMP-TARGET") -> CampaignState:
    return CampaignState(
        campaign_id=campaign_id,
        mission="bind exact target provenance without semantic routing",
        status="active",
        current_state="initialized",
    )


def test_target_snapshot_is_deterministic_and_detects_worktree_change(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    first = capture_target_snapshot(repo)
    second = capture_target_snapshot(repo)

    assert first == second
    assert first.dirty is False
    assert len(first.repository_id) == 64
    assert len(first.worktree_sha256) == 64

    (repo / "tracked.txt").write_text("changed\n", encoding="utf-8")
    changed = capture_target_snapshot(repo)

    assert changed.repository_id == first.repository_id
    assert changed.head_sha == first.head_sha
    assert changed.tree_sha == first.tree_sha
    assert changed.worktree_sha256 != first.worktree_sha256
    assert changed.dirty is True


def test_targetless_v2_serialization_keeps_pre_binding_shape() -> None:
    state_payload = dump_campaign_state(_state())
    transition_payload = dump_transition_record(
        TransitionRecord(
            id="T0",
            from_state="initialized",
            to_state="next",
            evidence=(),
            decision="explicit agent decision",
        )
    )

    assert state_payload["schema_version"] == "2"
    assert "target_snapshot" not in state_payload
    assert "from_target_snapshot_sha256" not in transition_payload
    assert "to_target_snapshot_sha256" not in transition_payload


def test_initialize_persists_first_class_target_snapshot(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    workspace = tmp_path / "campaign"

    snapshot = CampaignService(workspace, target_repo=repo).initialize(_state())
    assert snapshot.state.target_snapshot is not None
    expected = capture_target_snapshot(repo)
    assert snapshot.state.target_snapshot == expected

    raw = (workspace / "campaign-state.yaml").read_text(encoding="utf-8")
    assert "target_snapshot:" in raw
    assert expected.repository_id in raw
    assert expected.worktree_sha256 in raw

    fresh_context = CampaignService(workspace).resume()
    assert fresh_context.state.target_snapshot == expected


def test_resume_and_validate_fail_closed_on_unrecorded_target_drift(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    workspace = tmp_path / "campaign"
    CampaignService(workspace, target_repo=repo).initialize(_state())

    (repo / "tracked.txt").write_text("unrecorded change\n", encoding="utf-8")

    with pytest.raises(CampaignIntegrityError) as raised:
        CampaignService(workspace).resume()
    assert "TARGET_SNAPSHOT_DRIFT" in raised.value.diagnostic_codes

    validation = CampaignService(workspace).validate()
    assert validation.valid is False
    assert "TARGET_SNAPSHOT_DRIFT" in validation.diagnostic_codes


def test_lifecycle_transition_binds_source_and_post_work_target_snapshots(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    workspace = tmp_path / "campaign"
    service = CampaignService(workspace, target_repo=repo)
    initialized = service.initialize(_state())
    initial_target = initialized.state.target_snapshot
    assert initial_target is not None
    initial_digest = target_snapshot_sha256(initial_target)

    (repo / "tracked.txt").write_text("bounded work\n", encoding="utf-8")
    current = service.resume_for_transition().state
    committed = service.record_transition(
        new_state=replace(current, current_state="work_recorded"),
        transition=TransitionRecord(
            id="T1",
            from_state="initialized",
            to_state="work_recorded",
            evidence=(),
            decision="agent records bounded work disposition",
            authority=current.authority,
        ),
    )

    transition = committed.transitions[0]
    current_target = committed.state.target_snapshot
    assert current_target is not None
    current_digest = target_snapshot_sha256(current_target)
    assert transition.from_target_snapshot_sha256 == initial_digest
    assert transition.to_target_snapshot_sha256 == current_digest
    assert current_digest != initial_digest
    assert current_target.dirty is True

    # A second decision without additional repository change must continue the
    # target chain exactly from the first transition destination.
    state2 = committed.state
    committed2 = service.record_transition(
        new_state=replace(state2, current_state="reviewed"),
        transition=TransitionRecord(
            id="T2",
            from_state="work_recorded",
            to_state="reviewed",
            evidence=(),
            decision="agent records review disposition",
            authority=state2.authority,
        ),
    )
    second = committed2.transitions[1]
    assert second.from_target_snapshot_sha256 == transition.to_target_snapshot_sha256
    assert second.to_target_snapshot_sha256 == transition.to_target_snapshot_sha256


def test_explicit_wrong_target_identity_fails_closed(tmp_path: Path) -> None:
    repo = _repo(tmp_path, "target-a")
    other = _repo(tmp_path, "target-b")
    workspace = tmp_path / "campaign"
    CampaignService(workspace, target_repo=repo).initialize(_state())

    with pytest.raises(CampaignIntegrityError) as raised:
        CampaignService(workspace, target_repo=other).resume()
    assert "TARGET_REPOSITORY_IDENTITY_MISMATCH" in raised.value.diagnostic_codes


def test_handoff_resume_includes_target_and_rejects_later_drift(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    workspace = tmp_path / "campaign"
    CampaignService(workspace, target_repo=repo).initialize(_state())

    created = CampaignHandoffService(workspace).create(
        allowed_next_actions=("agent reviews current evidence",),
    )
    assert created.snapshot.state.target_snapshot is not None
    assert created.handoff.current_state.target_snapshot == created.snapshot.state.target_snapshot

    (repo / "tracked.txt").write_text("drift after handoff\n", encoding="utf-8")
    with pytest.raises(CampaignIntegrityError) as raised:
        CampaignHandoffService(workspace).resume()
    assert "TARGET_SNAPSHOT_DRIFT" in raised.value.diagnostic_codes


def test_cli_init_and_lineage_surface_target_binding(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    workspace = tmp_path / "campaign"
    runner = CliRunner()

    created = runner.invoke(
        cli,
        [
            "campaign", "init",
            "--workspace", str(workspace),
            "--campaign-id", "CMP-CLI-TARGET",
            "--mission", "prove durable target provenance",
            "--target-repo", str(repo),
            "--json",
        ],
    )
    assert created.exit_code == 0, created.output
    bound = CampaignService(workspace).resume()
    assert bound.state.target_snapshot is not None

    (repo / "tracked.txt").write_text("cli bounded work\n", encoding="utf-8")
    service = CampaignService(workspace)
    current = service.resume_for_transition().state
    service.record_transition(
        new_state=replace(current, current_state="recorded"),
        transition=TransitionRecord(
            id="CLI-T1",
            from_state="initialized",
            to_state="recorded",
            evidence=(),
            decision="agent records CLI fixture work",
            authority=current.authority,
        ),
    )

    lineage = runner.invoke(
        cli,
        ["campaign", "lineage", "--workspace", str(workspace), "--json"],
    )
    assert lineage.exit_code == 0, lineage.output
    payload = json.loads(lineage.output)
    assert payload["target_snapshot"]["repository_id"] == bound.state.target_snapshot.repository_id
    assert payload["target_snapshot_sha256"]
    assert payload["transitions"][0]["from_target_snapshot_sha256"]
    assert payload["transitions"][0]["to_target_snapshot_sha256"]


def test_untracked_nonignored_bytes_are_part_of_target_snapshot(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    clean = capture_target_snapshot(repo)
    (repo / "untracked.txt").write_text("untracked evidence\n", encoding="utf-8")
    untracked = capture_target_snapshot(repo)
    assert untracked.worktree_sha256 != clean.worktree_sha256
    assert untracked.dirty is True

    (repo / ".gitignore").write_text("ignored.txt\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore rule")
    before_ignored = capture_target_snapshot(repo)
    (repo / "ignored.txt").write_text("ignored bytes\n", encoding="utf-8")
    after_ignored = capture_target_snapshot(repo)
    assert after_ignored == before_ignored
