"""Exploratory capability issuer (Phase 3, issue #119).

``mint_exploratory_capability`` is the single entry point that turns a
genuine Phase 2 ``ValidatedCampaignBundle`` plus a well-formed
``ExploratoryAttemptRequest`` into a live capability. All trust-relevant
values are recomputed or verified here -- snapshot digests, policy
allowlists, validity window, approval provenance -- and the capability is
registered in the process-local issuer registry.

The minting checks run in a fixed precedence order so every rejection maps
to exactly one stable failure code.
"""

from __future__ import annotations

import datetime
import hashlib
import os
import uuid
from typing import Any, Mapping, Optional

from ..campaign_validation import is_genuine_campaign_bundle
from .digests import (
    compute_approval_snapshot_digest,
    compute_configuration_snapshot_digest,
)
from .failure_codes import (
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
from .models import (
    CapabilityBinding,
    ExploratoryAttemptRequest,
    _create_capability,
)
from .provenance import ProvenanceVerificationError
from .registry import _registry

EXPLORATORY_LANE = "EXPLORATORY"


def _as_datetime(value: Optional[str]) -> datetime.datetime:
    if value is None:
        return datetime.datetime.now(datetime.timezone.utc)
    parsed = datetime.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError(f"naive timestamp not allowed: {value!r}")
    return parsed


def _require_str(value: Any, label: str) -> str:
    text = str(value or "")
    if not text.strip():
        raise ExploratoryAuthorizationError(
            EXPLORATORY_MINT_REQUIRES_OPERATIVE_APPROVAL,
            f"approval document carries no {label}",
        )
    return text


def _require_operative_approval(raw: Mapping[str, Any]) -> None:
    """Defense-in-depth operationality checks (unreachable through the
    Phase 2 pipeline, which already rejects these documents -- the issuer
    is the security boundary and must not trust the validator profile
    alone)."""
    if "marker" in raw:
        raise ExploratoryAuthorizationError(
            EXPLORATORY_MINT_REQUIRES_OPERATIVE_APPROVAL,
            f"approval carries marker {raw.get('marker')!r} and can never "
            "be operative",
        )
    provenance = raw.get("approval_provenance") or {}
    mechanism = _require_str(
        provenance.get("mechanism", ""), "approval_provenance.mechanism"
    )
    if mechanism.strip().lower() == "none":
        raise ExploratoryAuthorizationError(
            EXPLORATORY_MINT_REQUIRES_APPROVAL_PROVENANCE,
            "approval_provenance.mechanism is 'none' (template approval)",
        )
    reference = _require_str(
        provenance.get("reference", ""), "approval_provenance.reference"
    )
    if not str(reference or "").strip():
        raise ExploratoryAuthorizationError(
            EXPLORATORY_MINT_REQUIRES_APPROVAL_PROVENANCE_REFERENCE,
            "approval_provenance.reference is empty",
        )
    statement = str(raw.get("approval_statement", "") or "").strip()
    if not statement:
        raise ExploratoryAuthorizationError(
            EXPLORATORY_MINT_REQUIRES_APPROVAL_STATEMENT,
            "approval_statement is empty",
        )


def _check_policy_window(policy_raw: Mapping[str, Any], now: datetime.datetime) -> None:
    window = policy_raw.get("validity_window") or {}
    try:
        not_before = _as_datetime(str(window.get("not_before", "")))
        not_after = _as_datetime(str(window.get("not_after", "")))
    except ValueError as exc:
        raise ExploratoryAuthorizationError(
            EXPLORATORY_MINT_POLICY_EXPIRED,
            f"policy validity_window is malformed: {exc}",
        ) from exc
    if not (not_before <= now <= not_after):
        raise ExploratoryAuthorizationError(
            EXPLORATORY_MINT_POLICY_EXPIRED,
            f"current time {now.isoformat()} is outside policy validity "
            f"window [{not_before.isoformat()}, {not_after.isoformat()}]",
        )


def _strict_uuid(attempt_id: str) -> bool:
    try:
        parsed = uuid.UUID(attempt_id)
    except (ValueError, AttributeError, TypeError):
        return False
    return str(parsed) == attempt_id


def mint_exploratory_capability(
    bundle: Any,
    request: ExploratoryAttemptRequest,
    *,
    verifier: Optional[Any] = None,
    now: Optional[str] = None,
) -> Any:
    """Mint a live, single-use exploratory capability from a genuine
    validated bundle plus a well-formed attempt request.

    ``verifier`` is required and fails closed when absent. ``now`` is an
    injectable ISO-8601 timestamp for deterministic tests; it defaults to
    the real clock.
    """
    if not is_genuine_campaign_bundle(bundle):
        raise ExploratoryAuthorizationError(
            EXPLORATORY_MINT_REQUIRES_GENUINE_BUNDLE,
            "the bundle is not a genuine validator-produced "
            "ValidatedCampaignBundle (it may be a reconstruction or a "
            "foreign object)",
        )

    # -- approval provenance corroboration -----------------------------------
    if verifier is None:
        raise ExploratoryAuthorizationError(
            EXPLORATORY_PROVENANCE_VERIFIER_REJECTED,
            "no approval-provenance verifier was supplied; refusing to "
            "self-attest consent (fail closed)",
        )
    try:
        verified = verifier.verify(bundle.approval)
    except ProvenanceVerificationError as exc:
        raise ExploratoryAuthorizationError(
            EXPLORATORY_PROVENANCE_VERIFIER_FAILED,
            f"approval-provenance verifier refused to corroborate: {exc}",
        ) from exc
    except Exception as exc:  # noqa: BLE001 - any verifier failure fails closed
        raise ExploratoryAuthorizationError(
            EXPLORATORY_PROVENANCE_VERIFIER_FAILED,
            f"approval-provenance verifier failed: {exc}",
        ) from exc
    provenance = bundle.approval.raw.get("approval_provenance") or {}
    if (
        getattr(verified, "mechanism", None) != provenance.get("mechanism")
        or getattr(verified, "reference", None) != provenance.get("reference")
    ):
        raise ExploratoryAuthorizationError(
            EXPLORATORY_PROVENANCE_VERIFIER_FAILED,
            "verifier result contradicts the validated approval provenance",
        )

    # -- approval operationality (defense-in-depth) --------------------------
    _require_operative_approval(bundle.approval.raw)

    # -- policy validity window ----------------------------------------------
    policy_raw = bundle.policy.raw
    current = _as_datetime(now)
    _check_policy_window(policy_raw, current)

    # -- request vs validated documents / policy allowlists ------------------
    if request.campaign_id != bundle.policy.campaign_id:
        raise ExploratoryAuthorizationError(
            EXPLORATORY_MINT_CAMPAIGN_ID_MISMATCH,
            f"request names campaign {request.campaign_id!r} but the "
            f"validated documents belong to {bundle.policy.campaign_id!r}",
        )
    if request.intended_model not in set(policy_raw.get("allowed_models", [])):
        raise ExploratoryAuthorizationError(
            EXPLORATORY_MINT_MODEL_NOT_ALLOWED,
            f"model {request.intended_model!r} is not in the policy's "
            "allowed_models",
        )
    if request.framework_sha not in set(policy_raw.get("allowed_framework_shas", [])):
        raise ExploratoryAuthorizationError(
            EXPLORATORY_MINT_FRAMEWORK_SHA_NOT_ALLOWED,
            f"framework sha {request.framework_sha!r} is not in the policy's "
            "allowed_framework_shas",
        )
    allowed_targets = {
        (str(item.get("repository", "")), str(item.get("sha", "")))
        for item in policy_raw.get("allowed_targets", [])
    }
    if (request.target_repository, request.target_sha) not in allowed_targets:
        raise ExploratoryAuthorizationError(
            EXPLORATORY_MINT_TARGET_NOT_ALLOWED,
            "the requested target (repository/sha) is not in the policy's "
            "allowed_targets",
        )
    if request.artifact_type not in set(policy_raw.get("allowed_artifact_types", [])):
        raise ExploratoryAuthorizationError(
            EXPLORATORY_MINT_ARTIFACT_TYPE_NOT_ALLOWED,
            f"artifact type {request.artifact_type!r} is not in the policy's "
            "allowed_artifact_types",
        )
    if request.configuration_id != bundle.configuration.configuration_id:
        raise ExploratoryAuthorizationError(
            EXPLORATORY_MINT_CONFIGURATION_ID_MISMATCH,
            "the request names a configuration the bundle did not validate",
        )
    # Defense-in-depth: Phase 2 already requires the validated configuration
    # to be a member of allowed_configuration_ids; the issuer re-checks.
    if request.configuration_id not in set(policy_raw.get("allowed_configuration_ids", [])):
        raise ExploratoryAuthorizationError(
            EXPLORATORY_MINT_CONFIGURATION_NOT_ALLOWED,
            "the validated configuration is not a member of the policy's "
            "allowed_configuration_ids",
        )

    # -- attempt identity -----------------------------------------------------
    if not _strict_uuid(request.attempt_id):
        raise ExploratoryAuthorizationError(
            EXPLORATORY_MINT_REQUIRES_ATTEMPT_ID_UUID,
            f"attempt_id {request.attempt_id!r} is not a strict lowercase "
            "UUID",
        )

    # -- capability binding (digests recomputed internally) ------------------
    window = policy_raw["validity_window"]
    binding = CapabilityBinding(
        campaign_id=bundle.policy.campaign_id,
        configuration_id=bundle.configuration.configuration_id,
        intended_model=request.intended_model,
        framework_sha=request.framework_sha,
        target_repository=request.target_repository,
        target_sha=request.target_sha,
        artifact_type=request.artifact_type,
        policy_digest=str(bundle.policy.policy_digest),
        approval_digest=compute_approval_snapshot_digest(bundle.approval.raw),
        configuration_snapshot_digest=compute_configuration_snapshot_digest(
            bundle.configuration.raw, bundle.configuration.configuration_id
        ),
        attempt_id=request.attempt_id,
        bound_output_path=request.output_path,
        executor_id=request.executor_id,
        provenance_mechanism=str(provenance.get("mechanism", "")),
        provenance_reference=str(provenance.get("reference", "")),
        valid_from=str(window.get("not_before", "")),
        expires_at=str(window.get("not_after", "")),
        lane=EXPLORATORY_LANE,
    )

    # -- registration (duplicate attempt ids are rejected) --------------------
    capability_id = hashlib.sha256(os.urandom(32)).hexdigest()
    if not _registry.issue(capability_id, request.attempt_id):
        raise ExploratoryAuthorizationError(
            EXPLORATORY_MINT_DUPLICATE_ATTEMPT_ID,
            f"attempt_id {request.attempt_id!r} was already issued in this "
            "process",
        )
    return _create_capability(
        _capability_id=capability_id, _binding=binding, _registry=_registry
    )
