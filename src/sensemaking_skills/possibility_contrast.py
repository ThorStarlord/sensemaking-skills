"""Scenario-conditioned assumption contrast over an authored possibility ecology.

The agent authors assumption scenarios; this module only projects which visible
possibilities depend on the negated or retained assumptions. It does not infer
assumptions, generate possibilities, rank scenarios, select a direction or
authorize action.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

MAX_SCENARIOS = 12
MAX_REFS = 20
_SLUG = re.compile(r"[a-z0-9][a-z0-9-]{0,63}\Z")


def _text(value: Any, field: str, *, maximum: int = 400) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValueError(
            f"{field} must be a non-empty string of at most {maximum} characters"
        )
    return value.strip()


def _refs(value: Any, field: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a list of claim ids")
    if len(value) > MAX_REFS:
        raise ValueError(f"{field} accepts at most {MAX_REFS} entries")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{field} entries must be non-empty claim ids")
        item = item.strip()
        if item not in result:
            result.append(item)
    return result


def _candidate_records(ecology: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    candidates: list[Mapping[str, Any]] = []
    seen: set[str] = set()
    for key in ("candidates", "descendant_goal_candidates"):
        values = ecology.get(key) or []
        if not isinstance(values, list):
            continue
        for item in values:
            if not isinstance(item, Mapping):
                continue
            identifier = item.get("claim_id")
            if isinstance(identifier, str) and identifier and identifier not in seen:
                seen.add(identifier)
                candidates.append(item)
    return candidates


def _is_assumption(relation: Mapping[str, Any]) -> bool:
    conceptual = str(relation.get("conceptual_relation") or "").strip().casefold()
    return conceptual.startswith("assumes") or conceptual.startswith(
        "sharesassumption"
    )


def _is_capability(relation: Mapping[str, Any]) -> bool:
    return (
        relation.get("predicate") == "requires_capability"
        and relation.get("other_kind") == "capability"
    )


def _is_conflict(relation: Mapping[str, Any]) -> bool:
    return relation.get("predicate") == "contradicts"


def _candidate_view(
    candidate: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], set[str]]:
    """Return the candidate's visible assumptions, capabilities, and linked claims."""

    identifier = str(candidate["claim_id"])
    assumptions: dict[str, dict[str, Any]] = {}
    capabilities: dict[str, dict[str, Any]] = {}
    conflicts: list[dict[str, Any]] = []
    linked: set[str] = set()
    relationships = candidate.get("relationships") or []
    for relation in relationships:
        if not isinstance(relation, Mapping):
            continue
        other_id = relation.get("other_claim_id")
        if not isinstance(other_id, str) or not other_id:
            continue
        linked.add(other_id)
        if _is_assumption(relation):
            assumptions.setdefault(other_id, {
                "claim_id": other_id,
                "statement": relation.get("other_statement"),
                "kind": relation.get("other_kind"),
                "epistemic_status": relation.get("other_epistemic_status"),
                "authority_kind": relation.get("other_authority_kind"),
                "conceptual_relation": relation.get("conceptual_relation"),
                "relation_id": relation.get("relation_id"),
                "relation_evidence_refs": list(
                    relation.get("relation_evidence_refs") or []
                ),
            })
        elif _is_capability(relation):
            capabilities.setdefault(other_id, {
                "claim_id": other_id,
                "statement": relation.get("other_statement"),
                "kind": relation.get("other_kind"),
                "epistemic_status": relation.get("other_epistemic_status"),
                "authority_kind": relation.get("other_authority_kind"),
                "relation_id": relation.get("relation_id"),
            })
        elif _is_conflict(relation):
            conflicts.append({
                "claim_id": other_id,
                "statement": relation.get("other_statement"),
                "kind": relation.get("other_kind"),
                "epistemic_status": relation.get("other_epistemic_status"),
                "relation_id": relation.get("relation_id"),
            })

    view = {
        "claim_id": identifier,
        "statement": candidate.get("statement"),
        "candidate_scope": candidate.get("candidate_scope"),
        "via_goals": candidate.get("via_goals") or [],
        "assumptions": sorted(assumptions.values(), key=lambda item: item["claim_id"]),
        "capabilities": sorted(capabilities.values(), key=lambda item: item["claim_id"]),
        "conflicts": sorted(conflicts, key=lambda item: item["claim_id"]),
        "relationship_total": candidate.get("relationship_total"),
        "relationship_omitted": candidate.get("relationship_omitted"),
        "assumption_coverage": (
            "PARTIAL"
            if (candidate.get("relationship_omitted") or 0) > 0
            else "COMPLETE"
        ),
    }
    return view, assumptions, linked


