"""Tests for validation module."""

import pytest
from pathlib import Path
from sensemaking_skills.validation import (
    CanonicalVocabulary,
    ArtifactValidator,
    ValidationError,
)


class TestCanonicalVocabulary:
    """Test CanonicalVocabulary loading and enum validation."""

    def test_load_package_defaults(self):
        """Test that package defaults are loaded successfully."""
        vocab = CanonicalVocabulary(Path("."))

        # Check that vocabulary was loaded
        assert vocab._vocabulary is not None
        assert len(vocab._vocabulary) > 0

        # Check key sections exist
        assert "fog_types" in vocab._vocabulary
        assert "routing_fields" in vocab._vocabulary
        assert "gates" in vocab._vocabulary
        assert "workflow_ids" in vocab._vocabulary

    def test_get_enum_values_routing_field(self):
        """Test getting enum values for a routing field."""
        vocab = CanonicalVocabulary(Path("."))

        # Test primary_fog_type enum
        fog_values = vocab.get_enum_values("primary_fog_type")
        assert fog_values is not None
        assert "product_fog" in fog_values
        assert "ui_fog" in fog_values
        assert "architecture_fog" in fog_values
        assert "docs_fog" in fog_values

    def test_get_enum_values_workflow_id(self):
        """Test getting enum values for workflow_id."""
        vocab = CanonicalVocabulary(Path("."))

        workflow_values = vocab.get_enum_values("recommended_workflow_id")
        assert workflow_values is not None
        assert "fast-path-workflow" in workflow_values
        assert "full-fog-workflow" in workflow_values

    def test_get_enum_values_nonexistent_field(self):
        """Test getting enum values for non-existent field."""
        vocab = CanonicalVocabulary(Path("."))

        result = vocab.get_enum_values("nonexistent_field")
        assert result is None

    def test_get_field_definition(self):
        """Test getting complete field definition."""
        vocab = CanonicalVocabulary(Path("."))

        field_def = vocab.get_field_definition("primary_fog_type")
        assert field_def is not None
        assert field_def["field"] == "primary_fog_type"
        assert field_def["type"] == "enum"
        assert field_def["required"] is True

    def test_validate_field_valid_enum(self):
        """Test validating a valid enum value."""
        vocab = CanonicalVocabulary(Path("."))

        error = vocab.validate_field("primary_fog_type", "product_fog")
        assert error is None

    def test_validate_field_invalid_enum(self):
        """Test validating an invalid enum value."""
        vocab = CanonicalVocabulary(Path("."))

        error = vocab.validate_field("primary_fog_type", "invalid_fog")
        assert error is not None
        assert isinstance(error, ValidationError)
        assert "Invalid value" in error.error_message

    def test_validate_field_required_missing(self):
        """Test validating a required field that is missing."""
        vocab = CanonicalVocabulary(Path("."))

        error = vocab.validate_field("primary_fog_type", None)
        assert error is not None
        assert isinstance(error, ValidationError)
        assert "missing" in error.error_message.lower()

    def test_get_vocabulary_returns_copy(self):
        """Test that get_vocabulary returns a copy."""
        vocab = CanonicalVocabulary(Path("."))

        vocab_dict = vocab.get_vocabulary()
        assert vocab_dict is not None

        # Modifying the copy shouldn't affect original
        original_len = len(vocab_dict)
        vocab_dict["test_key"] = "test_value"

        new_dict = vocab.get_vocabulary()
        assert "test_key" not in new_dict
        assert len(new_dict) == original_len


class TestArtifactValidator:
    """Test ArtifactValidator."""

    def test_validate_artifact_with_valid_data(self):
        """Test validating an artifact with valid data."""
        vocab = CanonicalVocabulary(Path("."))
        validator = ArtifactValidator(vocab)

        artifact_data = {
            "primary_fog_type": "product_fog",
            "recommended_workflow_id": "fast-path-workflow",
            "routing_decision_method": "user_explicit_override",
            "selected_workflow": "Test workflow selection",
        }

        errors = validator.validate_artifact("repository_sensemaking_brief", artifact_data)
        assert len(errors) == 0 or all(e.severity == "warning" for e in errors)

    def test_validate_artifact_with_invalid_field(self):
        """Test validating an artifact with invalid field value."""
        vocab = CanonicalVocabulary(Path("."))
        validator = ArtifactValidator(vocab)

        artifact_data = {
            "primary_fog_type": "invalid_fog",
        }

        errors = validator.validate_artifact("repository_sensemaking_brief", artifact_data)
        error_messages = [e.error_message for e in errors]

        # Should have error for invalid fog type
        assert any("Invalid value" in msg for msg in error_messages)

    def test_validate_artifact_nonexistent_id(self):
        """Test validating an artifact with non-existent ID."""
        vocab = CanonicalVocabulary(Path("."))
        validator = ArtifactValidator(vocab)

        artifact_data = {}
        errors = validator.validate_artifact("nonexistent_artifact_id", artifact_data)

        # Should have warning about artifact ID not found
        assert any("not found" in e.error_message.lower() for e in errors)

    def test_validate_gate_valid(self):
        """Test validating a valid gate."""
        vocab = CanonicalVocabulary(Path("."))
        validator = ArtifactValidator(vocab)

        error = validator.validate_gate("review_problem_frame")
        assert error is None

    def test_validate_gate_invalid(self):
        """Test validating an invalid gate."""
        vocab = CanonicalVocabulary(Path("."))
        validator = ArtifactValidator(vocab)

        error = validator.validate_gate("invalid_gate_id")
        assert error is not None
        assert "not found" in error.error_message.lower()

    def test_validate_workflow_id_valid(self):
        """Test validating a valid workflow ID."""
        vocab = CanonicalVocabulary(Path("."))
        validator = ArtifactValidator(vocab)

        error = validator.validate_workflow_id("fast-path-workflow")
        assert error is None

    def test_validate_workflow_id_invalid(self):
        """Test validating an invalid workflow ID."""
        vocab = CanonicalVocabulary(Path("."))
        validator = ArtifactValidator(vocab)

        error = validator.validate_workflow_id("invalid_workflow_id")
        assert error is not None
        assert "not found" in error.error_message.lower()


class TestValidationError:
    """Test ValidationError dataclass."""

    def test_validation_error_creation(self):
        """Test creating a ValidationError."""
        error = ValidationError(
            field_name="test_field",
            value="invalid_value",
            error_message="Test error message",
        )

        assert error.field_name == "test_field"
        assert error.value == "invalid_value"
        assert error.error_message == "Test error message"
        assert error.severity == "error"

    def test_validation_error_with_custom_severity(self):
        """Test creating a ValidationError with custom severity."""
        error = ValidationError(
            field_name="test_field",
            value="test_value",
            error_message="Test warning",
            severity="warning",
        )

        assert error.severity == "warning"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
