from __future__ import annotations

import subprocess
import sys
import tomllib
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "release-v1.0.yaml"
VALIDATOR = ROOT / "scripts" / "validate-release-contract.py"


def test_release_contract_declares_public_surface_and_support_matrix() -> None:
    data = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))

    assert data["schema_version"] == 1
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    source_version = pyproject["project"]["version"]
    target_version = data["release"]["version"]
    assert data["release"]["status"] == "development"
    assert source_version == f"{target_version}.dev0"
    assert data["release"]["scope_classification"] == "reduced"
    assert data["public_surface"]["cli"]
    assert data["public_surface"]["agent_entrypoints"] == [
        "strategic-sensemaking-loop"
    ]
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


def test_public_agent_entrypoints_are_canonical_and_non_experimental() -> None:
    data = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    canonical = {
        path.parent.name
        for path in (ROOT / "skills").glob("*/SKILL.md")
    }
    entrypoints = set(data["public_surface"]["agent_entrypoints"])
    experimental = set(data["skill_inventory"]["experimental"])

    assert entrypoints <= canonical
    assert entrypoints.isdisjoint(experimental)
