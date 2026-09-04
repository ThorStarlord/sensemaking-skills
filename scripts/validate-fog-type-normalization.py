#!/usr/bin/env python3
"""Validate and normalize fog types in artifacts.

This validator:
1. Accepts aliases (ui, product, docs, architecture, integration)
2. Normalizes to canonical forms (ui_fog, product_fog, etc.)
3. Rejects unrecognized fog type values, EXCEPT the intent-neutral sentinel
   `user_implied_fog_type: unknown` (legal per canonical-vocabulary.yaml
   routing_fields; never legal for primary_fog_type, the diagnosis)

Used by artifact producers (repo-sensemaker, workflow-planner) to ensure
downstream consumers always receive canonical fog type values.
"""

import os
import sys
import re
from pathlib import Path

import yaml

# Add scripts directory to path so we can import _validator_utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _validator_utils import (
    load_canonical_vocabulary,
    build_fog_type_normalizer,
    normalize_fog_type,
    validator_cli,
    extract_sections,
)


def validate_fog_type_normalization(artifact_path: str, repo_root: str) -> list[str]:
    """Validate and normalize fog types in artifact.

    Args:
        artifact_path: Path to artifact markdown file
        repo_root: Root directory of repository

    Returns:
        List of error messages (empty if validation passes)
    """
    errors = []

    if not artifact_path or not os.path.exists(artifact_path):
        return [f"ARTIFACT_NOT_FOUND: {artifact_path}"]

    artifact_content = Path(artifact_path).read_text(encoding="utf-8")

    # Extract machine-readable section
    sections = extract_sections(artifact_content)
    machine_section = sections.get("machine readable", "") or sections.get("machine_readable", "")

    if not machine_section:
        # Some artifacts don't have machine-readable sections
        return []

    # Remove markdown code fence markers if present
    machine_section = re.sub(r"```(?:yaml|yml)?\n?", "", machine_section).strip()

    # Try to parse YAML from machine-readable section
    try:
        machine_data = yaml.safe_load(machine_section)
        if not isinstance(machine_data, dict):
            return []
    except Exception as e:
        return [f"YAML_PARSE_ERROR: Could not parse machine-readable section: {e}"]

    # Load vocabulary and build normalizer
    vocab = load_canonical_vocabulary(repo_root)
    if not vocab:
        return [f"VOCAB_NOT_FOUND: canonical-vocabulary.yaml not found in {repo_root}"]

    normalizer = build_fog_type_normalizer(vocab)
    if not normalizer:
        return [f"NO_FOG_TYPES: canonical vocabulary contains no fog types"]

    # Check and normalize fog types in artifact
    fog_type_fields = ["primary_fog_type", "user_implied_fog_type"]
    for field in fog_type_fields:
        if field in machine_data:
            value = machine_data[field]
            if value is None:
                continue

            # `unknown` is a legal terminal value for user_implied_fog_type only
            # (canonical-vocabulary.yaml routing_fields): it means the user's
            # stated intent is fog-neutral. It is not a fog type and needs no
            # alias normalization. primary_fog_type (the diagnosis) is never
            # `unknown` and still fails below.
            if field == "user_implied_fog_type" and str(value).strip().lower() == "unknown":
                continue

            try:
                canonical = normalize_fog_type(str(value), normalizer)
                # Update the value to canonical form (for potential write-back)
                machine_data[field] = canonical
            except ValueError as e:
                errors.append(f"INVALID_FOG_TYPE: {field}={value!r}. {e}")

    return errors


def main() -> int:
    """CLI entry point."""
    return validator_cli(
        validate_fog_type_normalization,
        description="Validate and normalize fog types to canonical forms (product_fog, ui_fog, etc.)",
        error_codes=[
            "ARTIFACT_NOT_FOUND",
            "YAML_PARSE_ERROR",
            "VOCAB_NOT_FOUND",
            "NO_FOG_TYPES",
            "INVALID_FOG_TYPE",
        ],
        success_msg="Fog type normalization passed! All fog types are in canonical form.",
    )


if __name__ == "__main__":
    sys.exit(main())
