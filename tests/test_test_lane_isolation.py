from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_default_collection_excludes_nested_external_harness() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "deepseek-harness" not in result.stdout


def test_product_and_contract_validators_are_explicit_commands() -> None:
    package_json = (ROOT / "package.json").read_text(encoding="utf-8")
    assert '"test"' in package_json
    assert '"validate:release"' in package_json
