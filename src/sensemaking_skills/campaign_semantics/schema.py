"""Deterministic, one-way schema evolution for durable Campaign artifacts.

Schema migration is representation-only. It may normalize historical aliases or
move already-sanctioned extension data, but it must not infer semantic meaning,
choose work, or grant authority.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping

CURRENT_SCHEMA_VERSION = "2"
LEGACY_SCHEMA_VERSION = "1"
SUPPORTED_SCHEMA_VERSIONS = (LEGACY_SCHEMA_VERSION, CURRENT_SCHEMA_VERSION)
SUPPORTED_ARTIFACT_KINDS = frozenset(
    {
        "campaign_state",
        "transition",
        "campaign_policy",
        "campaign_trace",
        "campaign_handoff",
    }
)


class SchemaMigrationError(ValueError):
    """Raised when a representation cannot be upgraded without guessing."""


@dataclass(frozen=True)
class SchemaMigrationResult:
    artifact_kind: str
    source_version: str
    target_version: str
    migration_steps: tuple[str, ...]
    payload: dict[str, Any]

    @property
    def migrated(self) -> bool:
        return self.source_version != self.target_version


def detect_schema_version(value: Mapping[str, Any], *, path: str = "artifact") -> str:
    """Return the explicit or historical implicit Campaign schema version.

    The original Campaign contract treated a missing ``schema_version`` as v1,
    so absence remains an accepted v1 representation. No other coercion is
    performed: integer versions and unknown future versions fail closed.
    """

    if not isinstance(value, Mapping):
        raise SchemaMigrationError(f"{path} must be a mapping")
    version = value.get("schema_version", LEGACY_SCHEMA_VERSION)
    if not isinstance(version, str):
        raise SchemaMigrationError(
            f"schema_version at {path} must be a string, got {type(version).__name__}"
        )
    if version not in SUPPORTED_SCHEMA_VERSIONS:
        raise SchemaMigrationError(
            f"unsupported schema_version at {path}: {version!r}; "
            f"supported={list(SUPPORTED_SCHEMA_VERSIONS)!r}"
        )
    return version


def migrate_payload(
    value: Mapping[str, Any],
    *,
    artifact_kind: str,
    target_version: str = CURRENT_SCHEMA_VERSION,
) -> SchemaMigrationResult:
    """Upgrade one Campaign artifact representation to the current schema.

    Only forward migration to the current version is supported. The input is
    deep-copied and never mutated.
    """

    if artifact_kind not in SUPPORTED_ARTIFACT_KINDS:
        raise SchemaMigrationError(f"unsupported Campaign artifact kind: {artifact_kind!r}")
    if target_version != CURRENT_SCHEMA_VERSION:
        raise SchemaMigrationError(
            f"only one-way migration to current schema {CURRENT_SCHEMA_VERSION!r} is supported"
        )

    source_version = detect_schema_version(value, path=artifact_kind)
    payload = deepcopy(dict(value))
    if source_version == CURRENT_SCHEMA_VERSION:
        if artifact_kind == "campaign_handoff" and payload.get("current_state") is not None:
            nested = payload["current_state"]
            if not isinstance(nested, Mapping):
                raise SchemaMigrationError(
                    "campaign_handoff.current_state must be a mapping when present"
                )
            nested_version = detect_schema_version(
                nested, path="campaign_handoff.current_state"
            )
            if nested_version != CURRENT_SCHEMA_VERSION:
                raise SchemaMigrationError(
                    "current campaign_handoff cannot embed a legacy current_state"
                )
        return SchemaMigrationResult(
            artifact_kind=artifact_kind,
            source_version=source_version,
            target_version=CURRENT_SCHEMA_VERSION,
            migration_steps=(),
            payload=payload,
        )

    if source_version != LEGACY_SCHEMA_VERSION:  # defensive future-proofing
        raise SchemaMigrationError(
            f"no migration path from {source_version!r} to {CURRENT_SCHEMA_VERSION!r}"
        )

    steps: list[str] = []
    if artifact_kind == "campaign_state":
        _migrate_state_v1_to_v2(payload)
        steps.append("campaign_state:v1->v2")
    elif artifact_kind == "campaign_handoff":
        nested = payload.get("current_state")
        if nested is not None:
            if not isinstance(nested, Mapping):
                raise SchemaMigrationError(
                    "campaign_handoff.current_state must be a mapping when present"
                )
            nested_result = migrate_payload(nested, artifact_kind="campaign_state")
            payload["current_state"] = nested_result.payload
            steps.extend(
                f"campaign_handoff.current_state/{step}"
                for step in nested_result.migration_steps
            )
        _migrate_handoff_v1_to_v2(payload)
        steps.append("campaign_handoff:v1->v2")
    else:
        payload["schema_version"] = CURRENT_SCHEMA_VERSION
        steps.append(f"{artifact_kind}:v1->v2")

    if payload.get("schema_version") != CURRENT_SCHEMA_VERSION:
        raise SchemaMigrationError(
            f"migration for {artifact_kind!r} did not produce schema_version "
            f"{CURRENT_SCHEMA_VERSION!r}"
        )
    return SchemaMigrationResult(
        artifact_kind=artifact_kind,
        source_version=source_version,
        target_version=CURRENT_SCHEMA_VERSION,
        migration_steps=tuple(steps),
        payload=payload,
    )


def _migrate_state_v1_to_v2(payload: dict[str, Any]) -> None:
    """Canonicalize v1's top-level ``owner_routing`` extension into v2."""

    if "owner_routing" in payload:
        routing = payload.pop("owner_routing")
        extensions = payload.get("extensions")
        if extensions is None:
            extensions = {}
        if not isinstance(extensions, Mapping):
            raise SchemaMigrationError("campaign_state.extensions must be a mapping")
        extensions = deepcopy(dict(extensions))
        if "owner_routing" in extensions and extensions["owner_routing"] != routing:
            raise SchemaMigrationError(
                "campaign_state has conflicting owner_routing representations"
            )
        extensions["owner_routing"] = routing
        payload["extensions"] = extensions
    payload["schema_version"] = CURRENT_SCHEMA_VERSION


def _migrate_handoff_v1_to_v2(payload: dict[str, Any]) -> None:
    """Canonicalize v1's ``allowed_actions`` alias into v2."""

    if "allowed_actions" in payload:
        legacy_actions = payload.pop("allowed_actions")
        if (
            "allowed_next_actions" in payload
            and payload["allowed_next_actions"] != legacy_actions
        ):
            raise SchemaMigrationError(
                "campaign_handoff has conflicting allowed_actions representations"
            )
        payload["allowed_next_actions"] = legacy_actions
    payload["schema_version"] = CURRENT_SCHEMA_VERSION
