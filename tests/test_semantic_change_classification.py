"""Source-indexed regression tests for authored-field versus provenance drift.

These tests build real clean Git snapshots; a metadata-only change must not
masquerade as a change in an individual authored record's fields.
"""
from __future__ import annotations

import json
import subprocess
from dataclasses import replace
from pathlib import Path

import pytest
from click.testing import CliRunner

from sensemaking_skills.cli import cli
from sensemaking_skills.semantic_architecture.knowledge_sources import build_knowledge_snapshot
from sensemaking_skills.semantic_architecture.knowledge_store import (
    audit_knowledge_sources, query_knowledge, store_snapshot,
)

REPOSITORY = "example/change-classification"
PACK = ".sensemaking/knowledge/stewardship.json"


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.PIPE,
                                   text=True).strip()


def _commit(root: Path, label: str) -> str:
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", label)
    return _git(root, "rev-parse", "HEAD")


def _pack(root: Path) -> dict:
    return json.loads((root / PACK).read_text(encoding="utf-8"))


def _save(root: Path, data: dict, *, indent: int = 2) -> None:
    (root / PACK).write_text(json.dumps(data, indent=indent) + "\n", encoding="utf-8")


def _index(root: Path, db: Path, ref: str, *, omit_a_fingerprint: bool = False) -> None:
    snapshot = build_knowledge_snapshot(root, repository=REPOSITORY, target_ref=ref)
    if omit_a_fingerprint:
        snapshot = replace(snapshot, claims=tuple(
            replace(claim, attributes={
                key: value for key, value in claim.attributes.items() if key != "source_sha256"
            }) if claim.id == "cap:a" else claim
            for claim in snapshot.claims
        ))
    store_snapshot(db, snapshot, source_root=root)


def _changes(db: Path, old_ref: str, new_ref: str, *, limit: int = 50) -> dict:
    return query_knowledge(db, repository=REPOSITORY, target_ref=new_ref,
                           operation="changes", base_ref=old_ref, limit=limit)


def _records(payload: dict, kind: str = "claims") -> dict[str, dict]:
    return {record["id"]: record for record in payload["change_classification"][kind]}


