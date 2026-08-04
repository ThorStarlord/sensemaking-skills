"""Campaign summary projection generator for Phase 4 (#120).

Derives `campaign-summary.yaml` EXCLUSIVELY from the append-only campaign
ledger plus its referenced attempt directories. The ledger is the source
of truth; the summary is a rebuildable projection that:

1. validates the entire ledger (hash chain, sequence, transitions) -- a
   malformed or truncated ledger fails closed with CAMPAIGN_LEDGER_CORRUPT;
2. rejects orphan results (an attempt-result.yaml whose attempt_id has no
   RESERVED ledger event);
3. rejects missing attempt directories (a RESERVED event whose attempt
   directory is gone);
4. counts every reservation and every provider invocation from events;
5. includes EVERY attempt -- successful, failed, aborted, and
   incomplete/crash-visible -- with no selective-omission option;
6. reports cost/token ceilings honestly as post-hoc soft limits;
7. writes the derived summary atomically (temp file + rename).

There is deliberately no ``generate_summary(successes_only=True)``.
"""

from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml

from sensemaking_skills.campaign_validation.digests import compute_policy_digest
from sensemaking_skills.campaign_validation.models import ValidatedCampaignBundle
from .failure_codes import (
    CAMPAIGN_SUMMARY_MISSING_ATTEMPT_DIR,
    CAMPAIGN_SUMMARY_ORPHAN_RESULT,
    CampaignAccountingError,
)
from .ledger import CampaignLedger, campaign_lock
from .models import AttemptState, CampaignSummary, TERMINAL_STATES
from .reservation import _ceiling_amount, _observed_cost_tokens


