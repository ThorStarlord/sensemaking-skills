# Schema: Campaign Summary (v1)

The runtime-derived ledger for one campaign: what actually happened, as
opposed to what the policy authorizes. See ADR 0023 §8a, §9f. Append-only.

**This schema is not enforced by any runtime component in this phase.**

## Required fields

| Field | Type | Description |
|---|---|---|
| `summary_schema_version` | string | Must be `"1"`. |
| `campaign_id` | string | |
| `policy_digest` | string (sha256 hex) | The exact policy this summary reports against. |
| `campaign_state` | string enum | One of the campaign lifecycle states (ADR 0023 §8a): `DRAFT`, `AWAITING_HUMAN_APPROVAL`, `APPROVED_NOT_STARTED`, `ACTIVE`, `EXHAUSTED`, `EXPIRED`, `ABORTED`, `COMPLETED`. |
| `campaign_state_history` | list[object{state, at}] | Append-only, full transition history. |
| `reservations_issued` | object{count, ids} | Every `reservation_id` ever issued under this campaign. Never shrinks. |
| `provider_invocations_made` | integer | Count of attempts that reached `INVOKED` or later. |
| `remaining_budget` | object{attempt_slots, provider_invocations} | Computed as policy ceiling minus consumed (ADR 0023 §14); does not include a claimed exact remaining dollar/token figure beyond the soft, post-hoc `tokens_observed`/`cost_observed` totals. |
| `attempts` | list[attempt summary: {attempt_id, configuration_id, state, terminal_at}] | Full list, every attempt ever reserved, regardless of terminal state. Never filtered to only successes. |
| `first_reserved_at` | string (RFC3339), nullable | Null only if `campaign_state` has never left `APPROVED_NOT_STARTED`. |
| `last_activity_at` | string (RFC3339) | |
| `terminal_reason` | string, nullable | Required (non-null) once `campaign_state` is `EXHAUSTED`, `EXPIRED`, `ABORTED`, or `COMPLETED`. |

## Ledger integrity rules (ADR 0023 §6 threat 16, §9f)

- `attempts` must be a superset, by count and by ID, of every
  `reservation_id` in `reservations_issued` — no reservation is ever dropped
  from the summary, including every `ABORTED_BEFORE_INVOCATION` one.
- `provider_invocations_made` must never exceed the policy's
  `max_provider_invocations`; a summary reporting a higher count indicates a
  policy violation to be surfaced, not silently reconciled downward.
- This document never redefines or overrides a policy field (ADR 0023 §9c) —
  it only reports observed/consumed values against policy ceilings which
  remain the sole source of authority.

## Fail-closed rules

- `campaign_state` regressing (e.g. `EXHAUSTED` back to `ACTIVE`): invalid.
- `attempts` count less than `reservations_issued.count`: invalid — implies
  a dropped reservation.
- Unknown `summary_schema_version`: reject.

## Example — EXAMPLE_ONLY_NOT_OPERATIVE

```yaml
summary_schema_version: "1"
campaign_id: "EXP-0000-EXAMPLE"
policy_digest: "0000000000000000000000000000000000000000000000000000000000000000"
campaign_state: "ACTIVE"
campaign_state_history:
  - state: "DRAFT"
    at: "2025-12-30T00:00:00+00:00"
  - state: "AWAITING_HUMAN_APPROVAL"
    at: "2025-12-31T00:00:00+00:00"
  - state: "APPROVED_NOT_STARTED"
    at: "2026-01-01T00:00:00+00:00"
  - state: "ACTIVE"
    at: "2026-01-01T00:00:00+00:00"
reservations_issued:
  count: 2
  ids:
    - "00000000-0000-0000-0000-000000000001"
    - "00000000-0000-0000-0000-000000000002"
provider_invocations_made: 1
remaining_budget:
  attempt_slots: 3
  provider_invocations: 4
attempts:
  - attempt_id: "00000000-0000-0000-0000-000000000001"
    configuration_id: "1111111111111111111111111111111111111111111111111111111111111111"
    state: "VALIDATION_PASSED"
    terminal_at: "2026-01-01T00:03:30+00:00"
  - attempt_id: "00000000-0000-0000-0000-000000000002"
    configuration_id: "1111111111111111111111111111111111111111111111111111111111111111"
    state: "ABORTED_BEFORE_INVOCATION"
    terminal_at: "2026-01-01T00:04:00+00:00"
first_reserved_at: "2026-01-01T00:00:00+00:00"
last_activity_at: "2026-01-01T00:04:00+00:00"
terminal_reason: null
```

This example is authored under the Two-Lane YAML Profile v1 (ADR 0023
§10b): every string-valued field, including enum-like state names, is
quoted. `terminal_reason: null` is the permitted unquoted `null` plain
scalar.
