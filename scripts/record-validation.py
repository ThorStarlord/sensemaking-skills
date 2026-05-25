"""Record validation results to a persistent run log.

This script appends validation results to a markdown run log.
It's intentionally simple and boring — no validation, no decisions, just logging.

Design:
- Accept validation JSON from stdin or file
- Append a formatted entry to the run log
- Do not modify artifacts
- Do not implement any business logic
- Preserve the complete validation result for future auditing
"""

import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def format_validation_entry(validation_result: dict[str, Any]) -> str:
    """Format a validation result as a markdown log entry.

    Args:
        validation_result: The complete ValidationResult dict from validate-and-report.py

    Returns:
        A markdown-formatted log entry
    """
    timestamp = validation_result.get("validation_timestamp", datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))
    artifact_id = validation_result.get("artifact_id", "unknown")
    artifact_path = validation_result.get("artifact_path", "unknown")
    validator = validation_result.get("validator", "unknown")
    valid = validation_result.get("valid", False)
    errors = validation_result.get("errors", [])

    # Build entry header
    status = "VALID" if valid else "INVALID"
    entry = f"## Validation Attempt — {timestamp}\n\n"
    entry += f"- Artifact: `{artifact_id}`\n"
    entry += f"- Path: `{artifact_path}`\n"
    entry += f"- Validator: `{validator}`\n"
    entry += f"- Result: **{status}**\n"

    if not valid:
        entry += f"- Error count: {len(errors)}\n\n"

        # Create error table if there are errors
        if errors:
            entry += "| error_id | type | field | message | suggested_fix |\n"
            entry += "|---|---|---|---|---|\n"

            for error in errors:
                error_id = error.get("error_id", "")
                error_type = error.get("error_type", "")
                field = error.get("field", "")
                message = error.get("message", "").replace("|", "\\|").replace("\n", " ")[:100]
                fixes = error.get("suggested_fixes", [])
                suggested_fix = fixes[0].replace("|", "\\|")[:60] if fixes else ""

                entry += f"| `{error_id}` | {error_type} | {field} | {message} | {suggested_fix} |\n"

        # Collect unique references
        references = set()
        for error in errors:
            ref = error.get("reference")
            if ref:
                references.add(ref)

        if references:
            entry += "\nReferences:\n"
            for ref in sorted(references):
                entry += f"- `{ref}`\n"
    else:
        # Valid artifact - brief entry
        entry += "- Errors: 0\n"

    entry += "\n---\n\n"
    return entry


def record_validation(validation_json: dict[str, Any], run_log_path: str) -> None:
    """Append a validation result to the run log.

    Args:
        validation_json: The complete ValidationResult dict
        run_log_path: Path to the run log file (will be created if doesn't exist)

    Raises:
        IOError: If unable to write to the run log
    """
    run_log = Path(run_log_path)

    # Create parent directory if needed
    run_log.parent.mkdir(parents=True, exist_ok=True)

    # Create or append to log file
    entry = format_validation_entry(validation_json)

    # Add header if file is new
    if not run_log.exists():
        header = "# Validation Run Log\n\n"
        header += "This log records all validation attempts for artifacts in this repository.\n"
        header += "Each entry preserves the complete validation result for auditing.\n\n"
        run_log.write_text(header, encoding="utf-8")

    # Append entry
    with open(run_log_path, "a", encoding="utf-8") as f:
        f.write(entry)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Record validation results to a persistent run log."
    )
    parser.add_argument(
        "--validation-json",
        help="Path to validation JSON file (default: read from stdin)",
        default=None
    )
    parser.add_argument(
        "--run-log",
        help="Path to the run log file to append to",
        required=True
    )
    args = parser.parse_args(argv)

    # Read validation JSON
    try:
        if args.validation_json:
            # Read from file
            with open(args.validation_json, encoding="utf-8") as f:
                validation_json = json.load(f)
        else:
            # Read from stdin
            validation_json = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON input: {str(e)}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"ERROR: File not found: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Failed to read validation JSON: {str(e)}", file=sys.stderr)
        return 1

    # Record to log
    try:
        record_validation(validation_json, args.run_log)
        return 0
    except IOError as e:
        print(f"ERROR: Failed to write to run log: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Failed to record validation: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
