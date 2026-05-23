"""Command-line interface for Sensemaking Skills."""

import os
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
@click.option(
    "--from-session",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Path to artifact session directory from a prior workflow run",
)
def analyze(repo: Path, workflow: str, mode: str, from_session: Optional[Path]) -> None:
    """Analyze a repository and generate diagnostic artifacts.

    This command runs the specified workflow against your repository
    to analyze its structure, patterns, and architecture.

    Example:
        sensemaking-skills analyze --repo /path/to/repo --workflow fast-path-workflow --mode guided_execution
    """
    try:
        click.echo(f"Loading configuration from {repo}...")

        try:
            # Load configuration
            config_manager = ConfigManager(str(repo))
            config = config_manager.load()

            click.echo(f"✓ Configuration loaded")
            click.echo(f"  Repository: {repo}")
            click.echo(f"  Artifacts: {config.artifacts_dir}")
            click.echo()

        except FileNotFoundError as e:
            click.echo(f"✗ Configuration file not found: {repo}/sensemaking-config.yaml", err=True)
            click.echo(f"  Hint: Run 'sensemaking-skills init --repo {repo}' to create one", err=True)
            sys.exit(1)
        except Exception as e:
            click.echo(f"✗ Error loading configuration: {e}", err=True)
            sys.exit(1)

        # Create orchestrator
        orchestrator = SkillsOrchestrator(config=config)
        click.echo(f"Orchestrator initialized")

        # Show workflow info
        click.echo(f"Workflow: {workflow}")
        click.echo(f"Mode: {mode}")
        if from_session:
            click.echo(f"Resuming from: {from_session}")

        click.echo(f"\nStarting analysis of {repo}...")

        # Run the workflow
        exit_code = orchestrator.run_workflow(
            workflow_id=workflow,
            execution_mode=mode,
            from_session=str(from_session) if from_session else None,
        )

        sys.exit(exit_code)

    except SystemExit:
        raise
    except Exception as e:
        click.echo(f"✗ Unexpected error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--repo",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    required=True,
    help="Path to the target repository",
)
def list_workflows(repo: Path) -> None:
    """List all registered workflows available for a repository.

    Example:
        sensemaking-skills list-workflows --repo /path/to/repo
    """
    try:
        click.echo(f"Loading configuration from {repo}...")

        try:
            # Load configuration
            config_manager = ConfigManager(str(repo))
            config = config_manager.load()

            click.echo()

        except FileNotFoundError as e:
            click.echo(f"✗ Configuration file not found: {repo}/sensemaking-config.yaml", err=True)
            click.echo(f"  Hint: Run 'sensemaking-skills init --repo {repo}' to create one", err=True)
            sys.exit(1)
        except Exception as e:
            click.echo(f"✗ Error loading configuration: {e}", err=True)
            sys.exit(1)

        # Create orchestrator
        orchestrator = SkillsOrchestrator(config=config)

        # List workflows
        exit_code = orchestrator.list_workflows()

        sys.exit(exit_code)

    except SystemExit:
        raise
    except Exception as e:
        click.echo(f"✗ Unexpected error: {e}", err=True)
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
