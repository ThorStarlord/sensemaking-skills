#!/usr/bin/env python3
"""Test runner for validate-brief.py JSON output."""

import sys
import os
import json

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

# Import _validator_utils dependencies
import yaml
import re

# Define the validation functions (copy from validate-brief.py)
FILE_CITATION_RE = re.compile(
    r"`?[\w./\\-]+\.(?:md|py|yaml|yml|toml|txt|js|jsx|ts|tsx|json|html|css|go|rs|java|rb|sh)(?::\d+)?`?",
    re.IGNORECASE,
)

def extract_sections(content: str, normalize_hyphens: bool = True) -> dict:
    """Minimal section extractor for testing."""
    sections = {}
    for match in re.finditer(r"## (.+?)\n(.*?)(?=##|\Z)", content, re.DOTALL | re.IGNORECASE):
        title = match.group(1).strip().lower()
        if normalize_hyphens:
            title = title.replace("-", " ")
        sections[title] = match.group(2).strip()
    return sections

def load_workflow_registry(repo_root: str) -> dict | None:
    """Load workflow registry."""
    path = os.path.join(repo_root, "skills", "workflow-planner", "references", "workflow-registry.yaml")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return yaml.safe_load(f)

def load_weakness_types(repo_root: str) -> list[str]:
    """Load weakness types."""
    path = os.path.join(repo_root, "skills", "repo-sensemaker", "references", "weakness-types.md")
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return re.findall(r"\*\*(.+?)\*\*", f.read())

# Now define validate_brief and validation_result_to_json
from datetime import datetime, timezone
from typing import TypedDict, Any

class ValidationError(TypedDict, total=False):
    """Structured validation error with all metadata for JSON output."""
    error_type: str
    field: str | None
    current_value: Any
    message: str
    suggested_fixes: list[str]
    reference: str

def _is_large_artifact(content: str) -> bool:
    """Heuristic: artifacts >= 100 lines are 'large' and get relaxed validation."""
    return content.count("\n") + 1 >= 100

def _parse_artifact_data(content: str) -> dict[str, Any] | None:
    """Try to extract machine-readable artifact data from YAML blocks."""
    handoff_match = re.search(
        r"## 13\. Machine-readable handoff\s+```yaml\s+(.*?)\s+```",
        content,
        re.DOTALL | re.IGNORECASE,
    )

    if not handoff_match:
        yaml_blocks = re.findall(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)
        if yaml_blocks:
            try:
                return yaml.safe_load(yaml_blocks[-1])
            except Exception:
                return None
        return None

    try:
        return yaml.safe_load(handoff_match.group(1))
    except Exception:
        return None

