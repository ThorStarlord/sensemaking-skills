"""Campaign productization commands built from mechanical primitives only."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from .campaign_semantics import ContractError
from .campaigns import CampaignWorkspaceError
from .campaigns.capabilities import CapabilityCatalogError
from .campaigns.doctor import CampaignDoctorService, doctor_payload
from .campaigns.preflight import CampaignPreflightService
from .campaigns.provenance import (
    CampaignProvenanceService,
    provenance_payload,
    render_provenance_markdown,
)
from .campaigns.provenance_graph import CampaignProvenanceGraphService
from .campaigns.uncertainty_history import ALLOWED_STATUSES, UncertaintyHistoryService


ErrorEmitter = Callable[..., None]
JsonEcho = Callable[[dict[str, Any]], None]
PREFLIGHT_INVALID_EXIT = 3
HISTORY_INVALID_EXIT = 3
OPERABILITY_INVALID_EXIT = 3


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

    @campaign.command(name="uncertainty-record")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--event-id", required=True, help="Unique append-only lifecycle event id")
    @click.option("--uncertainty-id", required=True, help="Agent-supplied uncertainty identity")
    @click.option("--status", required=True, type=click.Choice(sorted(ALLOWED_STATUSES)))
    @click.option("--transition-id", default=None, help="Optional exact Campaign transition id")
    @click.option("--evidence-ref", "evidence_refs", multiple=True, help="Campaign-authoritative evidence ref")
    @click.option("--superseded-by", default=None, help="Replacement uncertainty id for status=superseded")
    @click.option("--note", default=None, help="Optional explicit lifecycle note; not a semantic ranking")
    @click.option("--json", "output_json", is_flag=True)
    def campaign_uncertainty_record(
        workspace: Path,
        event_id: str,
        uncertainty_id: str,
        status: str,
        transition_id: str | None,
        evidence_refs: tuple[str, ...],
        superseded_by: str | None,
        note: str | None,
        output_json: bool,
    ) -> None:
        """Append an agent-authored uncertainty lifecycle observation."""
        try:
            service = UncertaintyHistoryService(workspace)
            digest = service.append(
                event_id=event_id,
                uncertainty_id=uncertainty_id,
                status=status,
                transition_id=transition_id,
                evidence_refs=evidence_refs,
                superseded_by=superseded_by,
                note=note,
            )
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc

        payload = {
            "ok": True,
            "code": "CAMPAIGN_UNCERTAINTY_HISTORY_APPENDED",
            "event_id": event_id,
            "uncertainty_id": uncertainty_id,
            "status": status,
            "event_digest": digest,
            "campaign_schema_changed": False,
            "semantic_recommendation_included": False,
            "semantic_truth_established": False,
            "explicit_limit": "Uncertainty history records agent-authored lifecycle state; it does not select or rank uncertainty.",
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(f"CAMPAIGN_UNCERTAINTY_HISTORY_APPENDED {event_id} {digest}")
            click.echo(payload["explicit_limit"])

    @campaign.command(name="uncertainty-history")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def campaign_uncertainty_history(workspace: Path, output_json: bool) -> None:
        """Inspect and validate append-only uncertainty lifecycle history."""
        try:
            result = UncertaintyHistoryService(workspace).load()
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        payload = {
            "ok": result.valid,
            "code": (
                "CAMPAIGN_UNCERTAINTY_HISTORY_VALID"
                if result.valid
                else "CAMPAIGN_UNCERTAINTY_HISTORY_INVALID"
            ),
            "campaign_id": result.campaign_id,
            "records": list(result.records),
            "latest_statuses": dict(result.latest_statuses),
            "diagnostics": [
                {"code": item.code, "detail": item.detail, "line": item.line}
                for item in result.diagnostics
            ],
            "campaign_schema_changed": False,
            "semantic_recommendation_included": False,
            "semantic_truth_established": False,
            "explicit_limit": "CampaignState.active_uncertainty remains current authority; history does not select or rank uncertainty.",
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        if not result.valid:
            raise click.exceptions.Exit(HISTORY_INVALID_EXIT)

    @campaign.command(name="doctor")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option(
        "--responsibility-type",
        default=None,
        help="Optional agent-supplied type for capability-catalog diagnostics; never inferred",
    )
    @click.option("--json", "output_json", is_flag=True)
    def campaign_doctor(
        workspace: Path,
        responsibility_type: str | None,
        output_json: bool,
    ) -> None:
        """Classify mechanical failures into deterministic diagnostic paths."""
        normalized_type = responsibility_type.strip() if responsibility_type else None
        if responsibility_type is not None and not normalized_type:
            raise click.ClickException("--responsibility-type must be non-empty when supplied")
        try:
            result = CampaignDoctorService(workspace).inspect(normalized_type)
        except CapabilityCatalogError as exc:
            raise click.ClickException(str(exc)) from exc
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        payload = doctor_payload(result)
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        if not result.clean:
            raise click.exceptions.Exit(OPERABILITY_INVALID_EXIT)

    @campaign.command(name="provenance")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option(
        "--format",
        "output_format",
        type=click.Choice(["json", "markdown"]),
        default="markdown",
        show_default=True,
    )
    def campaign_provenance(workspace: Path, output_format: str) -> None:
        """Render local Campaign provenance; never publish it to GitHub."""
        try:
            value = CampaignProvenanceService(workspace).inspect()
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=(output_format == "json"))
            return
        if output_format == "json":
            payload = provenance_payload(value)
            json_echo({"ok": True, "code": "CAMPAIGN_PROVENANCE", **payload})
        else:
            click.echo(render_provenance_markdown(value), nl=False)

    @campaign.command(name="graph-integrity")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def campaign_graph_integrity(workspace: Path, output_json: bool) -> None:
        """Validate mechanically reconstructible provenance graph integrity."""
        try:
            graph = CampaignProvenanceGraphService(workspace).build()
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        payload = {
            "ok": graph.valid,
            "code": "CAMPAIGN_GRAPH_INTEGRITY_VALID" if graph.valid else "CAMPAIGN_GRAPH_INTEGRITY_INVALID",
            "campaign_id": graph.campaign_id,
            "node_count": len(graph.nodes),
            "edge_count": len(graph.edges),
            "diagnostics": [
                {"code": item.code, "detail": item.detail}
                for item in graph.diagnostics
            ],
            "semantic_truth_established": False,
            "explicit_limit": "Graph integrity establishes recorded provenance structure only; it does not establish semantic causality or correctness.",
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        if not graph.valid:
            raise click.exceptions.Exit(OPERABILITY_INVALID_EXIT)
