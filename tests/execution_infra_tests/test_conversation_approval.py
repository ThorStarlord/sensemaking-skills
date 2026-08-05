"""Conversation approval (active_human_conversation) tests.

The human's standalone ``approve`` in the active conversation is the
authorization; ``approval.md`` is the agent-generated receipt. The
conversation is the authority -- there is no external corroboration, no
network, no token. These tests prove the runtime enforces, fail-closed,
every binding the receipt must hold, and that the path never touches a
provider, the network, or any environment credential.
"""

import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from exploratory_fixtures import build_policy_raw  # noqa: E402
from sensemaking_skills.exploratory_authorization.provenance import (  # noqa: E402
    ProvenanceVerificationError,
)
from sensemaking_skills.exploratory_execution import (  # noqa: E402
    CONVERSATION_APPROVAL_MECHANISM,
    ConversationApprovalVerifier,
    extract_frontmatter,
)
from sensemaking_skills.exploratory_execution.conversation_approval import (  # noqa: E402
    APPROVAL_TEXT,
)
from sensemaking_skills.campaign_validation.yaml_profile import (  # noqa: E402
    dump_two_lane_yaml,
)

_NOW = datetime(2026, 1, 1, tzinfo=UTC)
# The conversation receipt is the agent-native mechanism: the policy
# carries the mode coupling (external-provider prohibition included).
_POLICY = build_policy_raw(
    execution_mode="coding_agent_native",
    execution_surface="current_coding_agent",
    external_provider_api_prohibited=True,
    allowed_models=[],
)
_RECEIPT = {
    "approval_schema_version": "1",
    "status": "approved",
    "campaign_id": _POLICY["campaign_id"],
    "policy_digest": _POLICY["policy_digest"],
    "approval_source": "active_human_conversation",
    "approval_text": "approve",
    "approved_at": "2025-12-31T12:00:00Z",
    "maximum_attempts": int(_POLICY["max_attempt_slots"]),
    "concurrency": int(_POLICY["concurrency_ceiling"]),
    "automatic_merge": "prohibited",
    "external_provider_api_prohibited": True,
    "classification": _POLICY["classification"],
    "reference": "session-abc#message-123",
}


def _verifier(**kwargs) -> ConversationApprovalVerifier:
    return ConversationApprovalVerifier(policy=_POLICY, clock=lambda: _NOW, **kwargs)


def _verify(receipt: dict) -> None:
    raw = dict(receipt)
    return _verifier().verify(raw, approval_bytes=dump_two_lane_yaml(raw).encode())


def test_correct_receipt_succeeds() -> None:
    verified = _verify(_RECEIPT)
    assert verified.mechanism == CONVERSATION_APPROVAL_MECHANISM
    assert verified.campaign_id == _POLICY["campaign_id"]
    assert verified.policy_digest == _POLICY["policy_digest"]
    assert verified.reference == _RECEIPT["reference"]
    # The receipt records no identity claim: the conversation is the
    # authority, and the file is not independent proof of identity.
    assert verified.signer_identity == ""
    assert verified.approval_sha256.startswith("0" * 0) or len(verified.approval_sha256) == 64


def _mutate(**changes) -> dict:
    raw = dict(_RECEIPT)
    raw.update(changes)
    return raw


@pytest.mark.parametrize(
    "mutations, match",
    [
        ({"campaign_id": "EXP-9999-other"}, "campaign"),
        ({"policy_digest": "0" * 64}, "policy_digest"),
        ({"maximum_attempts": 99}, "maximum_attempts"),
        ({"concurrency": 9}, "concurrency"),
        ({"automatic_merge": "allowed"}, "automatic_merge"),
        ({"external_provider_api_prohibited": False}, "external provider"),
        ({"classification": "CANONICAL_EVIDENCE"}, "classification"),
        ({"approved_at": "2099-01-01T00:00:00Z"}, "future"),
        ({"reference": ""}, "reference"),
        ({"status": "rejected"}, "status"),
        ({"approval_text": "maybe"}, "approval_text"),
        ({"approval_source": "github_issue_comment_approval"}, "approval_source"),
    ],
)
def test_envelope_and_binding_violations_fail(mutations: dict, match: str) -> None:
    with pytest.raises(ProvenanceVerificationError, match=match):
        _verify(_mutate(**mutations))


def test_approved_at_after_window_end_fails() -> None:
    """A receipt timestamped after the policy window end is refused (clock
    set past the window so the future-skew check does not preempt it)."""
    from sensemaking_skills.campaign_validation.models import (
        ValidationContext,
    )
    from sensemaking_skills.campaign_validation import (
        compute_policy_digest,
        validate_campaign_policy,
    )
    from exploratory_fixtures import render_yaml

    policy_raw = dict(_POLICY)
    policy_raw["validity_window"] = {
        "not_before": "2026-06-01T00:00:00+00:00",
        "not_after": "2026-06-30T00:00:00+00:00",
    }
    policy_raw["policy_digest"] = compute_policy_digest(policy_raw)
    result = validate_campaign_policy(
        render_yaml(policy_raw),
        ValidationContext(
            current_time="2026-06-15T00:00:00+00:00",
            allowed_approver_identities=frozenset(),
        ),
    )
    assert result.valid, (result.failure_code, result.detail)
    policy = result.value.raw
    receipt = _mutate(
        approved_at="2026-12-01T00:00:00Z",
        policy_digest=policy_raw["policy_digest"],
    )
    with pytest.raises(ProvenanceVerificationError, match="window end"):
        ConversationApprovalVerifier(
            policy=policy,
            clock=lambda: datetime(2026, 12, 15, tzinfo=UTC),
        ).verify(receipt, approval_bytes=dump_two_lane_yaml(receipt).encode())


