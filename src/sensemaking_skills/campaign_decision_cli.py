"""Click command registration for explicit agent-authored campaign decisions."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from .campaign_semantics import (
    Authority,
    ContractError,
    Responsibility,
    TerminalState,
    canonicalize,
)
from .campaigns import CampaignService, CampaignSnapshot, CampaignWorkspaceError
from .campaigns.decisions import (
    AdvanceDecision,
    CampaignDecisionService,
    CloseDecision,
    DeferDecision,
)


ErrorEmitter = Callable[..., None]
StatusPayload = Callable[[CampaignSnapshot], dict[str, Any]]
JsonEcho = Callable[[dict[str, Any]], None]
StatusEcho = Callable[..., None]


def _emit_decision_success(
    snapshot: CampaignSnapshot,
    *,
    code: str,
    output_json: bool,
    status_payload: StatusPayload,
    json_echo: JsonEcho,
    echo_status: StatusEcho,
) -> None:
    transition = snapshot.transitions[-1]
    if output_json:
        payload = status_payload(snapshot)
        payload["code"] = code
        payload["state"] = canonicalize(snapshot.state)
        payload["transition"] = canonicalize(transition)
        json_echo(payload)
        return

    echo_status(snapshot, heading=code)
    click.echo(f"Transition: {transition.id}")
    click.echo(f"Decision: {transition.decision}")
    if transition.evidence:
        click.echo("Decision evidence:")
        for evidence in transition.evidence:
            click.echo(f"  - {evidence}")
    else:
        click.echo("Decision evidence: none")
    if code == "CAMPAIGN_DEFERRED" and snapshot.state.deferred_responsibilities:
        deferred = snapshot.state.deferred_responsibilities[-1]
        click.echo(f"Deferred responsibility: {deferred.responsibility_id}")
        click.echo(f"Reason: {deferred.reason}")
        if deferred.reopen_when:
            click.echo("Reopen when:")
            for condition in deferred.reopen_when:
                click.echo(f"  - {condition}")
        if deferred.not_reopened_by:
            click.echo("Not reopened by:")
            for condition in deferred.not_reopened_by:
                click.echo(f"  - {condition}")


def _next_generated_id(prefix: str, existing: set[str]) -> str:
    """Return the first deterministic generated identifier not already used."""
    for index in range(1, 10000):
        candidate = f"{prefix}-AUTO-{index:04d}"
        if candidate not in existing:
            return candidate
    raise click.ClickException(f"no generated {prefix} identifier is available")


def _generated_transition_id(snapshot: CampaignSnapshot) -> str:
    return _next_generated_id("TR", {item.id for item in snapshot.transitions})


def _generated_responsibility_id(snapshot: CampaignSnapshot) -> str:
    state = snapshot.state
    used: set[str] = set()
    if state.active_responsibility is not None:
        used.add(state.active_responsibility.id)
    for item in getattr(state, "additional_active_responsibilities", ()):
        used.add(item.id)
    for item in state.deferred_responsibilities:
        used.add(item.responsibility_id)
    return _next_generated_id("R", used)


def register_campaign_decision_commands(
    campaign: click.Group,
    *,
    emit_error: ErrorEmitter,
    status_payload: StatusPayload,
    json_echo: JsonEcho,
    echo_status: StatusEcho,
) -> None:
    """Register P5 commands on the existing campaign Click group."""

    @campaign.command(name="advance")
    @click.option(
        "--workspace",
        required=True,
        type=click.Path(path_type=Path),
        help="Existing campaign workspace",
    )
    @click.option("--transition-id", default=None, help="Optional transition identifier; generated deterministically when omitted")
    @click.option("--to-state", default=None, help="Optional durable target-state label; generated from the decision when omitted")
    @click.option(
        "--decision",
        required=True,
        help="Agent-authored rationale for advancing",
    )
    @click.option(
        "--evidence",
        multiple=True,
        help="Durable campaign evidence ref supporting this decision; repeatable. Include the authority-source ref when decision-critical.",
    )
    @click.option(
        "--responsibility-id",
        default=None,
        help="Optional responsibility identifier; generated deterministically when omitted",
    )
    @click.option(
        "--responsibility-statement",
        required=True,
        help="What the next responsibility requires",
    )
    @click.option(
        "--decision-blocked",
        required=True,
        help="Decision that remains blocked until this responsibility is resolved",
    )
    @click.option(
        "--scope",
        required=True,
        help="Explicit boundary of the next responsibility",
    )
    @click.option(
        "--authority",
        required=True,
        type=click.Choice([authority.value for authority in Authority]),
        help="Agent-reported authority classification for the next responsibility; this records but does not grant/enforce authority",
    )
    @click.option(
        "--success-condition",
        "success_conditions",
        multiple=True,
        required=True,
        help="Success/stop condition for the next responsibility; repeatable",
    )
    @click.option("--json", "output_json", is_flag=True, help="Emit JSON")
    def campaign_advance(
        workspace: Path,
        transition_id: str | None,
        to_state: str | None,
        decision: str,
        evidence: tuple[str, ...],
        responsibility_id: str | None,
        responsibility_statement: str,
        decision_blocked: str,
        scope: str,
        authority: str,
        success_conditions: tuple[str, ...],
        output_json: bool,
    ) -> None:
        """Persist an explicit agent decision to advance into one responsibility."""
        try:
            current = CampaignService(workspace).resume_for_transition()
            resolved_responsibility_id = (
                responsibility_id or _generated_responsibility_id(current)
            )
            resolved_transition_id = transition_id or _generated_transition_id(current)
            resolved_to_state = (
                to_state or f"responsibility_active_{resolved_responsibility_id}"
            )
            responsibility = Responsibility(
                id=resolved_responsibility_id,
                statement=responsibility_statement,
                trigger_evidence=tuple(evidence),
                decision_blocked=decision_blocked,
                scope=scope,
                authority=Authority(authority),
                success_conditions=tuple(success_conditions),
            )
            authored = AdvanceDecision(
                transition_id=resolved_transition_id,
                to_state=resolved_to_state,
                decision=decision,
                evidence=tuple(evidence),
                next_responsibility=responsibility,
            )
            snapshot = CampaignDecisionService(workspace).advance(authored)
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        _emit_decision_success(
            snapshot,
            code="CAMPAIGN_ADVANCED",
            output_json=output_json,
            status_payload=status_payload,
            json_echo=json_echo,
            echo_status=echo_status,
        )

    @campaign.command(name="defer")
    @click.option(
        "--workspace",
        required=True,
        type=click.Path(path_type=Path),
        help="Existing campaign workspace",
    )
    @click.option("--transition-id", default=None, help="Optional transition identifier; generated deterministically when omitted")
    @click.option("--to-state", default=None, help="Optional durable target-state label; generated when omitted")
    @click.option(
        "--decision",
        required=True,
        help="Agent-authored rationale for deferral",
    )
    @click.option("--reason", required=True, help="Why the responsibility is deferred")
    @click.option(
        "--reopen-when",
        multiple=True,
        help="Condition that can reopen this responsibility; repeatable",
    )
    @click.option(
        "--not-reopened-by",
        multiple=True,
        help="Condition that must not reopen this responsibility; repeatable",
    )
    @click.option(
        "--evidence",
        multiple=True,
        help="Durable campaign evidence ref supporting this decision; repeatable",
    )
    @click.option("--json", "output_json", is_flag=True, help="Emit JSON")
    def campaign_defer(
        workspace: Path,
        transition_id: str | None,
        to_state: str | None,
        decision: str,
        reason: str,
        reopen_when: tuple[str, ...],
        not_reopened_by: tuple[str, ...],
        evidence: tuple[str, ...],
        output_json: bool,
    ) -> None:
        """Persist an explicit agent decision to defer the active responsibility."""
        try:
            current = CampaignService(workspace).resume_for_transition()
            resolved_transition_id = transition_id or _generated_transition_id(current)
            active_id = (
                current.state.active_responsibility.id
                if current.state.active_responsibility is not None
                else "current"
            )
            resolved_to_state = to_state or f"responsibility_deferred_{active_id}"
            authored = DeferDecision(
                transition_id=resolved_transition_id,
                to_state=resolved_to_state,
                decision=decision,
                reason=reason,
                reopen_when=tuple(reopen_when),
                not_reopened_by=tuple(not_reopened_by),
                evidence=tuple(evidence),
            )
            snapshot = CampaignDecisionService(workspace).defer(authored)
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        _emit_decision_success(
            snapshot,
            code="CAMPAIGN_DEFERRED",
            output_json=output_json,
            status_payload=status_payload,
            json_echo=json_echo,
            echo_status=echo_status,
        )

    @campaign.command(name="close")
    @click.option(
        "--workspace",
        required=True,
        type=click.Path(path_type=Path),
        help="Existing campaign workspace",
    )
    @click.option("--transition-id", default=None, help="Optional transition identifier; generated deterministically when omitted")
    @click.option("--to-state", default=None, help="Optional durable terminal-state label; generated from --terminal-state when omitted")
    @click.option(
        "--decision",
        required=True,
        help="Agent-authored rationale for closure",
    )
    @click.option(
        "--terminal-state",
        required=True,
        type=click.Choice([terminal.value for terminal in TerminalState]),
        help="Explicit terminal classification",
    )
    @click.option(
        "--evidence",
        multiple=True,
        help="Durable campaign evidence ref supporting this decision; repeatable",
    )
    @click.option("--json", "output_json", is_flag=True, help="Emit JSON")
    def campaign_close(
        workspace: Path,
        transition_id: str | None,
        to_state: str | None,
        decision: str,
        terminal_state: str,
        evidence: tuple[str, ...],
        output_json: bool,
    ) -> None:
        """Persist an explicit agent decision to close the campaign."""
        try:
            current = CampaignService(workspace).resume_for_transition()
            resolved_transition_id = transition_id or _generated_transition_id(current)
            resolved_to_state = to_state or f"terminal_{terminal_state}"
            authored = CloseDecision(
                transition_id=resolved_transition_id,
                to_state=resolved_to_state,
                decision=decision,
                terminal_state=TerminalState(terminal_state),
                evidence=tuple(evidence),
            )
            snapshot = CampaignDecisionService(workspace).close(authored)
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        _emit_decision_success(
            snapshot,
            code="CAMPAIGN_CLOSED",
            output_json=output_json,
            status_payload=status_payload,
            json_echo=json_echo,
            echo_status=echo_status,
        )
