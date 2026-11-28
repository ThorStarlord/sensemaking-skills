"""Deterministic lookup helpers; neither search nor coverage proves semantic truth."""
from __future__ import annotations

import re
from collections.abc import Mapping, Sequence

from .knowledge import (
    AUTHORED_SCHEMA_VERSIONS, CLAIM_KINDS, V2_CLAIM_KINDS,
    read_authored_claim, read_authored_relation, record_dict,
)
from .knowledge_architecture import lesson_citing_records


_QUESTION_WORD = re.compile(r"[^\W_]+", re.UNICODE)


def _query_tokens(text: str) -> tuple[str, ...]:
    """Case-folded distinct words for lexical discovery, not semantic analysis."""
    return tuple(dict.fromkeys(
        word for word in _QUESTION_WORD.findall(text.casefold()) if len(word) >= 2
    ))


_INFLECTIONS = ("ing", "ed", "es", "s")


def _stem(word: str) -> str:
    """Drop one common inflection so plural and tense forms of a query word can match.

    Lexical discovery only: "subagents" and "subagent" share a stem, while "already" does
    not reduce to "read". Short words keep their spelling so that little ones are not mangled.
    """
    for suffix in _INFLECTIONS:
        if word.endswith(suffix) and len(word) - len(suffix) >= 4:
            return word[: -len(suffix)]
    return word


# Function words and question scaffolding carry no topic. They are dropped before
# lexical ranking so that they cannot lift an unrelated claim above a content match.
_FUNCTION_WORDS = frozenset("""
a about above after again against all also am an and any are as at be because been
before being below between both but by can could did do does doing done down during
each either few for from further had has have having he her here hers him his how i
if in into is it its itself just let may me might more most must my no nor not now of
off on once only or other our out over own same shall she should so some such than
that the their them then there these they this those through to too under until up us
very via was we were what when where whether which while who whom why will with
within would yet you your
""".split())
# Shorter query words match only as whole words or stems, so "act" does not match "exact".
_SUBSTRING_MIN_LENGTH = 5


def _lexical_hit(word: str, name: str, statement: str, stems: set[str]) -> bool:
    """Whole word or inflection match; substring matching only for longer words."""
    if _stem(word) in stems:
        return True
    return len(word) >= _SUBSTRING_MIN_LENGTH and (word in name or word in statement)


# Conditions a later agent needs before applying a recalled lesson. A field that the
# reviewed record does not state is reported as NOT_RECORDED, never silently omitted.
_RECALL_CONDITION_FIELDS = (
    ("scope", ("scope",)),
    ("conditions", ("conditions",)),
    ("claim_ceiling", ("claim_ceiling",)),
    ("counterevidence", ("counterevidence",)),
    ("original_outcome", ("original_outcome",)),
    ("revisit_when", ("revisit_when", "staleness_condition")),
    ("decision_link", ("decision_changed", "operationalized_by")),
)


def lesson_recall_view(
    claim: Mapping[str, object], *,
    claims: Mapping[str, Mapping[str, object]],
    relations: Sequence[Mapping[str, object]],
) -> dict:
    """Return a copy of a lesson claim with explicit recall conditions and citing records.

    The indexed claim is not changed. Applicability to the current question is always
    NOT_ESTABLISHED: a recorded condition is authored context, not a finding that the
    lesson applies here.
    """
    attributes = claim.get("attributes")
    attributes = attributes if isinstance(attributes, Mapping) else {}
    conditions: dict[str, object] = {}
    for name, keys in _RECALL_CONDITION_FIELDS:
        conditions[name] = next(
            (attributes[key] for key in keys if attributes.get(key) not in (None, "", [])),
            "NOT_RECORDED",
        )
    conditions["applicability_to_current_question"] = "NOT_ESTABLISHED"
    return {
        **claim,
        "recall_conditions": conditions,
        "citing_records": lesson_citing_records(claim.get("id"), claims, relations),
    }


