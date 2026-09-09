"""Non-destructive schema qualification for durable Campaign artifacts.

Legacy Campaign bytes stay immutable. Semantic loaders migrate them in memory;
this service writes append-only, content-addressed receipts binding exact source
bytes to their exact deterministic current representation.
"""

from __future__ import annotations

import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

import yaml

from sensemaking_skills import path_containment as pc
from sensemaking_skills.campaign_semantics import (
    CampaignState,
    ContractError,
    load_campaign_handoff,
    load_campaign_policy,
    load_campaign_state,
    load_campaign_trace,
    load_transition_record,
)
from sensemaking_skills.campaign_semantics.schema import (
    CURRENT_SCHEMA_VERSION,
    LEGACY_SCHEMA_VERSION,
    SUPPORTED_ARTIFACT_KINDS,
    SchemaMigrationError,
    SchemaMigrationResult,
    migrate_payload,
)

from .admission import canonical_json_digest, sha256_file
from .errors import (
    CampaignIntegrityError,
    CampaignNotInitializedError,
    CampaignTransactionError,
    CampaignWorkspaceError,
)
from .store import CampaignStore

_RECEIPT_VERSION = "1"
_ENGINE = "sensemaking_skills.campaign_semantics.schema"
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_TRANSITION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*\.yaml$")
_DIRECT = {
    "campaign-state.yaml": "campaign_state",
    "trace.yaml": "campaign_trace",
    "campaign-policy.yaml": "campaign_policy",
    "campaign-handoff.yaml": "campaign_handoff",
}
_RECEIPT_FIELDS = {
    "receipt_schema_version", "campaign_id", "artifact_ref", "artifact_kind",
    "source_schema_version", "target_schema_version", "source_sha256",
    "migrated_payload_sha256", "migrated_payload", "migration_steps",
    "migration_engine",
}


def _integrity(message: str, code: str = "SCHEMA_MIGRATION_RECEIPT_INVALID") -> CampaignIntegrityError:
    return CampaignIntegrityError(message, diagnostic_codes=(code,))


@dataclass(frozen=True)
class SchemaMigrationReceipt:
    campaign_id: str
    artifact_ref: str
    artifact_kind: str
    source_schema_version: str
    target_schema_version: str
    source_sha256: str
    migrated_payload_sha256: str
    migrated_payload: Mapping[str, Any]
    migration_steps: tuple[str, ...]
    migration_engine: str = _ENGINE
    receipt_schema_version: str = _RECEIPT_VERSION


@dataclass(frozen=True)
class CampaignSchemaArtifactStatus:
    artifact_ref: str
    artifact_kind: str
    source_schema_version: str
    effective_schema_version: str
    source_sha256: str
    migrated_payload_sha256: str
    migration_steps: tuple[str, ...]
    migration_status: str
    receipt_ref: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CampaignSchemaStatus:
    campaign_id: str
    current_schema_version: str
    upgrade_required: bool
    artifacts: tuple[CampaignSchemaArtifactStatus, ...]
    receipt_count: int

    @property
    def qualified(self) -> bool:
        return not self.upgrade_required

    def to_dict(self) -> dict[str, Any]:
        return {
            "campaign_id": self.campaign_id,
            "current_schema_version": self.current_schema_version,
            "upgrade_required": self.upgrade_required,
            "qualified": self.qualified,
            "receipt_count": self.receipt_count,
            "artifacts": [item.to_dict() for item in self.artifacts],
        }


@dataclass(frozen=True)
class CampaignSchemaUpgradeResult:
    before: CampaignSchemaStatus
    after: CampaignSchemaStatus
    receipts_written: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "before": self.before.to_dict(),
            "after": self.after.to_dict(),
            "receipts_written": list(self.receipts_written),
        }


def dump_schema_migration_receipt(receipt: SchemaMigrationReceipt) -> dict[str, Any]:
    payload = {
        "receipt_schema_version": receipt.receipt_schema_version,
        "campaign_id": receipt.campaign_id,
        "artifact_ref": receipt.artifact_ref,
        "artifact_kind": receipt.artifact_kind,
        "source_schema_version": receipt.source_schema_version,
        "target_schema_version": receipt.target_schema_version,
        "source_sha256": receipt.source_sha256,
        "migrated_payload_sha256": receipt.migrated_payload_sha256,
        "migrated_payload": dict(receipt.migrated_payload),
        "migration_steps": list(receipt.migration_steps),
        "migration_engine": receipt.migration_engine,
    }
    load_schema_migration_receipt(payload)
    return payload


