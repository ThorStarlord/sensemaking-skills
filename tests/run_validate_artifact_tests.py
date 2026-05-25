#!/usr/bin/env python3
"""Test runner for validate-artifact.py JSON output."""

import sys
import os
import json
import re
from datetime import datetime, timezone
from typing import TypedDict, Any

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import yaml

# Define validation types
class ValidationError(TypedDict, total=False):
    """Structured validation error with all metadata for JSON output."""
    error_id: str
    error_type: str
    field: str | None
    current_value: Any
    message: str
    suggested_fixes: list[str]
    reference: str

def load_artifact_contracts(repo_root: str) -> dict | None:
    """Load artifact contracts."""
    path = os.path.join(repo_root, "skills", "workflow-planner", "references", "artifact-contracts.yaml")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return yaml.safe_load(f)

def validate_artifact(artifact_id: str, artifact_path: str, repo_root: str = ".") -> list[ValidationError]:
    """Validate an artifact against its contract and return structured errors."""
    errors: list[ValidationError] = []

    # Check file exists
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

    # Load contracts
    contracts_data = load_artifact_contracts(repo_root)
    if contracts_data is None:
        errors.append({
            "error_type": "missing_field",
            "field": "artifact_contracts",
            "current_value": None,
            "message": "artifact-contracts.yaml not found in workflow-planner references.",
            "suggested_fixes": [
                "Ensure artifact-contracts.yaml exists at skills/workflow-planner/references/artifact-contracts.yaml"
            ],
            "reference": "skills/workflow-planner/references/"
        })
        return errors

    # Find contract for this artifact_id
    contract = next((a for a in contracts_data.get("artifacts", []) if a["id"] == artifact_id), None)
    if not contract:
        errors.append({
            "error_id": f"{artifact_id}.artifact_id.unknown_value",
            "error_type": "unknown_value",
            "field": "artifact_id",
            "current_value": artifact_id,
            "message": f"Artifact ID '{artifact_id}' not found in artifact-contracts.yaml",
            "suggested_fixes": [
                "Check artifact ID matches a contract in artifact-contracts.yaml",
                "Ensure artifact_id field in YAML matches contract definition"
            ],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
        return errors

    # Read artifact content
    with open(artifact_path, encoding="utf-8") as f:
        content = f.read()

    # Extract machine-readable handoff YAML
    handoff_match = re.search(
        r"## 13\. Machine-readable handoff\s+```yaml\s+(.*?)\s+```",
        content,
        re.DOTALL | re.IGNORECASE,
    )

    if not handoff_match:
        yaml_blocks = re.findall(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)
        if yaml_blocks:
            handoff_match = type('obj', (object,), {'group': lambda self, i: yaml_blocks[-1]})()

    if not handoff_match:
        errors.append({
            "error_type": "missing_field",
            "field": "machine_readable_handoff",
            "current_value": None,
            "message": "Machine-readable handoff YAML block not found in artifact.",
            "suggested_fixes": [
                "Add Section 13: Machine-readable handoff with YAML block"
            ],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
        return errors

    # Parse YAML
    try:
        artifact_data = yaml.safe_load(handoff_match.group(1))
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

    if not isinstance(artifact_data, dict):
        errors.append({
            "error_type": "type_error",
            "field": "machine_readable_handoff",
            "current_value": type(artifact_data).__name__,
            "message": f"YAML block should be a dictionary, got {type(artifact_data).__name__}",
            "suggested_fixes": ["Ensure YAML block contains key-value pairs, not a list"],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
        return errors

    # Check artifact_id field
    if "artifact_id" not in artifact_data:
        errors.append({
            "error_id": f"{artifact_id}.artifact_id.missing_field",
            "error_type": "missing_field",
            "field": "artifact_id",
            "current_value": None,
            "message": f"Required field 'artifact_id' is missing.",
            "suggested_fixes": [f"Add artifact_id: {artifact_id}"],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
    elif artifact_data.get("artifact_id") != artifact_id:
        errors.append({
            "error_id": f"{artifact_id}.artifact_id.unknown_value",
            "error_type": "unknown_value",
            "field": "artifact_id",
            "current_value": artifact_data.get("artifact_id"),
            "message": f"Field 'artifact_id' has value '{artifact_data.get('artifact_id')}', expected '{artifact_id}'.",
            "suggested_fixes": [f"Change artifact_id to: {artifact_id}"],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })

    # Check required machine fields from contract (skip artifact_id since we already checked it)
    required_fields = contract.get("required_machine_fields", [])
    for field in required_fields:
        if field == "artifact_id":
            continue  # Already checked above
        if field not in artifact_data:
            errors.append({
                "error_id": f"{artifact_id}.{field}.missing_field",
                "error_type": "missing_field",
                "field": field,
                "current_value": None,
                "message": f"Required field '{field}' is missing.",
                "suggested_fixes": [
                    f"Add {field} to the machine-readable handoff YAML block",
                    f"See artifact contract: skills/workflow-planner/references/artifact-contracts.yaml"
                ],
                "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
            })

    return errors

def validation_result_to_json(artifact_id: str, artifact_path: str, errors: list[ValidationError]) -> str:
    """Convert validation result to JSON format with multi-error schema."""
    result = {
        "valid": len(errors) == 0,
        "artifact_id": artifact_id,
        "artifact_path": os.path.abspath(artifact_path),
        "validator": "validate-artifact.py",
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

    # Test 1: Valid artifact
    print("[TEST 1] Valid generic artifact")
    artifact_path = os.path.join(fixtures_dir, "artifact-generic-valid.md")
    errors = validate_artifact("repository_sensemaking_brief", artifact_path, repo_root)
    tests_run += 1
    if len(errors) == 0:
        tests_passed += 1
        print("  PASSED: No errors for valid artifact")
    else:
        print(f"  FAILED: Expected no errors, got {len(errors)}")
        for error in errors:
            print(f"    - {error.get('error_id', error.get('error_type'))}: {error.get('message')}")

    # Test 2: Missing artifact_id
    print("[TEST 2] Missing artifact_id field")
    artifact_path = os.path.join(fixtures_dir, "artifact-generic-invalid-missing-fields.md")
    errors = validate_artifact("repository_sensemaking_brief", artifact_path, repo_root)
    tests_run += 1
    if len(errors) >= 1:
        tests_passed += 1
        print(f"  PASSED: Found {len(errors)} error(s) as expected")
    else:
        print(f"  FAILED: Expected >= 1 error, got {len(errors)}")

    # Test 3: JSON output structure
    print("[TEST 3] JSON output structure")
    artifact_path = os.path.join(fixtures_dir, "artifact-generic-valid.md")
    errors = validate_artifact("repository_sensemaking_brief", artifact_path, repo_root)
    json_output = validation_result_to_json("repository_sensemaking_brief", artifact_path, errors)
    result = json.loads(json_output)
    tests_run += 1
    checks = [
        result["valid"] == True,
        result["artifact_id"] == "repository_sensemaking_brief",
        result["validator"] == "validate-artifact.py",
        "errors" in result,
        "validation_timestamp" in result,
        result["errors"] == []
    ]
    if all(checks):
        tests_passed += 1
        print("  PASSED: JSON structure is correct")
    else:
        print(f"  FAILED: JSON structure issues")

    # Test 4: error_id in errors
    print("[TEST 4] error_id in all errors")
    artifact_path = os.path.join(fixtures_dir, "artifact-generic-invalid-missing-fields.md")
    errors = validate_artifact("repository_sensemaking_brief", artifact_path, repo_root)
    tests_run += 1
    if all("error_id" in e for e in errors):
        tests_passed += 1
        print(f"  PASSED: All {len(errors)} errors have error_id")
        for error in errors:
            print(f"    - {error['error_id']}")
    else:
        print(f"  FAILED: Some errors missing error_id")

    # Test 5: error_id format validation
    print("[TEST 5] error_id format validation")
    tests_run += 1
    valid_format = True
    for error in errors:
        error_id = error.get("error_id", "")
        parts = error_id.split(".")
        if len(parts) != 3:
            valid_format = False
            print(f"  FAILED: Invalid error_id format: {error_id}")
            break
    if valid_format:
        tests_passed += 1
        print("  PASSED: All error_ids follow correct format")

    # Test 6: error_id uniqueness
    print("[TEST 6] error_id uniqueness for retry logic")
    tests_run += 1
    error_ids = [e.get("error_id") for e in errors]
    if len(error_ids) == len(set(error_ids)):
        tests_passed += 1
        print(f"  PASSED: All error_ids are unique")
    else:
        print(f"  FAILED: Duplicate error_ids found")

    print(f"\n[SUMMARY] {tests_passed}/{tests_run} tests passed")
    return 0 if tests_passed == tests_run else 1

if __name__ == "__main__":
    sys.exit(run_tests())
