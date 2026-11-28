"""Rehearse an explicit bounded source patch against committed product knowledge.

This composition applies only existing regular-file text modifications in a
disposable exact-commit checkout. It uses the existing BASE-only worktree
review; patched bytes are not indexed as knowledge or executed.
"""
from __future__ import annotations

import ast
import hashlib
import os
import subprocess
from pathlib import Path
from typing import Any

from .semantic_architecture.knowledge_architecture import is_repository_file_path
from .semantic_architecture.knowledge_sources import (
    _source, temporary_commit_checkout, verified_tracked_sources,
)
from .semantic_architecture.worktree_context import (
    _configured_external_filters, changed_paths_since_indexed_ref,
    guarded_git_text,
)
from .workspace_knowledge import (
    _checkout_root, _repository_label, _resolve_commit, _validate_ref_text,
    run_workspace_review_context,
)

_MAX_PATCH_BYTES = 256 * 1024
_MAX_FILES = 8
_LIMITS = (
    "Only explicit UTF-8 text patches to existing tracked regular files (at most 8 files and 256 KiB) are supported.",
    "Additions, deletions, renames, copies, binary patches, mode changes, symlinks, Git control files and submodules are refused.",
    "Git application and Python syntax parsing are mechanical observations, not runtime behavior or semantic correctness.",
    "Definition changes compare exact top-level source spans by unique name; duplicate names and unavailable spans are NOT ASSESSED.",
    "Review uses committed BASE knowledge and observed patch-overlay path names only. Patched bytes are not indexed as product intent.",
    "The temporary worktree and derived cache are disposable, not a security sandbox. No target code or tests are executed.",
    "No change is applied to the active checkout and no decision, action or publication is authorized.",
)


def _apply_git(root: Path, patch: bytes, *args: str) -> bytes:
    """Run only the selected Git apply operation, without hooks or filters."""
    disabled = _configured_external_filters(root)
    overrides = [part for key in disabled for part in ("-c", f"{key}=")]
    try:
        result = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", "-c", f"core.hooksPath={os.devnull}",
             "-c", "apply.ignoreWhitespace=no", *overrides,
             "-C", str(root), "apply", "--whitespace=nowarn", *args, "-"],
            input=patch, capture_output=True, timeout=120, check=False,
            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0"},
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError(f"patch rehearsal Git application unavailable: {exc}") from exc
    if result.returncode:
        detail = result.stderr.decode("utf-8", "replace").strip()[:500]
        raise ValueError(f"patch rehearsal refused: git apply failed: {detail}")
    return result.stdout


def _patch_paths(root: Path, patch: bytes, tracked: set[str], sha: str) -> list[str]:
    if _apply_git(root, patch, "--summary").strip():
        raise ValueError("patch rehearsal supports text modifications only, not structural changes")
    raw = _apply_git(root, patch, "--numstat", "-z")
    paths: list[str] = []
    for entry in raw.split(b"\0"):
        if not entry:
            continue
        fields = entry.split(b"\t", 2)
        if len(fields) != 3 or not all(value.isdigit() for value in fields[:2]):
            raise ValueError("patch rehearsal refuses binary or ambiguous file changes")
        path = fields[2].decode("utf-8")
        if (not is_repository_file_path(path) or path not in tracked
                or "\\" in path or ":" in path
                or any(ord(c) < 32 or ord(c) == 127 for c in path)
                or any(part.casefold() in {".git", ".gitattributes", ".gitmodules"}
                       for part in path.split("/"))):
            raise ValueError("patch rehearsal requires contained existing tracked non-control files")
        _source(root, tracked, path)
        paths.append(path)
    if not 1 <= len(paths) <= _MAX_FILES or len(set(paths)) != len(paths):
        raise ValueError("patch rehearsal requires 1..8 distinct modified files")
    tree = guarded_git_text(root, "--literal-pathspecs", "ls-tree", "-r", "-z",
                            sha, "--", *paths)
    regular = set()
    for entry in tree.split("\0"):
        if not entry:
            continue
        header, separator, path = entry.partition("\t")
        if not separator or header.split(" ", 1)[0] not in {"100644", "100755"}:
            raise ValueError("patch rehearsal refuses non-regular Git tree entries")
        regular.add(path)
    if regular != set(paths):
        raise ValueError("patch rehearsal could not establish the complete regular-file scope")
    return sorted(paths)


