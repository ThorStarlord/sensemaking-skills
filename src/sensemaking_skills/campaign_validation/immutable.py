"""Deep-freeze helper: turn a plain JSON-compatible value into a recursively
immutable, detached snapshot.

A ``@dataclass(frozen=True)`` only prevents *reassigning* its own fields; if
a field holds a plain ``dict``/``list``, that container's *contents* remain
freely mutable, and a caller who later mutates the original parsed input
(or the ``.raw`` mapping on a returned model) would silently corrupt data
already reported as "validated." ``freeze()`` closes that gap: every
mapping becomes a ``types.MappingProxyType`` wrapping a **new**, private
``dict`` (so a later mutation of the original source dict cannot reach the
frozen copy either -- detachment, not just a read-only view over the same
storage), and every sequence becomes a ``tuple`` of recursively frozen
elements. Scalars (``str``/``int``/``float``/``bool``/``None``) are already
immutable and are returned as-is.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Any, Mapping


def freeze(value: Any) -> Any:
    """Recursively freeze ``value`` into an immutable, detached snapshot."""
    if isinstance(value, Mapping):
        return MappingProxyType({k: freeze(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(freeze(v) for v in value)
    # str / int / float / bool / None are already immutable.
    return value
