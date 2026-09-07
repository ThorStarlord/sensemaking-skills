"""Explicit YAML boundaries for campaign-semantic artifacts.

Inputs may use the small set of historical representation variants observed in
real campaign artifacts. Outputs always use dataclass field names and enum
values.
"""

from __future__ import annotations

from dataclasses import fields
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, TypeVar

import yaml

from .models import (
    Authority, CampaignHandoff, CampaignPolicy, CampaignState, CampaignTrace, Dependency,
    DependencyType, DeferredResponsibility, ExternalBoundary, Responsibility,
    TerminalState, TransitionRecord, Uncertainty, to_dict,
)


class ContractError(ValueError):
    """Raised when an artifact cannot be represented without losing meaning."""


T = TypeVar("T")


def canonicalize(value: Any) -> Any:
    """Return deterministic decision-relevant data for semantic comparison."""
    return to_dict(value)


def _read(value: Any) -> Mapping[str, Any]:
    if isinstance(value, (str, Path)):
        with Path(value).open(encoding="utf-8") as handle:
            value = yaml.safe_load(handle)
    if not isinstance(value, Mapping):
        raise ContractError("artifact must be a mapping")
    return dict(value)


def _enum(enum_type: type[Enum], value: Any, field_name: str) -> Any:
    if value is None:
        return None
    try:
        return enum_type(value)
    except (TypeError, ValueError) as exc:
        raise ContractError(f"invalid {field_name}: {value!r}") from exc


def _tuple(value: Any, field_name: str) -> tuple[Any, ...]:
    if value is None:
        return ()
    if isinstance(value, (str, bytes)) or not isinstance(value, (list, tuple)):
        raise ContractError(f"{field_name} must be a list")
    return tuple(value)


def _unknown(data: Mapping[str, Any], known: set[str], *, path: str) -> dict[str, Any]:
    allowed = {"owner_routing"} if path == "campaign_state" else set()
    unknown = [key for key in data if key not in known and key not in allowed]
    if unknown:
        raise ContractError(f"unknown decision-relevant field(s) at {path}: {sorted(unknown)}")
    return {key: data[key] for key in data if key not in known}


def _responsibility(value: Mapping[str, Any], path: str = "responsibility", *, state_snapshot: bool = False) -> Responsibility:
    known = {field.name for field in fields(Responsibility)}
    required = ("id", "statement", "scope", "authority")
    missing = {name for name in required if name not in value}
    if not state_snapshot:
        missing |= {name for name in ("decision_blocked", "success_conditions") if name not in value}
    if missing:
        raise ContractError(f"{path} missing required fields: {sorted(missing)}")
    dependencies = tuple(
        Dependency(type=_enum(DependencyType, item.get("type"), f"{path}.dependencies.type"), requires=item.get("requires"))
        for item in _tuple(value.get("dependencies"), f"{path}.dependencies")
        if isinstance(item, Mapping)
    )
    if len(dependencies) != len(_tuple(value.get("dependencies"), f"{path}.dependencies")):
        raise ContractError(f"{path}.dependencies entries must be mappings")
    return Responsibility(
        id=value["id"], statement=value["statement"],
        trigger_evidence=_tuple(value.get("trigger_evidence"), f"{path}.trigger_evidence"),
        decision_blocked=value.get("decision_blocked"), scope=value["scope"],
        authority=_enum(Authority, value["authority"], f"{path}.authority"),
        success_conditions=_tuple(value.get("success_conditions"), f"{path}.success_conditions"),
        status=value.get("status", "active"), dependencies=dependencies,
    )


def _uncertainty(value: Mapping[str, Any], path: str = "active_uncertainty") -> Uncertainty:
    required = {"id", "question"}
    if not required <= value.keys():
        raise ContractError(f"{path} missing required fields: {sorted(required - value.keys())}")
    consequences = value.get("consequences", {})
    if not isinstance(consequences, Mapping):
        raise ContractError(f"{path}.consequences must be a mapping")
    return Uncertainty(id=value["id"], question=value["question"], consequences=dict(consequences), status=value.get("status", "active"), materiality=value.get("materiality", "decision_changing"))


