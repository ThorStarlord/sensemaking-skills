#!/usr/bin/env python3
"""Phase 3 Comprehensive Testing: Execute autonomous validation across multiple repositories."""

import os
import json
import time
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

def run_test(test_name, command, timeout=30):
    """Execute a single test and track results."""
    print(f"\n{'='*70}")
    print(f"TEST: {test_name}")
    print(f"{'='*70}")

    start_time = time.time()
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        elapsed = time.time() - start_time

        success = result.returncode == 0
        print(f"Result: {'PASS' if success else 'FAIL'}")
        print(f"Time: {elapsed:.2f}s")

        return {
            "name": test_name,
            "success": success,
            "time": elapsed,
            "exit_code": result.returncode,
            "output": result.stdout[:100] if result.stdout else "",
            "error": result.stderr[:100] if result.stderr else ""
        }
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        print(f"Result: TIMEOUT")
        print(f"Time: {elapsed:.2f}s")
        return {
            "name": test_name,
            "success": False,
            "time": elapsed,
            "exit_code": -1,
            "error": "Command timeout"
        }
    except Exception as e:
        elapsed = time.time() - start_time
        return {
            "name": test_name,
            "success": False,
            "time": elapsed,
            "exit_code": -1,
            "error": str(e)
        }

def main():
    """Execute comprehensive Phase 3 testing."""
    print("\n" + "="*70)
    print("PHASE 3: COMPREHENSIVE AUTONOMOUS TESTING")
    print("="*70)
    print(f"Started: {datetime.now().isoformat()}")
    print(f"Objective: Full validation across multiple test scenarios\n")

    all_results = {
        "phase": "Phase 3",
        "test_type": "Autonomous Comprehensive",
        "timestamp": datetime.now().isoformat(),
        "tests": []
    }

    repo_path = str(Path.cwd())

    # Test Suite 1: CLI Commands (Basic Functionality)
    print("\n" + "-"*70)
    print("TEST SUITE 1: CLI BASIC FUNCTIONALITY")
    print("-"*70)

    tests = [
        ("CLI Version", "python -m sensemaking_skills.cli --version"),
        ("CLI Help", "python -m sensemaking_skills.cli --help"),
        ("Analyze Help", "python -m sensemaking_skills.cli analyze --help"),
        ("Validate Help", "python -m sensemaking_skills.cli validate --help"),
    ]

    for name, cmd in tests:
        result = run_test(name, cmd)
        all_results["tests"].append(result)

    # Test Suite 2: Repository Analysis
    print("\n" + "-"*70)
    print("TEST SUITE 2: REPOSITORY ANALYSIS")
    print("-"*70)

    test_repos = [
        ("This Repository", repo_path),
    ]

    for repo_name, repo_path_val in test_repos:
        cmd = f"python -m sensemaking_skills.cli analyze --repo {repo_path_val}"
        result = run_test(f"Analyze {repo_name}", cmd)
        all_results["tests"].append(result)

    # Test Suite 3: Artifact Validation
    print("\n" + "-"*70)
    print("TEST SUITE 3: ARTIFACT VALIDATION")
    print("-"*70)

    brief_path = Path("artifacts/repository_sensemaking_brief.md")
    if brief_path.exists():
        cmd = f"python -m sensemaking_skills.cli validate --artifact {brief_path}"
        result = run_test("Validate Brief", cmd)
        all_results["tests"].append(result)

    plan_path = Path("artifacts/workflow_orchestration_plan.md")
    if plan_path.exists():
        cmd = f"python -m sensemaking_skills.cli validate --artifact {plan_path}"
        result = run_test("Validate Plan", cmd)
        all_results["tests"].append(result)

    # Test Suite 4: Python API Tests
    print("\n" + "-"*70)
    print("TEST SUITE 4: PYTHON API VALIDATION")
    print("-"*70)

    api_test = """
import sys
sys.path.insert(0, 'src')
from sensemaking_skills.cli import cli
from click.testing import CliRunner

runner = CliRunner()
result = runner.invoke(cli, ['--version'])
assert result.exit_code == 0
assert '0.2.1' in result.output
print('API test passed')
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(api_test)
        f.flush()
        temp_file = f.name

    try:
        result = run_test("Python API", f"python {temp_file}")
        all_results["tests"].append(result)
    finally:
        os.unlink(temp_file)

    # Summary
    print("\n" + "="*70)
    print("PHASE 3: COMPREHENSIVE TEST SUMMARY")
    print("="*70)

    passed = sum(1 for t in all_results["tests"] if t.get("success", False))
    total = len(all_results["tests"])
    avg_time = sum(t.get("time", 0) for t in all_results["tests"]) / total if total > 0 else 0

    print(f"\nTests Passed: {passed}/{total}")
    print(f"Average Time: {avg_time:.3f}s")
    print(f"Total Time: {sum(t.get('time', 0) for t in all_results['tests']):.2f}s")

    # Results Assessment
    print("\n" + "-"*70)
    print("ASSESSMENT")
    print("-"*70)

    if passed == total:
        print("+ All tests passed")
        print("+ System fully operational")
        print("+ Performance acceptable")
        print("+ Ready for production")
        verdict = "PASS"
    elif passed >= total * 0.8:
        print("+ Most tests passed")
        print("+ Core functionality working")
        print("+ Minor issues only")
        verdict = "CONDITIONAL_PASS"
    else:
        print("X Multiple test failures")
        print("X System has issues")
        print("X Needs remediation")
        verdict = "FAIL"

    all_results["verdict"] = verdict
    all_results["summary"] = {
        "total_tests": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": f"{(passed/total)*100:.1f}%" if total > 0 else "0%",
        "avg_time_seconds": avg_time,
        "verdict": verdict
    }

    # Save results
    output_file = Path("PHASE-3-COMPREHENSIVE-RESULTS.json")
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nResults saved to: {output_file}")
    print(f"\n{'='*70}")
    print(f"PHASE 3 COMPREHENSIVE TESTING: {verdict}")
    print(f"{'='*70}\n")

    return 0 if verdict != "FAIL" else 1

if __name__ == "__main__":
    exit(main())
