"""Append-only Campaign uncertainty history without semantic ranking authority.

CampaignState.active_uncertainty remains the authority for the current active
uncertainty. This companion preserves agent-authored lifecycle observations and
mechanically validates their identifiers, evidence references, transition
references, and hash chain. It never selects which uncertainty should be active.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .target_snapshot import CampaignService


UNCERTAINTY_HISTORY_FILENAME = "uncertainty-history.jsonl"
UNCERTAINTY_HISTORY_VERSION = "1"
ALLOWED_STATUSES = frozenset({"active", "resolved", "deferred", "superseded", "abandoned"})
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


@dataclass(frozen=True)
class UncertaintyHistoryDiagnostic:
    code: str
    detail: str
    line: int | None = None


@dataclass(frozen=True)
class UncertaintyHistoryResult:
    campaign_id: str
    records: tuple[Mapping[str, Any], ...]
    diagnostics: tuple[UncertaintyHistoryDiagnostic, ...]
    latest_statuses: Mapping[str, str]
    semantic_recommendation_included: bool = False
    semantic_truth_established: bool = False

    @property
    def valid(self) -> bool:
        return not self.diagnostics


def _canonical_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _nonempty_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _safe_id(value: Any, field: str) -> str:
    text = _nonempty_text(value, field)
    if not _SAFE_ID.fullmatch(text):
        raise ValueError(f"{field} must use only letters, numbers, '.', '_' or '-'")
    return text


def _event_payload(
    *,
    event_id: str,
    uncertainty_id: str,
    status: str,
    transition_id: str | None,
    evidence_refs: tuple[str, ...],
    superseded_by: str | None,
    note: str | None,
) -> dict[str, Any]:
    return {
        "schema_version": UNCERTAINTY_HISTORY_VERSION,
        "event_id": event_id,
        "uncertainty_id": uncertainty_id,
        "status": status,
        "transition_id": transition_id,
        "evidence_refs": list(evidence_refs),
        "superseded_by": superseded_by,
        "note": note,
    }


def _validate_event(value: Any) -> tuple[dict[str, Any] | None, tuple[UncertaintyHistoryDiagnostic, ...]]:
    diagnostics: list[UncertaintyHistoryDiagnostic] = []
    if not isinstance(value, Mapping):
        return None, (UncertaintyHistoryDiagnostic("UNCERTAINTY_HISTORY_EVENT_INVALID", "event must be an object"),)
    data = dict(value)
    required = {
        "schema_version",
        "event_id",
        "uncertainty_id",
        "status",
        "transition_id",
        "evidence_refs",
        "superseded_by",
        "note",
    }
    unknown = sorted(set(data) - required)
    missing = sorted(required - set(data))
    if unknown or missing:
        diagnostics.append(
            UncertaintyHistoryDiagnostic(
                "UNCERTAINTY_HISTORY_EVENT_FIELDS_INVALID",
                f"unknown={unknown} missing={missing}",
            )
        )
        return data, tuple(diagnostics)
    if data.get("schema_version") != UNCERTAINTY_HISTORY_VERSION:
        diagnostics.append(
            UncertaintyHistoryDiagnostic(
                "UNCERTAINTY_HISTORY_VERSION_UNSUPPORTED",
                f"unsupported schema_version {data.get('schema_version')!r}",
            )
        )
    for field in ("event_id", "uncertainty_id"):
        try:
            _safe_id(data.get(field), field)
        except ValueError as exc:
            diagnostics.append(UncertaintyHistoryDiagnostic("UNCERTAINTY_HISTORY_ID_INVALID", str(exc)))
    status = data.get("status")
    if status not in ALLOWED_STATUSES:
        diagnostics.append(
            UncertaintyHistoryDiagnostic(
                "UNCERTAINTY_HISTORY_STATUS_INVALID",
                f"status must be one of {sorted(ALLOWED_STATUSES)}",
            )
        )
    transition_id = data.get("transition_id")
    if transition_id is not None:
        try:
            _safe_id(transition_id, "transition_id")
        except ValueError as exc:
            diagnostics.append(UncertaintyHistoryDiagnostic("UNCERTAINTY_HISTORY_TRANSITION_ID_INVALID", str(exc)))
    refs = data.get("evidence_refs")
    if not isinstance(refs, list) or any(not isinstance(item, str) or not item for item in refs):
        diagnostics.append(
            UncertaintyHistoryDiagnostic(
                "UNCERTAINTY_HISTORY_EVIDENCE_REFS_INVALID",
                "evidence_refs must be a list of non-empty strings",
            )
        )
    elif len(refs) != len(set(refs)):
        diagnostics.append(
            UncertaintyHistoryDiagnostic(
                "UNCERTAINTY_HISTORY_EVIDENCE_REFS_DUPLICATE",
                "evidence_refs must not contain duplicates",
            )
        )
    superseded_by = data.get("superseded_by")
    if status == "superseded":
        try:
            replacement = _safe_id(superseded_by, "superseded_by")
            if replacement == data.get("uncertainty_id"):
                raise ValueError("superseded_by must differ from uncertainty_id")
        except ValueError as exc:
            diagnostics.append(UncertaintyHistoryDiagnostic("UNCERTAINTY_HISTORY_SUPERSESSION_INVALID", str(exc)))
    elif superseded_by is not None:
        diagnostics.append(
            UncertaintyHistoryDiagnostic(
                "UNCERTAINTY_HISTORY_SUPERSESSION_INVALID",
                "superseded_by is allowed only for status='superseded'",
            )
        )
    note = data.get("note")
    if note is not None and (not isinstance(note, str) or not note.strip()):
        diagnostics.append(
            UncertaintyHistoryDiagnostic(
                "UNCERTAINTY_HISTORY_NOTE_INVALID",
                "note must be null or a non-empty string",
            )
        )
    return data, tuple(diagnostics)


class UncertaintyHistoryService:
    """Persist and inspect a hash-chained uncertainty lifecycle companion."""

    def __init__(self, workspace: str | Path) -> None:
        self.lifecycle = CampaignService(workspace)
        self.path = self.lifecycle.store.root / UNCERTAINTY_HISTORY_FILENAME

    def load(self) -> UncertaintyHistoryResult:
        snapshot = self.lifecycle.resume()
        if not self.path.exists():
            return UncertaintyHistoryResult(
                campaign_id=snapshot.state.campaign_id,
                records=(),
                diagnostics=(),
                latest_statuses={},
            )
        try:
            lines = self.path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            return UncertaintyHistoryResult(
                campaign_id=snapshot.state.campaign_id,
                records=(),
                diagnostics=(UncertaintyHistoryDiagnostic("UNCERTAINTY_HISTORY_READ_FAILED", str(exc)),),
                latest_statuses={},
            )

        diagnostics: list[UncertaintyHistoryDiagnostic] = []
        records: list[Mapping[str, Any]] = []
        seen_event_ids: set[str] = set()
        previous_digest: str | None = None
        transition_ids = {item.id for item in snapshot.transitions}
        evidence_authority = set(snapshot.evidence_refs)
        latest_statuses: dict[str, str] = {}

        for line_number, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                diagnostics.append(
                    UncertaintyHistoryDiagnostic(
                        "UNCERTAINTY_HISTORY_INVALID_JSON",
                        str(exc),
                        line_number,
                    )
                )
                continue
            if not isinstance(record, Mapping) or not isinstance(record.get("event"), Mapping):
                diagnostics.append(
                    UncertaintyHistoryDiagnostic(
                        "UNCERTAINTY_HISTORY_RECORD_INVALID",
                        "record must contain an event object",
                        line_number,
                    )
                )
                continue
            event, event_diagnostics = _validate_event(record["event"])
            diagnostics.extend(
                UncertaintyHistoryDiagnostic(item.code, item.detail, line_number)
                for item in event_diagnostics
            )
            if record.get("previous_digest") != previous_digest:
                diagnostics.append(
                    UncertaintyHistoryDiagnostic(
                        "UNCERTAINTY_HISTORY_CHAIN_MISMATCH",
                        "previous_digest does not match the prior record",
                        line_number,
                    )
                )
            expected = _digest(
                {"event": dict(record["event"]), "previous_digest": record.get("previous_digest")}
            )
            if record.get("event_digest") != expected:
                diagnostics.append(
                    UncertaintyHistoryDiagnostic(
                        "UNCERTAINTY_HISTORY_DIGEST_MISMATCH",
                        "event_digest does not match canonical record bytes",
                        line_number,
                    )
                )
            previous_digest = record.get("event_digest") if isinstance(record.get("event_digest"), str) else None
            if event is None:
                continue
            event_id = event.get("event_id")
            if isinstance(event_id, str):
                if event_id in seen_event_ids:
                    diagnostics.append(
                        UncertaintyHistoryDiagnostic(
                            "UNCERTAINTY_HISTORY_DUPLICATE_EVENT_ID",
                            f"duplicate event_id {event_id!r}",
                            line_number,
                        )
                    )
                seen_event_ids.add(event_id)
            transition_id = event.get("transition_id")
            if isinstance(transition_id, str) and transition_id not in transition_ids:
                diagnostics.append(
                    UncertaintyHistoryDiagnostic(
                        "UNCERTAINTY_HISTORY_UNKNOWN_TRANSITION",
                        f"transition_id {transition_id!r} is not in the Campaign",
                        line_number,
                    )
                )
            refs = event.get("evidence_refs")
            if isinstance(refs, list):
                missing_refs = sorted(
                    item for item in refs if isinstance(item, str) and item not in evidence_authority
                )
                if missing_refs:
                    diagnostics.append(
                        UncertaintyHistoryDiagnostic(
                            "UNCERTAINTY_HISTORY_UNKNOWN_EVIDENCE",
                            "evidence refs are not exposed by current Campaign evidence authority: "
                            + ", ".join(missing_refs),
                            line_number,
                        )
                    )
            uncertainty_id = event.get("uncertainty_id")
            status = event.get("status")
            if isinstance(uncertainty_id, str) and isinstance(status, str):
                latest_statuses[uncertainty_id] = status
            records.append(record)

        return UncertaintyHistoryResult(
            campaign_id=snapshot.state.campaign_id,
            records=tuple(records),
            diagnostics=tuple(diagnostics),
            latest_statuses={key: latest_statuses[key] for key in sorted(latest_statuses)},
        )

    def append(
        self,
        *,
        event_id: str,
        uncertainty_id: str,
        status: str,
        transition_id: str | None = None,
        evidence_refs: tuple[str, ...] = (),
        superseded_by: str | None = None,
        note: str | None = None,
    ) -> str:
        snapshot = self.lifecycle.resume()
        existing = self.load()
        if not existing.valid:
            raise ValueError(
                "uncertainty history is invalid: "
                + ", ".join(item.code for item in existing.diagnostics)
            )

        event_id = _safe_id(event_id, "event_id")
        uncertainty_id = _safe_id(uncertainty_id, "uncertainty_id")
        if any(record.get("event", {}).get("event_id") == event_id for record in existing.records):
            raise ValueError(f"duplicate uncertainty history event_id: {event_id}")
        if status not in ALLOWED_STATUSES:
            raise ValueError(f"status must be one of {sorted(ALLOWED_STATUSES)}")
        normalized_transition = _safe_id(transition_id, "transition_id") if transition_id is not None else None
        transition_ids = {item.id for item in snapshot.transitions}
        if normalized_transition is not None and normalized_transition not in transition_ids:
            raise ValueError(f"unknown Campaign transition_id: {normalized_transition}")
        if len(evidence_refs) != len(set(evidence_refs)):
            raise ValueError("evidence_refs must not contain duplicates")
        evidence_authority = set(snapshot.evidence_refs)
        missing_refs = sorted(set(evidence_refs) - evidence_authority)
        if missing_refs:
            raise ValueError(
                "evidence refs are not exposed by Campaign evidence authority: "
                + ", ".join(missing_refs)
            )
        normalized_superseded_by = None
        if status == "superseded":
            normalized_superseded_by = _safe_id(superseded_by, "superseded_by")
            if normalized_superseded_by == uncertainty_id:
                raise ValueError("superseded_by must differ from uncertainty_id")
        elif superseded_by is not None:
            raise ValueError("superseded_by is allowed only for status='superseded'")
        normalized_note = note.strip() if isinstance(note, str) and note.strip() else None
        if note is not None and normalized_note is None:
            raise ValueError("note must be non-empty when supplied")

        if status == "active":
            active = snapshot.state.active_uncertainty
            if active is None or active.id != uncertainty_id:
                raise ValueError(
                    "status='active' may record only the CampaignState.active_uncertainty; "
                    "the companion does not select active uncertainty"
                )

        event = _event_payload(
            event_id=event_id,
            uncertainty_id=uncertainty_id,
            status=status,
            transition_id=normalized_transition,
            evidence_refs=tuple(evidence_refs),
            superseded_by=normalized_superseded_by,
            note=normalized_note,
        )
        event_diagnostics = _validate_event(event)[1]
        if event_diagnostics:
            raise ValueError(
                "invalid uncertainty history event: "
                + ", ".join(item.detail for item in event_diagnostics)
            )
        previous_digest = (
            existing.records[-1].get("event_digest") if existing.records else None
        )
        digest_input = {"event": event, "previous_digest": previous_digest}
        record = {**digest_input, "event_digest": _digest(digest_input)}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        return record["event_digest"]

    def summary(self) -> dict[str, Any]:
        result = self.load()
        return {
            "present": self.path.exists(),
            "valid": result.valid,
            "event_count": len(result.records),
            "uncertainty_count": len(result.latest_statuses),
            "latest_statuses": dict(result.latest_statuses),
            "diagnostics": [
                {"code": item.code, "detail": item.detail, "line": item.line}
                for item in result.diagnostics
            ],
            "schema_in_campaign_state": False,
            "semantic_recommendation_included": False,
            "semantic_truth_established": False,
        }
