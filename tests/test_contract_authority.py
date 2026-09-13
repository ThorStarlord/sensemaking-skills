from __future__ import annotations

import subprocess
import sys
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-contract-authority.py"


def test_stable_module_scan_detects_lab_imports(tmp_path: Path) -> None:
    module = tmp_path / "src" / "sensemaking_skills" / "campaigns" / "product.py"
    module.parent.mkdir(parents=True)
    module.write_text(
        "from sensemaking_skills.campaign_validation import validate\n",
        encoding="utf-8",
    )

    spec = importlib.util.spec_from_file_location("contract_authority", VALIDATOR)
    assert spec is not None and spec.loader is not None
    contract_authority = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(contract_authority)

    assert contract_authority.find_stable_lab_imports(
        tmp_path, ("sensemaking_skills.campaign_validation",)
    ) == [
        f"{Path('src') / 'sensemaking_skills' / 'campaigns' / 'product.py'}:1: sensemaking_skills.campaign_validation"
    ]


def test_contract_authority_validator_exists_and_accepts_repository() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--repo-root", str(ROOT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS" in result.stdout


def test_contract_authority_validator_rejects_missing_artifact_contract(tmp_path: Path) -> None:
    copied = tmp_path / "repo"
    copied.mkdir()
    for relative in (
        "release-v1.0.yaml",
        "pyproject.toml",
        "skills/workflow-planner/references/artifact-contracts.yaml",
        "skills/workflow-planner/references/skill-registry.yaml",
    ):
        destination = copied / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((ROOT / relative).read_bytes())
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--repo-root", str(copied)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "canonical Skill directory is missing" in result.stdout
