# Phase 4 implementation notes — durable campaign accounting and the attempt ledger

Program: Issue #116. This phase: Issue #120 (Phase 4). Governing contracts:
ADR 0023 (Two-Lane Experiment Authorization), ADR 0022 (Gate A), and the
schema-contract Markdown files in `docs/experiments/schemas/two-lane-v1/`.
This document describes the runtime implementation added in this phase; it
is not itself a contract — ADR 0023 and the schema contracts remain
normative.

## Scope

Phase 3 made an exploratory provider invocation *authorized*; Phase 4 makes
it *durable*. The system now proves — even after a crash — exactly what was
reserved, invoked, spent, returned, validated, failed, or abandoned, with
no attempt able to disappear, be retried under a reused identity, or be
selectively omitted from the campaign summary.

It implements:

* an append-only, tamper-evident campaign ledger (`ledger.jsonl`) with a
  JCS SHA-256 hash chain;
* durable, immutable attempt reservations created strictly before any
  provider call, with multi-dimensional budget enforcement;
* an attempt state machine recorded as an append-only event history;
* atomic raw-output preservation before any parsing or validation;
* a provider-boundary seam that composes the Phase 3 capability with the
  durable reservation (`invoke_exploratory_attempt`);
* crash recovery for reservations that never reached the provider;
* a campaign summary that is a *derived projection* of the ledger and fails
  closed on orphan results, missing attempt directories, or a malformed
  ledger.

