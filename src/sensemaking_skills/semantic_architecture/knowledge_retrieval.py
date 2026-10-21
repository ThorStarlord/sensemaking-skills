"""Deterministic lookup helpers; neither search nor coverage proves semantic truth."""
from __future__ import annotations

from collections.abc import Mapping

from .knowledge import CLAIM_KINDS


def validate_retrieval_options(
    *, operation: str, subject: str | None,
    search_terms: tuple[str, ...], expected_kinds: tuple[str, ...],
) -> None:
    """Reject misleading or ambiguous targeted-query option combinations."""
    if search_terms:
        if operation != "search":
            raise ValueError("search terms are supported only for search")
        if subject is not None:
            raise ValueError("search terms cannot be combined with subject")
        if len(search_terms) > 8 or any(
            not isinstance(term, str) or not term.strip() or len(term) > 80
            for term in search_terms
        ):
            raise ValueError("search terms must be 1..8 nonempty phrases up to 80 characters")
    if expected_kinds:
        if operation not in {"explain", "why"}:
            raise ValueError("expected kinds are supported only for explain or why")
        if any(kind not in CLAIM_KINDS for kind in expected_kinds):
            raise ValueError("unknown expected claim kind")


def search_matches(
    claims: Mapping[str, dict], *, subject: str | None,
    search_terms: tuple[str, ...] = (),
) -> tuple[list[dict], dict]:
    """Case-insensitive literal substring matching, with explicit OR expansion."""
    validate_retrieval_options(
        operation="search", subject=subject, search_terms=search_terms,
        expected_kinds=(),
    )
    if not search_terms:
        needle = (subject or "").casefold()
        found = [c for c in claims.values()
                 if needle in c["statement"].casefold() or needle in c["id"].casefold()]
        return found, {"search_mode": "literal", "search_hit_total": len(found)}
    needles = tuple(dict.fromkeys(term.strip().casefold() for term in search_terms))
    ranked: list[tuple[int, str, dict]] = []
    for claim in claims.values():
        haystack_id, haystack_statement = claim["id"].casefold(), claim["statement"].casefold()
        matching = sum(needle in haystack_id or needle in haystack_statement for needle in needles)
        if matching:
            ranked.append((-matching, claim["id"], claim))
    ranked.sort(key=lambda item: (item[0], item[1]))
    found = [item[2] for item in ranked]
    return found, {"search_mode": "explicit_terms_any", "search_hit_total": len(found)}


def bounded_kind_coverage(
    found_claims: list[dict], *, expected_kinds: tuple[str, ...], limit: int,
) -> dict:
    """Describe only an explicitly linked, one-hop pre-limit neighborhood."""
    requested = list(dict.fromkeys(expected_kinds))
    all_kinds = {claim["kind"] for claim in found_claims}
    returned_kinds = {claim["kind"] for claim in found_claims[:limit]}
    return {
        "requested_kinds": requested,
        "present_in_returned_claims": [k for k in requested if k in returned_kinds],
        "present_but_omitted_by_limit": [k for k in requested if k in all_kinds and k not in returned_kinds],
        "not_assessed_in_neighborhood": [k for k in requested if k not in all_kinds],
        "semantic_completeness_established": False,
    }
