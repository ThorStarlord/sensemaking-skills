"""Validate strategic companion artifacts mechanically.

This validator checks representation and protected boundary flags only. It does
not interpret evidence, choose owner/thesis outcomes, update strategy, or grant
implementation authority.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

SUPPORTED = {
    "strategic_reconciliation",
    "owner_decision_capsule",
    "thesis_review_packet",
    "external_evidence_packet",
}

CLAIM_DISPOSITIONS = {"CONFIRM", "REVISE", "RETRACT", "UNCHANGED"}
ASSUMPTION_DISPOSITIONS = {
    "CONFIRM",
    "RESOLVE",
    "REVISE",
    "INVALIDATE",
    "UNCHANGED",
}
PATH_DISPOSITIONS = {
    "CONTINUE",
    "REVISE",
    "SUPERSEDE",
    "CLOSE",
    "NO_PATH_CHANGE",
}
STRATEGIC_EFFECTS = {
    "NO_MODEL_CHANGE",
    "REAFFIRM",
    "REVISE_STRATEGY",
    "REOPEN_ANALYSIS",
    "OWNER_DECISION",
    "THESIS_REVIEW_REQUIRED",
}
THESIS_DISPOSITIONS = {
    "REAFFIRM",
    "REINTERPRET",
    "REVISE",
    "RETIRE",
    "SUPERSEDE",
}

PATH_TRANSITION_EFFECT_DISPOSITIONS = {
    "ESTABLISHED",
    "PARTIAL",
    "NOT_ESTABLISHED",
    "SUPERSEDED",
    "NO_CONCLUSION",
}


def _error(code: str, message: str) -> dict[str, str]:
    return {"error_id": code, "message": message}


def _extract(content: str) -> dict[str, Any] | None:
    for block in reversed(re.findall(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)):
        try:
            value = yaml.safe_load(block)
        except yaml.YAMLError:
            continue
        if isinstance(value, dict) and value.get("artifact_id") in SUPPORTED:
            return value
    return None


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any, *, allow_empty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (allow_empty or bool(value))
        and all(_text(item) for item in value)
    )


def _require_false(data: dict[str, Any], field: str, errors: list[dict[str, str]]) -> None:
    if data.get(field) is not False:
        errors.append(_error("STRATEGIC_COMPANION_BOUNDARY_INVALID", f"{field} must be false"))


def _require_true(data: dict[str, Any], field: str, errors: list[dict[str, str]]) -> None:
    if data.get(field) is not True:
        errors.append(_error("STRATEGIC_COMPANION_REQUIRED_TRUE_INVALID", f"{field} must be true"))


def _validate_reconciliation(data: dict[str, Any], errors: list[dict[str, str]]) -> None:
    required = {
        "target_repository",
        "prior_analysis_ref",
        "current_source_identity",
        "returned_evidence",
        "claim_updates",
        "assumption_updates",
        "path_disposition",
        "prior_path_id",
        "current_path_id",
        "strategic_effect",
        "candidate_next_responsibility",
        "implementation_authority_established_by_artifact",
        "semantic_truth_established",
        "created_at",
        "immutable",
    }
    missing = sorted(required - set(data))
    if missing:
        errors.append(_error("STRATEGIC_RECONCILIATION_FIELDS_MISSING", ", ".join(missing)))
    for field in ("target_repository", "prior_analysis_ref", "current_source_identity", "created_at"):
        if not _text(data.get(field)):
            errors.append(_error("STRATEGIC_RECONCILIATION_TEXT_INVALID", field))
    evidence = data.get("returned_evidence")
    if not isinstance(evidence, list):
        errors.append(_error("STRATEGIC_RECONCILIATION_EVIDENCE_INVALID", "returned_evidence must be a list"))
    else:
        for item in evidence:
            if not isinstance(item, dict) or not _text(item.get("evidence_ref")) or not _text(item.get("claim")):
                errors.append(_error("STRATEGIC_RECONCILIATION_EVIDENCE_INVALID", "each returned evidence entry requires evidence_ref and claim"))
    for field, allowed, key in (
        ("claim_updates", CLAIM_DISPOSITIONS, "claim_ref"),
        ("assumption_updates", ASSUMPTION_DISPOSITIONS, "assumption_id"),
    ):
        entries = data.get(field)
        if not isinstance(entries, list):
            errors.append(_error("STRATEGIC_RECONCILIATION_UPDATE_INVALID", f"{field} must be a list"))
            continue
        for item in entries:
            if not isinstance(item, dict) or not _text(item.get(key)) or item.get("disposition") not in allowed or not _text(item.get("reason")):
                errors.append(_error("STRATEGIC_RECONCILIATION_UPDATE_INVALID", f"invalid {field} entry"))
    if data.get("path_disposition") not in PATH_DISPOSITIONS:
        errors.append(_error("STRATEGIC_RECONCILIATION_PATH_DISPOSITION_INVALID", "invalid path_disposition"))
    if data.get("strategic_effect") not in STRATEGIC_EFFECTS:
        errors.append(_error("STRATEGIC_RECONCILIATION_EFFECT_INVALID", "invalid strategic_effect"))

    path_transition_effect = data.get("path_transition_effect")
    if path_transition_effect is not None:
        if (
            not isinstance(path_transition_effect, dict)
            or not _text(path_transition_effect.get("transition_ref"))
            or path_transition_effect.get("disposition")
            not in PATH_TRANSITION_EFFECT_DISPOSITIONS
        ):
            errors.append(
                _error(
                    "STRATEGIC_RECONCILIATION_PATH_TRANSITION_EFFECT_INVALID",
                    "path_transition_effect requires transition_ref and a supported disposition",
                )
            )
        else:
            prohibited = {
                "priority",
                "deadline",
                "estimate",
                "percent_complete",
                "assignee",
                "start_date",
                "due_date",
                "blocked_by",
                "next_transition",
            } & set(path_transition_effect)
            if prohibited:
                errors.append(
                    _error(
                        "STRATEGIC_RECONCILIATION_PATH_TRANSITION_ROADMAP_FIELD_FORBIDDEN",
                        "path_transition_effect contains roadmap/scheduling fields: "
                        + ", ".join(sorted(prohibited)),
                    )
                )
    _require_false(data, "implementation_authority_established_by_artifact", errors)
    _require_false(data, "semantic_truth_established", errors)


def _validate_owner(data: dict[str, Any], errors: list[dict[str, str]]) -> None:
    required = {
        "decision_id",
        "target_repository",
        "decision_statement",
        "repository_can_resolve",
        "options",
        "owner_decision_made_by_artifact",
        "implementation_authority_established_by_artifact",
        "created_at",
        "immutable",
    }
    missing = sorted(required - set(data))
    if missing:
        errors.append(_error("OWNER_DECISION_CAPSULE_FIELDS_MISSING", ", ".join(missing)))
    for field in ("decision_id", "target_repository", "decision_statement", "created_at"):
        if not _text(data.get(field)):
            errors.append(_error("OWNER_DECISION_CAPSULE_TEXT_INVALID", field))
    if data.get("repository_can_resolve") is not False:
        errors.append(_error("OWNER_DECISION_CAPSULE_SOURCE_BOUNDARY_INVALID", "repository_can_resolve must be false"))
    options = data.get("options")
    if not isinstance(options, list) or not options:
        errors.append(_error("OWNER_DECISION_CAPSULE_OPTIONS_INVALID", "options must be a non-empty list"))
    else:
        ids: set[str] = set()
        for item in options:
            if not isinstance(item, dict) or not _text(item.get("option_id")) or not _text(item.get("statement")):
                errors.append(_error("OWNER_DECISION_CAPSULE_OPTION_INVALID", "each option requires option_id and statement"))
                continue
            if item["option_id"] in ids:
                errors.append(_error("OWNER_DECISION_CAPSULE_OPTION_DUPLICATE", item["option_id"]))
            ids.add(item["option_id"])
            for field in ("unlocks", "tradeoffs", "authority_if_selected"):
                if not _string_list(item.get(field), allow_empty=True):
                    errors.append(_error("OWNER_DECISION_CAPSULE_OPTION_LIST_INVALID", f"{item['option_id']}.{field}"))
            for field in ("reversibility", "deferral_effect"):
                if not _text(item.get(field)):
                    errors.append(_error("OWNER_DECISION_CAPSULE_OPTION_TEXT_INVALID", f"{item['option_id']}.{field}"))
    _require_false(data, "owner_decision_made_by_artifact", errors)
    _require_false(data, "implementation_authority_established_by_artifact", errors)


def _validate_thesis(data: dict[str, Any], errors: list[dict[str, str]]) -> None:
    required = {
        "target_repository",
        "level4_commitment_ref",
        "challenge_statement",
        "evidence_refs",
        "affected_responsibilities",
        "candidate_dispositions",
        "downstream_reconciliation",
        "owner_ratification_required",
        "thesis_revision_ratified_by_artifact",
        "implementation_authority_established_by_artifact",
        "created_at",
        "immutable",
    }
    missing = sorted(required - set(data))
    if missing:
        errors.append(_error("THESIS_REVIEW_PACKET_FIELDS_MISSING", ", ".join(missing)))
    for field in ("target_repository", "level4_commitment_ref", "challenge_statement", "created_at"):
        if not _text(data.get(field)):
            errors.append(_error("THESIS_REVIEW_PACKET_TEXT_INVALID", field))
    for field in ("evidence_refs", "affected_responsibilities", "downstream_reconciliation"):
        if not _string_list(data.get(field)):
            errors.append(_error("THESIS_REVIEW_PACKET_LIST_INVALID", field))
    dispositions = data.get("candidate_dispositions")
    if not isinstance(dispositions, list) or not dispositions or any(item not in THESIS_DISPOSITIONS for item in dispositions):
        errors.append(_error("THESIS_REVIEW_PACKET_DISPOSITIONS_INVALID", "candidate_dispositions must use Level-4 dispositions"))
    _require_true(data, "owner_ratification_required", errors)
    _require_false(data, "thesis_revision_ratified_by_artifact", errors)
    _require_false(data, "implementation_authority_established_by_artifact", errors)


def _validate_external(data: dict[str, Any], errors: list[dict[str, str]]) -> None:
    required = {
        "target_decision_ref",
        "retrieved_at",
        "sources",
        "claims",
        "repository_fact_established_by_artifact",
        "semantic_truth_established",
        "implementation_authority_established_by_artifact",
        "created_at",
        "immutable",
    }
    missing = sorted(required - set(data))
    if missing:
        errors.append(_error("EXTERNAL_EVIDENCE_PACKET_FIELDS_MISSING", ", ".join(missing)))
    for field in ("target_decision_ref", "retrieved_at", "created_at"):
        if not _text(data.get(field)):
            errors.append(_error("EXTERNAL_EVIDENCE_PACKET_TEXT_INVALID", field))
    sources = data.get("sources")
    source_ids: set[str] = set()
    if not isinstance(sources, list) or not sources:
        errors.append(_error("EXTERNAL_EVIDENCE_PACKET_SOURCES_INVALID", "sources must be non-empty"))
    else:
        for item in sources:
            if not isinstance(item, dict) or not _text(item.get("source_id")) or not _text(item.get("uri")) or not _text(item.get("retrieved_at")):
                errors.append(_error("EXTERNAL_EVIDENCE_PACKET_SOURCE_INVALID", "each source requires source_id, uri, retrieved_at"))
                continue
            source_ids.add(item["source_id"])
    claims = data.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append(_error("EXTERNAL_EVIDENCE_PACKET_CLAIMS_INVALID", "claims must be non-empty"))
    else:
        for item in claims:
            if not isinstance(item, dict) or not _text(item.get("claim_id")) or not _text(item.get("statement")) or not _text(item.get("currentness_limit")):
                errors.append(_error("EXTERNAL_EVIDENCE_PACKET_CLAIM_INVALID", "each claim requires claim_id, statement, currentness_limit"))
                continue
            refs = item.get("source_ids")
            if not _string_list(refs) or any(ref not in source_ids for ref in refs):
                errors.append(_error("EXTERNAL_EVIDENCE_PACKET_CLAIM_SOURCE_INVALID", f"{item.get('claim_id')} references unknown sources"))
    _require_false(data, "repository_fact_established_by_artifact", errors)
    _require_false(data, "semantic_truth_established", errors)
    _require_false(data, "implementation_authority_established_by_artifact", errors)


def validate(path: Path) -> tuple[str | None, list[dict[str, str]]]:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [_error("STRATEGIC_COMPANION_FILE_UNREADABLE", str(exc))]
    data = _extract(content)
    if data is None:
        return None, [_error("STRATEGIC_COMPANION_MACHINE_BLOCK_MISSING", "No supported strategic companion YAML block found.")]
    artifact_id = data.get("artifact_id")
    errors: list[dict[str, str]] = []
    if data.get("immutable") is not True:
        errors.append(_error("STRATEGIC_COMPANION_IMMUTABILITY_INVALID", "immutable must be true"))
    if artifact_id == "strategic_reconciliation":
        _validate_reconciliation(data, errors)
    elif artifact_id == "owner_decision_capsule":
        _validate_owner(data, errors)
    elif artifact_id == "thesis_review_packet":
        _validate_thesis(data, errors)
    elif artifact_id == "external_evidence_packet":
        _validate_external(data, errors)
    return artifact_id, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    artifact_id, errors = validate(args.artifact)
    result = {
        "valid": not errors,
        "artifact_id": artifact_id,
        "artifact_path": str(args.artifact),
        "errors": errors,
        "semantic_truth_established": False,
        "strategy_mutated_by_validator": False,
        "owner_decision_made_by_validator": False,
        "thesis_revision_ratified_by_validator": False,
        "implementation_authorized_by_validator": False,
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    elif errors:
        print("FAIL")
        for item in errors:
            print(f"{item['error_id']}: {item['message']}")
    else:
        print("PASS")
        print("mechanical representation valid; semantic/authority outcomes not established")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())