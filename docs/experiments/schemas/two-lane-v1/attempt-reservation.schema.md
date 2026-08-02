# Schema: Attempt Reservation (v1)

The durable record created before an attempt reaches the provider. See ADR
0023 §8b, §9e, §14. A reservation is always visible, even if it aborts
before invocation.

**This schema is not enforced by any runtime component in this phase.**

## Required fields

| Field | Type | Immutable once set | Description |
|---|---|---|---|
| `reservation_schema_version` | string | yes | Must be `"1"`. |
| `reservation_id` | string (UUID or equivalent) | yes | Allocated at reservation time. |
| `attempt_id` | string (UUID or equivalent) | yes | 1:1 with `reservation_id`, allocated together. Never reused, never reassigned to a different provider call. |
| `campaign_id` | string | yes | |
| `configuration_id` | string (sha256 hex) | yes | References `configuration-identity.schema.md`. |
| `reserved_at` | string (RFC3339) | yes | Strictly before any provider call for this `attempt_id`. |
| `state` | string enum | append-only history | One of the attempt lifecycle states (ADR 0023 §8b): `RESERVED`, `ABORTED_BEFORE_INVOCATION`, `INVOKED`, `PROVIDER_FAILED`, `OUTPUT_CAPTURED`, `VALIDATION_FAILED`, `VALIDATION_PASSED`. |
| `state_history` | list[object{state, at}] | append-only | Every transition, in order. Never truncated or rewritten. |
| `terminal_states` | list[string] | fixed | Always exactly `["ABORTED_BEFORE_INVOCATION", "PROVIDER_FAILED", "VALIDATION_FAILED", "VALIDATION_PASSED"]` — included so a consumer can check terminality by membership without hardcoding the transition graph. |

## Legal transitions (restated from ADR 0023 §8b)

`RESERVED -> ABORTED_BEFORE_INVOCATION` (terminal) or `RESERVED -> INVOKED`.
No other transition originates at `RESERVED`. See `attempt-result.schema.md`
for transitions after `INVOKED`.

## Budget interaction (ADR 0023 §14)

- Creating a reservation consumes one **attempt slot** against the
  campaign's `max_attempt_slots` and one slot against
  `max_attempts_per_configuration` for this `configuration_id`, immediately
  at `reserved_at` — before any provider call.
- Transitioning to `ABORTED_BEFORE_INVOCATION` does **not** refund or
  re-consume anything; the attempt slot remains consumed (this is what
  bounds reservation churn), but no provider-invocation slot or cost/token
  budget is ever consumed for a reservation that never reached `INVOKED`.
- Transitioning to `INVOKED` additionally consumes one provider-invocation
  slot against `max_provider_invocations`.

## Fail-closed rules

- A reservation with `state: INVOKED` or later but no `reserved_at`
  strictly preceding the first `INVOKED` entry in `state_history`: invalid.
- A `reservation_id` or `attempt_id` appearing on more than one reservation
  document: invalid (ID reuse, ADR 0023 §6 threat 11).
- `configuration_id` not present in a corresponding
  `configuration-identity` document: invalid.

## Example — EXAMPLE_ONLY_NOT_OPERATIVE

```yaml
reservation_schema_version: "1"
reservation_id: "00000000-0000-0000-0000-000000000001"
attempt_id: "00000000-0000-0000-0000-000000000001"
campaign_id: EXP-0000-EXAMPLE
configuration_id: "1111111111111111111111111111111111111111111111111111111111111111"
reserved_at: "2026-01-01T00:00:00+00:00"
state: RESERVED
state_history:
  - state: RESERVED
    at: "2026-01-01T00:00:00+00:00"
terminal_states:
  - ABORTED_BEFORE_INVOCATION
  - PROVIDER_FAILED
  - VALIDATION_FAILED
  - VALIDATION_PASSED
```
