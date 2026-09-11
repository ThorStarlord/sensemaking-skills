"""Deterministic Campaign provenance graph construction and integrity checks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from sensemaking_skills.campaign_semantics import target_snapshot_sha256
from sensemaking_skills.semantic_architecture import (
    IntegrityEffect,
    SemanticStateStore,
    audit_semantic_references,
)

from .target_snapshot import CampaignService
from .uncertainty_history import UncertaintyHistoryService


SEMANTIC_STATE_FILENAME = "semantic-state.jsonl"


@dataclass(frozen=True)
class GraphIntegrityDiagnostic:
    code: str
    detail: str


@dataclass(frozen=True)
class CampaignProvenanceGraph:
    campaign_id: str
    nodes: tuple[Mapping[str, str], ...]
    edges: tuple[Mapping[str, str], ...]
    diagnostics: tuple[GraphIntegrityDiagnostic, ...]
    semantic_truth_established: bool = False

    @property
    def valid(self) -> bool:
        return not self.diagnostics


def _target_ref(snapshot: Any) -> str | None:
    target = snapshot.state.target_snapshot
    if target is None:
        return None
    return f"target-snapshot-sha256:{target_snapshot_sha256(target)}"


class CampaignProvenanceGraphService:
    """Build graph bytes from recorded provenance and check mechanical integrity."""

    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace)
        self.lifecycle = CampaignService(workspace)

    def build(self) -> CampaignProvenanceGraph:
        snapshot = self.lifecycle.resume()
        diagnostics: list[GraphIntegrityDiagnostic] = []
        nodes: dict[str, dict[str, str]] = {}
        edges: list[dict[str, str]] = []
        edge_keys: set[tuple[str, str, str]] = set()

        def add_node(identifier: str, kind: str) -> None:
            existing = nodes.get(identifier)
            if existing is not None and existing["kind"] != kind:
                diagnostics.append(
                    GraphIntegrityDiagnostic(
                        "GRAPH_NODE_ID_COLLISION",
                        f"node id {identifier!r} is used as both {existing['kind']} and {kind}",
                    )
                )
                return
            nodes.setdefault(identifier, {"id": identifier, "kind": kind, "label": identifier})

        def add_edge(source: str, target: str, relation: str) -> None:
            key = (source, target, relation)
            if key in edge_keys:
                diagnostics.append(
                    GraphIntegrityDiagnostic(
                        "GRAPH_DUPLICATE_EDGE",
                        f"duplicate edge {source!r} -[{relation}]-> {target!r}",
                    )
                )
                return
            edge_keys.add(key)
            edges.append({"from": source, "to": target, "relation": relation})

        campaign_id = snapshot.state.campaign_id
        add_node(campaign_id, "campaign")
        previous: str | None = None
        for transition in snapshot.transitions:
            add_node(transition.id, "transition")
            add_edge(campaign_id, transition.id, "contains_transition")
            if previous is not None:
                add_edge(previous, transition.id, "followed_by")
            previous = transition.id
            for evidence in transition.evidence:
                add_node(evidence, "evidence")
                add_edge(transition.id, evidence, "references_evidence")

        semantic_store = SemanticStateStore(self.workspace / SEMANTIC_STATE_FILENAME)
        semantic_records, semantic_diagnostics = semantic_store.load_raw()
        for item in semantic_diagnostics:
            diagnostics.append(GraphIntegrityDiagnostic(item.code, item.detail))

        if not semantic_diagnostics:
            active_uncertainty_ids: tuple[str, ...] = ()
            if snapshot.state.active_uncertainty is not None:
                active_uncertainty_ids = (snapshot.state.active_uncertainty.id,)
            audit = audit_semantic_references(
                semantic_records,
                campaign_evidence_refs=snapshot.evidence_refs,
                active_uncertainty_ids=active_uncertainty_ids,
                campaign_target_ref=_target_ref(snapshot),
            )
            for item in audit.items:
                if item.integrity_effect is IntegrityEffect.FAIL:
                    diagnostics.append(
                        GraphIntegrityDiagnostic(
                            "GRAPH_SEMANTIC_REFERENCE_INTEGRITY_FAILED",
                            f"{item.entry_id}:{item.field}:{item.reference}: {item.resolution.value}",
                        )
                    )

        for record in semantic_records:
            entry = record.get("entry", {})
            raw_entry_id = entry.get("entry_id")
            if not isinstance(raw_entry_id, str) or not raw_entry_id:
                continue
            entry_id = raw_entry_id
            add_node(entry_id, "semantic_state_entry")
            add_edge(campaign_id, entry_id, "has_semantic_companion_entry")
            for parent in entry.get("parent_entry_ids", []):
                if isinstance(parent, str) and parent:
                    add_edge(parent, entry_id, "semantic_parent_of")
            artifact = entry.get("artifact_ref")
            if isinstance(artifact, str) and artifact:
                add_node(artifact, "artifact_ref")
                add_edge(entry_id, artifact, "references_artifact")

        uncertainty = UncertaintyHistoryService(self.workspace).load()
        if not uncertainty.valid:
            diagnostics.extend(
                GraphIntegrityDiagnostic(
                    "GRAPH_UNCERTAINTY_HISTORY_INVALID",
                    f"{item.code}: {item.detail}",
                )
                for item in uncertainty.diagnostics
            )

        known = set(nodes)
        for edge in edges:
            if edge["from"] not in known or edge["to"] not in known:
                diagnostics.append(
                    GraphIntegrityDiagnostic(
                        "GRAPH_EDGE_ENDPOINT_MISSING",
                        f"edge endpoint missing for {edge['from']!r} -[{edge['relation']}]-> {edge['to']!r}",
                    )
                )

        return CampaignProvenanceGraph(
            campaign_id=campaign_id,
            nodes=tuple(nodes.values()),
            edges=tuple(edges),
            diagnostics=tuple(diagnostics),
        )
