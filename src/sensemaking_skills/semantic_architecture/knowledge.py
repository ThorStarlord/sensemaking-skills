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
# Version of the reviewed authored-document format. Kept separate from
# SCHEMA_VERSION, which versions the SQLite store: bumping the store would force
# a rebuild of every existing index.
AUTHORED_SCHEMA_VERSIONS = frozenset({1, 2})
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
# Version-2 additions (ADR 0033). Only reviewed authored documents declaring
# schema_version 2 may use them; generated and version-1 content never does.
V2_CLAIM_KINDS = frozenset({
    "layer", "bounded_context", "lifecycle_state", "architecture_rule",
})
V2_PREDICATES = frozenset({
    "belongs_to", "relates_to", "transitions_to", "flows_to", "exposes",
    "applies_to", "synonym_of", "distinct_from",
})
RULE_TYPES = frozenset({"dependency_direction", "placement", "naming", "forbidden_term", "convention"})
CARDINALITIES = frozenset({"1:1", "1:N", "N:M"})
RULE_SEVERITIES = frozenset({"warning", "error"})
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


def validate_snapshot(snapshot: KnowledgeSnapshot, *, existence_only_ids: frozenset[str] = frozenset()) -> None:
    """Check representational integrity, not semantic truth.

    ``existence_only_ids`` names endpoints whose authored record lives in another
    file. Their identity and kind are checked, but their attributes and rule scope
    are not: the owning file is validated where it is read.
    """
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
        if item.kind not in CLAIM_KINDS | V2_CLAIM_KINDS or item.epistemic_status not in EPISTEMIC_STATES:
            raise ValueError(f"invalid claim kind/status: {item.id}")
        if item.authority_kind not in AUTHORITY_KINDS:
            raise ValueError(f"invalid authority kind: {item.id}")
        if not item.statement.strip() or not item.source_ref.strip() or not item.authority_ref.strip():
            raise ValueError(f"claim requires statement/source/authority: {item.id}")
        if not item.evidence_refs or any(not str(v).strip() for v in item.evidence_refs):
            raise ValueError(f"claim requires evidence references: {item.id}")
        _json_object(item.attributes, item.id)
        if item.id not in existence_only_ids and (item.kind == "architecture_rule" or (item.kind == "component" and "owned_paths" in item.attributes)):
            validate_v2_attributes(item.kind, None, item.attributes, item.id)
    kinds = {item.id: item.kind for item in snapshot.claims}
    for item in snapshot.claims:
        if item.kind == "architecture_rule":
            _check_rule_references(item, seen_claims)
    seen_edges: set[str] = set()
    for relation in snapshot.relations:
        if not _required_id(relation.id) or relation.id in seen_edges:
            raise ValueError(f"invalid or duplicate relation id: {relation.id}")
        seen_edges.add(relation.id)
        if relation.predicate not in PREDICATES | V2_PREDICATES or relation.epistemic_status not in EPISTEMIC_STATES:
            raise ValueError(f"invalid relationship kind/status: {relation.id}")
        if relation.derivation not in DERIVATIONS:
            raise ValueError(f"invalid relationship derivation: {relation.id}")
        if relation.subject not in seen_claims or relation.object not in seen_claims:
            raise ValueError(f"relationship endpoint not in snapshot: {relation.id}")
        if not relation.source_ref.strip() or not relation.evidence_refs:
            raise ValueError(f"relationship missing evidence: {relation.id}")
        _json_object(relation.attributes, relation.id)
        if relation.predicate in V2_PREDICATES:
            validate_v2_attributes(None, relation.predicate, relation.attributes, relation.id)
            a, b = kinds[relation.subject], kinds[relation.object]
            if relation.predicate == "applies_to" and (a != "architecture_rule" or b not in {"component", "layer", "bounded_context"}):
                raise ValueError(f"applies_to needs rule -> component/layer/context: {relation.id}")
            if relation.predicate == "belongs_to" and b not in {"layer", "bounded_context"}:
                raise ValueError(f"belongs_to needs layer/context target: {relation.id}")
            if relation.predicate == "transitions_to" and (a != "lifecycle_state" or b != "lifecycle_state"):
                raise ValueError(f"transitions_to needs lifecycle states: {relation.id}")
            if relation.predicate == "exposes" and (a != "component" or b != "contract"):
                raise ValueError(f"exposes needs component -> contract: {relation.id}")
            if relation.predicate == "flows_to":
                if a != "component" or b != "component":
                    raise ValueError(f"flows_to needs component endpoints: {relation.id}")
                carries = relation.attributes.get("carries")
                if not isinstance(carries, str) or kinds.get(carries) != "contract":
                    raise ValueError(f"flows_to must reference a contract in carries: {relation.id}")
            if relation.predicate in {"synonym_of", "distinct_from"} and (a != "domain_concept" or b != "domain_concept"):
                raise ValueError(f"{relation.predicate} needs two domain concepts: {relation.id}")
    scoped_rules = {rel.subject for rel in snapshot.relations if rel.predicate == "applies_to"}
    for claim in snapshot.claims:
        if claim.kind == "architecture_rule" and claim.id not in existence_only_ids and not claim.attributes.get("applies_to") and claim.id not in scoped_rules:
            raise ValueError(f"architecture_rule has no path or graph scope: {claim.id}")


