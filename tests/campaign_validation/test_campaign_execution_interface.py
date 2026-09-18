"""Qualification for bounded execution handoff/result companions."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import Authority, CampaignState, Responsibility
from sensemaking_skills.campaigns import CampaignService
from sensemaking_skills.cli import cli


def _repo(tmp_path: Path) -> Path:
    repo = tmp_path / "target"
    repo.mkdir()
    subprocess.run(["git", "init", str(repo)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "tests@example.com"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "Sensemaking Tests"], check=True)
    (repo / "README.md").write_text("# target\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "README.md"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "initial"], check=True, capture_output=True)
    return repo


def _campaign(tmp_path: Path) -> tuple[Path, Path, CliRunner]:
    target = _repo(tmp_path)
    workspace = tmp_path / "campaign"
    responsibility = Responsibility(
        id="R-EXEC-1",
        statement="Implement the already-selected bounded repair",
        trigger_evidence=("evidence:1",),
        decision_blocked="Can the repair be closed?",
        scope="repository",
        authority=Authority.AUTHORIZED_AUTONOMOUSLY,
        success_conditions=("focused tests pass", "returned source identity is explicit"),
    )
    state = CampaignState(
        campaign_id="CMP-EXEC",
        mission="delegate bounded repository work",
        status="active",
        current_state="implementation_selected",
        active_responsibility=responsibility,
        authority=Authority.AUTHORIZED_AUTONOMOUSLY,
    )
    CampaignService(workspace, target_repo=target).initialize(state)
    return workspace, target, CliRunner()


def test_execution_handoff_binds_selected_responsibility_and_target(tmp_path: Path) -> None:
    workspace, _, runner = _campaign(tmp_path)

    result = runner.invoke(
        cli,
        [
            "campaign", "execution", "handoff",
            "--workspace", str(workspace),
            "--handoff-id", "H-1",
            "--executor-kind", "coding-agent",
            "--evidence-requirement", "exact changed source identity",
            "--evidence-requirement", "focused test result",
            "--forbidden-action", "publish",
            "--json",
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    handoff = payload["handoff"]
    assert handoff["responsibility"]["id"] == "R-EXEC-1"
    assert handoff["responsibility"]["authority"] == "authorized_autonomously"
    assert handoff["responsibility"]["success_conditions"] == [
        "focused tests pass",
        "returned source identity is explicit",
    ]
    assert handoff["targets"][0]["alias"] == "primary"
    assert handoff["selection_performed_by_tool"] is False
    assert handoff["authorization_granted_by_tool"] is False
    assert payload["global_closure_established"] is False


def test_worker_result_returns_evidence_without_global_closure(tmp_path: Path) -> None:
    workspace, target, runner = _campaign(tmp_path)
    before = subprocess.run(
        ["git", "-C", str(target), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    handoff = runner.invoke(
        cli,
        [
            "campaign", "execution", "handoff",
            "--workspace", str(workspace),
            "--handoff-id", "H-1",
            "--executor-kind", "coding-agent",
            "--evidence-requirement", "focused tests",
            "--json",
        ],
    )
    assert handoff.exit_code == 0, handoff.output

    returned = runner.invoke(
        cli,
        [
            "campaign", "execution", "result",
            "--workspace", str(workspace),
            "--result-id", "RES-1",
            "--handoff-id", "H-1",
            "--worker", "agent-1",
            "--source-before", before,
            "--source-after", "candidate-sha",
            "--changed-path", "src/example.py",
            "--validation", "pytest focused: PASS",
            "--evidence-ref", "worker:test-log",
            "--claim-supported", "focused repair implemented",
            "--claim-not-supported", "global repository closure",
            "--authority-exceeded", "no",
            "--json",
        ],
    )
    assert returned.exit_code == 0, returned.output
    payload = json.loads(returned.output)
    assert payload["worker_completion_establishes_global_closure"] is False
    assert payload["campaign_evidence_admitted"] is False
    assert payload["parent_reassessment_required"] is True
    assert payload["result"]["authority_exceeded"] is False

    snapshot = CampaignService(workspace).resume()
    assert snapshot.state.active_responsibility is not None
    assert snapshot.state.active_responsibility.id == "R-EXEC-1"


def test_working_context_projects_delegation_without_recommendation(tmp_path: Path) -> None:
    workspace, _, runner = _campaign(tmp_path)
    handoff = runner.invoke(
        cli,
        [
            "campaign", "execution", "handoff",
            "--workspace", str(workspace),
            "--handoff-id", "H-CTX",
            "--executor-kind", "coding-agent",
            "--evidence-requirement", "test result",
            "--json",
        ],
    )
    assert handoff.exit_code == 0, handoff.output

    result = runner.invoke(
        cli,
        ["campaign", "working-context", "--workspace", str(workspace), "--json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["active_responsibility"]["id"] == "R-EXEC-1"
    assert payload["latest_execution_handoff"]["handoff_id"] == "H-CTX"
    assert payload["semantic_recommendation_included"] is False
    assert payload["global_closure_established"] is False


def test_tampered_execution_record_fails_closed(tmp_path: Path) -> None:
    workspace, _, runner = _campaign(tmp_path)
    handoff = runner.invoke(
        cli,
        [
            "campaign", "execution", "handoff",
            "--workspace", str(workspace),
            "--handoff-id", "H-TAMPER",
            "--executor-kind", "coding-agent",
            "--evidence-requirement", "test result",
            "--json",
        ],
    )
    assert handoff.exit_code == 0, handoff.output

    path = workspace / "execution-handoffs.jsonl"
    record = json.loads(path.read_text(encoding="utf-8").strip())
    record["executor_kind"] = "other-worker"
    path.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")

    result = runner.invoke(
        cli,
        ["campaign", "execution", "inspect", "--workspace", str(workspace), "--json"],
    )
    assert result.exit_code == 3, result.output
    payload = json.loads(result.output)
    assert any(item["code"] == "EXECUTION_HANDOFF_DIGEST_MISMATCH" for item in payload["diagnostics"])