@pytest.fixture
def indexed(tmp_path: Path) -> tuple[Path, Path, str]:
    root = tmp_path / "product"
    (root / ".sensemaking/knowledge").mkdir(parents=True)
    (root / "src").mkdir()
    (root / "docs/adr").mkdir(parents=True)
    _git(root, "init", "-q")
    _git(root, "config", "user.name", "Semantic Fixture")
    _git(root, "config", "user.email", "fixture@example.invalid")
    (root / "src/a.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "src/b.py").write_text("VALUE = 2\n", encoding="utf-8")
    (root / "docs/adr/0031-test.md").write_text(
        "# ADR 0031: Stable test title\n\n**Status**: ACCEPTED\n", encoding="utf-8"
    )
    _save(root, {
        "schema_version": 1,
        "claims": [
            {"id": "cap:a", "kind": "capability", "statement": "Capability A",
             "authority_kind": "code", "authority_ref": "src/a.py",
             "evidence_refs": ["file:src/a.py"]},
            {"id": "cap:b", "kind": "capability", "statement": "Capability B",
             "authority_kind": "code", "authority_ref": "src/b.py",
             "evidence_refs": ["file:src/b.py"]},
        ],
        "relations": [
            {"id": "rel:a", "subject": "cap:a", "object": "cap:b",
             "predicate": "references", "evidence_refs": ["file:src/a.py"]},
            {"id": "rel:b", "subject": "cap:b", "object": "cap:a",
             "predicate": "references", "evidence_refs": ["file:src/b.py"]},
        ],
    })
    old_ref = _commit(root, "base")
    db = tmp_path / "semantic.sqlite"  # outside the target Git checkout
    _index(root, db, old_ref)
    return root, db, old_ref


def test_only_one_authored_claim_changes_when_shared_pack_changes(indexed):
    root, db, old = indexed
    data = _pack(root)
    data["claims"][0]["statement"] = "Capability A revised"
    _save(root, data)
    new = _commit(root, "edit claim A")
    _index(root, db, new)

    payload = _changes(db, old, new)
    # Existing raw IDs intentionally preserve full indexed-payload semantics.
    assert {"cap:a", "cap:b"} <= set(payload["claim_delta"]["changed"])
    details = _records(payload)
    assert details["cap:a"]["authored_fields_changed"] is True
    assert details["cap:a"]["provenance_only"] is False
    assert details["cap:b"]["authored_fields_changed"] is False
    assert details["cap:b"]["authoring_source_changed"] is True
    assert details["cap:b"]["provenance_only"] is True
    assert details["cap:b"]["changed_supporting_sources"] == []
    relations = _records(payload, "relations")
    assert relations["rel:a"]["provenance_only"] is True
    assert relations["rel:b"]["provenance_only"] is True
    assert payload["change_classification"]["counts"]["claims"]["provenance_only"] >= 1
    assert payload["semantic_truth_established"] is False
    assert payload["action_authorized"] is False


def test_separately_cited_implementation_change_is_not_authored_change(indexed):
    root, db, old = indexed
    (root / "src/a.py").write_text("VALUE = 42\n", encoding="utf-8")
    new = _commit(root, "edit cited implementation A")
    _index(root, db, new)
    payload = _changes(db, old, new)
    details = _records(payload)
    assert details["cap:a"]["authored_fields_changed"] is False
    assert details["cap:a"]["authoring_source_changed"] is False
    assert details["cap:a"]["changed_supporting_sources"] == [
        {"path": "src/a.py", "change": "fingerprint_changed"}
    ]
    assert details["cap:a"]["provenance_only"] is False
    assert "cap:b" not in payload["claim_delta"]["changed"]
    assert _records(payload, "relations")["rel:a"]["changed_supporting_sources"][0]["path"] == "src/a.py"
    # Source-byte audit is deliberately unchanged and conservative.
    audit = audit_knowledge_sources(
        db, repository=REPOSITORY, indexed_ref=old, current_repo_root=root, current_ref=new,
    )
    assert any(row["id"] == "cap:a" for row in audit["affected_records"])


def test_simultaneous_authored_and_evidence_change(indexed):
    root, db, old = indexed
    data = _pack(root)
    data["claims"][0]["statement"] = "New A decision"
    _save(root, data)
    (root / "src/a.py").write_text("VALUE = 88\n", encoding="utf-8")
    new = _commit(root, "edit statement and source")
    _index(root, db, new)
    details = _records(_changes(db, old, new))
    assert details["cap:a"]["authored_fields_changed"] is True
    assert details["cap:a"]["authoring_source_changed"] is True
    assert details["cap:a"]["changed_supporting_sources"][0]["path"] == "src/a.py"
    assert details["cap:b"]["provenance_only"] is True


def test_reformat_only_changes_container_provenance(indexed):
    root, db, old = indexed
    _save(root, _pack(root), indent=4)
    new = _commit(root, "reformat JSON")
    _index(root, db, new)
    rows = _records(_changes(db, old, new))
    assert set(rows) == {"cap:a", "cap:b"}
    assert all(row["provenance_only"] and not row["authored_fields_changed"]
               for row in rows.values())


def test_one_authored_relation_changes_without_sibling_relation_change(indexed):
    root, db, old = indexed
    data = _pack(root)
    data["relations"][0]["predicate"] = "depends_on"
    _save(root, data)
    new = _commit(root, "edit relation A")
    _index(root, db, new)
    rows = _records(_changes(db, old, new), "relations")
    assert rows["rel:a"]["authored_fields_changed"] is True
    assert rows["rel:a"]["provenance_only"] is False
    assert rows["rel:b"]["provenance_only"] is True


def test_moving_authored_record_between_pack_files_is_explicit(indexed):
    root, db, old = indexed
    data = _pack(root)
    moved = data["claims"].pop(0)
    _save(root, data)
    other = root / ".sensemaking/knowledge/moved.json"
    other.write_text(json.dumps({"schema_version": 1, "claims": [moved], "relations": []},
                                indent=2) + "\n", encoding="utf-8")
    new = _commit(root, "move A to another reviewed pack")
    _index(root, db, new)
    row = _records(_changes(db, old, new))["cap:a"]
    assert row["assessment_status"] == "ASSESSED"
    assert row["authored_fields_changed"] is False
    assert row["authoring_location_changed"] is True
    assert row["provenance_only"] is False


def test_added_and_removed_supporting_reference_are_distinguished(indexed):
    root, db, old = indexed
    data = _pack(root)
    data["claims"][0]["evidence_refs"].append("file:src/b.py")
    _save(root, data)
    middle = _commit(root, "add supporting reference")
    _index(root, db, middle)
    added = _records(_changes(db, old, middle))["cap:a"]
    assert added["authored_fields_changed"] is True
    assert {"path": "src/b.py", "change": "reference_added"} in added["changed_supporting_sources"]

    data["claims"][0]["evidence_refs"].remove("file:src/b.py")
    _save(root, data)
    latest = _commit(root, "remove supporting reference")
    _index(root, db, latest)
    removed = _records(_changes(db, middle, latest))["cap:a"]
    assert {"path": "src/b.py", "change": "reference_removed"} in removed["changed_supporting_sources"]


def test_missing_fingerprint_is_not_assessed(indexed):
    root, db, old = indexed
    (root / "README.md").write_text("Unrelated source\n", encoding="utf-8")
    new = _commit(root, "new revision")
    _index(root, db, new, omit_a_fingerprint=True)
    row = _records(_changes(db, old, new))["cap:a"]
    assert row["assessment_status"] == "NOT_ASSESSED"
    assert row["authored_fields_changed"] is False
    assert row["authoring_source_changed"] is None
    assert row["changed_supporting_sources"] is None
    assert row["provenance_only"] is None
    assert row["unassessed_reason"] == "source_fingerprints_unavailable"


def test_missing_origin_fingerprint_is_not_assessed(indexed):
    root, db, old = indexed
    (root / "README.md").write_text("Unrelated source\n", encoding="utf-8")
    new = _commit(root, "new revision")
    snapshot = build_knowledge_snapshot(root, repository=REPOSITORY, target_ref=new)
    snapshot = replace(snapshot, claims=tuple(
        replace(claim, attributes={
            **claim.attributes, "source_sha256": {"src/a.py": claim.attributes["source_sha256"]["src/a.py"]},
        }) if claim.id == "cap:a" else claim
        for claim in snapshot.claims
    ))
    store_snapshot(db, snapshot, source_root=root)
    row = _records(_changes(db, old, new))["cap:a"]
    assert row["assessment_status"] == "NOT_ASSESSED"
    assert row["unassessed_reason"] == "authored_container_fingerprint_unavailable"


def test_mechanical_or_non_authored_change_preserves_raw_delta(indexed):
    root, db, old = indexed
    adr = root / "docs/adr/0031-test.md"
    adr.write_text("# ADR 0031: A different title\n\n**Status**: ACCEPTED\n", encoding="utf-8")
    new = _commit(root, "rename ADR title")
    _index(root, db, new)
    result = _changes(db, old, new)
    assert "adr:0031" in result["claim_delta"]["changed"]
    row = _records(result)["adr:0031"]
    assert row["assessment_status"] == "NOT_ASSESSED"
    assert row["authored_fields_changed"] is None
    assert row["provenance_only"] is None


def test_totals_and_truncation_are_pre_limit_and_stable(indexed):
    root, db, old = indexed
    _save(root, _pack(root), indent=4)
    new = _commit(root, "reformat authored pack")
    _index(root, db, new)
    limited = _changes(db, old, new, limit=1)
    all_rows = _changes(db, old, new, limit=250)
    assert limited["truncated"] is True
    assert limited["change_classification"]["truncated"] is True
    assert len(limited["change_classification"]["claims"]) == 1
    assert len(limited["change_classification"]["relations"]) == 1
    assert limited["change_classification"]["counts"]["claims"]["changed_total"] == 2
    assert limited["change_classification"]["counts"]["relations"]["changed_total"] == 2
    assert all_rows["change_classification"]["counts"] == limited["change_classification"]["counts"]
    assert all_rows["change_classification"]["truncated"] is False
    assert all_rows["claim_delta"]["changed"] == ["cap:a", "cap:b"]
    assert all_rows["relation_delta"]["changed"] == ["rel:a", "rel:b"]


def test_add_remove_ids_are_raw_without_inferred_rename(indexed):
    root, db, old = indexed
    data = _pack(root)
    data["claims"][0]["id"] = "cap:renamed"
    data["relations"][0]["subject"] = "cap:renamed"
    data["relations"][1]["object"] = "cap:renamed"
    _save(root, data)
    new = _commit(root, "rename authored identity")
    _index(root, db, new)
    result = _changes(db, old, new)
    assert "cap:a" in result["claim_delta"]["removed"]
    assert "cap:renamed" in result["claim_delta"]["added"]
    assert "cap:a" not in _records(result)
    assert "cap:renamed" not in _records(result)
    assert any("renames" in note.lower() for note in result["change_classification"]["explicit_limits"])


def test_old_snapshot_readable_and_cli_response_additive(indexed):
    root, db, old = indexed
    data = _pack(root)
    data["claims"][0]["statement"] += " revised"
    _save(root, data)
    new = _commit(root, "edited source")
    _index(root, db, new)
    before = query_knowledge(db, repository=REPOSITORY, target_ref=old, operation="snapshot")
    assert before["counts"]["claims"] >= 2
    result = CliRunner().invoke(cli, [
        "semantic", "knowledge-query", "--db", str(db),
        "--repository", REPOSITORY, "--target-ref", new,
        "--operation", "changes", "--base-ref", old, "--json",
    ])
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "SEMANTIC_KNOWLEDGE_QUERY"
    assert payload["claim_delta"]["changed"] == ["cap:a", "cap:b"]
    assert payload["change_classification"]["counts"]["claims"]["changed_total"] == 2
    assert not payload["semantic_truth_established"] and not payload["action_authorized"]
