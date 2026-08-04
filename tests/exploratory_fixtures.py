"""Phase 3 (#119): shared fixtures for exploratory-authorization tests.

Builds genuine ``ValidatedCampaignBundle`` objects through the REAL Phase 2
validation pipeline (``validate_campaign_bundle``) over docs that satisfy
the Two-Lane YAML Profile v1, with digests computed by the real
``compute_policy_digest`` / ``compute_configuration_id`` algorithms.

Every identity used here is unmistakably a test identity:
``EXP-9001-alpha`` is the campaign id, ``example-*`` names are the model,
targets, and approver, and all SHAs are zero-prefixed test constants.
"""

from __future__ import annotations

import datetime
import sys
import uuid
from pathlib import Path
from typing import Any, Mapping, Optional

from sensemaking_skills.campaign_validation import (
    compute_configuration_id,
    compute_policy_digest,
    validate_campaign_bundle,
)
from sensemaking_skills.campaign_validation.models import (
    ValidationContext,
    ValidatedCampaignBundle,
)

_TESTS_CAMPAIGN_VALIDATION_DIR = str(
    Path(__file__).resolve().parent / "campaign_validation"
)
if _TESTS_CAMPAIGN_VALIDATION_DIR not in sys.path:
    sys.path.insert(0, _TESTS_CAMPAIGN_VALIDATION_DIR)

from helpers import to_bytes  # noqa: E402  (Phase 2 profile-compliant serializer)

TEST_CAMPAIGN_ID = "EXP-9001-alpha"
TEST_APPROVER_IDENTITY = "test-approver-handle"
TEST_MODEL = "example-model-identifier"
TEST_TARGET_REPOSITORY = "https://example.invalid/example-owner/example-target.git"
TEST_TARGET_SHA = "000000000000000000000000000000000000beef"
TEST_FRAMEWORK_SHA = "000000000000000000000000000000000000dead"
TEST_ARTIFACT_TYPE = "attempt_result"
TEST_ATTEMPT_ID = "a1b2c3d4-e5f6-4789-8abc-def012345678"

# The validity window is anchored to the clock at fixture import time so the
# suites stay deterministic on any future date (mint/consume use injected
# "now" values relative to the same anchor; the real-now boundary tests are
# always inside the window).
_ANCHOR_NOW = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
TEST_NOT_BEFORE = (_ANCHOR_NOW - datetime.timedelta(days=30)).isoformat()
TEST_NOT_AFTER = (_ANCHOR_NOW + datetime.timedelta(days=365)).isoformat()
TEST_VALIDATION_TIME = _ANCHOR_NOW.isoformat()
TEST_PROVENANCE_MECHANISM = "signed_commit"
TEST_PROVENANCE_REFERENCE = "000000000000000000000000000000000000c0de"


def build_policy_raw(*, campaign_id: str = TEST_CAMPAIGN_ID,
                     allowed_configuration_ids: Optional[list] = None,
                     include_policy_digest: bool = True) -> dict:
    raw = {
        "policy_schema_version": "1",
        "campaign_id": campaign_id,
        "classification": "EXPLORATORY_NOT_CANONICAL_EVIDENCE",
        "allowed_framework_shas": [TEST_FRAMEWORK_SHA],
        "allowed_targets": [
            {"repository": TEST_TARGET_REPOSITORY, "sha": TEST_TARGET_SHA}
        ],
        "allowed_models": [TEST_MODEL],
        "allowed_artifact_types": [TEST_ARTIFACT_TYPE, "repository_sensemaking_brief"],
        "allowed_configuration_ids": (
            allowed_configuration_ids if allowed_configuration_ids is not None
            else ["1111111111111111111111111111111111111111111111111111111111111111"]
        ),
        "max_attempt_slots": 3,
        "max_provider_invocations": 3,
        "max_attempts_per_configuration": 2,
        "concurrency_ceiling": 1,
        "token_ceiling": None,
        "cost_ceiling": None,
        "validity_window": {
            "not_before": TEST_NOT_BEFORE,
            "not_after": TEST_NOT_AFTER,
        },
        "target_mutation_prohibited": True,
        "fallback_prohibited": True,
        "repair_prohibited": True,
        "automatic_merge_prohibited": True,
        "preservation_requirements": (
            "Test fixture: every reservation and attempt result is preserved."
        ),
        "logging_requirements": (
            "Test fixture: every provider invocation is logged."
        ),
        "prepared_by": "campaign-operator-agent",
        "prepared_at": "2026-01-01T00:00:00+00:00",
    }
    if include_policy_digest:
        raw["policy_digest"] = compute_policy_digest(raw)
    return raw


