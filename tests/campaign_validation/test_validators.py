"""Tests for validate_campaign_policy / validate_campaign_approval /
validate_configuration_identity / validate_campaign_bundle.
"""

from __future__ import annotations

import copy

import pytest

from sensemaking_skills.campaign_validation import (
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
    build_valid_bundle,
    build_valid_bundle_bytes,
    finalize_configuration,
    finalize_policy,
)
from .helpers import to_bytes

NOW = "2026-06-01T00:00:00+00:00"


def _ctx(**overrides):
    defaults = dict(current_time=NOW, allowed_approver_identities=frozenset({AUTHORIZED_APPROVER}))
    defaults.update(overrides)
    return ValidationContext(**defaults)


# --- Bundle happy path -------------------------------------------------------

def test_valid_bundle_produces_immutable_bundle_no_capability():
    pb, ab, cb = build_valid_bundle_bytes()
    result = validate_campaign_bundle(pb, ab, cb, _ctx())
    assert result.valid
    assert isinstance(result.value, ValidatedCampaignBundle)
    # Must be data only: no callable, no "authorized"/"token" attribute exists.
    assert not hasattr(result.value, "invoke")
    assert not hasattr(result.value, "authorization_token")
    assert not callable(result.value)


def test_invalid_bundle_returns_stable_code_not_exception():
    pb, ab, cb = build_valid_bundle_bytes()
    result = validate_campaign_bundle(b"not: valid: yaml: at all:\n", ab, cb, _ctx())
    assert not result.valid
    assert result.failure_code == "CAMPAIGN_POLICY_SOURCE_PROFILE_INVALID"


# --- Policy: source profile / schema -----------------------------------------

