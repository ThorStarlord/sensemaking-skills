import os
import sys
import re
import argparse
import yaml

from _validator_utils import format_error

# Stable error codes
UNKNOWNS_MAP_FILE_NOT_FOUND = "UNKNOWNS_MAP_FILE_NOT_FOUND"
MISSING_ROUTING_BLOCK = "MISSING_ROUTING_BLOCK"
MISSING_ROUTING_FIELD = "MISSING_ROUTING_FIELD"
INVALID_ROUTING_YAML = "INVALID_ROUTING_YAML"
PARSING_ERROR = "PARSING_ERROR"

ROUTING_YAML_RE = re.compile(
    r"## 7\. Machine-readable routing\s+```yaml\s+(.*?)\s+```",
    re.DOTALL | re.IGNORECASE,
)


def validate_unknowns_map(artifact_path: str, repo_root: str = ".") -> list[str]:
    """Validate an unknowns map fixture against routing field requirements."""
    errors: list[str] = []

    if not os.path.exists(artifact_path):
        errors.append(
            format_error(
                UNKNOWNS_MAP_FILE_NOT_FOUND,
                f"Unknowns map file not found: {artifact_path}",
            )
        )
        return errors

    with open(artifact_path, encoding="utf-8") as f:
        content = f.read()

    # Check for routing block
    routing_match = ROUTING_YAML_RE.search(content)
    if not routing_match:
        errors.append(
            format_error(
                MISSING_ROUTING_BLOCK,
                "Missing '## 7. Machine-readable routing' YAML block.",
            )
        )
        return errors

    # Parse the YAML block
    try:
        routing_data = yaml.safe_load(routing_match.group(1))
    except Exception as e:
        errors.append(
            format_error(INVALID_ROUTING_YAML, f"Failed to parse routing YAML: {e}")
        )
        return errors

    if not isinstance(routing_data, dict):
        errors.append(
            format_error(
                PARSING_ERROR,
                "Routing block must be a YAML dictionary.",
            )
        )
        return errors

    # Check for required routing field: research_needed
    if "research_needed" not in routing_data:
        errors.append(
            format_error(
                MISSING_ROUTING_FIELD,
                "Routing block missing required field: 'research_needed'",
            )
        )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validator for unknowns map conditional routing fields."
    )
    parser.add_argument("artifact_path", nargs="?", help="Path to the unknowns map .md file")
    parser.add_argument("--repo-root", default=".", help="Root of the repository for file checks")
    parser.add_argument("--list-codes", action="store_true", help="List all error codes and exit")
    args = parser.parse_args(argv)

    if args.list_codes:
        codes = [
            UNKNOWNS_MAP_FILE_NOT_FOUND,
            MISSING_ROUTING_BLOCK,
            MISSING_ROUTING_FIELD,
            INVALID_ROUTING_YAML,
            PARSING_ERROR,
        ]
        print("Stable error codes for unknowns map validation:")
        for code in codes:
            print(f"  {code}")
        return 0

    if not args.artifact_path:
        parser.print_usage()
        return 1

    errs = validate_unknowns_map(args.artifact_path, args.repo_root)
    if errs:
        for e in errs:
            print(f"ERROR {e}")
        return 1
    else:
        print("Unknowns map verification passed! Routing field is valid.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
