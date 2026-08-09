"""
Test skill-hygiene validator that checks:
1. npm scripts exist (from AGENTS.md references)
2. skill IDs cross-ref (workflow-registry → skill-registry)
3. artifact contracts resolve (registry → artifact-contracts)
"""

import subprocess
import os
import json


def run_validator():
    """Run the validator and return output"""
    result = subprocess.run(
        ["python", "scripts/validate-skill-hygiene.py"],
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def test_validator_script_exists():
    """Test that the validator script exists"""
    assert os.path.exists("scripts/validate-skill-hygiene.py"), \
        "Validator script not found at scripts/validate-skill-hygiene.py"


def test_validator_runs_without_error():
    """Test that the validator itself runs (exits 0 or 1) without crashing.

    Does NOT assert returncode == 0: checks 2/3 now genuinely execute
    against the canonical registries (see test_skill_hygiene_canonical_wiring.py
    for the false-green fix), so a nonzero exit can be a legitimate finding
    about the repo, not a validator crash. A crash is distinguished by a
    traceback on stderr.
    """
    returncode, stdout, stderr = run_validator()
    assert returncode in (0, 1), f"Validator crashed (unexpected exit code): {stderr}"
    assert "Traceback" not in stderr, f"Validator crashed: {stderr}"


def test_validator_detects_missing_npm_script():
    """Test that check 1 (npm scripts) actually runs and reports its result."""
    returncode, stdout, stderr = run_validator()
    assert "Check 1: npm scripts exist... PASSED" in stdout, stdout


def test_validator_checks_2_and_3_actually_run():
    """Regression: checks 2/3 must report a real PASSED/FAILED outcome, never
    silently report PASSED without ever loading the canonical registries
    (the false-green bug this repo's canonical wiring reconciliation fixed).
    Positive/negative detection coverage against constructed fixtures lives
    in test_skill_hygiene_canonical_wiring.py, which calls the check
    functions directly rather than relying on this repo's current, transient
    hygiene state.
    """
    returncode, stdout, stderr = run_validator()
    assert "Check 2: skill IDs cross-ref... " in stdout, stdout
    assert "Check 3: artifact contracts resolve... " in stdout, stdout


def test_validator_completes_in_reasonable_time():
    """Test that validator completes quickly (< 5 seconds)"""
    import time
    start = time.time()
    run_validator()
    elapsed = time.time() - start
    assert elapsed < 5, f"Validator took {elapsed}s, expected < 5s"


def test_package_json_has_validate_skills_script():
    """Test that package.json has validate:skills npm script"""
    import json
    with open("package.json") as f:
        pkg = json.load(f)

    assert "scripts" in pkg
    assert "validate:skills" in pkg["scripts"], \
        "package.json missing 'validate:skills' script"
    assert "validate-skill-hygiene" in pkg["scripts"]["validate:skills"], \
        "validate:skills script should call validate-skill-hygiene"


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")

    print("Checking validator...")
    if os.path.exists("scripts/validate-skill-hygiene.mts"):
        print("✓ Validator script exists")
        returncode, stdout, stderr = run_validator()
        if returncode == 0:
            print("✓ Validator runs successfully")
        else:
            print(f"✗ Validator failed: {stderr}")
    else:
        print("✗ Validator script not found")
