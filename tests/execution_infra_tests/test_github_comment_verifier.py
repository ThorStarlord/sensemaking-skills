"""GitHub issue-comment campaign approval verifier and capture tests.

Lane A beta (Model B, Issue #122): a human posts ONE approval comment on
the campaign's GitHub issue; trusted framework code transcribes it into
the operative approval snapshot; the verifier corroborates the snapshot
against the LIVE GitHub API (fetchers injected here, so no verifier test
touches the network) before every capability mint.

Proof matrix required by the Model B plan:

* correct maintainer comment succeeds;
* wrong author fails;
* author without required permission fails;
* wrong campaign ID fails;
* wrong digest fails;
* vague comment fails;
* reaction-only approval fails;
* edited comment fails;
* deleted comment fails;
* expired approval fails;
* attempt limit expansion fails;
* automatic merge permission fails;
* agent-generated fixture cannot masquerade as live GitHub provenance;
* no provider is called in any verifier test;
* the capture tool transcribes only a genuine human comment;
* the runner dispatches by provenance mechanism (signed_commit still
  constructed for the legacy mechanism; unknown mechanisms refuse).
"""

import hashlib
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from exploratory_fixtures import (  # noqa: E402
    TEST_APPROVER_IDENTITY,
    TEST_CAMPAIGN_ID,
    TEST_FRAMEWORK_SHA,
    TEST_MODEL,
    TEST_TARGET_REPOSITORY,
    TEST_TARGET_SHA,
    TEST_VALIDATION_TIME,
    build_configuration_raw,
    build_policy_raw,
    render_yaml,
)

from sensemaking_skills.campaign_validation import (  # noqa: E402
    ValidationContext,
    compute_policy_digest,
    validate_campaign_bundle,
    validate_campaign_policy,
)
from sensemaking_skills.exploratory_authorization.provenance import (  # noqa: E402
    ProvenanceVerificationError,
)
from sensemaking_skills.exploratory_execution import (  # noqa: E402
    APPROVAL_MARKER,
    APPROVAL_MECHANISM,
    ApprovalCaptureError,
    GitHubIssueCommentApprovalVerifier,
    ProductionSignedCommitVerifier,
    capture_approval_snapshot,
    parse_approval_comment,
)
from sensemaking_skills.exploratory_execution.execution_identity import (  # noqa: E402
    GOVERNED_GITHUB_REPOSITORY,
)

_NOW = datetime(2026, 1, 1, tzinfo=UTC)
_CREATED_AT = "2025-12-31T12:00:00Z"
_EXPIRES_AT = "2026-01-02T00:00:00Z"
_COMMENT_ID = "123456"
_ISSUE = 122


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _approval_body(
    policy_raw: dict,
    *,
    campaign_id: str | None = None,
    policy_digest: str | None = None,
    maximum_attempts: int | None = None,
    concurrency: int | None = None,
    automatic_merge: str = "prohibited",
    classification: str | None = None,
    expires_at: str = _EXPIRES_AT,
    statement: str = "I authorize this bounded exploratory campaign.",
) -> str:
    return "\n".join(
        [
            APPROVAL_MARKER,
            "",
            f"campaign_id: {campaign_id or policy_raw['campaign_id']}",
            f"policy_digest: {policy_digest or policy_raw['policy_digest']}",
            f"maximum_attempts: {maximum_attempts or policy_raw['max_attempt_slots']}",
            f"concurrency: {concurrency or policy_raw['concurrency_ceiling']}",
            f"automatic_merge: {automatic_merge}",
            f"classification: {classification or policy_raw['classification']}",
            f"expires_at: {expires_at}",
            "",
            statement,
        ]
    )


def _comment(
    body: str,
    *,
    comment_id: str = _COMMENT_ID,
    author: str = TEST_APPROVER_IDENTITY,
    created_at: str = _CREATED_AT,
    issue: int = _ISSUE,
) -> dict:
    return {
        "id": comment_id,
        "html_url": (
            f"https://github.com/{GOVERNED_GITHUB_REPOSITORY}/issues/"
            f"{issue}#issuecomment-{comment_id}"
        ),
        "issue_url": (
            f"https://api.github.com/repos/{GOVERNED_GITHUB_REPOSITORY}/"
            f"issues/{issue}"
        ),
        "user": {"login": author},
        "created_at": created_at,
        "body": body,
    }


