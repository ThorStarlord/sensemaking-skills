"""Exploratory authorization data models (Phase 3, issue #119).

``ExploratoryInvocationCapability`` is the ONLY authoritative object in
this package: it is deeply immutable, non-copyable, non-serializable,
non-subclassable, and publicly non-constructible. Its authority is
delegated to the process-local issuer registry: ``live`` and ``consumed``
are asked of the registry, never of the object's own attributes, so a
forged reconstruction is not live and cannot be consumed.

Publicly constructible models (``ExploratoryAttemptRequest``,
``ExploratoryInvocationContext``, ``VerifiedApprovalProvenance``) are pure
data, deliberately: callers (the fixtures, the executor's boundary layer)
must be able to build them; they carry no authority.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Mapping, Optional

from .failure_codes import (
    EXPLORATORY_CAPABILITY_COPY_PROHIBITED,
    EXPLORATORY_CAPABILITY_IMMUTABLE,
    EXPLORATORY_CAPABILITY_SERIALIZATION_PROHIBITED,
)


@dataclass(frozen=True)
class ExploratoryAttemptRequest:
    """Immutable, well-formed request to mint an exploratory capability.

    Pure data, publicly constructible. ``attempt_id`` MUST be a strict
    lowercase UUID (enforced at mint).
    """

    attempt_id: str
    campaign_id: str
    configuration_id: str
    intended_model: str
    framework_sha: str
    target_repository: str
    target_sha: str
    artifact_type: str
    output_path: str
    executor_id: str


@dataclass(frozen=True)
class VerifiedApprovalProvenance:
    """What an ``ApprovalProvenanceVerifier`` confirmed about the approval.

    Publicly constructible so verifiers (including test doubles) can return
    it; the issuer cross-checks it against the validated approval document.
    """

    mechanism: str
    reference: str


@dataclass(frozen=True)
class ExploratoryInvocationContext:
    """Invocation facts gathered at the provider boundary, from the CALL.

    Built by the executor's boundary layer from the actual invocation
    (identity, declared exploratory values, derived lane, resolved output
    path) -- never from executor attributes or the capability itself.
    """

    model: str
    target_repository: str
    target_sha: str
    framework_sha: str
    artifact_type: str
    output_path: str
    campaign_id: str
    configuration_id: str
    configuration_snapshot_digest: str
    policy_digest: str
    approval_digest: str
    attempt_id: str
    lane: str


@dataclass(frozen=True)
class CapabilityBinding:
    """Everything the capability is bound to at mint time."""

    campaign_id: str
    configuration_id: str
    intended_model: str
    framework_sha: str
    target_repository: str
    target_sha: str
    artifact_type: str
    policy_digest: str
    approval_digest: str
    configuration_snapshot_digest: str
    attempt_id: str
    bound_output_path: str
    executor_id: str
    provenance_mechanism: str
    provenance_reference: str
    valid_from: str
    expires_at: str
    lane: str


@dataclass(frozen=True)
class ExploratoryConsumptionDecision:
    """The single-use grant produced by a successful consumption."""

    exact_model: str
    output_path: str
    attempt_id: str
    campaign_id: str
    configuration_id: str
    approval_digest: str
    lane: str


def _seal_capability(cls: type) -> tuple:
    """Return ``(create, is_genuine)`` for the capability class.

    ``create`` stamps a closure-held sentinel via ``object.__setattr__``
    (bypassing the overridden ``__setattr__``); ``is_genuine`` checks that
    sentinel by identity. A capability obtained any other way (public
    construction, ``object.__new__`` plus guessed attributes) lacks the
    sentinel and is not genuine -- though liveness is additionally decided
    by the issuer registry, so a forged object is doubly dead.
    """
    seal = object()

    def create(**kwargs: Any) -> Any:
        obj = object.__new__(cls)
        object.__setattr__(obj, "_seal", seal)
        for name, value in kwargs.items():
            object.__setattr__(obj, name, value)
        return obj

    def is_genuine(obj: Any) -> bool:
        return getattr(obj, "_seal", None) is seal

    return create, is_genuine


class ExploratoryInvocationCapability:
    """Sealed, immutable, single-use authorization for one exploratory
    provider invocation. Created ONLY by the issuer; authority delegated to
    the issuer registry."""

    _seal: object
    _capability_id: str
    _binding: CapabilityBinding
    _registry: object

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        raise TypeError(
            f"{EXPLORATORY_CAPABILITY_IMMUTABLE}: capabilities are created "
            "only by the issuer, never constructed by callers"
        )

    def __init_subclass__(cls, **kwargs: Any) -> None:
        raise TypeError(
            f"{EXPLORATORY_CAPABILITY_COPY_PROHIBITED}: subclassing a "
            "capability is forbidden"
        )

    def __setattr__(self, name: str, value: Any) -> None:
        raise TypeError(
            f"{EXPLORATORY_CAPABILITY_IMMUTABLE}: a capability is immutable"
        )

    def __delattr__(self, name: str) -> None:
        raise TypeError(
            f"{EXPLORATORY_CAPABILITY_IMMUTABLE}: a capability is immutable"
        )

    def __copy__(self) -> "ExploratoryInvocationCapability":
        raise TypeError(
            f"{EXPLORATORY_CAPABILITY_COPY_PROHIBITED}: a capability cannot "
            "be copied"
        )

    def __deepcopy__(self, memo: Any) -> "ExploratoryInvocationCapability":
        raise TypeError(
            f"{EXPLORATORY_CAPABILITY_COPY_PROHIBITED}: a capability cannot "
            "be deep-copied"
        )

    def __reduce_ex__(self, protocol: int) -> Any:
        raise TypeError(
            f"{EXPLORATORY_CAPABILITY_SERIALIZATION_PROHIBITED}: a capability "
            "cannot be serialized"
        )

    @property
    def binding(self) -> CapabilityBinding:
        return self._binding

    @property
    def attempt_id(self) -> str:
        return self._binding.attempt_id

    @property
    def campaign_id(self) -> str:
        return self._binding.campaign_id

    @property
    def configuration_id(self) -> str:
        return self._binding.configuration_id

    @property
    def expires_at(self) -> str:
        return self._binding.expires_at

    @property
    def live(self) -> bool:
        registry = getattr(self, "_registry", None)
        capability_id = getattr(self, "_capability_id", None)
        if registry is None or capability_id is None:
            return False
        return registry.is_live(capability_id)

    @property
    def consumed(self) -> bool:
        registry = getattr(self, "_registry", None)
        capability_id = getattr(self, "_capability_id", None)
        if registry is None or capability_id is None:
            return False
        return registry.is_spent(capability_id)


_create_capability, _is_genuine_capability = _seal_capability(
    ExploratoryInvocationCapability
)