def test_policy_missing():
    result = validate_campaign_policy(None, _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_MISSING"


def test_policy_malformed_yaml():
    result = validate_campaign_policy(b"a: [1, 2\n", _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_SOURCE_PROFILE_INVALID"


def test_policy_unsupported_schema_version():
    doc = finalize_policy(base_policy_doc(["1" * 64]))
    doc["policy_schema_version"] = "2"
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_SCHEMA_UNSUPPORTED"


@pytest.mark.parametrize("field", [
    "campaign_id", "classification", "allowed_framework_shas", "allowed_targets",
    "allowed_models", "allowed_artifact_types", "allowed_configuration_ids",
    "max_attempt_slots", "validity_window", "target_mutation_prohibited",
    "preservation_requirements", "prepared_by", "prepared_at",
])
def test_policy_missing_required_field(field):
    doc = finalize_policy(base_policy_doc(["1" * 64]))
    del doc[field]
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_SCHEMA_INVALID"


def test_policy_unknown_top_level_field_rejected():
    doc = finalize_policy(base_policy_doc(["1" * 64]))
    doc["totally_unknown_field"] = "x"
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_SCHEMA_INVALID"


def test_policy_wrong_campaign_id_pattern():
    doc = finalize_policy(base_policy_doc(["1" * 64]))
    doc["campaign_id"] = "EVIDENCE-0016"
    doc["policy_digest"] = "0" * 64
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_SCHEMA_INVALID"


def test_policy_wrong_classification():
    doc = base_policy_doc(["1" * 64])
    doc["classification"] = "CANONICAL_EVIDENCE"
    doc = finalize_policy(doc)
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_SCHEMA_INVALID"


def test_policy_malformed_framework_sha():
    doc = base_policy_doc(["1" * 64])
    doc["allowed_framework_shas"] = ["not-a-sha"]
    doc = finalize_policy(doc)
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_SCHEMA_INVALID"


def test_policy_duplicate_configuration_ids_rejected():
    doc = base_policy_doc(["1" * 64, "1" * 64])
    doc = finalize_policy(doc)
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code in ("CAMPAIGN_POLICY_SCHEMA_INVALID", "CAMPAIGN_POLICY_LIMITS_INVALID")


def test_policy_unsorted_configuration_ids_rejected():
    doc = base_policy_doc(["2" * 64, "1" * 64])
    doc["allowed_configuration_ids"] = ["2" * 64, "1" * 64]  # deliberately unsorted
    doc = finalize_policy(doc)
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_LIMITS_INVALID"


# --- Policy digest ------------------------------------------------------------

def test_policy_digest_malformed():
    doc = base_policy_doc(["1" * 64])
    doc["policy_digest"] = "not-a-hex-digest"
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code in ("CAMPAIGN_POLICY_SCHEMA_INVALID", "CAMPAIGN_POLICY_DIGEST_MALFORMED")


def test_policy_digest_mismatch():
    doc = finalize_policy(base_policy_doc(["1" * 64]))
    doc["policy_digest"] = "f" * 64
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_DIGEST_MISMATCH"


# --- Policy limits --------------------------------------------------------

@pytest.mark.parametrize("field,value", [
    ("max_attempt_slots", 0),
    ("max_attempts_per_configuration", 0),
    ("concurrency_ceiling", 0),
])
def test_policy_limit_boundary_violations(field, value):
    doc = base_policy_doc(["1" * 64])
    doc[field] = value
    doc = finalize_policy(doc)
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    # The JSON Schema's own minimum constraint may catch this before the
    # cross-field limits check runs; either stable code is an acceptable
    # fail-closed outcome for a boundary the schema already expresses.
    assert result.failure_code in ("CAMPAIGN_POLICY_LIMITS_INVALID", "CAMPAIGN_POLICY_SCHEMA_INVALID")


def test_policy_max_invocations_exceeds_max_slots():
    doc = base_policy_doc(["1" * 64])
    doc["max_attempt_slots"] = 2
    doc["max_provider_invocations"] = 5
    doc = finalize_policy(doc)
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_LIMITS_INVALID"


@pytest.mark.parametrize("flag", [
    "target_mutation_prohibited", "fallback_prohibited",
    "repair_prohibited", "automatic_merge_prohibited",
])
def test_policy_prohibited_flag_must_be_true(flag):
    doc = base_policy_doc(["1" * 64])
    doc[flag] = False
    doc = finalize_policy(doc)
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code in ("CAMPAIGN_POLICY_SCHEMA_INVALID", "CAMPAIGN_POLICY_LIMITS_INVALID")


# --- Validity window --------------------------------------------------------

def test_policy_not_yet_valid():
    doc = base_policy_doc(["1" * 64])
    doc["validity_window"] = {
        "not_before": "2099-01-01T00:00:00+00:00",
        "not_after": "2100-01-01T00:00:00+00:00",
    }
    doc = finalize_policy(doc)
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_NOT_YET_VALID"


def test_policy_expired():
    doc = base_policy_doc(["1" * 64])
    doc["validity_window"] = {
        "not_before": "2020-01-01T00:00:00+00:00",
        "not_after": "2021-01-01T00:00:00+00:00",
    }
    doc = finalize_policy(doc)
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_EXPIRED"


def test_policy_validity_window_not_before_after_not_after():
    doc = base_policy_doc(["1" * 64])
    doc["validity_window"] = {
        "not_before": "2026-06-02T00:00:00+00:00",
        "not_after": "2026-06-01T00:00:00+00:00",
    }
    doc = finalize_policy(doc)
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_VALIDITY_WINDOW_INVALID"


def test_policy_valid_within_window():
    doc = finalize_policy(base_policy_doc(["1" * 64]))
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.valid


# --- Approval ---------------------------------------------------------------

def _valid_policy():
    return finalize_policy(base_policy_doc(["1" * 64]))


def test_approval_missing():
    policy = _valid_policy()
    result = validate_campaign_approval(None, policy, _ctx())
    assert result.failure_code == "CAMPAIGN_APPROVAL_MISSING"


def test_approval_example_marker_always_non_operative():
    policy = _valid_policy()
    approval = base_approval_doc(policy)
    approval["marker"] = "EXAMPLE_ONLY_NOT_AUTHORIZATION"
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert result.failure_code == "CAMPAIGN_APPROVAL_EXAMPLE_TEMPLATE_NON_OPERATIVE"


@pytest.mark.parametrize("field,placeholder", [
    ("claimed_approver_identity", "<HUMAN-FILLS-IN-EXACT-GITHUB-HANDLE>"),
    ("approval_statement", "<HUMAN-FILLS-IN first-person consent text>"),
])
def test_approval_placeholder_rejected(field, placeholder):
    policy = _valid_policy()
    approval = base_approval_doc(policy)
    approval[field] = placeholder
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert result.failure_code in (
        "CAMPAIGN_APPROVAL_PLACEHOLDER_PRESENT", "CAMPAIGN_APPROVER_UNAUTHORIZED",
    )


def test_approval_missing_statement():
    policy = _valid_policy()
    approval = base_approval_doc(policy)
    approval["approval_statement"] = ""
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert result.failure_code == "CAMPAIGN_APPROVAL_SCHEMA_INVALID"


def test_approval_digest_mismatch():
    policy = _valid_policy()
    approval = base_approval_doc(policy)
    approval["policy_digest"] = "f" * 64
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert result.failure_code == "CAMPAIGN_APPROVAL_POLICY_MISMATCH"


def test_approval_campaign_mismatch():
    policy = _valid_policy()
    approval = base_approval_doc(policy)
    approval["campaign_id"] = "EXP-9999-other"
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert result.failure_code == "CAMPAIGN_APPROVAL_POLICY_MISMATCH"


def test_approval_unauthorized_claimed_identity():
    policy = _valid_policy()
    approval = base_approval_doc(policy)
    approval["claimed_approver_identity"] = "some-random-unauthorized-identity"
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert result.failure_code == "CAMPAIGN_APPROVER_UNAUTHORIZED"


def test_approval_missing_provenance_mechanism():
    policy = _valid_policy()
    approval = base_approval_doc(policy)
    approval["approval_provenance"]["mechanism"] = "none"
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert result.failure_code == "CAMPAIGN_APPROVAL_PROVENANCE_INVALID"


def test_approval_structurally_valid_provenance_accepted_without_external_verification():
    """Phase 2 does not mechanically verify provenance -- a structurally
    valid, non-placeholder declaration is accepted; this test documents that
    boundary explicitly, honestly, without claiming authentication."""
    policy = _valid_policy()
    approval = base_approval_doc(policy)
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert result.valid


def test_approval_valid_operative_case():
    policy = _valid_policy()
    approval = base_approval_doc(policy)
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert result.valid


# --- Configuration identity --------------------------------------------------

def _policy_allowing(config_doc):
    return finalize_policy(base_policy_doc([config_doc["configuration_id"]]))


def test_configuration_missing():
    policy = _valid_policy()
    result = validate_configuration_identity(None, policy)
    assert result.failure_code == "CAMPAIGN_CONFIGURATION_MISSING"


def test_configuration_id_mismatch():
    config = finalize_configuration(base_configuration_doc())
    policy = _policy_allowing(config)
    config["configuration_id"] = "f" * 64
    result = validate_configuration_identity(to_bytes(config), policy)
    assert result.failure_code == "CAMPAIGN_CONFIGURATION_ID_MISMATCH"


def test_configuration_id_not_in_allowlist():
    config = finalize_configuration(base_configuration_doc())
    other_policy = finalize_policy(base_policy_doc(["9" * 64]))
    result = validate_configuration_identity(to_bytes(config), other_policy)
    assert result.failure_code == "CAMPAIGN_CONFIGURATION_ID_NOT_ALLOWED"


def test_configuration_framework_not_allowed_independently():
    """Every independent allowlist check fires even if configuration_id
    membership alone would otherwise appear to pass -- see 'Conjunctive
    authorization semantics' in campaign-policy.schema.md."""
    config = finalize_configuration(base_configuration_doc())
    policy = _policy_allowing(config)
    policy["allowed_framework_shas"] = ["d" * 40]
    policy = finalize_policy(policy)
    result = validate_configuration_identity(to_bytes(config), policy)
    assert result.failure_code == "CAMPAIGN_CONFIGURATION_FRAMEWORK_NOT_ALLOWED"


def test_configuration_target_not_allowed():
    config = finalize_configuration(base_configuration_doc())
    policy = _policy_allowing(config)
    policy["allowed_targets"] = [{"repository": "https://example.invalid/other/repo.git", "sha": "d" * 40}]
    policy = finalize_policy(policy)
    result = validate_configuration_identity(to_bytes(config), policy)
    assert result.failure_code == "CAMPAIGN_CONFIGURATION_TARGET_NOT_ALLOWED"


def test_configuration_model_not_allowed():
    config = finalize_configuration(base_configuration_doc())
    policy = _policy_allowing(config)
    policy["allowed_models"] = ["some-other-model"]
    policy = finalize_policy(policy)
    result = validate_configuration_identity(to_bytes(config), policy)
    assert result.failure_code == "CAMPAIGN_CONFIGURATION_MODEL_NOT_ALLOWED"


def test_configuration_artifact_type_not_allowed():
    config = finalize_configuration(base_configuration_doc())
    policy = _policy_allowing(config)
    policy["allowed_artifact_types"] = ["some_other_artifact_type"]
    policy = finalize_policy(policy)
    result = validate_configuration_identity(to_bytes(config), policy)
    assert result.failure_code == "CAMPAIGN_CONFIGURATION_ARTIFACT_TYPE_NOT_ALLOWED"


@pytest.mark.parametrize("mutable_ref", ["HEAD", "main", "master", "latest", "origin/main"])
def test_configuration_mutable_ref_rejected(mutable_ref):
    config = base_configuration_doc()
    config["framework_sha"] = mutable_ref
    config = finalize_configuration(config)
    policy = _policy_allowing(config)
    result = validate_configuration_identity(to_bytes(config), policy)
    assert not result.valid


def test_configuration_valid_case_passes_every_check():
    config = finalize_configuration(base_configuration_doc())
    policy = _policy_allowing(config)
    result = validate_configuration_identity(to_bytes(config), policy)
    assert result.valid


def test_configuration_nested_execution_parameters_remain_valid_and_hashed():
    config = base_configuration_doc()
    config["execution_parameters"]["nested"] = {"depth_one": {"depth_two": [1, 2, "x"]}}
    config = finalize_configuration(config)
    policy = _policy_allowing(config)
    result = validate_configuration_identity(to_bytes(config), policy)
    assert result.valid


# --- Integration: full bundle -----------------------------------------------

_FORBIDDEN_PROVIDER_IMPORTS = (
    "skill_executor", "gate_a_authorization", "anthropic", "openai", "provider_client",
)


def test_bundle_provider_not_imported():
    """The validation core must never import provider-invocation code.

    (``fs_adapter.py`` legitimately loads ``gate_a_authorization`` for its
    pure path-containment helpers -- that is a data/path utility, not a
    provider invocation boundary -- so it is exempted here explicitly and
    covered instead by the "no Gate A behavior change" assertions elsewhere.)
    """
    import ast
    from pathlib import Path

    package_dir = Path(__file__).resolve().parents[2] / "src" / "sensemaking_skills" / "campaign_validation"
    for py_file in package_dir.glob("*.py"):
        if py_file.name == "fs_adapter.py":
            continue
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            for name in names:
                assert not any(bad in name for bad in _FORBIDDEN_PROVIDER_IMPORTS), (
                    f"{py_file.name} imports provider-facing module {name!r}"
                )


def test_bundle_every_invalid_case_has_stable_code():
    pb, ab, cb = build_valid_bundle_bytes()
    result = validate_campaign_bundle(pb, None, cb, _ctx())
    assert result.failure_code == "CAMPAIGN_APPROVAL_MISSING"
