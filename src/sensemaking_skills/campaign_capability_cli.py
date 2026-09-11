"""Click registration for Campaign capability and reconstruction surfaces."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from .campaign_handoff_cli import register_campaign_handoff_commands
from .campaign_lineage_cli import register_campaign_lineage_commands
from .campaign_productization_cli import register_campaign_productization_commands
from .campaign_reconciliation_cli import register_campaign_reconciliation_commands
from .campaign_semantics import ContractError
from .campaign_semantics.registry import RegisteredCapability
from .campaigns import CampaignWorkspaceError
from .campaigns.capabilities import CampaignCapabilityService, CapabilityCatalogError


ErrorEmitter = Callable[..., None]
JsonEcho = Callable[[dict[str, Any]], None]
CAPABILITY_CATALOG_EXIT = 3


def _candidate_payload(item: RegisteredCapability) -> dict[str, Any]:
    capability = item.capability
    return {
        "id": capability.id,
        "kind": item.kind,
        "accepted_responsibility_types": list(capability.accepted_responsibility_types),
        "input_artifact": capability.input_artifact,
        "output_artifact": capability.output_artifact,
        "completion_conditions": list(capability.completion_conditions),
        "mutates_repository": item.mutates_repository,
        "required_authority": item.authority.value,
        "availability": item.availability.value,
        "availability_reason": item.availability_reason,
        "returns_control": item.returns_control,
    }


def _emit_catalog_error(exc: CapabilityCatalogError, *, output_json: bool, json_echo: JsonEcho) -> None:
    payload = {"ok": False, "code": "CAPABILITY_CATALOG_ERROR", "message": str(exc), "diagnostics": []}
    if output_json:
        json_echo(payload)
    else:
        click.echo(f"CAPABILITY_CATALOG_ERROR: {exc}", err=True)
    raise click.exceptions.Exit(CAPABILITY_CATALOG_EXIT)


def _inspection_payload(result: Any) -> dict[str, Any]:
    candidates = [_candidate_payload(item) for item in result.candidates]
    return {
        "campaign_id": result.campaign_id,
        "responsibility_id": result.responsibility_id,
        "responsibility_type": result.responsibility_type,
        "responsibility_authority": result.responsibility_authority.value,
        "candidate_count": len(candidates),
        "candidates": candidates,
    }


def register_campaign_capability_commands(
    campaign: click.Group,
    *,
    emit_error: ErrorEmitter,
    json_echo: JsonEcho,
) -> None:
    """Register P6 inspection and compose later read/reconstruction surfaces."""

    @campaign.command(name="capabilities")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path), help="Existing campaign workspace with one active responsibility")
    @click.option(
        "--responsibility-type",
        required=True,
        help="Agent-supplied classification used only for declared capability lookup; it is never inferred from responsibility prose",
    )
    @click.option("--json", "output_json", is_flag=True, help="Emit JSON")
    def campaign_capabilities(workspace: Path, responsibility_type: str, output_json: bool) -> None:
        """List unranked declared candidates for an agent-classified responsibility."""
        try:
            result = CampaignCapabilityService(workspace).inspect(responsibility_type)
        except CapabilityCatalogError as exc:
            _emit_catalog_error(exc, output_json=output_json, json_echo=json_echo)
            return
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return

        payload = {"ok": True, "code": "CAMPAIGN_CAPABILITIES", **_inspection_payload(result)}
        if output_json:
            json_echo(payload)
            return

        click.echo("CAMPAIGN_CAPABILITIES")
        click.echo(f"Campaign: {result.campaign_id}")
        click.echo(f"Responsibility: {result.responsibility_id}")
        click.echo(f"Responsibility type: {result.responsibility_type}")
        click.echo(f"Responsibility authority: {result.responsibility_authority.value}")
        click.echo(f"Candidates: {payload['candidate_count']}")
        if not payload["candidates"]:
            click.echo("No declared compatible capabilities.")
            return
        for candidate in payload["candidates"]:
            click.echo()
            click.echo(candidate["id"])
            click.echo(f"  Kind: {candidate['kind']}")
            click.echo(f"  Availability: {candidate['availability']}")
            if candidate["availability_reason"]:
                click.echo(f"  Availability reason: {candidate['availability_reason']}")
            click.echo(f"  Required authority: {candidate['required_authority']}")
            click.echo("  Mutates repository: " + ("yes" if candidate["mutates_repository"] else "no"))
            click.echo(f"  Output artifact: {candidate['output_artifact']}")

    @campaign.command(name="capability-context")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option(
        "--responsibility-type",
        required=True,
        help="Explicit agent-supplied classification; this command never infers or selects it",
    )
    @click.option("--json", "output_json", is_flag=True)
    def campaign_capability_context(workspace: Path, responsibility_type: str, output_json: bool) -> None:
        """Project compatible declared capabilities after responsibility selection."""
        try:
            result = CampaignCapabilityService(workspace).inspect(responsibility_type)
        except CapabilityCatalogError as exc:
            _emit_catalog_error(exc, output_json=output_json, json_echo=json_echo)
            return
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return

        payload = {
            "ok": True,
            "code": "CAMPAIGN_CAPABILITY_CONTEXT",
            **_inspection_payload(result),
            "selection_performed": False,
            "recommendation_performed": False,
            "authority_granted": False,
            "semantic_truth_established": False,
            "explicit_limit": "Capability context enumerates mechanically compatible declarations for the agent-supplied responsibility type; the agent still chooses whether and what to invoke.",
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo("CAMPAIGN_CAPABILITY_CONTEXT")
            click.echo(f"Responsibility: {result.responsibility_id} ({result.responsibility_type})")
            for candidate in payload["candidates"]:
                click.echo(f"- {candidate['id']} [{candidate['availability']}] -> {candidate['output_artifact']}")
            click.echo(payload["explicit_limit"])

    # cli.py delegates extension registration through this existing hook. These
    # calls only register commands; they do not couple P6 selection semantics to
    # later lifecycle, reconstruction, or productization behavior.
    register_campaign_handoff_commands(campaign, emit_error=emit_error, json_echo=json_echo)
    register_campaign_lineage_commands(campaign, emit_error=emit_error, json_echo=json_echo)
    register_campaign_reconciliation_commands(campaign, emit_error=emit_error, json_echo=json_echo)
    register_campaign_productization_commands(campaign, emit_error=emit_error, json_echo=json_echo)
