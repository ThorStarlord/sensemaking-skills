"""Zero-setup workspace query over a derived index of one committed Git revision.

This is a front door over the existing knowledge build and query operations. It
indexes only committed bytes, keeps the rebuildable SQLite cache outside every
checkout, and never writes to the working tree, refs, index or configuration.
The cache is derived convenience, never authority.
"""

from __future__ import annotations

import hashlib
import os
import re
import sqlite3
import subprocess
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from .semantic_architecture.knowledge import KnowledgeSnapshot
from .semantic_architecture.knowledge_sources import (
    build_knowledge_snapshot, temporary_commit_checkout, verified_tracked_sources,
)
from .semantic_architecture.knowledge_store import query_context_paths, query_knowledge, store_snapshot
from .semantic_architecture.repository_bootstrap import orient_repository
from .semantic_architecture.worktree_context import changed_paths_since_indexed_ref, inspect_worktree_context

OPERATIONS = (
    "context-for", "rules-for", "search", "explain", "why", "impact", "term", "orientation-summary",
    "contradictions", "snapshot", "workspace-impact", "changes", "history",
)
_REFUSED_OPERATIONS = {
    "changes": "changes compares two committed revisions; run 'semantic workspace-changes --base-ref REV "
               "--ref REV' (no prepared database), or run knowledge-build for each revision with an explicit "
               "--db, then knowledge-query with that --db",
    "history": "history needs several indexed revisions in one database; run knowledge-build for each "
               "revision with an explicit --db, then knowledge-query with that --db",
}
_WORKSPACE_OPERATIONS = frozenset({"context-for", "workspace-impact"})
_MAX_PATHS = 8
_KEEP_SNAPSHOTS = 8
_GIT_TIMEOUT = 60
_SHA = re.compile(r"[0-9a-f]{40}")
_SNAPSHOT_FILE = re.compile(r"[0-9a-f]{40}\.sqlite")
_DRIVE = re.compile(r"[A-Za-z]:(?:[\\/]|$)")


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_OPTIONAL_LOCKS": "0"}
    try:
        return subprocess.run(
            ["git", "-c", "core.fsmonitor=false", *args], cwd=str(cwd), env=env,
            stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=_GIT_TIMEOUT, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError("Git is unavailable or did not respond in time") from exc


def _git_text(cwd: Path, *args: str, message: str) -> str:
    proc = _git(cwd, *args)
    if proc.returncode:
        raise ValueError(message)
    return proc.stdout.strip()


def _checkout_root(repo: Path) -> Path:
    top = _git_text(repo, "rev-parse", "--show-toplevel",
                    message=f"not inside a Git working tree: {repo}")
    return Path(top).resolve()


def _validate_ref_text(ref: str) -> None:
    if not ref or ref.startswith("-") or any(ch.isspace() or ord(ch) < 32 or ord(ch) == 127 for ch in ref):
        raise ValueError("--ref must be a non-empty revision without a leading '-', whitespace or control characters")


def _resolve_commit(root: Path, ref: str) -> str:
    proc = _git(root, "rev-parse", "--verify", "--quiet", "--end-of-options", f"{ref}^{{commit}}")
    sha = proc.stdout.strip()
    if proc.returncode or not _SHA.fullmatch(sha):
        raise ValueError(f"--ref {ascii(ref)} does not resolve to a commit in this repository")
    return sha


def _remote_path(url: str) -> str:
    if _DRIVE.match(url):
        return url
    if "://" in url:
        return urlsplit(url).path
    head, sep, rest = url.partition(":")
    if sep and "/" not in head and "\\" not in head:
        return rest
    return url


def _origin_label(root: Path) -> str | None:
    proc = _git(root, "config", "--get", "remote.origin.url")
    if proc.returncode == 1:
        return None
    if proc.returncode:
        raise ValueError("cannot read Git remote configuration")
    url = proc.stdout.strip()
    if not url:
        return None
    try:
        path = _remote_path(url)
    except ValueError:
        return None
    segments = [part for part in re.split(r"[\\/]", path) if part]
    if segments and segments[-1].endswith(".git"):
        stem = segments[-1][:-4]
        if stem:
            segments[-1] = stem
        else:
            segments.pop()
    kept = segments[-2:]
    if any("@" in part or ":" in part for part in kept):
        return None
    label = "/".join(kept)
    return label if 1 <= len(label) <= 255 else None


def _repository_label(root: Path, explicit: str | None) -> tuple[str, str]:
    if explicit is not None:
        label = explicit.strip()
        if not 1 <= len(label) <= 255:
            raise ValueError("--repository must be 1..255 characters")
        return label, "explicit"
    label = _origin_label(root)
    if label is not None:
        return label, "origin_remote"
    if not 1 <= len(root.name) <= 255:
        raise ValueError("cannot derive a repository label from the checkout; pass --repository")
    return root.name, "local_path"


def _default_index_dir() -> Path:
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA")
        cache_root = Path(base) if base else Path.home() / "AppData" / "Local"
    else:
        xdg = os.environ.get("XDG_CACHE_HOME", "")
        cache_root = Path(xdg) if xdg and os.path.isabs(xdg) else Path.home() / ".cache"
    return cache_root / "sensemaking-skills" / "index"


def _clone_key(root: Path) -> str:
    common = _git_text(root, "rev-parse", "--git-common-dir",
                       message="cannot locate the Git common directory")
    path = Path(common)
    if not path.is_absolute():
        path = root / path
    normalized = os.path.normcase(str(path.resolve()))
    return hashlib.sha256(normalized.encode("utf-8", "surrogateescape")).hexdigest()[:16]


def _cache_paths(root: Path, index_dir: str | Path | None, sha: str) -> tuple[Path, Path]:
    base = Path(index_dir).expanduser().resolve() if index_dir is not None else _default_index_dir().resolve()
    if base.is_relative_to(root):
        raise ValueError("index directory must be outside the Git checkout")
    clone_dir = base / _clone_key(root)
    database = clone_dir / f"{sha}.sqlite"
    for candidate in (clone_dir, database):
        # resolve() differs from the constructed path for a symlink or a Windows junction.
        if candidate.is_symlink() or (
            os.path.normcase(str(candidate.resolve())) != os.path.normcase(str(candidate))
        ):
            raise ValueError(f"refusing linked index path (symlink or junction): {candidate}")
    return clone_dir, database


def _ensure_directory(path: Path) -> None:
    os.makedirs(path, mode=0o700, exist_ok=True)


def _snapshot_for(root: Path, sha: str, label: str) -> tuple[KnowledgeSnapshot, str]:
    # Preserve the fast clean-HEAD path without running configured Git
    # clean/process filters during the dirtiness decision.
    context = inspect_worktree_context(root, sha)
    if context["head_matches_indexed_ref"] and context["worktree_clean"]:
        return build_knowledge_snapshot(root, repository=label, target_ref=sha), "active_checkout"
    with temporary_commit_checkout(root, sha) as checkout:
        snapshot = build_knowledge_snapshot(checkout, repository=label, target_ref=sha)
    return snapshot, "temporary_worktree"


def _prune(clone_dir: Path, keep: Path) -> None:
    candidates: list[tuple[float, str]] = []
    try:
        with os.scandir(clone_dir) as entries:
            for entry in entries:
                if not _SNAPSHOT_FILE.fullmatch(entry.name) or entry.is_symlink():
                    continue
                try:
                    candidates.append((entry.stat(follow_symlinks=False).st_mtime, entry.name))
                except OSError:
                    continue
    except OSError:
        return
    newest = {name for _, name in sorted(candidates, reverse=True)[:_KEEP_SNAPSHOTS]}
    newest.add(keep.name)
    for _, name in candidates:
        if name in newest:
            continue
        try:
            os.remove(clone_dir / name)
        except OSError:
            pass


def _ensure_snapshot(
    root: Path, sha: str, label: str, clone_dir: Path, database: Path, refresh: bool,
) -> tuple[str, str | None]:
    if refresh and database.exists():
        database.unlink()
    existed = database.exists()
    if existed:
        try:
            query_knowledge(database, repository=label, target_ref=sha, operation="snapshot", limit=1)
        except (ValueError, sqlite3.Error):
            pass
        else:
            try:
                os.utime(database, None)
            except OSError:
                pass
            return "reused", None
    _ensure_directory(clone_dir.parent)
    _ensure_directory(clone_dir)
    snapshot, source = _snapshot_for(root, sha, label)
    try:
        store_snapshot(database, snapshot, source_root=root)
    except ValueError as exc:
        if existed:
            raise ValueError(
                f"cannot store into existing cache file {database}: {exc}; retry with --refresh"
            ) from exc
        raise
    _prune(clone_dir, database)
    return "built", source


def _normalize_path(text: str) -> str:
    value = text.replace("\\", "/")
    if value.startswith("./"):
        value = value[2:]
    return value


def run_workspace_orient(
    *, repo: str | Path, ref: str = "HEAD", repository: str | None = None,
    max_files: int = 5000, sample_limit: int = 16,
) -> dict[str, Any]:
    """Orient a checkout from committed paths without a prepared knowledge index.

    Reuse bounded source-pinned orientation, resolving Git identity and using
    a safe detached checkout when the active workspace is dirty or off-ref.
    """
    if not 1 <= max_files <= 20000:
        raise ValueError("max_files must be 1..20000")
    if not 1 <= sample_limit <= 50:
        raise ValueError("sample_limit must be 1..50")
    _validate_ref_text(ref)
    repo_dir = Path(repo).expanduser().resolve()
    if not repo_dir.is_dir():
        raise ValueError(f"repository directory not found: {repo_dir}")
    root = _checkout_root(repo_dir)
    sha = _resolve_commit(root, ref)
    label, label_source = _repository_label(root, repository)
    context = inspect_worktree_context(root, sha)

    if context["head_matches_indexed_ref"] and context["worktree_clean"]:
        source_root, tracked = verified_tracked_sources(root, sha)
        payload = orient_repository(
            source_root, tracked, repository=label, target_ref=sha,
            max_files=max_files, sample_limit=sample_limit,
        )
        source_checkout = "active_checkout"
    else:
        with temporary_commit_checkout(root, sha) as checkout:
            source_root, tracked = verified_tracked_sources(checkout, sha)
            payload = orient_repository(
                source_root, tracked, repository=label, target_ref=sha,
                max_files=max_files, sample_limit=sample_limit,
            )
        source_checkout = "temporary_worktree"

    payload["source_checkout"] = source_checkout
    payload["workspace_context"] = context
    payload["repository_identity_source"] = label_source
    payload["repository_label_verified"] = False
    payload["working_changes_read"] = False
    payload["code"] = "SEMANTIC_REPOSITORY_ORIENTATION"
    return payload


def run_workspace_query(
    *, repo: str | Path, ref: str, operation: str,
    paths: tuple[str, ...] = (), subject: str | None = None,
    search_terms: tuple[str, ...] = (), expected_kinds: tuple[str, ...] = (),
    limit: int = 50, depth: int = 2, repository: str | None = None,
    index_dir: str | Path | None = None, refresh: bool = False,
) -> dict[str, Any]:
    """Build or reuse a derived index of one committed revision and run one read operation."""
    if operation in _REFUSED_OPERATIONS:
        raise ValueError(_REFUSED_OPERATIONS[operation])
    if operation not in OPERATIONS:
        raise ValueError(f"unsupported workspace query operation: {operation}")
    if operation == "context-for":
        if paths and subject is not None:
            raise ValueError("pass positional PATHS or --subject for context-for, not both")
        if not paths and subject is None:
            raise ValueError("context-for requires positional PATHS or --subject <repository-relative file path>")
        query_paths = tuple(_normalize_path(item) for item in (paths or (subject,)))
        if len(query_paths) > _MAX_PATHS:
            raise ValueError("context-for accepts 1..8 repository-relative paths")
    else:
        if paths:
            raise ValueError("positional PATHS are supported only for context-for")
        query_paths = ()
        if operation == "rules-for" and subject is not None:
            subject = _normalize_path(subject)
    _validate_ref_text(ref)
    repo_dir = Path(repo).expanduser().resolve()
    if not repo_dir.is_dir():
        raise ValueError(f"repository directory not found: {repo_dir}")
    root = _checkout_root(repo_dir)
    sha = _resolve_commit(root, ref)
    label, label_source = _repository_label(root, repository)
    clone_dir, database = _cache_paths(root, index_dir, sha)
    state, build_source = _ensure_snapshot(root, sha, label, clone_dir, database, refresh)

    changed = changed_paths_since_indexed_ref(root, sha)["paths"] if operation in _WORKSPACE_OPERATIONS else None
    try:
        if len(query_paths) >= 2:
            payload = query_context_paths(
                database, repository=label, target_ref=sha, paths=query_paths, limit=limit, depth=depth,
                search_terms=search_terms, expected_kinds=expected_kinds, workspace_changed_paths=changed,
            )
        else:
            payload = query_knowledge(
                database, repository=label, target_ref=sha, operation=operation,
                subject=query_paths[0] if operation == "context-for" else subject,
                limit=limit, depth=depth, search_terms=search_terms, expected_kinds=expected_kinds,
                workspace_changed_paths=changed,
            )
    except sqlite3.Error as exc:
        raise ValueError(f"cannot read cache file {database}: {exc}; retry with --refresh") from exc
    payload["workspace_context"] = inspect_worktree_context(root, sha)
    payload["code"] = "SEMANTIC_KNOWLEDGE_QUERY"
    payload["workspace_index"] = {
        "indexed_ref": sha,
        "ref_requested": ref,
        "repository": label,
        "repository_identity_source": label_source,
        "repository_label_verified": False,
        "index_path": str(database),
        "index_state": state,
        "build_source": build_source,
        "equivalent_operations": ["build", operation] if state == "built" else [operation],
    }
    return payload

def run_workspace_changes(
    *, repo: str | Path, base_ref: str, ref: str = "HEAD",
    repository: str | None = None, index_dir: str | Path | None = None,
    refresh: bool = False, limit: int = 50,
) -> dict[str, Any]:
    """Compare two committed semantic snapshots without manual multi-revision setup.

    Each revision uses the existing per-commit derived cache. Querying the base
    through a second read-only index preserves the established changes/delta
    classifier without a new schema or a mutable combined history database.
    """
    if not 1 <= limit <= 250:
        raise ValueError("changes limit must be 1..250")
    _validate_ref_text(base_ref)
    _validate_ref_text(ref)
    repo_dir = Path(repo).expanduser().resolve()
    if not repo_dir.is_dir():
        raise ValueError(f"repository directory not found: {repo_dir}")
    root = _checkout_root(repo_dir)
    base_sha = _resolve_commit(root, base_ref)
    sha = _resolve_commit(root, ref)
    label, label_source = _repository_label(root, repository)

    base_dir, base_db = _cache_paths(root, index_dir, base_sha)
    clone_dir, database = _cache_paths(root, index_dir, sha)
    base_state, base_source = _ensure_snapshot(
        root, base_sha, label, base_dir, base_db, refresh,
    )
    if base_sha == sha:
        state, build_source = base_state, base_source
    else:
        state, build_source = _ensure_snapshot(
            root, sha, label, clone_dir, database, refresh,
        )

    try:
        payload = query_knowledge(
            database, repository=label, target_ref=sha, operation="changes",
            base_ref=base_sha, base_db_path=base_db if base_sha != sha else None,
            limit=limit,
        )
    except sqlite3.Error as exc:
        raise ValueError(
            f"cannot read cached revision indexes; retry with --refresh: {exc}"
        ) from exc

    payload["code"] = "SEMANTIC_KNOWLEDGE_QUERY"
    payload["workspace_context"] = inspect_worktree_context(root, sha)
    payload["workspace_comparison"] = {
        "base_ref": base_sha,
        "base_ref_requested": base_ref,
        "target_ref": sha,
        "target_ref_requested": ref,
        "git_ancestry_assessed": False,
        "working_changes_read": False,
        "semantic_change_inferred": False,
        "note": (
            "Differences between two exact committed knowledge snapshots; "
            "not proof of Git ancestry, semantic impact or decision validity."
        ),
    }
    payload["workspace_index"] = {
        "indexed_ref": sha,
        "ref_requested": ref,
        "repository": label,
        "repository_identity_source": label_source,
        "repository_label_verified": False,
        "index_path": str(database),
        "index_state": state,
        "build_source": build_source,
        "equivalent_operations": ["build", "changes"] if state == "built" else ["changes"],
    }
    payload["workspace_base_index"] = {
        "indexed_ref": base_sha,
        "ref_requested": base_ref,
        "repository": label,
        "repository_identity_source": label_source,
        "repository_label_verified": False,
        "index_path": str(base_db),
        "index_state": base_state,
        "build_source": base_source,
    }
    return payload
