"""Deterministic execution projection over explicit multi-repository relations.

The projection converts only already-recorded ordering relations into prerequisite
edges and topological layers. It does not select work, infer architecture,
authorize parallelism, or create an execution plan.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .multi_target import MultiTargetService
from .multi_target_relations import (
    ORDERING_RELATION_TYPES,
    MultiTargetRelationService,
)


@dataclass(frozen=True)
class CrossRepositoryExecutionProjection:
    campaign_id: str
    valid: bool
    targets: tuple[Mapping[str, Any], ...]
    relations: tuple[Mapping[str, Any], ...]
    precedence_edges: tuple[Mapping[str, Any], ...]
    precedence_layers: tuple[tuple[str, ...], ...]
    descriptive_relations: tuple[Mapping[str, Any], ...]
    diagnostics: tuple[Mapping[str, Any], ...]
    semantic_truth_established: bool = False
    execution_plan_selected: bool = False
    parallel_execution_authorized: bool = False


def _topological_layers(
    aliases: list[str],
    precedence_pairs: set[tuple[str, str]],
) -> tuple[tuple[str, ...], ...]:
    predecessors: dict[str, set[str]] = {alias: set() for alias in aliases}
    successors: dict[str, set[str]] = {alias: set() for alias in aliases}
    for before, after in precedence_pairs:
        predecessors[after].add(before)
        successors[before].add(after)

    remaining = set(aliases)
    layers: list[tuple[str, ...]] = []
    while remaining:
        ready = tuple(
            sorted(
                alias
                for alias in remaining
                if not (predecessors[alias] & remaining)
            )
        )
        if not ready:
            raise ValueError("ordering relations contain a cycle")
        layers.append(ready)
        remaining.difference_update(ready)
    return tuple(layers)


class CrossRepositoryExecutionProjectionService:
    """Project explicit relation mechanics into read-only precedence layers."""

    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace).resolve()
        self.targets = MultiTargetService(self.workspace)
        self.relations = MultiTargetRelationService(self.workspace)

    def inspect(self) -> CrossRepositoryExecutionProjection:
        target_state = self.targets.inspect()
        relation_state = self.relations.inspect()
        diagnostics: list[Mapping[str, Any]] = []

        for item in target_state.diagnostics:
            diagnostics.append(
                {
                    "code": item.code,
                    "detail": item.detail,
                    "alias": item.alias,
                }
            )
        for item in relation_state.diagnostics:
            diagnostics.append(
                {
                    "code": item.code,
                    "detail": item.detail,
                    "relation_id": item.relation_id,
                    "line_number": item.line_number,
                }
            )

        targets = tuple(
            sorted(
                (
                    {
                        "alias": item["alias"],
                        "role": item["role"],
                        "authority": item["authority"],
                        "repository_id": item["snapshot"]["repository_id"],
                        "head_sha": item["snapshot"]["head_sha"],
                        "tree_sha": item["snapshot"]["tree_sha"],
                        "worktree_sha256": item["snapshot"]["worktree_sha256"],
                        "dirty": item["snapshot"]["dirty"],
                        "snapshot_sha256": item["snapshot_sha256"],
                    }
                    for item in target_state.targets
                ),
                key=lambda item: str(item["alias"]),
            )
        )
        relations = tuple(
            {
                "relation_id": item["relation_id"],
                "source_alias": item["source_alias"],
                "target_alias": item["target_alias"],
                "relation_type": item["relation_type"],
                "evidence_refs": list(item["evidence_refs"]),
            }
            for item in relation_state.relations
        )

        precedence_edges: list[Mapping[str, Any]] = []
        precedence_pairs: set[tuple[str, str]] = set()
        descriptive: list[Mapping[str, Any]] = []
        for item in relation_state.relations:
            relation_type = str(item["relation_type"])
            projected = {
                "relation_id": item["relation_id"],
                "source_alias": item["source_alias"],
                "target_alias": item["target_alias"],
                "relation_type": relation_type,
            }
            if relation_type in ORDERING_RELATION_TYPES:
                # "A depends_on B" and "A release_after B" both mean B must
                # precede A in the mechanical projection.
                before = str(item["target_alias"])
                after = str(item["source_alias"])
                edge = {
                    **projected,
                    "before": before,
                    "after": after,
                    "derivation": (
                        f"{relation_type}: target_alias precedes source_alias"
                    ),
                }
                precedence_edges.append(edge)
                precedence_pairs.add((before, after))
            else:
                descriptive.append(projected)

        valid = target_state.valid and relation_state.valid
        layers: tuple[tuple[str, ...], ...] = ()
        if valid:
            try:
                layers = _topological_layers(
                    [str(item["alias"]) for item in targets],
                    precedence_pairs,
                )
            except ValueError as exc:
                diagnostics.append(
                    {
                        "code": "CROSS_REPO_EXECUTION_PROJECTION_CYCLE",
                        "detail": str(exc),
                    }
                )
                valid = False

        return CrossRepositoryExecutionProjection(
            campaign_id=relation_state.campaign_id,
            valid=valid,
            targets=targets,
            relations=relations,
            precedence_edges=tuple(
                sorted(
                    precedence_edges,
                    key=lambda item: (
                        str(item["before"]),
                        str(item["after"]),
                        str(item["relation_id"]),
                    ),
                )
            ),
            precedence_layers=layers,
            descriptive_relations=tuple(
                sorted(
                    descriptive,
                    key=lambda item: str(item["relation_id"]),
                )
            ),
            diagnostics=tuple(diagnostics),
        )


def execution_projection_payload(
    value: CrossRepositoryExecutionProjection,
) -> dict[str, Any]:
    return {
        "campaign_id": value.campaign_id,
        "valid": value.valid,
        "targets": list(value.targets),
        "relations": list(value.relations),
        "precedence_edges": list(value.precedence_edges),
        "precedence_layers": [list(layer) for layer in value.precedence_layers],
        "descriptive_relations": list(value.descriptive_relations),
        "diagnostics": list(value.diagnostics),
        "semantic_truth_established": False,
        "semantic_recommendation_included": False,
        "execution_plan_selected": False,
        "parallel_execution_authorized": False,
        "explicit_limit": (
            "This view mechanically projects explicit ordering declarations. "
            "Layer membership does not mean work is warranted or safe to run in "
            "parallel, and the projection is not an execution plan."
        ),
    }


def render_execution_projection_mermaid(
    value: CrossRepositoryExecutionProjection,
) -> str:
    if not value.valid:
        raise ValueError("cannot render invalid execution projection")
    lines = ["flowchart LR"]
    node_ids = {
        str(target["alias"]): f"T{index}"
        for index, target in enumerate(value.targets)
    }
    for target in value.targets:
        alias = str(target["alias"])
        role = str(target["role"]).replace('"', "'")
        label = f"{alias}: {role}".replace('"', "'")
        lines.append(f'    {node_ids[alias]}["{label}"]')
    for edge in value.precedence_edges:
        relation = str(edge["relation_type"])
        before = node_ids[str(edge["before"])]
        after = node_ids[str(edge["after"])]
        lines.append(
            f'    {before} -->|"precedes ({relation})"| {after}'
        )
    for relation in value.descriptive_relations:
        relation_type = str(relation["relation_type"])
        source = node_ids[str(relation["source_alias"])]
        target = node_ids[str(relation["target_alias"])]
        lines.append(
            f'    {source} -. "{relation_type}" .-> {target}'
        )
    return "\n".join(lines)