def _snapshot_raw(policy_raw: dict, body: str, comment: dict) -> dict:
    parsed = parse_approval_comment(body)
    assert parsed is not None
    return {
        "approval_schema_version": "1",
        "campaign_id": policy_raw["campaign_id"],
        "policy_digest": policy_raw["policy_digest"],
        "claimed_approver_identity": comment["user"]["login"],
        "approval_provenance": {
            "mechanism": APPROVAL_MECHANISM,
            "reference": comment["html_url"],
            "repository": GOVERNED_GITHUB_REPOSITORY,
            "issue_number": str(_ISSUE),
            "comment_id": comment["id"],
            "comment_body_sha256": hashlib.sha256(
                comment["body"].encode("utf-8")
            ).hexdigest(),
        },
        "approval_statement": parsed["statement"],
        "approved_at": comment["created_at"],
    }


def _verifier(
    policy_raw: dict,
    comment: dict | None,
    *,
    permission: str = "admin",
    clock=None,
    fetch_permission_author: str | None = None,
) -> GitHubIssueCommentApprovalVerifier:
    def fetch_comment(comment_id: str):
        if comment is None or comment_id != str(comment["id"]):
            return None
        return comment

    def fetch_permission(login: str):
        if fetch_permission_author is not None and login != fetch_permission_author:
            return None
        return permission

    return GitHubIssueCommentApprovalVerifier(
        repository=GOVERNED_GITHUB_REPOSITORY,
        policy=policy_raw,
        clock=clock or (lambda: _NOW),
        fetch_comment=fetch_comment,
        fetch_permission=fetch_permission,
    )


def _run_verify(verifier, snapshot_raw: dict) -> None:
    snapshot_bytes = render_yaml(snapshot_raw)
    return verifier.verify(snapshot_raw, approval_bytes=snapshot_bytes)


# ---------------------------------------------------------------------------
# Parser (grammar) matrix
# ---------------------------------------------------------------------------


def test_parser_accepts_canonical_comment() -> None:
    policy_raw = build_policy_raw()
    parsed = parse_approval_comment(_approval_body(policy_raw))
    assert parsed is not None
    assert parsed["campaign_id"] == policy_raw["campaign_id"]
    assert parsed["policy_digest"] == policy_raw["policy_digest"]
    assert parsed["maximum_attempts"] == 3
    assert parsed["concurrency"] == 1
    assert parsed["automatic_merge"] == "prohibited"
    assert parsed["expires_at"] == _EXPIRES_AT
    assert parsed["statement"] == "I authorize this bounded exploratory campaign."


@pytest.mark.parametrize(
    "mutator",
    [
        lambda b: b.replace(APPROVAL_MARKER, "SOUNDS_GOOD"),  # wrong marker
        lambda b: b.replace(APPROVAL_MARKER, ""),  # missing marker
        lambda b: b.replace("maximum_attempts: 3", ""),  # missing field
        lambda b: b.replace("maximum_attempts: 3", "maximum_attempts: 3\nmaximum_attempts: 4"),  # duplicate
        lambda b: b.replace(
            "campaign_id: ", "mystery_field: x\ncampaign_id: "
        ),  # unknown field line
        lambda b: b.replace("maximum_attempts: 3", "maximum_attempts: lots"),  # bad int
        lambda b: b.replace("concurrency: 1", "concurrency: 1.5"),  # bad int
        lambda b: b.replace("I authorize", "I think"),  # no authorization word
        lambda b: b.replace("I authorize this bounded exploratory campaign.", ""),  # no statement
        lambda b: "looks good to me!",  # vague comment
        lambda b: "",  # reaction-only / empty
    ],
)
def test_parser_rejects_malformed_comments(mutator) -> None:
    policy_raw = build_policy_raw()
    body = mutator(_approval_body(policy_raw))
    assert parse_approval_comment(body) is None


# ---------------------------------------------------------------------------
# Verifier matrix (plan-required)
# ---------------------------------------------------------------------------


