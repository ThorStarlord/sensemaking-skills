"""Read-only local worktree metadata beside a committed semantic snapshot.

The checked-out source overlay is never part of the indexed knowledge result.
"""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path


class GitReadError(ValueError):
    """A guarded Git read failed. str(error) is the existing caller-visible text, unchanged.

    `detail` carries Git's own stderr (or the OS error), so a caller that already reported it can
    keep its own wording without losing the reason.
    """

    def __init__(self, message: str, detail: str = "") -> None:
        super().__init__(message)
        self.detail = detail


def _git(
    root: Path, *args: str, disable_filters: tuple[str, ...] = (),
    no_match_ok: bool = False,
) -> bytes:
    overrides = [part for name in disable_filters for part in ("-c", f"{name}=")]
    try:
        result = subprocess.run(
            # core.hooksPath: a diff against the worktree writes the index, which runs the
            # repository's post-index-change hook even with GIT_OPTIONAL_LOCKS=0.
            ["git", "-c", "core.fsmonitor=false", "-c", f"core.hooksPath={os.devnull}",
             *overrides, "-C", str(root), *args],
            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0"},
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            check=False,
        )
        if result.returncode and not (no_match_ok and result.returncode == 1):
            detail = result.stderr.decode("utf-8", "replace").strip()
            raise GitReadError("cannot inspect local Git repository worktree", detail=detail)
        return result.stdout
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GitReadError("cannot inspect local Git repository worktree", detail=str(exc)) from exc


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
    # `-c name=` is split at its first '=', so a name containing '=' or a line break would
    # disable the wrong key. Refuse such configuration instead of inspecting it unguarded.
    if any("=" in key or "\n" in key or "\r" in key for key in keys):
        raise ValueError("repository configuration names a Git filter containing '=' or a line break; "
                         "the guard cannot disable it safely")
    if len(keys) > 128:
        raise ValueError("too many configured Git external filters for safe inspection")
    return keys


def guarded_git_text(root: Path, *args: str, disable_filters: bool = True,
                     encoding: str = "utf-8", errors: str = "surrogateescape") -> str:
    """Return Git output with fsmonitor, configured external filters and repository hooks disabled.

    Read-only in intent, with one exception: a diff against the worktree may still refresh the
    index file. That is not suppressed, and no hook runs as a result.

    Use for any command that reads the index or the worktree (status, ls-files, diff against
    the worktree, rev-parse of a checkout). Git may run core.fsmonitor, or clean, smudge and
    process filters named by the repository's own configuration, while it reads those. Diff-like
    callers must still pass --no-textconv and --no-ext-diff.

    Known behaviour, not a bypass: for a file whose stored form comes from a transforming filter
    (git-lfs pattern), the raw comparison reports it modified. A driver marked required makes
    status fail, and Git's reason is included in the error. Callers fail closed on both.
    """
    # disable_filters=False keeps the repository's configured clean and smudge filters running, as
    # those callers did before. It still disables fsmonitor and repository hooks, which change no output.
    disabled = _configured_external_filters(root) if disable_filters else ()
    return _git(root, *args, disable_filters=disabled).decode(encoding, errors)


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


def changed_paths_since_indexed_ref(repo_root: Path, indexed_ref: str) -> dict[str, object]:
    """List paths whose working-tree state differs from the indexed commit.

    Covers commits made after indexing plus staged/unstaged/untracked edits.
    Return path names only. Git diff may inspect working-tree bytes internally;
    those bytes are not stored in the semantic index or treated as indexed evidence.
    """
    if not re.fullmatch(r"[0-9a-f]{40}", indexed_ref):
        raise ValueError("indexed_ref must be an exact 40-character Git SHA")
    root = Path(repo_root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError("target must be a Git repository directory")
    top = Path(_git(root, "rev-parse", "--show-toplevel").decode("utf-8").strip()).resolve()
    disabled = _configured_external_filters(top)
    try:
        _git(top, "cat-file", "-e", f"{indexed_ref}^{{commit}}", disable_filters=disabled)
    except ValueError as exc:
        raise ValueError("indexed revision is not available in the local Git repository; NOT ASSESSED") from exc
    tracked = _git(top, "diff", "--no-ext-diff", "--no-textconv", "--no-renames", "--ignore-submodules=all",
                   "--name-only", "-z", indexed_ref, "--", disable_filters=disabled).split(b"\x00")
    # A staged index entry can differ from the cited revision even when the
    # working file has been restored to identical bytes. Query both trees.
    staged = _git(top, "diff", "--cached", "--no-ext-diff", "--no-textconv", "--no-renames",
                  "--ignore-submodules=all", "--name-only", "-z", indexed_ref, "--",
                  disable_filters=disabled).split(b"\x00")
    untracked = _git(top, "ls-files", "--others", "--exclude-standard", "-z",
                     disable_filters=disabled).split(b"\x00")
    paths = frozenset(
        item.decode("utf-8", "surrogateescape") for item in (*tracked, *staged, *untracked) if item
    )
    return {"paths": paths, "external_filter_commands_disabled_count": len(disabled)}
