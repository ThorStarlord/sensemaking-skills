"""GitHub issue-comment campaign approval (Lane A beta, Model B).

Framework-governed replacement for the signed-commit ceremony on Lane A
beta campaigns: the human posts ONE approval comment on the campaign's
GitHub issue, trusted framework code transcribes that comment into the
operative ``approval.yaml`` (mechanical transcription, never agent-authored
consent), and this verifier corroborates the snapshot against the LIVE
GitHub API before every capability mint.

The verification chain (fail closed at every step):

    comment exists and is not deleted (404 = deleted)
        -> belongs to the governed repository and the recorded issue
        -> author login is a maintainer with the required repository
           permission (GitHub permissions, not a fingerprint registry)
        -> author login equals the approval's claimed_approver_identity
        -> body parses as the governed approval grammar (marker + exact
           fields + explicit authorization statement)
        -> campaign_id / policy_digest / attempt limit / concurrency /
           automatic-merge rule / classification / expiry agree with the
           validated policy (nothing may exceed the policy envelope)
        -> sha256(exact body bytes) equals provenance.comment_body_sha256
        -> approved_at equals the comment's created_at
        -> the parsed statement equals approval_statement

Editing or deleting the comment after capture fails verification: any
edit changes the body, so the body digest can never match; a deleted
comment is a 404. Every attempt re-verifies because mint calls the
verifier per attempt. A locally-authored snapshot that does not
correspond to a real GitHub comment (agent fixture) can never pass:
the verifier always re-fetches from GitHub and never trusts local bytes
alone.

The GitHub token is read from the environment (``GITHUB_TOKEN`` or
``GH_TOKEN``) when no token is supplied; without a token the live fetchers
fail closed. Tests inject fake fetchers, so no verifier test ever touches
the network or the provider.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.error
import urllib.request
from collections.abc import Callable, Mapping
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from sensemaking_skills.campaign_validation import validate_campaign_approval
from sensemaking_skills.campaign_validation.models import ValidationContext
from sensemaking_skills.campaign_validation.yaml_profile import dump_two_lane_yaml
from sensemaking_skills.exploratory_authorization.models import (
    VerifiedApprovalProvenance,
)
from sensemaking_skills.exploratory_authorization.provenance import (
    ProvenanceVerificationError,
)

from .execution_identity import (
    GOVERNED_GITHUB_REPOSITORY,
    GOVERNED_REQUIRED_APPROVER_PERMISSION,
)

APPROVAL_MECHANISM = "github_issue_comment_approval"
APPROVAL_MARKER = "APPROVE_EXPLORATORY_CAMPAIGN"

_KNOWN_FIELDS = (
    "campaign_id",
    "policy_digest",
    "maximum_attempts",
    "concurrency",
    "automatic_merge",
    "classification",
    "expires_at",
)
_REQUIRED_FIELDS = set(_KNOWN_FIELDS)
_FIELD_RE = re.compile(r"^([a-z_]+):\s*(.*)$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_COMMENT_ID_RE = re.compile(r"^[0-9]+$")
_ISSUE_REF_RE = re.compile(r"^([0-9]+)$")

#: GitHub collaborator permission hierarchy (highest first). Unknown
#: values rank as "none" and fail any required permission.
_PERMISSION_RANK = {
    "admin": 5,
    "maintain": 4,
    "write": 3,
    "triage": 2,
    "read": 1,
    "none": 0,
}


class GitHubApprovalError(Exception):
    """Capture/verification infrastructure failure (token, network, API)."""


#: Structural self-check offset (see ``capture_approval_snapshot``).
_ONE_MINUTE = timedelta(minutes=1)


def _norm_repository(value: Any) -> str:
    """Reduce a repository string to ``owner/repo`` for equality checks."""
    text = str(value or "").strip().rstrip("/").removesuffix(".git")
    return text.casefold()


def _parse_rfc3339(value: Any) -> datetime | None:
    try:
        return datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------------------
# Approval comment grammar
# ---------------------------------------------------------------------------


def parse_approval_comment(body: str) -> dict[str, Any] | None:
    """Parse a GitHub comment body as an approval comment.

    Grammar (exact)::

        APPROVE_EXPLORATORY_CAMPAIGN

        campaign_id: <id>
        policy_digest: <64-hex>
        maximum_attempts: <int>
        concurrency: <int>
        automatic_merge: prohibited
        classification: <classification>
        expires_at: <RFC3339>

        <explicit authorization statement containing "authorize">

    Returns the parsed field mapping (``campaign_id``, ``policy_digest``,
    ``maximum_attempts``, ``concurrency``, ``automatic_merge``,
    ``classification``, ``expires_at``, ``statement``) or ``None`` when the
    body is not an approval comment (vague comment, missing marker, missing
    or duplicate fields, unknown field lines inside the field block,
    malformed values, or a statement without the word "authorize").
    """
    if not isinstance(body, str) or not body.strip():
        return None
    lines = [ln.rstrip("\r") for ln in body.split("\n")]
    # Locate the marker as the first non-blank line.
    first = 0
    while first < len(lines) and not lines[first].strip():
        first += 1
    if first >= len(lines) or lines[first].strip() != APPROVAL_MARKER:
        return None

    fields: dict[str, Any] = {}
    statement_lines: list[str] = []
    in_fields = True
    for ln in lines[first + 1 :]:
        stripped = ln.strip()
        if not stripped:
            continue
        if in_fields:
            match = _FIELD_RE.match(stripped)
            if match is not None:
                key = match.group(1)
                if key not in _KNOWN_FIELDS:
                    return None  # unknown field inside the block
                if key in fields:
                    return None  # duplicate field
                fields[key] = match.group(2).strip()
                continue
            # A non-field line ends the field block and starts the statement.
            in_fields = False
        statement_lines.append(stripped)

    if not set(fields) >= _REQUIRED_FIELDS:
        return None

    try:
        maximum_attempts = int(fields["maximum_attempts"])
        concurrency = int(fields["concurrency"])
    except ValueError:
        return None
    if str(fields["policy_digest"]) and _SHA256_RE.fullmatch(fields["policy_digest"]) is None:
        return None
    if _parse_rfc3339(fields["expires_at"]) is None:
        return None
    statement = "\n".join(statement_lines).strip()
    if not statement or "authorize" not in statement.casefold():
        return None
    return {
        "campaign_id": fields["campaign_id"],
        "policy_digest": fields["policy_digest"],
        "maximum_attempts": maximum_attempts,
        "concurrency": concurrency,
        "automatic_merge": fields["automatic_merge"],
        "classification": fields["classification"],
        "expires_at": fields["expires_at"],
        "statement": statement,
    }


# ---------------------------------------------------------------------------
# GitHub API plumbing (live fetchers; tests inject doubles)
# ---------------------------------------------------------------------------


def _github_token() -> str:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
    if not token:
        raise GitHubApprovalError(
            "no GitHub token: set GITHUB_TOKEN or GH_TOKEN (fail closed; "
            "the verifier never proceeds without repository access)"
        )
    return token


def _github_get(url: str, *, token: str, timeout: int = 30) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "sensemaking-skills-governed-runner",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise GitHubApprovalError(f"github API 404 for {url}") from exc
        if exc.code in (401, 403):
            raise GitHubApprovalError(
                f"github API {exc.code} for {url} (auth or rate limit; "
                "fail closed)"
            ) from exc
        raise GitHubApprovalError(f"github API {exc.code} for {url}") from exc
    except urllib.error.URLError as exc:
        raise GitHubApprovalError(f"github API unreachable: {exc}") from exc


def _fetch_comment_live(repository: str, comment_id: str, *, token: str) -> dict[str, Any] | None:
    """Fetch one issue comment; ``None`` when it no longer exists (deleted)."""
    url = (
        f"https://api.github.com/repos/{repository}/issues/comments/"
        f"{comment_id}"
    )
    try:
        return _github_get(url, token=token)
    except GitHubApprovalError as exc:
        if "404" in str(exc):
            return None
        raise


def _fetch_permission_live(repository: str, login: str, *, token: str) -> str | None:
    url = (
        f"https://api.github.com/repos/{repository}/collaborators/"
        f"{login}/permission"
    )
    try:
        data = _github_get(url, token=token)
    except GitHubApprovalError as exc:
        if "404" in str(exc):
            return None
        raise
    return str(data.get("permission", ""))


def _fetch_comments_live(repository: str, issue_number: int, *, token: str) -> list[dict[str, Any]]:
    """Fetch all comments of an issue (newest last; caller sorts)."""
    comments: list[dict[str, Any]] = []
    url: str | None = (
        f"https://api.github.com/repos/{repository}/issues/{issue_number}"
        "/comments?per_page=100"
    )
    for _ in range(10):
        request = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "User-Agent": "sensemaking-skills-governed-runner",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                comments.extend(json.loads(response.read().decode("utf-8")))
                link = response.headers.get("Link", "")
        except urllib.error.HTTPError as exc:
            raise GitHubApprovalError(
                f"github API {exc.code} listing comments of issue "
                f"{issue_number}"
            ) from exc
        except urllib.error.URLError as exc:
            raise GitHubApprovalError(f"github API unreachable: {exc}") from exc
        next_url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                match = re.search(r"<([^>]+)>", part)
                if match:
                    next_url = match.group(1)
        if next_url is None:
            break
        url = next_url
    return comments


# ---------------------------------------------------------------------------
# The verifier
# ---------------------------------------------------------------------------


class GitHubIssueCommentApprovalVerifier:
    """Corroborates a ``github_issue_comment_approval`` provenance reference
    against the live GitHub API with full body- and identity-binding.

    Constructor arguments are framework-governed (the runner constructs
    this verifier from the pinned framework and the validated bundle; a
    caller-supplied verifier can never authorize the real campaign):
    ``repository`` is the governed repository, ``required_permission`` the
    minimum collaborator permission, and ``policy`` the validated campaign
    policy (limits/expiry checks trace to it). ``fetch_comment`` and
    ``fetch_permission`` are test seams; the defaults call the live API
    with the environment token.
    """

    def __init__(
        self,
        *,
        repository: str = GOVERNED_GITHUB_REPOSITORY,
        required_permission: str = GOVERNED_REQUIRED_APPROVER_PERMISSION,
        policy: Mapping[str, Any] | None = None,
        token: str | None = None,
        clock: Callable[[], datetime] | None = None,
        fetch_comment: Callable[[str], dict[str, Any] | None] | None = None,
        fetch_permission: Callable[[str], str | None] | None = None,
    ) -> None:
        self._repository = _norm_repository(repository)
        self._required_permission = required_permission
        self._policy = policy
        self._token = token
        self._clock = clock or (lambda: datetime.now(UTC))
        self._fetch_comment = fetch_comment
        self._fetch_permission = fetch_permission

    # -- live seams ---------------------------------------------------------

    def _comment(self, comment_id: str) -> dict[str, Any] | None:
        if self._fetch_comment is not None:
            return self._fetch_comment(comment_id)
        token = self._token or _github_token()
        return _fetch_comment_live(self._repository, comment_id, token=token)

    def _permission(self, login: str) -> str | None:
        if self._fetch_permission is not None:
            return self._fetch_permission(login)
        token = self._token or _github_token()
        return _fetch_permission_live(self._repository, login, token=token)

    # -- verification --------------------------------------------------------

    def verify(
        self, approval: Any, *, approval_bytes: bytes | None = None
    ) -> VerifiedApprovalProvenance:
        raw = getattr(approval, "raw", approval) or {}
        provenance = dict(raw.get("approval_provenance") or {})
        mechanism = str(provenance.get("mechanism", ""))
        if mechanism != APPROVAL_MECHANISM:
            raise ProvenanceVerificationError(
                f"github-issue-comment verifier: provenance mechanism "
                f"{mechanism!r} is not {APPROVAL_MECHANISM!r}"
            )
        if approval_bytes is None:
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: no operative approval bytes "
                "were supplied; body-binding cannot be proven (fail closed)"
            )
        if self._policy is None:
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: no validated policy was "
                "supplied; attempt-limit and expiry checks are impossible "
                "(fail closed)"
            )

        comment_id = str(provenance.get("comment_id", "")).strip()
        reference = str(provenance.get("reference", "")).strip()
        body_sha256 = str(provenance.get("comment_body_sha256", "")).strip()
        repository = str(provenance.get("repository") or "").strip()
        issue_number_raw = str(provenance.get("issue_number", "")).strip()

        if _COMMENT_ID_RE.fullmatch(comment_id) is None:
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: provenance comment_id is "
                f"not a numeric comment id: {comment_id!r}"
            )
        if _ISSUE_REF_RE.fullmatch(issue_number_raw) is None:
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: provenance issue_number is "
                f"not numeric: {issue_number_raw!r}"
            )
        if _SHA256_RE.fullmatch(body_sha256) is None:
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: provenance "
                "comment_body_sha256 is not a sha256 hex digest"
            )
        if not repository:
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: provenance repository is "
                "empty (fail closed)"
            )

        # 1/3 (pre-fetch). The provenance must name the GOVERNED repository;
        # this is checked before any network call so a foreign-repository
        # approval fails without even contacting GitHub.
        if _norm_repository(repository) != self._repository:
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: provenance repository "
                f"{repository!r} is not the governed repository "
                f"{self._repository!r}"
            )

        # 2/3. The comment must exist right now (deleted = 404 = absent).
        comment = self._comment(comment_id)
        if comment is None:
            raise ProvenanceVerificationError(
                f"github-issue-comment verifier: comment {comment_id} does "
                "not exist or has been deleted on GitHub; an approval "
                "comment cannot be deleted and remain operative"
            )

        # 3/3. Issue, reference, author, permission, body.
        issue_url = str(comment.get("issue_url", ""))
        expected_issue = (
            f"/repos/{self._repository}/issues/{int(issue_number_raw)}"
        )
        if not issue_url.casefold().endswith(expected_issue.casefold()):
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: comment does not belong to "
                f"the recorded issue ({issue_url!r} does not end with "
                f"{expected_issue!r})"
            )
        expected_ref = (
            f"github.com/{self._repository}/issues/{int(issue_number_raw)}"
            f"#issuecomment-{comment_id}"
        )
        if expected_ref not in reference.casefold():
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: provenance reference is not "
                f"the comment URL (expected {expected_ref!r} in "
                f"{reference!r})"
            )

        author = str((comment.get("user") or {}).get("login", ""))
        claimed = str(raw.get("claimed_approver_identity", "") or "")
        if not author or author != claimed:
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: comment author "
                f"{author!r} does not match claimed_approver_identity "
                f"{claimed!r}"
            )
        permission = self._permission(author)
        required_rank = _PERMISSION_RANK.get(
            self._required_permission, 100
        )
        actual_rank = _PERMISSION_RANK.get(str(permission or "").casefold(), 0)
        if permission is None or actual_rank < required_rank:
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: comment author "
                f"{author!r} has permission {permission!r}, below the "
                f"required {self._required_permission!r}"
            )

        body = str(comment.get("body", ""))
        if hashlib.sha256(body.encode("utf-8")).hexdigest() != body_sha256:
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: live comment body digest "
                "does not match provenance.comment_body_sha256; the comment "
                "was edited after the approval snapshot was recorded"
            )

        # 3/3. Grammar, policy agreement, statement, timestamps, digest.
        parsed = parse_approval_comment(body)
        if parsed is None:
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: comment body does not "
                "parse as the governed approval grammar (vague or "
                "malformed approval comment)"
            )
        policy = self._policy
        if parsed["campaign_id"] != str(raw.get("campaign_id", "")):
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: parsed campaign_id does "
                "not match the approval document"
            )
        if parsed["policy_digest"] != str(raw.get("policy_digest", "")):
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: parsed policy_digest does "
                "not match the approval document"
            )
        if parsed["campaign_id"] != str(policy.get("campaign_id", "")):
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: comment names a different "
                "campaign than the validated policy"
            )
        if parsed["policy_digest"] != str(policy.get("policy_digest", "")):
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: comment binds a different "
                "policy_digest than the validated policy"
            )
        if parsed["maximum_attempts"] > int(policy.get("max_attempt_slots", 0)):
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: comment maximum_attempts "
                f"{parsed['maximum_attempts']} exceeds the policy limit "
                f"{policy.get('max_attempt_slots')}"
            )
        if parsed["concurrency"] > int(policy.get("concurrency_ceiling", 0)):
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: comment concurrency "
                f"{parsed['concurrency']} exceeds the policy ceiling "
                f"{policy.get('concurrency_ceiling')}"
            )
        if parsed["automatic_merge"].strip().casefold() != "prohibited":
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: comment automatic_merge is "
                f"{parsed['automatic_merge']!r}, not 'prohibited'"
            )
        if policy.get("automatic_merge_prohibited") is not True:
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: the validated policy does "
                "not prohibit automatic merge; the comment's prohibition "
                "cannot bind it"
            )
        if parsed["classification"] != str(policy.get("classification", "")):
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: comment classification "
                f"{parsed['classification']!r} differs from the policy "
                f"{policy.get('classification')!r}"
            )
        window = policy.get("validity_window") or {}
        not_after = _parse_rfc3339(window.get("not_after"))
        expires_at = _parse_rfc3339(parsed["expires_at"])
        approved_at = _parse_rfc3339(raw.get("approved_at"))
        created_at = _parse_rfc3339(comment.get("created_at"))
        if approved_at is None or created_at is None or approved_at != created_at:
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: approval approved_at does "
                "not equal the comment's created_at"
            )
        if expires_at is None:
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: comment expires_at is not "
                "a valid RFC3339 timestamp"
            )
        if expires_at <= approved_at:
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: comment expires_at is not "
                "after the approval time"
            )
        if not_after is not None and expires_at > not_after:
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: comment expires_at "
                f"{parsed['expires_at']} exceeds the policy window end "
                f"{window.get('not_after')}"
            )
        if expires_at <= self._clock():
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: the approval has expired "
                f"(expires_at {parsed['expires_at']} is not in the future)"
            )
        if parsed["statement"] != str(raw.get("approval_statement", "")):
            raise ProvenanceVerificationError(
                "github-issue-comment verifier: parsed approval statement "
                "does not match the approval document's "
                "approval_statement"
            )

        return VerifiedApprovalProvenance(
            mechanism=APPROVAL_MECHANISM,
            reference=reference,
            signer_identity=author,
            approval_sha256=hashlib.sha256(approval_bytes).hexdigest(),
            campaign_id=str(raw.get("campaign_id", "")),
            policy_digest=str(raw.get("policy_digest", "")),
        )


# ---------------------------------------------------------------------------
# Approval snapshot capture (mechanical transcription, never consent)
# ---------------------------------------------------------------------------


class ApprovalCaptureError(Exception):
    """No verifiable human approval comment could be captured."""


def capture_approval_snapshot(
    *,
    repository: str = GOVERNED_GITHUB_REPOSITORY,
    issue_number: int,
    policy: Mapping[str, Any],
    token: str | None = None,
    out_path: Path | None = None,
    required_permission: str = GOVERNED_REQUIRED_APPROVER_PERMISSION,
    fetch_comments: Callable[[int], list[dict[str, Any]]] | None = None,
    fetch_permission: Callable[[str], str | None] | None = None,
    now: datetime | None = None,
) -> tuple[bytes, dict[str, Any]]:
    """Find the newest approval comment on the issue and transcribe it into
    the operative approval snapshot.

    The comment must parse as the governed grammar AND name the exact
    campaign_id and policy_digest of ``policy`` (a genuine validated
    ``CampaignPolicy`` or its raw mapping); its author must hold
    ``required_permission`` on the repository. The snapshot is a verbatim
    transcription of GitHub data (comment id, body digest, author, creation
    time, html_url) plus the policy fields -- trusted code recording a
    human-authored artifact, never agent-authored consent. When ``out_path``
    is given the snapshot is written there (profile-compliant YAML) after a
    self-check through the real ``validate_campaign_approval``.

    The self-check uses a validation time inside the policy window (the
    runner, not this tool, enforces the window at execution); the current
    wall clock is used whenever it is already inside the window.

    Returns ``(snapshot_bytes, comment)``. Raises ``ApprovalCaptureError``
    when no comment qualifies (nothing is written).
    """
    policy_raw = getattr(policy, "raw", policy)
    if fetch_comments is not None:
        comments = fetch_comments(issue_number)
    else:
        live_token = token or _github_token()
        comments = _fetch_comments_live(repository, issue_number, token=live_token)

    campaign_id = str(policy_raw.get("campaign_id", ""))
    policy_digest = str(policy_raw.get("policy_digest", ""))
    required_rank = _PERMISSION_RANK.get(required_permission, 100)
    check_now = now or datetime.now(UTC)
    window = policy_raw.get("validity_window") or {}
    not_before = _parse_rfc3339(window.get("not_before"))
    not_after = _parse_rfc3339(window.get("not_after"))
    if not_before is not None and check_now < not_before:
        check_now = not_before + _ONE_MINUTE  # structural self-check only
    elif not_after is not None and check_now >= not_after:
        check_now = not_after - _ONE_MINUTE

    # Newest first (GitHub comment ids are monotonic).
    for comment in sorted(comments, key=lambda c: int(c.get("id", 0)), reverse=True):
        body = str(comment.get("body", ""))
        parsed = parse_approval_comment(body)
        if parsed is None:
            continue
        if parsed["campaign_id"] != campaign_id or parsed["policy_digest"] != policy_digest:
            continue
        author = str((comment.get("user") or {}).get("login", ""))
        if not author:
            continue
        if fetch_permission is not None:
            permission = fetch_permission(author)
        else:
            live_token = token or _github_token()
            permission = _fetch_permission_live(repository, author, token=live_token)
        actual_rank = _PERMISSION_RANK.get(str(permission or "").casefold(), 0)
        if permission is None or actual_rank < required_rank:
            raise ApprovalCaptureError(
                f"approval comment {comment.get('id')} author {author!r} has "
                f"permission {permission!r}, below required "
                f"{required_permission!r}"
            )

        comment_id = str(comment.get("id", ""))
        created_at = str(comment.get("created_at", ""))
        html_url = str(comment.get("html_url", ""))
        snapshot = {
            "approval_schema_version": "1",
            "campaign_id": campaign_id,
            "policy_digest": policy_digest,
            "claimed_approver_identity": author,
            "approval_provenance": {
                "mechanism": APPROVAL_MECHANISM,
                "reference": html_url,
                "repository": repository,
                "issue_number": str(issue_number),
                "comment_id": comment_id,
                "comment_body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
            },
            "approval_statement": parsed["statement"],
            "approved_at": created_at,
        }
        snapshot_bytes = dump_two_lane_yaml(snapshot).encode("utf-8")

        # Self-check with the REAL validator before anything is written.
        # ``policy`` must be a genuine validated CampaignPolicy (the CLI
        # validates it first); a raw mapping fails closed here.
        context = ValidationContext(
            current_time=check_now.isoformat(),
            allowed_approver_identities=frozenset({author}),
        )
        result = validate_campaign_approval(snapshot_bytes, policy, context)
        if not result.valid:
            raise ApprovalCaptureError(
                f"captured snapshot failed the real validator: "
                f"{result.failure_code} {result.detail}"
            )

        if out_path is not None:
            out_path = Path(out_path)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(snapshot_bytes)
        return snapshot_bytes, comment

    raise ApprovalCaptureError(
        f"no approval comment found on issue {issue_number} matching "
        f"campaign {campaign_id!r} and policy_digest {policy_digest[:16]}..."
    )
