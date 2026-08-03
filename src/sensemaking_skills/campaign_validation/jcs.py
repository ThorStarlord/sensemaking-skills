"""RFC 8785 (JSON Canonicalization Scheme / JCS) adapter.

This module is a narrow adapter around the maintained, published
``rfc8785`` distribution (Trail of Bits), rather than a home-grown
canonicalizer. A prior revision of this module implemented JCS from
scratch; that was corrected after review because a maintained,
conformance-tested implementation is available on the configured package
index (``pip index versions rfc8785`` resolves ``0.1.4``), and reusing it
removes an entire class of subtle divergence risk -- RFC 8785 mandates
UTF-16 code-unit key ordering, not Python's default code-point string
ordering. The home-grown version got this wrong for any object key pair
that differs outside the Basic Multilingual Plane; ``rfc8785`` sorts by
``key.encode("utf-16be")`` exactly as the RFC requires.

``rfc8785`` does not reject negative zero (Python's ``float ==`` does not
distinguish ``+0.0``/``-0.0``, and the library's zero fast-path collapses
both to ``"0"``). Negative-zero rejection is schema v1 policy (ADR 0023
section 10b), not an RFC 8785 requirement, so it remains this module's job
and is enforced independently here, and again earlier still at parse time
in ``yaml_profile.py``.
"""

from __future__ import annotations

import math

import rfc8785

__all__ = ["JCSError", "canonicalize", "canonicalize_bytes"]


class JCSError(ValueError):
    """Raised when a value cannot be canonicalized under RFC 8785."""


def _reject_negative_zero(value: object) -> None:
    if isinstance(value, float) and value == 0.0 and math.copysign(1.0, value) < 0:
        raise JCSError("negative zero is not permitted")
    if isinstance(value, dict):
        for v in value.values():
            _reject_negative_zero(v)
    elif isinstance(value, (list, tuple)):
        for v in value:
            _reject_negative_zero(v)


def canonicalize_bytes(value: object) -> bytes:
    """Serialize ``value`` to its RFC 8785 canonical UTF-8 byte form.

    No trailing newline is appended (``rfc8785.dumps`` already omits one).
    Accepts plain ``dict``/``list``/``str``/``int``/``float``/``bool``/``None``
    -- the JSON-compatible value domain ``parse_two_lane_yaml`` produces.
    Immutable containers produced by this package's deep-freeze
    (``MappingProxyType``, ``tuple``) are NOT accepted directly here --
    digest computation always runs over the plain, pre-freeze parsed
    mapping (see ``digests.py``), never over the frozen, caller-facing
    ``ValidatedCampaignBundle`` snapshot.
    """
    _reject_negative_zero(value)
    try:
        return rfc8785.dumps(value)
    except rfc8785.CanonicalizationError as exc:
        raise JCSError(str(exc)) from exc


def canonicalize(value: object) -> str:
    """Serialize ``value`` to its RFC 8785 canonical JSON string (for tests/debugging)."""
    return canonicalize_bytes(value).decode("utf-8")
