"""Generic Level 2 validator for all artifact types.

This validator checks artifacts against their contracts in artifact-contracts.yaml.
It preserves the two-positional signature (artifact_id + artifact_path) as a documented
exception to the standard single-positional CLI.
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime, timezone
from typing import TypedDict, Any

import yaml

from _validator_utils import (
    format_error,
    load_artifact_contracts,
    load_canonical_vocabulary,
    build_fog_type_normalizer,
)

# Stable error codes
ARTIFACT_FILE_NOT_FOUND = "ARTIFACT_FILE_NOT_FOUND"
CONTRACTS_FILE_NOT_FOUND = "CONTRACTS_FILE_NOT_FOUND"
CONTRACT_NOT_FOUND = "CONTRACT_NOT_FOUND"
ABSOLUTE_FILE_LINK = "ABSOLUTE_FILE_LINK"
MISSING_REQUIRED_SECTION = "MISSING_REQUIRED_SECTION"
MISSING_YAML_BLOCK = "MISSING_YAML_BLOCK"
MISSING_MACHINE_FIELDS = "MISSING_MACHINE_FIELDS"
MISSING_EVIDENCE_EXCERPTS = "MISSING_EVIDENCE_EXCERPTS"
MISSING_EXCERPT_FIELD = "MISSING_EXCERPT_FIELD"
ABSOLUTE_EXCERPT_PATH = "ABSOLUTE_EXCERPT_PATH"
MISSING_RECOMMENDED_FIELD = "MISSING_RECOMMENDED_FIELD"
INVALID_ENUM_VALUE = "INVALID_ENUM_VALUE"
VOCAB_NOT_FOUND = "VOCAB_NOT_FOUND"


class ValidationError(TypedDict, total=False):
    """Structured validation error with all metadata for JSON output."""
    error_id: str  # e.g., <artifact_id>.<field>.<error_type>
    error_type: str  # missing_field, unknown_value, type_error, logic_error, semantic_conflict
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



def validate_artifact(artifact_id: str, artifact_path: str, repo_root: str = ".") -> list[ValidationError]:
    """Validate an artifact against its contract and return structured errors.

    Returns a list of ValidationError dicts. Empty list means validation passed.

    Phase 1 scope: Validate artifact existence, contract match, and required fields.
    """
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
        # Try Section 11 as fallback
        handoff_match = re.search(
            r"## 11\. Machine-readable plan\s+```yaml\s+(.*?)\s+```",
            content,
            re.DOTALL | re.IGNORECASE,
        )

    # Try generic YAML block if neither section found
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
                "Add Section 13: Machine-readable handoff with YAML block",
                "Or add Section 11: Machine-readable plan with YAML block"
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

    # --- PHASE 1 REQUIRED FIELD CHECKS ---
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


def validation_result_to_json(
    artifact_id: str,
    artifact_path: str,
    errors: list[ValidationError],
) -> str:
    """Convert validation result to JSON format with multi-error schema."""
    result: ValidationResult = {
        "valid": len(errors) == 0,
        "artifact_id": artifact_id,
        "artifact_path": os.path.abspath(artifact_path),
        "validator": "validate-artifact.py",
        "errors": errors,
        "validation_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }

    return json.dumps(result, indent=2, default=str)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an artifact against its contract.")
    parser.add_argument("artifact_id", help="The ID of the artifact (e.g., repository_sensemaking_brief)")
    parser.add_argument("artifact_path", nargs="?", help="Path to the artifact markdown file")
    parser.add_argument("--repo-root", default=".", help="Root directory of the repository")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--list-codes", action="store_true", help="List all error codes and exit")
    args = parser.parse_args(argv)

    if args.list_codes:
        codes = [
            ARTIFACT_FILE_NOT_FOUND,
            CONTRACTS_FILE_NOT_FOUND,
            CONTRACT_NOT_FOUND,
            ABSOLUTE_FILE_LINK,
            MISSING_REQUIRED_SECTION,
            MISSING_YAML_BLOCK,
            MISSING_MACHINE_FIELDS,
            MISSING_RECOMMENDED_FIELD,
            MISSING_EVIDENCE_EXCERPTS,
            MISSING_EXCERPT_FIELD,
            ABSOLUTE_EXCERPT_PATH,
            INVALID_ENUM_VALUE,
            VOCAB_NOT_FOUND,
        ]
        print("Stable error codes for artifact validation:")
        for code in codes:
            print(f"  {code}")
        return 0

    if not args.artifact_path:
        parser.print_usage()
        return 1

    errors = validate_artifact(args.artifact_id, args.artifact_path, args.repo_root)

    if args.json:
        print(validation_result_to_json(args.artifact_id, args.artifact_path, errors))
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
            print("Artifact validation passed! All required fields are present and valid.")
            return 0


if __name__ == "__main__":
    sys.exit(main())
