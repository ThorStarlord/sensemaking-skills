"""Shared exact-commit source access and local evidence-path normalization.

This boundary provides materialization, Git source identity and contained
tracked-file access. Semantic snapshot construction, claims and retrieval
belong to the consumers. The existing checkout and source-safety contracts
are preserved; a temporary worktree is not a security sandbox.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from .worktree_context import _configured_external_filters, inspect_worktree_context


def _git(root: Path, *args: str, timeout: int = 30) -> str:
    try:
        proc = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", *args], cwd=root, text=True, capture_output=True,
            timeout=timeout, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError(f"Git snapshot inspection unavailable: {exc}") from exc
    if proc.returncode:
        raise ValueError(f"Git snapshot inspection failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def verified_tracked_sources(repo_root: str | Path, target_ref: str) -> tuple[Path, set[str]]:
    """Fail closed unless target is exactly clean committed Git source bytes."""
    root = Path(repo_root).resolve()
    if not re.fullmatch(r"[0-9a-f]{40}", target_ref):
        raise ValueError("target_ref must be a full 40-character Git SHA")
    if Path(_git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise ValueError("repo_root must be the exact Git checkout root")
    # Use the same filter-safe, non-mutating source-state inspection as query
    # context. A bare git status can invoke configured external clean/process
    # filters while checking worktree bytes.
    context = inspect_worktree_context(root, target_ref)
    if not context["head_matches_indexed_ref"]:
        raise ValueError("target_ref does not equal the checked-out Git HEAD")
    if not context["worktree_clean"]:
        raise ValueError("dirty or untracked worktree: source bytes cannot be pinned")
    tracked = set(_git(root, "ls-files", "-z").split("\0"))
    tracked.discard("")
    return root, tracked


def _filtered_paths(checkout: Path) -> list[str]:
    """Tracked paths whose committed attributes name a filter; check-attr runs no filter."""
    try:
        listed = subprocess.run(["git", "-c", "core.fsmonitor=false", "ls-files", "-z"], cwd=checkout, text=True,
                                capture_output=True, timeout=60, check=False)
        proc = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", "check-attr", "-z", "--stdin", "filter"], cwd=checkout, input=listed.stdout,
            text=True, capture_output=True, timeout=60, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError(f"Git attribute inspection unavailable: {exc}") from exc
    if listed.returncode or proc.returncode:
        raise ValueError(f"Git attribute inspection failed: {(listed.stderr or proc.stderr).strip()}")
    fields = proc.stdout.split("\0")
    return [fields[i] for i in range(0, len(fields) - 2, 3)
            if fields[i + 2] not in ("unspecified", "unset")]


@contextmanager
def temporary_commit_checkout(repo_root: str | Path, target_ref: str) -> Iterator[Path]:
    """Yield a clean detached worktree of target_ref outside repo_root, then remove it.

    The worktree shares the repository's object store, so any local commit can be
    indexed while the active checkout is dirty or at another revision. Only the
    committed tree is checked out; the active working tree is never read. The
    checkout step disables hooks, the filesystem monitor and configured external
    clean/smudge/process filters; the clean-source checks that follow run as in an
    ordinary build. A commit whose attributes assign a filter to a tracked path is
    refused, because its unfiltered bytes would differ from an ordinary checkout.
    """
    if not re.fullmatch(r"[0-9a-f]{40}", target_ref):
        raise ValueError("target_ref must be a full 40-character Git SHA")
    root = Path(repo_root).resolve()
    if Path(_git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise ValueError("repo_root must be the exact Git checkout root")
    disabled = [part for name in _configured_external_filters(root) for part in ("-c", f"{name}=")]
    try:
        _git(root, "cat-file", "-e", f"{target_ref}^{{commit}}")
    except ValueError as exc:
        raise ValueError("target_ref is not a local commit; a shallow clone may need more history") from exc
    parent = Path(tempfile.mkdtemp(prefix="sensemaking-index-")).resolve()
    if parent.is_relative_to(root):
        shutil.rmtree(parent, ignore_errors=True)
        raise ValueError("temporary checkout would fall inside the repository checkout")
    no_hooks = parent / "no-hooks"
    no_hooks.mkdir()
    checkout = parent / "checkout"
    try:
        _git(root, "-c", f"core.hooksPath={no_hooks}", "-c", "core.fsmonitor=false", *disabled,
             "worktree", "add", "--quiet", "--detach", str(checkout), target_ref, timeout=300)
        if _filtered_paths(checkout):
            raise ValueError("temporary checkout refused: target_ref assigns Git filters to tracked paths")
        yield checkout
    finally:
        # Remove only this worktree; a repository-wide prune could drop other
        # worktrees' entries. An interrupted run leaves an entry Git lists as prunable.
        try:
            _git(root, "worktree", "remove", "--force", str(checkout))
        except ValueError:
            pass
        shutil.rmtree(parent, ignore_errors=True)


def _source(root: Path, tracked: set[str], relative: str) -> Path:
    if relative not in tracked:
        raise ValueError(f"source not tracked at target Git revision: {relative}")
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"source escaped repository root: {relative}") from exc
    if not candidate.is_file():
        raise ValueError(f"source missing: {relative}")
    part = root
    for name in Path(relative).parts:
        part = part / name
        if part.is_symlink():
            raise ValueError(f"symlink source refused: {relative}")
    return candidate


def _local_evidence_path(reference: str) -> str | None:
    if not reference.startswith("file:"):
        return None
    path = reference[5:].split("#", 1)[0]
    return re.sub(r":line:\d+$", "", path)
