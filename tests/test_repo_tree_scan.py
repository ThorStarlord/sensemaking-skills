"""Regression tests for the repository-tree scans in tests/support/repo_tree.py.

Parallel workers build wheels in the repository root, and a wheel build removes
its staging directory while another worker walks the tree. These tests simulate
that disappearance. They also check that the scans still find forbidden files,
still fail on unexpected filesystem errors, and still see the same tree when
nothing changes. Every simulation records that it fired, so a test cannot pass
without exercising the failure it names.
"""

from __future__ import annotations

import errno
import os
import shutil
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tests" / "support"))

from repo_tree import find_named, iter_tree, read_text_if_present


def _hook_scandir(monkeypatch, path: Path, action: Callable[[], None]) -> list[str]:
    """Run action the first time os.scandir is asked to list path.

    Returns the firing record, which the test asserts so a missed hook fails it.
    """
    fired: list[str] = []
    real_scandir = os.scandir
    target = os.fspath(path)

    def scandir(entry=".", *args, **kwargs):
        # shutil.rmtree lists directories by file descriptor, so non-path entries pass through.
        if isinstance(entry, (str, os.PathLike)) and os.fspath(entry) == target and not fired:
            fired.append(target)
            os.scandir = real_scandir  # the action may itself list the tree
            action()
        return real_scandir(entry, *args, **kwargs)

    monkeypatch.setattr(os, "scandir", scandir)
    return fired


def _raise(error: BaseException) -> None:
    raise error


def test_directory_removed_during_walk_is_skipped(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    staging = root / "build" / "bdist.linux-x86_64" / "wheel"
    (staging / "pkg").mkdir(parents=True)
    (staging / "pkg" / "data.txt").write_text("staged", encoding="utf-8")
    (root / "keep.md").write_text("kept", encoding="utf-8")
    fired = _hook_scandir(monkeypatch, staging, lambda: shutil.rmtree(staging))

    names = {path.relative_to(root).as_posix() for path in iter_tree(root)}

    assert fired == [os.fspath(staging)]
    assert "keep.md" in names
    assert not any(name.endswith("data.txt") for name in names)


def test_planted_forbidden_file_inside_build_tree_is_found(tmp_path):
    root = tmp_path / "repo"
    planted = root / "build" / "bdist.linux-x86_64" / "wheel" / "owner-approval.md"
    planted.parent.mkdir(parents=True)
    planted.write_text("approval", encoding="utf-8")

    assert find_named(root, "owner-approval.md") == [planted]


def test_forbidden_name_matches_directories_and_case_variants_only_exactly(tmp_path):
    root = tmp_path / "repo"
    (root / "a").mkdir(parents=True)
    (root / "a" / "Owner-Approval.md").write_text("variant", encoding="utf-8")
    (root / "b" / "owner-approval.md").mkdir(parents=True)
    (root / "c").mkdir()
    (root / "c" / "owner-approval.template.md").write_text("template", encoding="utf-8")
    (root / "c" / "owner-approval.SUPERSEDED-pre-artifact-root.md").write_text(
        "historical", encoding="utf-8"
    )

    found = sorted(
        path.relative_to(root).as_posix() for path in find_named(root, "owner-approval.md")
    )

    assert found == ["a/Owner-Approval.md", "b/owner-approval.md"]


def test_permission_failure_is_raised_not_skipped(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    locked = root / "locked"
    locked.mkdir(parents=True)
    denied = PermissionError(errno.EACCES, "permission denied", os.fspath(locked))
    fired = _hook_scandir(monkeypatch, locked, lambda: _raise(denied))

    with pytest.raises(PermissionError):
        find_named(root, "owner-approval.md")

    assert fired == [os.fspath(locked)]


def test_unexpected_filesystem_error_is_raised_not_skipped(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    broken = root / "broken"
    broken.mkdir(parents=True)
    failure = OSError(errno.EIO, "I/O error", os.fspath(broken))
    fired = _hook_scandir(monkeypatch, broken, lambda: _raise(failure))

    with pytest.raises(OSError) as raised:
        list(iter_tree(root))

    assert raised.value.errno == errno.EIO
    assert fired == [os.fspath(broken)]


def test_missing_root_fails_instead_of_passing_vacuously(tmp_path):
    with pytest.raises(NotADirectoryError):
        find_named(tmp_path / "absent", "owner-approval.md")


def test_tree_matches_rglob_when_nothing_changes(tmp_path):
    root = tmp_path / "repo"
    (root / "a" / "b").mkdir(parents=True)
    (root / "a" / "b" / "f.txt").write_text("1", encoding="utf-8")
    (root / ".hidden").write_text("2", encoding="utf-8")
    (root / "build" / "x").mkdir(parents=True)
    (root / "build" / "x" / "w.py").write_text("3", encoding="utf-8")
    try:
        os.symlink(root / "a", root / "link", target_is_directory=True)
    except (OSError, NotImplementedError):
        pass  # some Windows accounts cannot create symbolic links

    assert set(iter_tree(root)) == set(root.rglob("*"))


def test_removed_file_reads_as_none_and_other_read_failures_propagate(tmp_path, monkeypatch):
    present = tmp_path / "present.md"
    present.write_text("text", encoding="utf-8")

    assert read_text_if_present(present, encoding="utf-8") == "text"
    assert read_text_if_present(tmp_path / "removed.md") is None

    def deny_read(self, *args, **kwargs):
        raise PermissionError(errno.EACCES, "permission denied", str(self))

    monkeypatch.setattr(Path, "read_text", deny_read)
    with pytest.raises(PermissionError):
        read_text_if_present(present)
