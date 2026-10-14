"""Focused qualification for a lexical, source-bound semantic impact preview.

These tests use a real Git repository and never confer semantic authority.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from sensemaking_skills.semantic_architecture.impact import build_impact_preview


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


@pytest.fixture
def repository(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "test@example.invalid")
    git(repo, "config", "user.name", "Test Operator")
    (repo / ".sensemaking").mkdir()
    (repo / "specification").mkdir()
    (repo / "src").mkdir()
    (repo / "tests").mkdir()
    (repo / "specification" / "domain.md").write_text("Connection XP is not Affinity.\n", encoding="utf8")
    (repo / "src" / "relationships.ts").write_text("Relationship Experience and Memory\n", encoding="utf8")
    (repo / "src" / "affinity.ts").write_text("Affinity is a separate concept.\n", encoding="utf8")
    (repo / "tests" / "relationships.test.ts").write_text("Connection XP is not Affinity\n", encoding="utf8")
    (repo / ".sensemaking" / "context.md").write_text(
        "# Context\n"
        "- **Relationship Experience vs Memory**: Experiences are events; Memories are landmarks. [policy: specification/domain.md]\n"
        "- **Connection XP is not Affinity.** [policy: specification/domain.md]\n"
        "- **Experience schema:** still hypothetical. [hypothesis: not verified]\n"
        "- **A missing policy reference** to Connection XP. [policy: specification/missing.md]\n"
        "- **Memory** decisions were delegated. [delegated: 2026-10-12]\n"
        "- **Connection XP** owner decision. [owner: 2026-10-12]\n",
        encoding="utf8",
    )
    (repo / ".sensemaking" / "invariants.md").write_text(
        "# Constraints\n- No inventing narrative progression from Affinity. [test: tests/relationships.test.ts]\n",
        encoding="utf8",
    )
    (repo / ".sensemaking" / "intent.md").write_text(
        "# Intent\n- No autonomous Copy planner. [policy: specification/domain.md]\n",
        encoding="utf8",
    )
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "initial contract")
    return repo, git(repo, "rev-parse", "HEAD")


def test_terms_retrieve_relevant_grounding_and_candidate_surfaces(repository):
    repo, sha = repository
    result = build_impact_preview(repo, target_ref=sha, subject="Connection XP", related_terms=("Affinity",), include_globs=("src/*", "tests/*"))
    assert result.target_ref == sha
    assert len(result.grounding_claims) >= 3
    assert {c.provenance_kind for c in result.grounding_claims} >= {"policy", "owner", "test"}
    assert {p.path for p in result.candidate_surfaces} == {"src/affinity.ts", "tests/relationships.test.ts"}
    assert all(not s.path.startswith(".sensemaking/") for s in result.candidate_surfaces)
    assert result.semantic_truth_established is False
    assert result.change_authorized is False
    assert result.material_impact_established is False


def test_distinct_owner_delegated_and_hypothesis_provenance(repository):
    repo, sha = repository
    result = build_impact_preview(repo, target_ref=sha, subject="Memory")
    kinds = {c.provenance_kind for c in result.grounding_claims}
    assert kinds == {"policy", "delegated"}
    assert all(c.cited_path_exists is None for c in result.grounding_claims if c.provenance_kind == "delegated")
    hypo = build_impact_preview(repo, target_ref=sha, subject="Experience schema")
    assert [c.provenance_kind for c in hypo.grounding_claims] == ["hypothesis"]


def test_dangling_source_is_reported_not_treated_as_validated(repository):
    repo, sha = repository
    result = build_impact_preview(repo, target_ref=sha, subject="Connection XP")
    assert any("specification/missing.md" in ref for ref in result.missing_citations)
    assert any(c.cited_path_exists is False for c in result.grounding_claims)
    assert any("not prove" in lim for lim in result.explicit_limits)


def test_omitted_scope_is_not_reported_as_absence(repository):
    repo, sha = repository
    result = build_impact_preview(repo, target_ref=sha, subject="Connection XP", include_globs=("src/no-matches-*",))
    assert result.candidate_surfaces == ()
    assert any("NOT ASSESSED" in lim for lim in result.explicit_limits)


def test_deterministic_order_dedup_terms_and_overlapping_scopes(repository):
    repo, sha = repository
    kwargs = dict(target_ref=sha, subject="Affinity", related_terms=("Affinity", "Connection XP"), include_globs=("*", "src/*", "*"))
    first = build_impact_preview(repo, **kwargs)
    second = build_impact_preview(repo, **kwargs)
    assert first == second
    assert first.searched_terms == ("Affinity", "Connection XP")
    assert first.searched_globs == ("*", "src/*")
    assert len({s.path for s in first.candidate_surfaces}) == len(first.candidate_surfaces)


def test_cap_truncation_disclosed_not_silent(repository):
    repo, sha = repository
    result = build_impact_preview(repo, target_ref=sha, subject="Affinity", max_matches=1)
    assert result.truncated is True
    assert result.match_count > len(result.candidate_surfaces) == 1
    assert any("truncated" in lim for lim in result.explicit_limits)


def test_unrelated_owner_non_goal_is_not_attached(repository):
    repo, sha = repository
    result = build_impact_preview(repo, target_ref=sha, subject="Connection XP")
    assert not any("Copy planner" in c.statement for c in result.grounding_claims)


def test_mismatched_sha_fails_closed(repository):
    repo, sha = repository
    with pytest.raises(ValueError, match="does not match"):
        build_impact_preview(repo, target_ref="a" * 40, subject="Experience")


def test_invalid_or_short_sha_fails_closed(repository):
    repo, sha = repository
    with pytest.raises(ValueError, match="full 40-character"):
        build_impact_preview(repo, target_ref="sha:" + sha, subject="Experience")


def test_dirty_worktree_fails_closed(repository):
    repo, sha = repository
    (repo / "src" / "relationships.ts").write_text("changed\n", encoding="utf8")
    with pytest.raises(ValueError, match="not clean"):
        build_impact_preview(repo, target_ref=sha, subject="Experience")


def test_untracked_files_fail_closed(repository):
    repo, sha = repository
    (repo / "src" / "injected.ts").write_text("Connection XP\n", encoding="utf8")
    with pytest.raises(ValueError, match="not clean"):
        build_impact_preview(repo, target_ref=sha, subject="Connection XP")


def test_explicit_root_required(repository):
    repo, sha = repository
    with pytest.raises(ValueError, match="exact Git worktree root"):
        build_impact_preview(repo / "src", target_ref=sha, subject="Experience")


def test_empty_query_and_invalid_cap_rejected(repository):
    repo, sha = repository
    for subject in ("", "  "):
        with pytest.raises(ValueError, match="subject"):
            build_impact_preview(repo, target_ref=sha, subject=subject)
    for cap in (0, -5, 2001):
        with pytest.raises(ValueError, match="max_matches"):
            build_impact_preview(repo, target_ref=sha, subject="Experience", max_matches=cap)


def test_no_globs_rejected(repository):
    repo, sha = repository
    with pytest.raises(ValueError, match="include glob"):
        build_impact_preview(repo, target_ref=sha, subject="Experience", include_globs=("",))


def test_path_escape_in_pack_never_accepted(repository):
    repo, sha = repository
    file = repo / ".sensemaking" / "intent.md"
    file.write_text(file.read_text("utf8") + "- Secret Memory claim. [policy: ../../secret.md]\n", encoding="utf8")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "escape attempt")
    result = build_impact_preview(repo, target_ref=git(repo, "rev-parse", "HEAD"), subject="Memory")
    assert any("secret.md" in s for s in result.missing_citations)
    assert not any(c.cited_path_exists for c in result.grounding_claims if "secret.md" in c.provenance_target)


def test_no_repository_files_modified(repository):
    repo, sha = repository
    before = git(repo, "status", "--porcelain")
    build_impact_preview(repo, target_ref=sha, subject="Experience")
    assert git(repo, "status", "--porcelain") == before


def test_links_are_explicit_lexical_or_declared_not_inferred(repository):
    repo, sha = repository
    result = build_impact_preview(repo, target_ref=sha, subject="Connection XP", include_globs=("src/*", "tests/*"))
    assert result.evidence_links
    assert {l.derivation for l in result.evidence_links} <= {"LEXICAL", "DECLARED_NOT_VERIFIED"}
    assert all(l.predicate.startswith(("contains_literal_", "declares_")) for l in result.evidence_links)
    assert not any(l.predicate in {"depends_on", "implemented_by", "checked_by"} for l in result.evidence_links)
    assert any(l.predicate == "declares_policy_reference" for l in result.evidence_links)


def test_decision_records_are_covered_without_schema_duplication(repository):
    repo, sha = repository
    (repo / ".sensemaking" / "decisions").mkdir()
    (repo / ".sensemaking" / "decisions" / "001.md").write_text(
        "- Connection XP design decision. [delegated: 2026-10-10]\n", encoding="utf8",
    )
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "decision")
    now = git(repo, "rev-parse", "HEAD")
    preview = build_impact_preview(repo, target_ref=now, subject="Connection XP")
    assert any("decisions/001.md" in c.evidence_ref for c in preview.grounding_claims)


def test_cli_roundtrip(repository, tmp_path):
    import json
    from click.testing import CliRunner
    from sensemaking_skills.cli import cli
    repo, sha = repository
    out = tmp_path / "impact.json"
    result = CliRunner().invoke(
        cli,
        ["semantic", "impact-preview", "--repo", str(repo), "--target-ref", sha,
         "--subject", "Relationship Experience", "--related-term", "Memory",
         "--include-glob", "src/*", "--output", str(out), "--json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "SEMANTIC_IMPACT_PREVIEW"
    assert payload["semantic_truth_established"] is False
    assert payload["change_authorized"] is False
    assert any(x["path"] == "src/relationships.ts" for x in payload["candidate_surfaces"])
    assert json.loads(out.read_text("utf8")) == payload


def test_cli_rejects_dirty_checkout(repository):
    from click.testing import CliRunner
    from sensemaking_skills.cli import cli
    repo, sha = repository
    (repo / "src" / "relationships.ts").write_text("modified content", encoding="utf8")
    result = CliRunner().invoke(
        cli,
        ["semantic", "impact-preview", "--repo", str(repo), "--target-ref", sha,
         "--subject", "Connection XP", "--json"],
    )
    assert result.exit_code != 0
    assert "not clean" in result.output