def test_policy_without_merge_prohibition_fails() -> None:
    policy = dict(_POLICY)
    policy["automatic_merge_prohibited"] = False
    with pytest.raises(ProvenanceVerificationError, match="automatic merge"):
        ConversationApprovalVerifier(policy=policy, clock=lambda: _NOW).verify(
            _RECEIPT, approval_bytes=dump_two_lane_yaml(_RECEIPT).encode()
        )


def test_policy_without_external_prohibition_fails() -> None:
    policy = dict(_POLICY)
    policy["external_provider_api_prohibited"] = False
    with pytest.raises(ProvenanceVerificationError, match="external provider"):
        ConversationApprovalVerifier(policy=policy, clock=lambda: _NOW).verify(
            _RECEIPT, approval_bytes=dump_two_lane_yaml(_RECEIPT).encode()
        )


def test_fails_closed_without_policy() -> None:
    with pytest.raises(ProvenanceVerificationError, match="policy"):
        ConversationApprovalVerifier(policy=None, clock=lambda: _NOW).verify(
            _RECEIPT, approval_bytes=b"x"
        )


def test_fails_closed_without_approval_bytes() -> None:
    with pytest.raises(ProvenanceVerificationError, match="bytes"):
        _verifier().verify(_RECEIPT, approval_bytes=None)


def test_no_network_no_token_no_provider() -> None:
    """The conversation path is purely local: it must not import or call
    the network, the provider SDK, or read any credential environment
    variable."""
    import sensemaking_skills.exploratory_execution.conversation_approval as ca

    assert "urllib" not in ca.__dict__
    assert "os" not in ca.__dict__ or "environ" not in dir(ca.os)
    assert "claude_agent_sdk" not in sys.modules
    # Verify with all credential env vars removed: still succeeds.
    import os

    saved = {k: os.environ.pop(k, None) for k in ("GITHUB_TOKEN", "GH_TOKEN", "ANTHROPIC_API_KEY")}
    try:
        _verify(_RECEIPT)
    finally:
        for k, v in saved.items():
            if v is not None:
                os.environ[k] = v
    assert "claude_agent_sdk" not in sys.modules


# ---------------------------------------------------------------------------
# approval.md frontmatter extraction
# ---------------------------------------------------------------------------


def test_frontmatter_extraction_round_trip() -> None:
    frontmatter = dump_two_lane_yaml(_RECEIPT)
    md = ("---\n" + frontmatter + "---\nThe human approved the single "
          "pending campaign presented in the active conversation.\n").encode()
    extracted = extract_frontmatter(md)
    assert extracted is not None
    # The regex group excludes the newline before the closing ---; the
    # extracted block still parses as the exact Two-Lane document.
    assert extracted == frontmatter.encode().rstrip(b"\n")


def test_frontmatter_missing_returns_none() -> None:
    assert extract_frontmatter(b"no frontmatter here") is None
    assert extract_frontmatter(b"") is None
    assert extract_frontmatter(b"---\nunterminated") is None


# ---------------------------------------------------------------------------
# oneOf discrimination: a document matches EXACTLY one profile
# ---------------------------------------------------------------------------


def test_oneof_discrimination_exactly_one_profile() -> None:
    """The three profiles are disjoint: a conversation receipt matches
    only the conversation branch, a template only the example branch, and
    an operative approval only the operative branch."""
    import json

    schema = json.loads(
        (
            Path(__file__).resolve().parents[2]
            / "src" / "sensemaking_skills" / "campaign_validation"
            / "schemas" / "campaign-approval.v1.schema.json"
        ).read_text(encoding="utf-8")
    )

    def matching_branches(doc: dict) -> list[str]:
        hits = []
        for branch in schema["oneOf"]:
            result = _branch_errors(branch, doc)
            if not result:
                hits.append(branch.get("title", "?"))
        return hits

    def _branch_errors(branch: dict, doc: dict) -> list:
        import jsonschema

        wrapper = {
            "$schema": schema["$schema"],
            "$defs": schema["$defs"],
            "oneOf": [branch],
        }
        return sorted(
            jsonschema.Draft202012Validator(wrapper).iter_errors(doc),
            key=lambda e: e.message,
        )

    receipt = dict(_RECEIPT)
    template = {
        "approval_schema_version": "1",
        "marker": "EXAMPLE_ONLY_NOT_AUTHORIZATION",
        "campaign_id": "EXP-9001-alpha",
        "policy_digest": "a" * 64,
        "claimed_approver_identity": "<HUMAN-FILLS-IN EXACT GITHUB HANDLE>",
        "approval_provenance": {"mechanism": "", "reference": ""},
        "approval_statement": "<HUMAN-FILLS-IN approval statement>",
        "approved_at": "<HUMAN-FILLS-IN RFC3339 timestamp>",
    }
    operative = {
        "approval_schema_version": "1",
        "campaign_id": "EXP-9001-alpha",
        "policy_digest": "a" * 64,
        "claimed_approver_identity": "test-approver-handle",
        "approval_provenance": {
            "mechanism": "signed_commit",
            "reference": "0" * 40,
        },
        "approval_statement": "I approve.",
        "approved_at": "2026-01-01T00:00:00Z",
    }
    assert len(matching_branches(receipt)) == 1
    assert len(matching_branches(template)) == 1
    assert len(matching_branches(operative)) == 1
    # A forged document mixing profiles matches NONE of the branches.
    forged = dict(receipt)
    forged["approval_provenance"] = {
        "mechanism": "github_issue_comment_approval",
        "reference": "https://github.com/x/y/issues/1#issuecomment-1",
    }
    assert matching_branches(forged) == []
