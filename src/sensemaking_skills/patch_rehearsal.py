"""Rehearse an explicit bounded source patch against committed product knowledge.

This composition applies bounded regular-file text modifications in a
disposable exact-commit checkout. Explicit source/knowledge co-design admits
new files and one proposed pack, without indexing or executing patched bytes.
An explicit existing-pack update uses only an unstaged modification overlay.
"""
from __future__ import annotations

import ast
import hashlib
import os
import subprocess
from pathlib import Path
from typing import Any

from .semantic_architecture.knowledge_architecture import is_repository_file_path
from .semantic_architecture.source_access import (
    _local_evidence_path, _source, committed_regular_file_status,
    temporary_commit_checkout, verified_tracked_sources,
)
from .semantic_architecture.stewardship_validation import inspect_knowledge_proposal
from .semantic_architecture.worktree_context import (
    _configured_external_filters, changed_paths_since_indexed_ref,
    guarded_git_text,
)
from .workspace_knowledge import (
    _checkout_root, _repository_label, _resolve_commit, _validate_ref_text,
    run_workspace_query, run_workspace_review_context,
)

_MAX_PATCH_BYTES = 256 * 1024
_MAX_FILES = 8
_LIMITS = (
    "Only explicit UTF-8 text patches to existing tracked regular files (at most 8 files and 256 KiB) are supported.",
    "Additions, deletions, renames, copies, binary patches, mode changes, symlinks, Git control files and submodules are refused.",
    "Git application and Python syntax parsing are mechanical observations, not runtime behavior or semantic correctness.",
    "Definition comparison distinguishes AST and source-only changes, reports module-level AST/text differences, and does not infer runtime effects; duplicate names are NOT ASSESSED.",
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


def _new_file_path(root: Path, path: str) -> None:
    """Admit only absent files in existing contained, non-linked directories."""
    candidate = root / path
    if candidate.exists() or candidate.is_symlink():
        raise ValueError("new candidate path already exists")
    if not candidate.resolve().is_relative_to(root):
        raise ValueError("new candidate path escapes checkout")
    parent = root
    for part in path.split("/")[:-1]:
        parent /= part
        if parent.is_symlink() or not parent.is_dir():
            raise ValueError("new candidate file requires an existing non-linked directory")


def _check_candidate_filters(root: Path, paths: list[str]) -> None:
    # The clean BASE guard covers tracked paths. New paths can match a
    # previously unused attribute pattern. Refuse any assigned filter before
    # application or the single-pack steward's worktree inspection.
    raw = guarded_git_text(root, "check-attr", "-z", "filter", "--", *paths)
    fields = raw.split("\0")
    if not fields or fields[-1] != "" or len(fields) != 3 * len(paths) + 1:
        raise ValueError("cannot establish candidate filter scope")
    rows = [tuple(fields[i:i + 3]) for i in range(0, len(fields) - 1, 3)]
    if ({row[0] for row in rows} != set(paths)
            or any(attribute != "filter" or value not in {"unspecified", "unset"}
                   for _, attribute, value in rows)):
        raise ValueError("candidate filter assignment or unavailable attribute inspection")


def _patch_paths(
    root: Path, patch: bytes, tracked: set[str], sha: str, *,
    knowledge_proposal: str | None = None,
) -> tuple[list[str], set[str]]:
    summary = _apply_git(root, patch, "--summary").decode("utf-8").splitlines()
    if summary and (knowledge_proposal is None or any(
        not line.lstrip().startswith("create mode 100644 ") for line in summary
    )):
        raise ValueError("patch rehearsal supports text modifications only, not structural changes")
    raw = _apply_git(root, patch, "--numstat", "-z")
    paths: list[str] = []
    added: set[str] = set()
    for entry in raw.split(b"\0"):
        if not entry:
            continue
        fields = entry.split(b"\t", 2)
        if len(fields) != 3 or not all(value.isdigit() for value in fields[:2]):
            raise ValueError("patch rehearsal refuses binary or ambiguous file changes")
        path = fields[2].decode("utf-8")
        if (not is_repository_file_path(path)
                or "\\" in path or ":" in path
                or any(ord(c) < 32 or ord(c) == 127 for c in path)
                or any(part.casefold() in {".git", ".gitattributes", ".gitmodules"}
                       for part in path.split("/"))):
            raise ValueError("patch rehearsal requires contained existing tracked non-control files")
        if path in tracked:
            _source(root, tracked, path)
        elif knowledge_proposal is not None:
            _new_file_path(root, path)
            added.add(path)
        else:
            raise ValueError("patch rehearsal requires contained existing tracked non-control files")
        paths.append(path)
    if not 1 <= len(paths) <= _MAX_FILES or len(set(paths)) != len(paths):
        raise ValueError("patch rehearsal requires 1..8 distinct changed files")
    if len(summary) != len(added):
        raise ValueError("patch rehearsal could not reconcile new-file scope")
    if knowledge_proposal is not None:
        pack_paths = {path for path in paths
                      if path.casefold().startswith(".sensemaking/knowledge/")}
        if pack_paths != {knowledge_proposal} or knowledge_proposal not in added:
            raise ValueError("co-design requires exactly one new explicit knowledge pack")
        _check_candidate_filters(root, paths)
    existing = [path for path in paths if path not in added]
    tree = (guarded_git_text(root, "--literal-pathspecs", "ls-tree", "-r", "-z",
                             sha, "--", *existing) if existing else "")
    regular = set()
    for entry in tree.split("\0"):
        if not entry:
            continue
        header, separator, path = entry.partition("\t")
        if not separator or header.split(" ", 1)[0] not in {"100644", "100755"}:
            raise ValueError("patch rehearsal refuses non-regular Git tree entries")
        regular.add(path)
    if regular != set(existing):
        raise ValueError("patch rehearsal could not establish the complete regular-file scope")
    return sorted(paths), added


def _verify_staged_scope(root: Path, sha: str, paths: list[str], added: set[str]) -> None:
    """Confirm the actual disposable-index delta contains only allowed modes."""
    raw = guarded_git_text(
        root, "diff", "--cached", "--raw", "--no-abbrev", "--no-renames",
        "--no-ext-diff", "--no-textconv", "-z", sha, "--",
    )
    fields = raw.split("\0")
    if fields[-1] != "" or (len(fields) - 1) % 2:
        raise ValueError("cannot establish actual staged patch scope")
    seen = set()
    for i in range(0, len(fields) - 1, 2):
        metadata, path = fields[i:i + 2]
        parts = metadata.removeprefix(":").split()
        if len(parts) != 5 or path in seen:
            raise ValueError("ambiguous staged patch scope")
        old_mode, new_mode, _, _, status = parts
        if path in added:
            valid = (old_mode, new_mode, status) == ("000000", "100644", "A")
        else:
            valid = old_mode == new_mode and old_mode in {"100644", "100755"} and status == "M"
        if not valid:
            raise ValueError("unsupported staged patch change or file mode")
        seen.add(path)
    if seen != set(paths):
        raise ValueError("actual staged patch paths differ from declared scope")


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
            "ast_sha256": hashlib.sha256(ast.dump(node, include_attributes=False).encode("utf-8")).hexdigest(),
        }
    residual.append(b"".join(lines[cursor:]))
    return definitions, residual


