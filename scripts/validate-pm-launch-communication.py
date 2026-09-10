#!/usr/bin/env python3
"""Validate PM launch, GTM, competitive enablement, and communication artifacts.

This validator checks representation, evidence/status, identity/reference, and
explicit authority invariants. It does not establish readiness, market success,
competitive superiority, publication approval, or stakeholder agreement.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

VALIDATOR = "validate-pm-launch-communication.py"
SUPPORTED = {
    "readiness_report",
    "gtm_plan",
    "battlecard",
    "feature_announcement",
    "stakeholder_update",
}
HANDOFF_RE = re.compile(
    r"^##\s+(?:\d+\.\s*)?Machine-readable handoff\s*$\s*```yaml\s*(.*?)\s*```",
    re.MULTILINE | re.IGNORECASE | re.DOTALL,
)
SECTIONS = {
    "readiness_report": (
        "Launch context",
        "Evidence inventory",
        "Cross-functional readiness",
        "Launch-blocking conditions",
        "Go or no-go recommendation",
        "Rollback and monitoring",
        "Authority and unknowns",
    ),
    "gtm_plan": (
        "Objective and audience",
        "Evidence and positioning",
        "Channel strategy",
        "Messaging",
        "Timeline and coordination",
        "Metrics and contingencies",
        "Authority and unknowns",
    ),
    "battlecard": (
        "Scope and currentness",
        "Evidence inventory",
        "Competitive claims",
        "Comparison and where each side wins",
        "Objections and discovery questions",
        "Win-loss patterns and unknowns",
    ),
    "feature_announcement": (
        "Audience and release scope",
        "Source evidence",
        "Headline and summary",
        "Changes and user value",
        "Fixes performance and known issues",
        "Coming soon and commitments",
        "Publication boundary and unknowns",
    ),
    "stakeholder_update": (
        "Audience and currentness",
        "Executive summary",
        "Situation and evidence",
        "Analysis and decisions",
        "Next steps",
        "Risks and unresolved questions",
        "Distribution boundary",
    ),
}
EVIDENCE_STATES = {"hypothesis", "inferred", "observed", "unknown"}


def err(code: str, field: str, message: str, value: Any = None) -> dict[str, Any]:
    return {
        "error_id": code,
        "error_type": "contract_error",
        "field": field,
        "current_value": value,
        "message": message,
        "suggested_fixes": [],
        "reference": "docs/product-management/artifact-contracts.md",
    }


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def string_list(value: Any) -> bool:
    return isinstance(value, list) and all(text(item) for item in value)


def require(data: dict[str, Any], fields: tuple[str, ...], errors: list[dict[str, Any]]) -> None:
    for field in fields:
        if field not in data:
            errors.append(err("PM_MISSING_FIELD", field, f"required field {field!r} is missing"))


def list_value(data: dict[str, Any], field: str, errors: list[dict[str, Any]]) -> list[Any]:
    value = data.get(field)
    if not isinstance(value, list):
        errors.append(err("PM_LIST_REQUIRED", field, f"{field} must be a list", value))
        return []
    return value


def unique_ids(items: list[Any], field: str, errors: list[dict[str, Any]]) -> list[str]:
    ids: list[str] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict) or not text(item.get("id")):
            errors.append(err("PM_ID_REQUIRED", f"{field}[{index}].id", "non-empty id required"))
            continue
        ids.append(item["id"].strip())
    if len(ids) != len(set(ids)):
        errors.append(err("PM_DUPLICATE_ID", field, f"{field} contains duplicate ids", ids))
    return ids


def evidence_refs(item: dict[str, Any], field: str, errors: list[dict[str, Any]]) -> list[str]:
    refs = item.get("evidence_refs", [])
    if not string_list(refs):
        errors.append(err("PM_INVALID_EVIDENCE_REFS", field, "evidence refs must be a list of non-empty strings", refs))
        return []
    return refs


def validate_readiness(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    require(data, (
        "schema_version", "status", "launch_scope", "launch_tier", "target_window",
        "evidence_window", "evidence_refs", "checks", "recommendation", "conditions",
        "rollback_triggers", "monitoring_requirements", "external_launch_authority_ref",
        "unresolved_questions",
    ), errors)
    status = data.get("status")
    if status not in {"planning", "assessed"}:
        errors.append(err("PM_INVALID_STATUS", "status", "status must be planning or assessed", status))
    if not text(data.get("launch_scope")):
        errors.append(err("PM_TEXT_REQUIRED", "launch_scope", "launch_scope must be non-empty"))
    if data.get("launch_tier") not in {"tier1", "tier2", "tier3", "unspecified"}:
        errors.append(err("PM_INVALID_TYPE", "launch_tier", "invalid launch tier", data.get("launch_tier")))
    if not text(data.get("evidence_window")):
        errors.append(err("PM_TEXT_REQUIRED", "evidence_window", "evidence_window must be non-empty"))
    if not string_list(data.get("evidence_refs")):
        errors.append(err("PM_INVALID_EVIDENCE_REFS", "evidence_refs", "evidence_refs must be a list of strings", data.get("evidence_refs")))

    checks = list_value(data, "checks", errors)
    unique_ids(checks, "checks", errors)
    blocking_states: list[str] = []
    for index, item in enumerate(checks):
        if not isinstance(item, dict):
            errors.append(err("PM_MAPPING_REQUIRED", f"checks[{index}]", "check must be a mapping", item))
            continue
        if item.get("function") not in {"engineering", "design", "marketing", "sales", "support", "legal", "operations", "analytics", "other"}:
            errors.append(err("PM_INVALID_TYPE", f"checks[{index}].function", "invalid readiness function", item.get("function")))
        if not text(item.get("requirement")):
            errors.append(err("PM_TEXT_REQUIRED", f"checks[{index}].requirement", "check requirement must be non-empty"))
        criticality = item.get("criticality")
        if criticality not in {"launch_blocking", "required", "advisory"}:
            errors.append(err("PM_INVALID_TYPE", f"checks[{index}].criticality", "invalid criticality", criticality))
        state = item.get("state")
        if state not in {"unknown", "planned", "evidence_backed_complete", "blocked", "not_applicable"}:
            errors.append(err("PM_INVALID_STATUS", f"checks[{index}].state", "invalid readiness state", state))
        refs = evidence_refs(item, f"checks[{index}].evidence_refs", errors)
        if state == "evidence_backed_complete" and not refs:
            errors.append(err("PM_EVIDENCE_REQUIRED", f"checks[{index}].evidence_refs", "completed readiness check requires evidence refs"))
        if state == "not_applicable" and not text(item.get("note")):
            errors.append(err("PM_REASON_REQUIRED", f"checks[{index}].note", "not_applicable check requires a reason"))
        if criticality == "launch_blocking":
            blocking_states.append(str(state))

    recommendation = data.get("recommendation")
    if recommendation not in {"not_assessed", "go", "go_with_conditions", "no_go"}:
        errors.append(err("PM_INVALID_STATUS", "recommendation", "invalid readiness recommendation", recommendation))
    if status == "planning" and recommendation != "not_assessed":
        errors.append(err("PM_STATUS_CONFLICT", "recommendation", "planning status cannot claim an assessed recommendation", recommendation))
    if recommendation == "go":
        if status != "assessed":
            errors.append(err("PM_STATUS_CONFLICT", "status", "go recommendation requires assessed status", status))
        if any(state in {"unknown", "planned", "blocked"} for state in blocking_states):
            errors.append(err("PM_BLOCKER_CONFLICT", "checks", "go recommendation cannot coexist with unresolved launch-blocking checks", blocking_states))
    if recommendation == "go_with_conditions" and not list_value(data, "conditions", errors):
        errors.append(err("PM_CONDITIONS_REQUIRED", "conditions", "go_with_conditions requires at least one condition"))
    else:
        if not isinstance(data.get("conditions"), list):
            pass

    triggers = list_value(data, "rollback_triggers", errors)
    unique_ids(triggers, "rollback_triggers", errors)
    for index, item in enumerate(triggers):
        if not isinstance(item, dict):
            errors.append(err("PM_MAPPING_REQUIRED", f"rollback_triggers[{index}]", "rollback trigger must be a mapping"))
            continue
        if not text(item.get("statement")):
            errors.append(err("PM_TEXT_REQUIRED", f"rollback_triggers[{index}].statement", "rollback trigger statement required"))
        if item.get("status") != "proposed":
            errors.append(err("PM_INVALID_STATUS", f"rollback_triggers[{index}].status", "rollback triggers remain proposed", item.get("status")))
    list_value(data, "monitoring_requirements", errors)
    list_value(data, "unresolved_questions", errors)


def validate_gtm(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    require(data, (
        "schema_version", "status", "offer", "target_segment", "objective", "evidence_window",
        "evidence_refs", "positioning_claims", "channels", "messages", "metrics", "timeline",
        "contingencies", "external_execution_authority_ref", "unresolved_questions",
    ), errors)
    if data.get("status") != "proposed":
        errors.append(err("PM_INVALID_STATUS", "status", "gtm_plan status must remain proposed", data.get("status")))
    for field in ("offer", "target_segment", "objective", "evidence_window"):
        if not text(data.get(field)):
            errors.append(err("PM_TEXT_REQUIRED", field, f"{field} must be non-empty"))
    if not string_list(data.get("evidence_refs")):
        errors.append(err("PM_INVALID_EVIDENCE_REFS", "evidence_refs", "evidence_refs must be a list of strings", data.get("evidence_refs")))

    claims = list_value(data, "positioning_claims", errors)
    claim_ids = unique_ids(claims, "positioning_claims", errors)
    for index, item in enumerate(claims):
        if not isinstance(item, dict):
            continue
        if not text(item.get("statement")):
            errors.append(err("PM_TEXT_REQUIRED", f"positioning_claims[{index}].statement", "claim statement required"))
        status = item.get("evidence_status")
        if status not in EVIDENCE_STATES:
            errors.append(err("PM_INVALID_EVIDENCE_STATUS", f"positioning_claims[{index}].evidence_status", "invalid evidence status", status))
        refs = evidence_refs(item, f"positioning_claims[{index}].evidence_refs", errors)
        if status == "observed" and not refs:
            errors.append(err("PM_EVIDENCE_REQUIRED", f"positioning_claims[{index}].evidence_refs", "observed positioning claim requires evidence refs"))

    known_claims = set(claim_ids)
    for field in ("channels", "messages"):
        items = list_value(data, field, errors)
        unique_ids(items, field, errors)
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                continue
            if item.get("status") != "proposed":
                errors.append(err("PM_INVALID_STATUS", f"{field}[{index}].status", f"{field} entries remain proposed", item.get("status")))
            if field == "channels":
                for required in ("name", "rationale"):
                    if not text(item.get(required)):
                        errors.append(err("PM_TEXT_REQUIRED", f"{field}[{index}].{required}", f"{required} required"))
            else:
                for required in ("audience", "text"):
                    if not text(item.get(required)):
                        errors.append(err("PM_TEXT_REQUIRED", f"{field}[{index}].{required}", f"{required} required"))
            refs = item.get("source_claim_refs", [])
            if not string_list(refs):
                errors.append(err("PM_INVALID_REFS", f"{field}[{index}].source_claim_refs", "source_claim_refs must be a list of strings", refs))
            elif any(ref not in known_claims for ref in refs):
                errors.append(err("PM_UNKNOWN_REF", f"{field}[{index}].source_claim_refs", "entry references an unknown positioning claim", refs))

    metrics = list_value(data, "metrics", errors)
    unique_ids(metrics, "metrics", errors)
    for index, item in enumerate(metrics):
        if not isinstance(item, dict):
            continue
        if not text(item.get("name")):
            errors.append(err("PM_TEXT_REQUIRED", f"metrics[{index}].name", "metric name required"))
        baseline_status = item.get("baseline_status")
        if baseline_status not in {"unknown", "observed"}:
            errors.append(err("PM_INVALID_EVIDENCE_STATUS", f"metrics[{index}].baseline_status", "baseline_status must be unknown or observed", baseline_status))
        refs = item.get("baseline_evidence_refs", [])
        if not string_list(refs):
            errors.append(err("PM_INVALID_EVIDENCE_REFS", f"metrics[{index}].baseline_evidence_refs", "baseline evidence refs must be strings", refs))
        elif baseline_status == "observed" and not refs:
            errors.append(err("PM_EVIDENCE_REQUIRED", f"metrics[{index}].baseline_evidence_refs", "observed baseline requires evidence refs"))
        if baseline_status == "unknown" and item.get("baseline") is not None:
            errors.append(err("PM_STATUS_CONFLICT", f"metrics[{index}].baseline", "unknown baseline must remain null", item.get("baseline")))
        target_status = item.get("target_status")
        if target_status not in {"proposed", "ratified"}:
            errors.append(err("PM_INVALID_STATUS", f"metrics[{index}].target_status", "target_status must be proposed or ratified", target_status))
        if target_status == "ratified" and not text(item.get("target_authority_ref")):
            errors.append(err("PM_AUTHORITY_REQUIRED", f"metrics[{index}].target_authority_ref", "ratified target requires authority ref"))

    timeline = list_value(data, "timeline", errors)
    unique_ids(timeline, "timeline", errors)
    for index, item in enumerate(timeline):
        if not isinstance(item, dict):
            continue
        if not text(item.get("action")):
            errors.append(err("PM_TEXT_REQUIRED", f"timeline[{index}].action", "timeline action required"))
        commitment = item.get("commitment_status")
        if commitment not in {"proposed", "ratified"}:
            errors.append(err("PM_INVALID_STATUS", f"timeline[{index}].commitment_status", "invalid commitment status", commitment))
        if commitment == "ratified" and not text(item.get("authority_ref")):
            errors.append(err("PM_AUTHORITY_REQUIRED", f"timeline[{index}].authority_ref", "ratified timeline commitment requires authority ref"))
        if not isinstance(item.get("external_action"), bool):
            errors.append(err("PM_TYPE_ERROR", f"timeline[{index}].external_action", "external_action must be boolean", item.get("external_action")))
    list_value(data, "contingencies", errors)
    list_value(data, "unresolved_questions", errors)


def validate_battlecard(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    require(data, (
        "schema_version", "status", "our_product", "competitor", "segment", "evidence_cutoff",
        "evidence_refs", "claims", "comparisons", "talk_tracks", "valid_until", "unresolved_questions",
    ), errors)
    if data.get("status") != "draft":
        errors.append(err("PM_INVALID_STATUS", "status", "battlecard status must remain draft", data.get("status")))
    for field in ("our_product", "competitor", "segment", "evidence_cutoff"):
        if not text(data.get(field)):
            errors.append(err("PM_TEXT_REQUIRED", field, f"{field} must be non-empty"))
    if not string_list(data.get("evidence_refs")):
        errors.append(err("PM_INVALID_EVIDENCE_REFS", "evidence_refs", "evidence_refs must be a list of strings", data.get("evidence_refs")))

    claims = list_value(data, "claims", errors)
    claim_ids = unique_ids(claims, "claims", errors)
    claim_sides: dict[str, str] = {}
    for index, item in enumerate(claims):
        if not isinstance(item, dict):
            continue
        cid = item.get("id")
        side = item.get("side")
        if side not in {"us", "competitor", "market", "win_loss"}:
            errors.append(err("PM_INVALID_TYPE", f"claims[{index}].side", "invalid battlecard claim side", side))
        if text(cid):
            claim_sides[cid] = str(side)
        if not text(item.get("statement")):
            errors.append(err("PM_TEXT_REQUIRED", f"claims[{index}].statement", "claim statement required"))
        status = item.get("evidence_status")
        if status not in EVIDENCE_STATES:
            errors.append(err("PM_INVALID_EVIDENCE_STATUS", f"claims[{index}].evidence_status", "invalid evidence status", status))
        refs = evidence_refs(item, f"claims[{index}].evidence_refs", errors)
        if status == "observed" and not refs:
            errors.append(err("PM_EVIDENCE_REQUIRED", f"claims[{index}].evidence_refs", "observed competitive claim requires evidence refs"))

    known = set(claim_ids)
    comparisons = list_value(data, "comparisons", errors)
    unique_ids(comparisons, "comparisons", errors)
    for index, item in enumerate(comparisons):
        if not isinstance(item, dict):
            continue
        if not text(item.get("dimension")):
            errors.append(err("PM_TEXT_REQUIRED", f"comparisons[{index}].dimension", "comparison dimension required"))
        assessment = item.get("assessment")
        if assessment not in {"us_advantage", "competitor_advantage", "parity", "unknown"}:
            errors.append(err("PM_INVALID_STATUS", f"comparisons[{index}].assessment", "invalid comparison assessment", assessment))
        if item.get("evidence_status") not in {"hypothesis", "inferred", "unknown"}:
            errors.append(err("PM_INVALID_EVIDENCE_STATUS", f"comparisons[{index}].evidence_status", "comparisons are interpretations and cannot be marked observed", item.get("evidence_status")))
        our_ref = item.get("our_claim_ref")
        competitor_ref = item.get("competitor_claim_ref")
        for ref, expected_side, field in ((our_ref, "us", "our_claim_ref"), (competitor_ref, "competitor", "competitor_claim_ref")):
            if ref is None:
                continue
            if ref not in known:
                errors.append(err("PM_UNKNOWN_REF", f"comparisons[{index}].{field}", "comparison references unknown claim", ref))
            elif claim_sides.get(ref) != expected_side:
                errors.append(err("PM_REF_TYPE_MISMATCH", f"comparisons[{index}].{field}", f"{field} must reference a {expected_side} claim", ref))

    tracks = list_value(data, "talk_tracks", errors)
    unique_ids(tracks, "talk_tracks", errors)
    for index, item in enumerate(tracks):
        if not isinstance(item, dict):
            continue
        if item.get("type") not in {"where_we_win", "where_they_win", "objection_response", "discovery_question"}:
            errors.append(err("PM_INVALID_TYPE", f"talk_tracks[{index}].type", "invalid talk-track type", item.get("type")))
        if not text(item.get("text")):
            errors.append(err("PM_TEXT_REQUIRED", f"talk_tracks[{index}].text", "talk-track text required"))
        if item.get("status") != "proposed":
            errors.append(err("PM_INVALID_STATUS", f"talk_tracks[{index}].status", "talk tracks remain proposed", item.get("status")))
        refs = item.get("source_claim_refs", [])
        if not string_list(refs):
            errors.append(err("PM_INVALID_REFS", f"talk_tracks[{index}].source_claim_refs", "source_claim_refs must be strings", refs))
        elif any(ref not in known for ref in refs):
            errors.append(err("PM_UNKNOWN_REF", f"talk_tracks[{index}].source_claim_refs", "talk track references unknown claim", refs))
    list_value(data, "unresolved_questions", errors)


def validate_announcement(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    require(data, (
        "schema_version", "status", "audience", "as_of", "release_evidence_refs", "items",
        "cta", "publication_state", "publication_authority_ref", "unresolved_questions",
    ), errors)
    if data.get("status") != "draft":
        errors.append(err("PM_INVALID_STATUS", "status", "feature announcement status must remain draft", data.get("status")))
    if data.get("publication_state") != "draft":
        errors.append(err("PM_EXTERNAL_ACTION_STATE", "publication_state", "release-notes capability cannot claim publication", data.get("publication_state")))
    for field in ("audience", "as_of"):
        if not text(data.get(field)):
            errors.append(err("PM_TEXT_REQUIRED", field, f"{field} must be non-empty"))
    if not string_list(data.get("release_evidence_refs")):
        errors.append(err("PM_INVALID_EVIDENCE_REFS", "release_evidence_refs", "release evidence refs must be strings", data.get("release_evidence_refs")))

    items = list_value(data, "items", errors)
    unique_ids(items, "items", errors)
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        item_type = item.get("type")
        if item_type not in {"feature", "fix", "performance", "known_issue", "coming_soon"}:
            errors.append(err("PM_INVALID_TYPE", f"items[{index}].type", "invalid announcement item type", item_type))
        for field in ("title", "statement"):
            if not text(item.get(field)):
                errors.append(err("PM_TEXT_REQUIRED", f"items[{index}].{field}", f"{field} required"))
        availability = item.get("availability")
        if availability not in {"shipped", "beta", "planned", "unknown"}:
            errors.append(err("PM_INVALID_STATUS", f"items[{index}].availability", "invalid availability state", availability))
        claim_status = item.get("claim_status")
        if claim_status not in {"observed", "proposed", "unknown"}:
            errors.append(err("PM_INVALID_EVIDENCE_STATUS", f"items[{index}].claim_status", "invalid claim status", claim_status))
        refs = evidence_refs(item, f"items[{index}].evidence_refs", errors)
        if claim_status == "observed" and not refs:
            errors.append(err("PM_EVIDENCE_REQUIRED", f"items[{index}].evidence_refs", "observed announcement claim requires evidence refs"))
        if availability in {"shipped", "beta"} and (claim_status != "observed" or not refs):
            errors.append(err("PM_RELEASE_EVIDENCE_REQUIRED", f"items[{index}]", "shipped/beta availability requires observed claim status and release evidence"))
        if item_type == "coming_soon" and availability in {"shipped", "beta"}:
            errors.append(err("PM_STATUS_CONFLICT", f"items[{index}].availability", "coming-soon item cannot already be shipped/beta", availability))
        commitment = item.get("commitment_status")
        if commitment not in {"proposed", "ratified"}:
            errors.append(err("PM_INVALID_STATUS", f"items[{index}].commitment_status", "invalid commitment status", commitment))
        if commitment == "ratified" and not text(item.get("authority_ref")):
            errors.append(err("PM_AUTHORITY_REQUIRED", f"items[{index}].authority_ref", "ratified announcement commitment requires authority ref"))
    list_value(data, "unresolved_questions", errors)


def validate_stakeholder(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    require(data, (
        "schema_version", "status", "audience", "purpose", "as_of", "source_refs", "claims",
        "decisions", "next_steps", "risks", "decision_request", "publication_state",
        "unresolved_questions",
    ), errors)
    if data.get("status") != "draft":
        errors.append(err("PM_INVALID_STATUS", "status", "stakeholder update status must remain draft", data.get("status")))
    if data.get("publication_state") != "draft":
        errors.append(err("PM_EXTERNAL_ACTION_STATE", "publication_state", "stakeholder-update capability cannot claim distribution", data.get("publication_state")))
    for field in ("audience", "as_of"):
        if not text(data.get(field)):
            errors.append(err("PM_TEXT_REQUIRED", field, f"{field} must be non-empty"))
    purpose = data.get("purpose")
    if purpose not in {"inform", "decision_request"}:
        errors.append(err("PM_INVALID_TYPE", "purpose", "purpose must be inform or decision_request", purpose))
    if purpose == "decision_request" and not text(data.get("decision_request")):
        errors.append(err("PM_DECISION_REQUEST_REQUIRED", "decision_request", "decision_request purpose requires a concrete request"))
    if not string_list(data.get("source_refs")):
        errors.append(err("PM_INVALID_REFS", "source_refs", "source_refs must be a list of strings", data.get("source_refs")))

    claims = list_value(data, "claims", errors)
    unique_ids(claims, "claims", errors)
    for index, item in enumerate(claims):
        if not isinstance(item, dict):
            continue
        if not text(item.get("statement")):
            errors.append(err("PM_TEXT_REQUIRED", f"claims[{index}].statement", "claim statement required"))
        status = item.get("epistemic_status")
        if status not in {"observed", "derived", "inferred", "hypothesized", "ratified", "unresolved"}:
            errors.append(err("PM_INVALID_EPISTEMIC_STATUS", f"claims[{index}].epistemic_status", "invalid epistemic status", status))
        refs = evidence_refs(item, f"claims[{index}].evidence_refs", errors)
        if status in {"observed", "derived"} and not refs:
            errors.append(err("PM_EVIDENCE_REQUIRED", f"claims[{index}].evidence_refs", f"{status} claim requires evidence refs"))
        if status == "derived" and not text(item.get("derivation_rule")):
            errors.append(err("PM_DERIVATION_REQUIRED", f"claims[{index}].derivation_rule", "derived claim requires derivation_rule"))
        if status == "ratified" and not text(item.get("authority_ref")):
            errors.append(err("PM_AUTHORITY_REQUIRED", f"claims[{index}].authority_ref", "ratified claim requires authority ref"))

    decisions = list_value(data, "decisions", errors)
    unique_ids(decisions, "decisions", errors)
    for index, item in enumerate(decisions):
        if not isinstance(item, dict):
            continue
        if not text(item.get("statement")):
            errors.append(err("PM_TEXT_REQUIRED", f"decisions[{index}].statement", "decision statement required"))
        status = item.get("status")
        if status not in {"proposed", "ratified"}:
            errors.append(err("PM_INVALID_STATUS", f"decisions[{index}].status", "invalid decision status", status))
        if status == "ratified" and not text(item.get("authority_ref")):
            errors.append(err("PM_AUTHORITY_REQUIRED", f"decisions[{index}].authority_ref", "ratified decision requires authority ref"))

    next_steps = list_value(data, "next_steps", errors)
    unique_ids(next_steps, "next_steps", errors)
    for index, item in enumerate(next_steps):
        if not isinstance(item, dict):
            continue
        if not text(item.get("action")):
            errors.append(err("PM_TEXT_REQUIRED", f"next_steps[{index}].action", "next-step action required"))
        if not text(item.get("owner_role")):
            errors.append(err("PM_TEXT_REQUIRED", f"next_steps[{index}].owner_role", "owner_role required"))
        status = item.get("commitment_status")
        if status not in {"proposed", "ratified"}:
            errors.append(err("PM_INVALID_STATUS", f"next_steps[{index}].commitment_status", "invalid commitment status", status))
        if status == "ratified" and not text(item.get("authority_ref")):
            errors.append(err("PM_AUTHORITY_REQUIRED", f"next_steps[{index}].authority_ref", "ratified next-step commitment requires authority ref"))

    risks = list_value(data, "risks", errors)
    unique_ids(risks, "risks", errors)
    for index, item in enumerate(risks):
        if not isinstance(item, dict):
            continue
        if not text(item.get("statement")):
            errors.append(err("PM_TEXT_REQUIRED", f"risks[{index}].statement", "risk statement required"))
        status = item.get("evidence_status")
        if status not in EVIDENCE_STATES:
            errors.append(err("PM_INVALID_EVIDENCE_STATUS", f"risks[{index}].evidence_status", "invalid risk evidence status", status))
        refs = evidence_refs(item, f"risks[{index}].evidence_refs", errors)
        if status == "observed" and not refs:
            errors.append(err("PM_EVIDENCE_REQUIRED", f"risks[{index}].evidence_refs", "observed risk requires evidence refs"))
    list_value(data, "unresolved_questions", errors)


def validate(path: Path) -> tuple[str, list[dict[str, Any]]]:
    if not path.is_file():
        return "unknown", [err("PM_ARTIFACT_NOT_FOUND", "artifact", f"artifact not found: {path}")]
    content = path.read_text(encoding="utf-8")
    blocks = HANDOFF_RE.findall(content)
    if len(blocks) != 1:
        return "unknown", [err("PM_HANDOFF_BLOCK_COUNT", "machine_readable_handoff", "expected exactly one machine-readable handoff YAML block", len(blocks))]
    try:
        data = yaml.safe_load(blocks[0])
    except yaml.YAMLError as exc:
        return "unknown", [err("PM_INVALID_YAML", "machine_readable_handoff", f"invalid YAML: {exc}")]
    if not isinstance(data, dict):
        return "unknown", [err("PM_INVALID_YAML_SHAPE", "machine_readable_handoff", "handoff must be a mapping", data)]
    artifact_id = data.get("artifact_id")
    if artifact_id not in SUPPORTED:
        return str(artifact_id or "unknown"), [err("PM_UNSUPPORTED_ARTIFACT", "artifact_id", "unsupported PM launch/communication artifact", artifact_id)]

    errors: list[dict[str, Any]] = []
    for section in SECTIONS[artifact_id]:
        if not re.search(rf"^##\s+(?:\d+\.\s*)?{re.escape(section)}\s*$", content, re.MULTILINE | re.IGNORECASE):
            errors.append(err("PM_MISSING_SECTION", "sections", f"required section {section!r} is missing"))
    if data.get("schema_version") not in {"1", 1}:
        errors.append(err("PM_INVALID_SCHEMA_VERSION", "schema_version", "schema_version must be 1", data.get("schema_version")))

    validators = {
        "readiness_report": validate_readiness,
        "gtm_plan": validate_gtm,
        "battlecard": validate_battlecard,
        "feature_announcement": validate_announcement,
        "stakeholder_update": validate_stakeholder,
    }
    validators[artifact_id](data, errors)
    return artifact_id, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate PM launch and communication artifacts")
    parser.add_argument("artifact_path")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    artifact_id, errors = validate(Path(args.artifact_path))
    result = {
        "valid": not errors,
        "artifact_id": artifact_id,
        "artifact_path": str(Path(args.artifact_path).resolve()),
        "validator": VALIDATOR,
        "errors": errors,
        "validation_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    if args.json:
        print(json.dumps(result, indent=2))
    elif errors:
        for item in errors:
            print(f"ERROR {item['error_id']}: {item['message']}")
    else:
        print(f"{artifact_id} validation passed")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
