"""Worktree metadata must never masquerade as the committed knowledge index."""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from sensemaking_skills.semantic_architecture.worktree_context import inspect_worktree_context


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


@pytest.fixture
def checkout(tmp_path: Path) -> tuple[Path, str]:
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q")
    git(root, "config", "user.email", "tests@example.com")
    git(root, "config", "user.name", "Tests")
    (root / "tracked.txt").write_text("original\n", encoding="utf-8")
    git(root, "add", "tracked.txt")
    git(root, "commit", "-qm", "initial")
    return root, git(root, "rev-parse", "HEAD")


def test_clean_matching_head_reports_no_unindexed_changes(checkout):
    root, sha = checkout
    data = inspect_worktree_context(root, sha)
    assert data["current_head"] == sha
    assert data["indexed_ref"] == sha
    assert data["head_matches_indexed_ref"] is True
    assert data["worktree_clean"] is True
    assert data["uncommitted_changes_not_indexed"] is False
    assert data["source_alignment_not_semantic_truth"] is True
    assert data["modified_tracked_count"] == data["untracked_count"] == 0


def test_dirty_current_workspace_query_reports_unindexed_changes(checkout):
    root, sha = checkout
    (root / "tracked.txt").write_text("changed\n", encoding="utf-8")
    (root / "extra.txt").write_text("untracked\n", encoding="utf-8")
    data = inspect_worktree_context(root, sha)
    assert data["head_matches_indexed_ref"] is True
    assert data["worktree_clean"] is False
    assert data["modified_tracked_count"] == 1
    assert data["untracked_count"] == 1
    assert data["uncommitted_changes_not_indexed"] is True


def test_historical_index_from_new_head_is_labeled_historical(checkout):
    root, old_sha = checkout
    (root / "tracked.txt").write_text("new committed file\n", encoding="utf-8")
    git(root, "commit", "-qam", "next")
    data = inspect_worktree_context(root, old_sha)
    assert data["head_matches_indexed_ref"] is False
    assert data["worktree_clean"] is True
    assert data["uncommitted_changes_not_indexed"] is False
    assert data["current_head"] != old_sha


def test_staged_changes_are_reported(checkout):
    root, sha = checkout
    (root / "tracked.txt").write_text("staged\n", encoding="utf-8")
    git(root, "add", "tracked.txt")
    data = inspect_worktree_context(root, sha)
    assert data["modified_tracked_count"] == 1
    assert data["worktree_clean"] is False


def test_non_repository_is_rejected(tmp_path: Path):
    with pytest.raises(ValueError, match="Git repository"):
        inspect_worktree_context(tmp_path, "f" * 40)
