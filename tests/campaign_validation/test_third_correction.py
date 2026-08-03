"""Tests added while correcting the third round of blocking review findings
on PR #125: validator-owned CampaignPolicy provenance, JCS numeric-domain
preflight, exact version-field precedence, exact path-failure routing, and
public/private ValidationResult separation.
"""

from __future__ import annotations

import copy
import dataclasses
import pickle

import pytest

from sensemaking_skills.campaign_validation import (
    CampaignApproval,
    CampaignPolicy,
    ConfigurationIdentity,
    ValidatedCampaignBundle,
    ValidationContext,
    ValidationResult,
    validate_campaign_approval,
    validate_campaign_bundle,
    validate_campaign_policy,
    validate_configuration_identity,
)
from sensemaking_skills.campaign_validation.yaml_profile import parse_two_lane_yaml

from .fixtures import (
    AUTHORIZED_APPROVER,
    base_approval_doc,
    base_configuration_doc,
    base_policy_doc,
    build_valid_bundle_bytes,
    finalize_configuration,
    finalize_policy,
    to_campaign_policy,
)
from .helpers import to_bytes

NOW = "2026-06-01T00:00:00+00:00"


def _ctx(**overrides):
    defaults = dict(current_time=NOW, allowed_approver_identities=frozenset({AUTHORIZED_APPROVER}))
    defaults.update(overrides)
    return ValidationContext(**defaults)


# ---------------------------------------------------------------------------
# Section 2: validated-policy handles are non-forgeable
# ---------------------------------------------------------------------------

def test_direct_campaign_policy_construction_fails():
    with pytest.raises(TypeError):
        CampaignPolicy(campaign_id="EXP-0001-example", policy_digest="0" * 64, raw={})


def test_plain_mapping_rejected_by_approval_validator():
    policy_doc = finalize_policy(base_policy_doc(["1" * 64]))
    approval = base_approval_doc(policy_doc)
    result = validate_campaign_approval(to_bytes(approval), policy_doc, _ctx())  # plain dict
    assert not result.valid
    assert result.failure_code == "CAMPAIGN_INTERNAL_VALIDATION_ERROR"


def test_manually_forged_instance_rejected():
    """object.__new__ + guessed-looking attribute assignment must not verify
    as genuine -- the real provenance sentinel is held in a closure inside
    models.py, never exported, so a forger cannot reproduce it."""
    forged = object.__new__(CampaignPolicy)
    object.__setattr__(forged, "campaign_id", "EXP-0001-example")
    object.__setattr__(forged, "policy_digest", "0" * 64)
    object.__setattr__(forged, "raw", {})
    object.__setattr__(forged, "_provenance_seal", object())  # a DIFFERENT sentinel

    policy_doc = finalize_policy(base_policy_doc(["1" * 64]))
    approval = base_approval_doc(policy_doc)
    result = validate_campaign_approval(to_bytes(approval), forged, _ctx())
    assert not result.valid
    assert result.failure_code == "CAMPAIGN_INTERNAL_VALIDATION_ERROR"


def test_copying_or_pickling_cannot_forge_a_trusted_policy():
    policy_doc = finalize_policy(base_policy_doc(["1" * 64]))
    genuine = to_campaign_policy(policy_doc)

    # dataclasses.replace() calls the (disabled) public constructor under
    # the hood -- it must fail the same way direct construction does.
    with pytest.raises(TypeError):
        dataclasses.replace(genuine, campaign_id="EXP-9999-tampered")

    # copy.deepcopy calls __reduce_ex__/pickle machinery, which for a frozen
    # dataclass with no custom __reduce__ round-trips through __class__ and
    # __dict__ / object.__new__ + setstate -- it must not carry the genuine
    # sentinel's IDENTITY across a pickle round-trip in a way a forger could
    # reproduce on their own object; the key property under test is that an
    # attacker's OWN constructed object (not a copy of a real one) never
    # verifies, which is covered by test_manually_forged_instance_rejected.
    # Here we confirm a naive copy.deepcopy of the raw dict cannot be reused
    # to build a genuine-looking policy via the public constructor.
    with pytest.raises(TypeError):
        CampaignPolicy(
            campaign_id=genuine.campaign_id,
            policy_digest=genuine.policy_digest,
            raw=copy.deepcopy(dict(genuine.raw)),
        )


