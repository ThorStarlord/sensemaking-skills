#!/usr/bin/env python3
"""Validate the experimental semantic_reasoning_profile v1 contract.

This validator checks representation only. It deliberately does not judge claim
truth, evidence sufficiency, uncertainty priority, responsibility warrant,
architectural quality, repair success, or Campaign disposition.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

VALIDATOR = "validate-semantic-reasoning-profile.py"
REFERENCE = "docs/semantic-architecture/common-semantic-contract.md"
ARTIFACT_ID = "semantic_reasoning_profile"
SCHEMA_VERSION = 1

ACCESS_MODES = {"github_exact_sha", "local_snapshot", "inherited_artifact"}
CURRENTNESS_STATUSES = {
    "pinned_snapshot",
    "verified_current",
    "inherited_currentness",
    "unverified",
}
OBSERVATION_METHODS = {
    "direct_read",
    "probe",
    "git_metadata",
    "validator_output",
    "artifact_read",
    "owner_statement",
    "other",
}
EPISTEMIC_STATUSES = {
    "OBSERVED",
    "DERIVED",
    "INFERRED",
    "HYPOTHESIZED",
    "RATIFIED",
    "CONTRADICTED",
    "SUPERSEDED",
    "UNRESOLVED",
}
EVIDENCE_GROUNDED_STATUSES = {
    "OBSERVED",
    "DERIVED",
    "INFERRED",
    "RATIFIED",
    "CONTRADICTED",
    "SUPERSEDED",
}
UNCERTAINTY_STATUSES = {"active", "resolved", "deferred"}
REQUIRED_TOP_LEVEL = {
    "artifact_id",
    "schema_version",
    "pilot_id",
    "source_skill",
    "target",
    "currentness",
    "observations",
    "claims",
    "uncertainties",
    "explicit_limits",
}


def _err(code: str, field: str, message: str, value: Any = None) -> dict[str, Any]:
    return {
        "error_id": code,
        "error_type": "contract_error",
        "field": field,
        "current_value": value,
        "message": message,
        "suggested_fixes": [],
        "reference": REFERENCE,
    }


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any, *, nonempty: bool = False) -> bool:
    if not isinstance(value, list):
        return False
    if nonempty and not value:
        return False
    return all(_text(item) for item in value)


def _mapping(value: Any) -> bool:
    return isinstance(value, dict)


def _require_fields(
    data: dict[str, Any],
    required: set[str],
    *,
    prefix: str,
    errors: list[dict[str, Any]],
) -> None:
    for field in sorted(required):
        if field not in data:
            path = f"{prefix}.{field}" if prefix else field
            errors.append(_err("SEMANTIC_MISSING_FIELD", path, f"required field {path!r} is missing"))


def _unique_ids(
    items: Any,
    *,
    field: str,
    require_nonempty: bool,
    errors: list[dict[str, Any]],
) -> None:
    if not isinstance(items, list):
        errors.append(_err("SEMANTIC_LIST_REQUIRED", field, f"{field} must be a list", items))
        return
    if require_nonempty and not items:
        errors.append(_err("SEMANTIC_NONEMPTY_LIST_REQUIRED", field, f"{field} must contain at least one item", items))
        return
    ids: list[str] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(_err("SEMANTIC_MAPPING_REQUIRED", f"{field}[{index}]", "item must be a mapping", item))
            continue
        item_id = item.get("id")
        if not _text(item_id):
            errors.append(_err("SEMANTIC_ID_REQUIRED", f"{field}[{index}].id", "item id must be non-empty text", item_id))
            continue
        ids.append(item_id.strip())
    if len(ids) != len(set(ids)):
        errors.append(_err("SEMANTIC_DUPLICATE_ID", field, f"{field} contains duplicate ids", ids))


def _validate_target(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    target = data.get("target")
    if not _mapping(target):
        errors.append(_err("SEMANTIC_MAPPING_REQUIRED", "target", "target must be a mapping", target))
        return
    _require_fields(target, {"repository", "ref", "access_mode"}, prefix="target", errors=errors)
    for field in ("repository", "ref"):
        if field in target and not _text(target.get(field)):
            errors.append(_err("SEMANTIC_TEXT_REQUIRED", f"target.{field}", f"target.{field} must be non-empty text", target.get(field)))
    if target.get("access_mode") not in ACCESS_MODES:
        errors.append(
            _err(
                "SEMANTIC_INVALID_ACCESS_MODE",
                "target.access_mode",
                f"access_mode must be one of {sorted(ACCESS_MODES)}",
                target.get("access_mode"),
            )
        )


def _validate_currentness(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    currentness = data.get("currentness")
    if not _mapping(currentness):
        errors.append(_err("SEMANTIC_MAPPING_REQUIRED", "currentness", "currentness must be a mapping", currentness))
        return
    _require_fields(currentness, {"status", "evidence_refs"}, prefix="currentness", errors=errors)
    status = currentness.get("status")
    if status not in CURRENTNESS_STATUSES:
        errors.append(
            _err(
                "SEMANTIC_INVALID_CURRENTNESS_STATUS",
                "currentness.status",
                f"status must be one of {sorted(CURRENTNESS_STATUSES)}",
                status,
            )
        )
    refs = currentness.get("evidence_refs")
    if not _string_list(refs):
        errors.append(_err("SEMANTIC_INVALID_EVIDENCE_REFS", "currentness.evidence_refs", "evidence_refs must be a list of non-empty strings", refs))
    elif status != "unverified" and not refs:
        errors.append(
            _err(
                "SEMANTIC_CURRENTNESS_EVIDENCE_REQUIRED",
                "currentness.evidence_refs",
                "verified/pinned/inherited currentness requires at least one evidence ref",
                refs,
            )
        )


def _validate_observations(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    observations = data.get("observations")
    _unique_ids(observations, field="observations", require_nonempty=True, errors=errors)
    if not isinstance(observations, list):
        return
    for index, observation in enumerate(observations):
        if not isinstance(observation, dict):
            continue
        _require_fields(observation, {"id", "statement", "method", "evidence_refs"}, prefix=f"observations[{index}]", errors=errors)
        if "statement" in observation and not _text(observation.get("statement")):
            errors.append(_err("SEMANTIC_TEXT_REQUIRED", f"observations[{index}].statement", "observation statement must be non-empty text", observation.get("statement")))
        if observation.get("method") not in OBSERVATION_METHODS:
            errors.append(
                _err(
                    "SEMANTIC_INVALID_OBSERVATION_METHOD",
                    f"observations[{index}].method",
                    f"method must be one of {sorted(OBSERVATION_METHODS)}",
                    observation.get("method"),
                )
            )
        refs = observation.get("evidence_refs")
        if not _string_list(refs, nonempty=True):
            errors.append(_err("SEMANTIC_OBSERVATION_EVIDENCE_REQUIRED", f"observations[{index}].evidence_refs", "every observation requires at least one evidence ref", refs))


def _validate_claims(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    claims = data.get("claims")
    _unique_ids(claims, field="claims", require_nonempty=True, errors=errors)
    if not isinstance(claims, list):
        return
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            continue
        _require_fields(
            claim,
            {"id", "statement", "epistemic_status", "evidence_refs", "scope", "limits"},
            prefix=f"claims[{index}]",
            errors=errors,
        )
        for field in ("statement", "scope"):
            if field in claim and not _text(claim.get(field)):
                errors.append(_err("SEMANTIC_TEXT_REQUIRED", f"claims[{index}].{field}", f"claim {field} must be non-empty text", claim.get(field)))
        status = claim.get("epistemic_status")
        if status not in EPISTEMIC_STATUSES:
            errors.append(
                _err(
                    "SEMANTIC_INVALID_EPISTEMIC_STATUS",
                    f"claims[{index}].epistemic_status",
                    f"epistemic_status must be one of {sorted(EPISTEMIC_STATUSES)}",
                    status,
                )
            )
        refs = claim.get("evidence_refs")
        if not _string_list(refs):
            errors.append(_err("SEMANTIC_INVALID_EVIDENCE_REFS", f"claims[{index}].evidence_refs", "claim evidence_refs must be a list of non-empty strings", refs))
        elif status in EVIDENCE_GROUNDED_STATUSES and not refs:
            errors.append(
                _err(
                    "SEMANTIC_CLAIM_EVIDENCE_REQUIRED",
                    f"claims[{index}].evidence_refs",
                    f"{status} claims require at least one evidence ref",
                    refs,
                )
            )
        if not _string_list(claim.get("limits")):
            errors.append(_err("SEMANTIC_INVALID_LIMITS", f"claims[{index}].limits", "claim limits must be a list of non-empty strings", claim.get("limits")))


def _validate_uncertainties(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    uncertainties = data.get("uncertainties")
    _unique_ids(uncertainties, field="uncertainties", require_nonempty=False, errors=errors)
    if not isinstance(uncertainties, list):
        return
    for index, uncertainty in enumerate(uncertainties):
        if not isinstance(uncertainty, dict):
            continue
        _require_fields(
            uncertainty,
            {"id", "question", "decision_relevance", "evidence_needed", "status"},
            prefix=f"uncertainties[{index}]",
            errors=errors,
        )
        for field in ("question", "decision_relevance"):
            if field in uncertainty and not _text(uncertainty.get(field)):
                errors.append(_err("SEMANTIC_TEXT_REQUIRED", f"uncertainties[{index}].{field}", f"uncertainty {field} must be non-empty text", uncertainty.get(field)))
        if not _string_list(uncertainty.get("evidence_needed")):
            errors.append(_err("SEMANTIC_INVALID_EVIDENCE_NEEDED", f"uncertainties[{index}].evidence_needed", "evidence_needed must be a list of non-empty strings", uncertainty.get("evidence_needed")))
        if uncertainty.get("status") not in UNCERTAINTY_STATUSES:
            errors.append(
                _err(
                    "SEMANTIC_INVALID_UNCERTAINTY_STATUS",
                    f"uncertainties[{index}].status",
                    f"status must be one of {sorted(UNCERTAINTY_STATUSES)}",
                    uncertainty.get("status"),
                )
            )


def validate(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return [_err("SEMANTIC_PROFILE_NOT_FOUND", "artifact", f"profile file not found: {path}")]

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return [_err("SEMANTIC_INVALID_YAML", "artifact", f"could not parse profile YAML: {exc}")]

    if not isinstance(data, dict):
        return [_err("SEMANTIC_INVALID_YAML_SHAPE", "artifact", "profile YAML must be a mapping", data)]

    errors: list[dict[str, Any]] = []
    _require_fields(data, REQUIRED_TOP_LEVEL, prefix="", errors=errors)

    if data.get("artifact_id") != ARTIFACT_ID:
        errors.append(_err("SEMANTIC_INVALID_ARTIFACT_ID", "artifact_id", f"artifact_id must be {ARTIFACT_ID!r}", data.get("artifact_id")))
    if data.get("schema_version") not in {SCHEMA_VERSION, str(SCHEMA_VERSION)}:
        errors.append(_err("SEMANTIC_INVALID_SCHEMA_VERSION", "schema_version", "schema_version must be 1", data.get("schema_version")))
    for field in ("pilot_id", "source_skill"):
        if field in data and not _text(data.get(field)):
            errors.append(_err("SEMANTIC_TEXT_REQUIRED", field, f"{field} must be non-empty text", data.get(field)))

    _validate_target(data, errors)
    _validate_currentness(data, errors)
    _validate_observations(data, errors)
    _validate_claims(data, errors)
    _validate_uncertainties(data, errors)

    limits = data.get("explicit_limits")
    if not _string_list(limits, nonempty=True):
        errors.append(_err("SEMANTIC_EXPLICIT_LIMIT_REQUIRED", "explicit_limits", "explicit_limits must contain at least one non-empty limit/non-claim", limits))

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate semantic_reasoning_profile v1 representation")
    parser.add_argument("profile_path", help="Path to semantic reasoning profile YAML")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    args = parser.parse_args(argv)

    path = Path(args.profile_path)
    errors = validate(path)
    result = {
        "valid": not errors,
        "artifact_id": ARTIFACT_ID,
        "artifact_path": str(path.resolve()),
        "validator": VALIDATOR,
        "errors": errors,
        "validation_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "semantic_truth_established": False,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    elif errors:
        for error in errors:
            print(f"ERROR {error['error_id']}: {error['message']}")
    else:
        print("semantic_reasoning_profile representation validation passed; semantic truth not established")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
