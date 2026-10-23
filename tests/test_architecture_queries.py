"""Path-scoped architecture queries over reviewed knowledge (ADR 0033, Phase 2)."""
from __future__ import annotations

from sensemaking_skills.semantic_architecture.knowledge_architecture import (
    NOT_ASSESSED_NOTE, glob_to_regex, orientation_summary, rules_for, term,
)


def _claim(cid, kind, statement="s", evidence=(), attributes=None):
    return {"id": cid, "kind": kind, "statement": statement, "evidence_refs": list(evidence),
            "attributes": attributes or {}}


def _rel(rid, subject, predicate, obj):
    return {"id": rid, "subject": subject, "predicate": predicate, "object": obj}


CLAIMS = {c["id"]: c for c in [
    _claim("component:semantic-store", "component",
           evidence=["file:src/sensemaking_skills/semantic_architecture/knowledge_store.py"],
           attributes={"owned_paths": ["src/sensemaking_skills/semantic_architecture/knowledge_store.py"]}),
    _claim("component:semantic-retrieval", "component",
           evidence=["file:src/sensemaking_skills/semantic_architecture/knowledge_retrieval.py"],
           attributes={"owned_paths": ["src/sensemaking_skills/semantic_architecture/knowledge_retrieval.py"]}),
    _claim("component:lab", "component", evidence=["file:src/sensemaking_skills/campaign_validation/x.py"],
           attributes={"owned_paths": ["src/sensemaking_skills/campaign_validation/x.py"]}),
    _claim("layer:semantic-plane", "layer"),
    _claim("bounded_context:knowledge", "bounded_context"),
    _claim("rule:semantic-no-lab", "architecture_rule", "Semantic modules must not import lab code.",
           attributes={"rule_type": "dependency_direction", "severity": "error",
                       "applies_to": ["src/sensemaking_skills/semantic_architecture/**"],
                       "forbidden_targets": ["component:lab"]}),
    _claim("rule:store-only-writes", "architecture_rule", "Only the store writes the database.",
           attributes={"rule_type": "convention", "severity": "warning",
                       "applies_to": ["src/other/**"]}),
    _claim("domain_concept:fog-type", "domain_concept", "A fog type classifies the uncertainty."),
    _claim("domain_concept:weakness-type", "domain_concept", "A weakness type classifies a boundary."),
    _claim("domain_concept:fog", "domain_concept", "fog"),
]}
RELATIONS = [
    _rel("r1", "component:semantic-store", "belongs_to", "layer:semantic-plane"),
    _rel("r2", "component:semantic-store", "belongs_to", "bounded_context:knowledge"),
    _rel("r3", "component:semantic-store", "tested_by", "verification:store-tests"),
    _rel("r4", "domain_concept:fog-type", "distinct_from", "domain_concept:weakness-type"),
    _rel("r5", "domain_concept:fog", "synonym_of", "domain_concept:fog-type"),
    _rel("r6", "rule:store-only-writes", "applies_to", "component:semantic-store"),
]


# -- glob matching -------------------------------------------------------------

def test_double_star_crosses_directories_and_single_star_does_not():
    assert glob_to_regex("src/**").match("src/a/b/c.py")
    assert glob_to_regex("src/**/*.py").match("src/a/b/c.py")
    assert glob_to_regex("scripts/validate-*.py").match("scripts/validate-brief.py")
    assert not glob_to_regex("scripts/validate-*.py").match("scripts/nested/validate-brief.py")
    assert not glob_to_regex("src/*.py").match("src/a/b.py")


# -- rules-for ---------------------------------------------------------------

def test_rules_for_a_covered_path_returns_owner_layer_context_rules_and_tests():
    result = rules_for(CLAIMS, RELATIONS,
                       path="src/sensemaking_skills/semantic_architecture/knowledge_store.py", limit=20)
    assert result["coverage_status"] == "COVERED"
    assert result["owning_components"] == ["component:semantic-store"]
    assert result["layers"] == ["layer:semantic-plane"]
    assert result["bounded_contexts"] == ["bounded_context:knowledge"]
    assert result["tests"] == ["verification:store-tests"]
    ids = {rule["claim_id"] for rule in result["applicable_rules"]}
    assert ids == {"rule:semantic-no-lab", "rule:store-only-writes"}
    scope_matched = next(r for r in result["applicable_rules"] if r["claim_id"] == "rule:semantic-no-lab")
    assert scope_matched["matched_by"] == ["path scope src/sensemaking_skills/semantic_architecture/**"]
    assert result["note"] is None


def test_component_scoped_rule_matches_through_its_owner_only():
    result = rules_for(CLAIMS, RELATIONS,
                       path="src/sensemaking_skills/semantic_architecture/knowledge_store.py", limit=20)
    store_rule = next(r for r in result["applicable_rules"] if r["claim_id"] == "rule:store-only-writes")
    assert store_rule["matched_by"] == ["declared graph target component:semantic-store"]


