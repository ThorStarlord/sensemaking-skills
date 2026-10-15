"""CLI integration tests."""
import importlib.util
import json
import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner
from sensemaking_skills.cli import cli


@pytest.fixture
def runner():
    """Provide Click CLI test runner."""
    return CliRunner()


class TestCLIBasic:
    """Test basic CLI functionality."""

    def test_cli_version(self, runner):
        """Test --version flag."""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "1.0.0" in result.output

    def test_cli_help(self, runner):
        """Test --help flag."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Sensemaking Skills" in result.output
        assert "analyze" in result.output
        assert "validate" in result.output
        assert "test" in result.output
        assert "campaign" in result.output

    def test_analyze_help(self, runner):
        """Test analyze subcommand help."""
        result = runner.invoke(cli, ["analyze", "--help"])
        assert result.exit_code == 0
        assert "--repo" in result.output

    def test_validate_help(self, runner):
        """Test validate subcommand help."""
        result = runner.invoke(cli, ["validate", "--help"])
        assert result.exit_code == 0
        assert "--artifact" in result.output

    def test_test_help(self, runner):
        """Test test subcommand help."""
        result = runner.invoke(cli, ["test", "--help"])
        assert result.exit_code == 0
        assert "--repos" in result.output

    def test_campaign_help_exposes_small_durable_kernel(self, runner):
        result = runner.invoke(cli, ["campaign", "--help"])
        assert result.exit_code == 0
        for command in (
            "init",
            "ingest",
            "status",
            "validate",
            "advance",
            "defer",
            "close",
            "inspect",
            "resume-profile",
            "working-context",
            "advanced",
        ):
            assert command in result.output
        assert "history" not in result.output

    def test_campaign_advanced_help_exposes_secondary_commands(self, runner):
        result = runner.invoke(cli, ["campaign", "advanced", "--help"])
        assert result.exit_code == 0
        assert "history" in result.output

    def test_analyze_without_repo(self, runner):
        """Test analyze without --repo returns error."""
        result = runner.invoke(cli, ["analyze"])
        assert result.exit_code != 0
        assert "Error" in result.output or "repo" in result.output.lower()

    def test_validate_without_artifact(self, runner):
        """Test validate without --artifact returns error."""
        result = runner.invoke(cli, ["validate"])
        assert result.exit_code != 0

    def test_validate_with_missing_artifact(self, runner):
        """Test validate with non-existent artifact returns error."""
        result = runner.invoke(cli, ["validate", "--artifact", "/nonexistent/path.md"])
        assert result.exit_code != 0
        assert "does not exist" in result.output.lower()


def test_runner_implicit_execution_mode_deprecation_contract(tmp_path):
    """Keep issue #264's focused runner contract in the load-bearing core gate."""
    test_path = Path(__file__).with_name("test_runner_execution_mode_deprecation.py")
    spec = importlib.util.spec_from_file_location(
        "runner_execution_mode_deprecation_contract",
        test_path,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module.test_omitted_execution_mode_is_rejected_without_spawning(tmp_path)
    module.test_explicit_yolo_execution_is_rejected_without_spawning(tmp_path)
    module.test_explicit_guided_execution_has_no_deprecation_warning(tmp_path)
    module.test_parent_session_path_requests_guided_execution_explicitly(tmp_path)


def test_validate_invalid_artifact_uses_real_router_and_contract_exit(tmp_path):
    artifact = tmp_path / "bad.md"
    artifact.write_text("# Not a machine-readable Sensemaking artifact\n", encoding="utf-8")
    root = Path(__file__).resolve().parents[1]
    result = CliRunner().invoke(
        cli, ["validate", "--artifact", str(artifact), "--repo-root", str(root), "--json"]
    )
    assert result.exit_code == 5, result.output
    payload = json.loads(result.stdout)
    assert payload["valid"] is False
    assert payload["errors"]
    assert payload["artifact_path"] == str(artifact)


def test_validate_missing_artifact_json_is_not_a_success(tmp_path):
    missing = tmp_path / "missing.md"
    result = CliRunner().invoke(
        cli, ["validate", "--artifact", str(missing), "--json"]
    )
    assert result.exit_code == 5
    payload = json.loads(result.stdout)
    assert payload["valid"] is False
    assert "does not exist" in payload["errors"][0]["message"]


def test_validate_missing_canonical_scripts_is_operational_error(tmp_path):
    artifact = tmp_path / "artifact.md"
    artifact.write_text("example", encoding="utf-8")
    result = CliRunner().invoke(
        cli, ["validate", "--artifact", str(artifact), "--repo-root", str(tmp_path), "--json"]
    )
    assert result.exit_code == 6
    payload = json.loads(result.stdout)
    assert payload["valid"] is False
    assert payload["errors"][0]["error_id"].endswith(".validator.execution_error")


def test_validate_routes_valid_canonical_result(monkeypatch, tmp_path):
    artifact = tmp_path / "artifact.md"
    artifact.write_text("fixture", encoding="utf-8")
    payload = {
        "valid": True, "artifact_id": "repository_sensemaking_brief",
        "artifact_path": str(artifact), "validator": "validate-brief.py",
        "errors": [], "validation_timestamp": "2026-10-14T00:00:00Z",
    }
    def fake_run(command, **kwargs):
        assert command[1].endswith("scripts/validate-and-report.py")
        assert str(artifact) in command
        return subprocess.CompletedProcess(command, 0, stdout=json.dumps(payload), stderr="")
    monkeypatch.setattr("sensemaking_skills.cli.subprocess.run", fake_run)
    root = Path(__file__).resolve().parents[1]
    result = CliRunner().invoke(cli, ["validate", "--artifact", str(artifact), "--repo-root", str(root), "--json"])
    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout) == payload


