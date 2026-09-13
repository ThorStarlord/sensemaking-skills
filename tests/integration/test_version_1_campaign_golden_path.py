from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from sensemaking_skills.cli import cli


def _invoke(runner: CliRunner, args: list[str]):
    result = runner.invoke(cli, args)
    assert result.exit_code == 0, result.output
    return result


def test_campaign_cli_golden_path_is_reconstructible_and_portable(tmp_path: Path) -> None:
    runner = CliRunner()
    workspace = tmp_path / "campaign"
    bundle = tmp_path / "campaign.zip"
    imported = tmp_path / "imported"

    initialized = _invoke(
        runner,
        [
            "campaign", "init", "--workspace", str(workspace),
            "--campaign-id", "CMP-V1-GOLDEN",
            "--mission", "prove the stable Campaign lifecycle",
            "--json",
        ],
    )
    assert json.loads(initialized.output)["current_state"] == "initialized"

    status = _invoke(runner, ["campaign", "status", "--workspace", str(workspace), "--json"])
    assert json.loads(status.output)["schema_version"] == "2"

    valid = _invoke(runner, ["campaign", "validate", "--workspace", str(workspace), "--json"])
    assert json.loads(valid.output)["valid"] is True

    resume = _invoke(
        runner,
        ["campaign", "resume-context", "--workspace", str(workspace), "--json"],
    )
    resume_payload = json.loads(resume.output)
    assert resume_payload["semantic_recommendation_included"] is False
    assert "recommended_next_action" not in resume_payload

    _invoke(
        runner,
        ["campaign", "bundle-export", "--workspace", str(workspace), "--output", str(bundle), "--json"],
    )
    verified = _invoke(runner, ["campaign", "bundle-verify", "--bundle", str(bundle), "--json"])
    assert json.loads(verified.output)["code"] == "CAMPAIGN_BUNDLE_VALID"

    imported_result = _invoke(
        runner,
        ["campaign", "bundle-import", "--bundle", str(bundle), "--workspace", str(imported), "--json"],
    )
    assert json.loads(imported_result.output)["code"] == "CAMPAIGN_BUNDLE_IMPORTED"
    imported_status = _invoke(
        runner, ["campaign", "status", "--workspace", str(imported), "--json"]
    )
    assert json.loads(imported_status.output)["campaign_id"] == "CMP-V1-GOLDEN"
