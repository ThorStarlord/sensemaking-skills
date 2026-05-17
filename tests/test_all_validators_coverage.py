"""Tests for Level 3 Validator coverage verification in Phase 5.

This test module verifies that all 5 Level 3 validators for the Skill Invocation
Framework are present and executable:
1. validate-plan.py - Validates implementation plans
2. validate-prompt-handoff.py - Validates prompt handoff artifacts
3. validate-brief.py - Validates UI/feature briefs
4. validate-skill-improvement-plan.py - Validates skill improvement proposals
5. validate-usage-research-report.py - Validates usage research reports
"""

import os
from pathlib import Path


class TestValidatorCoverage:
    """Test coverage of all required Level 3 validators."""

    EXPECTED_VALIDATORS = [
        "validate-plan.py",
        "validate-prompt-handoff.py",
        "validate-brief.py",
        "validate-skill-improvement-plan.py",
        "validate-usage-research-report.py",
    ]

    @property
    def scripts_dir(self) -> Path:
        """Get the scripts directory path relative to repo root."""
        # From this test file's location, go up to repo root, then to scripts
        test_file = Path(__file__)
        repo_root = test_file.parent.parent
        return repo_root / "scripts"

    def test_all_level3_validators_exist(self):
        """Verify all 5 expected Level 3 validators exist in scripts/ directory."""
        for validator in self.EXPECTED_VALIDATORS:
            validator_path = self.scripts_dir / validator
            assert validator_path.exists(), (
                f"Validator {validator} not found at {validator_path}"
            )

    def test_validators_are_executable(self):
        """Verify all Level 3 validators are executable Python files."""
        for validator in self.EXPECTED_VALIDATORS:
            validator_path = self.scripts_dir / validator
            assert validator_path.is_file(), (
                f"{validator} is not a file at {validator_path}"
            )
            # Check that the file has a .py extension
            assert validator_path.suffix == ".py", (
                f"{validator} should be a .py file, got {validator_path.suffix}"
            )
            # Check that the file is readable
            assert os.access(str(validator_path), os.R_OK), (
                f"{validator} at {validator_path} is not readable"
            )