def _deferred(value: Mapping[str, Any], path: str) -> DeferredResponsibility:
    required = {"responsibility_id", "reason"}
    if not required <= value.keys():
        raise ContractError(f"{path} missing required fields: {sorted(required - value.keys())}")
    return DeferredResponsibility(responsibility_id=value["responsibility_id"], reason=value["reason"], reopen_when=_tuple(value.get("reopen_when"), f"{path}.reopen_when"), not_reopened_by=_tuple(value.get("not_reopened_by"), f"{path}.not_reopened_by"), status=value.get("status", "deferred"))


def _boundary(value: Mapping[str, Any], path: str) -> ExternalBoundary:
    required = {"id", "capability", "owner", "repository_owned", "accessible", "implication"}
    if not required <= value.keys():
        raise ContractError(f"{path} missing required fields: {sorted(required - value.keys())}")
    return ExternalBoundary(id=value["id"], capability=value["capability"], owner=value["owner"], repository_owned=bool(value["repository_owned"]), accessible=bool(value["accessible"]), evidence=_tuple(value.get("evidence"), f"{path}.evidence"), implication=value["implication"], reopen_when=_tuple(value.get("reopen_when"), f"{path}.reopen_when"))


def load_campaign_state(value: Any) -> CampaignState:
    data = _read(value)
    required = {"campaign_id", "mission", "status", "current_state"}
    if not required <= data.keys():
        raise ContractError(f"campaign state missing required fields: {sorted(required - data.keys())}")
    if data.get("schema_version", "1") != "1":
        raise ContractError(f"unsupported schema_version: {data['schema_version']!r}")
    active = data.get("active_responsibility")
    state = CampaignState(
        campaign_id=data["campaign_id"], mission=data["mission"], status=data["status"], current_state=data["current_state"],
        active_responsibility=_responsibility(active, state_snapshot=True) if active is not None else None,
        active_uncertainty=_uncertainty(data["active_uncertainty"]) if data.get("active_uncertainty") is not None else None,
        established_facts=_tuple(data.get("established_facts"), "established_facts"), resolved_questions=_tuple(data.get("resolved_questions"), "resolved_questions"),
        deferred_responsibilities=tuple(_deferred(item, f"deferred_responsibilities[{i}]") for i, item in enumerate(_tuple(data.get("deferred_responsibilities"), "deferred_responsibilities"))),
        external_boundaries=tuple(_boundary(item, f"external_boundaries[{i}]") for i, item in enumerate(_tuple(data.get("external_boundaries"), "external_boundaries"))),
        authority=_enum(Authority, data.get("authority"), "authority"), terminal_state=_enum(TerminalState, data.get("terminal_state"), "terminal_state"),
        additional_active_responsibilities=tuple(_responsibility(item, f"additional_active_responsibilities[{i}]", state_snapshot=True) for i, item in enumerate(_tuple(data.get("additional_active_responsibilities"), "additional_active_responsibilities"))),
        schema_version=data.get("schema_version", "1"), extensions={**dict(data.get("extensions", {})), **_unknown(data, {"campaign_id", "mission", "status", "current_state", "active_responsibility", "active_uncertainty", "established_facts", "resolved_questions", "deferred_responsibilities", "external_boundaries", "authority", "terminal_state", "additional_active_responsibilities", "schema_version", "extensions"}, path="campaign_state")},
    )
    result = __import__("sensemaking_skills.campaign_semantics.models", fromlist=["validate_campaign_state"]).validate_campaign_state(state)
    if not result.valid:
        details = "; ".join(d.code for d in result.diagnostics)
        if "TERMINAL_STATE_HAS_ACTIVE_RESPONSIBILITY" in details:
            details = "terminal state has active responsibility (" + details + ")"
        raise ContractError("campaign state invalid: " + details)
    return state


def dump_campaign_state(value: CampaignState) -> dict[str, Any]:
    if not isinstance(value, CampaignState):
        raise ContractError("dump_campaign_state expects CampaignState")
    return to_dict(value)


