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
from .campaigns import CampaignSnapshot, CampaignWorkspaceError
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
    @click.option("--transition-id", required=True, help="Unique transition identifier")
    @click.option("--to-state", required=True, help="Explicit durable target-state label")
    @click.option(
        "--decision",
        required=True,
        help="Agent-authored rationale for advancing",
    )
    @click.option(
        "--evidence",
        multiple=True,
        help="Durable campaign evidence ref supporting this decision; repeatable",
    )
    @click.option(
        "--responsibility-id",
        required=True,
        help="Agent-authored identifier for the next responsibility",
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
        help="Authority classification for the next responsibility",
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
        transition_id: str,
        to_state: str,
        decision: str,
        evidence: tuple[str, ...],
        responsibility_id: str,
        responsibility_statement: str,
        decision_blocked: str,
        scope: str,
        authority: str,
        success_conditions: tuple[str, ...],
        output_json: bool,
    ) -> None:
        """Persist an explicit agent decision to advance into one responsibility."""
        responsibility = Responsibility(
            id=responsibility_id,
            statement=responsibility_statement,
            trigger_evidence=tuple(evidence),
            decision_blocked=decision_blocked,
            scope=scope,
            authority=Authority(authority),
            success_conditions=tuple(success_conditions),
        )
        authored = AdvanceDecision(
            transition_id=transition_id,
            to_state=to_state,
            decision=decision,
            evidence=tuple(evidence),
            next_responsibility=responsibility,
        )
        try:
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
    @click.option("--transition-id", required=True, help="Unique transition identifier")
    @click.option("--to-state", required=True, help="Explicit durable target-state label")
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
        transition_id: str,
        to_state: str,
        decision: str,
        reason: str,
        reopen_when: tuple[str, ...],
        not_reopened_by: tuple[str, ...],
        evidence: tuple[str, ...],
        output_json: bool,
    ) -> None:
        """Persist an explicit agent decision to defer the active responsibility."""
        authored = DeferDecision(
            transition_id=transition_id,
            to_state=to_state,
            decision=decision,
            reason=reason,
            reopen_when=tuple(reopen_when),
            not_reopened_by=tuple(not_reopened_by),
            evidence=tuple(evidence),
        )
        try:
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
    @click.option("--transition-id", required=True, help="Unique transition identifier")
    @click.option("--to-state", required=True, help="Explicit durable terminal-state label")
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
        transition_id: str,
        to_state: str,
        decision: str,
        terminal_state: str,
        evidence: tuple[str, ...],
        output_json: bool,
    ) -> None:
        """Persist an explicit agent decision to close the campaign."""
        authored = CloseDecision(
            transition_id=transition_id,
            to_state=to_state,
            decision=decision,
            terminal_state=TerminalState(terminal_state),
            evidence=tuple(evidence),
        )
        try:
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
