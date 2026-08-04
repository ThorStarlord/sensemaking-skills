"""Phase 3 (#119): exploratory invocation capability lifecycle proofs.

Covers minting, non-forgeability, liveness, atomic single consumption, and
permanent spend-on-failure of ``ExploratoryInvocationCapability``. The
provider boundary itself is exercised in
``test_exploratory_provider_boundary.py``; this module proves the
capability object and its issuer registry directly.

Invariants under test (task brief sections 5-7, 10-12):

- The capability is minted ONLY from a genuine ``ValidatedCampaignBundle``
  plus a well-formed ``ExploratoryAttemptRequest``; digests are recomputed
  internally, never supplied by callers.
- The object is deeply immutable, non-copyable, non-serializable, and
  carries no authority of its own -- the process-local registry is the
  issuer and the only liveness authority.
- Consumption is atomic (ISSUED -> CONSUMING -> CONSUMED), at most one
  winner, every binding drift and expiry burns the capability, and a
  provider failure never revives it.
"""

from __future__ import annotations

import copy
import datetime
import pickle
import sys
import threading
import uuid
from pathlib import Path

import pytest

REPO_ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT_DIR / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import gate_a_authorization as ga  # noqa: E402 (pins checkout-local package first)

from exploratory_fixtures import (  # noqa: E402
    TEST_ARTIFACT_TYPE,
    TEST_ATTEMPT_ID,
    TEST_CAMPAIGN_ID,
    TEST_FRAMEWORK_SHA,
    TEST_MODEL,
    TEST_NOT_AFTER,
    TEST_PROVENANCE_REFERENCE,
    TEST_TARGET_REPOSITORY,
    TEST_TARGET_SHA,
    TrustedReferenceProvenanceVerifier,
    build_request,
    build_valid_bundle,
    make_context,
    new_attempt_id,
)

from sensemaking_skills.exploratory_authorization import (  # noqa: E402
    ExploratoryAuthorizationError,
    burn_exploratory_capability,
    consume_exploratory_capability,
    mint_exploratory_capability,
)
import sensemaking_skills.exploratory_authorization as ea  # noqa: E402
from sensemaking_skills.exploratory_authorization.digests import (  # noqa: E402
    compute_approval_snapshot_digest,
    compute_configuration_snapshot_digest,
)
from sensemaking_skills.exploratory_authorization.failure_codes import (  # noqa: E402
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
    EXPLORATORY_CAPABILITY_SERIALIZATION_PROHIBITED,
    EXPLORATORY_CAPABILITY_WRONG_TYPE,
    EXPLORATORY_MINT_CAMPAIGN_ID_MISMATCH,
    EXPLORATORY_MINT_CONFIGURATION_ID_MISMATCH,
    EXPLORATORY_MINT_ARTIFACT_TYPE_NOT_ALLOWED,
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
)
from sensemaking_skills.exploratory_authorization.models import (  # noqa: E402
    ExploratoryInvocationCapability,
)
from sensemaking_skills.exploratory_authorization.provenance import (  # noqa: E402
    ProvenanceVerificationError,
)

# "now" anchors relative to the import-time clock, mirroring the fixture's
# clock-relative validity window so the suite stays deterministic forever.
_ANCHOR = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
DEFAULT_NOW = _ANCHOR.isoformat()
LATE_NOW = (_ANCHOR + datetime.timedelta(days=400)).isoformat()
EARLY_NOW = (_ANCHOR - datetime.timedelta(days=400)).isoformat()


def _trusted_verifier(bundle):
    return TrustedReferenceProvenanceVerifier(
        expected_digest=compute_approval_snapshot_digest(bundle.approval.raw)
    )


def minted(*, bundle=None, request=None, verifier=None, now=DEFAULT_NOW):
    bundle = bundle if bundle is not None else build_valid_bundle()
    request = request if request is not None else build_request(
        configuration_id=bundle.configuration.configuration_id
    )
    return mint_exploratory_capability(
        bundle, request, verifier=verifier or _trusted_verifier(bundle), now=now
    )


def assert_code(exc: ExploratoryAuthorizationError, code: str) -> None:
    assert exc.failure_code == code, f"expected {code}, got {exc.failure_code}"
    assert code in str(exc)


