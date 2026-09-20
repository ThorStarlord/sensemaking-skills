"""Mechanically validate change_impact_analysis artifacts.

Representation only: the validator does not decide material impact, authorize a
change, expand repository scope, execute follow-up work, or establish semantic truth.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


CHANGE_STATES = {"CONTEMPLATED", "IMPLEMENTED", "VERIFIED"}
IMPACT_CATEGORIES = {
    "code",
    "contract",
    "artifact",
    "test",
    "documentation",
    "claim",
    "decision",
    "authority",
    "repository_boundary",
    "release",
    "external_dependency",
}
CLOSURE_EFFECTS = {
    "NO_CLOSURE_EFFECT",
    "ADDITIONAL_VERIFICATION_REQUIRED",
    "RECONCILIATION_REQUIRED",
    "OWNER_DECISION_REQUIRED",
    "STRATEGIC_REASSESSMENT_REQUIRED",
    "THESIS_REVIEW_REQUIRED",
}
REQUIRED = {
    "artifact_id",
    "analysis_ref",
    "target_repository",
    "target_source_identity",
    "change",
    "impact_items",
    "cross_repository_impacts",
    "claim_consequences",
    "followup_responsibilities",
    "closure_effect",
    "automatic_repository_discovery_performed",
    "change_authorized_by_artifact",
    "followup_execution_authorized_by_artifact",
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


def _extract(content: str) -> dict[str, Any] | None:
    for block in reversed(re.findall(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)):
        try:
            value = yaml.safe_load(block)
        except yaml.YAMLError:
            continue
        if isinstance(value, dict) and value.get("artifact_id") == "change_impact_analysis":
            return value
    return None


def validate(path: Path) -> list[dict[str, str]]:
    try:
        content=path.read_text(encoding="utf-8")
    except OSError as exc:
        return [_error("CHANGE_IMPACT_FILE_UNREADABLE",str(exc))]
    data=_extract(content)
    if data is None:
        return [_error("CHANGE_IMPACT_MACHINE_BLOCK_MISSING","No change_impact_analysis YAML block found.")]

    errors:list[dict[str,str]]=[]
    missing=sorted(REQUIRED-set(data))
    if missing:
        errors.append(_error("CHANGE_IMPACT_FIELDS_MISSING",", ".join(missing)))

    for field in ("analysis_ref","target_repository","target_source_identity","created_at"):
        if not _text(data.get(field)):
            errors.append(_error("CHANGE_IMPACT_TEXT_INVALID",field))

    change=data.get("change")
    if not isinstance(change,dict):
        errors.append(_error("CHANGE_IMPACT_CHANGE_INVALID","change must be a mapping"))
    else:
        if not _text(change.get("change_id")) or not _text(change.get("statement")):
            errors.append(_error("CHANGE_IMPACT_CHANGE_TEXT_INVALID","change_id and statement must be non-empty"))
        if change.get("state") not in CHANGE_STATES:
            errors.append(_error("CHANGE_IMPACT_CHANGE_STATE_INVALID","invalid change.state"))
        if not _string_list(change.get("evidence_refs")):
            errors.append(_error("CHANGE_IMPACT_CHANGE_EVIDENCE_INVALID","change.evidence_refs must be non-empty string list"))

    impacts=data.get("impact_items")
    surface_ids:set[str]=set()
    if not isinstance(impacts,list):
        errors.append(_error("CHANGE_IMPACT_ITEMS_INVALID","impact_items must be a list"))
        impacts=[]
    for index,item in enumerate(impacts):
        if not isinstance(item,dict):
            errors.append(_error("CHANGE_IMPACT_ITEM_INVALID",f"impact_items[{index}] must be mapping"))
            continue
        sid=item.get("surface_id")
        if not _text(sid) or sid in surface_ids:
            errors.append(_error("CHANGE_IMPACT_SURFACE_ID_INVALID",f"impact_items[{index}].surface_id invalid/duplicate"))
        else:
            surface_ids.add(sid)
        if item.get("category") not in IMPACT_CATEGORIES:
            errors.append(_error("CHANGE_IMPACT_CATEGORY_INVALID",f"impact_items[{index}].category"))
        for field in ("target_ref","impact_statement","authority_boundary"):
            if not _text(item.get(field)):
                errors.append(_error("CHANGE_IMPACT_ITEM_TEXT_INVALID",f"impact_items[{index}].{field}"))
        if not _string_list(item.get("evidence_refs")):
            errors.append(_error("CHANGE_IMPACT_ITEM_EVIDENCE_INVALID",f"impact_items[{index}].evidence_refs"))
        if not isinstance(item.get("semantic_review_required"),bool):
            errors.append(_error("CHANGE_IMPACT_REVIEW_FLAG_INVALID",f"impact_items[{index}].semantic_review_required"))
        if not _string_list(item.get("required_actions"),allow_empty=True):
            errors.append(_error("CHANGE_IMPACT_REQUIRED_ACTIONS_INVALID",f"impact_items[{index}].required_actions"))

    cross=data.get("cross_repository_impacts")
    if not isinstance(cross,list):
        errors.append(_error("CHANGE_IMPACT_CROSS_REPO_INVALID","cross_repository_impacts must be a list"))
    else:
        for index,item in enumerate(cross):
            if not isinstance(item,dict):
                errors.append(_error("CHANGE_IMPACT_CROSS_REPO_ENTRY_INVALID",f"cross_repository_impacts[{index}]"))
                continue
            for field in ("repository_alias","repository","impact_statement"):
                if not _text(item.get(field)):
                    errors.append(_error("CHANGE_IMPACT_CROSS_REPO_TEXT_INVALID",f"cross_repository_impacts[{index}].{field}"))
            if not _string_list(item.get("evidence_refs")):
                errors.append(_error("CHANGE_IMPACT_CROSS_REPO_EVIDENCE_INVALID",f"cross_repository_impacts[{index}].evidence_refs"))

    consequences=data.get("claim_consequences")
    if not isinstance(consequences,list):
        errors.append(_error("CHANGE_IMPACT_CLAIM_CONSEQUENCES_INVALID","claim_consequences must be a list"))
    else:
        for index,item in enumerate(consequences):
            if not isinstance(item,dict) or not _text(item.get("claim_ref")) or not _text(item.get("effect")):
                errors.append(_error("CHANGE_IMPACT_CLAIM_CONSEQUENCE_INVALID",f"claim_consequences[{index}] requires claim_ref and effect"))

    followups=data.get("followup_responsibilities")
    followup_ids:set[str]=set()
    if not isinstance(followups,list):
        errors.append(_error("CHANGE_IMPACT_FOLLOWUPS_INVALID","followup_responsibilities must be a list"))
    else:
        for index,item in enumerate(followups):
            if not isinstance(item,dict):
                errors.append(_error("CHANGE_IMPACT_FOLLOWUP_INVALID",f"followup_responsibilities[{index}]"))
                continue
            rid=item.get("responsibility_id")
            if not _text(rid) or rid in followup_ids or not _text(item.get("statement")):
                errors.append(_error("CHANGE_IMPACT_FOLLOWUP_ID_INVALID",f"followup_responsibilities[{index}] invalid/duplicate"))
            else:
                followup_ids.add(rid)
            affected=item.get("affected_surface_ids")
            if not _string_list(affected) or any(sid not in surface_ids for sid in affected):
                errors.append(_error("CHANGE_IMPACT_FOLLOWUP_SURFACES_INVALID",f"followup_responsibilities[{index}].affected_surface_ids"))

    if data.get("closure_effect") not in CLOSURE_EFFECTS:
        errors.append(_error("CHANGE_IMPACT_CLOSURE_EFFECT_INVALID","invalid closure_effect"))

    for field in (
        "automatic_repository_discovery_performed",
        "change_authorized_by_artifact",
        "followup_execution_authorized_by_artifact",
        "semantic_truth_established",
    ):
        if data.get(field) is not False:
            errors.append(_error("CHANGE_IMPACT_BOUNDARY_INVALID",f"{field} must be false"))
    if data.get("immutable") is not True:
        errors.append(_error("CHANGE_IMPACT_IMMUTABILITY_INVALID","immutable must be true"))

    forbidden={"score","scores","weight","weights","rank","ranking","severity_score","risk_score"}
    stack:[tuple[str,Any]]=[("",data)]
    while stack:
        prefix,value=stack.pop()
        if isinstance(value,dict):
            for key,child in value.items():
                child_path=f"{prefix}.{key}" if prefix else str(key)
                if str(key).lower() in forbidden:
                    errors.append(_error("CHANGE_IMPACT_SCORING_FIELD_FORBIDDEN",child_path))
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
        "artifact_id":"change_impact_analysis",
        "artifact_path":str(args.artifact),
        "errors":errors,
        "automatic_repository_discovery_performed":False,
        "material_impact_selected_by_validator":False,
        "change_authorized_by_validator":False,
        "followup_execution_authorized_by_validator":False,
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
        print("mechanical representation valid; impact materiality and authorization remain semantic/external")
    return 1 if errors else 0


if __name__=="__main__":
    sys.exit(main())
