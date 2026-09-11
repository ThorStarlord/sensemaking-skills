"""CLI for explicit multi-repository Campaign target sets."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from .campaign_semantics import Authority, ContractError
from .campaigns import CampaignWorkspaceError
from .campaigns.multi_target import MultiTargetService
from .campaigns.multi_target_rebind import MultiTargetRebindService
from .campaigns.multi_target_relations import RELATION_TYPES, MultiTargetRelationService


ErrorEmitter = Callable[..., None]
JsonEcho = Callable[[dict[str, Any]], None]
INVALID_EXIT = 3


def _verification_payload(result: Any) -> dict[str, Any]:
    return {
        "ok": result.valid,
        "campaign_id": result.campaign_id,
        "target_set_sha256": result.target_set_sha256,
        "target_count": len(result.targets),
        "targets": list(result.targets),
        "diagnostics": [
            {"code": item.code, "detail": item.detail, "alias": item.alias}
            for item in result.diagnostics
        ],
        "semantic_truth_established": False,
        "semantic_recommendation_included": False,
        "explicit_limit": "Multi-target integrity verifies recorded repository identity/state only; it does not establish cross-repository semantic correctness or atomicity.",
    }


def _relations_payload(result: Any, *, code: str) -> dict[str, Any]:
    return {
        "ok": result.valid,
        "code": code,
        "campaign_id": result.campaign_id,
        "relation_count": len(result.relations),
        "relations": list(result.relations),
        "ordering_cycles": [list(item) for item in result.ordering_cycles],
        "diagnostics": [
            {
                "code": item.code,
                "detail": item.detail,
                "relation_id": item.relation_id,
                "line_number": item.line_number,
            }
            for item in result.diagnostics
        ],
        "semantic_truth_established": False,
        "semantic_recommendation_included": False,
        "explicit_limit": "Cross-repository relations are caller-authored declarations. Mechanical validity does not establish architectural truth, execution order, or authorization.",
    }


def _relations_mermaid(graph: dict[str, Any]) -> str:
    lines = ["flowchart LR"]
    for node in graph["nodes"]:
        safe = str(node).replace('"', "'")
        lines.append(f'    {node}["{safe}"]')
    for edge in graph["edges"]:
        relation = str(edge["type"])
        lines.append(f'    {edge["source"]} -->|"{relation}"| {edge["target"]}')
    return "\n".join(lines)


def register_campaign_multi_target_commands(
    campaign: click.Group,
    *,
    emit_error: ErrorEmitter,
    json_echo: JsonEcho,
) -> None:
    @campaign.group(name="multi-target")
    def multi_target_group() -> None:
        """Operate an explicit multi-repository target-set companion."""

    @multi_target_group.command(name="add")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--alias", required=True)
    @click.option("--target-repo", required=True, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--role", required=True, help="Explicit role of this repository in the responsibility")
    @click.option("--authority", required=True, type=click.Choice([item.value for item in Authority]))
    @click.option("--evidence-ref", "evidence_refs", multiple=True)
    @click.option("--json", "output_json", is_flag=True)
    def multi_target_add(
        workspace: Path,
        alias: str,
        target_repo: Path,
        role: str,
        authority: str,
        evidence_refs: tuple[str, ...],
        output_json: bool,
    ) -> None:
        """Bind one explicitly selected repository target by exact snapshot."""
        try:
            digest = MultiTargetService(workspace).add(
                alias=alias,
                target_repo=target_repo,
                role=role,
                authority=Authority(authority),
                evidence_refs=evidence_refs,
            )
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
        payload = {
            "ok": True,
            "code": "CAMPAIGN_MULTI_TARGET_ADDED",
            "alias": alias,
            "target_set_sha256": digest,
            "repository_selection_performed": False,
            "semantic_truth_established": False,
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))

    @multi_target_group.command(name="inspect")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def multi_target_inspect(workspace: Path, output_json: bool) -> None:
        """Inspect exact target-set metadata without checking live drift."""
        try:
            result = MultiTargetService(workspace).inspect()
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        payload = {"code": "CAMPAIGN_MULTI_TARGET_INSPECT", **_verification_payload(result)}
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        if not result.valid:
            raise click.exceptions.Exit(INVALID_EXIT)

    @multi_target_group.command(name="verify")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--alias", default=None, help="Optional exact alias; omit to verify all targets")
    @click.option("--json", "output_json", is_flag=True)
    def multi_target_verify(workspace: Path, alias: str | None, output_json: bool) -> None:
        """Detect live identity/state drift for recorded repository targets."""
        try:
            result = MultiTargetService(workspace).verify(alias)
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
        payload = {"code": "CAMPAIGN_MULTI_TARGET_VALID" if result.valid else "CAMPAIGN_MULTI_TARGET_INVALID", **_verification_payload(result)}
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        if not result.valid:
            raise click.exceptions.Exit(INVALID_EXIT)

    @multi_target_group.command(name="refresh")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--alias", required=True, help="Explicit target alias whose new live snapshot should be recorded")
    @click.option("--json", "output_json", is_flag=True)
    def multi_target_refresh(workspace: Path, alias: str, output_json: bool) -> None:
        """Record a new snapshot for one explicit target after authorized work."""
        try:
            result = MultiTargetService(workspace).refresh(alias)
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
        payload = {
            "ok": True,
            "code": "CAMPAIGN_MULTI_TARGET_REFRESHED",
            **result,
            "refresh_selected_by_tool": False,
            "semantic_recommendation_included": False,
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))

    @multi_target_group.command(name="rebind")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--alias", required=True, help="Exact existing target alias selected by the caller")
    @click.option("--target-repo", required=True, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def multi_target_rebind(workspace: Path, alias: str, target_repo: Path, output_json: bool) -> None:
        """Rebind one explicit target alias to an equivalent local repository path."""
        try:
            result = MultiTargetRebindService(workspace).rebind(alias=alias, target_repo=target_repo)
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
        payload = {
            "ok": True,
            "code": "CAMPAIGN_MULTI_TARGET_REBOUND",
            **result,
            "rebind_selected_by_tool": False,
            "semantic_recommendation_included": False,
            "explicit_limit": "Multi-target rebind accepts an exact caller-selected alias/path and verifies identity/state; it does not discover repositories or refresh changed target state.",
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))

    @multi_target_group.command(name="relate")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--relation-id", required=True)
    @click.option("--source-alias", required=True)
    @click.option("--target-alias", required=True)
    @click.option("--relation-type", required=True, type=click.Choice(RELATION_TYPES))
    @click.option("--evidence-ref", "evidence_refs", multiple=True)
    @click.option("--json", "output_json", is_flag=True)
    def multi_target_relate(
        workspace: Path,
        relation_id: str,
        source_alias: str,
        target_alias: str,
        relation_type: str,
        evidence_refs: tuple[str, ...],
        output_json: bool,
    ) -> None:
        """Append one explicit caller-authored relation between existing aliases."""
        try:
            digest = MultiTargetRelationService(workspace).append(
                relation_id=relation_id,
                source_alias=source_alias,
                target_alias=target_alias,
                relation_type=relation_type,
                evidence_refs=evidence_refs,
            )
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
        payload = {
            "ok": True,
            "code": "CAMPAIGN_MULTI_TARGET_RELATION_APPENDED",
            "relation_id": relation_id,
            "record_digest": digest,
            "relation_selected_by_tool": False,
            "semantic_truth_established": False,
            "semantic_recommendation_included": False,
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))

    @multi_target_group.command(name="dependency-check")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def multi_target_dependency_check(workspace: Path, output_json: bool) -> None:
        """Validate relation identities, hash chain, evidence, aliases, and ordering cycles."""
        try:
            result = MultiTargetRelationService(workspace).inspect()
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        payload = _relations_payload(
            result,
            code=("CAMPAIGN_MULTI_TARGET_DEPENDENCIES_VALID" if result.valid else "CAMPAIGN_MULTI_TARGET_DEPENDENCIES_INVALID"),
        )
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        if not result.valid:
            raise click.exceptions.Exit(INVALID_EXIT)

    @multi_target_group.command(name="graph")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--format", "output_format", type=click.Choice(["json", "mermaid"]), default="json", show_default=True)
    def multi_target_graph(workspace: Path, output_format: str) -> None:
        """Render explicit target relationships without inferring architecture."""
        try:
            graph = MultiTargetRelationService(workspace).graph()
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=(output_format == "json"))
            return
        if output_format == "mermaid":
            click.echo(_relations_mermaid(graph))
        else:
            json_echo({"ok": graph["valid"], "code": "CAMPAIGN_MULTI_TARGET_GRAPH", **graph})
        if not graph["valid"]:
            raise click.exceptions.Exit(INVALID_EXIT)
