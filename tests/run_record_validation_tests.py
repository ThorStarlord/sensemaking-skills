#!/usr/bin/env python3
"""Test runner for record-validation.py."""

import sys
import os
import json
import tempfile
import subprocess
from pathlib import Path


def run_cmd(cmd, stdin_data=None, cwd=None):
    """Run a command with optional stdin."""
    result = subprocess.run(
        cmd,
        input=stdin_data,
        capture_output=True,
        text=True,
        cwd=cwd or "."
    )
    return result.stdout, result.stderr, result.returncode


def run_tests():
    """Run all tests for record-validation.py."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tests_run = 0
    tests_passed = 0

    # Create a temporary directory for test logs
    with tempfile.TemporaryDirectory() as tmpdir:
        run_log = os.path.join(tmpdir, "validation.log")

        # Test 1: Valid validation result logs correctly
        print("[TEST 1] Valid artifact validation logs correctly")
        valid_result = {
            "valid": True,
            "artifact_id": "repository_sensemaking_brief",
            "artifact_path": "/path/to/brief.md",
            "validator": "validate-brief.py",
            "errors": [],
            "validation_timestamp": "2026-05-25T10:30:00Z"
        }
        stdout, stderr, returncode = run_cmd(
            ["python3", "scripts/record-validation.py", "--run-log", run_log],
            stdin_data=json.dumps(valid_result),
            cwd=repo_root
        )
        tests_run += 1
        if returncode == 0 and os.path.exists(run_log):
            with open(run_log) as f:
                log_content = f.read()
            if "VALID" in log_content and "repository_sensemaking_brief" in log_content:
                tests_passed += 1
                print("  PASSED: Valid result logged with correct content")
            else:
                print("  FAILED: Log content missing expected entries")
        else:
            print(f"  FAILED: Return code {returncode}, log exists: {os.path.exists(run_log)}")

        # Test 2: Invalid validation result logs all error_ids
        print("[TEST 2] Invalid artifact validation logs all error_ids")
        invalid_result = {
            "valid": False,
            "artifact_id": "repository_sensemaking_brief",
            "artifact_path": "/path/to/brief.md",
            "validator": "validate-brief.py",
            "errors": [
                {
                    "error_id": "repository_sensemaking_brief.primary_fog_type.missing_field",
                    "error_type": "missing_field",
                    "field": "primary_fog_type",
                    "current_value": None,
                    "message": "Required field is missing.",
                    "suggested_fixes": ["Add primary_fog_type: product_fog"],
                    "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
                },
                {
                    "error_id": "repository_sensemaking_brief.evidence.logic_error",
                    "error_type": "logic_error",
                    "field": "evidence",
                    "current_value": [],
                    "message": "Evidence list is empty.",
                    "suggested_fixes": ["Add evidence entries"],
                    "reference": "docs/adr/0003-artifact-composition-pattern.md"
                }
            ],
            "validation_timestamp": "2026-05-25T10:30:00Z"
        }
        run_log2 = os.path.join(tmpdir, "validation2.log")
        stdout, stderr, returncode = run_cmd(
            ["python3", "scripts/record-validation.py", "--run-log", run_log2],
            stdin_data=json.dumps(invalid_result),
            cwd=repo_root
        )
        tests_run += 1
        if returncode == 0 and os.path.exists(run_log2):
            with open(run_log2) as f:
                log_content = f.read()
            has_error1 = "repository_sensemaking_brief.primary_fog_type.missing_field" in log_content
            has_error2 = "repository_sensemaking_brief.evidence.logic_error" in log_content
            has_invalid = "INVALID" in log_content
            has_error_count = "Error count: 2" in log_content
            if has_error1 and has_error2 and has_invalid and has_error_count:
                tests_passed += 1
                print("  PASSED: All error_ids logged with error count")
            else:
                print("  FAILED: Missing error_ids or error count in log")
                if not has_error1:
                    print("    Missing error_id 1")
                if not has_error2:
                    print("    Missing error_id 2")
                if not has_error_count:
                    print("    Missing error count")
        else:
            print(f"  FAILED: Return code {returncode}")

        # Test 3: stdin input works
        print("[TEST 3] stdin input works")
        run_log3 = os.path.join(tmpdir, "validation3.log")
        stdout, stderr, returncode = run_cmd(
            ["python3", "scripts/record-validation.py", "--run-log", run_log3],
            stdin_data=json.dumps(valid_result),
            cwd=repo_root
        )
        tests_run += 1
        if returncode == 0 and os.path.exists(run_log3):
            tests_passed += 1
            print("  PASSED: stdin input processed successfully")
        else:
            print(f"  FAILED: Return code {returncode}")

        # Test 4: file input works
        print("[TEST 4] file input works")
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(valid_result, f)
            json_file = f.name
        try:
            run_log4 = os.path.join(tmpdir, "validation4.log")
            stdout, stderr, returncode = run_cmd(
                ["python3", "scripts/record-validation.py", "--validation-json", json_file, "--run-log", run_log4],
                cwd=repo_root
            )
            tests_run += 1
            if returncode == 0 and os.path.exists(run_log4):
                tests_passed += 1
                print("  PASSED: file input processed successfully")
            else:
                print(f"  FAILED: Return code {returncode}")
        finally:
            os.unlink(json_file)

        # Test 5: missing or invalid JSON handled gracefully
        print("[TEST 5] invalid JSON handled gracefully")
        run_log5 = os.path.join(tmpdir, "validation5.log")
        stdout, stderr, returncode = run_cmd(
            ["python3", "scripts/record-validation.py", "--run-log", run_log5],
            stdin_data="{ invalid json }",
            cwd=repo_root
        )
        tests_run += 1
        if returncode != 0 and "ERROR" in stderr:
            tests_passed += 1
            print("  PASSED: invalid JSON rejected gracefully")
        else:
            print(f"  FAILED: invalid JSON should return error code, got {returncode}")

        # Test 6: script does not modify artifact
        print("[TEST 6] script does not modify artifact")
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Test Artifact\n\nOriginal content\n")
            artifact_file = f.name
        try:
            original_mtime = os.path.getmtime(artifact_file)
            with open(artifact_file) as f:
                original_content = f.read()

            run_log6 = os.path.join(tmpdir, "validation6.log")
            stdout, stderr, returncode = run_cmd(
                ["python3", "scripts/record-validation.py", "--run-log", run_log6],
                stdin_data=json.dumps({
                    "valid": False,
                    "artifact_id": "test",
                    "artifact_path": artifact_file,
                    "validator": "test",
                    "errors": [],
                    "validation_timestamp": "2026-05-25T10:30:00Z"
                }),
                cwd=repo_root
            )

            # Check artifact unchanged
            with open(artifact_file) as f:
                new_content = f.read()
            new_mtime = os.path.getmtime(artifact_file)

            tests_run += 1
            if original_content == new_content and returncode == 0:
                tests_passed += 1
                print("  PASSED: artifact not modified by record-validation.py")
            else:
                print(f"  FAILED: artifact was modified or record failed")
        finally:
            os.unlink(artifact_file)

        # Test 7: log file is created if missing
        print("[TEST 7] log file created if missing")
        run_log7 = os.path.join(tmpdir, "subdir", "validation7.log")
        stdout, stderr, returncode = run_cmd(
            ["python3", "scripts/record-validation.py", "--run-log", run_log7],
            stdin_data=json.dumps(valid_result),
            cwd=repo_root
        )
        tests_run += 1
        if returncode == 0 and os.path.exists(run_log7):
            tests_passed += 1
            print("  PASSED: log file created with parent directories")
        else:
            print(f"  FAILED: log file not created")

        # Test 8: log file can be appended to
        print("[TEST 8] multiple entries append correctly")
        run_log8 = os.path.join(tmpdir, "validation8.log")

        # First entry
        stdout, stderr, returncode = run_cmd(
            ["python3", "scripts/record-validation.py", "--run-log", run_log8],
            stdin_data=json.dumps(valid_result),
            cwd=repo_root
        )

        # Second entry
        invalid_result["validation_timestamp"] = "2026-05-25T10:31:00Z"
        stdout, stderr, returncode = run_cmd(
            ["python3", "scripts/record-validation.py", "--run-log", run_log8],
            stdin_data=json.dumps(invalid_result),
            cwd=repo_root
        )

        tests_run += 1
        if returncode == 0:
            with open(run_log8) as f:
                log_content = f.read()
            # Count how many validation attempt headers we have
            attempt_count = log_content.count("## Validation Attempt")
            if attempt_count == 2:
                tests_passed += 1
                print("  PASSED: multiple entries appended correctly")
            else:
                print(f"  FAILED: expected 2 entries, found {attempt_count}")
        else:
            print(f"  FAILED: Return code {returncode}")

    print(f"\n[SUMMARY] {tests_passed}/{tests_run} tests passed")
    return 0 if tests_passed == tests_run else 1


if __name__ == "__main__":
    sys.exit(run_tests())