def validate_retrieval_options(
    *, operation: str, subject: str | None,
    search_terms: tuple[str, ...], expected_kinds: tuple[str, ...],
    query_text: str | None = None, search_kinds: tuple[str, ...] = (),
) -> None:
    """Reject misleading or ambiguous targeted-query option combinations."""
    if query_text is not None:
        if operation != "search":
            raise ValueError("query text is supported only for search")
        if subject is not None or search_terms:
            raise ValueError("query text cannot be combined with subject or --term")
        if (not isinstance(query_text, str) or len(query_text) > 300
                or any(ord(char) < 32 or ord(char) == 127 for char in query_text)
                or not 1 <= len(_query_tokens(query_text)) <= 24):
            raise ValueError("query text must contain 1..24 distinct words (length 2+) within 300 characters")
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
    if search_kinds:
        if operation != "search":
            raise ValueError("search kinds are supported only for search")
        if any(kind not in CLAIM_KINDS | V2_CLAIM_KINDS for kind in search_kinds):
            raise ValueError("unknown search claim kind")
    if expected_kinds:
        if operation not in {"explain", "why"}:
            raise ValueError("expected kinds are supported only for explain or why")
        if any(kind not in CLAIM_KINDS | V2_CLAIM_KINDS for kind in expected_kinds):
            raise ValueError("unknown expected claim kind")


def search_matches(
    claims: Mapping[str, dict], *, subject: str | None,
    search_terms: tuple[str, ...] = (), query_text: str | None = None,
    search_kinds: tuple[str, ...] = (), limit: int = 50,
) -> tuple[list[dict], dict]:
    """Literal search, explicit OR phrases, or opt-in ranked lexical question tokens."""
    validate_retrieval_options(
        operation="search", subject=subject, search_terms=search_terms,
        expected_kinds=(), query_text=query_text, search_kinds=search_kinds,
    )
    kind_filter = frozenset(search_kinds)
    candidates = [claim for claim in claims.values()
                  if not kind_filter or claim["kind"] in kind_filter]
    filter_metadata = {"search_kind_filter": sorted(kind_filter)} if kind_filter else {}
    if query_text is not None:
        tokens = _query_tokens(query_text)
        content_words = tuple(word for word in tokens if word not in _FUNCTION_WORDS)
        ranked: list[tuple[int, int, str, dict, tuple[str, ...]]] = []
        for claim in candidates:
            # The kind prefix ("lesson:") is taxonomy shared by every claim of a kind, not topic.
            name = claim["id"].casefold().partition(":")[2] or claim["id"].casefold()
            statement = claim["statement"].casefold()
            stems = {_stem(word) for word in _QUESTION_WORD.findall(f"{name} {statement}")}
            matched = tuple(
                word for word in content_words
                if _lexical_hit(word, name, statement, stems)
            )
            if matched:
                ranked.append((
                    -len(matched), -sum(len(word) for word in matched),
                    claim["id"], claim, matched,
                ))
        ranked.sort(key=lambda item: (item[0], item[1], item[2]))
        found = [item[3] for item in ranked]
        return found, {
            **filter_metadata,
            "search_mode": "ranked_lexical_tokens_any",
            "search_hit_total": len(found),
            "query_tokens": list(tokens),
            "ignored_function_words": [word for word in tokens if word in _FUNCTION_WORDS],
            "match_details": [
                {"claim_id": item[2], "matched_tokens": list(item[4])}
                for item in ranked[:limit]
            ],
            "match_details_truncated": len(ranked) > limit,
            "ranking_limit": (
                "Ranked by number and total length of matching distinct content words "
                "(function words ignored) or their stems (plural and tense forms), then claim ID. "
                "Words under five letters match only as whole words or stems; claim-kind "
                "prefixes are not matched. Matches are discovery candidates, "
                "not semantic similarity, verified applicability or authority."
            ),
        }
    if not search_terms:
        needle = (subject or "").casefold()
        found = [c for c in candidates
                 if needle in c["statement"].casefold() or needle in c["id"].casefold()]
        return found, {**filter_metadata, "search_mode": "literal", "search_hit_total": len(found)}
    needles = tuple(dict.fromkeys(term.strip().casefold() for term in search_terms))
    ranked: list[tuple[int, str, dict]] = []
    for claim in candidates:
        haystack_id, haystack_statement = claim["id"].casefold(), claim["statement"].casefold()
        matching = sum(needle in haystack_id or needle in haystack_statement for needle in needles)
        if matching:
            ranked.append((-matching, claim["id"], claim))
    ranked.sort(key=lambda item: (item[0], item[1]))
    found = [item[2] for item in ranked]
    return found, {**filter_metadata, "search_mode": "explicit_terms_any", "search_hit_total": len(found)}


