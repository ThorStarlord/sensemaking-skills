"""Explicit YAML boundaries for campaign-semantic artifacts.

Inputs may use the small set of historical representation variants observed in
real campaign artifacts. Loaders deterministically upgrade supported historical
representations in memory; outputs always use the current schema plus dataclass
field names and enum values.

Every public loader enforces the same contract uniformly, at the top level and
inside every nested decision-relevant record:

* unknown fields are rejected with ``ContractError`` -- never silently dropped;
* supported legacy ``schema_version`` values are migrated only through the
  explicit one-way migration registry;
* missing or malformed known fields raise ``ContractError`` rather than leaking
  ``KeyError`` / ``TypeError``.

Schema v2 canonicalizes the historical top-level ``owner_routing`` state
extension under ``extensions`` and the handoff ``allowed_actions`` alias to
``allowed_next_actions``. A ``CampaignHandoff``'s ``campaign_id`` must match the
``campaign_id`` of its resolved current state.
"""

from __future__ import annotations

from dataclasses import fields
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Mapping, TypeVar

import yaml

from .models import (
    Authority, CampaignHandoff, CampaignPolicy, CampaignState, CampaignTrace, Dependency,
    DependencyType, DeferredResponsibility, ExternalBoundary, Responsibility,
    TerminalState, TransitionRecord, Uncertainty, to_dict, validate_campaign_state,
)
from .schema import CURRENT_SCHEMA_VERSION, SchemaMigrationError, migrate_payload


class ContractError(ValueError):
    """Raised when an artifact cannot be represented without losing meaning."""


T = TypeVar("T")

_SCHEMA_VERSION = CURRENT_SCHEMA_VERSION

_RESPONSIBILITY_FIELDS = {f.name for f in fields(Responsibility)}
_UNCERTAINTY_FIELDS = {f.name for f in fields(Uncertainty)}
_DEFERRED_FIELDS = {f.name for f in fields(DeferredResponsibility)}
_BOUNDARY_FIELDS = {f.name for f in fields(ExternalBoundary)}
_DEPENDENCY_FIELDS = {f.name for f in fields(Dependency)}
_STATE_FIELDS = {f.name for f in fields(CampaignState)}
_TRANSITION_FIELDS = {f.name for f in fields(TransitionRecord)}
_POLICY_FIELDS = {f.name for f in fields(CampaignPolicy)}
_TRACE_FIELDS = {f.name for f in fields(CampaignTrace)}
_HANDOFF_FIELDS = {f.name for f in fields(CampaignHandoff)} | {"current_state_reference"}


def canonicalize(value: Any) -> Any:
    """Return deterministic decision-relevant data for semantic comparison."""
    return to_dict(value)


def _read(value: Any) -> dict[str, Any]:
    if isinstance(value, (str, Path)):
        with Path(value).open(encoding="utf-8") as handle:
            value = yaml.safe_load(handle)
    if not isinstance(value, Mapping):
        raise ContractError("artifact must be a mapping")
    return dict(value)


def _prepare(data: Mapping[str, Any], *, artifact_kind: str, path: str) -> dict[str, Any]:
    try:
        return migrate_payload(data, artifact_kind=artifact_kind).payload
    except SchemaMigrationError as exc:
        raise ContractError(f"schema migration failed at {path}: {exc}") from exc


def _dump_current(value: Any, *, artifact_kind: str, path: str) -> dict[str, Any]:
    data = to_dict(value)
    try:
        return migrate_payload(data, artifact_kind=artifact_kind).payload
    except SchemaMigrationError as exc:
        raise ContractError(f"schema migration failed at {path}: {exc}") from exc


def _require(data: Mapping[str, Any], required: Iterable[str], *, path: str) -> None:
    missing = sorted(name for name in required if name not in data)
    if missing:
        raise ContractError(f"{path} missing required fields: {missing}")


def _schema_version(data: Mapping[str, Any], *, path: str) -> str:
    version = data.get("schema_version")
    if version != _SCHEMA_VERSION:
        raise ContractError(f"unsupported schema_version at {path}: {version!r}")
    return version


