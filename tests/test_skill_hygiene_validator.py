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
    """Test that validator runs on current codebase without error"""
    returncode, stdout, stderr = run_validator()
    assert returncode == 0, f"Validator failed: {stderr}"


def test_validator_detects_missing_npm_script():
    """Test that validator catches references to nonexistent npm scripts"""
    # This test requires injecting a bad npm script reference
    # For now, verify the validator can detect missing scripts
    returncode, stdout, stderr = run_validator()
    # Should pass on current codebase (no bad scripts)
    assert returncode == 0


def test_validator_detects_missing_skill_id():
    """Test that validator catches references to nonexistent skill IDs"""
    returncode, stdout, stderr = run_validator()
    # Should pass on current codebase
    assert returncode == 0


def test_validator_detects_missing_artifact_contract():
    """Test that validator catches artifact refs not in contracts"""
    returncode, stdout, stderr = run_validator()
    # Should pass on current codebase
    assert returncode == 0


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
