"""Workspace-impact: which indexed records cite sources changed since the index.

The result is a path-level re-inspection candidate list. It must never index
the working overlay, hash dirty bytes as evidence, or invalidate a claim.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

from sensemaking_skills.cli import cli
from sensemaking_skills.semantic_architecture.knowledge_sources import build_knowledge_snapshot
from sensemaking_skills.semantic_architecture.knowledge_store import query_knowledge, store_snapshot
from sensemaking_skills.semantic_architecture.worktree_context import changed_paths_since_indexed_ref

REPOSITORY = "example/book"


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True, stderr=subprocess.PIPE).strip()


def _commit(root: Path, message: str) -> str:
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", message)
    return _git(root, "rev-parse", "HEAD")


@pytest.fixture
def indexed(tmp_path: Path) -> tuple[Path, Path, str]:
    root = tmp_path / "book"
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "steward@example.invalid")
    _git(root, "config", "user.name", "Steward Test")
    (root / "src").mkdir()
    (root / ".sensemaking/knowledge").mkdir(parents=True)
    (root / "MISSION.md").write_text("# Product\nAuthor controls acceptance.\n", encoding="utf-8")
    (root / "src/studio.js").write_text("export const open = () => 'working';\n", encoding="utf-8")
    (root / "src/unrelated.js").write_text("export const other = 1;\n", encoding="utf-8")
    records = {
        "schema_version": 1,
        "claims": [
            {"id": "goal:author-control", "kind": "goal", "statement": "Authors control acceptance",
             "authority_kind": "policy", "authority_ref": "MISSION.md",
             "evidence_refs": ["file:MISSION.md"]},
            {"id": "component:studio", "kind": "component", "statement": "Studio serves working state",
             "epistemic_status": "observed", "authority_kind": "code",
             "authority_ref": "src/studio.js", "evidence_refs": ["file:src/studio.js"]},
        ],
        "relations": [
            {"id": "rel:studio-goal", "subject": "component:studio", "predicate": "constrained_by",
             "object": "goal:author-control", "evidence_refs": ["file:src/studio.js"]},
        ],
    }
    (root / ".sensemaking/knowledge/book.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    sha = _commit(root, "reviewed knowledge")
    db = tmp_path / "knowledge.sqlite"
    snap = build_knowledge_snapshot(root, repository=REPOSITORY, target_ref=sha,
                                    include_repository_structure=True)
    store_snapshot(db, snap, source_root=root)
    return root, db, sha


def _impact(db: Path, root: Path, sha: str, limit: int = 50) -> dict:
    changed = changed_paths_since_indexed_ref(root, sha)
    return query_knowledge(db, repository=REPOSITORY, target_ref=sha, operation="workspace-impact",
                           workspace_changed_paths=changed["paths"], limit=limit)


def _by_id(payload: dict) -> dict[str, dict]:
    return {item["id"]: item for item in payload["workspace_impact"]["affected_records"]}


def test_clean_matching_workspace_reports_no_affected_records(indexed):
    root, db, sha = indexed
    payload = _impact(db, root, sha)
    assert payload["workspace_impact"]["changed_path_total"] == 0
    assert payload["workspace_impact"]["affected_records"] == []
    assert payload["claims"] == [] and payload["relations"] == []
    assert payload["truncated"] is False
    assert payload["semantic_truth_established"] is False
    assert payload["action_authorized"] is False


def test_dirty_cited_evidence_lists_reviewed_records_only(indexed):
    root, db, sha = indexed
    (root / "src/studio.js").write_text("export const open = () => 'revised';\n", encoding="utf-8")
    (root / "src/unrelated.js").write_text("export const other = 2;\n", encoding="utf-8")
    payload = _impact(db, root, sha)
    affected = _by_id(payload)
    assert set(affected) == {"component:studio", "rel:studio-goal"}
    assert affected["component:studio"]["changed_evidence_sources"] == ["src/studio.js"]
    assert affected["component:studio"]["record_source_changed"] is False
    assert {c["id"] for c in payload["claims"]} == {"component:studio"}
    assert {r["id"] for r in payload["relations"]} == {"rel:studio-goal"}
    # Mechanical path records are counted, never presented as reviewed knowledge.
    mechanical = payload["workspace_impact"]["mechanical_overlap_counts"]
    assert mechanical["claims"] >= 2 and mechanical["relations"] >= 2
    assert payload["workspace_impact"]["changed_path_total"] == 2


def test_edited_record_definition_is_distinguished_from_changed_evidence(indexed):
    root, db, sha = indexed
    path = root / ".sensemaking/knowledge/book.json"
    path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    affected = _by_id(_impact(db, root, sha))
    assert affected["goal:author-control"]["record_source_changed"] is True
    assert affected["goal:author-control"]["changed_evidence_sources"] == []


def test_committed_changes_since_historical_index_are_included(indexed):
    root, db, sha = indexed
    (root / "MISSION.md").write_text("# Product\nRevised and committed.\n", encoding="utf-8")
    _commit(root, "later product change")
    payload = _impact(db, root, sha)
    assert "goal:author-control" in _by_id(payload)
    assert payload["workspace_impact"]["changed_path_total"] == 1


def test_deleted_cited_source_is_reported(indexed):
    root, db, sha = indexed
    _git(root, "mv", "src/studio.js", "src/workspace.js")
    affected = _by_id(_impact(db, root, sha))
    assert affected["component:studio"]["changed_evidence_sources"] == ["src/studio.js"]


def test_limit_truncates_with_totals(indexed):
    root, db, sha = indexed
    (root / "src/studio.js").write_text("changed\n", encoding="utf-8")
    (root / "MISSION.md").write_text("changed\n", encoding="utf-8")
    payload = _impact(db, root, sha, limit=1)
    assert len(payload["workspace_impact"]["affected_records"]) == 1
    assert payload["workspace_impact"]["affected_record_total"] == 3
    assert payload["truncated"] is True


def test_workspace_impact_requires_changed_paths(indexed):
    _, db, sha = indexed
    with pytest.raises(ValueError, match="requires"):
        query_knowledge(db, repository=REPOSITORY, target_ref=sha, operation="workspace-impact")


def test_unavailable_indexed_revision_is_not_assessed(indexed):
    root, _, _ = indexed
    with pytest.raises(ValueError, match="NOT ASSESSED"):
        changed_paths_since_indexed_ref(root, "f" * 40)


def test_changed_paths_must_not_execute_repository_clean_filter(indexed, tmp_path):
    root, _, _ = indexed
    (root / ".gitattributes").write_text("MISSION.md filter=evil\n", encoding="utf-8")
    sha = _commit(root, "attributes")
    marker = tmp_path / "filter-ran.txt"
    clean = tmp_path / "clean.sh"
    clean.write_text(f"#!/bin/sh\nprintf 'ran' > '{marker}'\ncat\n", encoding="utf-8")
    clean.chmod(0o755)
    _git(root, "config", "filter.evil.clean", str(clean))
    (root / "MISSION.md").write_text("changed\n", encoding="utf-8")
    result = changed_paths_since_indexed_ref(root, sha)
    assert "MISSION.md" in result["paths"]
    assert not marker.exists()


def test_cli_workspace_impact_from_dirty_checkout(indexed):
    root, db, sha = indexed
    (root / "src/studio.js").write_text("revised\n", encoding="utf-8")
    base = ["semantic", "knowledge-query", "--db", str(db), "--repository", REPOSITORY,
            "--target-ref", sha, "--operation", "workspace-impact", "--json"]
    runner = CliRunner()
    missing = runner.invoke(cli, base)
    assert missing.exit_code != 0 and "--repo" in missing.output
    result = runner.invoke(cli, base + ["--repo", str(root)])
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["operation"] == "workspace-impact"
    assert "component:studio" in _by_id(payload)
    assert payload["workspace_context"]["uncommitted_changes_not_indexed"] is True
    assert payload["workspace_impact"]["overlay_indexed"] is False


def test_uncited_changed_paths_expose_reviewed_coverage_gaps(indexed):
    root, db, sha = indexed
    (root / "src/studio.js").write_text("revised\n", encoding="utf-8")
    # Cited only by mechanical structure records, never by reviewed knowledge.
    (root / "src/unrelated.js").write_text("export const other = 2;\n", encoding="utf-8")
    (root / "NOTES.md").write_text("untracked note\n", encoding="utf-8")
    impact = _impact(db, root, sha)["workspace_impact"]
    assert impact["uncited_changed_paths"] == ["NOTES.md", "src/unrelated.js"]
    assert impact["uncited_changed_path_total"] == 2
    assert impact["changed_path_total"] == 3


def test_clean_workspace_has_no_uncited_changed_paths(indexed):
    root, db, sha = indexed
    impact = _impact(db, root, sha)["workspace_impact"]
    assert impact["uncited_changed_paths"] == []
    assert impact["uncited_changed_path_total"] == 0


def test_uncited_changed_paths_are_bounded_and_disclose_truncation(indexed):
    root, db, sha = indexed
    for name in ("a.md", "b.md", "c.md"):
        (root / name).write_text("new\n", encoding="utf-8")
    payload = _impact(db, root, sha, limit=2)
    impact = payload["workspace_impact"]
    assert impact["affected_record_total"] == 0
    assert impact["uncited_changed_paths"] == ["a.md", "b.md"]
    assert impact["uncited_changed_path_total"] == 3
    assert payload["truncated"] is True
