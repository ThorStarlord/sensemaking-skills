"""P8 artifact/evidence lineage for durable Sensemaking campaigns.

Lineage records mechanically verifiable provenance and explicit evidence
consumption. It never decides whether evidence is persuasive, sufficient, or
semantically warrants a transition.

P8 adds two durable structures lazily beneath an existing campaign workspace:

``lineage/evidence/<sha256>``
    Content-addressed snapshots for evidence whose original workspace path is
    not already content-addressed by the Campaign contract.

``lineage/consumptions/<transition-id>/<receipt-digest>.yaml``
    Append-only precommit intent binding one transition id to the exact evidence
    bytes supplied by the agent-authored decision. The receipt filename is the
    canonical payload digest. A lifecycle failure may leave an orphan intent;
    lineage only treats a receipt as consumption when the transition itself is
    durably committed.

The P4 artifact store remains authoritative for admitted artifacts. P8 does not
grandfather arbitrary ``artifacts/`` files as evidence and does not create a
second semantic decision log.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

import yaml

from sensemaking_skills import path_containment as pc

from .admission import (
    ArtifactAdmission,
    ArtifactAdmissionContractError,
    load_artifact_admission,
    sha256_file,
)
from .errors import (
    CampaignIntegrityError,
    CampaignTransactionError,
    CampaignWorkspaceError,
)
from .service import CampaignService, CampaignSnapshot
from .store import CampaignStore


_SCHEMA_VERSION = "1"
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_RECEIPT_FIELDS = {
    "campaign_id",
    "transition_id",
    "evidence_bindings",
    "schema_version",
}
_BINDING_FIELDS = {
    "source_ref",
    "immutable_ref",
    "sha256",
    "kind",
    "provenance",
}
_KINDS = {"raw_evidence", "admitted_artifact", "admission_receipt"}


class CampaignLineageContractError(ValueError):
    """Raised when a lineage receipt cannot be represented without ambiguity."""


@dataclass(frozen=True)
class EvidenceBinding:
    source_ref: str
    immutable_ref: str
    sha256: str
    kind: str
    provenance: Mapping[str, Any]


@dataclass(frozen=True)
class ConsumptionReceipt:
    campaign_id: str
    transition_id: str
    evidence_bindings: tuple[EvidenceBinding, ...]
    schema_version: str = _SCHEMA_VERSION


@dataclass(frozen=True)
class LineageEvidence:
    ref: str
    kind: str
    current_sha256: str
    immutable_by_source_contract: bool
    provenance: Mapping[str, Any]


@dataclass(frozen=True)
class ConsumptionEdge:
    transition_id: str
    transition_digest: str
    evidence_ref: str
    binding_status: str
    consumed_sha256: str | None
    immutable_ref: str | None
    source_matches_consumed_bytes: bool | None
    kind: str | None
    provenance: Mapping[str, Any]


@dataclass(frozen=True)
class TransitionLineage:
    transition_id: str
    transition_digest: str
    evidence_refs: tuple[str, ...]
    binding_status: str
    receipt_ref: str | None


@dataclass(frozen=True)
class CampaignLineageResult:
    campaign_id: str
    evidence: tuple[LineageEvidence, ...]
    transitions: tuple[TransitionLineage, ...]
    consumption_edges: tuple[ConsumptionEdge, ...]
    orphan_intent_refs: tuple[str, ...]


def _canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _assert_physically_contained(path: Path, root: Path) -> None:
    try:
        resolved, failure = pc.resolve_containment(path, root)
    except Exception as exc:  # pragma: no cover - defensive fail-closed guard
        raise CampaignWorkspaceError(
            f"could not establish lineage path containment for {path}: {exc}"
        ) from exc
    if failure is not None or resolved is None:
        raise CampaignWorkspaceError(
            "campaign lineage path is not physically contained: "
            f"path={path} root={root} failure={failure}"
        )
    real_root = root.resolve(strict=False)
    if (
        pc.canonicalize_path(resolved).relative_to_root(
            pc.canonicalize_path(real_root)
        )
        is None
    ):
        raise CampaignWorkspaceError(
            f"campaign lineage path escapes its physical root: {path}"
        )


def _binding_payload(binding: EvidenceBinding) -> dict[str, Any]:
    return {
        "source_ref": binding.source_ref,
        "immutable_ref": binding.immutable_ref,
        "sha256": binding.sha256,
        "kind": binding.kind,
        "provenance": dict(binding.provenance),
    }


def _receipt_payload(receipt: ConsumptionReceipt) -> dict[str, Any]:
    return {
        "campaign_id": receipt.campaign_id,
        "transition_id": receipt.transition_id,
        "evidence_bindings": [
            _binding_payload(binding) for binding in receipt.evidence_bindings
        ],
        "schema_version": receipt.schema_version,
    }


def _require_text(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise CampaignLineageContractError(f"{field} must be a non-empty string")
    return value


def _load_binding(value: Any, *, path: str) -> EvidenceBinding:
    if not isinstance(value, Mapping):
        raise CampaignLineageContractError(f"{path} must be a mapping")
    data = dict(value)
    unknown = sorted(set(data) - _BINDING_FIELDS)
    missing = sorted(_BINDING_FIELDS - set(data))
    if unknown or missing:
        raise CampaignLineageContractError(
            f"{path} fields invalid: unknown={unknown} missing={missing}"
        )
    source_ref = _require_text(data["source_ref"], field=f"{path}.source_ref")
    immutable_ref = _require_text(
        data["immutable_ref"], field=f"{path}.immutable_ref"
    )
    digest = _require_text(data["sha256"], field=f"{path}.sha256")
    if not _SHA256_RE.fullmatch(digest):
        raise CampaignLineageContractError(f"{path}.sha256 must be lowercase SHA-256")
    kind = _require_text(data["kind"], field=f"{path}.kind")
    if kind not in _KINDS:
        raise CampaignLineageContractError(f"unsupported evidence kind: {kind!r}")
    provenance = data["provenance"]
    if not isinstance(provenance, Mapping):
        raise CampaignLineageContractError(f"{path}.provenance must be a mapping")
    for ref_name, ref_value in (
        ("source_ref", source_ref),
        ("immutable_ref", immutable_ref),
    ):
        parsed = PurePosixPath(ref_value)
        if parsed.is_absolute() or ".." in parsed.parts:
            raise CampaignLineageContractError(
                f"{path}.{ref_name} must be workspace-relative"
            )
    return EvidenceBinding(
        source_ref=source_ref,
        immutable_ref=immutable_ref,
        sha256=digest,
        kind=kind,
        provenance=dict(provenance),
    )


def load_consumption_receipt(value: Any) -> ConsumptionReceipt:
    source_path: Path | None = None
    if isinstance(value, (str, Path)):
        source_path = Path(value)
        with source_path.open(encoding="utf-8") as handle:
            value = yaml.safe_load(handle)
    if not isinstance(value, Mapping):
        raise CampaignLineageContractError("lineage consumption receipt must be a mapping")
    data = dict(value)
    unknown = sorted(set(data) - _RECEIPT_FIELDS)
    missing = sorted(_RECEIPT_FIELDS - set(data))
    if unknown or missing:
        raise CampaignLineageContractError(
            f"lineage receipt fields invalid: unknown={unknown} missing={missing}"
        )
    if data["schema_version"] != _SCHEMA_VERSION:
        raise CampaignLineageContractError(
            f"unsupported lineage schema_version: {data['schema_version']!r}"
        )
    campaign_id = _require_text(data["campaign_id"], field="campaign_id")
    transition_id = _require_text(data["transition_id"], field="transition_id")
    if not _SAFE_ID.fullmatch(transition_id):
        raise CampaignLineageContractError("unsafe transition_id in lineage receipt")
    raw_bindings = data["evidence_bindings"]
    if not isinstance(raw_bindings, list):
        raise CampaignLineageContractError("evidence_bindings must be a list")
    bindings = tuple(
        _load_binding(item, path=f"evidence_bindings[{index}]")
        for index, item in enumerate(raw_bindings)
    )
    receipt = ConsumptionReceipt(
        campaign_id=campaign_id,
        transition_id=transition_id,
        evidence_bindings=bindings,
    )
    if source_path is not None:
        if source_path.suffix != ".yaml":
            raise CampaignLineageContractError("lineage receipt must use .yaml")
        expected = _canonical_digest(_receipt_payload(receipt))
        if source_path.stem != expected:
            raise CampaignLineageContractError(
                "lineage receipt filename no longer matches canonical payload"
            )
    return receipt


def _exclusive_write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        return
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump(dict(payload), handle, sort_keys=False, allow_unicode=True)
        handle.flush()
        os.fsync(handle.fileno())


def _write_snapshot(root: Path, source: Path, digest: str) -> str:
    lineage_root = root / "lineage"
    evidence_root = lineage_root / "evidence"
    lineage_root.mkdir(exist_ok=True)
    evidence_root.mkdir(exist_ok=True)
    _assert_physically_contained(lineage_root, root)
    _assert_physically_contained(evidence_root, lineage_root)
    path = evidence_root / digest
    _assert_physically_contained(path, evidence_root)
    if path.exists():
        if path.is_symlink() or not path.is_file() or sha256_file(path) != digest:
            raise CampaignIntegrityError(
                "content-addressed lineage evidence snapshot is invalid",
                diagnostic_codes=("LINEAGE_IMMUTABLE_EVIDENCE_INVALID",),
            )
        return path.relative_to(root).as_posix()

    data = source.read_bytes()
    if hashlib.sha256(data).hexdigest() != digest:
        raise CampaignIntegrityError(
            "evidence changed while preparing lineage snapshot",
            diagnostic_codes=("LINEAGE_SOURCE_CHANGED_DURING_CAPTURE",),
        )
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        if sha256_file(path) != digest:
            raise CampaignIntegrityError(
                "lineage evidence snapshot collision",
                diagnostic_codes=("LINEAGE_IMMUTABLE_EVIDENCE_INVALID",),
            )
    else:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    return path.relative_to(root).as_posix()


def _admissions(store: CampaignStore) -> tuple[tuple[str, ArtifactAdmission], ...]:
    root = store.root
    directory = store.workspace.admissions_dir
    if not directory.is_dir():
        raise CampaignIntegrityError(
            "campaign admissions directory is missing",
            diagnostic_codes=("ARTIFACT_ADMISSIONS_DIRECTORY_MISSING",),
        )
    records: list[tuple[str, ArtifactAdmission]] = []
    for path in sorted(directory.rglob("*.yaml")):
        try:
            admission = load_artifact_admission(path)
        except (ArtifactAdmissionContractError, OSError, yaml.YAMLError) as exc:
            raise CampaignIntegrityError(
                "artifact admission receipt is invalid while reconstructing lineage",
                diagnostic_codes=("INVALID_ARTIFACT_ADMISSION",),
            ) from exc
        records.append((path.relative_to(root).as_posix(), admission))
    return tuple(records)


def _resolve_evidence(
    store: CampaignStore,
    ref: str,
    admissions: tuple[tuple[str, ArtifactAdmission], ...],
    *,
    snapshot_mutable_source: bool,
) -> EvidenceBinding:
    root = store.root
    source = root / PurePosixPath(ref)
    if source.is_symlink() or not source.is_file():
        raise CampaignIntegrityError(
            f"lineage evidence source is missing or not a regular file: {ref}",
            diagnostic_codes=("LINEAGE_EVIDENCE_SOURCE_INVALID",),
        )
    digest = sha256_file(source)

    if ref.startswith("evidence/"):
        immutable_ref = (
            _write_snapshot(root, source, digest) if snapshot_mutable_source else ref
        )
        return EvidenceBinding(
            source_ref=ref,
            immutable_ref=immutable_ref,
            sha256=digest,
            kind="raw_evidence",
            provenance={"source": "campaign_evidence"},
        )

    if ref.startswith("artifacts/"):
        matches = [
            (receipt_ref, admission)
            for receipt_ref, admission in admissions
            if admission.artifact_ref == ref
        ]
        if not matches:
            raise CampaignIntegrityError(
                f"admitted artifact has no admission provenance: {ref}",
                diagnostic_codes=("LINEAGE_ARTIFACT_ADMISSION_MISSING",),
            )
        expected = {admission.artifact_sha256 for _, admission in matches}
        if expected != {digest}:
            raise CampaignIntegrityError(
                "admitted artifact lineage digest disagrees with admission receipt",
                diagnostic_codes=("ADMITTED_ARTIFACT_DIGEST_MISMATCH",),
            )
        return EvidenceBinding(
            source_ref=ref,
            immutable_ref=ref,
            sha256=digest,
            kind="admitted_artifact",
            provenance={
                "artifact_id": matches[0][1].artifact_id,
                "admission_refs": [receipt_ref for receipt_ref, _ in matches],
            },
        )

    if ref.startswith("admissions/"):
        matches = [item for item in admissions if item[0] == ref]
        if len(matches) != 1:
            raise CampaignIntegrityError(
                f"admission receipt provenance is ambiguous or missing: {ref}",
                diagnostic_codes=("LINEAGE_ADMISSION_PROVENANCE_INVALID",),
            )
        admission = matches[0][1]
        immutable_ref = (
            _write_snapshot(root, source, digest) if snapshot_mutable_source else ref
        )
        return EvidenceBinding(
            source_ref=ref,
            immutable_ref=immutable_ref,
            sha256=digest,
            kind="admission_receipt",
            provenance={
                "artifact_id": admission.artifact_id,
                "artifact_ref": admission.artifact_ref,
                "artifact_sha256": admission.artifact_sha256,
                "validator": admission.validator,
                "validation_timestamp": admission.validation_timestamp,
            },
        )

    raise CampaignIntegrityError(
        f"unsupported Campaign evidence ref in lineage: {ref}",
        diagnostic_codes=("LINEAGE_EVIDENCE_KIND_UNKNOWN",),
    )


def _receipt_ref(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


class CampaignLineageService:
    """Prepare immutable evidence consumption and reconstruct read-only lineage."""

    def __init__(self, workspace: str | Path) -> None:
        self.lifecycle = CampaignService(workspace)
        self.store = self.lifecycle.store

    def prepare_consumption(
        self,
        *,
        transition_id: str,
        evidence_refs: tuple[str, ...],
    ) -> str | None:
        """Persist append-only evidence intent before the semantic lifecycle commit.

        An orphan receipt is harmless if the later transition fails. Retrying the
        same transition id is idempotent only when the exact evidence binding is
        unchanged; a conflicting intent fails closed.
        """
        if not evidence_refs:
            return None
        if not _SAFE_ID.fullmatch(transition_id):
            raise CampaignTransactionError("unsafe transition id for lineage receipt")

        snapshot = self.lifecycle.resume()
        available = set(snapshot.evidence_refs)
        missing = [ref for ref in evidence_refs if ref not in available]
        if missing:
            raise CampaignTransactionError(
                "lineage consumption references missing evidence: " + ", ".join(missing)
            )
        admissions = _admissions(self.store)
        bindings = tuple(
            _resolve_evidence(
                self.store,
                ref,
                admissions,
                snapshot_mutable_source=True,
            )
            for ref in evidence_refs
        )
        receipt = ConsumptionReceipt(
            campaign_id=snapshot.state.campaign_id,
            transition_id=transition_id,
            evidence_bindings=bindings,
        )
        payload = _receipt_payload(receipt)
        digest = _canonical_digest(payload)

        lineage_root = self.store.root / "lineage"
        consumptions_root = lineage_root / "consumptions"
        transition_root = consumptions_root / transition_id
        lineage_root.mkdir(exist_ok=True)
        consumptions_root.mkdir(exist_ok=True)
        transition_root.mkdir(exist_ok=True)
        _assert_physically_contained(lineage_root, self.store.root)
        _assert_physically_contained(consumptions_root, lineage_root)
        _assert_physically_contained(transition_root, consumptions_root)

        existing = sorted(transition_root.glob("*.yaml"))
        for path in existing:
            try:
                loaded = load_consumption_receipt(path)
            except (CampaignLineageContractError, OSError, yaml.YAMLError) as exc:
                raise CampaignIntegrityError(
                    "existing lineage consumption intent is invalid",
                    diagnostic_codes=("INVALID_LINEAGE_CONSUMPTION_RECEIPT",),
                ) from exc
            if _canonical_digest(_receipt_payload(loaded)) != digest:
                raise CampaignTransactionError(
                    "transition id already has a different lineage consumption intent"
                )
        path = transition_root / f"{digest}.yaml"
        _exclusive_write_yaml(path, payload)
        return _receipt_ref(self.store.root, path)

    def inspect(self) -> CampaignLineageResult:
        """Reconstruct evidence identities and only explicit transition consumption."""
        snapshot = self.lifecycle.resume()
        admissions = _admissions(self.store)
        evidence_records = tuple(
            self._current_evidence_record(ref, admissions)
            for ref in snapshot.evidence_refs
        )

        digest_by_transition: dict[str, str] = {}
        for event in snapshot.trace.events:
            if isinstance(event, Mapping) and event.get("event") == "transition_committed":
                transition_id = event.get("transition_id")
                transition_digest = event.get("transition_digest")
                if isinstance(transition_id, str) and isinstance(transition_digest, str):
                    digest_by_transition[transition_id] = transition_digest

        transition_results: list[TransitionLineage] = []
        edges: list[ConsumptionEdge] = []
        committed_ids = {transition.id for transition in snapshot.transitions}
        for transition in snapshot.transitions:
            transition_digest = digest_by_transition[transition.id]
            receipt_ref, receipt = self._receipt_for_transition(transition.id)
            if receipt is None:
                transition_results.append(
                    TransitionLineage(
                        transition_id=transition.id,
                        transition_digest=transition_digest,
                        evidence_refs=transition.evidence,
                        binding_status="legacy_unbound",
                        receipt_ref=None,
                    )
                )
                for ref in transition.evidence:
                    current = _resolve_evidence(
                        self.store,
                        ref,
                        admissions,
                        snapshot_mutable_source=False,
                    )
                    edges.append(
                        ConsumptionEdge(
                            transition_id=transition.id,
                            transition_digest=transition_digest,
                            evidence_ref=ref,
                            binding_status="legacy_unbound",
                            consumed_sha256=None,
                            immutable_ref=None,
                            source_matches_consumed_bytes=None,
                            kind=current.kind,
                            provenance=current.provenance,
                        )
                    )
                continue

            if receipt.campaign_id != snapshot.state.campaign_id:
                raise CampaignIntegrityError(
                    "lineage receipt belongs to a different campaign",
                    diagnostic_codes=("LINEAGE_CAMPAIGN_ID_MISMATCH",),
                )
            receipt_refs = tuple(binding.source_ref for binding in receipt.evidence_bindings)
            if receipt_refs != transition.evidence:
                raise CampaignIntegrityError(
                    "lineage receipt evidence refs do not match TransitionRecord.evidence",
                    diagnostic_codes=("LINEAGE_EVIDENCE_REFERENCE_MISMATCH",),
                )

            transition_results.append(
                TransitionLineage(
                    transition_id=transition.id,
                    transition_digest=transition_digest,
                    evidence_refs=transition.evidence,
                    binding_status="bound",
                    receipt_ref=receipt_ref,
                )
            )
            for binding in receipt.evidence_bindings:
                immutable = self.store.root / PurePosixPath(binding.immutable_ref)
                if immutable.is_symlink() or not immutable.is_file():
                    raise CampaignIntegrityError(
                        "immutable lineage evidence is missing",
                        diagnostic_codes=("LINEAGE_IMMUTABLE_EVIDENCE_MISSING",),
                    )
                if sha256_file(immutable) != binding.sha256:
                    raise CampaignIntegrityError(
                        "immutable lineage evidence no longer matches its consumption digest",
                        diagnostic_codes=("LINEAGE_IMMUTABLE_EVIDENCE_DIGEST_MISMATCH",),
                    )
                source = self.store.root / PurePosixPath(binding.source_ref)
                source_matches = (
                    source.is_file()
                    and not source.is_symlink()
                    and sha256_file(source) == binding.sha256
                )
                edges.append(
                    ConsumptionEdge(
                        transition_id=transition.id,
                        transition_digest=transition_digest,
                        evidence_ref=binding.source_ref,
                        binding_status="bound",
                        consumed_sha256=binding.sha256,
                        immutable_ref=binding.immutable_ref,
                        source_matches_consumed_bytes=source_matches,
                        kind=binding.kind,
                        provenance=binding.provenance,
                    )
                )

        orphan_refs = self._orphan_intents(committed_ids)
        return CampaignLineageResult(
            campaign_id=snapshot.state.campaign_id,
            evidence=evidence_records,
            transitions=tuple(transition_results),
            consumption_edges=tuple(edges),
            orphan_intent_refs=orphan_refs,
        )

    def _current_evidence_record(
        self,
        ref: str,
        admissions: tuple[tuple[str, ArtifactAdmission], ...],
    ) -> LineageEvidence:
        binding = _resolve_evidence(
            self.store,
            ref,
            admissions,
            snapshot_mutable_source=False,
        )
        return LineageEvidence(
            ref=ref,
            kind=binding.kind,
            current_sha256=binding.sha256,
            immutable_by_source_contract=binding.kind == "admitted_artifact",
            provenance=binding.provenance,
        )

    def _receipt_for_transition(
        self, transition_id: str
    ) -> tuple[str | None, ConsumptionReceipt | None]:
        root = self.store.root / "lineage" / "consumptions" / transition_id
        if not root.exists():
            return None, None
        if root.is_symlink() or not root.is_dir():
            raise CampaignIntegrityError(
                "lineage transition receipt path is invalid",
                diagnostic_codes=("INVALID_LINEAGE_CONSUMPTION_RECEIPT",),
            )
        paths = sorted(root.glob("*.yaml"))
        if not paths:
            return None, None
        if len(paths) != 1:
            raise CampaignIntegrityError(
                "committed transition has multiple lineage consumption receipts",
                diagnostic_codes=("AMBIGUOUS_LINEAGE_CONSUMPTION_RECEIPT",),
            )
        try:
            receipt = load_consumption_receipt(paths[0])
        except (CampaignLineageContractError, OSError, yaml.YAMLError) as exc:
            raise CampaignIntegrityError(
                "committed transition lineage receipt is invalid",
                diagnostic_codes=("INVALID_LINEAGE_CONSUMPTION_RECEIPT",),
            ) from exc
        if receipt.transition_id != transition_id:
            raise CampaignIntegrityError(
                "lineage receipt transition id does not match its directory",
                diagnostic_codes=("LINEAGE_TRANSITION_ID_MISMATCH",),
            )
        return _receipt_ref(self.store.root, paths[0]), receipt

    def _orphan_intents(self, committed_ids: set[str]) -> tuple[str, ...]:
        root = self.store.root / "lineage" / "consumptions"
        if not root.exists():
            return ()
        refs: list[str] = []
        for directory in sorted(root.iterdir()):
            if directory.name in committed_ids or not directory.is_dir():
                continue
            for path in sorted(directory.glob("*.yaml")):
                refs.append(_receipt_ref(self.store.root, path))
        return tuple(refs)
