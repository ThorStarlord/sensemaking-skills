"""Framework full-tree drift proof tests (Phase 6 correction, #122).

``framework_tree_unchanged`` must detect ANY difference between the
execution checkout and the pinned commit: committed tree, index, working
tree, AND untracked files. The Phase 6 readiness version compared only
``git diff <pin> HEAD`` and missed a dirty working tree at HEAD == pin --
this suite proves that hole is closed.
"""

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from sensemaking_skills.exploratory_execution import (
    execution_module_digests,
    framework_tree_unchanged,
    module_digest,
)


class _Repo:
    def __init__(self, tmp_path: Path, seed: str = "1"):
        self.path = tmp_path / "repo"
        self.path.mkdir()
        self._git(["init", "-q"])
        self._git(["config", "user.email", "t@e.i"])
        self._git(["config", "user.name", "T"])
        (self.path / "src").mkdir()
        # The seed guarantees distinct commit objects even when two repos
        # are created within the same second (identical tree + metadata
        # would otherwise produce identical SHAs).
        (self.path / "src" / "mod.py").write_text(f"x = {seed}\n", encoding="utf-8")
        (self.path / "skills").mkdir()
        (self.path / "skills" / "SKILL.md").write_text("skill\n", encoding="utf-8")
        self._git(["add", "."])
        self._git(["commit", "-q", "-m", "head"])
        self.sha = self._git(["rev-parse", "HEAD"]).stdout.strip()

    def _git(self, args):
        return subprocess.run(
            ["git", "-C", str(self.path)] + args,
            capture_output=True, text=True, check=False,
        )


def test_clean_checkout_at_pin_is_unchanged(tmp_path: Path) -> None:
    repo = _Repo(tmp_path)
    assert framework_tree_unchanged(repo.sha, repo.path) is True


def test_dirty_working_tree_is_detected(tmp_path: Path) -> None:
    """THE Phase 6 readiness hole: HEAD == pin with a modified file on
    disk must be detected as drift."""
    repo = _Repo(tmp_path)
    (repo.path / "src" / "mod.py").write_text("x = 999\n", encoding="utf-8")
    status = repo._git(["status", "--porcelain"]).stdout.strip()
    assert status != ""
    assert framework_tree_unchanged(repo.sha, repo.path) is False


def test_untracked_file_is_detected(tmp_path: Path) -> None:
    repo = _Repo(tmp_path)
    (repo.path / "sneaky.py").write_text("print('x')\n", encoding="utf-8")
    assert framework_tree_unchanged(repo.sha, repo.path) is False


def test_committed_tree_change_is_detected(tmp_path: Path) -> None:
    repo = _Repo(tmp_path)
    (repo.path / "src" / "mod.py").write_text("x = 2\n", encoding="utf-8")
    repo._git(["add", "."])
    repo._git(["commit", "-q", "-m", "new head"])
    assert framework_tree_unchanged(repo.sha, repo.path) is False


def test_staged_change_is_detected(tmp_path: Path) -> None:
    repo = _Repo(tmp_path)
    (repo.path / "src" / "mod.py").write_text("x = 3\n", encoding="utf-8")
    repo._git(["add", "."])
    assert framework_tree_unchanged(repo.sha, repo.path) is False


def test_wrong_head_is_detected(tmp_path: Path) -> None:
    repo = _Repo(tmp_path, seed="1")
    other = _Repo(tmp_path.parent, seed="2")
    assert framework_tree_unchanged(other.sha, repo.path) is False


def test_module_digests_are_content_addressed(tmp_path: Path) -> None:
    repo = _Repo(tmp_path)
    d1 = module_digest(repo.path / "src" / "mod.py")
    (repo.path / "src" / "mod.py").write_text("x = 2\n", encoding="utf-8")
    d2 = module_digest(repo.path / "src" / "mod.py")
    assert d1 != d2
    assert len(d1) == 64


def test_execution_module_digests_fail_on_missing_module(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError) as exc:
        execution_module_digests(tmp_path)
    assert "missing" in str(exc.value)