def test_validate_router_execution_failure_is_exit_6(monkeypatch, tmp_path):
    artifact = tmp_path / "artifact.md"
    artifact.write_text("fixture", encoding="utf-8")
    root = Path(__file__).resolve().parents[1]
    def fail_run(*args, **kwargs):
        return subprocess.CompletedProcess(args[0], 1, stdout="not-json", stderr="validator crashed")
    monkeypatch.setattr("sensemaking_skills.cli.subprocess.run", fail_run)
    result = CliRunner().invoke(cli, ["validate", "--artifact", str(artifact), "--repo-root", str(root), "--json"])
    assert result.exit_code == 6, result.output
    assert json.loads(result.stdout)["valid"] is False


def test_validate_real_known_good_plan_is_valid():
    root = Path(__file__).resolve().parents[1]
    artifact = root / "tests" / "fixtures" / "validate-and-report" / "valid" / "dispatches-to-validate-plan.md"
    result = CliRunner().invoke(
        cli, ["validate", "--artifact", str(artifact), "--repo-root", str(root), "--json"]
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.stdout)
    assert payload["valid"] is True
    assert payload["artifact_id"] == "workflow_orchestration_plan"
    assert payload["errors"] == []


def test_validate_default_root_reuses_campaign_validator_resolver(monkeypatch, tmp_path):
    """Top-level validation shares the shipped Campaign validator runtime."""
    artifact = tmp_path / "artifact.md"
    artifact.write_text("fixture", encoding="utf-8")
    expected_root = Path(__file__).resolve().parents[1]
    payload = {
        "valid": True, "artifact_id": "repository_sensemaking_brief",
        "artifact_path": str(artifact), "validator": "validate-brief.py",
        "errors": [], "validation_timestamp": "2026-10-14T00:00:00Z",
    }

    def fake_root(requested):
        assert requested is None
        return expected_root, expected_root / "scripts" / "validate-and-report.py"

    def fake_run(command, **kwargs):
        assert command[1] == str(expected_root / "scripts" / "validate-and-report.py")
        assert kwargs["cwd"] == expected_root
        return subprocess.CompletedProcess(command, 0, stdout=json.dumps(payload), stderr="")

    monkeypatch.setattr(
        "sensemaking_skills.cli.ArtifactAdmissionService._require_framework_root",
        fake_root,
    )
    monkeypatch.setattr("sensemaking_skills.cli.subprocess.run", fake_run)
    result = CliRunner().invoke(cli, ["validate", "--artifact", str(artifact), "--json"])
    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout) == payload
