#!/usr/bin/env python3
"""CLI utility to validate an artifact and record the facts to the run ledger.

Wraps the canonical validate-output.py dispatcher, computes hashes, and logs
both record-artifact and record-validation events to the ledger.
"""

import os
import sys
import argparse
import subprocess


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an artifact and record the facts to the ledger.")
    parser.add_argument("--ledger-path", required=True, help="Path to the ledger JSONL file")
    parser.add_argument("--step-id", required=True, help="Step ID")
    parser.add_argument("--artifact-id", required=True, help="Artifact ID from contract")
    parser.add_argument("--path", required=True, help="Path to the artifact file to validate")
    parser.add_argument("--repo-root", default=".", help="Root directory of the repository")

    args = parser.parse_args()

    repo_root = os.path.abspath(args.repo_root)
    ledger_path = os.path.abspath(args.ledger_path)
    artifact_path = os.path.abspath(args.path)

    # 1. Record the artifact creation fact first
    # This logs the artifact path and computes its SHA-256 hash.
    run_ledger_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run-ledger.py")
    
    art_cmd = [
        sys.executable,
        run_ledger_script,
        "--ledger-path", ledger_path,
        "--repo-root", repo_root,
        "record-artifact",
        "--step-id", args.step_id,
        "--artifact-id", args.artifact_id,
        "--path", artifact_path
    ]
    
    print(f"  ~ Recording artifact creation via run-ledger.py...")
    art_res = subprocess.run(art_cmd, capture_output=True, text=True)
    if art_res.returncode != 0:
        print(f"[ERROR] Failed to record artifact: {art_res.stderr or art_res.stdout}", file=sys.stderr)
        return 1

    # 2. Build the validator command
    validate_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "validate-output.py")
    # Store command relative to repo-root if possible for portability in the ledger
    try:
        rel_validate_script = os.path.relpath(validate_script, repo_root).replace("\\", "/")
    except ValueError:
        rel_validate_script = validate_script.replace("\\", "/")

    try:
        rel_artifact_path = os.path.relpath(artifact_path, repo_root).replace("\\", "/")
    except ValueError:
        rel_artifact_path = artifact_path.replace("\\", "/")
    
    val_command = f"python {rel_validate_script} {args.artifact_id} {rel_artifact_path}"

    # 3. Run the validator dispatcher
    run_val_cmd = [
        sys.executable,
        validate_script,
        args.artifact_id,
        artifact_path,
        "--repo-root", repo_root
    ]

    print(f"  ~ Running validation command: {val_command}")
    val_res = subprocess.run(run_val_cmd, capture_output=True, text=True)
    exit_code = val_res.returncode
    status = "passed" if exit_code == 0 else "failed"

    # Print output to stdout/stderr so executing environment/user can see it
    if val_res.stdout:
        print(val_res.stdout.strip())
    if val_res.stderr:
        print(val_res.stderr.strip(), file=sys.stderr)

    # 4. Record validation results
    val_cmd_to_log = f"python {rel_validate_script} {args.artifact_id} {rel_artifact_path} --repo-root ."
    rec_val_cmd = [
        sys.executable,
        run_ledger_script,
        "--ledger-path", ledger_path,
        "--repo-root", repo_root,
        "record-validation",
        "--step-id", args.step_id,
        "--artifact-id", args.artifact_id,
        "--command", val_cmd_to_log,
        "--exit-code", str(exit_code),
        "--status", status
    ]

    print(f"  ~ Recording validation fact via run-ledger.py...")
    rec_res = subprocess.run(rec_val_cmd, capture_output=True, text=True)
    if rec_res.returncode != 0:
        print(f"[ERROR] Failed to record validation fact: {rec_res.stderr or rec_res.stdout}", file=sys.stderr)
        return 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
