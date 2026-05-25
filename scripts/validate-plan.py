"""Specialized Level 3 validator for workflow-orchestration-plan artifacts."""

import os
import sys
import re
import json
import argparse
from datetime import datetime, timezone
from typing import TypedDict, Any

import yaml

from _validator_utils import format_error, load_workflow_registry, load_artifact_contracts, load_skill_registry

# Stable error codes
WORKFLOW_NOT_FOUND = "WORKFLOW_NOT_FOUND"
EXECUTION_MODE_DENIED = "EXECUTION_MODE_DENIED"
INPUT_MISMATCH = "INPUT_MISMATCH"
STEP_COUNT_MISMATCH = "STEP_COUNT_MISMATCH"
STEP_SKILL_MISMATCH = "STEP_SKILL_MISMATCH"
STEP_TYPE_MISMATCH = "STEP_TYPE_MISMATCH"
GATE_MISMATCH = "GATE_MISMATCH"
INPUT_ARTIFACT_MISMATCH = "INPUT_ARTIFACT_MISMATCH"
OUTPUT_ARTIFACT_MISMATCH = "OUTPUT_ARTIFACT_MISMATCH"
ARTIFACT_NOT_CONTRACTED = "ARTIFACT_NOT_CONTRACTED"
GATE_BEHAVIOR_MISSING = "GATE_BEHAVIOR_MISSING"
SIMULATED_GATE_CLASH = "SIMULATED_GATE_CLASH"
STOP_CONDITIONS_EMPTY = "STOP_CONDITIONS_EMPTY"
SUBSET_NOT_CONTIGUOUS = "SUBSET_NOT_CONTIGUOUS"
SECTION_11_MALFORMED = "SECTION_11_MALFORMED"
ABSOLUTE_PATH_DETECTED = "ABSOLUTE_PATH_DETECTED"
HALLUCINATED_SKILL = "HALLUCINATED_SKILL"
MISSING_DECISION_FIELD = "MISSING_DECISION_FIELD"
INVALID_CONDITIONAL_BRANCH = "INVALID_CONDITIONAL_BRANCH"
CONFLICT_NOT_ESCALATED = "CONFLICT_NOT_ESCALATED"


class ValidationError(TypedDict, total=False):
    """Structured validation error with all metadata for JSON output."""
    error_id: str  # e.g., workflow_orchestration_plan.primary_fog_type.missing_field
    error_type: str  # missing_field, unknown_value, semantic_conflict, type_error, logic_error
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