@pytest.fixture(autouse=True)
def _fresh_registry():
    """Each test starts from an empty process-local issuer registry."""
    ea.reset_exploratory_registry()
    yield


# ---------------------------------------------------------------------------
# Minting: the happy path
# ---------------------------------------------------------------------------


def test_mint_returns_live_capability_with_bound_values():
    bundle = build_valid_bundle()
    request = build_request(configuration_id=bundle.configuration.configuration_id)
    capability = minted(bundle=bundle, request=request)
    assert capability.live is True
    assert capability.consumed is False
    assert capability.attempt_id == request.attempt_id
    assert capability.campaign_id == bundle.policy.campaign_id
    assert capability.configuration_id == bundle.configuration.configuration_id
    binding = capability.binding
    assert binding.intended_model == TEST_MODEL
    assert binding.framework_sha == TEST_FRAMEWORK_SHA
    assert binding.target_repository == TEST_TARGET_REPOSITORY
    assert binding.target_sha == TEST_TARGET_SHA
    assert binding.artifact_type == TEST_ARTIFACT_TYPE
    assert binding.policy_digest == bundle.policy.policy_digest
    assert binding.bound_output_path == request.output_path
    assert binding.executor_id == request.executor_id
    assert binding.expires_at == TEST_NOT_AFTER
    assert capability.expires_at == TEST_NOT_AFTER


def test_mint_recomputes_both_snapshot_digests_internally():
    bundle = build_valid_bundle()
    capability = minted(bundle=bundle)
    assert capability.binding.approval_digest == compute_approval_snapshot_digest(
        bundle.approval.raw
    )
    assert capability.binding.configuration_snapshot_digest == (
        compute_configuration_snapshot_digest(
            bundle.configuration.raw, bundle.configuration.configuration_id
        )
    )


def test_mint_binds_verified_provenance():
    bundle = build_valid_bundle()
    capability = minted(bundle=bundle)
    assert capability.binding.provenance_mechanism == "signed_commit"
    assert capability.binding.provenance_reference == (
        "000000000000000000000000000000000000c0de"
    )


def test_capability_is_not_a_canonical_authorized_invocation():
    capability = minted()
    assert isinstance(capability, ga.AuthorizedInvocation) is False
    assert isinstance(capability, ExploratoryInvocationCapability) is True


def test_request_is_immutable():
    bundle = build_valid_bundle()
    request = build_request(configuration_id=bundle.configuration.configuration_id)
    with pytest.raises(Exception):
        request.attempt_id = new_attempt_id()


# ---------------------------------------------------------------------------
# Minting: genuine-bundle provenance
# ---------------------------------------------------------------------------


def _forged_bundle_from(bundle):
    from sensemaking_skills.campaign_validation.models import (
        CampaignApproval,
        CampaignPolicy,
        ConfigurationIdentity,
        ValidatedCampaignBundle,
    )

    def _forged(cls, **attrs):
        instance = object.__new__(cls)
        for name, value in attrs.items():
            object.__setattr__(instance, name, value)
        return instance

    forged = _forged(
        ValidatedCampaignBundle,
        policy=_forged(
            CampaignPolicy,
            campaign_id=bundle.policy.campaign_id,
            policy_digest=bundle.policy.policy_digest,
            raw=dict(bundle.policy.raw),
        ),
        approval=_forged(
            CampaignApproval,
            campaign_id=bundle.approval.campaign_id,
            policy_digest=bundle.approval.policy_digest,
            claimed_approver_identity=bundle.approval.claimed_approver_identity,
            raw=dict(bundle.approval.raw),
        ),
        configuration=_forged(
            ConfigurationIdentity,
            configuration_id=bundle.configuration.configuration_id,
            campaign_id=bundle.configuration.campaign_id,
            raw=dict(bundle.configuration.raw),
        ),
    )
    return forged


def test_mint_rejects_forged_bundle():
    bundle = build_valid_bundle()
    forged = _forged_bundle_from(bundle)
    request = build_request(configuration_id=bundle.configuration.configuration_id)
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        mint_exploratory_capability(
            forged, request, verifier=_trusted_verifier(bundle), now=DEFAULT_NOW
        )
    assert_code(exc.value, EXPLORATORY_MINT_REQUIRES_GENUINE_BUNDLE)


