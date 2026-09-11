"""CLI surfaces for deterministic terminal Campaign completion and archival."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from .campaign_semantics import ContractError
from .campaigns import CampaignWorkspaceError
from .campaigns.completion import CampaignCompletionService


ErrorEmitter = Callable[..., None]
JsonEcho = Callable[[dict[str, Any]], None]
INVALID_EXIT = 3


def _completion_payload(result: Any, *, code: str) -> dict[str, Any]:
    return {
        "ok": result.valid,
        "code": code,
        "campaign_id": result.campaign_id,
        "present": result.present,
        "receipt_sha256": result.receipt_sha256,
        "receipt": dict(result.payload) if result.payload is not None else None,
        "diagnostics": list(result.diagnostics),
        "semantic_truth_established": False,
        "semantic_success_established": False,
        "explicit_limit": "Completion receipts summarize an already-terminal Campaign mechanically; they do not close the Campaign or prove that its terminal decision was correct.",
    }


def _archive_payload(result: Any) -> dict[str, Any]:
    return {
        "ok": result.valid,
        "code": "CAMPAIGN_ARCHIVED" if result.valid else "CAMPAIGN_ARCHIVE_INVALID",
        "campaign_id": result.campaign_id,
        "present": result.present,
        "archive_sha256": result.archive_sha256,
        "diagnostics": list(result.diagnostics),
        "workspace_moved": False,
        "workspace_deleted": False,
        "semantic_success_established": False,
        "explicit_limit": "Archive is a durable marker for an already-terminal Campaign with a valid completion receipt; it is not a success judgment and does not move or delete the workspace.",
    }


def register_campaign_completion_commands(
    campaign: click.Group,
    *,
    emit_error: ErrorEmitter,
    json_echo: JsonEcho,
) -> None:
    @campaign.command(name="closeout")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def campaign_closeout(workspace: Path, output_json: bool) -> None:
        """Write/reconcile a deterministic receipt for an already-terminal Campaign."""
        try:
            result = CampaignCompletionService(workspace).closeout()
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        except (OSError, ValueError) as exc:
            raise click.ClickException(str(exc)) from exc
        payload = _completion_payload(result, code="CAMPAIGN_CLOSEOUT_RECORDED")
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        if not result.valid:
            raise click.exceptions.Exit(INVALID_EXIT)

    @campaign.command(name="completion-receipt")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def campaign_completion_receipt(workspace: Path, output_json: bool) -> None:
        """Verify the completion receipt against current durable terminal state."""
        try:
            result = CampaignCompletionService(workspace).inspect_receipt()
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        except (OSError, ValueError) as exc:
            raise click.ClickException(str(exc)) from exc
        payload = _completion_payload(
            result,
            code="CAMPAIGN_COMPLETION_RECEIPT_VALID" if result.valid else "CAMPAIGN_COMPLETION_RECEIPT_INVALID",
        )
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        if not result.valid:
            raise click.exceptions.Exit(INVALID_EXIT)

    @campaign.command(name="archive")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def campaign_archive(workspace: Path, output_json: bool) -> None:
        """Mark a receipt-qualified terminal Campaign archived without moving it."""
        try:
            result = CampaignCompletionService(workspace).archive()
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        except (OSError, ValueError) as exc:
            raise click.ClickException(str(exc)) from exc
        payload = _archive_payload(result)
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        if not result.valid:
            raise click.exceptions.Exit(INVALID_EXIT)
