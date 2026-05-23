"""Tests for fog type normalization in validators."""

import os
import sys
import tempfile
import importlib.util
from pathlib import Path

import unittest

# Add scripts directory so we can import validators
scripts_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, scripts_dir)

# Load the validator module (it has a hyphen in the name)
validator_path = os.path.join(scripts_dir, "validate-fog-type-normalization.py")
spec = importlib.util.spec_from_file_location("validate_fog_type_normalization", validator_path)
validator_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator_module)
validate_fog_type_normalization = validator_module.validate_fog_type_normalization


class TestFogTypeNormalization(unittest.TestCase):
    """Test fog type validation and normalization."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.repo_root = Path(__file__).parent.parent

    def test_normalizes_canonical_forms(self):
        """Canonical fog types should pass validation."""
        artifact_content = """
# Test Artifact

## Machine Readable

```yaml
artifact_id: test
primary_fog_type: product_fog
user_implied_fog_type: ui_fog
secondary_fog_types: [docs_fog, architecture_fog]
```
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(artifact_content)
            fname = f.name

        try:
            errors = validate_fog_type_normalization(fname, str(self.repo_root))
            self.assertFalse(
                errors,
                f"Canonical fog types should pass validation, got errors: {errors}"
            )
        finally:
            os.unlink(fname)

    def test_normalizes_alias_forms(self):
        """Fog type aliases (product, ui, docs, etc.) should normalize to canonical."""
        artifact_content = """
# Test Artifact

## Machine Readable

```yaml
artifact_id: test
primary_fog_type: product
user_implied_fog_type: ui
secondary_fog_types: [docs, architecture]
```
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(artifact_content)
            fname = f.name

        try:
            errors = validate_fog_type_normalization(fname, str(self.repo_root))
            self.assertFalse(
                errors,
                f"Alias fog types should normalize without errors, got: {errors}"
            )
        finally:
            os.unlink(fname)

    def test_rejects_unknown_fog_types(self):
        """Unknown fog types should fail validation."""
        artifact_content = """
# Test Artifact

## Machine Readable

```yaml
artifact_id: test
primary_fog_type: unknown_fog
user_implied_fog_type: ui_fog
```
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(artifact_content)
            fname = f.name

        try:
            errors = validate_fog_type_normalization(fname, str(self.repo_root))
            self.assertTrue(
                any("INVALID_FOG_TYPE" in err for err in errors),
                f"Unknown fog type should fail validation, got: {errors}"
            )
        finally:
            os.unlink(fname)

    def test_handles_missing_machine_section(self):
        """Artifacts without machine-readable sections should pass."""
        artifact_content = """
# Test Artifact

This is a human-readable section with no machine-readable content.
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(artifact_content)
            fname = f.name

        try:
            errors = validate_fog_type_normalization(fname, str(self.repo_root))
            self.assertFalse(
                errors,
                f"Missing machine section should be handled gracefully, got: {errors}"
            )
        finally:
            os.unlink(fname)


if __name__ == "__main__":
    unittest.main()