def _module_structure(tree: ast.Module) -> list[tuple[str, str]]:
    """Compare non-definition AST plus definition order, not runtime semantics."""
    return [
        ("definition", node.name) if isinstance(node, _DEFINITION_TYPES)
        else ("statement", ast.dump(node, include_attributes=False))
        for node in tree.body
    ]


def _definition_changes(before: bytes, after: bytes, limit: int) -> dict[str, Any]:
    """Compare unique top-level definitions in the actual disposable overlay."""
    try:
        left_tree, right_tree = ast.parse(before), ast.parse(after)
        left, left_residual = _definition_source(before, left_tree)
        right, right_residual = _definition_source(after, right_tree)
        module_ast_changed = _module_structure(left_tree) != _module_structure(right_tree)
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
        elif old["ast_sha256"] != new["ast_sha256"]:
            change = "AST_CHANGED"
        elif old["source_sha256"] != new["source_sha256"]:
            change = "SOURCE_ONLY_CHANGED"
        else:
            continue
        rows.append({"name": name, "change": change, "before": old, "after": new})
    return {
        "status": "COMPARED_TOP_LEVEL_DEFINITIONS",
        "comparison_basis": "TOP_LEVEL_AST_AND_EXACT_SOURCE",
        "changes": rows[:limit], "change_total": len(rows),
        "truncated": len(rows) > limit,
        "module_context_source_changed": left_residual != right_residual,
        "module_context_ast_changed": module_ast_changed,
        "runtime_behavior_assessed": False,
    }


