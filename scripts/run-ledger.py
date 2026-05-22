#!/usr/bin/env python3
"""CLI utility to manage the decentralized run ledger in append-only JSONL format.

Proves the causal chain of steps, records input/output artifact hashes, validator
execution details, and git SHAs.
"""

import os
import sys
import json
import argparse
import datetime
import hashlib
import subprocess
import yaml


def resolve_path(path: str, repo_root: str) -> str:
    """Resolve a path relative to the repository root using forward slashes."""
    abs_path = os.path.abspath(path)
    abs_root = os.path.abspath(repo_root)
    if abs_path.startswith(abs_root):
        rel = os.path.relpath(abs_path, abs_root)
        return rel.replace("\\", "/")
    return path.replace("\\", "/")


def get_git_commit(repo_root: str) -> str:
    """Get the HEAD git commit SHA, with a '-dirty' suffix if the tree has changes."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True
        )
        commit = result.stdout.strip()
        
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True
        )
        if status_result.stdout.strip():
            commit += "-dirty"
        return commit
    except Exception:
        return "unknown_commit"


def compute_file_hash(path: str) -> str:
    """Compute the SHA-256 hash of a file."""
    if not os.path.exists(path):
        return "file_not_found"
    sha256 = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256.update(byte_block)
        return sha256.hexdigest()
    except Exception:
        return "hash_error"


def append_ledger_event(ledger_path: str, event_data: dict) -> None:
    """Append a single event dictionary as a JSON line to the ledger file."""
    os.makedirs(os.path.dirname(os.path.abspath(ledger_path)), exist_ok=True)
    event_data["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with open(ledger_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event_data) + "\n")


def read_ledger_events(ledger_path: str) -> list[dict]:
    """Read all event dictionaries from a JSONL ledger file."""
    if not os.path.exists(ledger_path):
        return []
    events = []
    with open(ledger_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return events


def handle_start_run(args) -> int:
    repo_root = os.path.abspath(args.repo_root)
    commit = get_git_commit(repo_root)
    event = {
        "event": "run_started",
        "run_id": args.run_id,
        "workflow_id": args.workflow,
        "mode": args.mode,
        "git_commit": commit
    }
    append_ledger_event(args.ledger_path, event)
    print(f"[OK] Run {args.run_id} ({args.workflow}) started.")
    return 0


def handle_start_step(args) -> int:
    repo_root = os.path.abspath(args.repo_root)
    inputs = []
    if args.inputs:
        paths = [p.strip() for p in args.inputs.split(",")]
        for p in paths:
            if not p:
                continue
            abs_p = os.path.abspath(p)
            rel_p = resolve_path(abs_p, repo_root)
            f_hash = compute_file_hash(abs_p)
            inputs.append({
                "path": rel_p,
                "hash": f_hash
            })
    
    event = {
        "event": "step_started",
        "step_id": args.step_id,
        "skill_id": args.skill_id,
        "inputs": inputs
    }
    append_ledger_event(args.ledger_path, event)
    print(f"[OK] Step {args.step_id} ({args.skill_id}) started.")
    return 0


def handle_record_artifact(args) -> int:
    repo_root = os.path.abspath(args.repo_root)
    abs_path = os.path.abspath(args.path)
    rel_path = resolve_path(abs_path, repo_root)
    f_hash = compute_file_hash(abs_path)
    
    event = {
        "event": "artifact_created",
        "step_id": args.step_id,
        "artifact_id": args.artifact_id,
        "path": rel_path,
        "hash": f_hash
    }
    append_ledger_event(args.ledger_path, event)
    print(f"[OK] Artifact {args.artifact_id} recorded at {rel_path}.")
    return 0


def handle_record_validation(args) -> int:
    event = {
        "event": "validation_completed",
        "step_id": args.step_id,
        "artifact_id": args.artifact_id,
        "validator_command": args.command,
        "exit_code": args.exit_code,
        "status": args.status
    }
    append_ledger_event(args.ledger_path, event)
    print(f"[OK] Validation for step {args.step_id} / {args.artifact_id} recorded (exit code: {args.exit_code}).")
    return 0


def handle_complete_step(args) -> int:
    event = {
        "event": "step_completed",
        "step_id": args.step_id,
        "status": args.status,
        "gate_status": args.gate_status
    }
    append_ledger_event(args.ledger_path, event)
    print(f"[OK] Step {args.step_id} completed with status: {args.status}.")
    return 0


def handle_finalize_run(args) -> int:
    repo_root = os.path.abspath(args.repo_root)
    events = read_ledger_events(args.ledger_path)
    if not events:
        print(f"[ERROR] Ledger is empty or not found: {args.ledger_path}", file=sys.stderr)
        return 1

    # Extract metadata and step outcomes
    run_started = next((e for e in events if e.get("event") == "run_started"), None)
    if not run_started:
        print("[ERROR] Ledger does not contain run_started event", file=sys.stderr)
        return 1

    run_id = run_started.get("run_id", "unknown_run")
    workflow_id = run_started.get("workflow_id")
    mode = run_started.get("mode")

    step_completions = [e for e in events if e.get("event") == "step_completed"]
    step_starts = [e for e in events if e.get("event") == "step_started"]
    
    steps_total = len(step_starts)
    steps_completed = 0
    any_failed = False
    all_completed_or_skipped = True

    completed_ids = set()
    for e in step_completions:
        completed_ids.add(e.get("step_id"))
        status = e.get("status")
        if status == "failed":
            any_failed = True
            all_completed_or_skipped = False
        elif status in ("passed", "skipped", "completed"):
            steps_completed += 1
        else:
            all_completed_or_skipped = False

    # Check if any started step is not completed
    for e in step_starts:
        if e.get("step_id") not in completed_ids:
            all_completed_or_skipped = False

    if any_failed:
        final_status = "failed"
    elif all_completed_or_skipped and steps_total > 0:
        final_status = "completed"
    else:
        final_status = "partial"

    event = {
        "event": "run_completed",
        "run_id": run_id,
        "status": final_status
    }
    append_ledger_event(args.ledger_path, event)
    print(f"[OK] Run {run_id} finalized with status: {final_status}")

    # Optionally update mode coverage
    if args.update_mode_coverage:
        coverage_path = os.path.join(repo_root, "docs", "mode-coverage.yaml")
        if not os.path.exists(coverage_path):
            print(f"[ERROR] docs/mode-coverage.yaml not found at {coverage_path}", file=sys.stderr)
            return 1

        try:
            with open(coverage_path, "r", encoding="utf-8") as f:
                coverage = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"[ERROR] Failed to load mode-coverage.yaml: {e}", file=sys.stderr)
            return 1

        # Extract validators and gates
        validators = ["level_1: validate-repo.py"]
        gates_exercised = False
        approved_count = 0
        denied_count = 0

        for e in events:
            if e.get("event") == "validation_completed":
                cmd = e.get("validator_command")
                if cmd:
                    import re
                    matches = re.findall(r"validate-[\w-]+\.py", cmd)
                    for script in matches:
                        if script == "validate-repo.py":
                            continue
                        level = "level_2" if script == "validate-artifact.py" else "level_3"
                        label = f"{level}: {script}"
                        if label not in validators:
                            validators.append(label)

            if e.get("event") == "step_completed":
                gate_status = e.get("gate_status")
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

        run_log_rel = os.path.relpath(os.path.abspath(args.ledger_path), repo_root).replace("\\", "/")

        mode_entries = coverage.setdefault("mode_coverage", [])
        existing = next((entry for entry in mode_entries if entry.get("workflow_id") == workflow_id and entry.get("mode") == mode), None)

        entry_data = {
            "mode": mode,
            "workflow_id": workflow_id,
            "last_run": datetime.datetime.now().strftime("%Y-%m-%d"),
            "run_log_path": run_log_rel,
            "steps_completed": steps_completed,
            "steps_total": steps_total,
            "validators_exercised": validators,
            "gates_exercised": gates_exercised,
            "gates_note": gates_note,
            "hardening_triggered": "none",
            "notes": f"Executed via decentralized run ledger system. Run ID: {run_id}."
        }

        if existing:
            existing.update(entry_data)
        else:
            mode_entries.append(entry_data)

        # Update orchestration_runner tool entry
        system_tools = coverage.setdefault("system_tools", [])
        runner_tool = next((t for t in system_tools if t.get("tool") == "orchestration-runner.py"), None)
        wf_entry = f"{workflow_id} ({mode})"

        if runner_tool:
            wf_list = runner_tool.setdefault("workflows_executed", [])
            if wf_entry not in wf_list:
                wf_list.append(wf_entry)
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

        # Update orchestration_runner aggregated summaries
        workflows_run = set()
        for entry in mode_entries:
            wf = entry.get("workflow_id")
            if wf:
                workflows_run.add(wf)

        runner_section = coverage.setdefault("orchestration_runner", {})
        runner_section["last_run"] = datetime.datetime.now().strftime("%Y-%m-%d")
        runner_section["workflow_families_proven"] = sorted(list(workflows_run))
        runner_section["total_workflow_families"] = len(workflows_run)

        try:
            with open(coverage_path, "w", encoding="utf-8") as f:
                yaml.dump(coverage, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            print(f"[OK] docs/mode-coverage.yaml successfully updated.")
        except Exception as e:
            print(f"[ERROR] Failed to save mode-coverage.yaml: {e}", file=sys.stderr)
            return 1

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Inverted execution run ledger management tool.")
    parser.add_argument("--repo-root", default=".", help="Root directory of the repository")
    parser.add_argument("--ledger-path", required=True, help="Path to the run ledger JSONL file")
    
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # start-run
    p_start_run = subparsers.add_parser("start-run")
    p_start_run.add_argument("--run-id", required=True, help="Unique run ID")
    p_start_run.add_argument("--workflow", required=True, help="Workflow ID")
    p_start_run.add_argument("--mode", required=True, help="Execution mode")

    # start-step
    p_start_step = subparsers.add_parser("start-step")
    p_start_step.add_argument("--step-id", required=True, help="Step ID")
    p_start_step.add_argument("--skill-id", required=True, help="Skill ID")
    p_start_step.add_argument("--inputs", help="Comma-separated input file paths")

    # record-artifact
    p_rec_art = subparsers.add_parser("record-artifact")
    p_rec_art.add_argument("--step-id", required=True, help="Step ID")
    p_rec_art.add_argument("--artifact-id", required=True, help="Artifact ID from contract")
    p_rec_art.add_argument("--path", required=True, help="Path to produced artifact file")

    # record-validation
    p_rec_val = subparsers.add_parser("record-validation")
    p_rec_val.add_argument("--step-id", required=True, help="Step ID")
    p_rec_val.add_argument("--artifact-id", required=True, help="Artifact ID")
    p_rec_val.add_argument("--command", required=True, help="Validator command run")
    p_rec_val.add_argument("--exit-code", type=int, required=True, help="Validator exit code")
    p_rec_val.add_argument("--status", required=True, choices=["passed", "failed"], help="Validation status")

    # complete-step
    p_comp_step = subparsers.add_parser("complete-step")
    p_comp_step.add_argument("--step-id", required=True, help="Step ID")
    p_comp_step.add_argument("--status", required=True, choices=["passed", "failed", "skipped", "completed"], help="Step status")
    p_comp_step.add_argument("--gate-status", required=True, choices=["approved", "denied", "bypassed", "none"], help="Gate outcome")

    # finalize-run
    p_finalize = subparsers.add_parser("finalize-run")
    p_finalize.add_argument("--update-mode-coverage", action="store_true", help="Update docs/mode-coverage.yaml")

    args = parser.parse_args()

    if args.subcommand == "start-run":
        return handle_start_run(args)
    elif args.subcommand == "start-step":
        return handle_start_step(args)
    elif args.subcommand == "record-artifact":
        return handle_record_artifact(args)
    elif args.subcommand == "record-validation":
        return handle_record_validation(args)
    elif args.subcommand == "complete-step":
        return handle_complete_step(args)
    elif args.subcommand == "finalize-run":
        return handle_finalize_run(args)

    return 1


if __name__ == "__main__":
    sys.exit(main())
