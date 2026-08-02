# Schema: Campaign Policy (v1)

Immutable authority-and-limits document for one Lane A exploratory campaign.
Prepared by the coding agent, made operative only by a matching
`campaign-approval` record (`campaign-approval.schema.md`) referencing this
document's `policy_digest`. See ADR 0023 §9a, §9c.

**This schema is not enforced by any runtime component in this phase.**

## Required fields

| Field | Type | Immutable | Description |
|---|---|---|---|
| `policy_schema_version` | string | yes | Must be `"1"` for this contract. Unknown version fails closed. |
| `campaign_id` | string | yes | Pattern `EXP-\d{4}(-[a-z0-9-]+)?`. Never an Evidence number. |
| `policy_digest` | string (sha256 hex) | computed, yes once set | Digest of this document's normative fields (all fields except `policy_digest` itself), per ADR 0023 §10. |
| `classification` | string enum | yes | Must be exactly `EXPLORATORY_NOT_CANONICAL_EVIDENCE`. |
| `allowed_framework_shas` | list[string] | yes | Exact commit SHAs only. No branch names, no `HEAD`, no mutable refs. |
| `allowed_targets` | list[object{repository, sha}] | yes | Exact repository URL + exact commit SHA pairs. |
| `allowed_models` | list[string] | yes | Exact model identifiers. |
| `allowed_artifact_types` | list[string] | yes | Artifact types this campaign may produce. |
| `allowed_configurations` | list[object] or constraint expression | yes | Constrains which `configuration_id` values (see `configuration-identity.schema.md`) are legal under this policy. |
| `max_attempt_slots` | integer >= 1 | yes | Pre-invocation enforceable (ADR 0023 §14). |
| `max_provider_invocations` | integer >= 0, <= `max_attempt_slots` | yes | Pre-invocation enforceable. |
| `max_attempts_per_configuration` | integer >= 1 | yes | Pre-invocation enforceable. |
| `concurrency_ceiling` | integer >= 1 | yes | Pre-invocation enforceable. |
| `token_ceiling` | integer, nullable | yes | Soft, post-hoc monitored (ADR 0023 §14). Not a hard pre-call control. |
| `cost_ceiling` | object{amount, currency}, nullable | yes | Soft, post-hoc monitored. Never claimed as exact pre-call enforcement. |
| `validity_window` | object{not_before, not_after} (RFC3339) | yes | Pre-invocation enforceable expiry. |
| `target_mutation_prohibited` | boolean | yes | Must be `true`. |
| `fallback_prohibited` | boolean | yes | Must be `true`. |
| `repair_prohibited` | boolean | yes | Must be `true`. |
| `automatic_merge_prohibited` | boolean | yes | Must be `true`. |
| `preservation_requirements` | string | yes | Free text naming what must be preserved (e.g. "every reservation and attempt result, including failed and aborted"). |
| `logging_requirements` | string | yes | Free text naming logging obligations. |
| `prepared_by` | string | yes | Identity/role of preparer (e.g. `campaign-operator-agent`). Not an approval. |
| `prepared_at` | string (RFC3339) | yes | |

## Explicitly excluded (runtime-derived; must NOT appear in this document)

Reservations made, provider invocations made, remaining budget, actual costs
or tokens observed, attempt timestamps, attempt lifecycle states, produced
outputs, validation outcomes, campaign terminal state. These belong in the
campaign summary / ledger (`campaign-summary.schema.md`, ADR 0023 §9f). A
policy document containing any of these fields is invalid under this schema
regardless of value.

## Fail-closed rules

- Unknown `policy_schema_version`: reject.
- Any unknown top-level field: reject (no silent pass-through).
- Any of the four `*_prohibited` fields absent or `false`: reject — this
  schema version does not support relaxing them.
- `campaign_id` not matching the `EXP-NNNN` pattern, or matching an Evidence
  number pattern: reject.

## Versioning

A future `policy_schema_version: "2"` may add fields but must not repurpose
a v1 field name for a different meaning. A v1 consumer must reject a v2
document rather than partially parse it.

## Example — EXAMPLE_ONLY_NOT_OPERATIVE

```yaml
policy_schema_version: "1"
campaign_id: EXP-0000-EXAMPLE
policy_digest: "0000000000000000000000000000000000000000000000000000000000000000"
classification: EXPLORATORY_NOT_CANONICAL_EVIDENCE
allowed_framework_shas:
  - "0000000000000000000000000000000000dead"
allowed_targets:
  - repository: "https://example.invalid/example-owner/example-target.git"
    sha: "0000000000000000000000000000000000beef"
allowed_models:
  - "example-model-identifier"
allowed_artifact_types:
  - "repository_sensemaking_brief"
allowed_configurations:
  - artifact_type: "repository_sensemaking_brief"
    prompt_revision: "example-v0"
max_attempt_slots: 5
max_provider_invocations: 5
max_attempts_per_configuration: 2
concurrency_ceiling: 1
token_ceiling: null
cost_ceiling: null
validity_window:
  not_before: "2026-01-01T00:00:00+00:00"
  not_after: "2026-01-08T00:00:00+00:00"
target_mutation_prohibited: true
fallback_prohibited: true
repair_prohibited: true
automatic_merge_prohibited: true
preservation_requirements: "Every reservation and attempt result is preserved permanently, including failed and aborted attempts."
logging_requirements: "Every provider invocation and its raw output reference is logged in the campaign ledger."
prepared_by: campaign-operator-agent
prepared_at: "2026-01-01T00:00:00+00:00"
```
