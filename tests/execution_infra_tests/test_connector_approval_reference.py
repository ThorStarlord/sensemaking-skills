"""Connector-native conversation-approval audit-locator tests.

The standalone human ``approve`` remains the authorization. These tests cover
the explicit agent-recorded GitHub issue-comment audit locator used on
surfaces that cannot truthfully access platform session/message identifiers.
"""

import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from campaign_validation.fixtures import to_campaign_policy  # noqa: E402
from exploratory_fixtures import TEST_VALIDATION_TIME, build_policy_raw  # noqa: E402
from sensemaking_skills.campaign_validation import validate_campaign_approval  # noqa: E402
from sensemaking_skills.campaign_validation.models import ValidationContext  # noqa: E402
from sensemaking_skills.campaign_validation.yaml_profile import (  # noqa: E402
    dump_two_lane_yaml,
)
from sensemaking_skills.exploratory_authorization.provenance import (  # noqa: E402
    ProvenanceVerificationError,
)
from sensemaking_skills.exploratory_execution.conversation_approval import (  # noqa: E402
    APPROVAL_REFERENCE_KIND_GITHUB_ISSUE_COMMENT,
    ConversationApprovalVerifier,
)

_NOW = datetime(2026, 1, 1, tzinfo=UTC)
_POLICY = build_policy_raw(
    execution_mode="coding_agent_native",
    execution_surface="github_connector",
    external_provider_api_prohibited=True,
    allowed_models=[],
)
_REFERENCE = (
    "https://github.com/ThorStarlord/sensemaking-skills/issues/200"
    "#issuecomment-5330000000"
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
    "reference_kind": APPROVAL_REFERENCE_KIND_GITHUB_ISSUE_COMMENT,
    "reference": _REFERENCE,
}


def _verify(receipt: dict):
    raw = dict(receipt)
    return ConversationApprovalVerifier(
        policy=_POLICY,
        clock=lambda: _NOW,
    ).verify(raw, approval_bytes=dump_two_lane_yaml(raw).encode())


def test_connector_native_issue_comment_locator_succeeds() -> None:
    verified = _verify(_RECEIPT)
    assert verified.reference == _REFERENCE
    assert verified.campaign_id == _POLICY["campaign_id"]
    assert verified.policy_digest == _POLICY["policy_digest"]
    assert verified.signer_identity == ""


@pytest.mark.parametrize(
    "reference",
    [
        "https://example.com/ThorStarlord/sensemaking-skills/issues/200#issuecomment-1",
        "https://github.com/ThorStarlord/sensemaking-skills/issues/200",
        "https://github.com/ThorStarlord/sensemaking-skills/pull/200#issuecomment-1",
        "https://github.com/ThorStarlord/sensemaking-skills/issues/0#issuecomment-1",
        "https://github.com/ThorStarlord/sensemaking-skills/issues/200#issuecomment-0",
        "https://github.com/example/example/issues/<ISSUE>#issuecomment-<COMMENT>",
        "github.com/ThorStarlord/sensemaking-skills/issues/200#issuecomment-1",
    ],
)
def test_connector_native_issue_comment_locator_rejects_malformed_reference(
    reference: str,
) -> None:
    receipt = dict(_RECEIPT)
    receipt["reference"] = reference
    with pytest.raises(ProvenanceVerificationError, match="GitHub audit reference"):
        _verify(receipt)


def test_github_comment_url_requires_explicit_reference_kind() -> None:
    receipt = dict(_RECEIPT)
    receipt.pop("reference_kind")
    with pytest.raises(ProvenanceVerificationError, match="require reference_kind"):
        _verify(receipt)


def test_unknown_reference_kind_fails_closed() -> None:
    receipt = dict(_RECEIPT)
    receipt["reference_kind"] = "some_other_kind"
    with pytest.raises(ProvenanceVerificationError, match="unsupported.*reference_kind"):
        _verify(receipt)


def test_legacy_truthful_conversation_pointer_remains_valid() -> None:
    receipt = dict(_RECEIPT)
    receipt.pop("reference_kind")
    receipt["reference"] = "session-real#message-real"
    verified = _verify(receipt)
    assert verified.reference == "session-real#message-real"


def _schema_context():
    policy = to_campaign_policy(_POLICY, current_time=TEST_VALIDATION_TIME)
    ctx = ValidationContext(
        current_time="2026-01-01T00:00:00+00:00",
        allowed_approver_identities=frozenset(),
    )
    return policy, ctx


def test_schema_accepts_explicit_connector_native_locator() -> None:
    policy, ctx = _schema_context()
    result = validate_campaign_approval(
        dump_two_lane_yaml(dict(_RECEIPT)).encode(), policy, ctx
    )
    assert result.valid, (result.failure_code, result.detail)


def test_schema_rejects_github_locator_without_reference_kind() -> None:
    policy, ctx = _schema_context()
    receipt = dict(_RECEIPT)
    receipt.pop("reference_kind")
    result = validate_campaign_approval(
        dump_two_lane_yaml(receipt).encode(), policy, ctx
    )
    assert not result.valid
    assert result.failure_code == "CAMPAIGN_APPROVAL_SCHEMA_INVALID"


def test_schema_rejects_unknown_reference_kind() -> None:
    policy, ctx = _schema_context()
    receipt = dict(_RECEIPT)
    receipt["reference_kind"] = "some_other_kind"
    result = validate_campaign_approval(
        dump_two_lane_yaml(receipt).encode(), policy, ctx
    )
    assert not result.valid
    assert result.failure_code == "CAMPAIGN_APPROVAL_SCHEMA_INVALID"
