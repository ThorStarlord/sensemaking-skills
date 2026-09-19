"""Hermetic qualification for cross-repository execution projection."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import CampaignState
from sensemaking_skills.campaigns import CampaignService
from sensemaking_skills.cli import cli


def _repo(root: Path, name: str) -> Path:
    path = root / name
    path.mkdir()
    subprocess.run(["git", "init", str(path)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "tests@example.com"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "Sensemaking Tests"], check=True)
    (path / "README.md").write_text(f"# {name}\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(path), "add", "README.md"], check=True)
    subprocess.run(["git", "-C", str(path), "commit", "-m", "initial"], check=True, capture_output=True)
    return path


def _workspace(tmp_path: Path) -> tuple[Path, CliRunner]:
    repos = tmp_path / "repos"
    repos.mkdir()
    paths = {
        name: _repo(repos, name)
        for name in ("frontend", "backend", "shared")
    }
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-EXEC-PROJECTION",
            mission="project explicit cross-repository precedence",
            status="active",
            current_state="scoped",
        )
    )
    runner = CliRunner()
    for alias, role in (
        ("frontend", "web client"),
        ("backend", "service API"),
        ("shared", "shared schema"),
    ):
        result = runner.invoke(
            cli,
            [
                "campaign", "multi-target", "add",
                "--workspace", str(workspace),
                "--alias", alias,
                "--target-repo", str(paths[alias]),
                "--role", role,
                "--authority", "authorized_autonomously",
                "--json",
            ],
        )
        assert result.exit_code == 0, result.output
    return workspace, runner


def _relate(
    runner: CliRunner,
    workspace: Path,
    relation_id: str,
    source: str,
    target: str,
    relation_type: str,
):
    result = runner.invoke(
        cli,
        [
            "campaign", "multi-target", "relate",
            "--workspace", str(workspace),
            "--relation-id", relation_id,
            "--source-alias", source,
            "--target-alias", target,
            "--relation-type", relation_type,
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output


def test_execution_view_projects_declared_prerequisites_without_selecting_plan(tmp_path: Path) -> None:
    workspace, runner = _workspace(tmp_path)
    _relate(runner, workspace, "REL-1", "frontend", "backend", "depends_on")
    _relate(runner, workspace, "REL-2", "backend", "shared", "release_after")
    _relate(
        runner,
        workspace,
        "REL-3",
        "backend",
        "frontend",
        "provides_interface_to",
    )

    result = runner.invoke(
        cli,
        [
            "campaign", "multi-target", "execution-view",
            "--workspace", str(workspace),
            "--format", "json",
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["valid"] is True
    assert payload["precedence_layers"] == [["shared"], ["backend"], ["frontend"]]
    assert {
        (item["before"], item["after"], item["relation_type"])
        for item in payload["precedence_edges"]
    } == {
        ("backend", "frontend", "depends_on"),
        ("shared", "backend", "release_after"),
    }
    assert [item["relation_id"] for item in payload["descriptive_relations"]] == [
        "REL-3"
    ]
    assert payload["execution_plan_selected"] is False
    assert payload["parallel_execution_authorized"] is False
    assert payload["semantic_recommendation_included"] is False
    assert "not an execution plan" in payload["explicit_limit"]


def test_descriptive_only_relations_leave_all_targets_in_same_precedence_layer(tmp_path: Path) -> None:
    workspace, runner = _workspace(tmp_path)
    _relate(
        runner,
        workspace,
        "REL-1",
        "backend",
        "frontend",
        "provides_interface_to",
    )
    _relate(
        runner,
        workspace,
        "REL-2",
        "frontend",
        "backend",
        "consumes_interface_from",
    )

    result = runner.invoke(
        cli,
        [
            "campaign", "multi-target", "execution-view",
            "--workspace", str(workspace),
            "--format", "json",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["precedence_edges"] == []
    assert payload["precedence_layers"] == [["backend", "frontend", "shared"]]
    assert payload["parallel_execution_authorized"] is False


def test_execution_view_mermaid_labels_precedence_as_projection(tmp_path: Path) -> None:
    workspace, runner = _workspace(tmp_path)
    _relate(runner, workspace, "REL-1", "frontend", "backend", "depends_on")

    result = runner.invoke(
        cli,
        [
            "campaign", "multi-target", "execution-view",
            "--workspace", str(workspace),
            "--format", "mermaid",
        ],
    )
    assert result.exit_code == 0, result.output
    assert "flowchart LR" in result.output
    assert "precedes (depends_on)" in result.output
    assert "frontend: web client" in result.output
    assert "backend: service API" in result.output


def test_execution_view_fails_closed_when_relation_companion_is_tampered(tmp_path: Path) -> None:
    workspace, runner = _workspace(tmp_path)
    _relate(runner, workspace, "REL-1", "frontend", "backend", "depends_on")

    path = workspace / "multi-target-relations.jsonl"
    record = json.loads(path.read_text(encoding="utf-8").strip())
    record["target_alias"] = "shared"
    path.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")

    result = runner.invoke(
        cli,
        [
            "campaign", "multi-target", "execution-view",
            "--workspace", str(workspace),
            "--format", "json",
        ],
    )
    assert result.exit_code == 3, result.output
    payload = json.loads(result.output)
    assert payload["valid"] is False
    assert payload["execution_plan_selected"] is False
    assert any(
        item["code"] == "MULTI_TARGET_RELATION_DIGEST_MISMATCH"
        for item in payload["diagnostics"]
    )