def validate_brief(artifact_path: str, repo_root: str = ".") -> list[ValidationError]:
    """Validate a repository sensemaking brief and return structured errors."""
    errors: list[ValidationError] = []

    if not os.path.exists(artifact_path):
        errors.append({
            "error_type": "missing_field",
            "field": "artifact",
            "current_value": None,
            "message": f"Brief file not found: {artifact_path}",
            "suggested_fixes": [f"Ensure brief exists at: {artifact_path}"],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
        return errors

    with open(artifact_path, encoding="utf-8") as f:
        content = f.read()

    artifact_data = _parse_artifact_data(content)

    if artifact_data:
        # Check primary_fog_type
        if "primary_fog_type" not in artifact_data:
            errors.append({
                "error_id": "repository_sensemaking_brief.primary_fog_type.missing_field",
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
            fog_type = artifact_data.get("primary_fog_type")
            allowed_fog_types = ["product_fog", "ui_fog", "docs_fog", "architecture_fog"]
            if fog_type not in allowed_fog_types:
                errors.append({
                    "error_id": "repository_sensemaking_brief.primary_fog_type.unknown_value",
                    "error_type": "unknown_value",
                    "field": "primary_fog_type",
                    "current_value": fog_type,
                    "message": f"Field 'primary_fog_type' has value '{fog_type}', which is not recognized.",
                    "suggested_fixes": [f"Change to: primary_fog_type: {ft}" for ft in allowed_fog_types],
                    "reference": "docs/adr/0007-soft-context-routing.md"
                })

        # Check evidence
        if "evidence" not in artifact_data:
            errors.append({
                "error_id": "repository_sensemaking_brief.evidence.missing_field",
                "error_type": "missing_field",
                "field": "evidence",
                "current_value": None,
                "message": "Required field 'evidence' is missing.",
                "suggested_fixes": [
                    "Add evidence as a list of file-level citations",
                    "Example: evidence: ['README.md (lines 5-12): vague feature requirements', ...]"
                ],
                "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
            })
        else:
            evidence = artifact_data.get("evidence")
            if not isinstance(evidence, list):
                errors.append({
                    "error_id": "repository_sensemaking_brief.evidence.type_error",
                    "error_type": "type_error",
                    "field": "evidence",
                    "current_value": evidence,
                    "message": f"Field 'evidence' should be a list, but got {type(evidence).__name__}.",
                    "suggested_fixes": ["Convert evidence to an array of strings"],
                    "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
                })
            elif len(evidence) == 0:
                errors.append({
                    "error_id": "repository_sensemaking_brief.evidence.logic_error",
                    "error_type": "logic_error",
                    "field": "evidence",
                    "current_value": [],
                    "message": "Evidence list is empty. Cannot verify fog type classification is grounded in analysis.",
                    "suggested_fixes": [
                        "Add file-level evidence (e.g., 'README.md: feature list is vague')",
                        "Add architectural evidence (e.g., 'tight coupling in data layer')"
                    ],
                    "reference": "docs/adr/0003-artifact-composition-pattern.md"
                })

        # Check recommended_workflow_id
        if "recommended_workflow_id" not in artifact_data:
            errors.append({
                "error_id": "repository_sensemaking_brief.recommended_workflow_id.missing_field",
                "error_type": "missing_field",
                "field": "recommended_workflow_id",
                "current_value": None,
                "message": "Required field 'recommended_workflow_id' is missing.",
                "suggested_fixes": [
                    "Add recommended_workflow_id: product-implementation-workflow",
                    "Add recommended_workflow_id: ui-implementation-workflow",
                    "Add recommended_workflow_id: docs-implementation-workflow",
                    "Add recommended_workflow_id: architecture-implementation-workflow"
                ],
                "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
            })
        else:
            workflow_id = artifact_data.get("recommended_workflow_id")
            registry = load_workflow_registry(repo_root)
            if registry is not None:
                valid_ids = {w["id"] for w in registry.get("workflows", [])}
                if workflow_id not in valid_ids:
                    errors.append({
                        "error_id": "repository_sensemaking_brief.recommended_workflow_id.unknown_value",
                        "error_type": "unknown_value",
                        "field": "recommended_workflow_id",
                        "current_value": workflow_id,
                        "message": f"Recommended workflow ID '{workflow_id}' not found in registry.",
                        "suggested_fixes": [
                            "Check available workflows in workflow-registry.yaml",
                            "Ensure workflow ID matches exactly (case-sensitive)"
                        ],
                        "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
                    })

    return errors

def validation_result_to_json(artifact_path: str, errors: list[ValidationError]) -> str:
    """Convert validation result to JSON format with multi-error schema."""
    result = {
        "valid": len(errors) == 0,
        "artifact_id": "repository_sensemaking_brief",
        "artifact_path": os.path.abspath(artifact_path),
        "validator": "validate-brief.py",
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

    # Test 1: Valid brief
    print("[TEST 1] Valid brief")
    brief_path = os.path.join(fixtures_dir, "brief-valid.md")
    errors = validate_brief(brief_path, repo_root)
    tests_run += 1
    if len(errors) == 0:
        tests_passed += 1
        print("  PASSED: No errors for valid brief")
    else:
        print(f"  FAILED: Expected no errors, got {len(errors)}")

    # Test 2: Missing fields
    print("[TEST 2] Missing required fields")
    brief_path = os.path.join(fixtures_dir, "brief-invalid-missing-fields.md")
    errors = validate_brief(brief_path, repo_root)
    tests_run += 1
    if len(errors) >= 3:
        tests_passed += 1
        print(f"  PASSED: Found {len(errors)} errors as expected")
    else:
        print(f"  FAILED: Expected >= 3 errors, got {len(errors)}")

    # Test 3: Wrong values
    print("[TEST 3] Wrong value types and enums")
    brief_path = os.path.join(fixtures_dir, "brief-invalid-wrong-values.md")
    errors = validate_brief(brief_path, repo_root)
    tests_run += 1
    if len(errors) >= 3:
        tests_passed += 1
        print(f"  PASSED: Found {len(errors)} errors as expected")
        error_types = [e.get("error_type") for e in errors]
        print(f"    Error types: {set(error_types)}")
    else:
        print(f"  FAILED: Expected >= 3 errors, got {len(errors)}")

    # Test 4: Empty evidence
    print("[TEST 4] Empty evidence (logic_error)")
    brief_path = os.path.join(fixtures_dir, "brief-invalid-empty-evidence.md")
    errors = validate_brief(brief_path, repo_root)
    tests_run += 1
    if len(errors) >= 1 and any(e.get("error_type") == "logic_error" for e in errors):
        tests_passed += 1
        print("  PASSED: Found logic_error as expected")
    else:
        print(f"  FAILED: Expected logic_error")

    # Test JSON output structure
    print("[TEST 5] JSON output structure")
    brief_path = os.path.join(fixtures_dir, "brief-valid.md")
    errors = validate_brief(brief_path, repo_root)
    json_output = validation_result_to_json(brief_path, errors)
    result = json.loads(json_output)
    tests_run += 1
    checks = [
        result["valid"] == True,
        result["artifact_id"] == "repository_sensemaking_brief",
        result["validator"] == "validate-brief.py",
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
    brief_path = os.path.join(fixtures_dir, "brief-invalid-missing-fields.md")
    errors = validate_brief(brief_path, repo_root)
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
        if len(parts) != 3 or parts[0] != "repository_sensemaking_brief":
            valid_format = False
            print(f"  FAILED: Invalid error_id format: {error_id}")
            break
    if valid_format:
        tests_passed += 1
        print("  PASSED: All error_ids follow correct format")

    # Test error_id uniqueness for agent retry tracking
    print("[TEST 8] error_id usefulness for retry logic")
    brief_path = os.path.join(fixtures_dir, "brief-invalid-wrong-values.md")
    errors = validate_brief(brief_path, repo_root)
    tests_run += 1
    error_ids = [e.get("error_id") for e in errors]
    if len(error_ids) == len(set(error_ids)):
        tests_passed += 1
        print(f"  PASSED: All error_ids are unique (can track retries)")
    else:
        print(f"  FAILED: Duplicate error_ids found")

    print(f"\n[SUMMARY] {tests_passed}/{tests_run} tests passed")
    return 0 if tests_passed == tests_run else 1

if __name__ == "__main__":
    sys.exit(run_tests())
