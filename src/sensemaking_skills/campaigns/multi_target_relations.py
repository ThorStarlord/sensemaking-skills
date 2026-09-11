"""Append-only explicit relationships between already-declared Campaign targets.

Relations are caller-authored metadata. This module validates identity, alias,
evidence, hash-chain, and mechanically contradictory ordering cycles; it never
infers repository relationships, architecture, work order, or authorization.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .companion_io import append_jsonl_fsync, mapping_sha256
from .multi_target import MultiTargetService, _safe_alias
from .target_snapshot import CampaignService


MULTI_TARGET_RELATIONS_FILENAME = "multi-target-relations.jsonl"
MULTI_TARGET_RELATIONS_VERSION = "1"
RELATION_TYPES = (
    "depends_on",
    "provides_interface_to",
    "consumes_interface_from",
    "must_change_with",
    "release_after",
)
ORDERING_RELATION_TYPES = frozenset({"depends_on", "release_after"})
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


@dataclass(frozen=True)
class MultiTargetRelationDiagnostic:
    code: str
    detail: str
    relation_id: str | None = None
    line_number: int | None = None


@dataclass(frozen=True)
class MultiTargetRelationCheck:
    campaign_id: str
    valid: bool
    relations: tuple[Mapping[str, Any], ...]
    diagnostics: tuple[MultiTargetRelationDiagnostic, ...]
    ordering_cycles: tuple[tuple[str, ...], ...] = ()
    semantic_truth_established: bool = False


def _record_core(record: Mapping[str, Any]) -> dict[str, Any]:
    return {key: record[key] for key in (
        "schema_version",
        "campaign_id",
        "relation_id",
        "source_alias",
        "target_alias",
        "relation_type",
        "evidence_refs",
        "previous_digest",
        "semantic_truth_established",
    )}


def _safe_relation_id(value: str) -> str:
    if not isinstance(value, str) or not _SAFE_ID.fullmatch(value):
        raise ValueError("relation_id must use only letters, numbers, '.', '_' or '-' and start alphanumerically")
    return value


def _ordering_cycles(relations: list[Mapping[str, Any]]) -> tuple[tuple[str, ...], ...]:
    graph: dict[str, set[str]] = {}
    for record in relations:
        if record.get("relation_type") not in ORDERING_RELATION_TYPES:
            continue
        source = str(record["source_alias"])
        target = str(record["target_alias"])
        graph.setdefault(source, set()).add(target)
        graph.setdefault(target, set())

    state: dict[str, int] = {}
    stack: list[str] = []
    cycles: set[tuple[str, ...]] = set()

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for nxt in sorted(graph.get(node, ())):
            if state.get(nxt, 0) == 0:
                visit(nxt)
            elif state.get(nxt) == 1:
                start = stack.index(nxt)
                cycle = stack[start:] + [nxt]
                core = cycle[:-1]
                if core:
                    rotations = [tuple(core[index:] + core[:index]) for index in range(len(core))]
                    canonical = min(rotations)
                    cycles.add(canonical + (canonical[0],))
        stack.pop()
        state[node] = 2

    for node in sorted(graph):
        if state.get(node, 0) == 0:
            visit(node)
    return tuple(sorted(cycles))


class MultiTargetRelationService:
    """Persist and validate caller-authored cross-repository relations."""

    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace).resolve()
        self.lifecycle = CampaignService(self.workspace)
        self.targets = MultiTargetService(self.workspace)
        self.path = self.workspace / MULTI_TARGET_RELATIONS_FILENAME

    def inspect(self) -> MultiTargetRelationCheck:
        snapshot = self.lifecycle.resume()
        campaign_id = snapshot.state.campaign_id
        target_state = self.targets.inspect()
        diagnostics: list[MultiTargetRelationDiagnostic] = []
        if not target_state.valid:
            diagnostics.extend(
                MultiTargetRelationDiagnostic("MULTI_TARGET_RELATION_TARGET_SET_INVALID", item.code)
                for item in target_state.diagnostics
            )
        aliases = {str(item["alias"]) for item in target_state.targets}
        evidence = set(snapshot.evidence_refs)
        if not self.path.exists():
            return MultiTargetRelationCheck(campaign_id, not diagnostics, (), tuple(diagnostics))

        relations: list[Mapping[str, Any]] = []
        seen_ids: set[str] = set()
        seen_edges: set[tuple[str, str, str]] = set()
        previous_digest: str | None = None
        required = {
            "schema_version",
            "campaign_id",
            "relation_id",
            "source_alias",
            "target_alias",
            "relation_type",
            "evidence_refs",
            "previous_digest",
            "semantic_truth_established",
            "record_digest",
        }
        for line_number, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as exc:
                diagnostics.append(MultiTargetRelationDiagnostic("MULTI_TARGET_RELATION_JSON_INVALID", str(exc), line_number=line_number))
                continue
            if not isinstance(raw, dict) or set(raw) != required:
                diagnostics.append(MultiTargetRelationDiagnostic("MULTI_TARGET_RELATION_FIELDS_INVALID", f"line {line_number} must contain exactly {sorted(required)}", line_number=line_number))
                continue
            relation_id = raw.get("relation_id") if isinstance(raw.get("relation_id"), str) else None
            try:
                if relation_id is None:
                    raise ValueError("relation_id must be text")
                _safe_relation_id(relation_id)
            except ValueError as exc:
                diagnostics.append(MultiTargetRelationDiagnostic("MULTI_TARGET_RELATION_ID_INVALID", str(exc), relation_id, line_number))
            if relation_id in seen_ids:
                diagnostics.append(MultiTargetRelationDiagnostic("MULTI_TARGET_RELATION_ID_DUPLICATE", "relation_id must be unique", relation_id, line_number))
            if relation_id is not None:
                seen_ids.add(relation_id)
            if raw.get("schema_version") != MULTI_TARGET_RELATIONS_VERSION:
                diagnostics.append(MultiTargetRelationDiagnostic("MULTI_TARGET_RELATION_VERSION_UNSUPPORTED", "unsupported schema_version", relation_id, line_number))
            if raw.get("campaign_id") != campaign_id:
                diagnostics.append(MultiTargetRelationDiagnostic("MULTI_TARGET_RELATION_CAMPAIGN_ID_MISMATCH", "campaign_id does not match Campaign state", relation_id, line_number))
            try:
                source = _safe_alias(raw.get("source_alias"))
                target = _safe_alias(raw.get("target_alias"))
            except ValueError as exc:
                diagnostics.append(MultiTargetRelationDiagnostic("MULTI_TARGET_RELATION_ALIAS_INVALID", str(exc), relation_id, line_number))
                source = target = ""
            if source and source not in aliases:
                diagnostics.append(MultiTargetRelationDiagnostic("MULTI_TARGET_RELATION_SOURCE_UNKNOWN", f"unknown source alias {source!r}", relation_id, line_number))
            if target and target not in aliases:
                diagnostics.append(MultiTargetRelationDiagnostic("MULTI_TARGET_RELATION_TARGET_UNKNOWN", f"unknown target alias {target!r}", relation_id, line_number))
            if source and source == target:
                diagnostics.append(MultiTargetRelationDiagnostic("MULTI_TARGET_RELATION_SELF_EDGE", "source_alias and target_alias must differ", relation_id, line_number))
            relation_type = raw.get("relation_type")
            if relation_type not in RELATION_TYPES:
                diagnostics.append(MultiTargetRelationDiagnostic("MULTI_TARGET_RELATION_TYPE_INVALID", f"relation_type must be one of {RELATION_TYPES}", relation_id, line_number))
            edge = (source, target, str(relation_type))
            if source and target and edge in seen_edges:
                diagnostics.append(MultiTargetRelationDiagnostic("MULTI_TARGET_RELATION_EDGE_DUPLICATE", "duplicate source/target/type declaration", relation_id, line_number))
            seen_edges.add(edge)
            refs = raw.get("evidence_refs")
            if not isinstance(refs, list) or any(not isinstance(item, str) or not item for item in refs):
                diagnostics.append(MultiTargetRelationDiagnostic("MULTI_TARGET_RELATION_EVIDENCE_INVALID", "evidence_refs must be a list of non-empty strings", relation_id, line_number))
            else:
                if len(refs) != len(set(refs)):
                    diagnostics.append(MultiTargetRelationDiagnostic("MULTI_TARGET_RELATION_EVIDENCE_DUPLICATE", "evidence_refs must not contain duplicates", relation_id, line_number))
                missing = sorted(set(refs) - evidence)
                if missing:
                    diagnostics.append(MultiTargetRelationDiagnostic("MULTI_TARGET_RELATION_EVIDENCE_UNKNOWN", "evidence refs are outside Campaign authority: " + ", ".join(missing), relation_id, line_number))
            if raw.get("previous_digest") != previous_digest:
                diagnostics.append(MultiTargetRelationDiagnostic("MULTI_TARGET_RELATION_CHAIN_MISMATCH", "previous_digest does not match prior record", relation_id, line_number))
            if raw.get("semantic_truth_established") is not False:
                diagnostics.append(MultiTargetRelationDiagnostic("MULTI_TARGET_RELATION_SEMANTIC_AUTHORITY_INVALID", "semantic_truth_established must remain false", relation_id, line_number))
            try:
                expected_digest = mapping_sha256(_record_core(raw))
            except KeyError:
                expected_digest = ""
            if raw.get("record_digest") != expected_digest:
                diagnostics.append(MultiTargetRelationDiagnostic("MULTI_TARGET_RELATION_DIGEST_MISMATCH", "record_digest does not match record content", relation_id, line_number))
            if isinstance(raw.get("record_digest"), str):
                previous_digest = str(raw["record_digest"])
            relations.append(raw)

        cycles = _ordering_cycles(relations)
        for cycle in cycles:
            diagnostics.append(MultiTargetRelationDiagnostic("MULTI_TARGET_ORDERING_CYCLE", "ordering relations contain a cycle: " + " -> ".join(cycle)))
        return MultiTargetRelationCheck(campaign_id, not diagnostics, tuple(relations), tuple(diagnostics), cycles)

    def append(
        self,
        *,
        relation_id: str,
        source_alias: str,
        target_alias: str,
        relation_type: str,
        evidence_refs: tuple[str, ...] = (),
    ) -> str:
        current = self.inspect()
        if not current.valid:
            raise ValueError("multi-target relation companion is invalid")
        relation_id = _safe_relation_id(relation_id)
        source_alias = _safe_alias(source_alias)
        target_alias = _safe_alias(target_alias)
        if source_alias == target_alias:
            raise ValueError("source_alias and target_alias must differ")
        aliases = {str(item["alias"]) for item in self.targets.inspect().targets}
        if source_alias not in aliases or target_alias not in aliases:
            raise ValueError("source_alias and target_alias must already exist in the multi-target set")
        if relation_type not in RELATION_TYPES:
            raise ValueError(f"relation_type must be one of {RELATION_TYPES}")
        if relation_id in {str(item["relation_id"]) for item in current.relations}:
            raise ValueError(f"relation_id already exists: {relation_id}")
        edge = (source_alias, target_alias, relation_type)
        if edge in {(str(item["source_alias"]), str(item["target_alias"]), str(item["relation_type"])) for item in current.relations}:
            raise ValueError("the same source/target/type relation is already recorded")
        if len(evidence_refs) != len(set(evidence_refs)):
            raise ValueError("evidence_refs must not contain duplicates")
        missing = sorted(set(evidence_refs) - set(self.lifecycle.resume().evidence_refs))
        if missing:
            raise ValueError("evidence refs are outside Campaign authority: " + ", ".join(missing))
        previous = str(current.relations[-1]["record_digest"]) if current.relations else None
        core: dict[str, Any] = {
            "schema_version": MULTI_TARGET_RELATIONS_VERSION,
            "campaign_id": current.campaign_id,
            "relation_id": relation_id,
            "source_alias": source_alias,
            "target_alias": target_alias,
            "relation_type": relation_type,
            "evidence_refs": list(evidence_refs),
            "previous_digest": previous,
            "semantic_truth_established": False,
        }
        record = {**core, "record_digest": mapping_sha256(core)}
        prospective = [*current.relations, record]
        cycles = _ordering_cycles(prospective)
        if cycles:
            raise ValueError("refuse relation because ordering relations would contain a cycle: " + " -> ".join(cycles[0]))
        append_jsonl_fsync(self.path, record)
        return str(record["record_digest"])

    def graph(self) -> dict[str, Any]:
        checked = self.inspect()
        nodes = sorted({str(item["alias"]) for item in self.targets.inspect().targets})
        edges = [
            {
                "relation_id": item["relation_id"],
                "source": item["source_alias"],
                "target": item["target_alias"],
                "type": item["relation_type"],
            }
            for item in checked.relations
        ]
        return {
            "campaign_id": checked.campaign_id,
            "valid": checked.valid,
            "nodes": nodes,
            "edges": edges,
            "ordering_cycles": [list(cycle) for cycle in checked.ordering_cycles],
            "diagnostics": [
                {"code": item.code, "detail": item.detail, "relation_id": item.relation_id, "line_number": item.line_number}
                for item in checked.diagnostics
            ],
            "semantic_truth_established": False,
            "semantic_recommendation_included": False,
        }
