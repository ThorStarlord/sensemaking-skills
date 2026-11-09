"""Path-scoped architecture queries over reviewed knowledge (ADR 0033, Phase 2)."""
from __future__ import annotations

from sensemaking_skills.semantic_architecture.knowledge_architecture import (
    NOT_ASSESSED_NOTE, context_for, glob_to_regex, orientation_summary, rules_for, term,
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
        attributes={"rule_type": "convention", "severity": "warning", "applies_to": []})
    edges = [*RELATIONS, _rel("r7", "rule:layer", "applies_to", "layer:semantic-plane")]
    result = rules_for(claims, edges, path="src/sensemaking_skills/semantic_architecture/knowledge_store.py", limit=50)
    assert any(r["claim_id"] == "rule:layer" for r in result["applicable_rules"])

def test_pilot_provenance_and_explicit_ownership_not_confused():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    records = [json.loads((root / ".sensemaking/knowledge" / n).read_text(encoding="utf-8"))
               for n in ("architecture.json", "domain.json", "stewardship.json")]
    claims = {c["id"]: c for r in records for c in r["claims"]}
    relations = [e for r in records for e in r["relations"]]
    store = rules_for(claims, relations,
        path="src/sensemaking_skills/semantic_architecture/knowledge_store.py", limit=50)
    assert store["owning_components"] == ["component:knowledge-store"]
    assert not store["ownership_ambiguous"]
    assert store["layers"] == ["layer:knowledge-plane"]
    assert store["bounded_contexts"] == ["bounded_context:knowledge-stewardship"]
    assert any(r["claim_id"] == "rule:stable-core-no-lab-imports"
               for r in store["applicable_rules"])
    validator = rules_for(claims, relations, path="scripts/validate-brief.py", limit=50)
    assert validator["owning_components"] == ["component:brief-validator"]
    placement = next(r for r in validator["applicable_rules"]
                     if r["claim_id"] == "rule:validators-placement")
    assert placement["epistemic_status"] == "hypothetical"
    assert placement["authority_kind"] == "hypothesis"
    assert any(r["subject"] == "component:repository-semantic-steward-skill"
               and r["predicate"] == "exposes"
               and r["object"] == "contract:semantic-query-receipt" for r in relations)
    assert not any(r["subject"] == "contract:repository-sensemaking-brief"
                   and r["predicate"] == "belongs_to" for r in relations)


# -- file-level verification relevance (context-for) ---------------------------

TEST_PATH = "tests/test_store_regression.py"
SRC_PATH = "src/sensemaking_skills/semantic_architecture/knowledge_store.py"


def _verification(cid, *, authority_ref=None, evidence=()):
    claim = _claim(cid, "verification", f"{cid} regression")
    claim["authority_ref"] = authority_ref
    claim["evidence_refs"] = list(evidence)
    return claim


def _test_claims():
    claims = dict(CLAIMS)
    claims["verification:store-regression"] = _verification(
        "verification:store-regression", authority_ref=TEST_PATH, evidence=[f"file:{TEST_PATH}"])
    claims["decision:store-regression"] = _claim("decision:store-regression", "decision", "Store decision.")
    return claims


def _test_relations():
    kept = [r for r in RELATIONS if r["id"] != "r3"]
    return [*kept,
            _rel("t1", "component:semantic-store", "tested_by", "verification:store-regression"),
            _rel("t2", "component:semantic-store", "decided_by", "decision:store-regression")]


def _ids(items):
    return [item["claim_id"] for item in items]


def test_test_file_reaches_verification_and_verified_component_without_ownership():
    ctx, returned, rel_ids = context_for(_test_claims(), _test_relations(), path=TEST_PATH, limit=20)
    assert ctx["ownership"]["components"] == []
    assert ctx["ownership"]["coverage_status"] == "NOT_ASSESSED"
    assert _ids(ctx["verification_refs"]) == ["verification:store-regression"]
    assert _ids(ctx["verified_components"]) == ["component:semantic-store"]
    assert _ids(ctx["decisions"]) == ["decision:store-regression"]
    assert {"t1", "t2"} <= set(rel_ids)
    assert {"verification:store-regression", "component:semantic-store"} <= set(returned)
    gaps = {g["category"]: g["status"] for g in ctx["knowledge_gaps"]}
    assert gaps["verification_relevance"] == "NOT_AN_OWNER"
    assert "verified_components" not in gaps


def test_each_verification_link_says_why_it_is_relevant():
    ctx, _, _ = context_for(_test_claims(), _test_relations(), path=TEST_PATH, limit=20)
    verification = ctx["verification_refs"][0]
    assert any(text.startswith("authority_ref:") for text in verification["matched_by"])
    verified = ctx["verified_components"][0]
    assert verified["matched_by"]
    assert all("not ownership" in text for text in verified["matched_by"])


def test_verified_component_does_not_expand_to_all_its_other_verifications():
    claims = _test_claims()
    claims["verification:other-test"] = _verification(
        "verification:other-test", authority_ref="tests/test_other.py", evidence=["file:tests/test_other.py"])
    relations = [*_test_relations(),
                 _rel("t4", "component:semantic-store", "tested_by", "verification:other-test")]
    ctx, _, _ = context_for(claims, relations, path=TEST_PATH, limit=20)
    assert _ids(ctx["verification_refs"]) == ["verification:store-regression"]
    assert _ids(ctx["verified_components"]) == ["component:semantic-store"]


