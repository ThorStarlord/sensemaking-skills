"""Pure, deterministic query selection and bounded-coverage contracts."""
from __future__ import annotations

import pytest

from sensemaking_skills.semantic_architecture.knowledge_retrieval import (
    bounded_kind_coverage,
    search_matches,
    validate_retrieval_options,
)


def samples():
    return {
        "id:a": {"id": "id:a", "kind": "decision", "statement": "Replay history"},
        "id:b": {"id": "id:b", "kind": "alternative", "statement": "Replay ordering alternative"},
        "id:c": {"id": "id:c", "kind": "verification", "statement": "Order restored"},
    }


def test_explicit_retrieval_uses_literal_or_and_stable_match_counts():
    claims, metadata = search_matches(samples(), subject=None, search_terms=("REPLAY", "ordering"))
    assert [c["id"] for c in claims] == ["id:b", "id:a"]
    assert metadata == {"search_mode": "explicit_terms_any", "search_hit_total": 2}


def test_legacy_literal_search_preserves_claim_iteration_order():
    claims, metadata = search_matches(samples(), subject="Replay")
    assert [c["id"] for c in claims] == ["id:a", "id:b"]
    assert metadata["search_mode"] == "literal"
    assert metadata["search_hit_total"] == 2


def test_bounded_coverage_discloses_limit_omissions_and_unknowns():
    claims = list(samples().values())
    coverage = bounded_kind_coverage(claims, expected_kinds=("decision", "alternative", "verification", "hypothesis"), limit=1)
    assert coverage["present_in_returned_claims"] == ["decision"]
    assert coverage["present_but_omitted_by_limit"] == ["alternative", "verification"]
    assert coverage["not_assessed_in_neighborhood"] == ["hypothesis"]
    assert coverage["semantic_completeness_established"] is False


def test_invalid_retrieval_option_combinations_are_rejected():
    with pytest.raises(ValueError, match="cannot"):
        validate_retrieval_options(operation="search", subject="replay", search_terms=("history",), expected_kinds=())
    with pytest.raises(ValueError, match="only"):
        validate_retrieval_options(operation="snapshot", subject=None, search_terms=("history",), expected_kinds=())
    with pytest.raises(ValueError, match="only"):
        validate_retrieval_options(operation="search", subject=None, search_terms=(), expected_kinds=("verification",))
    with pytest.raises(ValueError, match="unknown"):
        validate_retrieval_options(operation="why", subject="id:a", search_terms=(), expected_kinds=("banana",))
    for terms in (("",), ("r" * 81,), tuple("x" + str(i) for i in range(9))):
        with pytest.raises(ValueError, match="search terms"):
            validate_retrieval_options(operation="search", subject=None, search_terms=terms, expected_kinds=())


def test_duplicate_search_terms_do_not_skew_order():
    claims, data = search_matches(samples(), subject=None, search_terms=("replay", "REPLAY", "ordering"))
    assert claims[0]["id"] == "id:b"
    assert data["search_hit_total"] == 2
