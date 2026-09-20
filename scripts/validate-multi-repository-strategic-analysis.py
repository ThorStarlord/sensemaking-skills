"""Mechanically validate Multi-Repository Strategic Analysis artifacts.

The validator checks only bounded representation, explicit target references,
qualitative comparison shape, and protected authority flags. It does not discover
repositories, infer architecture, rank paths, select work, or authorize mutation.
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
RELATION_TYPES = {
    "depends_on",
    "provides_interface_to",
    "consumes_interface_from",
    "must_change_with",
    "release_after",
}
UNCERTAINTY_SOURCES = {
    "repository_evidence",
    "empirical",
    "owner_intent",
    "external_environment",
    "none",
}
LENSES = {
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

REQUIRED = {
    "artifact_id",
    "analysis_ref",
    "governing_intent",
    "target_repositories",
    "explicit_relations",
    "capability_ownership",
    "boundary_tensions",
    "construction_paths",
    "path_comparison",
    "decision_changing_uncertainty",
    "strategic_disposition",
    "selected_path_id",
    "candidate_repository_responsibility",
    "affected_target_aliases",
    "automatic_repository_discovery_performed",
    "target_scope_expanded_by_artifact",
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


def _extract(content: str) -> dict[str, Any] | None:
    for block in reversed(re.findall(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)):
        try:
            value = yaml.safe_load(block)
        except yaml.YAMLError:
            continue
        if isinstance(value, dict) and value.get("artifact_id") == "multi_repository_strategic_analysis":
            return value
    return None


def validate(path: Path) -> list[dict[str, str]]:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [_error("MULTI_REPO_ANALYSIS_FILE_UNREADABLE", str(exc))]
    data = _extract(content)
    if data is None:
        return [_error("MULTI_REPO_ANALYSIS_MACHINE_BLOCK_MISSING", "No multi_repository_strategic_analysis YAML block found.")]

    errors: list[dict[str, str]] = []
    missing = sorted(REQUIRED - set(data))
    if missing:
        errors.append(_error("MULTI_REPO_ANALYSIS_FIELDS_MISSING", ", ".join(missing)))

    if data.get("artifact_id") != "multi_repository_strategic_analysis":
        errors.append(_error("MULTI_REPO_ANALYSIS_ARTIFACT_ID_INVALID", "artifact_id must be multi_repository_strategic_analysis"))
    for field in ("analysis_ref", "governing_intent", "created_at"):
        if not _text(data.get(field)):
            errors.append(_error("MULTI_REPO_ANALYSIS_TEXT_INVALID", field))

    targets = data.get("target_repositories")
    aliases: set[str] = set()
    repositories: set[str] = set()
    if not isinstance(targets, list) or len(targets) < 2:
        errors.append(_error("MULTI_REPO_ANALYSIS_TARGETS_INVALID", "target_repositories must contain at least two explicitly selected targets"))
        targets = []
    for index, item in enumerate(targets):
        if not isinstance(item, dict):
            errors.append(_error("MULTI_REPO_ANALYSIS_TARGET_INVALID", f"target_repositories[{index}] must be a mapping"))
            continue
        alias=item.get("alias")
        repository=item.get("repository")
        if not all(_text(item.get(field)) for field in ("alias","repository","source_identity","role")):
            errors.append(_error("MULTI_REPO_ANALYSIS_TARGET_INVALID", f"target_repositories[{index}] requires alias, repository, source_identity, role"))
        if _text(alias):
            if alias in aliases:
                errors.append(_error("MULTI_REPO_ANALYSIS_TARGET_ALIAS_DUPLICATE", alias))
            aliases.add(alias)
        if _text(repository):
            if repository in repositories:
                errors.append(_error("MULTI_REPO_ANALYSIS_REPOSITORY_DUPLICATE", repository))
            repositories.add(repository)
        if not _string_list(item.get("evidence_refs")):
            errors.append(_error("MULTI_REPO_ANALYSIS_TARGET_EVIDENCE_INVALID", f"target_repositories[{index}].evidence_refs"))

    relations=data.get("explicit_relations")
    relation_ids:set[str]=set()
    if not isinstance(relations,list):
        errors.append(_error("MULTI_REPO_ANALYSIS_RELATIONS_INVALID","explicit_relations must be a list"))
        relations=[]
    for index,item in enumerate(relations):
        if not isinstance(item,dict):
            errors.append(_error("MULTI_REPO_ANALYSIS_RELATION_INVALID",f"explicit_relations[{index}] must be a mapping"))
            continue
        rid=item.get("relation_id")
        source=item.get("source_alias")
        target=item.get("target_alias")
        rtype=item.get("relation_type")
        if not _text(rid) or rid in relation_ids:
            errors.append(_error("MULTI_REPO_ANALYSIS_RELATION_ID_INVALID",f"explicit_relations[{index}].relation_id invalid/duplicate"))
        else:
            relation_ids.add(rid)
        if source not in aliases or target not in aliases or source==target:
            errors.append(_error("MULTI_REPO_ANALYSIS_RELATION_ALIAS_INVALID",f"explicit_relations[{index}] aliases must reference different selected targets"))
        if rtype not in RELATION_TYPES:
            errors.append(_error("MULTI_REPO_ANALYSIS_RELATION_TYPE_INVALID",f"explicit_relations[{index}].relation_type"))
        if not _string_list(item.get("evidence_refs")):
            errors.append(_error("MULTI_REPO_ANALYSIS_RELATION_EVIDENCE_INVALID",f"explicit_relations[{index}].evidence_refs"))

    capabilities=data.get("capability_ownership")
    capability_ids:set[str]=set()
    if not isinstance(capabilities,list):
        errors.append(_error("MULTI_REPO_ANALYSIS_CAPABILITIES_INVALID","capability_ownership must be a list"))
        capabilities=[]
    for index,item in enumerate(capabilities):
        if not isinstance(item,dict):
            errors.append(_error("MULTI_REPO_ANALYSIS_CAPABILITY_INVALID",f"capability_ownership[{index}] must be a mapping"))
            continue
        cid=item.get("capability_id")
        if not _text(cid) or cid in capability_ids:
            errors.append(_error("MULTI_REPO_ANALYSIS_CAPABILITY_ID_INVALID",f"capability_ownership[{index}].capability_id invalid/duplicate"))
        else:
            capability_ids.add(cid)
        owners=item.get("current_owner_aliases")
        if not _string_list(owners) or any(alias not in aliases for alias in owners):
            errors.append(_error("MULTI_REPO_ANALYSIS_CAPABILITY_OWNER_INVALID",f"capability_ownership[{index}].current_owner_aliases"))
        if item.get("state") not in CAPABILITY_STATES:
            errors.append(_error("MULTI_REPO_ANALYSIS_CAPABILITY_STATE_INVALID",f"capability_ownership[{index}].state"))
        if not _string_list(item.get("evidence_refs")):
            errors.append(_error("MULTI_REPO_ANALYSIS_CAPABILITY_EVIDENCE_INVALID",f"capability_ownership[{index}].evidence_refs"))
        if not _text(item.get("boundary_consequence")):
            errors.append(_error("MULTI_REPO_ANALYSIS_CAPABILITY_BOUNDARY_INVALID",f"capability_ownership[{index}].boundary_consequence"))

    tensions=data.get("boundary_tensions")
    tension_ids:set[str]=set()
    if not isinstance(tensions,list):
        errors.append(_error("MULTI_REPO_ANALYSIS_TENSIONS_INVALID","boundary_tensions must be a list"))
        tensions=[]
    for index,item in enumerate(tensions):
        if not isinstance(item,dict) or not _text(item.get("tension_id")) or not _text(item.get("statement")):
            errors.append(_error("MULTI_REPO_ANALYSIS_TENSION_INVALID",f"boundary_tensions[{index}] requires tension_id and statement"))
            continue
        if item["tension_id"] in tension_ids:
            errors.append(_error("MULTI_REPO_ANALYSIS_TENSION_DUPLICATE",item["tension_id"]))
        tension_ids.add(item["tension_id"])

    paths=data.get("construction_paths")
    path_ids:set[str]=set()
    if not isinstance(paths,list) or len(paths)>5:
        errors.append(_error("MULTI_REPO_ANALYSIS_PATHS_INVALID","construction_paths must be a list with at most five paths"))
        paths=[]
    for index,item in enumerate(paths):
        if not isinstance(item,dict):
            errors.append(_error("MULTI_REPO_ANALYSIS_PATH_INVALID",f"construction_paths[{index}] must be a mapping"))
            continue
        pid=item.get("path_id")
        if not _text(pid) or pid in path_ids:
            errors.append(_error("MULTI_REPO_ANALYSIS_PATH_ID_INVALID",f"construction_paths[{index}].path_id invalid/duplicate"))
        else:
            path_ids.add(pid)
        for field in ("name","future_state","reversibility"):
            if not _text(item.get(field)):
                errors.append(_error("MULTI_REPO_ANALYSIS_PATH_TEXT_INVALID",f"construction_paths[{index}].{field}"))
        for field in ("boundary_changes","construction_sequence","dependencies","unlocks","risks","evidence_gaps"):
            if not _string_list(item.get(field),allow_empty=True):
                errors.append(_error("MULTI_REPO_ANALYSIS_PATH_LIST_INVALID",f"construction_paths[{index}].{field}"))
        allocations=item.get("capability_allocations")
        if not isinstance(allocations,list):
            errors.append(_error("MULTI_REPO_ANALYSIS_ALLOCATIONS_INVALID",f"construction_paths[{index}].capability_allocations"))
            allocations=[]
        for allocation in allocations:
            if not isinstance(allocation,dict):
                errors.append(_error("MULTI_REPO_ANALYSIS_ALLOCATION_INVALID",f"construction_paths[{index}] allocation must be mapping"))
                continue
            if allocation.get("capability_id") not in capability_ids:
                errors.append(_error("MULTI_REPO_ANALYSIS_ALLOCATION_CAPABILITY_UNKNOWN",str(allocation.get("capability_id"))))
            owners=allocation.get("proposed_owner_aliases")
            if not _string_list(owners) or any(alias not in aliases for alias in owners):
                errors.append(_error("MULTI_REPO_ANALYSIS_ALLOCATION_OWNER_INVALID",str(owners)))
            if not _text(allocation.get("boundary_pattern")):
                errors.append(_error("MULTI_REPO_ANALYSIS_ALLOCATION_PATTERN_INVALID","boundary_pattern must be qualitative text"))

    comparisons=data.get("path_comparison")
    compared:set[str]=set()
    if not isinstance(comparisons,list):
        errors.append(_error("MULTI_REPO_ANALYSIS_COMPARISON_INVALID","path_comparison must be a list"))
        comparisons=[]
    for index,item in enumerate(comparisons):
        if not isinstance(item,dict) or item.get("path_id") not in path_ids or not isinstance(item.get("lenses"),dict):
            errors.append(_error("MULTI_REPO_ANALYSIS_COMPARISON_ENTRY_INVALID",f"path_comparison[{index}]"))
            continue
        pid=item["path_id"]
        if pid in compared:
            errors.append(_error("MULTI_REPO_ANALYSIS_COMPARISON_DUPLICATE",pid))
        compared.add(pid)
        lenses=item["lenses"]
        missing_lenses=sorted(LENSES-set(lenses))
        extra_lenses=sorted(set(lenses)-LENSES)
        if missing_lenses or extra_lenses:
            errors.append(_error("MULTI_REPO_ANALYSIS_LENSES_INVALID",f"missing={missing_lenses}, extra={extra_lenses}"))
        if _contains_number(lenses):
            errors.append(_error("MULTI_REPO_ANALYSIS_NUMERIC_SCORING_FORBIDDEN","comparison lenses must be qualitative prose"))
        for key,value in lenses.items():
            if key in LENSES and not _text(value):
                errors.append(_error("MULTI_REPO_ANALYSIS_LENS_TEXT_INVALID",f"{pid}.{key}"))
    if compared != path_ids:
        errors.append(_error("MULTI_REPO_ANALYSIS_COMPARISON_INCOMPLETE","every declared path must have exactly one comparison"))

    uncertainty=data.get("decision_changing_uncertainty")
    if not isinstance(uncertainty,dict):
        errors.append(_error("MULTI_REPO_ANALYSIS_UNCERTAINTY_INVALID","decision_changing_uncertainty must be mapping"))
    else:
        for field in ("statement","could_change","evidence_needed"):
            if not _text(uncertainty.get(field)):
                errors.append(_error("MULTI_REPO_ANALYSIS_UNCERTAINTY_TEXT_INVALID",field))
        if not isinstance(uncertainty.get("inquiry_warranted"),bool):
            errors.append(_error("MULTI_REPO_ANALYSIS_INQUIRY_FLAG_INVALID","inquiry_warranted must be boolean"))
        if uncertainty.get("source") not in UNCERTAINTY_SOURCES:
            errors.append(_error("MULTI_REPO_ANALYSIS_UNCERTAINTY_SOURCE_INVALID","invalid source"))

    disposition=data.get("strategic_disposition")
    if disposition not in DISPOSITIONS:
        errors.append(_error("MULTI_REPO_ANALYSIS_DISPOSITION_INVALID","invalid strategic_disposition"))
    selected=data.get("selected_path_id")
    if selected is not None and selected not in path_ids:
        errors.append(_error("MULTI_REPO_ANALYSIS_SELECTED_PATH_UNKNOWN","selected_path_id must be null or reference a path"))
    if disposition=="BUILD" and selected not in path_ids:
        errors.append(_error("MULTI_REPO_ANALYSIS_BUILD_PATH_REQUIRED","BUILD requires selected_path_id"))
    if disposition=="BUILD" and not _text(data.get("candidate_repository_responsibility")):
        errors.append(_error("MULTI_REPO_ANALYSIS_BUILD_RESPONSIBILITY_REQUIRED","BUILD requires candidate_repository_responsibility"))
    affected=data.get("affected_target_aliases")
    if not isinstance(affected,list) or any(alias not in aliases for alias in affected):
        errors.append(_error("MULTI_REPO_ANALYSIS_AFFECTED_TARGETS_INVALID","affected_target_aliases must reference selected targets"))
    if disposition=="BUILD" and not affected:
        errors.append(_error("MULTI_REPO_ANALYSIS_BUILD_TARGETS_REQUIRED","BUILD requires affected_target_aliases"))

    for field in (
        "automatic_repository_discovery_performed",
        "target_scope_expanded_by_artifact",
        "implementation_authority_established_by_artifact",
        "semantic_truth_established",
    ):
        if data.get(field) is not False:
            errors.append(_error("MULTI_REPO_ANALYSIS_BOUNDARY_INVALID",f"{field} must be false"))
    if data.get("immutable") is not True:
        errors.append(_error("MULTI_REPO_ANALYSIS_IMMUTABILITY_INVALID","immutable must be true"))

    forbidden={"score","scores","weight","weights","rank","ranking","total"}
    stack:[tuple[str,Any]]=[("",data)]
    while stack:
        prefix,value=stack.pop()
        if isinstance(value,dict):
            for key,child in value.items():
                child_path=f"{prefix}.{key}" if prefix else str(key)
                if str(key).lower() in forbidden:
                    errors.append(_error("MULTI_REPO_ANALYSIS_SCORING_FIELD_FORBIDDEN",child_path))
                stack.append((child_path,child))
        elif isinstance(value,list):
            for index,child in enumerate(value):
                stack.append((f"{prefix}[{index}]",child))
    return errors


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact",type=Path)
    parser.add_argument("--json",action="store_true")
    args=parser.parse_args()
    errors=validate(args.artifact)
    result={
        "valid":not errors,
        "artifact_id":"multi_repository_strategic_analysis",
        "artifact_path":str(args.artifact),
        "errors":errors,
        "automatic_repository_discovery_performed":False,
        "target_scope_expanded_by_validator":False,
        "strategy_selected_by_validator":False,
        "implementation_authorized_by_validator":False,
        "semantic_truth_established":False,
    }
    if args.json:
        print(json.dumps(result,indent=2,sort_keys=True))
    elif errors:
        print("FAIL")
        for item in errors:
            print(f"{item['error_id']}: {item['message']}")
    else:
        print("PASS")
        print("mechanical representation valid; repository scope and strategic correctness remain semantic/caller-owned")
    return 1 if errors else 0


if __name__=="__main__":
    sys.exit(main())
