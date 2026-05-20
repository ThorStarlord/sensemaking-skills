"""Specialized Level 3 validator for prd artifacts."""

import os
import sys
import re
import yaml
import argparse

from _validator_utils import format_error, load_artifact_contracts

VALID_GOAL_PRESERVATIONS = {"exact_match", "core_with_expansion", "diverged"}
VALID_EXPANSION_STATUSES = {"exact_match", "pending_user_approval", "approved_by_user", "diverged"}

REQUIRED_SECTIONS = [
    "executive summary",
    "user goal",
    "goal preservation and expansion",
    "features",
    "out of scope",
    "acceptance criteria",
    "non functional requirements",
    "machine readable handoff",
]

HEADING_RE = re.compile(r"^##\s+(?:\d+\.\s*)?(?P<name>.+?)\s*$", re.MULTILINE)

MISSING_SECTION = "MISSING_SECTION"
MALFORMED_YAML = "MALFORMED_YAML"
INVALID_GOAL_PRESERVATION = "INVALID_GOAL_PRESERVATION"
INVALID_SCOPE_EXPANSION_TYPE = "INVALID_SCOPE_EXPANSION_TYPE"
EXPANSION_WITHOUT_APPROVAL = "EXPANSION_WITHOUT_APPROVAL"
INVALID_EXPANSION_STATUS = "INVALID_EXPANSION_STATUS"
ABSOLUTE_PATH_DETECTED = "ABSOLUTE_PATH_DETECTED"


def _extract_sections(content: str) -> dict[str, str]:
    sections = {}
    matches = list(HEADING_RE.finditer(content))
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
        # Normalize: lowercase, hyphens to spaces
        name = match.group("name").strip().lower().replace("-", " ")
        sections[name] = content[start:end].strip()
    return sections


def validate_prd(artifact_path: str, repo_root: str = ".") -> list[str]:
    errors: list[str] = []

    if not os.path.exists(artifact_path):
        errors.append(format_error(MISSING_SECTION, f"PRD file not found: {artifact_path}"))
        return errors

    with open(artifact_path, encoding="utf-8") as f:
        content = f.read()

    sections = _extract_sections(content)

    # 1. Required sections
    for section in REQUIRED_SECTIONS:
        if section not in sections:
            errors.append(format_error(MISSING_SECTION, f"Required section '{section}' not found"))

    # 2. Extract machine-readable YAML
    yaml_match = re.search(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)
    if not yaml_match:
        errors.append(format_error(MALFORMED_YAML, "No YAML code block found in the artifact"))
        return errors

    try:
        meta = yaml.safe_load(yaml_match.group(1))
    except Exception as e:
        errors.append(format_error(MALFORMED_YAML, f"Failed to parse YAML block: {e}"))
        return errors

    if not isinstance(meta, dict):
        errors.append(format_error(MALFORMED_YAML, "YAML block is not a dictionary"))
        return errors

    # 3. user_goal_preserved_as validation
    goal = meta.get("user_goal_preserved_as")
    if goal is None:
        errors.append(format_error(MALFORMED_YAML, "Missing 'user_goal_preserved_as' in YAML block"))
    elif goal not in VALID_GOAL_PRESERVATIONS:
        errors.append(format_error(INVALID_GOAL_PRESERVATION, f"Invalid user_goal_preserved_as '{goal}'; must be one of {sorted(VALID_GOAL_PRESERVATIONS)}"))

    # 4. scope_expansion_proposed is boolean
    proposed = meta.get("scope_expansion_proposed")
    if proposed is not None and not isinstance(proposed, bool):
        errors.append(format_error(INVALID_SCOPE_EXPANSION_TYPE, "scope_expansion_proposed must be a boolean"))

    # 5. scope_expansion_requires_approval is boolean
    requires = meta.get("scope_expansion_requires_approval")
    if requires is not None and not isinstance(requires, bool):
        errors.append(format_error(INVALID_SCOPE_EXPANSION_TYPE, "scope_expansion_requires_approval must be a boolean"))

    # 6. If scope_expansion_proposed is true, requires_approval must be true (unless already approved)
    if proposed is True and requires is False:
        errors.append(format_error(EXPANSION_WITHOUT_APPROVAL, "scope_expansion_proposed is true but scope_expansion_requires_approval is false; expansion always requires approval"))

    # 7. scope_expansion_status if present
    status = meta.get("scope_expansion_status")
    if status is not None and status not in VALID_EXPANSION_STATUSES:
        errors.append(format_error(INVALID_EXPANSION_STATUS, f"Invalid scope_expansion_status '{status}'; must be one of {sorted(VALID_EXPANSION_STATUSES)}"))

    # 8. source_intent_ref path hygiene
    ref = meta.get("source_intent_ref", "")
    if isinstance(ref, str) and ref.startswith(("/", "file://", "C:", "D:")):
        errors.append(format_error(ABSOLUTE_PATH_DETECTED, f"source_intent_ref is an absolute path: '{ref}'"))

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a PRD artifact.")
    parser.add_argument("artifact_path", nargs="?", help="Path to the .md PRD file")
    parser.add_argument("--repo-root", default=".", help="Root directory of the repository")
    parser.add_argument("--list-codes", action="store_true", help="List all error codes and exit")
    args = parser.parse_args(argv)

    if args.list_codes:
        codes = [
            MISSING_SECTION,
            MALFORMED_YAML,
            INVALID_GOAL_PRESERVATION,
            INVALID_SCOPE_EXPANSION_TYPE,
            EXPANSION_WITHOUT_APPROVAL,
            INVALID_EXPANSION_STATUS,
            ABSOLUTE_PATH_DETECTED,
        ]
        print("Stable error codes for PRD validation:")
        for code in codes:
            print(f"  {code}")
        return 0

    if not args.artifact_path:
        parser.print_usage()
        return 1

    errs = validate_prd(args.artifact_path, args.repo_root)
    if errs:
        for e in errs:
            print(f"ERROR {e}")
        return 1
    else:
        print("PRD validation passed!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
