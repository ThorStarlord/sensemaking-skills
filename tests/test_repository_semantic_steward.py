"""Repository Semantic Steward: packaging and revision-lifecycle contracts.

These are mechanical same-context tests. They do not qualify independent-agent
knowledge reuse, real-world value, or automatic architectural interpretation.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import yaml
from click.testing import CliRunner

from sensemaking_skills.cli import cli

from sensemaking_skills.semantic_architecture.knowledge_sources import build_knowledge_snapshot
from sensemaking_skills.semantic_architecture.knowledge_store import (
    audit_knowledge_sources, query_knowledge, store_snapshot,
)
from sensemaking_skills.semantic_architecture.stewardship_validation import inspect_knowledge_proposal

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "repository-semantic-steward"


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=root, text=True, stderr=subprocess.PIPE,
    ).strip()


def _commit(root: Path, message: str) -> str:
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", message)
    return _git(root, "rev-parse", "HEAD")


def test_steward_skill_registered_and_compact():
    content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = yaml.safe_load(content.split("---", 2)[1])
    assert frontmatter["name"] == "repository-semantic-steward"
    for term in ["BOOTSTRAP", "RECALL", "RECONCILE", "AUDIT", "messy", "independent"]:
        assert term.lower() in content.lower()
    meta = yaml.safe_load((SKILL / "agents/openai.yaml").read_text(encoding="utf-8"))
    assert meta["interface"]["display_name"] == "Repository Semantic Steward"
    for name in (
        "bootstrap.md", "recall.md", "reconciliation.md",
        "knowledge-contract.md", "schema-evolution.md", "qualification.md",
    ):
        assert (SKILL / "references" / name).is_file()
        assert f"(references/{name})" in content
    registry = yaml.safe_load(
        (ROOT / "skills/workflow-planner/references/skill-registry.yaml").read_text(encoding="utf-8")
    )
    entries = [s for eco in registry["ecosystems"].values() for s in eco["skills"]]
    entry = next(s for s in entries if s["id"] == "repository-semantic-steward")
    assert entry["availability"]["executable_by_orchestrator"] is False
    assert entry["availability"]["requires_installed_skill"] is True
    assert "artifact" not in entry
    release = yaml.safe_load((ROOT / "release-v1.0.yaml").read_text(encoding="utf-8"))
    assert "repository-semantic-steward" in release["skill_inventory"]["internal"]


def test_steward_self_repository_recall_and_index_guidance():
    """Doc contracts match source-pinned recall rather than mandating a fresh checkout."""
    control = (ROOT / "skills/using-sensemaking/SKILL.md").read_text(encoding="utf-8")
    steward = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    recall = (SKILL / "references/recall.md").read_text(encoding="utf-8")
    evidence = json.loads((ROOT / ".sensemaking/knowledge/stewardship.json").read_text(encoding="utf-8"))
    assert "Sensemaking Skills itself" in control
    assert "NO_MODEL_CHANGE" in control
    assert "`knowledge-query --repo .`" in steward
    assert "clean checked-out" in steward
    assert "dirty active checkout" in steward
    assert "source" in recall.lower()
    claim = next(c for c in evidence["claims"] if c["id"] == "inv:index-snapshot-vs-working-overlay")
    assert claim["kind"] == "invariant"
    assert all((ROOT / p.removeprefix("file:")).is_file() for p in claim["evidence_refs"])
    assert any(
        rel["subject"] == "cap:semantic-queries"
        and rel["object"] == claim["id"]
        and rel["predicate"] == "constrained_by"
        for rel in evidence["relations"]
    )

def test_stewardship_revision_lifecycle_and_currentness(tmp_path: Path):
    root = tmp_path / "auteur-like"
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "steward@example.invalid")
    _git(root, "config", "user.name", "Steward Test")
    for name in ["src", "docs/adr", ".sensemaking/knowledge"]:
        (root / name).mkdir(parents=True, exist_ok=True)
    (root / "MISSION.md").write_text("# Mission\nKeep explicit author authority.\n", encoding="utf-8")
    (root / "docs/adr/019-map.md").write_text(
        "# ADR 019: Derived Map\n\n**Status:** Accepted\n"
        "\n## Decision\nDerived maps do not accept story changes.\n", encoding="utf-8",
    )
    (root / "src/studio.js").write_text("export function openBook() { return 'working'; }\n", encoding="utf-8")
    first = _commit(root, "first committed product")
    db = tmp_path / "semantic.sqlite"
    initial = build_knowledge_snapshot(
        root, repository="example/auteur", target_ref=first,
        include_repository_structure=True,
    )
    store_snapshot(db, initial, source_root=root)
    assert any(c.id == "adr:019" for c in initial.claims)
    assert any(c.statement == "src/studio.js" for c in initial.claims)

    candidate = root / ".sensemaking/knowledge/book.json"
    candidate_data = {
        "schema_version": 1,
        "claims": [
            {"id": "goal:author-control", "kind": "goal", "statement": "Authors control acceptance",
             "authority_kind": "policy", "authority_ref": "MISSION.md",
             "evidence_refs": ["file:MISSION.md"]},
            {"id": "cap:book-reentry", "kind": "capability", "statement": "Book re-entry is explicit",
             "authority_kind": "document", "authority_ref": "docs/adr/019-map.md",
             "evidence_refs": ["file:docs/adr/019-map.md"]},
            {"id": "component:studio", "kind": "component", "statement": "Studio serves working Book state",
             "epistemic_status": "observed", "authority_kind": "code",
             "authority_ref": "src/studio.js", "evidence_refs": ["file:src/studio.js"]},
        ],
        "relations": [
            {"id": "rel:reentry-implementation", "subject": "cap:book-reentry",
             "predicate": "implemented_by", "object": "component:studio",
             "evidence_refs": ["file:src/studio.js"]},
            {"id": "rel:reentry-authority", "subject": "cap:book-reentry",
             "predicate": "constrained_by", "object": "goal:author-control",
             "evidence_refs": ["file:MISSION.md"]},
        ],
    }
    candidate.write_text(json.dumps(candidate_data, indent=2), encoding="utf-8")
    checked = inspect_knowledge_proposal(root, candidate)
    assert checked["valid"] is True and checked["worktree_clean"] is False
    assert checked["semantic_truth_established"] is False
    second = _commit(root, "reviewed initial semantic memory")
    middle = build_knowledge_snapshot(root, repository="example/auteur", target_ref=second)
    store_snapshot(db, middle, source_root=root)
    result = query_knowledge(
        db, repository="example/auteur", target_ref=second,
        operation="explain", subject="cap:book-reentry",
    )
    assert any(edge["predicate"] == "implemented_by" for edge in result["relations"])

    (root / "src/studio.js").write_text(
        "export function openBook() { return 'working-revised'; }\n",
        encoding="utf-8",
    )
    third = _commit(root, "change source without rewriting knowledge")
    after = build_knowledge_snapshot(root, repository="example/auteur", target_ref=third)
    store_snapshot(db, after, source_root=root)
    audited = audit_knowledge_sources(
        db, repository="example/auteur", indexed_ref=second,
        current_repo_root=root, current_ref=third,
    )
    assert audited["source_status_counts"]["source_changed"] >= 1
    changed = query_knowledge(
        db, repository="example/auteur", target_ref=third,
        operation="changes", base_ref=second,
    )
    assert "component:studio" in changed["claim_delta"]["changed"]
    assert any(c.id == "cap:book-reentry" for c in after.claims)
    assert after.semantic_truth_established is False


def test_steward_cli_uses_committed_knowledge_from_dirty_active_workspace(tmp_path: Path):
    root = tmp_path / "book-project"
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "steward@example.invalid")
    _git(root, "config", "user.name", "Steward Test")
    (root / "docs/adr").mkdir(parents=True)
    (root / ".sensemaking/knowledge").mkdir(parents=True)
    (root / "MISSION.md").write_text("# Product\nAuthor controls acceptance.\n", encoding="utf-8")
    (root / "docs/adr/019-book.md").write_text(
        "# ADR 019: Book re-entry\n\n**Status:** Accepted\n", encoding="utf-8",
    )
    records = {
        "schema_version": 1,
        "claims": [{
            "id": "cap:book-reentry", "kind": "capability",
            "statement": "Book re-entry is explicitly author controlled",
            "authority_kind": "policy", "authority_ref": "MISSION.md",
            "evidence_refs": ["file:MISSION.md"],
        }],
        "relations": [],
    }
    (root / ".sensemaking/knowledge/book.json").write_text(
        json.dumps(records), encoding="utf-8",
    )
    sha = _commit(root, "reviewed product knowledge")
    index = tmp_path / "knowledge.sqlite"
    snap = build_knowledge_snapshot(root, repository="example/book", target_ref=sha)
    store_snapshot(index, snap, source_root=root)

    (root / "MISSION.md").write_text("# Product\nChanged but not committed.\n", encoding="utf-8")
    base = [
        "semantic", "knowledge-query", "--db", str(index),
        "--repository", "example/book", "--target-ref", sha, "--json",
    ]
    runner = CliRunner()
    search = runner.invoke(cli, base + [
        "--operation", "search", "--term", "book re-entry", "--term", "author",
        "--repo", str(root),
    ])
    assert search.exit_code == 0, search.output
    search_payload = json.loads(search.output)
    assert search_payload["search_mode"] == "explicit_terms_any"
    assert search_payload["search_hit_total"] >= 1
    assert search_payload["workspace_context"]["worktree_clean"] is False

    explain = runner.invoke(cli, base + [
        "--operation", "explain", "--subject", "cap:book-reentry",
        "--expect-kind", "alternative", "--expect-kind", "verification",
        "--repo", str(root),
    ])
    assert explain.exit_code == 0, explain.output
    payload = json.loads(explain.output)
    assert payload["bounded_coverage"]["not_assessed_in_neighborhood"] == [
        "alternative", "verification",
    ]
    assert payload["workspace_context"]["uncommitted_changes_not_indexed"] is True
    assert payload["action_authorized"] is False
    assert payload["semantic_truth_established"] is False
