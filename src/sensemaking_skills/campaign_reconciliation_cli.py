"""Click registration for P9 read-only Campaign reconciliation lifecycle."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from .campaign_semantics import ContractError
from .campaigns import CampaignWorkspaceError
from .campaigns.reconciliation import (
    CampaignReconciliationResult,
    CampaignReconciliationService,
    ReconciliationEvidence,
)


ErrorEmitter = Callable[..., None]
JsonEcho = Callable[[dict[str, Any]], None]


def _report_payload(item: ReconciliationEvidence) -> dict[str, Any]:
    return {
        "artifact_id": item.artifact_id,
        "artifact_ref": item.artifact_ref,
        "artifact_sha256": item.artifact_sha256,
        "admissions": [
            {
                "ref": admission.ref,
                "validator": admission.validator,
                "validation_timestamp": admission.validation_timestamp,
                "validation_result_sha256": admission.validation_result_sha256,
            }
            for admission in item.admissions
        ],
        "disposition_status": item.disposition_status,
        "disposition_required": item.disposition_required,
        "bound_transition_ids": list(item.bound_transition_ids),
        "legacy_unbound_transition_ids": list(item.legacy_unbound_transition_ids),
    }


def _result_payload(result: CampaignReconciliationResult) -> dict[str, Any]:
    reports = [_report_payload(item) for item in result.reports]
    return {
        "ok": True,
        "code": "CAMPAIGN_RECONCILIATION",
        "campaign_id": result.campaign_id,
        "report_count": len(reports),
        "disposition_required_count": result.disposition_required_count,
        "disposition_recorded_count": result.disposition_recorded_count,
        "legacy_unbound_count": result.legacy_unbound_count,
        "reports": reports,
    }


def register_campaign_reconciliation_commands(
    campaign: click.Group,
    *,
    emit_error: ErrorEmitter,
    json_echo: JsonEcho,
) -> None:
    """Register P9's deterministic reconciliation inspection command."""

    @campaign.command(name="reconciliation")
    @click.option(
        "--workspace",
        required=True,
        type=click.Path(path_type=Path),
        help="Existing Campaign workspace",
    )
    @click.option("--json", "output_json", is_flag=True, help="Emit JSON")
    def campaign_reconciliation(workspace: Path, output_json: bool) -> None:
        """Inspect admitted reconciliation evidence and explicit disposition state."""
        try:
            result = CampaignReconciliationService(workspace).inspect()
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return

        payload = _result_payload(result)
        if output_json:
            json_echo(payload)
            return

        click.echo("CAMPAIGN_RECONCILIATION")
        click.echo(f"Campaign: {result.campaign_id}")
        click.echo(f"Reports: {len(result.reports)}")
        click.echo(f"Disposition required: {result.disposition_required_count}")
        click.echo(f"Disposition recorded: {result.disposition_recorded_count}")
        click.echo(f"Legacy unbound: {result.legacy_unbound_count}")
        if not result.reports:
            click.echo("No admitted reconciliation evidence.")
            return

        for report in result.reports:
            click.echo()
            click.echo(report.artifact_ref)
            click.echo(f"  Artifact ID: {report.artifact_id}")
            click.echo(f"  SHA-256: {report.artifact_sha256}")
            click.echo(f"  Disposition status: {report.disposition_status}")
            if report.bound_transition_ids:
                click.echo(
                    "  Bound transition(s): " + ", ".join(report.bound_transition_ids)
                )
            if report.legacy_unbound_transition_ids:
                click.echo(
                    "  Legacy unbound transition(s): "
                    + ", ".join(report.legacy_unbound_transition_ids)
                )
            click.echo("  Admission receipt(s):")
            for admission in report.admissions:
                click.echo(f"    - {admission.ref}")
                click.echo(f"      validator: {admission.validator}")
                click.echo(
                    f"      validation timestamp: {admission.validation_timestamp}"
                )
