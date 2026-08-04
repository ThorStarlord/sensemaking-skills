"""Exploratory authorization failure codes (Phase 3, issue #119).
Every rejection path in the exploratory lane maps to exactly one stable
code. Codes are plain string constants so they survive serialization,
comparison, and log greps. Names follow the shape
``EXPLORATORY_<SCOPE>_<REASON>``:

- ``EXPLORATORY_MINT_*`` -- issuer-side rejections (bad or non-genuine
  inputs, policy violations, duplicate attempt ids).
- ``EXPLORATORY_BINDING_*_MISMATCH`` -- consumption-side binding drift:
  the invocation facts differ from what the capability was minted for.
- ``EXPLORATORY_CAPABILITY_*`` -- capability-object and registry-state
  failures (immutability, copies, liveness, concurrency, spend).
- ``EXPLORATORY_PROVENANCE_*`` -- approval-provenance verifier failures.

The provider-boundary dispatcher additionally surfaces
``EXPLORATORY_CAPABILITY_REQUIRED`` when an EXPLORATORY invocation reaches
the executor without any capability.
"""

from __future__ import annotations


class ExploratoryAuthorizationError(Exception):
    """Raised on every exploratory-authorization rejection.

    Carries a stable ``failure_code``; ``str(exc)`` renders
    ``"<code>: <detail>"`` so the code survives logging.
    """

    def __init__(self, failure_code: str, detail: str) -> None:
        super().__init__(f"{failure_code}: {detail}")
        self.failure_code = failure_code
        self.detail = detail

# -- Issuer (mint) ----------------------------------------------------------

#: The bundle is not a genuine validator-produced ValidatedCampaignBundle.
EXPLORATORY_MINT_REQUIRES_GENUINE_BUNDLE = "EXPLORATORY_MINT_REQUIRES_GENUINE_BUNDLE"
#: Defense-in-depth: approval is template-shaped (marker) or otherwise
#: inoperative. Unreachable through the Phase 2 pipeline, which rejects
#: these documents first; kept because the issuer is the security boundary.
EXPLORATORY_MINT_REQUIRES_OPERATIVE_APPROVAL = "EXPLORATORY_MINT_REQUIRES_OPERATIVE_APPROVAL"
#: Defense-in-depth: approval carries no provenance mechanism.
EXPLORATORY_MINT_REQUIRES_APPROVAL_PROVENANCE = "EXPLORATORY_MINT_REQUIRES_APPROVAL_PROVENANCE"
#: Defense-in-depth: approval provenance carries no reference.
EXPLORATORY_MINT_REQUIRES_APPROVAL_PROVENANCE_REFERENCE = (
    "EXPLORATORY_MINT_REQUIRES_APPROVAL_PROVENANCE_REFERENCE"
)
#: Defense-in-depth: approval carries no explicit statement.
EXPLORATORY_MINT_REQUIRES_APPROVAL_STATEMENT = "EXPLORATORY_MINT_REQUIRES_APPROVAL_STATEMENT"
#: The policy validity window does not contain the mint time.
EXPLORATORY_MINT_POLICY_EXPIRED = "EXPLORATORY_MINT_POLICY_EXPIRED"
#: The request names a different campaign than the validated documents.
EXPLORATORY_MINT_CAMPAIGN_ID_MISMATCH = "EXPLORATORY_MINT_CAMPAIGN_ID_MISMATCH"
#: The request names a configuration the bundle did not validate.
EXPLORATORY_MINT_CONFIGURATION_ID_MISMATCH = "EXPLORATORY_MINT_CONFIGURATION_ID_MISMATCH"
#: Defense-in-depth: the validated configuration is not a member of the
#: policy's allowed_configuration_ids (unreachable through valid bundles;
#: Phase 2 already enforces membership).
EXPLORATORY_MINT_CONFIGURATION_NOT_ALLOWED = "EXPLORATORY_MINT_CONFIGURATION_NOT_ALLOWED"
#: The requested model is not in the policy's allowed_models.
EXPLORATORY_MINT_MODEL_NOT_ALLOWED = "EXPLORATORY_MINT_MODEL_NOT_ALLOWED"
#: The requested framework sha is not in the policy's allowed_framework_shas.
EXPLORATORY_MINT_FRAMEWORK_SHA_NOT_ALLOWED = "EXPLORATORY_MINT_FRAMEWORK_SHA_NOT_ALLOWED"
#: The requested target (repository/sha pair) is not in the policy's
#: allowed_targets.
EXPLORATORY_MINT_TARGET_NOT_ALLOWED = "EXPLORATORY_MINT_TARGET_NOT_ALLOWED"
#: The requested artifact type is not in the policy's allowed_artifact_types.
EXPLORATORY_MINT_ARTIFACT_TYPE_NOT_ALLOWED = "EXPLORATORY_MINT_ARTIFACT_TYPE_NOT_ALLOWED"
#: The attempt id is not a strict lowercase UUID.
EXPLORATORY_MINT_REQUIRES_ATTEMPT_ID_UUID = "EXPLORATORY_MINT_REQUIRES_ATTEMPT_ID_UUID"
#: The attempt id was already issued in this process.
EXPLORATORY_MINT_DUPLICATE_ATTEMPT_ID = "EXPLORATORY_MINT_DUPLICATE_ATTEMPT_ID"

