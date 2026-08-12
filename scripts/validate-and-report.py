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


# Authoritative machine-readable handoff heading. Every registered artifact
# producer places its handoff YAML under a "## Machine-readable <noun>"
# heading (optionally numbered, e.g. "## 13. Machine-readable handoff" or
# "## Machine-readable Handoff"; the brief and plan producers both currently
# use Section 13 in practice, and older fixtures omit the number entirely).
# The generic router must select THAT block deterministically rather than
# "the first (or last) YAML fence in the document" -- earlier fences (e.g.
# nested YAML examples inside prose/instruction comments, like Section 8's
# evidence-schema example) are not authoritative and must be ignored
# (issue #97). One shared pattern covers all registered artifact types
# instead of a per-artifact special case.
_AUTHORITATIVE_HEADING_PATTERNS = [
    r"## (?:\d+\.\s*)?Machine-readable (?:handoff|plan|decision)",
]

# artifact_id: <value> as its own line, tolerant of quoting. Used as a
# targeted fallback when the authoritative block's full YAML fails to parse
# (see ArtifactIdExtractionResult.MALFORMED_YAML below) so that a syntax
# error in an unrelated field (e.g. an unescaped quote inside `evidence:`)
# does not masquerade as "artifact_id is missing".
_ARTIFACT_ID_LINE_RE = re.compile(
    r'^[ \t]*artifact_id[ \t]*:[ \t]*["\']?([A-Za-z0-9_\-.]+)["\']?[ \t]*$',
    re.MULTILINE,
)


class ArtifactIdExtraction:
    """Structured result of locating artifact_id in the authoritative
    machine-readable handoff block.

    ``status`` is one of:
      - "ok": artifact_id recovered deterministically.
      - "no_authoritative_block": no recognized handoff heading/fence found.
      - "ambiguous_authoritative_blocks": more than one authoritative heading
        matched (e.g. two "## 13. Machine-readable handoff" sections).
      - "malformed_authoritative_yaml": the authoritative block's YAML could
        not be parsed at all, AND a targeted artifact_id line could not be
        recovered either.
      - "missing_field": the authoritative block parsed (or was recovered),
        but no artifact_id field/line is present.
      - "duplicate_key": more than one artifact_id line/key with the SAME
        value was found in the authoritative block.
      - "conflicting_artifact_id": more than one artifact_id line/key with
        DIFFERENT values was found in the authoritative block.
    """

    __slots__ = ("status", "artifact_id", "detail")

    def __init__(self, status: str, artifact_id: str | None = None, detail: str = ""):
        self.status = status
        self.artifact_id = artifact_id
        self.detail = detail


def _find_authoritative_blocks(content: str) -> list[str]:
    """Return the raw YAML text of every authoritative handoff block found.

    Only the FIRST matching heading pattern (Section 13, else Section 11) is
    considered -- a document is not expected to carry both a brief handoff
    and a plan handoff. Within that heading pattern, every matching heading
    occurrence is returned so callers can detect ambiguity (more than one
    "## 13. Machine-readable handoff" section, which should never happen in
    a well-formed artifact).
    """
    for heading_pattern in _AUTHORITATIVE_HEADING_PATTERNS:
        pattern = heading_pattern + r"\s+```yaml\s+(.*?)\s+```"
        blocks = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        if blocks:
            return blocks
    return []


def _extract_artifact_id_from_block(block_text: str) -> ArtifactIdExtraction:
    """Extract artifact_id from a single authoritative block's raw YAML text."""
    # Scan for repeated top-level artifact_id lines FIRST, independent of
    # whether the block's YAML parses. PyYAML's SafeLoader silently resolves
    # duplicate mapping keys (last one wins) rather than raising -- so a
    # conflicting pair of differently-valued artifact_id keys would parse
    # "successfully" and silently pick the last value, which issue #97
    # explicitly forbids ("A conflicting model-provided artifact_id must
    # never silently override runtime authority"). Duplicate/conflicting
    # keys must therefore be caught even on the happy YAML-parse path.
    line_matches = _ARTIFACT_ID_LINE_RE.findall(block_text)
    if len(line_matches) > 1:
        return _resolve_line_matches(line_matches)

    try:
        yaml_data = yaml.safe_load(block_text)
    except Exception as e:
        # The block's YAML is malformed (e.g. an unescaped quote inside an
        # unrelated field such as `evidence:`). Do not silently report this
        # as "missing field" -- attempt a targeted, deterministic recovery
        # of just the artifact_id line so routing can still succeed, while
        # the malformed YAML itself remains a real, reportable defect that
        # the artifact-specific validator will surface downstream.
        matches = _ARTIFACT_ID_LINE_RE.findall(block_text)
        if not matches:
            return ArtifactIdExtraction(
                "malformed_authoritative_yaml",
                detail=f"YAML parse error in authoritative handoff block: {e}",
            )
        return _resolve_line_matches(matches)

    if isinstance(yaml_data, dict):
        if "artifact_id" not in yaml_data:
            return ArtifactIdExtraction("missing_field")
        value = yaml_data.get("artifact_id")
        if not isinstance(value, str) or not value:
            return ArtifactIdExtraction("missing_field")
        return ArtifactIdExtraction("ok", artifact_id=value)

    # Not a mapping at all (e.g. malformed fence captured a bare scalar/list
    # instead of the real block) -- try the same targeted line recovery.
    matches = _ARTIFACT_ID_LINE_RE.findall(block_text)
    if not matches:
        return ArtifactIdExtraction("missing_field")
    return _resolve_line_matches(matches)


