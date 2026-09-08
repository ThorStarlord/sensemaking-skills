"""Typed campaign artifacts and integrity-only reconstruction checks."""

from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass
from enum import Enum
from typing import Any, Mapping, Optional


class _TextEnum(str, Enum):
    def __str__(self) -> str: return self.value


class Authority(_TextEnum):
    AUTHORIZED_AUTONOMOUSLY = "authorized_autonomously"
    OWNER_AUTHORIZATION_REQUIRED = "owner_authorization_required"
    EXTERNAL_AUTHORITY_REQUIRED = "external_authority_required"
    PROHIBITED = "prohibited"
    OUTSIDE_PRODUCT_BOUNDARY = "outside_product_boundary"


class TerminalState(_TextEnum):
    GOAL_ACHIEVED = "goal_achieved"
    NO_FURTHER_WORK_WARRANTED = "no_further_work_warranted"
    OWNER_DECISION_REQUIRED = "owner_decision_required"
    AUTHORITY_BOUNDARY_REACHED = "authority_boundary_reached"
    EXTERNAL_BLOCKER = "external_blocker"
    EVIDENCE_INSUFFICIENT = "evidence_insufficient"
    INVALID_EXECUTION = "invalid_execution"
    DEFERRED = "deferred"
    QUALIFIED_PR_READY = "qualified_pr_ready"


class DependencyType(_TextEnum):
    TASK = "task"
    EVIDENCE = "evidence"
    AUTHORITY = "authority"


@dataclass(frozen=True)
class Capability:
    id: str
    accepted_responsibility_types: tuple[str, ...]
    output_artifact: str
    input_artifact: Optional[str] = None
    completion_conditions: tuple[str, ...] = ()


@dataclass(frozen=True)
class CapabilityAvailability:
    capability_id: str
    available: bool
    reason: str = ""


@dataclass(frozen=True)
class CampaignConstitution:
    mission: str
    principles: tuple[str, ...]
    non_goals: tuple[str, ...]
    terminal_states: tuple[TerminalState, ...]
    version: str = "1"


@dataclass(frozen=True)
class Dependency:
    type: DependencyType
    requires: str
    def to_dict(self) -> dict[str, Any]: return {"type": self.type.value, "requires": self.requires}


@dataclass(frozen=True)
class Uncertainty:
    id: str
    question: str
    consequences: Mapping[str, str]
    status: str = "active"
    materiality: str = "decision_changing"


@dataclass(frozen=True)
class Responsibility:
    id: str
    statement: str
    trigger_evidence: tuple[str, ...]
    decision_blocked: Optional[str]
    scope: str
    authority: Authority
    success_conditions: tuple[str, ...]
    status: str = "active"
    dependencies: tuple[Dependency, ...] = ()


@dataclass(frozen=True)
class DeferredResponsibility:
    responsibility_id: str
    reason: str
    reopen_when: tuple[str, ...]
    not_reopened_by: tuple[str, ...] = ()
    status: str = "deferred"


@dataclass(frozen=True)
class ExternalBoundary:
    id: str
    capability: str
    owner: str
    repository_owned: bool
    accessible: bool
    evidence: tuple[str, ...]
    implication: str
    reopen_when: tuple[str, ...]


@dataclass(frozen=True)
class ClaimEvidence:
    claim: str
    scope: str
    method: str
    coverage: tuple[str, ...]
    claim_strength: str
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class CampaignState:
    campaign_id: str
    mission: str
    status: str
    current_state: str
    active_responsibility: Optional[Responsibility] = None
    active_uncertainty: Optional[Uncertainty] = None
    established_facts: tuple[str, ...] = ()
    resolved_questions: tuple[str, ...] = ()
    deferred_responsibilities: tuple[DeferredResponsibility, ...] = ()
    external_boundaries: tuple[ExternalBoundary, ...] = ()
    authority: Optional[Authority] = None
    terminal_state: Optional[TerminalState] = None
    additional_active_responsibilities: tuple[Responsibility, ...] = ()
    schema_version: str = "1"
    extensions: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TransitionRecord:
    id: str
    from_state: str
    to_state: str
    evidence: tuple[str, ...]
    decision: str
    next_responsibility: Optional[str] = None
    terminal_state: Optional[TerminalState] = None
    authority: Optional[Authority] = None
    schema_version: str = "1"


@dataclass(frozen=True)
class CampaignPolicy:
    campaign_id: str
    mission: str
    known_transitions: tuple[Mapping[str, Any], ...] = ()
    authority_boundaries: Mapping[str, str] = field(default_factory=dict)
    stop_conditions: tuple[TerminalState, ...] = ()
    dynamic_responsibility_policy: tuple[str, ...] = ()
    schema_version: str = "1"


