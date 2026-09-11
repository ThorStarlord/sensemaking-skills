"""Hermetic qualification for multi-repository Campaign target sets."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import CampaignState
from sensemaking_skills.campaigns import CampaignService
from sensemaking_skills.cli import cli


def _git_repo(root: Path, name: str) -> Path:
    repo = root / name
    repo.mkdir()
    subprocess.run(["git", "init", str(repo)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "tests@example.com"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "Sensemaking Tests"], check=True)
    (repo / "README.md").write_text(f"# {name}\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "README.md"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "initial"], check=True, capture_output=True)
    return repo


def _campaign(root: Path) -> Path:
    workspace = root / "campaign"
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-MULTI",
            mission="coordinate an explicit cross-repository responsibility",
            status="active",
            current_state="scoped",
        )
    )
    return workspace


def _add(runner: CliRunner, workspace: Path, alias: str, repo: Path, role: str):
    return runner.invoke(
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


def test_multi_target_identity_and_drift_are_mechanical_companions(tmp_path: Path) -> None:
    repos = tmp_path / "repos"
    repos.mkdir()
    frontend = _git_repo(repos, "frontend")
    backend = _git_repo(repos, "backend")
    workspace = _campaign(tmp_path)
    runner = CliRunner()

    first = _add(runner, workspace, "frontend", frontend, "web client")
    assert first.exit_code == 0, first.output
    second = _add(runner, workspace, "backend", backend, "service API")
    assert second.exit_code == 0, second.output

    inspected = runner.invoke(cli, ["campaign", "multi-target", "inspect", "--workspace", str(workspace), "--json"])
    assert inspected.exit_code == 0, inspected.output
    payload = json.loads(inspected.output)
    assert payload["target_count"] == 2
    assert {item["alias"] for item in payload["targets"]} == {"frontend", "backend"}
    assert len({item["snapshot"]["repository_id"] for item in payload["targets"]}) == 2
    assert payload["semantic_truth_established"] is False

    verified = runner.invoke(cli, ["campaign", "multi-target", "verify", "--workspace", str(workspace), "--json"])
    assert verified.exit_code == 0, verified.output
    assert json.loads(verified.output)["ok"] is True

    # Multi-target state is a companion and does not silently replace the v2
    # primary target contract.
    campaign_state = CampaignService(workspace).resume().state
    assert campaign_state.schema_version == "2"
    assert campaign_state.target_snapshot is None


def test_multi_target_drift_fails_closed_then_explicit_refresh_records_it(tmp_path: Path) -> None:
    repos = tmp_path / "repos"
    repos.mkdir()
    frontend = _git_repo(repos, "frontend")
    workspace = _campaign(tmp_path)
    runner = CliRunner()
    assert _add(runner, workspace, "frontend", frontend, "web client").exit_code == 0

    (frontend / "README.md").write_text("# frontend changed\n", encoding="utf-8")
    drifted = runner.invoke(cli, ["campaign", "multi-target", "verify", "--workspace", str(workspace), "--alias", "frontend", "--json"])
    assert drifted.exit_code == 3, drifted.output
    drift_payload = json.loads(drifted.output)
    assert any(item["code"] == "MULTI_TARGET_SNAPSHOT_DRIFT" for item in drift_payload["diagnostics"])

    refreshed = runner.invoke(cli, ["campaign", "multi-target", "refresh", "--workspace", str(workspace), "--alias", "frontend", "--json"])
    assert refreshed.exit_code == 0, refreshed.output
    refresh_payload = json.loads(refreshed.output)
    assert refresh_payload["changed"] is True
    assert refresh_payload["refresh_selected_by_tool"] is False
    assert (workspace / "multi-target-history.jsonl").is_file()

    verified = runner.invoke(cli, ["campaign", "multi-target", "verify", "--workspace", str(workspace), "--alias", "frontend", "--json"])
    assert verified.exit_code == 0, verified.output


def test_multi_target_rejects_duplicate_repository_identity_and_tampering(tmp_path: Path) -> None:
    repos = tmp_path / "repos"
    repos.mkdir()
    frontend = _git_repo(repos, "frontend")
    workspace = _campaign(tmp_path)
    runner = CliRunner()
    assert _add(runner, workspace, "frontend", frontend, "web client").exit_code == 0

    duplicate = _add(runner, workspace, "frontend-copy", frontend, "duplicate")
    assert duplicate.exit_code != 0
    assert "already bound" in duplicate.output

    path = workspace / "multi-targets.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["targets"][0]["role"] = "tampered role"
    path.write_text(json.dumps(manifest, sort_keys=True) + "\n", encoding="utf-8")

    inspected = runner.invoke(cli, ["campaign", "multi-target", "inspect", "--workspace", str(workspace), "--json"])
    assert inspected.exit_code == 3, inspected.output
    payload = json.loads(inspected.output)
    assert any(item["code"] == "MULTI_TARGET_SET_DIGEST_MISMATCH" for item in payload["diagnostics"])
