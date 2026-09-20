"""Mechanically validate Strategic Repository Analysis artifacts.

This validator checks representation and internal references only. It does not
score strategic quality, choose a path, or establish implementation authority.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

CAPABILITY_STATES = {
    "ESTABLISHED",
    "PARTIAL",
    "MISSING",
    "DEFERRED",
    "BLOCKED",
    "CLAIMED_UNVERIFIED",
    "OUT_OF_SCOPE",
}
DISPOSITIONS = {
    "BUILD",
    "INVESTIGATE",
    "DEFER",
    "NO_CHANGE",
    "OWNER_DECISION",
    "THESIS_REVIEW",
}
CONTINUITY_DISPOSITIONS = {
    "NEW",
    "REAFFIRM",
    "CONTINUE",
    "REVISE",
    "SUPERSEDE",
    "CLOSE",
}
UNCERTAINTY_SOURCES = {
    "repository_evidence",
    "empirical",
    "owner_intent",
    "external_environment",
    "none",
}
COMPARISON_LENSES = {
    "mission_relevance",
    "decision_value",
    "blocking_power",
    "evidence_sufficiency",
    "consequence_of_error",
    "deferral_cost",
    "reversibility",
    "authority_availability",
    "dependency",
    "smallest_warranted_intervention",
}

REQUIRED_TOP_LEVEL = {
    "artifact_id",
    "target_repository",
    "target_source_identity",
    "governing_intent",
    "capability_states",
    "strategic_frontier",
    "construction_paths",
    "path_comparison",
    "decision_changing_uncertainty",
    "strategic_disposition",
    "selected_path_id",
    "candidate_repository_responsibility",
    "smallest_warranted_intervention",
    "implementation_authority_established_by_artifact",
    "semantic_truth_established",
    "created_at",
    "immutable",
}

PATH_FIELDS = {
    "path_id",
    "name",
    "future_state",
    "builds_on",
    "required_capabilities",
    "construction_sequence",
    "dependencies",
    "unlocks",
    "risks",
    "reversibility",
    "evidence_gaps",
}


def _error(code: str, message: str) -> dict[str, str]:
    return {"error_id": code, "message": message}


def _extract_machine_block(content: str) -> dict[str, Any] | None:
    blocks = re.findall(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)
    for block in reversed(blocks):
        try:
            value = yaml.safe_load(block)
        except yaml.YAMLError:
            continue
        if isinstance(value, dict) and value.get("artifact_id") == "strategic_repository_analysis":
            return value
    return None


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any) -> bool:
    return isinstance(value, list) and all(_nonempty_string(item) for item in value)


def _contains_number(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, dict):
        return any(_contains_number(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_number(item) for item in value)
    return False


def validate(path: Path) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [_error("STRATEGIC_ANALYSIS_FILE_UNREADABLE", str(exc))]

    data = _extract_machine_block(content)
    if data is None:
        return [
            _error(
                "STRATEGIC_ANALYSIS_MACHINE_BLOCK_MISSING",
                "No strategic_repository_analysis YAML block was found.",
            )
        ]

    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        errors.append(
            _error(
                "STRATEGIC_ANALYSIS_FIELDS_MISSING",
                "Missing fields: " + ", ".join(missing),
            )
        )

    if data.get("artifact_id") != "strategic_repository_analysis":
        errors.append(
            _error(
                "STRATEGIC_ANALYSIS_ARTIFACT_ID_INVALID",
                "artifact_id must be strategic_repository_analysis",
            )
        )

    if not _nonempty_string(data.get("target_repository")):
        errors.append(
            _error("STRATEGIC_ANALYSIS_TARGET_INVALID", "target_repository must be non-empty")
        )
    if not _nonempty_string(data.get("target_source_identity")):
        errors.append(
            _error(
                "STRATEGIC_ANALYSIS_SOURCE_IDENTITY_INVALID",
                "target_source_identity must be non-empty",
            )
        )
    if not _nonempty_string(data.get("governing_intent")):
        errors.append(
            _error(
                "STRATEGIC_ANALYSIS_INTENT_INVALID",
                "governing_intent must be non-empty",
            )
        )

    governing_authority_refs = data.get("governing_authority_refs")
    if governing_authority_refs is not None and not _string_list(governing_authority_refs):
        errors.append(
            _error(
                "STRATEGIC_ANALYSIS_GOVERNING_AUTHORITY_REFS_INVALID",
                "governing_authority_refs must be a list of non-empty strings when present",
            )
        )

    capabilities = data.get("capability_states")
    if not isinstance(capabilities, list):
        errors.append(
            _error(
                "STRATEGIC_ANALYSIS_CAPABILITY_STATES_INVALID",
                "capability_states must be a list",
            )
        )
        capabilities = []
    seen_capabilities: set[str] = set()
    for index, item in enumerate(capabilities):
        if not isinstance(item, dict):
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_CAPABILITY_ENTRY_INVALID",
                    f"capability_states[{index}] must be a mapping",
                )
            )
            continue
        capability_id = item.get("capability_id")
        state = item.get("state")
        refs = item.get("evidence_refs")
        if not _nonempty_string(capability_id):
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_CAPABILITY_ID_INVALID",
                    f"capability_states[{index}].capability_id must be non-empty",
                )
            )
        elif capability_id in seen_capabilities:
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_CAPABILITY_ID_DUPLICATE",
                    f"duplicate capability_id: {capability_id}",
                )
            )
        else:
            seen_capabilities.add(capability_id)
        if state not in CAPABILITY_STATES:
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_CAPABILITY_STATE_INVALID",
                    f"capability_states[{index}].state must be one of {sorted(CAPABILITY_STATES)}",
                )
            )
        if not _string_list(refs):
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_CAPABILITY_EVIDENCE_INVALID",
                    f"capability_states[{index}].evidence_refs must be a list of non-empty strings",
                )
            )

    frontier = data.get("strategic_frontier")
    if not isinstance(frontier, list):
        errors.append(
            _error(
                "STRATEGIC_ANALYSIS_FRONTIER_INVALID",
                "strategic_frontier must be a list",
            )
        )
        frontier = []
    frontier_ids: set[str] = set()
    for index, item in enumerate(frontier):
        if not isinstance(item, dict):
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_FRONTIER_ENTRY_INVALID",
                    f"strategic_frontier[{index}] must be a mapping",
                )
            )
            continue
        fid = item.get("frontier_id")
        statement = item.get("statement")
        if not _nonempty_string(fid) or not _nonempty_string(statement):
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_FRONTIER_ENTRY_INVALID",
                    f"strategic_frontier[{index}] requires frontier_id and statement",
                )
            )
        elif fid in frontier_ids:
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_FRONTIER_ID_DUPLICATE",
                    f"duplicate frontier_id: {fid}",
                )
            )
        else:
            frontier_ids.add(fid)

    paths = data.get("construction_paths")
    if not isinstance(paths, list):
        errors.append(
            _error(
                "STRATEGIC_ANALYSIS_PATHS_INVALID",
                "construction_paths must be a list",
            )
        )
        paths = []
    if len(paths) > 5:
        errors.append(
            _error(
                "STRATEGIC_ANALYSIS_TOO_MANY_PATHS",
                "construction_paths must contain at most 5 paths",
            )
        )

    path_ids: set[str] = set()
    transition_refs: set[str] = set()
    for index, item in enumerate(paths):
        if not isinstance(item, dict):
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_PATH_INVALID",
                    f"construction_paths[{index}] must be a mapping",
                )
            )
            continue
        missing_path = sorted(PATH_FIELDS - set(item))
        if missing_path:
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_PATH_FIELDS_MISSING",
                    f"construction_paths[{index}] missing: {', '.join(missing_path)}",
                )
            )
        path_id = item.get("path_id")
        if not _nonempty_string(path_id):
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_PATH_ID_INVALID",
                    f"construction_paths[{index}].path_id must be non-empty",
                )
            )
        elif path_id in path_ids:
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_PATH_ID_DUPLICATE",
                    f"duplicate path_id: {path_id}",
                )
            )
        else:
            path_ids.add(path_id)

        for field in (
            "builds_on",
            "required_capabilities",
            "construction_sequence",
            "dependencies",
            "unlocks",
            "risks",
            "evidence_gaps",
            "assumptions",
            "reassessment_triggers",
        ):
            if field in item and not _string_list(item.get(field)):
                errors.append(
                    _error(
                        "STRATEGIC_ANALYSIS_PATH_LIST_INVALID",
                        f"construction_paths[{index}].{field} must be a list of non-empty strings",
                    )
                )

        path_transitions = item.get("path_transitions")
        if path_transitions is not None:
            if not isinstance(path_transitions, list):
                errors.append(
                    _error(
                        "STRATEGIC_ANALYSIS_PATH_TRANSITIONS_INVALID",
                        f"construction_paths[{index}].path_transitions must be a list when present",
                    )
                )
            else:
                prohibited_transition_fields = {
                    "priority",
                    "deadline",
                    "estimate",
                    "percent_complete",
                    "assignee",
                    "start_date",
                    "due_date",
                    "blocked_by",
                    "next_transition",
                }
                for transition_index, transition in enumerate(path_transitions):
                    if not isinstance(transition, dict):
                        errors.append(
                            _error(
                                "STRATEGIC_ANALYSIS_PATH_TRANSITION_INVALID",
                                f"construction_paths[{index}].path_transitions[{transition_index}] must be a mapping",
                            )
                        )
                        continue
                    transition_ref = transition.get("transition_ref")
                    transition_text = transition.get("transition")
                    if not _nonempty_string(transition_ref) or not _nonempty_string(
                        transition_text
                    ):
                        errors.append(
                            _error(
                                "STRATEGIC_ANALYSIS_PATH_TRANSITION_INVALID",
                                f"construction_paths[{index}].path_transitions[{transition_index}] requires transition_ref and transition",
                            )
                        )
                        continue
                    if _nonempty_string(path_id) and not transition_ref.startswith(
                        f"{path_id}/"
                    ):
                        errors.append(
                            _error(
                                "STRATEGIC_ANALYSIS_PATH_TRANSITION_PREFIX_INVALID",
                                f"{transition_ref} must be namespaced under {path_id}/",
                            )
                        )
                    if transition_ref in transition_refs:
                        errors.append(
                            _error(
                                "STRATEGIC_ANALYSIS_PATH_TRANSITION_DUPLICATE",
                                f"duplicate transition_ref: {transition_ref}",
                            )
                        )
                    else:
                        transition_refs.add(transition_ref)
                    prohibited = sorted(prohibited_transition_fields & set(transition))
                    if prohibited:
                        errors.append(
                            _error(
                                "STRATEGIC_ANALYSIS_PATH_TRANSITION_ROADMAP_FIELD_FORBIDDEN",
                                "path transition contains roadmap/scheduling fields: "
                                + ", ".join(prohibited),
                            )
                        )
        for field in ("name", "future_state", "reversibility"):
            if field in item and not _nonempty_string(item.get(field)):
                errors.append(
                    _error(
                        "STRATEGIC_ANALYSIS_PATH_TEXT_INVALID",
                        f"construction_paths[{index}].{field} must be non-empty",
                    )
                )

    candidate_transition_ref = data.get("candidate_path_transition_ref")
    if candidate_transition_ref is not None:
        if not _nonempty_string(candidate_transition_ref):
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_CANDIDATE_TRANSITION_REF_INVALID",
                    "candidate_path_transition_ref must be a non-empty string when present",
                )
            )
        elif candidate_transition_ref not in transition_refs:
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_CANDIDATE_TRANSITION_UNKNOWN",
                    "candidate_path_transition_ref must reference a declared path transition",
                )
            )

    comparisons = data.get("path_comparison")
    if not isinstance(comparisons, list):
        errors.append(
            _error(
                "STRATEGIC_ANALYSIS_COMPARISON_INVALID",
                "path_comparison must be a list",
            )
        )
        comparisons = []
    compared_ids: set[str] = set()
    for index, item in enumerate(comparisons):
        if not isinstance(item, dict):
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_COMPARISON_ENTRY_INVALID",
                    f"path_comparison[{index}] must be a mapping",
                )
            )
            continue
        pid = item.get("path_id")
        lenses = item.get("lenses")
        if pid not in path_ids:
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_COMPARISON_PATH_UNKNOWN",
                    f"path_comparison[{index}].path_id does not reference a construction path",
                )
            )
        elif pid in compared_ids:
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_COMPARISON_PATH_DUPLICATE",
                    f"duplicate path comparison for {pid}",
                )
            )
        else:
            compared_ids.add(pid)
        if not isinstance(lenses, dict):
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_LENSES_INVALID",
                    f"path_comparison[{index}].lenses must be a mapping",
                )
            )
            continue
        missing_lenses = sorted(COMPARISON_LENSES - set(lenses))
        extra_lenses = sorted(set(lenses) - COMPARISON_LENSES)
        if missing_lenses:
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_LENSES_MISSING",
                    f"path_comparison[{index}] missing lenses: {', '.join(missing_lenses)}",
                )
            )
        if extra_lenses:
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_LENSES_UNKNOWN",
                    f"path_comparison[{index}] unknown lenses: {', '.join(extra_lenses)}",
                )
            )
        if _contains_number(lenses):
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_NUMERIC_SCORING_FORBIDDEN",
                    "path comparison lenses must be qualitative prose, not numeric scores",
                )
            )
        for key, value in lenses.items():
            if key in COMPARISON_LENSES and not _nonempty_string(value):
                errors.append(
                    _error(
                        "STRATEGIC_ANALYSIS_LENS_VALUE_INVALID",
                        f"path_comparison[{index}].lenses.{key} must be non-empty qualitative text",
                    )
                )

    if path_ids and compared_ids != path_ids:
        missing_comparisons = sorted(path_ids - compared_ids)
        if missing_comparisons:
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_COMPARISON_INCOMPLETE",
                    "Missing path comparison for: " + ", ".join(missing_comparisons),
                )
            )

    uncertainty = data.get("decision_changing_uncertainty")
    if not isinstance(uncertainty, dict):
        errors.append(
            _error(
                "STRATEGIC_ANALYSIS_UNCERTAINTY_INVALID",
                "decision_changing_uncertainty must be a mapping",
            )
        )
    else:
        for field in ("statement", "could_change", "evidence_needed"):
            if not _nonempty_string(uncertainty.get(field)):
                errors.append(
                    _error(
                        "STRATEGIC_ANALYSIS_UNCERTAINTY_FIELD_INVALID",
                        f"decision_changing_uncertainty.{field} must be non-empty",
                    )
                )
        if not isinstance(uncertainty.get("inquiry_warranted"), bool):
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_INQUIRY_FLAG_INVALID",
                    "decision_changing_uncertainty.inquiry_warranted must be boolean",
                )
            )
        if uncertainty.get("source") not in UNCERTAINTY_SOURCES:
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_UNCERTAINTY_SOURCE_INVALID",
                    f"decision_changing_uncertainty.source must be one of {sorted(UNCERTAINTY_SOURCES)}",
                )
            )

    analysis_ref = data.get("analysis_ref")
    if analysis_ref is not None and not _nonempty_string(analysis_ref):
        errors.append(
            _error(
                "STRATEGIC_ANALYSIS_REF_INVALID",
                "analysis_ref must be a non-empty string when present",
            )
        )

    continuity = data.get("continuity")
    if continuity is not None:
        if not isinstance(continuity, dict):
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_CONTINUITY_INVALID",
                    "continuity must be a mapping when present",
                )
            )
        else:
            prior_ref = continuity.get("prior_analysis_ref")
            if prior_ref is not None and not _nonempty_string(prior_ref):
                errors.append(
                    _error(
                        "STRATEGIC_ANALYSIS_PRIOR_REF_INVALID",
                        "continuity.prior_analysis_ref must be null or a non-empty string",
                    )
                )
            if continuity.get("disposition") not in CONTINUITY_DISPOSITIONS:
                errors.append(
                    _error(
                        "STRATEGIC_ANALYSIS_CONTINUITY_DISPOSITION_INVALID",
                        "continuity.disposition must be one of "
                        + ", ".join(sorted(CONTINUITY_DISPOSITIONS)),
                    )
                )
            if not _nonempty_string(continuity.get("reason")):
                errors.append(
                    _error(
                        "STRATEGIC_ANALYSIS_CONTINUITY_REASON_INVALID",
                        "continuity.reason must be non-empty",
                    )
                )
            prior_path = continuity.get("prior_selected_path_id")
            if prior_path is not None and not _nonempty_string(prior_path):
                errors.append(
                    _error(
                        "STRATEGIC_ANALYSIS_PRIOR_PATH_INVALID",
                        "continuity.prior_selected_path_id must be null or a non-empty string",
                    )
                )

    assumptions = data.get("decision_assumptions")
    if assumptions is not None:
        if not isinstance(assumptions, list):
            errors.append(
                _error(
                    "STRATEGIC_ANALYSIS_ASSUMPTIONS_INVALID",
                    "decision_assumptions must be a list when present",
                )
            )
        else:
            seen_assumptions: set[str] = set()
            for index, item in enumerate(assumptions):
                if not isinstance(item, dict):
                    errors.append(
                        _error(
                            "STRATEGIC_ANALYSIS_ASSUMPTION_ENTRY_INVALID",
                            f"decision_assumptions[{index}] must be a mapping",
                        )
                    )
                    continue
                assumption_id = item.get("assumption_id")
                if not _nonempty_string(assumption_id):
                    errors.append(
                        _error(
                            "STRATEGIC_ANALYSIS_ASSUMPTION_ID_INVALID",
                            f"decision_assumptions[{index}].assumption_id must be non-empty",
                        )
                    )
                elif assumption_id in seen_assumptions:
                    errors.append(
                        _error(
                            "STRATEGIC_ANALYSIS_ASSUMPTION_ID_DUPLICATE",
                            f"duplicate assumption_id: {assumption_id}",
                        )
                    )
                else:
                    seen_assumptions.add(assumption_id)
                if not _nonempty_string(item.get("statement")):
                    errors.append(
                        _error(
                            "STRATEGIC_ANALYSIS_ASSUMPTION_STATEMENT_INVALID",
                            f"decision_assumptions[{index}].statement must be non-empty",
                        )
                    )
                if not _string_list(item.get("evidence_refs")):
                    errors.append(
                        _error(
                            "STRATEGIC_ANALYSIS_ASSUMPTION_EVIDENCE_INVALID",
                            f"decision_assumptions[{index}].evidence_refs must be a list of non-empty strings",
                        )
                    )
                if not _string_list(item.get("reassessment_triggers")):
                    errors.append(
                        _error(
                            "STRATEGIC_ANALYSIS_REASSESSMENT_TRIGGERS_INVALID",
                            f"decision_assumptions[{index}].reassessment_triggers must be a list of non-empty strings",
                        )
                    )

    disposition = data.get("strategic_disposition")
    if disposition not in DISPOSITIONS:
        errors.append(
            _error(
                "STRATEGIC_ANALYSIS_DISPOSITION_INVALID",
                f"strategic_disposition must be one of {sorted(DISPOSITIONS)}",
            )
        )

    selected = data.get("selected_path_id")
    if selected is not None and selected not in path_ids:
        errors.append(
            _error(
                "STRATEGIC_ANALYSIS_SELECTED_PATH_UNKNOWN",
                "selected_path_id must be null or reference construction_paths",
            )
        )
    if disposition == "BUILD" and selected not in path_ids:
        errors.append(
            _error(
                "STRATEGIC_ANALYSIS_BUILD_PATH_REQUIRED",
                "BUILD requires selected_path_id to reference a construction path",
            )
        )
    if disposition == "BUILD" and not _nonempty_string(
        data.get("candidate_repository_responsibility")
    ):
        errors.append(
            _error(
                "STRATEGIC_ANALYSIS_BUILD_RESPONSIBILITY_REQUIRED",
                "BUILD requires candidate_repository_responsibility",
            )
        )

    if data.get("implementation_authority_established_by_artifact") is not False:
        errors.append(
            _error(
                "STRATEGIC_ANALYSIS_AUTHORITY_BOUNDARY_INVALID",
                "implementation_authority_established_by_artifact must be false",
            )
        )
    if data.get("semantic_truth_established") is not False:
        errors.append(
            _error(
                "STRATEGIC_ANALYSIS_SEMANTIC_AUTHORITY_INVALID",
                "semantic_truth_established must be false",
            )
        )
    if data.get("immutable") is not True:
        errors.append(
            _error(
                "STRATEGIC_ANALYSIS_IMMUTABILITY_INVALID",
                "immutable must be true",
            )
        )

    forbidden_score_keys = {"score", "scores", "weight", "weights", "total", "rank", "ranking"}
    stack: list[tuple[str, Any]] = [("", data)]
    while stack:
        prefix, value = stack.pop()
        if isinstance(value, dict):
            for key, child in value.items():
                key_lower = str(key).lower()
                child_path = f"{prefix}.{key}" if prefix else str(key)
                if key_lower in forbidden_score_keys:
                    errors.append(
                        _error(
                            "STRATEGIC_ANALYSIS_SCORING_FIELD_FORBIDDEN",
                            f"numeric/ranking field is forbidden: {child_path}",
                        )
                    )
                stack.append((child_path, child))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                stack.append((f"{prefix}[{index}]", child))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    errors = validate(args.artifact)
    result = {
        "valid": not errors,
        "artifact_id": "strategic_repository_analysis",
        "artifact_path": str(args.artifact),
        "errors": errors,
        "checks": [
            "required_machine_shape",
            "capability_state_vocabulary",
            "construction_path_integrity",
            "qualitative_comparison_integrity",
            "decision_changing_uncertainty_shape",
            "optional_continuity_and_assumption_integrity",
            "strategic_disposition_reference_integrity",
            "authority_and_semantic_claim_boundaries",
            "anti_numeric_scoring",
        ],
        "semantic_truth_established": False,
        "strategy_selected_by_validator": False,
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
        print("mechanical representation valid; strategic correctness not established")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())