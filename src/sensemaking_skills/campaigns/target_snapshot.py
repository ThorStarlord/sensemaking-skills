"""Durable Git target snapshot capture and target-aware Campaign lifecycle.

Target binding is mechanical provenance. It records exactly which repository
identity and working-tree state a Campaign concerns, detects unrecorded drift,
and binds lifecycle edges to source/destination target snapshot digests. It does
not decide whether repository changes are correct, warranted, sufficient, or
which capability should run next.
"""

from __future__ import annotations

import hashlib
import os
import stat
import subprocess
from dataclasses import replace
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from sensemaking_skills.campaign_semantics import (
    CampaignState,
    TargetSnapshot,
    TransitionRecord,
    target_snapshot_sha256,
)

from .errors import CampaignIntegrityError, CampaignTransactionError, CampaignWorkspaceError
from .service import (
    CampaignDiagnostic,
    CampaignService as BaseCampaignService,
    CampaignSnapshot,
    CampaignValidationResult,
)


def _git(root: Path, *args: str, allow_failure: bool = False) -> bytes | None:
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        raise CampaignWorkspaceError(f"could not execute git for target repository: {exc}") from exc
    if completed.returncode != 0:
        if allow_failure:
            return None
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise CampaignWorkspaceError(
            f"target repository git command failed ({' '.join(args)}): {detail or completed.returncode}"
        )
    return completed.stdout


def _text_git(root: Path, *args: str, allow_failure: bool = False) -> str | None:
    raw = _git(root, *args, allow_failure=allow_failure)
    if raw is None:
        return None
    return raw.decode("utf-8", errors="strict").strip()


def _sanitize_remote(value: str) -> str:
    """Remove credentials/query/fragment while preserving repository identity."""
    value = value.strip()
    if "://" in value:
        parsed = urlsplit(value)
        host = parsed.hostname or ""
        if parsed.port is not None:
            host = f"{host}:{parsed.port}"
        return urlunsplit((parsed.scheme.lower(), host.lower(), parsed.path.rstrip("/"), "", ""))
    # SCP-like Git URL: git@github.com:owner/repo.git -> github.com:owner/repo.git
    if "@" in value and ":" in value.split("@", 1)[1]:
        value = value.split("@", 1)[1]
    return value.rstrip("/")


def _identity(root: Path) -> tuple[str, str]:
    origin = _text_git(root, "config", "--get", "remote.origin.url", allow_failure=True)
    if origin:
        source = "origin"
        locator = _sanitize_remote(origin)
    else:
        source = "local_path"
        locator = os.path.normcase(str(root.resolve(strict=True)))
    digest = hashlib.sha256(f"{source}\0{locator}".encode("utf-8")).hexdigest()
    return source, digest


def _feed(hasher: Any, label: bytes, data: bytes) -> None:
    hasher.update(len(label).to_bytes(4, "big"))
    hasher.update(label)
    hasher.update(len(data).to_bytes(8, "big"))
    hasher.update(data)


def _file_digest(path: Path) -> bytes:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest().encode("ascii")


def _worktree_digest(root: Path) -> tuple[str, bool]:
    """Hash Git index/status plus tracked and untracked non-ignored bytes."""
    index = _git(root, "ls-files", "-s", "-z") or b""
    status_bytes = _git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all") or b""
    paths_raw = _git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard") or b""
    paths = sorted(item for item in paths_raw.split(b"\0") if item)

    hasher = hashlib.sha256()
    _feed(hasher, b"git-index", index)
    _feed(hasher, b"git-status", status_bytes)

    for raw_path in paths:
        _feed(hasher, b"path", raw_path)
        relative = os.fsdecode(raw_path)
        path = root / relative
        try:
            info = path.lstat()
        except FileNotFoundError:
            _feed(hasher, b"kind", b"missing")
            continue
        mode = stat.S_IMODE(info.st_mode)
        _feed(hasher, b"mode", f"{mode:o}".encode("ascii"))
        if stat.S_ISLNK(info.st_mode):
            _feed(hasher, b"kind", b"symlink")
            _feed(hasher, b"target", os.fsencode(os.readlink(path)))
        elif stat.S_ISREG(info.st_mode):
            _feed(hasher, b"kind", b"file")
            _feed(hasher, b"sha256", _file_digest(path))
        elif stat.S_ISDIR(info.st_mode):
            _feed(hasher, b"kind", b"directory")
            sub_head = _text_git(path, "rev-parse", "HEAD", allow_failure=True)
            if sub_head:
                _feed(hasher, b"submodule-head", sub_head.encode("ascii"))
                sub_status = _git(path, "status", "--porcelain=v1", "-z", "--untracked-files=all", allow_failure=True)
                _feed(hasher, b"submodule-status", sub_status or b"")
        else:
            _feed(hasher, b"kind", f"special:{stat.S_IFMT(info.st_mode):o}".encode("ascii"))

    return hasher.hexdigest(), bool(status_bytes)


