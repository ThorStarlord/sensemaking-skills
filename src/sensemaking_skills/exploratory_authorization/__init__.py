"""Exploratory authorization for the two-lane v1 program (Phase 3, #119).

Public API:

* ``mint_exploratory_capability(bundle, request, *, verifier=None, now=None)``
  -- turn a genuine Phase 2 ``ValidatedCampaignBundle`` plus a well-formed
  ``ExploratoryAttemptRequest`` into a live, single-use capability.
* ``consume_exploratory_capability(capability, context, *, now=None)`` --
  the provider-boundary spend: atomic, exactly-once, binding-verified.
* ``burn_exploratory_capability(capability)`` -- permanent kill (provider
  failure after consumption).
* ``ExploratoryAuthorizationError`` -- the single rejection exception, with
  a stable ``failure_code``.
* ``reset_exploratory_registry()`` -- test-only registry reset.

Every failure code is a stable string constant (see ``failure_codes``).
The capability object is immutable, non-copyable, non-serializable, and
publicly non-constructible; the process-local registry is the only
liveness authority.
"""

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
    EXPLORATORY_CAPABILITY_COPY_PROHIBITED,
    EXPLORATORY_CAPABILITY_EXPIRED,
    EXPLORATORY_CAPABILITY_IMMUTABLE,
    EXPLORATORY_CAPABILITY_NOT_LIVE,
    EXPLORATORY_CAPABILITY_REQUIRED,
    EXPLORATORY_CAPABILITY_SERIALIZATION_PROHIBITED,
    EXPLORATORY_CAPABILITY_WRONG_TYPE,
    EXPLORATORY_MINT_ARTIFACT_TYPE_NOT_ALLOWED,
    EXPLORATORY_MINT_CAMPAIGN_ID_MISMATCH,
    EXPLORATORY_MINT_CONFIGURATION_ID_MISMATCH,
    EXPLORATORY_MINT_CONFIGURATION_NOT_ALLOWED,
    EXPLORATORY_MINT_DUPLICATE_ATTEMPT_ID,
    EXPLORATORY_MINT_FRAMEWORK_SHA_NOT_ALLOWED,
    EXPLORATORY_MINT_MODEL_NOT_ALLOWED,
    EXPLORATORY_MINT_POLICY_EXPIRED,
    EXPLORATORY_MINT_REQUIRES_APPROVAL_PROVENANCE,
    EXPLORATORY_MINT_REQUIRES_APPROVAL_PROVENANCE_REFERENCE,
    EXPLORATORY_MINT_REQUIRES_APPROVAL_STATEMENT,
    EXPLORATORY_MINT_REQUIRES_ATTEMPT_ID_UUID,
    EXPLORATORY_MINT_REQUIRES_GENUINE_BUNDLE,
    EXPLORATORY_MINT_REQUIRES_OPERATIVE_APPROVAL,
    EXPLORATORY_MINT_TARGET_NOT_ALLOWED,
    EXPLORATORY_PROVENANCE_VERIFIER_FAILED,
    EXPLORATORY_PROVENANCE_VERIFIER_REJECTED,
    ExploratoryAuthorizationError,
)
from .boundary import (
    burn_exploratory_capability,
    consume_exploratory_capability,
    exploratory_capability_availability,
)
from .issuer import EXPLORATORY_LANE, mint_exploratory_capability
from .models import (
    ExploratoryConsumptionDecision,
    ExploratoryInvocationCapability,
    ExploratoryInvocationContext,
)
from .registry import (
    ExploratoryCapabilityRegistry,
    get_exploratory_registry,
    reset_exploratory_registry,
)

__all__ = [
    "EXPLORATORY_LANE",
    "ExploratoryAuthorizationError",
    "ExploratoryConsumptionDecision",
    "ExploratoryInvocationCapability",
    "ExploratoryInvocationContext",
    "burn_exploratory_capability",
    "consume_exploratory_capability",
    "exploratory_capability_availability",
    "mint_exploratory_capability",
    "reset_exploratory_registry",
    "get_exploratory_registry",
    "ExploratoryCapabilityRegistry",
]
