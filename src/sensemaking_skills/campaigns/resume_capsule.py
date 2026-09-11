"""Deterministic Resume Capsule projections over durable Campaign state.

Version 1 remains the backward-compatible default surface. Version 2 adds
explicit progressive-disclosure profiles and deterministic list bounds without
semantic summarization or next-action recommendation.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from sensemaking_skills.campaign_semantics import canonicalize, target_snapshot_sha256

from .preflight import CampaignPreflightService
from .uncertainty_history import UncertaintyHistoryService


RESUME_PROFILES = ("minimal", "working", "audit")


def _enum(value: Any) -> Any:
    return value.value if value is not None and hasattr(value, "value") else value


def _target_ref(state: Any) -> str | None:
    target = state.target_snapshot
    if target is None:
        return None
    return f"target-snapshot-sha256:{target_snapshot_sha256(target)}"


def _compact_responsibility(value: Any) -> dict[str, Any] | None:
    if value is None:
        return None
    return {
        "id": value.id,
        "statement": value.statement,
        "authority": _enum(value.authority),
        "status": value.status,
        "decision_blocked": value.decision_blocked,
    }


def _compact_uncertainty(value: Any) -> dict[str, Any] | None:
    if value is None:
        return None
    return {
        "id": value.id,
        "question": value.question,
        "status": value.status,
        "materiality": value.materiality,
    }


def _compact_transition(value: Any) -> dict[str, Any]:
    return {
        "id": value.id,
        "from_state": value.from_state,
        "to_state": value.to_state,
        "decision": value.decision,
        "evidence_refs": list(value.evidence),
        "next_responsibility": value.next_responsibility,
        "terminal_state": _enum(value.terminal_state),
    }


def _preflight_projection(workspace: Path) -> dict[str, Any]:
    result = CampaignPreflightService(workspace).inspect()
    return {
        "ready": result.ready,
        "checks": [
            {
                "id": check.id,
                "status": check.status,
                "diagnostic_count": len(check.diagnostics),
                "diagnostics": list(check.diagnostics),
            }
            for check in result.checks
        ],
        "semantic_recommendation_included": False,
        "semantic_truth_established": False,
        "explicit_limit": "Mechanical preflight does not decide whether the agent should proceed.",
    }


def _uncertainty_history_projection(workspace: Path, *, compact: bool) -> dict[str, Any]:
    summary = UncertaintyHistoryService(workspace).summary()
    if not compact:
        return summary
    return {
        "present": bool(summary["present"]),
        "valid": bool(summary["valid"]),
        "event_count": int(summary["event_count"]),
        "uncertainty_count": int(summary["uncertainty_count"]),
        "latest_statuses": dict(summary["latest_statuses"]),
        "diagnostic_count": len(summary["diagnostics"]),
        "schema_in_campaign_state": False,
        "semantic_recommendation_included": False,
        "semantic_truth_established": False,
    }


def _bounded(values: list[Any], limit: int | None, field: str, omissions: dict[str, int]) -> list[Any]:
    if limit is None or len(values) <= limit:
        return values
    omissions[field] = len(values) - limit
    return values[-limit:]


def _v1_capsule(
    *,
    workspace: Path,
    snapshot: Any,
    semantic_summary: Mapping[str, Any],
    recent_transitions: int,
    compact: bool,
    include_preflight: bool,
) -> dict[str, Any]:
    state = snapshot.state
    recent = snapshot.transitions[-recent_transitions:] if recent_transitions else ()
    common: dict[str, Any] = {
        "ok": True,
        "code": "CAMPAIGN_RESUME_CONTEXT",
        "capsule_version": "1",
        "projection": "compact" if compact else "full",
        "campaign_id": state.campaign_id,
        "mission": state.mission,
        "status": state.status,
        "current_state": state.current_state,
        "authority": _enum(state.authority),
        "terminal_state": _enum(state.terminal_state),
        "uncertainty_history": _uncertainty_history_projection(workspace, compact=compact),
        "semantic_recommendation_included": False,
        "semantic_truth_established": False,
        "explicit_limit": "This capsule reconstructs durable declared state and deterministic mechanical summaries; it does not decide the next warranted action.",
    }

    if compact:
        common.update(
            {
                "target_ref": _target_ref(state),
                "active_responsibility": _compact_responsibility(state.active_responsibility),
                "active_uncertainty": _compact_uncertainty(state.active_uncertainty),
                "counts": {
                    "established_facts": len(state.established_facts),
                    "resolved_questions": len(state.resolved_questions),
                    "deferred_responsibilities": len(state.deferred_responsibilities),
                    "external_boundaries": len(state.external_boundaries),
                    "evidence_refs": len(snapshot.evidence_refs),
                    "transitions": len(snapshot.transitions),
                },
                "recent_transitions": [_compact_transition(item) for item in recent],
                "handoff_present": snapshot.handoff is not None,
                "semantic_companion": {
                    "present": bool(semantic_summary.get("present")),
                    "valid": bool(semantic_summary.get("valid")),
                    "entry_count": int(semantic_summary.get("entry_count", 0)),
                    "schema_in_campaign_state": False,
                    "semantic_truth_established": False,
                },
            }
        )
    else:
        common.update(
            {
                "target_snapshot": canonicalize(state.target_snapshot) if state.target_snapshot is not None else None,
                "active_responsibility": canonicalize(state.active_responsibility) if state.active_responsibility is not None else None,
                "active_uncertainty": canonicalize(state.active_uncertainty) if state.active_uncertainty is not None else None,
                "established_facts": list(state.established_facts),
                "resolved_questions": list(state.resolved_questions),
                "deferred_responsibilities": [canonicalize(item) for item in state.deferred_responsibilities],
                "external_boundaries": [canonicalize(item) for item in state.external_boundaries],
                "evidence_refs": list(snapshot.evidence_refs),
                "recent_transitions": [canonicalize(item) for item in recent],
                "handoff": canonicalize(snapshot.handoff) if snapshot.handoff is not None else None,
                "semantic_companion": dict(semantic_summary),
            }
        )

    if include_preflight:
        common["preflight"] = _preflight_projection(workspace)
    return common


def build_resume_capsule(
    *,
    workspace: Path,
    snapshot: Any,
    semantic_summary: Mapping[str, Any],
    recent_transitions: int,
    compact: bool,
    include_preflight: bool,
    profile: str | None = None,
    max_items: int | None = None,
) -> dict[str, Any]:
    """Build a stable Resume Capsule projection.

    With no explicit ``profile`` this preserves the v1 full/compact contract.
    Explicit profiles activate v2 progressive disclosure. All projections
    contain only durable state and deterministic mechanical summaries.
    """

    if profile is None:
        return _v1_capsule(
            workspace=workspace,
            snapshot=snapshot,
            semantic_summary=semantic_summary,
            recent_transitions=recent_transitions,
            compact=compact,
            include_preflight=include_preflight,
        )
    if profile not in RESUME_PROFILES:
        raise ValueError(f"profile must be one of {RESUME_PROFILES}")
    if max_items is not None and max_items < 1:
        raise ValueError("max_items must be at least 1")

    state = snapshot.state
    recent = snapshot.transitions[-recent_transitions:] if recent_transitions else ()
    omissions: dict[str, int] = {}
    base: dict[str, Any] = {
        "ok": True,
        "code": "CAMPAIGN_RESUME_CONTEXT",
        "capsule_version": "2",
        "projection": profile,
        "campaign_id": state.campaign_id,
        "mission": state.mission,
        "status": state.status,
        "current_state": state.current_state,
        "authority": _enum(state.authority),
        "terminal_state": _enum(state.terminal_state),
        "target_ref": _target_ref(state),
        "active_responsibility": _compact_responsibility(state.active_responsibility),
        "active_uncertainty": _compact_uncertainty(state.active_uncertainty),
        "semantic_recommendation_included": False,
        "semantic_truth_established": False,
        "explicit_limit": "Progressive disclosure changes deterministic representation density only; it does not summarize semantically or recommend action.",
    }

    if profile == "minimal":
        latest = [_compact_transition(item) for item in recent[-1:]]
        base.update(
            {
                "recent_transitions": latest,
                "counts": {
                    "established_facts": len(state.established_facts),
                    "resolved_questions": len(state.resolved_questions),
                    "deferred_responsibilities": len(state.deferred_responsibilities),
                    "external_boundaries": len(state.external_boundaries),
                    "evidence_refs": len(snapshot.evidence_refs),
                    "transitions": len(snapshot.transitions),
                },
                "handoff_present": snapshot.handoff is not None,
                "uncertainty_history": _uncertainty_history_projection(workspace, compact=True),
            }
        )
    else:
        facts = _bounded(list(state.established_facts), max_items, "established_facts", omissions)
        resolved = _bounded(list(state.resolved_questions), max_items, "resolved_questions", omissions)
        deferred = _bounded(
            [canonicalize(item) for item in state.deferred_responsibilities],
            max_items,
            "deferred_responsibilities",
            omissions,
        )
        evidence = _bounded(list(snapshot.evidence_refs), max_items, "evidence_refs", omissions)
        transitions = _bounded(
            [canonicalize(item) for item in recent],
            max_items,
            "recent_transitions",
            omissions,
        )
        base.update(
            {
                "established_facts": facts,
                "resolved_questions": resolved,
                "deferred_responsibilities": deferred,
                "evidence_refs": evidence,
                "recent_transitions": transitions,
                "handoff": canonicalize(snapshot.handoff) if snapshot.handoff is not None else None,
                "uncertainty_history": _uncertainty_history_projection(workspace, compact=False),
            }
        )
        if profile == "audit":
            base.update(
                {
                    "target_snapshot": canonicalize(state.target_snapshot) if state.target_snapshot is not None else None,
                    "external_boundaries": _bounded(
                        [canonicalize(item) for item in state.external_boundaries],
                        max_items,
                        "external_boundaries",
                        omissions,
                    ),
                    "semantic_companion": dict(semantic_summary),
                    "preflight": _preflight_projection(workspace),
                }
            )
        else:
            base["semantic_companion"] = {
                "present": bool(semantic_summary.get("present")),
                "valid": bool(semantic_summary.get("valid")),
                "entry_count": int(semantic_summary.get("entry_count", 0)),
                "schema_in_campaign_state": False,
                "semantic_truth_established": False,
            }
            if include_preflight:
                base["preflight"] = _preflight_projection(workspace)

    if omissions:
        base["omissions"] = {
            "policy": "tail_preserving_max_items",
            "omitted_counts": omissions,
            "semantic_selection_performed": False,
        }
    return base
