"""Deterministic repository probes for repo-sensemaker.

Pure probe functions: git subprocess reads and filesystem traversal only.
No pytest subprocess, no network, no writes. Every function returns plain
dicts safe for YAML serialization.
"""

from __future__ import annotations

import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Dict, List


def _git(repo_root: Path, *args: str) -> str:
    """Run a read-only git command; return stdout stripped ('' on failure)."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
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
    ignored_present = _git(repo_root, "status", "--porcelain=v1", "--ignored").splitlines()
    porcelain = _git(repo_root, "status", "--porcelain=v1").splitlines()
    dirty = sum(1 for line in porcelain if not line.startswith("??"))

    return {
        "is_git_repo": True,
        "branch": branch,
        "head_sha": head_sha,
        "head_message": head_message,
        "tracked_file_count": len(tracked),
        "untracked_file_count": len(untracked),
        "ignored_present_entry_count": sum(1 for line in ignored_present if line.startswith("!!")),
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


CI_FILE_CANDIDATES = (
    ".gitlab-ci.yml",
    ".circleci/config.yml",
)
CI_TOKEN_RE = re.compile(r"scripts/[\w./-]+\.py|\bpytest\b")
README_TOKEN_RE = re.compile(r"scripts/[\w./-]+\.py")


def _ci_texts(repo_root: Path) -> List[str]:
    texts: List[str] = []
    workflows_dir = repo_root / ".github" / "workflows"
    if workflows_dir.is_dir():
        texts.extend(
            p.read_text(encoding="utf-8", errors="replace")
            for p in sorted(workflows_dir.glob("*.y*ml"))
        )
    for candidate in CI_FILE_CANDIDATES:
        path = repo_root / candidate
        if path.is_file():
            texts.append(path.read_text(encoding="utf-8", errors="replace"))
    return texts


def ci_enforcement(repo_root: Path) -> Dict[str, object]:
    """Compare README-declared verification entrypoints against CI run steps."""
    readme = repo_root / "README.md"
    declared: List[str] = []
    if readme.is_file():
        text = readme.read_text(encoding="utf-8", errors="replace")
        declared = list(dict.fromkeys(README_TOKEN_RE.findall(text)))

    enforced: List[str] = []
    for ci_text in _ci_texts(repo_root):
        for line in ci_text.splitlines():
            stripped = line.strip()
            if stripped.lstrip("- ").startswith("run:"):
                enforced.extend(CI_TOKEN_RE.findall(stripped))
    enforced = list(dict.fromkeys(enforced))

    declared_in_ci = [check for check in declared if check in enforced]

    if not declared:
        vg = 0.0
        notes = "no declared verification entrypoints found in README"
    elif not enforced:
        vg = 1.0
        notes = "no CI run steps found; all declared checks unenforced"
    else:
        vg = round(1 - len(declared_in_ci) / len(declared), 2)
        notes = "" if vg == 0.0 else "declared-but-unenforced checks detected"

    return {
        "declared_checks": declared,
        "enforced_checks": enforced,
        "declared_in_ci": declared_in_ci,
        "vg": vg,
        "notes": notes,
    }
