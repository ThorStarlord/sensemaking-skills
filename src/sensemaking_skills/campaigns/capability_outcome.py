"""Agent-authored capability-outcome binding for one Campaign.

The binding is a compact continuation record for one selected opportunity. It
does not select the opportunity, verify its sources, establish realization or
replace the Campaign mission and active responsibility. It is stored under the
Campaign state's ``extensions.capability_outcome`` key and projected by the
existing working-context and resume surfaces.

A binding is committed with a lifecycle transition that preserves the active
responsibility. It is immutable for one Campaign: a different governing outcome
requires a new Campaign rather than silently rewriting the old commitment.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from sensemaking_skills.campaign_semantics import canonicalize

from .errors import CampaignTransactionError

CAPABILITY_OUTCOME_EXTENSION = "capability_outcome"
CAPABILITY_OUTCOME_SCHEMA_VERSION = "1"
CAPABILITY_OUTCOME_EPISTEMIC_STATUS = "selected_hypothesis"
CAPABILITY_OUTCOME_REALIZATION = "not_established"


def _require_text(value: str, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CampaignTransactionError(f"{field} must be non-empty")
    return value.strip()


def _clean_items(values: Sequence[str], *, field: str) -> list[str]:
    cleaned = [_require_text(value, field=field) for value in values]
    return list(dict.fromkeys(cleaned))


def build_capability_outcome(
    *,
    possibility_id: str,
    desired_behavior: str,
    completion_condition: str,
    selection_basis: str,
    bound_from_state: str,
    source_refs: Sequence[str] = (),
    assumptions: Sequence[str] = (),
    counterevidence: Sequence[str] = (),
    required_capabilities: Sequence[str] = (),
    remaining_conditions: Sequence[str] = (),
) -> dict[str, Any]:
    """Build the validated agent-authored extension payload.

    Every value is authored by the agent. The deterministic layer only
    normalizes whitespace, removes exact duplicates and fixes the claim
    ceiling: a bound outcome is a selected hypothesis, not observed
    realization.
    """

    return {
        "schema_version": CAPABILITY_OUTCOME_SCHEMA_VERSION,
        "possibility_id": _require_text(possibility_id, field="possibility_id"),
        "desired_behavior": _require_text(desired_behavior, field="desired_behavior"),
        "completion_condition": _require_text(
            completion_condition, field="completion_condition"
        ),
        "selection_basis": _require_text(selection_basis, field="selection_basis"),
        "epistemic_status": CAPABILITY_OUTCOME_EPISTEMIC_STATUS,
        "realization": CAPABILITY_OUTCOME_REALIZATION,
        "bound_from_state": _require_text(bound_from_state, field="bound_from_state"),
        "source_refs": _clean_items(source_refs, field="source_ref"),
        "assumptions": _clean_items(assumptions, field="assumption"),
        "counterevidence": _clean_items(counterevidence, field="counterevidence"),
        "required_capabilities": _clean_items(
            required_capabilities, field="required_capability"
        ),
        "remaining_conditions": _clean_items(
            remaining_conditions, field="remaining_condition"
        ),
    }


def _outcome_mapping(state: Any) -> Mapping[str, Any] | None:
    extensions = getattr(state, "extensions", None)
    if not isinstance(extensions, Mapping):
        return None
    value = extensions.get(CAPABILITY_OUTCOME_EXTENSION)
    return value if isinstance(value, Mapping) else None


def capability_outcome_projection(state: Any) -> dict[str, Any] | None:
    """Return the full durable outcome for a Campaign, or ``None``."""

    value = _outcome_mapping(state)
    if value is None:
        return None
    return canonicalize(dict(value))


def capability_outcome_summary(state: Any) -> dict[str, Any] | None:
    """Return a compact identity/count projection for dense resume capsules."""

    value = _outcome_mapping(state)
    if value is None:
        return None
    return {
        "possibility_id": value.get("possibility_id"),
        "desired_behavior": value.get("desired_behavior"),
        "completion_condition": value.get("completion_condition"),
        "epistemic_status": value.get("epistemic_status"),
        "realization": value.get("realization"),
        "source_ref_count": len(value.get("source_refs") or []),
        "assumption_count": len(value.get("assumptions") or []),
        "counterevidence_count": len(value.get("counterevidence") or []),
        "required_capability_count": len(value.get("required_capabilities") or []),
        "remaining_condition_count": len(value.get("remaining_conditions") or []),
        "semantic_selection_performed": False,
    }