def _possibility_rehearsal_context(
    checkout: Path, sha: str, label: str, possibility: str,
    files: list[dict[str, Any]], limit: int, review_index_path: str,
) -> dict[str, Any]:
    """Join a selected BASE opportunity's authored context to actual patch paths."""
    query = run_workspace_query(
        repo=checkout, ref=sha, operation="possibility-ecology",
        subject=possibility, repository=label, limit=limit,
        index_dir=checkout.parent / "rehearsal-index",
    )
    ecology = query["possibility_ecology"]
    index = query["workspace_index"]
    if (query["target_ref"] != sha or query["repository"] != label
            or index["indexed_ref"] != sha or index["index_path"] != review_index_path):
        raise ValueError("possibility context did not preserve the exact BASE review index")
    if ecology["focus_kind"] != "opportunity" or ecology["focus"]["claim_id"] != possibility:
        raise ValueError("--possibility requires an existing opportunity claim at BASE")

    # Compare names only. Citations and explicit component ownership have
    # different meanings and neither establishes a necessary implementation.
    path_matches: dict[str, list[dict[str, Any]]] = {item["path"]: [] for item in files}

    def record_match(
        basis: str, record_id: str, refs: list[str], *, literal: bool = False,
    ) -> None:
        for path, matches in path_matches.items():
            matching = sorted({
                ref for ref in refs if isinstance(ref, str)
                and (ref == path if literal else _local_evidence_path(ref) == path)
            })
            if matching:
                matches.append({"basis": basis, "record_id": record_id,
                                "references": matching})

    def claim_matches(record: dict, prefix: str, basis: str, claim_id: str) -> None:
        record_match(basis + "_EVIDENCE", claim_id, record[prefix + "evidence_refs"])
        authority = record.get(prefix + "authority_ref")
        if isinstance(authority, str):
            record_match(basis + "_AUTHORITY", claim_id, [authority],
                         literal=not authority.startswith("file:"))

    focus = ecology["focus"]
    claim_matches(focus, "", "POSSIBILITY", possibility)
    for route in ecology["required_capability_routes"]:
        capability = route["capability_claim_id"]
        claim_matches(route, "capability_", "REQUIRED_CAPABILITY", capability)
        record_match("REQUIRES_RELATION_EVIDENCE", route["requires_capability_relation_id"],
                     route["requires_capability_relation_evidence_refs"])
        for component in route["implementation_components"]:
            cid = component["component_claim_id"]
            claim_matches(component, "component_", "IMPLEMENTATION_COMPONENT", cid)
            record_match("COMPONENT_OWNED_PATH", cid, component["component_owned_paths"],
                         literal=True)
            record_match("IMPLEMENTED_BY_RELATION_EVIDENCE",
                         component["implemented_by_relation_id"],
                         component["implemented_by_relation_evidence_refs"])

    path_context = []
    for item in files:
        path = item["path"]
        status = committed_regular_file_status(checkout, sha, path)
        expected = "ABSENT_FROM_TREE" if item["before_sha256"] is None else "REGULAR_FILE"
        if status != expected:
            raise ValueError("possibility context BASE tree status disagrees with verified patch scope")
        # The same component may occur along several declared requirement routes.
        # Keep unique record/basis/reference matches; the full routes remain above.
        matches = []
        for match in path_matches[path]:
            if match not in matches:
                matches.append(match)
        path_context.append({
            "path": path, "base_tree_status": status,
            "status": "AUTHORED_MATCH" if matches else "NOT_ASSESSED",
            "matches": matches,
        })
    return {
        "base_ref": sha, "possibility_id": possibility,
        "possibility_ecology": ecology, "patch_path_context": path_context,
        "review_index_reused": True, "index_state": index["index_state"],
        "truncated": bool(query["truncated"] or ecology["truncated"]),
        "coverage_complete": False, "implementation_verified": False,
        "action_authorized": False,
        "explicit_limits": [
            "Only the selected BASE opportunity and returned direct prerequisite routes are joined to actual patch paths.",
            "Matches are exact local citation/authority names or explicitly declared component owned paths, not inferred dependencies or necessary changes.",
            "Citations are not ownership. Missing links or matches are NOT_ASSESSED, not irrelevance, readiness or evidence of no dependency.",
            "BASE tree status describes the committed path, not candidate existence or behavior. Candidate bytes and proposed records are not indexed as BASE knowledge.",
            "No feasibility, adequacy, implementation, selection or authorization is established.",
        ],
    }


