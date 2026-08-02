# Two-Lane Experiment Schema Contracts (v1)

Proposed machine-readable schema contracts for the two-lane experiment
authorization program (Issue #116), Phase 1 (Issue #117, ADR 0023:
`docs/adr/0023-two-lane-experiment-authorization.md`).

**Status: PROPOSED. Documentation and contract only. No runtime component
in this repository parses, validates, or enforces these schemas yet. No
campaign, approval, reservation, or attempt defined by these schemas is
operative.**

## Contracts

| Contract | File | Produced by (future) | Consumed by (future) |
|---|---|---|---|
| Campaign policy | `campaign-policy.schema.md` | Human + agent (drafted by agent, approved by human) | Campaign consumer (#119) |
| Campaign approval | `campaign-approval.schema.md` | Human (approval act) | Campaign consumer (#119) |
| Configuration identity | `configuration-identity.schema.md` | Campaign consumer, at reservation time | Attempt reservation, attempt result |
| Attempt reservation | `attempt-reservation.schema.md` | Campaign consumer, before provider invocation | Attempt result, campaign summary |
| Attempt result | `attempt-result.schema.md` | Attempt executor (#120), after provider response or abort | Campaign summary |
| Campaign summary | `campaign-summary.schema.md` | Ledger (#120) | Human review, canonical-promotion decision (§13 of ADR 0023) |

## Conventions

- Each schema is a normative Markdown document: a field table (name, type,
  immutable-vs-runtime-derived, required, description) plus a fenced YAML
  example.
- Every example is marked `EXAMPLE_ONLY_NOT_AUTHORIZATION` (approval
  examples) or `EXAMPLE_ONLY_NOT_OPERATIVE` (all other examples) and uses
  unmistakable placeholder values (`EXP-0000-EXAMPLE`, SHAs of all `0`s or
  `f`s, `example.invalid` hostnames) so no example can be mistaken for, or
  copy-pasted into, an operative record.
- `schema_version` is present on every top-level document and is a required
  field. A future consumer must fail closed (reject, not best-effort-parse)
  on an unrecognized `schema_version` or an unknown required field.
- Digest fields use SHA-256 over the canonical serialization defined in
  ADR 0023 §10 (UTF-8, LF line endings, sorted keys, no trailing whitespace).
- These schemas are declarative documentation, not JSON Schema/YAML Schema
  documents with a validator binding — consistent with this repository's
  existing convention of normative-YAML-plus-prose contracts (see
  `experiments/run-control/0016-.../authorization-record.yaml` and
  `skills/workflow-planner/references/artifact-contracts.yaml`). A future
  phase (#118) may add a machine validator; this phase defines the contract
  it would validate against.
