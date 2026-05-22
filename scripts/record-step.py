#!/usr/bin/env python3
"""CLI utility to record step start and completion facts to a run ledger.

Maintains step provenance, input/output paths, SHA-256 hashes, git commit SHAs,
validation exit codes, and timestamps.
"""

import os
import sys
import argparse
import datetime
import hashlib
import yaml


def get_git_commit(repo_root: str) -> str:
    try:
        import subprocess
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception:
        return "unknown_commit"


def compute_file_hash(path: str) -> str | None:
    if not os.path.exists(path):
        return None
    sha256 = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256.update(byte_block)
        return sha256.hexdigest()
    except Exception:
        return "hash_error"


def handle_start(args) -> int:
    repo_root = os.path.abspath(args.repo_root)
    ledger_path = os.path.abspath(args.ledger_path)
    
    # Resolve Git commit if not provided
    git_commit = args.git_commit
    if not git_commit or git_commit == "auto":
        git_commit = get_git_commit(repo_root)

    # Calculate input artifact hashes
    inputs = []
    if args.input_artifacts:
        paths = [p.strip() for p in args.input_artifacts.split(",")]
        for p in paths:
            if not p:
                continue
            # Calculate path relative to repo_root for portability if under repo_root
            abs_p = os.path.abspath(p)
            rel_p = os.path.relpath(abs_p, repo_root).replace("\\", "/") if abs_p.startswith(repo_root) else p
            
            f_hash = compute_file_hash(abs_p)
            inputs.append({
                "path": rel_p,
                "hash": f_hash or "file_not_found"
            })

    now_str = datetime.datetime.now().isoformat()
    
    # Load or initialize ledger
    ledger_data = {}
    if os.path.exists(ledger_path):
        try:
            with open(ledger_path, "r", encoding="utf-8") as f:
                ledger_data = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"[ERROR] Failed to load existing ledger at {args.ledger_path}: {e}", file=sys.stderr)
            return 1
    
    if not ledger_data:
        # Initialize ledger structure
        run_id = args.run_id or f"run-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
        ledger_data = {
            "run_metadata": {
                "run_id": run_id,
                "git_commit": git_commit,
                "timestamp_start": now_str,
                "status": "started"
            },
            "steps": []
        }
        print(f"  ~ Initializing new run ledger for run_id: {run_id}")

    # Set/update workflow_id and mode in run_metadata if provided
    if getattr(args, "workflow_id", None):
        ledger_data.setdefault("run_metadata", {})["workflow_id"] = args.workflow_id
    if getattr(args, "mode", None):
        ledger_data.setdefault("run_metadata", {})["mode"] = args.mode

    steps = ledger_data.setdefault("steps", [])
    
    # Check if step already exists
    step_id_str = str(args.step_id)
    step = next((s for s in steps if str(s.get("step_id")) == step_id_str), None)
    
    if step:
        # Update existing step
        step["status"] = "started"
        step["timestamp_start"] = now_str
        step["inputs"] = inputs
        step["skill_id"] = args.skill_id
        if git_commit:
            step["git_commit"] = git_commit
        print(f"  ~ Updated existing step {step_id_str} status to started")
    else:
        # Append new step
        step = {
            "step_id": args.step_id,
            "skill_id": args.skill_id,
            "status": "started",
            "timestamp_start": now_str,
            "inputs": inputs,
            "git_commit": git_commit
        }
        steps.append(step)
        print(f"  ~ Appended new step {step_id_str} in ledger")

    # Save ledger
    os.makedirs(os.path.dirname(ledger_path), exist_ok=True)
    try:
        with open(ledger_path, "w", encoding="utf-8") as f:
            yaml.dump(ledger_data, f, default_flow_style=False)
        print(f"[OK] Step {step_id_str} started recorded in {args.ledger_path}")
        return 0
    except Exception as e:
        print(f"[ERROR] Failed to write ledger: {e}", file=sys.stderr)
        return 1