It deliberately stops before: preparing or running EXP-0001; modifying
Evidence 0016; distributed locking; multi-host execution; target mutation;
automatic merge; autonomous campaign orchestration; and wiring
`skill_executor.py` to the new seam (the seam is exercised by tests with a
spy provider; production executor wiring is a later phase's work).

## Production module location

| Location | Responsibility |
|---|---|
| `src/sensemaking_skills/campaign_accounting/` | The Phase 4 package: failure codes, digest chaining, ledger, reservation manager, outcome recorder, provider boundary, summary projection, recovery |

## The central invariant

```text
No durable reservation
        ↓
No capability
        ↓
No provider invocation
```

`DurableReservationManager.reserve_attempt` is the first irreversible act:
it consumes an attempt slot (never refunded, even for an
`ABORTED_BEFORE_INVOCATION`), creates the attempt directory exclusively,
persists `reservation.yaml` + `request-metadata.json` (flushed and
fsynced), and appends the `RESERVED` ledger event — all under one campaign
lock, so two processes can never both believe capacity existed.

`reservation_id` and `attempt_id` are allocated together and remain
one-to-one forever; both are strict lowercase UUIDs (matching the Phase 3
mint requirement). An `attempt_id` is never reused after any transition.

## The attempt state machine

```text
RESERVED
   ├──→ ABORTED_BEFORE_INVOCATION     terminal
   └──→ INVOKED
           ├──→ PROVIDER_FAILED        terminal
           └──→ OUTPUT_CAPTURED
                    ├──→ VALIDATION_FAILED   terminal
                    └──→ VALIDATION_PASSED   terminal
```

The ledger stores every transition as an event; the final record retains
the whole history (`state_history`), so the record explains *where* and
*why* an attempt failed instead of collapsing to one mutable status. A
terminal state never transitions again, and `INVOKED` is entered at most
once per `attempt_id` — a second provider call is always a new attempt with
a new reservation, a new budget charge, and a new history.

## The ledger

`CampaignLedger` maintains `ledger.jsonl` under a cross-process lock
(`ledger.lock`; `msvcrt.locking` on Windows, `fcntl.flock` on POSIX —
Phase 4 v1 is one-process locking, concurrency ceiling one). Every event
carries:

```text
sequence, timestamp, campaign_id, attempt_id, event_type, payload,
previous_event_hash, event_hash
```

with `event_hash = SHA-256(JCS(event without event_hash))` and
`previous_event_hash` chaining every event to its predecessor (genesis =
64 zero bytes). Reading validates, in order: JSON well-formedness, required
fields, sequence continuity, campaign-ID match, previous-hash chain,
recomputed event hash, and transition legality. A truncated final line, a
rewritten payload, a reordered sequence, or an illegal transition raises
`CAMPAIGN_LEDGER_TRUNCATED` / `CAMPAIGN_LEDGER_HASH_MISMATCH` /
`CAMPAIGN_LEDGER_SEQUENCE_DISCONTINUITY` / `CAMPAIGN_LEDGER_CORRUPT` —
never a best-effort partial read.

## Crash-safe ordering

The provider call never occurs before the durable `INVOKED` transition:
`record_invoked` verifies the reservation is live (reservation file +
ledger state `RESERVED`), re-checks the policy window and the invocation
budget, appends the `INVOKED` event, and fsyncs — only then may the
provider run. Consequences per crash point:

| Crash point | Durable state | Recovery |
|---|---|---|
| Before reservation | nothing | no attempt, no budget consumed |
| After `RESERVED` | `RESERVED` | `ABORTED_BEFORE_INVOCATION`; slot stays consumed |
| After capability consumption, before `INVOKED` | `RESERVED` | same; the process-local capability died with the process |
| After durable `INVOKED` | `INVOKED` | left as-is: visible, spent, never retried under the same attempt ID |
| During raw-output write | `INVOKED` + partial `.tmp-*` file | no `OUTPUT_CAPTURED` event; nothing incomplete is ever presented as captured |
| After raw-output rename, before event | `INVOKED` + complete `raw-output.*` | capture resumes by appending `OUTPUT_CAPTURED` (validation may resume; the provider is never called again) |
| After `OUTPUT_CAPTURED`, before validation | `OUTPUT_CAPTURED` | validation may be resumed from the preserved raw output |

The conservative window is accepted by design: recording `INVOKED` before
the network call may overcount an invocation that never left the machine —
possible overcount is safer than an invisible call.

## Raw output preservation

```text
provider response
        ↓
write exact bytes to .tmp file
        ↓
fsync
        ↓
atomic rename to raw-output.<ext>
        ↓
append OUTPUT_CAPTURED event
        ↓
extract produced artifact
        ↓
validate
```

The runtime keeps three distinguishable artifacts: raw provider output,
produced artifact, and validation result. A validation state with no raw
output is unreachable (the state machine forbids `INVOKED → VALIDATION_*`).

## Budget accounting

* **Attempt slots** — every `RESERVED` event consumes one; aborts, failures,
  interruptions, and successes all count; never refunded.
* **Provider-invocation slots** — every `INVOKED` transition consumes one;
  a pre-invocation abort does not.
* **Per-configuration slots** — reservations grouped by exact
  `configuration_id`.
* **Concurrency** — nonterminal attempts (`RESERVED`, `INVOKED`,
  `OUTPUT_CAPTURED`); v1 enforces an effective ceiling of one.
* **Expiry** — the policy `validity_window` is checked at reservation AND
  at the provider boundary; outside the window, `CAMPAIGN_EXPIRED`.
* **Cost/token ceilings** — soft and post-hoc (ADR 0023 §14). Observed
  tokens/cost are recorded in terminal event payloads; once the observed
  total crosses a declared ceiling the campaign becomes `EXHAUSTED` and
  accepts no further reservations or invocations. The implementation never
  claims exact pre-invocation dollar-cost enforcement.

## The provider boundary

`invoke_exploratory_attempt` (in `boundary.py`) is the single seam:

```text
verify reservation exists and is live (durable, ledger-checked)
verify capability matches reservation (attempt/campaign/configuration)
consume capability (Phase 3, atomic, exactly one winner)
persist INVOKED (durable, fsynced)
enter provider
preserve raw output atomically
validate and persist the terminal outcome
```

The boundary rejects: no reservation; a reservation-shaped mapping or a
reconstructed object (`AttemptReservation` is sealed; only
`reserve_attempt` can produce a genuine one); a reservation from another
campaign or configuration; a capability bound to another attempt; an
expired, already-invoked, or terminal reservation; and any Phase 3 binding
drift (which burns the capability).

Interruption handling (Phase 3 follow-up #2): the provider call is wrapped
so that any `BaseException` first burns the capability (spent forever),
then — for ordinary `Exception`s — records `PROVIDER_FAILED` durably, and
for interruption-like exceptions (`KeyboardInterrupt`, `SystemExit`)
leaves the durable state `INVOKED`-incomplete (visible and spent, never
fabricated into a provider failure), then re-raises. Nothing swallows
shutdown signals; interruption cannot erase the attempt.

Retry is always a new attempt: new reservation, new attempt ID, new budget
charge, new history. There is no hidden retry, no silent repair, no
fallback inside an attempt.

## The campaign summary

`CampaignSummaryGenerator` derives `campaign-summary.yaml` exclusively from
the ledger and its attempt directories, under the lock:

1. validate the entire ledger (hash chain, sequence, transitions);
2. reject orphan results (an `attempt-result.yaml` whose attempt has no
   `RESERVED` event → `CAMPAIGN_SUMMARY_ORPHAN_RESULT`);
3. reject missing attempt directories (a `RESERVED` event whose directory
   is gone → `CAMPAIGN_SUMMARY_MISSING_ATTEMPT_DIR`);
4. count reservations and invocations from events;
5. include every attempt — successful, failed, aborted, and
   incomplete/crash-visible — with `terminal_at` only when terminal;
6. report remaining budget, including soft cost/token ceilings and
   observed totals;
7. derive `APPROVED_NOT_STARTED` / `ACTIVE` / `EXPIRED` / `EXHAUSTED`;
8. write atomically (temp file + rename).

There is deliberately no `successes_only` mode; selective omission is one
of the explicit threats this phase closes.

## Recovery

`AttemptRecovery.recover_uninvoked_reservations` classifies attempts whose
latest ledger state is `RESERVED` as `ABORTED_BEFORE_INVOCATION`
(attempt slot stays consumed). It never touches `INVOKED` or
`OUTPUT_CAPTURED` attempts — those remain visible and incomplete, and a
validation may be resumed from preserved raw output.

## Decisions frozen in this phase

* Ledger format: one append-only `ledger.jsonl`, JCS-canonicalized JSON
  lines, SHA-256 hash chain; genesis = 64 zero bytes.
* Flush policy: every durable write is `flush()` + `os.fsync()` before the
  next step; summaries and raw outputs are written via temp file + atomic
  rename.
* Locking: one `ledger.lock` per campaign; `msvcrt` on Windows, `fcntl` on
  POSIX; no distributed coordination.
* Concurrency: effective ceiling one (v1 limitation, per Issue #120).
* Attempt identity: strict lowercase UUIDs; `reservation_id == attempt_id`
  (1:1, never reassigned).
* Cost/token ceilings: soft, post-hoc; never claimed as pre-call hard
  limits.
* Resume rules: only validation resumes; a provider call is never repeated
  for an attempt.

## TDD and test layout

All suites were written red first and pass at the exact head:

| Suite | Coverage |
|---|---|
| `tests/campaign_accounting/test_ledger.py` | Hash chain, sequence, truncation, tampering, illegal transitions |
| `tests/campaign_accounting/test_reservation.py` | Durable reservations, cross-document consistency, budgets, concurrency, expiry, duplicate IDs |
| `tests/campaign_accounting/test_recorder.py` | Lifecycle transitions, raw-output preservation, validation results, provider failures, pre-invocation aborts |
| `tests/campaign_accounting/test_boundary.py` | `invoke_exploratory_attempt`: zero-provider-call denial paths, durable-INVOKED-before-provider, burn on failure, interruption handling, no hidden retry, retry-as-new-attempt |
| `tests/campaign_accounting/test_summary.py` / `test_summary_integrity.py` | Complete enumeration, fail-closed reconciliation, EXPIRED/EXHAUSTED, soft ceilings, atomic writes |
| `tests/campaign_accounting/test_recovery.py` | Crash classification, idempotency, resume-validation |
| `tests/campaign_accounting/test_crash_safety.py` | Real subprocess kills (`os._exit`) after reservation and after INVOKED: no attempt can be erased, no ID reused |

## Verification summary

* Phase 4 suites: 66 passed / 0 failed (including subprocess crash tests).
* Phase 3 suites + canonical boundary suites remain green (no regression;
  Phase 4 does not modify `skill_executor.py`, `gate_a_authorization.py`,
  or the canonical Gate A path).
* No `EXP-*` campaign state is created by the suites; every test uses a
  spy provider and asserts zero provider calls on every denial path. No
  real provider is ever invoked, and EXP-0001 is not prepared or executed.

Stop marker for this phase:

```text
CAMPAIGN_LEDGER_PR_READY_FOR_REVIEW
```