def capture_target_snapshot(target_repo: str | Path) -> TargetSnapshot:
    """Capture deterministic identity and Git/worktree state for one target."""
    requested = Path(target_repo).expanduser()
    try:
        requested = requested.resolve(strict=True)
    except OSError as exc:
        raise CampaignWorkspaceError(f"could not resolve target repository: {requested}: {exc}") from exc
    if not requested.is_dir():
        raise CampaignWorkspaceError(f"target repository is not a directory: {requested}")

    top = _text_git(requested, "rev-parse", "--show-toplevel")
    if not top:
        raise CampaignWorkspaceError(f"target repository is not a Git worktree: {requested}")
    root = Path(top).resolve(strict=True)
    head = _text_git(root, "rev-parse", "HEAD")
    tree = _text_git(root, "rev-parse", "HEAD^{tree}")
    if not head or not tree:
        raise CampaignWorkspaceError("target repository must have a resolvable HEAD and tree")
    identity_source, repository_id = _identity(root)
    worktree_sha256, dirty = _worktree_digest(root)
    return TargetSnapshot(
        repository_root=str(root),
        repository_id=repository_id,
        identity_source=identity_source,
        head_sha=head,
        tree_sha=tree,
        worktree_sha256=worktree_sha256,
        dirty=dirty,
    )


def target_snapshots_equivalent(expected: TargetSnapshot, actual: TargetSnapshot) -> bool:
    """Compare identity/state while treating repository_root as a locator hint."""
    return (
        expected.repository_id == actual.repository_id
        and expected.identity_source == actual.identity_source
        and expected.vcs == actual.vcs
        and expected.head_sha == actual.head_sha
        and expected.tree_sha == actual.tree_sha
        and expected.worktree_sha256 == actual.worktree_sha256
        and expected.dirty == actual.dirty
    )


