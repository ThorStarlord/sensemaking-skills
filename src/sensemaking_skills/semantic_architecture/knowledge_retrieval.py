"""Deterministic lookup helpers; neither search nor coverage proves semantic truth."""
from __future__ import annotations

from collections.abc import Mapping

from .knowledge import CLAIM_KINDS, V2_CLAIM_KINDS


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
        if any(kind not in CLAIM_KINDS | V2_CLAIM_KINDS for kind in expected_kinds):
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
    reviewed_cited: set[str] = set()
    records = [("claim", c) for c in claims.values()] + [("relation", r) for r in relations]
    for record_type, record in records:
        cited = record.get("attributes", {}).get("source_sha256", {})
        if isinstance(cited, dict) and not _is_mechanical(record):
            reviewed_cited.update(cited)
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
    # Changed paths no reviewed record cites (mechanical-only citation does not
    # count): coverage gaps to inspect directly, not evidence of no effect.
    uncited = sorted(changed_paths - reviewed_cited)
    metadata = {
        "changed_path_total": len(changed_paths),
        "affected_record_total": len(affected),
        "affected_records": affected[:limit],
        "uncited_changed_path_total": len(uncited),
        "uncited_changed_paths": uncited[:limit],
        "mechanical_overlap_counts": mechanical,
        "overlay_indexed": False,
        "workspace_impact_limit": (
            "Path-level overlap between cited source fingerprints and working-tree changes since the "
            "indexed revision. Re-inspect listed records; a change does not invalidate them, and "
            "records without fingerprints or uncited consequences are NOT ASSESSED. "
            "uncited_changed_paths are coverage gaps, not evidence of no semantic effect."
        ),
    }
    return hit_claims, hit_relations, metadata



def context_workspace_overlap(
    claims: Mapping[str, dict], relations: tuple[dict, ...], *,
    selected_claim_ids: list[str], selected_relation_ids: list[str],
    changed_paths: frozenset[str], target_path: str, limit: int,
    context_truncated: bool,
) -> dict:
    """Read-only source-path overlap for records selected by context-for.

    A changed cited file is a re-inspection candidate, never a finding that the
    authored claim is wrong. Source fingerprints describe the indexed commit,
    not the working-tree overlay.
    """
    relation_ids = set(selected_relation_ids)
    selected = (
        [("claim", claims[cid]) for cid in selected_claim_ids if cid in claims]
        + [("relation", r) for r in relations if r["id"] in relation_ids]
    )
    affected: list[dict] = []
    without_fingerprints = 0
    mechanical = 0
    for record_type, record in selected:
        if _is_mechanical(record):
            mechanical += 1
            continue
        cited = record.get("attributes", {}).get("source_sha256")
        if not isinstance(cited, dict) or not cited:
            without_fingerprints += 1
            continue
        overlap = sorted(path for path in cited if path in changed_paths)
        if overlap:
            origin = record.get("source_ref", "")
            source_path = origin[5:] if origin.startswith("file:") else None
            affected.append({
                "record_type": record_type, "id": record["id"],
                "record_source_changed": source_path in overlap,
                "changed_evidence_sources": [p for p in overlap if p != source_path],
            })
    return {
        "target_path_changed": target_path in changed_paths,
        "changed_path_total": len(changed_paths),
        "selected_record_total": len(selected),
        "affected_record_total": len(affected),
        "affected_records": affected[:limit],
        "affected_records_omitted": max(0, len(affected) - limit),
        "records_without_fingerprints": without_fingerprints,
        "mechanical_records_not_assessed": mechanical,
        "context_selection_truncated": context_truncated,
        "overlay_indexed": False,
        "semantic_staleness_established": False,
        "note": (
            "Changed paths since the indexed commit overlap cited sources of selected "
            "records. Re-inspect originals; fingerprint overlap is neither a content "
            "comparison nor proof a claim changed meaning. Uncited paths, missing "
            "fingerprints and relationships outside this bounded context are NOT ASSESSED."
        ),
    }


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


# Authored-record classification is a projection over existing indexed payloads.
# It never re-reads a working tree, changes snapshot identity or judges truth.
def _authored_pack(record: dict) -> str | None:
    ref = record.get("source_ref")
    if isinstance(ref, str) and ref.startswith("file:.sensemaking/knowledge/") and ref.endswith(".json"):
        return ref[5:]
    return None


def _authored_fields(record: dict) -> dict | None:
    attrs = record.get("attributes")
    if not isinstance(attrs, dict):
        return None
    # source_ref and these two attributes are produced by the index builder,
    # not by an individual claim/relation's Git-reviewed authored fields.
    authored_attrs = {key: value for key, value in attrs.items()
                      if key not in {"source_sha256", "authority_verified"}}
    return {**{key: value for key, value in record.items()
               if key not in {"source_ref", "attributes"}}, "attributes": authored_attrs}


