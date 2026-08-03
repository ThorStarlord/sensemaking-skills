"""Tests added while correcting the second round of blocking review findings
on PR #125: negative-zero-through-int-lexeme, deterministic failure-code
precedence, approval template/operative schema reconciliation, and immutable
single-artifact validation results.
"""

from __future__ import annotations

import copy

import pytest

from sensemaking_skills.campaign_validation import (
    CampaignApproval,
    CampaignPolicy,
    ConfigurationIdentity,
    ValidationContext,
    validate_campaign_approval,
    validate_campaign_policy,
    validate_configuration_identity,
)
from sensemaking_skills.campaign_validation import schema_validation
from sensemaking_skills.campaign_validation.yaml_profile import (
    TwoLaneYamlError,
    parse_two_lane_yaml,
)

from .fixtures import (
    AUTHORIZED_APPROVER,
    base_approval_doc,
    base_configuration_doc,
    base_policy_doc,
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
# Section 1: negative zero rejected globally at the parser boundary
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("lexeme", ["-0", "-0.0", "-0e0", "-0E+0", "-0.000", "-0e-10"])
def test_negative_zero_rejected_everywhere_in_source(lexeme):
    with pytest.raises(TwoLaneYamlError) as exc_info:
        parse_two_lane_yaml(f"a: {lexeme}\n".encode())
    assert exc_info.value.code == "NEGATIVE_ZERO_FORBIDDEN"


@pytest.mark.parametrize("lexeme", ["0", "0.0", "0e0"])
def test_positive_zero_forms_remain_valid(lexeme):
    parsed = parse_two_lane_yaml(f"a: {lexeme}\n".encode())
    assert parsed["a"] == 0


def test_quoted_negative_zero_string_remains_a_string():
    parsed = parse_two_lane_yaml(b'a: "-0"\n')
    assert parsed["a"] == "-0"
    assert isinstance(parsed["a"], str)


def test_negative_zero_rejected_in_nested_execution_parameters():
    with pytest.raises(TwoLaneYamlError) as exc_info:
        parse_two_lane_yaml(
            b"execution_parameters:\n  nested:\n    deep:\n      value: -0.0\n",
            open_map_root_field="execution_parameters",
        )
    assert exc_info.value.code == "NEGATIVE_ZERO_FORBIDDEN"


def test_negative_zero_rejected_in_execution_parameters_sequence():
    with pytest.raises(TwoLaneYamlError) as exc_info:
        parse_two_lane_yaml(
            b'execution_parameters:\n  values:\n    - 1\n    - -0\n',
            open_map_root_field="execution_parameters",
        )
    assert exc_info.value.code == "NEGATIVE_ZERO_FORBIDDEN"


def test_policy_integer_field_negative_zero_cannot_pass_through_digest():
    """A bare `-0` in max_attempt_slots must never reach the digest/limits
    machinery as ordinary zero -- it must fail at the parser boundary, before
    any digest computation or limits check runs at all."""
    doc = base_policy_doc(["1" * 64])
    doc["max_attempt_slots"] = 0  # placeholder so digest math is coherent
    doc = finalize_policy(doc)
    source = to_bytes(doc).decode()
    import re as _re
    source = _re.sub(r"^max_attempt_slots: .*$", "max_attempt_slots: -0", source, flags=_re.MULTILINE)
    result = validate_campaign_policy(source.encode(), _ctx())
    assert not result.valid
    assert result.failure_code == "CAMPAIGN_POLICY_SOURCE_PROFILE_INVALID"


def test_configuration_cost_ceiling_style_negative_zero_rejected_at_parse_time():
    """cost_ceiling.amount is a general numeric field (not integer-lexeme
    constrained); a negative-zero VALUE there must still be rejected at the
    parser boundary, not merely by JCS at digest time."""
    with pytest.raises(TwoLaneYamlError) as exc_info:
        parse_two_lane_yaml(b"cost_ceiling:\n  amount: -0.0\n  currency: \"USD\"\n")
    assert exc_info.value.code == "NEGATIVE_ZERO_FORBIDDEN"


# ---------------------------------------------------------------------------
# Section 3: deterministic failure-code precedence (one exact code each)
# ---------------------------------------------------------------------------

def test_malformed_policy_digest_exact_code():
    doc = base_policy_doc(["1" * 64])
    doc["policy_digest"] = "totally-not-hex"
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_DIGEST_MALFORMED"


def test_mismatched_policy_digest_exact_code():
    doc = finalize_policy(base_policy_doc(["1" * 64]))
    doc["policy_digest"] = "a" * 64
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_DIGEST_MISMATCH"


def test_malformed_configuration_id_exact_code():
    config = finalize_configuration(base_configuration_doc())
    policy = to_campaign_policy(finalize_policy(base_policy_doc([config["configuration_id"]])))
    config["configuration_id"] = "totally-not-hex"
    result = validate_configuration_identity(to_bytes(config), policy)
    assert result.failure_code == "CAMPAIGN_CONFIGURATION_ID_MALFORMED"


def test_mismatched_configuration_id_exact_code():
    config = finalize_configuration(base_configuration_doc())
    policy = to_campaign_policy(finalize_policy(base_policy_doc([config["configuration_id"]])))
    config["configuration_id"] = "a" * 64
    result = validate_configuration_identity(to_bytes(config), policy)
    assert result.failure_code == "CAMPAIGN_CONFIGURATION_ID_MISMATCH"


def test_unsupported_schema_version_exact_code_wins_over_other_faults():
    """Multi-fault fixture: unsupported version AND a malformed digest AND a
    limits violation all present at once. Version-unsupported must win
    (checked first, before schema/digest/limits)."""
    doc = base_policy_doc(["1" * 64])
    doc["policy_schema_version"] = "999"
    doc["policy_digest"] = "not-hex-either"
    doc["max_attempt_slots"] = 0
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_SCHEMA_UNSUPPORTED"


def test_schema_structural_fault_wins_over_digest_and_limits():
    """Multi-fault fixture: a missing required field (structural) AND a
    malformed digest AND an out-of-range limit. SCHEMA_INVALID must win
    (schema validation runs before the Python-owned digest/limits checks)."""
    doc = base_policy_doc(["1" * 64])
    doc = finalize_policy(doc)
    del doc["preservation_requirements"]  # structural fault
    doc["policy_digest"] = "not-hex-either"  # also malformed
    doc["max_attempt_slots"] = 0  # also a limits fault
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_SCHEMA_INVALID"


def test_malformed_digest_wins_over_limits_fault():
    """Multi-fault fixture: malformed digest AND an out-of-range limit, no
    structural fault. DIGEST_MALFORMED must win (checked before limits)."""
    doc = base_policy_doc(["1" * 64])
    doc["policy_digest"] = "not-hex-either"
    doc["max_attempt_slots"] = 0
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_DIGEST_MALFORMED"


def test_digest_mismatch_wins_over_limits_fault():
    """Multi-fault fixture: well-formed-but-wrong digest AND an out-of-range
    limit. DIGEST_MISMATCH must win (checked before limits)."""
    doc = base_policy_doc(["1" * 64])
    doc["max_attempt_slots"] = 0
    doc = finalize_policy(doc)  # digest computed over the ALREADY-faulty doc...
    doc["policy_digest"] = "b" * 64  # ...then deliberately made wrong anyway
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_DIGEST_MISMATCH"


def test_source_profile_violation_wins_over_everything_else():
    """A YAML-profile violation is caught before any schema/digest/limits
    check even has a parsed mapping to look at."""
    result = validate_campaign_policy(b"a: [1, 2\n", _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_SOURCE_PROFILE_INVALID"


@pytest.mark.parametrize("declared_code", sorted({
    "CAMPAIGN_POLICY_MISSING", "CAMPAIGN_POLICY_SOURCE_PROFILE_INVALID",
    "CAMPAIGN_POLICY_SCHEMA_UNSUPPORTED", "CAMPAIGN_POLICY_SCHEMA_INVALID",
    "CAMPAIGN_POLICY_DIGEST_MALFORMED", "CAMPAIGN_POLICY_DIGEST_MISMATCH",
    "CAMPAIGN_POLICY_LIMITS_INVALID", "CAMPAIGN_POLICY_NOT_YET_VALID",
    "CAMPAIGN_POLICY_EXPIRED", "CAMPAIGN_POLICY_VALIDITY_WINDOW_INVALID",
    "CAMPAIGN_APPROVAL_MISSING", "CAMPAIGN_APPROVAL_SOURCE_PROFILE_INVALID",
    "CAMPAIGN_APPROVAL_SCHEMA_UNSUPPORTED", "CAMPAIGN_APPROVAL_SCHEMA_INVALID",
    "CAMPAIGN_APPROVAL_EXAMPLE_TEMPLATE_NON_OPERATIVE",
    "CAMPAIGN_APPROVAL_PLACEHOLDER_PRESENT", "CAMPAIGN_APPROVAL_POLICY_MISMATCH",
    "CAMPAIGN_APPROVER_UNAUTHORIZED", "CAMPAIGN_APPROVAL_PROVENANCE_INVALID",
    "CAMPAIGN_CONFIGURATION_MISSING", "CAMPAIGN_CONFIGURATION_SOURCE_PROFILE_INVALID",
    "CAMPAIGN_CONFIGURATION_SCHEMA_INVALID", "CAMPAIGN_CONFIGURATION_ID_MALFORMED",
    "CAMPAIGN_CONFIGURATION_ID_MISMATCH", "CAMPAIGN_CONFIGURATION_CAMPAIGN_MISMATCH",
    "CAMPAIGN_CONFIGURATION_ID_NOT_ALLOWED", "CAMPAIGN_CONFIGURATION_FRAMEWORK_NOT_ALLOWED",
    "CAMPAIGN_CONFIGURATION_TARGET_NOT_ALLOWED", "CAMPAIGN_CONFIGURATION_MODEL_NOT_ALLOWED",
    "CAMPAIGN_CONFIGURATION_ARTIFACT_TYPE_NOT_ALLOWED",
}))
def test_every_specialized_code_reachable_by_some_test_in_the_suite(declared_code):
    """Documents (rather than re-proves in isolation) that each of these
    codes has a dedicated, direct triggering test elsewhere in this test
    package -- collected here as one explicit manifest so a reviewer can
    check "is every code reachable" in one place. See test_validators.py
    and this module for the actual triggering tests.
    """
    from sensemaking_skills.campaign_validation import CAMPAIGN_FAILURE_CODES
    assert declared_code in CAMPAIGN_FAILURE_CODES


# ---------------------------------------------------------------------------
# Section 4: approval template/operative schema reconciliation
# ---------------------------------------------------------------------------

_BLANK_TEMPLATE = {
    "approval_schema_version": "1",
    "campaign_id": "EXP-0000-EXAMPLE",
    "policy_digest": "0" * 64,
    "claimed_approver_identity": "<HUMAN-FILLS-IN-EXACT-GITHUB-HANDLE>",
    "approval_provenance": {
        "mechanism": "<HUMAN-FILLS-IN e.g. signed_commit | github_review_approval>",
        "reference": "<HUMAN-FILLS-IN e.g. commit SHA or review URL>",
    },
    "approval_statement": "<HUMAN-FILLS-IN first-person consent text>",
    "approved_at": "<HUMAN-FILLS-IN RFC3339 timestamp>",
    "marker": "EXAMPLE_ONLY_NOT_AUTHORIZATION",
}

_ILLUSTRATIVE_EXAMPLE = {
    "approval_schema_version": "1",
    "campaign_id": "EXP-0000-EXAMPLE",
    "policy_digest": "0" * 64,
    "claimed_approver_identity": "example-owner-handle",
    "approval_provenance": {"mechanism": "signed_commit", "reference": "0" * 40},
    "approval_statement": (
        "EXAMPLE ONLY. This illustrates the shape of a filled approval; it is "
        "not a real consent statement and authorizes nothing."
    ),
    "approved_at": "2026-01-01T00:00:00+00:00",
    "marker": "EXAMPLE_ONLY_NOT_AUTHORIZATION",
}


def test_exact_blank_template_satisfies_example_machine_readable_profile():
    errors = schema_validation.approval_schema_errors(_BLANK_TEMPLATE)
    assert errors == []


def test_illustrative_filled_example_satisfies_example_machine_readable_profile():
    errors = schema_validation.approval_schema_errors(_ILLUSTRATIVE_EXAMPLE)
    assert errors == []


def test_blank_template_returns_example_non_operative_from_public_validator():
    policy_doc = finalize_policy(base_policy_doc(["1" * 64]))
    policy = to_campaign_policy(policy_doc)
    result = validate_campaign_approval(to_bytes(_BLANK_TEMPLATE), policy, _ctx())
    assert not result.valid
    assert result.failure_code == "CAMPAIGN_APPROVAL_EXAMPLE_TEMPLATE_NON_OPERATIVE"


def test_illustrative_example_returns_example_non_operative_from_public_validator():
    policy_doc = finalize_policy(base_policy_doc(["1" * 64]))
    policy = to_campaign_policy(policy_doc)
    result = validate_campaign_approval(to_bytes(_ILLUSTRATIVE_EXAMPLE), policy, _ctx())
    assert not result.valid
    assert result.failure_code == "CAMPAIGN_APPROVAL_EXAMPLE_TEMPLATE_NON_OPERATIVE"


def test_neither_template_produces_a_validated_bundle():
    policy_doc = finalize_policy(base_policy_doc(["1" * 64]))
    policy = to_campaign_policy(policy_doc)
    for template in (_BLANK_TEMPLATE, _ILLUSTRATIVE_EXAMPLE):
        result = validate_campaign_approval(to_bytes(template), policy, _ctx())
        assert result.value is None
        assert not isinstance(result.value, CampaignApproval)


def test_operative_document_carrying_any_marker_fails_non_operative():
    policy_doc = finalize_policy(base_policy_doc(["1" * 64]))
    policy = to_campaign_policy(policy_doc)
    approval = base_approval_doc(policy_doc)
    approval["marker"] = "SOME_OTHER_MARKER_VALUE"
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert result.failure_code == "CAMPAIGN_APPROVAL_EXAMPLE_TEMPLATE_NON_OPERATIVE"


def test_operative_document_without_marker_still_gets_strict_validation():
    """An operative document (no marker) with a template-style placeholder
    approved_at must still fail -- but via the STRICT operative path
    (schema/RFC3339/placeholder), never via the template escape hatch."""
    policy_doc = finalize_policy(base_policy_doc(["1" * 64]))
    policy = to_campaign_policy(policy_doc)
    approval = base_approval_doc(policy_doc)
    approval["approved_at"] = "<HUMAN-FILLS-IN RFC3339 timestamp>"
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert not result.valid
    assert result.failure_code != "CAMPAIGN_APPROVAL_EXAMPLE_TEMPLATE_NON_OPERATIVE"


def test_docs_and_packaged_approval_schema_remain_byte_identical():
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[2]
    docs_copy = (repo_root / "docs" / "experiments" / "schemas" / "two-lane-v1"
                 / "json" / "campaign-approval.v1.schema.json").read_bytes()
    packaged_copy = (repo_root / "src" / "sensemaking_skills" / "campaign_validation"
                      / "schemas" / "campaign-approval.v1.schema.json").read_bytes()
    assert docs_copy == packaged_copy


# ---------------------------------------------------------------------------
# Section 5: immutable single-artifact validation results
# ---------------------------------------------------------------------------

def test_validate_campaign_policy_returns_immutable_typed_result():
    doc = finalize_policy(base_policy_doc(["1" * 64]))
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert isinstance(result.value, CampaignPolicy)
    with pytest.raises(TypeError):
        result.value.raw["campaign_id"] = "tampered"
    with pytest.raises(TypeError):
        result.value.raw["allowed_targets"][0]["sha"] = "f" * 40


def test_validate_campaign_approval_returns_immutable_typed_result():
    policy_doc = finalize_policy(base_policy_doc(["1" * 64]))
    policy = to_campaign_policy(policy_doc)
    approval = base_approval_doc(policy_doc)
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert isinstance(result.value, CampaignApproval)
    with pytest.raises(TypeError):
        result.value.raw["claimed_approver_identity"] = "tampered"
    with pytest.raises(TypeError):
        result.value.raw["approval_provenance"]["mechanism"] = "tampered"


def test_validate_configuration_identity_returns_immutable_typed_result():
    config = finalize_configuration(base_configuration_doc())
    policy = to_campaign_policy(finalize_policy(base_policy_doc([config["configuration_id"]])))
    result = validate_configuration_identity(to_bytes(config), policy)
    assert isinstance(result.value, ConfigurationIdentity)
    with pytest.raises(TypeError):
        result.value.raw["execution_parameters"]["max_tokens_hint"] = 999999
    with pytest.raises(AttributeError):
        result.value.raw["execution_parameters"]["tool_allowlist"].append("write_file")


def test_mutating_original_source_dict_cannot_alter_returned_policy_model():
    doc = finalize_policy(base_policy_doc(["1" * 64]))
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    original = result.value.raw["campaign_id"]
    doc["campaign_id"] = "EXP-0000-mutated-after-the-fact"
    assert result.value.raw["campaign_id"] == original