# -- Provenance verifier ----------------------------------------------------

#: No verifier was supplied; the issuer fails closed.
EXPLORATORY_PROVENANCE_VERIFIER_REJECTED = "EXPLORATORY_PROVENANCE_VERIFIER_REJECTED"
#: The verifier raised, or returned provenance that contradicts the
#: validated approval document.
EXPLORATORY_PROVENANCE_VERIFIER_FAILED = "EXPLORATORY_PROVENANCE_VERIFIER_FAILED"

# -- Capability object / registry -------------------------------------------

#: Attribute assignment/deletion on a capability is prohibited.
EXPLORATORY_CAPABILITY_IMMUTABLE = "EXPLORATORY_CAPABILITY_IMMUTABLE"
#: Copies, deepcopies, and subclasses are prohibited.
EXPLORATORY_CAPABILITY_COPY_PROHIBITED = "EXPLORATORY_CAPABILITY_COPY_PROHIBITED"
#: Serialization (pickle) is prohibited.
EXPLORATORY_CAPABILITY_SERIALIZATION_PROHIBITED = (
    "EXPLORATORY_CAPABILITY_SERIALIZATION_PROHIBITED"
)
#: The capability is not a live issuance of this process's registry.
EXPLORATORY_CAPABILITY_NOT_LIVE = "EXPLORATORY_CAPABILITY_NOT_LIVE"
#: The capability object has the wrong type entirely.
EXPLORATORY_CAPABILITY_WRONG_TYPE = "EXPLORATORY_CAPABILITY_WRONG_TYPE"
#: Consumption raced another consumption in progress.
EXPLORATORY_CAPABILITY_CONCURRENT_CONSUMPTION = (
    "EXPLORATORY_CAPABILITY_CONCURRENT_CONSUMPTION"
)
#: The capability was already consumed.
EXPLORATORY_CAPABILITY_ALREADY_CONSUMED = "EXPLORATORY_CAPABILITY_ALREADY_CONSUMED"
#: The capability is dead (burned): permanently unusable.
EXPLORATORY_CAPABILITY_CONSUMPTION_FAILED = "EXPLORATORY_CAPABILITY_CONSUMPTION_FAILED"
#: The policy validity window did not contain the consumption time.
EXPLORATORY_CAPABILITY_EXPIRED = "EXPLORATORY_CAPABILITY_EXPIRED"

# -- Provider-boundary dispatcher -------------------------------------------

#: An EXPLORATORY invocation reached the executor without a capability.
EXPLORATORY_CAPABILITY_REQUIRED = "EXPLORATORY_CAPABILITY_REQUIRED"

# -- Consumption binding drift (one code per category) ----------------------

EXPLORATORY_BINDING_MODEL_MISMATCH = "EXPLORATORY_BINDING_MODEL_MISMATCH"
EXPLORATORY_BINDING_TARGET_REPOSITORY_MISMATCH = (
    "EXPLORATORY_BINDING_TARGET_REPOSITORY_MISMATCH"
)
EXPLORATORY_BINDING_TARGET_SHA_MISMATCH = "EXPLORATORY_BINDING_TARGET_SHA_MISMATCH"
EXPLORATORY_BINDING_FRAMEWORK_SHA_MISMATCH = "EXPLORATORY_BINDING_FRAMEWORK_SHA_MISMATCH"
EXPLORATORY_BINDING_ARTIFACT_TYPE_MISMATCH = "EXPLORATORY_BINDING_ARTIFACT_TYPE_MISMATCH"
EXPLORATORY_BINDING_CONFIGURATION_ID_MISMATCH = (
    "EXPLORATORY_BINDING_CONFIGURATION_ID_MISMATCH"
)
EXPLORATORY_BINDING_CONFIGURATION_SNAPSHOT_MISMATCH = (
    "EXPLORATORY_BINDING_CONFIGURATION_SNAPSHOT_MISMATCH"
)
EXPLORATORY_BINDING_CAMPAIGN_ID_MISMATCH = "EXPLORATORY_BINDING_CAMPAIGN_ID_MISMATCH"
EXPLORATORY_BINDING_POLICY_DIGEST_MISMATCH = "EXPLORATORY_BINDING_POLICY_DIGEST_MISMATCH"
EXPLORATORY_BINDING_APPROVAL_DIGEST_MISMATCH = (
    "EXPLORATORY_BINDING_APPROVAL_DIGEST_MISMATCH"
)
EXPLORATORY_BINDING_ATTEMPT_ID_MISMATCH = "EXPLORATORY_BINDING_ATTEMPT_ID_MISMATCH"
EXPLORATORY_BINDING_LANE_MISMATCH = "EXPLORATORY_BINDING_LANE_MISMATCH"
EXPLORATORY_BINDING_OUTPUT_PATH_MISMATCH = "EXPLORATORY_BINDING_OUTPUT_PATH_MISMATCH"