def rehearse_patch(
    *, repo: str | Path, ref: str, patch_file: str | Path, limit: int = 25,
    knowledge_proposal: str | None = None, possibility: str | None = None,
    knowledge_update: str | None = None,
) -> dict[str, Any]:
    """Apply a bounded candidate patch and compose existing BASE review evidence."""
    if not 1 <= limit <= 100:
        raise ValueError("patch rehearsal requires limit 1..100")
    if knowledge_proposal is not None and knowledge_update is not None:
        raise ValueError("--knowledge-proposal and --knowledge-update are mutually exclusive")
    selected_pack = knowledge_update if knowledge_update is not None else knowledge_proposal
    updating = knowledge_update is not None
    if selected_pack is not None:
        parts = selected_pack.split("/")
        if (not is_repository_file_path(selected_pack)
                or len(parts) != 3 or parts[:2] != [".sensemaking", "knowledge"]
                or not parts[2].endswith(".json")):
            if updating:
                raise ValueError("knowledge update must name one existing direct .sensemaking/knowledge/*.json pack")
            raise ValueError("knowledge proposal must name one new direct .sensemaking/knowledge/*.json pack")
    _validate_ref_text(ref)
    root = _checkout_root(Path(repo).expanduser().resolve())
    sha = _resolve_commit(root, ref)
    label, label_source = _repository_label(root, None)
    patch = _read_patch(Path(patch_file).expanduser())
    with temporary_commit_checkout(root, sha) as checkout:
        checkout, tracked = verified_tracked_sources(checkout, sha)
        paths, added = _patch_paths(
            checkout, patch, tracked, sha, knowledge_proposal=knowledge_proposal,
        )
        if updating:
            pack_paths = {path for path in paths
                          if path.casefold().startswith(".sensemaking/knowledge/")}
            if pack_paths != {selected_pack} or selected_pack not in tracked:
                raise ValueError("co-design update requires exactly one existing explicit knowledge pack")
            _check_candidate_filters(checkout, paths)
        before = {path: (None if path in added else _source(checkout, tracked, path).read_bytes())
                  for path in paths}
        # Only the disposable worktree's own index is modified in co-design.
        # Git may retain candidate blobs in the shared object store.
        apply_options = ("--index",) if knowledge_proposal is not None else ()
        _apply_git(checkout, patch, *apply_options, "--check")
        _apply_git(checkout, patch, *apply_options)
        changes = changed_paths_since_indexed_ref(checkout, sha)
        if changes["paths"] != frozenset(paths) or changes["untracked"]:
            raise ValueError("rehearsed patch changed paths outside the declared scope")
        if knowledge_proposal is not None:
            if changes["staged"] != frozenset(paths) or changes["unstaged"]:
                raise ValueError("co-design overlay differs from its verified disposable index")
            _verify_staged_scope(checkout, sha, paths, added)
            tracked = set(filter(None, guarded_git_text(checkout, "ls-files", "-z").split("\0")))
        elif changes["staged"] or guarded_git_text(
            checkout, "diff", "--no-ext-diff", "--no-textconv", "--no-renames", "--summary", sha,
        ):
            raise ValueError("rehearsed patch changed file modes or index outside the declared scope")
        files = []
        for path in paths:
            raw = _source(checkout, tracked, path).read_bytes()
            item: dict[str, Any] = {
                "path": path, "before_sha256": (
                    hashlib.sha256(before[path]).hexdigest() if before[path] is not None else None
                ),
                "after_sha256": hashlib.sha256(raw).hexdigest(),
                "python_syntax": "NOT_ASSESSED",
            }
            if selected_pack is not None:
                item["change_kind"] = "ADDED" if path in added else "MODIFIED"
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
                item["definition_changes"] = _definition_changes(before[path] or b"", raw, limit)
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
        possibility_context = (
            _possibility_rehearsal_context(
                checkout, sha, label, possibility, files, limit,
                review["workspace_index"]["index_path"],
            ) if possibility is not None else None
        )
        review["workspace_index"]["cache_lifetime"] = "DISPOSABLE_REHEARSAL"
        review["workspace_index"]["index_path"] = None
        review["workspace_index"]["repository_identity_source"] = label_source
        candidate_knowledge = None
        if selected_pack is not None:
            selected_file = next(item for item in files if item["path"] == selected_pack)
            proposal_hash = selected_file["after_sha256"]
            candidate_knowledge = {
                "proposal": selected_pack, "proposal_sha256": proposal_hash,
                **({"operation": "UPDATE_EXISTING",
                    "base_proposal_sha256": selected_file["before_sha256"]} if updating else {}),
                "status": "NOT_VALIDATED", "validation": None, "reason": None,
                "accepted": False, "action_authorized": False,
            }
            try:
                validation = inspect_knowledge_proposal(checkout, Path(selected_pack))
            except (ValueError, OSError, UnicodeError, RuntimeError, subprocess.TimeoutExpired) as exc:
                candidate_knowledge["reason"] = str(exc)[:500]
            else:
                if (validation["head_sha"] != sha or not validation["valid"]
                        or validation["other_packs_source"] != "committed_HEAD_only"
                        or validation["dirty_other_packs_ignored"]
                        or validation["staged_other_packs_ignored"]
                        or validation["action_authorized"]):
                    raise ValueError("candidate knowledge preflight did not preserve the intended scope")
                candidate_knowledge["status"] = "MECHANICALLY_VALID"
                candidate_knowledge["validation"] = validation
            if (changed_paths_since_indexed_ref(checkout, sha) != changes
                    or hashlib.sha256(_source(checkout, tracked, selected_pack).read_bytes()).hexdigest()
                    != proposal_hash):
                raise ValueError("co-design overlay changed during proposal preflight")
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
            **({"possibility_context": possibility_context}
               if possibility is not None else {}),
            **({"candidate_knowledge": candidate_knowledge,
                "disposable_index_used": not updating,
                "candidate_objects_may_remain_in_shared_git_store": not updating}
               if selected_pack is not None else {}),
            "active_checkout_patch_applied": False,
            "target_code_executed": False, "tests_executed": False,
            "patched_bytes_indexed": False, "semantic_truth_established": False,
            "action_authorized": False, "explicit_limits": (
                list(_LIMITS) if selected_pack is None else [
                    ("Co-design update admits one existing direct knowledge pack and existing regular-file modifications only, within the existing eight-path and 256 KiB budget." if updating else
                     "Co-design admits one new direct knowledge pack and contained non-executable regular-file additions in existing directories, within the existing eight-path and 256 KiB budget."),
                    "Deletion, rename, copy, mode change, binary, linked, Git control and filter-assigned candidate paths are refused.",
                    *list(_LIMITS[2:]),
                    ("The update uses only the disposable worktree overlay, not staged candidate objects." if updating else
                     "The candidate index and worktree are disposable; Git candidate objects may remain in the shared object store."),
                    "Single-pack preflight reads candidate index-tracked evidence and committed HEAD packs only. MECHANICALLY_VALID is not accepted knowledge, a whole-candidate build or semantic correctness; NOT_VALIDATED includes unavailable checks.",
                ]
            ),
        }
