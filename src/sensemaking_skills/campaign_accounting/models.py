"""Data structures and state transitions for Phase 4 campaign accounting (#120).

Defines the attempt lifecycle states, immutable data models, and transition validation
in compliance with ADR 0023 and two-lane schemas v1.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set

from .failure_codes import (
    ATTEMPT_ALREADY_TERMINAL,
    ATTEMPT_STATE_INVALID_TRANSITION,
    CampaignAccountingError,
)

EXPLORATORY_CLASSIFICATION = "EXPLORATORY_NOT_CANONICAL_EVIDENCE"


class AttemptState(str, Enum):
    RESERVED = "RESERVED"
    ABORTED_BEFORE_INVOCATION = "ABORTED_BEFORE_INVOCATION"
    INVOKED = "INVOKED"
    PROVIDER_FAILED = "PROVIDER_FAILED"
    OUTPUT_CAPTURED = "OUTPUT_CAPTURED"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    VALIDATION_PASSED = "VALIDATION_PASSED"


TERMINAL_STATES: Set[str] = {
    AttemptState.ABORTED_BEFORE_INVOCATION.value,
    AttemptState.PROVIDER_FAILED.value,
    AttemptState.VALIDATION_FAILED.value,
    AttemptState.VALIDATION_PASSED.value,
}

LEGAL_TRANSITIONS: Dict[str, Set[str]] = {
    AttemptState.RESERVED.value: {
        AttemptState.ABORTED_BEFORE_INVOCATION.value,
        AttemptState.INVOKED.value,
    },
    AttemptState.INVOKED.value: {
        AttemptState.PROVIDER_FAILED.value,
        AttemptState.OUTPUT_CAPTURED.value,
    },
    AttemptState.OUTPUT_CAPTURED.value: {
        AttemptState.VALIDATION_FAILED.value,
        AttemptState.VALIDATION_PASSED.value,
    },
}


def validate_state_transition(current_state: str, new_state: str) -> None:
    """Validate that current_state -> new_state transition is legal."""
    if current_state in TERMINAL_STATES:
        raise CampaignAccountingError(
            ATTEMPT_ALREADY_TERMINAL,
            f"Attempt is already in terminal state '{current_state}' and cannot transition to '{new_state}'",
        )
    allowed = LEGAL_TRANSITIONS.get(current_state, set())
    if new_state not in allowed:
        raise CampaignAccountingError(
            ATTEMPT_STATE_INVALID_TRANSITION,
            f"Illegal state transition from '{current_state}' to '{new_state}'",
        )


@dataclass(frozen=True)
class StateHistoryEntry:
    state: str
    at: str


@dataclass(frozen=True)
class AttemptReservation:
    """The durable, on-disk attempt reservation created before provider entry.

    Not publicly constructible: instances are produced ONLY by
    ``DurableReservationManager.reserve_attempt``, which stamps a
    per-process sentinel via ``_create_attempt_reservation``. A plain
    ``AttemptReservation(...)`` call, a ``dataclasses.replace`` copy, or a
    hand-built ``object.__new__`` reconstruction lacks that sentinel and
    fails ``is_genuine_attempt_reservation`` -- the provider boundary must
    never accept a reservation-shaped object as authority.
    """

    reservation_id: str
    attempt_id: str
    campaign_id: str
    configuration_id: str
    reserved_at: str
    state: str = AttemptState.RESERVED.value
    state_history: List[Dict[str, str]] = field(default_factory=list)
    reservation_schema_version: str = "1"
    terminal_states: List[str] = field(
        default_factory=lambda: [
            AttemptState.ABORTED_BEFORE_INVOCATION.value,
            AttemptState.PROVIDER_FAILED.value,
            AttemptState.VALIDATION_FAILED.value,
            AttemptState.VALIDATION_PASSED.value,
        ]
    )

    def __post_init__(self) -> None:
        _forbid_public_construction(self, "AttemptReservation")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "reservation_schema_version": self.reservation_schema_version,
            "reservation_id": self.reservation_id,
            "attempt_id": self.attempt_id,
            "campaign_id": self.campaign_id,
            "configuration_id": self.configuration_id,
            "reserved_at": self.reserved_at,
            "state": self.state,
            "state_history": self.state_history,
            "terminal_states": self.terminal_states,
        }


def _forbid_public_construction(instance: object, class_name: str) -> None:
    raise TypeError(
        f"{class_name} cannot be constructed directly. It is produced only "
        "by the campaign accounting runtime (reserve_attempt)."
    )


def _seal_reservation_dataclass(cls: type) -> tuple:
    """Return ``(create, is_genuine)`` for ``AttemptReservation``.

    Mirrors the Phase 2 validator-owned provenance pattern
    (``campaign_validation.models``): ``create`` bypasses ``__init__``
    entirely via ``object.__new__`` and stamps a closure-held sentinel;
    ``is_genuine`` checks that sentinel by identity. A reservation obtained
    any other way fails the check.

    Because ``__init__`` is bypassed, ``create`` also applies every declared
    dataclass field: explicit kwargs first, then the field's default or
    ``default_factory`` (matching what the public constructor would have
    produced), and it rejects missing required fields.
    """
    import dataclasses as _dc

    seal = object()
    field_defs = _dc.fields(cls)

    def create(**kwargs: Any) -> Any:
        obj = object.__new__(cls)
        for f in field_defs:
            if f.name in kwargs:
                value = kwargs[f.name]
            elif f.default is not _dc.MISSING:
                value = f.default
            elif f.default_factory is not _dc.MISSING:  # type: ignore[misc]
                value = f.default_factory()  # type: ignore[misc]
            else:
                raise TypeError(
                    f"{cls.__name__} requires field {f.name!r} but it was "
                    "not supplied to the sealed factory"
                )
            object.__setattr__(obj, f.name, value)
        object.__setattr__(obj, "_provenance_seal", seal)
        return obj

    def is_genuine(obj: Any) -> bool:
        return isinstance(obj, cls) and getattr(obj, "_provenance_seal", None) is seal

    return create, is_genuine


_create_attempt_reservation, _is_genuine_attempt_reservation = _seal_reservation_dataclass(
    AttemptReservation
)


def is_genuine_attempt_reservation(obj: Any) -> bool:
    """True iff ``obj`` is a reservation produced by ``reserve_attempt``."""
    return _is_genuine_attempt_reservation(obj)


@dataclass(frozen=True)
class LedgerEvent:
    sequence: int
    timestamp: str
    campaign_id: str
    attempt_id: str
    event_type: str
    payload: Dict[str, Any]
    previous_event_hash: str
    event_hash: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sequence": self.sequence,
            "timestamp": self.timestamp,
            "campaign_id": self.campaign_id,
            "attempt_id": self.attempt_id,
            "event_type": self.event_type,
            "payload": self.payload,
            "previous_event_hash": self.previous_event_hash,
            "event_hash": self.event_hash,
        }


@dataclass(frozen=True)
class AttemptResult:
    attempt_id: str
    campaign_id: str
    configuration_id: str
    state: str
    state_history: List[Dict[str, str]]
    provider_invoked_at: Optional[str]
    raw_output_reference: Optional[str]
    validated_output_reference: Optional[str]
    validation_outcome: Optional[Dict[str, Any]]
    tokens_observed: Optional[int] = None
    cost_observed: Optional[Dict[str, Any]] = None
    terminal_at: Optional[str] = None
    classification: str = EXPLORATORY_CLASSIFICATION
    result_schema_version: str = "1"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "result_schema_version": self.result_schema_version,
            "attempt_id": self.attempt_id,
            "campaign_id": self.campaign_id,
            "configuration_id": self.configuration_id,
            "state": self.state,
            "state_history": self.state_history,
            "provider_invoked_at": self.provider_invoked_at,
            "raw_output_reference": self.raw_output_reference,
            "validated_output_reference": self.validated_output_reference,
            "validation_outcome": self.validation_outcome,
            "classification": self.classification,
            "tokens_observed": self.tokens_observed,
            "cost_observed": self.cost_observed,
            "terminal_at": self.terminal_at,
        }


@dataclass(frozen=True)
class ProviderResponse:
    """The raw provider response plus post-hoc usage observations.

    Pure data, publicly constructible. ``raw_output`` is the exact bytes
    the durable recorder preserves verbatim. ``tokens_observed`` and
    ``cost_observed`` are post-hoc measurements (ADR 0023 §14), never
    pre-call guarantees.
    """

    raw_output: bytes
    tokens_observed: Optional[int] = None
    cost_observed: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class ValidationOutcome:
    """The result of validating a preserved raw provider response.

    Pure data, publicly constructible: the caller's validator produces it
    from the raw bytes. ``artifact_content`` is the extracted candidate
    artifact to preserve beside the raw output (None when validation could
    not extract one). ``tokens_observed``/``cost_observed`` are post-hoc
    measurements (ADR 0023 §14), never pre-call guarantees.
    """

    passed: bool
    details: Any
    artifact_content: Optional[str] = None
    artifact_filename: str = "produced-artifact.md"
    validated_output_ref: Optional[str] = None
    tokens_observed: Optional[int] = None
    cost_observed: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class CampaignSummary:
    campaign_id: str
    policy_digest: str
    campaign_state: str
    campaign_state_history: List[Dict[str, str]]
    reservations_issued: Dict[str, Any]
    provider_invocations_made: int
    remaining_budget: Dict[str, Any]
    attempts: List[Dict[str, Any]]
    last_activity_at: str
    first_reserved_at: Optional[str] = None
    terminal_reason: Optional[str] = None
    summary_schema_version: str = "1"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary_schema_version": self.summary_schema_version,
            "campaign_id": self.campaign_id,
            "policy_digest": self.policy_digest,
            "campaign_state": self.campaign_state,
            "campaign_state_history": self.campaign_state_history,
            "reservations_issued": self.reservations_issued,
            "provider_invocations_made": self.provider_invocations_made,
            "remaining_budget": self.remaining_budget,
            "attempts": self.attempts,
            "first_reserved_at": self.first_reserved_at,
            "last_activity_at": self.last_activity_at,
            "terminal_reason": self.terminal_reason,
        }
