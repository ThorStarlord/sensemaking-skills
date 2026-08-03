# Schema: Attempt Result (v1)

The outcome record for one attempt, from `INVOKED` (or
`ABORTED_BEFORE_INVOCATION`) to a terminal state. Extends the reservation
(same `attempt_id`). See ADR 0023 §8b, §9e, §11, §14.

**This schema is not enforced by any runtime component in this phase.**

## Required fields

| Field | Type | Runtime-derived | Description |
|---|---|---|---|
| `result_schema_version` | string | no | Must be `"1"`. |
| `attempt_id` | string (UUID) | no | Must match an existing `attempt-reservation` document's `attempt_id`. |
| `campaign_id` | string | no | |
| `configuration_id` | string (sha256 hex) | no | |
| `state` | string enum | yes | Current/terminal state, per ADR 0023 §8b. |
| `state_history` | list[object{state, at}] | yes | Full history, superset of the reservation's history at handoff, append-only. |
| `provider_invoked_at` | string (RFC3339), nullable | yes | Null only when `state == ABORTED_BEFORE_INVOCATION`. Present and non-null for every state from `INVOKED` onward. |
| `raw_output_reference` | string (path or content-address), nullable | yes | Reference to the unprocessed provider output. Null only for `ABORTED_BEFORE_INVOCATION` and `PROVIDER_FAILED` (no output exists). Required (non-null) once `state` reaches `OUTPUT_CAPTURED` or later — omitting this while claiming a captured/validated state is invalid (ADR 0023 §6 threat 19). |
| `validated_output_reference` | string (path), nullable | yes | Reference to the post-validation artifact. Present only once `state` is `VALIDATION_PASSED` (or `VALIDATION_FAILED` with a partial artifact retained for inspection). |
| `validation_outcome` | object{passed, details}, nullable | yes | Present once `state` is `VALIDATION_FAILED` or `VALIDATION_PASSED`. |
| `classification` | string enum | no | Must be exactly `EXPLORATORY_NOT_CANONICAL_EVIDENCE` on every attempt result produced under this schema (ADR 0023 §11). |
| `tokens_observed` | integer, nullable | yes | Post-hoc measurement (ADR 0023 §14). Null for `ABORTED_BEFORE_INVOCATION`. |
| `cost_observed` | object{amount, currency}, nullable | yes | Post-hoc measurement. Never presented as a pre-call guarantee. |
| `terminal_at` | string (RFC3339), nullable | yes | Set exactly when `state` first enters a terminal value; never updated again. |

## Terminal-state invariants (ADR 0023 §7, §9)

- Once `state` is one of `ABORTED_BEFORE_INVOCATION`, `PROVIDER_FAILED`,
  `VALIDATION_FAILED`, or `VALIDATION_PASSED`, no further transition is
  legal for this `attempt_id`. A retry is always a new `attempt_id` with its
  own new reservation.
- A `PROVIDER_FAILED`, `VALIDATION_FAILED`, or `ABORTED_BEFORE_INVOCATION`
  result is preserved permanently, identically to a `VALIDATION_PASSED`
  result — no schema field or consumer may omit, archive-and-hide, or
  soft-delete a failed/aborted attempt result.

## Fail-closed rules

- `classification` missing or not exactly `EXPLORATORY_NOT_CANONICAL_EVIDENCE`:
  invalid — this schema never produces canonical evidence.
- `state` regressing to an earlier value relative to `state_history`:
  invalid.
- `raw_output_reference` null while `state` is `OUTPUT_CAPTURED`,
  `VALIDATION_FAILED`, or `VALIDATION_PASSED`: invalid.
- `attempt_id` not matching a known reservation: invalid — no
  reservation-less attempt result is legal (ADR 0023 §6 threat 12).

## Example — EXAMPLE_ONLY_NOT_OPERATIVE

```yaml
result_schema_version: "1"
attempt_id: "00000000-0000-0000-0000-000000000001"
campaign_id: "EXP-0000-EXAMPLE"
configuration_id: "1111111111111111111111111111111111111111111111111111111111111111"
state: "VALIDATION_PASSED"
state_history:
  - state: "RESERVED"
    at: "2026-01-01T00:00:00+00:00"
  - state: "INVOKED"
    at: "2026-01-01T00:00:05+00:00"
  - state: "OUTPUT_CAPTURED"
    at: "2026-01-01T00:03:00+00:00"
  - state: "VALIDATION_PASSED"
    at: "2026-01-01T00:03:30+00:00"
provider_invoked_at: "2026-01-01T00:00:05+00:00"
raw_output_reference: "experiments/campaigns/EXP-0000-EXAMPLE/attempts/00000000-0000-0000-0000-000000000001/raw-output.example"
validated_output_reference: "experiments/campaigns/EXP-0000-EXAMPLE/attempts/00000000-0000-0000-0000-000000000001/validated-output.example.md"
validation_outcome:
  passed: true
  details: "EXAMPLE ONLY: illustrative validator summary."
classification: "EXPLORATORY_NOT_CANONICAL_EVIDENCE"
tokens_observed: 12345
cost_observed:
  amount: "0.00"
  currency: "USD"
terminal_at: "2026-01-01T00:03:30+00:00"
```

This example is authored under the Two-Lane YAML Profile v1 (ADR 0023
§10b): every string-valued field, including enum-like state names and
`classification`, is quoted.
