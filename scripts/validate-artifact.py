"""Generic Level 2 validator for all artifact types.

This validator checks artifacts against their contracts in artifact-contracts.yaml.
It preserves the two-positional signature (artifact_id + artifact_path) as a documented
exception to the standard single-positional CLI.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

import yaml

from _validator_utils import (
    build_fog_type_normalizer,
    format_error,
    load_artifact_contracts,
    load_canonical_vocabulary,
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

warnings = []  # Collect warnings separately from errors


def _validate_enum_fields(yaml_data, artifact_id, vocab, errors):
    """Validate routing field enum values against canonical vocabulary."""
    if not vocab or not yaml_data:
        return

    routing_fields = {f["field"]: f for f in vocab.get("routing_fields", [])}
    for field_name, field_spec in routing_fields.items():
        if field_name not in yaml_data:
            continue
        value = yaml_data[field_name]
        if value is None:
            continue
        allowed_values = field_spec.get("values", [])
        if not allowed_values:
            continue
        if field_spec.get("type") == "list(enum)":
            if isinstance(value, list):
                for i, item in enumerate(value):
                    if item not in allowed_values:
                        errors.append(
                            format_error(
                                INVALID_ENUM_VALUE,
                                f"Field '{field_name}[{i}]' has invalid value '{item}'. "
                                f"Allowed: {', '.join(str(v) for v in allowed_values)}",
                            )
                        )
        elif value not in allowed_values:
            errors.append(
                format_error(
                    INVALID_ENUM_VALUE,
                    f"Field '{field_name}' has invalid value '{value}'. "
                    f"Allowed: {', '.join(str(v) for v in allowed_values)}",
                )
            )

    fog_type_normalizer = build_fog_type_normalizer(vocab)
    if not fog_type_normalizer:
        return
    for field in ["primary_fog_type"]:
        if field in yaml_data:
            value = yaml_data[field]
            if value and value not in fog_type_normalizer:
                errors.append(
                    format_error(
                        INVALID_ENUM_VALUE,
                        f"Field '{field}' has unknown fog type '{value}'. "
                        f"Must be one of: {', '.join(sorted(fog_type_normalizer.keys()))}",
                    )
                )


def validate_artifact(artifact_id, artifact_path, repo_root=".", strict_recommended=False):
    errors = []

    if not os.path.exists(artifact_path):
        errors.append(
            format_error(
                ARTIFACT_FILE_NOT_FOUND,
                f"Artifact file not found: {artifact_path}",
            )
        )
        return errors

    contracts_data = load_artifact_contracts(repo_root)
    if contracts_data is None:
        errors.append(
            format_error(
                CONTRACTS_FILE_NOT_FOUND,
                "artifact-contracts.yaml not found in workflow-planner references.",
            )
        )
        return errors

    contract = next(
        (a for a in contracts_data.get("artifacts", []) if a["id"] == artifact_id),
        None,
    )
    if not contract:
        errors.append(
            format_error(
                CONTRACT_NOT_FOUND,
                f"Contract for artifact_id '{artifact_id}' not found in artifact-contracts.yaml",
            )
        )
        return errors

    with open(artifact_path, "r", encoding="utf-8") as f:
        content = f.read()

    line_count = content.count("\n") + 1

    if "file:///" in content:
        errors.append(
            format_error(
                ABSOLUTE_FILE_LINK,
                "Absolute 'file:///' links are banned in generated artifacts. Use relative paths.",
            )
        )

    required_sections = contract.get("required_sections", [])
    missing_sections = []
    for section in required_sections:
        section_regex_part = (
            re.escape(section)
            .replace("_", r"[\s_\-]")
            .replace(r"\_", r"[\s_\-]")
        )
        pattern = rf"^##\s+(?:\d+\.\s+)?{section_regex_part}"
        if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            missing_sections.append(section)

    if missing_sections and line_count < 100:
        skill_name = contract.get("produced_by", "unknown")
        template_path = f"skills/{skill_name}/references/{artifact_id}-template.md"
        error_msg = (
            f"Missing {len(missing_sections)} required section(s): "
            f"{', '.join(missing_sections)}\n"
        )
        error_msg += f"Expected template: {template_path}\n"
        error_msg += (
            "Artifact contract: skills/workflow-planner/references/"
            f"artifact-contracts.yaml (id: {artifact_id})"
        )
        errors.append(format_error(MISSING_REQUIRED_SECTION, error_msg))
    elif missing_sections and line_count >= 100:
        warnings.append(
            format_error(
                MISSING_REQUIRED_SECTION,
                f"Large artifact ({line_count} lines) missing {len(missing_sections)} "
                f"required section heading(s): {', '.join(missing_sections)}. "
                "Content is likely present under alternative headings.",
            )
        )

    required_fields = contract.get("required_machine_fields", [])
    recommended_fields = contract.get("recommended_machine_fields", [])
    yaml_data = None

    if required_fields or recommended_fields:
        yaml_blocks = re.findall(r"---\s+(.*?)\s+---", content, re.DOTALL)
        yaml_blocks += re.findall(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)

        if not yaml_blocks:
            errors.append(
                format_error(MISSING_YAML_BLOCK, "Missing machine-readable YAML block")
            )
        else:
            found_valid_block = False
            for yaml_text in yaml_blocks:
                try:
                    data = yaml.safe_load(yaml_text)
                    if isinstance(data, dict):
                        missing = [f for f in required_fields if f not in data]
                        if not missing:
                            found_valid_block = True
                            yaml_data = data
                            break
                except Exception:
                    pass

            if not found_valid_block:
                has_any_yaml = False
                has_source_ref = False
                for yaml_text in yaml_blocks:
                    try:
                        data = yaml.safe_load(yaml_text)
                        if isinstance(data, dict):
                            has_any_yaml = True
                            if "source_intent_ref" in data:
                                has_source_ref = True
                                yaml_data = data
                                break
                    except Exception:
                        pass

                if not has_any_yaml:
                    errors.append(
                        format_error(
                            MISSING_YAML_BLOCK,
                            "Missing machine-readable YAML block",
                        )
                    )
                elif not has_source_ref:
                    skill_name = contract.get("produced_by", "unknown")
                    template_path = (
                        f"skills/{skill_name}/references/{artifact_id}-template.md"
                    )
                    error_msg = (
                        "Missing required machine-readable fields: "
                        f"{', '.join(required_fields)}\n"
                    )
                    error_msg += "Add YAML block at end of artifact:\n```yaml\n"
                    for field in required_fields:
                        error_msg += f"{field}: <value>\n"
                    error_msg += f"```\nSee template: {template_path}"
                    errors.append(format_error(MISSING_MACHINE_FIELDS, error_msg))
                elif line_count >= 100:
                    missing = [f for f in required_fields if f not in yaml_data]
                    for field in missing:
                        warnings.append(
                            format_error(
                                MISSING_MACHINE_FIELDS,
                                f"Required machine field '{field}' not in YAML block "
                                "(large artifact; value likely in prose content)",
                            )
                        )
                else:
                    skill_name = contract.get("produced_by", "unknown")
                    template_path = (
                        f"skills/{skill_name}/references/{artifact_id}-template.md"
                    )
                    error_msg = (
                        "Missing required machine-readable fields: "
                        f"{', '.join(required_fields)}\n"
                    )
                    error_msg += "Add YAML block at end of artifact:\n```yaml\n"
                    for field in required_fields:
                        error_msg += f"{field}: <value>\n"
                    error_msg += f"```\nSee template: {template_path}"
                    errors.append(format_error(MISSING_MACHINE_FIELDS, error_msg))

    if yaml_data and recommended_fields:
        for field in recommended_fields:
            if field not in yaml_data:
                msg = format_error(
                    MISSING_RECOMMENDED_FIELD,
                    f"Recommended field missing: {field}",
                )
                if strict_recommended:
                    errors.append(msg)
                else:
                    warnings.append(msg)

    if yaml_data:
        vocab = load_canonical_vocabulary(repo_root)
        if vocab:
            _validate_enum_fields(yaml_data, artifact_id, vocab, errors)

    if artifact_id == "repository_sensemaking_brief":
        evidence_match = re.search(
            r"evidence_excerpts:.*?```yaml\s+(.*?)\s+```",
            content,
            re.DOTALL | re.IGNORECASE,
        )
        if not evidence_match:
            evidence_match = re.search(
                r"```yaml\s+(evidence_excerpts:.*?)\s+```",
                content,
                re.DOTALL,
            )

        if not evidence_match and line_count >= 100:
            warnings.append(
                format_error(
                    MISSING_EVIDENCE_EXCERPTS,
                    "No structured evidence_excerpts YAML block found "
                    "(large artifact; evidence likely present in markdown table or prose)",
                )
            )
        elif not evidence_match:
            errors.append(
                format_error(
                    MISSING_EVIDENCE_EXCERPTS,
                    "Missing or malformed YAML block for evidence_excerpts",
                )
            )
        else:
            try:
                evidence_data = yaml.safe_load(evidence_match.group(1))
                excerpts = evidence_data.get("evidence_excerpts", [])
                if not isinstance(excerpts, list):
                    errors.append(
                        format_error(
                            MISSING_EVIDENCE_EXCERPTS,
                            "evidence_excerpts must be a list of excerpts",
                        )
                    )
                else:
                    for i, exc in enumerate(excerpts):
                        for field in ["file", "lines", "quote", "supports_claim"]:
                            if field not in exc:
                                errors.append(
                                    format_error(
                                        MISSING_EXCERPT_FIELD,
                                        f"evidence_excerpt[{i}] missing field: {field}",
                                    )
                                )
                        if "file" in exc and exc["file"].startswith("file:///"):
                            errors.append(
                                format_error(
                                    ABSOLUTE_EXCERPT_PATH,
                                    f"evidence_excerpt[{i}] file path must be relative, "
                                    f"got: {exc['file']}",
                                )
                            )
            except Exception as exc:
                errors.append(
                    format_error(
                        MISSING_EVIDENCE_EXCERPTS,
                        f"Failed to parse evidence_excerpts YAML: {exc}",
                    )
                )

    return errors


def _json_error(error: str) -> dict:
    """Represent the existing stable-code prose error in the unified JSON shape."""
    code, separator, message = error.partition(": ")
    if not separator:
        code = "VALIDATION_ERROR"
        message = error
    return {
        "error_id": code,
        "error_type": "validation_error",
        "field": None,
        "current_value": None,
        "message": message,
        "suggested_fixes": [],
        "reference": "skills/workflow-planner/references/artifact-contracts.yaml",
    }


def validation_result(artifact_id: str, artifact_path: str, errors: list[str]) -> dict:
    """Return the unified top-level validator result consumed by the router."""
    return {
        "valid": len(errors) == 0,
        "artifact_id": artifact_id,
        "artifact_path": os.path.abspath(artifact_path),
        "validator": "validate-artifact.py",
        "errors": [_json_error(error) for error in errors],
        "validation_timestamp": datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate an artifact against its contract."
    )
    parser.add_argument(
        "artifact_id",
        help="The ID of the artifact (e.g., repository_sensemaking_brief)",
    )
    parser.add_argument(
        "artifact_path",
        nargs="?",
        help="Path to the artifact markdown file",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Root directory of the repository",
    )
    parser.add_argument(
        "--list-codes",
        action="store_true",
        help="List all error codes and exit",
    )
    parser.add_argument(
        "--strict-recommended",
        action="store_true",
        help="Treat missing recommended fields as errors",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit the unified validator JSON result",
    )
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

    global warnings
    warnings = []
    errs = validate_artifact(
        args.artifact_id,
        args.artifact_path,
        args.repo_root,
        args.strict_recommended,
    )

    if args.json:
        print(
            json.dumps(
                validation_result(args.artifact_id, args.artifact_path, errs),
                indent=2,
            )
        )
        return 1 if errs else 0

    if errs:
        print("[FAIL] Artifact validation failed:")
        for error in errs:
            print(f"  ERROR {error}")
        return 1

    print("[PASS] Required fields present")
    if warnings:
        for warning in warnings:
            print(f"[WARN] {warning}")
        print(f"\n  • {len(warnings)} warning(s)")
        return 0

    print("[OK] All fields (required + recommended) present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
