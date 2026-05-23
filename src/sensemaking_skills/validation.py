"""Target-repo aware validation engine for Sensemaking Skills."""

import yaml
from typing import Optional, Dict, List, Any
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ValidationError:
    """Represents a validation error."""
    field_name: str
    value: Any
    error_message: str
    severity: str = "error"  # error, warning, info


class CanonicalVocabulary:
    """Manages canonical vocabulary and enum values for validation.

    Loads package defaults from src/sensemaking_skills/defaults/canonical-vocabulary.yaml
    and allows user overrides via custom vocabulary files in target repos.
    """

    def __init__(self, target_repo: Path, user_vocab: Optional[Dict] = None):
        """Initialize vocabulary with defaults and optional user overrides.

        Args:
            target_repo: Path to the target repository
            user_vocab: Optional user-provided vocabulary dictionary to override defaults
        """
        self.target_repo = Path(target_repo)
        self._vocabulary = {}

        # Load package defaults
        self._load_package_defaults()

        # Apply user overrides if provided
        if user_vocab:
            self._vocabulary.update(user_vocab)

    def _load_package_defaults(self):
        """Load canonical vocabulary defaults from package."""
        defaults_path = Path(__file__).parent / "defaults" / "canonical-vocabulary.yaml"

        if not defaults_path.exists():
            raise FileNotFoundError(
                f"Package defaults not found: {defaults_path}"
            )

        try:
            with open(defaults_path, "r") as f:
                self._vocabulary = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse canonical vocabulary: {e}")

    def load_target_repo_vocabulary(self, vocab_path: str = "canonical-vocabulary.yaml"):
        """Load target repository's custom vocabulary.

        Args:
            vocab_path: Path to vocabulary file in target repo (relative or absolute)

        Raises:
            FileNotFoundError: If vocabulary file not found
            yaml.YAMLError: If vocabulary file is invalid YAML
        """
        if Path(vocab_path).is_absolute():
            custom_vocab_path = Path(vocab_path)
        else:
            custom_vocab_path = self.target_repo / vocab_path

        if custom_vocab_path.exists():
            try:
                with open(custom_vocab_path, "r") as f:
                    custom_vocab = yaml.safe_load(f) or {}
                    self._vocabulary.update(custom_vocab)
            except yaml.YAMLError as e:
                raise ValueError(
                    f"Failed to parse target repo vocabulary {custom_vocab_path}: {e}"
                )

    def get_enum_values(self, field_name: str) -> Optional[List[str]]:
        """Get valid enum values for a field.

        Args:
            field_name: Field name to look up enum values for

        Returns:
            List of valid enum values or None if field not found or is not an enum
        """
        # Check routing_fields section
        routing_fields = self._vocabulary.get("routing_fields", [])
        for field in routing_fields:
            if field.get("field") == field_name:
                field_type = field.get("type", "")
                if field_type == "enum" or field_type.startswith("list(enum"):
                    return field.get("values", [])

        return None

    def get_field_definition(self, field_name: str) -> Optional[Dict]:
        """Get complete field definition from routing_fields.

        Args:
            field_name: Field name to look up

        Returns:
            Field definition dictionary or None if not found
        """
        routing_fields = self._vocabulary.get("routing_fields", [])
        for field in routing_fields:
            if field.get("field") == field_name:
                return field

        return None

    def validate_field(self, field_name: str, value: Any) -> Optional[ValidationError]:
        """Validate a single field against vocabulary rules.

        Args:
            field_name: Field name to validate
            value: Field value to validate

        Returns:
            ValidationError if validation fails, None if valid
        """
        field_def = self.get_field_definition(field_name)

        if not field_def:
            return ValidationError(
                field_name=field_name,
                value=value,
                error_message=f"Field '{field_name}' not found in vocabulary",
                severity="warning"
            )

        # Check if field is required
        is_required = field_def.get("required", False)
        if is_required and value is None:
            return ValidationError(
                field_name=field_name,
                value=value,
                error_message=f"Required field '{field_name}' is missing",
                severity="error"
            )

        # If value is None and not required, it's valid
        if value is None:
            return None

        # Validate enum values
        field_type = field_def.get("type", "")
        if field_type == "enum":
            valid_values = field_def.get("values", [])
            if value not in valid_values:
                return ValidationError(
                    field_name=field_name,
                    value=value,
                    error_message=f"Invalid value '{value}' for enum field '{field_name}'. "
                                 f"Valid values are: {', '.join(valid_values)}",
                    severity="error"
                )

        elif field_type.startswith("list(enum"):
            # Validate list of enum values
            if isinstance(value, list):
                valid_values = field_def.get("values", [])
                for item in value:
                    if item not in valid_values:
                        return ValidationError(
                            field_name=field_name,
                            value=value,
                            error_message=f"Invalid value '{item}' in list for field '{field_name}'. "
                                         f"Valid values are: {', '.join(valid_values)}",
                            severity="error"
                        )

        return None

    def get_vocabulary(self) -> Dict:
        """Get entire vocabulary dictionary.

        Returns:
            Complete vocabulary dictionary
        """
        return self._vocabulary.copy()


