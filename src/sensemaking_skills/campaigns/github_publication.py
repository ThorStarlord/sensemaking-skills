"""Explicit GitHub publication of deterministic Campaign provenance.

Publication is preview-by-default and requires an explicit publish transition.
The publisher posts to the GitHub Issue Comments API, which also covers pull
requests. It never selects a repository/issue, reads tokens from output, or
upgrades mechanical provenance into semantic truth.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Protocol
from urllib import error, request

from .provenance import CampaignProvenanceService, render_provenance_markdown


_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_API_VERSION = "2022-11-28"


class GitHubPublicationError(RuntimeError):
    pass


class JsonTransport(Protocol):
    def request_json(
        self,
        *,
        method: str,
        url: str,
        token: str,
        payload: dict[str, Any] | None = None,
    ) -> Any: ...


class UrllibGitHubTransport:
    """Small stdlib-only GitHub JSON transport."""

    def request_json(
        self,
        *,
        method: str,
        url: str,
        token: str,
        payload: dict[str, Any] | None = None,
    ) -> Any:
        data = None
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": _API_VERSION,
                "Content-Type": "application/json",
                "User-Agent": "sensemaking-skills",
            },
        )
        try:
            with request.urlopen(req, timeout=30) as response:
                body = response.read().decode("utf-8")
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise GitHubPublicationError(
                f"GitHub API returned HTTP {exc.code}: {detail[:500]}"
            ) from exc
        except error.URLError as exc:
            raise GitHubPublicationError(f"GitHub API request failed: {exc}") from exc
        if not body:
            return None
        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise GitHubPublicationError(
                "GitHub API returned non-JSON response"
            ) from exc


@dataclass(frozen=True)
class GitHubProvenanceProjection:
    repository: str
    issue_number: int
    endpoint: str
    marker: str
    body: str
    body_sha256: str
    campaign_id: str
    semantic_truth_established: bool = False


def build_github_provenance_projection(
    workspace: str | Path,
    *,
    repository: str,
    issue_number: int,
) -> GitHubProvenanceProjection:
    if not isinstance(repository, str) or not _REPOSITORY.fullmatch(repository):
        raise ValueError("repository must be OWNER/REPO")
    if not isinstance(issue_number, int) or issue_number <= 0:
        raise ValueError("issue_number must be a positive integer")

    provenance = CampaignProvenanceService(workspace).inspect()
    rendered = render_provenance_markdown(provenance).rstrip() + "\n"
    body_sha256 = hashlib.sha256(rendered.encode("utf-8")).hexdigest()
    marker = (
        "<!-- sensemaking-provenance:v1 "
        f"campaign={provenance.campaign_id} sha256={body_sha256} -->"
    )
    body = marker + "\n" + rendered
    return GitHubProvenanceProjection(
        repository=repository,
        issue_number=issue_number,
        endpoint=(
            f"https://api.github.com/repos/{repository}/issues/"
            f"{issue_number}/comments"
        ),
        marker=marker,
        body=body,
        body_sha256=body_sha256,
        campaign_id=provenance.campaign_id,
    )


def github_provenance_payload(
    value: GitHubProvenanceProjection,
    *,
    published: bool = False,
    already_present: bool = False,
    comment_id: int | None = None,
    comment_url: str | None = None,
    authorization_explicit: bool = False,
) -> dict[str, Any]:
    return {
        "repository": value.repository,
        "issue_number": value.issue_number,
        "campaign_id": value.campaign_id,
        "endpoint": value.endpoint,
        "marker": value.marker,
        "body": value.body,
        "body_sha256": value.body_sha256,
        "published": published,
        "already_present": already_present,
        "comment_id": comment_id,
        "comment_url": comment_url,
        "authorization_explicit": authorization_explicit,
        "publication_selected_by_tool": False,
        "semantic_truth_established": False,
        "explicit_limit": (
            "Publishing deterministic Campaign provenance does not establish "
            "semantic correctness, authorize repository work, or alter Campaign state."
        ),
    }


class GitHubProvenancePublisher:
    """Preview and explicitly publish one exact provenance projection."""

    def __init__(self, transport: JsonTransport | None = None) -> None:
        self.transport = transport or UrllibGitHubTransport()

    def publish(
        self,
        projection: GitHubProvenanceProjection,
        *,
        token: str,
    ) -> dict[str, Any]:
        if not isinstance(token, str) or not token:
            raise ValueError("GitHub token must be non-empty")

        existing = self.transport.request_json(
            method="GET",
            url=projection.endpoint + "?per_page=100",
            token=token,
        )
        if not isinstance(existing, list):
            raise GitHubPublicationError(
                "GitHub comments response must be a JSON list"
            )
        for item in existing:
            if not isinstance(item, dict):
                continue
            body = item.get("body")
            if isinstance(body, str) and projection.marker in body:
                return github_provenance_payload(
                    projection,
                    published=True,
                    already_present=True,
                    comment_id=(
                        int(item["id"]) if isinstance(item.get("id"), int) else None
                    ),
                    comment_url=(
                        str(item["html_url"])
                        if isinstance(item.get("html_url"), str)
                        else None
                    ),
                    authorization_explicit=True,
                )

        created = self.transport.request_json(
            method="POST",
            url=projection.endpoint,
            token=token,
            payload={"body": projection.body},
        )
        if not isinstance(created, dict):
            raise GitHubPublicationError(
                "GitHub comment creation response must be a JSON object"
            )
        return github_provenance_payload(
            projection,
            published=True,
            already_present=False,
            comment_id=(
                int(created["id"]) if isinstance(created.get("id"), int) else None
            ),
            comment_url=(
                str(created["html_url"])
                if isinstance(created.get("html_url"), str)
                else None
            ),
            authorization_explicit=True,
        )
