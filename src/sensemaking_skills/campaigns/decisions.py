"""Typed agent-authored campaign decisions layered on the P2 lifecycle service.

This module packages semantic decisions supplied by the active coding agent and
translates them into the existing deterministic ``CampaignService`` lifecycle
operations. It does not inspect artifact contents, infer responsibility, rank
capabilities, or decide whether a campaign should advance, defer, or close.

P8 adds a mechanical precommit lineage step. Before the existing P2 lifecycle
primitive commits an authored decision, the exact supplied evidence refs are
bound to immutable identities. The lineage intent does not authorize or justify
the decision; it only preserves what bytes the agent explicitly cited.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path

from sensemaking_skills.campaign_semantics import (
    Responsibility,
    TerminalState,
    TransitionRecord,
)

from .errors import CampaignTransactionError
from .lineage import CampaignLineageService
from .service import CampaignService, CampaignSnapshot


@dataclass(frozen=True)
class AdvanceDecision:
    """Agent-authored instruction to advance into one explicit responsibility."""

    transition_id: str
    to_state: str
    decision: str
    next_responsibility: Responsibility
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class DeferDecision:
    """Agent-authored instruction to defer the current active responsibility."""

    transition_id: str
    to_state: str
    decision: str
    reason: str
    reopen_when: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()
    not_reopened_by: tuple[str, ...] = ()


@dataclass(frozen=True)
class CloseDecision:
    """Agent-authored instruction to enter one explicit terminal state."""

    transition_id: str
    to_state: str
    decision: str
    terminal_state: TerminalState
    evidence: tuple[str, ...] = ()


def _require_text(value: str, *, field: str) -> None:
    if not value.strip():
        raise CampaignTransactionError(f"{field} must be non-empty")


class CampaignDecisionService:
    """Persist explicit agent decisions without making those decisions itself."""

    def __init__(
        self,
        workspace: str | Path,
        *,
        target_repo: str | Path | None = None,
    ) -> None:
        self.lifecycle = CampaignService(workspace, target_repo=target_repo)
        self.lineage = CampaignLineageService(workspace)

    def advance(self, authored: AdvanceDecision) -> CampaignSnapshot:
        """Advance using the exact responsibility and evidence supplied by the agent."""
        _require_text(authored.transition_id, field="transition_id")
        _require_text(authored.to_state, field="to_state")
        _require_text(authored.decision, field="decision")

        responsibility = authored.next_responsibility
        _require_text(responsibility.id, field="responsibility.id")
        _require_text(responsibility.statement, field="responsibility.statement")
        _require_text(responsibility.scope, field="responsibility.scope")
        if responsibility.decision_blocked is None:
            raise CampaignTransactionError(
                "responsibility.decision_blocked must be explicitly supplied"
            )
        _require_text(
            responsibility.decision_blocked,
            field="responsibility.decision_blocked",
        )
        if responsibility.status != "active":
            raise CampaignTransactionError(
                "next responsibility must have status 'active'"
            )
        if not responsibility.success_conditions:
            raise CampaignTransactionError(
                "next responsibility must define at least one success condition"
            )

        transition_evidence = set(authored.evidence)
        unbound_trigger_evidence = sorted(
            set(responsibility.trigger_evidence) - transition_evidence
        )
        if unbound_trigger_evidence:
            raise CampaignTransactionError(
                "next responsibility trigger evidence must be recorded on the "
                "advance transition: " + ", ".join(unbound_trigger_evidence)
            )

        snapshot = self.lifecycle.resume()
        available = set(snapshot.evidence_refs)
        missing_trigger_evidence = sorted(
            set(responsibility.trigger_evidence) - available
        )
        if missing_trigger_evidence:
            raise CampaignTransactionError(
                "next responsibility references missing trigger evidence: "
                + ", ".join(missing_trigger_evidence)
            )

        current = snapshot.state
        new_state = replace(
            current,
            status="active",
            current_state=authored.to_state,
            active_responsibility=responsibility,
            additional_active_responsibilities=(),
            authority=responsibility.authority,
            terminal_state=None,
        )
        transition = TransitionRecord(
            id=authored.transition_id,
            from_state=current.current_state,
            to_state=authored.to_state,
            evidence=authored.evidence,
            decision=authored.decision,
            next_responsibility=responsibility.id,
            terminal_state=None,
            authority=current.authority,
        )

        # Append-only P8 intent is prepared before the P2 commit. If the later
        # lifecycle write fails, the uncommitted lineage intent is an auditable
        # orphan and is never treated as a consumed-evidence edge.
        self.lineage.prepare_consumption(
            transition_id=authored.transition_id,
            evidence_refs=authored.evidence,
        )
        return self.lifecycle.record_transition(
            new_state=new_state,
            transition=transition,
        )

    def defer(self, authored: DeferDecision) -> CampaignSnapshot:
        """Delegate an explicit defer decision to the existing P2 primitive."""
        _require_text(authored.transition_id, field="transition_id")
        _require_text(authored.to_state, field="to_state")
        _require_text(authored.decision, field="decision")
        _require_text(authored.reason, field="reason")
        self.lineage.prepare_consumption(
            transition_id=authored.transition_id,
            evidence_refs=authored.evidence,
        )
        return self.lifecycle.defer_responsibility(
            transition_id=authored.transition_id,
            to_state=authored.to_state,
            reason=authored.reason,
            reopen_when=authored.reopen_when,
            decision=authored.decision,
            evidence=authored.evidence,
            not_reopened_by=authored.not_reopened_by,
        )

    def close(self, authored: CloseDecision) -> CampaignSnapshot:
        """Delegate an explicit terminal decision to the existing P2 primitive."""
        _require_text(authored.transition_id, field="transition_id")
        _require_text(authored.to_state, field="to_state")
        _require_text(authored.decision, field="decision")
        self.lineage.prepare_consumption(
            transition_id=authored.transition_id,
            evidence_refs=authored.evidence,
        )
        return self.lifecycle.terminate(
            transition_id=authored.transition_id,
            to_state=authored.to_state,
            terminal_state=authored.terminal_state,
            decision=authored.decision,
            evidence=authored.evidence,
        )
