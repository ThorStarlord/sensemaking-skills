"""Specialized validator for architectural_review_recommendation artifact.

Validates decision quality, consistency of decision reasoning, and risk mapping.
Follows the same error reporting pattern as validate-brief.py.
"""

import os
import sys
import json
import argparse
import re
from datetime import datetime, timezone
from typing import TypedDict, Any

import yaml

from _validator_utils import format_error, extract_sections

# Stable error codes
ARTIFACT_FILE_NOT_FOUND = "ARTIFACT_FILE_NOT_FOUND"
MISSING_MACHINE_FIELDS = "MISSING_MACHINE_FIELDS"
INVALID_DECISION_VALUE = "INVALID_DECISION_VALUE"
INVALID_CONFIDENCE_VALUE = "INVALID_CONFIDENCE_VALUE"
DECISION_RISK_MISMATCH = "DECISION_RISK_MISMATCH"
PURSUE_NARROWED_INCOMPLETE = "PURSUE_NARROWED_INCOMPLETE"
INVESTIGATE_INCOMPLETE = "INVESTIGATE_INCOMPLETE"
DEFER_REJECT_INCOMPLETE = "DEFER_REJECT_INCOMPLETE"
SUCCESS_MEASURES_INCOMPLETE = "SUCCESS_MEASURES_INCOMPLETE"
PARSING_ERROR = "PARSING_ERROR"


class ValidationError(TypedDict, total=False):
    """Structured validation error with all metadata for JSON output."""
    error_id: str
    error_type: str
    field: str | None
    current_value: Any
    message: str
    suggested_fixes: list[str]
    reference: str


class ValidationResult(TypedDict):
    """Complete validation result with metadata."""
    valid: bool
    artifact_id: str
    artifact_path: str
    validator: str
    errors: list[ValidationError]
    validation_timestamp: str


def _parse_artifact_data(content: str) -> dict[str, Any] | None:
    """Extract machine-readable YAML from the artifact.

    Looks for YAML blocks, prioritizing structured handoff sections.
    """
    yaml_blocks = re.findall(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)
    if not yaml_blocks:
        return None

    try:
        return yaml.safe_load(yaml_blocks[-1])
    except Exception:
        return None