def _reject_unknown(data: Mapping[str, Any], known: Iterable[str], *, path: str, allowed: Iterable[str] = ()) -> dict[str, Any]:
    """Fail on any unknown key; return the subset that is a sanctioned extension."""
    known_set = set(known)
    allowed_set = set(allowed)
    unknown = sorted(key for key in data if key not in known_set and key not in allowed_set)
    if unknown:
        raise ContractError(f"unknown decision-relevant field(s) at {path}: {unknown}")
    return {key: data[key] for key in data if key in allowed_set}


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


def _mapping(value: Any, field_name: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise ContractError(f"{field_name} must be a mapping")
    return dict(value)


def _dependency(item: Any, path: str) -> Dependency:
    if not isinstance(item, Mapping):
        raise ContractError(f"{path} must be a mapping")
    _reject_unknown(item, _DEPENDENCY_FIELDS, path=path)
    _require(item, ("type", "requires"), path=path)
    return Dependency(type=_enum(DependencyType, item["type"], f"{path}.type"), requires=item["requires"])


def _responsibility(value: Any, path: str = "responsibility", *, state_snapshot: bool = False) -> Responsibility:
    if not isinstance(value, Mapping):
        raise ContractError(f"{path} must be a mapping")
    _reject_unknown(value, _RESPONSIBILITY_FIELDS, path=path)
    required = ["id", "statement", "scope", "authority"]
    if not state_snapshot:
        required += ["decision_blocked", "success_conditions"]
    _require(value, required, path=path)
    dependencies = tuple(
        _dependency(item, f"{path}.dependencies[{i}]")
        for i, item in enumerate(_tuple(value.get("dependencies"), f"{path}.dependencies"))
    )
    return Responsibility(
        id=value["id"], statement=value["statement"],
        trigger_evidence=_tuple(value.get("trigger_evidence"), f"{path}.trigger_evidence"),
        decision_blocked=value.get("decision_blocked"), scope=value["scope"],
        authority=_enum(Authority, value["authority"], f"{path}.authority"),
        success_conditions=_tuple(value.get("success_conditions"), f"{path}.success_conditions"),
        status=value.get("status", "active"), dependencies=dependencies,
    )


def _uncertainty(value: Any, path: str = "active_uncertainty") -> Uncertainty:
    if not isinstance(value, Mapping):
        raise ContractError(f"{path} must be a mapping")
    _reject_unknown(value, _UNCERTAINTY_FIELDS, path=path)
    _require(value, ("id", "question"), path=path)
    return Uncertainty(
        id=value["id"], question=value["question"],
        consequences=_mapping(value.get("consequences"), f"{path}.consequences"),
        status=value.get("status", "active"),
        materiality=value.get("materiality", "decision_changing"),
    )


def _deferred(value: Any, path: str) -> DeferredResponsibility:
    if not isinstance(value, Mapping):
        raise ContractError(f"{path} must be a mapping")
    _reject_unknown(value, _DEFERRED_FIELDS, path=path)
    _require(value, ("responsibility_id", "reason"), path=path)
    return DeferredResponsibility(
        responsibility_id=value["responsibility_id"], reason=value["reason"],
        reopen_when=_tuple(value.get("reopen_when"), f"{path}.reopen_when"),
        not_reopened_by=_tuple(value.get("not_reopened_by"), f"{path}.not_reopened_by"),
        status=value.get("status", "deferred"),
    )


def _boundary(value: Any, path: str) -> ExternalBoundary:
    if not isinstance(value, Mapping):
        raise ContractError(f"{path} must be a mapping")
    _reject_unknown(value, _BOUNDARY_FIELDS, path=path)
    _require(value, ("id", "capability", "owner", "repository_owned", "accessible", "implication"), path=path)
    return ExternalBoundary(
        id=value["id"], capability=value["capability"], owner=value["owner"],
        repository_owned=bool(value["repository_owned"]), accessible=bool(value["accessible"]),
        evidence=_tuple(value.get("evidence"), f"{path}.evidence"),
        implication=value["implication"], reopen_when=_tuple(value.get("reopen_when"), f"{path}.reopen_when"),
    )


def load_campaign_state(value: Any) -> CampaignState:
    data = _prepare(_read(value), artifact_kind="campaign_state", path="campaign_state")
    _require(data, ("campaign_id", "mission", "status", "current_state"), path="campaign_state")
    schema_version = _schema_version(data, path="campaign_state")
    _reject_unknown(data, _STATE_FIELDS, path="campaign_state")
    extensions = _mapping(data.get("extensions"), "campaign_state.extensions")
    active = data.get("active_responsibility")
    state = CampaignState(
        campaign_id=data["campaign_id"], mission=data["mission"], status=data["status"], current_state=data["current_state"],
        active_responsibility=_responsibility(active, "active_responsibility", state_snapshot=True) if active is not None else None,
        active_uncertainty=_uncertainty(data["active_uncertainty"]) if data.get("active_uncertainty") is not None else None,
        established_facts=_tuple(data.get("established_facts"), "established_facts"),
        resolved_questions=_tuple(data.get("resolved_questions"), "resolved_questions"),
        deferred_responsibilities=tuple(_deferred(item, f"deferred_responsibilities[{i}]") for i, item in enumerate(_tuple(data.get("deferred_responsibilities"), "deferred_responsibilities"))),
        external_boundaries=tuple(_boundary(item, f"external_boundaries[{i}]") for i, item in enumerate(_tuple(data.get("external_boundaries"), "external_boundaries"))),
        authority=_enum(Authority, data.get("authority"), "authority"),
        terminal_state=_enum(TerminalState, data.get("terminal_state"), "terminal_state"),
        additional_active_responsibilities=tuple(_responsibility(item, f"additional_active_responsibilities[{i}]", state_snapshot=True) for i, item in enumerate(_tuple(data.get("additional_active_responsibilities"), "additional_active_responsibilities"))),
        schema_version=schema_version,
        extensions=extensions,
    )
    result = validate_campaign_state(state)
    if not result.valid:
        details = "; ".join(d.code for d in result.diagnostics)
        if "TERMINAL_STATE_HAS_ACTIVE_RESPONSIBILITY" in details:
            details = "terminal state has active responsibility (" + details + ")"
        raise ContractError("campaign state invalid: " + details)
    return state


def dump_campaign_state(value: CampaignState) -> dict[str, Any]:
    if not isinstance(value, CampaignState):
        raise ContractError("dump_campaign_state expects CampaignState")
    return _dump_current(value, artifact_kind="campaign_state", path="campaign_state")


def load_transition_record(value: Any) -> TransitionRecord:
    data = _prepare(_read(value), artifact_kind="transition", path="transition")
    _require(data, ("id", "from_state", "to_state", "evidence", "decision"), path="transition")
    schema_version = _schema_version(data, path="transition")
    _reject_unknown(data, _TRANSITION_FIELDS, path="transition")
    return TransitionRecord(
        id=data["id"], from_state=data["from_state"], to_state=data["to_state"],
        evidence=_tuple(data["evidence"], "transition.evidence"), decision=data["decision"],
        next_responsibility=data.get("next_responsibility"),
        terminal_state=_enum(TerminalState, data.get("terminal_state"), "transition.terminal_state"),
        authority=_enum(Authority, data.get("authority"), "transition.authority"),
        schema_version=schema_version,
    )


def dump_transition_record(value: TransitionRecord) -> dict[str, Any]:
    if not isinstance(value, TransitionRecord):
        raise ContractError("dump_transition_record expects TransitionRecord")
    return _dump_current(value, artifact_kind="transition", path="transition")


def load_campaign_policy(value: Any) -> CampaignPolicy:
    data = _prepare(_read(value), artifact_kind="campaign_policy", path="campaign_policy")
    _require(data, ("campaign_id", "mission"), path="campaign_policy")
    schema_version = _schema_version(data, path="campaign_policy")
    _reject_unknown(data, _POLICY_FIELDS, path="campaign_policy")
    return CampaignPolicy(
        campaign_id=data["campaign_id"], mission=data["mission"],
        known_transitions=tuple(
            _mapping(item, f"campaign_policy.known_transitions[{i}]")
            for i, item in enumerate(_tuple(data.get("known_transitions"), "campaign_policy.known_transitions"))
        ),
        authority_boundaries=_mapping(data.get("authority_boundaries"), "campaign_policy.authority_boundaries"),
        stop_conditions=tuple(
            _enum(TerminalState, item, "campaign_policy.stop_conditions")
            for item in _tuple(data.get("stop_conditions"), "campaign_policy.stop_conditions")
        ),
        dynamic_responsibility_policy=_tuple(data.get("dynamic_responsibility_policy"), "campaign_policy.dynamic_responsibility_policy"),
        schema_version=schema_version,
    )


def dump_campaign_policy(value: CampaignPolicy) -> dict[str, Any]:
    if not isinstance(value, CampaignPolicy):
        raise ContractError("dump_campaign_policy expects CampaignPolicy")
    return _dump_current(value, artifact_kind="campaign_policy", path="campaign_policy")


def load_campaign_trace(value: Any) -> CampaignTrace:
    data = _prepare(_read(value), artifact_kind="campaign_trace", path="campaign_trace")
    _require(data, ("campaign_id",), path="campaign_trace")
    schema_version = _schema_version(data, path="campaign_trace")
    events = data.get("events", [])
    if not isinstance(events, list):
        raise ContractError("campaign_trace.events must be a list")
    _reject_unknown(data, _TRACE_FIELDS, path="campaign_trace")
    return CampaignTrace(
        campaign_id=data["campaign_id"], events=tuple(events),
        schema_version=schema_version,
        replication_id=data.get("replication_id"),
        initial_state=data.get("initial_state"),
        terminal_state=data.get("terminal_state"),
        extensions=_mapping(data.get("extensions"), "campaign_trace.extensions"),
    )


def dump_campaign_trace(value: CampaignTrace) -> dict[str, Any]:
    if not isinstance(value, CampaignTrace):
        raise ContractError("dump_campaign_trace expects CampaignTrace")
    return _dump_current(value, artifact_kind="campaign_trace", path="campaign_trace")


def load_responsibility(value: Any) -> Responsibility:
    return _responsibility(_read(value))


def dump_responsibility(value: Responsibility) -> dict[str, Any]:
    if not isinstance(value, Responsibility):
        raise ContractError("dump_responsibility expects Responsibility")
    return to_dict(value)


def load_campaign_handoff(value: Any, *, current_state: CampaignState | None = None) -> CampaignHandoff:
    data = _prepare(_read(value), artifact_kind="campaign_handoff", path="campaign_handoff")
    _require(data, ("campaign_id", "stop_conditions"), path="campaign_handoff")
    schema_version = _schema_version(data, path="campaign_handoff")
    _reject_unknown(data, _HANDOFF_FIELDS, path="campaign_handoff")
    state_value = data.get("current_state")
    if isinstance(state_value, Mapping):
        state = load_campaign_state(state_value)
    elif state_value is not None:
        raise ContractError("campaign_handoff.current_state must be a mapping")
    elif current_state is not None:
        state = current_state
    elif data.get("current_state_reference"):
        raise ContractError("handoff current_state_reference requires a resolved current_state")
    else:
        raise ContractError("handoff requires current_state")
    if data["campaign_id"] != state.campaign_id:
        raise ContractError(
            f"handoff campaign_id {data['campaign_id']!r} does not match "
            f"current_state campaign_id {state.campaign_id!r}"
        )
    actions = data.get("allowed_next_actions")
    if actions is None:
        raise ContractError("handoff requires allowed_next_actions")
    return CampaignHandoff(
        campaign_id=data["campaign_id"], current_state=state,
        canonical_artifacts=_tuple(data.get("canonical_artifacts"), "campaign_handoff.canonical_artifacts"),
        allowed_next_actions=_tuple(actions, "campaign_handoff.allowed_next_actions"),
        stop_conditions=tuple(
            _enum(TerminalState, item, "campaign_handoff.stop_conditions")
            for item in _tuple(data["stop_conditions"], "campaign_handoff.stop_conditions")
        ),
        schema_version=schema_version,
    )


def dump_campaign_handoff(value: CampaignHandoff) -> dict[str, Any]:
    if not isinstance(value, CampaignHandoff):
        raise ContractError("dump_campaign_handoff expects CampaignHandoff")
    return _dump_current(value, artifact_kind="campaign_handoff", path="campaign_handoff")
