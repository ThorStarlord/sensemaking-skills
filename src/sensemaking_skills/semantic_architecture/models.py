"""Mechanical representation models for the Sensemaking Semantic Architecture.

These records preserve observations, provenance, and bounded repository structure.
They do not decide semantic truth, architectural quality, warranted responsibility,
or which Skill should run.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass
from enum import Enum
from typing import Any, Mapping


class _TextEnum(str, Enum):
    def __str__(self) -> str:
        return self.value


class Completeness(_TextEnum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    UNKNOWN = "unknown"


class Currentness(_TextEnum):
    PINNED_SNAPSHOT = "pinned_snapshot"
    OBSERVED_CURRENT = "observed_current"
    INHERITED_CURRENTNESS = "inherited_currentness"
    UNVERIFIED = "unverified"


class ObservationKind(_TextEnum):
    FILE_CONTAINMENT = "file_containment"
    PYTHON_IMPORT = "python_import"
    MANIFEST_DEPENDENCY = "manifest_dependency"
    EXACT_SEARCH_MATCH = "exact_search_match"
    EXACT_SEARCH_SUMMARY = "exact_search_summary"


@dataclass(frozen=True)
class SemanticDiagnostic:
    code: str
    detail: str
    path: str = ""


@dataclass(frozen=True)
class SemanticObservation:
    id: str
    kind: ObservationKind
    subject: str
    predicate: str
    object: str
    evidence_refs: tuple[str, ...]
    source: str
    scope: str
    completeness: Completeness
    currentness: Currentness
    target_ref: str
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SemanticProbeResult:
    probe_id: str
    target_ref: str
    scope: str
    completeness: Completeness
    observations: tuple[SemanticObservation, ...]
    diagnostics: tuple[SemanticDiagnostic, ...] = ()
    semantic_truth_established: bool = False


@dataclass(frozen=True)
class SemanticMapEntity:
    id: str
    kind: str
    locator: str
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class SemanticMapRelation:
    id: str
    subject: str
    predicate: str
    object: str
    epistemic_status: str
    evidence_refs: tuple[str, ...]
    source_observation_id: str
    scope: str
    limits: tuple[str, ...] = ()


@dataclass(frozen=True)
class RepositorySemanticMap:
    map_id: str
    target_ref: str
    entities: tuple[SemanticMapEntity, ...]
    relations: tuple[SemanticMapRelation, ...]
    claim_refs: tuple[str, ...] = ()
    uncertainty_refs: tuple[str, ...] = ()
    explicit_limits: tuple[str, ...] = ()
    artifact_id: str = "repository_semantic_map"
    schema_version: int = 1
    semantic_truth_established: bool = False


@dataclass(frozen=True)
class SemanticStateEntry:
    entry_id: str
    source_skill: str
    artifact_ref: str
    target_ref: str
    evidence_refs: tuple[str, ...] = ()
    claim_refs: tuple[str, ...] = ()
    uncertainty_refs: tuple[str, ...] = ()
    parent_entry_ids: tuple[str, ...] = ()
    semantic_profile_ref: str | None = None
    notes: tuple[str, ...] = ()
    created_at: str = ""


@dataclass(frozen=True)
class SkillContractManifest:
    skill_id: str
    domain: str
    responsibilities: tuple[str, ...]
    consumes: tuple[str, ...]
    produces: tuple[str, ...]
    semantic_concepts: tuple[str, ...]
    repository_mutation: bool
    schema_version: int = 1


@dataclass(frozen=True)
class DomainPackManifest:
    domain_id: str
    capability_ledger: str
    skill_manifests: tuple[str, ...]
    responsibility_vocabulary: tuple[str, ...]
    artifact_contracts: tuple[str, ...]
    qualification_policy: str
    schema_version: int = 1


def _walk(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {item.name: _walk(getattr(value, item.name)) for item in fields(value)}
    if isinstance(value, Mapping):
        return {str(key): _walk(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_walk(item) for item in value]
    return value


def to_dict(value: Any) -> dict[str, Any]:
    """Return a JSON/YAML-safe representation without adding semantic meaning."""
    resolved = _walk(value)
    if not isinstance(resolved, dict):
        raise TypeError("semantic architecture record must serialize to a mapping")
    return resolved
