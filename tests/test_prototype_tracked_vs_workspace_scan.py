"""
Tests for scripts/prototype_tracked_vs_workspace_scan.py.

PROTOTYPE (prototype/repo-sensemaker-vnext). Formalizes the P4 ".venv
correction" (workspace scan != tracked product surface) as a reusable check.
"""

import importlib.util
import os
import subprocess
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

_spec = importlib.util.spec_from_file_location(
    "prototype_tracked_vs_workspace_scan",
    os.path.join(SCRIPTS_DIR, "prototype_tracked_vs_workspace_scan.py"),
)
scan = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(scan)


def _write(path, content="x"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _init_git_repo(tmp_path, tracked_files):
    subprocess.run(["git", "init", "-q"], cwd=str(tmp_path), check=True)
    subprocess.run(["git", "config", "user.email", "t@example.com"], cwd=str(tmp_path), check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=str(tmp_path), check=True)
    for f in tracked_files:
        _write(str(tmp_path / f))
    subprocess.run(["git", "add", "-A"], cwd=str(tmp_path), check=True)
    subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=str(tmp_path), check=True)


def test_reproduces_the_p4_dot_venv_pattern(tmp_path):
    """5 tracked product files, plus a much larger untracked .venv/ tree --
    exactly P4's own reconciliation (5 tracked .md files vs. 30 total, 25 of
    which lived under .venv/)."""
    _init_git_repo(tmp_path, [
        "README.md",
        "src/app.py",
    ])
    for i in range(20):
        _write(str(tmp_path / ".venv" / "site-packages" / f"pkg{i}.py"))

    result = scan.compare_tracked_vs_workspace(str(tmp_path), ".")

    assert result["is_git_repo"] is True
    assert result["tracked_count"] == 2
    assert result["workspace_count"] == 22
    assert result["untracked_count"] == 20
    assert result["untracked_ratio"] > 0.8
    assert ".venv" in result["untracked_top_level_dirs"]


def test_no_untracked_files_gives_zero_ratio(tmp_path):
    _init_git_repo(tmp_path, ["README.md", "src/app.py"])

    result = scan.compare_tracked_vs_workspace(str(tmp_path), ".")

    assert result["untracked_count"] == 0
    assert result["untracked_ratio"] == 0.0
    assert result["untracked_top_level_dirs"] == []


def test_scoped_to_a_subdirectory(tmp_path):
    _init_git_repo(tmp_path, ["README.md", "src/tracked.py"])
    _write(str(tmp_path / "src" / "untracked.py"))
    _write(str(tmp_path / "other" / "unrelated_untracked.py"))

    result = scan.compare_tracked_vs_workspace(str(tmp_path), "src")

    # Only src/ is in scope -- other/'s untracked file must not be counted.
    assert result["tracked_count"] == 1
    assert result["workspace_count"] == 2
    assert result["untracked_count"] == 1


def test_falls_back_gracefully_outside_a_git_repo(tmp_path):
    _write(str(tmp_path / "a.txt"))
    _write(str(tmp_path / "b.txt"))

    result = scan.compare_tracked_vs_workspace(str(tmp_path), ".")

    assert result["is_git_repo"] is False
    assert result["workspace_count"] == 2
    assert result["untracked_count"] == 2


def test_against_real_repo_scripts_dir_is_mostly_tracked():
    """Sanity check: this repo's own scripts/ directory should have a low
    (near-zero) untracked ratio -- unlike a directory containing a .venv/."""
    result = scan.compare_tracked_vs_workspace(REPO_ROOT, "scripts")

    assert result["is_git_repo"] is True
    assert result["tracked_count"] > 10
    assert result["untracked_ratio"] < 0.3


def test_main_warns_above_threshold(tmp_path, capsys):
    _init_git_repo(tmp_path, ["README.md"])
    for i in range(10):
        _write(str(tmp_path / ".venv" / f"f{i}.py"))

    code = scan.main(["--repo-root", str(tmp_path), "--subdir", "."])
    out = capsys.readouterr().out

    assert code == 0
    assert "WARNING" in out
