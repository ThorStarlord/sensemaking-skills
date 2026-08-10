import subprocess
from pathlib import Path

from scripts.repo_probes import churn, ci_enforcement, git_state


def _new_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@t"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "t"], check=True)
    return repo


def _commit(repo: Path, message: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo), "-c", "commit.gpgsign=false", "commit", "-q", "-m", message],
        check=True,
    )


def _init_committed_repo(tmp_path: Path) -> Path:
    repo = _new_repo(tmp_path)
    (repo / "file.txt").write_text("one", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    _commit(repo, "initial")
    (repo / "file.txt").write_text("two", encoding="utf-8")
    (repo / "untracked.txt").write_text("u", encoding="utf-8")
    return repo


def test_git_state_reports_verified_current_state(tmp_path: Path) -> None:
    repo = _init_committed_repo(tmp_path)
    (repo / ".gitignore").write_text("ignored.txt\n", encoding="utf-8")
    (repo / "ignored.txt").write_text("ignored", encoding="utf-8")
    state = git_state(repo)
    assert state["is_git_repo"] is True
    assert state["branch"] == "main"
    assert state["head_message"] == "initial"
    assert state["tracked_file_count"] == 1
    assert state["untracked_file_count"] == 2
    assert state["dirty_file_count"] == 1
    assert state["ignored_present_entry_count"] == 1
    assert len(state["head_sha"]) >= 7


def test_git_state_reports_non_git_directory(tmp_path: Path) -> None:
    state = git_state(tmp_path)
    assert state["is_git_repo"] is False
    assert state["tracked_file_count"] == 0


def test_git_state_empty_repo(tmp_path: Path) -> None:
    repo = _new_repo(tmp_path)
    state = git_state(repo)
    assert state["is_git_repo"] is True
    assert state["tracked_file_count"] == 0


def test_git_state_detached_head(tmp_path: Path) -> None:
    repo = _new_repo(tmp_path)
    (repo / "file.txt").write_text("one", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    _commit(repo, "initial")
    subprocess.run(["git", "-C", str(repo), "checkout", "--detach", "-q"], check=True)
    state = git_state(repo)
    assert state["is_git_repo"] is True
    assert state["branch"] is None


def test_churn_reports_top_changed_files(tmp_path: Path) -> None:
    repo = _init_committed_repo(tmp_path)
    report = churn(repo, commits=10)
    assert report["commits_scanned"] == 1
    assert report["top_changed_files"] == ["file.txt"]


def _repo_with_readme_and_ci(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / ".github" / "workflows").mkdir(parents=True)
    (repo / "README.md").write_text(
        "## Verification\nCI runs the same entrypoint: `python scripts/check.py` and pytest.\n",
        encoding="utf-8",
    )
    (repo / ".github" / "workflows" / "validation.yml").write_text(
        "jobs:\n  test:\n    steps:\n      - run: pytest -q\n",
        encoding="utf-8",
    )
    return repo


def test_verification_gap_detects_unenforced_ci_claim(tmp_path: Path) -> None:
    report = ci_enforcement(_repo_with_readme_and_ci(tmp_path))
    assert report["declared_checks"] == ["scripts/check.py"]
    assert report["enforced_checks"] == ["pytest"]
    assert report["declared_in_ci"] == []
    assert report["vg"] == 1.0


def test_verification_gap_zero_when_fully_enforced(tmp_path: Path) -> None:
    repo = _repo_with_readme_and_ci(tmp_path)
    (repo / ".github" / "workflows" / "validation.yml").write_text(
        "jobs:\n  test:\n    steps:\n      - run: python scripts/check.py\n",
        encoding="utf-8",
    )
    report = ci_enforcement(repo)
    assert report["declared_in_ci"] == ["scripts/check.py"]
    assert report["vg"] == 0.0


def test_verification_gap_zero_when_no_checks_declared(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("Nothing about verification here.\n", encoding="utf-8")
    report = ci_enforcement(repo)
    assert report["declared_checks"] == []
    assert report["vg"] == 0.0
