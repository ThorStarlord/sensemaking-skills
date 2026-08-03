"""Tests for the Two-Lane YAML Profile v1 parser (source-token + composed-node layers)."""

from __future__ import annotations

import pytest

from sensemaking_skills.campaign_validation.yaml_profile import (
    TwoLaneYamlError,
    parse_two_lane_yaml,
)


def _err(source: str) -> TwoLaneYamlError:
    with pytest.raises(TwoLaneYamlError) as exc_info:
        parse_two_lane_yaml(source.encode("utf-8"))
    return exc_info.value


# --- Layer A: source-token rejections -------------------------------------

def test_anchor_rejected():
    assert _err("a: &anchor 1\nb: 2\n").code == "ANCHOR_FORBIDDEN"


def test_alias_rejected_even_with_matching_anchor():
    assert _err("a: &anchor 1\nb: *anchor\n").code == "ANCHOR_FORBIDDEN"


def test_bare_alias_with_no_anchor_definition_is_independently_rejected():
    """The alias token itself must be caught, not merely an earlier anchor
    rejection incidentally satisfying the assertion (deferred Phase 1 test,
    promoted here per the spec)."""
    result = _err("a: *undefined_alias\n")
    assert result.code == "ALIAS_FORBIDDEN"


def test_explicit_standard_tag_rejected():
    assert _err('a: !!str "1"\n').code == "TAG_FORBIDDEN"


def test_explicit_custom_tag_rejected():
    assert _err("a: !mytag value\n").code in ("TAG_FORBIDDEN", "MALFORMED_YAML")


def test_yaml_11_directive_rejected():
    assert _err("%YAML 1.1\n---\na: 1\n").code == "YAML_VERSION_FORBIDDEN"


def test_yaml_12_directive_permitted():
    parsed = parse_two_lane_yaml(b"%YAML 1.2\n---\na: 1\n")
    assert parsed == {"a": 1}


def test_tag_directive_rejected():
    assert _err("%TAG ! tag:example.com,2000:\n---\na: 1\n").code == "DIRECTIVE_FORBIDDEN"


def test_merge_key_rejected_via_key_grammar():
    err = _err('"<<": "x"\n')
    assert err.code in ("QUOTED_KEY_FORBIDDEN", "MAPPING_KEY_GRAMMAR_VIOLATION")


def test_complex_key_forbidden():
    err = _err("? [a, b]\n: 1\n")
    assert err.code in ("EXPLICIT_KEY_FORBIDDEN", "COMPLEX_KEY_FORBIDDEN", "MALFORMED_YAML")


def test_duplicate_keys_rejected():
    assert _err("a: 1\na: 2\n").code == "DUPLICATE_KEY_FORBIDDEN"


def test_block_literal_scalar_rejected():
    assert _err("a: |\n  hello\n  world\n").code == "BLOCK_SCALAR_FORBIDDEN"


def test_block_folded_scalar_rejected():
    assert _err("a: >\n  hello\n  world\n").code == "BLOCK_SCALAR_FORBIDDEN"


def test_multiline_double_quoted_scalar_rejected():
    assert _err('a: "line one\nline two"\n').code == "MULTILINE_QUOTED_SCALAR_FORBIDDEN"


def test_multiline_single_quoted_scalar_rejected():
    assert _err("a: 'line one\nline two'\n").code == "MULTILINE_QUOTED_SCALAR_FORBIDDEN"


def test_multiple_documents_rejected():
    assert _err("a: 1\n---\nb: 2\n").code == "MULTIPLE_DOCUMENTS_FORBIDDEN"


def test_malformed_yaml_rejected():
    assert _err("a: [1, 2\n").code == "MALFORMED_YAML"


def test_empty_document_rejected():
    assert _err("").code == "EMPTY_DOCUMENT"
    assert _err("   \n").code == "EMPTY_DOCUMENT"


def test_root_not_mapping_rejected():
    with pytest.raises(TwoLaneYamlError) as exc_info:
        parse_two_lane_yaml(b"- 1\n- 2\n")
    assert exc_info.value.code == "ROOT_NOT_MAPPING"


# --- Layer B: scalar resolution --------------------------------------------

@pytest.mark.parametrize("source,expected", [
    ('a: "yes"\n', "yes"),
    ('a: "on"\n', "on"),
    ('a: "01"\n', "01"),
    ('a: "2026-01-01"\n', "2026-01-01"),
    ("a: true\n", True),
    ("a: false\n", False),
    ("a: null\n", None),
    ("a: 0\n", 0),
    ("a: -1\n", -1),
    ("a: 1.5\n", 1.5),
    ("a: 1e3\n", 1000.0),
    ('a: "1"\n', "1"),
])
def test_conformance_table_accepted(source, expected):
    assert parse_two_lane_yaml(source.encode())["a"] == expected


