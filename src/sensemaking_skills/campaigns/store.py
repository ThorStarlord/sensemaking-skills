"""Durable file-backed storage for campaign-semantic artifacts.

Storage is intentionally non-semantic: it validates typed contracts, preserves
append-only history, and writes current snapshots atomically.  Selecting the
next responsibility or capability remains an agent decision.
"""

from __future__ import annotations

import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any, Mapping

import yaml

from sensemaking_skills import path_containment as pc
from sensemaking_skills.campaign_semantics import (
    CampaignHandoff,
    CampaignPolicy,
    CampaignState,
    CampaignTrace,
    TransitionRecord,
    dump_campaign_handoff,
    dump_campaign_policy,
    dump_campaign_state,
    dump_campaign_trace,
    dump_transition_record,
    load_campaign_handoff,
    load_campaign_policy,
    load_campaign_state,
    load_campaign_trace,
    load_transition_record,
)

from .errors import (
    CampaignAlreadyExistsError,
    CampaignIdentityError,
    CampaignNotInitializedError,
    CampaignWorkspaceError,
)
from .workspace import CampaignWorkspace

_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def _assert_physically_contained(path: Path, root: Path) -> None:
    """Fail closed unless ``path`` resolves physically beneath ``root``.

    This reuses the repository's shared path-containment primitive so evidence
    enumeration cannot turn a symlink or Windows reparse point into an escape
    from the campaign workspace.
    """
    try:
        resolved, failure = pc.resolve_containment(path, root)
    except Exception as exc:  # pragma: no cover - defensive fail-closed guard
        raise CampaignWorkspaceError(
            f"could not establish physical containment for {path}: {exc}"
        ) from exc

    if failure is not None or resolved is None:
        raise CampaignWorkspaceError(
            "campaign evidence path is not physically contained: "
            f"path={path} root={root} failure={failure}"
        )

    try:
        real_root = root.resolve(strict=False)
    except OSError as exc:
        raise CampaignWorkspaceError(
            f"could not resolve campaign evidence root {root}: {exc}"
        ) from exc

    canon_resolved = pc.canonicalize_path(resolved)
    canon_root = pc.canonicalize_path(real_root)
    if canon_resolved.relative_to_root(canon_root) is None:
        raise CampaignWorkspaceError(
            "campaign evidence path is outside its physical root: "
            f"path={path} resolved={resolved} root={real_root}"
        )


def _validated_state_payload(state: CampaignState) -> dict[str, Any]:
    payload = dump_campaign_state(state)
    load_campaign_state(payload)
    return payload


def _validated_policy_payload(policy: CampaignPolicy) -> dict[str, Any]:
    payload = dump_campaign_policy(policy)
    load_campaign_policy(payload)
    return payload


def _validated_trace_payload(trace: CampaignTrace) -> dict[str, Any]:
    payload = dump_campaign_trace(trace)
    load_campaign_trace(payload)
    return payload


def _validated_transition_payload(transition: TransitionRecord) -> dict[str, Any]:
    payload = dump_transition_record(transition)
    load_transition_record(payload)
    return payload


def _validated_handoff_payload(handoff: CampaignHandoff) -> dict[str, Any]:
    payload = dump_campaign_handoff(handoff)
    load_campaign_handoff(payload)
    return payload


def _write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump(
            dict(payload),
            handle,
            sort_keys=False,
            allow_unicode=True,
        )
        handle.flush()
        os.fsync(handle.fileno())


def _atomic_write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            yaml.safe_dump(
                dict(payload),
                handle,
                sort_keys=False,
                allow_unicode=True,
            )
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def _exclusive_write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError as exc:
        raise CampaignWorkspaceError(f"append-only record already exists: {path.name}") from exc
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump(
            dict(payload),
            handle,
            sort_keys=False,
            allow_unicode=True,
        )
        handle.flush()
        os.fsync(handle.fileno())


