#!/usr/bin/env python3
"""Deterministic validator for the PM Customer Discovery artifact slice.

Validates representation and evidence-shape contracts only. It never decides
whether a persona, discovery conclusion, opportunity, or hypothesis is
semantically correct.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

VALIDATOR = "validate-pm-artifact.py"
SUPPORTED = {
    "persona_definition",
    "discovery_findings",
    "synthesis_report",
    "opportunity_map",
    "hypothesis_statement",
}
REQUIRED_SECTIONS = {
    "persona_definition": ("Persona summary", "Context and profile", "Jobs to Be Done", "Pains and desired outcomes", "Current solutions and behaviors", "Evidence and confidence", "Assumptions and research gaps"),
    "discovery_findings": ("Problem framing", "Existing evidence", "Hypotheses and uncertainties", "Learning plan", "Decision criteria", "Unresolved questions"),
    "synthesis_report": ("Research context and sources", "Jobs to Be Done", "Behavioral patterns", "Problems and contradictions", "Evidence excerpts", "Implications and next research"),
    "opportunity_map": ("Desired outcome", "Opportunities", "Opportunity comparison", "Candidate solutions and risky assumptions", "Learning tests", "Recommended branch"),
    "hypothesis_statement": ("Hypothesis", "Context and evidence", "Target and expected behavior", "Measures and thresholds", "Risk assumptions", "Validation approach", "Success, pivot, and kill criteria"),
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
            errors.append(_err("PM_ID_REQUIRED", f"{field}[{index}].id", "item id must be non-empty"))
            continue
        ids.append(item["id"].strip())
    if len(ids) != len(set(ids)):
        errors.append(_err("PM_DUPLICATE_ID", field, f"{field} contains duplicate ids", ids))


def _require(data: dict[str, Any], fields: tuple[str, ...], errors: list[dict[str, Any]]) -> None:
    for field in fields:
        if field not in data:
            errors.append(_err("PM_MISSING_FIELD", field, f"required field {field!r} is missing"))


def _validate_persona(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    _require(data, ("schema_version", "persona_id", "status", "segment", "primary_job", "evidence_refs", "assumptions", "unresolved_questions"), errors)
    for field in ("persona_id", "segment", "primary_job"):
        if field in data and not _text(data[field]):
            errors.append(_err("PM_TEXT_REQUIRED", field, f"{field} must be non-empty text", data[field]))
    status = data.get("status")
    if status not in {"provisional", "evidence_backed"}:
        errors.append(_err("PM_INVALID_STATUS", "status", "persona status must be provisional or evidence_backed", status))
    refs = data.get("evidence_refs")
    if not _string_list(refs):
        errors.append(_err("PM_INVALID_EVIDENCE_REFS", "evidence_refs", "evidence_refs must be a list of non-empty strings", refs))
    elif status == "evidence_backed" and not refs:
        errors.append(_err("PM_EVIDENCE_REQUIRED", "evidence_refs", "evidence_backed persona requires at least one evidence reference", refs))
    for field in ("assumptions", "unresolved_questions"):
        if field in data and not isinstance(data[field], list):
            errors.append(_err("PM_LIST_REQUIRED", field, f"{field} must be a list", data[field]))


def _validate_discovery(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    _require(data, ("schema_version", "problem_statement", "hypotheses", "unresolved_questions"), errors)
    if "problem_statement" in data and not _text(data["problem_statement"]):
        errors.append(_err("PM_TEXT_REQUIRED", "problem_statement", "problem_statement must be non-empty text", data["problem_statement"]))
    hypotheses = data.get("hypotheses")
    _unique_ids(hypotheses, field="hypotheses", errors=errors)
    if isinstance(hypotheses, list):
        for i, hyp in enumerate(hypotheses):
            if not isinstance(hyp, dict):
                continue
            for field in ("statement", "learning_method", "decision_criterion"):
                if not _text(hyp.get(field)):
                    errors.append(_err("PM_TEXT_REQUIRED", f"hypotheses[{i}].{field}", f"{field} must be non-empty text", hyp.get(field)))
            status = hyp.get("status")
            if status not in {"untested", "evidence_backed", "contradicted"}:
                errors.append(_err("PM_INVALID_STATUS", f"hypotheses[{i}].status", "status must be untested, evidence_backed, or contradicted", status))
            refs = hyp.get("evidence_refs")
            if not _string_list(refs):
                errors.append(_err("PM_INVALID_EVIDENCE_REFS", f"hypotheses[{i}].evidence_refs", "evidence_refs must be a list of non-empty strings", refs))
            elif status == "evidence_backed" and not refs:
                errors.append(_err("PM_EVIDENCE_REQUIRED", f"hypotheses[{i}].evidence_refs", "evidence_backed hypothesis requires evidence", refs))
    if "unresolved_questions" in data and not isinstance(data["unresolved_questions"], list):
        errors.append(_err("PM_LIST_REQUIRED", "unresolved_questions", "unresolved_questions must be a list", data["unresolved_questions"]))


def _validate_synthesis(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    _require(data, ("schema_version", "source_interviews", "findings", "contradictions", "unresolved_questions"), errors)
    sources = data.get("source_interviews")
    if not _string_list(sources, nonempty=True):
        errors.append(_err("PM_SOURCE_REQUIRED", "source_interviews", "source_interviews must contain at least one non-empty source reference", sources))
        source_set: set[str] = set()
    else:
        source_set = set(sources)
    findings = data.get("findings")
    _unique_ids(findings, field="findings", errors=errors)
    if isinstance(findings, list):
        for i, finding in enumerate(findings):
            if not isinstance(finding, dict):
                continue
            if not _text(finding.get("statement")):
                errors.append(_err("PM_TEXT_REQUIRED", f"findings[{i}].statement", "finding statement must be non-empty", finding.get("statement")))
            refs = finding.get("source_refs")
            if not _string_list(refs, nonempty=True):
                errors.append(_err("PM_SOURCE_REQUIRED", f"findings[{i}].source_refs", "each finding needs at least one source reference", refs))
            elif source_set and not set(refs).issubset(source_set):
                errors.append(_err("PM_UNKNOWN_SOURCE_REF", f"findings[{i}].source_refs", "finding source_refs must resolve within source_interviews", refs))
            confidence = finding.get("confidence")
            if confidence not in {"low", "medium", "high"}:
                errors.append(_err("PM_INVALID_CONFIDENCE", f"findings[{i}].confidence", "confidence must be low, medium, or high", confidence))
            freq = finding.get("frequency")
            if not isinstance(freq, dict) or not isinstance(freq.get("count"), int) or not isinstance(freq.get("total"), int):
                errors.append(_err("PM_INVALID_FREQUENCY", f"findings[{i}].frequency", "frequency must contain integer count and total", freq))
            elif freq["count"] < 0 or freq["total"] <= 0 or freq["count"] > freq["total"]:
                errors.append(_err("PM_INVALID_FREQUENCY", f"findings[{i}].frequency", "frequency requires 0 <= count <= total and total > 0", freq))
    for field in ("contradictions", "unresolved_questions"):
        if field in data and not isinstance(data[field], list):
            errors.append(_err("PM_LIST_REQUIRED", field, f"{field} must be a list", data[field]))


def _validate_opportunity(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    _require(data, ("schema_version", "desired_outcome", "opportunities", "recommended_branch", "unresolved_questions"), errors)
    outcome = data.get("desired_outcome")
    if not isinstance(outcome, dict) or not _text(outcome.get("statement")):
        errors.append(_err("PM_INVALID_OUTCOME", "desired_outcome", "desired_outcome must be a mapping with a non-empty statement", outcome))
    opportunities = data.get("opportunities")
    _unique_ids(opportunities, field="opportunities", errors=errors)
    if isinstance(opportunities, list):
        for i, opp in enumerate(opportunities):
            if not isinstance(opp, dict):
                continue
            if not _text(opp.get("statement")):
                errors.append(_err("PM_TEXT_REQUIRED", f"opportunities[{i}].statement", "opportunity statement must be non-empty", opp.get("statement")))
            status = opp.get("status")
            if status not in {"assumption", "evidence_backed"}:
                errors.append(_err("PM_INVALID_STATUS", f"opportunities[{i}].status", "status must be assumption or evidence_backed", status))
            refs = opp.get("evidence_refs")
            if not _string_list(refs):
                errors.append(_err("PM_INVALID_EVIDENCE_REFS", f"opportunities[{i}].evidence_refs", "evidence_refs must be a list of non-empty strings", refs))
            elif status == "evidence_backed" and not refs:
                errors.append(_err("PM_EVIDENCE_REQUIRED", f"opportunities[{i}].evidence_refs", "evidence_backed opportunity requires evidence", refs))
            imp, sat, score = opp.get("importance"), opp.get("satisfaction"), opp.get("score")
            if imp is not None and (not isinstance(imp, (int, float)) or isinstance(imp, bool) or not 1 <= imp <= 5):
                errors.append(_err("PM_INVALID_SCORE_INPUT", f"opportunities[{i}].importance", "importance must be null or numeric 1-5", imp))
            if sat is not None and (not isinstance(sat, (int, float)) or isinstance(sat, bool) or not 1 <= sat <= 5):
                errors.append(_err("PM_INVALID_SCORE_INPUT", f"opportunities[{i}].satisfaction", "satisfaction must be null or numeric 1-5", sat))
            if score is not None:
                if not isinstance(score, (int, float)) or isinstance(score, bool):
                    errors.append(_err("PM_INVALID_SCORE", f"opportunities[{i}].score", "score must be null or numeric", score))
                elif isinstance(imp, (int, float)) and not isinstance(imp, bool) and isinstance(sat, (int, float)) and not isinstance(sat, bool):
                    expected = imp * (1 - sat / 5)
                    if not math.isclose(float(score), float(expected), abs_tol=0.02):
                        errors.append(_err("PM_SCORE_MISMATCH", f"opportunities[{i}].score", f"score must equal importance * (1 - satisfaction/5); expected {expected:.3f}", score))
                else:
                    errors.append(_err("PM_SCORE_WITHOUT_INPUTS", f"opportunities[{i}].score", "score requires numeric importance and satisfaction inputs", score))
    if data.get("recommended_branch") is not None and not _text(data.get("recommended_branch")):
        errors.append(_err("PM_TEXT_REQUIRED", "recommended_branch", "recommended_branch must be null or non-empty text", data.get("recommended_branch")))
    if "unresolved_questions" in data and not isinstance(data["unresolved_questions"], list):
        errors.append(_err("PM_LIST_REQUIRED", "unresolved_questions", "unresolved_questions must be a list", data["unresolved_questions"]))


def _validate_hypothesis(data: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    required = ("schema_version", "hypothesis_id", "target_segment", "problem_or_opportunity", "intervention", "expected_outcome", "primary_measure", "success_criterion", "kill_criterion", "evidence_refs", "assumptions", "validation_method", "status")
    _require(data, required, errors)
    for field in ("hypothesis_id", "target_segment", "problem_or_opportunity", "intervention", "expected_outcome", "primary_measure", "success_criterion", "kill_criterion", "validation_method"):
        if field in data and not _text(data[field]):
            errors.append(_err("PM_TEXT_REQUIRED", field, f"{field} must be non-empty text", data[field]))
    if data.get("status") != "proposed":
        errors.append(_err("PM_INVALID_STATUS", "status", "hypothesis_statement status must be proposed; outcomes belong to empirical evidence", data.get("status")))
    if "evidence_refs" in data and not _string_list(data["evidence_refs"]):
        errors.append(_err("PM_INVALID_EVIDENCE_REFS", "evidence_refs", "evidence_refs must be a list of non-empty strings", data["evidence_refs"]))
    if "assumptions" in data and not isinstance(data["assumptions"], list):
        errors.append(_err("PM_LIST_REQUIRED", "assumptions", "assumptions must be a list", data["assumptions"]))


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
        return str(artifact_id or "unknown"), [_err("PM_UNSUPPORTED_ARTIFACT", "artifact_id", f"unsupported PM artifact_id: {artifact_id!r}", artifact_id)]
    errors: list[dict[str, Any]] = []
    for heading in REQUIRED_SECTIONS[artifact_id]:
        pattern = re.compile(r"^##\s+(?:\d+\.\s*)?" + re.escape(heading) + r"\s*$", re.MULTILINE | re.IGNORECASE)
        if not pattern.search(content):
            errors.append(_err("PM_MISSING_SECTION", "sections", f"missing required section: {heading}"))
    if data.get("schema_version") != "1":
        errors.append(_err("PM_SCHEMA_VERSION", "schema_version", "schema_version must be string '1'", data.get("schema_version")))
    {
        "persona_definition": _validate_persona,
        "discovery_findings": _validate_discovery,
        "synthesis_report": _validate_synthesis,
        "opportunity_map": _validate_opportunity,
        "hypothesis_statement": _validate_hypothesis,
    }[artifact_id](data, errors)
    return artifact_id, errors


def result(path: Path) -> dict[str, Any]:
    artifact_id, errors = validate(path)
    return {
        "valid": not errors,
        "artifact_id": artifact_id,
        "artifact_path": str(path.resolve()),
        "validator": VALIDATOR,
        "errors": errors,
        "validation_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate PM Customer Discovery artifacts")
    parser.add_argument("artifact_path")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = result(Path(args.artifact_path))
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print("VALID" if payload["valid"] else "INVALID")
        for error in payload["errors"]:
            print(f"- {error['error_id']}: {error['message']}")
    return 0 if payload["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
