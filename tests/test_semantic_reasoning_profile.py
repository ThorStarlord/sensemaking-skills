from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-semantic-reasoning-profile.py"
PM_VALIDATOR = ROOT / "scripts" / "validate-pm-feature-definition.py"
PHASE10 = ROOT / "docs" / "semantic-architecture" / "phase-10"
CHECKED_IN_PROFILES = (
    ROOT / "docs" / "semantic-architecture" / "pilots" / "pilot-a-profile.yaml",
    ROOT / "docs" / "semantic-architecture" / "pilots" / "pilot-b-profile.yaml",
    ROOT / "docs" / "semantic-architecture" / "pilots" / "pilot-c-profile.yaml",
    PHASE10 / "episode-1-chess-mentor-profile.yaml",
    PHASE10 / "episode-2-react-incremental-profile.yaml",
    PHASE10 / "episode-3-viralfactory-profile.yaml",
)


def _run(path: Path) -> tuple[subprocess.CompletedProcess[str], dict]:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), str(path), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    payload = json.loads(completed.stdout)
    return completed, payload


def _run_pm(path: Path) -> tuple[subprocess.CompletedProcess[str], dict]:
    completed = subprocess.run(
        [
            sys.executable,
            str(PM_VALIDATOR),
            str(path),
            "--repo-root",
            str(ROOT),
            "--json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    payload = json.loads(completed.stdout)
    return completed, payload


def _base_profile() -> dict:
    return {
        "artifact_id": "semantic_reasoning_profile",
        "schema_version": 1,
        "pilot_id": "test-pilot",
        "source_skill": "test-skill",
        "target": {
            "repository": "owner/repo",
            "ref": "abc123",
            "access_mode": "github_exact_sha",
        },
        "currentness": {
            "status": "pinned_snapshot",
            "evidence_refs": ["commit:abc123"],
        },
        "observations": [
            {
                "id": "O1",
                "statement": "file exists",
                "method": "direct_read",
                "evidence_refs": ["path/to/file"],
            }
        ],
        "claims": [
            {
                "id": "C1",
                "statement": "bounded interpretation",
                "epistemic_status": "INFERRED",
                "evidence_refs": ["path/to/file"],
                "scope": "test scope",
                "limits": ["does not establish semantic truth"],
            }
        ],
        "uncertainties": [],
        "explicit_limits": ["test fixture does not establish real-world truth"],
    }


def _write(tmp_path: Path, payload: dict) -> Path:
    path = tmp_path / "profile.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return path


def test_checked_in_semantic_profiles_validate() -> None:
    for profile in CHECKED_IN_PROFILES:
        completed, payload = _run(profile)
        assert completed.returncode == 0, (profile, completed.stdout, completed.stderr)
        assert payload["valid"] is True
        assert payload["semantic_truth_established"] is False
        assert payload["validator"] == "validate-semantic-reasoning-profile.py"


def test_phase10_pm_risk_artifact_keeps_domain_validator_authority() -> None:
    artifact = PHASE10 / "episode-3-viralfactory-risk-analysis.md"
    completed, payload = _run_pm(artifact)
    assert completed.returncode == 0, (artifact, completed.stdout, completed.stderr)
    assert payload["valid"] is True
    assert payload["artifact_id"] == "risk_analysis"
    assert payload["validator"] == "validate-pm-feature-definition.py"


def test_inferred_claim_requires_evidence(tmp_path: Path) -> None:
    payload = _base_profile()
    payload["claims"][0]["evidence_refs"] = []
    completed, result = _run(_write(tmp_path, payload))
    assert completed.returncode == 1
    assert result["valid"] is False
    assert "SEMANTIC_CLAIM_EVIDENCE_REQUIRED" in {e["error_id"] for e in result["errors"]}


def test_invalid_epistemic_status_is_rejected(tmp_path: Path) -> None:
    payload = _base_profile()
    payload["claims"][0]["epistemic_status"] = "TRUE"
    completed, result = _run(_write(tmp_path, payload))
    assert completed.returncode == 1
    assert "SEMANTIC_INVALID_EPISTEMIC_STATUS" in {e["error_id"] for e in result["errors"]}


def test_duplicate_claim_ids_are_rejected(tmp_path: Path) -> None:
    payload = _base_profile()
    duplicate = dict(payload["claims"][0])
    duplicate["statement"] = "different statement with duplicate identity"
    payload["claims"].append(duplicate)
    completed, result = _run(_write(tmp_path, payload))
    assert completed.returncode == 1
    assert "SEMANTIC_DUPLICATE_ID" in {e["error_id"] for e in result["errors"]}


def test_hypothesis_may_be_explicitly_ungrounded_without_becoming_truth(tmp_path: Path) -> None:
    payload = _base_profile()
    payload["claims"][0].update(
        {
            "statement": "a bounded future risk may exist",
            "epistemic_status": "HYPOTHESIZED",
            "evidence_refs": [],
            "limits": ["hypothesis has not been empirically observed"],
        }
    )
    completed, result = _run(_write(tmp_path, payload))
    assert completed.returncode == 0
    assert result["valid"] is True
    assert result["semantic_truth_established"] is False


def test_verified_currentness_requires_evidence(tmp_path: Path) -> None:
    payload = _base_profile()
    payload["currentness"]["evidence_refs"] = []
    completed, result = _run(_write(tmp_path, payload))
    assert completed.returncode == 1
    assert "SEMANTIC_CURRENTNESS_EVIDENCE_REQUIRED" in {e["error_id"] for e in result["errors"]}


def test_explicit_unverified_currentness_may_have_no_evidence(tmp_path: Path) -> None:
    payload = _base_profile()
    payload["currentness"] = {"status": "unverified", "evidence_refs": []}
    completed, result = _run(_write(tmp_path, payload))
    assert completed.returncode == 0
    assert result["valid"] is True