def is_path_scope(reference: str) -> bool:
    """A path scope contains a separator or glob; identifiers never do."""
    return "/" in reference or "*" in reference or "?" in reference or (
        ":" not in reference and "." in reference
    )


def _valid_repo_path(value: str, *, glob: bool) -> bool:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        return False
    if value.startswith(("/", "~")) or any(x in {"", ".", ".."} for x in value.rstrip("/").split("/")):
        return False
    return glob or not any(c in value for c in "*?[]")


def validate_v2_attributes(kind: str | None, predicate: str | None, attrs: Mapping[str, Any], reference: str) -> None:
    """Check the typed attributes version-2 constructs require (ADR 0033)."""
    if kind == "component" and "owned_paths" in attrs:
        paths = attrs["owned_paths"]
        if not isinstance(paths, list) or not paths or any(not _valid_repo_path(x, glob=False) for x in paths) or len(set(paths)) != len(paths):
            raise ValueError(f"component owned_paths must be distinct repository-relative paths: {reference}")
        directories = [x for x in paths if x.endswith("/")]
        if directories:
            raise ValueError(f"component owned_paths lists files, not directories {directories}; list the tracked files: {reference}")
    if kind == "architecture_rule":
        if attrs.get("rule_type") not in RULE_TYPES:
            raise ValueError(f"architecture_rule needs rule_type in {sorted(RULE_TYPES)}: {reference}")
        if attrs.get("severity") not in RULE_SEVERITIES:
            raise ValueError(f"architecture_rule needs severity warning|error: {reference}")
        scope = attrs.get("applies_to", [])
        if not isinstance(scope, list) or any(not isinstance(v, str) or not v.strip() for v in scope):
            raise ValueError(f"architecture_rule applies_to must list repository paths or be empty for graph-only scope: {reference}")
        for item in scope:
            if not is_path_scope(item) or not _valid_repo_path(item, glob=True):
                raise ValueError(f"applies_to path must be repository-relative: {reference}")
            if item.endswith("/"):
                raise ValueError(f"applies_to scope {item!r} matches no file; scope a directory as {item}**: {reference}")
        rule_type = attrs["rule_type"]
        for key in ("allowed_targets", "forbidden_targets"):
            if key in attrs and attrs[key] is not None and (
                not isinstance(attrs[key], list) or any(not isinstance(v, str) or not v.strip() for v in attrs[key])
            ):
                raise ValueError(f"{key} must be a list of claim IDs: {reference}")
        if rule_type == "dependency_direction" and not (attrs.get("allowed_targets") or attrs.get("forbidden_targets")):
            raise ValueError(f"dependency_direction needs allowed_targets or forbidden_targets: {reference}")
        allowed = set(attrs.get("allowed_targets") or [])
        forbidden = set(attrs.get("forbidden_targets") or [])
        if allowed & forbidden:
            raise ValueError(f"dependency_direction has contradictory allowed/forbidden targets: {reference}")
        if rule_type in {"placement", "naming"} and not isinstance(attrs.get("pattern"), str):
            raise ValueError(f"{rule_type} rule needs a pattern: {reference}")
        if rule_type == "forbidden_term" and not (isinstance(attrs.get("terms"), list) and attrs["terms"]):
            raise ValueError(f"forbidden_term rule needs terms: {reference}")
    if predicate == "relates_to" and attrs.get("cardinality") not in CARDINALITIES:
        raise ValueError(f"relates_to needs cardinality in {sorted(CARDINALITIES)}: {reference}")


