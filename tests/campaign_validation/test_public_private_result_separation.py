"""Proves public ValidationResult.value never carries a private intermediate
shape (a plain dict, list, or tuple of candidates) -- only the documented
validated model union.
"""

from __future__ import annotations

from sensemaking_skills.campaign_validation import (
    CampaignApproval,
    CampaignPolicy,
    ConfigurationIdentity,
    ValidatedCampaignBundle,
    ValidationContext,
    validate_campaign_approval,
    validate_campaign_bundle,
    validate_campaign_policy,
    validate_configuration_identity,
)

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
_MODEL_UNION = (CampaignPolicy, CampaignApproval, ConfigurationIdentity, ValidatedCampaignBundle)


def _ctx():
    return ValidationContext(current_time=NOW, allowed_approver_identities=frozenset({AUTHORIZED_APPROVER}))


def test_policy_success_value_is_never_a_dict_list_or_tuple():
    doc = finalize_policy(base_policy_doc(["1" * 64]))
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.valid
    assert isinstance(result.value, _MODEL_UNION)
    assert not isinstance(result.value, (dict, list, tuple))


def test_approval_success_value_is_never_a_dict_list_or_tuple():
    policy_doc = finalize_policy(base_policy_doc(["1" * 64]))
    policy = to_campaign_policy(policy_doc)
    approval = base_approval_doc(policy_doc)
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert result.valid
    assert isinstance(result.value, _MODEL_UNION)
    assert not isinstance(result.value, (dict, list, tuple))


def test_configuration_success_value_is_never_a_dict_list_or_tuple():
    config = finalize_configuration(base_configuration_doc())
    policy = to_campaign_policy(finalize_policy(base_policy_doc([config["configuration_id"]])))
    result = validate_configuration_identity(to_bytes(config), policy)
    assert result.valid
    assert isinstance(result.value, _MODEL_UNION)
    assert not isinstance(result.value, (dict, list, tuple))


def test_bundle_success_value_is_never_a_dict_list_or_tuple():
    pb, ab, cb = build_valid_bundle_bytes()
    result = validate_campaign_bundle(pb, ab, cb, _ctx())
    assert result.valid
    assert isinstance(result.value, _MODEL_UNION)
    assert not isinstance(result.value, (dict, list, tuple))


def test_internal_result_type_is_not_part_of_the_public_api():
    import sensemaking_skills.campaign_validation as pkg

    assert not hasattr(pkg, "_InternalResult")
    assert "_InternalResult" not in pkg.__all__
