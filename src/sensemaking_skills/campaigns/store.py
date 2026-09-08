"""Durable file-backed storage for campaign-semantic artifacts.

Storage is intentionally non-semantic: it validates typed contracts, preserves
append-only history, and writes current snapshots atomically. Selecting the next
responsibility or capability remains an agent decision.

P2 adds a small durable transaction journal. Publishing a fully prepared journal
directory is the commit-intent boundary; live files are then materialized in an
idempotent order with ``campaign-state.yaml`` last. A crash after commit intent
is recoverable without guessing semantic intent.

P4 distinguishes raw evidence from validated artifacts. Files under ``evidence/``
remain ordinary durable evidence. Files under ``artifacts/`` become evidence only
when an append-only admission receipt binds their exact digest to a successful
canonical validator result.
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

from .admission import (
    ArtifactAdmissionContractError,
    load_artifact_admission,
    sha256_file,
)
from .errors import (
    CampaignAlreadyExistsError,
    CampaignIdentityError,
    CampaignIntegrityError,
    CampaignNotInitializedError,
    CampaignTransactionError,
    CampaignWorkspaceError,
)
from .workspace import CampaignWorkspace

_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def _assert_physically_contained(path: Path, root: Path) -> None:
    """Fail closed unless ``path`` resolves physically beneath ``root``."""
    try:
        resolved, failure = pc.resolve_containment(path, root)
    except Exception as exc:  # pragma: no cover - defensive fail-closed guard
        raise CampaignWorkspaceError(
            f"could not establish physical containment for {path}: {exc}"
        ) from exc

    if failure is not None or resolved is None:
        raise CampaignWorkspaceError(
            "campaign path is not physically contained: "
            f"path={path} root={root} failure={failure}"
        )

    try:
        real_root = root.resolve(strict=False)
    except OSError as exc:
        raise CampaignWorkspaceError(
            f"could not resolve campaign root {root}: {exc}"
        ) from exc

    canon_resolved = pc.canonicalize_path(resolved)
    canon_root = pc.canonicalize_path(real_root)
    if canon_resolved.relative_to_root(canon_root) is None:
        raise CampaignWorkspaceError(
            "campaign path is outside its physical root: "
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
        yaml.safe_dump(dict(payload), handle, sort_keys=False, allow_unicode=True)
        handle.flush()
        os.fsync(handle.fileno())


def _atomic_write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            yaml.safe_dump(dict(payload), handle, sort_keys=False, allow_unicode=True)
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
        raise CampaignWorkspaceError(
            f"append-only record already exists: {path.name}"
        ) from exc
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump(dict(payload), handle, sort_keys=False, allow_unicode=True)
        handle.flush()
        os.fsync(handle.fileno())


def _trace_is_one_event_extension(current: CampaignTrace, prepared: CampaignTrace) -> bool:
    return (
        prepared.campaign_id == current.campaign_id
        and prepared.schema_version == current.schema_version
        and prepared.replication_id == current.replication_id
        and prepared.initial_state == current.initial_state
        and prepared.extensions == current.extensions
        and len(prepared.events) == len(current.events) + 1
        and prepared.events[:-1] == current.events
    )


class CampaignStore:
    """Persist one campaign without selecting or executing campaign work."""

    def __init__(self, workspace: str | Path, *, target_repo: str | Path | None = None):
        self.workspace = CampaignWorkspace(
            Path(workspace), Path(target_repo) if target_repo is not None else None
        )

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
            (staging / ".transactions").mkdir()
            (staging / "artifacts").mkdir()
            (staging / "evidence").mkdir()
            (staging / "admissions").mkdir()
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
        """Append one immutable transition outside a P2 lifecycle transaction."""
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
        """Return durable evidence refs, requiring admission for artifact files."""
        self._require_initialized()
        current = self.load_state()
        refs: list[str] = []

        # Raw evidence remains directly citable. Preserve the P1 physical-
        # containment guard so symlink/reparse escapes fail closed.
        evidence_dir = self.workspace.evidence_dir
        _assert_physically_contained(evidence_dir, self.root)
        for path in sorted(evidence_dir.rglob("*")):
            _assert_physically_contained(path, evidence_dir)
            if path.is_file():
                refs.append(path.relative_to(self.root).as_posix())

        # Scan artifacts for containment, but deliberately do not grant evidence
        # status merely because a file exists here. P4 admission receipts below
        # are the only authority that promotes an artifact into evidence.
        artifacts_dir = self.workspace.artifacts_dir
        _assert_physically_contained(artifacts_dir, self.root)
        for path in sorted(artifacts_dir.rglob("*")):
            _assert_physically_contained(path, artifacts_dir)

        admissions_dir = self.workspace.admissions_dir
        if not admissions_dir.is_dir():
            raise CampaignIntegrityError(
                "campaign admissions directory is missing",
                diagnostic_codes=("ARTIFACT_ADMISSIONS_DIRECTORY_MISSING",),
            )
        _assert_physically_contained(admissions_dir, self.root)
        for path in sorted(admissions_dir.rglob("*")):
            _assert_physically_contained(path, admissions_dir)
            if path.is_dir():
                continue
            if path.is_symlink() or not path.is_file() or path.suffix != ".yaml":
                raise CampaignIntegrityError(
                    "artifact admissions directory contains an invalid entry",
                    diagnostic_codes=("INVALID_ARTIFACT_ADMISSION",),
                )
            try:
                admission = load_artifact_admission(path)
            except (ArtifactAdmissionContractError, OSError, yaml.YAMLError) as exc:
                raise CampaignIntegrityError(
                    "artifact admission receipt is invalid",
                    diagnostic_codes=("INVALID_ARTIFACT_ADMISSION",),
                ) from exc
            if admission.campaign_id != current.campaign_id:
                raise CampaignIntegrityError(
                    "artifact admission belongs to a different campaign",
                    diagnostic_codes=("ARTIFACT_ADMISSION_CAMPAIGN_ID_MISMATCH",),
                )

            artifact_path = self.root / admission.artifact_ref
            _assert_physically_contained(artifact_path, artifacts_dir)
            if artifact_path.is_symlink() or not artifact_path.is_file():
                raise CampaignIntegrityError(
                    "admitted artifact is missing or not a regular file",
                    diagnostic_codes=("ADMITTED_ARTIFACT_MISSING",),
                )
            if sha256_file(artifact_path) != admission.artifact_sha256:
                raise CampaignIntegrityError(
                    "admitted artifact no longer matches its admission digest",
                    diagnostic_codes=("ADMITTED_ARTIFACT_DIGEST_MISMATCH",),
                )

            refs.append(admission.artifact_ref)
            refs.append(path.relative_to(self.root).as_posix())

        return tuple(sorted(dict.fromkeys(refs)))

    def commit_lifecycle(
        self,
        *,
        state: CampaignState,
        transition: TransitionRecord,
        trace: CampaignTrace,
    ) -> Path:
        """Commit transition+trace+state with durable, crash-recoverable intent."""
        self._require_initialized()
        self.recover_lifecycle_transactions()
        current = self.load_state()
        if not _SAFE_ID.fullmatch(transition.id):
            raise CampaignTransactionError("unsafe transition id for lifecycle commit")
        if state.campaign_id != current.campaign_id or trace.campaign_id != current.campaign_id:
            raise CampaignIdentityError("lifecycle transaction campaign identity mismatch")

        state_payload = _validated_state_payload(state)
        transition_payload = _validated_transition_payload(transition)
        trace_payload = _validated_trace_payload(trace)

        final_transition = self.workspace.transitions_dir / f"{transition.id}.yaml"
        if os.path.lexists(final_transition):
            raise CampaignTransactionError(
                f"transition id already committed: {transition.id}"
            )

        transactions_dir = self.workspace.transactions_dir
        transactions_dir.mkdir(parents=True, exist_ok=True)
        _assert_physically_contained(transactions_dir, self.root)
        transaction_dir = transactions_dir / transition.id
        if os.path.lexists(transaction_dir):
            raise CampaignTransactionError(
                f"pending lifecycle transaction already exists: {transition.id}"
            )

        staging = Path(
            tempfile.mkdtemp(prefix=f".{transition.id}.staging-", dir=transactions_dir)
        )
        published = False
        try:
            _write_yaml(staging / "campaign-state.yaml", state_payload)
            _write_yaml(staging / "transition.yaml", transition_payload)
            _write_yaml(staging / "trace.yaml", trace_payload)
            try:
                os.replace(staging, transaction_dir)
            except OSError as exc:
                raise CampaignTransactionError(
                    f"could not publish lifecycle commit intent for {transition.id}: {exc}"
                ) from exc
            published = True
        finally:
            if not published and staging.exists():
                shutil.rmtree(staging)

        try:
            self._apply_lifecycle_transaction(transaction_dir)
        except Exception as exc:
            if isinstance(exc, CampaignTransactionError):
                detail = str(exc)
            else:
                detail = repr(exc)
            raise CampaignTransactionError(
                "lifecycle commit intent is durable but materialization is pending; "
                f"resume/recovery must complete transition {transition.id}: {detail}"
            ) from exc
        return final_transition

    def recover_lifecycle_transactions(self) -> tuple[str, ...]:
        """Complete every published P2 transaction idempotently."""
        self._require_initialized()
        transactions_dir = self.workspace.transactions_dir
        transactions_dir.mkdir(parents=True, exist_ok=True)
        _assert_physically_contained(transactions_dir, self.root)

        # Unpublished staging directories carry no commit intent.
        for entry in tuple(transactions_dir.iterdir()):
            if entry.name.startswith(".") and ".staging-" in entry.name:
                if entry.is_symlink():
                    entry.unlink()
                elif entry.is_dir():
                    shutil.rmtree(entry)
                else:
                    entry.unlink()

        recovered: list[str] = []
        for transaction_dir in sorted(
            entry for entry in transactions_dir.iterdir() if not entry.name.startswith(".")
        ):
            if (
                transaction_dir.is_symlink()
                or not transaction_dir.is_dir()
                or not _SAFE_ID.fullmatch(transaction_dir.name)
            ):
                raise CampaignTransactionError(
                    f"invalid transaction journal entry: {transaction_dir.name}"
                )
            _assert_physically_contained(transaction_dir, transactions_dir)
            try:
                self._apply_lifecycle_transaction(transaction_dir)
            except Exception as exc:
                raise CampaignTransactionError(
                    f"failed to recover lifecycle transaction {transaction_dir.name}: {exc}"
                ) from exc
            recovered.append(transaction_dir.name)
        return tuple(recovered)

    def _apply_lifecycle_transaction(self, transaction_dir: Path) -> None:
        _assert_physically_contained(transaction_dir, self.workspace.transactions_dir)
        state_path = transaction_dir / "campaign-state.yaml"
        transition_path = transaction_dir / "transition.yaml"
        trace_path = transaction_dir / "trace.yaml"
        for prepared_path in (state_path, transition_path, trace_path):
            _assert_physically_contained(prepared_path, transaction_dir)
            if not prepared_path.is_file():
                raise CampaignTransactionError(
                    f"prepared lifecycle artifact is missing: {prepared_path.name}"
                )

        prepared_state = load_campaign_state(state_path)
        prepared_transition = load_transition_record(transition_path)
        prepared_trace = load_campaign_trace(trace_path)
        current_state = self.load_state()
        current_trace = self.load_trace()

        if prepared_transition.id != transaction_dir.name:
            raise CampaignTransactionError("transaction directory/id mismatch")
        if not (
            prepared_state.campaign_id
            == prepared_trace.campaign_id
            == current_state.campaign_id
        ):
            raise CampaignIdentityError(
                "prepared lifecycle artifacts disagree on campaign_id"
            )
        if (
            current_state != prepared_state
            and current_state.current_state != prepared_transition.from_state
        ):
            raise CampaignTransactionError(
                "live campaign state is neither the transaction source nor the exact prepared state"
            )

        final_transition = self.workspace.transitions_dir / f"{prepared_transition.id}.yaml"
        _assert_physically_contained(final_transition, self.workspace.transitions_dir)
        if os.path.lexists(final_transition):
            if not final_transition.is_file():
                raise CampaignTransactionError("committed transition path is not a file")
            if load_transition_record(final_transition) != prepared_transition:
                raise CampaignTransactionError(
                    "committed transition id has divergent content"
                )
        else:
            _exclusive_write_yaml(
                final_transition,
                _validated_transition_payload(prepared_transition),
            )

        if current_trace != prepared_trace:
            if not _trace_is_one_event_extension(current_trace, prepared_trace):
                raise CampaignTransactionError(
                    "prepared trace is not an exact one-event extension of live trace"
                )
            _atomic_write_yaml(
                self.workspace.trace_path,
                _validated_trace_payload(prepared_trace),
            )

        # Any existing handoff snapshots the pre-transition state. Absence is valid.
        if os.path.lexists(self.workspace.handoff_path):
            if self.workspace.handoff_path.is_dir():
                raise CampaignTransactionError(
                    "campaign handoff path is unexpectedly a directory"
                )
            self.workspace.handoff_path.unlink()

        # Publish the authoritative current-state snapshot last. Therefore an
        # observed advanced state always has its transition and trace history.
        current_state = self.load_state()
        if current_state != prepared_state:
            if current_state.current_state != prepared_transition.from_state:
                raise CampaignTransactionError(
                    "campaign state diverged during lifecycle commit"
                )
            _atomic_write_yaml(
                self.workspace.state_path,
                _validated_state_payload(prepared_state),
            )

        if self.load_state() != prepared_state:
            raise CampaignTransactionError(
                "campaign state verification failed after commit"
            )
        if load_transition_record(final_transition) != prepared_transition:
            raise CampaignTransactionError(
                "transition verification failed after commit"
            )
        if self.load_trace() != prepared_trace:
            raise CampaignTransactionError("trace verification failed after commit")

        shutil.rmtree(transaction_dir)
