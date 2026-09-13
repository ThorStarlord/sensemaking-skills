from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-docs-currentness.py"


def test_current_documentation_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--repo-root", str(ROOT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS" in result.stdout


def test_maintainer_guide_and_checklist_define_release_authority() -> None:
    guide = (ROOT / "docs" / "maintainer-guide-v1.0.md").read_text(encoding="utf-8")
    checklist = (ROOT / "docs" / "release-v1.0-checklist.md").read_text(encoding="utf-8")
    for text in (guide, checklist):
        assert "release-v1.0-contract.md" in text
        assert "semantic truth" in text
        assert "publication" in text