def validate_plan(plan_path: str, repo_root: str = ".") -> list[ValidationError]:
    """Validate a workflow orchestration plan and return structured errors.

    Returns a list of ValidationError dicts. Empty list means validation passed.

    Phase 1 scope: Validate required fields only:
    - artifact_id
    - primary_fog_type
    - chosen_workflow_id
    - routing_decision_method
    - workflow_steps (non-empty array)
    - created_at
    """
    errors: list[ValidationError] = []

    # Check file exists
    if not os.path.exists(plan_path):
        errors.append({
            "error_type": "missing_field",
            "field": "artifact",
            "current_value": None,
            "message": f"Plan file not found: {plan_path}",
            "suggested_fixes": [f"Ensure plan exists at: {plan_path}"],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
        return errors

    with open(plan_path, encoding="utf-8") as f:
        content = f.read()

    # Extract machine-readable handoff YAML
    handoff_match = re.search(
        r"## 13\. Machine-readable handoff\s+```yaml\s+(.*?)\s+```",
        content,
        re.DOTALL | re.IGNORECASE,
    )

    if not handoff_match:
        # Try to find Section 11 as fallback for backward compatibility
        handoff_match = re.search(
            r"## 11\. Machine-readable plan\s+```yaml\s+(.*?)\s+```",
            content,
            re.DOTALL | re.IGNORECASE,
        )

    if not handoff_match:
        errors.append({
            "error_type": "missing_field",
            "field": "machine_readable_handoff",
            "current_value": None,
            "message": "Machine-readable handoff YAML block not found in plan artifact.",
            "suggested_fixes": [
                "Add Section 13 with YAML block containing plan metadata",
                "Or add Section 11 with YAML block for backward compatibility"
            ],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
        return errors

    try:
        plan_data = yaml.safe_load(handoff_match.group(1))
    except Exception as e:
        errors.append({
            "error_type": "type_error",
            "field": "machine_readable_handoff",
            "current_value": None,
            "message": f"Failed to parse YAML block: {str(e)}",
            "suggested_fixes": ["Ensure YAML syntax is correct", "Check indentation and formatting"],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
        return errors

    if not isinstance(plan_data, dict):
        errors.append({
            "error_type": "type_error",
            "field": "machine_readable_handoff",
            "current_value": type(plan_data).__name__,
            "message": f"YAML block should be a dictionary, got {type(plan_data).__name__}",
            "suggested_fixes": ["Ensure YAML block contains key-value pairs, not a list"],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
        return errors

    # --- PHASE 1 REQUIRED FIELD CHECKS ---
    # Check primary_fog_type
    if "primary_fog_type" not in plan_data:
        errors.append({
            "error_id": "workflow_orchestration_plan.primary_fog_type.missing_field",
            "error_type": "missing_field",
            "field": "primary_fog_type",
            "current_value": None,
            "message": "Required field 'primary_fog_type' is missing.",
            "suggested_fixes": [
                "Add primary_fog_type: product_fog",
                "Add primary_fog_type: ui_fog",
                "Add primary_fog_type: docs_fog",
                "Add primary_fog_type: architecture_fog"
            ],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
    else:
        fog_type = plan_data.get("primary_fog_type")
        allowed_fog_types = ["product_fog", "ui_fog", "docs_fog", "architecture_fog"]
        if fog_type not in allowed_fog_types:
            errors.append({
                "error_id": "workflow_orchestration_plan.primary_fog_type.unknown_value",
                "error_type": "unknown_value",
                "field": "primary_fog_type",
                "current_value": fog_type,
                "message": f"Field 'primary_fog_type' has value '{fog_type}', which is not recognized.",
                "suggested_fixes": [f"Change to: primary_fog_type: {ft}" for ft in allowed_fog_types],
                "reference": "docs/adr/0007-soft-context-routing.md"
            })

    # Check chosen_workflow_id
    if "chosen_workflow_id" not in plan_data:
        errors.append({
            "error_id": "workflow_orchestration_plan.chosen_workflow_id.missing_field",
            "error_type": "missing_field",
            "field": "chosen_workflow_id",
            "current_value": None,
            "message": "Required field 'chosen_workflow_id' is missing.",
            "suggested_fixes": [
                "Add chosen_workflow_id: product-implementation-workflow",
                "Add chosen_workflow_id: ui-implementation-workflow",
                "Add chosen_workflow_id: docs-implementation-workflow",
                "Add chosen_workflow_id: architecture-implementation-workflow"
            ],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
    else:
        workflow_id = plan_data.get("chosen_workflow_id")
        workflow_reg = load_workflow_registry(repo_root)
        if workflow_reg is not None:
            valid_ids = {w["id"] for w in workflow_reg.get("workflows", [])}
            if workflow_id not in valid_ids:
                errors.append({
                    "error_id": "workflow_orchestration_plan.chosen_workflow_id.unknown_value",
                    "error_type": "unknown_value",
                    "field": "chosen_workflow_id",
                    "current_value": workflow_id,
                    "message": f"Workflow ID '{workflow_id}' not found in registry.",
                    "suggested_fixes": [
                        "Check available workflows in workflow-registry.yaml",
                        "Ensure workflow ID matches exactly (case-sensitive)"
                    ],
                    "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
                })

    # Check routing_decision_method
    if "routing_decision_method" not in plan_data:
        errors.append({
            "error_id": "workflow_orchestration_plan.routing_decision_method.missing_field",
            "error_type": "missing_field",
            "field": "routing_decision_method",
            "current_value": None,
            "message": "Required field 'routing_decision_method' is missing.",
            "suggested_fixes": [
                "Add routing_decision_method: automated",
                "Add routing_decision_method: manual_override",
                "Add routing_decision_method: context_based"
            ],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })

    # Check workflow_steps (should be non-empty array)
    if "workflow_steps" not in plan_data:
        errors.append({
            "error_id": "workflow_orchestration_plan.workflow_steps.missing_field",
            "error_type": "missing_field",
            "field": "workflow_steps",
            "current_value": None,
            "message": "Required field 'workflow_steps' is missing.",
            "suggested_fixes": [
                "Add workflow_steps as an array of step objects",
                "Each step should have: step_id, skill, input_artifact, output_artifact, gate, description"
            ],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
    else:
        workflow_steps = plan_data.get("workflow_steps")
        if not isinstance(workflow_steps, list):
            errors.append({
                "error_id": "workflow_orchestration_plan.workflow_steps.type_error",
                "error_type": "type_error",
                "field": "workflow_steps",
                "current_value": workflow_steps,
                "message": f"Field 'workflow_steps' should be an array, but got {type(workflow_steps).__name__}.",
                "suggested_fixes": ["Convert workflow_steps to an array of step objects"],
                "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
            })
        elif len(workflow_steps) == 0:
            errors.append({
                "error_id": "workflow_orchestration_plan.workflow_steps.logic_error",
                "error_type": "logic_error",
                "field": "workflow_steps",
                "current_value": [],
                "message": "workflow_steps array is empty. At least one workflow step is required.",
                "suggested_fixes": [
                    "Add at least one step to workflow_steps",
                    "Each step should have: step_id, skill, input_artifact, output_artifact, gate, description"
                ],
                "reference": "docs/adr/0003-artifact-composition-pattern.md"
            })

    # Check created_at
    if "created_at" not in plan_data:
        errors.append({
            "error_id": "workflow_orchestration_plan.created_at.missing_field",
            "error_type": "missing_field",
            "field": "created_at",
            "current_value": None,
            "message": "Required field 'created_at' is missing.",
            "suggested_fixes": [
                "Add created_at with ISO 8601 timestamp (e.g., 2026-05-25T10:30:00Z)"
            ],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })

    # --- SEMANTIC CONFLICT CHECK: primary_fog_type vs chosen_workflow_id ---
    # Mapping of fog types to expected workflow IDs
    fog_to_workflow = {
        "product_fog": "product-implementation-workflow",
        "ui_fog": "ui-implementation-workflow",
        "docs_fog": "docs-implementation-workflow",
        "architecture_fog": "architecture-implementation-workflow",
    }

    fog_type = plan_data.get("primary_fog_type")
    workflow_id = plan_data.get("chosen_workflow_id")
    routing_method = plan_data.get("routing_decision_method")

    # Only check alignment if both fields are present and valid
    if fog_type in fog_to_workflow and workflow_id:
        expected_workflow = fog_to_workflow[fog_type]
        if workflow_id != expected_workflow and routing_method != "manual_override":
            errors.append({
                "error_id": "workflow_orchestration_plan.chosen_workflow_id.semantic_conflict",
                "error_type": "semantic_conflict",
                "field": "chosen_workflow_id",
                "current_value": workflow_id,
                "message": f"Workflow '{workflow_id}' does not align with primary_fog_type '{fog_type}'. Expected '{expected_workflow}' unless routing_decision_method is 'manual_override'.",
                "suggested_fixes": [
                    f"Change chosen_workflow_id to: {expected_workflow}",
                    "Or set routing_decision_method to: manual_override (if intentional)"
                ],
                "reference": "docs/adr/0007-soft-context-routing.md"
            })

    return errors


def validation_result_to_json(
    plan_path: str,
    errors: list[ValidationError],
) -> str:
    """Convert validation result to JSON format with multi-error schema."""
    result: ValidationResult = {
        "valid": len(errors) == 0,
        "artifact_id": "workflow_orchestration_plan",
        "artifact_path": os.path.abspath(plan_path),
        "validator": "validate-plan.py",
        "errors": errors,
        "validation_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }

    return json.dumps(result, indent=2, default=str)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Specialized validator for workflow orchestration plan.")
    parser.add_argument("artifact_path", nargs="?", help="Path to the plan .md file")
    parser.add_argument("--repo-root", default=".", help="Root of the repository for file checks")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--list-codes", action="store_true", help="List all error codes and exit")
    args = parser.parse_args(argv)

    if args.list_codes:
        codes = [
            WORKFLOW_NOT_FOUND,
            EXECUTION_MODE_DENIED,
            INPUT_MISMATCH,
            STEP_COUNT_MISMATCH,
            STEP_SKILL_MISMATCH,
            STEP_TYPE_MISMATCH,
            GATE_MISMATCH,
            INPUT_ARTIFACT_MISMATCH,
            OUTPUT_ARTIFACT_MISMATCH,
            ARTIFACT_NOT_CONTRACTED,
            GATE_BEHAVIOR_MISSING,
            SIMULATED_GATE_CLASH,
            STOP_CONDITIONS_EMPTY,
            SUBSET_NOT_CONTIGUOUS,
            SECTION_11_MALFORMED,
            ABSOLUTE_PATH_DETECTED,
            HALLUCINATED_SKILL,
            MISSING_DECISION_FIELD,
            INVALID_CONDITIONAL_BRANCH,
            CONFLICT_NOT_ESCALATED,
        ]
        print("Stable error codes for plan validation:")
        for code in codes:
            print(f"  {code}")
        return 0

    if not args.artifact_path:
        parser.print_usage()
        return 1

    errors = validate_plan(args.artifact_path, args.repo_root)

    if args.json:
        print(validation_result_to_json(args.artifact_path, errors))
        return 0 if len(errors) == 0 else 1
    else:
        # Legacy prose output for backward compatibility
        if errors:
            for error in errors:
                error_type = error.get("error_type", "unknown")
                field = error.get("field", "")
                message = error.get("message", "")
                print(f"ERROR [{error_type}] {field}: {message}")
            return 1
        else:
            print("Plan validation passed! All required fields are present and valid.")
            return 0


if __name__ == "__main__":
    sys.exit(main())
