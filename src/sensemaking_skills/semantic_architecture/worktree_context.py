"""Read-only local worktree metadata beside a committed semantic snapshot.

The checked-out source overlay is never part of the indexed knowledge result.
"""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path


def _git(root: Path, *args: str) -> bytes:
    try:
        return subprocess.check_output(
            ["git", "-c", "core.fsmonitor=false", "-C", str(root), *args],
            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0"},
            stderr=subprocess.PIPE,
            timeout=20,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise ValueError("cannot inspect local Git repository worktree") from exc


def inspect_worktree_context(repo_root: Path, indexed_ref: str) -> dict[str, object]:
    """Inspect current Git HEAD and dirtiness, without indexing working bytes."""
    if not re.fullmatch(r"[0-9a-f]{40}", indexed_ref):
        raise ValueError("indexed_ref must be an exact 40-character Git SHA")
    root = Path(repo_root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError("target must be a Git repository directory")
    top = Path(_git(root, "rev-parse", "--show-toplevel").decode("utf-8").strip()).resolve()
    head = _git(top, "rev-parse", "HEAD").decode("ascii").strip()
    tracked = _git(top, "diff", "--no-ext-diff", "--no-textconv", "--name-only", "-z", "HEAD", "--").split(b"\x00")
    untracked = _git(top, "ls-files", "--others", "--exclude-standard", "-z").split(b"\x00")
    status = _git(top, "status", "--porcelain=v1", "--untracked-files=all", "-z")
    return {
        "current_head": head,
        "indexed_ref": indexed_ref,
        "head_matches_indexed_ref": head == indexed_ref,
        "worktree_clean": not bool(status),
        "modified_tracked_count": sum(bool(path) for path in tracked),
        "untracked_count": sum(bool(path) for path in untracked),
        "uncommitted_changes_not_indexed": bool(status),
        "source_alignment_not_semantic_truth": True,
    }
