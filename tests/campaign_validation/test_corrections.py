"""Tests added while correcting blocking review findings on PR #125.

Covers: integer-lexeme source-form enforcement, exact numeric-domain
rejection (overflow/underflow/precision), campaign-binding enforcement,
deep immutability of ValidatedCampaignBundle, filesystem fail-closed
behavior, explicit-key detection (flow form), and stricter timestamp/
placeholder validation.
"""

from __future__ import annotations

import copy

import pytest

from sensemaking_skills.campaign_validation import (
    ValidationContext,
    validate_campaign_bundle,
    validate_campaign_policy,
    validate_configuration_identity,
)
from sensemaking_skills.campaign_validation.fs_adapter import ArtifactRootError
from sensemaking_skills.campaign_validation.immutable import freeze
from sensemaking_skills.campaign_validation.yaml_profile import (
    TwoLaneYamlError,
    parse_two_lane_yaml,
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
    to_campaign_policy,
)
from .helpers import to_bytes

NOW = "2026-06-01T00:00:00+00:00"


def _ctx(**overrides):
    defaults = dict(current_time=NOW, allowed_approver_identities=frozenset({AUTHORIZED_APPROVER}))
    defaults.update(overrides)
    return ValidationContext(**defaults)


# ---------------------------------------------------------------------------
# Section 1/2: integer-lexeme source form + exact numeric domain
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("field,lexeme", [
    ("max_attempt_slots", "5.0"),
    ("max_attempt_slots", "5e0"),
    ("max_attempt_slots", "5E+0"),
])
def test_policy_integer_field_rejects_float_lexeme_even_when_integral(field, lexeme):
    """The lexeme's MATHEMATICAL value (5) must exactly match what was
    hashed into policy_digest (base_policy_doc's default max_attempt_slots
    is 5) -- only its SOURCE FORM changes (int-lexeme '5' -> float-lexeme
    '5.0'/'5e0'/'5E+0'). Per ADR 0023, 5 and 5.0 canonicalize to the same
    JCS bytes, so this substitution does not change policy_digest; it
    isolates purely the source-form check under test, independent of the
    (separately tested) digest-integrity check.
    """
    doc = base_policy_doc(["1" * 64])
    assert doc[field] == 5
    doc = finalize_policy(doc)
    source = to_bytes(doc).decode()
    import re as _re
    source = _re.sub(rf"^{field}: .*$", f"{field}: {lexeme}", source, flags=_re.MULTILINE)
    result = validate_campaign_policy(source.encode(), _ctx())
    assert not result.valid
    assert result.failure_code == "CAMPAIGN_POLICY_LIMITS_INVALID"


def test_policy_integer_field_accepts_plain_integer_lexeme():
    doc = finalize_policy(base_policy_doc(["1" * 64]))
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert result.valid


def test_policy_max_attempt_slots_5_5_rejected():
    doc = base_policy_doc(["1" * 64])
    doc["max_attempt_slots"] = 5  # placeholder int so digest math works below
    doc = finalize_policy(doc)
    source = to_bytes(doc).decode()
    import re as _re
    source = _re.sub(r"^max_attempt_slots: .*$", "max_attempt_slots: 5.5", source, flags=_re.MULTILINE)
    result = validate_campaign_policy(source.encode(), _ctx())
    assert not result.valid


def test_policy_max_attempt_slots_quoted_string_rejected():
    doc = finalize_policy(base_policy_doc(["1" * 64]))
    source = to_bytes(doc).decode()
    import re as _re
    source = _re.sub(r"^max_attempt_slots: .*$", 'max_attempt_slots: "5"', source, flags=_re.MULTILINE)
    result = validate_campaign_policy(source.encode(), _ctx())
    assert not result.valid
    assert result.failure_code == "CAMPAIGN_POLICY_SCHEMA_INVALID"


