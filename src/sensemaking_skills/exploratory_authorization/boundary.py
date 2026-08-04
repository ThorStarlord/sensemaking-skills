"""Provider-boundary consumption of exploratory capabilities.

``consume_exploratory_capability`` is the single narrow point the executor
calls immediately before the provider call. It:

1. checks the capability type, registry liveness, and state (each state
   maps to exactly one failure code),
2. re-checks the policy validity window at consumption time,
3. atomically claims ISSUED -> CONSUMING (exactly one winner),
4. validates every binding field against the invocation context -- any
   drift burns the capability (CONSUMING -> DEAD) and raises its own code,
5. finalizes CONSUMED and returns the single-use grant.

``burn_exploratory_capability`` permanently kills a capability (any state
-> DEAD). The executor calls it when the provider call fails after
consumption, so a failed attempt never revives or re-issues anything.
"""

from __future__ import annotations

from typing import Any, Optional

from ..path_containment import canonicalize_path
from .failure_codes import (
    EXPLORATORY_BINDING_APPROVAL_DIGEST_MISMATCH,
    EXPLORATORY_BINDING_ARTIFACT_TYPE_MISMATCH,
    EXPLORATORY_BINDING_ATTEMPT_ID_MISMATCH,
    EXPLORATORY_BINDING_CAMPAIGN_ID_MISMATCH,
    EXPLORATORY_BINDING_CONFIGURATION_ID_MISMATCH,
    EXPLORATORY_BINDING_CONFIGURATION_SNAPSHOT_MISMATCH,
    EXPLORATORY_BINDING_FRAMEWORK_SHA_MISMATCH,
    EXPLORATORY_BINDING_LANE_MISMATCH,
    EXPLORATORY_BINDING_MODEL_MISMATCH,
    EXPLORATORY_BINDING_OUTPUT_PATH_MISMATCH,
    EXPLORATORY_BINDING_POLICY_DIGEST_MISMATCH,
    EXPLORATORY_BINDING_TARGET_REPOSITORY_MISMATCH,
    EXPLORATORY_BINDING_TARGET_SHA_MISMATCH,
    EXPLORATORY_CAPABILITY_ALREADY_CONSUMED,
    EXPLORATORY_CAPABILITY_CONCURRENT_CONSUMPTION,
    EXPLORATORY_CAPABILITY_CONSUMPTION_FAILED,
    EXPLORATORY_CAPABILITY_EXPIRED,
    EXPLORATORY_CAPABILITY_NOT_LIVE,
    EXPLORATORY_CAPABILITY_REQUIRED,
    EXPLORATORY_CAPABILITY_WRONG_TYPE,
    ExploratoryAuthorizationError,
)
from .issuer import EXPLORATORY_LANE, _as_datetime
from .models import (
    CapabilityBinding,
    ExploratoryConsumptionDecision,
    ExploratoryInvocationCapability,
    ExploratoryInvocationContext,
)
from .registry import CapabilityState


def _binding_mismatch(code: str, label: str, expected: Any, actual: Any) -> None:
    raise ExploratoryAuthorizationError(
        code,
        f"binding drift: {label} = {actual!r} but the capability is bound "
        f"to {expected!r}",
    )


def _validate_binding(binding: CapabilityBinding, context: ExploratoryInvocationContext) -> None:
    checks = (
        (EXPLORATORY_BINDING_MODEL_MISMATCH, "model", binding.intended_model, context.model),
        (EXPLORATORY_BINDING_TARGET_REPOSITORY_MISMATCH, "target_repository",
         binding.target_repository, context.target_repository),
        (EXPLORATORY_BINDING_TARGET_SHA_MISMATCH, "target_sha", binding.target_sha, context.target_sha),
        (EXPLORATORY_BINDING_FRAMEWORK_SHA_MISMATCH, "framework_sha", binding.framework_sha, context.framework_sha),
        (EXPLORATORY_BINDING_ARTIFACT_TYPE_MISMATCH, "artifact_type", binding.artifact_type, context.artifact_type),
        (EXPLORATORY_BINDING_CONFIGURATION_ID_MISMATCH, "configuration_id",
         binding.configuration_id, context.configuration_id),
        (EXPLORATORY_BINDING_CONFIGURATION_SNAPSHOT_MISMATCH, "configuration_snapshot_digest",
         binding.configuration_snapshot_digest, context.configuration_snapshot_digest),
        (EXPLORATORY_BINDING_CAMPAIGN_ID_MISMATCH, "campaign_id", binding.campaign_id, context.campaign_id),
        (EXPLORATORY_BINDING_POLICY_DIGEST_MISMATCH, "policy_digest", binding.policy_digest, context.policy_digest),
        (EXPLORATORY_BINDING_APPROVAL_DIGEST_MISMATCH, "approval_digest",
         binding.approval_digest, context.approval_digest),
        (EXPLORATORY_BINDING_ATTEMPT_ID_MISMATCH, "attempt_id", binding.attempt_id, context.attempt_id),
        (EXPLORATORY_BINDING_LANE_MISMATCH, "lane", binding.lane, context.lane),
    )
    for code, label, expected, actual in checks:
        if actual != expected:
            _binding_mismatch(code, label, expected, actual)
    if canonicalize_path(context.output_path) != canonicalize_path(binding.bound_output_path):
        _binding_mismatch(
            EXPLORATORY_BINDING_OUTPUT_PATH_MISMATCH,
            "output_path",
            binding.bound_output_path,
            context.output_path,
        )