@pytest.mark.parametrize("bad_scalar", [
    "yes", "no", "on", "off", "Yes", "No", "True", "False", "TRUE", "FALSE",
    "Null", "NULL", "~", "01", "-01", "0o7", "0x10", "+1", ".5", "1.",
    ".inf", "-.inf", ".nan", "2026-01-01",
])
def test_conformance_table_rejected_plain_scalars(bad_scalar):
    err = _err(f"a: {bad_scalar}\n")
    assert err.code in ("PLAIN_SCALAR_FORBIDDEN", "MALFORMED_YAML")


def test_quoting_style_does_not_affect_string_value():
    single = parse_two_lane_yaml(b"a: 'hello'\n")
    double = parse_two_lane_yaml(b'a: "hello"\n')
    assert single == double == {"a": "hello"}


def test_integral_1_0_and_1e0_are_positive_controls():
    assert parse_two_lane_yaml(b"a: 1.0\n")["a"] == 1.0
    assert parse_two_lane_yaml(b"a: 1e0\n")["a"] == 1.0
    assert parse_two_lane_yaml(b"a: 1\n")["a"] == 1
    assert parse_two_lane_yaml(b"a: 1.0\n")["a"] == parse_two_lane_yaml(b"a: 1e0\n")["a"] == 1


def test_negative_zero_rejected():
    assert _err("a: -0.0\n").code == "NEGATIVE_ZERO_FORBIDDEN"


# --- Mapping key grammar ----------------------------------------------------

def test_unquoted_ascii_key_accepted():
    assert parse_two_lane_yaml(b"campaign_id: \"x\"\n") == {"campaign_id": "x"}


def test_quoted_key_rejected():
    assert _err('"campaign_id": "x"\n').code == "QUOTED_KEY_FORBIDDEN"


@pytest.mark.parametrize("bad_key", ["Campaign_Id", "1abc", "abc-def", "abc def", "ABC"])
def test_malformed_key_rejected(bad_key):
    err = _err(f'{bad_key}: "x"\n')
    assert err.code in ("MAPPING_KEY_GRAMMAR_VIOLATION", "MALFORMED_YAML")


@pytest.mark.parametrize("reserved", ["true", "false", "null", "yes", "no", "on", "off"])
def test_reserved_key_rejected(reserved):
    assert _err(f'{reserved}: "x"\n').code == "RESERVED_KEY_FORBIDDEN"


def test_unicode_key_rejected():
    err = _err('café: "x"\n')
    assert err.code in ("MAPPING_KEY_GRAMMAR_VIOLATION", "MALFORMED_YAML")


# --- Open-map subtree (execution_parameters) --------------------------------

def test_open_map_subtree_permits_arbitrary_nested_structure():
    source = (
        b'execution_parameters:\n'
        b'  max_tokens_hint: 4096\n'
        b'  nested:\n'
        b'    inner_flag: true\n'
        b'  items:\n'
        b'    - "a"\n'
        b'    - nested_in_seq: 1\n'
    )
    parsed = parse_two_lane_yaml(source, open_map_root_field="execution_parameters")
    assert parsed["execution_parameters"]["nested"]["inner_flag"] is True
    assert parsed["execution_parameters"]["items"][1]["nested_in_seq"] == 1


def test_open_map_subtree_still_forbids_reserved_and_malformed_keys():
    source = b'execution_parameters:\n  true: 1\n'
    err = _err_with_open(source)
    assert err.code == "RESERVED_KEY_FORBIDDEN"


def _err_with_open(source_bytes: bytes) -> TwoLaneYamlError:
    with pytest.raises(TwoLaneYamlError) as exc_info:
        parse_two_lane_yaml(source_bytes, open_map_root_field="execution_parameters")
    return exc_info.value


def test_open_map_subtree_still_forbids_duplicate_keys():
    source = b'execution_parameters:\n  a: 1\n  nested:\n    x: 1\n    x: 2\n'
    assert _err_with_open(source).code == "DUPLICATE_KEY_FORBIDDEN"


def test_non_bytes_input_rejected():
    with pytest.raises(TwoLaneYamlError) as exc_info:
        parse_two_lane_yaml("a: 1\n")  # str, not bytes
    assert exc_info.value.code == "SOURCE_NOT_BYTES"


def test_invalid_utf8_rejected():
    with pytest.raises(TwoLaneYamlError) as exc_info:
        parse_two_lane_yaml(b"\xff\xfe\x00a: 1")
    assert exc_info.value.code == "INVALID_UTF8"