class CampaignService(BaseCampaignService):
    """Campaign lifecycle with durable target provenance and drift detection."""

    def __init__(self, workspace: str | Path, *, target_repo: str | Path | None = None) -> None:
        super().__init__(workspace, target_repo=target_repo)
        self._explicit_target = Path(target_repo).expanduser() if target_repo is not None else None
        self._allow_target_drift = False

    def initialize(self, state: CampaignState, *, policy=None) -> CampaignSnapshot:
        target = capture_target_snapshot(self._explicit_target) if self._explicit_target is not None else None
        if target is not None:
            if state.target_snapshot is not None and not target_snapshots_equivalent(state.target_snapshot, target):
                raise CampaignTransactionError(
                    "campaign initialization target_snapshot disagrees with --target-repo"
                )
            state = replace(state, target_snapshot=target)
        return super().initialize(state, policy=policy)

    def _target_path(self, snapshot: TargetSnapshot) -> Path:
        return self._explicit_target if self._explicit_target is not None else Path(snapshot.repository_root)

    @staticmethod
    def _history_diagnostics(snapshot: CampaignSnapshot) -> list[CampaignDiagnostic]:
        diagnostics: list[CampaignDiagnostic] = []
        previous_digest: str | None = None
        bound_seen = False
        for transition in snapshot.transitions:
            source = transition.from_target_snapshot_sha256
            destination = transition.to_target_snapshot_sha256
            if (source is None) != (destination is None):
                diagnostics.append(
                    CampaignDiagnostic(
                        "TARGET_TRANSITION_BINDING_INCOMPLETE",
                        f"transition {transition.id!r} must bind both source and destination target snapshots",
                    )
                )
                continue
            if source is None:
                if bound_seen:
                    diagnostics.append(
                        CampaignDiagnostic(
                            "TARGET_TRANSITION_BINDING_REGRESSION",
                            f"transition {transition.id!r} drops target provenance after binding began",
                        )
                    )
                continue
            bound_seen = True
            if previous_digest is not None and source != previous_digest:
                diagnostics.append(
                    CampaignDiagnostic(
                        "TARGET_TRANSITION_CHAIN_MISMATCH",
                        f"transition {transition.id!r} source target digest does not match prior destination",
                    )
                )
            previous_digest = destination

        current_target = snapshot.state.target_snapshot
        current_digest = target_snapshot_sha256(current_target) if current_target is not None else None
        if bound_seen:
            if current_digest is None:
                diagnostics.append(
                    CampaignDiagnostic(
                        "TARGET_SNAPSHOT_MISSING",
                        "target-bound transition history requires a current target snapshot",
                    )
                )
            elif previous_digest != current_digest:
                diagnostics.append(
                    CampaignDiagnostic(
                        "TARGET_CURRENT_SNAPSHOT_MISMATCH",
                        "current target snapshot does not match the final transition destination",
                    )
                )
        return diagnostics

    def _live_diagnostics(self, snapshot: CampaignSnapshot) -> list[CampaignDiagnostic]:
        expected = snapshot.state.target_snapshot
        if expected is None:
            return []
        try:
            actual = capture_target_snapshot(self._target_path(expected))
        except CampaignWorkspaceError as exc:
            return [CampaignDiagnostic("TARGET_REPOSITORY_UNAVAILABLE", str(exc))]
        if actual.repository_id != expected.repository_id or actual.identity_source != expected.identity_source:
            return [
                CampaignDiagnostic(
                    "TARGET_REPOSITORY_IDENTITY_MISMATCH",
                    "live target repository identity does not match the Campaign target identity",
                )
            ]
        if not target_snapshots_equivalent(expected, actual):
            return [
                CampaignDiagnostic(
                    "TARGET_SNAPSHOT_DRIFT",
                    "live target repository state differs from the last durably recorded Campaign target snapshot",
                )
            ]
        return []

    @staticmethod
    def _raise_target(diagnostics: list[CampaignDiagnostic]) -> None:
        if diagnostics:
            raise CampaignIntegrityError(
                "target-bound campaign reconstruction failed",
                diagnostic_codes=tuple(item.code for item in diagnostics),
            )

    def resume_for_transition(self) -> CampaignSnapshot:
        """Reconstruct durable history while permitting a new live post-work snapshot."""
        snapshot = super().resume()
        self._raise_target(self._history_diagnostics(snapshot))
        return snapshot

    def resume(self) -> CampaignSnapshot:
        snapshot = self.resume_for_transition()
        if not self._allow_target_drift:
            self._raise_target(self._live_diagnostics(snapshot))
        return snapshot

    def validate(self) -> CampaignValidationResult:
        base = super().validate()
        if not base.valid:
            return base
        snapshot = super().resume()
        diagnostics = [*self._history_diagnostics(snapshot), *self._live_diagnostics(snapshot)]
        if not diagnostics:
            return base
        return CampaignValidationResult(False, (*base.diagnostics, *diagnostics))

    def _capture_transition_target(self, current: CampaignState) -> TargetSnapshot | None:
        expected = current.target_snapshot
        if expected is None and self._explicit_target is None:
            return None
        path = self._explicit_target if self._explicit_target is not None else Path(expected.repository_root)  # type: ignore[union-attr]
        actual = capture_target_snapshot(path)
        if expected is not None and (
            actual.repository_id != expected.repository_id
            or actual.identity_source != expected.identity_source
        ):
            raise CampaignTransactionError(
                "live target repository identity differs from the Campaign target identity"
            )
        return actual

    def record_transition(self, *, new_state: CampaignState, transition: TransitionRecord) -> CampaignSnapshot:
        snapshot = self.resume_for_transition()
        current = snapshot.state
        destination = self._capture_transition_target(current)
        source = current.target_snapshot

        if destination is None:
            if new_state.target_snapshot is not None:
                raise CampaignTransactionError(
                    "target_snapshot cannot be agent-authored for an unbound Campaign without --target-repo"
                )
            normalized_state = new_state
            source_digest = None
            destination_digest = None
        else:
            if new_state.target_snapshot is not None:
                allowed = (
                    (source is not None and target_snapshots_equivalent(new_state.target_snapshot, source))
                    or target_snapshots_equivalent(new_state.target_snapshot, destination)
                )
                if not allowed:
                    raise CampaignTransactionError(
                        "new_state.target_snapshot disagrees with mechanically captured target state"
                    )
            normalized_state = replace(new_state, target_snapshot=destination)
            source_digest = target_snapshot_sha256(source) if source is not None else None
            destination_digest = target_snapshot_sha256(destination)

        authored_from = transition.from_target_snapshot_sha256
        authored_to = transition.to_target_snapshot_sha256
        if authored_from is not None and authored_from != source_digest:
            raise CampaignTransactionError(
                "transition source target digest disagrees with current Campaign target snapshot"
            )
        if authored_to is not None and authored_to != destination_digest:
            raise CampaignTransactionError(
                "transition destination target digest disagrees with mechanically captured target snapshot"
            )
        if (source_digest is None) != (destination_digest is None):
            # First binding edge for a legacy targetless Campaign cannot prove a
            # pre-existing source snapshot. Persist the binding in state and let
            # the next edge begin fully bound rather than inventing provenance.
            normalized_transition = transition
        else:
            normalized_transition = replace(
                transition,
                from_target_snapshot_sha256=source_digest,
                to_target_snapshot_sha256=destination_digest,
            )

        self._allow_target_drift = True
        try:
            super().record_transition(
                new_state=normalized_state,
                transition=normalized_transition,
            )
        finally:
            self._allow_target_drift = False
        return self.resume()

    def defer_responsibility(self, *args: Any, **kwargs: Any) -> CampaignSnapshot:
        self._allow_target_drift = True
        try:
            return super().defer_responsibility(*args, **kwargs)
        finally:
            self._allow_target_drift = False

    def terminate(self, *args: Any, **kwargs: Any) -> CampaignSnapshot:
        self._allow_target_drift = True
        try:
            return super().terminate(*args, **kwargs)
        finally:
            self._allow_target_drift = False