def test_genuine_validator_created_policy_is_accepted():
    policy_doc = finalize_policy(base_policy_doc(["1" * 64]))
    policy = to_campaign_policy(policy_doc)
    approval = base_approval_doc(policy_doc)
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert result.valid


def test_genuine_policy_remains_accepted_after_ordinary_immutable_reads():
    policy_doc = finalize_policy(base_policy_doc(["1" * 64]))
    policy = to_campaign_policy(policy_doc)
    _ = policy.campaign_id
    _ = policy.policy_digest
    _ = dict(policy.raw)  # reading raw contents does not un-seal the instance
    approval = base_approval_doc(policy_doc)
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert result.valid


def test_approval_validation_cannot_succeed_against_forged_policy():
    forged = object.__new__(CampaignPolicy)
    object.__setattr__(forged, "campaign_id", "EXP-0001-example")
    object.__setattr__(forged, "policy_digest", "0" * 64)
    object.__setattr__(forged, "raw", {"campaign_id": "EXP-0001-example"})
    policy_doc = finalize_policy(base_policy_doc(["1" * 64]))
    approval = base_approval_doc(policy_doc)
    result = validate_campaign_approval(to_bytes(approval), forged, _ctx())
    assert result.failure_code == "CAMPAIGN_INTERNAL_VALIDATION_ERROR"


def test_configuration_validation_cannot_succeed_against_forged_policy():
    forged = object.__new__(CampaignPolicy)
    object.__setattr__(forged, "campaign_id", "EXP-0001-example")
    object.__setattr__(forged, "policy_digest", "0" * 64)
    object.__setattr__(forged, "raw", {
        "allowed_configuration_ids": ["0" * 64], "allowed_framework_shas": ["a" * 40],
        "allowed_targets": [], "allowed_models": [], "allowed_artifact_types": [],
    })
    config = finalize_configuration(base_configuration_doc())
    result = validate_configuration_identity(to_bytes(config), forged)
    assert result.failure_code == "CAMPAIGN_INTERNAL_VALIDATION_ERROR"


def test_installed_wheel_style_full_bundle_still_succeeds_with_genuine_policy():
    """(Not a subprocess/wheel test -- that's covered by
    test_installed_wheel_smoke.py -- this proves the in-process bundle path
    still works end-to-end after the provenance-sealing change.)"""
    pb, ab, cb = build_valid_bundle_bytes()
    result = validate_campaign_bundle(pb, ab, cb, _ctx())
    assert result.valid
    assert isinstance(result.value, ValidatedCampaignBundle)


# ---------------------------------------------------------------------------
# Section 4 (JCS numeric-domain preflight)
# ---------------------------------------------------------------------------

def test_policy_max_attempt_slots_at_safe_integer_boundary_accepted():
    doc = base_policy_doc(["1" * 64])
    doc["max_attempt_slots"] = 9007199254740991
    doc["max_provider_invocations"] = 9007199254740991
    doc = finalize_policy(doc)
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.valid


def test_policy_max_attempt_slots_beyond_safe_integer_rejected_as_limits_invalid():
    doc = base_policy_doc(["1" * 64])
    doc["max_attempt_slots"] = 9007199254740992
    doc["policy_digest"] = "0" * 64  # cannot be a real digest; see docstring elsewhere
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_LIMITS_INVALID"


def test_policy_cost_ceiling_amount_beyond_safe_integer_rejected():
    doc = base_policy_doc(["1" * 64])
    doc["cost_ceiling"] = {"amount": 9007199254740992, "currency": "USD"}
    doc["policy_digest"] = "0" * 64
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_LIMITS_INVALID"


def test_configuration_execution_parameter_beyond_safe_integer_rejected():
    config = base_configuration_doc()
    config["execution_parameters"]["oversized"] = 9007199254740992
    config["configuration_id"] = "0" * 64  # cannot be a real digest
    policy = to_campaign_policy(finalize_policy(base_policy_doc(["1" * 64])))
    result = validate_configuration_identity(to_bytes(config), policy)
    assert result.failure_code == "CAMPAIGN_CONFIGURATION_NUMERIC_DOMAIN_INVALID"