class CampaignStore:
    """Persist one campaign without selecting or executing campaign work."""

    def __init__(self, workspace: str | Path, *, target_repo: str | Path | None = None):
        self.workspace = CampaignWorkspace(Path(workspace), Path(target_repo) if target_repo is not None else None)

    @property
    def root(self) -> Path:
        return self.workspace.root

    def is_initialized(self) -> bool:
        return self.workspace.state_path.is_file()

    def _require_initialized(self) -> None:
        if not self.is_initialized():
            raise CampaignNotInitializedError(
                f"campaign workspace is not initialized: {self.root}"
            )

    def initialize(
        self,
        state: CampaignState,
        *,
        policy: CampaignPolicy | None = None,
    ) -> None:
        """Create an isolated workspace as one directory-level commit."""
        self.workspace.assert_isolated_from_target()
        if os.path.lexists(self.workspace.requested_root):
            raise CampaignAlreadyExistsError(
                "campaign workspace already exists: "
                f"{self.workspace.requested_root}"
            )

        state_payload = _validated_state_payload(state)
        if policy is not None and policy.campaign_id != state.campaign_id:
            raise CampaignIdentityError(
                "campaign policy and state must use the same campaign_id"
            )
        policy_payload = _validated_policy_payload(policy) if policy is not None else None
        trace = CampaignTrace(
            campaign_id=state.campaign_id,
            initial_state=state.current_state,
        )
        trace_payload = _validated_trace_payload(trace)

        self.root.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(
            tempfile.mkdtemp(prefix=f".{self.root.name}.staging-", dir=self.root.parent)
        )
        try:
            (staging / "transitions").mkdir()
            (staging / "artifacts").mkdir()
            (staging / "evidence").mkdir()
            _write_yaml(staging / "campaign-state.yaml", state_payload)
            _write_yaml(staging / "trace.yaml", trace_payload)
            if policy_payload is not None:
                _write_yaml(staging / "campaign-policy.yaml", policy_payload)
            os.replace(staging, self.root)
        finally:
            if staging.exists():
                shutil.rmtree(staging)

    def load_state(self) -> CampaignState:
        self._require_initialized()
        return load_campaign_state(self.workspace.state_path)

    def save_state(self, state: CampaignState) -> None:
        self._require_initialized()
        current = self.load_state()
        if state.campaign_id != current.campaign_id:
            raise CampaignIdentityError(
                "replacement campaign state must preserve campaign_id"
            )
        _atomic_write_yaml(self.workspace.state_path, _validated_state_payload(state))

    def save_policy(self, policy: CampaignPolicy) -> None:
        current = self.load_state()
        if policy.campaign_id != current.campaign_id:
            raise CampaignIdentityError(
                "campaign policy and state must use the same campaign_id"
            )
        _atomic_write_yaml(self.workspace.policy_path, _validated_policy_payload(policy))

    def load_policy(self) -> CampaignPolicy:
        self._require_initialized()
        if not self.workspace.policy_path.is_file():
            raise CampaignNotInitializedError("campaign policy has not been written")
        policy = load_campaign_policy(self.workspace.policy_path)
        if policy.campaign_id != self.load_state().campaign_id:
            raise CampaignIdentityError("stored campaign policy has the wrong campaign_id")
        return policy

    def append_transition(self, transition: TransitionRecord) -> Path:
        """Append one immutable transition record.

        P1 intentionally does not update CampaignState here.  P2's service layer
        will own the atomic state+transition lifecycle operation.
        """
        self._require_initialized()
        if not _SAFE_ID.fullmatch(transition.id):
            raise CampaignWorkspaceError(
                "transition id must use only letters, numbers, '.', '_' or '-'"
            )
        path = self.workspace.transitions_dir / f"{transition.id}.yaml"
        _exclusive_write_yaml(path, _validated_transition_payload(transition))
        return path

    def load_transitions(self) -> tuple[TransitionRecord, ...]:
        self._require_initialized()
        records = [
            load_transition_record(path)
            for path in sorted(self.workspace.transitions_dir.glob("*.yaml"))
        ]
        ids = [record.id for record in records]
        if len(ids) != len(set(ids)):
            raise CampaignWorkspaceError("duplicate transition ids in workspace")
        return tuple(records)

    def load_trace(self) -> CampaignTrace:
        self._require_initialized()
        trace = load_campaign_trace(self.workspace.trace_path)
        if trace.campaign_id != self.load_state().campaign_id:
            raise CampaignIdentityError("stored campaign trace has the wrong campaign_id")
        return trace

    def append_trace_event(self, event: Mapping[str, Any]) -> None:
        if not isinstance(event, Mapping):
            raise CampaignWorkspaceError("trace event must be a mapping")
        trace = self.load_trace()
        updated = CampaignTrace(
            campaign_id=trace.campaign_id,
            events=(*trace.events, dict(event)),
            schema_version=trace.schema_version,
            replication_id=trace.replication_id,
            initial_state=trace.initial_state,
            terminal_state=trace.terminal_state,
            extensions=trace.extensions,
        )
        _atomic_write_yaml(self.workspace.trace_path, _validated_trace_payload(updated))

    def write_handoff(self, handoff: CampaignHandoff) -> None:
        current = self.load_state()
        if handoff.campaign_id != current.campaign_id:
            raise CampaignIdentityError(
                "campaign handoff and state must use the same campaign_id"
            )
        if handoff.current_state != current:
            raise CampaignIdentityError(
                "campaign handoff current_state must equal campaign-state.yaml"
            )
        _atomic_write_yaml(
            self.workspace.handoff_path,
            _validated_handoff_payload(handoff),
        )

    def load_handoff(self) -> CampaignHandoff:
        self._require_initialized()
        if not self.workspace.handoff_path.is_file():
            raise CampaignNotInitializedError("campaign handoff has not been written")
        current = self.load_state()
        handoff = load_campaign_handoff(self.workspace.handoff_path)
        if handoff.campaign_id != current.campaign_id:
            raise CampaignIdentityError("stored campaign handoff has the wrong campaign_id")
        if handoff.current_state != current:
            raise CampaignIdentityError(
                "stored campaign handoff current_state does not match campaign-state.yaml"
            )
        return handoff

    def evidence_refs(self) -> tuple[str, ...]:
        """Return stable workspace-relative file references available as evidence."""
        self._require_initialized()
        refs: list[str] = []
        for directory in (self.workspace.artifacts_dir, self.workspace.evidence_dir):
            _assert_physically_contained(directory, self.root)
            for path in sorted(directory.rglob("*")):
                _assert_physically_contained(path, directory)
                if path.is_file():
                    refs.append(path.relative_to(self.root).as_posix())
        return tuple(refs)
