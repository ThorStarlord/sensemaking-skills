"""Single agent-facing validation entrypoint.

The router extracts ``artifact_id`` only from the authoritative machine-readable
handoff/plan/decision block, selects a canonical validator, executes it, and
returns one structured JSON result. Routing does not establish semantic truth.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any, TypedDict

import yaml


class ValidationError(TypedDict, total=False):
    error_id: str
    error_type: str
    field: str | None
    current_value: Any
    message: str
    suggested_fixes: list[str]
    reference: str


class ValidationResult(TypedDict):
    valid: bool
    artifact_id: str
    artifact_path: str
    validator: str
    errors: list[ValidationError]
    validation_timestamp: str


_AUTHORITATIVE_HEADING_PATTERNS = [
    r"## (?:\d+\.\s*)?Machine-readable (?:handoff|plan|decision)",
]
_ARTIFACT_ID_LINE_RE = re.compile(
    r'^[ \t]*artifact_id[ \t]*:[ \t]*["\']?([A-Za-z0-9_\-.]+)["\']?[ \t]*$',
    re.MULTILINE,
)
_PM_ARTIFACT_IDS = {
    "persona_definition",
    "discovery_findings",
    "synthesis_report",
    "opportunity_map",
    "hypothesis_statement",
}
_PM_FEATURE_DEFINITION_IDS = {
    "story_list",
    "criteria_list",
    "risk_analysis",
}


class ArtifactIdExtraction:
    __slots__ = ("status", "artifact_id", "detail")

    def __init__(self, status: str, artifact_id: str | None = None, detail: str = ""):
        self.status = status
        self.artifact_id = artifact_id
        self.detail = detail


def _find_authoritative_blocks(content: str) -> list[str]:
    for heading_pattern in _AUTHORITATIVE_HEADING_PATTERNS:
        pattern = heading_pattern + r"\s+```yaml\s+(.*?)\s+```"
        blocks = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        if blocks:
            return blocks
    return []


def _resolve_line_matches(matches: list[str]) -> ArtifactIdExtraction:
    unique_values = list(dict.fromkeys(matches))
    if len(unique_values) == 1:
        if len(matches) > 1:
            return ArtifactIdExtraction(
                "duplicate_key",
                artifact_id=unique_values[0],
                detail=f"artifact_id repeated {len(matches)} times with the same value",
            )
        return ArtifactIdExtraction("ok", artifact_id=unique_values[0])
    return ArtifactIdExtraction(
        "conflicting_artifact_id",
        detail=f"artifact_id has conflicting values: {unique_values}",
    )


def _extract_artifact_id_from_block(block_text: str) -> ArtifactIdExtraction:
    line_matches = _ARTIFACT_ID_LINE_RE.findall(block_text)
    if len(line_matches) > 1:
        return _resolve_line_matches(line_matches)

    try:
        yaml_data = yaml.safe_load(block_text)
    except Exception as exc:
        matches = _ARTIFACT_ID_LINE_RE.findall(block_text)
        if not matches:
            return ArtifactIdExtraction(
                "malformed_authoritative_yaml",
                detail=f"YAML parse error in authoritative handoff block: {exc}",
            )
        return _resolve_line_matches(matches)

    if isinstance(yaml_data, dict):
        if "artifact_id" not in yaml_data:
            return ArtifactIdExtraction("missing_field")
        value = yaml_data.get("artifact_id")
        if not isinstance(value, str) or not value:
            return ArtifactIdExtraction("missing_field")
        return ArtifactIdExtraction("ok", artifact_id=value)

    matches = _ARTIFACT_ID_LINE_RE.findall(block_text)
    if not matches:
        return ArtifactIdExtraction("missing_field")
    return _resolve_line_matches(matches)


def extract_artifact_id_detailed(artifact_path: str) -> ArtifactIdExtraction:
    if not os.path.exists(artifact_path):
        return ArtifactIdExtraction(
            "no_authoritative_block", detail="artifact file not found"
        )
    try:
        with open(artifact_path, encoding="utf-8") as handle:
            content = handle.read()
    except Exception as exc:
        return ArtifactIdExtraction(
            "no_authoritative_block", detail=f"could not read file: {exc}"
        )

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
    result = extract_artifact_id_detailed(artifact_path)
    return result.artifact_id if result.status in ("ok", "duplicate_key") else None


_ROUTING_ERROR_TAXONOMY = {
    "no_authoritative_block": (
        "no_authoritative_block",
        "No authoritative machine-readable handoff block found (expected a \"## 13. Machine-readable handoff\" or \"## 11. Machine-readable plan\" section containing a ```yaml fence).",
        ["Add the authoritative machine-readable handoff section with a ```yaml fence"],
    ),
    "ambiguous_authoritative_blocks": (
        "ambiguous_authoritative_blocks",
        "Multiple authoritative machine-readable handoff blocks were found; exactly one is required.",
        ["Remove duplicate machine-readable handoff sections so only one authoritative block remains"],
    ),
    "malformed_authoritative_yaml": (
        "malformed_authoritative_yaml",
        "The authoritative machine-readable handoff block's YAML could not be parsed and no artifact_id could be recovered.",
        ["Fix the YAML syntax error in the authoritative handoff block (check for unescaped quotes/characters)"],
    ),
    "missing_field": (
        "missing_field",
        "Cannot determine artifact_id from the authoritative machine-readable handoff block: the field is not present.",
        ["Add artifact_id field to the authoritative machine-readable handoff YAML block"],
    ),
    "duplicate_key": (
        "duplicate_key",
        "artifact_id appears more than once in the authoritative handoff block (with the same value); duplicate keys are not permitted.",
        ["Remove the duplicate artifact_id key so it appears exactly once"],
    ),
    "conflicting_artifact_id": (
        "conflicting_value",
        "artifact_id appears more than once in the authoritative handoff block with conflicting values; the router will not silently pick one.",
        ["Resolve the conflicting artifact_id values so exactly one value is present"],
    ),
}


def _routing_error_result(status: str, detail: str, artifact_path: str) -> ValidationResult:
    error_suffix, message, suggested_fixes = _ROUTING_ERROR_TAXONOMY.get(
        status,
        (
            "missing_field",
            "Cannot determine artifact_id from file.",
            ["Add artifact_id field to machine-readable handoff YAML block"],
        ),
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
                "error_type": "missing_field"
                if error_suffix in ("missing_field", "no_authoritative_block")
                else "logic_error",
                "field": "artifact_id",
                "current_value": None,
                "message": full_message,
                "suggested_fixes": suggested_fixes,
                "reference": "skills/workflow-planner/references/artifact-contracts.yaml",
            }
        ],
        "validation_timestamp": datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
    }


def select_validator(artifact_id: str | None) -> str:
    if artifact_id == "repository_sensemaking_brief":
        return "scripts/validate-brief.py"
    if artifact_id == "workflow_orchestration_plan":
        return "scripts/validate-plan.py"
    if artifact_id == "architectural_review_recommendation":
        return "scripts/validate-architectural-review-recommendation.py"
    if artifact_id in _PM_ARTIFACT_IDS:
        return "scripts/validate-pm-artifact.py"
    if artifact_id in _PM_FEATURE_DEFINITION_IDS:
        return "scripts/validate-pm-feature-definition.py"
    return "scripts/validate-artifact.py"


def invoke_validator(
    validator_path: str,
    artifact_id: str | None,
    artifact_path: str,
    repo_root: str = ".",
    target_repo: str | None = None,
    probe_report: str | None = None,
) -> ValidationResult:
    try:
        if validator_path == "scripts/validate-artifact.py":
            if not artifact_id:
                return _routing_error_result("missing_field", "", artifact_path)
            cmd = [
                sys.executable,
                validator_path,
                artifact_id,
                artifact_path,
                "--repo-root",
                repo_root,
                "--json",
            ]
        else:
            cmd = [
                sys.executable,
                validator_path,
                artifact_path,
                "--repo-root",
                repo_root,
                "--json",
            ]
            if target_repo and validator_path.endswith("validate-brief.py"):
                cmd.extend(["--target-repo", target_repo])
            if probe_report and validator_path.endswith("validate-brief.py"):
                cmd.extend(["--probe-report", probe_report])

        completed = subprocess.run(
            cmd, capture_output=True, text=True, cwd=repo_root, check=False
        )
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
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
                        "message": f"Validator returned invalid JSON: {exc}",
                        "suggested_fixes": [
                            "Run the validator directly with --json",
                            "Check validator stderr for syntax or dependency errors",
                        ],
                        "reference": "docs/validator-json-refactor-guide.md",
                    }
                ],
                "validation_timestamp": datetime.now(timezone.utc)
                .isoformat()
                .replace("+00:00", "Z"),
            }
        return payload
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
                        "Check scripts directory path",
                    ],
                    "reference": "docs/validator-json-refactor-guide.md",
                }
            ],
            "validation_timestamp": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
        }
    except Exception as exc:
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
                    "message": f"Validator failed to execute: {exc}",
                    "suggested_fixes": [
                        "Run the validator directly with --json",
                        "Check validator stderr for syntax or dependency errors",
                    ],
                    "reference": "docs/validator-json-refactor-guide.md",
                }
            ],
            "validation_timestamp": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
        }


def validate_and_report(
    artifact_path: str,
    repo_root: str = ".",
    target_repo: str | None = None,
    probe_report: str | None = None,
) -> ValidationResult:
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
                    "reference": "skills/workflow-planner/references/artifact-contracts.yaml",
                }
            ],
            "validation_timestamp": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
        }

    extraction = extract_artifact_id_detailed(artifact_path)
    if extraction.status != "ok":
        return _routing_error_result(
            extraction.status, extraction.detail, artifact_path
        )
    artifact_id = extraction.artifact_id
    validator_path = select_validator(artifact_id)
    return invoke_validator(
        validator_path,
        artifact_id,
        artifact_path,
        repo_root,
        target_repo,
        probe_report,
    )


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
    parser.add_argument(
        "--probe-report",
        default=None,
        help="Explicit same-episode local Probe Engine report path forwarded to validate-brief.py",
    )
    args = parser.parse_args(argv)
    result = validate_and_report(
        args.artifact_path, args.repo_root, args.target_repo, args.probe_report
    )
    print(json.dumps(result, indent=2, default=str))
    if result["valid"]:
        return 0
    if result["validator"] == "validate-and-report.py":
        return 2
    return 1


if __name__ == "__main__":
    sys.exit(main())
