"""P11 release-portability proof for self-contained artifact admission."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import venv
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "architectural-review-recommendation"
VALID_ARTIFACT = FIXTURES / "fixture-valid-pursue.md"
INVALID_ARTIFACT = FIXTURES / "fixture-invalid-missing-evidence.md"


def _venv_python(venv_dir: Path) -> Path:
    return venv_dir / (
        "Scripts/python.exe" if sys.platform.startswith("win") else "bin/python"
    )


def _venv_script(venv_dir: Path, name: str) -> Path:
    return (
        venv_dir
        / ("Scripts" if sys.platform.startswith("win") else "bin")
        / name
    )


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _build_and_install_wheel(tmp_path: Path) -> tuple[Path, Path]:
    wheel_dir = tmp_path / "wheel"
    venv_dir = tmp_path / "venv"

    build = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            str(REPO_ROOT),
            "--no-deps",
            "--wheel-dir",
            str(wheel_dir),
        ],
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert build.returncode == 0, build.stdout + build.stderr
    wheels = list(wheel_dir.glob("*.whl"))
    assert len(wheels) == 1, wheels

    venv.create(venv_dir, with_pip=True)
    install = subprocess.run(
        [str(_venv_python(venv_dir)), "-m", "pip", "install", str(wheels[0])],
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert install.returncode == 0, install.stdout + install.stderr
    return wheels[0], venv_dir


def _run(cli: str, work_dir: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [cli, *args],
        capture_output=True,
        text=True,
        timeout=240,
        cwd=str(work_dir),
    )


def _init(cli: str, work_dir: Path, workspace: Path, campaign_id: str) -> None:
    result = _run(
        cli,
        work_dir,
        "campaign",
        "init",
        "--workspace",
        str(workspace),
        "--campaign-id",
        campaign_id,
        "--mission",
        "prove installed-distribution artifact admission",
        "--json",
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_installed_wheel_ingests_without_framework_checkout(tmp_path: Path):
    _wheel, venv_dir = _build_and_install_wheel(tmp_path)
    work_dir = tmp_path / "outside-source-checkout"
    work_dir.mkdir()
    cli = str(_venv_script(venv_dir, "sensemaking-skills"))

    help_run = _run(cli, work_dir, "campaign", "ingest", "--help")
    assert help_run.returncode == 0, help_run.stdout + help_run.stderr
    normalized_help = " ".join(help_run.stdout.split())
    assert "--framework-root" in normalized_help
    assert "installed canonical validator runtime is used by default" in normalized_help

    valid = work_dir / "valid-recommendation.md"
    valid.write_bytes(VALID_ARTIFACT.read_bytes())
    workspace = work_dir / "campaign-valid"
    _init(cli, work_dir, workspace, "CMP-P11-WHEEL-VALID")

    admitted = _run(
        cli,
        work_dir,
        "campaign",
        "ingest",
        "--workspace",
        str(workspace),
        "--artifact",
        str(valid),
        "--json",
    )
    assert admitted.returncode == 0, admitted.stdout + admitted.stderr
    payload = json.loads(admitted.stdout)
    assert payload["code"] == "ARTIFACT_ADMITTED"
    assert payload["artifact_id"] == "architectural_review_recommendation"
    assert payload["validator"] == "validate-architectural-review-recommendation.py"

    # Build-derived runtime bytes must be exactly the repository's canonical
    # router/validator bytes; provenance is not allowed to degrade merely
    # because validation came from an installed distribution.
    assert payload["router_sha256"] == _sha256(
        REPO_ROOT / "scripts" / "validate-and-report.py"
    )
    assert payload["validator_sha256"] == _sha256(
        REPO_ROOT / "scripts" / "validate-architectural-review-recommendation.py"
    )

    status = _run(
        cli,
        work_dir,
        "campaign",
        "status",
        "--workspace",
        str(workspace),
        "--json",
    )
    assert status.returncode == 0, status.stdout + status.stderr
    assert json.loads(status.stdout)["evidence_count"] == 2

    invalid = work_dir / "invalid-recommendation.md"
    invalid.write_bytes(INVALID_ARTIFACT.read_bytes())
    rejected_workspace = work_dir / "campaign-rejected"
    _init(cli, work_dir, rejected_workspace, "CMP-P11-WHEEL-REJECTED")
    rejected = _run(
        cli,
        work_dir,
        "campaign",
        "ingest",
        "--workspace",
        str(rejected_workspace),
        "--artifact",
        str(invalid),
        "--json",
    )
    assert rejected.returncode == 5, rejected.stdout + rejected.stderr
    rejected_payload = json.loads(rejected.stdout)
    assert rejected_payload["code"] == "ARTIFACT_VALIDATION_REJECTED"
    assert rejected_payload["validation_result"]["valid"] is False

    # An explicit bad development override must fail closed; it must never be
    # silently replaced by the packaged runtime after the caller selected it.
    empty_runtime = work_dir / "empty-runtime"
    empty_runtime.mkdir()
    override_workspace = work_dir / "campaign-override-error"
    _init(cli, work_dir, override_workspace, "CMP-P11-WHEEL-OVERRIDE")
    failed = _run(
        cli,
        work_dir,
        "campaign",
        "ingest",
        "--workspace",
        str(override_workspace),
        "--artifact",
        str(valid),
        "--framework-root",
        str(empty_runtime),
        "--json",
    )
    assert failed.returncode == 6, failed.stdout + failed.stderr
    failed_payload = json.loads(failed.stdout)
    assert failed_payload["code"] == "ARTIFACT_VALIDATOR_ERROR"

    failed_status = _run(
        cli,
        work_dir,
        "campaign",
        "status",
        "--workspace",
        str(override_workspace),
        "--json",
    )
    assert failed_status.returncode == 0
    assert json.loads(failed_status.stdout)["evidence_count"] == 0
