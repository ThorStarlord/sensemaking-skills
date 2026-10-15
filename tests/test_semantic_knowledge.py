"""Epistemic stewardship tests: exact source, durable history, no fake authority."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

from sensemaking_skills.cli import cli
from sensemaking_skills.semantic_architecture.knowledge import (
    KnowledgeClaim, KnowledgeRelation, KnowledgeSnapshot, validate_snapshot,
)
from sensemaking_skills.semantic_architecture.knowledge_sources import build_knowledge_snapshot
from sensemaking_skills.semantic_architecture.knowledge_store import audit_knowledge_sources, query_knowledge, store_snapshot


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True, stderr=subprocess.PIPE).strip()


def commit(root: Path, message: str) -> str:
    git(root, "add", "-A")
    git(root, "commit", "-qm", message)
    return git(root, "rev-parse", "HEAD")


def authored_data() -> dict:
    doc = "docs/adr/0031-stewardship.md"
    src = "src/replay.py"
    return {
        "schema_version": 1,
        "claims": [
            {"id": "goal:continuity", "kind": "goal", "statement": "Knowledge should outlive one coding session",
             "authority_kind": "policy", "authority_ref": doc, "evidence_refs": [f"file:{doc}"]},
            {"id": "cap:replay", "kind": "capability", "statement": "A later agent can replay event history",
             "authority_kind": "policy", "authority_ref": doc, "evidence_refs": [f"file:{doc}"]},
            {"id": "inv:ordering", "kind": "invariant", "statement": "Authoritative revisions must win",
             "authority_kind": "policy", "authority_ref": doc, "evidence_refs": [f"file:{doc}"]},
            {"id": "component:replay", "kind": "component", "statement": "Replay implementation path",
             "epistemic_status": "observed", "authority_kind": "code", "authority_ref": src,
             "evidence_refs": [f"file:{src}:line:1"]},
            {"id": "decision:obsolete", "kind": "decision", "statement": "Previously considered arrival ordering",
             "epistemic_status": "superseded", "authority_kind": "policy", "authority_ref": doc,
             "evidence_refs": [f"file:{doc}"]},
        ],
        "relations": [
            {"id": "edge:goal", "subject": "cap:replay", "predicate": "serves_goal",
             "object": "goal:continuity", "evidence_refs": [f"file:{doc}"]},
            {"id": "edge:constraint", "subject": "cap:replay", "predicate": "constrained_by",
             "object": "inv:ordering", "evidence_refs": [f"file:{doc}"]},
            {"id": "edge:implemented", "subject": "cap:replay", "predicate": "implemented_by",
             "object": "component:replay", "evidence_refs": [f"file:{src}"]},
            {"id": "edge:decision", "subject": "cap:replay", "predicate": "decided_by",
             "object": "adr:0031", "evidence_refs": [f"file:{doc}"]},
            {"id": "edge:contradiction", "subject": "inv:ordering", "predicate": "contradicts",
             "object": "decision:obsolete", "epistemic_status": "contested",
             "evidence_refs": [f"file:{doc}"]},
        ],
    }


@pytest.fixture
def repo(tmp_path: Path) -> tuple[Path, str]:
    root = tmp_path / "target"
    root.mkdir()
    git(root, "init", "-q")
    git(root, "config", "user.email", "fixture@example.invalid")
    git(root, "config", "user.name", "Knowledge Fixture")
    for part in [".sensemaking/knowledge", "docs/adr", "src"]:
        (root / part).mkdir(parents=True, exist_ok=True)
    (root / "docs/adr/0031-stewardship.md").write_text(
        "# ADR 0031: Durable stewardship\n\n**Status**: ACCEPTED - owner selected\n"
        "\n## Decision\nChoice: keep intent separate from implementation.\n", encoding="utf-8"
    )
    (root / "src/replay.py").write_text("import json\n# event revision ordering\n", encoding="utf-8")
    (root / ".sensemaking/intent.md").write_text(
        "# Intent\n- Knowledge must be retained. [owner: 2026-10-15]\n"
        "- Unknown product preferences remain hypotheses. [hypothesis]\n", encoding="utf-8"
    )
    (root / ".sensemaking/invariants.md").write_text(
        "- Revisions are authoritative. [policy: docs/adr/0031-stewardship.md]\n"
        "- This citation is absent. [test: tests/missing_test.py]\n", encoding="utf-8"
    )
    (root / ".sensemaking/knowledge/stewardship.json").write_text(
        json.dumps(authored_data(), indent=2), encoding="utf-8"
    )
    return root, commit(root, "init realistic semantic source")


def build(repo: tuple[Path, str], **kwargs) -> KnowledgeSnapshot:
    root, sha = repo
    return build_knowledge_snapshot(
        root, repository="example/product", target_ref=sha, **kwargs
    )


def test_semantic_claims_and_boundaries(repo):
    snap = build(repo)
    validate_snapshot(snap)
    ids = {c.id for c in snap.claims}
    assert {"goal:continuity", "cap:replay", "adr:0031", "inv:ordering"} <= ids
    adr = next(c for c in snap.claims if c.id == "adr:0031")
    assert adr.epistemic_status == "observed"
    assert "keep intent separate" in adr.attributes["verbatim_sections"]["decision"]
    assert adr.attributes["authority_verified"] is False
    owner = next(c for c in snap.claims if c.authority_kind == "owner")
    assert owner.attributes["authority_verified"] is False
    cited_missing = [c for c in snap.claims if c.attributes.get("cited_source_present") is False]
    assert len(cited_missing) == 1
    assert snap.semantic_truth_established is False
    assert snap.action_authorized is False
    assert "absence" in " ".join(snap.limits).lower() or "NOT ASSESSED" in " ".join(snap.limits)


def test_persist_query_impact_why_contradictions(repo, tmp_path):
    snap = build(repo)
    path = tmp_path / "index.sqlite"
    receipt = store_snapshot(path, snap, source_root=repo[0])
    assert receipt["claim_count"] == len(snap.claims) and not receipt["already_indexed"]
    again = store_snapshot(path, snap, source_root=repo[0])
    assert receipt["digest"] == again["digest"] and again["already_indexed"]

    args = {"repository": snap.repository, "target_ref": snap.target_ref}
    explanation = query_knowledge(path, operation="explain", subject="cap:replay", **args)
    assert {"inv:ordering", "goal:continuity", "adr:0031"} <= {c["id"] for c in explanation["claims"]}
    assert any(e["predicate"] == "implemented_by" for e in explanation["relations"])
    assert not explanation["semantic_truth_established"]
    assert not explanation["action_authorized"]
    impact = query_knowledge(path, operation="impact", subject="cap:replay", depth=2, **args)
    assert any(e["predicate"] == "contradicts" for e in impact["relations"])
    assert "CANDIDATES" in impact["impact_limit"]
    why = query_knowledge(path, operation="why", subject="adr:0031", **args)
    assert why["claims"][0]["kind"] == "decision"
    explicit = query_knowledge(path, operation="contradictions", **args)
    assert [e["id"] for e in explicit["relations"]] == ["edge:contradiction"]


def test_query_requires_exact_indexed_revision(repo, tmp_path):
    db = tmp_path / "index.db"
    snap = build(repo)
    store_snapshot(db, snap, source_root=repo[0])
    with pytest.raises(ValueError, match="not been indexed"):
        query_knowledge(db, repository=snap.repository, target_ref="f" * 40, operation="snapshot")
    with pytest.raises(ValueError, match="decision"):
        query_knowledge(db, repository=snap.repository, target_ref=snap.target_ref,
                        operation="why", subject="cap:replay")
    with pytest.raises(ValueError, match="NOT ASSESSED"):
        query_knowledge(db, repository=snap.repository, target_ref=snap.target_ref,
                        operation="impact", subject="cap:unknown")


def test_multiple_revisions_preserve_history_and_cited_source_drift(repo, tmp_path):
    root, old_sha = repo
    db = tmp_path / "index.sqlite"
    first = build(repo)
    store_snapshot(db, first, source_root=root)
    (root / "src/replay.py").write_text("import json\n# new algorithm, same capability wording\n", encoding="utf-8")
    newer_sha = commit(root, "change implementation evidence")
    second = build((root, newer_sha))
    store_snapshot(db, second, source_root=root)
    old = query_knowledge(db, repository=first.repository, target_ref=old_sha,
                          operation="explain", subject="component:replay")
    new = query_knowledge(db, repository=second.repository, target_ref=newer_sha,
                          operation="explain", subject="component:replay")
    assert old["claims"][0]["attributes"]["source_sha256"] != new["claims"][0]["attributes"]["source_sha256"]
    changes = query_knowledge(db, repository=second.repository, target_ref=newer_sha,
                              operation="changes", base_ref=old_sha)
    assert "component:replay" in changes["claim_delta"]["changed"]
    assert "edge:implemented" in changes["relation_delta"]["changed"]
    hist = query_knowledge(db, repository=second.repository, target_ref=newer_sha,
                           operation="history", subject="component:replay")
    assert [h["revision"] for h in hist["claim_history"]] == [old_sha, newer_sha]
    assert "not proven Git ancestry" in hist["history_limit"]


def test_authored_owner_authority_cannot_self_verify(repo):
    root, _ = repo
    p = root / ".sensemaking/knowledge/stewardship.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["claims"][0]["attributes"] = {"authority_verified": True}
    p.write_text(json.dumps(data), encoding="utf-8")
    sha = commit(root, "fabricated authority")
    with pytest.raises(ValueError, match="verified authority"):
        build((root, sha))


def test_authored_relation_cannot_masquerade_as_mechanical(repo):
    root, _ = repo
    p = root / ".sensemaking/knowledge/stewardship.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["relations"][0]["derivation"] = "mechanical"
    p.write_text(json.dumps(data), encoding="utf-8")
    sha = commit(root, "false derivation")
    with pytest.raises(ValueError, match="cannot claim mechanical"):
        build((root, sha))


def test_dangling_authored_source_fails_closed(repo):
    root, _ = repo
    p = root / ".sensemaking/knowledge/stewardship.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["claims"][0]["evidence_refs"] = ["file:../../outside.md"]
    p.write_text(json.dumps(data), encoding="utf-8")
    sha = commit(root, "invalid source")
    with pytest.raises(ValueError, match="not tracked"):
        build((root, sha))


def test_untracked_dirty_and_wrong_head_fails_closed(repo):
    root, sha = repo
    with pytest.raises(ValueError, match="target_ref"):
        build_knowledge_snapshot(root, repository="demo", target_ref="not-a-sha")
    with pytest.raises(ValueError, match="does not equal"):
        build_knowledge_snapshot(root, repository="demo", target_ref="a" * 40)
    (root / "rogue.txt").write_text("injected untracked source", encoding="utf-8")
    with pytest.raises(ValueError, match="dirty"):
        build(repo)


def test_deterministic_reconstruction_and_no_index_inside_repo(repo, tmp_path):
    root, _ = repo
    first = build(repo)
    second = build(repo)
    assert first == second
    with pytest.raises(ValueError, match="outside"):
        store_snapshot(root / "knowledge.sqlite", first, source_root=root)
    db = tmp_path / "evidence.sqlite"
    receipt = store_snapshot(db, first, source_root=root)
    assert receipt["digest"] == store_snapshot(db, second, source_root=root)["digest"]
    assert not git(root, "status", "--porcelain")


def test_opt_in_imports_are_syntax_only_and_limited(repo):
    snap = build(repo, include_python_imports=True, max_imports=1)
    assert any(c.kind == "source" for c in snap.claims)
    assert any(r.predicate == "references" and r.derivation == "mechanical" for r in snap.relations)
    assert not any(r.predicate == "depends_on" for r in snap.relations)


def test_no_relationship_inferred_from_cooccurrence(repo, tmp_path):
    snap = build(repo)
    assert all(e.predicate != "depends_on" for e in snap.relations)
    db = tmp_path / "index.sqlite"
    store_snapshot(db, snap, source_root=repo[0])
    result = query_knowledge(db, repository=snap.repository, target_ref=snap.target_ref,
                             operation="search", subject="replay")
    assert result["relations"] == []
    assert result["claims"]


def test_cannot_change_snapshot_for_same_sha(repo, tmp_path):
    snap = build(repo)
    db = tmp_path / "index.sqlite"
    store_snapshot(db, snap, source_root=repo[0])
    modified = KnowledgeSnapshot(
        repository=snap.repository, target_ref=snap.target_ref,
        claims=(*snap.claims, KnowledgeClaim(
            id="hyp:new", kind="hypothesis", statement="I made this up",
            epistemic_status="hypothetical", authority_kind="hypothesis",
            authority_ref="hypothesis", source_ref="file:README.md",
            evidence_refs=("file:README.md",),
        )), relations=snap.relations,
        source_scope=snap.source_scope, limits=snap.limits,
    )
    with pytest.raises(ValueError, match="conflicting content"):
        store_snapshot(db, modified, source_root=repo[0])


def test_cli_build_then_query(repo, tmp_path):
    root, sha = repo
    db = tmp_path / "index.db"
    runner = CliRunner()
    made = runner.invoke(cli, [
        "semantic", "knowledge-build", "--repo", str(root),
        "--repository", "example/product", "--target-ref", sha,
        "--db", str(db), "--json",
    ])
    assert made.exit_code == 0, made.output
    payload = json.loads(made.output)
    assert payload["code"] == "SEMANTIC_KNOWLEDGE_INDEXED"
    queried = runner.invoke(cli, [
        "semantic", "knowledge-query", "--db", str(db),
        "--repository", "example/product", "--target-ref", sha,
        "--operation", "why", "--subject", "adr:0031", "--json",
    ])
    assert queried.exit_code == 0, queried.output
    q = json.loads(queried.output)
    assert q["claims"][0]["id"] == "adr:0031"
    assert q["action_authorized"] is False


def test_cli_dirty_checkout_reports_error(repo, tmp_path):
    root, sha = repo
    (root / "src/replay.py").write_text("modified\n", encoding="utf-8")
    r = CliRunner().invoke(cli, [
        "semantic", "knowledge-build", "--repo", str(root),
        "--repository", "demo", "--target-ref", sha,
        "--db", str(tmp_path / "k.db"), "--json",
    ])
    assert r.exit_code != 0
    assert "dirty" in r.output


def test_relationship_integrity_rejects_unbound_endpoints(repo):
    snap = build(repo)
    bad = KnowledgeRelation(
        id="edge:bad", subject="nonexistent:xyz", predicate="tested_by",
        object="cap:replay", epistemic_status="declared", derivation="authored",
        source_ref="file:docs/adr/0031-stewardship.md", evidence_refs=("file:docs/adr/0031-stewardship.md",),
    )
    tampered = KnowledgeSnapshot(
        repository=snap.repository, target_ref=snap.target_ref,
        claims=snap.claims, relations=(*snap.relations, bad),
        source_scope=snap.source_scope, limits=snap.limits,
    )
    with pytest.raises(ValueError, match="endpoint"):
        validate_snapshot(tampered)



def test_read_only_source_drift_audit_across_two_revisions(repo, tmp_path):
    root, original_sha = repo
    db = tmp_path / "knowledge.db"
    snapshot = build(repo)
    store_snapshot(db, snapshot, source_root=root)
    same = audit_knowledge_sources(
        db, repository=snapshot.repository, indexed_ref=original_sha,
        current_repo_root=root, current_ref=original_sha,
    )
    assert same["source_status_counts"]["source_changed"] == 0
    assert same["source_status_counts"]["source_missing_or_unsafe"] == 0

    (root / "src/replay.py").write_text("import json\n# new implementation\n", encoding="utf8")
    current_sha = commit(root, "change replay")
    found = audit_knowledge_sources(
        db, repository=snapshot.repository, indexed_ref=original_sha,
        current_repo_root=root, current_ref=current_sha,
    )
    assert found["source_status_counts"]["source_changed"] >= 2
    assert any(r["id"] == "component:replay" for r in found["affected_records"])
    assert not found["semantic_truth_established"]
    assert not found["action_authorized"]

    (root / "src/replay.py").unlink()
    newest = commit(root, "remove replay module")
    missing = audit_knowledge_sources(
        db, repository=snapshot.repository, indexed_ref=original_sha,
        current_repo_root=root, current_ref=newest,
    )
    assert missing["source_status_counts"]["source_missing_or_unsafe"] >= 2
    assert any(r["id"] == "component:replay" and "src/replay.py" in r["missing_or_unsafe_sources"]
               for r in missing["affected_records"])


def test_cli_source_audit_after_new_commit(repo, tmp_path):
    root, previous = repo
    db = tmp_path / "index.db"
    store_snapshot(db, build(repo), source_root=root)
    (root / "src/replay.py").write_text("import json\n# now different\n", encoding="utf-8")
    current = commit(root, "change evidence")
    r = CliRunner().invoke(cli, [
        "semantic", "knowledge-audit", "--db", str(db),
        "--repo", str(root), "--repository", "example/product",
        "--indexed-ref", previous, "--current-ref", current, "--json",
    ])
    assert r.exit_code == 0, r.output
    payload = json.loads(r.output)
    assert payload["code"] == "SEMANTIC_KNOWLEDGE_SOURCE_AUDIT"
    assert payload["source_status_counts"]["source_changed"] > 0
