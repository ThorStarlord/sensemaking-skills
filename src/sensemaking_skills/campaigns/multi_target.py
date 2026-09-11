"""Multi-repository Campaign target-set companion with deterministic drift checks.

Campaign schema v2 remains unchanged. The primary ``target_snapshot`` field keeps
its existing meaning. This module adds a bounded companion for responsibilities
that explicitly span multiple repositories. The companion records identity,
authority, role, evidence references, and exact target snapshots; it never
infers which repositories belong in the responsibility or whether cross-repo
work is warranted.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from sensemaking_skills.campaign_semantics import Authority, TargetSnapshot, canonicalize, target_snapshot_sha256

from .target_snapshot import CampaignService, capture_target_snapshot, target_snapshots_equivalent


MULTI_TARGET_FILENAME = "multi-targets.json"
MULTI_TARGET_HISTORY_FILENAME = "multi-target-history.jsonl"
MULTI_TARGET_VERSION = "1"
_SAFE_ALIAS = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


@dataclass(frozen=True)
class MultiTargetDiagnostic:
    code: str
    detail: str
    alias: str | None = None


@dataclass(frozen=True)
class MultiTargetVerification:
    campaign_id: str
    valid: bool
    target_set_sha256: str | None
    targets: tuple[Mapping[str, Any], ...]
    diagnostics: tuple[MultiTargetDiagnostic, ...]
    semantic_truth_established: bool = False


def _canonical_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sha256(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _safe_alias(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("alias must be non-empty text")
    alias = value.strip()
    if not _SAFE_ALIAS.fullmatch(alias):
        raise ValueError("alias must use only letters, numbers, '.', '_' or '-'")
    return alias


def _snapshot_from_dict(value: Any) -> TargetSnapshot:
    if not isinstance(value, Mapping):
        raise ValueError("target snapshot must be an object")
    required = {
        "repository_root",
        "repository_id",
        "identity_source",
        "head_sha",
        "tree_sha",
        "worktree_sha256",
        "dirty",
        "vcs",
    }
    if set(value) != required:
        raise ValueError(f"target snapshot fields must be exactly {sorted(required)}")
    if value.get("identity_source") not in {"origin", "local_path"}:
        raise ValueError("target snapshot identity_source must be origin or local_path")
    if value.get("vcs") != "git":
        raise ValueError("target snapshot vcs must be git")
    for field in ("repository_root", "repository_id", "head_sha", "tree_sha", "worktree_sha256"):
        if not isinstance(value.get(field), str) or not value.get(field):
            raise ValueError(f"target snapshot {field} must be non-empty text")
    if not isinstance(value.get("dirty"), bool):
        raise ValueError("target snapshot dirty must be boolean")
    return TargetSnapshot(**dict(value))


def _manifest_payload(campaign_id: str, targets: list[dict[str, Any]]) -> dict[str, Any]:
    core = {
        "schema_version": MULTI_TARGET_VERSION,
        "campaign_id": campaign_id,
        "targets": sorted(targets, key=lambda item: item["alias"]),
        "semantic_truth_established": False,
    }
    return {**core, "target_set_sha256": _sha256(core)}


def _history_digest_input(record: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": record["schema_version"],
        "campaign_id": record["campaign_id"],
        "alias": record["alias"],
        "from_snapshot_sha256": record["from_snapshot_sha256"],
        "to_snapshot_sha256": record["to_snapshot_sha256"],
        "previous_digest": record["previous_digest"],
    }


class MultiTargetService:
    """Persist and verify an explicit multi-repository target set."""

    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace).resolve()
        self.lifecycle = CampaignService(self.workspace)
        self.manifest_path = self.workspace / MULTI_TARGET_FILENAME
        self.history_path = self.workspace / MULTI_TARGET_HISTORY_FILENAME

    def _campaign_id(self) -> str:
        return self.lifecycle.resume().state.campaign_id

    def _load_manifest(self) -> tuple[dict[str, Any] | None, list[MultiTargetDiagnostic]]:
        campaign_id = self._campaign_id()
        if not self.manifest_path.exists():
            return None, []
        diagnostics: list[MultiTargetDiagnostic] = []
        try:
            data = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            return None, [MultiTargetDiagnostic("MULTI_TARGET_MANIFEST_READ_FAILED", str(exc))]
        if not isinstance(data, dict):
            return None, [MultiTargetDiagnostic("MULTI_TARGET_MANIFEST_INVALID", "manifest must be an object")]
        required = {"schema_version", "campaign_id", "targets", "semantic_truth_established", "target_set_sha256"}
        if set(data) != required:
            diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_MANIFEST_FIELDS_INVALID", f"fields must be exactly {sorted(required)}"))
            return data, diagnostics
        if data.get("schema_version") != MULTI_TARGET_VERSION:
            diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_VERSION_UNSUPPORTED", f"unsupported schema_version {data.get('schema_version')!r}"))
        if data.get("campaign_id") != campaign_id:
            diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_CAMPAIGN_ID_MISMATCH", "manifest campaign_id does not match Campaign state"))
        if data.get("semantic_truth_established") is not False:
            diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_SEMANTIC_AUTHORITY_INVALID", "semantic_truth_established must remain false"))
        targets = data.get("targets")
        if not isinstance(targets, list):
            diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_TARGETS_INVALID", "targets must be a list"))
            return data, diagnostics
        aliases: set[str] = set()
        repository_ids: set[str] = set()
        campaign_evidence = set(self.lifecycle.resume().evidence_refs)
        for index, raw in enumerate(targets):
            if not isinstance(raw, Mapping):
                diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_ENTRY_INVALID", f"targets[{index}] must be an object"))
                continue
            entry = dict(raw)
            expected = {"alias", "role", "authority", "evidence_refs", "snapshot", "snapshot_sha256"}
            if set(entry) != expected:
                diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_ENTRY_FIELDS_INVALID", f"targets[{index}] fields must be exactly {sorted(expected)}"))
                continue
            try:
                alias = _safe_alias(entry.get("alias"))
            except ValueError as exc:
                diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_ALIAS_INVALID", str(exc)))
                continue
            if alias in aliases:
                diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_ALIAS_DUPLICATE", f"duplicate alias {alias!r}", alias))
            aliases.add(alias)
            if not isinstance(entry.get("role"), str) or not entry.get("role", "").strip():
                diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_ROLE_INVALID", "role must be non-empty text", alias))
            try:
                Authority(entry.get("authority"))
            except (TypeError, ValueError):
                diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_AUTHORITY_INVALID", "authority must be a known Authority value", alias))
            refs = entry.get("evidence_refs")
            if not isinstance(refs, list) or any(not isinstance(item, str) or not item for item in refs):
                diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_EVIDENCE_INVALID", "evidence_refs must be a list of non-empty strings", alias))
            else:
                if len(refs) != len(set(refs)):
                    diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_EVIDENCE_DUPLICATE", "evidence_refs must not contain duplicates", alias))
                missing = sorted(set(refs) - campaign_evidence)
                if missing:
                    diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_UNKNOWN_EVIDENCE", "evidence refs are outside Campaign authority: " + ", ".join(missing), alias))
            try:
                snapshot = _snapshot_from_dict(entry.get("snapshot"))
            except ValueError as exc:
                diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_SNAPSHOT_INVALID", str(exc), alias))
                continue
            digest = target_snapshot_sha256(snapshot)
            if entry.get("snapshot_sha256") != digest:
                diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_SNAPSHOT_DIGEST_MISMATCH", "snapshot_sha256 does not match snapshot bytes", alias))
            if snapshot.repository_id in repository_ids:
                diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_REPOSITORY_DUPLICATE", "same repository identity is bound under multiple aliases", alias))
            repository_ids.add(snapshot.repository_id)
        core = {key: data[key] for key in ("schema_version", "campaign_id", "targets", "semantic_truth_established") if key in data}
        if data.get("target_set_sha256") != _sha256(core):
            diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_SET_DIGEST_MISMATCH", "target_set_sha256 does not match manifest content"))
        return data, diagnostics

    def inspect(self) -> MultiTargetVerification:
        campaign_id = self._campaign_id()
        data, diagnostics = self._load_manifest()
        if data is None:
            return MultiTargetVerification(campaign_id, not diagnostics, None, (), tuple(diagnostics))
        targets = tuple(data.get("targets", [])) if isinstance(data.get("targets"), list) else ()
        return MultiTargetVerification(campaign_id, not diagnostics, data.get("target_set_sha256"), targets, tuple(diagnostics))

    def add(
        self,
        *,
        alias: str,
        target_repo: str | Path,
        role: str,
        authority: Authority,
        evidence_refs: tuple[str, ...] = (),
    ) -> str:
        campaign_id = self._campaign_id()
        existing = self.inspect()
        if not existing.valid:
            raise ValueError("multi-target manifest is invalid: " + ", ".join(item.code for item in existing.diagnostics))
        alias = _safe_alias(alias)
        role = role.strip() if isinstance(role, str) else ""
        if not role:
            raise ValueError("role must be non-empty text")
        if len(evidence_refs) != len(set(evidence_refs)):
            raise ValueError("evidence_refs must not contain duplicates")
        missing = sorted(set(evidence_refs) - set(self.lifecycle.resume().evidence_refs))
        if missing:
            raise ValueError("evidence refs are outside Campaign authority: " + ", ".join(missing))
        target = capture_target_snapshot(target_repo)
        target_root = Path(target.repository_root).resolve()
        if self.workspace == target_root or target_root in self.workspace.parents or self.workspace in target_root.parents:
            raise ValueError("Campaign workspace and multi-target repository must be disjoint directory trees")
        targets = [dict(item) for item in existing.targets]
        if alias in {item["alias"] for item in targets}:
            raise ValueError(f"multi-target alias already exists: {alias}")
        if target.repository_id in {item["snapshot"]["repository_id"] for item in targets}:
            raise ValueError("repository identity is already bound in this Campaign target set")
        targets.append(
            {
                "alias": alias,
                "role": role,
                "authority": authority.value,
                "evidence_refs": list(evidence_refs),
                "snapshot": canonicalize(target),
                "snapshot_sha256": target_snapshot_sha256(target),
            }
        )
        manifest = _manifest_payload(campaign_id, targets)
        temp = self.manifest_path.with_suffix(".json.tmp")
        temp.write_text(json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
        os.replace(temp, self.manifest_path)
        return str(manifest["target_set_sha256"])

    def verify(self, alias: str | None = None) -> MultiTargetVerification:
        inspected = self.inspect()
        if not inspected.valid:
            return inspected
        diagnostics: list[MultiTargetDiagnostic] = []
        targets = [dict(item) for item in inspected.targets]
        if alias is not None:
            alias = _safe_alias(alias)
            targets = [item for item in targets if item["alias"] == alias]
            if not targets:
                diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_ALIAS_NOT_FOUND", f"unknown alias {alias!r}", alias))
        for entry in targets:
            entry_alias = str(entry["alias"])
            expected = _snapshot_from_dict(entry["snapshot"])
            try:
                actual = capture_target_snapshot(expected.repository_root)
            except Exception as exc:
                diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_REPOSITORY_UNAVAILABLE", str(exc), entry_alias))
                continue
            if actual.repository_id != expected.repository_id or actual.identity_source != expected.identity_source:
                diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_IDENTITY_MISMATCH", "live repository identity differs from recorded target identity", entry_alias))
                continue
            if not target_snapshots_equivalent(expected, actual):
                diagnostics.append(MultiTargetDiagnostic("MULTI_TARGET_SNAPSHOT_DRIFT", "live repository state differs from recorded snapshot", entry_alias))
        return MultiTargetVerification(
            campaign_id=inspected.campaign_id,
            valid=not diagnostics,
            target_set_sha256=inspected.target_set_sha256,
            targets=tuple(targets),
            diagnostics=tuple(diagnostics),
        )

    def _last_history_digest(self) -> str | None:
        if not self.history_path.exists():
            return None
        lines = [line for line in self.history_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not lines:
            return None
        record = json.loads(lines[-1])
        return record.get("record_digest") if isinstance(record, dict) else None

    def refresh(self, alias: str) -> dict[str, Any]:
        alias = _safe_alias(alias)
        inspected = self.inspect()
        if not inspected.valid:
            raise ValueError("multi-target manifest is invalid")
        targets = [dict(item) for item in inspected.targets]
        matches = [item for item in targets if item["alias"] == alias]
        if not matches:
            raise ValueError(f"unknown multi-target alias: {alias}")
        entry = matches[0]
        expected = _snapshot_from_dict(entry["snapshot"])
        actual = capture_target_snapshot(expected.repository_root)
        if actual.repository_id != expected.repository_id or actual.identity_source != expected.identity_source:
            raise ValueError("refuse refresh because live repository identity differs from recorded identity")
        before = target_snapshot_sha256(expected)
        after = target_snapshot_sha256(actual)
        entry["snapshot"] = canonicalize(actual)
        entry["snapshot_sha256"] = after
        manifest = _manifest_payload(inspected.campaign_id, targets)
        temp = self.manifest_path.with_suffix(".json.tmp")
        temp.write_text(json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
        os.replace(temp, self.manifest_path)
        previous_digest = self._last_history_digest()
        record: dict[str, Any] = {
            "schema_version": MULTI_TARGET_VERSION,
            "campaign_id": inspected.campaign_id,
            "alias": alias,
            "from_snapshot_sha256": before,
            "to_snapshot_sha256": after,
            "previous_digest": previous_digest,
        }
        record["record_digest"] = _sha256(_history_digest_input(record))
        with self.history_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        return {
            "campaign_id": inspected.campaign_id,
            "alias": alias,
            "from_snapshot_sha256": before,
            "to_snapshot_sha256": after,
            "target_set_sha256": manifest["target_set_sha256"],
            "changed": before != after,
            "semantic_truth_established": False,
        }
