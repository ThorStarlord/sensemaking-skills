"""Click registration for P8 read-only Campaign artifact/evidence lineage."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from .campaign_semantics import ContractError
from .campaigns import CampaignWorkspaceError
from .campaigns.lineage import (
    CampaignLineageResult,
    CampaignLineageService,
    ConsumptionEdge,
    LineageEvidence,
    TransitionLineage,
)


ErrorEmitter = Callable[..., None]
JsonEcho = Callable[[dict[str, Any]], None]


def _evidence_payload(item: LineageEvidence) -> dict[str, Any]:
    return {
        "ref": item.ref,
        "kind": item.kind,
        "current_sha256": item.current_sha256,
        "immutable_by_source_contract": item.immutable_by_source_contract,
        "provenance": dict(item.provenance),
    }


def _transition_payload(item: TransitionLineage) -> dict[str, Any]:
    return {
        "transition_id": item.transition_id,
        "transition_digest": item.transition_digest,
        "evidence_refs": list(item.evidence_refs),
        "binding_status": item.binding_status,
        "receipt_ref": item.receipt_ref,
    }


def _edge_payload(item: ConsumptionEdge) -> dict[str, Any]:
    return {
        "transition_id": item.transition_id,
        "transition_digest": item.transition_digest,
        "evidence_ref": item.evidence_ref,
        "binding_status": item.binding_status,
        "consumed_sha256": item.consumed_sha256,
        "immutable_ref": item.immutable_ref,
        "source_matches_consumed_bytes": item.source_matches_consumed_bytes,
        "kind": item.kind,
        "provenance": dict(item.provenance),
    }


def _payload(result: CampaignLineageResult) -> dict[str, Any]:
    return {
        "ok": True,
        "code": "CAMPAIGN_LINEAGE",
        "campaign_id": result.campaign_id,
        "evidence_count": len(result.evidence),
        "transition_count": len(result.transitions),
        "consumption_edge_count": len(result.consumption_edges),
        "evidence": [_evidence_payload(item) for item in result.evidence],
        "transitions": [_transition_payload(item) for item in result.transitions],
        "consumption_edges": [_edge_payload(item) for item in result.consumption_edges],
        "orphan_intent_refs": list(result.orphan_intent_refs),
    }


def register_campaign_lineage_commands(
    campaign: click.Group,
    *,
    emit_error: ErrorEmitter,
    json_echo: JsonEcho,
) -> None:
    """Register deterministic P8 lineage inspection on the Campaign group."""

    @campaign.command(name="lineage")
    @click.option(
        "--workspace",
        required=True,
        type=click.Path(path_type=Path),
        help="Existing Campaign workspace",
    )
    @click.option("--json", "output_json", is_flag=True, help="Emit JSON")
    def campaign_lineage(workspace: Path, output_json: bool) -> None:
        """Show evidence identity/provenance and explicit transition consumption."""
        try:
            result = CampaignLineageService(workspace).inspect()
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return

        payload = _payload(result)
        if output_json:
            json_echo(payload)
            return

        click.echo("CAMPAIGN_LINEAGE")
        click.echo(f"Campaign: {result.campaign_id}")
        click.echo(f"Evidence records: {len(result.evidence)}")
        click.echo(f"Transitions: {len(result.transitions)}")
        click.echo(f"Consumption edges: {len(result.consumption_edges)}")
        if result.orphan_intent_refs:
            click.echo(f"Orphan precommit intents: {len(result.orphan_intent_refs)}")

        for transition in result.transitions:
            click.echo()
            click.echo(f"Transition: {transition.transition_id}")
            click.echo(f"  Digest: {transition.transition_digest}")
            click.echo(f"  Lineage binding: {transition.binding_status}")
            click.echo(f"  Receipt: {transition.receipt_ref or 'none'}")
            matching = [
                edge
                for edge in result.consumption_edges
                if edge.transition_id == transition.transition_id
            ]
            if not matching:
                click.echo("  Evidence consumed: none")
                continue
            click.echo("  Evidence consumed:")
            for edge in matching:
                digest = edge.consumed_sha256 or "legacy-unbound"
                immutable = edge.immutable_ref or "none"
                click.echo(f"    - {edge.evidence_ref}")
                click.echo(f"      kind: {edge.kind or 'unknown'}")
                click.echo(f"      consumed SHA-256: {digest}")
                click.echo(f"      immutable ref: {immutable}")
                if edge.source_matches_consumed_bytes is not None:
                    click.echo(
                        "      source still matches consumed bytes: "
                        + ("yes" if edge.source_matches_consumed_bytes else "no")
                    )

        click.echo()
        click.echo(
            "Lineage records identity/provenance and explicit consumption only; "
            "it does not establish semantic sufficiency, recommendation, or authority."
        )