# ---------------------------------------------------------------------------
# Minting: approval operationality
#
# NOTE: the mint also enforces approval operationality (marker, provenance
# mechanism/reference, approval statement) as defense-in-depth
# (EXPLORATORY_MINT_REQUIRES_OPERATIVE_APPROVAL and friends), but those
# checks are UNREACHABLE through the real Phase 2 pipeline: the bundle
# validator rejects marker approvals, "none"/missing provenance, and blank
# statements before mint ever runs. The positive test below pins the
# transitive guarantee: every minted capability's provenance is operative.
# ---------------------------------------------------------------------------


def test_mint_capability_provenance_is_operative():
    capability = minted()
    assert capability.binding.provenance_mechanism == "signed_commit"
    assert capability.binding.provenance_reference == TEST_PROVENANCE_REFERENCE
    assert capability.binding.provenance_mechanism not in ("", "none")


# ---------------------------------------------------------------------------
# Minting: policy validity window
# ---------------------------------------------------------------------------


def test_mint_rejects_policy_already_expired():
    bundle = build_valid_bundle()
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        minted(bundle=bundle, now=LATE_NOW)
    assert_code(exc.value, EXPLORATORY_MINT_POLICY_EXPIRED)


def test_mint_rejects_policy_not_yet_valid():
    bundle = build_valid_bundle()
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        minted(bundle=bundle, now=EARLY_NOW)
    assert_code(exc.value, EXPLORATORY_MINT_POLICY_EXPIRED)


# ---------------------------------------------------------------------------
# Minting: request vs validated documents
# ---------------------------------------------------------------------------


def test_mint_rejects_campaign_id_mismatch():
    bundle = build_valid_bundle()
    request = build_request(
        configuration_id=bundle.configuration.configuration_id,
        campaign_id="EXP-9002-other",
    )
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        minted(bundle=bundle, request=request)
    assert_code(exc.value, EXPLORATORY_MINT_CAMPAIGN_ID_MISMATCH)


def test_mint_rejects_configuration_id_mismatch():
    bundle = build_valid_bundle()
    request = build_request(
        configuration_id="2222222222222222222222222222222222222222222222222222222222222222"
    )
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        minted(bundle=bundle, request=request)
    assert_code(exc.value, EXPLORATORY_MINT_CONFIGURATION_ID_MISMATCH)


def test_mint_rejects_model_not_in_allowlist():
    bundle = build_valid_bundle()
    request = build_request(
        configuration_id=bundle.configuration.configuration_id,
        intended_model="unlisted-model",
    )
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        minted(bundle=bundle, request=request)
    assert_code(exc.value, EXPLORATORY_MINT_MODEL_NOT_ALLOWED)


def test_mint_rejects_framework_sha_not_in_allowlist():
    bundle = build_valid_bundle()
    request = build_request(
        configuration_id=bundle.configuration.configuration_id,
        framework_sha="0" * 40,
    )
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        minted(bundle=bundle, request=request)
    assert_code(exc.value, EXPLORATORY_MINT_FRAMEWORK_SHA_NOT_ALLOWED)


def test_mint_rejects_target_repository_not_in_allowlist():
    bundle = build_valid_bundle()
    request = build_request(
        configuration_id=bundle.configuration.configuration_id,
        target_repository="https://example.invalid/example-owner/other-target.git",
    )
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        minted(bundle=bundle, request=request)
    assert_code(exc.value, EXPLORATORY_MINT_TARGET_NOT_ALLOWED)


def test_mint_rejects_target_sha_not_in_allowlist():
    bundle = build_valid_bundle()
    request = build_request(
        configuration_id=bundle.configuration.configuration_id,
        target_sha="0" * 40,
    )
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        minted(bundle=bundle, request=request)
    assert_code(exc.value, EXPLORATORY_MINT_TARGET_NOT_ALLOWED)


def test_mint_rejects_artifact_type_not_in_allowlist():
    bundle = build_valid_bundle()
    request = build_request(
        configuration_id=bundle.configuration.configuration_id,
        artifact_type="unlisted_artifact",
    )
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        minted(bundle=bundle, request=request)
    assert_code(exc.value, EXPLORATORY_MINT_ARTIFACT_TYPE_NOT_ALLOWED)


