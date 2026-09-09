"""P4/P11 CLI integration tests for validated artifact ingestion."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from sensemaking_skills.cli import (
    ARTIFACT_INVALID_EXIT,
    ARTIFACT_VALIDATOR_EXIT,
    cli,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "architectural-review-recommendation"
VALID_ARTIFACT = FIXTURES / "fixture-valid-pursue.md"
INVALID_ARTIFACT = FIXTURES / "fixture-invalid-missing-evidence.md"


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def _init(runner: CliRunner, workspace: Path) -> None:
    result = runner.invoke(
        cli,
        [
            "campaign",
            "init",
            "--workspace",
            str(workspace),
            "--campaign-id",
            "CMP-P4-CLI",
            "--mission",
            "admit only validator-qualified artifact bytes",
        ],
    )
    assert result.exit_code == 0, result.output


def test_campaign_ingest_admits_valid_artifact_with_default_runtime_and_status_reports_evidence(
    runner, tmp_path
):
    workspace = tmp_path / "campaign"
    _init(runner, workspace)

    # In editable/source-checkout development the default runtime resolves the
    # canonical checkout. Installed-wheel coverage below proves the same command
    # uses the packaged build-derived runtime without a framework checkout.
    result = runner.invoke(
        cli,
        [
            "campaign",
            "ingest",
            "--workspace",
            str(workspace),
            "--artifact",
            str(VALID_ARTIFACT),
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "ARTIFACT_ADMITTED"
    assert payload["artifact_id"] == "architectural_review_recommendation"
    assert payload["validator"] == "validate-architectural-review-recommendation.py"
    assert len(payload["artifact_sha256"]) == 64
    assert payload["artifact_ref"].startswith("artifacts/")
    assert payload["admission_ref"].startswith("admissions/")

    status = runner.invoke(
        cli,
        ["campaign", "status", "--workspace", str(workspace), "--json"],
    )
    assert status.exit_code == 0, status.output
    status_payload = json.loads(status.output)
    assert status_payload["evidence_count"] == 2
    assert payload["artifact_ref"] in status_payload["evidence_refs"]
    assert payload["admission_ref"] in status_payload["evidence_refs"]


def test_campaign_ingest_distinguishes_artifact_rejection_from_explicit_runtime_failure(
    runner, tmp_path
):
    workspace = tmp_path / "campaign"
    _init(runner, workspace)

    rejected = runner.invoke(
        cli,
        [
            "campaign",
            "ingest",
            "--workspace",
            str(workspace),
            "--artifact",
            str(INVALID_ARTIFACT),
            "--framework-root",
            str(REPO_ROOT),
            "--json",
        ],
    )
    assert rejected.exit_code == ARTIFACT_INVALID_EXIT
    rejected_payload = json.loads(rejected.output)
    assert rejected_payload["code"] == "ARTIFACT_VALIDATION_REJECTED"
    assert rejected_payload["validation_result"]["valid"] is False
    assert rejected_payload["validation_result"]["validator"] == (
        "validate-architectural-review-recommendation.py"
    )

    empty_framework = tmp_path / "empty-framework"
    empty_framework.mkdir()
    failed = runner.invoke(
        cli,
        [
            "campaign",
            "ingest",
            "--workspace",
            str(workspace),
            "--artifact",
            str(VALID_ARTIFACT),
            "--framework-root",
            str(empty_framework),
            "--json",
        ],
    )
    assert failed.exit_code == ARTIFACT_VALIDATOR_EXIT
    failed_payload = json.loads(failed.output)
    assert failed_payload["code"] == "ARTIFACT_VALIDATOR_ERROR"
    assert "validation_result" not in failed_payload

    status = runner.invoke(
        cli,
        ["campaign", "status", "--workspace", str(workspace), "--json"],
    )
    assert status.exit_code == 0
    assert json.loads(status.output)["evidence_count"] == 0


def test_campaign_ingest_help_exposes_optional_framework_checkout_override(runner):
    result = runner.invoke(cli, ["campaign", "ingest", "--help"])
    assert result.exit_code == 0
    assert "--framework-root" in result.output
    assert "installed canonical validator runtime is used by default" in result.output
    assert "--artifact" in result.output
    assert "--target-repo" in result.output
