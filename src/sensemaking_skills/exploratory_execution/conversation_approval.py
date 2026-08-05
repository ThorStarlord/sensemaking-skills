"""Conversation approval (active_human_conversation) - the human's
standalone ``approve`` in the active conversation.

The human approves in the conversation; the coding agent performs every
repository operation; a Markdown file (``approval.md``) records the
decision; no GitHub comment, capture script, API token, or live comment
revalidation is involved.

Trust model (deliberate, per the governance decision): the conversation
is the source of authority. ``approval.md`` is the agent-generated
audit receipt containing the precise meaning of that decision -- it is
NOT independent proof of human identity, and no runtime component can
corroborate it externally. What the runtime DOES enforce, fail-closed,
before every prepare and finalize operation:

* the receipt exists and parses (frontmatter is a Two-Lane v1 document);
* it is the conversation-approval profile (``approval_source:
  active_human_conversation``, ``approval_text: approve``,
  ``status: approved``);
* it binds the EXACT campaign id and policy digest;
* it never exceeds the approved policy envelope: attempt limit,
  concurrency, automatic-merge prohibition, external-provider-API
  prohibition, classification, and window end;
* ``approved_at`` is a plausible receipt timestamp (not in the future);
* the reference (conversation record) is non-empty for audit.

The conversation discipline -- exactly one pending campaign, presented
envelope, unchanged digest, standalone ``approve``, not inside a quote
or hypothetical -- is enforced by the coding agent in the conversation
(see skills/coding-agent-native-campaign/SKILL.md); the runtime cannot
see the transcript.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Callable

from sensemaking_skills.exploratory_authorization.models import (
    VerifiedApprovalProvenance,
)
from sensemaking_skills.exploratory_authorization.provenance import (
    ProvenanceVerificationError,
)

APPROVAL_MECHANISM = "active_human_conversation"
APPROVAL_TEXT = "approve"
APPROVAL_FILENAME = "approval.md"

_FRONTMATTER_RE = re.compile(
    r"^---\s*\n(.*?)\n---\s*(\n|$)", re.DOTALL
)


def extract_frontmatter(source: bytes) -> bytes | None:
    """Extract the YAML frontmatter block of an ``approval.md`` receipt.

    Returns the frontmatter bytes (a Two-Lane v1 document) or ``None``
    when the file has no well-formed ``---`` frontmatter block.
    """
    text = source.decode("utf-8", errors="replace")
    match = _FRONTMATTER_RE.match(text)
    if match is None:
        return None
    return match.group(1).encode("utf-8")


def _parse_rfc3339(value: Any) -> datetime | None:
    try:
        return datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


class ConversationApprovalVerifier:
    """Corroborate the conversation-approval receipt against the validated
    policy. No network, no token, no external artifact: the receipt's
    internal consistency with the approved envelope IS the check (the
    conversation is the authority; see module docstring).
    """

    def __init__(
        self,
        *,
        policy: Mapping[str, Any] | None = None,
        clock: Callable[[], datetime] | None = None,
        max_future_skew: timedelta | None = None,
    ) -> None:
        self._policy = policy
        self._clock = clock or (lambda: datetime.now(UTC))
        self._max_future_skew = max_future_skew or timedelta(minutes=5)

    def verify(
        self, approval: Any, *, approval_bytes: bytes | None = None
    ) -> VerifiedApprovalProvenance:
        raw = getattr(approval, "raw", approval) or {}
        if raw.get("approval_source") != APPROVAL_MECHANISM:
            raise ProvenanceVerificationError(
                "conversation verifier: document is not an "
                f"active_human_conversation receipt "
                f"(approval_source={raw.get('approval_source')!r})"
            )
        if approval_bytes is None:
            raise ProvenanceVerificationError(
                "conversation verifier: no operative approval bytes were "
                "supplied (fail closed)"
            )
        if self._policy is None:
            raise ProvenanceVerificationError(
                "conversation verifier: no validated policy was supplied; "
                "envelope checks are impossible (fail closed)"
            )
        policy = self._policy

        # The receipt is the operative document: every binding must hold.
        if raw.get("status") != "approved" or raw.get("approval_text") != APPROVAL_TEXT:
            raise ProvenanceVerificationError(
                "conversation verifier: receipt is not a status=approved, "
                f"approval_text={APPROVAL_TEXT!r} decision"
            )
        reference = str(raw.get("reference", "")).strip()
        if not reference:
            raise ProvenanceVerificationError(
                "conversation verifier: receipt reference (conversation "
                "record) is empty (fail closed)"
            )
        if re.fullmatch(r"[^\s<>]+#[^\s<>]+", reference) is None:
            raise ProvenanceVerificationError(
                "conversation verifier: receipt reference must be a "
                "concrete '<session-id>#<message-id>' pointer with no "
                "whitespace or angle brackets"
            )
        if raw.get("campaign_id") != str(policy.get("campaign_id", "")):
            raise ProvenanceVerificationError(
                "conversation verifier: receipt binds a different campaign "
                "than the validated policy"
            )
        if raw.get("policy_digest") != str(policy.get("policy_digest", "")):
            raise ProvenanceVerificationError(
                "conversation verifier: receipt binds a different "
                "policy_digest than the validated policy"
            )
        try:
            maximum_attempts = int(raw["maximum_attempts"])
            concurrency = int(raw["concurrency"])
        except (KeyError, TypeError, ValueError):
            raise ProvenanceVerificationError(
                "conversation verifier: receipt maximum_attempts/concurrency "
                "are not integers"
            ) from None
        if maximum_attempts > int(policy.get("max_attempt_slots", 0)):
            raise ProvenanceVerificationError(
                "conversation verifier: receipt maximum_attempts "
                f"{maximum_attempts} exceeds the policy limit "
                f"{policy.get('max_attempt_slots')}"
            )
        if concurrency > int(policy.get("concurrency_ceiling", 0)):
            raise ProvenanceVerificationError(
                "conversation verifier: receipt concurrency "
                f"{concurrency} exceeds the policy ceiling "
                f"{policy.get('concurrency_ceiling')}"
            )
        if str(raw.get("automatic_merge", "")).casefold() != "prohibited":
            raise ProvenanceVerificationError(
                "conversation verifier: receipt automatic_merge is not "
                "'prohibited'"
            )
        if policy.get("automatic_merge_prohibited") is not True:
            raise ProvenanceVerificationError(
                "conversation verifier: the validated policy does not "
                "prohibit automatic merge; the receipt's prohibition cannot "
                "bind it"
            )
        if raw.get("external_provider_api_prohibited") is not True:
            raise ProvenanceVerificationError(
                "conversation verifier: receipt does not prohibit external "
                "provider APIs"
            )
        if policy.get("external_provider_api_prohibited") is not True:
            raise ProvenanceVerificationError(
                "conversation verifier: the validated policy does not "
                "prohibit external provider APIs; the receipt's prohibition "
                "cannot bind it"
            )
        if raw.get("classification") != str(policy.get("classification", "")):
            raise ProvenanceVerificationError(
                "conversation verifier: receipt classification differs from "
                "the validated policy"
            )
        approved_at = _parse_rfc3339(raw.get("approved_at"))
        if approved_at is None:
            raise ProvenanceVerificationError(
                "conversation verifier: receipt approved_at is not a valid "
                "RFC3339 timestamp"
            )
        if approved_at > self._clock() + self._max_future_skew:
            raise ProvenanceVerificationError(
                "conversation verifier: receipt approved_at is in the "
                "future; a receipt cannot predate the decision it records"
            )
        window = policy.get("validity_window") or {}
        not_after = _parse_rfc3339(window.get("not_after"))
        if not_after is not None and approved_at > not_after:
            raise ProvenanceVerificationError(
                "conversation verifier: receipt approved_at is after the "
                "policy window end"
            )

        return VerifiedApprovalProvenance(
            mechanism=APPROVAL_MECHANISM,
            reference=reference,
            signer_identity="",  # the conversation is the authority; the
            # receipt records no identity claim (ADR decision: the file is
            # not independent proof of identity).
            approval_sha256=hashlib.sha256(approval_bytes).hexdigest(),
            campaign_id=str(raw.get("campaign_id", "")),
            policy_digest=str(raw.get("policy_digest", "")),
        )