def build_configuration_raw(*, campaign_id: str = TEST_CAMPAIGN_ID,
                            artifact_type: str = TEST_ARTIFACT_TYPE) -> dict:
    raw = {
        "configuration_schema_version": "1",
        "campaign_id": campaign_id,
        "framework_sha": TEST_FRAMEWORK_SHA,
        "target_repository": TEST_TARGET_REPOSITORY,
        "target_sha": TEST_TARGET_SHA,
        "model_identifier": TEST_MODEL,
        "prompt_or_skill_revision": "v1",
        "validator_revision": "v1",
        "artifact_type": artifact_type,
        "execution_parameters": {},
    }
    raw["configuration_id"] = compute_configuration_id(raw)
    return raw


def build_approval_raw(*, campaign_id: str = TEST_CAMPAIGN_ID,
                       policy_digest: Optional[str] = None,
                       mechanism: str = TEST_PROVENANCE_MECHANISM,
                       reference: str = TEST_PROVENANCE_REFERENCE,
                       statement: str = "Test-only approval statement.",
                       include_marker: bool = False) -> dict:
    raw = {
        "approval_schema_version": "1",
        "campaign_id": campaign_id,
        "policy_digest": policy_digest or compute_policy_digest(
            build_policy_raw(campaign_id=campaign_id)),
        "claimed_approver_identity": TEST_APPROVER_IDENTITY,
        "approval_provenance": {"mechanism": mechanism, "reference": reference},
        "approval_statement": statement,
        "approved_at": "2026-01-01T00:00:00+00:00",
    }
    if include_marker:
        raw["marker"] = "EXAMPLE_ONLY_NOT_AUTHORIZATION"
    return raw


def render_yaml(raw: Mapping[str, Any]) -> bytes:
    return to_bytes(raw)


def build_valid_bundle(*, campaign_id: str = TEST_CAMPAIGN_ID,
                       approval_kwargs: Optional[dict] = None,
                       configuration_kwargs: Optional[dict] = None,
                       current_time: str = TEST_VALIDATION_TIME,
                       ) -> ValidatedCampaignBundle:
    """Run the REAL Phase 2 bundle pipeline over freshly built docs."""
    policy_raw = build_policy_raw(campaign_id=campaign_id)
    config_raw = build_configuration_raw(
        campaign_id=campaign_id, **(configuration_kwargs or {}))
    policy_raw["allowed_configuration_ids"] = sorted(
        [config_raw["configuration_id"]]
    )
    policy_raw["policy_digest"] = compute_policy_digest(policy_raw)
    policy_digest = policy_raw["policy_digest"]
    approval_raw = build_approval_raw(
        campaign_id=campaign_id,
        policy_digest=policy_digest,
        **(approval_kwargs or {}),
    )
    context = ValidationContext(
        current_time=current_time,
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
    )
    result = validate_campaign_bundle(
        render_yaml(policy_raw),
        render_yaml(approval_raw),
        render_yaml(config_raw),
        context,
    )
    assert result.valid, (
        f"fixture bundle failed validation: {result.failure_code} {result.detail}"
    )
    assert result.value is not None
    return result.value


