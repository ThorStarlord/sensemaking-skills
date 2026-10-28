"""Mechanically validate architectural_synthesis artifacts.

Representation only: the validator does not compare options, prefer or select
one, authorize implementation, or establish semantic truth. It checks identity,
links between options, consequences and the preference, the separation of a
provisional preference from a decision, and the authorization invariants.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ARTIFACT_ID = "architectural_synthesis"
SCHEMA_VERSIONS = {1}

OPTION_ID = re.compile(r"arch:[a-z0-9][a-z0-9._-]*\Z")
POSSIBILITY_ID = re.compile(r"poss:[a-z0-9][a-z0-9._-]*\Z")
CONSEQUENCE_ID = re.compile(r"conseq:[a-z0-9][a-z0-9._-]*\Z")

COMPARISON_OUTCOMES = {
    "PROVISIONALLY_PREFERRED",
    "RETAINED_ALTERNATIVE",
    "DECLINED",
    "UNRESOLVED",
}
PREFERENCE_STATUSES = {"PROVISIONAL"}
FEEDBACK_OUTCOMES = {
    "REAFFIRM",
    "REVISE_PREFERENCE",
    "REOPEN_ALTERNATIVES",
    "INVESTIGATE",
    "DEFER",
    "NO_CHANGE",
    "OWNER_DECISION_REQUIRED",
    "THESIS_REVIEW_REQUIRED",
}
FORBIDDEN_KEYS = {"score", "scores", "weight", "weights", "rank", "ranking", "risk_score"}

REQUIRED = {
    "artifact_id",
    "schema_version",
    "target_repository",
    "target_source_identity",
    "governing_intent_refs",
    "target_possibility_refs",
    "current_architecture_refs",
    "architecture_options",
    "option_comparison",
    "provisional_preference",
    "unresolved_questions",
    "implementation_authority_established_by_artifact",
    "semantic_truth_established",
    "created_at",
    "immutable",
}


def _error(code: str, message: str) -> dict[str, str]:
    return {"error_id": code, "message": message}


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any, *, allow_empty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (allow_empty or bool(value))
        and all(_text(item) for item in value)
    )


def _id_list(value: Any, pattern: re.Pattern[str]) -> bool:
    return _string_list(value, allow_empty=True) and all(pattern.fullmatch(item) for item in value)


def _extract(content: str) -> dict[str, Any] | None:
    for block in reversed(re.findall(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)):
        try:
            value = yaml.safe_load(block)
        except yaml.YAMLError:
            continue
        if isinstance(value, dict) and value.get("artifact_id") == ARTIFACT_ID:
            return value
    return None


def _validate_options(data: dict[str, Any], errors: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    options = data.get("architecture_options")
    if not isinstance(options, list) or len(options) < 2:
        errors.append(_error(
            "SYNTHESIS_OPTIONS_INVALID",
            "architecture_options must list at least two options; evaluate a single "
            "proposed direction with architectural-review instead",
        ))
        return {}

    by_id: dict[str, dict[str, Any]] = {}
    for index, option in enumerate(options):
        where = f"architecture_options[{index}]"
        if not isinstance(option, dict):
            errors.append(_error("SYNTHESIS_OPTION_INVALID", f"{where} must be a mapping"))
            continue
        option_id = option.get("option_id")
        if not isinstance(option_id, str) or not OPTION_ID.fullmatch(option_id):
            errors.append(_error("SYNTHESIS_OPTION_ID_INVALID", f"{where}.option_id must match arch:<slug>"))
        elif option_id in by_id:
            errors.append(_error("SYNTHESIS_OPTION_ID_DUPLICATE", f"{where}.option_id {option_id}"))
        else:
            by_id[option_id] = option
        for field in ("title", "proposed_structure", "comparison_reason"):
            if not _text(option.get(field)):
                errors.append(_error("SYNTHESIS_OPTION_TEXT_INVALID", f"{where}.{field}"))
        if option.get("comparison_outcome") not in COMPARISON_OUTCOMES:
            errors.append(_error(
                "SYNTHESIS_OPTION_OUTCOME_INVALID",
                f"{where}.comparison_outcome must be one of {sorted(COMPARISON_OUTCOMES)}",
            ))
        if not _string_list(option.get("assumption_refs"), allow_empty=True):
            errors.append(_error("SYNTHESIS_OPTION_ASSUMPTIONS_INVALID", f"{where}.assumption_refs"))
        if not _id_list(option.get("conditional_consequence_refs"), CONSEQUENCE_ID):
            errors.append(_error(
                "SYNTHESIS_OPTION_CONSEQUENCES_INVALID",
                f"{where}.conditional_consequence_refs must be a list of conseq:<slug> ids",
            ))
        if "reuses_refs" in option and not _string_list(option["reuses_refs"], allow_empty=True):
            errors.append(_error("SYNTHESIS_OPTION_REUSES_INVALID", f"{where}.reuses_refs"))
        transitions = option.get("proposed_transitions")
        if not isinstance(transitions, list):
            errors.append(_error("SYNTHESIS_TRANSITIONS_INVALID", f"{where}.proposed_transitions must be a list"))
            continue
        for t_index, transition in enumerate(transitions):
            t_where = f"{where}.proposed_transitions[{t_index}]"
            if not isinstance(transition, dict) or not all(
                _text(transition.get(field)) for field in ("target_ref", "change")
            ):
                errors.append(_error("SYNTHESIS_TRANSITION_INVALID", f"{t_where} needs target_ref and change"))
    return by_id


def _validate_preference(
    data: dict[str, Any],
    options: dict[str, dict[str, Any]],
    errors: list[dict[str, str]],
) -> None:
    preferred = sorted(
        option_id
        for option_id, option in options.items()
        if option.get("comparison_outcome") == "PROVISIONALLY_PREFERRED"
    )
    preference = data.get("provisional_preference")
    if preference is None:
        if not _text(data.get("no_preference_reason")):
            errors.append(_error(
                "SYNTHESIS_NO_PREFERENCE_REASON_MISSING",
                "provisional_preference is null; state no_preference_reason",
            ))
        if preferred:
            errors.append(_error(
                "SYNTHESIS_PREFERENCE_INCONSISTENT",
                f"no provisional_preference, but options are PROVISIONALLY_PREFERRED: {preferred}",
            ))
        return
    if not isinstance(preference, dict):
        errors.append(_error("SYNTHESIS_PREFERENCE_INVALID", "provisional_preference must be a mapping or null"))
        return
    status = preference.get("status")
    if status not in PREFERENCE_STATUSES:
        errors.append(_error(
            "SYNTHESIS_PREFERENCE_STATUS_NOT_PROVISIONAL",
            f"provisional_preference.status is {status!r}; a synthesis records only a PROVISIONAL "
            "preference, and selection belongs to the governing decision process",
        ))
    for field in ("attribution", "rationale"):
        if not _text(preference.get(field)):
            errors.append(_error("SYNTHESIS_PREFERENCE_TEXT_INVALID", f"provisional_preference.{field}"))
    if "scope" in preference and not _text(preference["scope"]):
        errors.append(_error("SYNTHESIS_PREFERENCE_TEXT_INVALID", "provisional_preference.scope"))
    option_id = preference.get("option_id")
    if option_id not in options:
        errors.append(_error(
            "SYNTHESIS_PREFERENCE_OPTION_UNKNOWN",
            f"provisional_preference.option_id {option_id!r} is not a listed option",
        ))
    elif preferred != [option_id]:
        errors.append(_error(
            "SYNTHESIS_PREFERENCE_INCONSISTENT",
            f"only {option_id} may be PROVISIONALLY_PREFERRED; found {preferred}",
        ))


def _validate_feedback(
    data: dict[str, Any],
    options: dict[str, dict[str, Any]],
    errors: list[dict[str, str]],
) -> None:
    if "preference_feedback" not in data:
        return
    feedback = data["preference_feedback"]
    if not isinstance(feedback, list):
        errors.append(_error("SYNTHESIS_FEEDBACK_INVALID", "preference_feedback must be a list"))
        return
    known = {
        ref
        for option in options.values()
        for ref in option.get("conditional_consequence_refs") or []
        if isinstance(ref, str)
    }
    for index, item in enumerate(feedback):
        where = f"preference_feedback[{index}]"
        if not isinstance(item, dict):
            errors.append(_error("SYNTHESIS_FEEDBACK_INVALID", f"{where} must be a mapping"))
            continue
        if item.get("consequence_ref") not in known:
            errors.append(_error(
                "SYNTHESIS_FEEDBACK_CONSEQUENCE_UNKNOWN",
                f"{where}.consequence_ref must be one of the options' conditional_consequence_refs",
            ))
        if item.get("outcome") not in FEEDBACK_OUTCOMES:
            errors.append(_error(
                "SYNTHESIS_FEEDBACK_OUTCOME_INVALID",
                f"{where}.outcome must be one of {sorted(FEEDBACK_OUTCOMES)}",
            ))
        if not _text(item.get("effect")):
            errors.append(_error("SYNTHESIS_FEEDBACK_TEXT_INVALID", f"{where}.effect"))


def _forbidden_keys(data: Any, errors: list[dict[str, str]]) -> None:
    stack: list[tuple[str, Any]] = [("", data)]
    while stack:
        prefix, value = stack.pop()
        if isinstance(value, dict):
            for key, child in value.items():
                path = f"{prefix}.{key}" if prefix else str(key)
                if str(key).lower() in FORBIDDEN_KEYS:
                    errors.append(_error("SYNTHESIS_SCORING_FIELD_FORBIDDEN", path))
                stack.append((path, child))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                stack.append((f"{prefix}[{index}]", child))


def validate(path: Path) -> list[dict[str, str]]:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [_error("SYNTHESIS_FILE_UNREADABLE", str(exc))]
    data = _extract(content)
    if data is None:
        return [_error("SYNTHESIS_MACHINE_BLOCK_MISSING", f"No {ARTIFACT_ID} YAML block found.")]

    errors: list[dict[str, str]] = []
    missing = sorted(REQUIRED - set(data))
    if missing:
        errors.append(_error("SYNTHESIS_FIELDS_MISSING", ", ".join(missing)))

    if data.get("schema_version") not in SCHEMA_VERSIONS:
        errors.append(_error("SYNTHESIS_SCHEMA_VERSION_INVALID", f"schema_version must be one of {sorted(SCHEMA_VERSIONS)}"))
    for field in ("target_repository", "target_source_identity"):
        if not _text(data.get(field)):
            errors.append(_error("SYNTHESIS_TEXT_INVALID", field))
    created_at = data.get("created_at")
    if not (_text(created_at) or isinstance(created_at, (dt.date, dt.datetime))):
        errors.append(_error("SYNTHESIS_TEXT_INVALID", "created_at"))
    for field in ("governing_intent_refs", "current_architecture_refs"):
        if not _string_list(data.get(field)):
            errors.append(_error("SYNTHESIS_REFS_INVALID", f"{field} must be a non-empty list of strings"))
    if not _id_list(data.get("target_possibility_refs"), POSSIBILITY_ID):
        errors.append(_error("SYNTHESIS_POSSIBILITY_REFS_INVALID", "target_possibility_refs must list poss:<slug> ids"))
    if "derived_possibility_refs" in data and not _id_list(data["derived_possibility_refs"], POSSIBILITY_ID):
        errors.append(_error("SYNTHESIS_POSSIBILITY_REFS_INVALID", "derived_possibility_refs must list poss:<slug> ids"))
    if not _string_list(data.get("unresolved_questions"), allow_empty=True):
        errors.append(_error("SYNTHESIS_LIST_INVALID", "unresolved_questions must be a list of strings"))
    if "reconsideration_conditions" in data and not _string_list(data["reconsideration_conditions"], allow_empty=True):
        errors.append(_error("SYNTHESIS_LIST_INVALID", "reconsideration_conditions must be a list of strings"))
    if "candidate_responsibility" in data and data["candidate_responsibility"] is not None and not _text(data["candidate_responsibility"]):
        errors.append(_error("SYNTHESIS_TEXT_INVALID", "candidate_responsibility"))

    options = _validate_options(data, errors)

    comparison = data.get("option_comparison")
    if not isinstance(comparison, dict):
        errors.append(_error("SYNTHESIS_COMPARISON_INVALID", "option_comparison must be a mapping"))
    else:
        if not _string_list(comparison.get("lenses")):
            errors.append(_error("SYNTHESIS_COMPARISON_INVALID", "option_comparison.lenses must be a non-empty list"))
        for field in ("attribution", "summary"):
            if not _text(comparison.get(field)):
                errors.append(_error("SYNTHESIS_COMPARISON_INVALID", f"option_comparison.{field}"))

    _validate_preference(data, options, errors)
    _validate_feedback(data, options, errors)

    for field in ("implementation_authority_established_by_artifact", "semantic_truth_established"):
        if data.get(field) is not False:
            errors.append(_error("SYNTHESIS_AUTHORITY_FLAG_INVALID", f"{field} must be false"))
    if not isinstance(data.get("immutable"), bool):
        errors.append(_error("SYNTHESIS_IMMUTABLE_INVALID", "immutable must be a boolean"))

    _forbidden_keys(data, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--repo-root", default=".", help="Accepted for validator-runner compatibility; unused")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    errors = validate(args.artifact)
    result = {
        "valid": not errors,
        "artifact_id": ARTIFACT_ID,
        "artifact_path": str(args.artifact),
        "errors": errors,
        "option_selected_by_validator": False,
        "implementation_authorized_by_validator": False,
        "semantic_truth_established": False,
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    elif errors:
        print("FAIL")
        for item in errors:
            print(f"{item['error_id']}: {item['message']}")
    else:
        print("PASS")
        print("mechanical representation valid; option quality, preference and authorization remain semantic/external")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
