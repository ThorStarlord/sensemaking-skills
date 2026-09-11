"""Campaign productization commands built from mechanical primitives only."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from .campaign_semantics import ContractError
from .campaigns import CampaignWorkspaceError
from .campaigns.capabilities import CapabilityCatalogError
from .campaigns.preflight import CampaignPreflightService


ErrorEmitter = Callable[..., None]
JsonEcho = Callable[[dict[str, Any]], None]
PREFLIGHT_INVALID_EXIT = 3


def _check_payload(check: Any) -> dict[str, Any]:
    return {
        "id": check.id,
        "status": check.status,
        "detail": check.detail,
        "diagnostics": list(check.diagnostics),
        "data": dict(check.data),
    }


def register_campaign_productization_commands(
    campaign: click.Group,
    *,
    emit_error: ErrorEmitter,
    json_echo: JsonEcho,
) -> None:
    """Register additive productization commands without semantic routing."""

    @campaign.command(name="preflight")
    @click.option(
        "--workspace",
        required=True,
        type=click.Path(path_type=Path),
        help="Existing Campaign workspace to inspect mechanically",
    )
    @click.option(
        "--responsibility-type",
        default=None,
        help=(
            "Optional agent-supplied responsibility classification used only to "
            "enumerate compatible declared capabilities; never inferred"
        ),
    )
    @click.option("--json", "output_json", is_flag=True, help="Emit JSON")
    def campaign_preflight(
        workspace: Path,
        responsibility_type: str | None,
        output_json: bool,
    ) -> None:
        """Aggregate existing mechanical Campaign readiness checks."""
        normalized_type = responsibility_type.strip() if responsibility_type else None
        if responsibility_type is not None and not normalized_type:
            raise click.ClickException("--responsibility-type must be non-empty when supplied")
        try:
            result = CampaignPreflightService(workspace).inspect(normalized_type)
        except CapabilityCatalogError as exc:
            payload = {
                "ok": False,
                "ready": False,
                "code": "CAMPAIGN_PREFLIGHT_CAPABILITY_CATALOG_ERROR",
                "campaign_id": None,
                "checks": [],
                "message": str(exc),
                "semantic_recommendation_included": False,
                "semantic_truth_established": False,
                "explicit_limit": "Mechanical preflight does not decide whether the agent should proceed.",
            }
            if output_json:
                json_echo(payload)
            else:
                click.echo(f"CAMPAIGN_PREFLIGHT_CAPABILITY_CATALOG_ERROR: {exc}", err=True)
            raise click.exceptions.Exit(PREFLIGHT_INVALID_EXIT)
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return

        payload = {
            "ok": result.ready,
            "ready": result.ready,
            "code": (
                "CAMPAIGN_PREFLIGHT_PASS"
                if result.ready
                else "CAMPAIGN_PREFLIGHT_FAIL"
            ),
            "campaign_id": result.campaign_id,
            "checks": [_check_payload(check) for check in result.checks],
            "semantic_recommendation_included": result.semantic_recommendation_included,
            "semantic_truth_established": result.semantic_truth_established,
            "explicit_limit": "Mechanical preflight does not decide whether the agent should proceed.",
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(payload["code"])
            if result.campaign_id:
                click.echo(f"Campaign: {result.campaign_id}")
            for check in result.checks:
                click.echo(f"{check.status.upper():>14}  {check.id}: {check.detail}")
                for diagnostic in check.diagnostics:
                    click.echo(f"  - {diagnostic}")
            click.echo(payload["explicit_limit"])
        if not result.ready:
            raise click.exceptions.Exit(PREFLIGHT_INVALID_EXIT)
