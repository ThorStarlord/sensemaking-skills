"""Single agent-facing validation entrypoint.

This helper:
1. Accepts an artifact path
2. Determines which validator to use based on artifact_id
3. Invokes the appropriate validator with --json
4. Returns unified structured JSON
5. Wraps errors in the same schema for consistent parsing

Purpose: Agents call this one script, get structured JSON back, and never
need to worry about which validator to invoke.
"""

import os
import sys
import json
import re
import subprocess
import argparse
from datetime import datetime, timezone
from typing import TypedDict, Any

import yaml


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


def extract_artifact_id(artifact_path: str) -> str | None:
    """Extract artifact_id from the artifact's YAML block.

    Returns the artifact_id if found, None otherwise.
    """
    if not os.path.exists(artifact_path):
        return None

    try:
        with open(artifact_path, encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return None

    # Try Section 13 first
    handoff_match = re.search(
        r"## 13\. Machine-readable handoff\s+```yaml\s+(.*?)\s+```",
        content,
        re.DOTALL | re.IGNORECASE,
    )

    # Fall back to Section 11
    if not handoff_match:
        handoff_match = re.search(
            r"## 11\. Machine-readable plan\s+```yaml\s+(.*?)\s+```",
            content,
            re.DOTALL | re.IGNORECASE,
        )

    # Fall back to any YAML block
    if not handoff_match:
        yaml_blocks = re.findall(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)
        if yaml_blocks:
            handoff_match = type('obj', (object,), {'group': lambda self, i: yaml_blocks[-1]})()

    if not handoff_match:
        return None

    try:
        yaml_data = yaml.safe_load(handoff_match.group(1))
        if isinstance(yaml_data, dict):
            return yaml_data.get("artifact_id")
    except Exception:
        pass

    return None


def select_validator(artifact_id: str | None) -> str:
    """Select which validator to use based on artifact_id.

    Returns the path to the validator script.
    """
    if artifact_id == "repository_sensemaking_brief":
        return "scripts/validate-brief.py"
    elif artifact_id == "workflow_orchestration_plan":
        return "scripts/validate-plan.py"
    elif artifact_id == "architectural_review_recommendation":
        return "scripts/validate-architectural-review-recommendation.py"
    else:
        # Generic fallback (requires both artifact_id and path)
        return "scripts/validate-artifact.py"


def invoke_validator(
    validator_path: str,
    artifact_id: str | None,
    artifact_path: str,
    repo_root: str = ".",
) -> ValidationResult:
    """Invoke a specific validator with --json and return the result.

    Args:
        validator_path: Path to the validator script (e.g., scripts/validate-brief.py)
        artifact_id: The artifact ID (may be None for generic validator)
        artifact_path: Path to the artifact to validate
        repo_root: Repository root for relative path resolution

    Returns:
        ValidationResult with all errors and metadata
    """
    try:
        # Build command
        if validator_path == "scripts/validate-artifact.py":
            # Generic validator requires artifact_id as positional arg
            if not artifact_id:
                # Can't determine artifact_id, return error
                return {
                    "valid": False,
                    "artifact_id": "unknown",
                    "artifact_path": os.path.abspath(artifact_path),
                    "validator": "validate-and-report.py",
                    "errors": [
                        {
                            "error_id": "unknown.artifact_id.missing_field",
                            "error_type": "missing_field",
                            "field": "artifact_id",
                            "current_value": None,
                            "message": "Cannot determine artifact_id from file. Generic validator requires artifact_id to be present in YAML block.",
                            "suggested_fixes": [
                                "Add artifact_id field to machine-readable handoff YAML block"
                            ],
                            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
                        }
                    ],
                    "validation_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
                }

            cmd = [
                "python3",
                validator_path,
                artifact_id,
                artifact_path,
                "--repo-root", repo_root,
                "--json"
            ]
        else:
            # Specific validators (brief, plan) take only artifact_path
            cmd = [
                "python3",
                validator_path,
                artifact_path,
                "--repo-root", repo_root,
                "--json"
            ]

        # Run validator
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=repo_root
        )

        # Parse validator output
        try:
            json_output = json.loads(result.stdout)
            return json_output
        except json.JSONDecodeError as e:
            # Validator returned invalid JSON
            return {
                "valid": False,
                "artifact_id": artifact_id or "unknown",
                "artifact_path": os.path.abspath(artifact_path),
                "validator": "validate-and-report.py",
                "errors": [
                    {
                        "error_id": f"{artifact_id or 'unknown'}.validator.execution_error",
                        "error_type": "logic_error",
                        "field": "validator",
                        "current_value": validator_path,
                        "message": f"Validator returned invalid JSON: {str(e)}",
                        "suggested_fixes": [
                            "Run the validator directly with --json",
                            "Check validator stderr for syntax or dependency errors"
                        ],
                        "reference": "docs/validator-json-refactor-guide.md"
                    }
                ],
                "validation_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            }

    except FileNotFoundError:
        return {
            "valid": False,
            "artifact_id": artifact_id or "unknown",
            "artifact_path": os.path.abspath(artifact_path),
            "validator": "validate-and-report.py",
            "errors": [
                {
                    "error_id": f"{artifact_id or 'unknown'}.validator.execution_error",
                    "error_type": "logic_error",
                    "field": "validator",
                    "current_value": validator_path,
                    "message": f"Validator not found: {validator_path}",
                    "suggested_fixes": [
                        "Ensure validator script exists",
                        "Check scripts directory path"
                    ],
                    "reference": "docs/validator-json-refactor-guide.md"
                }
            ],
            "validation_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }

    except Exception as e:
        return {
            "valid": False,
            "artifact_id": artifact_id or "unknown",
            "artifact_path": os.path.abspath(artifact_path),
            "validator": "validate-and-report.py",
            "errors": [
                {
                    "error_id": f"{artifact_id or 'unknown'}.validator.execution_error",
                    "error_type": "logic_error",
                    "field": "validator",
                    "current_value": validator_path,
                    "message": f"Validator failed to execute: {str(e)}",
                    "suggested_fixes": [
                        "Run the validator directly with --json",
                        "Check validator stderr for syntax or dependency errors"
                    ],
                    "reference": "docs/validator-json-refactor-guide.md"
                }
            ],
            "validation_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }


def validate_and_report(artifact_path: str, repo_root: str = ".") -> ValidationResult:
    """Validate an artifact and return unified structured JSON.

    This is the main agent-facing function. It:
    1. Extracts artifact_id from the file
    2. Selects the appropriate validator
    3. Invokes it with --json
    4. Returns the result (or wrapped error if validator fails)

    Args:
        artifact_path: Path to the artifact to validate
        repo_root: Repository root for relative path resolution

    Returns:
        ValidationResult with all errors in unified schema
    """
    # Check file exists
    if not os.path.exists(artifact_path):
        return {
            "valid": False,
            "artifact_id": "unknown",
            "artifact_path": os.path.abspath(artifact_path),
            "validator": "validate-and-report.py",
            "errors": [
                {
                    "error_type": "missing_field",
                    "field": "artifact",
                    "current_value": None,
                    "message": f"Artifact file not found: {artifact_path}",
                    "suggested_fixes": [f"Ensure artifact exists at: {artifact_path}"],
                    "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
                }
            ],
            "validation_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }

    # Extract artifact_id from the file
    artifact_id = extract_artifact_id(artifact_path)

    # Select appropriate validator
    validator_path = select_validator(artifact_id)

    # Invoke validator and return result
    return invoke_validator(validator_path, artifact_id, artifact_path, repo_root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate any Phase 1 artifact and return unified structured JSON."
    )
    parser.add_argument("artifact_path", help="Path to the artifact markdown file")
    parser.add_argument("--repo-root", default=".", help="Root directory of the repository")
    args = parser.parse_args(argv)

    result = validate_and_report(args.artifact_path, args.repo_root)

    # Always output JSON
    print(json.dumps(result, indent=2, default=str))

    # Exit codes:
    # 0 = artifact valid
    # 1 = artifact invalid but JSON returned successfully
    # 2 = helper/validator execution failure (error from validate-and-report.py itself)
    if result["valid"]:
        return 0
    elif result["validator"] == "validate-and-report.py":
        # This is a helper/execution error (not a validation error)
        return 2
    else:
        # This is a validation error (artifact invalid but validator succeeded)
        return 1


if __name__ == "__main__":
    sys.exit(main())