def _artifact_kind_for_ref(ref: str) -> str | None:
    path = PurePosixPath(ref)
    if len(path.parts) == 1:
        return _DIRECT.get(path.name)
    if len(path.parts) == 2 and path.parts[0] == "transitions" and _TRANSITION.fullmatch(path.name):
        return "transition"
    return None


def _validate_ref(ref: str) -> None:
    path = PurePosixPath(ref)
    if path.is_absolute() or ".." in path.parts or any(":" in part for part in path.parts):
        raise _integrity("schema migration artifact_ref must be workspace-relative and unambiguous")
    if _artifact_kind_for_ref(ref) is None:
        raise _integrity("schema migration artifact_ref is not a canonical Campaign semantic artifact")


def load_schema_migration_receipt(value: Any) -> SchemaMigrationReceipt:
    source: Path | None = None
    if isinstance(value, (str, Path)):
        source = Path(value)
        try:
            value = yaml.safe_load(source.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            raise _integrity(f"could not read schema migration receipt: {exc}") from exc
    if not isinstance(value, Mapping):
        raise _integrity("schema migration receipt must be a mapping")
    data = dict(value)
    if set(data) != _RECEIPT_FIELDS:
        raise _integrity("schema migration receipt fields do not match the current receipt contract")
    text_fields = (
        "campaign_id", "artifact_ref", "artifact_kind", "source_schema_version",
        "target_schema_version", "migration_engine",
    )
    if any(not isinstance(data[field], str) or not data[field] for field in text_fields):
        raise _integrity("schema migration receipt text fields must be non-empty")
    if data["receipt_schema_version"] != _RECEIPT_VERSION:
        raise _integrity("unsupported schema migration receipt version")
    if data["source_schema_version"] != LEGACY_SCHEMA_VERSION or data["target_schema_version"] != CURRENT_SCHEMA_VERSION:
        raise _integrity("schema migration receipt must bind a supported legacy version to current")
    if data["artifact_kind"] not in SUPPORTED_ARTIFACT_KINDS or data["migration_engine"] != _ENGINE:
        raise _integrity("schema migration receipt names an unsupported artifact kind or engine")
    if any(not isinstance(data[field], str) or not _SHA256.fullmatch(data[field]) for field in ("source_sha256", "migrated_payload_sha256")):
        raise _integrity("schema migration receipt digests must be lowercase SHA-256")
    _validate_ref(data["artifact_ref"])
    if data["artifact_kind"] != _artifact_kind_for_ref(data["artifact_ref"]):
        raise _integrity("schema migration receipt artifact_kind does not match artifact_ref")
    migrated = data["migrated_payload"]
    if not isinstance(migrated, Mapping):
        raise _integrity("schema migration receipt migrated_payload must be a mapping")
    migrated = dict(migrated)
    if migrated.get("schema_version") != CURRENT_SCHEMA_VERSION:
        raise _integrity("schema migration receipt payload is not current schema")
    if canonical_json_digest(migrated) != data["migrated_payload_sha256"]:
        raise _integrity("schema migration receipt migrated_payload digest mismatch", "SCHEMA_MIGRATION_RECEIPT_DIGEST_MISMATCH")
    steps = data["migration_steps"]
    if not isinstance(steps, list) or not steps or any(not isinstance(step, str) or not step for step in steps):
        raise _integrity("schema migration receipt requires non-empty migration_steps")
    receipt = SchemaMigrationReceipt(
        campaign_id=data["campaign_id"], artifact_ref=data["artifact_ref"],
        artifact_kind=data["artifact_kind"], source_schema_version=data["source_schema_version"],
        target_schema_version=data["target_schema_version"], source_sha256=data["source_sha256"],
        migrated_payload_sha256=data["migrated_payload_sha256"], migrated_payload=migrated,
        migration_steps=tuple(steps), migration_engine=data["migration_engine"],
        receipt_schema_version=data["receipt_schema_version"],
    )
    if source is not None and source.name != canonical_json_digest(dump_schema_migration_receipt(receipt)) + ".yaml":
        raise _integrity("schema migration receipt filename does not match payload", "SCHEMA_MIGRATION_RECEIPT_DIGEST_MISMATCH")
    return receipt


def _contained(path: Path, root: Path, *, directory: bool = False) -> Path:
    if path.is_symlink() or (not path.is_dir() if directory else not path.is_file()):
        raise _integrity(f"Campaign schema path is missing or unsafe: {path}", "SCHEMA_ARTIFACT_UNSAFE")
    try:
        resolved, failure = pc.resolve_containment(path, root)
    except Exception as exc:
        raise CampaignWorkspaceError(f"could not establish Campaign schema containment: {path}: {exc}") from exc
    if failure is not None or resolved is None:
        raise _integrity(f"Campaign schema path escapes workspace: {path}; failure={failure}", "SCHEMA_ARTIFACT_UNSAFE")
    return resolved


def _read_mapping(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise _integrity(f"could not read Campaign schema artifact {path.name}: {exc}", "SCHEMA_ARTIFACT_INVALID") from exc
    if not isinstance(value, Mapping):
        raise _integrity(f"Campaign schema artifact must be a mapping: {path.name}", "SCHEMA_ARTIFACT_INVALID")
    return dict(value)


def _exclusive_write(path: Path, payload: Mapping[str, Any]) -> bool:
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        if dump_schema_migration_receipt(load_schema_migration_receipt(path)) == dict(payload):
            return False
        raise CampaignTransactionError(f"schema migration receipt path contains divergent content: {path.name}")
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump(dict(payload), handle, sort_keys=False, allow_unicode=True)
        handle.flush()
        os.fsync(handle.fileno())
    return True


class CampaignSchemaEvolutionService:
    """Inspect and qualify deterministic representation upgrades without rewriting history."""

    def __init__(self, workspace: str | Path) -> None:
        self.store = CampaignStore(workspace)

    @property
    def receipts_dir(self) -> Path:
        return self.store.root / "schema-migrations"

    def status(self) -> CampaignSchemaStatus:
        if not self.store.is_initialized():
            raise CampaignNotInitializedError(f"campaign workspace is not initialized: {self.store.root}")
        self.store.recover_lifecycle_transactions()
        state = self.store.load_state()
        receipts = self._load_receipts()
        artifacts = tuple(self._inspect(ref, kind, path, state, receipts) for ref, kind, path in self._artifact_paths())
        return CampaignSchemaStatus(
            campaign_id=state.campaign_id,
            current_schema_version=CURRENT_SCHEMA_VERSION,
            upgrade_required=any(item.migration_status == "pending" for item in artifacts),
            artifacts=artifacts,
            receipt_count=len(receipts),
        )

    def upgrade(self) -> CampaignSchemaUpgradeResult:
        before = self.status()
        written: list[str] = []
        for item in before.artifacts:
            if item.migration_status != "pending":
                continue
            path = self.store.root / PurePosixPath(item.artifact_ref)
            receipt = self._build_receipt(item.artifact_ref, item.artifact_kind, path, self.store.load_state())
            if receipt is None:
                continue
            payload = dump_schema_migration_receipt(receipt)
            self._ensure_receipts_dir()
            destination = self.receipts_dir / (canonical_json_digest(payload) + ".yaml")
            if _exclusive_write(destination, payload):
                written.append(destination.relative_to(self.store.root).as_posix())
        after = self.status()
        if after.upgrade_required:
            raise CampaignTransactionError("Campaign schema upgrade did not qualify every legacy artifact; workspace may have changed concurrently")
        return CampaignSchemaUpgradeResult(before, after, tuple(written))

    def _artifact_paths(self) -> tuple[tuple[str, str, Path], ...]:
        root = self.store.root
        result: list[tuple[str, str, Path]] = []
        for ref, kind, path in (
            ("campaign-state.yaml", "campaign_state", self.store.workspace.state_path),
            ("trace.yaml", "campaign_trace", self.store.workspace.trace_path),
        ):
            _contained(path, root)
            result.append((ref, kind, path))
        for ref, kind, path in (
            ("campaign-policy.yaml", "campaign_policy", self.store.workspace.policy_path),
            ("campaign-handoff.yaml", "campaign_handoff", self.store.workspace.handoff_path),
        ):
            if os.path.lexists(path):
                _contained(path, root)
                result.append((ref, kind, path))
        transitions = self.store.workspace.transitions_dir
        _contained(transitions, root, directory=True)
        for path in sorted(transitions.glob("*.yaml")):
            _contained(path, root)
            result.append((f"transitions/{path.name}", "transition", path))
        return tuple(result)

    def _migration(self, ref: str, kind: str, path: Path, state: CampaignState) -> tuple[SchemaMigrationResult, str]:
        source_sha = sha256_file(_contained(path, self.store.root))
        try:
            migration = migrate_payload(_read_mapping(path), artifact_kind=kind)
            self._validate_migrated(migration, kind, state)
        except (SchemaMigrationError, ContractError) as exc:
            raise _integrity(f"Campaign artifact {ref} cannot migrate to current schema: {exc}", "SCHEMA_MIGRATION_UNAVAILABLE") from exc
        return migration, source_sha

    def _inspect(
        self,
        ref: str,
        kind: str,
        path: Path,
        state: CampaignState,
        receipts: tuple[tuple[str, SchemaMigrationReceipt], ...],
    ) -> CampaignSchemaArtifactStatus:
        migration, source_sha = self._migration(ref, kind, path, state)
        migrated_sha = canonical_json_digest(migration.payload)
        receipt_ref = self._matching_receipt(receipts, state.campaign_id, ref, kind, source_sha, migrated_sha, migration)
        status = "current" if migration.source_version == CURRENT_SCHEMA_VERSION else ("qualified" if receipt_ref else "pending")
        return CampaignSchemaArtifactStatus(
            ref, kind, migration.source_version, migration.target_version, source_sha,
            migrated_sha, migration.migration_steps, status, receipt_ref,
        )

    def _build_receipt(self, ref: str, kind: str, path: Path, state: CampaignState) -> SchemaMigrationReceipt | None:
        migration, source_sha = self._migration(ref, kind, path, state)
        if migration.source_version == CURRENT_SCHEMA_VERSION:
            return None
        return SchemaMigrationReceipt(
            campaign_id=state.campaign_id, artifact_ref=ref, artifact_kind=kind,
            source_schema_version=migration.source_version,
            target_schema_version=migration.target_version,
            source_sha256=source_sha,
            migrated_payload_sha256=canonical_json_digest(migration.payload),
            migrated_payload=migration.payload,
            migration_steps=migration.migration_steps,
        )

    @staticmethod
    def _validate_migrated(migration: SchemaMigrationResult, kind: str, state: CampaignState) -> None:
        payload = migration.payload
        if kind == "campaign_state":
            model = load_campaign_state(payload)
        elif kind == "transition":
            load_transition_record(payload)
            return
        elif kind == "campaign_policy":
            model = load_campaign_policy(payload)
        elif kind == "campaign_trace":
            model = load_campaign_trace(payload)
        elif kind == "campaign_handoff":
            model = load_campaign_handoff(payload, current_state=state)
        else:  # pragma: no cover
            raise SchemaMigrationError(f"unsupported artifact kind: {kind}")
        if model.campaign_id != state.campaign_id:
            raise ContractError(f"{kind} campaign_id does not match campaign-state")

    def _ensure_receipts_dir(self) -> None:
        if os.path.lexists(self.receipts_dir):
            _contained(self.receipts_dir, self.store.root, directory=True)
            return
        self.receipts_dir.mkdir()
        _contained(self.receipts_dir, self.store.root, directory=True)

    def _load_receipts(self) -> tuple[tuple[str, SchemaMigrationReceipt], ...]:
        if not os.path.lexists(self.receipts_dir):
            return ()
        _contained(self.receipts_dir, self.store.root, directory=True)
        result = []
        for path in sorted(self.receipts_dir.iterdir()):
            _contained(path, self.store.root)
            if path.suffix != ".yaml":
                raise _integrity("schema migration receipt directory contains a non-YAML entry")
            result.append((path.relative_to(self.store.root).as_posix(), load_schema_migration_receipt(path)))
        return tuple(result)

    @staticmethod
    def _matching_receipt(
        receipts: tuple[tuple[str, SchemaMigrationReceipt], ...],
        campaign_id: str,
        ref: str,
        kind: str,
        source_sha: str,
        migrated_sha: str,
        migration: SchemaMigrationResult,
    ) -> str | None:
        for receipt_ref, receipt in receipts:
            if (
                receipt.campaign_id == campaign_id
                and receipt.artifact_ref == ref
                and receipt.artifact_kind == kind
                and receipt.source_schema_version == migration.source_version
                and receipt.target_schema_version == migration.target_version
                and receipt.source_sha256 == source_sha
                and receipt.migrated_payload_sha256 == migrated_sha
                and dict(receipt.migrated_payload) == migration.payload
                and receipt.migration_steps == migration.migration_steps
            ):
                return receipt_ref
        return None
