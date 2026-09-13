from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml
from click.testing import CliRunner

from sensemaking_skills.cli import cli


ROOT = Path(__file__).resolve().parents[1]


def test_cli_contract_matches_registered_surface() -> None:
    contract = yaml.safe_load(
        (ROOT / "docs" / "cli-contract-v1.0.yaml").read_text(encoding="utf-8")
    )
    result = CliRunner().invoke(cli, ["--help"])
    assert result.exit_code == contract["exit_codes"]["success"]
    for command in contract["stable_commands"] + contract["compatibility_commands"]:
        assert command in result.output


def test_cli_usage_and_operational_errors_have_stable_categories() -> None:
    runner = CliRunner()
    usage = runner.invoke(cli, ["does-not-exist"])
    operational = runner.invoke(cli, ["campaign", "status", "--workspace", str(ROOT)])

    assert usage.exit_code == 2
    assert operational.exit_code == 4


def test_campaign_json_errors_are_single_machine_readable_objects() -> None:
    result = CliRunner().invoke(cli, ["campaign", "status", "--workspace", str(ROOT), "--json"])

    assert result.exit_code == 4
    payload = json.loads(result.output)
    assert payload["ok"] is False
    assert payload["code"] == "CAMPAIGN_NOT_INITIALIZED"
    assert isinstance(payload["diagnostics"], list)


def test_campaign_human_readable_success_surface_is_stable() -> None:
    runner = CliRunner()
    with TemporaryDirectory() as temp_dir:
        workspace = Path(temp_dir) / "campaign"
        created = runner.invoke(
            cli,
            [
                "campaign", "init", "--workspace", str(workspace),
                "--campaign-id", "CMP-CONTRACT-1", "--mission", "contract test",
            ],
        )
        assert created.exit_code == 0

        status = runner.invoke(cli, ["campaign", "status", "--workspace", str(workspace)])
        validation = runner.invoke(cli, ["campaign", "validate", "--workspace", str(workspace)])
        history = runner.invoke(cli, ["campaign", "history", "--workspace", str(workspace)])

        assert status.exit_code == 0
        assert "CAMPAIGN_STATUS" in status.output
        assert "Campaign: CMP-CONTRACT-1" in status.output
        assert validation.exit_code == 0
        assert validation.output.strip() == "CAMPAIGN_VALID"
        assert history.exit_code == 0
        assert "CAMPAIGN_HISTORY" in history.output


def test_cli_contract_is_linked_from_public_surface() -> None:
    text = (ROOT / "docs" / "public-surface-v1.0.md").read_text(encoding="utf-8")
    assert "cli-contract-v1.0.yaml" in text
