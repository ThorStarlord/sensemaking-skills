"""TargetCheckout tests (Phase 6 correction, #122).

Proves the target is materialized at the EXACT approved SHA with verified
origin, clean index/worktree, no untracked files, and no submodules -- and
that existing checkouts are never silently mutated or "fixed".
"""

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from sensemaking_skills.exploratory_execution import (
    TargetCheckout,
    TargetCheckoutError,
)

TARGET_REPO = "https://github.com/ThorStarlord/auteur.git"


class _TargetRepo:
    """A real local git repo standing in for the approved target."""

    def __init__(self, tmp_path: Path, name: str = "origin"):
        self.path = tmp_path / name
        self.path.mkdir()
        self._git(["init", "-q"])
        self._git(["config", "user.email", "t@e.i"])
        self._git(["config", "user.name", "T"])
        self._write("file.txt", "content")
        self._git(["add", "file.txt"])
        self._git(["commit", "-q", "-m", "initial"])
        self.sha = self._git(["rev-parse", "HEAD"]).stdout.strip()

    def _git(self, args):
        return subprocess.run(
            ["git", "-C", str(self.path)] + args,
            capture_output=True, text=True, check=False,
        )

    def _write(self, name, content):
        p = self.path / name
        p.write_text(content, encoding="utf-8")
        self._git(["add", name])
        self._git(["commit", "-q", "-m", f"add {name}"])

    def clone_to(self, dest: Path) -> None:
        result = subprocess.run(
            ["git", "clone", "-q", str(self.path), str(dest)],
            capture_output=True, text=True, check=False,
        )
        assert result.returncode == 0, result.stderr


def test_prepare_clones_fresh_checkout_at_exact_sha(tmp_path: Path) -> None:
    origin = _TargetRepo(tmp_path)
    checkout = TargetCheckout.prepare(
        target_repository=str(origin.path),
        target_sha=origin.sha,
        work_root=tmp_path / "work",
    )
    assert checkout.path.is_dir()
    assert checkout.path.name == "target"
    assert checkout.target_sha == origin.sha
    checkout.verify_integrity()  # re-verification is idempotent


def test_prepare_reuses_verified_existing_checkout(tmp_path: Path) -> None:
    origin = _TargetRepo(tmp_path)
    dest = tmp_path / "work" / "target"
    origin.clone_to(dest)
    checkout = TargetCheckout.prepare(
        target_repository=str(origin.path),
        target_sha=origin.sha,
        work_root=tmp_path / "work",
    )
    assert checkout.path == dest
    checkout.verify_integrity()


def test_refuses_wrong_head(tmp_path: Path) -> None:
    origin = _TargetRepo(tmp_path)
    origin._write("second.txt", "more")  # HEAD moves past the pinned sha
    dest = tmp_path / "work" / "target"
    origin.clone_to(dest)
    with pytest.raises(TargetCheckoutError) as exc:
        TargetCheckout.prepare(
            target_repository=str(origin.path),
            target_sha=origin.sha,
            work_root=tmp_path / "work",
        )
    assert "not the approved target sha" in str(exc.value)


def test_refuses_dirty_working_tree(tmp_path: Path) -> None:
    origin = _TargetRepo(tmp_path)
    dest = tmp_path / "work" / "target"
    origin.clone_to(dest)
    (dest / "file.txt").write_text("MUTATED", encoding="utf-8")
    with pytest.raises(TargetCheckoutError) as exc:
        TargetCheckout.prepare(
            target_repository=str(origin.path),
            target_sha=origin.sha,
            work_root=tmp_path / "work",
        )
    assert "not clean" in str(exc.value)


def test_refuses_untracked_files(tmp_path: Path) -> None:
    origin = _TargetRepo(tmp_path)
    dest = tmp_path / "work" / "target"
    origin.clone_to(dest)
    (dest / "sneaky-untracked.txt").write_text("x", encoding="utf-8")
    with pytest.raises(TargetCheckoutError) as exc:
        TargetCheckout.prepare(
            target_repository=str(origin.path),
            target_sha=origin.sha,
            work_root=tmp_path / "work",
        )
    assert "not clean" in str(exc.value)


def test_refuses_wrong_origin(tmp_path: Path) -> None:
    origin = _TargetRepo(tmp_path)
    other = _TargetRepo(tmp_path, name="other")
    dest = tmp_path / "work" / "target"
    other.clone_to(dest)  # clone of the WRONG repository
    with pytest.raises(TargetCheckoutError) as exc:
        TargetCheckout.prepare(
            target_repository=str(origin.path),
            target_sha=other.sha,
            work_root=tmp_path / "work",
        )
    assert "not the approved target repository" in str(exc.value)


def test_refuses_submodules(tmp_path: Path) -> None:
    origin = _TargetRepo(tmp_path)
    dest = tmp_path / "work" / "target"
    origin.clone_to(dest)
    (dest / ".gitmodules").write_text("[submodule \"x\"]\n", encoding="utf-8")
    with pytest.raises(TargetCheckoutError) as exc:
        TargetCheckout.prepare(
            target_repository=str(origin.path),
            target_sha=origin.sha,
            work_root=tmp_path / "work",
        )
    message = str(exc.value).lower()
    assert "submodule" in message or "not clean" in message


def test_refuses_non_git_directory(tmp_path: Path) -> None:
    work = tmp_path / "work"
    (work / "target").mkdir(parents=True)
    (work / "target" / "file.txt").write_text("x", encoding="utf-8")
    with pytest.raises(TargetCheckoutError) as exc:
        TargetCheckout.prepare(
            target_repository=str(tmp_path / "origin"),
            target_sha="0" * 40,
            work_root=work,
        )
    assert "not a git repository" in str(exc.value)


def test_verify_integrity_detects_mutation_after_prepare(tmp_path: Path) -> None:
    origin = _TargetRepo(tmp_path)
    dest = tmp_path / "work" / "target"
    origin.clone_to(dest)
    checkout = TargetCheckout.prepare(
        target_repository=str(origin.path),
        target_sha=origin.sha,
        work_root=tmp_path / "work",
    )
    (dest / "file.txt").write_text("MUTATED AFTER PREPARE", encoding="utf-8")
    with pytest.raises(TargetCheckoutError) as exc:
        checkout.verify_integrity()
    assert "not clean" in str(exc.value)
