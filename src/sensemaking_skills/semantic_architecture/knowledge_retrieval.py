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


def _is_mechanical(record: dict) -> bool:
    return record.get("authority_kind") == "mechanical" or record.get("derivation") == "mechanical"


def workspace_source_overlap(
    claims: Mapping[str, dict], relations: tuple[dict, ...], *,
    changed_paths: frozenset[str], limit: int,
) -> tuple[list[dict], list[dict], dict]:
    """Match indexed source fingerprints to changed workspace paths.

    A match is a reason to re-inspect the record, never revocation: the
    working overlay is not indexed and its bytes are not compared.
    """
    affected: list[dict] = []
    hit_claims: list[dict] = []
    hit_relations: list[dict] = []
    mechanical = {"claims": 0, "relations": 0}
    records = [("claim", c) for c in claims.values()] + [("relation", r) for r in relations]
    for record_type, record in records:
        cited = record.get("attributes", {}).get("source_sha256", {})
        overlap = sorted(path for path in cited if path in changed_paths) if isinstance(cited, dict) else []
        if not overlap:
            continue
        if _is_mechanical(record):
            mechanical[f"{record_type}s"] += 1
            continue
        source_ref = record.get("source_ref", "")
        record_source = source_ref[5:] if source_ref.startswith("file:") else None
        affected.append({
            "record_type": record_type, "id": record["id"],
            "record_source_changed": record_source in overlap,
            "changed_evidence_sources": [p for p in overlap if p != record_source],
        })
        (hit_claims if record_type == "claim" else hit_relations).append(record)
    metadata = {
        "changed_path_total": len(changed_paths),
        "affected_record_total": len(affected),
        "affected_records": affected[:limit],
        "mechanical_overlap_counts": mechanical,
        "overlay_indexed": False,
        "workspace_impact_limit": (
            "Path-level overlap between cited source fingerprints and working-tree changes since the "
            "indexed revision. Re-inspect listed records; a change does not invalidate them, and "
            "records without fingerprints or uncited consequences are NOT ASSESSED."
        ),
    }
    return hit_claims, hit_relations, metadata


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
