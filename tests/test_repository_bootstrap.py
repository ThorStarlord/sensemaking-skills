"""Executable read-only repository bootstrap and structural-knowledge contracts."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

from sensemaking_skills.cli import cli
from sensemaking_skills.semantic_architecture.knowledge import stable_id, validate_snapshot
from sensemaking_skills.semantic_architecture.knowledge_sources import (
    build_knowledge_snapshot, verified_tracked_sources,
)
from sensemaking_skills.semantic_architecture.knowledge_store import (
    audit_knowledge_sources, query_knowledge, store_snapshot,
)
from sensemaking_skills.semantic_architecture.repository_bootstrap import (
    orient_repository, structural_records,
)


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=root, text=True, stderr=subprocess.PIPE
    ).strip()


def commit(root: Path, reason: str) -> str:
    git(root, "add", "-A")
    git(root, "commit", "-qm", reason)
    return git(root, "rev-parse", "HEAD")


@pytest.fixture
def target(tmp_path: Path) -> tuple[Path, str]:
    root = tmp_path / "product"
    root.mkdir()
    git(root, "init", "-q")
    git(root, "config", "user.name", "Bootstrap Test")
    git(root, "config", "user.email", "bootstrap@example.invalid")
    for directory in ["src/app", "tests", "docs/adr", ".sensemaking/knowledge", "frontend"]:
        (root / directory).mkdir(parents=True, exist_ok=True)
    (root / "README.md").write_text("# A product\n", encoding="utf-8")
    (root / "docs/product-strategy.md").write_text("# Strategy\n", encoding="utf-8")
    (root / "docs/adr/0031-stewardship.md").write_text(
        "# ADR 0031: Keep history\n\n**Status:** Accepted\n", encoding="utf-8"
    )
    (root / ".sensemaking/intent.md").write_text(
        "- Long-lived knowledge [owner: 2026-10-15]\n", encoding="utf-8"
    )
    (root / "src/app/__init__.py").write_text("", encoding="utf-8")
    (root / "src/app/service.py").write_text("import json\n", encoding="utf-8")
    (root / "tests/test_service.py").write_text("import json\n", encoding="utf-8")
    (root / "frontend/page.tsx").write_text("export default function Home() {}\n", encoding="utf-8")
    (root / "pyproject.toml").write_text(
        "[project]\nname = 'sample'\nversion = '0.0.1'\n", encoding="utf-8"
    )
    return root, commit(root, "initial fixture")


def snapshot(target: tuple[Path, str], **kwargs):
    root, sha = target
    return build_knowledge_snapshot(
        root, repository="example/product", target_ref=sha, **kwargs
    )


def test_orientation_is_pinned_bounded_and_non_authoritative(target):
    root, sha = target
    valid, tracked = verified_tracked_sources(root, sha)
    result = orient_repository(valid, tracked, repository="example/product", target_ref=sha)
    assert result["repository"] == "example/product"
    assert result["target_ref"] == sha
    assert set(result["entry_documents"]) == {
        "README.md", "docs/product-strategy.md", ".sensemaking/intent.md",
    }
    assert "pyproject.toml" in result["manifest_examples"]
    assert "src/app/service.py" in result["source_examples"]
    assert "tests/test_service.py" in result["test_examples"]
    assert result["language_file_counts"]["TypeScript"] == 1
    assert result["adr_path_count"] == 1
    assert result["semantic_truth_established"] is False
    assert result["action_authorized"] is False
    assert "NOT ASSESSED" in " ".join(result["limits"])


def test_bounded_orientation_reports_partial_scope(target):
    root, sha = target
    valid, tracked = verified_tracked_sources(root, sha)
    result = orient_repository(valid, tracked, repository="example/product",
                               target_ref=sha, max_files=2, sample_limit=1)
    assert result["path_inventory_truncated"]
    assert result["inspected_file_count"] == 2
    assert len(result["top_level"]) == 1
    assert result["eligible_file_count"] > 2
    with pytest.raises(ValueError, match="max_files"):
        orient_repository(valid, tracked, repository="example/product", target_ref=sha, max_files=0)


def test_opt_in_structure_preserves_epistemics_and_fingerprints(target, tmp_path):
    root, sha = target
    snap = snapshot(target, include_repository_structure=True, include_python_imports=True)
    validate_snapshot(snap)
    service_id = stable_id("file", "src/app/service.py")
    dir_id = stable_id("directory", "src/app")
    service = next(c for c in snap.claims if c.id == service_id)
    assert service.kind == "source"
    assert service.epistemic_status == "observed"
    assert service.authority_kind == "mechanical"
    assert service.attributes["authority_verified"] is False
    assert service.attributes["source_sha256"]["src/app/service.py"]
    assert sum(c.id == service_id for c in snap.claims) == 1
    assert next(c for c in snap.claims if c.id == dir_id).kind == "directory"
    assert not any(c.kind == "component" and c.authority_kind == "mechanical" for c in snap.claims)
    assert any(r.subject == service_id and r.object == dir_id
               and r.predicate == "contained_in" and r.derivation == "mechanical"
               for r in snap.relations)
    assert any(r.subject == service_id and r.predicate == "references"
               for r in snap.relations)
    assert not any(r.predicate in {"depends_on", "implemented_by", "tested_by"}
                   and r.derivation == "mechanical" for r in snap.relations)
    assert snap.action_authorized is False and snap.semantic_truth_established is False
    db = tmp_path / "index.sqlite"
    store_snapshot(db, snap, source_root=root)
    out = query_knowledge(db, repository=snap.repository, target_ref=sha,
                          operation="explain", subject=service_id)
    assert any(r["predicate"] == "contained_in" for r in out["relations"])


def test_structure_is_deterministic_and_truncation_is_explicit(target):
    root, sha = target
    base = snapshot(target, include_repository_structure=True, max_structural_files=1)
    other = snapshot(target, include_repository_structure=True, max_structural_files=1)
    assert base == other
    assert any("truncated" in limitation for limitation in base.limits)
    assert len([c for c in base.claims if c.attributes.get("scope") == "committed file existence, not content semantics"]) == 1
    _, tracked = verified_tracked_sources(root, sha)
    with pytest.raises(ValueError, match="max_structural_files"):
        structural_records(root, tracked, max_structural_files=0)


def test_history_preserves_changed_source_without_inferred_effect(target, tmp_path):
    root, sha = target
    db = tmp_path / "knowledge.db"
    old = snapshot(target, include_repository_structure=True)
    store_snapshot(db, old, source_root=root)
    (root / "src/app/service.py").write_text("import json\n# revised behavior\n", encoding="utf-8")
    next_sha = commit(root, "new implementation")
    new = snapshot((root, next_sha), include_repository_structure=True)
    store_snapshot(db, new, source_root=root)
    source_id = stable_id("file", "src/app/service.py")
    previous = next(c for c in old.claims if c.id == source_id)
    current = next(c for c in new.claims if c.id == source_id)
    assert previous.attributes["source_sha256"] != current.attributes["source_sha256"]
    changes = query_knowledge(db, repository="example/product", target_ref=next_sha,
                              operation="changes", base_ref=sha)
    assert source_id in changes["claim_delta"]["changed"]
    history = query_knowledge(db, repository="example/product", target_ref=next_sha,
                              operation="history", subject=source_id)
    assert len(history["claim_history"]) == 2
    audited = audit_knowledge_sources(db, repository="example/product", indexed_ref=sha,
                                      current_repo_root=root, current_ref=next_sha)
    assert audited["source_status_counts"]["source_changed"] > 0


def test_cli_orient_and_build_with_existing_index(target, tmp_path):
    root, sha = target
    db = tmp_path / "knowledge.db"
    runner = CliRunner()
    created = runner.invoke(cli, [
        "semantic", "knowledge-build", "--repo", str(root), "--repository", "example/product",
        "--target-ref", sha, "--db", str(db), "--include-repository-structure",
        "--include-python-imports", "--json",
    ])
    assert created.exit_code == 0, created.output
    assert json.loads(created.output)["code"] == "SEMANTIC_KNOWLEDGE_INDEXED"
    orient = runner.invoke(cli, [
        "semantic", "knowledge-orient", "--repo", str(root),
        "--repository", "example/product", "--target-ref", sha,
        "--db", str(db), "--json",
    ])
    assert orient.exit_code == 0, orient.output
    payload = json.loads(orient.output)
    assert payload["code"] == "SEMANTIC_REPOSITORY_ORIENTATION"
    assert payload["knowledge_index"]["counts"]["claims"] >= 3
    assert payload["knowledge_index"]["semantic_truth_established"] is False
    queried = runner.invoke(cli, [
        "semantic", "knowledge-query", "--db", str(db),
        "--repository", "example/product", "--target-ref", sha,
        "--operation", "search", "--subject", "src/app/service.py", "--json",
    ])
    assert queried.exit_code == 0, queried.output
    assert json.loads(queried.output)["claims"]


def test_clean_checkout_guard_and_no_mutation(target, tmp_path):
    root, sha = target
    runner = CliRunner()
    before = git(root, "status", "--porcelain", "--untracked-files=all")
    orient = runner.invoke(cli, [
        "semantic", "knowledge-orient", "--repo", str(root), "--repository", "example/product",
        "--target-ref", sha, "--json",
    ])
    assert orient.exit_code == 0, orient.output
    assert git(root, "status", "--porcelain", "--untracked-files=all") == before == ""
    (root / "untracked.txt").write_text("not part of pinned HEAD", encoding="utf-8")
    dirty = runner.invoke(cli, [
        "semantic", "knowledge-orient", "--repo", str(root), "--repository", "example/product",
        "--target-ref", sha, "--json",
    ])
    assert dirty.exit_code != 0
    assert "dirty or untracked" in dirty.output
    with pytest.raises(ValueError, match="dirty or untracked"):
        snapshot(target, include_repository_structure=True)


def test_symlink_evidence_fails_closed(target, tmp_path):
    root, sha = target
    outside = tmp_path / "outside.py"
    outside.write_text("SECRET = 42\n", encoding="utf-8")
    link = root / "src/app/hidden.py"
    try:
        os.symlink(outside, link)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation not supported")
    altered = commit(root, "link to external path")
    with pytest.raises(ValueError, match="symlink"):
        snapshot((root, altered), include_repository_structure=True)


def test_non_python_source_is_observed_without_inferred_semantics(target):
    snap = snapshot(target, include_repository_structure=True)
    assert not any("syntax" in scope.lower() for scope in snap.source_scope)
    node = next(c for c in snap.claims if c.id == stable_id("file", "frontend/page.tsx"))
    assert node.kind == "source" and node.authority_kind == "mechanical"
    assert not any(r.predicate in {"depends_on", "implemented_by", "tested_by"}
                   for r in snap.relations)
    assert all(not r.attributes.get("authority_verified", False) for r in snap.relations)


def test_auteur_entry_docs_and_three_digit_adrs(target):
    root, _ = target
    (root / "MISSION.md").write_text("# Mission\n", encoding="utf-8")
    (root / "docs/narrative-architecture.md").write_text("# Architecture\n", encoding="utf-8")
    (root / "docs/adr/019-map.md").write_text(
        "# ADR 019: Map authority\n\n**Status:** Accepted\n", encoding="utf-8"
    )
    sha = commit(root, "add Auteur-shaped documents")
    valid, tracked = verified_tracked_sources(root, sha)
    oriented = orient_repository(valid, tracked, repository="example/product", target_ref=sha)
    assert "MISSION.md" in oriented["entry_documents"]
    assert "docs/narrative-architecture.md" in oriented["entry_documents"]
    snap = snapshot((root, sha))
    adr = next(c for c in snap.claims if c.id == "adr:019")
    assert "Map authority" in adr.statement
    assert adr.source_ref == "file:docs/adr/019-map.md:line:1"


def test_proposal_check_accepts_dirty_untracked_draft_but_does_not_index_it(target):
    from sensemaking_skills.semantic_architecture.stewardship_validation import inspect_knowledge_proposal

    root, sha = target
    proposal = root / ".sensemaking/knowledge/proposed.json"
    proposal.write_text(json.dumps({
        "schema_version": 1,
        "claims": [{
            "id": "cap:book-reentry", "kind": "capability",
            "statement": "Book re-entry is a proposed capability",
            "authority_kind": "document",
            "authority_ref": "docs/adr/0031-stewardship.md",
            "evidence_refs": ["file:docs/adr/0031-stewardship.md"],
        }],
        "relations": [{
            "id": "rel:book-adr", "subject": "cap:book-reentry",
            "predicate": "decided_by", "object": "adr:0031",
            "evidence_refs": ["file:docs/adr/0031-stewardship.md"],
        }],
    }), encoding="utf-8")
    response = inspect_knowledge_proposal(root, proposal)
    assert response["code"] == "SEMANTIC_KNOWLEDGE_PROPOSAL_VALID"
    assert response["head_sha"] == sha
    assert response["worktree_clean"] is False
    assert response["existing_endpoints_checked"] == 1
    assert response["semantic_truth_established"] is False
    runner = CliRunner()
    cli_out = runner.invoke(cli, [
        "semantic", "knowledge-proposal-check", "--repo", str(root),
        "--proposal", str(proposal), "--json",
    ])
    assert cli_out.exit_code == 0, cli_out.output
    assert json.loads(cli_out.output)["valid"] is True
    assert git(root, "rev-parse", "HEAD") == sha


def test_proposal_check_rejects_missing_evidence_and_unknown_relation(target):
    from sensemaking_skills.semantic_architecture.stewardship_validation import inspect_knowledge_proposal

    root, _ = target
    path = root / ".sensemaking/knowledge/draft.json"
    candidate = {
        "schema_version": 1,
        "claims": [{"id": "cap:draft", "kind": "capability", "statement": "Proposed",
                    "authority_kind": "hypothesis", "authority_ref": "hypothesis",
                    "evidence_refs": ["file:missing-source.py"]}],
        "relations": [],
    }
    path.write_text(json.dumps(candidate), encoding="utf-8")
    with pytest.raises(ValueError, match="not Git-tracked|missing|tracked"):
        inspect_knowledge_proposal(root, path)
    candidate["claims"][0]["evidence_refs"] = ["file:README.md"]
    candidate["relations"] = [{
        "id": "edge:missing", "subject": "cap:draft", "predicate": "references",
        "object": "component:not-real", "evidence_refs": ["file:README.md"],
    }]
    path.write_text(json.dumps(candidate), encoding="utf-8")
    with pytest.raises(ValueError, match="unresolved relationship endpoint"):
        inspect_knowledge_proposal(root, path)

