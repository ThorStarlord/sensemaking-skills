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