def _is_mechanical(record: dict) -> bool:
    return record.get("authority_kind") == "mechanical" or record.get("derivation") == "mechanical"


def _path_matches_change(
    path: str, changed_paths: frozenset[str], untracked_directory_entries: frozenset[str],
) -> bool:
    """Exact membership, or a path under an unexpanded untracked directory entry."""
    return path in changed_paths or any(
        path.startswith(entry) for entry in untracked_directory_entries if entry.endswith("/")
    )


def _change_scope_metadata(
    untracked_directory_entries: frozenset[str], untracked_expansion: str,
) -> dict:
    """Disclose whether changed paths are file names or include untracked entries."""
    if untracked_expansion not in ("file_paths", "entry_paths"):
        raise ValueError("untracked_expansion must be 'file_paths' or 'entry_paths'")
    expanded = untracked_expansion == "file_paths"
    metadata = {
        "changed_path_granularity": (
            "all_file_paths" if expanded else "tracked_files_and_untracked_entries"
        ),
        "untracked_directory_entry_total": len(untracked_directory_entries),
        "untracked_directory_files_expanded": expanded,
        "note": (
            "Changed paths are individual file names. Cited and target paths are "
            "matched exactly."
            if expanded else
            "Changed paths are tracked file names plus Git's untracked entries. A wholly "
            "untracked directory is one entry ending in '/'; files inside it were not "
            "enumerated and are NOT ASSESSED individually. Cited and target paths are "
            "still matched exactly, including paths under an unexpanded directory. "
            "Directory entries mean at least one untracked file exists below them, not "
            "that their contents are irrelevant."
        ),
    }
    if not expanded:
        metadata["untracked_file_total"] = "NOT_ASSESSED"
    return metadata


def workspace_source_overlap(
    claims: Mapping[str, dict], relations: tuple[dict, ...], *,
    changed_paths: frozenset[str], limit: int,
    untracked_directory_entries: frozenset[str] = frozenset(),
    untracked_expansion: str = "file_paths",
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
        overlap = (
            sorted(path for path in cited
                   if _path_matches_change(path, changed_paths, untracked_directory_entries))
            if isinstance(cited, dict) else []
        )
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
        "change_scope": _change_scope_metadata(
            untracked_directory_entries, untracked_expansion),
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
            "uncited_changed_paths are coverage gaps, not evidence of no semantic effect. "
            "With untracked entry granularity, a directory entry covers unenumerated files."
        ),
    }
    return hit_claims, hit_relations, metadata



def _source_overlap(
    records: list[tuple[str, dict]], changed_paths: frozenset[str],
    untracked_directory_entries: frozenset[str],
) -> tuple[list[dict], int, int]:
    """Affected entries, records without fingerprints and mechanical records, in input order."""
    affected: list[dict] = []
    without_fingerprints = 0
    mechanical = 0
    for record_type, record in records:
        if _is_mechanical(record):
            mechanical += 1
            continue
        cited = record.get("attributes", {}).get("source_sha256")
        if not isinstance(cited, dict) or not cited:
            without_fingerprints += 1
            continue
        overlap = sorted(
            path for path in cited
            if _path_matches_change(path, changed_paths, untracked_directory_entries))
        if overlap:
            origin = record.get("source_ref", "")
            source_path = origin[5:] if origin.startswith("file:") else None
            affected.append({
                "record_type": record_type, "id": record["id"],
                "record_source_changed": source_path in overlap,
                "changed_evidence_sources": [p for p in overlap if p != source_path],
            })
    return affected, without_fingerprints, mechanical


