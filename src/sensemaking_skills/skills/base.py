"""Base skill class for all Sensemaking Skills.

Provides common infrastructure for skill execution including artifact management,
logging, and configuration access.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime
from ..config import SkillsConfig
from ..paths import PathResolver


class BaseSkill(ABC):
    """Abstract base class for all Sensemaking Skills.

    Provides common infrastructure for skill execution:
    - Configuration and path management
    - Artifact reading and writing
    - Logging
    - Target repository awareness
    """

    def __init__(self, config: SkillsConfig):
        """Initialize skill with configuration.

        Args:
            config: SkillsConfig instance containing paths and settings
        """
        self.config = config
        self.path_resolver = PathResolver(config)
        self.target_repo = config.project_root
        self.artifacts_dir = self.path_resolver.artifacts_dir()
        self._skill_name = self.__class__.__name__

    def __repr__(self) -> str:
        """Return string representation of skill."""
        return f"{self._skill_name}(target_repo={self.target_repo})"

    @abstractmethod
    def run(self, **kwargs) -> Dict[str, Any]:
        """Execute the skill.

        Subclasses must implement this method to perform skill-specific work.

        Args:
            **kwargs: Skill-specific arguments

        Returns:
            Dictionary containing skill execution results, including:
            - artifact_id: ID of any artifact created/modified
            - success: Boolean indicating execution success
            - message: Human-readable result message
            - Any skill-specific results
        """
        pass

    def write_artifact(self, artifact_id: str, content: str) -> Path:
        """Write artifact to target repository.

        Args:
            artifact_id: Identifier for the artifact (without .md extension)
            content: Content to write to artifact

        Returns:
            Path where artifact was written

        Raises:
            IOError: If artifact cannot be written
        """
        artifact_path = self.path_resolver.artifact_path(artifact_id)
        artifact_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(artifact_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.log(f"Wrote artifact: {artifact_id} -> {artifact_path}")
            return artifact_path
        except IOError as e:
            raise IOError(f"Failed to write artifact {artifact_id}: {e}")

    def read_artifact(self, artifact_id: str) -> Optional[str]:
        """Read artifact from target repository if it exists.

        Args:
            artifact_id: Identifier for the artifact (without .md extension)

        Returns:
            Artifact content if found, None otherwise
        """
        artifact_path = self.path_resolver.artifact_path(artifact_id)

        if not artifact_path.exists():
            self.log(f"Artifact not found: {artifact_id}")
            return None

        try:
            with open(artifact_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.log(f"Read artifact: {artifact_id} ({len(content)} bytes)")
            return content
        except IOError as e:
            self.log(f"Error reading artifact {artifact_id}: {e}")
            return None

    def artifact_exists(self, artifact_id: str) -> bool:
        """Check if an artifact exists.

        Args:
            artifact_id: Identifier for the artifact

        Returns:
            True if artifact exists, False otherwise
        """
        artifact_path = self.path_resolver.artifact_path(artifact_id)
        return artifact_path.exists()

    def log(self, message: str, level: str = "INFO") -> None:
        """Log a message during skill execution.

        Args:
            message: Message to log
            level: Log level (INFO, WARNING, ERROR)
        """
        timestamp = datetime.now().isoformat(timespec="seconds")
        prefix = f"[{timestamp}] [{level}] [{self._skill_name}]"
        print(f"{prefix} {message}")

    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)

    def get_context_file_path(self) -> Path:
        """Get path to CONTEXT.md file in target repository.

        Returns:
            Path to CONTEXT.md
        """
        return self.path_resolver.context_file()

    def read_context_file(self) -> Optional[str]:
        """Read CONTEXT.md file from target repository.

        Returns:
            Content of CONTEXT.md if exists, None otherwise
        """
        context_path = self.get_context_file_path()
        if not context_path.exists():
            self.log("CONTEXT.md not found in target repository")
            return None

        try:
            with open(context_path, "r", encoding="utf-8") as f:
                return f.read()
        except IOError as e:
            self.log(f"Error reading CONTEXT.md: {e}", level="ERROR")
            return None

    def list_artifacts(self) -> list[str]:
        """List all artifacts in the artifacts directory.

        Returns:
            List of artifact IDs (without .md extension)
        """
        artifacts = []
        if self.artifacts_dir.exists():
            for artifact_file in self.artifacts_dir.glob("*.md"):
                artifacts.append(artifact_file.stem)
        return sorted(artifacts)
