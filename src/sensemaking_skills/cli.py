#!/usr/bin/env python3
"""
Sensemaking Skills CLI: Repository diagnosis and workflow orchestration.

This CLI coordinates with the agent-native architecture.
For full diagnostic capabilities, use Claude Code with the skill files.
"""

import click
import sys
from pathlib import Path
from . import __version__
from .setup_skills import setup_skills as run_setup_skills


@click.group()
@click.version_option(__version__)
def cli():
    """
    Sensemaking Skills: Agent-native repository diagnosis.
    
    This CLI provides validation and testing utilities.
    For full diagnostics, open this repository in Claude Code and read:
    
        skills/using-sensemaking/SKILL.md
    
    Then ask the agent to diagnose your repository using:
    
        skills/repo-sensemaker/SKILL.md
    """
    pass


@cli.command()
@click.option("--repo", type=click.Path(exists=True), 
              help="Path to repository to analyze")
@click.option("--output", type=click.Path(), default="artifacts/",
              help="Output directory for artifacts (default: artifacts/)")
def analyze(repo, output):
    """
    Analyze a repository for fog type and weakest boundary.
    
    This CLI prepares the environment for agent-driven diagnosis.
    For full diagnostics, see: skills/repo-sensemaker/SKILL.md
    
    Usage:
        sensemaking-skills analyze --repo /path/to/repo
    """
    if not repo:
        click.echo("Error: --repo is required", err=True)
        sys.exit(1)
    
    repo_path = Path(repo).resolve()
    output_path = Path(output).resolve()
    
    click.echo(f"Repository: {repo_path}")
    click.echo(f"Output: {output_path}")
    click.echo()
    click.echo("To analyze this repository, use Claude Code:")
    click.echo()
    click.echo("1. Open this repository in Claude Code")
    click.echo("2. Read: skills/using-sensemaking/SKILL.md")
    click.echo("3. Ask the agent to use: skills/repo-sensemaker/SKILL.md")
    click.echo(f"4. Specify target repo: {repo_path}")
    click.echo("5. Artifacts will be saved to: artifacts/")
    click.echo()
    click.echo("To validate artifacts after agent creates them:")
    click.echo("    sensemaking-skills validate --artifact artifacts/repository_sensemaking_brief.md")


@cli.command()
@click.option("--artifact", type=click.Path(exists=True), required=True,
              help="Path to artifact to validate")
@click.option("--json", "output_json", is_flag=True,
              help="Output validation results as JSON")
def validate(artifact, output_json):
    """
    Validate a repository sensemaking brief or workflow orchestration plan.
    
    Usage:
        sensemaking-skills validate --artifact artifacts/repository_sensemaking_brief.md
    """
    artifact_path = Path(artifact).resolve()
    
    if not artifact_path.exists():
        click.echo(f"Error: Artifact not found: {artifact_path}", err=True)
        sys.exit(1)
    
    click.echo(f"Validating: {artifact_path}")
    click.echo()
    click.echo("To validate artifacts, run:")
    click.echo()
    click.echo(f"    python scripts/validate-and-report.py {artifact_path}")
    click.echo()
    click.echo("Or use Python directly:")
    click.echo()
    click.echo(f"    python scripts/validate-brief.py {artifact_path} --json")


@cli.command()
@click.option("--repos", type=int, default=10,
              help="Number of repositories to test (default: 10)")
def test(repos):
    """
    Run shadow-mode test automation.

    Tests the validation infrastructure against sample repositories.
    """
    click.echo(f"Running shadow-mode tests with {repos} repositories...")
    click.echo()
    click.echo("To run tests, use:")
    click.echo()
    click.echo("    python scripts/shadow-mode-runner.py")
    click.echo()
    click.echo("Or run the full test suite:")
    click.echo()
    click.echo("    python -m pytest tests/ -v")


@cli.command(name="setup-skills")
@click.option("--target",
              type=click.Choice(["agents", "claude-superpowers", "all", "custom"]),
              default="agents",
              help="Installation target: agents (default), claude-superpowers, all, or custom")
@click.option("--skills-dir",
              type=click.Path(),
              default=None,
              help="Custom skills directory (required if --target=custom)")
@click.option("--dry-run",
              is_flag=True,
              help="Show what would be done without actually installing")
@click.option("--force",
              is_flag=True,
              help="Overwrite existing skills")
@click.option("--verbose", "-v",
              is_flag=True,
              help="Print detailed output")
def setup_skills(target, skills_dir, dry_run, force, verbose):
    r"""
    Install sensemaking-skills SKILL.md files to agent-discoverable locations.

    Makes skills available to Claude Code, OpenCode, and other agents.

    Default target is ~/.agents/skills (or C:\Users\*\.agents\skills on Windows).

    After installation, agents can invoke:
        /skill using-sensemaking
        /skill repo-sensemaker
        /skill workflow-planner

    Examples:
        sensemaking-skills setup-skills
        sensemaking-skills setup-skills --target all
        sensemaking-skills setup-skills --target custom --skills-dir /path/to/skills
        sensemaking-skills setup-skills --dry-run
    """
    success = run_setup_skills(
        target=target,
        skills_dir=skills_dir,
        dry_run=dry_run,
        force=force,
        verbose=verbose
    )

    if not success:
        sys.exit(1)


def main():
    """Entry point for CLI."""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\nInterrupted by user", err=True)
        sys.exit(130)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