@dataclass(frozen=True)
class CampaignHandoff:
    campaign_id: str
    current_state: CampaignState
    canonical_artifacts: tuple[str, ...]
    allowed_next_actions: tuple[str, ...]
    stop_conditions: tuple[TerminalState, ...]
    schema_version: str = "1"


@dataclass(frozen=True)
class CampaignTrace:
    campaign_id: str
    events: tuple[Mapping[str, Any], ...] = ()
    schema_version: str = "1"
    replication_id: Optional[str] = None
    initial_state: Optional[str] = None
    terminal_state: Optional[str] = None
    extensions: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ValidationDiagnostic:
    code: str
    detail: str
    path: str = ""


@dataclass(frozen=True)
class ReconstructionResult:
    valid: bool
    diagnostics: tuple[ValidationDiagnostic, ...] = ()


def _walk(value: Any) -> Any:
    if isinstance(value, Enum): return value.value
    if is_dataclass(value): return {f.name: _walk(getattr(value, f.name)) for f in fields(value)}
    if isinstance(value, Mapping): return {str(k): _walk(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)): return [_walk(v) for v in value]
    return value


def to_dict(value: Any) -> dict[str, Any]:
    """Serialize an artifact without losing enum values or nested records."""
    return _walk(value)


def validate_reconstruction(
    state: CampaignState,
    transitions: tuple[TransitionRecord, ...],
    existing_evidence: set[str],
) -> ReconstructionResult:
    diagnostics: list[ValidationDiagnostic] = []
    ids = [t.id for t in transitions]
    if len(ids) != len(set(ids)):
        diagnostics.append(ValidationDiagnostic("DUPLICATE_TRANSITION_ID", "transition IDs must be unique"))
    previous = state.current_state
    for transition in transitions:
        if transition.from_state != previous:
            diagnostics.append(ValidationDiagnostic("BROKEN_TRANSITION_CHAIN", f"{transition.id} starts at {transition.from_state!r}, expected {previous!r}"))
        previous = transition.to_state
        for evidence in transition.evidence:
            if evidence not in existing_evidence:
                diagnostics.append(ValidationDiagnostic("MISSING_EVIDENCE", f"referenced evidence {evidence!r} does not exist"))
    active_count = bool(state.active_responsibility) + len(state.additional_active_responsibilities)
    if active_count > 1:
        diagnostics.append(ValidationDiagnostic("MULTIPLE_ACTIVE_RESPONSIBILITIES", "campaign state must have at most one active responsibility"))
    if state.active_responsibility and state.active_responsibility.decision_blocked == "":
        diagnostics.append(ValidationDiagnostic("RESPONSIBILITY_MISSING_DECISION", "active responsibility must identify its blocked decision"))
    if state.status == "terminal" or state.terminal_state:
        if active_count:
            diagnostics.append(ValidationDiagnostic("TERMINAL_STATE_HAS_ACTIVE_RESPONSIBILITY", "terminal state cannot retain executable responsibility"))
    if state.active_responsibility and state.authority is None:
        diagnostics.append(ValidationDiagnostic("MISSING_AUTHORITY", "active responsibility requires an authority classification"))
    # A TASK dependency may legitimately point at any responsibility the state
    # still knows about: the active one, any additional active one, or a
    # deferred one. Only a dependency on an id the state cannot account for is
    # a defect.
    known_responsibility_ids: set[str] = set()
    if state.active_responsibility:
        known_responsibility_ids.add(state.active_responsibility.id)
    known_responsibility_ids.update(r.id for r in state.additional_active_responsibilities)
    known_responsibility_ids.update(d.responsibility_id for d in state.deferred_responsibilities)
    checked = [r for r in (state.active_responsibility, *state.additional_active_responsibilities) if r is not None]
    for responsibility in checked:
        for dependency in responsibility.dependencies:
            if dependency.type is DependencyType.TASK and dependency.requires not in known_responsibility_ids:
                diagnostics.append(ValidationDiagnostic("MISSING_TASK_DEPENDENCY", f"responsibility dependency {dependency.requires!r} does not exist"))
            if dependency.type is DependencyType.EVIDENCE and dependency.requires not in existing_evidence:
                diagnostics.append(ValidationDiagnostic("MISSING_EVIDENCE_DEPENDENCY", f"evidence dependency {dependency.requires!r} does not exist"))
    return ReconstructionResult(not diagnostics, tuple(diagnostics))


def validate_campaign_state(state: CampaignState) -> ReconstructionResult:
    """Validate state-local integrity without judging semantic warrant."""
    return validate_reconstruction(state, (), set())
