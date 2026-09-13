from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "public-surface-v1.0.md"


def test_stable_cli_commands_are_registered() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "sensemaking_skills.cli", "--help"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    for command in ("campaign", "semantic", "setup-skills", "validate", "analyze"):
        assert command in result.stdout


def test_legacy_runner_policy_is_explicit() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "compatibility-only" in text
    assert "semantic routing authority" in text
    assert "source-only" in text
    assert "error-boundaries-v1.0.md" in text
