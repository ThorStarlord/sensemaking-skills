"""Digests and tamper-evident hash chaining for Phase 4 campaign accounting (#120).

Uses RFC 8785 canonicalization (via sensemaking_skills.campaign_validation.jcs)
and SHA-256 hex digests for ledger event hash chaining.
"""

import hashlib
from typing import Any, Dict

from sensemaking_skills.campaign_validation.jcs import canonicalize_bytes

GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"


def compute_event_hash(event_dict_without_hash: Dict[str, Any]) -> str:
    """Compute SHA-256 hex digest of a ledger event dictionary under JCS canonicalization.

    The event_dict_without_hash must contain all event fields (sequence, timestamp,
    campaign_id, attempt_id, event_type, payload, previous_event_hash) EXCEPT 'event_hash'.
    """
    event_copy = dict(event_dict_without_hash)
    event_copy.pop("event_hash", None)
    canonical_bytes = canonicalize_bytes(event_copy)
    return hashlib.sha256(canonical_bytes).hexdigest()