def test_mint_configuration_is_transitively_allowed_by_policy():
    # The Phase 2 bundle validator requires the validated configuration to be
    # a member of the policy's allowed_configuration_ids (defense in depth:
    # the mint re-checks membership too, EXPLORATORY_MINT_CONFIGURATION_NOT_ALLOWED,
    # which is unreachable through valid bundles). Pinning the transitive
    # guarantee at the capability level.
    bundle = build_valid_bundle()
    capability = minted(bundle=bundle)
    assert capability.configuration_id in bundle.policy.raw["allowed_configuration_ids"]


# ---------------------------------------------------------------------------
# Minting: attempt identity
# ---------------------------------------------------------------------------


def test_mint_rejects_malformed_attempt_id():
    bundle = build_valid_bundle()
    for bad in ("", "not-a-uuid", str(uuid.uuid4()).upper(), "x" * 36):
        request = build_request(
            configuration_id=bundle.configuration.configuration_id,
            attempt_id=bad,
        )
        with pytest.raises(ExploratoryAuthorizationError) as exc:
            minted(bundle=bundle, request=request)
        assert_code(exc.value, EXPLORATORY_MINT_REQUIRES_ATTEMPT_ID_UUID)


def test_mint_rejects_duplicate_attempt_id_in_process():
    bundle = build_valid_bundle()
    request = build_request(configuration_id=bundle.configuration.configuration_id)
    minted(bundle=bundle, request=request)
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        minted(bundle=bundle, request=request)
    assert_code(exc.value, EXPLORATORY_MINT_DUPLICATE_ATTEMPT_ID)


def test_mint_accepts_second_attempt_with_new_attempt_id():
    bundle = build_valid_bundle()
    first = minted(bundle=bundle)
    second_request = build_request(
        configuration_id=bundle.configuration.configuration_id,
        attempt_id=new_attempt_id(),
    )
    second = minted(bundle=bundle, request=second_request)
    assert first.attempt_id != second.attempt_id
    assert first.live and second.live


# ---------------------------------------------------------------------------
# Provenance verifier boundary
# ---------------------------------------------------------------------------


def test_mint_without_verifier_fails_closed():
    bundle = build_valid_bundle()
    request = build_request(configuration_id=bundle.configuration.configuration_id)
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        mint_exploratory_capability(bundle, request, verifier=None, now=DEFAULT_NOW)
    assert_code(exc.value, EXPLORATORY_PROVENANCE_VERIFIER_REJECTED)


def test_mint_with_verifier_raising_fails():
    bundle = build_valid_bundle()

    class RaisingVerifier:
        def verify(self, approval):
            raise ProvenanceVerificationError("corroboration unavailable")

    request = build_request(configuration_id=bundle.configuration.configuration_id)
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        mint_exploratory_capability(
            bundle, request, verifier=RaisingVerifier(), now=DEFAULT_NOW
        )
    assert_code(exc.value, EXPLORATORY_PROVENANCE_VERIFIER_FAILED)


def test_mint_verifier_must_bind_exact_approval_digest():
    bundle = build_valid_bundle()
    wrong_digest = "0" * 64
    verifier = TrustedReferenceProvenanceVerifier(expected_digest=wrong_digest)
    request = build_request(configuration_id=bundle.configuration.configuration_id)
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        mint_exploratory_capability(bundle, request, verifier=verifier, now=DEFAULT_NOW)
    assert_code(exc.value, EXPLORATORY_PROVENANCE_VERIFIER_FAILED)


def test_mint_verifier_result_must_match_declared_provenance():
    bundle = build_valid_bundle()

    class ConflictingVerifier:
        def verify(self, approval):
            from sensemaking_skills.exploratory_authorization.models import (
                VerifiedApprovalProvenance,
            )

            return VerifiedApprovalProvenance(
                mechanism="github_review_approval", reference="https://review/123"
            )

    request = build_request(configuration_id=bundle.configuration.configuration_id)
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        mint_exploratory_capability(
            bundle, request, verifier=ConflictingVerifier(), now=DEFAULT_NOW
        )
    assert_code(exc.value, EXPLORATORY_PROVENANCE_VERIFIER_FAILED)


# ---------------------------------------------------------------------------
# Non-forgeability: the capability object
# ---------------------------------------------------------------------------


def test_capability_cannot_be_constructed_directly():
    with pytest.raises(Exception):
        ExploratoryInvocationCapability("wrong-token", "0000000000000000000000000000000000000000000000000000000000000000")


