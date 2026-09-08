"""Click registration for Campaign capability and reconstruction surfaces."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from .campaign_handoff_cli import register_campaign_handoff_commands
from .campaign_lineage_cli import register_campaign_lineage_commands
from .campaign_reconciliation_cli import register_campaign_reconciliation_commands
from .campaign_semantics import ContractError
from .campaign_semantics.registry import RegisteredCapability
from .campaigns import CampaignWorkspaceError
from .campaigns.capabilities import (
    CampaignCapabilityService,
    CapabilityCatalogError,
)


ErrorEmitter = Callable[..., None]
JsonEcho = Callable[[dict[str, Any]], None]
CAPABILITY_CATALOG_EXIT = 3


def _candidate_payload(item: RegisteredCapability) -> dict[str, Any]:
    capability = item.capability
    return {
        "id": capability.id,
        "kind": item.kind,
        "accepted_responsibility_types": list(
            capability.accepted_responsibility_types
        ),
        "input_artifact": capability.input_artifact,
        "output_artifact": capability.output_artifact,
        "completion_conditions": list(capability.completion_conditions),
        "mutates_repository": item.mutates_repository,
        "required_authority": item.authority.value,
        "availability": item.availability.value,
        "availability_reason": item.availability_reason,
        "returns_control": item.returns_control,
    }


def _emit_catalog_error(
    exc: CapabilityCatalogError,
    *,
    output_json: bool,
    json_echo: JsonEcho,
) -> None:
    payload = {
        "ok": False,
        "code": "CAPABILITY_CATALOG_ERROR",
        "message": str(exc),
        "diagnostics": [],
    }
    if output_json:
        json_echo(payload)
    else:
        click.echo(f"CAPABILITY_CATALOG_ERROR: {exc}", err=True)
    raise click.exceptions.Exit(CAPABILITY_CATALOG_EXIT)


def register_campaign_capability_commands(
    campaign: click.Group,
    *,
    emit_error: ErrorEmitter,
    json_echo: JsonEcho,
) -> None:
    """Register P6 inspection and compose later read/reconstruction surfaces."""

    @campaign.command(name="capabilities")
    @click.option(
        "--workspace",
        required=True,
        type=click.Path(path_type=Path),
        help="Existing campaign workspace with one active responsibility",
    )
    @click.option(
        "--responsibility-type",
        required=True,
        help=(
            "Agent-supplied classification used only for declared capability lookup; "
            "it is never inferred from responsibility prose"
        ),
    )
    @click.option("--json", "output_json", is_flag=True, help="Emit JSON")
    def campaign_capabilities(
        workspace: Path,
        responsibility_type: str,
        output_json: bool,
    ) -> None:
        """List unranked declared candidates for an agent-classified responsibility."""
        try:
            result = CampaignCapabilityService(workspace).inspect(
                responsibility_type
            )
        except CapabilityCatalogError as exc:
            _emit_catalog_error(exc, output_json=output_json, json_echo=json_echo)
            return
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return

        candidates = [_candidate_payload(item) for item in result.candidates]
        payload = {
            "ok": True,
            "code": "CAMPAIGN_CAPABILITIES",
            "campaign_id": result.campaign_id,
            "responsibility_id": result.responsibility_id,
            "responsibility_type": result.responsibility_type,
            "responsibility_authority": result.responsibility_authority.value,
            "candidate_count": len(candidates),
            "candidates": candidates,
        }
        if output_json:
            json_echo(payload)
            return

        click.echo("CAMPAIGN_CAPABILITIES")
        click.echo(f"Campaign: {result.campaign_id}")
        click.echo(f"Responsibility: {result.responsibility_id}")
        click.echo(f"Responsibility type: {result.responsibility_type}")
        click.echo(
            f"Responsibility authority: {result.responsibility_authority.value}"
        )
        click.echo(f"Candidates: {len(candidates)}")
        if not candidates:
            click.echo("No declared compatible capabilities.")
            return
        for candidate in candidates:
            click.echo()
            click.echo(candidate["id"])
            click.echo(f"  Kind: {candidate['kind']}")
            click.echo(f"  Availability: {candidate['availability']}")
            if candidate["availability_reason"]:
                click.echo(f"  Availability reason: {candidate['availability_reason']}")
            click.echo(f"  Required authority: {candidate['required_authority']}")
            click.echo(
                "  Mutates repository: "
                + ("yes" if candidate["mutates_repository"] else "no")
            )
            click.echo(f"  Output artifact: {candidate['output_artifact']}")

    # cli.py delegates extension registration through this existing hook. These
    # calls only register commands; they do not couple P6 selection semantics to
    # P7/P8/P9 behavior.
    register_campaign_handoff_commands(
        campaign,
        emit_error=emit_error,
        json_echo=json_echo,
    )
    register_campaign_lineage_commands(
        campaign,
        emit_error=emit_error,
        json_echo=json_echo,
    )
    register_campaign_reconciliation_commands(
        campaign,
        emit_error=emit_error,
        json_echo=json_echo,
    )
