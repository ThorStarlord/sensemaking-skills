#!/usr/bin/env python3
"""Workflow Presenter — generates beautiful markdown summaries from workflow execution JSON.

This skill reads the structured workflow_summary.json produced by orchestration-runner.py
and generates a human-readable EXECUTION_SUMMARY.md with formatted output, artifact links,
and clear next steps.

Usage:
    python workflow-presenter.py <workflow_summary.json> [--output-dir <dir>]
"""

import sys
import json
import os
from datetime import datetime
from pathlib import Path


def load_summary(json_path: str) -> dict | None:
    """Load workflow summary JSON. Returns dict or None if error."""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to load {json_path}: {e}")
        return None


def generate_summary_markdown(summary: dict) -> str:
    """Generate beautiful markdown from workflow summary."""
    lines = []

    # Header
    lines.extend([
        f"# Workflow Execution Summary",
        f"",
        f"**Workflow**: {summary.get('workflow_name', 'Unknown')} (`{summary.get('workflow_id')}`)  ",
        f"**Mode**: {summary.get('mode')}  ",
        f"**Status**: {_status_emoji(summary.get('status'))} **{summary.get('status').upper()}**  ",
        f"**Session**: `{summary.get('session_id')}`  ",
        f"**Branch**: `{summary.get('branch', 'unknown')}`  ",
        f"**Executed**: {summary.get('executed_at', 'unknown')}  ",
        f"",
    ])

    # Summary metrics
    steps_total = summary.get("steps_total", 0)
    steps_completed = summary.get("steps_completed", 0)
    steps_failed = summary.get("steps_failed", 0)

    status = summary.get("status")
    if status == "completed":
        badge = "✓"
    elif status == "failed":
        badge = "✗"
    else:
        badge = "⚠"

    lines.extend([
        f"## Execution Summary",
        f"",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Steps Executed | {steps_completed}/{steps_total} {badge} |",
        f"| Steps Failed | {steps_failed} |",
        f"| Final Status | {status.upper()} |",
        f"",
    ])

    # Steps execution details
    steps = summary.get("steps", [])
    if steps:
        lines.extend([
            f"## Steps Executed",
            f"",
        ])

        for step in steps:
            step_id = step.get("step_id", "?")
            skill = step.get("skill", "unknown")
            status = step.get("status", "UNKNOWN")
            output = step.get("output_artifact", "N/A")
            artifact_path = step.get("artifact_path", "")
            duration = step.get("duration_seconds", 0)

            status_icon = _status_emoji(status)

            lines.extend([
                f"### Step {step_id}: {skill}",
                f"",
                f"- **Status**: {status_icon} `{status}`",
            ])

            if artifact_path:
                # Make artifact path relative to repo root for link
                artifact_name = os.path.basename(artifact_path)
                lines.append(f"- **Output**: [{artifact_name}]({artifact_path})")
            else:
                lines.append(f"- **Output**: {output}")

            if duration > 0:
                lines.append(f"- **Duration**: {duration:.1f}s")

            # Validator results
            validators = step.get("validators", [])
            if validators:
                lines.append(f"- **Validation**:")
                for v in validators:
                    v_level = v.get("level", "unknown")
                    v_result = v.get("result", "UNKNOWN")
                    v_icon = "✓" if v_result == "PASSED" else "✗"
                    lines.append(f"  - {v_icon} {v_level}: {v_result}")

            lines.append("")

    # Artifacts summary
    lines.extend([
        f"## Artifacts Created",
        f"",
    ])

    artifact_count = 0
    for step in steps:
        artifact_path = step.get("artifact_path", "")
        artifact_name = step.get("output_artifact", "")
        if artifact_path and artifact_name:
            artifact_count += 1
            lines.append(f"- [{artifact_name}]({artifact_path})")

    if artifact_count == 0:
        lines.append(f"- No artifacts created in this execution")

    lines.append("")

    # Conclusion
    lines.extend([
        f"## Status",
        f"",
    ])

    status = summary.get("status")
    if status == "completed":
        lines.extend([
            f"✓ **Success**: All workflow steps executed and validated successfully.",
            f"",
            f"### Next Steps",
            f"",
            f"1. Review the artifacts created above",
            f"2. Follow any recommendations from individual steps",
            f"3. Continue with the next workflow or implement changes as needed",
            f"",
        ])
    elif status == "failed":
        errors = summary.get("errors", [])
        lines.extend([
            f"✗ **Failed**: Workflow execution encountered errors.",
            f"",
        ])
        if errors:
            lines.append(f"### Error Details")
            lines.append(f"")
            for error in errors[:3]:  # Show first 3 errors
                lines.append(f"- {error}")
            lines.append("")
        lines.extend([
            f"### Troubleshooting",
            f"",
            f"1. Check the run log for detailed execution information",
            f"2. Review error messages above",
            f"3. Fix the issue and re-run the workflow",
            f"",
        ])
    else:
        note = summary.get("final_note", "")
        lines.append(f"⚠ **Partial**: Workflow execution is incomplete.")
        lines.append(f"")
        if note:
            lines.append(f"**Note**: {note}")
        lines.append(f"")

    # Footer
    lines.extend([
        f"---",
        f"",
        f"*Generated by Workflow Presenter at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
    ])

    return "\n".join(lines)


def _status_emoji(status: str) -> str:
    """Get emoji for status."""
    if not status:
        return "?"
    status_upper = status.upper()
    if status_upper in ("COMPLETED", "EXECUTED", "VALIDATED", "PLANNED", "PROMPT_GENERATED", "APPROVED"):
        return "✓"
    elif status_upper == "FAILED":
        return "✗"
    elif status_upper in ("PAUSED", "PARTIAL", "PROMPT_CHAIN_GENERATED"):
        return "⚠"
    else:
        return "•"


def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    if argv is None:
        argv = sys.argv[1:]

    if not argv or argv[0] in ("--help", "-h"):
        print(__doc__)
        return 0

    json_path = argv[0]
    if not os.path.exists(json_path):
        print(f"ERROR: File not found: {json_path}")
        return 1

    # Determine output directory
    output_dir = None
    if len(argv) > 1 and argv[1] == "--output-dir":
        if len(argv) > 2:
            output_dir = argv[2]

    if not output_dir:
        output_dir = os.path.dirname(json_path)

    # Load summary
    summary = load_summary(json_path)
    if not summary:
        return 1

    # Generate markdown
    markdown = generate_summary_markdown(summary)

    # Write output
    output_path = os.path.join(output_dir, "EXECUTION_SUMMARY.md")
    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        print(f"[OK] Execution summary generated: {output_path}")
        print(f"Summary generated at: {output_path}")
        return 0
    except Exception as e:
        print(f"ERROR: Failed to write {output_path}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
