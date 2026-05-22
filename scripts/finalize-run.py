#!/usr/bin/env python3
"""CLI utility to finalize a run ledger.

Calculates the overall status based on step executions, updates run metadata,
and optionally updates docs/mode-coverage.yaml with the compiled facts.
"""

import os
import sys
import argparse
import datetime
import re
import yaml


def load_yaml(path: str) -> dict | None:
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load YAML at {path}: {e}", file=sys.stderr)
        return None


def save_yaml(data: dict, path: str) -> bool:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save YAML at {path}: {e}", file=sys.stderr)
        return False


def get_validators_exercised(steps: list) -> list[str]:
    validators = ["level_1: validate-repo.py"]
    for step in steps:
        cmd = step.get("validator_command")
        if cmd:
            # Find all validator script names (validate-*.py)
            matches = re.findall(r"validate-[\w-]+\.py", cmd)
            for script in matches:
                if script == "validate-repo.py":
                    continue
                level = "level_2" if script == "validate-artifact.py" else "level_3"
                label = f"{level}: {script}"
                if label not in validators:
                    validators.append(label)
    return validators


def get_gates_info(steps: list, mode: str) -> tuple[bool, str]:
    gates_exercised = False
    approved_count = 0
    denied_count = 0

    for step in steps:
        gate_status = step.get("gate_status")
        if gate_status in ("approved", "approved_by_user", "automated_approval"):
            gates_exercised = True
            approved_count += 1
        elif gate_status in ("denied", "denied_by_user"):
            gates_exercised = True
            denied_count += 1

    if mode == "plan_only":
        gates_note = "not_applicable_plan_only"
    elif mode == "prompt_chain":
        gates_note = "not_applicable_prompt_chain"
    elif mode == "yolo_execution":
        gates_note = "bypassed_by_yolo"
    elif mode == "autonomous_execution":
        gates_note = "automated_approval_all_gates"
    else:
        gates_note = f"{approved_count} approved, {denied_count} denied"

    return gates_exercised, gates_note


def main() -> int:
    parser = argparse.ArgumentParser(description="Finalize a run ledger and update mode coverage.")
    parser.add_argument("--ledger-path", required=True, help="Path to the ledger YAML file")
    parser.add_argument("--repo-root", default=".", help="Root directory of the repository")
    parser.add_argument("--update-mode-coverage", action="store_true", help="Update docs/mode-coverage.yaml")
    parser.add_argument("--workflow-id", help="Override workflow ID for mode coverage")
    parser.add_argument("--mode", help="Override execution mode for mode coverage")

    args = parser.parse_args()

    repo_root = os.path.abspath(args.repo_root)
    ledger_path = os.path.abspath(args.ledger_path)

    ledger_data = load_yaml(ledger_path)
    if not ledger_data:
        print(f"[ERROR] Run ledger not found or empty at {args.ledger_path}", file=sys.stderr)
        return 1

    steps = ledger_data.get("steps", [])
    run_metadata = ledger_data.setdefault("run_metadata", {})

    # Evaluate step statuses to determine overall status
    steps_total = len(steps)
    steps_completed = 0
    any_failed = False
    all_completed_or_skipped = True

    for step in steps:
        status = step.get("status")
        if status == "failed":
            any_failed = True
            all_completed_or_skipped = False
        elif status in ("passed", "skipped"):
            steps_completed += 1
        else:
            all_completed_or_skipped = False

    # Decide status
    if any_failed:
        final_status = "failed"
    elif all_completed_or_skipped and steps_total > 0:
        final_status = "completed"
    else:
        final_status = "partial"

    run_metadata["status"] = final_status
    run_metadata["timestamp_end"] = datetime.datetime.now().isoformat()

    # Save finalized ledger
    if not save_yaml(ledger_data, ledger_path):
        return 1
    print(f"[OK] Ledger finalized with status: {final_status}")

    # Optionally update mode coverage
    if args.update_mode_coverage:
        coverage_path = os.path.join(repo_root, "docs", "mode-coverage.yaml")
        coverage = load_yaml(coverage_path)
        if not coverage:
            print(f"[ERROR] Could not load mode-coverage.yaml at {coverage_path}", file=sys.stderr)
            return 1

        workflow_id = args.workflow_id or run_metadata.get("workflow_id")
        mode = args.mode or run_metadata.get("mode")

        if not workflow_id or not mode:
            print("[ERROR] workflow_id and mode must be defined in the ledger metadata or passed via CLI args", file=sys.stderr)
            return 1

        run_id = run_metadata.get("run_id", "unknown_run")
        run_log_rel = os.path.relpath(ledger_path, repo_root).replace("\\", "/")

        validators_exercised = get_validators_exercised(steps)
        gates_exercised, gates_note = get_gates_info(steps, mode)

        mode_entries = coverage.setdefault("mode_coverage", [])
        
        # Look for existing entry to update
        existing = next((e for e in mode_entries if e.get("workflow_id") == workflow_id and e.get("mode") == mode), None)

        entry_data = {
            "mode": mode,
            "workflow_id": workflow_id,
            "last_run": datetime.datetime.now().strftime("%Y-%m-%d"),
            "run_log_path": run_log_rel,
            "steps_completed": steps_completed,
            "steps_total": steps_total,
            "validators_exercised": validators_exercised,
            "gates_exercised": gates_exercised,
            "gates_note": gates_note,
            "hardening_triggered": "none",
            "notes": f"Executed via decentralized run ledger system. Run ID: {run_id}."
        }

        if existing:
            existing.update(entry_data)
            print(f"  ~ Updated existing mode coverage entry for {workflow_id} ({mode})")
        else:
            mode_entries.append(entry_data)
            print(f"  ~ Appended new mode coverage entry for {workflow_id} ({mode})")

        # Update orchestration_runner / system_tools sections
        system_tools = coverage.setdefault("system_tools", [])
        runner_tool = next((t for t in system_tools if t.get("tool") == "orchestration-runner.py"), None)
        wf_entry = f"{workflow_id} ({mode})"

        if runner_tool:
            wf_list = runner_tool.setdefault("workflows_executed", [])
            if isinstance(wf_list, list):
                if wf_entry not in wf_list:
                    wf_list.append(wf_entry)
            else:
                runner_tool["workflows_executed"] = [wf_entry]
            runner_tool["last_run"] = datetime.datetime.now().strftime("%Y-%m-%d")
            runner_tool["last_session"] = run_id
        else:
            system_tools.append({
                "tool": "orchestration-runner.py",
                "status": "active",
                "last_run": datetime.datetime.now().strftime("%Y-%m-%d"),
                "last_session": run_id,
                "workflows_executed": [wf_entry],
                "modes_proven": [mode],
            })

        # Aggregate workflow families
        workflows_run = set()
        for entry in mode_entries:
            wf = entry.get("workflow_id", "")
            if wf:
                workflows_run.add(wf)

        runner_section = coverage.setdefault("orchestration_runner", {})
        runner_section["last_run"] = datetime.datetime.now().strftime("%Y-%m-%d")
        runner_section["workflow_families_proven"] = sorted(list(workflows_run))
        runner_section["total_workflow_families"] = len(workflows_run)

        if save_yaml(coverage, coverage_path):
            print(f"[OK] mode-coverage.yaml successfully updated.")
        else:
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
