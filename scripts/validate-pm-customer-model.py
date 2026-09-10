#!/usr/bin/env python3
"""Validate PM customer-journey and Ideal Customer Profile representation contracts.

The validator checks bounded structure, identity/reference integrity, local evidence
states, and explicit claim-strength invariants. It does not decide whether a
journey or customer profile is semantically correct, representative, or valuable.
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
METRIC_STATES = {"unknown", "proposed", "observed"}
ICP_CLAIM_LISTS = (
    "profile_claims",
    "behaviors",
    "jobs",
    "pains",
    "ideal_indicators",
    "disqualifiers",
)


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


def require(
    data: dict[str, Any], fields: tuple[str, ...], errors: list[dict[str, Any]]
) -> None:
    for field in fields:
        if field not in data:
            errors.append(
                err("PM_MISSING_FIELD", field, f"required field {field!r} is missing")
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
        errors.append(
            err("PM_DUPLICATE_ID", field, f"{field} contains duplicate ids", ids)
        )
    return ids


def validate_evidence_claim(
    item: dict[str, Any],
    field: str,
    errors: list[dict[str, Any]],
    *,
    statement_field: str | None = None,
) -> bool:
    if statement_field and not text(item.get(statement_field)):
        errors.append(
            err(
                "PM_TEXT_REQUIRED",
                f"{field}.{statement_field}",
                f"{statement_field} must be non-empty",
                item.get(statement_field),
            )
        )
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
    require(
        data,
        (
            "schema_version",
            "status",
            "persona_ref",
            "scope",
            "evidence_window",
            "evidence_refs",
            "stages",
            "critical_moments",
            "recommendations",
            "unresolved_questions",
        ),
        errors,
    )

    status = data.get("status")
    if status not in {"hypothesis", "evidence_backed", "mixed"}:
        errors.append(err("PM_INVALID_STATUS", "status", "invalid journey status", status))
    if not text(data.get("persona_ref")):
        errors.append(
            err("PM_SOURCE_REQUIRED", "persona_ref", "persona_ref must be non-empty")
        )
    if not text(data.get("scope")):
        errors.append(err("PM_TEXT_REQUIRED", "scope", "scope must be non-empty"))
    if not text(data.get("evidence_window")):
        errors.append(
            err(
                "PM_TEXT_REQUIRED",
                "evidence_window",
                "evidence_window must be non-empty",
            )
        )
    top_refs = data.get("evidence_refs")
    if not string_list(top_refs):
        errors.append(
            err(
                "PM_INVALID_EVIDENCE_REFS",
                "evidence_refs",
                "evidence_refs must be a list of non-empty strings",
                top_refs,
            )
        )
        top_refs = []

    stage_ids = unique_ids(data.get("stages"), "stages", errors)
    orders: list[int] = []
    observed_count = 0
    for index, stage in enumerate(data.get("stages") or []):
        if not isinstance(stage, dict):
            continue
        if not text(stage.get("name")):
            errors.append(
                err(
                    "PM_TEXT_REQUIRED",
                    f"stages[{index}].name",
                    "stage name required",
                )
            )
        order = stage.get("order")
        if not isinstance(order, int) or isinstance(order, bool) or order <= 0:
            errors.append(
                err(
                    "PM_INVALID_ORDER",
                    f"stages[{index}].order",
                    "stage order must be a positive integer",
                    order,
                )
            )
        else:
            orders.append(order)

        for key in (
            "touchpoints",
            "actions",
            "questions",
            "pain_points",
            "opportunities",
        ):
            if key in stage and not isinstance(stage[key], list):
                errors.append(
                    err(
                        "PM_LIST_REQUIRED",
                        f"stages[{index}].{key}",
                        f"{key} must be a list",
                        stage[key],
                    )
                )

        emotions = stage.get("emotions", [])
        if not isinstance(emotions, list):
            errors.append(
                err(
                    "PM_LIST_REQUIRED",
                    f"stages[{index}].emotions",
                    "emotions must be a list",
                    emotions,
                )
            )
        else:
            for j, emotion in enumerate(emotions):
                if not isinstance(emotion, dict):
                    errors.append(
                        err(
                            "PM_MAPPING_REQUIRED",
                            f"stages[{index}].emotions[{j}]",
                            "emotion must be a mapping",
                        )
                    )
                    continue
                observed_count += int(
                    validate_evidence_claim(
                        emotion,
                        f"stages[{index}].emotions[{j}]",
                        errors,
                        statement_field="value",
                    )
                )

        metrics = stage.get("metrics", [])
        if not isinstance(metrics, list):
            errors.append(
                err(
                    "PM_LIST_REQUIRED",
                    f"stages[{index}].metrics",
                    "metrics must be a list",
                    metrics,
                )
            )
        else:
            for j, metric in enumerate(metrics):
                if not isinstance(metric, dict):
                    errors.append(
                        err(
                            "PM_MAPPING_REQUIRED",
                            f"stages[{index}].metrics[{j}]",
                            "metric must be a mapping",
                        )
                    )
                    continue
                if not text(metric.get("name")):
                    errors.append(
                        err(
                            "PM_TEXT_REQUIRED",
                            f"stages[{index}].metrics[{j}].name",
                            "metric name required",
                        )
                    )
                metric_status = metric.get("evidence_status")
                if metric_status not in METRIC_STATES:
                    errors.append(
                        err(
                            "PM_INVALID_EVIDENCE_STATUS",
                            f"stages[{index}].metrics[{j}].evidence_status",
                            f"metric evidence_status must be one of {sorted(METRIC_STATES)}",
                            metric_status,
                        )
                    )
                refs = metric.get("evidence_refs", [])
                if not string_list(refs):
                    errors.append(
                        err(
                            "PM_INVALID_EVIDENCE_REFS",
                            f"stages[{index}].metrics[{j}].evidence_refs",
                            "metric evidence_refs must be a list of non-empty strings",
                            refs,
                        )
                    )
                elif metric_status == "observed":
                    if not refs:
                        errors.append(
                            err(
                                "PM_EVIDENCE_REQUIRED",
                                f"stages[{index}].metrics[{j}].evidence_refs",
                                "observed metric requires evidence refs",
                                refs,
                            )
                        )
                    else:
                        observed_count += 1

    if len(orders) != len(set(orders)):
        errors.append(
            err(
                "PM_DUPLICATE_ORDER",
                "stages",
                "stage order values must be unique",
                orders,
            )
        )

    unique_ids(data.get("critical_moments"), "critical_moments", errors)
    for index, moment in enumerate(data.get("critical_moments") or []):
        if not isinstance(moment, dict):
            continue
        if moment.get("type") not in {"aha", "moment_of_truth", "churn_trigger"}:
            errors.append(
                err(
                    "PM_INVALID_TYPE",
                    f"critical_moments[{index}].type",
                    "invalid critical-moment type",
                    moment.get("type"),
                )
            )
        if moment.get("stage_ref") not in stage_ids:
            errors.append(
                err(
                    "PM_UNKNOWN_REF",
                    f"critical_moments[{index}].stage_ref",
                    "critical moment must reference a declared stage",
                    moment.get("stage_ref"),
                )
            )
        observed_count += int(
            validate_evidence_claim(
                moment,
                f"critical_moments[{index}]",
                errors,
                statement_field="statement",
            )
        )

    if not isinstance(data.get("recommendations"), list):
        errors.append(
            err(
                "PM_LIST_REQUIRED",
                "recommendations",
                "recommendations must be a list",
                data.get("recommendations"),
            )
        )
    if not isinstance(data.get("unresolved_questions"), list):
        errors.append(
            err(
                "PM_LIST_REQUIRED",
                "unresolved_questions",
                "unresolved_questions must be a list",
                data.get("unresolved_questions"),
            )
        )

    if status == "evidence_backed" and (not top_refs or observed_count == 0):
        errors.append(
            err(
                "PM_EVIDENCE_REQUIRED",
                "status",
                "evidence_backed journey requires top-level evidence refs and at least one observed evidence-bearing claim",
            )
        )
    if status == "hypothesis" and observed_count > 0:
        errors.append(
            err(
                "PM_STATUS_CONFLICT",
                "status",
                "journey containing observed claims must use mixed or evidence_backed status",
                status,
            )
        )


def validate_icp(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    require(
        data,
        (
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
        ),
        errors,
    )

    status = data.get("status")
    if status not in {"hypothesis", "evidence_backed", "mixed"}:
        errors.append(err("PM_INVALID_STATUS", "status", "invalid ICP status", status))
    if not text(data.get("segment")):
        errors.append(err("PM_TEXT_REQUIRED", "segment", "segment must be non-empty"))
    if not text(data.get("evidence_window")):
        errors.append(
            err(
                "PM_TEXT_REQUIRED",
                "evidence_window",
                "evidence_window must be non-empty",
            )
        )
    top_refs = data.get("evidence_refs")
    if not string_list(top_refs):
        errors.append(
            err(
                "PM_INVALID_EVIDENCE_REFS",
                "evidence_refs",
                "evidence_refs must be a list of non-empty strings",
                top_refs,
            )
        )
        top_refs = []

    observed_count = 0
    claim_ids: list[str] = []
    for key in ICP_CLAIM_LISTS:
        ids = unique_ids(data.get(key), key, errors)
        claim_ids.extend(ids)
        for index, item in enumerate(data.get(key) or []):
            if not isinstance(item, dict):
                continue
            if key == "profile_claims":
                if not text(item.get("dimension")):
                    errors.append(
                        err(
                            "PM_TEXT_REQUIRED",
                            f"{key}[{index}].dimension",
                            "profile-claim dimension required",
                        )
                    )
                if item.get("value") is None:
                    errors.append(
                        err(
                            "PM_VALUE_REQUIRED",
                            f"{key}[{index}].value",
                            "profile-claim value is required; use an explicit unknown claim if unresolved",
                        )
                    )
                statement_field = None
            else:
                statement_field = "statement"
            if key == "disqualifiers" and item.get("type") not in {"hard", "soft"}:
                errors.append(
                    err(
                        "PM_INVALID_TYPE",
                        f"{key}[{index}].type",
                        "disqualifier type must be hard or soft",
                        item.get("type"),
                    )
                )
            observed_count += int(
                validate_evidence_claim(
                    item,
                    f"{key}[{index}]",
                    errors,
                    statement_field=statement_field,
                )
            )

    if len(claim_ids) != len(set(claim_ids)):
        errors.append(
            err(
                "PM_DUPLICATE_ID",
                "icp_claims",
                "customer claim/indicator/disqualifier ids must be globally unique",
                claim_ids,
            )
        )

    implications = data.get("gtm_implications")
    implication_ids = unique_ids(implications, "gtm_implications", errors)
    if set(implication_ids) & set(claim_ids):
        errors.append(
            err(
                "PM_DUPLICATE_ID",
                "gtm_implications",
                "GTM implication ids must be distinct from customer claim ids",
                implication_ids,
            )
        )
    if isinstance(implications, list):
        known_claim_ids = set(claim_ids)
        for index, item in enumerate(implications):
            if not isinstance(item, dict):
                continue
            if item.get("function") not in {
                "product",
                "marketing",
                "sales",
                "customer_success",
                "other",
            }:
                errors.append(
                    err(
                        "PM_INVALID_TYPE",
                        f"gtm_implications[{index}].function",
                        "invalid GTM function",
                        item.get("function"),
                    )
                )
            if not text(item.get("recommendation")):
                errors.append(
                    err(
                        "PM_TEXT_REQUIRED",
                        f"gtm_implications[{index}].recommendation",
                        "GTM recommendation required",
                    )
                )
            if item.get("status") != "proposed":
                errors.append(
                    err(
                        "PM_INVALID_STATUS",
                        f"gtm_implications[{index}].status",
                        "GTM implications must remain proposed",
                        item.get("status"),
                    )
                )
            refs = item.get("source_claim_refs", [])
            if not string_list(refs):
                errors.append(
                    err(
                        "PM_INVALID_REFS",
                        f"gtm_implications[{index}].source_claim_refs",
                        "source_claim_refs must be a list of non-empty strings",
                        refs,
                    )
                )
            elif any(ref not in known_claim_ids for ref in refs):
                errors.append(
                    err(
                        "PM_UNKNOWN_REF",
                        f"gtm_implications[{index}].source_claim_refs",
                        "GTM implication references an unknown customer claim id",
                        refs,
                    )
                )

    if not isinstance(data.get("unresolved_questions"), list):
        errors.append(
            err(
                "PM_LIST_REQUIRED",
                "unresolved_questions",
                "unresolved_questions must be a list",
                data.get("unresolved_questions"),
            )
        )

    if status == "evidence_backed" and (not top_refs or observed_count == 0):
        errors.append(
            err(
                "PM_EVIDENCE_REQUIRED",
                "status",
                "evidence_backed ICP requires top-level evidence refs and at least one observed evidence-bearing claim",
            )
        )
    if status == "hypothesis" and observed_count > 0:
        errors.append(
            err(
                "PM_STATUS_CONFLICT",
                "status",
                "ICP containing observed claims must use mixed or evidence_backed status",
                status,
            )
        )


def validate(path: Path) -> tuple[str, list[dict[str, Any]]]:
    if not path.is_file():
        return "unknown", [
            err("PM_ARTIFACT_NOT_FOUND", "artifact", f"artifact not found: {path}")
        ]
    content = path.read_text(encoding="utf-8")
    blocks = HANDOFF_RE.findall(content)
    if len(blocks) != 1:
        return "unknown", [
            err(
                "PM_HANDOFF_BLOCK_COUNT",
                "machine_readable_handoff",
                "expected exactly one machine-readable handoff YAML block",
                len(blocks),
            )
        ]
    try:
        data = yaml.safe_load(blocks[0])
    except yaml.YAMLError as exc:
        return "unknown", [
            err(
                "PM_INVALID_YAML",
                "machine_readable_handoff",
                f"invalid YAML: {exc}",
            )
        ]
    if not isinstance(data, dict):
        return "unknown", [
            err(
                "PM_INVALID_YAML_SHAPE",
                "machine_readable_handoff",
                "handoff must be a mapping",
                data,
            )
        ]

    artifact_id = data.get("artifact_id")
    if artifact_id not in SUPPORTED:
        return str(artifact_id or "unknown"), [
            err(
                "PM_UNSUPPORTED_ARTIFACT",
                "artifact_id",
                "unsupported PM customer-model artifact",
                artifact_id,
            )
        ]

    errors: list[dict[str, Any]] = []
    for section in SECTIONS[artifact_id]:
        if not re.search(
            rf"^##\s+(?:\d+\.\s*)?{re.escape(section)}\s*$",
            content,
            re.MULTILINE | re.IGNORECASE,
        ):
            errors.append(
                err(
                    "PM_MISSING_SECTION",
                    "sections",
                    f"required section {section!r} is missing",
                )
            )
    if data.get("schema_version") not in {"1", 1}:
        errors.append(
            err(
                "PM_INVALID_SCHEMA_VERSION",
                "schema_version",
                "schema_version must be 1",
                data.get("schema_version"),
            )
        )

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
        "validation_timestamp": datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
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
