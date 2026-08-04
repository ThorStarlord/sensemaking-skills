"""Durable campaign accounting for two-lane v1 (Phase 4, #120).

Public API:

* `DurableReservationManager` -- creates immutable, on-disk attempt reservations before provider calls.
* `CampaignLedger` -- append-only, tamper-evident hash-chained event ledger (`ledger.jsonl`).
* `AttemptOutcomeRecorder` -- records lifecycle outcomes (INVOKED, OUTPUT_CAPTURED, VALIDATION_*, etc.) and raw outputs.
* `CampaignSummaryGenerator` -- derives authoritative `campaign-summary.yaml` projections.
* `AttemptRecovery` -- reconciles uninvoked/interrupted attempts post-crash.
* `CampaignAccountingError` -- single exception for accounting/ledger/budget violations.
"""

from .failure_codes import (
    ATTEMPT_ALREADY_TERMINAL,
    ATTEMPT_DIRECTORY_EXISTS,
    ATTEMPT_ID_NOT_UUID,
    ATTEMPT_NOT_RESERVED,
    ATTEMPT_STATE_INVALID_TRANSITION,
    BUDGET_EXCEEDED_ATTEMPT_SLOTS,
    BUDGET_EXCEEDED_CONFIGURATION_SLOTS,
    BUDGET_EXCEEDED_PROVIDER_INVOCATIONS,
    CAMPAIGN_EXPIRED,
    CAMPAIGN_LEDGER_CORRUPT,
    CAMPAIGN_LEDGER_HASH_MISMATCH,
    CAMPAIGN_LEDGER_SEQUENCE_DISCONTINUITY,
    CAMPAIGN_LEDGER_TRUNCATED,
    CAMPAIGN_NOT_ACTIVE,
    CAMPAIGN_SUMMARY_MISSING_ATTEMPT_DIR,
    CAMPAIGN_SUMMARY_ORPHAN_RESULT,
    CONFIGURATION_ID_MISMATCH,
    CROSS_DOCUMENT_CAMPAIGN_ID_MISMATCH,
    RAW_OUTPUT_MISSING_FOR_CAPTURED_STATE,
    RESERVATION_ATTEMPT_MISMATCH,
    RESERVATION_CAMPAIGN_MISMATCH,
    RESERVATION_CONFIGURATION_MISMATCH,
    RESERVATION_EXISTS_FOR_ATTEMPT,
    RESERVATION_EXPIRED,
    RESERVATION_NOT_GENUINE,
    RESERVATION_NOT_LIVE,
    RESERVATION_REQUIRED_BEFORE_INVOCATION,
    CampaignAccountingError,
)
from .boundary import (
    invoke_exploratory_attempt,
    verify_capability_matches_reservation,
    verify_reservation_live_for_invocation,
)
from .digests import GENESIS_HASH, compute_event_hash
from .ledger import CampaignLedger, campaign_lock
from .models import (
    EXPLORATORY_CLASSIFICATION,
    LEGAL_TRANSITIONS,
    TERMINAL_STATES,
    AttemptReservation,
    AttemptResult,
    AttemptState,
    CampaignSummary,
    LedgerEvent,
    StateHistoryEntry,
    ValidationOutcome,
    is_genuine_attempt_reservation,
    validate_state_transition,
)
from .recorder import AttemptOutcomeRecorder
from .recovery import AttemptRecovery
from .reservation import DurableReservationManager, verify_cross_document_campaign_id
from .summary import CampaignSummaryGenerator

__all__ = [
    "ATTEMPT_ALREADY_TERMINAL",
    "ATTEMPT_DIRECTORY_EXISTS",
    "ATTEMPT_ID_NOT_UUID",
    "ATTEMPT_NOT_RESERVED",
    "ATTEMPT_STATE_INVALID_TRANSITION",
    "BUDGET_EXCEEDED_ATTEMPT_SLOTS",
    "BUDGET_EXCEEDED_CONFIGURATION_SLOTS",
    "BUDGET_EXCEEDED_PROVIDER_INVOCATIONS",
    "CAMPAIGN_EXPIRED",
    "CAMPAIGN_LEDGER_CORRUPT",
    "CAMPAIGN_LEDGER_HASH_MISMATCH",
    "CAMPAIGN_LEDGER_SEQUENCE_DISCONTINUITY",
    "CAMPAIGN_LEDGER_TRUNCATED",
    "CAMPAIGN_NOT_ACTIVE",
    "CAMPAIGN_SUMMARY_MISSING_ATTEMPT_DIR",
    "CAMPAIGN_SUMMARY_ORPHAN_RESULT",
    "CONFIGURATION_ID_MISMATCH",
    "CROSS_DOCUMENT_CAMPAIGN_ID_MISMATCH",
    "EXPLORATORY_CLASSIFICATION",
    "GENESIS_HASH",
    "LEGAL_TRANSITIONS",
    "RAW_OUTPUT_MISSING_FOR_CAPTURED_STATE",
    "RESERVATION_ATTEMPT_MISMATCH",
    "RESERVATION_CAMPAIGN_MISMATCH",
    "RESERVATION_CONFIGURATION_MISMATCH",
    "RESERVATION_EXISTS_FOR_ATTEMPT",
    "RESERVATION_EXPIRED",
    "RESERVATION_NOT_GENUINE",
    "RESERVATION_NOT_LIVE",
    "RESERVATION_REQUIRED_BEFORE_INVOCATION",
    "TERMINAL_STATES",
    "AttemptOutcomeRecorder",
    "AttemptRecovery",
    "AttemptReservation",
    "AttemptResult",
    "AttemptState",
    "CampaignAccountingError",
    "CampaignLedger",
    "CampaignSummary",
    "CampaignSummaryGenerator",
    "DurableReservationManager",
    "LedgerEvent",
    "StateHistoryEntry",
    "ValidationOutcome",
    "campaign_lock",
    "compute_event_hash",
    "invoke_exploratory_attempt",
    "is_genuine_attempt_reservation",
    "validate_state_transition",
    "verify_capability_matches_reservation",
    "verify_cross_document_campaign_id",
    "verify_reservation_live_for_invocation",
]
