"""Read-only local worktree metadata beside a committed semantic snapshot.

The checked-out source overlay is never part of the indexed knowledge result.
"""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path


def _git(
    root: Path, *args: str, disable_filters: tuple[str, ...] = (),
    no_match_ok: bool = False,
) -> bytes:
    overrides = [part for name in disable_filters for part in ("-c", f"{name}=")]
    try:
        result = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", *overrides, "-C", str(root), *args],
            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0"},
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=20,
            check=False,
        )
        if result.returncode and not (no_match_ok and result.returncode == 1):
            raise ValueError("cannot inspect local Git repository worktree")
        return result.stdout
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError("cannot inspect local Git repository worktree") from exc


def _configured_external_filters(root: Path) -> tuple[str, ...]:
    """Find custom filter commands so read operations can disable each one."""
    names = _git(
        root, "config", "--null", "--name-only", "--get-regexp",
        r"^filter\..*\.(clean|smudge|process)$", no_match_ok=True,
    )
    keys = tuple(sorted(set(
        item.decode("utf-8", "surrogateescape")
        for item in names.split(b"\x00") if item
    )))
    if len(keys) > 128:
        raise ValueError("too many configured Git external filters for safe inspection")
    return keys


def inspect_worktree_context(repo_root: Path, indexed_ref: str) -> dict[str, object]:
    """Inspect HEAD and dirtiness without indexing or running source filters."""
    if not re.fullmatch(r"[0-9a-f]{40}", indexed_ref):
        raise ValueError("indexed_ref must be an exact 40-character Git SHA")
    root = Path(repo_root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError("target must be a Git repository directory")
    top = Path(_git(root, "rev-parse", "--show-toplevel").decode("utf-8").strip()).resolve()
    disabled = _configured_external_filters(top)
    head = _git(top, "rev-parse", "HEAD", disable_filters=disabled).decode("ascii").strip()
    tracked = _git(top, "diff", "--no-ext-diff", "--no-textconv", "--ignore-submodules=all", "--name-only", "-z", "HEAD", "--", disable_filters=disabled).split(b"\x00")
    untracked = _git(top, "ls-files", "--others", "--exclude-standard", "-z", disable_filters=disabled).split(b"\x00")
    status = _git(top, "status", "--porcelain=v1", "--ignore-submodules=all", "--untracked-files=all", "-z", disable_filters=disabled)
    return {
        "current_head": head,
        "indexed_ref": indexed_ref,
        "head_matches_indexed_ref": head == indexed_ref,
        "worktree_clean": not bool(status),
        "modified_tracked_count": sum(bool(path) for path in tracked),
        "untracked_count": sum(bool(path) for path in untracked),
        "uncommitted_changes_not_indexed": bool(status),
        "source_alignment_not_semantic_truth": True,
        "external_filter_commands_disabled_count": len(disabled),
        "submodule_worktrees_not_assessed": True,
    }
