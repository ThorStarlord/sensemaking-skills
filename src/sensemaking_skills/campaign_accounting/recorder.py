"""Attempt outcome recorder for Phase 4 (#120).

Records lifecycle state transitions (INVOKED, OUTPUT_CAPTURED,
VALIDATION_PASSED, VALIDATION_FAILED, PROVIDER_FAILED,
ABORTED_BEFORE_INVOCATION), preserves raw provider responses atomically
before validation, and writes immutable attempt-result.yaml records.

Crash-safety ordering rules implemented here:

* The provider call must never occur before the durable ``INVOKED``
  transition (``record_invoked`` flushes and fsyncs before returning).
* Raw provider output is written to a temp file, fsynced, then atomically
  renamed to the immutable ``raw-output.*`` path -- only then is the
  ``OUTPUT_CAPTURED`` event appended. A crash mid-write leaves a partial
  ``.tmp-*`` file and no OUTPUT_CAPTURED event, so nothing incomplete is
  ever presented as captured.
* Every file write happens only AFTER the ledger state check passes under
  the campaign lock, so an illegal re-entry (a second validation, a
  provider-failure after a terminal state, a raw-output capture from a
  non-INVOKED state) fails before any existing file is touched.
"""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml

from sensemaking_skills.campaign_validation.models import ValidatedCampaignBundle
from .failure_codes import (
    ARTIFACT_ALREADY_EXISTS,
    ARTIFACT_FILENAME_INVALID,
    ATTEMPT_ALREADY_TERMINAL,
    ATTEMPT_NOT_RESERVED,
    ATTEMPT_STATE_INVALID_TRANSITION,
    BUDGET_EXCEEDED_PROVIDER_INVOCATIONS,
    CAMPAIGN_EXPIRED,
    CAMPAIGN_NOT_ACTIVE,
    RAW_OUTPUT_MISSING_FOR_CAPTURED_STATE,
    RAW_REQUEST_ALREADY_EXISTS,
    RAW_REQUEST_FILENAME_INVALID,
    CampaignAccountingError,
)
from .filenames import (
    validate_artifact_leaf_name,
    validate_produced_artifact_filename,
    validate_raw_output_extension,
)
from .ledger import CampaignLedger, campaign_lock
from .models import (
    EXPLORATORY_CLASSIFICATION,
    AttemptResult,
    AttemptState,
    TERMINAL_STATES,
)
from .reservation import _campaign_cost_token_exhausted


def _latest_attempt_state(events: List[Any], attempt_id: str) -> Optional[str]:
    """Latest state event for ``attempt_id`` among ledger events."""
    latest: Optional[str] = None
    for e in events:
        if e.attempt_id == attempt_id and e.event_type in [s.value for s in AttemptState]:
            latest = e.event_type
    return latest


def _require_state(events: List[Any], attempt_id: str, expected: str) -> None:
    current = _latest_attempt_state(events, attempt_id)
    if current is None:
        raise CampaignAccountingError(
            ATTEMPT_NOT_RESERVED,
            f"Attempt '{attempt_id}' is not reserved in the campaign ledger",
        )
    if current != expected:
        raise CampaignAccountingError(
            ATTEMPT_ALREADY_TERMINAL
            if current in TERMINAL_STATES
            else ATTEMPT_STATE_INVALID_TRANSITION,
            f"Attempt '{attempt_id}' is in state '{current}'; expected "
            f"'{expected}' for this operation",
        )