def test_token_ceiling_rejects_float_lexeme_when_non_null():
    doc = base_policy_doc(["1" * 64])
    doc["token_ceiling"] = 100
    doc = finalize_policy(doc)
    source = to_bytes(doc).decode()
    import re as _re
    source = _re.sub(r"^token_ceiling: .*$", "token_ceiling: 100.0", source, flags=_re.MULTILINE)
    result = validate_campaign_policy(source.encode(), _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_LIMITS_INVALID"


@pytest.mark.parametrize("lexeme", ["0.1", "1.5", "1e3", "1e-7"])
def test_exact_numeric_domain_positive_controls(lexeme):
    parsed = parse_two_lane_yaml(f"a: {lexeme}\n".encode())
    assert isinstance(parsed["a"], float)


def test_exact_numeric_domain_overflow_rejected():
    with pytest.raises(TwoLaneYamlError) as exc_info:
        parse_two_lane_yaml(b"a: 1e9999\n")
    assert exc_info.value.code == "NUMERIC_OVERFLOW"


def test_exact_numeric_domain_underflow_rejected():
    with pytest.raises(TwoLaneYamlError) as exc_info:
        parse_two_lane_yaml(b"a: 1e-9999\n")
    assert exc_info.value.code == "NUMERIC_UNDERFLOW"


def test_exact_numeric_domain_precision_heavy_decimal_rejected():
    with pytest.raises(TwoLaneYamlError) as exc_info:
        parse_two_lane_yaml(b"a: 0.10000000000000001\n")
    assert exc_info.value.code == "NUMERIC_PRECISION_UNSUPPORTED"


def test_safe_integer_overflow_in_policy_field_fails_closed():
    """9007199254740992 (2**53) is outside the interoperable safe-integer
    domain for a policy limit field. It is even outside RFC 8785's own
    representable integer domain, so a real conforming policy could never
    carry a matching digest for it in the first place -- the point of this
    control is that the value fails closed one way or another (here: a
    digest that cannot be computed for it is never valid), never that it is
    silently accepted.
    """
    doc = base_policy_doc(["1" * 64])
    doc["max_attempt_slots"] = 9007199254740992  # 2**53, outside safe-integer domain
    doc["policy_digest"] = "0" * 64  # placeholder -- see docstring; cannot be a real digest
    result = validate_campaign_policy(to_bytes(doc), _ctx())
    assert not result.valid


# ---------------------------------------------------------------------------
# Section 4: configuration-to-campaign binding
# ---------------------------------------------------------------------------

def test_configuration_campaign_mismatch_fails_even_with_every_other_check_passing():
    """Every hashed field unchanged, configuration_id valid, every
    constituent allowlist passing -- only campaign_id differs. Must fail
    with CAMPAIGN_CONFIGURATION_CAMPAIGN_MISMATCH specifically, because
    campaign_id is excluded from the configuration_id hash and so cannot be
    caught any other way.
    """
    config = finalize_configuration(base_configuration_doc())
    policy = to_campaign_policy(finalize_policy(base_policy_doc([config["configuration_id"]])))

    mutated_config = copy.deepcopy(config)
    mutated_config["campaign_id"] = "EXP-9999-different-campaign"
    # configuration_id is NOT recomputed -- it must remain valid, since
    # campaign_id is excluded from the hash (this is the whole point).
    assert mutated_config["configuration_id"] == config["configuration_id"]

    result = validate_configuration_identity(to_bytes(mutated_config), policy)
    assert result.failure_code == "CAMPAIGN_CONFIGURATION_CAMPAIGN_MISMATCH"


def test_configuration_matching_campaign_id_passes():
    config = finalize_configuration(base_configuration_doc())
    policy = to_campaign_policy(finalize_policy(base_policy_doc([config["configuration_id"]])))
    result = validate_configuration_identity(to_bytes(config), policy)
    assert result.valid


# ---------------------------------------------------------------------------
# Section 5: deep immutability
# ---------------------------------------------------------------------------

def test_freeze_produces_immutable_mapping_and_tuple():
    original = {"a": [1, 2, {"b": "x"}], "c": {"d": 1}}
    frozen = freeze(original)
    with pytest.raises(TypeError):
        frozen["a"] = "mutated"
    with pytest.raises(TypeError):
        frozen["c"]["d"] = 999
    assert isinstance(frozen["a"], tuple)
    with pytest.raises((TypeError, AttributeError)):
        frozen["a"].append("mutated")
    assert isinstance(frozen["a"][2], type(frozen))  # nested mapping also frozen
    with pytest.raises(TypeError):
        frozen["a"][2]["b"] = "mutated"


def test_freeze_detaches_from_original_mutation():
    original = {"nested": {"x": 1}}
    frozen = freeze(original)
    original["nested"]["x"] = 999
    original["nested"]["y"] = "new"
    assert frozen["nested"]["x"] == 1
    assert "y" not in frozen["nested"]


def test_validated_bundle_raw_mappings_are_immutable_at_every_level():
    pb, ab, cb = build_valid_bundle_bytes()
    result = validate_campaign_bundle(pb, ab, cb, _ctx())
    assert result.valid
    bundle = result.value

    with pytest.raises(TypeError):
        bundle.policy.raw["campaign_id"] = "EXP-9999-tampered"
    with pytest.raises(TypeError):
        bundle.approval.raw["claimed_approver_identity"] = "someone-else"
    with pytest.raises(TypeError):
        bundle.configuration.raw["execution_parameters"]["max_tokens_hint"] = 999999
    with pytest.raises(TypeError):
        bundle.policy.raw["allowed_targets"][0]["sha"] = "f" * 40


def test_mutating_original_parsed_dict_does_not_alter_bundle():
    policy_doc, approval_doc, config_doc = build_valid_bundle()
    pb, ab, cb = to_bytes(policy_doc), to_bytes(approval_doc), to_bytes(config_doc)
    result = validate_campaign_bundle(pb, ab, cb, _ctx())
    assert result.valid
    original_campaign_id = result.value.policy.raw["campaign_id"]

    # Mutate the ORIGINAL source dict after validation -- must not reach
    # the already-returned bundle (freeze() copies, it does not view).
    policy_doc["campaign_id"] = "EXP-0000-mutated"
    policy_doc["allowed_targets"][0]["sha"] = "f" * 40

    assert result.value.policy.raw["campaign_id"] == original_campaign_id
    assert result.value.policy.raw["allowed_targets"][0]["sha"] != "f" * 40


# ---------------------------------------------------------------------------
# Section 7: filesystem fail-closed
# ---------------------------------------------------------------------------

def test_load_candidates_wraps_read_permission_error(tmp_path, monkeypatch):
    from sensemaking_skills.campaign_validation import load_and_validate_policy_from_root

    target = tmp_path / "policy.yaml"
    target.write_text("a: 1\n", encoding="utf-8")

    import sensemaking_skills.campaign_validation.validators as validators_mod

    def _boom(path):
        raise ArtifactRootError("CAMPAIGN_FILESYSTEM_ERROR", "simulated permission denied")

    monkeypatch.setattr(validators_mod, "read_utf8_bytes", _boom)
    result = load_and_validate_policy_from_root(str(tmp_path), ["policy.yaml"], _ctx())
    assert result.failure_code == "CAMPAIGN_FILESYSTEM_ERROR"


def test_load_candidates_directory_replacing_file(tmp_path):
    from sensemaking_skills.campaign_validation import load_and_validate_policy_from_root

    (tmp_path / "policy.yaml").mkdir()  # a directory, not a file
    result = load_and_validate_policy_from_root(str(tmp_path), ["policy.yaml"], _ctx())
    # is_file() is False for a directory -> treated as "candidate not present",
    # not a crash; zero matches -> missing.
    assert result.failure_code == "CAMPAIGN_POLICY_MISSING"


def test_load_candidates_malformed_utf8(tmp_path):
    from sensemaking_skills.campaign_validation import load_and_validate_policy_from_root

    (tmp_path / "policy.yaml").write_bytes(b"\xff\xfe\x00bad")
    result = load_and_validate_policy_from_root(str(tmp_path), ["policy.yaml"], _ctx())
    assert result.failure_code == "CAMPAIGN_POLICY_SOURCE_PROFILE_INVALID"


# ---------------------------------------------------------------------------
# Section 8: explicit-key flow-form detection
# ---------------------------------------------------------------------------

def test_explicit_key_flow_form_rejected():
    with pytest.raises(TwoLaneYamlError) as exc_info:
        parse_two_lane_yaml(b'{? campaign_id: "value"}\n')
    assert exc_info.value.code == "EXPLICIT_KEY_FORBIDDEN"


def test_question_mark_inside_quoted_string_not_rejected():
    parsed = parse_two_lane_yaml(b'a: "is this ok?"\n')
    assert parsed == {"a": "is this ok?"}


def test_question_mark_inside_comment_not_rejected():
    parsed = parse_two_lane_yaml(b"a: 1  # what about this ?\n")
    assert parsed == {"a": 1}


def test_normal_flow_mapping_accepted():
    parsed = parse_two_lane_yaml(b'{a: 1, b: "x"}\n')
    assert parsed == {"a": 1, "b": "x"}


# ---------------------------------------------------------------------------
# Section 10: timestamps + placeholders
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("bad_timestamp", [
    "2026-13-01T00:00:00+00:00",  # invalid month
    "2026-01-32T00:00:00+00:00",  # invalid day
    "2026-01-01T25:00:00+00:00",  # invalid hour
    "2026-01-01T00:61:00+00:00",  # invalid minute
])
def test_invalid_approval_timestamp_rejected(bad_timestamp):
    policy_doc = finalize_policy(base_policy_doc(["1" * 64]))
    policy = to_campaign_policy(policy_doc)
    approval = base_approval_doc(policy_doc)
    approval["approved_at"] = bad_timestamp
    from sensemaking_skills.campaign_validation import validate_campaign_approval
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert not result.valid


@pytest.mark.parametrize("placeholder", ["pending", "PENDING", "Tbd", "n/a", "N/A", "changeme"])
def test_lowercase_and_mixed_case_human_placeholder_rejected_exact_code(placeholder):
    policy_doc = finalize_policy(base_policy_doc(["1" * 64]))
    policy = to_campaign_policy(policy_doc)
    approval = base_approval_doc(policy_doc)
    approval["claimed_approver_identity"] = placeholder
    from sensemaking_skills.campaign_validation import validate_campaign_approval
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert result.failure_code == "CAMPAIGN_APPROVAL_PLACEHOLDER_PRESENT"


def test_legitimate_prose_containing_placeholder_word_not_misclassified():
    """'None of my objections remain' is genuine prose, not a placeholder --
    the exact-whole-value rule must not misfire on a longer sentence that
    merely starts with a sentinel word."""
    policy_doc = finalize_policy(base_policy_doc(["1" * 64]))
    policy = to_campaign_policy(policy_doc)
    approval = base_approval_doc(policy_doc)
    approval["approval_statement"] = "None of my objections remain; I approve this policy."
    from sensemaking_skills.campaign_validation import validate_campaign_approval
    result = validate_campaign_approval(to_bytes(approval), policy, _ctx())
    assert result.valid
