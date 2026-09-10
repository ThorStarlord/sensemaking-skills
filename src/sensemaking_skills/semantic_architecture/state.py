"""Append-only cross-Skill semantic state references.

This companion log preserves provenance between Skills without adding fields to
Campaign schema v2. Entries contain references, not hidden reasoning or a
semantic recommendation engine.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import SemanticDiagnostic, SemanticStateEntry, to_dict


def _canonical_bytes(value: dict[str, Any]) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _digest(value: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


class SemanticStateStore:
    """Persist a hash-chained JSONL companion state log."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def append(self, entry: SemanticStateEntry) -> str:
        records, diagnostics = self.load_raw()
        if diagnostics:
            raise ValueError("semantic state log is invalid: " + ", ".join(item.code for item in diagnostics))
        if any(record["entry"].get("entry_id") == entry.entry_id for record in records):
            raise ValueError(f"duplicate semantic state entry_id: {entry.entry_id}")
        known_ids = {record["entry"].get("entry_id") for record in records}
        missing_parents = sorted(set(entry.parent_entry_ids) - known_ids)
        if missing_parents:
            raise ValueError("semantic state parent entries do not exist: " + ", ".join(missing_parents))

        if not entry.created_at:
            entry = replace(
                entry,
                created_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            )
        payload = to_dict(entry)
        previous_digest = records[-1]["entry_digest"] if records else None
        digest_input = {"entry": payload, "previous_digest": previous_digest}
        record = {
            **digest_input,
            "entry_digest": _digest(digest_input),
        }

        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        return record["entry_digest"]

    def load_raw(self) -> tuple[list[dict[str, Any]], tuple[SemanticDiagnostic, ...]]:
        if not self.path.exists():
            return [], ()
        records: list[dict[str, Any]] = []
        diagnostics: list[SemanticDiagnostic] = []
        previous_digest: str | None = None
        seen_ids: set[str] = set()
        try:
            lines = self.path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            return [], (SemanticDiagnostic("SEMANTIC_STATE_READ_FAILED", str(exc), str(self.path)),)

        for index, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                diagnostics.append(
                    SemanticDiagnostic("SEMANTIC_STATE_INVALID_JSON", f"line {index}: {exc}", str(self.path))
                )
                continue
            if not isinstance(record, dict) or not isinstance(record.get("entry"), dict):
                diagnostics.append(
                    SemanticDiagnostic("SEMANTIC_STATE_INVALID_RECORD", f"line {index} is not a valid record", str(self.path))
                )
                continue
            if record.get("previous_digest") != previous_digest:
                diagnostics.append(
                    SemanticDiagnostic("SEMANTIC_STATE_CHAIN_MISMATCH", f"line {index} previous_digest mismatch", str(self.path))
                )
            expected = _digest(
                {"entry": record["entry"], "previous_digest": record.get("previous_digest")}
            )
            if record.get("entry_digest") != expected:
                diagnostics.append(
                    SemanticDiagnostic("SEMANTIC_STATE_DIGEST_MISMATCH", f"line {index} digest mismatch", str(self.path))
                )
            entry_id = record["entry"].get("entry_id")
            if not isinstance(entry_id, str) or not entry_id:
                diagnostics.append(
                    SemanticDiagnostic("SEMANTIC_STATE_ENTRY_ID_REQUIRED", f"line {index} requires entry_id", str(self.path))
                )
            elif entry_id in seen_ids:
                diagnostics.append(
                    SemanticDiagnostic("SEMANTIC_STATE_DUPLICATE_ENTRY_ID", f"duplicate entry_id {entry_id!r}", str(self.path))
                )
            else:
                seen_ids.add(entry_id)
            parents = record["entry"].get("parent_entry_ids", [])
            if not isinstance(parents, list) or any(parent not in seen_ids for parent in parents):
                diagnostics.append(
                    SemanticDiagnostic("SEMANTIC_STATE_INVALID_PARENT", f"line {index} references a missing/future parent", str(self.path))
                )
            records.append(record)
            previous_digest = record.get("entry_digest")
        return records, tuple(diagnostics)

    def validate(self) -> tuple[SemanticDiagnostic, ...]:
        return self.load_raw()[1]
