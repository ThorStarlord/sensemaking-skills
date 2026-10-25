"""Opt-in, read-only binding of reviewed context-for results to a Campaign target.

The Campaign working context remains the authority for responsibility, authority
and stop conditions. This adapter attaches one to eight explicitly requested,
source-pinned architectural queries beside it. The knowledge checkout's repository
identity is checked mechanically against the Campaign target before any result is
returned. The result is never a selected responsibility, a next action or permission
to act.
"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Any, Sequence

from .campaigns import CampaignWorkspaceError
from .campaigns.target_snapshot import repository_identity
from .semantic_architecture.knowledge_store import query_context_paths, query_knowledge
from .semantic_architecture.worktree_context import (
    changed_paths_since_indexed_ref,
    inspect_worktree_context,
)

MATCH = "MATCH"
MISMATCH = "MISMATCH"
NOT_ASSESSED = "NOT_ASSESSED"
HISTORICAL = "HISTORICAL"
ALIGNED = "ALIGNED_TO_INDEXED_REVISION"
MAX_KNOWLEDGE_PATHS = 8

_SHA_PATTERN = re.compile(r"[0-9a-f]{40}")


class CampaignKnowledgeError(CampaignWorkspaceError):
    """An explicitly requested reviewed-knowledge view could not be bound or queried."""


def select_campaign_target(targets: Sequence[dict[str, Any]], alias: str | None) -> dict[str, Any]:
    """Return the single Campaign target a knowledge query may bind to; never guess one."""
    if not targets:
        raise CampaignKnowledgeError(
            "reviewed knowledge needs a bound Campaign target; this Campaign has none"
        )
    aliases = ", ".join(str(item["alias"]) for item in targets)
    if alias is None:
        if len(targets) > 1:
            raise CampaignKnowledgeError(
                f"several Campaign targets are bound; pass --target-alias (one of: {aliases})"
            )
        return dict(targets[0])
    for item in targets:
        if item["alias"] == alias:
            return dict(item)
    raise CampaignKnowledgeError(f"unknown --target-alias {alias!r}; bound aliases: {aliases}")


def build_reviewed_knowledge(
    *,
    targets: Sequence[dict[str, Any]],
    target_alias: str | None,
    knowledge_db: Path,
    knowledge_repository: str,
    knowledge_ref: str,
    knowledge_repo: Path,
    knowledge_paths: Sequence[str],
) -> dict[str, Any]:
    """Bind source-pinned context-for results for one to eight files to a Campaign target."""
    paths = tuple(knowledge_paths)
    if not 1 <= len(paths) <= MAX_KNOWLEDGE_PATHS:
        raise CampaignKnowledgeError(f"reviewed knowledge accepts 1 to {MAX_KNOWLEDGE_PATHS} paths")
    if len(set(paths)) != len(paths):
        raise CampaignKnowledgeError("reviewed knowledge paths must be distinct")
    if not _SHA_PATTERN.fullmatch(knowledge_ref):
        raise CampaignKnowledgeError("--knowledge-ref must be an exact 40-character Git SHA")
    target = select_campaign_target(targets, target_alias)
    worktree = _inspect_checkout(knowledge_repo, knowledge_ref)
    identity_source, repository_id = _checkout_identity(knowledge_repo)
    if repository_id != target.get("repository_id"):
        raise CampaignKnowledgeError(
            f"the knowledge checkout is not the repository bound to Campaign target "
            f"{target['alias']!r}; refusing to attribute its index to this Campaign"
        )
    target_head = str(target.get("head_sha") or "")
    if target_head:
        commit_match = MATCH if target_head == knowledge_ref else MISMATCH
    else:
        commit_match = NOT_ASSESSED
    changed_paths, overlay_note = _workspace_overlay(knowledge_repo, knowledge_ref)
    query = _query_paths(
        knowledge_db, repository=knowledge_repository, target_ref=knowledge_ref,
        paths=paths, changed_paths=changed_paths,
    )
    contexts = _contexts_by_path(query, paths)
    if overlay_note is not None:
        for context in contexts.values():
            context["workspace_relevance"] = {
                "assessment": NOT_ASSESSED,
                "overlay_indexed": False,
                "semantic_staleness_established": False,
                "note": "Cannot compare worktree changes with the indexed revision: " + overlay_note,
            }
    if commit_match == MISMATCH or not worktree["head_matches_indexed_ref"]:
        applicability = HISTORICAL
    elif commit_match == NOT_ASSESSED:
        applicability = NOT_ASSESSED
    else:
        applicability = ALIGNED
    return {
        "source_identity": {
            "repository": knowledge_repository,
            "indexed_ref": knowledge_ref,
            "repository_identity_source": identity_source,
            "repository_label_verified": False,
            "observed_worktree_head": worktree["current_head"],
            "head_matches_indexed_ref": worktree["head_matches_indexed_ref"],
            "worktree_clean": worktree["worktree_clean"],
            "uncommitted_changes_not_indexed": worktree["uncommitted_changes_not_indexed"],
        },
        "target_binding": {
            "target_alias": target["alias"],
            "repository_id_match": MATCH,
            "source_commit_match": commit_match,
            "target_head_sha": target_head or None,
        },
        "applicability": applicability,
        "selected_paths": list(paths),
        "query": query,
        "caveats": _caveats(
            paths=paths, ref=knowledge_ref, target=target, target_head=target_head,
            commit_match=commit_match, worktree=worktree, overlay_note=overlay_note,
            query=query, contexts=contexts,
        ),
        "semantic_truth_established": False,
        "action_authorized": False,
    }


def _inspect_checkout(repo: Path, indexed_ref: str) -> dict[str, Any]:
    try:
        return inspect_worktree_context(repo, indexed_ref)
    except (ValueError, OSError) as exc:
        raise CampaignKnowledgeError(
            f"the knowledge checkout could not be inspected as a Git worktree: {exc}"
        ) from exc


def _checkout_identity(repo: Path) -> tuple[str, str]:
    try:
        return repository_identity(repo)
    except (CampaignWorkspaceError, OSError, UnicodeError) as exc:
        raise CampaignKnowledgeError(
            f"the knowledge checkout identity could not be verified: {exc}"
        ) from exc


def _workspace_overlay(repo: Path, indexed_ref: str) -> tuple[Any, str | None]:
    """Changed paths for the context-for overlay, or the reason they cannot be compared."""
    try:
        return changed_paths_since_indexed_ref(repo, indexed_ref)["paths"], None
    except ValueError as exc:
        return None, str(exc)


def _query_paths(
    db_path: Path, *, repository: str, target_ref: str, paths: tuple[str, ...], changed_paths: Any,
) -> dict[str, Any]:
    """One file keeps the single context-for envelope; two to eight use the multi-file envelope."""
    try:
        if len(paths) == 1:
            return query_knowledge(
                db_path, repository=repository, target_ref=target_ref, operation="context-for",
                subject=paths[0], workspace_changed_paths=changed_paths,
            )
        return query_context_paths(
            db_path, repository=repository, target_ref=target_ref, paths=paths,
            workspace_changed_paths=changed_paths,
        )
    except (ValueError, OSError, UnicodeError, sqlite3.Error) as exc:
        raise CampaignKnowledgeError(f"reviewed knowledge query failed: {exc}") from exc


def _contexts_by_path(query: dict[str, Any], paths: tuple[str, ...]) -> dict[str, dict[str, Any]]:
    """Per-file context objects, shared by reference with the unmodified query envelope."""
    if len(paths) == 1:
        return {paths[0]: query["context"]}
    return {item["path"]: item["context"] for item in query["contexts"]}


def _caveats(
    *, paths: tuple[str, ...], ref: str, target: dict[str, Any], target_head: str,
    commit_match: str, worktree: dict[str, Any], overlay_note: str | None,
    query: dict[str, Any], contexts: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    multi = len(paths) > 1
    caveats: list[dict[str, str]] = []
    if commit_match == MISMATCH:
        caveats.append({
            "code": "HISTORICAL_TARGET_HEAD",
            "detail": f"Indexed revision {ref} differs from the Campaign target head "
                      f"{target_head}; the records describe the indexed revision only.",
        })
    if not worktree["head_matches_indexed_ref"]:
        caveats.append({
            "code": "HISTORICAL_CHECKOUT_HEAD",
            "detail": f"The active checkout is at {worktree['current_head']}, not the indexed "
                      "revision; re-inspect the original source before relying on these records.",
        })
    if not worktree["worktree_clean"]:
        caveats.append({
            "code": "UNINDEXED_WORKTREE_CHANGES",
            "detail": "Uncommitted or untracked changes are not indexed; overlap is path-level "
                      "only and no file content is compared.",
        })
    if target.get("dirty"):
        caveats.append({
            "code": "TARGET_SNAPSHOT_DIRTY",
            "detail": "The Campaign target snapshot recorded uncommitted state that the indexed "
                      "revision does not represent.",
        })
    if overlay_note is not None:
        caveats.append({"code": "WORKSPACE_RELEVANCE_NOT_ASSESSED", "detail": overlay_note})
    for path, context in contexts.items():
        scope = {"path": path} if multi else {}
        gaps = context["knowledge_gaps"]
        unassessed = [gap["category"] for gap in gaps if gap["status"] == "NOT_ASSESSED"]
        if unassessed:
            caveats.append({
                "code": "COVERAGE_NOT_ASSESSED", **scope,
                "detail": "NOT ASSESSED for: " + ", ".join(unassessed) + ". An absent record is "
                          "not evidence that nothing applies.",
            })
        for gap in gaps:
            if gap["status"] == "AMBIGUOUS":
                caveats.append({"code": "OWNERSHIP_AMBIGUOUS", **scope, "detail": gap["note"]})
            elif gap["status"] == "EPISTEMIC_CAVEAT":
                caveats.append({"code": "EPISTEMIC_CAVEAT", **scope, "detail": gap["note"]})
    if query["truncated"]:
        if multi:
            detail = ("The bounded per-file queries omitted records for: "
                      + ", ".join(query["multi_file_context"]["truncated_paths"])
                      + "; see query.contexts[].context.omitted.")
        else:
            detail = "The bounded query omitted records; see query.context.omitted."
        caveats.append({"code": "TRUNCATED", "detail": detail})
    if multi:
        caveats.append({
            "code": "MULTI_FILE_NOT_COMPLETE",
            "detail": "Each file's results are bounded and deduplicated. A record shared by "
                      "several files does not imply a dependency between them, and the selected "
                      "set does not establish completeness of the task's architecture.",
        })
    caveats.append({
        "code": "INSPECT_ORIGINAL_SOURCE",
        "detail": "Read " + ", ".join(paths) + " and their cited authorities before relying on "
                  "these records; they are source-linked claims, not permission to act.",
    })
    return caveats
