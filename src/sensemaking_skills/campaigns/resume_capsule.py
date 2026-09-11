"""Deterministic Resume Capsule v1 projections over durable Campaign state."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from sensemaking_skills.campaign_semantics import canonicalize, target_snapshot_sha256

from .preflight import CampaignPreflightService
from .uncertainty_history import UncertaintyHistoryService


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


def build_resume_capsule(
    *,
    workspace: Path,
    snapshot: Any,
    semantic_summary: Mapping[str, Any],
    recent_transitions: int,
    compact: bool,
    include_preflight: bool,
) -> dict[str, Any]:
    """Build a stable full or compact fresh-context projection.

    The projection contains only durable state and deterministic mechanical
    summaries. It never chooses or recommends a next action.
    """

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
                "target_snapshot": (
                    canonicalize(state.target_snapshot)
                    if state.target_snapshot is not None
                    else None
                ),
                "active_responsibility": (
                    canonicalize(state.active_responsibility)
                    if state.active_responsibility is not None
                    else None
                ),
                "active_uncertainty": (
                    canonicalize(state.active_uncertainty)
                    if state.active_uncertainty is not None
                    else None
                ),
                "established_facts": list(state.established_facts),
                "resolved_questions": list(state.resolved_questions),
                "deferred_responsibilities": [
                    canonicalize(item) for item in state.deferred_responsibilities
                ],
                "external_boundaries": [
                    canonicalize(item) for item in state.external_boundaries
                ],
                "evidence_refs": list(snapshot.evidence_refs),
                "recent_transitions": [canonicalize(item) for item in recent],
                "handoff": (
                    canonicalize(snapshot.handoff)
                    if snapshot.handoff is not None
                    else None
                ),
                "semantic_companion": dict(semantic_summary),
            }
        )

    if include_preflight:
        common["preflight"] = _preflight_projection(workspace)
    return common
