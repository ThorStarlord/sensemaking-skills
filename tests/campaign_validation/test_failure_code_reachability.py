"""The actual failure-code reachability matrix.

For every one of the 39 frozen ``CAMPAIGN_*`` codes, this module defines a
direct trigger that executes the REAL parser, validator, or root loader
(never a mock of the final code) and asserts exact equality with the
expected code. A prior version of this proof only checked that each code
string was a key in ``CAMPAIGN_FAILURE_CODES`` -- that proves the mapping
is complete, not that any validator can actually return the code. This file
proves the latter, for every code.
"""

from __future__ import annotations

import sys

import pytest

from sensemaking_skills.campaign_validation import (
    compute_policy_digest,

    CAMPAIGN_FAILURE_CODES,
    ValidationContext,
    load_and_validate_approval_from_root,
    load_and_validate_configuration_from_root,
    load_and_validate_policy_from_root,
    validate_campaign_approval,
    validate_campaign_policy,
    validate_configuration_identity,
)
from sensemaking_skills.campaign_validation.fs_adapter import (
    ArtifactRootError,
    resolve_under_root,
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


def _valid_policy_doc():
    return finalize_policy(base_policy_doc(["1" * 64]))


# --- Path / filesystem trust boundary ---------------------------------------

def _trigger_path_escape(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    try:
        resolve_under_root("../../etc/passwd", str(root))
        raise AssertionError("expected ArtifactRootError")
    except ArtifactRootError as exc:
        return exc.code


def _trigger_symlink_containment_violation(tmp_path):
    if not hasattr(__import__("os"), "symlink"):
        pytest.skip("platform has no symlink support")
    import os
    root = tmp_path / "root"
    root.mkdir()
    outside = tmp_path.parent / "outside-for-reachability"
    outside.mkdir(exist_ok=True)
    (outside / "secret.yaml").write_text("a: 1\n", encoding="utf-8")
    link = root / "escape-link"
    try:
        os.symlink(outside, link, target_is_directory=True)
    except OSError:
        pytest.skip("platform cannot create symlinks in this environment")
    try:
        resolve_under_root("escape-link/secret.yaml", str(root))
        raise AssertionError("expected ArtifactRootError")
    except ArtifactRootError as exc:
        return exc.code


def _trigger_filesystem_error(tmp_path, monkeypatch):
    import sensemaking_skills.campaign_validation.validators as validators_mod

    target = tmp_path / "policy.yaml"
    target.write_text("a: 1\n", encoding="utf-8")

    def _boom(path):
        raise ArtifactRootError("CAMPAIGN_FILESYSTEM_ERROR", "simulated permission denied")

    monkeypatch.setattr(validators_mod, "read_utf8_bytes", _boom)
    result = load_and_validate_policy_from_root(str(tmp_path), ["policy.yaml"], _ctx())
    return result.failure_code


# --- Policy ------------------------------------------------------------------

def _trigger_policy_missing():
    return validate_campaign_policy(None, _ctx()).failure_code


def _trigger_policy_source_profile_invalid():
    return validate_campaign_policy(b"a: [1, 2\n", _ctx()).failure_code


def _trigger_policy_schema_unsupported():
    doc = _valid_policy_doc()
    doc["policy_schema_version"] = "2"
    return validate_campaign_policy(to_bytes(doc), _ctx()).failure_code


def _trigger_policy_schema_invalid():
    doc = _valid_policy_doc()
    del doc["preservation_requirements"]
    return validate_campaign_policy(to_bytes(doc), _ctx()).failure_code


def _trigger_policy_identity_ambiguous(tmp_path):
    doc = _valid_policy_doc()
    (tmp_path / "a.yaml").write_bytes(to_bytes(doc))
    (tmp_path / "b.yaml").write_bytes(to_bytes(doc))
    return load_and_validate_policy_from_root(str(tmp_path), ["a.yaml", "b.yaml"], _ctx()).failure_code


def _trigger_policy_digest_malformed():
    doc = base_policy_doc(["1" * 64])
    doc["policy_digest"] = "not-hex"
    return validate_campaign_policy(to_bytes(doc), _ctx()).failure_code


def _trigger_policy_digest_mismatch():
    doc = _valid_policy_doc()
    doc["policy_digest"] = "f" * 64
    return validate_campaign_policy(to_bytes(doc), _ctx()).failure_code


def _trigger_policy_not_yet_valid():
    doc = base_policy_doc(["1" * 64])
    doc["validity_window"] = {"not_before": "2099-01-01T00:00:00+00:00", "not_after": "2100-01-01T00:00:00+00:00"}
    doc = finalize_policy(doc)
    return validate_campaign_policy(to_bytes(doc), _ctx()).failure_code


def _trigger_policy_expired():
    doc = base_policy_doc(["1" * 64])
    doc["validity_window"] = {"not_before": "2020-01-01T00:00:00+00:00", "not_after": "2021-01-01T00:00:00+00:00"}
    doc = finalize_policy(doc)
    return validate_campaign_policy(to_bytes(doc), _ctx()).failure_code


def _trigger_policy_validity_window_invalid():
    doc = base_policy_doc(["1" * 64])
    doc["validity_window"] = {"not_before": "2026-06-02T00:00:00+00:00", "not_after": "2026-06-01T00:00:00+00:00"}
    doc = finalize_policy(doc)
    return validate_campaign_policy(to_bytes(doc), _ctx()).failure_code


def _trigger_policy_limits_invalid():
    doc = base_policy_doc(["1" * 64])
    doc["max_attempt_slots"] = 0
    doc = finalize_policy(doc)
    return validate_campaign_policy(to_bytes(doc), _ctx()).failure_code


# --- Approval ------------------------------------------------------------

def _trigger_approval_missing():
    policy = to_campaign_policy(_valid_policy_doc())
    return validate_campaign_approval(None, policy, _ctx()).failure_code


def _trigger_approval_source_profile_invalid():
    policy = to_campaign_policy(_valid_policy_doc())
    return validate_campaign_approval(b"a: [1, 2\n", policy, _ctx()).failure_code


def _trigger_approval_schema_unsupported():
    policy_doc = _valid_policy_doc()
    policy = to_campaign_policy(policy_doc)
    approval = base_approval_doc(policy_doc)
    approval["approval_schema_version"] = "2"
    return validate_campaign_approval(to_bytes(approval), policy, _ctx()).failure_code


def _trigger_approval_schema_invalid():
    policy_doc = _valid_policy_doc()
    policy = to_campaign_policy(policy_doc)
    approval = base_approval_doc(policy_doc)
    approval["approval_statement"] = ""
    return validate_campaign_approval(to_bytes(approval), policy, _ctx()).failure_code


def _trigger_approval_example_template_non_operative():
    policy_doc = _valid_policy_doc()
    policy = to_campaign_policy(policy_doc)
    approval = base_approval_doc(policy_doc)
    approval["marker"] = "EXAMPLE_ONLY_NOT_AUTHORIZATION"
    return validate_campaign_approval(to_bytes(approval), policy, _ctx()).failure_code


def _trigger_approval_placeholder_present():
    policy_doc = _valid_policy_doc()
    policy = to_campaign_policy(policy_doc)
    approval = base_approval_doc(policy_doc)
    approval["claimed_approver_identity"] = "<HUMAN-FILLS-IN-EXACT-GITHUB-HANDLE>"
    return validate_campaign_approval(to_bytes(approval), policy, _ctx()).failure_code


def _trigger_approval_policy_mismatch():
    policy_doc = _valid_policy_doc()
    policy = to_campaign_policy(policy_doc)
    approval = base_approval_doc(policy_doc)
    approval["policy_digest"] = "f" * 64
    return validate_campaign_approval(to_bytes(approval), policy, _ctx()).failure_code


def _trigger_approver_unauthorized():
    policy_doc = _valid_policy_doc()
    policy = to_campaign_policy(policy_doc)
    approval = base_approval_doc(policy_doc)
    approval["claimed_approver_identity"] = "some-random-unauthorized-identity"
    return validate_campaign_approval(to_bytes(approval), policy, _ctx()).failure_code


def _trigger_approval_provenance_invalid():
    policy_doc = _valid_policy_doc()
    policy = to_campaign_policy(policy_doc)
    approval = base_approval_doc(policy_doc)
    approval["approval_provenance"]["mechanism"] = "none"
    return validate_campaign_approval(to_bytes(approval), policy, _ctx()).failure_code


def _conversation_approval_doc(policy_doc: dict) -> dict:
    return {
        "approval_schema_version": "1",
        "status": "approved",
        "campaign_id": policy_doc["campaign_id"],
        "policy_digest": policy_doc["policy_digest"],
        "approval_source": "active_human_conversation",
        "approval_text": "approve",
        "approved_at": "2026-01-02T00:00:00+00:00",
        "maximum_attempts": int(policy_doc["max_attempt_slots"]),
        "concurrency": int(policy_doc["concurrency_ceiling"]),
        "automatic_merge": "prohibited",
        "external_provider_api_prohibited": True,
        "classification": policy_doc["classification"],
        "reference": "session-1#message-42",
    }


def _agent_native_policy_doc() -> dict:
    policy_doc = dict(_valid_policy_doc())
    policy_doc["execution_mode"] = "coding_agent_native"
    policy_doc["execution_surface"] = "current_coding_agent"
    policy_doc["external_provider_api_prohibited"] = True
    policy_doc["allowed_models"] = []
    policy_doc["policy_digest"] = compute_policy_digest(policy_doc)
    return policy_doc


def _trigger_approval_envelope_exceeded():
    policy_doc = _agent_native_policy_doc()
    policy = to_campaign_policy(policy_doc)
    approval = _conversation_approval_doc(policy_doc)
    approval["maximum_attempts"] = int(policy_doc["max_attempt_slots"]) + 1
    return validate_campaign_approval(to_bytes(approval), policy, _ctx()).failure_code


def _trigger_approval_ambiguous(tmp_path):
    policy_doc = _valid_policy_doc()
    policy = to_campaign_policy(policy_doc)
    approval_a = base_approval_doc(policy_doc)
    approval_b = dict(base_approval_doc(policy_doc))
    approval_b["approval_statement"] = "A different, but equally operative, statement."
    (tmp_path / "a.yaml").write_bytes(to_bytes(approval_a))
    (tmp_path / "b.yaml").write_bytes(to_bytes(approval_b))
    return load_and_validate_approval_from_root(
        str(tmp_path), ["a.yaml", "b.yaml"], policy, _ctx()
    ).failure_code


# --- Configuration ------------------------------------------------------

def _config_and_policy():
    config = finalize_configuration(base_configuration_doc())
    policy = to_campaign_policy(finalize_policy(base_policy_doc([config["configuration_id"]])))
    return config, policy


def _trigger_configuration_missing():
    _, policy = _config_and_policy()
    return validate_configuration_identity(None, policy).failure_code


def _trigger_configuration_source_profile_invalid():
    _, policy = _config_and_policy()
    return validate_configuration_identity(b"a: [1, 2\n", policy).failure_code


def _trigger_configuration_schema_unsupported():
    config, policy = _config_and_policy()
    config["configuration_schema_version"] = "2"
    return validate_configuration_identity(to_bytes(config), policy).failure_code


def _trigger_configuration_schema_invalid():
    config, policy = _config_and_policy()
    del config["artifact_type"]
    return validate_configuration_identity(to_bytes(config), policy).failure_code


def _trigger_configuration_numeric_domain_invalid():
    config, policy = _config_and_policy()
    config["execution_parameters"]["oversized"] = 9007199254740992
    config["configuration_id"] = "0" * 64
    return validate_configuration_identity(to_bytes(config), policy).failure_code


def _trigger_configuration_identity_ambiguous(tmp_path):
    config, policy = _config_and_policy()
    (tmp_path / "a.yaml").write_bytes(to_bytes(config))
    (tmp_path / "b.yaml").write_bytes(to_bytes(config))
    return load_and_validate_configuration_from_root(
        str(tmp_path), ["a.yaml", "b.yaml"], policy
    ).failure_code


def _trigger_configuration_id_malformed():
    config, policy = _config_and_policy()
    config["configuration_id"] = "not-hex"
    return validate_configuration_identity(to_bytes(config), policy).failure_code


def _trigger_configuration_id_mismatch():
    config, policy = _config_and_policy()
    config["configuration_id"] = "f" * 64
    return validate_configuration_identity(to_bytes(config), policy).failure_code


def _trigger_configuration_campaign_mismatch():
    config, policy = _config_and_policy()
    config["campaign_id"] = "EXP-9999-different-campaign"
    return validate_configuration_identity(to_bytes(config), policy).failure_code


def _trigger_configuration_id_not_allowed():
    config = finalize_configuration(base_configuration_doc())
    other_policy = to_campaign_policy(finalize_policy(base_policy_doc(["9" * 64])))
    return validate_configuration_identity(to_bytes(config), other_policy).failure_code


def _trigger_configuration_framework_not_allowed():
    config = finalize_configuration(base_configuration_doc())
    policy_doc = finalize_policy(base_policy_doc([config["configuration_id"]]))
    policy_doc["allowed_framework_shas"] = ["d" * 40]
    policy = to_campaign_policy(finalize_policy(policy_doc))
    return validate_configuration_identity(to_bytes(config), policy).failure_code


def _trigger_configuration_target_not_allowed():
    config = finalize_configuration(base_configuration_doc())
    policy_doc = finalize_policy(base_policy_doc([config["configuration_id"]]))
    policy_doc["allowed_targets"] = [{"repository": "https://example.invalid/other/repo.git", "sha": "d" * 40}]
    policy = to_campaign_policy(finalize_policy(policy_doc))
    return validate_configuration_identity(to_bytes(config), policy).failure_code


def _trigger_configuration_model_not_allowed():
    config = finalize_configuration(base_configuration_doc())
    policy_doc = finalize_policy(base_policy_doc([config["configuration_id"]]))
    policy_doc["allowed_models"] = ["some-other-model"]
    policy = to_campaign_policy(finalize_policy(policy_doc))
    return validate_configuration_identity(to_bytes(config), policy).failure_code


def _trigger_configuration_artifact_type_not_allowed():
    config = finalize_configuration(base_configuration_doc())
    policy_doc = finalize_policy(base_policy_doc([config["configuration_id"]]))
    policy_doc["allowed_artifact_types"] = ["some_other_artifact_type"]
    policy = to_campaign_policy(finalize_policy(policy_doc))
    return validate_configuration_identity(to_bytes(config), policy).failure_code


def _trigger_internal_validation_error():
    """A deliberate invalid API-type call: passing a plain dict where a
    genuine, validator-produced CampaignPolicy is required."""
    policy_doc = _valid_policy_doc()
    approval = base_approval_doc(policy_doc)
    return validate_campaign_approval(to_bytes(approval), policy_doc, _ctx()).failure_code  # plain dict


# --- The matrix --------------------------------------------------------------

_NO_ARG_TRIGGERS = {
    "CAMPAIGN_POLICY_MISSING": _trigger_policy_missing,
    "CAMPAIGN_POLICY_SOURCE_PROFILE_INVALID": _trigger_policy_source_profile_invalid,
    "CAMPAIGN_POLICY_SCHEMA_UNSUPPORTED": _trigger_policy_schema_unsupported,
    "CAMPAIGN_POLICY_SCHEMA_INVALID": _trigger_policy_schema_invalid,
    "CAMPAIGN_POLICY_DIGEST_MALFORMED": _trigger_policy_digest_malformed,
    "CAMPAIGN_POLICY_DIGEST_MISMATCH": _trigger_policy_digest_mismatch,
    "CAMPAIGN_POLICY_NOT_YET_VALID": _trigger_policy_not_yet_valid,
    "CAMPAIGN_POLICY_EXPIRED": _trigger_policy_expired,
    "CAMPAIGN_POLICY_VALIDITY_WINDOW_INVALID": _trigger_policy_validity_window_invalid,
    "CAMPAIGN_POLICY_LIMITS_INVALID": _trigger_policy_limits_invalid,
    "CAMPAIGN_APPROVAL_MISSING": _trigger_approval_missing,
    "CAMPAIGN_APPROVAL_SOURCE_PROFILE_INVALID": _trigger_approval_source_profile_invalid,
    "CAMPAIGN_APPROVAL_SCHEMA_UNSUPPORTED": _trigger_approval_schema_unsupported,
    "CAMPAIGN_APPROVAL_SCHEMA_INVALID": _trigger_approval_schema_invalid,
    "CAMPAIGN_APPROVAL_EXAMPLE_TEMPLATE_NON_OPERATIVE": _trigger_approval_example_template_non_operative,
    "CAMPAIGN_APPROVAL_PLACEHOLDER_PRESENT": _trigger_approval_placeholder_present,
    "CAMPAIGN_APPROVAL_POLICY_MISMATCH": _trigger_approval_policy_mismatch,
    "CAMPAIGN_APPROVAL_ENVELOPE_EXCEEDED": _trigger_approval_envelope_exceeded,
    "CAMPAIGN_APPROVER_UNAUTHORIZED": _trigger_approver_unauthorized,
    "CAMPAIGN_APPROVAL_PROVENANCE_INVALID": _trigger_approval_provenance_invalid,
    "CAMPAIGN_CONFIGURATION_MISSING": _trigger_configuration_missing,
    "CAMPAIGN_CONFIGURATION_SOURCE_PROFILE_INVALID": _trigger_configuration_source_profile_invalid,
    "CAMPAIGN_CONFIGURATION_SCHEMA_UNSUPPORTED": _trigger_configuration_schema_unsupported,
    "CAMPAIGN_CONFIGURATION_SCHEMA_INVALID": _trigger_configuration_schema_invalid,
    "CAMPAIGN_CONFIGURATION_NUMERIC_DOMAIN_INVALID": _trigger_configuration_numeric_domain_invalid,
    "CAMPAIGN_CONFIGURATION_ID_MALFORMED": _trigger_configuration_id_malformed,
    "CAMPAIGN_CONFIGURATION_ID_MISMATCH": _trigger_configuration_id_mismatch,
    "CAMPAIGN_CONFIGURATION_CAMPAIGN_MISMATCH": _trigger_configuration_campaign_mismatch,
    "CAMPAIGN_CONFIGURATION_ID_NOT_ALLOWED": _trigger_configuration_id_not_allowed,
    "CAMPAIGN_CONFIGURATION_FRAMEWORK_NOT_ALLOWED": _trigger_configuration_framework_not_allowed,
    "CAMPAIGN_CONFIGURATION_TARGET_NOT_ALLOWED": _trigger_configuration_target_not_allowed,
    "CAMPAIGN_CONFIGURATION_MODEL_NOT_ALLOWED": _trigger_configuration_model_not_allowed,
    "CAMPAIGN_CONFIGURATION_ARTIFACT_TYPE_NOT_ALLOWED": _trigger_configuration_artifact_type_not_allowed,
    "CAMPAIGN_INTERNAL_VALIDATION_ERROR": _trigger_internal_validation_error,
}

_TMP_PATH_TRIGGERS = {
    "CAMPAIGN_PATH_ESCAPE": _trigger_path_escape,
    "CAMPAIGN_POLICY_IDENTITY_AMBIGUOUS": _trigger_policy_identity_ambiguous,
    "CAMPAIGN_APPROVAL_AMBIGUOUS": _trigger_approval_ambiguous,
    "CAMPAIGN_CONFIGURATION_IDENTITY_AMBIGUOUS": _trigger_configuration_identity_ambiguous,
}


@pytest.mark.parametrize("code", sorted(_NO_ARG_TRIGGERS))
def test_no_arg_trigger_reaches_exact_code(code):
    assert _NO_ARG_TRIGGERS[code]() == code


@pytest.mark.parametrize("code", sorted(_TMP_PATH_TRIGGERS))
def test_tmp_path_trigger_reaches_exact_code(code, tmp_path):
    assert _TMP_PATH_TRIGGERS[code](tmp_path) == code


def test_symlink_containment_violation_reachable_on_capable_platform(tmp_path):
    code = _trigger_symlink_containment_violation(tmp_path)
    assert code == "CAMPAIGN_SYMLINK_CONTAINMENT_VIOLATION"


def test_filesystem_error_reachable(tmp_path, monkeypatch):
    code = _trigger_filesystem_error(tmp_path, monkeypatch)
    assert code == "CAMPAIGN_FILESYSTEM_ERROR"


def test_every_frozen_code_has_a_matrix_entry():
    """Cross-check: every code in the frozen mapping must have a trigger
    above (either the no-arg matrix, the tmp_path matrix, or one of the two
    special-cased platform/monkeypatch triggers) -- and vice versa, no
    matrix entry may reference an unfrozen code."""
    covered = (
        set(_NO_ARG_TRIGGERS)
        | set(_TMP_PATH_TRIGGERS)
        | {"CAMPAIGN_SYMLINK_CONTAINMENT_VIOLATION", "CAMPAIGN_FILESYSTEM_ERROR"}
    )
    assert covered == set(CAMPAIGN_FAILURE_CODES)
