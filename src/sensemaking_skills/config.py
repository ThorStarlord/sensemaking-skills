"""Configuration management for Sensemaking Skills."""

import os
import yaml
from typing import Optional, Dict, Any
from pathlib import Path


class SkillsConfig:
    """Configuration data structure for Sensemaking Skills."""

    def __init__(self, config_dict: Dict[str, Any]):
        """Initialize configuration from dictionary.

        Args:
            config_dict: Configuration dictionary loaded from YAML
        """
        self._config = config_dict
        self.project_root = Path(config_dict.get("project_root", "."))
        self.artifacts_dir = Path(config_dict.get("artifacts_dir", "artifacts"))
        self.context_file = config_dict.get("context_file", "CONTEXT.md")
        self.skills_dir = Path(config_dict.get("skills_dir", "skills"))
        self.workflows_dir = Path(config_dict.get("workflows_dir", "workflows"))
        self.adr_dir = Path(config_dict.get("adr_dir", "docs/adr"))

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary.

        Returns:
            Configuration dictionary
        """
        return self._config.copy()


class ConfigManager:
    """Manages configuration loading and resolution."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize ConfigManager.

        Args:
            config_path: Path to configuration YAML file. If not provided,
                        looks for sensemaking-config.yaml in current directory
                        or project root.
        """
        self.config_path = self._resolve_config_path(config_path)
        self.config = self._load_config()

    def _resolve_config_path(self, config_path: Optional[str]) -> Path:
        """Resolve configuration file path.

        Args:
            config_path: Explicit path or None to search for config

        Returns:
            Path to configuration file
        """
        if config_path:
            return Path(config_path)

        # Search in current directory and parent directories
        candidates = [
            Path.cwd() / "sensemaking-config.yaml",
            Path.cwd() / ".claude" / "sensemaking-config.yaml",
            Path.home() / ".claude" / "sensemaking-config.yaml",
        ]

        for candidate in candidates:
            if candidate.exists():
                return candidate

        # Return default path (may not exist yet)
        return Path.cwd() / "sensemaking-config.yaml"

    def _load_config(self) -> SkillsConfig:
        """Load configuration from file.

        Returns:
            SkillsConfig instance

        Raises:
            FileNotFoundError: If config file not found
            yaml.YAMLError: If config file is invalid YAML
        """
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}\n"
                f"Create one using the template at templates/sensemaking-config.yaml.template"
            )

        try:
            with open(self.config_path, "r") as f:
                config_dict = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise yaml.YAMLError(
                f"Failed to parse configuration file {self.config_path}: {e}"
            )

        # Set project root if not specified
        if "project_root" not in config_dict:
            config_dict["project_root"] = str(self.config_path.parent)

        return SkillsConfig(config_dict)

    def create_default_config(self, project_root: str = ".") -> SkillsConfig:
        """Create a default configuration.

        Args:
            project_root: Root directory of the target project

        Returns:
            SkillsConfig instance with default values
        """
        default_config = {
            "project_root": str(project_root),
            "artifacts_dir": "artifacts",
            "context_file": "CONTEXT.md",
            "skills_dir": "skills",
            "workflows_dir": "workflows",
            "adr_dir": "docs/adr",
        }
        return SkillsConfig(default_config)

    def save_config(self, config: SkillsConfig, output_path: Optional[str] = None):
        """Save configuration to file.

        Args:
            config: SkillsConfig instance to save
            output_path: Path to save configuration. Defaults to self.config_path
        """
        output_path = Path(output_path or self.config_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            yaml.dump(config.to_dict(), f, default_flow_style=False)
