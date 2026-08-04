"""Framework-drift invariant tests (Issue #122).

The campaign policy pins ``framework_sha 4ba049e...``. The execution
infrastructure lives OUTSIDE the campaign configuration, so the framework
code (``src/`` + the canonical executor and Gate A scripts) must remain
BYTE-IDENTICAL to the pinned SHA at this head. If this test fails, the
framework drifted and the pinned campaign configuration no longer
describes the code that would execute -- a new preparation revision and a
new approval would be required.
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from execution_infra.versions import (
    FRAMEWORK_CODE_PATHS,
    framework_code_unchanged,
)

PINNED_FRAMEWORK_SHA = "4ba049e04e74699a009147df112baed3f7536343"
REPO_ROOT = Path(__file__).resolve().parents[2]


def test_framework_code_is_byte_identical_to_the_pin() -> None:
    assert framework_code_unchanged(PINNED_FRAMEWORK_SHA, REPO_ROOT), (
        "framework code drifted from the pinned SHA; the EXP-0001 campaign "
        "configuration no longer describes the executing code"
    )


def test_framework_code_paths_exist_at_the_pin() -> None:
    """The pinned SHA genuinely contains the framework paths we protect."""
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-tree", "-r", "--name-only",
         PINNED_FRAMEWORK_SHA, "--"] + FRAMEWORK_CODE_PATHS,
        capture_output=True, text=True, timeout=60, check=False,
    )
    assert result.returncode == 0
    assert "src/sensemaking_skills/campaign_accounting" in result.stdout
    assert "scripts/skill_executor.py" in result.stdout
    assert "scripts/gate_a_authorization.py" in result.stdout


def test_drift_is_detected_when_a_framework_file_changes(tmp_path: Path) -> None:
    """The drift check must be sensitive: a framework-file edit flips it."""
    # A repo whose HEAD differs from the pin in a framework path. Use a
    # fresh worktree-like copy: simplest is a temp repo with one commit.
    repo = tmp_path / "drifted"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "p@e.i"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "P"], check=True)
    src = repo / "src"
    src.mkdir()
    (src / "changed.py").write_text("x = 1\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "head"], check=True)
    head = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()
    # A second commit mutates a framework path.
    (src / "changed.py").write_text("x = 2\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "drift"], check=True)

    assert framework_code_unchanged(head, repo, framework_paths=["src"]) is False
