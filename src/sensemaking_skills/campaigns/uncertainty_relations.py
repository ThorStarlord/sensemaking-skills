"""Append-only uncertainty relationships without ranking or selection authority."""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .target_snapshot import CampaignService
from .uncertainty_history import UncertaintyHistoryService


UNCERTAINTY_RELATIONS_FILENAME = "uncertainty-relations.jsonl"
UNCERTAINTY_RELATIONS_VERSION = "1"
RELATION_TYPES = frozenset(
    {
        "depends_on",
        "blocks_decision",
        "introduced_by_transition",
        "resolved_by_transition",
        "supersedes",
    }
)
_UNCERTAINTY_TARGET_RELATIONS = frozenset({"depends_on", "supersedes"})
_TRANSITION_TARGET_RELATIONS = frozenset({"introduced_by_transition", "resolved_by_transition"})
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


@dataclass(frozen=True)
class UncertaintyRelationDiagnostic:
    code: str
    detail: str
    line: int | None = None


@dataclass(frozen=True)
class UncertaintyRelationResult:
    campaign_id: str
    records: tuple[Mapping[str, Any], ...]
    diagnostics: tuple[UncertaintyRelationDiagnostic, ...]

    @property
    def valid(self) -> bool:
        return not self.diagnostics


def _canonical_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _safe_id(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    text = value.strip()
    if not _SAFE_ID.fullmatch(text):
        raise ValueError(f"{field} must use only letters, numbers, '.', '_' or '-'")
    return text


def _known_uncertainties(snapshot: Any, history: Any) -> set[str]:
    known = set(history.latest_statuses)
    if snapshot.state.active_uncertainty is not None:
        known.add(snapshot.state.active_uncertainty.id)
    return known


class UncertaintyRelationService:
    """Persist explicitly authored uncertainty relations as a hash-chained companion."""

    def __init__(self, workspace: str | Path) -> None:
        self.lifecycle = CampaignService(workspace)
        self.path = self.lifecycle.store.root / UNCERTAINTY_RELATIONS_FILENAME

    def load(self) -> UncertaintyRelationResult:
        snapshot = self.lifecycle.resume()
        history = UncertaintyHistoryService(self.lifecycle.store.root).load()
        diagnostics: list[UncertaintyRelationDiagnostic] = []
        if not history.valid:
            diagnostics.append(
                UncertaintyRelationDiagnostic(
                    "UNCERTAINTY_RELATIONS_HISTORY_INVALID",
                    "uncertainty history must be valid before relationships can be trusted",
                )
            )
        if not self.path.exists():
            return UncertaintyRelationResult(snapshot.state.campaign_id, (), tuple(diagnostics))

        try:
            lines = self.path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            return UncertaintyRelationResult(
                snapshot.state.campaign_id,
                (),
                (UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_READ_FAILED", str(exc)),),
            )

        records: list[Mapping[str, Any]] = []
        previous_digest: str | None = None
        seen_ids: set[str] = set()
        known_uncertainties = _known_uncertainties(snapshot, history)
        transition_ids = {item.id for item in snapshot.transitions}
        evidence_authority = set(snapshot.evidence_refs)

        for line_number, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_INVALID_JSON", str(exc), line_number))
                continue
            if not isinstance(record, Mapping) or not isinstance(record.get("relation"), Mapping):
                diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_RECORD_INVALID", "record must contain a relation object", line_number))
                continue
            relation = dict(record["relation"])
            required = {"schema_version", "relation_id", "source_uncertainty_id", "relation_type", "target_ref", "evidence_refs", "note"}
            if set(relation) != required:
                diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_FIELDS_INVALID", f"fields must be exactly {sorted(required)}", line_number))
                continue
            if relation.get("schema_version") != UNCERTAINTY_RELATIONS_VERSION:
                diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_VERSION_UNSUPPORTED", f"unsupported schema_version {relation.get('schema_version')!r}", line_number))
            relation_id = relation.get("relation_id")
            try:
                normalized_relation_id = _safe_id(relation_id, "relation_id")
            except ValueError as exc:
                diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_ID_INVALID", str(exc), line_number))
                normalized_relation_id = None
            if normalized_relation_id:
                if normalized_relation_id in seen_ids:
                    diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_DUPLICATE_ID", f"duplicate relation_id {normalized_relation_id!r}", line_number))
                seen_ids.add(normalized_relation_id)
            source = relation.get("source_uncertainty_id")
            try:
                source = _safe_id(source, "source_uncertainty_id")
            except ValueError as exc:
                diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_SOURCE_INVALID", str(exc), line_number))
                source = None
            if source and source not in known_uncertainties:
                diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_UNKNOWN_SOURCE", f"unknown uncertainty {source!r}", line_number))
            relation_type = relation.get("relation_type")
            if relation_type not in RELATION_TYPES:
                diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_TYPE_INVALID", f"relation_type must be one of {sorted(RELATION_TYPES)}", line_number))
            target = relation.get("target_ref")
            if not isinstance(target, str) or not target.strip():
                diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_TARGET_INVALID", "target_ref must be non-empty text", line_number))
            else:
                target = target.strip()
                if relation_type in _UNCERTAINTY_TARGET_RELATIONS:
                    try:
                        target_id = _safe_id(target, "target_ref")
                    except ValueError as exc:
                        diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_TARGET_INVALID", str(exc), line_number))
                    else:
                        if target_id not in known_uncertainties:
                            diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_UNKNOWN_TARGET", f"unknown uncertainty {target_id!r}", line_number))
                        if source == target_id:
                            diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_SELF_REFERENCE", "uncertainty relation may not target itself", line_number))
                elif relation_type in _TRANSITION_TARGET_RELATIONS and target not in transition_ids:
                    diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_UNKNOWN_TRANSITION", f"unknown transition {target!r}", line_number))
            refs = relation.get("evidence_refs")
            if not isinstance(refs, list) or any(not isinstance(item, str) or not item for item in refs):
                diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_EVIDENCE_INVALID", "evidence_refs must be a list of non-empty strings", line_number))
            else:
                if len(refs) != len(set(refs)):
                    diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_EVIDENCE_DUPLICATE", "evidence_refs must not contain duplicates", line_number))
                missing = sorted(set(refs) - evidence_authority)
                if missing:
                    diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_UNKNOWN_EVIDENCE", "evidence refs are outside Campaign authority: " + ", ".join(missing), line_number))
            note = relation.get("note")
            if note is not None and (not isinstance(note, str) or not note.strip()):
                diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_NOTE_INVALID", "note must be null or non-empty text", line_number))
            if record.get("previous_digest") != previous_digest:
                diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_CHAIN_MISMATCH", "previous_digest does not match prior record", line_number))
            expected = _digest({"relation": relation, "previous_digest": record.get("previous_digest")})
            if record.get("relation_digest") != expected:
                diagnostics.append(UncertaintyRelationDiagnostic("UNCERTAINTY_RELATIONS_DIGEST_MISMATCH", "relation_digest does not match canonical record bytes", line_number))
            previous_digest = record.get("relation_digest") if isinstance(record.get("relation_digest"), str) else None
            records.append(record)

        return UncertaintyRelationResult(snapshot.state.campaign_id, tuple(records), tuple(diagnostics))

    def append(
        self,
        *,
        relation_id: str,
        source_uncertainty_id: str,
        relation_type: str,
        target_ref: str,
        evidence_refs: tuple[str, ...] = (),
        note: str | None = None,
    ) -> str:
        snapshot = self.lifecycle.resume()
        history = UncertaintyHistoryService(self.lifecycle.store.root).load()
        if not history.valid:
            raise ValueError("uncertainty history is invalid")
        existing = self.load()
        if not existing.valid:
            raise ValueError("uncertainty relationships are invalid: " + ", ".join(item.code for item in existing.diagnostics))

        relation_id = _safe_id(relation_id, "relation_id")
        source_uncertainty_id = _safe_id(source_uncertainty_id, "source_uncertainty_id")
        if relation_type not in RELATION_TYPES:
            raise ValueError(f"relation_type must be one of {sorted(RELATION_TYPES)}")
        if not isinstance(target_ref, str) or not target_ref.strip():
            raise ValueError("target_ref must be non-empty text")
        target_ref = target_ref.strip()
        if any(record.get("relation", {}).get("relation_id") == relation_id for record in existing.records):
            raise ValueError(f"duplicate relation_id: {relation_id}")

        known = _known_uncertainties(snapshot, history)
        if source_uncertainty_id not in known:
            raise ValueError(f"unknown source uncertainty: {source_uncertainty_id}")
        if relation_type in _UNCERTAINTY_TARGET_RELATIONS:
            target_ref = _safe_id(target_ref, "target_ref")
            if target_ref not in known:
                raise ValueError(f"unknown target uncertainty: {target_ref}")
            if target_ref == source_uncertainty_id:
                raise ValueError("uncertainty relation may not target itself")
        if relation_type in _TRANSITION_TARGET_RELATIONS:
            if target_ref not in {item.id for item in snapshot.transitions}:
                raise ValueError(f"unknown Campaign transition: {target_ref}")
        if len(evidence_refs) != len(set(evidence_refs)):
            raise ValueError("evidence_refs must not contain duplicates")
        missing = sorted(set(evidence_refs) - set(snapshot.evidence_refs))
        if missing:
            raise ValueError("evidence refs are outside Campaign authority: " + ", ".join(missing))
        normalized_note = note.strip() if isinstance(note, str) and note.strip() else None
        if note is not None and normalized_note is None:
            raise ValueError("note must be non-empty when supplied")

        relation = {
            "schema_version": UNCERTAINTY_RELATIONS_VERSION,
            "relation_id": relation_id,
            "source_uncertainty_id": source_uncertainty_id,
            "relation_type": relation_type,
            "target_ref": target_ref,
            "evidence_refs": list(evidence_refs),
            "note": normalized_note,
        }
        previous_digest = existing.records[-1].get("relation_digest") if existing.records else None
        digest_input = {"relation": relation, "previous_digest": previous_digest}
        record = {**digest_input, "relation_digest": _digest(digest_input)}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        return record["relation_digest"]

    def show(self, uncertainty_id: str) -> dict[str, Any]:
        uncertainty_id = _safe_id(uncertainty_id, "uncertainty_id")
        snapshot = self.lifecycle.resume()
        history = UncertaintyHistoryService(self.lifecycle.store.root).load()
        relations = self.load()
        events = [record for record in history.records if record.get("event", {}).get("uncertainty_id") == uncertainty_id]
        outbound = [record for record in relations.records if record.get("relation", {}).get("source_uncertainty_id") == uncertainty_id]
        inbound = [record for record in relations.records if record.get("relation", {}).get("target_ref") == uncertainty_id and record.get("relation", {}).get("relation_type") in _UNCERTAINTY_TARGET_RELATIONS]
        active = snapshot.state.active_uncertainty
        known = bool(events) or (active is not None and active.id == uncertainty_id)
        return {
            "found": known,
            "uncertainty_id": uncertainty_id,
            "active": active is not None and active.id == uncertainty_id,
            "current": None if active is None or active.id != uncertainty_id else {"id": active.id, "question": active.question, "status": active.status, "materiality": active.materiality},
            "history": events,
            "outbound_relations": outbound,
            "inbound_relations": inbound,
            "history_valid": history.valid,
            "relations_valid": relations.valid,
            "semantic_recommendation_included": False,
            "semantic_truth_established": False,
        }

    def graph(self) -> dict[str, Any]:
        snapshot = self.lifecycle.resume()
        history = UncertaintyHistoryService(self.lifecycle.store.root).load()
        relations = self.load()
        nodes: dict[str, dict[str, str]] = {}
        edges: list[dict[str, str]] = []
        for uncertainty_id, status in history.latest_statuses.items():
            nodes[uncertainty_id] = {"id": uncertainty_id, "kind": "uncertainty", "label": uncertainty_id, "status": status}
        if snapshot.state.active_uncertainty is not None:
            item = snapshot.state.active_uncertainty
            nodes.setdefault(item.id, {"id": item.id, "kind": "uncertainty", "label": item.id, "status": item.status})
        for record in relations.records:
            relation = record.get("relation", {})
            source = str(relation.get("source_uncertainty_id"))
            target = str(relation.get("target_ref"))
            relation_type = str(relation.get("relation_type"))
            target_kind = "uncertainty" if relation_type in _UNCERTAINTY_TARGET_RELATIONS else ("transition" if relation_type in _TRANSITION_TARGET_RELATIONS else "decision_ref")
            nodes.setdefault(target, {"id": target, "kind": target_kind, "label": target})
            edges.append({"from": source, "to": target, "relation": relation_type, "relation_id": str(relation.get("relation_id"))})
        return {
            "ok": history.valid and relations.valid,
            "campaign_id": snapshot.state.campaign_id,
            "nodes": [nodes[key] for key in sorted(nodes)],
            "edges": sorted(edges, key=lambda item: (item["from"], item["relation"], item["to"], item["relation_id"])),
            "diagnostics": [
                {"code": item.code, "detail": item.detail, "line": item.line}
                for item in relations.diagnostics
            ],
            "semantic_ranking_performed": False,
            "semantic_recommendation_included": False,
            "semantic_truth_established": False,
        }