def test_capability_is_immutable():
    capability = minted()
    with pytest.raises(Exception) as exc:
        capability._capability_id = "x"
    assert EXPLORATORY_CAPABILITY_IMMUTABLE in str(exc.value)
    with pytest.raises(Exception) as exc:
        del capability._capability_id
    assert EXPLORATORY_CAPABILITY_IMMUTABLE in str(exc.value)


def test_capability_rejects_copy_and_deepcopy():
    capability = minted()
    for copier in (copy.copy, copy.deepcopy):
        with pytest.raises(TypeError) as exc:
            copier(capability)
        assert EXPLORATORY_CAPABILITY_COPY_PROHIBITED in str(exc.value)


def test_capability_rejects_pickling():
    capability = minted()
    with pytest.raises(TypeError) as exc:
        pickle.dumps(capability)
    assert EXPLORATORY_CAPABILITY_SERIALIZATION_PROHIBITED in str(exc.value)


def test_capability_rejects_subclassing():
    with pytest.raises(TypeError) as exc:
        type("ForgedCapability", (ExploratoryInvocationCapability,), {})
    assert EXPLORATORY_CAPABILITY_COPY_PROHIBITED in str(exc.value)


def test_forged_capability_object_is_not_live():
    forged = object.__new__(ExploratoryInvocationCapability)
    assert forged.live is False


def test_capability_with_random_id_is_not_live():
    capability = minted()
    forged = object.__new__(ExploratoryInvocationCapability)
    object.__setattr__(forged, "_capability_id", "0" * 64)
    assert forged.live is False
    assert capability.live is True


# ---------------------------------------------------------------------------
# Consumption: the happy path
# ---------------------------------------------------------------------------


def test_consume_happy_path_spends_exactly_once():
    capability = minted()
    decision = consume_exploratory_capability(capability, make_context(capability=capability))
    assert decision.exact_model == TEST_MODEL
    assert decision.output_path == capability.binding.bound_output_path
    assert decision.attempt_id == capability.attempt_id
    assert decision.campaign_id == capability.campaign_id
    assert capability.live is False
    assert capability.consumed is True


def test_consume_second_call_is_rejected():
    capability = minted()
    consume_exploratory_capability(capability, make_context(capability=capability))
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        consume_exploratory_capability(capability, make_context(capability=capability))
    assert_code(exc.value, EXPLORATORY_CAPABILITY_ALREADY_CONSUMED)


def test_consume_with_wrong_type_is_rejected():
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        consume_exploratory_capability(object(), None)
    assert_code(exc.value, EXPLORATORY_CAPABILITY_WRONG_TYPE)


def test_consume_not_live_capability_is_rejected():
    capability = minted()
    consume_exploratory_capability(capability, make_context(capability=capability))
    second = object.__new__(ExploratoryInvocationCapability)
    object.__setattr__(second, "_capability_id", "0" * 64)
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        consume_exploratory_capability(second, make_context(capability=capability))
    assert_code(exc.value, EXPLORATORY_CAPABILITY_NOT_LIVE)


# ---------------------------------------------------------------------------
# Consumption: binding drift (13 categories) burns the capability
# ---------------------------------------------------------------------------

DRIFT_CASES = [
    ("model", {"model": "some-other-model"}, EXPLORATORY_BINDING_MODEL_MISMATCH),
    ("target_repository", {"target_repository": "https://example.invalid/example-owner/other.git"}, EXPLORATORY_BINDING_TARGET_REPOSITORY_MISMATCH),
    ("target_sha", {"target_sha": "0" * 40}, EXPLORATORY_BINDING_TARGET_SHA_MISMATCH),
    ("framework_sha", {"framework_sha": "0" * 40}, EXPLORATORY_BINDING_FRAMEWORK_SHA_MISMATCH),
    ("artifact_type", {"artifact_type": "unlisted_artifact"}, EXPLORATORY_BINDING_ARTIFACT_TYPE_MISMATCH),
    ("configuration_id", {"configuration_id": "2222222222222222222222222222222222222222222222222222222222222222"}, EXPLORATORY_BINDING_CONFIGURATION_ID_MISMATCH),
    ("configuration_snapshot", {"configuration_snapshot_digest": "3" * 64}, EXPLORATORY_BINDING_CONFIGURATION_SNAPSHOT_MISMATCH),
    ("campaign_id", {"campaign_id": "EXP-9002-other"}, EXPLORATORY_BINDING_CAMPAIGN_ID_MISMATCH),
    ("policy_digest", {"policy_digest": "4" * 64}, EXPLORATORY_BINDING_POLICY_DIGEST_MISMATCH),
    ("approval_digest", {"approval_digest": "5" * 64}, EXPLORATORY_BINDING_APPROVAL_DIGEST_MISMATCH),
    ("attempt_id", {"attempt_id": "f1e2d3c4-b5a6-4987-8c9d-0e1f2a3b4c5d"}, EXPLORATORY_BINDING_ATTEMPT_ID_MISMATCH),
    ("lane", {"lane": "AMBIGUOUS"}, EXPLORATORY_BINDING_LANE_MISMATCH),
    ("output_path", {"output_path": "/tmp/exploratory-tests/elsewhere/attempt-2.md"}, EXPLORATORY_BINDING_OUTPUT_PATH_MISMATCH),
]


