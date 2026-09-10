#!/usr/bin/env python3
"""Deterministic validator for PM feature-definition artifacts.

Validates representation, traceability, and evidence/status shape only. It does not
judge whether a story is valuable, criteria are sufficient, or a risk assessment is
strategically correct.
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

VALIDATOR = "validate-pm-feature-definition.py"
SUPPORTED = {"story_list", "criteria_list", "risk_analysis"}
REQUIRED_SECTIONS = {
    "story_list": (
        "Source and scope",
        "Stories",
        "Dependencies and sequencing",
        "Open questions",
    ),
    "criteria_list": (
        "Source requirements",
        "Acceptance scenarios",
        "Coverage notes",
        "Unresolved decisions",
    ),
    "risk_analysis": (
        "Context and assumptions",
        "Tigers",
        "Paper tigers",
        "Elephants",
        "Mitigations and monitoring",
        "Recommendation",
    ),
}
HANDOFF_RE = re.compile(
    r"^##\s+(?:\d+\.\s*)?Machine-readable handoff\s*$\s*```yaml\s*(.*?)\s*```",
    re.MULTILINE | re.IGNORECASE | re.DOTALL,
)


def _err(code: str, field: str, message: str, value: Any = None) -> dict[str, Any]:
    return {
        "error_id": code,
        "error_type": "contract_error",
        "field": field,
        "current_value": value,
        "message": message,
        "suggested_fixes": [],
        "reference": "docs/product-management/artifact-contracts.md",
    }


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any, *, nonempty: bool = False) -> bool:
    if not isinstance(value, list):
        return False
    if nonempty and not value:
        return False
    return all(_text(item) for item in value)


def _unique_ids(items: Any, *, field: str, errors: list[dict[str, Any]]) -> None:
    if not isinstance(items, list):
        errors.append(_err("PM_LIST_REQUIRED", field, f"{field} must be a list", items))
        return
    ids: list[str] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict) or not _text(item.get("id")):
            errors.append(
                _err(
                    "PM_ID_REQUIRED",
                    f"{field}[{index}].id",
                    "item id must be non-empty",
                    None if not isinstance(item, dict) else item.get("id"),
                )
            )
            continue
        ids.append(item["id"].strip())
    if len(ids) != len(set(ids)):
        errors.append(_err("PM_DUPLICATE_ID", field, f"{field} contains duplicate ids", ids))


def _require(data: dict[str, Any], fields: tuple[str, ...], errors: list[dict[str, Any]]) -> None:
    for field in fields:
        if field not in data:
            errors.append(_err("PM_MISSING_FIELD", field, f"required field {field!r} is missing"))


def _validate_story_list(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    _require(
        data,
        ("schema_version", "source_artifact_ref", "scope_status", "stories", "unresolved_questions"),
        errors,
    )
    if not _text(data.get("source_artifact_ref")):
        errors.append(_err("PM_SOURCE_REQUIRED", "source_artifact_ref", "source_artifact_ref must be non-empty", data.get("source_artifact_ref")))
    if data.get("scope_status") not in {"approved", "proposed", "mixed"}:
        errors.append(_err("PM_INVALID_STATUS", "scope_status", "scope_status must be approved, proposed, or mixed", data.get("scope_status")))

    stories = data.get("stories")
    _unique_ids(stories, field="stories", errors=errors)
    if isinstance(stories, list):
        for i, story in enumerate(stories):
            if not isinstance(story, dict):
                continue
            for field in ("want", "value"):
                if not _text(story.get(field)):
                    errors.append(_err("PM_TEXT_REQUIRED", f"stories[{i}].{field}", f"{field} must be non-empty text", story.get(field)))
            actor = story.get("actor")
            if actor is not None and not _text(actor):
                errors.append(_err("PM_TEXT_REQUIRED", f"stories[{i}].actor", "actor must be null/omitted or non-empty text", actor))
            if not _string_list(story.get("source_refs"), nonempty=True):
                errors.append(_err("PM_SOURCE_REQUIRED", f"stories[{i}].source_refs", "each story requires at least one source reference", story.get("source_refs")))
            if not _string_list(story.get("acceptance_intent"), nonempty=True):
                errors.append(_err("PM_ACCEPTANCE_REQUIRED", f"stories[{i}].acceptance_intent", "each story requires at least one acceptance intent", story.get("acceptance_intent")))
            if not isinstance(story.get("dependencies", []), list):
                errors.append(_err("PM_LIST_REQUIRED", f"stories[{i}].dependencies", "dependencies must be a list", story.get("dependencies")))
            if story.get("scope_status") not in {"approved", "proposed"}:
                errors.append(_err("PM_INVALID_STATUS", f"stories[{i}].scope_status", "story scope_status must be approved or proposed", story.get("scope_status")))

    if not isinstance(data.get("unresolved_questions"), list):
        errors.append(_err("PM_LIST_REQUIRED", "unresolved_questions", "unresolved_questions must be a list", data.get("unresolved_questions")))


def _validate_criteria_list(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    _require(
        data,
        ("schema_version", "source_artifact_ref", "scenarios", "unresolved_questions"),
        errors,
    )
    if not _text(data.get("source_artifact_ref")):
        errors.append(_err("PM_SOURCE_REQUIRED", "source_artifact_ref", "source_artifact_ref must be non-empty", data.get("source_artifact_ref")))

    scenarios = data.get("scenarios")
    _unique_ids(scenarios, field="scenarios", errors=errors)
    categories = {"happy_path", "alternate", "edge", "error", "state", "integration", "accessibility", "performance"}
    if isinstance(scenarios, list):
        for i, scenario in enumerate(scenarios):
            if not isinstance(scenario, dict):
                continue
            if not _text(scenario.get("source_story_ref")):
                errors.append(_err("PM_SOURCE_REQUIRED", f"scenarios[{i}].source_story_ref", "scenario must trace to a source story/requirement", scenario.get("source_story_ref")))
            if scenario.get("category") not in categories:
                errors.append(_err("PM_INVALID_CATEGORY", f"scenarios[{i}].category", f"category must be one of {sorted(categories)}", scenario.get("category")))
            for field in ("given", "when"):
                if not _text(scenario.get(field)):
                    errors.append(_err("PM_TEXT_REQUIRED", f"scenarios[{i}].{field}", f"{field} must be non-empty text", scenario.get(field)))
            if not _string_list(scenario.get("then"), nonempty=True):
                errors.append(_err("PM_ASSERTION_REQUIRED", f"scenarios[{i}].then", "then must contain at least one observable assertion", scenario.get("then")))
            if scenario.get("status") != "specified":
                errors.append(_err("PM_INVALID_STATUS", f"scenarios[{i}].status", "criteria scenario status must be specified; execution status belongs to test evidence", scenario.get("status")))

    if not isinstance(data.get("unresolved_questions"), list):
        errors.append(_err("PM_LIST_REQUIRED", "unresolved_questions", "unresolved_questions must be a list", data.get("unresolved_questions")))


def _validate_risk_analysis(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    _require(
        data,
        ("schema_version", "source_artifact_ref", "risks", "recommendation", "conditions", "unresolved_questions"),
        errors,
    )
    if not _text(data.get("source_artifact_ref")):
        errors.append(_err("PM_SOURCE_REQUIRED", "source_artifact_ref", "source_artifact_ref must be non-empty", data.get("source_artifact_ref")))

    risks = data.get("risks")
    _unique_ids(risks, field="risks", errors=errors)
    classes = {"tiger", "paper_tiger", "elephant"}
    evidence_statuses = {"observed", "inferred", "hypothetical", "unknown"}
    urgencies = {"launch_blocking", "fast_follow", "track", "investigate"}
    levels = {"high", "medium", "low", "unknown"}
    if isinstance(risks, list):
        for i, risk in enumerate(risks):
            if not isinstance(risk, dict):
                continue
            if risk.get("class") not in classes:
                errors.append(_err("PM_INVALID_RISK_CLASS", f"risks[{i}].class", f"class must be one of {sorted(classes)}", risk.get("class")))
            if not _text(risk.get("statement")):
                errors.append(_err("PM_TEXT_REQUIRED", f"risks[{i}].statement", "risk statement must be non-empty", risk.get("statement")))
            evidence_status = risk.get("evidence_status")
            if evidence_status not in evidence_statuses:
                errors.append(_err("PM_INVALID_EVIDENCE_STATUS", f"risks[{i}].evidence_status", f"evidence_status must be one of {sorted(evidence_statuses)}", evidence_status))
            refs = risk.get("evidence_refs")
            if not _string_list(refs):
                errors.append(_err("PM_INVALID_EVIDENCE_REFS", f"risks[{i}].evidence_refs", "evidence_refs must be a list of non-empty strings", refs))
            if risk.get("class") == "tiger" and evidence_status == "hypothetical":
                errors.append(_err("PM_TIGER_NEEDS_EVIDENCE", f"risks[{i}].evidence_status", "a purely hypothetical risk cannot be encoded as a current tiger; use elephant/paper_tiger or stronger evidence status", evidence_status))
            if risk.get("urgency") not in urgencies:
                errors.append(_err("PM_INVALID_URGENCY", f"risks[{i}].urgency", f"urgency must be one of {sorted(urgencies)}", risk.get("urgency")))
            for field in ("impact", "probability"):
                if risk.get(field) not in levels:
                    errors.append(_err("PM_INVALID_LEVEL", f"risks[{i}].{field}", f"{field} must be one of {sorted(levels)}", risk.get(field)))
            for field in ("mitigation", "owner_role", "success_criterion", "escalation_signal"):
                if field in risk and risk[field] is not None and not _text(risk[field]):
                    errors.append(_err("PM_TEXT_REQUIRED", f"risks[{i}].{field}", f"{field} must be null/omitted or non-empty text", risk[field]))

    if data.get("recommendation") not in {"go", "go_with_conditions", "no_go", "insufficient_evidence"}:
        errors.append(_err("PM_INVALID_RECOMMENDATION", "recommendation", "recommendation must be go, go_with_conditions, no_go, or insufficient_evidence", data.get("recommendation")))
    if not isinstance(data.get("conditions"), list):
        errors.append(_err("PM_LIST_REQUIRED", "conditions", "conditions must be a list", data.get("conditions")))
    if not isinstance(data.get("unresolved_questions"), list):
        errors.append(_err("PM_LIST_REQUIRED", "unresolved_questions", "unresolved_questions must be a list", data.get("unresolved_questions")))


def validate(path: Path) -> tuple[str, list[dict[str, Any]]]:
    if not path.is_file():
        return "unknown", [_err("PM_ARTIFACT_NOT_FOUND", "artifact", f"artifact file not found: {path}")]

    content = path.read_text(encoding="utf-8")
    blocks = HANDOFF_RE.findall(content)
    if len(blocks) != 1:
        return "unknown", [_err("PM_HANDOFF_BLOCK_COUNT", "machine_readable_handoff", "expected exactly one '## Machine-readable handoff' YAML block", len(blocks))]

    try:
        data = yaml.safe_load(blocks[0])
    except yaml.YAMLError as exc:
        return "unknown", [_err("PM_INVALID_YAML", "machine_readable_handoff", f"invalid YAML: {exc}")]
    if not isinstance(data, dict):
        return "unknown", [_err("PM_INVALID_YAML_SHAPE", "machine_readable_handoff", "handoff YAML must be a mapping", data)]

    artifact_id = data.get("artifact_id")
    if artifact_id not in SUPPORTED:
        return str(artifact_id or "unknown"), [_err("PM_UNSUPPORTED_ARTIFACT", "artifact_id", f"unsupported feature-definition artifact: {artifact_id!r}", artifact_id)]

    errors: list[dict[str, Any]] = []
    for section in REQUIRED_SECTIONS[artifact_id]:
        if not re.search(rf"^##\s+(?:\d+\.\s*)?{re.escape(section)}\s*$", content, re.MULTILINE | re.IGNORECASE):
            errors.append(_err("PM_MISSING_SECTION", "sections", f"required section {section!r} is missing"))

    if data.get("schema_version") not in {"1", 1}:
        errors.append(_err("PM_INVALID_SCHEMA_VERSION", "schema_version", "schema_version must be 1", data.get("schema_version")))

    if artifact_id == "story_list":
        _validate_story_list(data, errors)
    elif artifact_id == "criteria_list":
        _validate_criteria_list(data, errors)
    else:
        _validate_risk_analysis(data, errors)

    return artifact_id, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate PM feature-definition artifacts")
    parser.add_argument("artifact_path", help="Path to artifact markdown")
    parser.add_argument("--repo-root", default=".", help="Repository root (reserved for validator interface parity)")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON")
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
        for error in errors:
            print(f"ERROR {error['error_id']}: {error['message']}")
    else:
        print(f"{artifact_id} validation passed")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
