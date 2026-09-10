"""Bounded Repository Semantic Map construction.

The map shares mechanically observed repository structure plus references to
agent-authored semantic state. It is explicitly incomplete and must not be used
as a complete source of truth for a repository.
"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from typing import Iterable

from .models import (
    RepositorySemanticMap,
    SemanticMapEntity,
    SemanticMapRelation,
    SemanticObservation,
)


def _id(prefix: str, value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
    return f"{prefix}-{digest}"


def build_repository_semantic_map(
    *,
    map_id: str,
    target_ref: str,
    observations: Iterable[SemanticObservation],
    claim_refs: Iterable[str] = (),
    uncertainty_refs: Iterable[str] = (),
    explicit_limits: Iterable[str] = (),
) -> RepositorySemanticMap:
    """Build a deterministic bounded map from already-collected observations."""
    resolved = tuple(observations)
    mismatched = sorted({item.target_ref for item in resolved if item.target_ref != target_ref})
    if mismatched:
        raise ValueError(
            "all observations must use the map target_ref; mismatched refs: "
            + ", ".join(mismatched)
        )

    evidence_by_locator: dict[str, set[str]] = defaultdict(set)
    relations: list[SemanticMapRelation] = []
    for observation in resolved:
        evidence_by_locator[observation.subject].update(observation.evidence_refs)
        evidence_by_locator[observation.object].update(observation.evidence_refs)
        relations.append(
            SemanticMapRelation(
                id=_id("REL", observation.id),
                subject=observation.subject,
                predicate=observation.predicate,
                object=observation.object,
                epistemic_status="DERIVED",
                evidence_refs=observation.evidence_refs,
                source_observation_id=observation.id,
                scope=observation.scope,
                limits=(
                    "mechanical relation only; semantic/architectural significance not established",
                ),
            )
        )

    entities = tuple(
        SemanticMapEntity(
            id=_id("ENT", locator),
            kind="repository_locator",
            locator=locator,
            evidence_refs=tuple(sorted(evidence_by_locator[locator])),
        )
        for locator in sorted(evidence_by_locator)
    )

    limits = tuple(dict.fromkeys(explicit_limits))
    default_limit = (
        "bounded map of supplied observations; absence from this map does not establish repository absence"
    )
    if default_limit not in limits:
        limits = (*limits, default_limit)

    return RepositorySemanticMap(
        map_id=map_id,
        target_ref=target_ref,
        entities=entities,
        relations=tuple(sorted(relations, key=lambda item: item.id)),
        claim_refs=tuple(dict.fromkeys(claim_refs)),
        uncertainty_refs=tuple(dict.fromkeys(uncertainty_refs)),
        explicit_limits=limits,
    )