def _scenarios(document: Mapping[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(document, Mapping):
        raise ValueError("scenario document must be a JSON object")
    unknown = set(document) - {"scenarios"}
    if unknown:
        raise ValueError(f"unknown scenario document fields: {sorted(unknown)}")
    raw = document.get("scenarios")
    if not isinstance(raw, list) or not 1 <= len(raw) <= MAX_SCENARIOS:
        raise ValueError(f"scenarios must contain 1..{MAX_SCENARIOS} entries")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in raw:
        if not isinstance(item, Mapping):
            raise ValueError("each scenario must be an object")
        unknown = set(item) - {"id", "negated", "held"}
        if unknown:
            raise ValueError(f"unknown scenario fields: {sorted(unknown)}")
        identifier = _text(item.get("id"), "scenario.id", maximum=64)
        if not _SLUG.fullmatch(identifier):
            raise ValueError("scenario.id must be a lowercase slug (1..64 characters)")
        if identifier in seen:
            raise ValueError(f"duplicate scenario id: {identifier}")
        seen.add(identifier)
        negated = _refs(item.get("negated"), f"scenario {identifier}.negated")
        held = _refs(item.get("held"), f"scenario {identifier}.held")
        overlap = sorted(set(negated) & set(held))
        if overlap:
            raise ValueError(
                f"scenario {identifier} both holds and negates: {', '.join(overlap)}"
            )
        result.append({"id": identifier, "negated": negated, "held": held})
    return result


def build_possibility_contrast(
    ecology: Mapping[str, Any], document: Mapping[str, Any]
) -> dict[str, Any]:
    """Project authored assumptions and agent-authored scenarios.

    Only visible one-hop candidate relationships are read. A candidate whose
    relationship projection is truncated is marked ``PARTIAL``; an absent
    assumption is ``NOT_ASSESSED``, not evidence that no assumption exists.
    """

    if not isinstance(ecology, Mapping):
        raise ValueError("ecology must be an object")
    scenario_list = _scenarios(document)
    candidate_records = _candidate_records(ecology)
    candidate_omitted = int(ecology.get("candidate_omitted") or 0)
    descendant_omitted = int(ecology.get("descendant_candidate_omitted") or 0)
    if not candidate_records:
        return {
            "focus_kind": ecology.get("focus_kind"),
            "focus": ecology.get("focus"),
            "candidate_count": 0,
            "assumption_count": 0,
            "assumptions": [],
            "shared_assumptions": [],
            "unassessed_candidates": [],
            "scenario_results": [],
            "coverage": {
                "candidate_total": 0,
                "candidate_omitted": candidate_omitted,
                "descendant_candidate_omitted": descendant_omitted,
                "assumption_total": 0,
                "unassessed_candidate_total": 0,
                "relationship_omitted_candidate_total": 0,
            },
            "selection_performed": False,
            "recommendation_performed": False,
            "semantic_truth_established": False,
            "action_authorized": False,
            "explicit_limits": [
                "No candidate possibilities were visible in the bounded ecology; "
                "assumption coverage is NOT_ASSESSED, not evidence that none exist.",
                "The tool does not generate, rank, select or recommend a possibility.",
            ],
        }

    candidates: list[dict[str, Any]] = []
    assumption_index: dict[str, dict[str, Any]] = {}
    linked_by_candidate: dict[str, set[str]] = {}
    for record in candidate_records:
        view, assumptions, linked = _candidate_view(record)
        candidates.append(view)
        linked_by_candidate[view["claim_id"]] = linked
        for assumption_id, assumption in assumptions.items():
            entry = assumption_index.setdefault(assumption_id, {
                **assumption,
                "used_by": [],
            })
            if view["claim_id"] not in entry["used_by"]:
                entry["used_by"].append(view["claim_id"])
    assumption_list = sorted(assumption_index.values(), key=lambda item: item["claim_id"])
    known_assumptions = set(assumption_index)

    for scenario in scenario_list:
        unknown = sorted(
            (set(scenario["negated"]) | set(scenario["held"])) - known_assumptions
        )
        if unknown:
            raise ValueError(
                f"scenario {scenario['id']} references assumptions not used by any "
                f"visible candidate: {', '.join(unknown)}"
            )

    shared_assumptions: list[dict[str, Any]] = []
    for assumption in assumption_list:
        users = sorted(assumption["used_by"])
        if len(users) < 2:
            continue
        pairs = [
            {"candidates": [left, right],
             "direct_relation": bool(
                 right in linked_by_candidate.get(left, set())
                 or left in linked_by_candidate.get(right, set())
             )}
            for index, left in enumerate(users)
            for right in users[index + 1:]
        ]
        shared_assumptions.append({
            "assumption_id": assumption["claim_id"],
            "statement": assumption.get("statement"),
            "candidate_ids": users,
            "pairs": pairs,
            "pairs_without_direct_relation": [
                pair["candidates"] for pair in pairs if not pair["direct_relation"]
            ],
            "assessment": (
                "UNREPRESENTED_COMBINATION"
                if any(not pair["direct_relation"] for pair in pairs)
                else "RELATED"
            ),
        })

    scenario_results: list[dict[str, Any]] = []
    for scenario in scenario_list:
        negated = set(scenario["negated"])
        held = set(scenario["held"])
        affected: list[dict[str, Any]] = []
        unaffected: list[dict[str, Any]] = []
        unassessed: list[dict[str, Any]] = []
        conflicts: list[dict[str, Any]] = []
        capability_ids: set[str] = set()
        for candidate in candidates:
            assumed = {item["claim_id"] for item in candidate["assumptions"]}
            negated_hits = sorted(assumed & negated)
            conflict_hits = sorted(
                item["claim_id"] for item in candidate["conflicts"] if item["claim_id"] in held
            )
            summary = {
                "claim_id": candidate["claim_id"],
                "statement": candidate["statement"],
                "candidate_scope": candidate["candidate_scope"],
                "via_goals": candidate["via_goals"],
                "assumption_count": len(assumed),
                "negated_assumptions": negated_hits,
                "capability_ids": [
                    item["claim_id"] for item in candidate["capabilities"]
                ],
                "assumption_coverage": candidate["assumption_coverage"],
            }
            capability_ids.update(summary["capability_ids"])
            if not assumed:
                summary["state"] = "NOT_ASSESSED"
                unassessed.append(summary)
            elif negated_hits:
                summary["state"] = "AFFECTED"
                affected.append(summary)
            else:
                summary["state"] = "UNAFFECTED"
                unaffected.append(summary)
            for conflict_id in conflict_hits:
                conflicts.append({
                    "claim_id": candidate["claim_id"],
                    "conflicts_with": conflict_id,
                    "state": "CONFLICTS_WITH_HELD_ASSUMPTION",
                })
        scenario_results.append({
            "id": scenario["id"],
            "negated": scenario["negated"],
            "held": scenario["held"],
            "affected": affected,
            "unaffected": unaffected,
            "unassessed": unassessed,
            "conflicts": conflicts,
            "counts": {
                "affected": len(affected),
                "unaffected": len(unaffected),
                "unassessed": len(unassessed),
                "conflicts": len(conflicts),
            },
            "capability_ids": sorted(capability_ids),
        })

    unassessed_candidates = [
        {"claim_id": item["claim_id"], "statement": item["statement"],
         "candidate_scope": item["candidate_scope"]}
        for item in candidates if not item["assumptions"]
    ]
    relationship_omitted = [
        item["claim_id"] for item in candidates
        if (item["relationship_omitted"] or 0) > 0
    ]
    explicit_limits = [
        "Reads only visible one-hop candidate relationships. A candidate with "
        "relationship_omitted > 0 has PARTIAL assumption coverage; use explain "
        "on that claim before relying on an absence.",
        "Assumptions are authored references with conceptual_relation assumes "
        "or sharesAssumptionWith. Other premises are NOT_ASSESSED, not absent.",
        "A scenario is a hypothetical retention or negation, not evidence that "
        "an assumption is true or false.",
        "Shared assumptions and missing direct relations are questions for the "
        "agent, not recommendations or combinations the tool endorses.",
        "The tool does not generate, rank, select or recommend a possibility, "
        "and it does not authorize construction.",
    ]
    if candidate_omitted or descendant_omitted:
        explicit_limits.insert(
            0,
            f"The candidate projection omitted {candidate_omitted} direct and "
            f"{descendant_omitted} descendant candidate(s) by the query limit; "
            "omitted candidates were not contrasted. The affected, unaffected, "
            "unassessed and shared-assumption results are PARTIAL, not the "
            "complete candidate set.",
        )
    return {
        "focus_kind": ecology.get("focus_kind"),
        "focus": ecology.get("focus"),
        "candidate_count": len(candidates),
        "assumption_count": len(assumption_list),
        "assumptions": assumption_list,
        "shared_assumptions": shared_assumptions,
        "candidates": candidates,
        "unassessed_candidates": unassessed_candidates,
        "scenario_results": scenario_results,
        "coverage": {
            "candidate_total": len(candidates),
            "candidate_omitted": candidate_omitted,
            "descendant_candidate_omitted": descendant_omitted,
            "assumption_total": len(assumption_list),
            "unassessed_candidate_total": len(unassessed_candidates),
            "relationship_omitted_candidate_total": len(relationship_omitted),
            "relationship_omitted_candidate_ids": sorted(relationship_omitted),
        },
        "selection_performed": False,
        "recommendation_performed": False,
        "semantic_truth_established": False,
        "action_authorized": False,
        "explicit_limits": explicit_limits,
        "scenario_count": len(scenario_results),
    }
