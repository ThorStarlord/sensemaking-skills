"""Rebuildable SQLite index for *versioned*, evidence-bound semantic records.

Git-authored semantic records and exact repository bytes remain authoritative
sources; this database is a local derived index and cannot grant permissions.
Queries expose only explicit edges and preserve uncertainty and history.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from urllib.parse import quote

from .knowledge import KnowledgeSnapshot, fingerprint, record_dict, validate_snapshot, SCHEMA_VERSION

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
) -> dict:
    """Retrieve exact, explicitly declared links; never infer semantic closure.

    history/changes are about *indexed* revisions, NOT automatically proven
    chronological or Git-ancestry relationships.
    """
    if not 1 <= limit <= 250 or not 0 <= depth <= 4:
        raise ValueError("query limit must be 1..250 and depth 0..4")
    valid = {"search", "explain", "impact", "why", "contradictions", "history", "changes", "snapshot"}
    if operation not in valid:
        raise ValueError(f"unsupported semantic knowledge query: {operation}")
    if operation in {"explain", "impact", "why", "history"} and not subject:
        raise ValueError(f"{operation} requires a claim identifier")
    if operation == "changes" and not base_ref:
        raise ValueError("changes requires explicit base_ref")
    conn = _read_only(db_path)
    try:
        snap = _snapshot(conn, repository, target_ref)
        key = (repository, target_ref)
        claims = _read_claims(conn, key)
        relations = _read_relations(conn, key)
        found_claims: list[dict] = []
        found_relations: list[dict] = []
        extra: dict = {}
        if operation == "snapshot":
            extra["counts"] = {"claims": len(claims), "relations": len(relations)}
            extra["digest"] = snap["digest"]
        elif operation == "search":
            needle = (subject or "").casefold()
            found_claims = [c for c in claims.values() if needle in c["statement"].casefold() or needle in c["id"].casefold()]
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
            for _ in range(depth):
                selected |= {r["object"] for r in relations if r["subject"] in selected}
                selected |= {r["subject"] for r in relations if r["object"] in selected}
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
            extra["history_limit"] = "Indexed order is not proven Git ancestry or chronology."
        elif operation == "changes":
            assert base_ref is not None
            _snapshot(conn, repository, base_ref)
            old_key = (repository, base_ref)
            old_claims = _read_claims(conn, old_key)
            old_relations = {r["id"]: r for r in _read_relations(conn, old_key)}
            new_relations = {r["id"]: r for r in relations}
            extra["claim_delta"] = {
                "added": sorted(claims.keys() - old_claims.keys())[:limit],
                "removed": sorted(old_claims.keys() - claims.keys())[:limit],
                "changed": sorted(k for k in claims.keys() & old_claims.keys() if claims[k] != old_claims[k])[:limit],
            }
            extra["relation_delta"] = {
                "added": sorted(new_relations.keys() - old_relations.keys())[:limit],
                "removed": sorted(old_relations.keys() - new_relations.keys())[:limit],
                "changed": sorted(k for k in new_relations.keys() & old_relations.keys()
                                  if new_relations[k] != old_relations[k])[:limit],
            }
            extra["comparison_limit"] = "Snapshot set differences only; repository ancestry and semantic effects are NOT established."

        truncated = len(found_claims) > limit or len(found_relations) > limit
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
