from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "release-v1.0.yaml"
VALIDATOR = ROOT / "scripts" / "validate-release-contract.py"


def test_release_contract_declares_public_surface_and_support_matrix() -> None:
    data = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))

    assert data["schema_version"] == 1
    assert data["release"]["version"] == "1.0.0rc1"
    assert data["release"]["scope_classification"] == "reduced"
    assert data["public_surface"]["cli"]
    assert data["support"]["python"]
    assert data["support"]["harnesses"]
    assert data["support"]["native_harnesses"] == []
    assert data["claims"]
    assert all(isinstance(claim["support_required"], bool) for claim in data["claims"])


def test_release_contract_classifies_every_canonical_skill() -> None:
    data = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    canonical = {
        path.parent.name
        for path in (ROOT / "skills").glob("*/SKILL.md")
    }
    classified = set(data["skill_inventory"]["supported"])
    classified |= set(data["skill_inventory"]["internal"])
    classified |= set(data["skill_inventory"]["experimental"])
    assert classified == canonical


def test_release_contract_validator_accepts_repository() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--repo-root", str(ROOT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS" in result.stdout
