"""CLI for explicit portable primary-target locator rebinding."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from .campaign_semantics import ContractError
from .campaigns import CampaignWorkspaceError
from .campaigns.target_rebind import PrimaryTargetRebindService


ErrorEmitter = Callable[..., None]
JsonEcho = Callable[[dict[str, Any]], None]
INVALID_EXIT = 3


def _payload(result: Any, *, code: str) -> dict[str, Any]:
    return {
        "ok": result.valid,
        "code": code,
        "campaign_id": result.campaign_id,
        "repository_root": result.repository_root,
        "locator_sha256": result.locator_sha256,
        "diagnostics": [
            {"code": item.code, "detail": item.detail}
            for item in result.diagnostics
        ],
        "repository_discovery_performed": False,
        "semantic_truth_established": False,
        "semantic_recommendation_included": False,
        "explicit_limit": "Target rebinding accepts a caller-supplied path and verifies exact recorded repository identity/state; it does not discover, select, refresh, or authorize repository work.",
    }


def register_campaign_target_rebind_commands(
    campaign: click.Group,
    *,
    emit_error: ErrorEmitter,
    json_echo: JsonEcho,
) -> None:
    @campaign.group(name="target")
    def target_group() -> None:
        """Operate explicit primary-target locator companions."""

    @target_group.command(name="rebind")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--target-repo", required=True, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def target_rebind(workspace: Path, target_repo: Path, output_json: bool) -> None:
        """Bind a caller-supplied new path to the exact existing target state."""
        try:
            result = PrimaryTargetRebindService(workspace).rebind(target_repo)
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
        payload = _payload(result, code="CAMPAIGN_TARGET_REBOUND")
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))

    @target_group.command(name="verify-rebind")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def target_verify_rebind(workspace: Path, output_json: bool) -> None:
        """Verify the durable rebound locator against live repository bytes."""
        try:
            result = PrimaryTargetRebindService(workspace).verify()
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
        payload = _payload(
            result,
            code=("CAMPAIGN_TARGET_REBIND_VALID" if result.valid else "CAMPAIGN_TARGET_REBIND_INVALID"),
        )
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        if not result.valid:
            raise click.exceptions.Exit(INVALID_EXIT)
