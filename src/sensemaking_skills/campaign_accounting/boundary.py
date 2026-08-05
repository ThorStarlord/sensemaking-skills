"""Phase 3 + Phase 4 provider boundary (Issue #120).

This is the single narrow seam where a capability-backed exploratory
invocation is allowed to cross into the provider. It composes the Phase 3
capability machinery with the Phase 4 durable reservation ledger:

    verify reservation exists and is live (durable)
    verify capability matches reservation
    consume capability (Phase 3, atomic, exactly one winner)
    persist INVOKED transition (durable, fsynced)
    enter provider
    preserve raw output (durable, atomic rename)
    validate and persist the terminal outcome

The ordering is a crash-safety contract: the provider call NEVER occurs
before the durable INVOKED transition. A crash at any earlier point leaves
a reservation that recovery can classify as ABORTED_BEFORE_INVOCATION; a
crash after INVOKED leaves a visible, spent, incomplete attempt that can
never be retried under the same attempt ID.

The boundary accepts a genuine ``AttemptReservation`` produced by
``DurableReservationManager.reserve_attempt`` only. It rejects:

* ``None`` / a caller-supplied attempt ID with no reservation;
* a plain reservation-shaped mapping or a reconstructed object;
* a reservation from another campaign or another configuration;
* a reservation whose ledger state is no longer ``RESERVED`` (already
  INVOKED or terminal);
* a reservation whose policy validity window has elapsed.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional
import yaml

from sensemaking_skills.campaign_validation.models import ValidatedCampaignBundle
from sensemaking_skills.exploratory_authorization import (
    burn_exploratory_capability,
    consume_exploratory_capability,
)
from .failure_codes import (
    RESERVATION_ATTEMPT_MISMATCH,
    RESERVATION_CAMPAIGN_MISMATCH,
    RESERVATION_CONFIGURATION_MISMATCH,
    RESERVATION_EXPIRED,
    RESERVATION_NOT_GENUINE,
    RESERVATION_NOT_LIVE,
    RESERVATION_REQUIRED_BEFORE_INVOCATION,
    CampaignAccountingError,
)
from .ledger import CampaignLedger, campaign_lock
from .models import (
    AttemptReservation,
    AttemptResult,
    AttemptState,
    ProviderResponse,
    ValidationOutcome,
    is_genuine_attempt_reservation,
)
from .permit import (
    consume_provider_permit,
    issue_provider_permit,
)
from .recorder import AttemptOutcomeRecorder


def verify_reservation_live_for_invocation(
    *,
    bundle: ValidatedCampaignBundle,
    reservation: Optional[AttemptReservation],
    campaign_root: Path,
    now: datetime,
) -> None:
    """Fail closed unless ``reservation`` is genuine, matching, and live.

    Liveness is decided by the DURABLE ledger and the on-disk reservation,
    never by the in-memory object's attributes: a stale or forged object
    cannot authorize anything.
    """
    if reservation is None:
        raise CampaignAccountingError(
            RESERVATION_REQUIRED_BEFORE_INVOCATION,
            "no durable reservation was supplied; a provider call requires "
            "one prior durable reservation",
        )
    if not is_genuine_attempt_reservation(reservation):
        raise CampaignAccountingError(
            RESERVATION_NOT_GENUINE,
            "the supplied reservation is not a genuine reservation produced "
            "by DurableReservationManager.reserve_attempt (it may be a "
            "reconstruction or a reservation-shaped object)",
        )

    if reservation.campaign_id != bundle.policy.campaign_id:
        raise CampaignAccountingError(
            RESERVATION_CAMPAIGN_MISMATCH,
            f"reservation names campaign '{reservation.campaign_id}' but the "
            f"validated bundle belongs to '{bundle.policy.campaign_id}'",
        )
    if reservation.configuration_id != bundle.configuration.configuration_id:
        raise CampaignAccountingError(
            RESERVATION_CONFIGURATION_MISMATCH,
            f"reservation names configuration '{reservation.configuration_id}' "
            f"but the validated bundle carries "
            f"'{bundle.configuration.configuration_id}'",
        )

    # Policy validity window re-check at the provider boundary.
    validity = bundle.policy.raw.get("validity_window") or {}
    if validity:
        not_before = datetime.fromisoformat(validity["not_before"])
        not_after = datetime.fromisoformat(validity["not_after"])
        if now < not_before or now > not_after:
            raise CampaignAccountingError(
                RESERVATION_EXPIRED,
                f"reservation for attempt '{reservation.attempt_id}' is "
                f"outside the policy validity window "
                f"[{validity['not_before']}, {validity['not_after']}] at "
                f"{now.isoformat()}",
            )

    # Durable liveness: the ledger (authoritative) must show RESERVED as the
    # attempt's latest state, and the on-disk reservation must agree with
    # the object on every identity field.
    campaign_dir = Path(campaign_root) / reservation.campaign_id
    ledger = CampaignLedger(campaign_dir, reservation.campaign_id)
    with campaign_lock(campaign_dir):
        events = ledger.read_events()
        latest: Optional[str] = None
        for e in events:
            if e.attempt_id == reservation.attempt_id and (
                e.event_type in [s.value for s in AttemptState]
            ):
                latest = e.event_type
        if latest != AttemptState.RESERVED.value:
            raise CampaignAccountingError(
                RESERVATION_NOT_LIVE,
                f"attempt '{reservation.attempt_id}' is not live: its latest "
                f"ledger state is '{latest}' (expected RESERVED)",
            )

        res_file = campaign_dir / "attempts" / reservation.attempt_id / "reservation.yaml"
        if not res_file.exists():
            raise CampaignAccountingError(
                RESERVATION_NOT_LIVE,
                f"attempt '{reservation.attempt_id}' has no on-disk "
                f"reservation at '{res_file}'",
            )
        with open(res_file, "r", encoding="utf-8") as f:
            on_disk = yaml.safe_load(f) or {}
        for field in ("reservation_id", "attempt_id", "campaign_id", "configuration_id"):
            if on_disk.get(field) != getattr(reservation, field):
                raise CampaignAccountingError(
                    RESERVATION_NOT_LIVE,
                    f"on-disk reservation disagrees with the supplied "
                    f"reservation on '{field}'",
                )


def verify_capability_matches_reservation(
    *,
    capability: Any,
    reservation: AttemptReservation,
) -> None:
    """Fail closed unless the capability is bound to the same attempt.

    Defense-in-depth on top of the Phase 3 consumption's 13-field binding
    check: the capability must name the exact reservation's attempt,
    campaign, and configuration.
    """
    binding = getattr(capability, "binding", None)
    if binding is None:
        raise CampaignAccountingError(
            RESERVATION_NOT_GENUINE,
            "the capability carries no binding; it cannot be matched to a "
            "reservation",
        )
    if binding.attempt_id != reservation.attempt_id:
        raise CampaignAccountingError(
            RESERVATION_ATTEMPT_MISMATCH,
            f"capability is bound to attempt '{binding.attempt_id}' but the "
            f"reservation is for attempt '{reservation.attempt_id}'",
        )
    if binding.campaign_id != reservation.campaign_id:
        raise CampaignAccountingError(
            RESERVATION_CAMPAIGN_MISMATCH,
            f"capability is bound to campaign '{binding.campaign_id}' but the "
            f"reservation is for campaign '{reservation.campaign_id}'",
        )
    if binding.configuration_id != reservation.configuration_id:
        raise CampaignAccountingError(
            RESERVATION_CONFIGURATION_MISMATCH,
            f"capability is bound to configuration '{binding.configuration_id}' "
            f"but the reservation is for configuration "
            f"'{reservation.configuration_id}'",
        )


def invoke_exploratory_attempt(
    *,
    bundle: ValidatedCampaignBundle,
    capability: Any,
    reservation: AttemptReservation,
    campaign_root: Path,
    context: Any,
    provider: Callable[..., ProviderResponse],
    validate: Callable[[bytes], ValidationOutcome],
    prompt: str,
    now: Optional[datetime] = None,
) -> AttemptResult:
    """Run exactly one reservation-backed, capability-bound attempt.

    ``provider`` is called as ``provider(permit=..., context=..., prompt=...)``
    and must return a ``ProviderResponse`` carrying the exact raw response
    bytes plus post-hoc usage observations. ``validate`` turns the
    preserved raw bytes into a ``ValidationOutcome``.

    Guarantees:

    * Zero provider calls on every denial path (no reservation, forged
      reservation, wrong campaign/configuration/attempt, expired, not
      live, consumed/spent capability, binding drift).
    * The exact request bytes are preserved durably (``raw-request.txt``)
      while the attempt is still RESERVED, and the durable INVOKED
      transition -- which names the preserved request -- is persisted and
      fsynced BEFORE the provider is called.
    * The one-shot provider permit is issued only AFTER the durable INVOKED
      transition and consumed atomically immediately before provider entry;
      the provider cannot be reached with an unissued, unconsumed, or
      stale permit.
    * The raw response is preserved atomically before validation.
    * A provider ``Exception`` records PROVIDER_FAILED and burns the
      capability, then re-raises.
    * An interruption-like ``BaseException`` (e.g. KeyboardInterrupt)
      leaves the durable state as INVOKED-incomplete -- visible, spent,
      never retried -- burns the capability, and is re-raised.
    * Validation failure records VALIDATION_FAILED with the raw output and
      produced artifact preserved; there is no silent repair or hidden
      retry.
    """
    if now is None:
        now = datetime.now(timezone.utc)
    now_iso = now.isoformat()

    # 1. Durable reservation must exist and be live BEFORE anything else.
    verify_reservation_live_for_invocation(
        bundle=bundle,
        reservation=reservation,
        campaign_root=campaign_root,
        now=now,
    )

    # 2. The capability must be bound to exactly this reservation.
    verify_capability_matches_reservation(
        capability=capability, reservation=reservation
    )

    # 3. Consume the Phase 3 capability atomically. Any drift burns it.
    decision = consume_exploratory_capability(capability, context, now=now_iso)

    recorder = AttemptOutcomeRecorder(
        Path(campaign_root), decision.campaign_id, decision.attempt_id
    )

    # 4. Preserve the exact request bytes before the durable INVOKED
    #    transition (state: RESERVED).
    request_ref = recorder.record_raw_request(prompt.encode("utf-8"), now=now)

    # 5. Persist the durable INVOKED transition -- naming the preserved
    #    request. From here on the attempt is spent and visible even if
    #    this process dies.
    recorder.record_invoked(bundle, now=now, raw_request_reference=request_ref)

    # 6. Issue the one-shot provider permit (requires ledger state INVOKED)
    #    and consume it immediately: the provider may only be entered with
    #    a genuine, consumed, attempt-bound permit.
    permit = issue_provider_permit(
        campaign_root=Path(campaign_root),
        campaign_id=decision.campaign_id,
        attempt_id=decision.attempt_id,
        configuration_id=decision.configuration_id,
        now=now,
    )
    consume_provider_permit(permit, campaign_root=Path(campaign_root))

    # 7. Enter the provider.
    try:
        response = provider(permit=permit, context=context, prompt=prompt)
    except BaseException as exc:
        # The capability is spent forever regardless of what happened.
        burn_exploratory_capability(capability)
        if isinstance(exc, Exception):
            # Ordinary provider failure: durably terminal PROVIDER_FAILED.
            recorder.record_provider_failure(
                str(exc) or exc.__class__.__name__, now=now
            )
        # Interruption-like exceptions (KeyboardInterrupt, SystemExit) leave
        # the durable state INVOKED-incomplete on purpose: the ledger shows
        # the attempt began and never finished; recovery must not pretend a
        # provider failure occurred. The interruption is always re-raised.
        raise
    if not isinstance(response, ProviderResponse):
        raise TypeError(
            "provider must return a ProviderResponse (raw_output bytes + "
            f"usage observations), got {type(response).__name__}"
        )

    # 8. Preserve the raw response before parsing or validating anything.
    recorder.record_raw_output(response.raw_output, now=now)

    # 9. Validate the preserved raw output and record the terminal outcome.
    outcome = validate(response.raw_output)

    artifact_ref = None
    if outcome.artifact_content is not None:
        artifact_ref = recorder.record_produced_artifact(
            outcome.artifact_content, outcome.artifact_filename
        )

    return recorder.record_validation_outcome(
        passed=outcome.passed,
        details=outcome.details,
        validated_output_ref=outcome.validated_output_ref or artifact_ref,
        tokens_observed=(
            response.tokens_observed
            if response.tokens_observed is not None
            else outcome.tokens_observed
        ),
        cost_observed=(
            response.cost_observed if response.cost_observed is not None
            else outcome.cost_observed
        ),
        now=now,
    )
