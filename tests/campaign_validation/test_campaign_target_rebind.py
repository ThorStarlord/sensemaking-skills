"""Hermetic qualification for explicit portable Campaign target rebinding."""

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
    subprocess.run(["git", "-C", str(repo), "remote", "add", "origin", f"https://example.invalid/sensemaking/{name}.git"], check=True)
    (repo / "README.md").write_text(f"# {name}\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "README.md"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "initial"], check=True, capture_output=True)
    return repo


def test_primary_target_rebind_restores_validation_without_rewriting_snapshot(tmp_path: Path) -> None:
    repos = tmp_path / "repos"
    repos.mkdir()
    target = _git_repo(repos, "primary")
    workspace = tmp_path / "campaign"
    CampaignService(workspace, target_repo=target).initialize(
        CampaignState(campaign_id="CMP-REBIND", mission="portable continuation", status="active", current_state="scoped")
    )
    original = CampaignService(workspace).resume().state.target_snapshot
    assert original is not None

    relocated = repos / "primary-relocated"
    target.rename(relocated)
    before = CampaignService(workspace).validate()
    assert not before.valid
    assert "TARGET_REPOSITORY_UNAVAILABLE" in before.diagnostic_codes

    runner = CliRunner()
    rebound = runner.invoke(
        cli,
        ["campaign", "target", "rebind", "--workspace", str(workspace), "--target-repo", str(relocated), "--json"],
    )
    assert rebound.exit_code == 0, rebound.output
    payload = json.loads(rebound.output)
    assert payload["code"] == "CAMPAIGN_TARGET_REBOUND"
    assert payload["repository_discovery_performed"] is False
    assert (workspace / "target-rebind.json").is_file()

    verified = runner.invoke(cli, ["campaign", "target", "verify-rebind", "--workspace", str(workspace), "--json"])
    assert verified.exit_code == 0, verified.output
    assert json.loads(verified.output)["ok"] is True
    after = CampaignService(workspace).resume().state.target_snapshot
    assert after == original
    assert after.repository_root != str(relocated.resolve())


def test_primary_target_rebind_rejects_wrong_identity_or_changed_state(tmp_path: Path) -> None:
    repos = tmp_path / "repos"
    repos.mkdir()
    target = _git_repo(repos, "primary")
    other = _git_repo(repos, "other")
    workspace = tmp_path / "campaign"
    CampaignService(workspace, target_repo=target).initialize(
        CampaignState(campaign_id="CMP-REBIND-NEG", mission="reject unsafe rebinding", status="active", current_state="scoped")
    )
    relocated = repos / "primary-relocated"
    target.rename(relocated)
    runner = CliRunner()

    wrong = runner.invoke(cli, ["campaign", "target", "rebind", "--workspace", str(workspace), "--target-repo", str(other), "--json"])
    assert wrong.exit_code != 0
    assert "identity differs" in wrong.output

    (relocated / "README.md").write_text("# changed\n", encoding="utf-8")
    drift = runner.invoke(cli, ["campaign", "target", "rebind", "--workspace", str(workspace), "--target-repo", str(relocated), "--json"])
    assert drift.exit_code != 0
    assert "state differs" in drift.output


def test_multi_target_rebind_accepts_same_exact_target_at_new_path(tmp_path: Path) -> None:
    repos = tmp_path / "repos"
    repos.mkdir()
    target = _git_repo(repos, "service")
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(
        CampaignState(campaign_id="CMP-MULTI-REBIND", mission="portable multi-target work", status="active", current_state="scoped")
    )
    runner = CliRunner()
    added = runner.invoke(
        cli,
        [
            "campaign", "multi-target", "add",
            "--workspace", str(workspace),
            "--alias", "service",
            "--target-repo", str(target),
            "--role", "service API",
            "--authority", "authorized_autonomously",
            "--json",
        ],
    )
    assert added.exit_code == 0, added.output
    relocated = repos / "service-relocated"
    target.rename(relocated)

    unavailable = runner.invoke(cli, ["campaign", "multi-target", "verify", "--workspace", str(workspace), "--alias", "service", "--json"])
    assert unavailable.exit_code == 3

    rebound = runner.invoke(
        cli,
        ["campaign", "multi-target", "rebind", "--workspace", str(workspace), "--alias", "service", "--target-repo", str(relocated), "--json"],
    )
    assert rebound.exit_code == 0, rebound.output
    payload = json.loads(rebound.output)
    assert payload["rebind_selected_by_tool"] is False
    assert payload["from_snapshot_sha256"] != payload["to_snapshot_sha256"]
    assert (workspace / "multi-target-rebind-history.jsonl").is_file()

    verified = runner.invoke(cli, ["campaign", "multi-target", "verify", "--workspace", str(workspace), "--alias", "service", "--json"])
    assert verified.exit_code == 0, verified.output
    preflight = runner.invoke(cli, ["campaign", "preflight", "--workspace", str(workspace), "--json"])
    assert preflight.exit_code == 0, preflight.output
