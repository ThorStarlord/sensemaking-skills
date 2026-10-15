"""Source-pinned self-repository smoke: use REAL ADRs and authored knowledge.

This is an end-to-end index/query observation at a Git SHA, not evidence of
independent-agent longitudinal learning or of better product decisions.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from sensemaking_skills.semantic_architecture.knowledge_sources import build_knowledge_snapshot
from sensemaking_skills.semantic_architecture.knowledge_store import store_snapshot, query_knowledge


def _git(cwd: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def test_real_repo_stewardship_knowledge_rebuild(tmp_path):
    source = Path(__file__).resolve().parents[1]
    head = _git(source, "rev-parse", "HEAD")
    checkout = tmp_path / "exact-head"
    # Independent checkout of the exact code/ADR bytes; no previous dialogue,
    # no fabricated authority, and no mutation of the candidate worktree.
    _git(source, "worktree", "add", "--detach", str(checkout), head)
    try:
        snap = build_knowledge_snapshot(
            checkout, repository="ThorStarlord/sensemaking-skills",
            target_ref=head, include_python_imports=False,
        )
        assert snap.claims and snap.relations
        db = tmp_path / "semantic.sqlite"
        receipt = store_snapshot(db, snap, source_root=checkout)
        assert receipt["claim_count"] >= 8
        a = dict(repository=snap.repository, target_ref=head)
        decision = query_knowledge(db, operation="why", subject="adr:0031", **a)
        assert any(c["id"] == "cap:semantic-queries" for c in decision["claims"])
        impact = query_knowledge(db, operation="impact", subject="cap:semantic-queries", **a)
        assert any(c["id"] == "goal:longterm-stewardship" for c in impact["claims"])
        assert any(e["predicate"] == "constrained_by" for e in impact["relations"])
        assert impact["semantic_truth_established"] is False
        assert impact["action_authorized"] is False
        cached = store_snapshot(db, snap, source_root=checkout)
        assert cached["already_indexed"]
    finally:
        _git(source, "worktree", "remove", "--force", str(checkout))
