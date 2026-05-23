"""Sensemaking Skills - Artifact-driven diagnostic and orchestration for any repository."""

__version__ = "1.0.0"
__author__ = "Dimmi Andreus"

from .config import ConfigManager
from .runner import SkillsOrchestrator

__all__ = ["ConfigManager", "SkillsOrchestrator"]