def build_request(
    *, attempt_id: str = TEST_ATTEMPT_ID,
    campaign_id: str = TEST_CAMPAIGN_ID,
    configuration_id: Optional[str] = None,
    intended_model: str = TEST_MODEL,
    framework_sha: str = TEST_FRAMEWORK_SHA,
    target_repository: str = TEST_TARGET_REPOSITORY,
    target_sha: str = TEST_TARGET_SHA,
    artifact_type: str = TEST_ARTIFACT_TYPE,
    output_path: str = "/tmp/exploratory-tests/output/attempt-1.md",
    executor_id: str = "test-executor",
):
    from sensemaking_skills.exploratory_authorization.models import (
        ExploratoryAttemptRequest,
    )

    return ExploratoryAttemptRequest(
        attempt_id=attempt_id,
        campaign_id=campaign_id,
        configuration_id=configuration_id or "1111111111111111111111111111111111111111111111111111111111111111",
        intended_model=intended_model,
        framework_sha=framework_sha,
        target_repository=target_repository,
        target_sha=target_sha,
        artifact_type=artifact_type,
        output_path=output_path,
        executor_id=executor_id,
    )


def new_attempt_id() -> str:
    return str(uuid.uuid4())


class TrustedReferenceProvenanceVerifier:
    """Test double for ``ApprovalProvenanceVerifier``.

    Trusts exactly one approval: the one whose recomputed approval snapshot
    digest equals ``expected_digest`` and whose provenance mechanism and
    reference match the configured values. Anything else raises
    ``ProvenanceVerificationError`` -- including an approval whose digest
    does not bind to what the verifier was configured for.
    """

    def __init__(self, expected_digest: Optional[str] = None,
                 mechanism: str = TEST_PROVENANCE_MECHANISM,
                 reference: str = TEST_PROVENANCE_REFERENCE):
        self.expected_digest = expected_digest
        self.mechanism = mechanism
        self.reference = reference

    def verify(self, approval):
        from sensemaking_skills.exploratory_authorization.digests import (
            compute_approval_snapshot_digest,
        )
        from sensemaking_skills.exploratory_authorization.models import (
            VerifiedApprovalProvenance,
        )
        from sensemaking_skills.exploratory_authorization.provenance import (
            ProvenanceVerificationError,
        )

        actual = compute_approval_snapshot_digest(approval.raw)
        provenance = approval.raw["approval_provenance"]
        if (self.expected_digest is not None and actual != self.expected_digest):
            raise ProvenanceVerificationError(
                "approval digest does not match the verifier binding"
            )
        if provenance.get("mechanism") != self.mechanism:
            raise ProvenanceVerificationError("provenance mechanism mismatch")
        if provenance.get("reference") != self.reference:
            raise ProvenanceVerificationError("provenance reference mismatch")
        return VerifiedApprovalProvenance(
            mechanism=provenance["mechanism"], reference=provenance["reference"]
        )


def make_context(
    *, capability,
    model=None, target_repository=None, target_sha=None, framework_sha=None,
    artifact_type=None, output_path=None, campaign_id=None,
    configuration_id=None, configuration_snapshot_digest=None,
    policy_digest=None, approval_digest=None, attempt_id=None, lane=None,
):
    """Build a consumption context from a capability's binding with optional
    per-field overrides (each override simulates one drift category)."""
    from sensemaking_skills.exploratory_authorization.boundary import (
        ExploratoryInvocationContext,
    )

    b = capability.binding
    return ExploratoryInvocationContext(
        model=model if model is not None else b.intended_model,
        target_repository=(
            target_repository if target_repository is not None
            else b.target_repository),
        target_sha=target_sha if target_sha is not None else b.target_sha,
        framework_sha=framework_sha if framework_sha is not None else b.framework_sha,
        artifact_type=artifact_type if artifact_type is not None else b.artifact_type,
        output_path=output_path if output_path is not None else b.bound_output_path,
        campaign_id=campaign_id if campaign_id is not None else b.campaign_id,
        configuration_id=(
            configuration_id if configuration_id is not None
            else b.configuration_id),
        configuration_snapshot_digest=(
            configuration_snapshot_digest
            if configuration_snapshot_digest is not None
            else b.configuration_snapshot_digest),
        policy_digest=policy_digest if policy_digest is not None else b.policy_digest,
        approval_digest=(
            approval_digest if approval_digest is not None
            else b.approval_digest),
        attempt_id=attempt_id if attempt_id is not None else b.attempt_id,
        lane=lane if lane is not None else "EXPLORATORY",
    )
