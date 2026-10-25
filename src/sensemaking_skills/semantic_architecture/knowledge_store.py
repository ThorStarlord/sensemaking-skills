"""Rebuildable SQLite index for *versioned*, evidence-bound semantic records.

Git-authored semantic records and exact repository bytes remain authoritative
sources; this database is a local derived index and cannot grant permissions.
Queries expose only explicit edges and preserve uncertainty and history.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path
from urllib.parse import quote

from .knowledge import KnowledgeSnapshot, fingerprint, record_dict, validate_snapshot, SCHEMA_VERSION
from .knowledge_architecture import context_for, is_repository_file_path, orientation_summary, rules_for, term
from .knowledge_retrieval import (
    assess_current_authored_record, bounded_kind_coverage, classify_indexed_changes,
    context_workspace_overlap, search_matches, validate_retrieval_options,
    workspace_source_overlap,
)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS snapshots (
  repository TEXT NOT NULL,
  target_ref TEXT NOT NULL,
  digest TEXT NOT NULL,
  source_scope TEXT NOT NULL,
  limits TEXT NOT NULL,
  schema_version INTEGER NOT NULL,
  PRIMARY KEY (repository,target_ref)
);
CREATE TABLE IF NOT EXISTS claims (
  repository TEXT NOT NULL,
  target_ref TEXT NOT NULL,
  id TEXT NOT NULL,
  kind TEXT NOT NULL,
  statement TEXT NOT NULL,
  epistemic_status TEXT NOT NULL,
  payload TEXT NOT NULL,
  PRIMARY KEY (repository,target_ref,id),
  FOREIGN KEY (repository,target_ref) REFERENCES snapshots(repository,target_ref)
);
CREATE TABLE IF NOT EXISTS relations (
  repository TEXT NOT NULL,
  target_ref TEXT NOT NULL,
  id TEXT NOT NULL,
  subject TEXT NOT NULL,
  predicate TEXT NOT NULL,
  object TEXT NOT NULL,
  payload TEXT NOT NULL,
  PRIMARY KEY (repository,target_ref,id),
  FOREIGN KEY (repository,target_ref) REFERENCES snapshots(repository,target_ref)
);
CREATE INDEX IF NOT EXISTS claims_kind_idx ON claims(repository,target_ref,kind);
CREATE INDEX IF NOT EXISTS relations_subject_idx ON relations(repository,target_ref,subject);
CREATE INDEX IF NOT EXISTS relations_object_idx ON relations(repository,target_ref,object);
"""


