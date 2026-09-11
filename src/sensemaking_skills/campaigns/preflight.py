"""Mechanical Campaign preflight aggregation.

Preflight composes already-authoritative Campaign, target, admission, semantic-
reference, capability metadata, optional multi-target checks, and optional
caller-authored multi-target relation integrity. It reports representation and
integrity facts only. It never infers a responsibility type, repository
relationship, ranks a capability, or says whether the agent should proceed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from sensemaking_skills.campaign_semantics import target_snapshot_sha256
from sensemaking_skills.campaign_semantics.registry import AvailabilityStatus
from sensemaking_skills.semantic_architecture import (
    IntegrityEffect,
    SemanticStateStore,
    audit_semantic_references,
)

from .capabilities import CampaignCapabilityService
from .multi_target import MULTI_TARGET_FILENAME, MultiTargetService
from .multi_target_relations import MULTI_TARGET_RELATIONS_FILENAME, MultiTargetRelationService
from .target_snapshot import CampaignService


SEMANTIC_STATE_FILENAME = "semantic-state.jsonl"


@dataclass(frozen=True)
class CampaignPreflightCheck:
    """One mechanically decidable preflight observation."""

    id: str
    status: str
    detail: str
    diagnostics: tuple[str, ...] = ()
    data: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CampaignPreflightResult:
    """Aggregate preflight result without semantic proceed/stop authority."""

    campaign_id: str | None
    ready: bool
    checks: tuple[CampaignPreflightCheck, ...]
    semantic_recommendation_included: bool = False
    semantic_truth_established: bool = False


def _target_ref(snapshot: Any) -> str | None:
    target = snapshot.state.target_snapshot
    if target is None:
        return None
    return f"target-snapshot-sha256:{target_snapshot_sha256(target)}"


class CampaignPreflightService:
    """Compose existing mechanical checks into one read-only preflight."""

    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace)
        self.lifecycle = CampaignService(workspace)

    def inspect(self, responsibility_type: str | None = None) -> CampaignPreflightResult:
        """Return a deterministic readiness projection.

        ``responsibility_type`` is optional and must be supplied by the caller.
        Preflight deliberately refuses to infer it from responsibility prose.
        """

        checks: list[CampaignPreflightCheck] = []
        validation = self.lifecycle.validate()
        if not validation.valid:
            diagnostics = tuple(item.code for item in validation.diagnostics)
            checks.append(
                CampaignPreflightCheck(
                    id="campaign_integrity",
                    status="fail",
                    detail="durable Campaign reconstruction is invalid",
                    diagnostics=diagnostics,
                )
            )
            return CampaignPreflightResult(
                campaign_id=None,
                ready=False,
                checks=tuple(checks),
            )

        snapshot = self.lifecycle.resume()
        state = snapshot.state
        checks.append(
            CampaignPreflightCheck(
                id="campaign_integrity",
                status="pass",
                detail="durable Campaign reconstruction, transition history, evidence/admissions, and target binding are valid",
                data={
                    "transition_count": len(snapshot.transitions),
                    "evidence_ref_count": len(snapshot.evidence_refs),
                },
            )
        )

        checks.append(
            CampaignPreflightCheck(
                id="target_binding",
                status="pass" if state.target_snapshot is not None else "not_applicable",
                detail=(
                    "live target identity/state matches the durably recorded TargetSnapshot"
                    if state.target_snapshot is not None
                    else "Campaign is not primary-target-bound"
                ),
                data={"target_ref": _target_ref(snapshot)},
            )
        )

        multi_target_path = self.workspace / MULTI_TARGET_FILENAME
        if not multi_target_path.exists():
            checks.append(
                CampaignPreflightCheck(
                    id="multi_target_integrity",
                    status="not_applicable",
                    detail="no optional multi-repository target-set companion is present",
                )
            )
        else:
            multi_target = MultiTargetService(self.workspace).verify()
            diagnostics = tuple(
                f"{item.code}:{item.alias or '-'}" for item in multi_target.diagnostics
            )
            checks.append(
                CampaignPreflightCheck(
                    id="multi_target_integrity",
                    status="pass" if multi_target.valid else "fail",
                    detail=(
                        "all declared multi-repository target identities and live snapshots match"
                        if multi_target.valid
                        else "multi-repository target-set integrity or live snapshot verification failed"
                    ),
                    diagnostics=diagnostics,
                    data={
                        "target_count": len(multi_target.targets),
                        "target_set_sha256": multi_target.target_set_sha256,
                    },
                )
            )

        relation_path = self.workspace / MULTI_TARGET_RELATIONS_FILENAME
        if not relation_path.exists():
            checks.append(
                CampaignPreflightCheck(
                    id="multi_target_relation_integrity",
                    status="not_applicable",
                    detail="no optional cross-repository relation companion is present",
                )
            )
        else:
            relation_check = MultiTargetRelationService(self.workspace).inspect()
            diagnostics = tuple(
                f"{item.code}:{item.relation_id or '-'}:{item.line_number or '-'}"
                for item in relation_check.diagnostics
            )
            checks.append(
                CampaignPreflightCheck(
                    id="multi_target_relation_integrity",
                    status="pass" if relation_check.valid else "fail",
                    detail=(
                        "caller-authored cross-repository relation identities, aliases, evidence, hash chain, and ordering constraints are mechanically valid"
                        if relation_check.valid
                        else "cross-repository relation companion failed mechanical validation"
                    ),
                    diagnostics=diagnostics,
                    data={
                        "relation_count": len(relation_check.relations),
                        "ordering_cycle_count": len(relation_check.ordering_cycles),
                    },
                )
            )

        if state.active_responsibility is None:
            authority_status = "not_applicable"
            authority_detail = "Campaign has no active responsibility"
        else:
            authority_status = "pass"
            authority_detail = "active responsibility has mechanically consistent authority metadata"
        checks.append(
            CampaignPreflightCheck(
                id="authority_metadata",
                status=authority_status,
                detail=authority_detail,
                data={
                    "authority": state.authority.value if state.authority is not None else None,
                    "responsibility_id": (
                        state.active_responsibility.id
                        if state.active_responsibility is not None
                        else None
                    ),
                },
            )
        )

        checks.append(
            CampaignPreflightCheck(
                id="handoff_integrity",
                status="pass" if snapshot.handoff is not None else "not_applicable",
                detail=(
                    "handoff is bound to the exact current Campaign state"
                    if snapshot.handoff is not None
                    else "no durable handoff is present"
                ),
            )
        )

        semantic_path = self.workspace / SEMANTIC_STATE_FILENAME
        if not semantic_path.exists():
            checks.append(
                CampaignPreflightCheck(
                    id="semantic_reference_integrity",
                    status="not_applicable",
                    detail="no optional semantic companion is present",
                )
            )
        else:
            records, diagnostics = SemanticStateStore(semantic_path).load_raw()
            if diagnostics:
                checks.append(
                    CampaignPreflightCheck(
                        id="semantic_reference_integrity",
                        status="fail",
                        detail="semantic companion chain is invalid",
                        diagnostics=tuple(item.code for item in diagnostics),
                    )
                )
            else:
                active_uncertainty_ids: tuple[str, ...] = ()
                if state.active_uncertainty is not None:
                    active_uncertainty_ids = (state.active_uncertainty.id,)
                audit = audit_semantic_references(
                    records,
                    campaign_evidence_refs=snapshot.evidence_refs,
                    active_uncertainty_ids=active_uncertainty_ids,
                    campaign_target_ref=_target_ref(snapshot),
                )
                failing = tuple(
                    f"{item.entry_id}:{item.field}:{item.reference}"
                    for item in audit.items
                    if item.integrity_effect is IntegrityEffect.FAIL
                )
                checks.append(
                    CampaignPreflightCheck(
                        id="semantic_reference_integrity",
                        status="fail" if failing else "pass",
                        detail=(
                            "semantic companion contains dangling/ambiguous Campaign-local references"
                            if failing
                            else "semantic companion chain and addressable reference integrity are valid"
                        ),
                        diagnostics=failing,
                        data={
                            "entry_count": len(records),
                            "resolved_count": audit.resolved_count,
                            "not_addressable_count": audit.not_addressable_count,
                            "integrity_failure_count": audit.integrity_failure_count,
                        },
                    )
                )

        if responsibility_type is None:
            checks.append(
                CampaignPreflightCheck(
                    id="capability_catalog",
                    status="not_evaluated",
                    detail="responsibility type was not supplied; preflight will not infer one",
                )
            )
        elif state.active_responsibility is None:
            checks.append(
                CampaignPreflightCheck(
                    id="capability_catalog",
                    status="not_applicable",
                    detail="capability inspection requires an active responsibility",
                    data={"responsibility_type": responsibility_type},
                )
            )
        else:
            inspection = CampaignCapabilityService(self.workspace).inspect(responsibility_type)
            counts = {status.value: 0 for status in AvailabilityStatus}
            for candidate in inspection.candidates:
                counts[candidate.availability.value] += 1
            checks.append(
                CampaignPreflightCheck(
                    id="capability_catalog",
                    status="pass",
                    detail="declared compatible capabilities were enumerated without ranking or selection",
                    data={
                        "responsibility_type": responsibility_type,
                        "candidate_count": len(inspection.candidates),
                        "availability_counts": counts,
                        "candidate_ids": [
                            candidate.capability.id for candidate in inspection.candidates
                        ],
                    },
                )
            )

        ready = not any(check.status == "fail" for check in checks)
        return CampaignPreflightResult(
            campaign_id=state.campaign_id,
            ready=ready,
            checks=tuple(checks),
        )