def context_workspace_overlap(
    claims: Mapping[str, dict], relations: tuple[dict, ...], *,
    selected_claim_ids: list[str], selected_relation_ids: list[str],
    changed_paths: frozenset[str], target_path: str, limit: int,
    context_truncated: bool,
    candidate_claim_ids: tuple[str, ...] = (),
    candidate_relation_ids: tuple[str, ...] = (),
    untracked_directory_entries: frozenset[str] = frozenset(),
    untracked_expansion: str = "file_paths",
) -> dict:
    """Read-only source-path overlap for records selected by context-for.

    A changed cited file is a re-inspection candidate, never a finding that the
    authored claim is wrong. Source fingerprints describe the indexed commit,
    not the working-tree overlay. Relevance candidates, the capabilities behind
    them and their route relations are compared in a separate
    ``relevance_candidates`` block with its own limit, so they never displace a
    record of the context categories and the existing counts keep their meaning.
    """
    relation_ids = set(selected_relation_ids)
    selected = (
        [("claim", claims[cid]) for cid in selected_claim_ids if cid in claims]
        + [("relation", r) for r in relations if r["id"] in relation_ids]
    )
    affected, without_fingerprints, mechanical = _source_overlap(
        selected, changed_paths, untracked_directory_entries)
    candidate_relations = set(candidate_relation_ids) - relation_ids
    candidates = (
        [("claim", claims[cid]) for cid in candidate_claim_ids if cid in claims]
        + [("relation", r) for r in relations if r["id"] in candidate_relations]
    )
    candidate_affected, candidate_unfingerprinted, candidate_mechanical = _source_overlap(
        candidates, changed_paths, untracked_directory_entries)
    return {
        "target_path_changed": _path_matches_change(
            target_path, changed_paths, untracked_directory_entries),
        "changed_path_total": len(changed_paths),
        "change_scope": _change_scope_metadata(
            untracked_directory_entries, untracked_expansion),
        "selected_record_total": len(selected),
        "affected_record_total": len(affected),
        "affected_records": affected[:limit],
        "affected_records_omitted": max(0, len(affected) - limit),
        "records_without_fingerprints": without_fingerprints,
        "mechanical_records_not_assessed": mechanical,
        "relevance_candidates": {
            "record_total": len(candidates),
            "affected_record_total": len(candidate_affected),
            "affected_records": candidate_affected[:limit],
            "affected_records_omitted": max(0, len(candidate_affected) - limit),
            "records_without_fingerprints": candidate_unfingerprinted,
            "mechanical_records_not_assessed": candidate_mechanical,
            "note": (
                "Same path-level comparison for returned relevance candidates, the capabilities "
                "behind them and their route relations. A changed cited source is a reason to "
                "re-inspect a candidate, not evidence that it applies to this file."
            ),
        },
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



def assess_current_authored_record(
    indexed: dict, *, record_type: str, current_pack: object,
) -> dict:
    """Compare one indexed Git-authored record with its current pack entry.

    This is a per-record *representation* comparison. Missing entries could
    have moved, been removed or been replaced; no semantic validity follows.
    Source-byte auditing remains independent and conservative.
    """
    result = {
        "assessment_status": "NOT_ASSESSED",
        "authored_fields_changed": None,
        "record_at_original_path": None,
    }
    prior_path = _authored_pack(indexed)
    prior_fields = _authored_fields(indexed)
    if prior_path is None or prior_fields is None or record_type not in {"claim", "relation"}:
        result["unassessed_reason"] = "not_a_supported_indexed_authored_record"
        return result
    if not isinstance(current_pack, dict) or (
        type(current_pack.get("schema_version")) is not int
        or current_pack["schema_version"] not in AUTHORED_SCHEMA_VERSIONS
        or not isinstance(current_pack.get("claims"), list)
        or not isinstance(current_pack.get("relations"), list)
        or len(current_pack["claims"]) > 500
        or len(current_pack["relations"]) > 1000
    ):
        result["unassessed_reason"] = "current_authored_pack_missing_or_invalid"
        return result
    group = current_pack["claims" if record_type == "claim" else "relations"]
    matches = [row for row in group
               if isinstance(row, dict) and row.get("id") == indexed.get("id")]
    if len(matches) == 0:
        result["record_at_original_path"] = False
        result["unassessed_reason"] = "record_absent_from_original_pack_may_have_moved"
        return result
    if len(matches) > 1:
        result["unassessed_reason"] = "duplicate_record_id_in_current_pack"
        return result
    try:
        reader = read_authored_claim if record_type == "claim" else read_authored_relation
        current = record_dict(reader(
            matches[0], source_ref=f"file:{prior_path}",
            schema_version=current_pack["schema_version"],
        ))
        # dataclasses.asdict retains tuple evidence_refs while SQLite JSON
        # restores the indexed records' evidence_refs as lists. Normalize the
        # comparison to the indexed representation before assessing fields.
        current["evidence_refs"] = list(current["evidence_refs"])
        current_fields = _authored_fields(current)
    except (ValueError, TypeError, KeyError, AttributeError):
        result["unassessed_reason"] = "current_record_invalid_or_unparseable"
        return result
    if current_fields is None:
        result["unassessed_reason"] = "normalized_authored_fields_unavailable"
        return result
    result["assessment_status"] = "ASSESSED"
    result["authored_fields_changed"] = prior_fields != current_fields
    result["record_at_original_path"] = True
    return result


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


def possibility_evolution(
    previous_claims: Mapping[str, dict], current_claims: Mapping[str, dict],
    previous_relations: Mapping[str, dict], current_relations: Mapping[str, dict],
    *, limit: int, focus: str | None = None,
) -> dict:
    """Compare authored opportunity records and their direct authored context.

    Read the complete indexed snapshots before applying display limits. The
    same ID is a record-comparison key, not a semantic identity proof.
    """
    def authored(records: Mapping[str, dict]) -> dict[str, dict]:
        return {key: row for key, row in records.items() if _authored_pack(row) is not None}

    old_claims, new_claims = authored(previous_claims), authored(current_claims)
    old_edges, new_edges = authored(previous_relations), authored(current_relations)
    old_opps = {key for key, row in old_claims.items() if row.get("kind") == "opportunity"}
    new_opps = {key for key, row in new_claims.items() if row.get("kind") == "opportunity"}
    opportunity_ids = old_opps | new_opps
    if focus is not None:
        if focus not in opportunity_ids:
            raise ValueError("possibility focus must identify an authored opportunity at BASE or TARGET")
        old_opps &= {focus}
        new_opps &= {focus}
        opportunity_ids = {focus}

    def neighborhood(edges: Mapping[str, dict], opportunities: set[str]):
        incident = set()
        neighbors: dict[str, set[str]] = {}
        for rid, row in edges.items():
            subject, obj = row["subject"], row["object"]
            if subject in opportunities or obj in opportunities:
                incident.add(rid)
            if subject in opportunities and obj not in opportunity_ids:
                neighbors.setdefault(obj, set()).add(subject)
            if obj in opportunities and subject not in opportunity_ids:
                neighbors.setdefault(subject, set()).add(obj)
        return incident, neighbors

    old_incident, old_neighbors = neighborhood(old_edges, old_opps)
    new_incident, new_neighbors = neighborhood(new_edges, new_opps)

    def record_view(row: dict | None) -> dict | None:
        if row is None:
            return None
        fields = _authored_fields(row)
        return None if fields is None else {**fields, "source_ref": row.get("source_ref")}

    def delta(ids: set[str], old: Mapping[str, dict], new: Mapping[str, dict],
              *, old_scope: set[str], new_scope: set[str],
              link_context: bool = False) -> dict:
        groups: dict[str, list[dict]] = {"added": [], "removed": [], "changed": []}
        unchanged = 0
        link_context_truncated = False
        for identifier in sorted(ids):
            before, after = old.get(identifier), new.get(identifier)
            if before is None and after is None:
                continue
            membership_changed = (identifier in old_scope) != (identifier in new_scope)
            links_before = sorted(old_neighbors.get(identifier, set())) if link_context else []
            links_after = sorted(new_neighbors.get(identifier, set())) if link_context else []
            if before == after and not membership_changed and links_before == links_after:
                unchanged += 1
                continue
            kind = "added" if before is None else "removed" if after is None else "changed"
            row = {
                "id": identifier,
                "before": record_view(before),
                "after": record_view(after),
                "in_scope_before": identifier in old_scope,
                "in_scope_after": identifier in new_scope,
                "classification": (
                    _classify_record_change(before, after)
                    if before is not None and after is not None and before != after else None
                ),
            }
            if link_context:
                row["linked_opportunity_ids_before"] = links_before[:limit]
                row["linked_opportunity_ids_after"] = links_after[:limit]
                row["linked_opportunity_counts"] = {
                    "before": len(links_before), "after": len(links_after),
                }
                if len(links_before) > limit or len(links_after) > limit:
                    link_context_truncated = True
            groups[kind].append(row)

        # Authored field, membership and adjacency changes remain visible ahead
        # of pack-fingerprint-only changes. This is presentation, not value rank.
        def display_key(row: dict) -> tuple[int, str]:
            detail = row["classification"] or {}
            substantive = (
                detail.get("authored_fields_changed") is True
                or row["in_scope_before"] != row["in_scope_after"]
                or row.get("linked_opportunity_ids_before") != row.get("linked_opportunity_ids_after")
            )
            return (0 if substantive else 2 if detail.get("provenance_only") is True else 1,
                    row["id"])

        groups["changed"].sort(key=display_key)
        counts = {kind: len(rows) for kind, rows in groups.items()}
        return {
            **{kind: rows[:limit] for kind, rows in groups.items()},
            "counts": {**counts, "unchanged": unchanged},
            "omitted": {kind: max(0, count - limit) for kind, count in counts.items()},
            "truncated": link_context_truncated or any(count > limit for count in counts.values()),
        }

    opportunities = delta(opportunity_ids, old_claims, new_claims,
                          old_scope=old_opps, new_scope=new_opps)
    relations = delta(old_incident | new_incident, old_edges, new_edges,
                      old_scope=old_incident, new_scope=new_incident)
    linked_claims = delta(set(old_neighbors) | set(new_neighbors), old_claims, new_claims,
                          old_scope=set(old_neighbors), new_scope=set(new_neighbors),
                          link_context=True)
    focus_context = {}
    if focus is not None:
        before, after = old_claims.get(focus), new_claims.get(focus)
        presence = ("BOTH" if focus in old_opps and focus in new_opps else
                    "BASE_ONLY" if focus in old_opps else "TARGET_ONLY")
        focus_context = {
            "focus": {
                "id": focus, "opportunity_presence": presence,
                "before": record_view(before), "after": record_view(after),
                "classification": (
                    _classify_record_change(before, after)
                    if before is not None and after is not None and before != after else None
                ),
            },
            "scope": "one selected authored opportunity and direct authored neighborhood",
        }
    return {
        **focus_context,
        "opportunities": opportunities,
        "direct_authored_relations": relations,
        "directly_linked_authored_claims": linked_claims,
        "opportunity_count_before": len(old_opps),
        "opportunity_count_after": len(new_opps),
        "truncated": any(group["truncated"] for group in (opportunities, relations, linked_claims)),
        "explicit_limits": [
            "Only indexed Git-authored opportunities, incident authored relations and their directly linked authored claims are compared; no multi-hop or unindexed coverage.",
            "Added/removed mean record presence in these indexed authored snapshots, not discovery, realization, rejection or invalidation. Scope flags distinguish changing membership from record existence.",
            "Before/after show authored fields and original source pointers; classification reuses the indexed record/source fingerprint comparison.",
            "Changes in linked claims or relations are reconsideration candidates, not proof of premise necessity, enabling effects, semantic correspondence or new opportunities.",
            "Display order favors authored/membership/adjacency changes over pack-only fingerprint noise; no priority, feasibility, selection, causality or authority is inferred.",
            "Each category is independently limited; unchanged or absent records do not establish that a possibility remains warranted.",
            *([
                "Focus is explicit at either indexed revision and shown even when unchanged. Presence describes opportunity kind, not semantic validity.",
                "Only the selected opportunity's incident authored relations and directly linked authored claims (including other opportunities) are in scope. Counts and limits apply within this scope; unrelated records are NOT_ASSESSED here.",
            ] if focus is not None else []),
        ],
    }