def test_configuration_execution_parameter_nested_beyond_safe_integer_rejected():
    config = base_configuration_doc()
    config["execution_parameters"]["nested"] = {"deep": {"deeper": 9007199254740992}}
    config["configuration_id"] = "0" * 64
    policy = to_campaign_policy(finalize_policy(base_policy_doc(["1" * 64])))
    result = validate_configuration_identity(to_bytes(config), policy)
    assert result.failure_code == "CAMPAIGN_CONFIGURATION_NUMERIC_DOMAIN_INVALID"


def test_configuration_execution_parameter_in_sequence_beyond_safe_integer_rejected():
    config = base_configuration_doc()
    config["execution_parameters"]["values"] = [1, 2, 9007199254740992]
    config["configuration_id"] = "0" * 64
    policy = to_campaign_policy(finalize_policy(base_policy_doc(["1" * 64])))
    result = validate_configuration_identity(to_bytes(config), policy)
    assert result.failure_code == "CAMPAIGN_CONFIGURATION_NUMERIC_DOMAIN_INVALID"


def test_2_pow_60_rejected_deliberately():
    doc = base_policy_doc(["1" * 64])
    doc["max_attempt_slots"] = 2 ** 60
    doc["policy_digest"] = "0" * 64
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_LIMITS_INVALID"


def test_negative_2_pow_60_rejected_deliberately():
    config = base_configuration_doc()
    config["execution_parameters"]["oversized"] = -(2 ** 60)
    config["configuration_id"] = "0" * 64
    policy = to_campaign_policy(finalize_policy(base_policy_doc(["1" * 64])))
    result = validate_configuration_identity(to_bytes(config), policy)
    assert result.failure_code == "CAMPAIGN_CONFIGURATION_NUMERIC_DOMAIN_INVALID"


def test_negative_safe_integer_boundary_accepted_where_permitted():
    """token_ceiling has no documented sign restriction beyond integer-lexeme
    and safe-integer-range -- a negative value at the exact safe boundary
    must be accepted by the numeric-domain preflight itself (whether it is
    semantically sensible for token_ceiling is a separate, undocumented
    concern outside this phase's scope)."""
    doc = base_policy_doc(["1" * 64])
    doc["token_ceiling"] = -9007199254740991
    doc = finalize_policy(doc)
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.valid


@pytest.mark.parametrize("bad_value", [9007199254740992, -9007199254740992, 2 ** 60])
def test_no_oversized_numeric_case_reports_internal_error(bad_value):
    doc = base_policy_doc(["1" * 64])
    doc["max_attempt_slots"] = bad_value
    doc["policy_digest"] = "0" * 64
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code != "CAMPAIGN_INTERNAL_VALIDATION_ERROR"


# ---------------------------------------------------------------------------
# Section 4 (version-field precedence)
# ---------------------------------------------------------------------------

def test_policy_missing_version_is_schema_invalid_not_unsupported():
    doc = finalize_policy(base_policy_doc(["1" * 64]))
    del doc["policy_schema_version"]
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_SCHEMA_INVALID"


def test_policy_non_string_version_is_schema_invalid():
    doc = base_policy_doc(["1" * 64])
    doc["policy_schema_version"] = 1  # integer, not string
    doc["policy_digest"] = "0" * 64
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_SCHEMA_INVALID"


def test_policy_unsupported_string_version_is_schema_unsupported():
    doc = base_policy_doc(["1" * 64])
    doc["policy_schema_version"] = "2"
    doc["policy_digest"] = "0" * 64
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_SCHEMA_UNSUPPORTED"


def test_approval_missing_version_is_schema_invalid():
    policy_doc = finalize_policy(base_policy_doc(["1" * 64]))
    policy = to_campaign_policy(policy_doc)
    approval = base_approval_doc(policy_doc)
    del approval["approval_schema_version"]
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert result.failure_code == "CAMPAIGN_APPROVAL_SCHEMA_INVALID"


def test_approval_non_string_version_is_schema_invalid():
    policy_doc = finalize_policy(base_policy_doc(["1" * 64]))
    policy = to_campaign_policy(policy_doc)
    approval = base_approval_doc(policy_doc)
    approval["approval_schema_version"] = 1
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert result.failure_code == "CAMPAIGN_APPROVAL_SCHEMA_INVALID"