def _source_fingerprints(record: dict) -> dict[str, str] | None:
    attrs = record.get("attributes")
    fingerprints = attrs.get("source_sha256") if isinstance(attrs, dict) else None
    if not isinstance(fingerprints, dict) or not fingerprints:
        return None
    if any(not isinstance(path, str) or not path or
           not isinstance(digest, str) or len(digest) != 64
           for path, digest in fingerprints.items()):
        return None
    return fingerprints


def _expected_local_fingerprints(record: dict) -> set[str] | None:
    """Local cited paths should have indexed hashes in both snapshots."""
    references = record.get("evidence_refs")
    if not isinstance(references, (list, tuple)) or any(
        not isinstance(reference, str) for reference in references
    ):
        return None
    paths = set()
    for reference in references:
        if reference.startswith("file:"):
            path = reference[5:].split("#", 1)[0]
            prefix, marker, line = path.rpartition(":line:")
            paths.add(prefix if marker and line.isdigit() else path)
    if record.get("authority_kind") in {"policy", "code", "test"}:
        authority = record.get("authority_ref")
        if not isinstance(authority, str) or not authority:
            return None
        paths.add(authority)
    return paths


def _classify_record_change(previous: dict, current: dict) -> dict:
    """Explain raw indexed changes without inferring architectural truth."""
    result = {
        "id": current["id"],
        "assessment_status": "NOT_ASSESSED",
        "authored_fields_changed": None,
        "authoring_location_changed": None,
        "authoring_source_changed": None,
        "changed_supporting_sources": None,
        "provenance_only": None,
    }
    old_pack, new_pack = _authored_pack(previous), _authored_pack(current)
    old_fields, new_fields = _authored_fields(previous), _authored_fields(current)
    if old_pack is None or new_pack is None or old_fields is None or new_fields is None:
        result["unassessed_reason"] = "not_two_supported_git_authored_records"
        return result

    result["authored_fields_changed"] = old_fields != new_fields
    result["authoring_location_changed"] = old_pack != new_pack
    old_fingerprints = _source_fingerprints(previous)
    new_fingerprints = _source_fingerprints(current)
    if old_fingerprints is None or new_fingerprints is None:
        result["unassessed_reason"] = "source_fingerprints_unavailable"
        return result
    if old_pack not in old_fingerprints or new_pack not in new_fingerprints:
        result["unassessed_reason"] = "authored_container_fingerprint_unavailable"
        return result
    old_cited = _expected_local_fingerprints(previous)
    new_cited = _expected_local_fingerprints(current)
    if (old_cited is None or new_cited is None
            or not old_cited.issubset(old_fingerprints)
            or not new_cited.issubset(new_fingerprints)):
        result["unassessed_reason"] = "cited_source_fingerprints_unavailable"
        return result

    # A moved record can refer to two distinct packs; location is a separate
    # observation, even if the two packs happen to have identical bytes.
    result["authoring_source_changed"] = (
        old_fingerprints[old_pack] != new_fingerprints[new_pack]
    )
    supporting = []
    for path in sorted((old_fingerprints.keys() | new_fingerprints.keys()) - {old_pack, new_pack}):
        if path not in old_fingerprints:
            supporting.append({"path": path, "change": "reference_added"})
        elif path not in new_fingerprints:
            supporting.append({"path": path, "change": "reference_removed"})
        elif old_fingerprints[path] != new_fingerprints[path]:
            supporting.append({"path": path, "change": "fingerprint_changed"})
    result["changed_supporting_sources"] = supporting
    result["provenance_only"] = bool(
        not result["authored_fields_changed"]
        and not result["authoring_location_changed"]
        and not supporting
    )
    result["assessment_status"] = "ASSESSED"
    return result


def classify_indexed_changes(
    previous: Mapping[str, dict], current: Mapping[str, dict], *, limit: int,
) -> tuple[list[dict], dict]:
    """Classify changed common IDs; preserve raw deltas and all pre-limit totals."""
    changed = sorted(
        identifier for identifier in previous.keys() & current.keys()
        if previous[identifier] != current[identifier]
    )
    counts = {
        "changed_total": len(changed), "assessed": 0, "not_assessed": 0,
        "authored_fields_changed": 0, "authoring_location_changed": 0,
        "authoring_source_changed": 0, "supporting_sources_changed": 0,
        "provenance_only": 0,
    }
    entries = []
    for identifier in changed:
        detail = _classify_record_change(previous[identifier], current[identifier])
        counts["assessed" if detail["assessment_status"] == "ASSESSED" else "not_assessed"] += 1
        for facet in ("authored_fields_changed", "authoring_location_changed",
                      "authoring_source_changed", "provenance_only"):
            if detail[facet] is True:
                counts[facet] += 1
        if detail["changed_supporting_sources"]:
            counts["supporting_sources_changed"] += 1
        if len(entries) < limit:
            entries.append(detail)
    return entries, counts
