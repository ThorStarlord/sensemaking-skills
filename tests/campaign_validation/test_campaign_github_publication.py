"""Qualification for explicit GitHub Campaign-provenance publication."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import CampaignState
from sensemaking_skills.campaigns import CampaignService
from sensemaking_skills.campaigns.github_publication import (
    GitHubProvenancePublisher,
    build_github_provenance_projection,
)
from sensemaking_skills.cli import cli


class FakeTransport:
    def __init__(self, responses: list[Any]) -> None:
        self.responses = list(responses)
        self.calls: list[dict[str, Any]] = []

    def request_json(
        self,
        *,
        method: str,
        url: str,
        token: str,
        payload: dict[str, Any] | None = None,
    ) -> Any:
        self.calls.append(
            {
                "method": method,
                "url": url,
                "token": token,
                "payload": payload,
            }
        )
        return self.responses.pop(0)


def _workspace(tmp_path: Path) -> Path:
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-PUBLISH",
            mission="preserve provenance",
            status="active",
            current_state="working",
        )
    )
    return workspace


def test_provenance_publication_preview_is_deterministic_and_nonmutating(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    runner = CliRunner()

    first = runner.invoke(
        cli,
        [
            "campaign", "provenance-publish",
            "--workspace", str(workspace),
            "--repository", "ThorStarlord/example",
            "--issue-number", "17",
            "--json",
        ],
    )
    second = runner.invoke(
        cli,
        [
            "campaign", "provenance-publish",
            "--workspace", str(workspace),
            "--repository", "ThorStarlord/example",
            "--issue-number", "17",
            "--json",
        ],
    )

    assert first.exit_code == 0, first.output
    assert second.exit_code == 0, second.output
    left = json.loads(first.output)
    right = json.loads(second.output)
    assert left["code"] == "CAMPAIGN_PROVENANCE_PUBLICATION_PREVIEW"
    assert left["published"] is False
    assert left["authorization_explicit"] is False
    assert left["publication_selected_by_tool"] is False
    assert left["semantic_truth_established"] is False
    assert left["marker"] == right["marker"]
    assert left["body_sha256"] == right["body_sha256"]
    assert "<!-- sensemaking-provenance:v1 " in left["body"]


def test_publish_posts_once_when_exact_marker_is_absent(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    projection = build_github_provenance_projection(
        workspace,
        repository="ThorStarlord/example",
        issue_number=17,
    )
    transport = FakeTransport(
        [
            [],
            {"id": 99, "html_url": "https://github.com/ThorStarlord/example/issues/17#issuecomment-99"},
        ]
    )
    payload = GitHubProvenancePublisher(transport).publish(
        projection,
        token="secret-token",
    )

    assert payload["published"] is True
    assert payload["already_present"] is False
    assert payload["authorization_explicit"] is True
    assert payload["comment_id"] == 99
    assert [call["method"] for call in transport.calls] == ["GET", "POST"]
    assert transport.calls[1]["payload"] == {"body": projection.body}


def test_publish_is_idempotent_when_exact_marker_already_exists(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    projection = build_github_provenance_projection(
        workspace,
        repository="ThorStarlord/example",
        issue_number=17,
    )
    transport = FakeTransport(
        [
            [
                {
                    "id": 41,
                    "html_url": "https://github.com/ThorStarlord/example/issues/17#issuecomment-41",
                    "body": projection.marker + "\nexisting provenance",
                }
            ]
        ]
    )
    payload = GitHubProvenancePublisher(transport).publish(
        projection,
        token="secret-token",
    )

    assert payload["published"] is True
    assert payload["already_present"] is True
    assert payload["comment_id"] == 41
    assert [call["method"] for call in transport.calls] == ["GET"]


def test_cli_publish_requires_explicit_token_environment(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    result = CliRunner().invoke(
        cli,
        [
            "campaign", "provenance-publish",
            "--workspace", str(workspace),
            "--repository", "ThorStarlord/example",
            "--issue-number", "17",
            "--publish",
            "--token-env", "SENSEMAKING_TEST_MISSING_TOKEN",
            "--json",
        ],
        env={"SENSEMAKING_TEST_MISSING_TOKEN": ""},
    )

    assert result.exit_code != 0
    assert "requires a non-empty token" in result.output