def _resolve_line_matches(matches: list[str]) -> ArtifactIdExtraction:
    """Resolve one or more regex-recovered artifact_id line matches into a
    deterministic result: duplicate (same value repeated) vs. conflicting
    (different values) must never be silently collapsed to "the first one".
    """
    unique_values = list(dict.fromkeys(matches))
    if len(unique_values) == 1:
        if len(matches) > 1:
            return ArtifactIdExtraction(
                "duplicate_key", artifact_id=unique_values[0],
                detail=f"artifact_id repeated {len(matches)} times with the same value",
            )
        return ArtifactIdExtraction("ok", artifact_id=unique_values[0])
    return ArtifactIdExtraction(
        "conflicting_artifact_id",
        detail=f"artifact_id has conflicting values: {unique_values}",
    )


def extract_artifact_id_detailed(artifact_path: str) -> ArtifactIdExtraction:
    """Locate the authoritative machine-readable handoff block and extract
    artifact_id from it, returning a structured result that distinguishes
    *why* extraction failed (see ArtifactIdExtraction) instead of collapsing
    every failure mode into "artifact_id is missing" (issue #97).
    """
    if not os.path.exists(artifact_path):
        return ArtifactIdExtraction("no_authoritative_block", detail="artifact file not found")

    try:
        with open(artifact_path, encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return ArtifactIdExtraction("no_authoritative_block", detail=f"could not read file: {e}")

    blocks = _find_authoritative_blocks(content)

    if not blocks:
        return ArtifactIdExtraction("no_authoritative_block")

    if len(blocks) > 1:
        return ArtifactIdExtraction(
            "ambiguous_authoritative_blocks",
            detail=f"found {len(blocks)} authoritative handoff blocks; expected exactly one",
        )

    return _extract_artifact_id_from_block(blocks[0])


def extract_artifact_id(artifact_path: str) -> str | None:
    """Backwards-compatible wrapper: extract artifact_id from the artifact's
    authoritative YAML handoff block, or None if it could not be determined
    for any reason.

    Prefer extract_artifact_id_detailed() for callers that need to report
    *why* extraction failed (no block found vs. malformed YAML vs. missing
    field vs. duplicate/conflicting values).
    """
    result = extract_artifact_id_detailed(artifact_path)
    return result.artifact_id if result.status in ("ok", "duplicate_key") else None


# Error taxonomy for generic-routing failures (issue #97). Each status from
# ArtifactIdExtraction maps to a distinct, stable error_id/message pair so
# "no authoritative block", "malformed YAML", "missing field",
# "duplicate key", "conflicting value", and "ambiguous blocks" are never
# collapsed into a single "unknown.artifact_id.missing_field" unless that is
# genuinely the condition (field truly absent from an otherwise-parseable
# authoritative block).
_ROUTING_ERROR_TAXONOMY = {
    "no_authoritative_block": (
        "no_authoritative_block",
        "No authoritative machine-readable handoff block found "
        "(expected a \"## 13. Machine-readable handoff\" or "
        "\"## 11. Machine-readable plan\" section containing a ```yaml fence).",
        ["Add the authoritative machine-readable handoff section with a ```yaml fence"],
    ),
    "ambiguous_authoritative_blocks": (
        "ambiguous_authoritative_blocks",
        "Multiple authoritative machine-readable handoff blocks were found; "
        "exactly one is required.",
        ["Remove duplicate machine-readable handoff sections so only one authoritative block remains"],
    ),
    "malformed_authoritative_yaml": (
        "malformed_authoritative_yaml",
        "The authoritative machine-readable handoff block's YAML could not "
        "be parsed and no artifact_id could be recovered.",
        ["Fix the YAML syntax error in the authoritative handoff block (check for unescaped quotes/characters)"],
    ),
    "missing_field": (
        "missing_field",
        "Cannot determine artifact_id from the authoritative machine-readable "
        "handoff block: the field is not present.",
        ["Add artifact_id field to the authoritative machine-readable handoff YAML block"],
    ),
    "duplicate_key": (
        "duplicate_key",
        "artifact_id appears more than once in the authoritative handoff "
        "block (with the same value); duplicate keys are not permitted.",
        ["Remove the duplicate artifact_id key so it appears exactly once"],
    ),
    "conflicting_artifact_id": (
        "conflicting_value",
        "artifact_id appears more than once in the authoritative handoff "
        "block with conflicting values; the router will not silently pick one.",
        ["Resolve the conflicting artifact_id values so exactly one value is present"],
    ),
}


def _routing_error_result(status: str, detail: str, artifact_path: str) -> ValidationResult:
    """Build a ValidationResult for a generic-routing failure, using the
    stable error taxonomy above instead of a single collapsed error code.
    """
    error_suffix, message, suggested_fixes = _ROUTING_ERROR_TAXONOMY.get(
        status,
        ("missing_field", "Cannot determine artifact_id from file.", [
            "Add artifact_id field to machine-readable handoff YAML block"
        ]),
    )
    full_message = message if not detail else f"{message} ({detail})"
    return {
        "valid": False,
        "artifact_id": "unknown",
        "artifact_path": os.path.abspath(artifact_path),
        "validator": "validate-and-report.py",
        "errors": [
            {
                "error_id": f"unknown.artifact_id.{error_suffix}",
                "error_type": "missing_field" if error_suffix in ("missing_field", "no_authoritative_block") else "logic_error",
                "field": "artifact_id",
                "current_value": None,
                "message": full_message,
                "suggested_fixes": suggested_fixes,
                "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
            }
        ],
        "validation_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }


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
    target_repo: str | None = None,
) -> ValidationResult:
    """Invoke a specific validator with --json and return the result.

    Args:
        validator_path: Path to the validator script (e.g., scripts/validate-brief.py)
        artifact_id: The artifact ID (may be None for generic validator)
        artifact_path: Path to the artifact to validate
        repo_root: Repository root for relative path resolution
        target_repo: Root of the repository the artifact is ABOUT, if different
            from repo_root (external-repository runs). Passed through to
            validators that support it (currently validate-brief.py).

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
                sys.executable,
                validator_path,
                artifact_id,
                artifact_path,
                "--repo-root", repo_root,
                "--json"
            ]
        else:
            # Specific validators (brief, plan) take only artifact_path
            cmd = [
                sys.executable,
                validator_path,
                artifact_path,
                "--repo-root", repo_root,
                "--json"
            ]
            # validate-brief.py is target_repo-aware: pass the target repo
            # through when it differs from repo_root (external-repo runs) so
            # evidence citations resolve against the repo the brief is about.
            if target_repo and validator_path.endswith("validate-brief.py"):
                cmd.extend(["--target-repo", target_repo])

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


def validate_and_report(
    artifact_path: str,
    repo_root: str = ".",
    target_repo: str | None = None,
) -> ValidationResult:
    """Validate an artifact and return unified structured JSON.

    This is the main agent-facing function. It:
    1. Extracts artifact_id from the file
    2. Selects the appropriate validator
    3. Invokes it with --json
    4. Returns the result (or wrapped error if validator fails)

    Args:
        artifact_path: Path to the artifact to validate
        repo_root: Repository root for relative path resolution
        target_repo: Root of the repository the artifact is ABOUT, if
            different from repo_root (external-repository runs).

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

    # Locate the authoritative machine-readable handoff block and extract
    # artifact_id from it, with a structured reason when that fails (issue
    # #97: a malformed-but-present authoritative block must not be reported
    # the same way as "no block" or "field truly missing").
    extraction = extract_artifact_id_detailed(artifact_path)

    if extraction.status != "ok":
        return _routing_error_result(extraction.status, extraction.detail, artifact_path)

    artifact_id = extraction.artifact_id

    # Select appropriate validator
    validator_path = select_validator(artifact_id)

    # Invoke validator and return result
    return invoke_validator(validator_path, artifact_id, artifact_path, repo_root, target_repo)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate any Phase 1 artifact and return unified structured JSON."
    )
    parser.add_argument("artifact_path", help="Path to the artifact markdown file")
    parser.add_argument("--repo-root", default=".", help="Root directory of the repository")
    parser.add_argument(
        "--target-repo",
        default=None,
        help="Root of the repository the artifact is ABOUT, if different from --repo-root",
    )
    args = parser.parse_args(argv)

    result = validate_and_report(args.artifact_path, args.repo_root, args.target_repo)

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
