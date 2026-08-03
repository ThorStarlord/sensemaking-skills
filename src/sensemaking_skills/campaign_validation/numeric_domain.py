"""Recursive JCS/RFC-8785 numeric-domain preflight.

Arbitrary-precision integer lexemes parse as genuine Python ``int``
(``yaml_profile.py`` never truncates precision), but ``rfc8785`` only
accepts integers within the interoperable safe-integer domain
(``-9007199254740991`` to ``9007199254740991`` inclusive) -- an ordinary,
EXPECTED invalid-document case (a policy author writing an absurdly large
limit, or an execution_parameters value that overflows the domain) is not
an internal implementation failure and must never be reported as
``CAMPAIGN_INTERNAL_VALIDATION_ERROR``.

This module walks a parsed document recursively -- BEFORE digest
computation -- and reports the first out-of-domain integer's structured
field path, if any. Booleans are never treated as integers (``isinstance``
checks ``bool`` first). Parser-level rejections (negative zero, non-finite,
overflow-to-infinity, nonzero-underflow, unsupported binary64 precision)
already happened earlier, in ``yaml_profile.py``, and are not re-checked
here -- this module is specifically the safe-INTEGER range check that
``rfc8785`` itself enforces at digest time, promoted earlier so it gets its
own deterministic, non-internal failure code.
"""

from __future__ import annotations

from typing import Any, Optional

_SAFE_INT_MIN = -9007199254740991
_SAFE_INT_MAX = 9007199254740991

__all__ = ["SAFE_INT_MIN", "SAFE_INT_MAX", "find_out_of_domain_path"]

SAFE_INT_MIN = _SAFE_INT_MIN
SAFE_INT_MAX = _SAFE_INT_MAX


def find_out_of_domain_path(value: Any, path: str = "$") -> Optional[str]:
    """Return the structured field path of the first out-of-domain integer
    found in ``value`` (recursively through mappings and sequences), or
    ``None`` if every integer in ``value`` is within the safe-integer
    domain.
    """
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        if not (_SAFE_INT_MIN <= value <= _SAFE_INT_MAX):
            return path
        return None
    if isinstance(value, dict):
        for key, sub_value in value.items():
            found = find_out_of_domain_path(sub_value, f"{path}.{key}")
            if found is not None:
                return found
        return None
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            found = find_out_of_domain_path(item, f"{path}[{index}]")
            if found is not None:
                return found
        return None
    # str / float / None already validated (float non-finite/negative-zero/
    # precision) at parse time in yaml_profile.py; nothing further to check.
    return None
