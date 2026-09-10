#!/usr/bin/env python3
"""Validate customer-journey and ICP representation/evidence contracts.

This validator checks identity, reference, ordering, and evidence-status invariants.
It does not decide whether a journey or ICP is semantically correct.
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

VALIDATOR = "validate-pm-customer-model.py"
SUPPORTED = {"journey_map", "ideal_customer_profile"}
HANDOFF_RE = re.compile(
    r"^##\s+(?:\d+\.\s*)?Machine-readable handoff\s*$\s*```yaml\s*(.*?)\s*```",
    re.MULTILINE | re.IGNORECASE | re.DOTALL,
)
SECTIONS = {
    "journey_map": (
        "Persona and scope",
        "Evidence inventory",
        "Journey stages",
        "Critical moments",
        "Opportunities and unknowns",
    ),
    "ideal_customer_profile": (
        "Scope and evidence",
        "Profile",
        "Behaviors and buying context",
        "Jobs needs and pains",
        "Ideal-of-ideal and disqualifiers",
        "GTM implications",
        "Validation gaps",
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


def string_list(value: Any, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (not nonempty or bool(value))
        and all(text(item) for item in value)
    )


def unique_ids(
    items: Any, field: str, errors: list[dict[str, Any]]
) -> list[str]:
    if not isinstance(items, list):
        errors.append(err("PM_LIST_REQUIRED", field, f"{field} must be a list", items))
        return []
    ids: list[str] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict) or not text(item.get("id")):
            errors.append(
                err(
                    "PM_ID_REQUIRED",
                    f"{field}[{index}].id",
                    "non-empty id required",
                    None if not isinstance(item, dict) else item.get("id"),
                )
            )
            continue
        ids.append(item["id"].strip())
    if len(ids) != len(set(ids)):
        errors.append(err("PM_DUPLICATE_ID", field, f"{field} contains duplicate ids", ids))
    return ids


def validate_evidence_claim(
    item: dict[str, Any], field: str, errors: list[dict[str, Any]]
) -> bool:
    status = item.get("evidence_status")
    if status not in EVIDENCE_STATES:
        errors.append(
            err(
                "PM_INVALID_EVIDENCE_STATUS",
                f"{field}.evidence_status",
                f"evidence_status must be one of {sorted(EVIDENCE_STATES)}",
                status,
            )
        )
        return False
    refs = item.get("evidence_refs", [])
    if not string_list(refs):
        errors.append(
            err(
                "PM_INVALID_EVIDENCE_REFS",
                f"{field}.evidence_refs",
                "evidence_refs must be a list of non-empty strings",
                refs,
            )
        )
        return False
    if status == "observed" and not refs:
        errors.append(
            err(
                "PM_EVIDENCE_REQUIRED",
                f"{field}.evidence_refs",
                "observed claim requires evidence refs",
                refs,
            )
        )
        return False
    return status == "observed" and bool(refs)


def validate_journey(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    required = (
        "schema_version",
        "status",
        "persona_ref",
        "scope",
        "stages",
        "critical_moments",
        "recommendations",
        "unresolved_questions",
    )
    for field in required:
        if field not in data:
            errors.append(err("PM_MISSING_FIELD", field, f"required field {field!r} is missing"))

    if data.get("status") not in {"hypothesis", "evidence_backed", "mixed"}:
        errors.append(err("PM_INVALID_STATUS", "status", "invalid journey status", data.get("status")))
    if not text(data.get("persona_ref")):
        errors.append(err("PM_SOURCE_REQUIRED", "persona_ref", "persona_ref must be non-empty"))
    if not text(data.get("scope")):
        errors.append(err("PM_TEXT_REQUIRED", "scope", "scope must be non-empty"))

    stage_ids = unique_ids(data.get("stages"), "stages", errors)
    orders: list[int] = []
    observed_count = 0
    for index, stage in enumerate(data.get("stages") or []):
        if not isinstance(stage, dict):
            continue
        if not text(stage.get("name")):
            errors.append(err("PM_TEXT_REQUIRED", f"stages[{index}].name", "stage name required"))
        order = stage.get("order")
        if not isinstance(order, int) or isinstance(order, bool) or order <= 0:
            errors.append(err("PM_INVALID_ORDER", f"stages[{index}].order", "stage order must be a positive integer", order))
        else:
            orders.append(order)
        for key in ("touchpoints", "actions", "questions", "pain_points", "opportunities"):
            if key in stage and not isinstance(stage[key], list):
                errors.append(err("PM_LIST_REQUIRED", f"stages[{index}].{key}", f"{key} must be a list", stage[key]))
        for j, emotion in enumerate(stage.get("emotions") or []):
            if not isinstance(emotion, dict):
                errors.append(err("PM_MAPPING_REQUIRED", f"stages[{index}].emotions[{j}]", "emotion must be a mapping"))
                continue
            observed_count += int(validate_evidence_claim(emotion, f"stages[{index}].emotions[{j}]", errors))
        for j, metric in enumerate(stage.get("metrics") or []):
            if not isinstance(metric, dict):
                errors.append(err("PM_MAPPING_REQUIRED", f"stages[{index}].metrics[{j}]", "metric must be a mapping"))
                continue
            status = metric.get("evidence_status")
            if status not in {"unknown", "proposed", "observed"}:
                errors.append(err("PM_INVALID_EVIDENCE_STATUS", f"stages[{index}].metrics[{j}].evidence_status", "invalid metric evidence status", status))
            refs = metric.get("evidence_refs", [])
            if not string_list(refs):
                errors.append(err("PM_INVALID_EVIDENCE_REFS", f"stages[{index}].metrics[{j}].evidence_refs", "metric evidence_refs must be a list", refs))
            elif status == "observed":
                if not refs:
                    errors.append(err("PM_EVIDENCE_REQUIRED", f"stages[{index}].metrics[{j}].evidence_refs", "observed metric requires evidence refs", refs))
                else:
                    observed_count += 1

    if len(orders) != len(set(orders)):
        errors.append(err("PM_DUPLICATE_ORDER", "stages", "stage order values must be unique", orders))

    unique_ids(data.get("critical_moments"), "critical_moments", errors)
    for index, moment in enumerate(data.get("critical_moments") or []):
        if not isinstance(moment, dict):
            continue
        if moment.get("type") not in {"aha", "moment_of_truth", "churn_trigger"}:
            errors.append(err("PM_INVALID_TYPE", f"critical_moments[{index}].type", "invalid critical-moment type", moment.get("type")))
        if moment.get("stage_ref") not in stage_ids:
            errors.append(err("PM_UNKNOWN_REF", f"critical_moments[{index}].stage_ref", "critical moment must reference a declared stage", moment.get("stage_ref")))
        observed_count += int(validate_evidence_claim(moment, f"critical_moments[{index}]", errors))

    if data.get("status") == "evidence_backed" and observed_count == 0:
        errors.append(err("PM_EVIDENCE_REQUIRED", "status", "evidence_backed journey requires at least one observed evidence-bearing claim"))


def validate_icp(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    required = (
        "schema_version",
        "status",
        "segment",
        "evidence_window",
        "evidence_refs",
        "profile_claims",
        "behaviors",
        "jobs",
        "pains",
        "ideal_indicators",
        "disqualifiers",
        "gtm_implications",
        "unresolved_questions",
    )
    for field in required:
        if field not in data:
            errors.append(err("PM_MISSING_FIELD", field, f"required field {field!r} is missing"))

    status = data.get("status")
    if status not in {"hypothesis", "evidence_backed", "mixed"}:
        errors.append(err("PM_INVALID_STATUS", "status", "invalid ICP status", status))
    if not text(data.get("segment")):
        errors.append(err("PM_TEXT_REQUIRED", "segment", "segment must be non-empty"))
    if not text(data.get("evidence_window")):
        errors.append(err("PM_TEXT_REQUIRED", "evidence_window", "evidence_window must be non-empty"))
    top_refs = data.get("evidence_refs")
    if not string_list(top_refs):
        errors.append(err("PM_INVALID_EVIDENCE_REFS", "evidence_refs", "evidence_refs must be a list of non-empty strings", top_refs))
        top_refs = []

    observed_count = 0
    all_ids: list[str] = []
    for key in ("profile_claims", "ideal_indicators", "disqualifiers"):
        ids = unique_ids(data.get(key), key, errors)
        all_ids.extend(ids)
        for index, item in enumerate(data.get(key) or []):
            if not isinstance(item, dict):
                continue
            if key == "disqualifiers" and item.get("type") not in {"hard", "soft"}:
                errors.append(err("PM_INVALID_TYPE", f"{key}[{index}].type", "disqualifier type must be hard or soft", item.get("type")))
            observed_count += int(validate_evidence_claim(item, f"{key}[{index}]", errors))
    if len(all_ids) != len(set(all_ids)):
        errors.append(err("PM_DUPLICATE_ID", "icp_claims", "claim/indicator/disqualifier ids must be globally unique", all_ids))

    for key in ("behaviors", "jobs", "pains", "gtm_implications", "unresolved_questions"):
        if not isinstance(data.get(key), list):
            errors.append(err("PM_LIST_REQUIRED", key, f"{key} must be a list", data.get(key)))

    if status == "evidence_backed":
        if not top_refs or observed_count == 0:
            errors.append(err("PM_EVIDENCE_REQUIRED", "status", "evidence_backed ICP requires top-level evidence refs and at least one observed evidence-bearing claim"))
    if status == "hypothesis" and observed_count > 0:
        errors.append(err("PM_STATUS_CONFLICT", "status", "ICP with observed claims should use mixed or evidence_backed status", status))


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
        return str(artifact_id or "unknown"), [err("PM_UNSUPPORTED_ARTIFACT", "artifact_id", "unsupported PM customer-model artifact", artifact_id)]

    errors: list[dict[str, Any]] = []
    for section in SECTIONS[artifact_id]:
        if not re.search(rf"^##\s+(?:\d+\.\s*)?{re.escape(section)}\s*$", content, re.MULTILINE | re.IGNORECASE):
            errors.append(err("PM_MISSING_SECTION", "sections", f"required section {section!r} is missing"))
    if data.get("schema_version") not in {"1", 1}:
        errors.append(err("PM_INVALID_SCHEMA_VERSION", "schema_version", "schema_version must be 1", data.get("schema_version")))
    if artifact_id == "journey_map":
        validate_journey(data, errors)
    else:
        validate_icp(data, errors)
    return artifact_id, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate PM customer-model artifacts")
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