def _check_rule_references(item: "KnowledgeClaim", claim_ids: set[str]) -> None:
    """Every non-path scope or target of a rule must name a claim in the snapshot."""
    refs = list(item.attributes.get("applies_to", []))
    refs += list(item.attributes.get("allowed_targets", []) or [])
    refs += list(item.attributes.get("forbidden_targets", []) or [])
    for ref in refs:
        if not is_path_scope(ref) and ref not in claim_ids:
            raise ValueError(f"architecture_rule references unknown claim {ref!r}: {item.id}")


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


def read_authored_claim(data: dict[str, Any], *, source_ref: str, schema_version: int = 1) -> KnowledgeClaim:
    """Parse a reviewed authored record; its declared authority is NOT validated."""
    if not isinstance(data, dict):
        raise ValueError("authored claim must be an object")
    allowed = {"id", "kind", "statement", "epistemic_status", "authority_kind", "authority_ref", "evidence_refs", "attributes"}
    if set(data) - allowed:
        raise ValueError(f"unknown authored-claim fields: {sorted(set(data) - allowed)}")
    missing = {"id", "kind", "statement", "authority_kind", "authority_ref"} - set(data)
    if missing:
        raise ValueError(f"authored claim missing required fields: {sorted(missing)}")
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
    if data["kind"] in V2_CLAIM_KINDS or (data["kind"] == "component" and "owned_paths" in attrs):
        if schema_version < 2:
            raise ValueError(f"kind {data['kind']} requires schema_version 2: {data['id']}")
        validate_v2_attributes(data["kind"], None, attrs, data["id"])
    return KnowledgeClaim(
        id=data["id"], kind=data["kind"], statement=data["statement"],
        epistemic_status=status,
        authority_kind=authority, authority_ref=data["authority_ref"],
        source_ref=source_ref, evidence_refs=tuple(refs),
        attributes={**attrs, "authority_verified": False},
    )


def read_authored_relation(data: dict[str, Any], *, source_ref: str, schema_version: int = 1) -> KnowledgeRelation:
    if not isinstance(data, dict):
        raise ValueError("authored relation must be an object")
    allowed = {"id", "subject", "predicate", "object", "epistemic_status", "derivation", "evidence_refs", "attributes"}
    if set(data) - allowed:
        raise ValueError(f"unknown authored-relation fields: {sorted(set(data) - allowed)}")
    missing = {"id", "subject", "predicate", "object"} - set(data)
    if missing:
        raise ValueError(f"authored relation missing required fields: {sorted(missing)}")
    refs = data.get("evidence_refs")
    if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
        raise ValueError("authored relation evidence_refs must be a list of strings")
    derivation = data.get("derivation", "authored")
    attrs = data.get("attributes", {})
    if derivation not in {"authored", "declared"}:
        raise ValueError("authored relations cannot claim mechanical derivation")
    if not isinstance(attrs, dict) or {"authority_verified", "semantic_truth_established", "action_authorized"} & attrs.keys():
        raise ValueError("authored relations cannot assert verified authority or permission")
    if data["predicate"] in V2_PREDICATES:
        if schema_version < 2:
            raise ValueError(f"predicate {data['predicate']} requires schema_version 2: {data['id']}")
        validate_v2_attributes(None, data["predicate"], attrs, data["id"])
    return KnowledgeRelation(
        id=data["id"], subject=data["subject"], predicate=data["predicate"],
        object=data["object"], epistemic_status=data.get("epistemic_status", "declared"),
        derivation=derivation, source_ref=source_ref,
        evidence_refs=tuple(refs), attributes={**attrs, "authority_verified": False},
    )
