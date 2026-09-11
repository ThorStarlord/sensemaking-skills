"""Explicit path rebinding for existing multi-target repository identities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sensemaking_skills.campaign_semantics import canonicalize, target_snapshot_sha256

from .companion_io import append_jsonl_fsync, atomic_write_json, mapping_sha256
from .multi_target import MultiTargetService, _manifest_payload, _safe_alias, _snapshot_from_dict
from .target_snapshot import capture_target_snapshot, target_snapshots_equivalent


MULTI_TARGET_REBIND_HISTORY_FILENAME = "multi-target-rebind-history.jsonl"
MULTI_TARGET_REBIND_VERSION = "1"


class MultiTargetRebindService:
    """Rebind one explicit alias to another local path for the same exact target."""

    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace).resolve()
        self.targets = MultiTargetService(self.workspace)
        self.history_path = self.workspace / MULTI_TARGET_REBIND_HISTORY_FILENAME

    def _last_digest(self) -> str | None:
        if not self.history_path.exists():
            return None
        lines = [line for line in self.history_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not lines:
            return None
        try:
            value = json.loads(lines[-1])
        except json.JSONDecodeError as exc:
            raise ValueError("multi-target rebind history is invalid JSON") from exc
        if not isinstance(value, dict) or not isinstance(value.get("record_digest"), str):
            raise ValueError("multi-target rebind history tail is invalid")
        return str(value["record_digest"])

    def rebind(self, *, alias: str, target_repo: str | Path) -> dict[str, Any]:
        alias = _safe_alias(alias)
        inspected = self.targets.inspect()
        if not inspected.valid:
            raise ValueError("multi-target manifest is invalid")
        targets = [dict(item) for item in inspected.targets]
        matches = [item for item in targets if item.get("alias") == alias]
        if not matches:
            raise ValueError(f"unknown multi-target alias: {alias}")
        entry = matches[0]
        expected = _snapshot_from_dict(entry["snapshot"])
        actual = capture_target_snapshot(target_repo)
        if actual.repository_id != expected.repository_id or actual.identity_source != expected.identity_source:
            raise ValueError("refuse rebind because candidate repository identity differs from the recorded multi-target identity")
        if not target_snapshots_equivalent(expected, actual):
            raise ValueError("refuse rebind because candidate repository state differs from the recorded multi-target snapshot")
        target_root = Path(actual.repository_root).resolve()
        if self.workspace == target_root or target_root in self.workspace.parents or self.workspace in target_root.parents:
            raise ValueError("Campaign workspace and rebound multi-target repository must be disjoint directory trees")

        before = target_snapshot_sha256(expected)
        entry["snapshot"] = canonicalize(actual)
        entry["snapshot_sha256"] = target_snapshot_sha256(actual)
        manifest = _manifest_payload(inspected.campaign_id, targets)
        atomic_write_json(self.targets.manifest_path, manifest)

        record: dict[str, Any] = {
            "schema_version": MULTI_TARGET_REBIND_VERSION,
            "campaign_id": inspected.campaign_id,
            "alias": alias,
            "repository_id": expected.repository_id,
            "from_repository_root": expected.repository_root,
            "to_repository_root": actual.repository_root,
            "from_snapshot_sha256": before,
            "to_snapshot_sha256": target_snapshot_sha256(actual),
            "previous_digest": self._last_digest(),
            "semantic_truth_established": False,
        }
        record["record_digest"] = mapping_sha256(record)
        append_jsonl_fsync(self.history_path, record)

        return {
            "campaign_id": inspected.campaign_id,
            "alias": alias,
            "repository_id": expected.repository_id,
            "from_repository_root": expected.repository_root,
            "to_repository_root": actual.repository_root,
            "from_snapshot_sha256": before,
            "to_snapshot_sha256": target_snapshot_sha256(actual),
            "target_set_sha256": manifest["target_set_sha256"],
            "record_digest": record["record_digest"],
            "repository_discovery_performed": False,
            "semantic_truth_established": False,
        }
