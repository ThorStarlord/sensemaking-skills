#!/usr/bin/env python3
"""
Sensemaking Skills CLI: repository diagnosis utilities and durable campaigns.

The CLI preserves the agent-native architecture. Campaign commands expose
mechanically validated durable state; they do not diagnose repositories, choose
responsibilities, rank capabilities, or decide what work should happen next.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import click

from . import __version__
from .campaign_semantics import CampaignState, ContractError, canonicalize
from .campaigns import (
    ArtifactAdmissionService,
    ArtifactValidationRejectedError,
    ArtifactValidatorError,
    CampaignAlreadyExistsError,
    CampaignIdentityError,
    CampaignIntegrityError,
    CampaignNotInitializedError,
    CampaignService,
    CampaignSnapshot,
    CampaignTransactionError,
    CampaignWorkspaceError,
)
from .setup_skills import setup_skills as run_setup_skills


CAMPAIGN_INVALID_EXIT = 3
CAMPAIGN_WORKSPACE_EXIT = 4
ARTIFACT_INVALID_EXIT = 5
ARTIFACT_VALIDATOR_EXIT = 6


@click.group()
@click.version_option(__version__)
def cli():
    """
    Sensemaking Skills: Agent-native repository diagnosis.

    This CLI provides validation, testing, setup, and durable campaign
    operations. For full repository diagnosis, use the agent-native skills in
    skills/.
    """
    pass


def _enum_value(value: Any) -> Any:
    return value.value if value is not None and hasattr(value, "value") else value


def _json_echo(payload: dict[str, Any]) -> None:
    click.echo(json.dumps(payload, sort_keys=True, ensure_ascii=False))


def _campaign_error_code(exc: Exception) -> str:
    if isinstance(exc, ArtifactValidationRejectedError):
        return "ARTIFACT_VALIDATION_REJECTED"
    if isinstance(exc, ArtifactValidatorError):
        return "ARTIFACT_VALIDATOR_ERROR"
    if isinstance(exc, CampaignIntegrityError):
        return "CAMPAIGN_INTEGRITY_ERROR"
    if isinstance(exc, ContractError):
        return "CAMPAIGN_INTEGRITY_ERROR"
    if isinstance(exc, CampaignAlreadyExistsError):
        return "CAMPAIGN_ALREADY_EXISTS"
    if isinstance(exc, CampaignNotInitializedError):
        return "CAMPAIGN_NOT_INITIALIZED"
    if isinstance(exc, CampaignIdentityError):
        return "CAMPAIGN_IDENTITY_ERROR"
    if isinstance(exc, CampaignTransactionError):
        return "CAMPAIGN_TRANSACTION_ERROR"
    return "CAMPAIGN_WORKSPACE_ERROR"


def _campaign_error_exit(exc: Exception) -> int:
    if isinstance(exc, ArtifactValidationRejectedError):
        return ARTIFACT_INVALID_EXIT
    if isinstance(exc, ArtifactValidatorError):
        return ARTIFACT_VALIDATOR_EXIT
    if isinstance(exc, (CampaignIntegrityError, ContractError)):
        return CAMPAIGN_INVALID_EXIT
    return CAMPAIGN_WORKSPACE_EXIT


def _campaign_error_diagnostics(exc: Exception) -> list[str]:
    if isinstance(exc, CampaignIntegrityError):
        return list(exc.diagnostic_codes)
    return []


def _emit_campaign_error(exc: Exception, *, output_json: bool) -> None:
    code = _campaign_error_code(exc)
    diagnostics = _campaign_error_diagnostics(exc)
    payload: dict[str, Any] = {
        "ok": False,
        "code": code,
        "message": str(exc),
        "diagnostics": diagnostics,
    }
    if isinstance(exc, ArtifactValidationRejectedError):
        payload["validation_result"] = exc.validation_result
    if output_json:
        _json_echo(payload)
    else:
        click.echo(f"{code}: {exc}", err=True)
        for diagnostic in diagnostics:
            click.echo(f"  - {diagnostic}", err=True)
        if isinstance(exc, ArtifactValidationRejectedError):
            for error in exc.validation_result.get("errors", []):
                if isinstance(error, dict):
                    error_id = error.get("error_id", "validation_error")
                    message = error.get("message", str(error))
                    click.echo(f"  - {error_id}: {message}", err=True)
    raise click.exceptions.Exit(_campaign_error_exit(exc))


def _status_payload(snapshot: CampaignSnapshot) -> dict[str, Any]:
    state = snapshot.state
    return {
        "ok": True,
        "campaign_id": state.campaign_id,
        "mission": state.mission,
        "status": state.status,
        "current_state": state.current_state,
        "authority": _enum_value(state.authority),
        "terminal_state": _enum_value(state.terminal_state),
        "active_responsibility": (
            canonicalize(state.active_responsibility)
            if state.active_responsibility is not None
            else None
        ),
        "active_uncertainty": (
            canonicalize(state.active_uncertainty)
            if state.active_uncertainty is not None
            else None
        ),
        "transition_count": len(snapshot.transitions),
        "evidence_count": len(snapshot.evidence_refs),
        "evidence_refs": list(snapshot.evidence_refs),
        "has_policy": snapshot.policy is not None,
        "has_handoff": snapshot.handoff is not None,
    }


def _echo_campaign_status(snapshot: CampaignSnapshot, *, heading: str) -> None:
    state = snapshot.state
    click.echo(heading)
    click.echo(f"Campaign: {state.campaign_id}")
    click.echo(f"Mission: {state.mission}")
    click.echo(f"Status: {state.status}")
    click.echo(f"Current state: {state.current_state}")
    click.echo(f"Authority: {_enum_value(state.authority) or 'none'}")
    click.echo(f"Terminal state: {_enum_value(state.terminal_state) or 'none'}")
    if state.active_responsibility is None:
        click.echo("Active responsibility: none")
    else:
        click.echo(
            "Active responsibility: "
            f"{state.active_responsibility.id} — {state.active_responsibility.statement}"
        )
    click.echo(f"Transitions: {len(snapshot.transitions)}")
    click.echo(f"Evidence records: {len(snapshot.evidence_refs)}")
    click.echo(f"Policy: {'present' if snapshot.policy is not None else 'none'}")
    click.echo(f"Handoff: {'present' if snapshot.handoff is not None else 'none'}")


def _history_payload(snapshot: CampaignSnapshot) -> dict[str, Any]:
    return {
        "ok": True,
        "campaign_id": snapshot.state.campaign_id,
        "initial_state": snapshot.trace.initial_state,
        "current_state": snapshot.state.current_state,
        "transition_count": len(snapshot.transitions),
        "transitions": [canonicalize(transition) for transition in snapshot.transitions],
    }


@cli.command()
@click.option(
    "--repo",
    type=click.Path(exists=True),
    help="Path to repository to analyze",
)
@click.option(
    "--output",
    type=click.Path(),
    default="artifacts/",
    help="Output directory for artifacts (default: artifacts/)",
)
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
    click.echo(
        "    sensemaking-skills validate --artifact "
        "artifacts/repository_sensemaking_brief.md"
    )


@cli.command()
@click.option(
    "--artifact",
    type=click.Path(exists=True),
    required=True,
    help="Path to artifact to validate",
)
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    help="Output validation results as JSON",
)
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
@click.option(
    "--repos",
    type=int,
    default=10,
    help="Number of repositories to test (default: 10)",
)
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
@click.option(
    "--target",
    type=click.Choice(["agents", "claude-superpowers", "all", "custom"]),
    default="agents",
    help=(
        "Installation target: agents (default), claude-superpowers, all, or custom"
    ),
)
@click.option(
    "--skills-dir",
    type=click.Path(),
    default=None,
    help="Custom skills directory (required if --target=custom)",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be done without actually installing",
)
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite existing skills",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Print detailed output",
)
def setup_skills(target, skills_dir, dry_run, force, verbose):
    r"""
    Install sensemaking-skills SKILL.md files to agent-discoverable locations.

    Makes skills available to Claude Code, OpenCode, and other agents.

    Default target is ~/.agents/skills (or C:\Users\*\.agents\skills on Windows).

    After installation, agents can invoke:
        /skill using-sensemaking
        /skill repo-sensemaker
        /skill workflow-planner
    """
    success = run_setup_skills(
        target=target,
        skills_dir=skills_dir,
        dry_run=dry_run,
        force=force,
        verbose=verbose,
    )

    if not success:
        sys.exit(1)


@cli.group()
def campaign():
    """Operate durable campaigns without making semantic decisions."""
    pass


@campaign.command(name="init")
@click.option(
    "--workspace",
    required=True,
    type=click.Path(path_type=Path),
    help="Campaign workspace directory to create",
)
@click.option("--campaign-id", required=True, help="Durable campaign identifier")
@click.option("--mission", required=True, help="Owner/agent supplied campaign mission")
@click.option(
    "--state",
    "initial_state",
    default="initialized",
    show_default=True,
    help="Initial durable state label; no semantic meaning is inferred",
)
@click.option(
    "--target-repo",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=None,
    help="Optional target repository; workspace must be outside it",
)
@click.option("--json", "output_json", is_flag=True, help="Emit JSON")
def campaign_init(
    workspace: Path,
    campaign_id: str,
    mission: str,
    initial_state: str,
    target_repo: Path | None,
    output_json: bool,
):
    """Create a campaign from explicitly supplied state; infer nothing."""
    state = CampaignState(
        campaign_id=campaign_id,
        mission=mission,
        status="active",
        current_state=initial_state,
    )
    try:
        snapshot = CampaignService(workspace, target_repo=target_repo).initialize(state)
    except (CampaignWorkspaceError, ContractError) as exc:
        _emit_campaign_error(exc, output_json=output_json)

    if output_json:
        payload = _status_payload(snapshot)
        payload["code"] = "CAMPAIGN_INITIALIZED"
        _json_echo(payload)
    else:
        _echo_campaign_status(snapshot, heading="CAMPAIGN_INITIALIZED")


@campaign.command(name="ingest")
@click.option(
    "--workspace",
    required=True,
    type=click.Path(path_type=Path),
    help="Existing campaign workspace",
)
@click.option(
    "--artifact",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Artifact file to validate and admit",
)
@click.option(
    "--framework-root",
    required=True,
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Sensemaking framework checkout containing scripts/validate-and-report.py",
)
@click.option(
    "--target-repo",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=None,
    help="Repository the artifact is about, for target-aware validators",
)
@click.option(
    "--probe-report",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=None,
    help="Explicit same-episode Probe Engine report for brief validation",
)
@click.option("--json", "output_json", is_flag=True, help="Emit JSON")
def campaign_ingest(
    workspace: Path,
    artifact: Path,
    framework_root: Path,
    target_repo: Path | None,
    probe_report: Path | None,
    output_json: bool,
):
    """Canonically validate exact artifact bytes, then admit them as evidence."""
    try:
        result = ArtifactAdmissionService(workspace).admit(
            artifact,
            framework_root=framework_root,
            target_repo=target_repo,
            probe_report=probe_report,
        )
    except (CampaignWorkspaceError, ContractError) as exc:
        _emit_campaign_error(exc, output_json=output_json)

    payload = {
        "ok": True,
        "code": "ARTIFACT_ADMITTED",
        "artifact_id": result.artifact_id,
        "artifact_ref": result.artifact_ref,
        "admission_ref": result.admission_ref,
        "artifact_sha256": result.artifact_sha256,
        "validator": result.admission.validator,
        "validation_timestamp": result.admission.validation_timestamp,
        "router_sha256": result.admission.router_sha256,
        "validator_sha256": result.admission.validator_sha256,
    }
    if output_json:
        _json_echo(payload)
    else:
        click.echo("ARTIFACT_ADMITTED")
        click.echo(f"Artifact ID: {result.artifact_id}")
        click.echo(f"Artifact ref: {result.artifact_ref}")
        click.echo(f"Admission ref: {result.admission_ref}")
        click.echo(f"Artifact SHA-256: {result.artifact_sha256}")
        click.echo(f"Validator: {result.admission.validator}")


@campaign.command(name="status")
@click.option(
    "--workspace",
    required=True,
    type=click.Path(path_type=Path),
    help="Existing campaign workspace",
)
@click.option("--json", "output_json", is_flag=True, help="Emit JSON")
def campaign_status(workspace: Path, output_json: bool):
    """Show what durable campaign state currently says."""
    try:
        snapshot = CampaignService(workspace).resume()
    except (CampaignWorkspaceError, ContractError) as exc:
        _emit_campaign_error(exc, output_json=output_json)

    if output_json:
        payload = _status_payload(snapshot)
        payload["code"] = "CAMPAIGN_STATUS"
        _json_echo(payload)
    else:
        _echo_campaign_status(snapshot, heading="CAMPAIGN_STATUS")


@campaign.command(name="validate")
@click.option(
    "--workspace",
    required=True,
    type=click.Path(path_type=Path),
    help="Existing campaign workspace",
)
@click.option("--json", "output_json", is_flag=True, help="Emit JSON")
def campaign_validate(workspace: Path, output_json: bool):
    """Validate durable reconstruction and return a stable exit code."""
    try:
        result = CampaignService(workspace).validate()
    except (CampaignWorkspaceError, ContractError) as exc:
        _emit_campaign_error(exc, output_json=output_json)

    diagnostics = [
        {"code": diagnostic.code, "detail": diagnostic.detail}
        for diagnostic in result.diagnostics
    ]
    code = "CAMPAIGN_VALID" if result.valid else "CAMPAIGN_INVALID"
    if output_json:
        _json_echo(
            {
                "ok": result.valid,
                "valid": result.valid,
                "code": code,
                "diagnostics": diagnostics,
            }
        )
    else:
        click.echo(code)
        for diagnostic in result.diagnostics:
            click.echo(f"  {diagnostic.code}: {diagnostic.detail}")

    if not result.valid:
        raise click.exceptions.Exit(CAMPAIGN_INVALID_EXIT)


@campaign.command(name="history")
@click.option(
    "--workspace",
    required=True,
    type=click.Path(path_type=Path),
    help="Existing campaign workspace",
)
@click.option("--json", "output_json", is_flag=True, help="Emit JSON")
def campaign_history(workspace: Path, output_json: bool):
    """Show trace-defined transition history; never infer a next action."""
    try:
        snapshot = CampaignService(workspace).resume()
    except (CampaignWorkspaceError, ContractError) as exc:
        _emit_campaign_error(exc, output_json=output_json)

    if output_json:
        payload = _history_payload(snapshot)
        payload["code"] = "CAMPAIGN_HISTORY"
        _json_echo(payload)
        return

    click.echo("CAMPAIGN_HISTORY")
    click.echo(f"Campaign: {snapshot.state.campaign_id}")
    click.echo(f"Initial state: {snapshot.trace.initial_state or 'unknown'}")
    click.echo(f"Current state: {snapshot.state.current_state}")
    click.echo(f"Transitions: {len(snapshot.transitions)}")
    for transition in snapshot.transitions:
        click.echo()
        click.echo(f"{transition.id}: {transition.from_state} -> {transition.to_state}")
        click.echo(f"Decision: {transition.decision}")
        if transition.evidence:
            click.echo("Evidence:")
            for evidence in transition.evidence:
                click.echo(f"  - {evidence}")
        else:
            click.echo("Evidence: none")
        click.echo(
            "Next responsibility: "
            f"{transition.next_responsibility or 'none'}"
        )
        click.echo(
            "Terminal state: "
            f"{_enum_value(transition.terminal_state) or 'none'}"
        )


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