def _read_patch(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ValueError("patch input must be a regular file")
    with path.open("rb") as stream:
        patch = stream.read(_MAX_PATCH_BYTES + 1)
    if not patch or len(patch) > _MAX_PATCH_BYTES or b"\0" in patch:
        raise ValueError("patch input must be nonempty UTF-8 text of at most 256 KiB")
    patch.decode("utf-8")
    return patch


_DEFINITION_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


def _definition_source(raw: bytes, tree: ast.Module) -> tuple[dict[str, dict[str, Any]], list[Any]]:
    """Inventory top-level definitions by unique name and preserve residual source."""
    lines = raw.splitlines(keepends=True)
    definitions: dict[str, dict[str, Any]] = {}
    residual: list[Any] = []
    cursor = 0
    for node in tree.body:
        if not isinstance(node, _DEFINITION_TYPES):
            continue
        if node.name in definitions:
            raise ValueError("duplicate top-level definition name")
        start = min([node.lineno, *(d.lineno for d in node.decorator_list)]) - 1
        end = node.end_lineno
        if end is None or not cursor <= start < end <= len(lines):
            raise ValueError("definition source span unavailable")
        residual.extend([b"".join(lines[cursor:start]), ("definition", node.name)])
        cursor = end
        definitions[node.name] = {
            "kind": type(node).__name__, "line": start + 1, "end_line": end,
            "source_sha256": hashlib.sha256(b"".join(lines[start:end])).hexdigest(),
        }
    residual.append(b"".join(lines[cursor:]))
    return definitions, residual


def _definition_changes(before: bytes, after: bytes, limit: int) -> dict[str, Any]:
    """Compare unique top-level definitions in the actual disposable overlay."""
    try:
        left_tree, right_tree = ast.parse(before), ast.parse(after)
        left, left_residual = _definition_source(before, left_tree)
        right, right_residual = _definition_source(after, right_tree)
    except (SyntaxError, ValueError, RecursionError) as exc:
        return {"status": "NOT_ASSESSED", "reason": str(exc)[:240],
                "changes": [], "change_total": None, "truncated": False}
    rows = []
    for name in sorted(left.keys() | right.keys()):
        old, new = left.get(name), right.get(name)
        if old is None:
            change = "ADDED"
        elif new is None:
            change = "REMOVED"
        elif old["source_sha256"] != new["source_sha256"]:
            change = "SOURCE_CHANGED"
        else:
            continue
        rows.append({"name": name, "change": change, "before": old, "after": new})
    return {
        "status": "COMPARED_TOP_LEVEL_DEFINITIONS",
        "comparison_basis": "EXACT_DEFINITION_SOURCE",
        "changes": rows[:limit], "change_total": len(rows),
        "truncated": len(rows) > limit,
        "module_context_source_changed": left_residual != right_residual,
        "runtime_behavior_assessed": False,
    }


def rehearse_patch(
    *, repo: str | Path, ref: str, patch_file: str | Path, limit: int = 25,
) -> dict[str, Any]:
    """Apply a bounded candidate patch and compose existing BASE review evidence."""
    if not 1 <= limit <= 100:
        raise ValueError("patch rehearsal requires limit 1..100")
    _validate_ref_text(ref)
    root = _checkout_root(Path(repo).expanduser().resolve())
    sha = _resolve_commit(root, ref)
    label, label_source = _repository_label(root, None)
    patch = _read_patch(Path(patch_file).expanduser())
    with temporary_commit_checkout(root, sha) as checkout:
        checkout, tracked = verified_tracked_sources(checkout, sha)
        paths = _patch_paths(checkout, patch, tracked, sha)
        before = {path: _source(checkout, tracked, path).read_bytes() for path in paths}
        _apply_git(checkout, patch, "--check")
        _apply_git(checkout, patch)
        changes = changed_paths_since_indexed_ref(checkout, sha)
        if (changes["paths"] != frozenset(paths) or changes["staged"]
                or changes["untracked"]
                or guarded_git_text(checkout, "diff", "--no-ext-diff",
                                    "--no-textconv", "--no-renames", "--summary", sha)):
            raise ValueError("rehearsed patch changed paths or file modes outside the declared scope")
        files = []
        for path in paths:
            raw = _source(checkout, tracked, path).read_bytes()
            item: dict[str, Any] = {
                "path": path, "before_sha256": hashlib.sha256(before[path]).hexdigest(),
                "after_sha256": hashlib.sha256(raw).hexdigest(),
                "python_syntax": "NOT_ASSESSED",
            }
            if item["after_sha256"] == item["before_sha256"]:
                raise ValueError(f"rehearsed file has no byte change: {path}")
            if path.endswith(".py"):
                try:
                    ast.parse(raw, filename=path)
                except (SyntaxError, ValueError) as exc:
                    item["python_syntax"] = "FAIL"
                    item["syntax_error_line"] = getattr(exc, "lineno", None)
                else:
                    item["python_syntax"] = "PASS"
                item["definition_changes"] = _definition_changes(before[path], raw, limit)
            files.append(item)
        review = run_workspace_review_context(
            repo=checkout, base_ref=sha, ref=sha, repository=label,
            index_dir=checkout.parent / "rehearsal-index", limit=limit,
            max_paths=len(paths), include_worktree=True, include_candidates=True,
        )
        if (review["base_ref"] != sha or review["target_ref"] != sha
                or set(review["review_scope"]["selected_paths"]) != set(paths)
                or review["review_scope"]["working_changes_indexed"]
                or review["review_scope"]["worktree_changed_paths_total"] != len(paths)):
            raise ValueError("rehearsal review did not preserve the verified patch scope and BASE")
        review["workspace_index"]["cache_lifetime"] = "DISPOSABLE_REHEARSAL"
        review["workspace_index"]["index_path"] = None
        review["workspace_index"]["repository_identity_source"] = label_source
        return {
            "code": "SEMANTIC_PATCH_REHEARSAL",
            "base_ref": sha, "repository": label,
            "patch_sha256": hashlib.sha256(patch).hexdigest(),
            "patch_bytes": len(patch), "files": files,
            "status": "REHEARSED",
            "application": {"git_apply_check": "PASS", "git_apply": "PASS",
                            "changed_paths_verified": True},
            "review_basis": "DISPOSABLE_PATCH_OVERLAY_BASE_KNOWLEDGE",
            "review": review,
            "active_checkout_patch_applied": False,
            "target_code_executed": False, "tests_executed": False,
            "patched_bytes_indexed": False, "semantic_truth_established": False,
            "action_authorized": False, "explicit_limits": list(_LIMITS),
        }
