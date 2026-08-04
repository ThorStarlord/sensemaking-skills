"""Durable reservation manager for Phase 4 (#120).

Creates immutable, on-disk attempt reservations before any provider call,
enforcing multi-dimensional policy budget limits, cross-document campaign-ID
consistency, and non-reusability of attempt IDs.

The central Phase 4 invariant is:

    No durable reservation -> No capability -> No provider invocation

``reserve_attempt`` is the first irreversible act: it consumes an attempt
slot (never refunded, even when the attempt later aborts before invocation)
and writes the reservation to disk under the campaign lock BEFORE any
capability can be minted or any provider entered.
"""

from datetime import datetime, timezone
import json
import os
import re
import uuid
from pathlib import Path
from typing import Any, Dict, Optional
import yaml

from sensemaking_skills.campaign_validation.models import ValidatedCampaignBundle
from .failure_codes import (
    ATTEMPT_DIRECTORY_EXISTS,
    ATTEMPT_ID_NOT_UUID,
    BUDGET_EXCEEDED_ATTEMPT_SLOTS,
    BUDGET_EXCEEDED_CONFIGURATION_SLOTS,
    CAMPAIGN_EXPIRED,
    CAMPAIGN_NOT_ACTIVE,
    CONFIGURATION_ID_MISMATCH,
    CROSS_DOCUMENT_CAMPAIGN_ID_MISMATCH,
    RESERVATION_EXISTS_FOR_ATTEMPT,
    CampaignAccountingError,
)
from .ledger import CampaignLedger, campaign_lock
from .models import (
    _create_attempt_reservation,
    AttemptReservation,
    AttemptState,
    TERMINAL_STATES,
)

_STRICT_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)


def _strict_uuid(value: str) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError):
        return False
    # Strict lowercase canonical form only (matches Phase 3 minting).
    return str(parsed) == value and _STRICT_UUID_RE.match(value) is not None


def verify_cross_document_campaign_id(
    policy_campaign_id: str,
    approval_campaign_id: str,
    configuration_campaign_id: str,
    request_campaign_id: str,
) -> None:
    """Verify that campaign_id is identical across all four document contexts."""
    if not (
        policy_campaign_id
        == approval_campaign_id
        == configuration_campaign_id
        == request_campaign_id
    ):
        raise CampaignAccountingError(
            CROSS_DOCUMENT_CAMPAIGN_ID_MISMATCH,
            f"Campaign ID mismatch across documents: policy='{policy_campaign_id}', "
            f"approval='{approval_campaign_id}', configuration='{configuration_campaign_id}', "
            f"request='{request_campaign_id}'",
        )


def _policy_ceiling(policy_raw: Dict[str, Any], key: str, default: Any) -> Any:
    return policy_raw.get(key, default)


def _as_amount(value: Any) -> Optional[float]:
    """Coerce an observed/ceiling amount (number or numeric string) to float.

    Cost amounts may legitimately arrive as strings (the two-lane schema
    examples write ``amount: "0.00"``). Non-numeric values are treated as
    absent -- they never crash accounting, they simply do not count.
    """
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def _ceiling_amount(ceiling: Any) -> Optional[float]:
    """Extract the numeric amount from a declared ceiling.

    ``token_ceiling`` is a number; ``cost_ceiling`` is
    ``object{amount, currency}`` per the campaign-policy schema v1.
    """
    if isinstance(ceiling, dict):
        return _as_amount(ceiling.get("amount"))
    return _as_amount(ceiling)


def _observed_cost_tokens(events: list) -> Dict[str, float]:
    """Sum observed tokens/cost from terminal event payloads.

    Cost ceilings are soft, post-hoc limits (ADR 0023 §14): observed totals
    are computed from what was actually reported, and a campaign whose
    observed totals cross a declared ceiling becomes EXHAUSTED so no further
    attempt may be reserved.
    """
    total_tokens = 0.0
    total_cost = 0.0
    for e in events:
        payload = e.payload or {}
        amount = _as_amount(payload.get("tokens_observed"))
        if amount is not None:
            total_tokens += amount
        cost = payload.get("cost_observed")
        if isinstance(cost, dict):
            cost_amount = _as_amount(cost.get("amount"))
            if cost_amount is not None:
                total_cost += cost_amount
    return total_tokens, total_cost


