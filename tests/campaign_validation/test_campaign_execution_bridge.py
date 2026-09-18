"""Qualification for generic executor interchange and factory projection."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import Authority, CampaignState, Responsibility
from sensemaking_skills.campaigns import CampaignService
from sensemaking_skills.campaigns.execution_bridge import (
    build_result_template,
    seal_result_envelope,
)
from sensemaking_skills.cli import cli


def _setup(tmp_path: Path) -> tuple[Path, CliRunner]:
    target = tmp_path / "target"
    target.mkdir()
    subprocess.run(["git", "init", str(target)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(target), "config", "user.email", "tests@example.com"], check=True)
    subprocess.run(["git", "-C", str(target), "config", "user.name", "Sensemaking Tests"], check=True)
    (target / "README.md").write_text("# target\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(target), "add", "README.md"], check=True)
    subprocess.run(["git", "-C", str(target), "commit", "-m", "initial"], check=True, capture_output=True)

    responsibility = Responsibility(
        id="R-BRIDGE",
        statement="Implement the selected bridge-safe repair",
        trigger_evidence=("evidence:bridge",),
        decision_blocked="Can the parent accept the repair?",
        scope="repository",
        authority=Authority.AUTHORIZED_AUTONOMOUSLY,
        success_conditions=("focused tests pass", "source identity is returned"),
    )
    workspace = tmp_path / "campaign"
    CampaignService(workspace, target_repo=target).initialize(
        CampaignState(
            campaign_id="CMP-BRIDGE",
            mission="delegate through a generic executor",
            status="active",
            current_state="selected",
            active_responsibility=responsibility,
            authority=Authority.AUTHORIZED_AUTONOMOUSLY,
        )
    )
    runner = CliRunner()
    created = runner.invoke(
        cli,
        [
            "campaign", "execution", "handoff",
            "--workspace", str(workspace),
            "--handoff-id", "H-BRIDGE",
            "--executor-kind", "external-factory",
            "--evidence-requirement", "focused test result",
            "--evidence-requirement", "exact source identity",
            "--forbidden-action", "publish",
            "--json",
        ],
    )
    assert created.exit_code == 0, created.output
    return workspace, runner


def test_generic_handoff_export_is_integrity_bound_and_nonexecuting(tmp_path: Path) -> None:
    workspace, runner = _setup(tmp_path)
    result = runner.invoke(
        cli,
        [
            "campaign", "execution", "export",
            "--workspace", str(workspace),
            "--handoff-id", "H-BRIDGE",
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    envelope = payload["envelope"]
    assert envelope["kind"] == "sensemaking.execution-handoff"
    assert envelope["handoff_id"] == "H-BRIDGE"
    assert envelope["envelope_digest"]
    assert envelope["selection_performed_by_tool"] is False
    assert envelope["execution_performed_by_tool"] is False
    assert payload["execution_performed_by_tool"] is False


def test_result_envelope_seal_and_import_preserve_parent_boundary(tmp_path: Path) -> None:
    workspace, runner = _setup(tmp_path)
    envelope = build_result_template(
        workspace,
        handoff_id="H-BRIDGE",
        result_id="RES-BRIDGE",
        worker="factory-worker",
    )
    envelope.update(
        {
            "source_before": "abc123",
            "source_after": "def456",
            "changed_paths": ["src/example.py"],
            "validations": ["pytest focused: PASS"],
            "evidence_refs": ["worker:test-log"],
            "claims_supported": ["bounded repair implemented"],
            "claims_not_supported": ["global closure"],
        }
    )
    sealed = seal_result_envelope(envelope)
    result_file = tmp_path / "result.json"
    result_file.write_text(json.dumps(sealed), encoding="utf-8")

    imported = runner.invoke(
        cli,
        [
            "campaign", "execution", "result-import",
            "--workspace", str(workspace),
            "--file", str(result_file),
            "--json",
        ],
    )
    assert imported.exit_code == 0, imported.output
    payload = json.loads(imported.output)
    assert payload["campaign_evidence_admitted"] is False
    assert payload["worker_completion_establishes_global_closure"] is False
    assert payload["parent_reassessment_required"] is True

    snapshot = CampaignService(workspace).resume()
    assert snapshot.state.active_responsibility is not None
    assert snapshot.state.active_responsibility.id == "R-BRIDGE"


def test_tampered_result_envelope_is_rejected(tmp_path: Path) -> None:
    workspace, runner = _setup(tmp_path)
    envelope = build_result_template(
        workspace,
        handoff_id="H-BRIDGE",
        result_id="RES-TAMPER",
        worker="factory-worker",
    )
    envelope.update({"source_before": "abc", "source_after": "def"})
    sealed = seal_result_envelope(envelope)
    sealed["source_after"] = "tampered"
    result_file = tmp_path / "tampered.json"
    result_file.write_text(json.dumps(sealed), encoding="utf-8")

    imported = runner.invoke(
        cli,
        [
            "campaign", "execution", "result-import",
            "--workspace", str(workspace),
            "--file", str(result_file),
            "--json",
        ],
    )
    assert imported.exit_code != 0
    assert "digest mismatch" in imported.output


def test_factory_issue_projection_requires_caller_selected_workflow(tmp_path: Path) -> None:
    workspace, runner = _setup(tmp_path)
    result = runner.invoke(
        cli,
        [
            "campaign", "execution", "factory-issue",
            "--workspace", str(workspace),
            "--handoff-id", "H-BRIDGE",
            "--repository", "ThorStarlord/example",
            "--workflow", "archon-lifecycle",
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["repository"] == "ThorStarlord/example"
    assert payload["workflow"] == "archon-lifecycle"
    assert payload["workflow_selected_by_tool"] is False
    assert payload["issue_published"] is False
    assert payload["execution_submitted"] is False
    assert "<!-- sensemaking-execution-handoff:v1 -->" in payload["issue"]["body"]
    assert "archon-lifecycle" in payload["factory_command_template"]
    assert "{ISSUE_URL}" in payload["factory_command_template"]


def test_factory_issue_projection_does_not_default_a_workflow(tmp_path: Path) -> None:
    workspace, runner = _setup(tmp_path)
    result = runner.invoke(
        cli,
        [
            "campaign", "execution", "factory-issue",
            "--workspace", str(workspace),
            "--handoff-id", "H-BRIDGE",
            "--repository", "ThorStarlord/example",
            "--json",
        ],
    )
    assert result.exit_code == 2
    assert "--workflow" in result.output