class AttemptOutcomeRecorder:
    """Records attempt lifecycle progress and durable artifacts."""

    def __init__(self, campaign_root: Path, campaign_id: str, attempt_id: str) -> None:
        self.campaign_root = Path(campaign_root)
        self.campaign_id = campaign_id
        self.attempt_id = attempt_id
        self.campaign_dir = self.campaign_root / campaign_id
        self.attempt_dir = self.campaign_dir / "attempts" / attempt_id
        self.ledger = CampaignLedger(self.campaign_dir, self.campaign_id)

    def _read_reservation_data(self) -> Dict[str, Any]:
        res_file = self.attempt_dir / "reservation.yaml"
        if not res_file.exists():
            raise CampaignAccountingError(
                ATTEMPT_NOT_RESERVED,
                f"Attempt '{self.attempt_id}' has no durable reservation at '{res_file}'",
            )
        with open(res_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _write_yaml(self, rel_name: str, data: Dict[str, Any]) -> None:
        target = self.attempt_dir / rel_name
        with open(target, "w", encoding="utf-8") as f:
            yaml.dump(data, f, sort_keys=False)
            f.flush()
            os.fsync(f.fileno())

    def _write_json(self, rel_name: str, data: Any) -> None:
        target = self.attempt_dir / rel_name
        with open(target, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())

    # ------------------------------------------------------------------ #
    # record_invoked: the durable INVOKED transition, BEFORE provider entry
    # ------------------------------------------------------------------ #

    def record_raw_request(
        self,
        raw: bytes,
        now: Optional[datetime] = None,
    ) -> str:
        """Immutably preserve the exact prompt/request bytes sent to the
        provider (Issue #122: 'Preserve all raw requests').

        The request is written while the attempt is still RESERVED, before
        the durable INVOKED transition and before any provider entry. The
        leaf name is fixed to ``raw-request.txt`` under the frozen leaf
        grammar; the write is temp-file + fsync + atomic rename under the
        campaign lock, and an existing file is never overwritten.
        """
        if now is None:
            now = datetime.now(timezone.utc)
        validate_artifact_leaf_name(
            "raw-request.txt",
            label="raw request filename",
            failure_code=RAW_REQUEST_FILENAME_INVALID,
        )
        target_path = self.attempt_dir / "raw-request.txt"
        temp_path = self.attempt_dir / ".tmp-raw-request.txt"
        rel_ref = (
            f"experiments/campaigns/{self.campaign_id}/attempts/"
            f"{self.attempt_id}/raw-request.txt"
        )
        with campaign_lock(self.campaign_dir):
            events = self.ledger.read_events()
            _require_state(events, self.attempt_id, AttemptState.RESERVED.value)
            if target_path.exists():
                existing = target_path.read_bytes()
                if existing == raw:
                    return rel_ref  # deterministic crash-resume
                raise CampaignAccountingError(
                    RAW_REQUEST_ALREADY_EXISTS,
                    f"attempt '{self.attempt_id}' already preserves a "
                    "different raw request; refusing to overwrite it",
                )
            with open(temp_path, "wb") as f:
                f.write(raw)
                f.flush()
                os.fsync(f.fileno())
            temp_path.replace(target_path)
        return rel_ref

    def record_invoked(
        self,
        bundle: ValidatedCampaignBundle,
        now: Optional[datetime] = None,
        raw_request_reference: Optional[str] = None,
    ) -> None:
        """Record the transition to INVOKED prior to entering the provider.

        Fails closed (with zero provider calls possible) when the attempt
        has no durable reservation, the reservation is not live in the
        ledger, the policy window has expired, the campaign is exhausted on
        observed cost/tokens, or the provider-invocation budget is spent.
        ``raw_request_reference`` (when present) is embedded in the INVOKED
        event payload so the durable record of the invocation names its
        exact preserved request.
        """
        if now is None:
            now = datetime.now(timezone.utc)
        timestamp_str = now.isoformat()

        policy = bundle.policy
        policy_raw = policy.raw

        with campaign_lock(self.campaign_dir):
            events = self.ledger.read_events()

            # The durable reservation file must exist and the ledger must
            # show the attempt as RESERVED right now.
            self._read_reservation_data()
            _require_state(events, self.attempt_id, AttemptState.RESERVED.value)

            # Expiry re-check at the provider boundary.
            validity = policy_raw.get("validity_window") or {}
            if validity:
                not_before = datetime.fromisoformat(validity["not_before"])
                not_after = datetime.fromisoformat(validity["not_after"])
                if now < not_before or now > not_after:
                    raise CampaignAccountingError(
                        CAMPAIGN_EXPIRED,
                        f"Campaign '{self.campaign_id}' is outside validity window ({validity['not_before']} to {validity['not_after']}) at {timestamp_str}",
                    )

            # Soft cost/token ceilings: no further invocation once observed
            # totals cross a declared ceiling.
            exhausted_reason = _campaign_cost_token_exhausted(policy_raw, events)
            if exhausted_reason is not None:
                raise CampaignAccountingError(
                    CAMPAIGN_NOT_ACTIVE,
                    f"Campaign '{self.campaign_id}' is exhausted: {exhausted_reason}",
                )

            # Provider-invocation budget: only INVOKED transitions consume
            # an invocation slot; a pre-invocation abort does not.
            invoked_events = [
                e for e in events if e.event_type == AttemptState.INVOKED.value
            ]
            max_provider_invocations = policy_raw.get("max_provider_invocations", 1)
            if len(invoked_events) >= max_provider_invocations:
                raise CampaignAccountingError(
                    BUDGET_EXCEEDED_PROVIDER_INVOCATIONS,
                    f"Campaign '{self.campaign_id}' has reached max_provider_invocations limit ({max_provider_invocations})",
                )

            # Append INVOKED event (fsynced) before returning to the caller
            # so the provider call can never precede the durable transition.
            payload: Dict[str, Any] = {"provider_invoked_at": timestamp_str}
            if raw_request_reference is not None:
                payload["raw_request_reference"] = raw_request_reference
            self.ledger._append_event_unlocked(
                events=events,
                timestamp=timestamp_str,
                attempt_id=self.attempt_id,
                event_type=AttemptState.INVOKED.value,
                payload=payload,
            )

    # ------------------------------------------------------------------ #
    # record_raw_output: preserve raw bytes BEFORE any parsing/validation
    # ------------------------------------------------------------------ #

    def record_raw_output(
        self,
        raw_data: bytes,
        extension: str = "bin",
        now: Optional[datetime] = None,
    ) -> str:
        """Preserve the raw provider response atomically.

        Sequence: verify the attempt is INVOKED (under lock) -> write the
        exact bytes to a temp file -> fsync -> atomic rename to the
        immutable ``raw-output.<ext>`` path -> append OUTPUT_CAPTURED.

        If the immutable path already exists while the ledger still shows
        INVOKED (a crash between the rename and the event append), the
        existing file is complete (rename only happens after fsync) and the
        capture is resumed by appending the OUTPUT_CAPTURED event -- the
        provider is never called again.
        """
        if now is None:
            now = datetime.now(timezone.utc)
        timestamp_str = now.isoformat()

        # The extension composes the immutable leaf name; it must stay
        # inside the frozen lowercase ASCII leaf grammar so the raw output
        # can never escape the attempt directory (fail-closed, before any
        # write or state read).
        validate_raw_output_extension(extension)

        filename = f"raw-output.{extension}"
        target_path = self.attempt_dir / filename
        temp_path = self.attempt_dir / f".tmp-{filename}"
        rel_ref = (
            f"experiments/campaigns/{self.campaign_id}/attempts/"
            f"{self.attempt_id}/{filename}"
        )

        with campaign_lock(self.campaign_dir):
            events = self.ledger.read_events()
            _require_state(events, self.attempt_id, AttemptState.INVOKED.value)

            if not target_path.exists():
                # Write to temp file and atomic rename. A crash before the
                # rename leaves only a partial .tmp file -- never a
                # plausible-looking raw-output.bin.
                with open(temp_path, "wb") as f:
                    f.write(raw_data)
                    f.flush()
                    os.fsync(f.fileno())
                temp_path.replace(target_path)

            self.ledger._append_event_unlocked(
                events=events,
                timestamp=timestamp_str,
                attempt_id=self.attempt_id,
                event_type=AttemptState.OUTPUT_CAPTURED.value,
                payload={"raw_output_reference": rel_ref},
            )

        return rel_ref

    def record_produced_artifact(
        self,
        content: str,
        filename: str = "produced-artifact.md",
    ) -> str:
        """Immutably preserve the produced candidate artifact.

        Path confinement (merge-blocker correction, Issue #120):

        1. ``filename`` must be a frozen lowercase ASCII leaf name -- no
           separators, drive/UNC qualification, ADS/colon syntax, ``..``,
           trailing dot/space aliases, hidden or empty names
           (``ARTIFACT_FILENAME_INVALID``, raised before any write or state
           read).
        2. The resolved target must sit directly beneath the exact attempt
           directory (defense-in-depth containment re-check).
        3. The ledger state must be ``OUTPUT_CAPTURED``: an artifact is only
           preserved after the raw provider output exists (state-gated).
        4. The target is immutable once created: an existing identical
           artifact is a deterministic crash-resume (the previous run
           crashed after the write, before the terminal ledger event); an
           existing different artifact is rejected
           (``ARTIFACT_ALREADY_EXISTS``) -- never overwritten.
        5. A new artifact is written through temp file + fsync + atomic
           rename under the campaign lock.
        """
        validate_produced_artifact_filename(filename)

        target_path = self.attempt_dir / filename
        try:
            resolved_target = target_path.resolve(strict=False)
            resolved_attempt = self.attempt_dir.resolve(strict=False)
        except OSError as exc:
            raise CampaignAccountingError(
                ARTIFACT_FILENAME_INVALID,
                f"produced artifact filename: cannot resolve {filename!r} "
                f"inside the attempt directory: {exc}",
            ) from exc
        if resolved_target.parent != resolved_attempt:
            raise CampaignAccountingError(
                ARTIFACT_FILENAME_INVALID,
                f"produced artifact filename: resolved target "
                f"'{resolved_target}' is not directly beneath the attempt "
                f"directory '{resolved_attempt}'",
            )

        payload = content.encode("utf-8")

        with campaign_lock(self.campaign_dir):
            events = self.ledger.read_events()
            # An artifact is preserved only after raw output was captured.
            _require_state(events, self.attempt_id, AttemptState.OUTPUT_CAPTURED.value)

            if target_path.exists():
                existing = target_path.read_bytes()
                if existing == payload:
                    # Deterministic crash-resume: an identical artifact was
                    # already preserved before any terminal ledger event;
                    # nothing is rewritten, nothing is overwritten.
                    return self._artifact_ref(filename)
                raise CampaignAccountingError(
                    ARTIFACT_ALREADY_EXISTS,
                    f"attempt '{self.attempt_id}' already preserves a "
                    f"different artifact at '{filename}'; refusing to "
                    f"overwrite it",
                )

            temp_path = self.attempt_dir / f".tmp-{filename}"
            with open(temp_path, "wb") as f:
                f.write(payload)
                f.flush()
                os.fsync(f.fileno())
            temp_path.replace(target_path)

        return self._artifact_ref(filename)

    def _artifact_ref(self, filename: str) -> str:
        return (
            f"experiments/campaigns/{self.campaign_id}/attempts/"
            f"{self.attempt_id}/{filename}"
        )

    # ------------------------------------------------------------------ #
    # record_validation_outcome: VALIDATION_PASSED / VALIDATION_FAILED
    # ------------------------------------------------------------------ #

    def record_validation_outcome(
        self,
        passed: bool,
        details: Any,
        validated_output_ref: Optional[str] = None,
        tokens_observed: Optional[int] = None,
        cost_observed: Optional[Dict[str, Any]] = None,
        now: Optional[datetime] = None,
    ) -> AttemptResult:
        """Record the validation result and write attempt-result.yaml.

        The ledger state is verified (must be OUTPUT_CAPTURED) BEFORE any
        file is written, so a second call on a terminal attempt fails
        without overwriting the existing result. ``tokens_observed`` and
        ``cost_observed`` are post-hoc measurements recorded into the
        ledger event payload for the summary projection.
        """
        if now is None:
            now = datetime.now(timezone.utc)
        timestamp_str = now.isoformat()

        target_state = (
            AttemptState.VALIDATION_PASSED.value
            if passed
            else AttemptState.VALIDATION_FAILED.value
        )

        with campaign_lock(self.campaign_dir):
            events = self.ledger.read_events()
            _require_state(events, self.attempt_id, AttemptState.OUTPUT_CAPTURED.value)
            attempt_events = [e for e in events if e.attempt_id == self.attempt_id]

            # Build full state history from the ledger.
            history = []
            provider_invoked_at = None
            raw_output_ref = None

            for e in attempt_events:
                if e.event_type in [s.value for s in AttemptState]:
                    history.append({"state": e.event_type, "at": e.timestamp})
                if e.event_type == AttemptState.INVOKED.value:
                    provider_invoked_at = e.payload.get("provider_invoked_at", e.timestamp)
                if e.event_type == AttemptState.OUTPUT_CAPTURED.value:
                    raw_output_ref = e.payload.get("raw_output_reference")

            if not raw_output_ref:
                raise CampaignAccountingError(
                    RAW_OUTPUT_MISSING_FOR_CAPTURED_STATE,
                    f"Cannot reach validation state for attempt '{self.attempt_id}': raw output reference is missing",
                )

            history.append({"state": target_state, "at": timestamp_str})

            val_outcome = {"passed": passed, "details": details}

            # Write validation-result.json, then attempt-result.yaml (each
            # fsynced), then the ledger event.
            self._write_json("validation-result.json", val_outcome)

            res_data = self._read_reservation_data()

            result = AttemptResult(
                attempt_id=self.attempt_id,
                campaign_id=self.campaign_id,
                configuration_id=res_data["configuration_id"],
                state=target_state,
                state_history=history,
                provider_invoked_at=provider_invoked_at,
                raw_output_reference=raw_output_ref,
                validated_output_reference=validated_output_ref,
                validation_outcome=val_outcome,
                tokens_observed=tokens_observed,
                cost_observed=cost_observed,
                terminal_at=timestamp_str,
                classification=EXPLORATORY_CLASSIFICATION,
            )

            self._write_yaml("attempt-result.yaml", result.to_dict())

            self.ledger._append_event_unlocked(
                events=events,
                timestamp=timestamp_str,
                attempt_id=self.attempt_id,
                event_type=target_state,
                payload={
                    "passed": passed,
                    "validation_outcome": val_outcome,
                    "terminal_at": timestamp_str,
                    "tokens_observed": tokens_observed,
                    "cost_observed": cost_observed,
                },
            )

            return result

    # ------------------------------------------------------------------ #
    # record_provider_failure: PROVIDER_FAILED (invocation began)
    # ------------------------------------------------------------------ #

    def record_provider_failure(
        self,
        details: str,
        now: Optional[datetime] = None,
        tokens_observed: Optional[int] = None,
        cost_observed: Optional[Dict[str, Any]] = None,
    ) -> AttemptResult:
        """Record the PROVIDER_FAILED terminal outcome.

        Only legal from INVOKED: the provider boundary was entered but no
        usable output exists. The ledger state is verified before any file
        is written.
        """
        if now is None:
            now = datetime.now(timezone.utc)
        timestamp_str = now.isoformat()

        with campaign_lock(self.campaign_dir):
            events = self.ledger.read_events()
            _require_state(events, self.attempt_id, AttemptState.INVOKED.value)
            attempt_events = [e for e in events if e.attempt_id == self.attempt_id]

            history = []
            provider_invoked_at = None
            for e in attempt_events:
                if e.event_type in [s.value for s in AttemptState]:
                    history.append({"state": e.event_type, "at": e.timestamp})
                if e.event_type == AttemptState.INVOKED.value:
                    provider_invoked_at = e.payload.get("provider_invoked_at", e.timestamp)

            target_state = AttemptState.PROVIDER_FAILED.value
            history.append({"state": target_state, "at": timestamp_str})

            res_data = self._read_reservation_data()

            result = AttemptResult(
                attempt_id=self.attempt_id,
                campaign_id=self.campaign_id,
                configuration_id=res_data["configuration_id"],
                state=target_state,
                state_history=history,
                provider_invoked_at=provider_invoked_at,
                raw_output_reference=None,
                validated_output_reference=None,
                validation_outcome=None,
                tokens_observed=tokens_observed,
                cost_observed=cost_observed,
                terminal_at=timestamp_str,
                classification=EXPLORATORY_CLASSIFICATION,
            )

            self._write_yaml("attempt-result.yaml", result.to_dict())

            self.ledger._append_event_unlocked(
                events=events,
                timestamp=timestamp_str,
                attempt_id=self.attempt_id,
                event_type=target_state,
                payload={
                    "details": details,
                    "terminal_at": timestamp_str,
                    "tokens_observed": tokens_observed,
                    "cost_observed": cost_observed,
                },
            )

            return result

    # ------------------------------------------------------------------ #
    # record_pre_invocation_abort: ABORTED_BEFORE_INVOCATION
    # ------------------------------------------------------------------ #

    def record_pre_invocation_abort(
        self,
        reason: str,
        now: Optional[datetime] = None,
    ) -> AttemptResult:
        """Record the ABORTED_BEFORE_INVOCATION terminal outcome.

        Only legal from RESERVED: the provider boundary was never entered.
        The attempt slot stays consumed. The ledger state is verified
        before any file is written.
        """
        if now is None:
            now = datetime.now(timezone.utc)
        timestamp_str = now.isoformat()

        with campaign_lock(self.campaign_dir):
            events = self.ledger.read_events()
            _require_state(events, self.attempt_id, AttemptState.RESERVED.value)
            attempt_events = [e for e in events if e.attempt_id == self.attempt_id]

            history = []
            for e in attempt_events:
                if e.event_type in [s.value for s in AttemptState]:
                    history.append({"state": e.event_type, "at": e.timestamp})

            target_state = AttemptState.ABORTED_BEFORE_INVOCATION.value
            history.append({"state": target_state, "at": timestamp_str})

            res_data = self._read_reservation_data()

            result = AttemptResult(
                attempt_id=self.attempt_id,
                campaign_id=self.campaign_id,
                configuration_id=res_data["configuration_id"],
                state=target_state,
                state_history=history,
                provider_invoked_at=None,
                raw_output_reference=None,
                validated_output_reference=None,
                validation_outcome=None,
                terminal_at=timestamp_str,
                classification=EXPLORATORY_CLASSIFICATION,
            )

            self._write_yaml("attempt-result.yaml", result.to_dict())

            self.ledger._append_event_unlocked(
                events=events,
                timestamp=timestamp_str,
                attempt_id=self.attempt_id,
                event_type=target_state,
                payload={"reason": reason, "terminal_at": timestamp_str},
            )

            return result
