"""Bounded standing of authored consequence hypotheses over existing evidence.

A prediction is a `hypothesis` claim with a ``conseq:`` id. A later assessment is
an ``observation`` claim that resolves it through an existing ``references``
relation and carries the authored assessment attributes. This module joins those
authored records with the source-byte currency the audit already computed.

It never decides whether a prediction was right, and it never converts observed
consistency into causation, benefit or failure. A consequence with no assessment
is NOT ASSESSED, not refuted; a changed source is a re-inspection candidate, not
an invalid prediction.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping

NO_ASSESSMENT = "NO_ASSESSMENT"
MIXED_ASSESSMENTS = "MIXED_ASSESSMENTS"
SUPERSEDED_ASSESSMENT = "SUPERSEDED"

_MAX_SOURCE_LIST = 8
_NO_ASSESSMENT_REASON = "NO_ASSESSMENT"
_ASSESSMENT_SOURCES_CHANGED = "ASSESSMENT_SOURCES_CHANGED"
_PREDICTION_SOURCES_CHANGED = "PREDICTION_SOURCES_CHANGED"

_NOTE = (
    "Standing joins authored consequence hypotheses with authored assessments and "
    "the audit's existing source-byte currency. It does not rank predictions, prove "
    "causation, or show that a design succeeded or failed."
)


def _assessment_status(claim: Mapping[str, Any]) -> str | None:
    if claim.get("kind") != "observation":
        return None
    status = (claim.get("attributes") or {}).get("assessment_status")
    return status if isinstance(status, str) else None


def _reaches(start: str, target: str, edges: Mapping[str, set[str]]) -> bool:
    pending = list(edges.get(start, ()))
    seen: set[str] = set()
    while pending:
        node = pending.pop()
        if node == target:
            return True
        if node in seen:
            continue
        seen.add(node)
        pending.extend(edges.get(node, ()))
    return False


def assessment_supersession(
    claims: Mapping[str, Mapping[str, Any]],
    relations: Iterable[Mapping[str, Any]],
) -> tuple[dict[str, set[str]], set[str]]:
    """Derive assessment supersession from same-prediction ``supersedes`` edges.

    An edge applies only when both endpoints are consequence assessments for the
    same ``conseq:`` hypothesis. The mapping is superseded -> superseding IDs.
    The set contains assessments on an invalid supersession cycle; callers keep
    those assessments active rather than letting a cycle erase the standing.
    """
    superseded_by: dict[str, set[str]] = {}
    for relation in relations:
        if relation.get("predicate") != "supersedes":
            continue
        subject, target = relation.get("subject"), relation.get("object")
        if not isinstance(subject, str) or not isinstance(target, str):
            continue
        subject_claim = claims.get(subject) or {}
        target_claim = claims.get(target) or {}
        if subject_claim.get("kind") != "observation" or target_claim.get("kind") != "observation":
            continue
        subject_ref = (subject_claim.get("attributes") or {}).get("consequence_ref")
        target_ref = (target_claim.get("attributes") or {}).get("consequence_ref")
        if not isinstance(subject_ref, str) or not subject_ref.startswith("conseq:"):
            continue
        if subject_ref != target_ref:
            continue
        superseded_by.setdefault(target, set()).add(subject)
    nodes = set(superseded_by)
    for subjects in superseded_by.values():
        nodes.update(subjects)
    cyclic = {node for node in nodes if _reaches(node, node, superseded_by)}
    return superseded_by, cyclic


def _currency(currency: Mapping[str, Mapping[str, Any]], identifier: str) -> dict:
    entry = currency.get(identifier) or {}
    changed = entry.get("changed") or []
    missing = entry.get("missing") or []
    return {
        "assessed": bool(entry.get("assessed")),
        "changed": sorted(value for value in changed if isinstance(value, str)),
        "missing": sorted(value for value in missing if isinstance(value, str)),
    }


def _drifted(entry: Mapping[str, Any]) -> bool:
    return bool(entry["changed"] or entry["missing"])


def consequence_standing(
    claims: Mapping[str, Mapping[str, Any]],
    relations: Iterable[Mapping[str, Any]],
    *,
    currency: Mapping[str, Mapping[str, Any]],
    limit: int,
) -> dict:
    """Project standing per ``conseq:`` hypothesis from authored records only."""
    if not 1 <= limit <= 500:
        raise ValueError("consequence standing limit must be between 1 and 500")

    assessments_by_consequence: dict[str, set[str]] = {}
    for relation in relations:
        if relation.get("predicate") != "references":
            continue
        subject, target = relation.get("subject"), relation.get("object")
        if not isinstance(subject, str) or not isinstance(target, str):
            continue
        if not target.startswith("conseq:"):
            continue
        if _assessment_status(claims.get(subject) or {}) is None:
            continue
        assessments_by_consequence.setdefault(target, set()).add(subject)

    superseded_by, cyclic = assessment_supersession(claims, relations)

    rows: list[dict] = []
    status_counts: dict[str, int] = {}
    not_assessed: list[str] = []
    for identifier in sorted(claims):
        claim = claims[identifier]
        if not identifier.startswith("conseq:") or claim.get("kind") != "hypothesis":
            continue
        attributes = claim.get("attributes") or {}
        assessment_ids = sorted(assessments_by_consequence.get(identifier, ()))
        history: list[dict] = []
        active_statuses: list[str] = []
        for assessment in assessment_ids:
            status = _assessment_status(claims[assessment]) or ""
            authored_superseded = status == SUPERSEDED_ASSESSMENT
            active = not authored_superseded and assessment not in superseded_by
            if assessment in cyclic:
                active = not authored_superseded
            history.append({
                "assessment_id": assessment,
                "assessment_status": status,
                "active": active,
                "superseded_by": (
                    [] if assessment in cyclic else sorted(superseded_by.get(assessment, ()))
                ),
            })
            if active:
                active_statuses.append(status)
        distinct = sorted({status for status in active_statuses if status})
        if not assessment_ids:
            standing = NO_ASSESSMENT
        elif not distinct:
            standing = SUPERSEDED_ASSESSMENT
        elif len(distinct) == 1:
            standing = distinct[0]
        else:
            standing = MIXED_ASSESSMENTS
        status_counts[standing] = status_counts.get(standing, 0) + 1

        active_assessment_ids = [
            entry["assessment_id"] for entry in history if entry["active"]
        ]
        prediction_currency = _currency(currency, identifier)
        assessment_currency = [
            _currency(currency, item) for item in active_assessment_ids
        ]
        currency_assessed = prediction_currency["assessed"] and all(
            entry["assessed"] for entry in assessment_currency
        )
        if not currency_assessed:
            not_assessed.append(identifier)
            due, reason = False, None
        elif not assessment_ids:
            due, reason = True, _NO_ASSESSMENT_REASON
        elif any(_drifted(entry) for entry in assessment_currency):
            due, reason = True, _ASSESSMENT_SOURCES_CHANGED
        elif _drifted(prediction_currency):
            due, reason = True, _PREDICTION_SOURCES_CHANGED
        else:
            due, reason = False, None

        changed = sorted({
            path for entry in [prediction_currency, *assessment_currency]
            for path in entry["changed"]
        })
        missing = sorted({
            path for entry in [prediction_currency, *assessment_currency]
            for path in entry["missing"]
        })
        legacy = attributes.get("assessments")
        rows.append({
            "consequence_id": identifier,
            "category": attributes.get("category") or "NOT_RECORDED",
            "source_option": attributes.get("source_option") or "NOT_RECORDED",
            "analysis_ref": attributes.get("analysis_ref") or "NOT_RECORDED",
            "would_change_decision_if": attributes.get("would_change_decision_if") or "NOT_RECORDED",
            "decision_changing": bool(attributes.get("decision_changing", False)),
            "feedback_outcome": attributes.get("feedback_outcome") or "NOT_RECORDED",
            "standing": standing,
            "assessment_ids": assessment_ids,
            "assessment_statuses": distinct,
            "assessment_history": history,
            "supersession_integrity": (
                "CYCLE" if any(item in cyclic for item in assessment_ids) else None
            ),
            "assessed_at_revisions": sorted({
                str((claims[item].get("attributes") or {}).get("assessed_at_revision"))
                for item in assessment_ids
                if (claims[item].get("attributes") or {}).get("assessed_at_revision")
            }),
            "due_for_recheck": due,
            "recheck_reason": reason,
            "source_currency": (
                "ASSESSED" if currency_assessed else "NOT_ASSESSED"
            ),
            "changed_sources": changed[:_MAX_SOURCE_LIST],
            "changed_sources_total": len(changed),
            "missing_sources": missing[:_MAX_SOURCE_LIST],
            "missing_sources_total": len(missing),
            "legacy_assessment_entries": len(legacy) if isinstance(legacy, list) else 0,
        })

    option_totals: dict[str, int] = {}
    for row in rows:
        source_option = row["source_option"]
        if source_option != "NOT_RECORDED":
            option_totals[source_option] = option_totals.get(source_option, 0) + 1

    visible_rows = rows[:limit]
    decision_links: dict[str, dict] = {}
    for row in visible_rows:
        source_option = row["source_option"]
        if source_option == "NOT_RECORDED":
            continue
        option = claims.get(source_option) or {}
        option_attributes = option.get("attributes")
        option_attributes = option_attributes if isinstance(option_attributes, Mapping) else {}
        preference = option_attributes.get("preference")
        preference_view = None
        if isinstance(preference, Mapping):
            preference_view = {
                key: preference.get(key) for key in
                ("status", "current_scope", "scope", "attributed_to", "authority", "basis")
                if preference.get(key) is not None
            }
            preference_history = preference.get("history")
            if isinstance(preference_history, list) and preference_history:
                preference_view["history"] = preference_history[-2:]
        link = decision_links.setdefault(source_option, {
            "source_option": source_option,
            "option_title": option_attributes.get("title") or "NOT_RECORDED",
            "option_preference": preference_view,
            "analysis_refs": [],
            "consequence_ids": [],
            "consequence_total": option_totals.get(source_option, 0),
            "standings": [],
            "decision_changing_consequences": [],
            "feedback_outcomes": [],
            "reconsideration": "AGENT_OWNED",
            "note": (
                "Authored decision link for the returned consequences only; "
                "consequence_total and complete disclose omitted members. Inspect "
                "the original option, prediction and analysis before reconsidering."
            ),
        })
        if row["analysis_ref"] != "NOT_RECORDED" and row["analysis_ref"] not in link["analysis_refs"]:
            link["analysis_refs"].append(row["analysis_ref"])
        link["consequence_ids"].append(row["consequence_id"])
        link["standings"].append({
            "consequence_id": row["consequence_id"],
            "standing": row["standing"],
            "due_for_recheck": row["due_for_recheck"],
            "recheck_reason": row["recheck_reason"],
        })
        if row["decision_changing"]:
            link["decision_changing_consequences"].append(row["consequence_id"])
        if row["feedback_outcome"] != "NOT_RECORDED" and row["feedback_outcome"] not in link["feedback_outcomes"]:
            link["feedback_outcomes"].append(row["feedback_outcome"])
    for link in decision_links.values():
        returned = len(link["consequence_ids"])
        link["consequence_returned_total"] = returned
        link["consequence_omitted_total"] = max(0, link["consequence_total"] - returned)
        link["complete"] = link["consequence_omitted_total"] == 0
    links = sorted(decision_links.values(), key=lambda item: item["source_option"])
    total_links = len(option_totals)
    returned_links = len(links)
    partial_links = sum(1 for link in links if not link["complete"])

    due_rows = [row["consequence_id"] for row in rows if row["due_for_recheck"]]
    return {
        "consequence_total": len(rows),
        "returned_consequence_total": len(visible_rows),
        "assessed_total": sum(1 for row in rows if row["assessment_ids"]),
        "not_assessed_total": sum(1 for row in rows if not row["assessment_ids"]),
        "due_for_recheck_total": len(due_rows),
        "status_counts": dict(sorted(status_counts.items())),
        "consequences": visible_rows,
        "decision_links": links,
        "decision_link_total": total_links,
        "decision_link_returned_total": returned_links,
        "decision_link_omitted_total": max(0, total_links - returned_links),
        "decision_link_partial_total": partial_links,
        "due_for_recheck": due_rows[:limit],
        "omitted": max(0, len(rows) - limit),
        "truncated": len(rows) > limit,
        "currency_not_assessed": not_assessed[:limit],
        "currency_not_assessed_total": len(not_assessed),
        "note": _NOTE,
        "explicit_limits": [
            "A recorded assessment is an attributed observation, not a decision, authority or proof.",
            "Consistency is not causation; no status shows that the design produced the effect or a benefit.",
            "NO_ASSESSMENT is NOT ASSESSED, not refuted; a superseded prediction keeps its history.",
            "Changed or missing cited bytes make re-inspection worthwhile; they do not invalidate a prediction.",
            "The authored knowledge pack a record lives in is excluded from its own currency comparison.",
            "Decision links are authored source-option/preference references; they do not show selection, validity or that reconsideration is warranted.",
            "Source-byte currency is not experiential currentness; a new experience is represented only by a new assessment observation.",
            "Each assessment keeps its authored status in assessment_history. A same-prediction supersedes edge, or an authored SUPERSEDED status, excludes it from current standing; the original assertion is never rewritten.",
            "MIXED_ASSESSMENTS means active assessments disagree. A supersession cycle is exposed as supersession_integrity CYCLE and does not erase every assessment from current standing.",
            "decision_link_total counts distinct recorded source-option groups; decision_link_returned_total counts groups present in this bounded view. A returned link with complete false omits member consequences.",
            "A revised prediction remains visible; inspect its epistemic_status and supersedes relations rather than treating a superseded prediction as current.",
        ],
    }
