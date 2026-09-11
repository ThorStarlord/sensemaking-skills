"""Deterministic terminal Campaign completion receipts and archive markers.

Completion observes a terminal decision that already exists. It never closes a
Campaign, decides whether the terminal decision was correct, or equates archive
with success. Archive is a durable marker only; no workspace files are moved or
deleted.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from sensemaking_skills.campaign_semantics import target_snapshot_sha256

from .preflight import CampaignPreflightService
from .provenance_graph import CampaignProvenanceGraphService
from .target_snapshot import CampaignService


COMPLETION_RECEIPT_FILENAME = "completion-receipt.json"
ARCHIVE_RECEIPT_FILENAME = "archive-receipt.json"
COMPLETION_VERSION = "1"
_EXCLUDED_TOP_LEVEL = frozenset({COMPLETION_RECEIPT_FILENAME, ARCHIVE_RECEIPT_FILENAME, ".transactions"})


@dataclass(frozen=True)
class CompletionInspection:
    campaign_id: str
    valid: bool
    present: bool
    receipt_sha256: str | None
    payload: Mapping[str, Any] | None
    diagnostics: tuple[str, ...] = ()
    semantic_truth_established: bool = False


@dataclass(frozen=True)
class ArchiveInspection:
    campaign_id: str | None
    valid: bool
    present: bool
    archive_sha256: str | None
    diagnostics: tuple[str, ...] = ()
    semantic_success_established: bool = False


def _canonical_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _file_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _workspace_manifest(workspace: Path) -> tuple[list[dict[str, Any]], str]:
    entries: list[dict[str, Any]] = []
    for path in sorted(workspace.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(workspace)
        if not relative.parts or relative.parts[0] in _EXCLUDED_TOP_LEVEL:
            continue
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise ValueError(f"completion receipt refuses symlinked workspace content: {relative.as_posix()}")
        if not stat.S_ISREG(info.st_mode):
            continue
        entries.append(
            {
                "path": relative.as_posix(),
                "size": info.st_size,
                "sha256": _file_sha256(path),
            }
        )
    manifest_core: dict[str, Any] = {"files": entries}
    return entries, _digest(manifest_core)


def _read_json(path: Path) -> Mapping[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"could not read {path.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain one JSON object")
    return value


def _atomic_json(path: Path, value: Mapping[str, Any]) -> None:
    temp = path.with_name(f".{path.name}.tmp")
    temp.write_text(json.dumps(dict(value), indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    with temp.open("rb") as handle:
        os.fsync(handle.fileno())
    os.replace(temp, path)


def _receipt_core(workspace: Path) -> dict[str, Any]:
    snapshot = CampaignService(workspace).resume()
    state = snapshot.state
    if state.status != "terminal" or state.terminal_state is None:
        raise ValueError("completion receipt requires an already-terminal Campaign; use campaign close for the semantic terminal decision")

    preflight = CampaignPreflightService(workspace).inspect()
    graph = CampaignProvenanceGraphService(workspace).build()
    files, manifest_sha256 = _workspace_manifest(workspace)
    target_sha = target_snapshot_sha256(state.target_snapshot) if state.target_snapshot is not None else None
    return {
        "receipt_version": COMPLETION_VERSION,
        "campaign_id": state.campaign_id,
        "campaign_schema_version": state.schema_version,
        "status": state.status,
        "current_state": state.current_state,
        "terminal_state": state.terminal_state.value,
        "transition_count": len(snapshot.transitions),
        "final_transition_id": snapshot.transitions[-1].id if snapshot.transitions else None,
        "evidence_refs": list(snapshot.evidence_refs),
        "deferred_responsibility_ids": [item.responsibility_id for item in state.deferred_responsibilities],
        "active_uncertainty_id": state.active_uncertainty.id if state.active_uncertainty is not None else None,
        "primary_target_snapshot_sha256": target_sha,
        "preflight_ready": preflight.ready,
        "preflight_checks": [{"id": item.id, "status": item.status} for item in preflight.checks],
        "provenance_graph_valid": graph.valid,
        "workspace_manifest_sha256": manifest_sha256,
        "workspace_files": files,
        "semantic_truth_established": False,
        "semantic_success_established": False,
    }


def _expected_receipt(workspace: Path) -> dict[str, Any]:
    core = _receipt_core(workspace)
    return {**core, "receipt_sha256": _digest(core)}


def inspect_archive_marker(workspace: str | Path) -> ArchiveInspection:
    root = Path(workspace).resolve()
    path = root / ARCHIVE_RECEIPT_FILENAME
    if not path.exists():
        return ArchiveInspection(None, True, False, None)
    try:
        value = _read_json(path)
    except ValueError as exc:
        return ArchiveInspection(None, False, True, None, (str(exc),))
    required = {
        "archive_version",
        "campaign_id",
        "terminal_state",
        "completion_receipt_sha256",
        "archived",
        "semantic_success_established",
        "archive_sha256",
    }
    diagnostics: list[str] = []
    if set(value) != required:
        diagnostics.append("ARCHIVE_FIELDS_INVALID")
    core = {key: value[key] for key in required if key != "archive_sha256" and key in value}
    if value.get("archive_sha256") != _digest(core):
        diagnostics.append("ARCHIVE_DIGEST_MISMATCH")
    if value.get("archived") is not True:
        diagnostics.append("ARCHIVE_MARKER_INVALID")
    if value.get("semantic_success_established") is not False:
        diagnostics.append("ARCHIVE_SEMANTIC_AUTHORITY_INVALID")
    completion_path = root / COMPLETION_RECEIPT_FILENAME
    if not completion_path.exists():
        diagnostics.append("ARCHIVE_COMPLETION_RECEIPT_MISSING")
    else:
        try:
            completion = _read_json(completion_path)
        except ValueError:
            diagnostics.append("ARCHIVE_COMPLETION_RECEIPT_INVALID")
        else:
            if value.get("completion_receipt_sha256") != completion.get("receipt_sha256"):
                diagnostics.append("ARCHIVE_COMPLETION_RECEIPT_MISMATCH")
    return ArchiveInspection(
        str(value.get("campaign_id")) if isinstance(value.get("campaign_id"), str) else None,
        not diagnostics,
        True,
        str(value.get("archive_sha256")) if isinstance(value.get("archive_sha256"), str) else None,
        tuple(diagnostics),
    )


class CampaignCompletionService:
    """Build, verify, and archive terminal Campaign mechanical state."""

    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace).resolve()
        self.receipt_path = self.workspace / COMPLETION_RECEIPT_FILENAME
        self.archive_path = self.workspace / ARCHIVE_RECEIPT_FILENAME

    def closeout(self) -> CompletionInspection:
        expected = _expected_receipt(self.workspace)
        _atomic_json(self.receipt_path, expected)
        return self.inspect_receipt()

    def inspect_receipt(self) -> CompletionInspection:
        snapshot = CampaignService(self.workspace).resume()
        campaign_id = snapshot.state.campaign_id
        if not self.receipt_path.exists():
            return CompletionInspection(campaign_id, False, False, None, None, ("COMPLETION_RECEIPT_MISSING",))
        try:
            actual = _read_json(self.receipt_path)
            expected = _expected_receipt(self.workspace)
        except ValueError as exc:
            return CompletionInspection(campaign_id, False, True, None, None, (str(exc),))
        diagnostics: list[str] = []
        if actual != expected:
            diagnostics.append("COMPLETION_RECEIPT_CURRENT_STATE_MISMATCH")
        receipt_sha = actual.get("receipt_sha256")
        return CompletionInspection(
            campaign_id,
            not diagnostics,
            True,
            str(receipt_sha) if isinstance(receipt_sha, str) else None,
            actual,
            tuple(diagnostics),
        )

    def archive(self) -> ArchiveInspection:
        receipt = self.inspect_receipt()
        if not receipt.valid or receipt.payload is None or receipt.receipt_sha256 is None:
            raise ValueError("archive requires a valid completion receipt for the current terminal Campaign state")
        terminal_state = receipt.payload.get("terminal_state")
        core = {
            "archive_version": COMPLETION_VERSION,
            "campaign_id": receipt.campaign_id,
            "terminal_state": terminal_state,
            "completion_receipt_sha256": receipt.receipt_sha256,
            "archived": True,
            "semantic_success_established": False,
        }
        marker = {**core, "archive_sha256": _digest(core)}
        if self.archive_path.exists():
            existing = _read_json(self.archive_path)
            if existing != marker:
                raise ValueError("archive marker already exists with different content")
        else:
            _atomic_json(self.archive_path, marker)
        return inspect_archive_marker(self.workspace)