def _dumps(data: object) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def _read_only(db_path: str | Path) -> sqlite3.Connection:
    path = Path(db_path).expanduser().resolve()
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"semantic knowledge index not found: {path}")
    try:
        conn = sqlite3.connect("file:" + quote(str(path), safe="/:") + "?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        if conn.execute("PRAGMA user_version").fetchone()[0] != SCHEMA_VERSION:
            conn.close()
            raise ValueError("unsupported semantic knowledge index schema version")
        return conn
    except sqlite3.Error as exc:
        raise ValueError(f"cannot read semantic knowledge index: {exc}") from exc


def store_snapshot(db_path: str | Path, snapshot: KnowledgeSnapshot, *, source_root: str | Path) -> dict:
    """Atomically store snapshot, preserving older revisions and refusing drift."""
    validate_snapshot(snapshot)
    path = Path(db_path).expanduser().absolute()
    root = Path(source_root).resolve()
    resolved = path.resolve()
    if resolved == root or resolved.is_relative_to(root) or path.is_symlink():
        raise ValueError("index must live outside the target Git checkout")
    if resolved.exists() and not resolved.is_file():
        raise ValueError("semantic knowledge index path is not a regular file")
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        conn = sqlite3.connect(path)
        try:
            conn.execute("PRAGMA foreign_keys=ON")
            version = conn.execute("PRAGMA user_version").fetchone()[0]
            if version not in (0, SCHEMA_VERSION):
                raise ValueError("unsupported index version; explicit migration required")
            with conn:
                conn.executescript(_SCHEMA)
                conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
                key = (snapshot.repository, snapshot.target_ref)
                digest = fingerprint(snapshot)
                existing = conn.execute(
                    "SELECT digest FROM snapshots WHERE repository=? AND target_ref=?", key
                ).fetchone()
                if existing and existing[0] != digest:
                    raise ValueError("conflicting content for an already-indexed Git snapshot")
                if existing:
                    return {"repository": key[0], "target_ref": key[1], "digest": digest,
                            "claim_count": len(snapshot.claims), "relation_count": len(snapshot.relations),
                            "already_indexed": True, "semantic_truth_established": False}
                conn.execute(
                    "INSERT INTO snapshots VALUES (?,?,?,?,?,?)",
                    (*key, digest, _dumps(snapshot.source_scope), _dumps(snapshot.limits), SCHEMA_VERSION),
                )
                conn.executemany(
                    "INSERT INTO claims VALUES (?,?,?,?,?,?,?)",
                    ((*key, v.id, v.kind, v.statement, v.epistemic_status, _dumps(record_dict(v))) for v in snapshot.claims),
                )
                conn.executemany(
                    "INSERT INTO relations VALUES (?,?,?,?,?,?,?)",
                    ((*key, v.id, v.subject, v.predicate, v.object, _dumps(record_dict(v))) for v in snapshot.relations),
                )
                return {"repository": key[0], "target_ref": key[1], "digest": digest,
                        "claim_count": len(snapshot.claims), "relation_count": len(snapshot.relations),
                        "already_indexed": False, "semantic_truth_established": False}
        finally:
            conn.close()
    except sqlite3.Error as exc:
        raise ValueError(f"semantic index write failed: {exc}") from exc


def _snapshot(conn: sqlite3.Connection, repository: str, target_ref: str) -> sqlite3.Row:
    snap = conn.execute(
        "SELECT * FROM snapshots WHERE repository=? AND target_ref=?", (repository, target_ref)
    ).fetchone()
    if snap is None:
        raise ValueError("requested repository/revision has not been indexed; NOT ASSESSED")
    return snap


def _read_claims(conn: sqlite3.Connection, key: tuple[str, str]) -> dict[str, dict]:
    return {
        row["id"]: json.loads(row["payload"])
        for row in conn.execute(
            "SELECT id,payload FROM claims WHERE repository=? AND target_ref=? ORDER BY id", key
        )
    }


def _read_relations(conn: sqlite3.Connection, key: tuple[str, str]) -> tuple[dict, ...]:
    return tuple(
        json.loads(row["payload"])
        for row in conn.execute(
            "SELECT payload FROM relations WHERE repository=? AND target_ref=? ORDER BY id", key
        )
    )


def query_knowledge(
    db_path: str | Path, *,
    repository: str, target_ref: str, operation: str,
    subject: str | None = None,
    base_ref: str | None = None,
    limit: int = 50, depth: int = 2,
    search_terms: tuple[str, ...] = (), expected_kinds: tuple[str, ...] = (),
    workspace_changed_paths: frozenset[str] | None = None,
) -> dict:
    """Retrieve exact, explicitly declared links; never infer semantic closure.

    history/changes are about *indexed* revisions, NOT automatically proven
    chronological or Git-ancestry relationships. Changes classifies existing
    indexed payload/fingerprint differences without inspecting current source.
    workspace-impact and the optional context-for worktree overlay match
    caller-observed changed paths against indexed source fingerprints only.
    """
    if not 1 <= limit <= 250 or not 0 <= depth <= 4:
        raise ValueError("query limit must be 1..250 and depth 0..4")
    valid = {"search", "explain", "impact", "why", "contradictions", "history", "changes", "snapshot",
             "workspace-impact", "rules-for", "term", "orientation-summary", "context-for"}
    if operation not in valid:
        raise ValueError(f"unsupported semantic knowledge query: {operation}")
    if operation in {"explain", "impact", "why", "history"} and not subject:
        raise ValueError(f"{operation} requires a claim identifier")
    if operation == "rules-for" and not subject:
        raise ValueError("rules-for requires --subject <repository-relative path>")
    if operation == "rules-for" and ("*" in subject or "?" in subject or subject.startswith("/")
                                     or ".." in subject.split("/")):
        raise ValueError("rules-for subject must be one repository-relative file path (no globs)")
    if operation == "context-for" and not subject:
        raise ValueError("context-for requires --subject <repository-relative file path>")
    if operation == "context-for" and not is_repository_file_path(subject):
        raise ValueError("context-for subject must be a repository-relative source path "
                         "(no globs, absolute paths, traversal or trailing slash)")
    if operation == "term" and not subject:
        raise ValueError("term requires --subject <term>")
    if operation == "changes" and not base_ref:
        raise ValueError("changes requires explicit base_ref")
    if operation == "workspace-impact" and workspace_changed_paths is None:
        raise ValueError("workspace-impact requires workspace changed paths (CLI --repo)")
    if workspace_changed_paths is not None and operation not in {"workspace-impact", "context-for"}:
        raise ValueError("workspace changed paths are supported only for workspace-impact or context-for")
    validate_retrieval_options(
        operation=operation, subject=subject, search_terms=search_terms,
        expected_kinds=expected_kinds,
    )
    conn = _read_only(db_path)
    try:
        snap = _snapshot(conn, repository, target_ref)
        key = (repository, target_ref)
        claims = _read_claims(conn, key)
        relations = _read_relations(conn, key)
        found_claims: list[dict] = []
        found_relations: list[dict] = []
        extra: dict = {}
        extra_truncated = False
        if operation == "snapshot":
            extra["counts"] = {"claims": len(claims), "relations": len(relations)}
            extra["digest"] = snap["digest"]
        elif operation == "search":
            found_claims, search_metadata = search_matches(
                claims, subject=subject, search_terms=search_terms,
            )
            extra.update(search_metadata)
        elif operation in {"explain", "why"}:
            if subject not in claims:
                raise ValueError("claim id not found in selected revision; NOT ASSESSED")
            if operation == "why" and claims[subject]["kind"] != "decision":
                raise ValueError("why requires a decision claim; no decision rationale inferred")
            found_claims = [claims[subject]]
            found_relations = [r for r in relations if r["subject"] == subject or r["object"] == subject]
            connected = {r["subject"] for r in found_relations} | {r["object"] for r in found_relations}
            found_claims.extend(claims[k] for k in sorted(connected - {subject}))
        elif operation == "impact":
            if subject not in claims:
                raise ValueError("claim id not found in selected revision; NOT ASSESSED")
            selected = {subject}
            frontier = {subject}
            for _ in range(depth):
                # One hop per iteration. Do not allow the second direction to
                # traverse vertices added by the first direction in this hop.
                neighbors = (
                    {r["object"] for r in relations if r["subject"] in frontier}
                    | {r["subject"] for r in relations if r["object"] in frontier}
                )
                frontier = neighbors - selected
                selected.update(frontier)
                if not frontier:
                    break
            found_claims = [claims[k] for k in sorted(selected)]
            found_relations = [r for r in relations if r["subject"] in selected and r["object"] in selected]
            extra["impact_limit"] = "Only declared edges are traversed (either direction); paths are CANDIDATES, not causal or transitive proofs."
        elif operation == "contradictions":
            found_relations = [r for r in relations if r["predicate"] == "contradicts" and
                               (not subject or subject in (r["subject"], r["object"]))]
            related = {endpoint for r in found_relations for endpoint in (r["subject"], r["object"])}
            found_claims = [claims[k] for k in sorted(related)]
            extra["contradiction_limit"] = "Only *explicit* contested relations; undetected contradictions may exist."
        elif operation == "history":
            rows = conn.execute(
                "SELECT s.rowid AS indexed_order,s.target_ref AS revision,c.payload AS claim "
                "FROM snapshots s JOIN claims c ON s.repository=c.repository AND s.target_ref=c.target_ref "
                "WHERE s.repository=? AND c.id=? ORDER BY s.rowid", (repository, subject)
            ).fetchall()
            extra["claim_history"] = [
                {"revision": r["revision"], "indexed_order": r["indexed_order"], "claim": json.loads(r["claim"])}
                for r in rows[:limit]
            ]
            extra["history_total_entries"] = len(rows)
            extra_truncated = len(rows) > limit
            extra["history_limit"] = "Indexed order is not proven Git ancestry or chronology."
        elif operation == "changes":
            assert base_ref is not None
            _snapshot(conn, repository, base_ref)
            old_key = (repository, base_ref)
            old_claims = _read_claims(conn, old_key)
            old_relations = {r["id"]: r for r in _read_relations(conn, old_key)}
            new_relations = {r["id"]: r for r in relations}
            claim_deltas = {
                "added": sorted(claims.keys() - old_claims.keys()),
                "removed": sorted(old_claims.keys() - claims.keys()),
                "changed": sorted(k for k in claims.keys() & old_claims.keys() if claims[k] != old_claims[k]),
            }
            relation_deltas = {
                "added": sorted(new_relations.keys() - old_relations.keys()),
                "removed": sorted(old_relations.keys() - new_relations.keys()),
                "changed": sorted(k for k in new_relations.keys() & old_relations.keys()
                                  if new_relations[k] != old_relations[k]),
            }
            extra_truncated = any(len(items) > limit for changes in (claim_deltas, relation_deltas)
                                  for items in changes.values())
            extra["claim_delta"] = {kind: items[:limit] for kind, items in claim_deltas.items()}
            extra["relation_delta"] = {kind: items[:limit] for kind, items in relation_deltas.items()}
            extra["delta_total_counts"] = {
                "claims": {kind: len(items) for kind, items in claim_deltas.items()},
                "relations": {kind: len(items) for kind, items in relation_deltas.items()},
            }
            claim_details, claim_counts = classify_indexed_changes(old_claims, claims, limit=limit)
            relation_details, relation_counts = classify_indexed_changes(old_relations, new_relations, limit=limit)
            extra["change_classification"] = {
                "claims": claim_details,
                "relations": relation_details,
                "counts": {"claims": claim_counts, "relations": relation_counts},
                "truncated": (
                    claim_counts["changed_total"] > limit or relation_counts["changed_total"] > limit
                ),
                "explicit_limits": [
                    "Raw claim_delta/relation_delta.changed retain their historical full-payload meaning.",
                    "Authored-field and fingerprint classifications are mechanical, not semantic validity.",
                    "Supporting-source entries describe indexed fingerprint/reference differences, not causal impact.",
                    "Unindexed, external or uncited evidence remains NOT ASSESSED; no Git ancestry is inferred.",
                    "Added/removed IDs are raw set differences; renames and replacements are NOT ASSESSED.",
                ],
            }
            extra["comparison_limit"] = "Snapshot set differences only; repository ancestry and semantic effects are NOT established."
        elif operation == "workspace-impact":
            assert workspace_changed_paths is not None
            found_claims, found_relations, overlap = workspace_source_overlap(
                claims, relations, changed_paths=workspace_changed_paths, limit=limit,
            )
            extra["workspace_impact"] = overlap
            extra_truncated = (
                overlap["affected_record_total"] > limit or overlap["uncited_changed_path_total"] > limit
            )

        elif operation == "rules-for":
            assert subject is not None
            extra["architecture"] = rules_for(claims, relations, path=subject, limit=limit)
            ids = {r["claim_id"] for r in extra["architecture"]["applicable_rules"]}
            for name in ("owning_components", "layers", "bounded_contexts", "tests"):
                ids.update(extra["architecture"][name])
            found_claims = [claims[cid] for cid in sorted(ids) if cid in claims]
            found_relations = [r for r in relations if (
                r["predicate"] in {"belongs_to", "tested_by", "applies_to"}
                and (r["subject"] in ids or r["object"] in ids)
                and r["subject"] in claims and r["object"] in claims
            )]
            extra_truncated = extra["architecture"]["truncated"]
        elif operation == "context-for":
            assert subject is not None
            extra["context"], selected_claims, selected_relations = context_for(
                claims, relations, path=subject, limit=limit,
            )
            # context_for independently caps each category. The top-level query
            # envelope has a separate global limit, so it may not contain every
            # referenced claim/relation. Prioritize ownership and governing
            # rules before optional historical or verification context.
            ctx = extra["context"]
            ranked = [
                *ctx["ownership"]["components"],
                *(rule["claim_id"] for rule in ctx["architecture_rules"]),
                *ctx["ownership"]["layers"],
                *ctx["ownership"]["bounded_contexts"],
                *(item["claim_id"] for name in
                  ("contracts", "decisions", "alternatives", "history",
                   "verification_refs")
                  for item in ctx[name]),
            ]
            ordered_claim_ids = list(dict.fromkeys(
                cid for cid in [*ranked, *selected_claims] if cid in claims
            ))
            found_claims = [claims[cid] for cid in ordered_claim_ids]
            relation_id_set = set(selected_relations)
            found_relations = [r for r in relations if r["id"] in relation_id_set]
            claim_overflow = max(0, len(found_claims) - limit)
            relation_overflow = max(0, len(found_relations) - limit)
            ctx["envelope_reference_coverage"] = {
                "selected_claim_total": len(found_claims),
                "returned_claim_total": min(len(found_claims), limit),
                "omitted_claim_total": claim_overflow,
                "omitted_claim_ids": [c["id"] for c in found_claims[limit:limit + min(limit, 25)]],
                "selected_relation_total": len(found_relations),
                "returned_relation_total": min(len(found_relations), limit),
                "omitted_relation_total": relation_overflow,
                "omitted_relation_ids": [r["id"] for r in found_relations[limit:limit + min(limit, 25)]],
                "note": (
                    "Context categories have independent limits. The top-level "
                    "claims/relations envelope has a separate global limit; "
                    "some category references may lack top-level records. "
                    "Inspect original cited sources; omission is NOT clearance."
                ),
            }
            if claim_overflow or relation_overflow:
                ctx["truncated"] = True
                ctx["knowledge_gaps"].append({
                    "category": "envelope", "status": "TRUNCATED",
                    "note": (
                        f"Global envelope limit {limit} omitted {claim_overflow} "
                        f"selected claim and {relation_overflow} relation record(s); "
                        "category entries may reference omitted records."
                    ),
                })
            extra_truncated = ctx["truncated"]
            if workspace_changed_paths is not None:
                extra["context"]["workspace_relevance"] = context_workspace_overlap(
                    claims, relations, selected_claim_ids=selected_claims,
                    selected_relation_ids=selected_relations,
                    changed_paths=workspace_changed_paths, target_path=subject,
                    limit=limit, context_truncated=extra["context"]["truncated"],
                )
                if extra["context"]["workspace_relevance"]["affected_records_omitted"]:
                    extra_truncated = True
        elif operation == "term":
            assert subject is not None
            extra["term"] = term(claims, relations, name=subject, limit=limit)
            term_ids = set(extra["term"]["matched_claims"]) | set(extra["term"]["synonyms"]) | set(extra["term"]["distinct_from"])
            found_claims = [claims[c] for c in sorted(term_ids) if c in claims]
            found_relations = [r for r in relations if r["predicate"] in {"synonym_of", "distinct_from"}
                               and r["subject"] in term_ids and r["object"] in term_ids]
            extra_truncated = extra["term"]["truncated"]
        elif operation == "orientation-summary":
            extra["orientation"] = orientation_summary(claims, relations)

        if expected_kinds:
            extra["bounded_coverage"] = bounded_kind_coverage(
                found_claims, expected_kinds=expected_kinds, limit=limit,
            )

        truncated = extra_truncated or len(found_claims) > limit or len(found_relations) > limit
        envelope = {
            "repository": repository, "target_ref": target_ref, "operation": operation,
            "claims": found_claims[:limit], "relations": found_relations[:limit],
            "truncated": truncated, "source_scope": json.loads(snap["source_scope"]),
            "explicit_limits": [*json.loads(snap["limits"]),
                                "Knowledge records are declared/observed at the indexed revision, NOT semantic truth or action authority."],
            "semantic_truth_established": False, "action_authorized": False,
        }
        envelope.update(extra)
        return envelope
    finally:
        conn.close()




def query_context_paths(
    db_path: str | Path, *, repository: str, target_ref: str,
    paths: tuple[str, ...], limit: int = 50, depth: int = 2,
    search_terms: tuple[str, ...] = (), expected_kinds: tuple[str, ...] = (),
    workspace_changed_paths: frozenset[str] | None = None,
) -> dict:
    """Compose existing source-pinned context-for responses for 2..8 files.

    No new inference or cross-file ownership is made: each file retains its own
    coverage, caveats and truncation. Top-level claims/relations deduplicate only
    the already-bounded per-file results, without claiming global completeness.
    """
    if not 2 <= len(paths) <= 8:
        raise ValueError("context-for --path requires 2..8 repository-relative source paths")
    if len(set(paths)) != len(paths):
        raise ValueError("context-for --path values must be distinct")
    if any(not is_repository_file_path(path) for path in paths):
        raise ValueError("context-for --path requires valid repository-relative source paths")

    contexts: list[dict] = []
    unique_claims: dict[str, dict] = {}
    unique_relations: dict[str, dict] = {}
    encountered: dict[str, list[str]] = {}
    any_truncated = False
    first: dict | None = None
    for path in paths:
        result = query_knowledge(
            db_path, repository=repository, target_ref=target_ref,
            operation="context-for", subject=path, limit=limit, depth=depth,
            search_terms=search_terms, expected_kinds=expected_kinds,
            workspace_changed_paths=workspace_changed_paths,
        )
        if first is None:
            first = result
        claim_ids = [record["id"] for record in result["claims"]]
        relation_ids = [record["id"] for record in result["relations"]]
        contexts.append({
            "path": path, "context": result["context"],
            "claim_ids": claim_ids, "relation_ids": relation_ids,
            "truncated": result["truncated"],
        })
        any_truncated |= result["truncated"]
        for record in result["claims"]:
            unique_claims[record["id"]] = record
            encountered.setdefault(record["id"], []).append(path)
        for record in result["relations"]:
            unique_relations[record["id"]] = record

    assert first is not None
    return {
        "repository": repository, "target_ref": target_ref,
        "operation": "context-for", "paths": list(paths),
        "contexts": contexts,
        "claims": [unique_claims[cid] for cid in sorted(unique_claims)],
        "relations": [unique_relations[rid] for rid in sorted(unique_relations)],
        "multi_file_context": {
            "path_count": len(paths), "per_path_limit": limit,
            "maximum_returned_claims": len(paths) * limit,
            "maximum_returned_relations": len(paths) * limit,
            "returned_unique_claim_count": len(unique_claims),
            "returned_unique_relation_count": len(unique_relations),
            "shared_claim_ids": sorted(cid for cid, sources in encountered.items()
                                      if len(sources) > 1),
            "truncated_paths": [item["path"] for item in contexts if item["truncated"]],
            "coverage_complete": False,
            "note": (
                "Deduplicated returned records only. Each path retains its own "
                "NOT_ASSESSED, epistemic caveats and truncation. A shared record "
                "does not imply a new dependency between the requested files."
            ),
        },
        "truncated": any_truncated, "source_scope": first["source_scope"],
        "explicit_limits": [
            *first["explicit_limits"],
            "Batch bounds apply per path; union records do not establish complete "
            "coverage of the task or relationships across paths.",
        ],
        "semantic_truth_established": False, "action_authorized": False,
    }


def audit_knowledge_sources(
    db_path: str | Path, *,
    repository: str, indexed_ref: str,
    current_repo_root: str | Path, current_ref: str,
    limit: int = 100,
) -> dict:
    """Report source-byte drift between an indexed past revision and clean HEAD.

    A changed byte means evidence should be re-examined; unchanged bytes do
    NOT establish that the asserted policy or architecture remains applicable.
    """
    from .knowledge_sources import _source, verified_tracked_sources

    if not 1 <= limit <= 500:
        raise ValueError("audit limit must be between 1 and 500")
    root, tracked = verified_tracked_sources(current_repo_root, current_ref)
    conn = _read_only(db_path)
    try:
        _snapshot(conn, repository, indexed_ref)
        key = (repository, indexed_ref)
        records = [
            ("claim", c) for c in _read_claims(conn, key).values()
        ] + [
            ("relation", r) for r in _read_relations(conn, key)
        ]
        digests: dict[str, str | None] = {}
        # A pack is loaded at most once, and only after the original source-byte
        # audit has identified its container as changed/missing. No overlay
        # content is ever indexed or taken as reviewed semantic authority.
        current_packs: dict[str, object] = {}
        authored_details: list[dict] = []
        authored_counts = {
            "authored_fields_changed": 0,
            "authored_fields_unchanged": 0,
            "record_absent_from_original_pack": 0,
            "not_assessed": 0,
        }
        results = []
        totals = {"unchanged_source_bytes": 0, "source_changed": 0,
                  "source_missing_or_unsafe": 0, "not_assessed": 0}
        for kind, item in records:
            expected = item.get("attributes", {}).get("source_sha256", {})
            if not isinstance(expected, dict) or not expected:
                status = "not_assessed"
                changed: list[str] = []
                missing: list[str] = []
            else:
                changed, missing = [], []
                for path, previous_hash in sorted(expected.items()):
                    if path not in digests:
                        try:
                            digests[path] = hashlib.sha256(_source(root, tracked, path).read_bytes()).hexdigest()
                        except (ValueError, OSError):
                            digests[path] = None
                    actual = digests[path]
                    if actual is None:
                        missing.append(path)
                    elif actual != previous_hash:
                        changed.append(path)
                status = (
                    "source_missing_or_unsafe" if missing else
                    "source_changed" if changed else "unchanged_source_bytes"
                )
            totals[status] += 1
            result_row = {
                "record_type": kind, "id": item["id"], "source_status": status,
                "changed_sources": changed, "missing_or_unsafe_sources": missing,
            }
            # A changed shared authored JSON pack affects every contained source
            # fingerprint. Disambiguate its individual record fields without
            # weakening the conservative source-status result.
            source_ref = item.get("source_ref", "")
            pack = source_ref[5:] if (
                isinstance(source_ref, str)
                and source_ref.startswith("file:.sensemaking/knowledge/")
                and source_ref.endswith(".json")
            ) else None
            if pack is not None and (pack in changed or pack in missing):
                if pack not in current_packs:
                    try:
                        data = _source(root, tracked, pack).read_bytes()
                        if len(data) > 2_000_000:
                            raise ValueError("oversized current authored pack")
                        current_packs[pack] = json.loads(data.decode("utf-8"))
                    except (ValueError, OSError, UnicodeError):
                        current_packs[pack] = None
                detail = assess_current_authored_record(
                    item, record_type=kind, current_pack=current_packs[pack],
                )
                detail.update({
                    "record_type": kind, "id": item["id"], "authored_pack": pack,
                    "other_changed_sources": [p for p in changed if p != pack],
                    "other_missing_or_unsafe_sources": [p for p in missing if p != pack],
                })
                if detail["record_at_original_path"] is False:
                    authored_counts["record_absent_from_original_pack"] += 1
                elif detail["assessment_status"] != "ASSESSED":
                    authored_counts["not_assessed"] += 1
                elif detail["authored_fields_changed"]:
                    authored_counts["authored_fields_changed"] += 1
                else:
                    authored_counts["authored_fields_unchanged"] += 1
                authored_details.append(detail)
                result_row["authored_record_assessment"] = {
                    "assessment_status": detail["assessment_status"],
                    "authored_fields_changed": detail["authored_fields_changed"],
                    "record_at_original_path": detail["record_at_original_path"],
                    **({"unassessed_reason": detail["unassessed_reason"]}
                       if "unassessed_reason" in detail else {}),
                }
            if status != "unchanged_source_bytes":
                results.append(result_row)
        return {
            "repository": repository, "indexed_ref": indexed_ref,
            "current_ref": current_ref, "record_count": len(records),
            "source_status_counts": totals,
            "affected_records": results[:limit],
            "authored_record_audit": {
                "assessed_container_record_total": len(authored_details),
                "counts": authored_counts,
                "records": authored_details[:limit],
                "truncated": len(authored_details) > limit,
                "note": (
                    "Comparison of normalized authored fields at the record's "
                    "previous tracked pack path only. Unchanged authored fields "
                    "do NOT establish current semantic validity. A missing record "
                    "may have moved; changed or missing supporting sources still "
                    "require inspection."
                ),
            },
            "truncated": len(results) > limit,
            "explicit_limits": [
                "This compares cited SOURCE BYTES, not semantic validity or Git ancestry.",
                "Unchanged files may contain stale interpretations; unindexed sources are NOT ASSESSED.",
                "Changed source evidence requires inspection, not automatic invalidation.",
                "Record-aware pack assessment is additive; it does not erase conservative byte drift.",
            ],
            "semantic_truth_established": False, "action_authorized": False,
        }
    finally:
        conn.close()
