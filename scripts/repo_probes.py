"""Deterministic repository probes for repo-sensemaker.

Pure probe functions: git subprocess reads and filesystem traversal only.
No pytest subprocess, no network, no writes. Every function returns plain
dicts safe for YAML serialization.
"""

from __future__ import annotations

import subprocess
from collections import Counter
from pathlib import Path
from typing import Dict


def _git(repo_root: Path, *args: str) -> str:
    """Run a read-only git command; return stdout stripped ('' on failure)."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            capture_output=True,
            text=True,
            cwd=str(repo_root),
            timeout=30,
        )
    except (subprocess.SubprocessError, OSError):
        return ""
    return proc.stdout.strip()


def git_state(repo_root: Path) -> Dict[str, object]:
    """Branch, head, and working-tree volume counts (verified, not documented)."""
    if _git(repo_root, "rev-parse", "--is-inside-work-tree") != "true":
        return {
            "is_git_repo": False,
            "branch": None,
            "head_sha": None,
            "head_message": None,
            "tracked_file_count": 0,
            "untracked_file_count": 0,
            "ignored_present_entry_count": 0,
            "dirty_file_count": 0,
        }

    branch = _git(repo_root, "symbolic-ref", "--short", "HEAD") or None
    head_sha = _git(repo_root, "rev-parse", "--short", "HEAD") or None
    head_message = _git(repo_root, "log", "-1", "--pretty=%s") or None

    tracked = _git(repo_root, "ls-files").splitlines()
    untracked = _git(repo_root, "ls-files", "--others", "--exclude-standard").splitlines()
    ignored_present = _git(repo_root, "status", "--porcelain=v1", "-uno", "--ignored").splitlines()
    porcelain = _git(repo_root, "status", "--porcelain=v1").splitlines()
    dirty = sum(1 for line in porcelain if not line.startswith("??"))

    return {
        "is_git_repo": True,
        "branch": branch,
        "head_sha": head_sha,
        "head_message": head_message,
        "tracked_file_count": len(tracked),
        "untracked_file_count": len(untracked),
        "ignored_present_entry_count": len(ignored_present),
        "dirty_file_count": dirty,
    }


def churn(repo_root: Path, commits: int = 50) -> Dict[str, object]:
    """Last-N-commit change frequency: descriptive signal, not a forecast."""
    subjects = _git(repo_root, "log", f"-{commits}", "--pretty=%s").splitlines()
    if not subjects:
        return {"commits_scanned": 0, "changed_files_last_n": 0, "top_changed_files": []}

    files = _git(repo_root, "log", f"-{commits}", "--pretty=format:", "--name-only").splitlines()
    counts = Counter(f for f in files if f and not f.startswith("docs/"))
    return {
        "commits_scanned": len(subjects),
        "changed_files_last_n": len(counts),
        "top_changed_files": [name for name, _ in counts.most_common(5)],
    }