def test_citations_from_other_claim_kinds_do_not_qualify():
    claims = _test_claims()
    claims["decision:unlinked-cites-test"] = _claim(
        "decision:unlinked-cites-test", "decision", "Cites the test only.", evidence=[f"file:{TEST_PATH}"])
    claims["component:citing-only"] = _claim(
        "component:citing-only", "component", evidence=[f"file:{TEST_PATH}"])
    ctx, returned, _ = context_for(claims, _test_relations(), path=TEST_PATH, limit=20)
    assert "decision:unlinked-cites-test" not in returned
    assert "component:citing-only" not in returned
    assert ctx["ownership"]["components"] == []


def test_evidence_citation_by_verification_is_labelled_as_evidence_only():
    claims = dict(CLAIMS)
    claims["verification:cites-only"] = _verification(
        "verification:cites-only", authority_ref="docs/testing.md", evidence=[f"file:{TEST_PATH}"])
    ctx, _, _ = context_for(claims, RELATIONS, path=TEST_PATH, limit=20)
    assert _ids(ctx["verification_refs"]) == ["verification:cites-only"]
    assert all(text.startswith("evidence_ref:") for text in ctx["verification_refs"][0]["matched_by"])
    assert ctx["verified_components"] == []
    gaps = {g["category"]: g["status"] for g in ctx["knowledge_gaps"]}
    assert gaps["verified_components"] == "NOT_ASSESSED"


def test_unrelated_test_file_gets_no_speculative_context():
    ctx, returned, rel_ids = context_for(
        _test_claims(), _test_relations(), path="tests/test_unrelated.py", limit=20)
    assert returned == []
    assert rel_ids == []
    assert ctx["verification_refs"] == [] and ctx["verified_components"] == []
    assert ctx["decisions"] == []
    gaps = {g["category"]: g["status"] for g in ctx["knowledge_gaps"]}
    assert gaps["verification_refs"] == "NOT_ASSESSED"
    assert "verification_relevance" not in gaps


def test_owned_path_keeps_its_tested_by_route_and_ignores_citations():
    claims = _test_claims()
    claims["verification:cites-src"] = _verification(
        "verification:cites-src", authority_ref="docs/testing.md", evidence=[f"file:{SRC_PATH}"])
    ctx, _, _ = context_for(claims, _test_relations(), path=SRC_PATH, limit=20)
    assert ctx["ownership"]["components"] == ["component:semantic-store"]
    verification = _ids(ctx["verification_refs"])
    assert "verification:store-regression" in verification  # existing owner tested_by route
    assert "verification:cites-src" not in verification
    assert ctx["verified_components"] == []
    assert "verification_relevance" not in {g["category"] for g in ctx["knowledge_gaps"]}


def test_verification_without_tested_by_is_disclosed_not_assumed():
    claims = dict(CLAIMS)
    claims["verification:untested"] = _verification(
        "verification:untested", authority_ref=TEST_PATH, evidence=[f"file:{TEST_PATH}"])
    ctx, _, _ = context_for(claims, RELATIONS, path=TEST_PATH, limit=20)
    assert _ids(ctx["verification_refs"]) == ["verification:untested"]
    assert ctx["verified_components"] == []
    assert ctx["decisions"] == []


def test_verified_components_are_bounded_and_disclosed():
    claims = _test_claims()
    claims["component:second-verifier"] = _claim("component:second-verifier", "component")
    relations = [*_test_relations(),
                 _rel("t3", "component:second-verifier", "tested_by", "verification:store-regression")]
    ctx, _, _ = context_for(claims, relations, path=TEST_PATH, limit=1)
    assert len(ctx["verified_components"]) == 1
    assert ctx["omitted"]["verified_components"] == 1
    assert ctx["truncated"] is True


def test_test_file_context_is_deterministic():
    first = context_for(_test_claims(), _test_relations(), path=TEST_PATH, limit=20)
    second = context_for(_test_claims(), _test_relations(), path=TEST_PATH, limit=20)
    assert first == second


def test_pilot_record_test_file_reaches_verification_and_decision_without_ownership():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    records = [json.loads((root / ".sensemaking/knowledge" / n).read_text(encoding="utf-8"))
               for n in ("architecture.json", "domain.json", "stewardship.json")]
    claims = {c["id"]: c for r in records for c in r["claims"]}
    relations = [e for r in records for e in r["relations"]]
    ctx, _, rel_ids = context_for(claims, relations,
        path="tests/test_legacy_workflow_planner_fail_closed.py", limit=50)
    assert ctx["ownership"]["components"] == []
    assert ctx["ownership"]["coverage_status"] == "NOT_ASSESSED"
    assert "verification:legacy-planner-fail-closed-tests" in _ids(ctx["verification_refs"])
    assert "component:legacy-workflow-planner" in _ids(ctx["verified_components"])
    assert "decision:legacy-planner-fails-closed" in _ids(ctx["decisions"])
    assert {"rel:legacy-planner-tested", "rel:legacy-planner-decided-by"} <= set(rel_ids)
