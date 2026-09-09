"""Agent-visible CLI for Campaign schema compatibility and upgrades.

This module is intentionally separate from the main CLI so schema maintenance
can evolve without coupling it to semantic campaign decisions. Invoke with:

    python -m sensemaking_skills.campaign_schema_cli status --workspace PATH
    python -m sensemaking_skills.campaign_schema_cli upgrade --workspace PATH
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import click

from .campaign_semantics import ContractError
from .campaigns.errors import CampaignWorkspaceError
from .campaigns.schema_evolution import CampaignSchemaEvolutionService


SCHEMA_INVALID_EXIT = 3


def _json_echo(payload: dict[str, Any]) -> None:
    click.echo(json.dumps(payload, sort_keys=True, ensure_ascii=False))


def _emit_error(exc: Exception, *, output_json: bool) -> None:
    payload = {
        "ok": False,
        "code": "CAMPAIGN_SCHEMA_ERROR",
        "message": str(exc),
    }
    diagnostic_codes = getattr(exc, "diagnostic_codes", ())
    if diagnostic_codes:
        payload["diagnostics"] = list(diagnostic_codes)
    if output_json:
        _json_echo(payload)
    else:
        click.echo(f"CAMPAIGN_SCHEMA_ERROR: {exc}", err=True)
    raise click.exceptions.Exit(SCHEMA_INVALID_EXIT)


@click.group()
def main() -> None:
    """Inspect or qualify deterministic Campaign schema upgrades."""


@main.command(name="status")
@click.option(
    "--workspace",
    required=True,
    type=click.Path(path_type=Path),
    help="Existing durable Campaign workspace",
)
@click.option("--json", "output_json", is_flag=True, help="Emit JSON")
def schema_status(workspace: Path, output_json: bool) -> None:
    """Inspect raw/effective schema versions and migration receipt coverage."""

    try:
        status = CampaignSchemaEvolutionService(workspace).status()
    except (CampaignWorkspaceError, ContractError) as exc:
        _emit_error(exc, output_json=output_json)

    payload = status.to_dict()
    payload.update(
        {
            "ok": True,
            "code": (
                "CAMPAIGN_SCHEMA_CURRENT"
                if status.qualified
                else "CAMPAIGN_SCHEMA_UPGRADE_REQUIRED"
            ),
        }
    )
    if output_json:
        _json_echo(payload)
        return

    click.echo(payload["code"])
    click.echo(f"Campaign: {status.campaign_id}")
    click.echo(f"Current schema: {status.current_schema_version}")
    click.echo(f"Migration receipts: {status.receipt_count}")
    for artifact in status.artifacts:
        suffix = f" -> {artifact.effective_schema_version}"
        if artifact.receipt_ref:
            suffix += f" ({artifact.receipt_ref})"
        click.echo(
            f"{artifact.migration_status:9} {artifact.artifact_ref}: "
            f"{artifact.source_schema_version}{suffix}"
        )


@main.command(name="upgrade")
@click.option(
    "--workspace",
    required=True,
    type=click.Path(path_type=Path),
    help="Existing durable Campaign workspace",
)
@click.option("--json", "output_json", is_flag=True, help="Emit JSON")
def schema_upgrade(workspace: Path, output_json: bool) -> None:
    """Write append-only receipts for every exact migratable legacy artifact."""

    try:
        result = CampaignSchemaEvolutionService(workspace).upgrade()
    except (CampaignWorkspaceError, ContractError) as exc:
        _emit_error(exc, output_json=output_json)

    payload = result.to_dict()
    payload.update(
        {
            "ok": True,
            "code": "CAMPAIGN_SCHEMA_UPGRADED",
        }
    )
    if output_json:
        _json_echo(payload)
        return

    click.echo("CAMPAIGN_SCHEMA_UPGRADED")
    click.echo(f"Campaign: {result.after.campaign_id}")
    click.echo(f"Current schema: {result.after.current_schema_version}")
    click.echo(f"Receipts written: {len(result.receipts_written)}")
    for receipt_ref in result.receipts_written:
        click.echo(f"  - {receipt_ref}")


if __name__ == "__main__":
    main()