def test_correct_maintainer_comment_succeeds() -> None:
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw)
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    verified = _run_verify(_verifier(policy_raw, comment), snapshot_raw)
    assert verified.mechanism == APPROVAL_MECHANISM
    assert verified.signer_identity == TEST_APPROVER_IDENTITY
    assert verified.campaign_id == policy_raw["campaign_id"]
    assert verified.policy_digest == policy_raw["policy_digest"]
    assert verified.approval_sha256 == hashlib.sha256(
        render_yaml(snapshot_raw)
    ).hexdigest()


def test_wrong_author_fails() -> None:
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw)
    comment = _comment(body, author="someone-else")
    # The snapshot was transcribed for the authorized identity, but the
    # live comment was posted by a different account.
    snapshot_raw = _snapshot_raw(policy_raw, body, _comment(body))
    with pytest.raises(ProvenanceVerificationError, match="claimed_approver"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


def test_author_without_required_permission_fails() -> None:
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw)
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    for permission in ("write", "read", "none", None):
        with pytest.raises(ProvenanceVerificationError, match="permission"):
            _run_verify(
                _verifier(policy_raw, comment, permission=permission),
                snapshot_raw,
            )


def test_wrong_campaign_id_fails() -> None:
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw, campaign_id="EXP-9999-other")
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    with pytest.raises(ProvenanceVerificationError, match="campaign"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


def test_wrong_digest_fails() -> None:
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw, policy_digest="0" * 64)
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    with pytest.raises(ProvenanceVerificationError, match="policy_digest"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


def test_vague_comment_fails() -> None:
    policy_raw = build_policy_raw()
    body = "looks good to me, go ahead"
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, _approval_body(policy_raw), comment)
    snapshot_raw["approval_provenance"]["comment_body_sha256"] = hashlib.sha256(
        body.encode("utf-8")
    ).hexdigest()
    with pytest.raises(ProvenanceVerificationError, match="grammar"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


def test_reaction_only_approval_fails() -> None:
    policy_raw = build_policy_raw()
    comment = _comment("")
    snapshot_raw = _snapshot_raw(policy_raw, _approval_body(policy_raw), comment)
    snapshot_raw["approval_provenance"]["comment_body_sha256"] = hashlib.sha256(
        b""
    ).hexdigest()
    with pytest.raises(ProvenanceVerificationError, match="grammar"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


def test_edited_comment_fails() -> None:
    policy_raw = build_policy_raw()
    original = _approval_body(policy_raw)
    edited = original.replace("maximum_attempts: 3", "maximum_attempts: 2")
    original_comment = _comment(original)  # digest recorded at capture time
    snapshot_raw = _snapshot_raw(policy_raw, original, original_comment)
    comment = _comment(edited)  # live comment was edited after capture
    with pytest.raises(ProvenanceVerificationError, match="edited"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


def test_deleted_comment_fails() -> None:
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw)
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    with pytest.raises(ProvenanceVerificationError, match="deleted"):
        _run_verify(_verifier(policy_raw, None), snapshot_raw)


def test_expired_approval_fails() -> None:
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw, expires_at="2025-12-31T12:30:00Z")
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    with pytest.raises(ProvenanceVerificationError, match="expired"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


def test_expiry_beyond_policy_window_fails() -> None:
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw, expires_at="2099-01-01T00:00:00Z")
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    with pytest.raises(ProvenanceVerificationError, match="exceeds the policy"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


def test_attempt_limit_expansion_fails() -> None:
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw, maximum_attempts=5)
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    with pytest.raises(ProvenanceVerificationError, match="maximum_attempts"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


def test_concurrency_expansion_fails() -> None:
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw, concurrency=2)
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    with pytest.raises(ProvenanceVerificationError, match="concurrency"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


def test_automatic_merge_not_prohibited_fails() -> None:
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw, automatic_merge="allowed")
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    with pytest.raises(ProvenanceVerificationError, match="automatic_merge"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


def test_policy_without_merge_prohibition_fails() -> None:
    policy_raw = build_policy_raw(automatic_merge_prohibited=False)
    policy_raw["policy_digest"] = compute_policy_digest(policy_raw)
    body = _approval_body(policy_raw)
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    with pytest.raises(ProvenanceVerificationError, match="automatic merge"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


def test_wrong_classification_fails() -> None:
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw, classification="CANONICAL_EVIDENCE")
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    with pytest.raises(ProvenanceVerificationError, match="classification"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


def test_wrong_issue_fails() -> None:
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw)
    comment = _comment(body, issue=999)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    with pytest.raises(ProvenanceVerificationError, match="issue"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


def test_wrong_repository_fails() -> None:
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw)
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    snapshot_raw["approval_provenance"]["repository"] = "Someone/Else"
    with pytest.raises(ProvenanceVerificationError, match="repository"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


def test_fabricated_reference_fails() -> None:
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw)
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    snapshot_raw["approval_provenance"]["reference"] = (
        "https://github.com/ThorStarlord/sensemaking-skills/issues/122"
        "#issuecomment-999999"
    )
    with pytest.raises(ProvenanceVerificationError, match="reference"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


def test_approved_at_mismatch_fails() -> None:
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw)
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    snapshot_raw["approved_at"] = "2025-12-31T11:00:00Z"
    with pytest.raises(ProvenanceVerificationError, match="created_at"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


def test_statement_mismatch_fails() -> None:
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw)
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    snapshot_raw["approval_statement"] = "A different statement."
    with pytest.raises(ProvenanceVerificationError, match="statement"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


# ---------------------------------------------------------------------------
# Agent-generated fixtures cannot masquerade as live provenance
# ---------------------------------------------------------------------------


def test_agent_fixture_with_unknown_comment_id_fails() -> None:
    """A locally-authored approval naming a comment GitHub does not have
    (or that never existed) can never corroborate."""
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw)
    comment = _comment(body, comment_id="000000")
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    # The live fetch only knows the real comment id; the fixture names another.
    real_comment = _comment(body)
    with pytest.raises(ProvenanceVerificationError, match="deleted"):
        _run_verify(_verifier(policy_raw, real_comment), snapshot_raw)


def test_agent_fixture_with_forged_body_digest_fails() -> None:
    """A local snapshot claiming a body digest that does not match the live
    comment bytes fails byte-binding."""
    policy_raw = build_policy_raw()
    real_body = _approval_body(policy_raw)
    comment = _comment(real_body)
    snapshot_raw = _snapshot_raw(policy_raw, real_body, comment)
    snapshot_raw["approval_provenance"]["comment_body_sha256"] = hashlib.sha256(
        b"forged bytes"
    ).hexdigest()
    with pytest.raises(ProvenanceVerificationError, match="digest"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


def test_agent_fixture_with_forged_author_fails() -> None:
    policy_raw = build_policy_raw()
    real_body = _approval_body(policy_raw)
    comment = _comment(real_body, author=TEST_APPROVER_IDENTITY)
    snapshot_raw = _snapshot_raw(policy_raw, real_body, comment)
    snapshot_raw["claimed_approver_identity"] = "forged-identity"
    with pytest.raises(ProvenanceVerificationError, match="claimed_approver"):
        _run_verify(_verifier(policy_raw, comment), snapshot_raw)


# ---------------------------------------------------------------------------
# No provider involvement
# ---------------------------------------------------------------------------


def test_verifier_never_touches_the_provider_sdk() -> None:
    """Verification runs without importing or calling the provider SDK."""
    assert "claude_agent_sdk" not in sys.modules
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw)
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    _run_verify(_verifier(policy_raw, comment), snapshot_raw)
    assert "claude_agent_sdk" not in sys.modules


def test_verifier_fails_closed_without_policy() -> None:
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw)
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    verifier = GitHubIssueCommentApprovalVerifier(
        repository=GOVERNED_GITHUB_REPOSITORY,
        policy=None,
        fetch_comment=lambda cid: comment,
        fetch_permission=lambda login: "admin",
        clock=lambda: _NOW,
    )
    with pytest.raises(ProvenanceVerificationError, match="policy"):
        verifier.verify(snapshot_raw, approval_bytes=render_yaml(snapshot_raw))


def test_verifier_fails_closed_without_approval_bytes() -> None:
    policy_raw = build_policy_raw()
    body = _approval_body(policy_raw)
    comment = _comment(body)
    snapshot_raw = _snapshot_raw(policy_raw, body, comment)
    with pytest.raises(ProvenanceVerificationError, match="bytes"):
        _verifier(policy_raw, comment).verify(snapshot_raw, approval_bytes=None)


# ---------------------------------------------------------------------------
# Capture (mechanical transcription)
# ---------------------------------------------------------------------------


def _genuine_policy(policy_raw: dict):
    result = validate_campaign_policy(
        render_yaml(policy_raw),
        ValidationContext(
            current_time=TEST_VALIDATION_TIME,
            allowed_approver_identities=frozenset(),
        ),
    )
    assert result.valid, f"{result.failure_code}: {result.detail}"
    return result.value


def test_capture_transcribes_human_comment(tmp_path: Path) -> None:
    policy_raw = build_policy_raw()
    policy = _genuine_policy(policy_raw)
    body = _approval_body(policy_raw)
    comment = _comment(body)
    out = tmp_path / "approval.yaml"
    snapshot_bytes, captured = capture_approval_snapshot(
        issue_number=_ISSUE,
        policy=policy,
        out_path=out,
        fetch_comments=lambda issue: [comment],
        fetch_permission=lambda login: "admin",
        now=_NOW,
    )
    assert captured["id"] == _COMMENT_ID
    assert out.read_bytes() == snapshot_bytes
    parsed = parse_approval_comment(comment["body"])
    # The snapshot round-trips and carries the verbatim transcription.
    from sensemaking_skills.campaign_validation import parse_two_lane_yaml
    snap = parse_two_lane_yaml(snapshot_bytes)
    assert snap["claimed_approver_identity"] == TEST_APPROVER_IDENTITY
    assert snap["approval_provenance"]["comment_id"] == _COMMENT_ID
    assert snap["approval_provenance"]["reference"] == comment["html_url"]
    assert snap["approved_at"] == comment["created_at"]
    assert snap["approval_statement"] == parsed["statement"]
    assert snap["approval_provenance"]["comment_body_sha256"] == hashlib.sha256(
        comment["body"].encode("utf-8")
    ).hexdigest()


def test_capture_picks_newest_matching_comment(tmp_path: Path) -> None:
    policy_raw = build_policy_raw()
    policy = _genuine_policy(policy_raw)
    older = _comment(_approval_body(policy_raw), comment_id="100")
    newest = _comment(_approval_body(policy_raw), comment_id="200")
    _, captured = capture_approval_snapshot(
        issue_number=_ISSUE,
        policy=policy,
        out_path=tmp_path / "approval.yaml",
        fetch_comments=lambda issue: [older, newest],
        fetch_permission=lambda login: "admin",
        now=_NOW,
    )
    assert captured["id"] == "200"


def test_capture_refuses_comment_without_permission(tmp_path: Path) -> None:
    policy_raw = build_policy_raw()
    policy = _genuine_policy(policy_raw)
    comment = _comment(_approval_body(policy_raw))
    with pytest.raises(ApprovalCaptureError, match="permission"):
        capture_approval_snapshot(
            issue_number=_ISSUE,
            policy=policy,
            out_path=tmp_path / "approval.yaml",
            fetch_comments=lambda issue: [comment],
            fetch_permission=lambda login: "read",
            now=_NOW,
        )
    assert not (tmp_path / "approval.yaml").exists()


def test_capture_refuses_no_matching_comment(tmp_path: Path) -> None:
    policy_raw = build_policy_raw()
    policy = _genuine_policy(policy_raw)
    vague = _comment("looks good to me")
    other_campaign = _comment(
        _approval_body(policy_raw, campaign_id="EXP-9999-other")
    )
    with pytest.raises(ApprovalCaptureError, match="no approval comment"):
        capture_approval_snapshot(
            issue_number=_ISSUE,
            policy=policy,
            out_path=tmp_path / "approval.yaml",
            fetch_comments=lambda issue: [vague, other_campaign],
            fetch_permission=lambda login: "admin",
            now=_NOW,
        )
    assert not (tmp_path / "approval.yaml").exists()


# ---------------------------------------------------------------------------
# Runner mechanism dispatch
# ---------------------------------------------------------------------------


def _genuine_bundle(approval_raw: dict) -> tuple:
    policy_raw = build_policy_raw()
    config_raw = build_configuration_raw()
    policy_raw["allowed_configuration_ids"] = sorted([config_raw["configuration_id"]])
    policy_raw["policy_digest"] = compute_policy_digest(policy_raw)
    approval_raw["campaign_id"] = policy_raw["campaign_id"]
    approval_raw["policy_digest"] = policy_raw["policy_digest"]
    result = validate_campaign_bundle(
        render_yaml(policy_raw),
        render_yaml(approval_raw),
        render_yaml(config_raw),
        ValidationContext(
            current_time=TEST_VALIDATION_TIME,
            allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
        ),
    )
    assert result.valid, f"{result.failure_code}: {result.detail}"
    return result.value, config_raw


def _runner_instance(tmp_path: Path):
    from execution_infra.runner import GovernedCampaignRunner

    return GovernedCampaignRunner(
        campaign_package_dir=tmp_path,
        campaign_root=tmp_path / "root",
        framework_checkout=Path(__file__).resolve().parents[2],
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
    )


def test_runner_dispatch_github_mechanism(tmp_path: Path) -> None:
    body = _approval_body(build_policy_raw())
    comment = _comment(body)
    approval_raw = _snapshot_raw(build_policy_raw(), body, comment)
    bundle, config_raw = _genuine_bundle(approval_raw)
    target = SimpleNamespace(path=tmp_path / "target")
    runner = _runner_instance(tmp_path)
    verifier, provider, validate = runner._production_components(
        config_raw, target, bundle
    )
    assert isinstance(verifier, GitHubIssueCommentApprovalVerifier)
    # The verifier is pinned to the governed repository, never to the
    # provenance-supplied value (an approval naming another repository
    # must fail inside verify(), not redirect the verifier).
    assert verifier._repository == GOVERNED_GITHUB_REPOSITORY.casefold()


def test_runner_dispatch_github_mechanism_ignores_provenance_repo(
    tmp_path: Path,
) -> None:
    """An approval naming a foreign repository still constructs a verifier
    pinned to the governed repository; verification then fails on the
    repository mismatch."""
    body = _approval_body(build_policy_raw())
    comment = _comment(body)
    approval_raw = _snapshot_raw(build_policy_raw(), body, comment)
    approval_raw["approval_provenance"]["repository"] = "EvilOrg/EvilRepo"
    bundle, config_raw = _genuine_bundle(approval_raw)
    target = SimpleNamespace(path=tmp_path / "target")
    runner = _runner_instance(tmp_path)
    verifier, provider, validate = runner._production_components(
        config_raw, target, bundle
    )
    assert isinstance(verifier, GitHubIssueCommentApprovalVerifier)
    assert verifier._repository == GOVERNED_GITHUB_REPOSITORY.casefold()
    # The repository mismatch fires pre-fetch, before any body binding.
    with pytest.raises(ProvenanceVerificationError, match="repository"):
        verifier.verify(bundle.approval, approval_bytes=b"unused")


def test_runner_dispatch_signed_commit_mechanism(tmp_path: Path) -> None:
    approval_raw = {
        "approval_schema_version": "1",
        "campaign_id": "",
        "policy_digest": "",
        "claimed_approver_identity": TEST_APPROVER_IDENTITY,
        "approval_provenance": {
            "mechanism": "signed_commit",
            "reference": "000000000000000000000000000000000000c0de",
        },
        "approval_statement": "Test-only approval statement.",
        "approved_at": "2026-01-01T00:00:00+00:00",
    }
    bundle, config_raw = _genuine_bundle(approval_raw)
    target = SimpleNamespace(path=tmp_path / "target")
    runner = _runner_instance(tmp_path)
    verifier, provider, validate = runner._production_components(
        config_raw, target, bundle
    )
    assert isinstance(verifier, ProductionSignedCommitVerifier)


def test_runner_dispatch_unknown_mechanism_refuses(tmp_path: Path) -> None:
    from execution_infra.runner import RunnerRefusal

    approval_raw = {
        "approval_schema_version": "1",
        "campaign_id": "",
        "policy_digest": "",
        "claimed_approver_identity": TEST_APPROVER_IDENTITY,
        "approval_provenance": {
            "mechanism": "carrier_pigeon",
            "reference": "some-reference",
        },
        "approval_statement": "Test-only approval statement.",
        "approved_at": "2026-01-01T00:00:00+00:00",
    }
    bundle, config_raw = _genuine_bundle(approval_raw)
    target = SimpleNamespace(path=tmp_path / "target")
    runner = _runner_instance(tmp_path)
    with pytest.raises(RunnerRefusal, match="mechanism"):
        runner._production_components(config_raw, target, bundle)
