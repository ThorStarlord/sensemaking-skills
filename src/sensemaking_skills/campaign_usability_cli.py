"""Campaign usability/composition surfaces built from existing mechanical authority."""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from .campaign_semantics import ContractError, canonicalize
from .campaigns import CampaignService, CampaignWorkspaceError
from .campaigns.bundle_inspection import (
    CampaignBundleInspectionError,
    inspect_bundle,
    verified_bundle_workspace,
)
from .campaigns.inventory import inspect_campaign_root, inventory_payload
from .campaigns.provenance_graph import CampaignProvenanceGraphService
from .campaigns.resume_capsule import RESUME_PROFILES, build_resume_capsule
from .campaigns.uncertainty_relations import RELATION_TYPES, UncertaintyRelationService
from .semantic_architecture import SemanticStateStore


ErrorEmitter = Callable[..., None]
JsonEcho = Callable[[dict[str, Any]], None]
INVALID_EXIT = 3


def _semantic_summary(workspace: Path) -> dict[str, Any]:
    path = workspace / "semantic-state.jsonl"
    records, diagnostics = SemanticStateStore(path).load_raw()
    return {
        "present": bool(records) or path.exists(),
        "valid": not diagnostics,
        "entry_count": len(records),
        "latest_entry": records[-1]["entry"] if records else None,
        "diagnostics": [canonicalize(item) for item in diagnostics],
        "schema_in_campaign_state": False,
        "semantic_truth_established": False,
    }


def _mermaid_id(value: str) -> str:
    return "N_" + re.sub(r"[^A-Za-z0-9_]", "_", value)


