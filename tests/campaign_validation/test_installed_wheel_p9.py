"""P9 installed-wheel proof from a work directory outside the source checkout."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import venv
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]


def _canonical_json_digest(value) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _venv_python(venv_dir: Path) -> Path:
    return venv_dir / ("Scripts/python.exe" if sys.platform.startswith("win") else "bin/python")


def _venv_script(venv_dir: Path, name: str) -> Path:
    return venv_dir / ("Scripts" if sys.platform.startswith("win") else "bin") / name


def _install_wheel(tmp_path: Path) -> tuple[Path, Path]:
    wheel_dir = tmp_path / "wheel"
    venv_dir = tmp_path / "venv"
    work_dir = tmp_path / "work"
    work_dir.mkdir()

    built = subprocess.run(
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
    assert built.returncode == 0, built.stdout + built.stderr
    wheels = list(wheel_dir.glob("*.whl"))
    assert len(wheels) == 1

    venv.create(venv_dir, with_pip=True)
    installed = subprocess.run(
        [str(_venv_python(venv_dir)), "-m", "pip", "install", str(wheels[0])],
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert installed.returncode == 0, installed.stdout + installed.stderr
    return venv_dir, work_dir


def _write_admitted_reconciliation_report(workspace: Path) -> str:
    artifact_id = "reconciliation_report"
    artifact_bytes = b"classification: verified\nrecommendation: agent decides\n"
    artifact_sha256 = hashlib.sha256(artifact_bytes).hexdigest()
    artifact_ref = f"artifacts/{artifact_id}/{artifact_sha256}.md"
    artifact_path = workspace / artifact_ref
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_bytes(artifact_bytes)

    validator = "installed-wheel-test-validator"
    validation_timestamp = "2026-09-08T14:00:00Z"
    validation_result = {
        "valid": True,
        "artifact_id": artifact_id,
        "validator": validator,
        "validation_timestamp": validation_timestamp,
        "errors": [],
    }
    payload = {
        "campaign_id": "CMP-P9-WHEEL",
        "artifact_id": artifact_id,
        "artifact_ref": artifact_ref,
        "artifact_sha256": artifact_sha256,
        "validator": validator,
        "validation_timestamp": validation_timestamp,
        "router_sha256": "1" * 64,
        "validator_sha256": "2" * 64,
        "validation_result_sha256": _canonical_json_digest(validation_result),
        "validation_result": validation_result,
        "schema_version": "1",
    }
    receipt_digest = _canonical_json_digest(payload)
    receipt_path = workspace / "admissions" / artifact_id / f"{receipt_digest}.yaml"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return artifact_ref


def test_installed_wheel_supports_p9_reconciliation_disposition_without_source_checkout(tmp_path):
    venv_dir, work_dir = _install_wheel(tmp_path)
    cli_path = str(_venv_script(venv_dir, "sensemaking-skills"))
    workspace = work_dir / "CMP-P9-WHEEL"

    campaign_help = subprocess.run(
        [cli_path, "campaign", "--help"],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=str(work_dir),
    )
    assert campaign_help.returncode == 0, campaign_help.stdout + campaign_help.stderr
    assert "reconciliation" in campaign_help.stdout

    initialized = subprocess.run(
        [
            cli_path,
            "campaign",
            "init",
            "--workspace",
            str(workspace),
            "--campaign-id",
            "CMP-P9-WHEEL",
            "--mission",
            "prove packaged P9 reconciliation lifecycle",
            "--json",
        ],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(work_dir),
    )
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr

    artifact_ref = _write_admitted_reconciliation_report(workspace)

    before = subprocess.run(
        [
            cli_path,
            "campaign",
            "reconciliation",
            "--workspace",
            str(workspace),
            "--json",
        ],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(work_dir),
    )
    assert before.returncode == 0, before.stdout + before.stderr
    before_payload = json.loads(before.stdout)
    assert before_payload["code"] == "CAMPAIGN_RECONCILIATION"
    assert before_payload["report_count"] == 1
    assert before_payload["disposition_required_count"] == 1
    assert before_payload["reports"][0]["artifact_ref"] == artifact_ref
    assert before_payload["reports"][0]["disposition_status"] == "disposition_required"

    advanced = subprocess.run(
        [
            cli_path,
            "campaign",
            "advance",
            "--workspace",
            str(workspace),
            "--transition-id",
            "TR-P9-WHEEL",
            "--to-state",
            "reconciliation_disposition_recorded",
            "--decision",
            "the agent explicitly consumes the admitted reconciliation report",
            "--evidence",
            artifact_ref,
            "--responsibility-id",
            "R-P9-WHEEL",
            "--responsibility-statement",
            "continue from the explicit reconciliation disposition",
            "--decision-blocked",
            "whether the next bounded responsibility is complete",
            "--scope",
            "installed-wheel P9 proof",
            "--authority",
            "authorized_autonomously",
            "--success-condition",
            "fresh installed CLI reconstructs the exact disposition edge",
            "--json",
        ],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(work_dir),
    )
    assert advanced.returncode == 0, advanced.stdout + advanced.stderr

    after = subprocess.run(
        [
            cli_path,
            "campaign",
            "reconciliation",
            "--workspace",
            str(workspace),
            "--json",
        ],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(work_dir),
    )
    assert after.returncode == 0, after.stdout + after.stderr
    after_payload = json.loads(after.stdout)
    report = after_payload["reports"][0]
    assert after_payload["disposition_required_count"] == 0
    assert after_payload["disposition_recorded_count"] == 1
    assert report["disposition_status"] == "disposition_recorded"
    assert report["bound_transition_ids"] == ["TR-P9-WHEEL"]

    encoded = json.dumps(after_payload, sort_keys=True).lower()
    for forbidden in (
        "recommended_action",
        "recommended_capability",
        "selected_capability",
        "semantic_score",
        "evidence_sufficient",
        "repair_authorized",
        "auto_advance",
        "auto_close",
    ):
        assert forbidden not in encoded