def validate_architectural_review_recommendation(artifact_path: str, repo_root: str = ".") -> list[ValidationError]:
    """Validate an architectural review recommendation artifact.

    Returns a list of ValidationError dicts. Empty list means validation passed.
    """
    errors: list[ValidationError] = []

    if not os.path.exists(artifact_path):
        errors.append({
            "error_type": "missing_field",
            "field": "artifact",
            "current_value": None,
            "message": f"Artifact file not found: {artifact_path}",
            "suggested_fixes": [f"Ensure artifact exists at: {artifact_path}"],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
        return errors

    with open(artifact_path, encoding="utf-8") as f:
        content = f.read()

    artifact_data = _parse_artifact_data(content)

    if not artifact_data:
        errors.append({
            "error_id": "architectural_review_recommendation.parsing_error",
            "error_type": "parsing_error",
            "field": "artifact_data",
            "current_value": None,
            "message": "Could not parse YAML from artifact. Ensure a YAML block is present.",
            "suggested_fixes": [
                "Add a YAML block with decision and supporting fields",
                "Example: ```yaml",
                "decision: pursue",
                "confidence: high",
                "```"
            ],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
        return errors

    if not isinstance(artifact_data, dict):
        errors.append({
            "error_id": "architectural_review_recommendation.artifact_data.type_error",
            "error_type": "type_error",
            "field": "artifact_data",
            "current_value": type(artifact_data).__name__,
            "message": "Machine-readable YAML must be a mapping/object (key-value pairs).",
            "suggested_fixes": [
                "Ensure the fenced ```yaml block contains key: value pairs (not a list)",
            ],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml",
        })
        return errors

    # Required machine fields per artifact-contracts.yaml
    for field_name in ("artifact_id", "created_at", "created_by"):
        if field_name not in artifact_data or not artifact_data.get(field_name):
            errors.append({
                "error_id": f"architectural_review_recommendation.{field_name}.missing_field",
                "error_type": "missing_field",
                "field": field_name,
                "current_value": None,
                "message": f"Required field '{field_name}' is missing.",
                "suggested_fixes": [f"Add {field_name}: ..."],
                "reference": "skills/workflow-planner/references/artifact-contracts.yaml",
            })

    if (
        artifact_data.get("artifact_id")
        and artifact_data.get("artifact_id") != "architectural_review_recommendation"
    ):
        errors.append({
            "error_id": "architectural_review_recommendation.artifact_id.unknown_value",
            "error_type": "unknown_value",
            "field": "artifact_id",
            "current_value": artifact_data.get("artifact_id"),
            "message": "Field 'artifact_id' must be 'architectural_review_recommendation'.",
            "suggested_fixes": ["Change to: artifact_id: architectural_review_recommendation"],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml",
        })

    # Required field: decision
    if "decision" not in artifact_data:
        errors.append({
            "error_id": "architectural_review_recommendation.decision.missing_field",
            "error_type": "missing_field",
            "field": "decision",
            "current_value": None,
            "message": "Required field 'decision' is missing.",
            "suggested_fixes": [
                "Add decision: pursue",
                "Add decision: pursue_narrowed",
                "Add decision: investigate_first",
                "Add decision: defer",
                "Add decision: reject"
            ],
            "reference": "docs/skill-design-architectural-review.md"
        })
    else:
        decision = artifact_data.get("decision")
        allowed_decisions = ["pursue", "pursue_narrowed", "investigate_first", "defer", "reject"]
        if decision not in allowed_decisions:
            errors.append({
                "error_id": "architectural_review_recommendation.decision.unknown_value",
                "error_type": "unknown_value",
                "field": "decision",
                "current_value": decision,
                "message": f"Field 'decision' has value '{decision}', which is not recognized.",
                "suggested_fixes": [f"Change to: decision: {d}" for d in allowed_decisions],
                "reference": "docs/skill-design-architectural-review.md"
            })
        else:
            # Validate decision-specific required fields
            if decision == "pursue_narrowed":
                if "approved_scope" not in artifact_data or not artifact_data["approved_scope"]:
                    errors.append({
                        "error_id": "architectural_review_recommendation.approved_scope.missing_field",
                        "error_type": "missing_field",
                        "field": "approved_scope",
                        "current_value": None,
                        "message": "Decision 'pursue_narrowed' requires 'approved_scope' to define the narrowed scope.",
                        "suggested_fixes": ["Add approved_scope: [list of approved aspects]"],
                        "reference": "docs/skill-design-architectural-review.md"
                    })
                if "excluded_scope" not in artifact_data or not artifact_data["excluded_scope"]:
                    errors.append({
                        "error_id": "architectural_review_recommendation.excluded_scope.missing_field",
                        "error_type": "missing_field",
                        "field": "excluded_scope",
                        "current_value": None,
                        "message": "Decision 'pursue_narrowed' requires 'excluded_scope' to define what is excluded.",
                        "suggested_fixes": ["Add excluded_scope: [list of excluded aspects]"],
                        "reference": "docs/skill-design-architectural-review.md"
                    })

            elif decision == "investigate_first":
                if "investigation_steps" not in artifact_data and "validation_step" not in artifact_data:
                    errors.append({
                        "error_id": "architectural_review_recommendation.investigation_steps.missing_field",
                        "error_type": "missing_field",
                        "field": "investigation_steps",
                        "current_value": None,
                        "message": "Decision 'investigate_first' requires either 'investigation_steps' or 'validation_step'.",
                        "suggested_fixes": [
                            "Add investigation_steps: [list of steps needed]",
                            "OR add validation_step: [validation description]"
                        ],
                        "reference": "docs/skill-design-architectural-review.md"
                    })

            elif decision in ("defer", "reject"):
                if "reversal_conditions" not in artifact_data or not artifact_data["reversal_conditions"]:
                    errors.append({
                        "error_id": "architectural_review_recommendation.reversal_conditions.missing_field",
                        "error_type": "missing_field",
                        "field": "reversal_conditions",
                        "current_value": None,
                        "message": f"Decision '{decision}' requires 'reversal_conditions' to define when this decision could change.",
                        "suggested_fixes": ["Add reversal_conditions: [list of conditions]"],
                        "reference": "docs/skill-design-architectural-review.md"
                    })

    # Required field: confidence
    if "confidence" not in artifact_data:
        errors.append({
            "error_id": "architectural_review_recommendation.confidence.missing_field",
            "error_type": "missing_field",
            "field": "confidence",
            "current_value": None,
            "message": "Required field 'confidence' is missing.",
            "suggested_fixes": [
                "Add confidence: high",
                "Add confidence: medium",
                "Add confidence: low"
            ],
            "reference": "docs/skill-design-architectural-review.md"
        })
    else:
        confidence = artifact_data.get("confidence")
        allowed_confidences = ["high", "medium", "low"]
        if confidence not in allowed_confidences:
            errors.append({
                "error_id": "architectural_review_recommendation.confidence.unknown_value",
                "error_type": "unknown_value",
                "field": "confidence",
                "current_value": confidence,
                "message": f"Field 'confidence' has value '{confidence}', which is not recognized.",
                "suggested_fixes": [f"Change to: confidence: {c}" for c in allowed_confidences],
                "reference": "docs/skill-design-architectural-review.md"
            })

    # Semantic check: low/medium confidence should have risks identified
    confidence = artifact_data.get("confidence")
    risks = artifact_data.get("risks_identified", [])
    if confidence in ("low", "medium"):
        if not risks or (isinstance(risks, list) and len(risks) == 0):
            errors.append({
                "error_id": "architectural_review_recommendation.risks_identified.logic_error",
                "error_type": "logic_error",
                "field": "risks_identified",
                "current_value": risks,
                "message": f"Confidence '{confidence}' should be supported by identified risks.",
                "suggested_fixes": [
                    "Add risks_identified: [list of risks]",
                    "If this is high-confidence despite low/medium, reconsider confidence level"
                ],
                "reference": "docs/skill-design-architectural-review.md"
            })

    # Optional but important: success_measures (if decision is pursue or pursue_narrowed)
    decision = artifact_data.get("decision")
    if decision and decision.startswith("pursue"):
        success_measures = artifact_data.get("success_measures", {})
        if not success_measures or not isinstance(success_measures, dict):
            errors.append({
                "error_id": "architectural_review_recommendation.success_measures.missing_field",
                "error_type": "missing_field",
                "field": "success_measures",
                "current_value": success_measures,
                "message": "Pursue decisions should include 'success_measures' to define how success will be measured.",
                "suggested_fixes": [
                    "Add success_measures: {metric: '...', baseline_status: '...', target: '...', measurement_method: '...'}"
                ],
                "reference": "docs/skill-design-architectural-review.md"
            })

    return errors


def validation_result_to_json(
    artifact_path: str,
    errors: list[ValidationError],
) -> str:
    """Convert validation result to JSON format with multi-error schema."""
    result: ValidationResult = {
        "valid": len(errors) == 0,
        "artifact_id": "architectural_review_recommendation",
        "artifact_path": os.path.abspath(artifact_path),
        "validator": "validate-architectural-review-recommendation.py",
        "errors": errors,
        "validation_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }

    return json.dumps(result, indent=2, default=str)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Specialized validator for architectural review recommendation.")
    parser.add_argument("artifact_path", nargs="?", help="Path to the architectural review recommendation .md file")
    parser.add_argument("--repo-root", default=".", help="Root of the repository for file checks")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--list-codes", action="store_true", help="List all error codes and exit")
    args = parser.parse_args(argv)

    if args.list_codes:
        codes = [
            ARTIFACT_FILE_NOT_FOUND,
            MISSING_MACHINE_FIELDS,
            INVALID_DECISION_VALUE,
            INVALID_CONFIDENCE_VALUE,
            DECISION_RISK_MISMATCH,
            PURSUE_NARROWED_INCOMPLETE,
            INVESTIGATE_INCOMPLETE,
            DEFER_REJECT_INCOMPLETE,
            SUCCESS_MEASURES_INCOMPLETE,
            PARSING_ERROR,
        ]
        print("Stable error codes for architectural review recommendation validation:")
        for code in codes:
            print(f"  {code}")
        return 0

    if not args.artifact_path:
        parser.print_usage()
        return 1

    errors = validate_architectural_review_recommendation(args.artifact_path, args.repo_root)

    if args.json:
        print(validation_result_to_json(args.artifact_path, errors))
        return 0 if len(errors) == 0 else 1
    else:
        if len(errors) == 0:
            print(f"OK: Validation passed for {args.artifact_path}")
            return 0
        else:
            print(f"FAIL: Validation failed for {args.artifact_path}")
            for error in errors:
                print(f"\n  Error: {error.get('error_id', 'unknown')}")
                print(f"  Field: {error.get('field', 'N/A')}")
                print(f"  Message: {error.get('message')}")
                if error.get('suggested_fixes'):
                    print(f"  Fixes: {', '.join(error['suggested_fixes'][:2])}")
            return 1


if __name__ == "__main__":
    sys.exit(main())