@pytest.mark.parametrize(
    "name,overrides,code", DRIFT_CASES, ids=[case[0] for case in DRIFT_CASES]
)
def test_consume_binding_drift_burns_capability(name, overrides, code):
    capability = minted()
    context = make_context(capability=capability, **overrides)
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        consume_exploratory_capability(capability, context)
    assert_code(exc.value, code)
    assert capability.live is False
    with pytest.raises(ExploratoryAuthorizationError) as exc2:
        consume_exploratory_capability(capability, make_context(capability=capability))
    assert_code(exc2.value, EXPLORATORY_CAPABILITY_CONSUMPTION_FAILED)


# ---------------------------------------------------------------------------
# Consumption: expiry between mint and consume
# ---------------------------------------------------------------------------


def test_consume_expired_capability_is_rejected_and_burned():
    capability = minted(now=DEFAULT_NOW)
    context = make_context(capability=capability)
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        consume_exploratory_capability(capability, context, now=LATE_NOW)
    assert_code(exc.value, EXPLORATORY_CAPABILITY_EXPIRED)
    assert capability.live is False


def test_consume_within_window_succeeds_at_boundary():
    capability = minted(now=DEFAULT_NOW)
    decision = consume_exploratory_capability(
        capability, make_context(capability=capability), now=TEST_NOT_AFTER
    )
    assert decision.exact_model == TEST_MODEL


# ---------------------------------------------------------------------------
# Consumption: concurrency (single winner)
# ---------------------------------------------------------------------------


def test_concurrent_consumption_single_winner():
    capability = minted()
    context = make_context(capability=capability)
    started = threading.Event()
    release = threading.Event()

    def hook():
        started.set()
        release.wait(5)

    errors = []

    def worker():
        try:
            consume_exploratory_capability(capability, context, _before_complete=hook)
        except Exception as exc:  # pragma: no cover - asserted below
            errors.append(exc)

    thread = threading.Thread(target=worker)
    thread.start()
    assert started.wait(5), "first consumer did not reach the critical section"
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        consume_exploratory_capability(capability, context)
    assert_code(exc.value, EXPLORATORY_CAPABILITY_CONCURRENT_CONSUMPTION)
    release.set()
    thread.join(5)
    assert not thread.is_alive(), "first consumer did not finish"
    assert not errors
    assert capability.live is False
    assert capability.consumed is True


# ---------------------------------------------------------------------------
# Consumption: permanent spend on provider failure
# ---------------------------------------------------------------------------


def test_provider_failure_burns_capability_permanently():
    capability = minted()
    consume_exploratory_capability(capability, make_context(capability=capability))
    burn_exploratory_capability(capability)
    assert capability.live is False
    assert capability.consumed is True
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        consume_exploratory_capability(capability, make_context(capability=capability))
    assert_code(exc.value, EXPLORATORY_CAPABILITY_CONSUMPTION_FAILED)


def test_burn_of_unconsumed_capability_spends_it():
    capability = minted()
    burn_exploratory_capability(capability)
    assert capability.live is False
    with pytest.raises(ExploratoryAuthorizationError) as exc:
        consume_exploratory_capability(capability, make_context(capability=capability))
    assert_code(exc.value, EXPLORATORY_CAPABILITY_CONSUMPTION_FAILED)
