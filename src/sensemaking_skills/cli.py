"""Command-line interface for Sensemaking Skills."""

import sys
from pathlib import Path
from typing import Optional

import click

from .config import ConfigManager, SkillsConfig
from .runner import SkillsOrchestrator


@click.group()
def main():
    """Sensemaking Skills - Artifact-driven diagnostic orchestration for any repository.

    Analyze your codebase structure, design patterns, and architecture
    to generate diagnostic artifacts and actionable insights.
    """
    pass


@main.command()
@click.option(
    "--repo",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    required=True,
    help="Path to the target repository to analyze",
)
@click.option(
    "--workflow",
    type=str,
    default="fast-path-workflow",
    help="Workflow to execute (default: fast-path-workflow)",
)
@click.option(
    "--mode",
    type=click.Choice(["guided_execution", "autonomous_execution", "plan_only"]),
    default="guided_execution",
    help="Execution mode (default: guided_execution)",
)
def analyze(repo: Path, workflow: str, mode: str) -> None:
    """Analyze a repository and generate diagnostic artifacts.

    This command runs the specified workflow against your repository
    to analyze its structure, patterns, and architecture.

    Example:
        sensemaking-skills analyze --repo /path/to/repo --workflow fast-path-workflow --mode guided_execution
    """
    try:
        click.echo(f"Loading configuration from {repo}...")

        # Change to repo directory for config resolution
        import os

        original_cwd = os.getcwd()
        os.chdir(repo)

        try:
            # Load configuration
            config_manager = ConfigManager()
            config = config_manager.config

            click.echo(f"Configuration loaded successfully")
            click.echo(f"  Project root: {config.project_root}")
            click.echo(f"  Artifacts dir: {config.artifacts_dir}")
            click.echo(f"  Skills dir: {config.skills_dir}")
            click.echo(f"  Workflows dir: {config.workflows_dir}")

            # Create orchestrator
            orchestrator = SkillsOrchestrator(config=config)
            click.echo(f"\nOrchestrator initialized: {orchestrator}")

            # Show workflow info
            click.echo(f"\nWorkflow: {workflow}")
            click.echo(f"Mode: {mode}")

            click.echo(f"\nStarting analysis...")
            click.echo("This feature is under development in Task 3 (Refactor Workflow Runtime)")

        finally:
            os.chdir(original_cwd)

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        click.echo(
            "Hint: Run 'sensemaking-skills init --repo <repo-path>' to initialize configuration",
            err=True,
        )
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--repo",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    required=True,
    help="Path to the repository to initialize",
)
def init(repo: Path) -> None:
    """Initialize sensemaking-skills configuration in a repository.

    This command creates a sensemaking-config.yaml file in the target
    repository with default configuration values.

    Example:
        sensemaking-skills init --repo /path/to/repo
    """
    try:
        config_file = repo / "sensemaking-config.yaml"

        # Check if config already exists
        if config_file.exists():
            click.confirm(
                f"Config file already exists at {config_file}. Overwrite?",
                abort=True,
            )

        # Find template file
        template_path = Path(__file__).parent.parent.parent / "templates" / "sensemaking-config.yaml.template"

        if not template_path.exists():
            click.echo(
                f"Error: Template file not found at {template_path}",
                err=True,
            )
            sys.exit(1)

        # Read template
        template_content = template_path.read_text()

        # Write config file
        config_file.write_text(template_content)

        click.echo(f"Successfully created configuration file:")
        click.echo(f"  {config_file}")
        click.echo(f"\nNext steps:")
        click.echo(f"  1. Review and customize {config_file} for your project")
        click.echo(f"  2. Run 'sensemaking-skills analyze --repo {repo}' to start analysis")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