class ArtifactValidator:
    """Validates artifacts against contracts and vocabulary."""

    def __init__(self, vocabulary: CanonicalVocabulary):
        """Initialize validator with vocabulary.

        Args:
            vocabulary: CanonicalVocabulary instance for enum validation
        """
        self.vocabulary = vocabulary

    def validate_artifact(
        self, artifact_id: str, artifact_data: Dict
    ) -> List[ValidationError]:
        """Validate artifact against contract and vocabulary.

        Args:
            artifact_id: Artifact ID (should match artifact_ids in vocabulary)
            artifact_data: Artifact data dictionary to validate

        Returns:
            List of ValidationError objects (empty if valid)
        """
        errors = []

        # Validate artifact_id exists in vocabulary
        vocab = self.vocabulary.get_vocabulary()
        artifact_ids = vocab.get("artifact_ids", [])
        artifact_def = None
        for art in artifact_ids:
            if art.get("id") == artifact_id:
                artifact_def = art
                break

        if not artifact_def:
            errors.append(ValidationError(
                field_name="artifact_id",
                value=artifact_id,
                error_message=f"Artifact ID '{artifact_id}' not found in vocabulary",
                severity="warning"
            ))
            return errors

        # Validate routing fields if present in artifact data
        routing_fields = vocab.get("routing_fields", [])
        for field_def in routing_fields:
            field_name = field_def.get("field")
            if field_name in artifact_data:
                field_error = self.vocabulary.validate_field(
                    field_name, artifact_data[field_name]
                )
                if field_error:
                    errors.append(field_error)

        return errors

    def validate_gate(self, gate_id: str) -> Optional[ValidationError]:
        """Validate that a gate_id exists and is valid.

        Args:
            gate_id: Gate ID to validate

        Returns:
            ValidationError if invalid, None if valid
        """
        vocab = self.vocabulary.get_vocabulary()
        gates = vocab.get("gates", [])

        for gate in gates:
            if gate.get("gate_id") == gate_id:
                return None

        return ValidationError(
            field_name="gate_id",
            value=gate_id,
            error_message=f"Gate ID '{gate_id}' not found in vocabulary",
            severity="error"
        )

    def validate_workflow_id(self, workflow_id: str) -> Optional[ValidationError]:
        """Validate that a workflow_id exists in vocabulary.

        Args:
            workflow_id: Workflow ID to validate

        Returns:
            ValidationError if invalid, None if valid
        """
        vocab = self.vocabulary.get_vocabulary()
        workflows = vocab.get("workflow_ids", [])

        for workflow in workflows:
            if workflow.get("id") == workflow_id:
                return None

        return ValidationError(
            field_name="workflow_id",
            value=workflow_id,
            error_message=f"Workflow ID '{workflow_id}' not found in vocabulary",
            severity="error"
        )
