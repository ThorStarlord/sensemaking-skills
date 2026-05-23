"""Repository Sensemaker Skill.

Analyzes target repository structure, content, and organization to produce
a comprehensive repository sensemaking brief.
"""

from pathlib import Path
from typing import Any, Dict, Optional
from .base import BaseSkill


class RepoSensemakerSkill(BaseSkill):
    """Analyzes target repository and produces sensemaking brief.

    This skill examines the target repository structure, identifies key files,
    reads documentation, and generates a comprehensive brief that helps subsequent
    skills understand the project's architecture and organization.
    """

    def run(self, **kwargs) -> Dict[str, Any]:
        """Execute repository analysis.

        Analyzes the target repository structure and produces a repository
        sensemaking brief artifact.

        Args:
            **kwargs: Optional arguments (none required for basic analysis)

        Returns:
            Dictionary containing:
            - artifact_id: "repository_sensemaking_brief"
            - success: True if analysis completed
            - message: Summary of analysis
            - repo_summary: Brief summary of repository
            - key_files_found: List of important files discovered
        """
        self.log("Starting repository analysis...")

        try:
            # Analyze repository structure
            repo_summary = self._analyze_repository_structure()
            key_files = self._identify_key_files()
            context_content = self._read_context_document()

            # Generate brief
            brief_content = self._generate_brief(repo_summary, key_files, context_content)

            # Write artifact
            artifact_id = "repository_sensemaking_brief"
            self.write_artifact(artifact_id, brief_content)

            return {
                "artifact_id": artifact_id,
                "success": True,
                "message": "Repository analysis completed successfully",
                "repo_summary": repo_summary,
                "key_files_found": key_files,
            }

        except Exception as e:
            self.log(f"Repository analysis failed: {e}", level="ERROR")
            return {
                "artifact_id": None,
                "success": False,
                "message": f"Analysis failed: {e}",
                "repo_summary": None,
                "key_files_found": [],
            }

    def _analyze_repository_structure(self) -> Dict[str, Any]:
        """Analyze target repository structure.

        Returns:
            Dictionary containing repository structure analysis
        """
        self.log("Analyzing repository structure...")
        target_repo = Path(self.target_repo)

        # Count files by type
        file_counts = self._count_files_by_type(target_repo)

        # Identify directories
        directories = self._identify_directories(target_repo)

        # Check for common project markers
        project_markers = self._identify_project_markers(target_repo)

        return {
            "root_path": str(target_repo),
            "file_counts": file_counts,
            "directories": directories,
            "project_markers": project_markers,
            "total_files": sum(file_counts.values()),
        }

    def _count_files_by_type(self, directory: Path) -> Dict[str, int]:
        """Count files by extension in directory.

        Args:
            directory: Directory to analyze

        Returns:
            Dictionary mapping extensions to file counts
        """
        counts = {}
        extensions = [
            ".py", ".js", ".ts", ".tsx", ".jsx",
            ".md", ".yaml", ".yml", ".json", ".txt",
            ".sh", ".bash", ".css", ".html",
        ]

        for ext in extensions:
            count = len(list(directory.rglob(f"*{ext}")))
            if count > 0:
                counts[ext] = count

        return counts

    def _identify_directories(self, directory: Path, max_depth: int = 2) -> list[str]:
        """Identify important directories.

        Args:
            directory: Directory to analyze
            max_depth: Maximum depth to traverse

        Returns:
            List of directory names found
        """
        important_dirs = [
            "src", "lib", "tests", "test", "docs", "scripts",
            "workflows", "skills", "config", "artifacts",
            ".github", ".gitlab", "node_modules", "venv",
            "env", "__pycache__", ".git",
        ]

        found_dirs = []
        for important_dir in important_dirs:
            if (directory / important_dir).is_dir():
                found_dirs.append(important_dir)

        return found_dirs

    def _identify_project_markers(self, directory: Path) -> list[str]:
        """Identify markers that indicate project type.

        Args:
            directory: Directory to analyze

        Returns:
            List of project markers found
        """
        markers = []
        marker_files = {
            "package.json": "Node.js project",
            "setup.py": "Python project",
            "requirements.txt": "Python project",
            "Gemfile": "Ruby project",
            "go.mod": "Go project",
            "Cargo.toml": "Rust project",
            "Dockerfile": "Docker container",
            "docker-compose.yml": "Docker Compose",
            "CONTEXT.md": "Sensemaking project",
            "workflows": "Workflow project",
            "skills": "Skills project",
            ".github": "GitHub Actions",
        }

        for marker, description in marker_files.items():
            if (directory / marker).exists():
                markers.append(f"{marker} ({description})")

        return markers

    def _identify_key_files(self) -> list[str]:
        """Identify key files in the repository.

        Returns:
            List of important files discovered
        """
        self.log("Identifying key files...")
        target_repo = Path(self.target_repo)
        key_files = []

        important_files = [
            "README.md", "CONTEXT.md", "setup.py", "package.json",
            "requirements.txt", "Dockerfile", "docker-compose.yml",
            "Makefile", ".gitignore", "LICENSE", "CONTRIBUTING.md",
            "ADR_0001.md", "AGENTS.md", "IMPLEMENTATION_SUMMARY.md",
        ]

        for filename in important_files:
            if (target_repo / filename).exists():
                key_files.append(filename)

        return key_files

    def _read_context_document(self) -> Optional[str]:
        """Read CONTEXT.md if available.

        Returns:
            Content of CONTEXT.md or None if not found
        """
        context_content = self.read_context_file()
        if context_content:
            self.log(f"Found CONTEXT.md ({len(context_content)} bytes)")
        return context_content

    def _generate_brief(
        self,
        repo_summary: Dict[str, Any],
        key_files: list[str],
        context_content: Optional[str],
    ) -> str:
        """Generate the repository sensemaking brief.

        Args:
            repo_summary: Repository structure analysis
            key_files: List of important files
            context_content: Content of CONTEXT.md if available

        Returns:
            Formatted brief content as markdown
        """
        brief = [
            "# Repository Sensemaking Brief",
            "",
            "## Overview",
            f"- **Repository Root**: {repo_summary['root_path']}",
            f"- **Total Files**: {repo_summary['total_files']}",
            "",
        ]

        # File counts
        if repo_summary["file_counts"]:
            brief.extend([
                "## File Distribution",
                "",
            ])
            for ext, count in sorted(repo_summary["file_counts"].items(), key=lambda x: x[1], reverse=True):
                brief.append(f"- {ext}: {count} files")
            brief.append("")

        # Directories
        if repo_summary["directories"]:
            brief.extend([
                "## Key Directories",
                "",
            ])
            for dirname in sorted(repo_summary["directories"]):
                brief.append(f"- `{dirname}/`")
            brief.append("")

        # Project markers
        if repo_summary["project_markers"]:
            brief.extend([
                "## Project Type Indicators",
                "",
            ])
            for marker in repo_summary["project_markers"]:
                brief.append(f"- {marker}")
            brief.append("")

        # Key files
        if key_files:
            brief.extend([
                "## Key Files",
                "",
            ])
            for filename in sorted(key_files):
                brief.append(f"- `{filename}`")
            brief.append("")

        # Context
        if context_content:
            brief.extend([
                "## CONTEXT.md Extract",
                "",
                "```markdown",
            ])
            # Include first 500 chars of context
            excerpt = context_content[:500]
            if len(context_content) > 500:
                excerpt += "\n...(truncated)"
            brief.append(excerpt)
            brief.extend([
                "```",
                "",
            ])

        brief.extend([
            "## Generated At",
            f"- This brief was auto-generated by RepoSensemakerSkill",
            "",
        ])

        return "\n".join(brief)