def _campaign_cost_token_exhausted(
    policy_raw: Dict[str, Any], events: list
) -> Optional[str]:
    """Return a reason string when observed totals cross a declared ceiling."""
    total_tokens, total_cost = _observed_cost_tokens(events)
    token_ceiling = _ceiling_amount(policy_raw.get("token_ceiling"))
    if token_ceiling is not None and total_tokens >= token_ceiling:
        return (
            f"observed token usage ({total_tokens:g}) reached the policy "
            f"token_ceiling ({token_ceiling:g})"
        )
    cost_ceiling = _ceiling_amount(policy_raw.get("cost_ceiling"))
    if cost_ceiling is not None and total_cost >= cost_ceiling:
        return (
            f"observed cost ({total_cost:g}) reached the policy "
            f"cost_ceiling ({cost_ceiling:g})"
        )
    return None


class DurableReservationManager:
    """Manages durable attempt reservations on disk."""

    def __init__(self, campaign_root: Path) -> None:
        self.campaign_root = Path(campaign_root)

    def reserve_attempt(
        self,
        bundle: ValidatedCampaignBundle,
        attempt_id: str,
        configuration_id: str,
        request_metadata: Dict[str, Any],
        now: Optional[datetime] = None,
    ) -> AttemptReservation:
        """Create a durable attempt reservation on disk.

        Enforces, in order:
        1. Strict lowercase-UUID attempt identity.
        2. Cross-document campaign consistency (policy/approval/configuration/
           request) -- a mismatched "Franken-bundle" never consumes a slot.
        3. Configuration consistency: the reserved ``configuration_id`` must
           be the one the validated bundle carries.
        4. Policy validity window (expiry).
        5. Attempt-slot, per-configuration, concurrency, and soft
           cost/token ceilings -- all under one campaign lock, so two
           processes can never both believe capacity exists.
        6. Exclusive attempt-directory creation; duplicate attempt IDs and
           recreated directories are rejected forever.
        """
        if not _strict_uuid(attempt_id):
            raise CampaignAccountingError(
                ATTEMPT_ID_NOT_UUID,
                f"attempt_id {attempt_id!r} is not a strict lowercase UUID",
            )
        if now is None:
            now = datetime.now(timezone.utc)
        reserved_at_str = now.isoformat()

        policy = bundle.policy
        approval = bundle.approval
        configuration = bundle.configuration
        campaign_id = policy.campaign_id

        # 1. Cross-document campaign consistency (Phase 3 follow-up #1).
        verify_cross_document_campaign_id(
            policy.campaign_id,
            approval.campaign_id,
            configuration.campaign_id,
            request_metadata.get("campaign_id", campaign_id),
        )

        # 2. The reserved configuration must be the validated one.
        if configuration_id != configuration.configuration_id:
            raise CampaignAccountingError(
                CONFIGURATION_ID_MISMATCH,
                f"request names configuration '{configuration_id}' but the "
                f"validated bundle carries '{configuration.configuration_id}'",
            )

        policy_raw = policy.raw
        validity = policy_raw.get("validity_window") or {}
        if validity:
            not_before = datetime.fromisoformat(validity["not_before"])
            not_after = datetime.fromisoformat(validity["not_after"])
            if now < not_before or now > not_after:
                raise CampaignAccountingError(
                    CAMPAIGN_EXPIRED,
                    f"Campaign '{campaign_id}' is outside validity window ({validity['not_before']} to {validity['not_after']}) at {reserved_at_str}",
                )

        campaign_dir = self.campaign_root / campaign_id
        ledger = CampaignLedger(campaign_dir, campaign_id)

        max_attempt_slots = _policy_ceiling(policy_raw, "max_attempt_slots", 1)
        max_attempts_per_configuration = _policy_ceiling(
            policy_raw, "max_attempts_per_configuration", 1
        )
        # Phase 4 v1 (Issue #120): one-process locking and an effective
        # concurrency ceiling of one. A policy declaring a lower ceiling
        # (0) is honored; a higher ceiling is capped at 1 until distributed
        # coordination exists.
        concurrency_ceiling = min(
            int(_policy_ceiling(policy_raw, "concurrency_ceiling", 1)), 1
        )

        with campaign_lock(campaign_dir):
            # Read existing ledger history (validates integrity; fails closed).
            events = ledger.read_events()

            # 3. Attempt-ID uniqueness: an attempt_id never represents two
            # provider calls, and never reappears after any transition.
            for event in events:
                if event.attempt_id == attempt_id:
                    raise CampaignAccountingError(
                        RESERVATION_EXISTS_FOR_ATTEMPT,
                        f"Reservation already exists for attempt ID '{attempt_id}'",
                    )

            # 4. Soft cost/token ceilings: once observed totals cross a
            # declared ceiling the campaign is EXHAUSTED and accepts no
            # further reservations.
            exhausted_reason = _campaign_cost_token_exhausted(policy_raw, events)
            if exhausted_reason is not None:
                raise CampaignAccountingError(
                    CAMPAIGN_NOT_ACTIVE,
                    f"Campaign '{campaign_id}' is exhausted: {exhausted_reason}",
                )

            # 5. Attempt-slot budget: every RESERVED event consumes a slot,
            # and slots are never refunded -- aborted, failed, interrupted,
            # and successful attempts all count.
            reserved_events = [
                e for e in events if e.event_type == AttemptState.RESERVED.value
            ]
            total_attempts_reserved = len(reserved_events)
            if total_attempts_reserved >= max_attempt_slots:
                raise CampaignAccountingError(
                    BUDGET_EXCEEDED_ATTEMPT_SLOTS,
                    f"Campaign '{campaign_id}' has reached max_attempt_slots limit ({max_attempt_slots})",
                )

            # 6. Per-configuration budget, grouped by exact configuration_id.
            config_attempts_reserved = sum(
                1
                for e in reserved_events
                if e.payload.get("configuration_id") == configuration_id
            )
            if config_attempts_reserved >= max_attempts_per_configuration:
                raise CampaignAccountingError(
                    BUDGET_EXCEEDED_CONFIGURATION_SLOTS,
                    f"Configuration '{configuration_id}' has reached max_attempts_per_configuration limit ({max_attempts_per_configuration})",
                )

            # 7. Concurrency: count nonterminal attempts (RESERVED, INVOKED,
            # OUTPUT_CAPTURED).
            attempts_latest_state: Dict[str, str] = {}
            for e in events:
                if e.event_type in [s.value for s in AttemptState]:
                    attempts_latest_state[e.attempt_id] = e.event_type

            active_attempts = [
                aid
                for aid, st in attempts_latest_state.items()
                if st not in TERMINAL_STATES
            ]
            if concurrency_ceiling >= 1 and len(active_attempts) >= concurrency_ceiling:
                raise CampaignAccountingError(
                    "CONCURRENCY_CEILING_EXCEEDED",
                    f"Campaign '{campaign_id}' concurrency ceiling ({concurrency_ceiling}) exceeded by active attempt '{active_attempts[0]}'",
                )

            # 8. Create attempt directory exclusively -- never reusable, never
            # overwritten, never recreated through the normal runtime.
            attempt_dir = campaign_dir / "attempts" / attempt_id
            if attempt_dir.exists():
                raise CampaignAccountingError(
                    ATTEMPT_DIRECTORY_EXISTS,
                    f"Attempt directory already exists at '{attempt_dir}'",
                )

            try:
                attempt_dir.mkdir(parents=True, exist_ok=False)
            except FileExistsError as exc:
                raise CampaignAccountingError(
                    ATTEMPT_DIRECTORY_EXISTS,
                    f"Attempt directory creation race at '{attempt_dir}'",
                ) from exc

            # 9. reservation_id and attempt_id are allocated together and
            # remain one-to-one forever (ADR 0023 §9e).
            reservation = _create_attempt_reservation(
                reservation_id=attempt_id,
                attempt_id=attempt_id,
                campaign_id=campaign_id,
                configuration_id=configuration_id,
                reserved_at=reserved_at_str,
                state=AttemptState.RESERVED.value,
                state_history=[
                    {"state": AttemptState.RESERVED.value, "at": reserved_at_str}
                ],
            )

            # 10. Persist reservation.yaml, then request-metadata.json, then
            # the RESERVED ledger event -- each flushed and fsynced before
            # the next step. The RESERVED event is what makes the attempt
            # visible to the world.
            res_file = attempt_dir / "reservation.yaml"
            with open(res_file, "w", encoding="utf-8") as f:
                yaml.dump(reservation.to_dict(), f, sort_keys=False)
                f.flush()
                os.fsync(f.fileno())

            meta_file = attempt_dir / "request-metadata.json"
            with open(meta_file, "w", encoding="utf-8") as f:
                json.dump(request_metadata, f, indent=2)
                f.flush()
                os.fsync(f.fileno())

            ledger._append_event_unlocked(
                events=events,
                timestamp=reserved_at_str,
                attempt_id=attempt_id,
                event_type=AttemptState.RESERVED.value,
                payload={
                    "configuration_id": configuration_id,
                    "reservation_id": attempt_id,
                },
            )

            return reservation
