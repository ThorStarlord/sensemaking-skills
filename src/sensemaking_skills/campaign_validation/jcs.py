"""RFC 8785 (JSON Canonicalization Scheme / JCS) implementation.

This module implements a from-scratch RFC 8785 serializer rather than
depending on a third-party package. No maintained PyPI package implementing
RFC 8785's ECMAScript-compatible number formatting exists in this
environment's package index at the time of writing (checked: no
``jsoncanonicalizer``/``rfc8785``/``python-json-canonicalize`` distribution
is resolvable from the configured index). ``canonicaljson`` (available) uses
Python's stdlib ``json`` module for number formatting, which does not follow
ECMAScript ``Number::toString`` (RFC 8785 section 3.2.2.3) -- e.g. Python's
``json.dumps(1.0)`` produces ``"1.0"``, not the JCS-mandated ``"1"``. Using
it would silently violate the "1.0 and 1e0 canonicalize identically"
requirement for any non-integer-typed field, so it is not suitable as the
normative JCS implementation here.

This implementation is restricted to exactly the value domain the Two-Lane
YAML Profile v1 parser can produce: ``None``, ``bool``, ``int``, ``float``,
``str``, ``list``, and ``dict`` with string keys. It does not attempt to be
a general-purpose JSON canonicalizer for arbitrary Python objects.
"""

from __future__ import annotations

import math
from decimal import Decimal


class JCSError(ValueError):
    """Raised when a value cannot be canonicalized under RFC 8785."""


def _canonical_number(value: float | int) -> str:
    """Render a JSON number per RFC 8785 section 3.2.2.3 (ES Number::toString).

    Integers are rendered as plain decimal integer strings (this is exactly
    what the ECMAScript algorithm below produces for integral values in the
    safe range, so an explicit fast path is just an optimization + clarity,
    not a divergent code path).
    """
    if isinstance(value, bool):  # pragma: no cover - guarded by caller
        raise JCSError("bool is not a JCS number")

    if isinstance(value, int):
        return str(value)

    if not isinstance(value, float):
        raise JCSError(f"not a JSON number: {value!r}")

    if math.isnan(value) or math.isinf(value):
        raise JCSError("non-finite numbers are not representable under RFC 8785")

    if value == 0.0:
        # Negative zero must already be rejected upstream (ADR 0023 policy);
        # this module fails closed if it is not.
        if math.copysign(1.0, value) < 0:
            raise JCSError("negative zero is not permitted")
        return "0"

    neg = value < 0
    x = abs(value)

    # Python's repr() of a float produces the shortest decimal string that
    # round-trips to the same IEEE-754 binary64 value -- the same guarantee
    # ECMAScript's Number::toString relies on. We extract the significant
    # digit string and decimal exponent from that shortest representation,
    # then re-render using the ECMAScript positional/exponential rules
    # (which differ from Python's repr formatting rules).
    d = Decimal(repr(x))
    sign, digit_tuple, exponent = d.as_tuple()
    digits = "".join(str(dd) for dd in digit_tuple)

    # Strip trailing zeros from the digit string, folding them into the
    # exponent, to get the minimal-length digit string "s" and its exponent.
    stripped = digits.rstrip("0")
    if stripped == "":
        stripped = "0"
        exponent = 0
    else:
        exponent += len(digits) - len(stripped)
    digits = stripped
    k = len(digits)
    n = exponent + k

    if k <= n <= 21:
        s = digits + ("0" * (n - k))
    elif 0 < n <= 21:
        s = digits[:n] + "." + digits[n:]
    elif -6 < n <= 0:
        s = "0." + ("0" * (-n)) + digits
    else:
        mantissa = digits if k == 1 else digits[0] + "." + digits[1:]
        exp = n - 1
        s = mantissa + "e" + ("+" if exp >= 0 else "-") + str(abs(exp))

    return ("-" + s) if neg else s


def _escape_string(value: str) -> str:
    """Escape a string per RFC 8785 section 3.2.2.2 (== RFC 8259 escaping)."""
    out = ["\""]
    for ch in value:
        cp = ord(ch)
        if ch == "\"":
            out.append("\\\"")
        elif ch == "\\":
            out.append("\\\\")
        elif ch == "\b":
            out.append("\\b")
        elif ch == "\f":
            out.append("\\f")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif cp < 0x20:
            out.append(f"\\u{cp:04x}")
        elif 0xD800 <= cp <= 0xDFFF:
            # Lone surrogate -- must never appear in a valid Python str
            # produced by our own parser, but fail closed if it does.
            raise JCSError("lone surrogate in string value")
        else:
            out.append(ch)
    out.append("\"")
    return "".join(out)


def canonicalize(value: object) -> str:
    """Serialize ``value`` to its RFC 8785 canonical JSON string form."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return _canonical_number(value)
    if isinstance(value, str):
        return _escape_string(value)
    if isinstance(value, list):
        return "[" + ",".join(canonicalize(v) for v in value) + "]"
    if isinstance(value, dict):
        items = []
        for k in sorted(value.keys()):
            if not isinstance(k, str):
                raise JCSError("JCS object keys must be strings")
            items.append(_escape_string(k) + ":" + canonicalize(value[k]))
        return "{" + ",".join(items) + "}"
    raise JCSError(f"value of type {type(value).__name__} is not JCS-serializable")


def canonicalize_bytes(value: object) -> bytes:
    """Serialize ``value`` to its RFC 8785 canonical UTF-8 byte form.

    No trailing newline is appended.
    """
    return canonicalize(value).encode("utf-8")
