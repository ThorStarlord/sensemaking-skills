"""File M: Validator test suite for architectural-review-recommendation artifacts.

Tests the specialized validator (File D) against approved fixtures (Files H-L).
Proves that the validator correctly enforces decision-outcome field rules.
"""

import os
import sys
import json
import subprocess

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "architectural-review-recommendation")
REPO_ROOT = os.path.dirname(os.path.dirname(__file__))


def run_validator(artifact_path: str) -> dict:
    """Run File D (validate-architectural-review-recommendation.py) and return JSON result."""
    result = subprocess.run(
        [sys.executable, os.path.join(SCRIPTS_DIR, "validate-architectural-review-recommendation.py"),
         artifact_path, "--json"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        return {"valid": False, "error": f"JSON parse error: {e}", "stdout": result.stdout[:200], "stderr": result.stderr[:200]}


def test_fixture_valid_pursue():
    """Fixture H: Valid pursue decision should pass validation."""
    fixture_path = os.path.join(FIXTURES_DIR, "fixture-valid-pursue.md")
    result = run_validator(fixture_path)

    assert result["valid"] is True, f"Fixture H should pass validation, got errors: {result.get('errors')}"
    assert result["artifact_id"] == "architectural_review_recommendation"
    assert len(result["errors"]) == 0
    print("[PASS] Fixture H (valid-pursue): Validator correctly passes valid pursue decision")


def test_fixture_valid_investigate_first():
    """Fixture I: Valid investigate_first decision should pass validation."""
    fixture_path = os.path.join(FIXTURES_DIR, "fixture-valid-investigate-first.md")
    result = run_validator(fixture_path)

    assert result["valid"] is True, f"Fixture I should pass validation, got errors: {result.get('errors')}"
    assert len(result["errors"]) == 0
    print("[PASS] Fixture I (valid-investigate-first): Validator correctly passes valid investigate_first decision")


def test_fixture_invalid_missing_evidence():
    """Fixture J: Invalid (missing evidence/success measures) should fail validation."""
    fixture_path = os.path.join(FIXTURES_DIR, "fixture-invalid-missing-evidence.md")
    result = run_validator(fixture_path)

    # Should fail because it's missing reasoning, analysis, and summary depth
    assert result["valid"] is False, "Fixture J should fail validation"
    assert len(result["errors"]) > 0, "Should have validation errors for missing evidence"
    # Validator should catch missing success_measures for pursue decision
    error_ids = [e.get("error_id") for e in result["errors"]]
    # At least one error should be related to missing content
    assert any("missing" in str(e).lower() for e in error_ids), f"Should report missing field, got: {error_ids}"
    print("[PASS] Fixture J (invalid-missing-evidence): Validator correctly rejects incomplete artifact")


def test_fixture_invalid_inconsistent_scope():
    """Fixture K: Invalid (pursue_narrowed without excluded_scope) should fail validation."""
    fixture_path = os.path.join(FIXTURES_DIR, "fixture-invalid-inconsistent-scope.md")
    result = run_validator(fixture_path)

    # Should fail because pursue_narrowed requires excluded_scope
    assert result["valid"] is False, "Fixture K should fail validation"
    assert len(result["errors"]) > 0, "Should have validation errors for incomplete pursue_narrowed"
    # Should specifically catch missing excluded_scope
    error_messages = " ".join(str(e.get("message", "")) for e in result["errors"])
    assert "excluded_scope" in error_messages.lower(), \
        f"Should report missing excluded_scope for pursue_narrowed, got: {result['errors']}"
    print("[PASS] Fixture K (invalid-inconsistent-scope): Validator correctly rejects pursue_narrowed without excluded_scope")


def test_fixture_authority_fragmentation_scenario():
    """Fixture L: Valid reject decision with proper reasoning should pass validation."""
    fixture_path = os.path.join(FIXTURES_DIR, "fixture-authority-fragmentation-scenario.md")
    result = run_validator(fixture_path)

    assert result["valid"] is True, f"Fixture L should pass validation, got errors: {result.get('errors')}"
    assert len(result["errors"]) == 0
    print("[PASS] Fixture L (authority-fragmentation-scenario): Validator correctly passes valid reject decision")


def test_fixture_valid_defer():
    """Fixture M: Valid defer decision with reversal_conditions should pass validation."""
    fixture_path = os.path.join(FIXTURES_DIR, "fixture-valid-defer.md")
    result = run_validator(fixture_path)

    assert result["valid"] is True, f"Fixture M should pass validation, got errors: {result.get('errors')}"
    assert len(result["errors"]) == 0
    print("[PASS] Fixture M (valid-defer): Validator correctly passes valid defer decision with reversal_conditions")


def test_validator_dispatches_through_validate_and_report():
    """Prove File O dispatcher correctly routes to File D."""
    fixture_path = os.path.join(FIXTURES_DIR, "fixture-valid-pursue.md")
    result = subprocess.run(
        [sys.executable, os.path.join(SCRIPTS_DIR, "validate-and-report.py"),
         fixture_path],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT
    )
    try:
        dispatch_result = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise AssertionError(f"Dispatcher should output valid JSON, got: {result.stdout[:200]}, error: {e}")

    assert dispatch_result["artifact_id"] == "architectural_review_recommendation"
    assert dispatch_result["validator"] == "validate-architectural-review-recommendation.py", \
        f"Dispatcher should route to File D, got: {dispatch_result['validator']}"
    assert dispatch_result["valid"] is True
    print("[PASS] Dispatcher (File O) correctly routes to File D validator")


if __name__ == "__main__":
    print("Running File M: Validator test suite against approved fixtures (H-L)")
    print()

    tests = [
        ("Fixture H: valid-pursue", test_fixture_valid_pursue),
        ("Fixture I: valid-investigate-first", test_fixture_valid_investigate_first),
        ("Fixture J: invalid-missing-evidence", test_fixture_invalid_missing_evidence),
        ("Fixture K: invalid-inconsistent-scope", test_fixture_invalid_inconsistent_scope),
        ("Fixture L: authority-fragmentation-scenario", test_fixture_authority_fragmentation_scenario),
        ("Fixture M: valid-defer", test_fixture_valid_defer),
        ("File O dispatcher routing", test_validator_dispatches_through_validate_and_report),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {name}: {e}")
            failed += 1

    print()
    print(f"Results: {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