def load_transition_record(value: Any) -> TransitionRecord:
    data = _read(value)
    required = {"id", "from_state", "to_state", "evidence", "decision"}
    if not required <= data.keys():
        raise ContractError(f"transition missing required fields: {sorted(required - data.keys())}")
    if data.get("schema_version", "1") != "1":
        raise ContractError(f"unsupported schema_version: {data['schema_version']!r}")
    return TransitionRecord(id=data["id"], from_state=data["from_state"], to_state=data["to_state"], evidence=_tuple(data["evidence"], "evidence"), decision=data["decision"], next_responsibility=data.get("next_responsibility"), terminal_state=_enum(TerminalState, data.get("terminal_state"), "terminal_state"), authority=_enum(Authority, data.get("authority"), "authority"), schema_version=data.get("schema_version", "1"))


def dump_transition_record(value: TransitionRecord) -> dict[str, Any]:
    return to_dict(value)


def load_campaign_policy(value: Any) -> CampaignPolicy:
    data = _read(value)
    return CampaignPolicy(campaign_id=data["campaign_id"], mission=data["mission"], known_transitions=tuple(data.get("known_transitions", ())), authority_boundaries=dict(data.get("authority_boundaries", {})), stop_conditions=tuple(_enum(TerminalState, item, "stop_conditions") for item in data.get("stop_conditions", ())), dynamic_responsibility_policy=tuple(data.get("dynamic_responsibility_policy", ())), schema_version=data.get("schema_version", "1"))


def dump_campaign_policy(value: CampaignPolicy) -> dict[str, Any]:
    return to_dict(value)


def load_campaign_trace(value: Any) -> CampaignTrace:
    data = _read(value)
    if "campaign_id" not in data or not isinstance(data.get("events", []), list):
        raise ContractError("trace requires campaign_id and list events")
    return CampaignTrace(campaign_id=data["campaign_id"], events=tuple(data.get("events", ())), schema_version=data.get("schema_version", "1"), replication_id=data.get("replication_id"), initial_state=data.get("initial_state"), terminal_state=data.get("terminal_state"), extensions=dict(data.get("extensions", {})))


def load_responsibility(value: Any) -> Responsibility:
    return _responsibility(_read(value))


def dump_responsibility(value: Responsibility) -> dict[str, Any]:
    if not isinstance(value, Responsibility):
        raise ContractError("dump_responsibility expects Responsibility")
    return to_dict(value)


def load_campaign_handoff(value: Any, *, current_state: CampaignState | None = None) -> CampaignHandoff:
    data = _read(value)
    required = {"campaign_id", "stop_conditions"}
    if not required <= data.keys():
        raise ContractError(f"handoff missing required fields: {sorted(required - data.keys())}")
    state_value = data.get("current_state")
    if isinstance(state_value, Mapping):
        state = load_campaign_state(state_value)
    elif current_state is not None:
        state = current_state
    elif data.get("current_state_reference"):
        raise ContractError("handoff current_state_reference requires current_state")
    else:
        raise ContractError("handoff requires current_state")
    actions = data.get("allowed_next_actions", data.get("allowed_actions"))
    if actions is None:
        raise ContractError("handoff requires allowed_next_actions")
    return CampaignHandoff(campaign_id=data["campaign_id"], current_state=state, canonical_artifacts=_tuple(data.get("canonical_artifacts"), "canonical_artifacts"), allowed_next_actions=_tuple(actions, "allowed_next_actions"), stop_conditions=tuple(_enum(TerminalState, item, "stop_conditions") for item in data["stop_conditions"]), schema_version=data.get("schema_version", "1"))


def dump_campaign_handoff(value: CampaignHandoff) -> dict[str, Any]:
    if not isinstance(value, CampaignHandoff):
        raise ContractError("dump_campaign_handoff expects CampaignHandoff")
    return to_dict(value)


def dump_campaign_trace(value: CampaignTrace) -> dict[str, Any]:
    return to_dict(value)
