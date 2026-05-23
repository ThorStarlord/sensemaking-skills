"""Path resolution and management for Sensemaking Skills."""

from pathlib import Path
from typing import Optional
from .config import SkillsConfig


class PathResolver:
    """Resolves and manages paths for Sensemaking Skills operations."""

    def __init__(self, config: SkillsConfig):
        """Initialize PathResolver with configuration.

        Args:
            config: SkillsConfig instance
        """
        self.config = config
        self.project_root = Path(config.project_root).resolve()

    def artifacts_dir(self) -> Path:
        """Get artifacts directory path.

        Returns:
            Path to artifacts directory
        """
        return (self.project_root / self.config.artifacts_dir).resolve()

    def context_file(self) -> Path:
        """Get context file path.

        Returns:
            Path to CONTEXT.md file
        """
        return (self.project_root / self.config.context_file).resolve()

    def skills_dir(self) -> Path:
        """Get skills directory path.

        Returns:
            Path to skills directory
        """
        return (self.project_root / self.config.skills_dir).resolve()

    def workflows_dir(self) -> Path:
        """Get workflows directory path.

        Returns:
            Path to workflows directory
        """
        return (self.project_root / self.config.workflows_dir).resolve()

    def adr_dir(self) -> Path:
        """Get ADR (Architecture Decision Record) directory path.

        Returns:
            Path to ADR directory
        """
        return (self.project_root / self.config.adr_dir).resolve()

    def artifact_path(self, artifact_id: str) -> Path:
        """Get path to a specific artifact.

        Args:
            artifact_id: Artifact identifier

        Returns:
            Path to artifact file
        """
        return (self.artifacts_dir() / f"{artifact_id}.md").resolve()

    def session_dir(self, session_id: str) -> Path:
        """Get session directory for run artifacts.

        Args:
            session_id: Unique session identifier

        Returns:
            Path to session directory (created if doesn't exist)
        """
        session_dir = self.project_root / "artifacts" / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_dir

    def skill_dir(self, skill_name: str) -> Path:
        """Get path to a specific skill directory.

        Args:
            skill_name: Name of the skill

        Returns:
            Path to skill directory
        """
        return (self.skills_dir() / skill_name).resolve()

    def workflow_file(self, workflow_name: str) -> Path:
        """Get path to a specific workflow file.

        Args:
            workflow_name: Name of the workflow

        Returns:
            Path to workflow file
        """
        return (self.workflows_dir() / f"{workflow_name}.yaml").resolve()

    def adr_file(self, adr_number: int) -> Path:
        """Get path to a specific ADR file.

        Args:
            adr_number: ADR number

        Returns:
            Path to ADR file
        """
        return (self.adr_dir() / f"{adr_number:04d}-*.md").resolve()

    def ensure_directories(self):
        """Create all required directories if they don't exist."""
        for directory in [
            self.project_root,
            self.artifacts_dir(),
            self.skills_dir(),
            self.workflows_dir(),
            self.adr_dir(),
        ]:
            directory.mkdir(parents=True, exist_ok=True)

    def is_valid_project(self) -> bool:
        """Check if project structure is valid.

        Returns:
            True if CONTEXT.md exists, False otherwise
        """
        return self.context_file().exists()
