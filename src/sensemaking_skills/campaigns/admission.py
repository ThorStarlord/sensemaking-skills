"""Strict durable receipt for P4 validated-artifact admission.

This module defines a small application-layer contract. It records only
mechanically verifiable facts about one canonical validator run; it does not
interpret artifact meaning or make campaign decisions.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

import yaml


_SCHEMA_VERSION = "1"
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_FIELDS = {
    "campaign_id",
    "artifact_id",
    "artifact_ref",
    "artifact_sha256",
    "validator",
    "validation_timestamp",
    "router_sha256",
    "validator_sha256",
    "validation_result_sha256",
    "validation_result",
    "schema_version",
}


class ArtifactAdmissionContractError(ValueError):
    """Raised when a persisted admission receipt loses mechanical integrity."""


@dataclass(frozen=True)
class ArtifactAdmission:
    campaign_id: str
    artifact_id: str
    artifact_ref: str
    artifact_sha256: str
    validator: str
    validation_timestamp: str
    router_sha256: str
    validator_sha256: str
    validation_result_sha256: str
    validation_result: Mapping[str, Any]
    schema_version: str = _SCHEMA_VERSION


def canonical_json_digest(value: Any) -> str:
    """Return a deterministic SHA-256 over JSON-compatible validation data."""
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require_text(data: Mapping[str, Any], field: str) -> str:
    value = data.get(field)
    if not isinstance(value, str) or not value:
        raise ArtifactAdmissionContractError(
            f"artifact admission field {field!r} must be a non-empty string"
        )
    return value


def _require_sha256(data: Mapping[str, Any], field: str) -> str:
    value = _require_text(data, field)
    if not _SHA256_RE.fullmatch(value):
        raise ArtifactAdmissionContractError(
            f"artifact admission field {field!r} must be a lowercase SHA-256 digest"
        )
    return value


def _validate_artifact_ref(value: str, artifact_id: str) -> None:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise ArtifactAdmissionContractError("artifact_ref must be workspace-relative")
    if len(path.parts) < 3 or path.parts[0] != "artifacts":
        raise ArtifactAdmissionContractError(
            "artifact_ref must live beneath the campaign artifacts/ directory"
        )
    if path.parts[1] != artifact_id:
        raise ArtifactAdmissionContractError(
            "artifact_ref artifact-id directory must match artifact_id"
        )


def dump_artifact_admission(admission: ArtifactAdmission) -> dict[str, Any]:
    payload = {
        "campaign_id": admission.campaign_id,
        "artifact_id": admission.artifact_id,
        "artifact_ref": admission.artifact_ref,
        "artifact_sha256": admission.artifact_sha256,
        "validator": admission.validator,
        "validation_timestamp": admission.validation_timestamp,
        "router_sha256": admission.router_sha256,
        "validator_sha256": admission.validator_sha256,
        "validation_result_sha256": admission.validation_result_sha256,
        "validation_result": dict(admission.validation_result),
        "schema_version": admission.schema_version,
    }
    load_artifact_admission(payload)
    return payload


def load_artifact_admission(value: Any) -> ArtifactAdmission:
    if isinstance(value, (str, Path)):
        with Path(value).open(encoding="utf-8") as handle:
            value = yaml.safe_load(handle)
    if not isinstance(value, Mapping):
        raise ArtifactAdmissionContractError("artifact admission must be a mapping")

    data = dict(value)
    unknown = sorted(set(data) - _FIELDS)
    missing = sorted(_FIELDS - set(data))
    if unknown:
        raise ArtifactAdmissionContractError(
            f"artifact admission has unknown fields: {unknown}"
        )
    if missing:
        raise ArtifactAdmissionContractError(
            f"artifact admission is missing required fields: {missing}"
        )
    if data.get("schema_version") != _SCHEMA_VERSION:
        raise ArtifactAdmissionContractError(
            f"unsupported artifact admission schema_version: {data.get('schema_version')!r}"
        )

    campaign_id = _require_text(data, "campaign_id")
    artifact_id = _require_text(data, "artifact_id")
    artifact_ref = _require_text(data, "artifact_ref")
    artifact_sha256 = _require_sha256(data, "artifact_sha256")
    validator = _require_text(data, "validator")
    validation_timestamp = _require_text(data, "validation_timestamp")
    router_sha256 = _require_sha256(data, "router_sha256")
    validator_sha256 = _require_sha256(data, "validator_sha256")
    validation_result_sha256 = _require_sha256(data, "validation_result_sha256")
    _validate_artifact_ref(artifact_ref, artifact_id)

    validation_result = data.get("validation_result")
    if not isinstance(validation_result, Mapping):
        raise ArtifactAdmissionContractError("validation_result must be a mapping")
    validation_result = dict(validation_result)
    if validation_result.get("valid") is not True:
        raise ArtifactAdmissionContractError(
            "artifact admission may only persist a validator result with valid=true"
        )
    if validation_result.get("artifact_id") != artifact_id:
        raise ArtifactAdmissionContractError(
            "validation_result artifact_id must match admission artifact_id"
        )
    if validation_result.get("validator") != validator:
        raise ArtifactAdmissionContractError(
            "validation_result validator must match admission validator"
        )
    if validation_result.get("validation_timestamp") != validation_timestamp:
        raise ArtifactAdmissionContractError(
            "validation_result timestamp must match admission timestamp"
        )
    if canonical_json_digest(validation_result) != validation_result_sha256:
        raise ArtifactAdmissionContractError(
            "validation_result no longer matches validation_result_sha256"
        )

    return ArtifactAdmission(
        campaign_id=campaign_id,
        artifact_id=artifact_id,
        artifact_ref=artifact_ref,
        artifact_sha256=artifact_sha256,
        validator=validator,
        validation_timestamp=validation_timestamp,
        router_sha256=router_sha256,
        validator_sha256=validator_sha256,
        validation_result_sha256=validation_result_sha256,
        validation_result=validation_result,
        schema_version=_SCHEMA_VERSION,
    )