def handle_complete(args) -> int:
    repo_root = os.path.abspath(args.repo_root)
    ledger_path = os.path.abspath(args.ledger_path)
    
    if not os.path.exists(ledger_path):
        print(f"[ERROR] Ledger file not found: {args.ledger_path}", file=sys.stderr)
        return 1

    try:
        with open(ledger_path, "r", encoding="utf-8") as f:
            ledger_data = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"[ERROR] Failed to read ledger: {e}", file=sys.stderr)
        return 1

    steps = ledger_data.get("steps", [])
    step_id_str = str(args.step_id)
    step = next((s for s in steps if str(s.get("step_id")) == step_id_str), None)

    if not step:
        # If complete is called directly without start, create a draft step record
        print(f"  [WARN] Step {step_id_str} not started in ledger, creating completed step record directly.")
        step = {
            "step_id": args.step_id,
            "skill_id": "unknown",
            "timestamp_start": datetime.datetime.now().isoformat()
        }
        steps.append(step)

    # Update completion facts
    step["status"] = args.status
    step["timestamp_end"] = datetime.datetime.now().isoformat()
    
    # Calculate output hashes
    if args.output_artifact:
        abs_out = os.path.abspath(args.output_artifact)
        rel_out = os.path.relpath(abs_out, repo_root).replace("\\", "/") if abs_out.startswith(repo_root) else args.output_artifact
        out_hash = compute_file_hash(abs_out)
        
        step["outputs"] = [{
            "path": rel_out,
            "hash": out_hash or "file_not_found"
        }]

    if args.validator_command:
        step["validator_command"] = args.validator_command
    
    if args.validator_exit_code is not None:
        step["validator_exit_code"] = args.validator_exit_code

    if args.gate_status:
        step["gate_status"] = args.gate_status

    # Save ledger
    try:
        with open(ledger_path, "w", encoding="utf-8") as f:
            yaml.dump(ledger_data, f, default_flow_style=False)
        print(f"[OK] Step {step_id_str} complete ({args.status}) recorded in {args.ledger_path}")
        return 0
    except Exception as e:
        print(f"[ERROR] Failed to write ledger: {e}", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Record step lifecycle to a run ledger.")
    parser.add_argument("--repo-root", default=".", help="Root directory of the repository")
    parser.add_argument("--ledger-path", required=True, help="Path to the ledger YAML file")
    parser.add_argument("--step-id", required=True, help="ID or name of the step")
    
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Start subcommand
    parser_start = subparsers.add_parser("start", help="Record step execution start")
    parser_start.add_argument("--run-id", help="Optional run ID (only used when initializing)")
    parser_start.add_argument("--skill-id", required=True, help="ID of the skill running")
    parser_start.add_argument("--input-artifacts", help="Comma-separated paths to input files")
    parser_start.add_argument("--git-commit", help="Git commit SHA (defaults to HEAD commit)")
    parser_start.add_argument("--workflow-id", help="Optional workflow ID for ledger metadata")
    parser_start.add_argument("--mode", help="Optional execution mode for ledger metadata")

    # Complete subcommand
    parser_complete = subparsers.add_parser("complete", help="Record step execution completion")
    parser_complete.add_argument("--output-artifact", help="Path to the output file produced")
    parser_complete.add_argument("--validator-command", help="Validator command executed")
    parser_complete.add_argument("--validator-exit-code", type=int, help="Validator process exit code")
    parser_complete.add_argument("--status", default="passed", choices=["passed", "failed", "skipped"], help="Execution status")
    parser_complete.add_argument("--gate-status", choices=["approved", "denied", "bypassed", "none"], help="Approval gate status")

    args = parser.parse_args()

    if args.command == "start":
        return handle_start(args)
    elif args.command == "complete":
        return handle_complete(args)
    
    return 1


if __name__ == "__main__":
    sys.exit(main())
