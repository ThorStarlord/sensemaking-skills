"""Hermetic qualification for explicit cross-repository dependency declarations."""

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
    frontend = _repo(repos, "frontend")
    backend = _repo(repos, "backend")
    shared = _repo(repos, "shared")
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-DEPS",
            mission="coordinate explicit repository dependencies",
            status="active",
            current_state="scoped",
        )
    )
    runner = CliRunner()
    for alias, repo, role in (
        ("frontend", frontend, "web client"),
        ("backend", backend, "service API"),
        ("shared", shared, "shared schema"),
    ):
        result = runner.invoke(
            cli,
            [
                "campaign", "multi-target", "add",
                "--workspace", str(workspace),
                "--alias", alias,
                "--target-repo", str(repo),
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
    return runner.invoke(
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


def test_explicit_dependency_graph_and_preflight_are_mechanical(tmp_path: Path) -> None:
    workspace, runner = _workspace(tmp_path)
    first = _relate(runner, workspace, "REL-1", "frontend", "backend", "depends_on")
    assert first.exit_code == 0, first.output
    assert json.loads(first.output)["relation_selected_by_tool"] is False
    second = _relate(runner, workspace, "REL-2", "backend", "shared", "release_after")
    assert second.exit_code == 0, second.output

    checked = runner.invoke(
        cli,
        ["campaign", "multi-target", "dependency-check", "--workspace", str(workspace), "--json"],
    )
    assert checked.exit_code == 0, checked.output
    payload = json.loads(checked.output)
    assert payload["relation_count"] == 2
    assert payload["ordering_cycles"] == []
    assert payload["semantic_truth_established"] is False

    graph = runner.invoke(
        cli,
        ["campaign", "multi-target", "graph", "--workspace", str(workspace), "--format", "json"],
    )
    assert graph.exit_code == 0, graph.output
    graph_payload = json.loads(graph.output)
    assert set(graph_payload["nodes"]) == {"frontend", "backend", "shared"}
    assert {edge["relation_id"] for edge in graph_payload["edges"]} == {"REL-1", "REL-2"}

    preflight = runner.invoke(cli, ["campaign", "preflight", "--workspace", str(workspace), "--json"])
    assert preflight.exit_code == 0, preflight.output
    preflight_payload = json.loads(preflight.output)
    relation_check = next(item for item in preflight_payload["checks"] if item["id"] == "multi_target_relation_integrity")
    assert relation_check["status"] == "pass"
    assert relation_check["data"]["relation_count"] == 2


def test_unknown_alias_duplicate_and_ordering_cycle_fail_closed(tmp_path: Path) -> None:
    workspace, runner = _workspace(tmp_path)
    unknown = _relate(runner, workspace, "REL-X", "frontend", "missing", "depends_on")
    assert unknown.exit_code != 0
    assert "must already exist" in unknown.output

    first = _relate(runner, workspace, "REL-1", "frontend", "backend", "depends_on")
    assert first.exit_code == 0
    duplicate = _relate(runner, workspace, "REL-2", "frontend", "backend", "depends_on")
    assert duplicate.exit_code != 0
    assert "already recorded" in duplicate.output

    cycle = _relate(runner, workspace, "REL-3", "backend", "frontend", "release_after")
    assert cycle.exit_code != 0
    assert "cycle" in cycle.output

    checked = runner.invoke(cli, ["campaign", "multi-target", "dependency-check", "--workspace", str(workspace), "--json"])
    assert checked.exit_code == 0, checked.output
    assert json.loads(checked.output)["relation_count"] == 1


def test_reciprocal_descriptive_relations_do_not_create_ordering_cycle(tmp_path: Path) -> None:
    workspace, runner = _workspace(tmp_path)
    assert _relate(runner, workspace, "REL-1", "backend", "frontend", "provides_interface_to").exit_code == 0
    assert _relate(runner, workspace, "REL-2", "frontend", "backend", "consumes_interface_from").exit_code == 0
    checked = runner.invoke(cli, ["campaign", "multi-target", "dependency-check", "--workspace", str(workspace), "--json"])
    assert checked.exit_code == 0, checked.output
    assert json.loads(checked.output)["ordering_cycles"] == []


def test_tampered_relation_chain_fails_dependency_check_and_preflight(tmp_path: Path) -> None:
    workspace, runner = _workspace(tmp_path)
    assert _relate(runner, workspace, "REL-1", "frontend", "backend", "depends_on").exit_code == 0
    path = workspace / "multi-target-relations.jsonl"
    record = json.loads(path.read_text(encoding="utf-8").strip())
    record["target_alias"] = "shared"
    path.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")

    checked = runner.invoke(cli, ["campaign", "multi-target", "dependency-check", "--workspace", str(workspace), "--json"])
    assert checked.exit_code == 3, checked.output
    payload = json.loads(checked.output)
    assert any(item["code"] == "MULTI_TARGET_RELATION_DIGEST_MISMATCH" for item in payload["diagnostics"])

    preflight = runner.invoke(cli, ["campaign", "preflight", "--workspace", str(workspace), "--json"])
    assert preflight.exit_code == 3, preflight.output
    preflight_payload = json.loads(preflight.output)
    relation_check = next(item for item in preflight_payload["checks"] if item["id"] == "multi_target_relation_integrity")
    assert relation_check["status"] == "fail"
