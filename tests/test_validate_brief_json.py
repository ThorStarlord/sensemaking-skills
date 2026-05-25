"""Tests for validate-brief.py JSON output functionality."""

import json
import os
import sys
import tempfile
import unittest
import importlib.util

# Add scripts directory to path
scripts_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, scripts_dir)

# Import validate_brief module
spec = importlib.util.spec_from_file_location("validate_brief", os.path.join(scripts_dir, "validate_brief.py"))
validate_brief_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_brief_module)

validate_brief = validate_brief_module.validate_brief
validation_result_to_json = validate_brief_module.validation_result_to_json


class TestValidateBriefJSON(unittest.TestCase):
    """Test JSON validation output for repository sensemaking brief."""

    def setUp(self):
        """Set up test fixtures."""
        self.repo_root = os.path.dirname(os.path.dirname(__file__))
        self.fixtures_dir = os.path.join(self.repo_root, "tests", "fixtures")

    def test_valid_brief_produces_no_errors(self):
        """Valid brief should have empty errors array."""
        brief_path = os.path.join(self.fixtures_dir, "brief-valid.md")
        errors = validate_brief(brief_path, self.repo_root)

        self.assertEqual(len(errors), 0, "Valid brief should have no errors")

    def test_valid_brief_json_format(self):
        """Valid brief should produce valid JSON with correct structure."""
        brief_path = os.path.join(self.fixtures_dir, "brief-valid.md")
        errors = validate_brief(brief_path, self.repo_root)
        json_output = validation_result_to_json(brief_path, errors)

        # Should be parseable JSON
        result = json.loads(json_output)

        # Check structure
        self.assertIn("valid", result)
        self.assertIn("artifact_id", result)
        self.assertIn("artifact_path", result)
        self.assertIn("validator", result)
        self.assertIn("errors", result)
        self.assertIn("validation_timestamp", result)

        # Valid should be True
        self.assertTrue(result["valid"])

        # Errors should be empty array
        self.assertEqual(result["errors"], [])

        # Check artifact_id
        self.assertEqual(result["artifact_id"], "repository_sensemaking_brief")

        # Check validator name
        self.assertEqual(result["validator"], "validate-brief.py")

    def test_missing_required_fields(self):
        """Brief missing required fields should produce multiple errors."""
        brief_path = os.path.join(self.fixtures_dir, "brief-invalid-missing-fields.md")
        errors = validate_brief(brief_path, self.repo_root)

        # Should have errors for missing fields
        self.assertGreater(len(errors), 0, "Invalid brief should have errors")

        # Check error types are correct
        error_types = [e.get("error_type") for e in errors]
        self.assertTrue(all(et == "missing_field" for et in error_types))

        # Check fields mentioned
        error_fields = [e.get("field") for e in errors]
        self.assertIn("primary_fog_type", error_fields)
        self.assertIn("evidence", error_fields)
        self.assertIn("recommended_workflow_id", error_fields)

    def test_missing_fields_json_has_suggested_fixes(self):
        """Each error should have suggested_fixes array."""
        brief_path = os.path.join(self.fixtures_dir, "brief-invalid-missing-fields.md")
        errors = validate_brief(brief_path, self.repo_root)
        json_output = validation_result_to_json(brief_path, errors)

        result = json.loads(json_output)

        # Each error should have suggested_fixes
        for error in result["errors"]:
            self.assertIn("suggested_fixes", error)
            self.assertIsInstance(error["suggested_fixes"], list)
            self.assertGreater(len(error["suggested_fixes"]), 0)

    def test_wrong_value_types(self):
        """Brief with wrong data types should produce type_error."""
        brief_path = os.path.join(self.fixtures_dir, "brief-invalid-wrong-values.md")
        errors = validate_brief(brief_path, self.repo_root)

        # Should have type_error for evidence (string instead of array)
        type_errors = [e for e in errors if e.get("error_type") == "type_error"]
        self.assertGreater(len(type_errors), 0)

        # Should have unknown_value for primary_fog_type and workflow_id
        unknown_errors = [e for e in errors if e.get("error_type") == "unknown_value"]
        self.assertGreater(len(unknown_errors), 0)

    def test_empty_evidence_produces_logic_error(self):
        """Brief with empty evidence array should produce logic_error."""
        brief_path = os.path.join(self.fixtures_dir, "brief-invalid-empty-evidence.md")
        errors = validate_brief(brief_path, self.repo_root)

        # Should have logic_error
        logic_errors = [e for e in errors if e.get("error_type") == "logic_error"]
        self.assertGreater(len(logic_errors), 0)

        # Check the error is about evidence
        evidence_errors = [e for e in logic_errors if e.get("field") == "evidence"]
        self.assertGreater(len(evidence_errors), 0)

    def test_json_includes_all_error_metadata(self):
        """Each error should include all required metadata fields."""
        brief_path = os.path.join(self.fixtures_dir, "brief-invalid-missing-fields.md")
        errors = validate_brief(brief_path, self.repo_root)
        json_output = validation_result_to_json(brief_path, errors)

        result = json.loads(json_output)

        # Check each error has required fields
        for error in result["errors"]:
            self.assertIn("error_type", error)
            self.assertIn("field", error)
            self.assertIn("current_value", error)
            self.assertIn("message", error)
            self.assertIn("suggested_fixes", error)
            self.assertIn("reference", error)

    def test_json_timestamp_is_iso8601_with_z(self):
        """Validation timestamp should be ISO 8601 with Z suffix."""
        brief_path = os.path.join(self.fixtures_dir, "brief-valid.md")
        errors = validate_brief(brief_path, self.repo_root)
        json_output = validation_result_to_json(brief_path, errors)

        result = json.loads(json_output)
        timestamp = result["validation_timestamp"]

        # Should end with Z
        self.assertTrue(timestamp.endswith("Z"))

        # Should be valid ISO 8601 format (simplified check)
        self.assertIn("T", timestamp)

    def test_json_contains_absolute_path(self):
        """artifact_path in JSON should be absolute."""
        brief_path = "tests/fixtures/brief-valid.md"
        errors = validate_brief(brief_path, self.repo_root)
        json_output = validation_result_to_json(brief_path, errors)

        result = json.loads(json_output)
        artifact_path = result["artifact_path"]

        # Should be absolute path
        self.assertTrue(os.path.isabs(artifact_path))

    def test_multiple_errors_returned_as_array(self):
        """Multiple validation errors should be in a single errors array."""
        brief_path = os.path.join(self.fixtures_dir, "brief-invalid-wrong-values.md")
        errors = validate_brief(brief_path, self.repo_root)
        json_output = validation_result_to_json(brief_path, errors)

        result = json.loads(json_output)

        # Should have errors array with multiple items
        self.assertGreater(len(result["errors"]), 1)

        # All should be in single request/response cycle
        self.assertEqual(result["artifact_id"], "repository_sensemaking_brief")
        self.assertFalse(result["valid"])

    def test_error_messages_are_human_readable(self):
        """Error messages should be clear and actionable."""
        brief_path = os.path.join(self.fixtures_dir, "brief-invalid-missing-fields.md")
        errors = validate_brief(brief_path, self.repo_root)

        # Check messages are not empty and descriptive
        for error in errors:
            message = error.get("message", "")
            self.assertGreater(len(message), 10, "Message should be descriptive")
            self.assertIn(error.get("field"), message, "Message should mention the field")

    def test_references_point_to_real_docs(self):
        """Each error should reference documentation."""
        brief_path = os.path.join(self.fixtures_dir, "brief-invalid-missing-fields.md")
        errors = validate_brief(brief_path, self.repo_root)

        # All errors should have references
        for error in errors:
            self.assertIn("reference", error)
            reference = error.get("reference")
            self.assertGreater(len(reference), 0, "Error should have a reference")
            # References should be file paths or ADR references
            self.assertTrue(
                reference.startswith("skills/") or
                reference.startswith("docs/") or
                reference.startswith("CONTEXT.md"),
                f"Reference should be a valid path: {reference}"
            )

    def test_backward_compatibility_prose_output(self):
        """Legacy prose output should still work without --json flag."""
        # This is tested via CLI integration tests
        # Here we just verify that validate_brief returns errors suitable for prose output
        brief_path = os.path.join(self.fixtures_dir, "brief-invalid-missing-fields.md")
        errors = validate_brief(brief_path, self.repo_root)

        # Should be able to construct prose output from errors
        for error in errors:
            error_type = error.get("error_type")
            field = error.get("field")
            message = error.get("message")

            # Prose would look like: "ERROR [error_type] field: message"
            prose = f"ERROR [{error_type}] {field}: {message}"
            self.assertGreater(len(prose), 20)


if __name__ == "__main__":
    unittest.main()
