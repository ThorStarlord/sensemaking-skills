"""Deterministic lifecycle service for durable Sensemaking campaigns.

The service composes ``CampaignStore`` primitives. It validates relationships
that are mechanically decidable (identity, transition chain, evidence presence,
authority metadata, terminal-state coherence) but never decides what repository
evidence means, which responsibility is warranted, or which capability should
be selected. Those remain agent judgments.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Mapping

from sensemaking_skills.campaign_semantics import (
    CampaignHandoff,
    CampaignPolicy,
    CampaignState,
    CampaignTrace,
    DeferredResponsibility,
    TerminalState,
    TransitionRecord,
    canonicalize,
    validate_reconstruction,
)

from .errors import CampaignIntegrityError, CampaignTransactionError
from .store import CampaignStore


def _artifact_digest(value: Any) -> str:
    """Deterministically bind a semantic record to trace history."""
    encoded = json.dumps(
        canonicalize(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class CampaignDiagnostic:
    code: str
    detail: str


@dataclass(frozen=True)
class CampaignValidationResult:
    valid: bool
    diagnostics: tuple[CampaignDiagnostic, ...] = ()

    @property
    def diagnostic_codes(self) -> tuple[str, ...]:
        return tuple(diagnostic.code for diagnostic in self.diagnostics)


@dataclass(frozen=True)
class CampaignSnapshot:
    state: CampaignState
    transitions: tuple[TransitionRecord, ...]
    trace: CampaignTrace
    evidence_refs: tuple[str, ...]
    policy: CampaignPolicy | None = None
    handoff: CampaignHandoff | None = None


class CampaignService:
    """Validate and persist agent-authored campaign lifecycle decisions."""

    def __init__(
        self,
        workspace: str | Path,
        *,
        target_repo: str | Path | None = None,
    ) -> None:
        self.store = CampaignStore(workspace, target_repo=target_repo)

    def initialize(
        self,
        state: CampaignState,
        *,
        policy: CampaignPolicy | None = None,
    ) -> CampaignSnapshot:
        """Initialize a structurally valid campaign; no responsibility is inferred."""
        diagnostics = self._state_diagnostics(state, set())
        if policy is not None:
            diagnostics.extend(self._policy_diagnostics(state, policy))
        self._raise_if_invalid(diagnostics, "campaign initialization is invalid")
        self.store.initialize(state, policy=policy)
        return self.resume()

    def validate(self) -> CampaignValidationResult:
        """Recover committed intent, then validate durable reconstruction."""
        self.store.recover_lifecycle_transactions()
        result, _ = self._inspect()
        return result

    def resume(self) -> CampaignSnapshot:
        """Recover and reconstruct a campaign for a fresh agent context."""
        self.store.recover_lifecycle_transactions()
        result, snapshot = self._inspect()
        if not result.valid:
            raise CampaignIntegrityError(
                "campaign reconstruction failed",
                diagnostic_codes=result.diagnostic_codes,
            )
        return snapshot

    def reconstruct(self) -> CampaignSnapshot:
        """Alias for ``resume`` emphasizing durable-state reconstruction."""
        return self.resume()

    def record_transition(
        self,
        *,
        new_state: CampaignState,
        transition: TransitionRecord,
    ) -> CampaignSnapshot:
        """Commit one agent-authored lifecycle transition transactionally."""
        snapshot = self.resume()
        current = snapshot.state

        if current.status == "terminal" or current.terminal_state is not None:
            raise CampaignTransactionError("terminal campaigns cannot advance")
        if transition.from_state != current.current_state:
            raise CampaignTransactionError(
                "transition.from_state must equal the current campaign state"
            )
        if transition.to_state != new_state.current_state:
            raise CampaignTransactionError(
                "transition.to_state must equal new_state.current_state"
            )
        if new_state.campaign_id != current.campaign_id:
            raise CampaignTransactionError("campaign_id cannot change during a transition")
        if new_state.mission != current.mission:
            raise CampaignTransactionError("campaign mission cannot change during a transition")
        if new_state.schema_version != current.schema_version:
            raise CampaignTransactionError(
                "campaign schema_version cannot change during a transition"
            )
        if transition.authority != current.authority:
            raise CampaignTransactionError(
                "transition authority must equal the source campaign authority"
            )

        expected_next = (
            new_state.active_responsibility.id
            if new_state.active_responsibility is not None
            else None
        )
        if transition.next_responsibility != expected_next:
            raise CampaignTransactionError(
                "transition.next_responsibility must match the new active responsibility"
            )
        if transition.terminal_state != new_state.terminal_state:
            raise CampaignTransactionError(
                "transition terminal_state must match new_state.terminal_state"
            )

        evidence = set(snapshot.evidence_refs)
        missing_transition_evidence = sorted(set(transition.evidence) - evidence)
        if missing_transition_evidence:
            raise CampaignTransactionError(
                "transition references missing evidence: "
                + ", ".join(missing_transition_evidence)
            )

        state_diagnostics = self._state_diagnostics(new_state, evidence)
        self._raise_if_invalid(state_diagnostics, "new campaign state is invalid")

        terminal_value = (
            new_state.terminal_state.value
            if new_state.terminal_state is not None
            else None
        )
        prepared_trace = replace(
            snapshot.trace,
            events=(
                *snapshot.trace.events,
                {
                    "event": "transition_committed",
                    "transition_id": transition.id,
                    "from_state": transition.from_state,
                    "to_state": transition.to_state,
                    "transition_digest": _artifact_digest(transition),
                    "state_digest": _artifact_digest(new_state),
                },
            ),
            terminal_state=terminal_value,
        )

        expected_transitions = (*snapshot.transitions, transition)
        expected_result, _ = self._validate_components(
            state=new_state,
            transitions=expected_transitions,
            trace=prepared_trace,
            evidence_refs=snapshot.evidence_refs,
            policy=snapshot.policy,
            handoff=None,
        )
        if not expected_result.valid:
            raise CampaignIntegrityError(
                "proposed lifecycle commit would not reconstruct",
                diagnostic_codes=expected_result.diagnostic_codes,
            )

        self.store.commit_lifecycle(
            state=new_state,
            transition=transition,
            trace=prepared_trace,
        )
        return self.resume()

    def defer_responsibility(
        self,
        *,
        transition_id: str,
        to_state: str,
        reason: str,
        reopen_when: tuple[str, ...],
        decision: str,
        evidence: tuple[str, ...] = (),
        not_reopened_by: tuple[str, ...] = (),
    ) -> CampaignSnapshot:
        """Persist an explicit agent decision to defer the active responsibility."""
        snapshot = self.resume()
        current = snapshot.state
        responsibility = current.active_responsibility
        if responsibility is None:
            raise CampaignTransactionError("there is no active responsibility to defer")
        if responsibility.status != "active":
            raise CampaignTransactionError("active responsibility is not in active status")
        if any(
            deferred.responsibility_id == responsibility.id
            for deferred in current.deferred_responsibilities
        ):
            raise CampaignTransactionError(
                "active responsibility already exists in deferred responsibilities"
            )

        deferred = DeferredResponsibility(
            responsibility_id=responsibility.id,
            reason=reason,
            reopen_when=reopen_when,
            not_reopened_by=not_reopened_by,
        )
        new_state = replace(
            current,
            current_state=to_state,
            active_responsibility=None,
            additional_active_responsibilities=(),
            deferred_responsibilities=(*current.deferred_responsibilities, deferred),
            authority=None,
            terminal_state=None,
            status="active",
        )
        transition = TransitionRecord(
            id=transition_id,
            from_state=current.current_state,
            to_state=to_state,
            evidence=evidence,
            decision=decision,
            next_responsibility=None,
            terminal_state=None,
            authority=current.authority,
        )
        return self.record_transition(new_state=new_state, transition=transition)

    def terminate(
        self,
        *,
        transition_id: str,
        to_state: str,
        terminal_state: TerminalState,
        decision: str,
        evidence: tuple[str, ...] = (),
    ) -> CampaignSnapshot:
        """Persist an explicit terminal campaign decision without choosing work."""
        snapshot = self.resume()
        current = snapshot.state
        if current.status == "terminal" or current.terminal_state is not None:
            raise CampaignTransactionError("campaign is already terminal")

        new_state = replace(
            current,
            status="terminal",
            current_state=to_state,
            active_responsibility=None,
            additional_active_responsibilities=(),
            terminal_state=terminal_state,
        )
        transition = TransitionRecord(
            id=transition_id,
            from_state=current.current_state,
            to_state=to_state,
            evidence=evidence,
            decision=decision,
            next_responsibility=None,
            terminal_state=terminal_state,
            authority=current.authority,
        )
        return self.record_transition(new_state=new_state, transition=transition)

    def generate_handoff(
        self,
        *,
        canonical_artifacts: tuple[str, ...],
        allowed_next_actions: tuple[str, ...],
        stop_conditions: tuple[TerminalState, ...],
    ) -> CampaignHandoff:
        """Write a handoff bound to the exact reconstructed current state."""
        snapshot = self.resume()
        available = set(snapshot.evidence_refs)
        available.update({"campaign-state.yaml", "trace.yaml"})
        if snapshot.policy is not None:
            available.add("campaign-policy.yaml")
        available.update(
            f"transitions/{transition.id}.yaml"
            for transition in snapshot.transitions
        )
        missing = sorted(set(canonical_artifacts) - available)
        if missing:
            raise CampaignTransactionError(
                "handoff references non-durable canonical artifacts: "
                + ", ".join(missing)
            )

        handoff = CampaignHandoff(
            campaign_id=snapshot.state.campaign_id,
            current_state=snapshot.state,
            canonical_artifacts=canonical_artifacts,
            allowed_next_actions=allowed_next_actions,
            stop_conditions=stop_conditions,
        )
        self.store.write_handoff(handoff)
        return self.store.load_handoff()

    def _inspect(self) -> tuple[CampaignValidationResult, CampaignSnapshot]:
        state = self.store.load_state()
        trace = self.store.load_trace()
        raw_transitions = self.store.load_transitions()
        evidence_refs = self.store.evidence_refs()

        policy = None
        if os.path.lexists(self.store.workspace.policy_path):
            policy = self.store.load_policy()
        handoff = None
        if os.path.lexists(self.store.workspace.handoff_path):
            handoff = self.store.load_handoff()

        result, ordered = self._validate_components(
            state=state,
            transitions=raw_transitions,
            trace=trace,
            evidence_refs=evidence_refs,
            policy=policy,
            handoff=handoff,
        )
        snapshot = CampaignSnapshot(
            state=state,
            transitions=ordered if result.valid else raw_transitions,
            trace=trace,
            evidence_refs=evidence_refs,
            policy=policy,
            handoff=handoff,
        )
        return result, snapshot

    def _validate_components(
        self,
        *,
        state: CampaignState,
        transitions: tuple[TransitionRecord, ...],
        trace: CampaignTrace,
        evidence_refs: tuple[str, ...],
        policy: CampaignPolicy | None,
        handoff: CampaignHandoff | None,
    ) -> tuple[CampaignValidationResult, tuple[TransitionRecord, ...]]:
        diagnostics: list[CampaignDiagnostic] = []
        evidence = set(evidence_refs)
        diagnostics.extend(self._state_diagnostics(state, evidence))
        if policy is not None:
            diagnostics.extend(self._policy_diagnostics(state, policy))
        if handoff is not None and handoff.current_state != state:
            diagnostics.append(
                CampaignDiagnostic(
                    "HANDOFF_STATE_MISMATCH",
                    "handoff current_state is not the exact campaign-state snapshot",
                )
            )

        ordered, history_diagnostics = self._reconstruct_history(
            state=state,
            transitions=transitions,
            trace=trace,
            evidence=evidence,
        )
        diagnostics.extend(history_diagnostics)
        return CampaignValidationResult(not diagnostics, tuple(diagnostics)), ordered

    @staticmethod
    def _state_diagnostics(
        state: CampaignState,
        evidence: set[str],
    ) -> list[CampaignDiagnostic]:
        diagnostics = [
            CampaignDiagnostic(diagnostic.code, diagnostic.detail)
            for diagnostic in validate_reconstruction(state, (), evidence).diagnostics
        ]
        if (
            state.active_responsibility is not None
            and state.authority != state.active_responsibility.authority
        ):
            diagnostics.append(
                CampaignDiagnostic(
                    "AUTHORITY_METADATA_MISMATCH",
                    "campaign authority must equal active responsibility authority",
                )
            )
        if state.status == "terminal" and state.terminal_state is None:
            diagnostics.append(
                CampaignDiagnostic(
                    "TERMINAL_STATUS_MISSING_TERMINAL_STATE",
                    "terminal campaign status requires terminal_state",
                )
            )
        if state.status != "terminal" and state.terminal_state is not None:
            diagnostics.append(
                CampaignDiagnostic(
                    "TERMINAL_STATE_STATUS_MISMATCH",
                    "terminal_state requires campaign status 'terminal'",
                )
            )
        return diagnostics

    @staticmethod
    def _policy_diagnostics(
        state: CampaignState,
        policy: CampaignPolicy,
    ) -> list[CampaignDiagnostic]:
        diagnostics: list[CampaignDiagnostic] = []
        if policy.campaign_id != state.campaign_id:
            diagnostics.append(
                CampaignDiagnostic(
                    "POLICY_CAMPAIGN_ID_MISMATCH",
                    "campaign policy and state use different campaign_id values",
                )
            )
        if policy.mission != state.mission:
            diagnostics.append(
                CampaignDiagnostic(
                    "POLICY_MISSION_MISMATCH",
                    "campaign policy mission must equal campaign state mission",
                )
            )
        if policy.schema_version != state.schema_version:
            diagnostics.append(
                CampaignDiagnostic(
                    "POLICY_SCHEMA_VERSION_MISMATCH",
                    "campaign policy and state schema versions differ",
                )
            )
        return diagnostics

    @staticmethod
    def _reconstruct_history(
        *,
        state: CampaignState,
        transitions: tuple[TransitionRecord, ...],
        trace: CampaignTrace,
        evidence: set[str],
    ) -> tuple[tuple[TransitionRecord, ...], list[CampaignDiagnostic]]:
        diagnostics: list[CampaignDiagnostic] = []
        if trace.campaign_id != state.campaign_id:
            diagnostics.append(
                CampaignDiagnostic(
                    "TRACE_CAMPAIGN_ID_MISMATCH",
                    "trace and state use different campaign_id values",
                )
            )
        if trace.initial_state is None:
            diagnostics.append(
                CampaignDiagnostic(
                    "TRACE_INITIAL_STATE_MISSING",
                    "trace must preserve the campaign initial state",
                )
            )

        by_id = {transition.id: transition for transition in transitions}
        if len(by_id) != len(transitions):
            diagnostics.append(
                CampaignDiagnostic(
                    "DUPLICATE_TRANSITION_ID",
                    "transition IDs must be unique",
                )
            )

        ordered: list[TransitionRecord] = []
        seen: set[str] = set()
        expected_state = trace.initial_state
        final_state_digest: str | None = None
        for index, event in enumerate(trace.events):
            if not isinstance(event, Mapping):
                diagnostics.append(
                    CampaignDiagnostic(
                        "INVALID_TRACE_EVENT",
                        f"trace event {index} is not a mapping",
                    )
                )
                continue
            if event.get("event") != "transition_committed":
                continue
            transition_id = event.get("transition_id")
            from_state = event.get("from_state")
            to_state = event.get("to_state")
            transition_digest = event.get("transition_digest")
            state_digest = event.get("state_digest")
            if not all(
                isinstance(value, str) and value
                for value in (
                    transition_id,
                    from_state,
                    to_state,
                    transition_digest,
                    state_digest,
                )
            ):
                diagnostics.append(
                    CampaignDiagnostic(
                        "INVALID_TRANSITION_TRACE_EVENT",
                        f"transition trace event {index} is incomplete",
                    )
                )
                continue
            if transition_id in seen:
                diagnostics.append(
                    CampaignDiagnostic(
                        "DUPLICATE_TRANSITION_TRACE_EVENT",
                        f"transition {transition_id!r} appears more than once in trace",
                    )
                )
                continue
            seen.add(transition_id)
            transition = by_id.get(transition_id)
            if transition is None:
                diagnostics.append(
                    CampaignDiagnostic(
                        "TRACE_MISSING_TRANSITION",
                        f"trace references missing transition {transition_id!r}",
                    )
                )
                continue
            if transition.from_state != from_state or transition.to_state != to_state:
                diagnostics.append(
                    CampaignDiagnostic(
                        "TRACE_TRANSITION_CONTENT_MISMATCH",
                        f"trace event for {transition_id!r} disagrees with transition record",
                    )
                )
            if _artifact_digest(transition) != transition_digest:
                diagnostics.append(
                    CampaignDiagnostic(
                        "TRANSITION_DIGEST_MISMATCH",
                        f"transition {transition_id!r} no longer matches its trace digest",
                    )
                )
            if expected_state is not None and transition.from_state != expected_state:
                diagnostics.append(
                    CampaignDiagnostic(
                        "BROKEN_TRANSITION_CHAIN",
                        f"{transition.id} starts at {transition.from_state!r}, expected {expected_state!r}",
                    )
                )
            expected_state = transition.to_state
            missing = sorted(set(transition.evidence) - evidence)
            if missing:
                diagnostics.append(
                    CampaignDiagnostic(
                        "MISSING_EVIDENCE",
                        f"{transition.id} references missing evidence: {', '.join(missing)}",
                    )
                )
            ordered.append(transition)
            final_state_digest = state_digest

        untraced = sorted(set(by_id) - seen)
        if untraced:
            diagnostics.append(
                CampaignDiagnostic(
                    "UNTRACED_TRANSITION",
                    "transition records are missing from trace order: " + ", ".join(untraced),
                )
            )
        if expected_state is not None and expected_state != state.current_state:
            diagnostics.append(
                CampaignDiagnostic(
                    "CURRENT_STATE_NOT_RECONSTRUCTIBLE",
                    f"history ends at {expected_state!r}, current state is {state.current_state!r}",
                )
            )
        if ordered and final_state_digest != _artifact_digest(state):
            diagnostics.append(
                CampaignDiagnostic(
                    "CURRENT_STATE_DIGEST_MISMATCH",
                    "current campaign state no longer matches the final trace digest",
                )
            )

        for transition in ordered[:-1]:
            if transition.terminal_state is not None:
                diagnostics.append(
                    CampaignDiagnostic(
                        "TERMINAL_TRANSITION_NOT_FINAL",
                        f"terminal transition {transition.id!r} is followed by later history",
                    )
                )
        if ordered:
            final_terminal = ordered[-1].terminal_state
            if final_terminal != state.terminal_state:
                diagnostics.append(
                    CampaignDiagnostic(
                        "FINAL_TRANSITION_TERMINAL_MISMATCH",
                        "final transition terminal_state does not match campaign state",
                    )
                )

        expected_trace_terminal = (
            state.terminal_state.value if state.terminal_state is not None else None
        )
        if trace.terminal_state != expected_trace_terminal:
            diagnostics.append(
                CampaignDiagnostic(
                    "TRACE_TERMINAL_STATE_MISMATCH",
                    "trace terminal_state does not match campaign state",
                )
            )
        return tuple(ordered), diagnostics

    @staticmethod
    def _raise_if_invalid(
        diagnostics: list[CampaignDiagnostic],
        message: str,
    ) -> None:
        if diagnostics:
            raise CampaignIntegrityError(
                message,
                diagnostic_codes=(diagnostic.code for diagnostic in diagnostics),
            )
