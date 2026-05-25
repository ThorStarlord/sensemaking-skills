#!/usr/bin/env python3
"""Test runner for validate-and-report.py."""

import sys
import os
import json
import subprocess

def run_cmd(cmd, cwd=None):
    """Run a command and return (stdout, stderr, returncode)."""
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd or "."
    )
    return result.stdout, result.stderr, result.returncode

def run_tests():
    """Run all tests for validate-and-report.py."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fixtures_dir = os.path.join(repo_root, "tests", "fixtures")

    tests_run = 0
    tests_passed = 0

    print("[TEST 1] Valid brief routes to validate-brief.py")
    artifact_path = os.path.join(fixtures_dir, "brief-valid.md")
    stdout, stderr, returncode = run_cmd(
        ["python3", "scripts/validate-and-report.py", artifact_path],
        cwd=repo_root
    )
    tests_run += 1
    try:
        result = json.loads(stdout)
        checks = [
            result["valid"] == True,
            result["artifact_id"] == "repository_sensemaking_brief",
            result["validator"] == "validate-brief.py",
            "errors" in result,
            result["errors"] == [],
            returncode == 0
        ]
        if all(checks):
            tests_passed += 1
            print("  PASSED: Valid brief routed to validate-brief.py and returned clean result")
        else:
            print(f"  FAILED: JSON structure or content issues")
            print(f"    Valid: {result.get('valid')}")
            print(f"    Artifact ID: {result.get('artifact_id')}")
            print(f"    Validator: {result.get('validator')}")
    except json.JSONDecodeError as e:
        print(f"  FAILED: Invalid JSON output: {str(e)}")

    print("[TEST 2] Valid plan routes to validate-plan.py")
    artifact_path = os.path.join(fixtures_dir, "plan-valid.md")
    stdout, stderr, returncode = run_cmd(
        ["python3", "scripts/validate-and-report.py", artifact_path],
        cwd=repo_root
    )
    tests_run += 1
    try:
        result = json.loads(stdout)
        checks = [
            result["valid"] == True,
            result["artifact_id"] == "workflow_orchestration_plan",
            result["validator"] == "validate-plan.py",
            result["errors"] == [],
            returncode == 0
        ]
        if all(checks):
            tests_passed += 1
            print("  PASSED: Valid plan routed to validate-plan.py and returned clean result")
        else:
            print(f"  FAILED: JSON structure or content issues")
            print(f"    Valid: {result.get('valid')}")
            print(f"    Artifact ID: {result.get('artifact_id')}")
            print(f"    Validator: {result.get('validator')}")
    except json.JSONDecodeError as e:
        print(f"  FAILED: Invalid JSON output: {str(e)}")

    print("[TEST 3] Known artifact (brief) correctly detected and routed")
    artifact_path = os.path.join(fixtures_dir, "artifact-generic-valid.md")
    stdout, stderr, returncode = run_cmd(
        ["python3", "scripts/validate-and-report.py", artifact_path],
        cwd=repo_root
    )
    tests_run += 1
    try:
        result = json.loads(stdout)
        # This artifact has artifact_id=repository_sensemaking_brief in YAML,
        # so it should route to validate-brief.py (correct behavior)
        checks = [
            result["valid"] == True,
            result["artifact_id"] == "repository_sensemaking_brief",
            result["validator"] == "validate-brief.py",
            result["errors"] == [],
            returncode == 0
        ]
        if all(checks):
            tests_passed += 1
            print("  PASSED: Artifact with known ID correctly routed to validate-brief.py")
        else:
            print(f"  FAILED: JSON structure or content issues")
            print(f"    Valid: {result.get('valid')}")
            print(f"    Validator: {result.get('validator')}")
    except json.JSONDecodeError as e:
        print(f"  FAILED: Invalid JSON output: {str(e)}")

    print("[TEST 4] Invalid brief returns structured errors")
    artifact_path = os.path.join(fixtures_dir, "brief-invalid-missing-fields.md")
    stdout, stderr, returncode = run_cmd(
        ["python3", "scripts/validate-and-report.py", artifact_path],
        cwd=repo_root
    )
    tests_run += 1
    try:
        result = json.loads(stdout)
        checks = [
            result["valid"] == False,
            len(result["errors"]) > 0,
            returncode == 1,
            "error_id" in result["errors"][0]
        ]
        if all(checks):
            tests_passed += 1
            print(f"  PASSED: Invalid brief returned {len(result['errors'])} structured errors")
            for error in result["errors"][:2]:
                print(f"    - {error.get('error_id')}: {error.get('error_type')}")
        else:
            print(f"  FAILED: Error structure issues")
            if result.get("errors"):
                print(f"    First error: {result['errors'][0]}")
    except json.JSONDecodeError as e:
        print(f"  FAILED: Invalid JSON output: {str(e)}")

    print("[TEST 5] Non-existent file returns structured error")
    artifact_path = os.path.join(fixtures_dir, "nonexistent-artifact.md")
    stdout, stderr, returncode = run_cmd(
        ["python3", "scripts/validate-and-report.py", artifact_path],
        cwd=repo_root
    )
    tests_run += 1
    try:
        result = json.loads(stdout)
        checks = [
            result["valid"] == False,
            len(result["errors"]) > 0,
            result["validator"] == "validate-and-report.py",
            returncode == 2,  # Exit code 2 for helper/execution failure (not validation failure)
            "artifact_id" in result
        ]
        if all(checks):
            tests_passed += 1
            print("  PASSED: Non-existent file handled gracefully with structured error (exit code 2)")
        else:
            print(f"  FAILED: Error handling issues")
            print(f"    Valid: {result.get('valid')}")
            print(f"    Validator: {result.get('validator')}")
            print(f"    Exit code: {returncode} (expected 2)")
            print(f"    Errors: {len(result.get('errors', []))} (expected > 0)")
    except json.JSONDecodeError as e:
        print(f"  FAILED: Invalid JSON output: {str(e)}")

    print("[TEST 6] All results have unified schema")
    test_paths = [
        os.path.join(fixtures_dir, "brief-valid.md"),
        os.path.join(fixtures_dir, "plan-valid.md"),
        os.path.join(fixtures_dir, "brief-invalid-missing-fields.md"),
    ]
    tests_run += 1
    all_valid_schema = True
    for artifact_path in test_paths:
        stdout, stderr, returncode = run_cmd(
            ["python3", "scripts/validate-and-report.py", artifact_path],
            cwd=repo_root
        )
        try:
            result = json.loads(stdout)
            required_keys = {"valid", "artifact_id", "artifact_path", "validator", "errors", "validation_timestamp"}
            if not required_keys.issubset(result.keys()):
                all_valid_schema = False
                print(f"    Missing keys in {artifact_path}: {required_keys - result.keys()}")
        except json.JSONDecodeError:
            all_valid_schema = False
            print(f"    Invalid JSON from {artifact_path}")

    if all_valid_schema:
        tests_passed += 1
        print("  PASSED: All results have unified schema with all required keys")
    else:
        print("  FAILED: Some results missing required schema keys")

    print("[TEST 7] error_id preserved in routed validation")
    artifact_path = os.path.join(fixtures_dir, "brief-invalid-missing-fields.md")
    stdout, stderr, returncode = run_cmd(
        ["python3", "scripts/validate-and-report.py", artifact_path],
        cwd=repo_root
    )
    tests_run += 1
    try:
        result = json.loads(stdout)
        error_ids_present = all("error_id" in e for e in result["errors"])
        if error_ids_present and len(result["errors"]) > 0:
            tests_passed += 1
            print(f"  PASSED: All {len(result['errors'])} errors have error_id fields")
            for error in result["errors"][:2]:
                print(f"    - {error.get('error_id')}")
        else:
            print("  FAILED: Some errors missing error_id")
    except json.JSONDecodeError as e:
        print(f"  FAILED: Invalid JSON output: {str(e)}")

    print(f"\n[SUMMARY] {tests_passed}/{tests_run} tests passed")
    return 0 if tests_passed == tests_run else 1

if __name__ == "__main__":
    sys.exit(run_tests())