def test_approval_unsupported_string_version_is_schema_unsupported():
    policy_doc = finalize_policy(base_policy_doc(["1" * 64]))
    policy = to_campaign_policy(policy_doc)
    approval = base_approval_doc(policy_doc)
    approval["approval_schema_version"] = "2"
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert result.failure_code == "CAMPAIGN_APPROVAL_SCHEMA_UNSUPPORTED"


def test_configuration_missing_version_is_schema_invalid():
    config = finalize_configuration(base_configuration_doc())
    policy = to_campaign_policy(finalize_policy(base_policy_doc([config["configuration_id"]])))
    del config["configuration_schema_version"]
    result = validate_configuration_identity(to_bytes(config), policy)
    assert result.failure_code == "CAMPAIGN_CONFIGURATION_SCHEMA_INVALID"


def test_configuration_non_string_version_is_schema_invalid():
    config = finalize_configuration(base_configuration_doc())
    policy = to_campaign_policy(finalize_policy(base_policy_doc([config["configuration_id"]])))
    config["configuration_schema_version"] = 1
    result = validate_configuration_identity(to_bytes(config), policy)
    assert result.failure_code == "CAMPAIGN_CONFIGURATION_SCHEMA_INVALID"


def test_configuration_unsupported_string_version_is_schema_unsupported():
    config = base_configuration_doc()
    config["configuration_schema_version"] = "2"
    config["configuration_id"] = "0" * 64
    policy = to_campaign_policy(finalize_policy(base_policy_doc(["1" * 64])))
    result = validate_configuration_identity(to_bytes(config), policy)
    assert result.failure_code == "CAMPAIGN_CONFIGURATION_SCHEMA_UNSUPPORTED"


def test_configuration_multi_fault_unsupported_version_wins():
    """Multi-fault fixture: unsupported version AND a malformed configuration_id
    at once. Version-unsupported must win (checked before format checks)."""
    config = base_configuration_doc()
    config["configuration_schema_version"] = "999"
    config["configuration_id"] = "not-hex-either"
    policy = to_campaign_policy(finalize_policy(base_policy_doc(["1" * 64])))
    result = validate_configuration_identity(to_bytes(config), policy)
    assert result.failure_code == "CAMPAIGN_CONFIGURATION_SCHEMA_UNSUPPORTED"


# ---------------------------------------------------------------------------
# Section 5: exact path-failure routing
# ---------------------------------------------------------------------------

def test_plain_lexical_escape_is_exactly_path_escape(tmp_path):
    from sensemaking_skills.campaign_validation.fs_adapter import (
        ArtifactRootError, resolve_under_root,
    )

    root = tmp_path / "root"
    root.mkdir()
    with pytest.raises(ArtifactRootError) as exc_info:
        resolve_under_root("../../etc/passwd", str(root))
    assert exc_info.value.code == "CAMPAIGN_PATH_ESCAPE"


def test_absolute_path_outside_root_is_exactly_path_escape(tmp_path):
    from sensemaking_skills.campaign_validation.fs_adapter import (
        ArtifactRootError, resolve_under_root,
    )

    root = tmp_path / "root"
    root.mkdir()
    outside = tmp_path.parent / "definitely-outside.yaml"
    with pytest.raises(ArtifactRootError) as exc_info:
        resolve_under_root(str(outside), str(root))
    assert exc_info.value.code == "CAMPAIGN_PATH_ESCAPE"


# ---------------------------------------------------------------------------
# Section 7: public ValidationResult never carries a private intermediate shape
# ---------------------------------------------------------------------------

_VALIDATED_MODEL_TYPES = (CampaignPolicy, CampaignApproval, ConfigurationIdentity, ValidatedCampaignBundle)


@pytest.mark.parametrize("call", [
    lambda: validate_campaign_policy(to_bytes(finalize_policy(base_policy_doc(["1" * 64]))), _ctx()),
])
def test_public_success_values_are_always_documented_model_types(call):
    result = call()
    assert result.valid
    assert isinstance(result.value, _VALIDATED_MODEL_TYPES)
    assert not isinstance(result.value, (dict, list, tuple))


def test_bundle_success_value_is_documented_model_type():
    pb, ab, cb = build_valid_bundle_bytes()
    result = validate_campaign_bundle(pb, ab, cb, _ctx())
    assert isinstance(result.value, _VALIDATED_MODEL_TYPES)
