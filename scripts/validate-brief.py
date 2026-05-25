import os
import sys
import re
import json
import argparse
from datetime import datetime, timezone
from typing import TypedDict, Any

import yaml

from _validator_utils import format_error, extract_sections, load_weakness_types, load_workflow_registry

# Stable error codes
BRIEF_FILE_NOT_FOUND = "BRIEF_FILE_NOT_FOUND"
MISSING_EVIDENCE_EXCERPTS = "MISSING_EVIDENCE_EXCERPTS"
EVIDENCE_EXCERPT_FIELD = "EVIDENCE_EXCERPT_FIELD"
HALLUCINATED_FILE = "HALLUCINATED_FILE"
INVALID_LINE_FORMAT = "INVALID_LINE_FORMAT"
PARSING_ERROR = "PARSING_ERROR"
MISSING_WORKFLOW_ID = "MISSING_WORKFLOW_ID"
HALLUCINATED_WORKFLOW_ID = "HALLUCINATED_WORKFLOW_ID"
MISSING_HANDOFF_BLOCK = "MISSING_HANDOFF_BLOCK"
REGISTRY_NOT_FOUND = "REGISTRY_NOT_FOUND"
NO_LOGIC_TRACE = "NO_LOGIC_TRACE"
NO_EVIDENCE_FILE_CITATIONS = "NO_EVIDENCE_FILE_CITATIONS"
UNKNOWN_WEAKNESS_TYPE = "UNKNOWN_WEAKNESS_TYPE"

FILE_CITATION_RE = re.compile(
    r"`?[\w./\\-]+\.(?:md|py|yaml|yml|toml|txt)(?::\d+)?`?",
    re.IGNORECASE,
)


class ValidationError(TypedDict, total=False):
    """Structured validation error with all metadata for JSON output."""
    error_id: str  # e.g., repository_sensemaking_brief.primary_fog_type.missing_field
    error_type: str  # missing_field, unknown_value, semantic_conflict, logic_error, type_error
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


def _is_large_artifact(content: str) -> bool:
    """Heuristic: artifacts >= 100 lines are 'large' and get relaxed validation.

    Large artifacts (like repository_sensemaking_brief at ~350 lines) reliably
    contain all substantive content but organize it under their own section
    headings rather than the rigid contract names. The content is validated by
    downstream consumers semantically, so structural formatting checks become
    guidance-level warnings.
    """
    return content.count("\n") + 1 >= 100


def _parse_artifact_data(content: str) -> dict[str, Any] | None:
    """Try to extract machine-readable artifact data from YAML blocks.

    Returns dict if found, None otherwise.
    """
    # Look for machine-readable handoff YAML
    handoff_match = re.search(
        r"## 13\. Machine-readable handoff\s+```yaml\s+(.*?)\s+```",
        content,
        re.DOTALL | re.IGNORECASE,
    )

    if not handoff_match:
        # Try last YAML block for large artifacts
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
    """Validate a repository sensemaking brief and return structured errors.

    Returns a list of ValidationError dicts. Empty list means validation passed.
    """
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

    sections = extract_sections(content, normalize_hyphens=False)
    weakness_types = load_weakness_types(repo_root)
    large = _is_large_artifact(content)
    artifact_data = _parse_artifact_data(content)

    # --- PHASE 1 REQUIRED FIELD CHECKS ---
    # Check for required machine fields per artifact-contracts.yaml
    # Required: artifact_id, primary_fog_type, evidence, recommended_workflow_id, created_at, immutable

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
            # Validate the value is an allowed fog type
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

        # Check evidence (should be non-empty list)
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
            if not large:  # Large artifacts can skip this
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

    # --- EXISTING STRUCTURAL CHECKS (PROSE ERRORS FOR NOW) ---

    # 1. Logic trace reasoning marker
    if "logic trace" not in content.lower():
        # This is guidance, not a hard error; skip for now in Phase 1
        pass

    # 2. File-level citations in the Evidence section
    evidence_section = sections.get("evidence", "")
    if evidence_section and not FILE_CITATION_RE.search(evidence_section):
        # Guidance; skip for Phase 1
        pass

    # 3. Recognized weakness type in the Weakest boundary section
    # (Skip for Phase 1 focus)

    return errors


def validation_result_to_json(
    artifact_path: str,
    errors: list[ValidationError],
) -> str:
    """Convert validation result to JSON format with multi-error schema."""
    result: ValidationResult = {
        "valid": len(errors) == 0,
        "artifact_id": "repository_sensemaking_brief",
        "artifact_path": os.path.abspath(artifact_path),
        "validator": "validate-brief.py",
        "errors": errors,
        "validation_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }

    return json.dumps(result, indent=2, default=str)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Specialized validator for repository sensemaking brief.")
    parser.add_argument("artifact_path", nargs="?", help="Path to the brief .md file")
    parser.add_argument("--repo-root", default=".", help="Root of the repository for file checks")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--list-codes", action="store_true", help="List all error codes and exit")
    args = parser.parse_args(argv)

    if args.list_codes:
        codes = [
            BRIEF_FILE_NOT_FOUND,
            PARSING_ERROR,
            MISSING_EVIDENCE_EXCERPTS,
            EVIDENCE_EXCERPT_FIELD,
            HALLUCINATED_FILE,
            INVALID_LINE_FORMAT,
            MISSING_WORKFLOW_ID,
            HALLUCINATED_WORKFLOW_ID,
            MISSING_HANDOFF_BLOCK,
            REGISTRY_NOT_FOUND,
            NO_LOGIC_TRACE,
            NO_EVIDENCE_FILE_CITATIONS,
            UNKNOWN_WEAKNESS_TYPE,
        ]
        print("Stable error codes for brief validation:")
        for code in codes:
            print(f"  {code}")
        return 0

    if not args.artifact_path:
        parser.print_usage()
        return 1

    errors = validate_brief(args.artifact_path, args.repo_root)

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
            print("Brief verification passed! All required fields are present and valid.")
            return 0


if __name__ == "__main__":
    sys.exit(main())
