"""RFC 8785 (JCS) canonicalization tests, including reference number vectors."""

from __future__ import annotations

import math

import pytest

from sensemaking_skills.campaign_validation.jcs import (
    JCSError,
    canonicalize,
    canonicalize_bytes,
)


@pytest.mark.parametrize(
    "value,expected",
    [
        (0, "0"),
        (0.0, "0"),
        (1, "1"),
        (1.0, "1"),
        (1e0, "1"),
        (-1, "-1"),
        (-1.0, "-1"),
        (1.5, "1.5"),
        (1000.0, "1000"),
        (1e3, "1000"),
        (1e21, "1e+21"),
        (1e-6, "0.000001"),
        (1e-7, "1e-7"),
        (1e20, "100000000000000000000"),
        (0.1, "0.1"),
        (2.5, "2.5"),
        (3.0, "3"),
        (123.456, "123.456"),
    ],
)
def test_number_canonicalization_reference_vectors(value, expected):
    assert canonicalize(value) == expected


def test_integer_and_float_equivalents_canonicalize_identically():
    assert canonicalize(1) == canonicalize(1.0) == canonicalize(1e0)
    assert canonicalize(5) == canonicalize(5.0)


def test_semantic_change_alters_canonical_form():
    assert canonicalize(1.5) != canonicalize(1.6)


def test_non_finite_numbers_rejected():
    with pytest.raises(JCSError):
        canonicalize(float("nan"))
    with pytest.raises(JCSError):
        canonicalize(float("inf"))
    with pytest.raises(JCSError):
        canonicalize(float("-inf"))


def test_negative_zero_rejected():
    with pytest.raises(JCSError):
        canonicalize(-0.0)


def test_object_keys_sorted_lexicographically():
    assert canonicalize({"b": 1, "a": 2}) == '{"a":2,"b":1}'


def test_array_order_preserved():
    assert canonicalize([3, 1, 2]) == "[3,1,2]"


def test_string_escaping():
    assert canonicalize("a\"b\\c\nd") == '"a\\"b\\\\c\\nd"'


def test_no_trailing_newline_in_bytes():
    payload = canonicalize_bytes({"a": 1})
    assert not payload.endswith(b"\n")
    assert payload == b'{"a":1}'


def test_presentation_order_does_not_affect_canonical_bytes():
    a = canonicalize_bytes({"x": 1, "y": 2})
    b = canonicalize_bytes({"y": 2, "x": 1})
    assert a == b


def test_unicode_string_preserved_without_normalization():
    nfc = "é"  # e-acute, precomposed
    nfd = "é"  # e + combining acute
    assert canonicalize(nfc) != canonicalize(nfd)


def test_unsupported_type_rejected():
    with pytest.raises(JCSError):
        canonicalize(object())


def test_bool_is_not_treated_as_number():
    assert canonicalize(True) == "true"
    assert canonicalize(False) == "false"


# --- Maintained rfc8785 dependency: additional conformance vectors ---------

def test_safe_integer_boundary_accepted():
    assert canonicalize(9007199254740991) == "9007199254740991"
    assert canonicalize(-9007199254740991) == "-9007199254740991"


def test_integer_beyond_safe_domain_rejected():
    with pytest.raises(JCSError):
        canonicalize(9007199254740992)
    with pytest.raises(JCSError):
        canonicalize(2**60)


def test_utf16_key_ordering_outside_bmp():
    """RFC 8785 orders object keys by their UTF-16 code-unit sequence, not by
    Unicode code point. An astral-plane character (encoded as a UTF-16
    surrogate pair, code units >= 0xD800) sorts differently than a
    code-point-only comparison would place it relative to a BMP character
    in the private-use area near 0xFFFF. This is exactly the class of bug a
    naive ``sorted(keys)`` (Python code-point order) gets wrong and the
    maintained ``rfc8785`` dependency gets right.
    """
    astral = "\U00010000"  # U+10000, first astral-plane code point
    bmp_high = "￿"    # last BMP code point
    # Code-point order: astral (0x10000) > bmp_high (0xFFFF) -> "bmp_high" first.
    # UTF-16 order: astral encodes as surrogate pair starting 0xD800, which is
    # LESS than 0xFFFF -> astral-keyed entry sorts FIRST under UTF-16 rules.
    payload = canonicalize({bmp_high: 1, astral: 2})
    first_key_pos = payload.index('"')
    # The astral character's key must appear before the BMP-high key's.
    assert payload.find(astral.encode("unicode_escape").decode()) == -1  # sanity: not literally embedded as escape
    # Simplest robust assertion: compare against rfc8785 directly to confirm
    # child conformance, and independently confirm code-point order would
    # have produced the opposite result.
    import rfc8785 as _ref
    assert canonicalize_bytes({bmp_high: 1, astral: 2}) == _ref.dumps({bmp_high: 1, astral: 2})
    codepoint_order_keys = sorted([bmp_high, astral])
    utf16_order_keys = sorted([bmp_high, astral], key=lambda s: s.encode("utf-16-be"))
    assert codepoint_order_keys != utf16_order_keys


def test_lone_surrogate_rejected():
    lone_surrogate = "\ud800"
    with pytest.raises(JCSError):
        canonicalize(lone_surrogate)


def test_exact_bytes_not_merely_equivalent_json():
    """A digest consumer cares about exact bytes, not just equivalent parsed
    JSON -- confirm no incidental whitespace/formatting differences exist
    versus the reference library's own output."""
    import rfc8785 as _ref

    value = {"b": [1, 2.5, "x", None, True], "a": {"nested": 1}}
    assert canonicalize_bytes(value) == _ref.dumps(value)