def _unfreeze(value: Any) -> Any:
    """Recursively convert frozen/immutable containers to plain Python types.

    Phase 2 validation returns policy.raw with nested MappingProxyType and
    tuple values. JCS canonicalize_bytes only handles plain dict/list/str/int/
    float/bool/None, so we must unfreeze before computing digests.
    """
    from types import MappingProxyType
    if isinstance(value, MappingProxyType):
        return {k: _unfreeze(v) for k, v in value.items()}
    if isinstance(value, dict):
        return {k: _unfreeze(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_unfreeze(v) for v in value]
    return value


def _reconcile_attempt_directories(campaign_dir: Path, events: List[Any]) -> None:
    """Fail closed on orphan results and missing attempt directories.

    * An attempt-result.yaml whose attempt_id has no RESERVED ledger event
      is an orphan result: the ledger is authoritative, so a result with no
      reservation is evidence of fabrication or tampering.
    * A RESERVED event whose attempt directory is missing means the
      attempt's artifacts were deleted -- the summary must not be generated
      as if the attempt never happened.
    """
    reserved_ids = {
        e.attempt_id
        for e in events
        if e.event_type == AttemptState.RESERVED.value
    }

    attempts_root = campaign_dir / "attempts"
    if attempts_root.is_dir():
        for child in attempts_root.iterdir():
            if not child.is_dir():
                continue
            if (child / "attempt-result.yaml").exists() and child.name not in reserved_ids:
                raise CampaignAccountingError(
                    CAMPAIGN_SUMMARY_ORPHAN_RESULT,
                    f"attempt directory '{child.name}' carries an "
                    f"attempt-result.yaml but the ledger has no RESERVED "
                    f"event for it",
                )

    for attempt_id in reserved_ids:
        if not (attempts_root / attempt_id).is_dir():
            raise CampaignAccountingError(
                CAMPAIGN_SUMMARY_MISSING_ATTEMPT_DIR,
                f"ledger has a RESERVED event for attempt '{attempt_id}' "
                f"but its attempt directory is missing",
            )


class CampaignSummaryGenerator:
    """Projects authoritative campaign summary from durable ledger state."""

    def __init__(self, campaign_root: Path) -> None:
        self.campaign_root = Path(campaign_root)

    def update_campaign_summary(
        self,
        bundle: ValidatedCampaignBundle,
        now: Optional[datetime] = None,
    ) -> CampaignSummary:
        """Generate and atomically write campaign-summary.yaml for a campaign."""
        if now is None:
            now = datetime.now(timezone.utc)
        timestamp_str = now.isoformat()

        policy = bundle.policy
        campaign_id = policy.campaign_id
        # policy.raw may contain MappingProxyType/tuple values frozen by Phase 2
        # validation. compute_policy_digest / JCS canonicalize_bytes requires
        # plain dicts and lists throughout the entire structure.
        policy_raw = _unfreeze(policy.raw)
        policy_digest = compute_policy_digest(policy_raw)
        campaign_dir = self.campaign_root / campaign_id

        ledger = CampaignLedger(campaign_dir, campaign_id)

        with campaign_lock(campaign_dir):
            # read_events validates the hash chain and transitions; a
            # malformed or truncated ledger fails closed here.
            events = ledger.read_events()
            _reconcile_attempt_directories(campaign_dir, events)

            reservation_ids: List[str] = []
            provider_invocations_made = 0
            attempts_map: Dict[str, Dict[str, Any]] = {}
            first_reserved_at: Optional[str] = None
            last_activity_at = timestamp_str

            for e in events:
                last_activity_at = e.timestamp
                if e.event_type == AttemptState.RESERVED.value:
                    if first_reserved_at is None:
                        first_reserved_at = e.timestamp
                    res_id = e.payload.get("reservation_id", e.attempt_id)
                    if res_id not in reservation_ids:
                        reservation_ids.append(res_id)

                    config_id = e.payload.get("configuration_id", "")
                    attempts_map[e.attempt_id] = {
                        "attempt_id": e.attempt_id,
                        "configuration_id": config_id,
                        "state": AttemptState.RESERVED.value,
                        "terminal_at": None,
                    }

                elif e.event_type == AttemptState.INVOKED.value:
                    provider_invocations_made += 1
                    if e.attempt_id in attempts_map:
                        attempts_map[e.attempt_id]["state"] = AttemptState.INVOKED.value

                elif e.event_type in [s.value for s in AttemptState]:
                    if e.attempt_id in attempts_map:
                        attempts_map[e.attempt_id]["state"] = e.event_type
                        if e.event_type in TERMINAL_STATES:
                            attempts_map[e.attempt_id]["terminal_at"] = (
                                e.payload.get("terminal_at", e.timestamp)
                            )

            attempts_list = list(attempts_map.values())

            max_attempt_slots = policy_raw.get("max_attempt_slots", 1)
            max_provider_invocations = policy_raw.get("max_provider_invocations", 1)
            remaining_attempt_slots = max(0, max_attempt_slots - len(reservation_ids))
            remaining_provider_invocations = max(
                0, max_provider_invocations - provider_invocations_made
            )

            # Cost/token ceilings are SOFT post-hoc limits (ADR 0023 §14):
            # reported from what was observed, never claimed as exact
            # pre-call guarantees.
            total_tokens, total_cost = _observed_cost_tokens(events)
            token_ceiling = _ceiling_amount(policy_raw.get("token_ceiling"))
            cost_ceiling = _ceiling_amount(policy_raw.get("cost_ceiling"))

            # Campaign state: APPROVED_NOT_STARTED -> ACTIVE -> EXPIRED /
            # EXHAUSTED. Any reached hard ceiling makes the campaign
            # EXHAUSTED, even with an incomplete (crash-visible) attempt.
            campaign_state = "ACTIVE"
            terminal_reason = None

            if len(reservation_ids) == 0:
                campaign_state = "APPROVED_NOT_STARTED"
            else:
                validity = policy_raw.get("validity_window") or {}
                not_after = None
                if validity:
                    not_after = datetime.fromisoformat(validity["not_after"])
                if not_after is not None and now > not_after:
                    campaign_state = "EXPIRED"
                    terminal_reason = "Policy validity window elapsed"
                elif (
                    remaining_attempt_slots == 0
                    or remaining_provider_invocations == 0
                    or (
                        token_ceiling is not None
                        and total_tokens >= token_ceiling
                    )
                    or (
                        cost_ceiling is not None
                        and total_cost >= cost_ceiling
                    )
                ):
                    campaign_state = "EXHAUSTED"
                    terminal_reason = "Policy ceiling reached"

            remaining_budget: Dict[str, Any] = {
                "attempt_slots": remaining_attempt_slots,
                "provider_invocations": remaining_provider_invocations,
            }
            if token_ceiling is not None:
                remaining_budget["tokens"] = max(0.0, token_ceiling - total_tokens)
            if cost_ceiling is not None:
                remaining_budget["cost"] = max(0.0, cost_ceiling - total_cost)
            remaining_budget["tokens_observed"] = total_tokens
            remaining_budget["cost_observed"] = total_cost

            summary = CampaignSummary(
                campaign_id=campaign_id,
                policy_digest=policy_digest,
                campaign_state=campaign_state,
                campaign_state_history=[
                    {"state": "APPROVED_NOT_STARTED", "at": first_reserved_at or timestamp_str},
                    {"state": campaign_state, "at": last_activity_at},
                ],
                reservations_issued={
                    "count": len(reservation_ids),
                    "ids": reservation_ids,
                },
                provider_invocations_made=provider_invocations_made,
                remaining_budget=remaining_budget,
                attempts=attempts_list,
                first_reserved_at=first_reserved_at,
                last_activity_at=last_activity_at,
                terminal_reason=terminal_reason,
            )

            # Atomically write campaign-summary.yaml (temp + rename) so a
            # crash never leaves a half-written summary.
            summary_file = campaign_dir / "campaign-summary.yaml"
            temp_file = campaign_dir / ".tmp-campaign-summary.yaml"
            with open(temp_file, "w", encoding="utf-8") as f:
                yaml.dump(summary.to_dict(), f, sort_keys=False)
                f.flush()
                os.fsync(f.fileno())
            temp_file.replace(summary_file)

            return summary
