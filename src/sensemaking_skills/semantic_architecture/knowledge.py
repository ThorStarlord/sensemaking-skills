"""Versioned epistemic records for persistent semantic stewardship.

This module is a *knowledge representation*, not an authority oracle or planner.
Current source evidence, owner decisions, inferred hypotheses and archived
history remain distinct. No state is written by importing this module.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from typing import Any, Mapping

SCHEMA_VERSION = 1
SHA_PATTERN = re.compile(r"[0-9a-f]{40}\Z")
ID_PATTERN = re.compile(r"[a-zA-Z][a-zA-Z0-9_.:\-]{2,127}\Z")
CLAIM_KINDS = frozenset({
    "goal", "non_goal", "domain_concept", "capability", "constraint",
    "invariant", "contract", "component", "directory", "source", "verification",
    "decision", "alternative", "incident", "lesson", "hypothesis",
    "opportunity", "observation",
})
EPISTEMIC_STATES = frozenset({
    "declared", "observed", "hypothetical", "contested", "superseded",
    "invalidated",
})
AUTHORITY_KINDS = frozenset({
    "owner", "delegated", "policy", "code", "test",
    "hypothesis", "mechanical", "document",
})
DERIVATIONS = frozenset({"authored", "declared", "mechanical", "lexical"})
PREDICATES = frozenset({
    "serves_goal", "requires_capability", "constrained_by", "depends_on",
    "implemented_by", "tested_by", "decided_by", "supersedes",
    "contradicts", "derived_from", "affected_by_change", "learned_from",
    "candidate_opportunity_for", "defines", "references", "contained_in",
})


@dataclass(frozen=True)
class KnowledgeClaim:
    id: str
    kind: str
    statement: str
    epistemic_status: str
    authority_kind: str
    authority_ref: str
    source_ref: str
    evidence_refs: tuple[str, ...]
    attributes: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class KnowledgeRelation:
    id: str
    subject: str
    predicate: str
    object: str
    epistemic_status: str
    derivation: str
    source_ref: str
    evidence_refs: tuple[str, ...]
    attributes: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class KnowledgeSnapshot:
    repository: str
    target_ref: str
    claims: tuple[KnowledgeClaim, ...]
    relations: tuple[KnowledgeRelation, ...]
    source_scope: tuple[str, ...]
    limits: tuple[str, ...]
    schema_version: int = SCHEMA_VERSION
    semantic_truth_established: bool = False
    action_authorized: bool = False


def stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("\0".join(parts).encode("utf-8")).hexdigest()[:24]
    return f"{prefix}:{digest}"


def _required_id(value: str) -> bool:
    return isinstance(value, str) and bool(ID_PATTERN.fullmatch(value))


def validate_snapshot(snapshot: KnowledgeSnapshot) -> None:
    """Check representational integrity, not semantic truth."""
    if snapshot.schema_version != SCHEMA_VERSION:
        raise ValueError("unsupported semantic knowledge schema version")
    if not snapshot.repository or not isinstance(snapshot.repository, str):
        raise ValueError("repository identity is required")
    if not SHA_PATTERN.fullmatch(snapshot.target_ref):
        raise ValueError("target_ref must be an exact 40-character Git SHA")
    if snapshot.semantic_truth_established or snapshot.action_authorized:
        raise ValueError("a semantic snapshot cannot establish truth or authorization")
    seen_claims: set[str] = set()
    for item in snapshot.claims:
        if not _required_id(item.id) or item.id in seen_claims:
            raise ValueError(f"invalid or duplicate claim id: {item.id}")
        seen_claims.add(item.id)
        if item.kind not in CLAIM_KINDS or item.epistemic_status not in EPISTEMIC_STATES:
            raise ValueError(f"invalid claim kind/status: {item.id}")
        if item.authority_kind not in AUTHORITY_KINDS:
            raise ValueError(f"invalid authority kind: {item.id}")
        if not item.statement.strip() or not item.source_ref.strip() or not item.authority_ref.strip():
            raise ValueError(f"claim requires statement/source/authority: {item.id}")
        if not item.evidence_refs or any(not str(v).strip() for v in item.evidence_refs):
            raise ValueError(f"claim requires evidence references: {item.id}")
        _json_object(item.attributes, item.id)
    seen_edges: set[str] = set()
    for relation in snapshot.relations:
        if not _required_id(relation.id) or relation.id in seen_edges:
            raise ValueError(f"invalid or duplicate relation id: {relation.id}")
        seen_edges.add(relation.id)
        if relation.predicate not in PREDICATES or relation.epistemic_status not in EPISTEMIC_STATES:
            raise ValueError(f"invalid relationship kind/status: {relation.id}")
        if relation.derivation not in DERIVATIONS:
            raise ValueError(f"invalid relationship derivation: {relation.id}")
        if relation.subject not in seen_claims or relation.object not in seen_claims:
            raise ValueError(f"relationship endpoint not in snapshot: {relation.id}")
        if not relation.source_ref.strip() or not relation.evidence_refs:
            raise ValueError(f"relationship missing evidence: {relation.id}")
        _json_object(relation.attributes, relation.id)


def _json_object(value: Mapping[str, Any], reference: str) -> None:
    if not isinstance(value, Mapping) or any(not isinstance(k, str) for k in value):
        raise ValueError(f"invalid attributes mapping: {reference}")
    try:
        encoded = json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"attributes are not finite JSON: {reference}") from exc
    if len(encoded) > 20000:
        raise ValueError(f"oversized metadata: {reference}")


def record_dict(record: KnowledgeClaim | KnowledgeRelation | KnowledgeSnapshot) -> dict[str, Any]:
    """Deterministic JSON-safe record for SQLite and CLI, without interpretation."""
    return asdict(record)


def fingerprint(snapshot: KnowledgeSnapshot) -> str:
    validate_snapshot(snapshot)
    data = json.dumps(record_dict(snapshot), sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def read_authored_claim(data: dict[str, Any], *, source_ref: str) -> KnowledgeClaim:
    """Parse a reviewed authored record; its declared authority is NOT validated."""
    if not isinstance(data, dict):
        raise ValueError("authored claim must be an object")
    allowed = {"id", "kind", "statement", "epistemic_status", "authority_kind", "authority_ref", "evidence_refs", "attributes"}
    if set(data) - allowed:
        raise ValueError(f"unknown authored-claim fields: {sorted(set(data) - allowed)}")
    refs = data.get("evidence_refs")
    if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
        raise ValueError("authored claim evidence_refs must be a list of strings")
    status = data.get("epistemic_status", "declared")
    authority = data["authority_kind"]
    attrs = data.get("attributes", {})
    if not isinstance(attrs, dict) or {"authority_verified", "semantic_truth_established", "action_authorized"} & attrs.keys():
        raise ValueError("authored data may not assert verified authority or action permission")
    if status == "observed" and authority not in {"code", "test", "document", "mechanical"}:
        raise ValueError("authored normative claim cannot masquerade as observed evidence")
    return KnowledgeClaim(
        id=data["id"], kind=data["kind"], statement=data["statement"],
        epistemic_status=status,
        authority_kind=authority, authority_ref=data["authority_ref"],
        source_ref=source_ref, evidence_refs=tuple(refs),
        attributes={**attrs, "authority_verified": False},
    )


def read_authored_relation(data: dict[str, Any], *, source_ref: str) -> KnowledgeRelation:
    if not isinstance(data, dict):
        raise ValueError("authored relation must be an object")
    allowed = {"id", "subject", "predicate", "object", "epistemic_status", "derivation", "evidence_refs", "attributes"}
    if set(data) - allowed:
        raise ValueError(f"unknown authored-relation fields: {sorted(set(data) - allowed)}")
    refs = data.get("evidence_refs")
    if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
        raise ValueError("authored relation evidence_refs must be a list of strings")
    derivation = data.get("derivation", "authored")
    attrs = data.get("attributes", {})
    if derivation not in {"authored", "declared"}:
        raise ValueError("authored relations cannot claim mechanical derivation")
    if not isinstance(attrs, dict) or {"authority_verified", "semantic_truth_established", "action_authorized"} & attrs.keys():
        raise ValueError("authored relations cannot assert verified authority or permission")
    return KnowledgeRelation(
        id=data["id"], subject=data["subject"], predicate=data["predicate"],
        object=data["object"], epistemic_status=data.get("epistemic_status", "declared"),
        derivation=derivation, source_ref=source_ref,
        evidence_refs=tuple(refs), attributes={**attrs, "authority_verified": False},
    )
