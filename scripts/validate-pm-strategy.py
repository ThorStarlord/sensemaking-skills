#!/usr/bin/env python3
"""Deterministic validator for PM strategy/prioritization artifacts.

Checks representation, evidence status, identity, references, and declared arithmetic.
It never decides which market claim, strategy, priority, metric, OKR, roadmap, or
business model is semantically best.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

VALIDATOR = "validate-pm-strategy.py"
SUPPORTED = {
    "market_analysis",
    "strategy_doc",
    "prioritized_list",
    "north_star_metric",
    "okr_list",
    "roadmap",
    "business_canvas",
}
HANDOFF_RE = re.compile(
    r"^##\s+(?:\d+\.\s*)?Machine-readable handoff\s*$\s*```yaml\s*(.*?)\s*```",
    re.MULTILINE | re.IGNORECASE | re.DOTALL,
)
SECTIONS = {
    "market_analysis": ("Scope and evidence cutoff", "Competitors and sources", "Comparison", "Strengths weaknesses gaps and threats", "Positioning options", "Recommendations and uncertainties"),
    "strategy_doc": ("Vision and context", "Target segments and non-targets", "Problems and evidence", "Strategic choices and non-choices", "Differentiation and business model", "Measures and roadmap themes", "Risks dependencies and open decisions"),
    "prioritized_list": ("Decision context", "Candidate evidence and scoring", "Recommended order and trade-offs", "Dependencies and validation needs", "Deferred items"),
    "north_star_metric": ("Value model and evidence", "Candidate metrics", "Candidate assessment", "Proposed North Star", "Input metrics and guardrails", "Measurement gaps and review cadence"),
    "okr_list": ("Strategy and cycle", "Objectives and key results", "Alignment", "Supporting initiatives", "Review cadence", "Uncertainties"),
    "roadmap": ("Goals and planning assumptions", "Themes and initiatives", "Dependencies and sequence", "Milestones and outcomes", "Capacity and contingency", "Review triggers and uncertainties"),
    "business_canvas": ("Canvas", "Evidence and assumptions", "Critical hypotheses", "Validation order", "Unknowns and limitations"),
}


def err(code: str, field: str, message: str, value: Any = None) -> dict[str, Any]:
    return {"error_id": code, "error_type": "contract_error", "field": field, "current_value": value, "message": message, "suggested_fixes": [], "reference": "docs/product-management/artifact-contracts.md"}


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def string_list(value: Any, nonempty: bool = False) -> bool:
    return isinstance(value, list) and (not nonempty or bool(value)) and all(text(x) for x in value)


def require(data: dict[str, Any], fields: tuple[str, ...], errors: list[dict[str, Any]]) -> None:
    for field in fields:
        if field not in data:
            errors.append(err("PM_MISSING_FIELD", field, f"required field {field!r} is missing"))


def unique(items: Any, field: str, errors: list[dict[str, Any]], nested: str = "id") -> list[str]:
    if not isinstance(items, list):
        errors.append(err("PM_LIST_REQUIRED", field, f"{field} must be a list", items)); return []
    ids: list[str] = []
    for i, item in enumerate(items):
        if not isinstance(item, dict) or not text(item.get(nested)):
            errors.append(err("PM_ID_REQUIRED", f"{field}[{i}].{nested}", "non-empty id required", None if not isinstance(item, dict) else item.get(nested)))
        else:
            ids.append(item[nested].strip())
    if len(ids) != len(set(ids)):
        errors.append(err("PM_DUPLICATE_ID", field, f"{field} contains duplicate ids", ids))
    return ids


def observed_requires_evidence(status: Any, refs: Any, field: str, errors: list[dict[str, Any]]) -> None:
    if status == "observed" and not string_list(refs, nonempty=True):
        errors.append(err("PM_EVIDENCE_REQUIRED", field, "observed claim requires evidence_refs", refs))


def validate_market(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    require(data, ("schema_version", "evidence_cutoff", "product", "segment", "competitors", "gaps", "positioning_options", "recommendations", "unresolved_questions"), errors)
    if not text(data.get("evidence_cutoff")): errors.append(err("PM_TEXT_REQUIRED", "evidence_cutoff", "evidence_cutoff must be non-empty"))
    ids = unique(data.get("competitors"), "competitors", errors)
    del ids
    for i, comp in enumerate(data.get("competitors") or []):
        if not isinstance(comp, dict): continue
        if not text(comp.get("name")): errors.append(err("PM_TEXT_REQUIRED", f"competitors[{i}].name", "competitor name required"))
        claims = comp.get("claims")
        if not isinstance(claims, list): errors.append(err("PM_LIST_REQUIRED", f"competitors[{i}].claims", "claims must be a list")); continue
        for j, claim in enumerate(claims):
            if not isinstance(claim, dict): errors.append(err("PM_MAPPING_REQUIRED", f"competitors[{i}].claims[{j}]", "claim must be a mapping")); continue
            status = claim.get("evidence_status")
            if status not in {"observed", "inferred", "unknown"}: errors.append(err("PM_INVALID_EVIDENCE_STATUS", f"competitors[{i}].claims[{j}].evidence_status", "invalid evidence status", status))
            observed_requires_evidence(status, claim.get("source_refs"), f"competitors[{i}].claims[{j}].source_refs", errors)


def validate_strategy(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    require(data, ("schema_version", "status", "vision", "target_segments", "non_targets", "problem_refs", "choices", "non_choices", "differentiation_hypotheses", "monetization_hypotheses", "measures", "roadmap_themes", "risks", "assumptions", "unresolved_questions"), errors)
    if data.get("status") != "proposed": errors.append(err("PM_INVALID_STATUS", "status", "strategy_doc status must be proposed", data.get("status")))
    unique(data.get("choices"), "choices", errors)
    for i, measure in enumerate(data.get("measures") or []):
        if not isinstance(measure, dict): continue
        status = measure.get("evidence_status")
        if status not in {"observed", "proposed", "unknown"}: errors.append(err("PM_INVALID_EVIDENCE_STATUS", f"measures[{i}].evidence_status", "invalid evidence status", status))
        observed_requires_evidence(status, measure.get("evidence_refs"), f"measures[{i}].evidence_refs", errors)


def number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def validate_priorities(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    require(data, ("schema_version", "scoring_method", "goal_refs", "items", "recommended_order", "unresolved_questions"), errors)
    if data.get("scoring_method") not in {"rice", "qualitative", "mixed"}: errors.append(err("PM_INVALID_METHOD", "scoring_method", "invalid scoring_method", data.get("scoring_method")))
    ids = unique(data.get("items"), "items", errors)
    for i, item in enumerate(data.get("items") or []):
        if not isinstance(item, dict): continue
        if item.get("decision") not in {"now", "next", "later", "validate_first"}: errors.append(err("PM_INVALID_DECISION", f"items[{i}].decision", "invalid decision", item.get("decision")))
        if not text(item.get("rationale")): errors.append(err("PM_TEXT_REQUIRED", f"items[{i}].rationale", "rationale required"))
        values = [item.get(k) for k in ("reach", "impact", "confidence", "effort")]
        if all(number(v) for v in values):
            reach, impact, confidence, effort = (float(v) for v in values)
            if effort <= 0: errors.append(err("PM_INVALID_EFFORT", f"items[{i}].effort", "effort must be positive", effort))
            else:
                expected = reach * impact * confidence / effort
                if not number(item.get("score")) or not math.isclose(float(item["score"]), expected, rel_tol=1e-6, abs_tol=1e-6):
                    errors.append(err("PM_SCORE_MISMATCH", f"items[{i}].score", f"score must equal declared RICE inputs ({expected})", item.get("score")))
        elif item.get("score") is not None:
            errors.append(err("PM_SCORE_WITHOUT_INPUTS", f"items[{i}].score", "score must be null when complete numeric inputs are unavailable", item.get("score")))
    order = data.get("recommended_order")
    if not string_list(order): errors.append(err("PM_LIST_REQUIRED", "recommended_order", "recommended_order must be a list of ids", order))
    elif any(x not in ids for x in order): errors.append(err("PM_UNKNOWN_REF", "recommended_order", "recommended_order references unknown item", order))


def validate_north_star(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    require(data, ("schema_version", "status", "business_game", "candidates", "selected_candidate_id", "baseline", "targets", "input_metrics", "guardrails", "unresolved_questions"), errors)
    if data.get("status") != "proposed": errors.append(err("PM_INVALID_STATUS", "status", "north_star_metric status must be proposed", data.get("status")))
    if data.get("business_game") not in {"attention", "transaction", "productivity", "other"}: errors.append(err("PM_INVALID_GAME", "business_game", "invalid business_game", data.get("business_game")))
    ids = unique(data.get("candidates"), "candidates", errors)
    if data.get("selected_candidate_id") not in ids: errors.append(err("PM_UNKNOWN_REF", "selected_candidate_id", "selected_candidate_id must reference a candidate", data.get("selected_candidate_id")))
    baseline = data.get("baseline")
    if not isinstance(baseline, dict): errors.append(err("PM_MAPPING_REQUIRED", "baseline", "baseline must be a mapping", baseline))
    else:
        status = baseline.get("evidence_status")
        if status not in {"unknown", "observed", "proposed"}: errors.append(err("PM_INVALID_EVIDENCE_STATUS", "baseline.evidence_status", "invalid baseline status", status))
        observed_requires_evidence(status, baseline.get("evidence_refs"), "baseline.evidence_refs", errors)


def validate_okr(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    require(data, ("schema_version", "status", "cycle", "strategy_refs", "objectives", "review_cadence", "unresolved_questions"), errors)
    if data.get("status") != "proposed": errors.append(err("PM_INVALID_STATUS", "status", "okr_list status must be proposed", data.get("status")))
    unique(data.get("objectives"), "objectives", errors)
    kr_ids: list[str] = []
    for i, obj in enumerate(data.get("objectives") or []):
        if not isinstance(obj, dict): continue
        if not text(obj.get("statement")) or not text(obj.get("owner_role")): errors.append(err("PM_TEXT_REQUIRED", f"objectives[{i}]", "objective statement and owner_role are required"))
        krs = obj.get("key_results")
        local = unique(krs, f"objectives[{i}].key_results", errors)
        kr_ids.extend(local)
        for j, kr in enumerate(krs or []):
            if not isinstance(kr, dict): continue
            if kr.get("result_type") != "outcome": errors.append(err("PM_OUTPUT_NOT_OUTCOME", f"objectives[{i}].key_results[{j}].result_type", "key result must describe an outcome", kr.get("result_type")))
            if kr.get("target_status") != "proposed": errors.append(err("PM_INVALID_STATUS", f"objectives[{i}].key_results[{j}].target_status", "target_status must be proposed", kr.get("target_status")))
            observed_requires_evidence(kr.get("baseline_status"), kr.get("baseline_evidence_refs"), f"objectives[{i}].key_results[{j}].baseline_evidence_refs", errors)
    if len(kr_ids) != len(set(kr_ids)): errors.append(err("PM_DUPLICATE_ID", "key_results", "key result ids must be globally unique", kr_ids))


def validate_roadmap(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    require(data, ("schema_version", "status", "period", "goal_refs", "initiatives", "milestones", "capacity_assumptions", "review_triggers", "unresolved_questions"), errors)
    if data.get("status") != "proposed": errors.append(err("PM_INVALID_STATUS", "status", "roadmap status must be proposed", data.get("status")))
    ids = unique(data.get("initiatives"), "initiatives", errors)
    for i, item in enumerate(data.get("initiatives") or []):
        if not isinstance(item, dict): continue
        timing_status = item.get("timing_status")
        if timing_status not in {"unknown", "estimate", "committed"}: errors.append(err("PM_INVALID_STATUS", f"initiatives[{i}].timing_status", "invalid timing_status", timing_status))
        if timing_status == "committed" and not text(item.get("authority_ref")): errors.append(err("PM_AUTHORITY_REQUIRED", f"initiatives[{i}].authority_ref", "committed timing requires authority_ref", item.get("authority_ref")))
        deps = item.get("dependencies", [])
        if not isinstance(deps, list): errors.append(err("PM_LIST_REQUIRED", f"initiatives[{i}].dependencies", "dependencies must be a list", deps))
        elif any(text(dep) and dep.startswith("INIT-") and dep not in ids for dep in deps): errors.append(err("PM_UNKNOWN_REF", f"initiatives[{i}].dependencies", "initiative dependency references unknown initiative", deps))


def validate_canvas(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    require(data, ("schema_version", "status", "blocks", "critical_hypotheses", "unresolved_questions"), errors)
    if data.get("status") != "hypothesis": errors.append(err("PM_INVALID_STATUS", "status", "business_canvas status must be hypothesis", data.get("status")))
    blocks = data.get("blocks")
    required = {"problem", "solution", "unique_value_proposition", "unfair_advantage", "customer_segments", "channels", "revenue_streams", "cost_structure", "key_metrics"}
    if not isinstance(blocks, dict): errors.append(err("PM_MAPPING_REQUIRED", "blocks", "blocks must be a mapping", blocks)); return
    missing = required - set(blocks)
    if missing: errors.append(err("PM_MISSING_FIELD", "blocks", f"missing Lean Canvas blocks: {sorted(missing)}"))
    for name in required & set(blocks):
        block = blocks[name]
        if not isinstance(block, dict): errors.append(err("PM_MAPPING_REQUIRED", f"blocks.{name}", "block must be a mapping", block)); continue
        status = block.get("evidence_status")
        if status not in {"observed", "inferred", "hypothesis", "unknown"}: errors.append(err("PM_INVALID_EVIDENCE_STATUS", f"blocks.{name}.evidence_status", "invalid evidence status", status))
        observed_requires_evidence(status, block.get("evidence_refs"), f"blocks.{name}.evidence_refs", errors)
    unique(data.get("critical_hypotheses"), "critical_hypotheses", errors)


VALIDATORS = {
    "market_analysis": validate_market,
    "strategy_doc": validate_strategy,
    "prioritized_list": validate_priorities,
    "north_star_metric": validate_north_star,
    "okr_list": validate_okr,
    "roadmap": validate_roadmap,
    "business_canvas": validate_canvas,
}


def validate(path: Path) -> tuple[str, list[dict[str, Any]]]:
    if not path.is_file(): return "unknown", [err("PM_ARTIFACT_NOT_FOUND", "artifact", f"artifact not found: {path}")]
    content = path.read_text(encoding="utf-8")
    blocks = HANDOFF_RE.findall(content)
    if len(blocks) != 1: return "unknown", [err("PM_HANDOFF_BLOCK_COUNT", "machine_readable_handoff", "expected exactly one machine-readable handoff YAML block", len(blocks))]
    try: data = yaml.safe_load(blocks[0])
    except yaml.YAMLError as exc: return "unknown", [err("PM_INVALID_YAML", "machine_readable_handoff", f"invalid YAML: {exc}")]
    if not isinstance(data, dict): return "unknown", [err("PM_INVALID_YAML_SHAPE", "machine_readable_handoff", "handoff must be a mapping", data)]
    artifact_id = data.get("artifact_id")
    if artifact_id not in SUPPORTED: return str(artifact_id or "unknown"), [err("PM_UNSUPPORTED_ARTIFACT", "artifact_id", "unsupported PM strategy artifact", artifact_id)]
    errors: list[dict[str, Any]] = []
    for section in SECTIONS[artifact_id]:
        if not re.search(rf"^##\s+(?:\d+\.\s*)?{re.escape(section)}\s*$", content, re.MULTILINE | re.IGNORECASE): errors.append(err("PM_MISSING_SECTION", "sections", f"required section {section!r} is missing"))
    if data.get("schema_version") not in {"1", 1}: errors.append(err("PM_INVALID_SCHEMA_VERSION", "schema_version", "schema_version must be 1", data.get("schema_version")))
    VALIDATORS[artifact_id](data, errors)
    return artifact_id, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate PM strategy artifacts")
    parser.add_argument("artifact_path")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    artifact_id, errors = validate(Path(args.artifact_path))
    result = {"valid": not errors, "artifact_id": artifact_id, "artifact_path": str(Path(args.artifact_path).resolve()), "validator": VALIDATOR, "errors": errors, "validation_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")}
    if args.json: print(json.dumps(result, indent=2))
    elif errors:
        for item in errors: print(f"ERROR {item['error_id']}: {item['message']}")
    else: print(f"{artifact_id} validation passed")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