def _state_failure(state: CapabilityState) -> str:
    if state is CapabilityState.CONSUMED:
        return EXPLORATORY_CAPABILITY_ALREADY_CONSUMED
    if state is CapabilityState.CONSUMING:
        return EXPLORATORY_CAPABILITY_CONCURRENT_CONSUMPTION
    return EXPLORATORY_CAPABILITY_CONSUMPTION_FAILED


def exploratory_capability_availability(capability: Any) -> Optional[str]:
    """Fail-fast pre-check: may this capability be consumed at all?

    Returns ``None`` when the capability may proceed to consumption, and the
    exact failure code otherwise. Deliberately non-consuming and
    non-destructive: the executor calls this in its early fail-fast layer so
    an obviously dead or wrong capability dies before any prompt is built,
    without burning anything (burning is reserved for the consumption path).
    """
    if capability is None:
        return EXPLORATORY_CAPABILITY_REQUIRED
    if not isinstance(capability, ExploratoryInvocationCapability):
        return EXPLORATORY_CAPABILITY_WRONG_TYPE
    registry = getattr(capability, "_registry", None)
    capability_id = getattr(capability, "_capability_id", None)
    if registry is None or capability_id is None:
        return EXPLORATORY_CAPABILITY_NOT_LIVE
    state = registry.state(capability_id)
    if state is None:
        return EXPLORATORY_CAPABILITY_NOT_LIVE
    if state is not CapabilityState.ISSUED:
        return _state_failure(state)
    return None


def consume_exploratory_capability(
    capability: Any,
    context: Any,
    *,
    now: Optional[str] = None,
    _before_complete: Optional[Any] = None,
) -> ExploratoryConsumptionDecision:
    """Atomically spend the capability for one provider invocation.

    ``_before_complete`` is a private test hook invoked inside the claimed
    critical section, before finalization; it lets tests prove that a
    second consumer sees CONSUMING. ``now`` is an injectable ISO-8601
    timestamp (defaults to the real clock).
    """
    if not isinstance(capability, ExploratoryInvocationCapability):
        raise ExploratoryAuthorizationError(
            EXPLORATORY_CAPABILITY_WRONG_TYPE,
            "an exploratory invocation requires an ExploratoryInvocationCapability",
        )
    registry = getattr(capability, "_registry", None)
    capability_id = getattr(capability, "_capability_id", None)
    if registry is None or capability_id is None:
        raise ExploratoryAuthorizationError(
            EXPLORATORY_CAPABILITY_NOT_LIVE,
            "the capability has no live issuance record",
        )

    state = registry.state(capability_id)
    if state is None:
        raise ExploratoryAuthorizationError(
            EXPLORATORY_CAPABILITY_NOT_LIVE,
            "the capability is not a live issuance of this registry",
        )
    if state is not CapabilityState.ISSUED:
        raise ExploratoryAuthorizationError(
            _state_failure(state),
            f"capability state is {state.value}; it cannot be consumed",
        )

    binding = capability.binding
    current = _as_datetime(now)
    try:
        not_before = _as_datetime(binding.valid_from)
        not_after = _as_datetime(binding.expires_at)
    except ValueError as exc:
        registry.burn(capability_id)
        raise ExploratoryAuthorizationError(
            EXPLORATORY_CAPABILITY_EXPIRED,
            f"capability validity window is malformed: {exc}",
        ) from exc
    if not (not_before <= current <= not_after):
        registry.burn(capability_id)
        raise ExploratoryAuthorizationError(
            EXPLORATORY_CAPABILITY_EXPIRED,
            f"consumption time {current.isoformat()} is outside the "
            f"capability validity window "
            f"[{not_before.isoformat()}, {not_after.isoformat()}]",
        )

    observed = registry.begin_consume(capability_id)
    if observed is not CapabilityState.CONSUMING:
        # Lost the claim: another thread holds CONSUMING, or the capability
        # is spent/dead. Never burn on the loser's path.
        raise ExploratoryAuthorizationError(
            _state_failure(observed),
            f"concurrent or spent capability (state {observed.value})",
        )

    try:
        _validate_binding(binding, context)
        if _before_complete is not None:
            _before_complete()
        registry.complete_consume(capability_id)
    except ExploratoryAuthorizationError:
        registry.fail_consume(capability_id)
        raise

    return ExploratoryConsumptionDecision(
        exact_model=binding.intended_model,
        output_path=binding.bound_output_path,
        attempt_id=binding.attempt_id,
        campaign_id=binding.campaign_id,
        configuration_id=binding.configuration_id,
        approval_digest=binding.approval_digest,
        lane=EXPLORATORY_LANE,
    )


def burn_exploratory_capability(capability: Any) -> None:
    """Permanently kill the capability (any state -> DEAD).

    Called by the executor when a provider call fails after consumption:
    the attempt is spent and can never be retried with this capability.
    """
    if not isinstance(capability, ExploratoryInvocationCapability):
        raise ExploratoryAuthorizationError(
            EXPLORATORY_CAPABILITY_WRONG_TYPE,
            "burn_exploratory_capability requires an "
            "ExploratoryInvocationCapability",
        )
    registry = getattr(capability, "_registry", None)
    capability_id = getattr(capability, "_capability_id", None)
    if registry is None or capability_id is None:
        return
    registry.burn(capability_id)
