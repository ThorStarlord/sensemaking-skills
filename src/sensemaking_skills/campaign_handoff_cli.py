"""Click command registration for P7 durable handoff/resume UX."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from .campaign_semantics import ContractError, TerminalState, canonicalize
from .campaigns import CampaignWorkspaceError
from .campaigns.handoff import CampaignHandoffService, CampaignResumeEnvelope


ErrorEmitter = Callable[..., None]
JsonEcho = Callable[[dict[str, Any]], None]


def _resume_payload(result: CampaignResumeEnvelope, *, code: str) -> dict[str, Any]:
    snapshot = result.snapshot
    return {
        "ok": True,
        "code": code,
        "campaign_id": snapshot.state.campaign_id,
        "handoff_ref": result.handoff_ref,
        "reconstruction_sha256": result.reconstruction_sha256,
        "state": canonicalize(snapshot.state),
        "transitions": [canonicalize(item) for item in snapshot.transitions],
        "trace": canonicalize(snapshot.trace),
        "evidence_refs": list(snapshot.evidence_refs),
        "policy": canonicalize(snapshot.policy) if snapshot.policy is not None else None,
        "handoff": canonicalize(result.handoff),
    }


def _echo_resume(result: CampaignResumeEnvelope, *, heading: str) -> None:
    state = result.snapshot.state
    click.echo(heading)
    click.echo(f"Campaign: {state.campaign_id}")
    click.echo(f"Status: {state.status}")
    click.echo(f"Current state: {state.current_state}")
    click.echo(
        "Authority: "
        + (state.authority.value if state.authority is not None else "none")
    )
    click.echo(
        "Terminal state: "
        + (state.terminal_state.value if state.terminal_state is not None else "none")
    )
    if state.active_responsibility is None:
        click.echo("Active responsibility: none")
    else:
        click.echo(
            f"Active responsibility: {state.active_responsibility.id} — "
            f"{state.active_responsibility.statement}"
        )
    click.echo(f"Transitions: {len(result.snapshot.transitions)}")
    click.echo(f"Evidence refs: {len(result.snapshot.evidence_refs)}")
    click.echo(f"Handoff: {result.handoff_ref}")
    click.echo(f"Reconstruction SHA-256: {result.reconstruction_sha256}")
    click.echo("Handoff-declared next actions are context only, not execution authority:")
    if result.handoff.allowed_next_actions:
        for action in result.handoff.allowed_next_actions:
            click.echo(f"  - {action}")
    else:
        click.echo("  none")
    click.echo("Handoff stop conditions:")
    if result.handoff.stop_conditions:
        for condition in result.handoff.stop_conditions:
            click.echo(f"  - {condition.value}")
    else:
        click.echo("  none")


def register_campaign_handoff_commands(
    campaign: click.Group,
    *,
    emit_error: ErrorEmitter,
    json_echo: JsonEcho,
) -> None:
    """Register P7 handoff creation and fresh-context resume commands."""

    terminal_values = [item.value for item in TerminalState]

    @campaign.command(name="handoff")
    @click.option(
        "--workspace",
        required=True,
        type=click.Path(path_type=Path),
        help="Existing campaign workspace to hand to a fresh agent/process",
    )
    @click.option(
        "--allowed-next-action",
        "allowed_next_actions",
        multiple=True,
        help=(
            "Explicit agent-authored context for a possible next action; repeatable. "
            "No action is inferred or authorized by this field."
        ),
    )
    @click.option(
        "--stop-condition",
        "stop_conditions",
        multiple=True,
        type=click.Choice(terminal_values, case_sensitive=True),
        help="Explicit terminal condition to preserve in the handoff; repeatable",
    )
    @click.option("--json", "output_json", is_flag=True, help="Emit JSON")
    def campaign_handoff(
        workspace: Path,
        allowed_next_actions: tuple[str, ...],
        stop_conditions: tuple[str, ...],
        output_json: bool,
    ) -> None:
        """Write an integrity-bound handoff from the exact current campaign."""
        try:
            result = CampaignHandoffService(workspace).create(
                allowed_next_actions=allowed_next_actions,
                stop_conditions=tuple(TerminalState(item) for item in stop_conditions),
            )
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return

        if output_json:
            json_echo(_resume_payload(result, code="CAMPAIGN_HANDOFF_WRITTEN"))
            return
        _echo_resume(result, heading="CAMPAIGN_HANDOFF_WRITTEN")

    @campaign.command(name="resume")
    @click.option(
        "--workspace",
        required=True,
        type=click.Path(path_type=Path),
        help="Existing campaign workspace containing a current P7-bound handoff",
    )
    @click.option("--json", "output_json", is_flag=True, help="Emit JSON")
    def campaign_resume(workspace: Path, output_json: bool) -> None:
        """Reconstruct exact durable context for a fresh agent/process."""
        try:
            result = CampaignHandoffService(workspace).resume()
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return

        if output_json:
            json_echo(_resume_payload(result, code="CAMPAIGN_RESUMED"))
            return
        _echo_resume(result, heading="CAMPAIGN_RESUMED")
