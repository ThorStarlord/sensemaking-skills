"""Regression coverage for cross-platform validator dispatch."""

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATE_AND_REPORT = REPO_ROOT / "scripts" / "validate-and-report.py"
VALID_BRIEF = REPO_ROOT / "tests" / "fixtures" / "repo-sensemaker-template-canonical.md"


def test_wrapper_uses_the_current_python_interpreter():
    result = subprocess.run(
        [sys.executable, str(VALIDATE_AND_REPORT), str(VALID_BRIEF)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["valid"] is True
    assert payload["validator"] == "validate-brief.py"
    assert payload["errors"] == []
