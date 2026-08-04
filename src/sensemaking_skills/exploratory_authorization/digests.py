"""Snapshot digests bound at mint time (Phase 3, issue #119).

Two digests, both ``SHA-256`` over the RFC 8785 (JCS) canonical form of the
complete parsed, validated document (``<doc>.raw``), as lowercase 64-hex:

- ``compute_approval_snapshot_digest`` -- binds the full campaign-approval
  document, including provenance, statement, and approver identity.
- ``compute_configuration_snapshot_digest`` -- binds the full
  configuration-identity document WITH ``configuration_id`` included.
  Unlike ``compute_configuration_id`` (which deliberately excludes
  ``campaign_id`` and ``configuration_id`` from the hash -- ADR 0023
  section 10), the snapshot must bind both, so a capability cannot be
  split across campaigns or across revisions of one document.

Digests are recomputed internally at mint; callers never supply trusted
digest values.
"""

from __future__ import annotations

import hashlib
from typing import Any, Mapping

from ..campaign_validation.jcs import canonicalize


def _to_plain(value: Any) -> Any:
    """Deep-convert the frozen, caller-facing document snapshot
    (``MappingProxyType`` / ``tuple``) back to plain JSON-compatible
    containers.

    ``campaign_validation.jcs`` deliberately accepts only plain parsed
    mappings; digest computation over the sealed bundle must normalize
    first.
    """
    if isinstance(value, Mapping):
        return {str(k): _to_plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_plain(v) for v in value]
    return value


def _sha256_hex(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonicalize(_to_plain(value)).encode("ascii")).hexdigest()


def compute_approval_snapshot_digest(raw: Mapping[str, Any]) -> str:
    """SHA-256 hex over the JCS canonical form of the approval document."""
    return _sha256_hex(raw)


def compute_configuration_snapshot_digest(
    raw: Mapping[str, Any], configuration_id: str
) -> str:
    """SHA-256 hex over the JCS canonical form of the configuration document
    WITH ``configuration_id`` explicitly included (key order is irrelevant:
    JCS sorts keys lexicographically)."""
    snapshot = dict(raw)
    snapshot["configuration_id"] = configuration_id
    return _sha256_hex(snapshot)
