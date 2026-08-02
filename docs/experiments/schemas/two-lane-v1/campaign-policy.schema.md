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
| `allowed_configuration_ids` | list[string (sha256 hex)] | yes | Exact, non-empty allowlist of `configuration_id` values (see `configuration-identity.schema.md`) legal under this policy. See "Configuration authorization" below for the format and matching rule. |
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

## Configuration authorization

`allowed_configuration_ids` is the single, exclusive mechanism for
determining whether a `configuration_id` is authorized under this policy.
Schema v1 defines no other configuration-authorization mechanism.

- **Format**: a non-empty list of lowercase 64-character SHA-256 hex
  strings. Each entry is an exact `configuration_id` as computed under
  `configuration-identity.schema.md` §10 — the digest of that configuration
  document's full normative field set, not a partial object and not any
  subset of fields.
- **No constraint expressions.** Schema v1 defines no configuration
  constraint expression, predicate, wildcard, pattern, range, or inheritance
  mechanism. A policy may only enumerate exact, already-computed
  `configuration_id` values.
- **No partial configuration objects.** The list never contains an object
  with individual fields (e.g. `artifact_type`, `prompt_or_skill_revision`);
  it contains only opaque digest strings.
- **Uniqueness and ordering**: duplicate IDs are invalid. The list must be
  sorted lexicographically (byte-wise, ascending) to give the document one
  canonical representation.
- **Fail closed**: an ID that is not a well-formed 64-character lowercase
  hex string, an empty list, or a malformed/unknown ID at consumption time
  all fail closed (reject).

### Conjunctive authorization semantics

An attempted configuration is legal under this policy only when **all** of
the following hold. These checks are conjunctive; none is a substitute for
another, and none takes precedence over another:

1. Its complete configuration document validates against
   `configuration-identity.schema.md`.
2. Its recomputed `configuration_id` exactly matches the ID carried by that
   document.
3. That exact ID is a member of `allowed_configuration_ids`.
4. `framework_sha` is independently present in `allowed_framework_shas`.
5. The exact `target_repository` + `target_sha` pair is independently
   present in `allowed_targets`.
6. `model_identifier` is independently present in `allowed_models`.
7. `artifact_type` is independently present in `allowed_artifact_types`.
8. Every other execution-relevant field is included in the configuration
   digest (so it cannot vary without producing a different
   `configuration_id`).

There is no precedence rule where membership in `allowed_configuration_ids`
overrides the other allowlists (2–7 above), and no rule where matching the
individual allowlists alone authorizes a `configuration_id` that is absent
from `allowed_configuration_ids`. This redundancy is intentional defense in
depth, not an inconsistency to be resolved by picking one check over the
other.

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
- `allowed_configuration_ids` empty, containing a malformed or non-lowercase
  entry, containing a duplicate entry, or not sorted lexicographically:
  reject.

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
allowed_configuration_ids:
  - "1111111111111111111111111111111111111111111111111111111111111111"
  - "2222222222222222222222222222222222222222222222222222222222222222"
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