def register_campaign_usability_commands(
    campaign: click.Group,
    *,
    emit_error: ErrorEmitter,
    json_echo: JsonEcho,
) -> None:
    @campaign.command(name="uncertainty-relate")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--relation-id", required=True)
    @click.option("--uncertainty-id", required=True, help="Explicit source uncertainty id")
    @click.option("--relation", "relation_type", required=True, type=click.Choice(sorted(RELATION_TYPES)))
    @click.option("--target", "target_ref", required=True, help="Explicit uncertainty/transition/decision ref")
    @click.option("--evidence-ref", "evidence_refs", multiple=True)
    @click.option("--note", default=None)
    @click.option("--json", "output_json", is_flag=True)
    def uncertainty_relate(
        workspace: Path,
        relation_id: str,
        uncertainty_id: str,
        relation_type: str,
        target_ref: str,
        evidence_refs: tuple[str, ...],
        note: str | None,
        output_json: bool,
    ) -> None:
        """Record one explicit uncertainty relationship; never rank uncertainties."""
        try:
            digest = UncertaintyRelationService(workspace).append(
                relation_id=relation_id,
                source_uncertainty_id=uncertainty_id,
                relation_type=relation_type,
                target_ref=target_ref,
                evidence_refs=evidence_refs,
                note=note,
            )
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
        payload = {
            "ok": True,
            "code": "CAMPAIGN_UNCERTAINTY_RELATION_APPENDED",
            "relation_id": relation_id,
            "relation_digest": digest,
            "semantic_ranking_performed": False,
            "semantic_recommendation_included": False,
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))

    @campaign.command(name="uncertainty-show")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.argument("uncertainty_id")
    @click.option("--json", "output_json", is_flag=True)
    def uncertainty_show(workspace: Path, uncertainty_id: str, output_json: bool) -> None:
        """Show deterministic lifecycle/relationship context for one uncertainty id."""
        try:
            payload = UncertaintyRelationService(workspace).show(uncertainty_id)
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
        payload = {"ok": bool(payload["found"]), "code": "CAMPAIGN_UNCERTAINTY_SHOWN" if payload["found"] else "CAMPAIGN_UNCERTAINTY_NOT_FOUND", **payload}
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        if not payload["found"]:
            raise click.exceptions.Exit(2)
        if not payload["history_valid"] or not payload["relations_valid"]:
            raise click.exceptions.Exit(INVALID_EXIT)

    @campaign.command(name="uncertainty-graph")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--format", "output_format", type=click.Choice(["json", "mermaid"]), default="json", show_default=True)
    def uncertainty_graph(workspace: Path, output_format: str) -> None:
        """Render explicitly recorded uncertainty relationships without ranking."""
        try:
            payload = UncertaintyRelationService(workspace).graph()
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=(output_format == "json"))
            return
        if output_format == "json":
            json_echo({"code": "CAMPAIGN_UNCERTAINTY_GRAPH", **payload})
        else:
            if not payload["ok"]:
                raise click.ClickException("uncertainty relation/history integrity is invalid")
            click.echo("graph TD")
            for node in payload["nodes"]:
                click.echo(f'  {_mermaid_id(node["id"])}["{node["label"].replace(chr(34), chr(39))}"]')
            for edge in payload["edges"]:
                click.echo(f'  {_mermaid_id(edge["from"])} -->|{edge["relation"]}| {_mermaid_id(edge["to"])}')
        if not payload["ok"]:
            raise click.exceptions.Exit(INVALID_EXIT)

    @campaign.command(name="bundle-inspect")
    @click.option("--bundle", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def bundle_inspect(bundle: Path, output_json: bool) -> None:
        """Inspect verified bundle metadata without importing it into a user workspace."""
        payload = {"code": "CAMPAIGN_BUNDLE_INSPECT", **inspect_bundle(bundle)}
        payload["ok"] = bool(payload["valid"])
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        if not payload["valid"]:
            raise click.exceptions.Exit(INVALID_EXIT)

    @campaign.command(name="bundle-resume-context")
    @click.option("--bundle", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
    @click.option("--profile", type=click.Choice(list(RESUME_PROFILES)), default="working", show_default=True)
    @click.option("--recent-transitions", type=click.IntRange(0, 50), default=5, show_default=True)
    @click.option("--max-items", type=click.IntRange(1, 1000), default=None)
    @click.option("--json", "output_json", is_flag=True)
    def bundle_resume_context(bundle: Path, profile: str, recent_transitions: int, max_items: int | None, output_json: bool) -> None:
        """Project Resume Capsule v2 from verified bundle bytes before durable import."""
        try:
            with verified_bundle_workspace(bundle) as workspace:
                snapshot = CampaignService(workspace).resume()
                payload = build_resume_capsule(
                    workspace=workspace,
                    snapshot=snapshot,
                    semantic_summary=_semantic_summary(workspace),
                    recent_transitions=recent_transitions,
                    compact=False,
                    include_preflight=False,
                    profile=profile,
                    max_items=max_items,
                )
        except CampaignBundleInspectionError as exc:
            raise click.ClickException(str(exc)) from exc
        payload["source"] = "verified_bundle_ephemeral_projection"
        payload["durable_import_performed"] = False
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))

    @campaign.command(name="bundle-graph")
    @click.option("--bundle", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def bundle_graph(bundle: Path, output_json: bool) -> None:
        """Build provenance graph from verified bundle bytes before durable import."""
        try:
            with verified_bundle_workspace(bundle) as workspace:
                graph = CampaignProvenanceGraphService(workspace).build()
        except CampaignBundleInspectionError as exc:
            raise click.ClickException(str(exc)) from exc
        payload = {
            "ok": graph.valid,
            "code": "CAMPAIGN_BUNDLE_GRAPH",
            "campaign_id": graph.campaign_id,
            "nodes": list(graph.nodes),
            "edges": list(graph.edges),
            "diagnostics": [{"code": item.code, "detail": item.detail} for item in graph.diagnostics],
            "durable_import_performed": False,
            "semantic_truth_established": False,
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        if not graph.valid:
            raise click.exceptions.Exit(INVALID_EXIT)

    @campaign.command(name="inventory")
    @click.option("--root", required=True, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--include-archived", is_flag=True, help="Include Campaigns carrying a valid archive marker")
    @click.option("--json", "output_json", is_flag=True)
    def campaign_inventory(root: Path, include_archived: bool, output_json: bool) -> None:
        """List Campaign workspaces and mechanical health without prioritization."""
        try:
            entries = inspect_campaign_root(root, include_archived=include_archived)
            payload = inventory_payload(entries)
            payload["include_archived"] = include_archived
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
