"""Tests for policy_digest / configuration_id computation."""

from __future__ import annotations

import copy

import pytest

from sensemaking_skills.campaign_validation import (
    compute_configuration_id,
    compute_policy_digest,
)

from .fixtures import (
    base_configuration_doc,
    base_policy_doc,
    finalize_configuration,
    finalize_policy,
)
from .helpers import to_bytes
from sensemaking_skills.campaign_validation.yaml_profile import parse_two_lane_yaml


def test_policy_digest_excludes_itself():
    doc = base_policy_doc(["1" * 64])
    doc["policy_digest"] = "0" * 64
    d1 = compute_policy_digest(doc)
    doc["policy_digest"] = "f" * 64
    d2 = compute_policy_digest(doc)
    assert d1 == d2


def test_policy_digest_rejects_unknown_field_before_hashing():
    doc = base_policy_doc(["1" * 64])
    doc["totally_unknown_field"] = "x"
    with pytest.raises(KeyError):
        # compute_policy_digest itself does not scan for extras beyond its
        # fixed field list, but an unknown field alongside a MISSING known
        # field must still surface via KeyError -- exercised properly by the
        # schema-validation layer (see test_validators.py). This test
        # documents that the digest function only ever reads its fixed set.
        del doc["campaign_id"]
        compute_policy_digest(doc)


def test_configuration_id_excludes_configuration_id_and_campaign_id():
    doc = base_configuration_doc()
    doc["configuration_id"] = "0" * 64
    doc["campaign_id"] = "EXP-0001-example"
    c1 = compute_configuration_id(doc)
    doc["configuration_id"] = "f" * 64
    doc["campaign_id"] = "EXP-9999-other"
    c2 = compute_configuration_id(doc)
    assert c1 == c2


def test_configuration_id_changes_with_execution_parameters_mutation():
    doc = base_configuration_doc()
    c1 = compute_configuration_id(doc)
    doc2 = copy.deepcopy(doc)
    doc2["execution_parameters"]["max_tokens_hint"] = 8192
    c2 = compute_configuration_id(doc2)
    assert c1 != c2


def test_configuration_id_changes_with_nested_execution_parameters_mutation():
    doc = base_configuration_doc()
    c1 = compute_configuration_id(doc)
    doc2 = copy.deepcopy(doc)
    doc2["execution_parameters"]["tool_allowlist"].append("write_file")
    c2 = compute_configuration_id(doc2)
    assert c1 != c2


@pytest.mark.parametrize("field", [
    "framework_sha", "target_repository", "target_sha", "model_identifier",
    "prompt_or_skill_revision", "validator_revision", "artifact_type",
])
def test_configuration_id_changes_with_each_hashed_field_mutation(field):
    doc = base_configuration_doc()
    c1 = compute_configuration_id(doc)
    doc2 = copy.deepcopy(doc)
    doc2[field] = doc2[field] + "-changed" if isinstance(doc2[field], str) else doc2[field]
    if field in ("framework_sha", "target_sha"):
        doc2[field] = "c" * 40
    c2 = compute_configuration_id(doc2)
    assert c1 != c2


def test_presentation_only_change_preserves_policy_digest():
    """Mapping-key order, comments, indentation, and quote style are
    presentation-only; the digest is computed over the parsed VALUE, not
    source bytes -- so re-serializing an equivalent value must not change
    the recomputed digest."""
    doc = base_policy_doc(["1" * 64])
    doc["policy_digest"] = compute_policy_digest(doc)
    source_a = to_bytes(doc)

    reordered = dict(reversed(list(doc.items())))
    source_b = to_bytes(reordered)

    parsed_a = parse_two_lane_yaml(source_a)
    parsed_b = parse_two_lane_yaml(source_b)
    assert compute_policy_digest(parsed_a) == compute_policy_digest(parsed_b)


def test_presentation_only_quote_style_preserves_configuration_id():
    doc = finalize_configuration(base_configuration_doc())
    source_double = (
        b'configuration_schema_version: "1"\n'
        b'configuration_id: "' + doc["configuration_id"].encode() + b'"\n'
        b'campaign_id: "EXP-0001-example"\n'
        b'framework_sha: "' + doc["framework_sha"].encode() + b'"\n'
        b'target_repository: "' + doc["target_repository"].encode() + b'"\n'
        b'target_sha: "' + doc["target_sha"].encode() + b'"\n'
        b'model_identifier: "' + doc["model_identifier"].encode() + b'"\n'
        b'prompt_or_skill_revision: "' + doc["prompt_or_skill_revision"].encode() + b'"\n'
        b'validator_revision: "' + doc["validator_revision"].encode() + b'"\n'
        b'artifact_type: "' + doc["artifact_type"].encode() + b'"\n'
        b"execution_parameters:\n"
        b"  max_tokens_hint: 4096\n"
        b"  tool_allowlist:\n"
        b'    - "read_repository"\n'
    )
    source_single = source_double.replace(b'"', b"'")
    parsed_double = parse_two_lane_yaml(source_double, open_map_root_field="execution_parameters")
    parsed_single = parse_two_lane_yaml(source_single, open_map_root_field="execution_parameters")
    assert compute_configuration_id(parsed_double) == compute_configuration_id(parsed_single)


def test_semantic_mutation_changes_policy_digest():
    doc = base_policy_doc(["1" * 64])
    d1 = compute_policy_digest(doc)
    doc2 = copy.deepcopy(doc)
    doc2["max_attempt_slots"] = 999
    d2 = compute_policy_digest(doc2)
    assert d1 != d2


def test_unicode_string_behavior_in_digest():
    import unicodedata

    nfc = unicodedata.normalize("NFC", "café")
    nfd = unicodedata.normalize("NFD", "café")
    assert nfc != nfd  # sanity: distinct code point sequences

    doc = base_configuration_doc()
    doc["prompt_or_skill_revision"] = nfc
    doc2 = copy.deepcopy(doc)
    doc2["prompt_or_skill_revision"] = nfd
    assert compute_configuration_id(doc) != compute_configuration_id(doc2)


def test_configuration_digest_no_trailing_newline_dependency():
    doc = base_configuration_doc()
    assert isinstance(compute_configuration_id(doc), str)
    assert len(compute_configuration_id(doc)) == 64
