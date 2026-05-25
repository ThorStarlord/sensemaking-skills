#!/usr/bin/env python3
"""Test runner for validate-plan.py JSON output."""

import sys
import os
import json

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

# Import _validator_utils dependencies
import yaml
import re
from datetime import datetime, timezone
from typing import TypedDict, Any

# Define the validation functions (copy from validate-plan.py)
class ValidationError(TypedDict, total=False):
    """Structured validation error with all metadata for JSON output."""
    error_id: str
    error_type: str
    field: str | None
    current_value: Any
    message: str
    suggested_fixes: list[str]
    reference: str

def load_workflow_registry(repo_root: str) -> dict | None:
    """Load workflow registry."""
    path = os.path.join(repo_root, "skills", "workflow-planner", "references", "workflow-registry.yaml")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return yaml.safe_load(f)

def validate_plan(plan_path: str, repo_root: str = ".") -> list[ValidationError]:
    """Validate a workflow orchestration plan and return structured errors."""
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
    fog_to_workflow = {
        "product_fog": "product-implementation-workflow",
        "ui_fog": "ui-implementation-workflow",
        "docs_fog": "docs-implementation-workflow",
        "architecture_fog": "architecture-implementation-workflow",
    }

    fog_type = plan_data.get("primary_fog_type")
    workflow_id = plan_data.get("chosen_workflow_id")
    routing_method = plan_data.get("routing_decision_method")

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


def validation_result_to_json(plan_path: str, errors: list[ValidationError]) -> str:
    """Convert validation result to JSON format with multi-error schema."""
    result = {
        "valid": len(errors) == 0,
        "artifact_id": "workflow_orchestration_plan",
        "artifact_path": os.path.abspath(plan_path),
        "validator": "validate-plan.py",
        "errors": errors,
        "validation_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }
    return json.dumps(result, indent=2, default=str)

# Now run tests
def run_tests():
    """Run all tests."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fixtures_dir = os.path.join(repo_root, "tests", "fixtures")

    tests_run = 0
    tests_passed = 0

    # Test 1: Valid plan
    print("[TEST 1] Valid plan")
    plan_path = os.path.join(fixtures_dir, "plan-valid.md")
    errors = validate_plan(plan_path, repo_root)
    tests_run += 1
    if len(errors) == 0:
        tests_passed += 1
        print("  PASSED: No errors for valid plan")
    else:
        print(f"  FAILED: Expected no errors, got {len(errors)}")
        for error in errors:
            print(f"    - {error.get('error_id', error.get('error_type'))}: {error.get('message')}")

    # Test 2: Missing fields
    print("[TEST 2] Missing required fields")
    plan_path = os.path.join(fixtures_dir, "plan-invalid-missing-fields.md")
    errors = validate_plan(plan_path, repo_root)
    tests_run += 1
    if len(errors) >= 4:  # Should be missing: primary_fog_type, chosen_workflow_id, workflow_steps, created_at
        tests_passed += 1
        print(f"  PASSED: Found {len(errors)} errors as expected")
    else:
        print(f"  FAILED: Expected >= 4 errors, got {len(errors)}")

    # Test 3: Wrong values
    print("[TEST 3] Wrong value types and enums")
    plan_path = os.path.join(fixtures_dir, "plan-invalid-wrong-values.md")
    errors = validate_plan(plan_path, repo_root)
    tests_run += 1
    if len(errors) >= 3:
        tests_passed += 1
        print(f"  PASSED: Found {len(errors)} errors as expected")
        error_types = [e.get("error_type") for e in errors]
        print(f"    Error types: {set(error_types)}")
    else:
        print(f"  FAILED: Expected >= 3 errors, got {len(errors)}")

    # Test 4: Empty workflow_steps
    print("[TEST 4] Empty workflow_steps (logic_error)")
    plan_path = os.path.join(fixtures_dir, "plan-invalid-empty-workflow-steps.md")
    errors = validate_plan(plan_path, repo_root)
    tests_run += 1
    if len(errors) >= 1 and any(e.get("error_type") == "logic_error" for e in errors):
        tests_passed += 1
        print("  PASSED: Found logic_error as expected")
    else:
        print(f"  FAILED: Expected logic_error")

    # Test JSON output structure
    print("[TEST 5] JSON output structure")
    plan_path = os.path.join(fixtures_dir, "plan-valid.md")
    errors = validate_plan(plan_path, repo_root)
    json_output = validation_result_to_json(plan_path, errors)
    result = json.loads(json_output)
    tests_run += 1
    checks = [
        result["valid"] == True,
        result["artifact_id"] == "workflow_orchestration_plan",
        result["validator"] == "validate-plan.py",
        "errors" in result,
        "validation_timestamp" in result,
        result["errors"] == []
    ]
    if all(checks):
        tests_passed += 1
        print("  PASSED: JSON structure is correct")
    else:
        print(f"  FAILED: JSON structure issues")

    # Test error_id format
    print("[TEST 6] error_id in all errors")
    plan_path = os.path.join(fixtures_dir, "plan-invalid-missing-fields.md")
    errors = validate_plan(plan_path, repo_root)
    tests_run += 1
    if all("error_id" in e for e in errors):
        tests_passed += 1
        print(f"  PASSED: All {len(errors)} errors have error_id")
        for error in errors:
            print(f"    - {error['error_id']}")
    else:
        print(f"  FAILED: Some errors missing error_id")

    # Test error_id format is correct
    print("[TEST 7] error_id format validation")
    tests_run += 1
    valid_format = True
    for error in errors:
        error_id = error.get("error_id", "")
        parts = error_id.split(".")
        if len(parts) != 3 or parts[0] != "workflow_orchestration_plan":
            valid_format = False
            print(f"  FAILED: Invalid error_id format: {error_id}")
            break
    if valid_format:
        tests_passed += 1
        print("  PASSED: All error_ids follow correct format")

    # Test error_id uniqueness for agent retry tracking
    print("[TEST 8] error_id usefulness for retry logic")
    plan_path = os.path.join(fixtures_dir, "plan-invalid-wrong-values.md")
    errors = validate_plan(plan_path, repo_root)
    tests_run += 1
    error_ids = [e.get("error_id") for e in errors]
    if len(error_ids) == len(set(error_ids)):
        tests_passed += 1
        print(f"  PASSED: All error_ids are unique (can track retries)")
    else:
        print(f"  FAILED: Duplicate error_ids found")

    # Test semantic_conflict check
    print("[TEST 9] semantic_conflict for misaligned fog type and workflow")
    plan_path = os.path.join(fixtures_dir, "plan-invalid-semantic-conflict.md")
    errors = validate_plan(plan_path, repo_root)
    tests_run += 1
    semantic_conflicts = [e for e in errors if e.get("error_type") == "semantic_conflict"]
    if len(semantic_conflicts) > 0:
        tests_passed += 1
        print(f"  PASSED: Found semantic_conflict as expected")
        for error in semantic_conflicts:
            print(f"    - {error.get('error_id')}: {error.get('message')}")
    else:
        print(f"  FAILED: Expected semantic_conflict error")

    print(f"\n[SUMMARY] {tests_passed}/{tests_run} tests passed")
    return 0 if tests_passed == tests_run else 1

if __name__ == "__main__":
    sys.exit(run_tests())
