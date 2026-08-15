#!/usr/bin/env python3
"""Integration test for unified validation pipeline (Task 3).

Tests that:
1. validate-and-report.py routes correctly based on artifact_id
2. record-validation.py logs results to run log
3. workflow-runtime.py integrates both correctly
"""

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


def test_unified_validator_pipeline():
    """Test the complete Phase 1 validation pipeline."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tests_run = 0
    tests_passed = 0

    with tempfile.TemporaryDirectory() as tmpdir:
        run_log = os.path.join(tmpdir, "validation_run_log.md")

        # Test 1: Valid brief artifact
        print("[TEST 1] validate-and-report.py with valid brief")
        valid_brief = os.path.join(repo_root, "tests", "fixtures", "brief-valid.md")
        if not os.path.exists(valid_brief):
            print("  SKIPPED: brief-valid.md fixture not found")
        else:
            stdout, stderr, returncode = run_cmd(
                [sys.executable, "scripts/validate-and-report.py", valid_brief],
                cwd=repo_root
            )
            tests_run += 1
            try:
                result = json.loads(stdout)
                if result.get("valid") and returncode == 0:
                    tests_passed += 1
                    print(f"  PASSED: validate-and-report.py returned valid JSON with valid=true")
                else:
                    print(f"  FAILED: Expected valid=true, got {result.get('valid')}, returncode={returncode}")
            except json.JSONDecodeError as e:
                print(f"  FAILED: Output was not valid JSON: {e}")

        # Test 2: Invalid brief artifact + logging
        print("[TEST 2] validate-and-report.py with invalid brief + record-validation.py")
        invalid_brief = os.path.join(repo_root, "tests", "fixtures", "brief-invalid-missing-fields.md")
        if not os.path.exists(invalid_brief):
            print("  SKIPPED: brief-invalid-missing-fields.md fixture not found")
        else:
            run_log_test2 = os.path.join(tmpdir, "test2_validation.log")

            # Step 1: Get validation output
            stdout, stderr, returncode = run_cmd(
                [sys.executable, "scripts/validate-and-report.py", invalid_brief],
                cwd=repo_root
            )

            tests_run += 1
            try:
                validation_result = json.loads(stdout)

                if not validation_result.get("valid") and returncode == 1:
                    # Step 2: Pipe to record-validation.py
                    log_stdout, log_stderr, log_rc = run_cmd(
                        [sys.executable, "scripts/record-validation.py", "--run-log", run_log_test2],
                        stdin_data=json.dumps(validation_result),
                        cwd=repo_root
                    )

                    if log_rc == 0 and os.path.exists(run_log_test2):
                        with open(run_log_test2) as f:
                            log_content = f.read()

                        # Verify log contains expected entries
                        has_header = "# Validation Run Log" in log_content
                        has_attempt = "## Validation Attempt" in log_content
                        has_invalid = "**INVALID**" in log_content
                        has_errors = "error_id" in log_content

                        if has_header and has_attempt and has_invalid and has_errors:
                            tests_passed += 1
                            print(f"  PASSED: Validation logged to run log with all expected fields")
                        else:
                            print(f"  FAILED: Log missing expected content")
                            print(f"    header={has_header}, attempt={has_attempt}, invalid={has_invalid}, errors={has_errors}")
                    else:
                        print(f"  FAILED: record-validation.py failed, rc={log_rc}")
                else:
                    print(f"  FAILED: Expected valid=false with rc=1, got valid={validation_result.get('valid')}, rc={returncode}")

            except json.JSONDecodeError as e:
                print(f"  FAILED: validate-and-report.py output was not valid JSON: {e}")

        # Test 3: Multiple entries in run log (append behavior)
        print("[TEST 3] Multiple validation entries append correctly to run log")
        run_log_test3 = os.path.join(tmpdir, "test3_validation.log")

        # Create first entry
        stdout1, _, _ = run_cmd(
            [sys.executable, "scripts/validate-and-report.py", valid_brief],
            cwd=repo_root
        )
        result1 = json.loads(stdout1)
        _, _, _ = run_cmd(
            [sys.executable, "scripts/record-validation.py", "--run-log", run_log_test3],
            stdin_data=json.dumps(result1),
            cwd=repo_root
        )

        # Create second entry
        stdout2, _, _ = run_cmd(
            [sys.executable, "scripts/validate-and-report.py", invalid_brief],
            cwd=repo_root
        )
        result2 = json.loads(stdout2)
        _, _, rc2 = run_cmd(
            [sys.executable, "scripts/record-validation.py", "--run-log", run_log_test3],
            stdin_data=json.dumps(result2),
            cwd=repo_root
        )

        tests_run += 1
        if rc2 == 0 and os.path.exists(run_log_test3):
            with open(run_log_test3) as f:
                log_content = f.read()

            attempt_count = log_content.count("## Validation Attempt")
            if attempt_count == 2:
                tests_passed += 1
                print(f"  PASSED: Multiple entries appended correctly (count={attempt_count})")
            else:
                print(f"  FAILED: Expected 2 entries, found {attempt_count}")
        else:
            print(f"  FAILED: Second record-validation.py call failed, rc={rc2}")

        # Test 4: Validate routing based on artifact_id
        print("[TEST 4] validate-and-report.py correctly routes to validate-brief.py")
        tests_run += 1
        if os.path.exists(valid_brief):
            stdout, _, returncode = run_cmd(
                [sys.executable, "scripts/validate-and-report.py", valid_brief],
                cwd=repo_root
            )
            try:
                result = json.loads(stdout)
                if result.get("artifact_id") == "repository_sensemaking_brief" and \
                   result.get("validator") == "validate-brief.py":
                    tests_passed += 1
                    print(f"  PASSED: Correctly routed to validate-brief.py")
                else:
                    print(f"  FAILED: artifact_id={result.get('artifact_id')}, validator={result.get('validator')}")
            except json.JSONDecodeError:
                print(f"  FAILED: Invalid JSON output")

    print(f"\n[SUMMARY] {tests_passed}/{tests_run} tests passed")
    return 0 if tests_passed == tests_run else 1


if __name__ == "__main__":
    sys.exit(test_unified_validator_pipeline())
