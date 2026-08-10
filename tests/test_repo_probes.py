import subprocess
from pathlib import Path

import pytest

from scripts.repo_probes import git_state, churn


def _init_committed_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@t"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "t"], check=True)
    (repo / "file.txt").write_text("one", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "initial"], check=True)
    (repo / "file.txt").write_text("two", encoding="utf-8")
    (repo / "untracked.txt").write_text("u", encoding="utf-8")
    return repo


def test_git_state_reports_verified_current_state(tmp_path: Path) -> None:
    repo = _init_committed_repo(tmp_path)
    state = git_state(repo)
    assert state["is_git_repo"] is True
    assert state["branch"] == "main"
    assert state["head_message"] == "initial"
    assert state["tracked_file_count"] == 1
    assert state["untracked_file_count"] == 1
    assert state["dirty_file_count"] == 1
    assert len(state["head_sha"]) >= 7


def test_git_state_reports_non_git_directory(tmp_path: Path) -> None:
    state = git_state(tmp_path)
    assert state["is_git_repo"] is False
    assert state["tracked_file_count"] == 0


def test_churn_reports_top_changed_files(tmp_path: Path) -> None:
    repo = _init_committed_repo(tmp_path)
    report = churn(repo, commits=10)
    assert report["commits_scanned"] == 1
    assert report["top_changed_files"] == ["file.txt"]