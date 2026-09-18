"""CLI for explicit Campaign execution handoff/result companions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import click

from .campaign_semantics import ContractError
from .campaigns import CampaignWorkspaceError
from .campaigns.execution import CampaignExecutionService


ErrorEmitter = Callable[..., None]
JsonEcho = Callable[[dict[str, Any]], None]


def _inspection_payload(service: CampaignExecutionService) -> dict[str, Any]:
    result = service.inspect()
    return {
        "ok": result.valid,
        "code": (
            "CAMPAIGN_EXECUTION_COMPANION_VALID"
            if result.valid
            else "CAMPAIGN_EXECUTION_COMPANION_INVALID"
        ),
        "campaign_id": result.campaign_id,
        "handoffs": list(result.handoffs),
        "results": list(result.results),
        "handoff_count": len(result.handoffs),
        "result_count": len(result.results),
        "diagnostics": [
            {
                "code": item.code,
                "detail": item.detail,
                "record_id": item.record_id,
                "line_number": item.line_number,
            }
            for item in result.diagnostics
        ],
        "semantic_truth_established": False,
        "explicit_limit": (
            "Execution companion integrity does not establish that delegated work "
            "was warranted, correctly executed, or sufficient for Campaign closure."
        ),
    }


def register_campaign_execution_commands(
    campaign: click.Group,
    *,
    emit_error: ErrorEmitter,
    json_echo: JsonEcho,
) -> None:
    @campaign.group(name="execution")
    def execution_group() -> None:
        """Bind selected work to external execution and returned evidence."""

    @execution_group.command(name="handoff")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--handoff-id", required=True)
    @click.option("--executor-kind", required=True)
    @click.option(
        "--evidence-requirement",
        "evidence_requirements",
        multiple=True,
        required=True,
        help="Explicit evidence the worker must return; repeat as needed.",
    )
    @click.option(
        "--forbidden-action",
        "forbidden_actions",
        multiple=True,
        help="Explicit action outside this delegation; repeat as needed.",
    )
    @click.option("--json", "output_json", is_flag=True)
    def execution_handoff(
        workspace: Path,
        handoff_id: str,
        executor_kind: str,
        evidence_requirements: tuple[str, ...],
        forbidden_actions: tuple[str, ...],
        output_json: bool,
    ) -> None:
        """Create a mechanical handoff from the already-selected responsibility."""
        try:
            service = CampaignExecutionService(workspace)
            digest = service.create_handoff(
                handoff_id=handoff_id,
                executor_kind=executor_kind,
                evidence_requirements=evidence_requirements,
                forbidden_actions=forbidden_actions,
            )
            inspected = service.inspect()
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        except (OSError, ValueError) as exc:
            raise click.ClickException(str(exc)) from exc

        record = next(
            item for item in inspected.handoffs if item["handoff_id"] == handoff_id
        )
        payload = {
            "ok": True,
            "code": "CAMPAIGN_EXECUTION_HANDOFF_RECORDED",
            "handoff": record,
            "record_digest": digest,
            "selection_performed_by_tool": False,
            "authorization_granted_by_tool": False,
            "global_closure_established": False,
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))

    @execution_group.command(name="result")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--result-id", required=True)
    @click.option("--handoff-id", required=True)
    @click.option("--worker", required=True)
    @click.option("--source-before", required=True)
    @click.option("--source-after", required=True)
    @click.option("--changed-path", "changed_paths", multiple=True)
    @click.option("--validation", "validations", multiple=True)
    @click.option("--evidence-ref", "evidence_refs", multiple=True)
    @click.option(
        "--unresolved-uncertainty",
        "unresolved_uncertainties",
        multiple=True,
    )
    @click.option("--claim-supported", "claims_supported", multiple=True)
    @click.option("--claim-not-supported", "claims_not_supported", multiple=True)
    @click.option(
        "--authority-exceeded",
        type=click.Choice(["yes", "no"]),
        required=True,
        help="Worker-reported fact; the tool does not infer it.",
    )
    @click.option("--json", "output_json", is_flag=True)
    def execution_result(
        workspace: Path,
        result_id: str,
        handoff_id: str,
        worker: str,
        source_before: str,
        source_after: str,
        changed_paths: tuple[str, ...],
        validations: tuple[str, ...],
        evidence_refs: tuple[str, ...],
        unresolved_uncertainties: tuple[str, ...],
        claims_supported: tuple[str, ...],
        claims_not_supported: tuple[str, ...],
        authority_exceeded: str,
        output_json: bool,
    ) -> None:
        """Record a worker return without treating worker success as closure."""
        try:
            service = CampaignExecutionService(workspace)
            digest = service.record_result(
                result_id=result_id,
                handoff_id=handoff_id,
                worker=worker,
                source_before=source_before,
                source_after=source_after,
                changed_paths=changed_paths,
                validations=validations,
                evidence_refs=evidence_refs,
                unresolved_uncertainties=unresolved_uncertainties,
                claims_supported=claims_supported,
                claims_not_supported=claims_not_supported,
                authority_exceeded=(authority_exceeded == "yes"),
            )
            inspected = service.inspect()
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        except (OSError, ValueError) as exc:
            raise click.ClickException(str(exc)) from exc

        record = next(
            item for item in inspected.results if item["result_id"] == result_id
        )
        payload = {
            "ok": True,
            "code": "CAMPAIGN_EXECUTION_RESULT_RECORDED",
            "result": record,
            "record_digest": digest,
            "campaign_evidence_admitted": False,
            "worker_completion_establishes_global_closure": False,
            "parent_reassessment_required": True,
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))

    @execution_group.command(name="inspect")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def execution_inspect(workspace: Path, output_json: bool) -> None:
        """Inspect execution companion integrity and exact recorded returns."""
        try:
            payload = _inspection_payload(CampaignExecutionService(workspace))
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        if not payload["ok"]:
            raise click.exceptions.Exit(3)

    @campaign.command(name="working-context")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def campaign_working_context(workspace: Path, output_json: bool) -> None:
        """Project compact high-delegation context without selecting a next action."""
        try:
            context = CampaignExecutionService(workspace).working_context()
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
        payload = {
            "ok": context["execution_companion_valid"],
            "code": "CAMPAIGN_WORKING_CONTEXT",
            **context,
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        if not payload["ok"]:
            raise click.exceptions.Exit(3)