def test_uncovered_path_is_not_assessed_not_empty_success():
    result = rules_for(CLAIMS, RELATIONS, path="docs/unrelated.md", limit=20)
    assert result["coverage_status"] == "NOT_ASSESSED"
    assert result["owning_components"] == []
    assert result["note"] == NOT_ASSESSED_NOTE
    # A glob rule can still apply to an uncovered path if its scope names it.
    scoped = rules_for(CLAIMS, RELATIONS, path="src/sensemaking_skills/semantic_architecture/new_module.py", limit=20)
    assert scoped["coverage_status"] == "NOT_ASSESSED"
    assert any(r["claim_id"] == "rule:semantic-no-lab" for r in scoped["applicable_rules"])


def test_rules_for_truncates_and_discloses():
    result = rules_for(CLAIMS, RELATIONS,
                       path="src/sensemaking_skills/semantic_architecture/knowledge_store.py", limit=1)
    assert len(result["applicable_rules"]) == 1
    assert result["truncated"] is True


# -- term --------------------------------------------------------------------

def test_term_reports_distinct_and_synonym_neighbours():
    weakness = term(CLAIMS, RELATIONS, name="fog-type", limit=10)
    assert weakness["matched_claims"] == ["domain_concept:fog-type"]
    assert weakness["distinct_from"] == ["domain_concept:weakness-type"]
    assert weakness["synonyms"] == ["domain_concept:fog"]
    assert weakness["coverage_status"] == "COVERED"


def test_unknown_term_is_not_assessed():
    result = term(CLAIMS, RELATIONS, name="campaign", limit=10)
    assert result["coverage_status"] == "NOT_ASSESSED"
    assert result["matched_claims"] == []


# -- orientation summary -------------------------------------------------------------

def test_orientation_summary_counts_kinds_and_says_what_is_missing():
    summary = orientation_summary(CLAIMS, RELATIONS, max_lines=200)
    assert summary["counts"]["architecture_rule"] == 2
    assert summary["counts"]["layer"] == 1
    assert "absent here is NOT ASSESSED" in summary["coverage_note"]
    assert summary["lines_omitted"] == 0


def test_orientation_summary_caps_lines_and_reports_omission():
    summary = orientation_summary(CLAIMS, RELATIONS, max_lines=2)
    assert len(summary["lines"]) == 2
    assert summary["lines_omitted"] > 0


def test_rules_for_subject_validation_at_the_store_boundary(tmp_path):
    """A real file path must be accepted; globs and escapes must be refused."""
    from sensemaking_skills.semantic_architecture.knowledge_store import query_knowledge
    import pytest

    db = tmp_path / "missing.sqlite"
    for subject in ("src/a/*.py", "/etc/passwd", "../outside.py"):
        with pytest.raises(ValueError, match="repository-relative"):
            query_knowledge(db, repository="o/r", target_ref="a" * 40, operation="rules-for", subject=subject)
    # A plain path passes validation and only then fails on the missing database.
    with pytest.raises(Exception) as excinfo:
        query_knowledge(db, repository="o/r", target_ref="a" * 40, operation="rules-for",
                        subject="src/sensemaking_skills/x.py")
    assert "repository-relative" not in str(excinfo.value)

def test_evidence_reference_cannot_establish_ownership():
    claims = dict(CLAIMS)
    claims["component:reader"] = _claim("component:reader", "component",
        evidence=["file:src/sensemaking_skills/semantic_architecture/knowledge_store.py"])
    result = rules_for(claims, RELATIONS, path="src/sensemaking_skills/semantic_architecture/knowledge_store.py", limit=50)
    assert result["owning_components"] == ["component:semantic-store"]


def test_duplicate_explicit_owners_are_disclosed():
    claims = dict(CLAIMS)
    claims["component:duplicate"] = _claim("component:duplicate", "component",
        attributes={"owned_paths": ["src/sensemaking_skills/semantic_architecture/knowledge_store.py"]})
    result = rules_for(claims, RELATIONS, path="src/sensemaking_skills/semantic_architecture/knowledge_store.py", limit=50)
    assert result["ownership_ambiguous"] is True


def test_graph_layer_scope_matches_owned_component():
    claims = dict(CLAIMS)
    claims["rule:layer"] = _claim("rule:layer", "architecture_rule", "Layer rule",
        attributes={"rule_type": "convention", "severity": "warning", "applies_to": ["src/elsewhere/**"]})
    edges = [*RELATIONS, _rel("r7", "rule:layer", "applies_to", "layer:semantic-plane")]
    result = rules_for(claims, edges, path="src/sensemaking_skills/semantic_architecture/knowledge_store.py", limit=50)
    assert any(r["claim_id"] == "rule:layer" for r in result["applicable_rules"])
