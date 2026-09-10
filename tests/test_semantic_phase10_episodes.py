from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEMANTIC_VALIDATOR = ROOT / "scripts" / "validate-semantic-reasoning-profile.py"
PM_VALIDATOR = ROOT / "scripts" / "validate-pm-feature-definition.py"
PHASE10 = ROOT / "docs" / "semantic-architecture" / "phase-10"

PROFILES = (
    PHASE10 / "episode-1-chess-mentor-profile.yaml",
    PHASE10 / "episode-2-react-incremental-profile.yaml",
    PHASE10 / "episode-3-viralfactory-profile.yaml",
)


def _run(script: Path, artifact: Path) -> tuple[subprocess.CompletedProcess[str], dict]:
    completed = subprocess.run(
        [sys.executable, str(script), str(artifact), "--repo-root", str(ROOT), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return completed, json.loads(completed.stdout)


def test_phase10_profiles_validate_without_claiming_semantic_truth() -> None:
    for profile in PROFILES:
        completed, payload = _run(SEMANTIC_VALIDATOR, profile)
        assert completed.returncode == 0, (profile, completed.stdout, completed.stderr)
        assert payload["valid"] is True
        assert payload["semantic_truth_established"] is False
        assert payload["validator"] == "validate-semantic-reasoning-profile.py"


def test_phase10_pm_risk_artifact_uses_existing_domain_contract() -> None:
    artifact = PHASE10 / "episode-3-viralfactory-risk-analysis.md"
    completed, payload = _run(PM_VALIDATOR, artifact)
    assert completed.returncode == 0, (completed.stdout, completed.stderr)
    assert payload["valid"] is True
    assert payload["artifact_id"] == "risk_analysis"
    assert payload["validator"] == "validate-pm-feature-definition.py"
