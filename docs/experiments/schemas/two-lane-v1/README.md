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
  unmistakable placeholder values (`EXP-0000-EXAMPLE`; 40-character Git SHA
  placeholders built from repeating `dead`/`beef`-style hex words, e.g.
  `000000000000000000000000000000000000dead`; 64-character SHA-256
  placeholders; `example.invalid` hostnames) so no example can be mistaken
  for, or copy-pasted into, an operative record.
- `schema_version` is present on every top-level document and is a required
  field. A future consumer must fail closed (reject, not best-effort-parse)
  on an unrecognized `schema_version` or an unknown required field.
- Digest fields use SHA-256 over the canonical serialization defined in
  ADR 0023 §10: source YAML is authored under the **Two-Lane YAML Profile
  v1** (§10b — YAML 1.2.2 syntax, JSON-Schema-only scalar resolution, YAML
  1.1 and implementation-default resolution forbidden, plain scalars
  restricted to `null`/`true`/`false`/RFC 8259 numbers, string values
  restricted to single-line quoted scalars — block scalar styles `|`, `>`,
  and their chomping/indentation variants are rejected) and parsed under
  fail-closed structural restrictions (§10b — no duplicate keys, aliases,
  anchors, tags, or merge keys). Mapping keys are a separate lexical class
  from scalar values, governed by their own grammar (§10b): every key must
  be an unquoted, plain ASCII field-name token matching `^[a-z][a-z0-9_]*$`.
  Every schema-defined mapping is **closed** by default: for a closed
  mapping, the key must exactly match a declared schema field, and quoted
  or complex keys are rejected. `execution_parameters` is the **sole open
  mapping** in schema v1 (ADR 0023 §10b "Closed and open mapping model"):
  arbitrary keys are permitted there only under the open-map key-grammar
  and reserved-key rules ADR 0023 §10b defines — there is no other general
  unknown-field escape hatch, and no other map becomes open through
  implementation choice. Unquoted field names such as `campaign_id:` are
  legal *because* of this mapping-key grammar, not as an exception to the
  string-quoting rule. This is parsed into a restricted JSON-compatible
  data model, then
  serialized with RFC 8785 (JCS) before
  hashing. Consumers must not hash the original YAML presentation bytes;
  comments, indentation, quoting style (where the resulting string is
  identical), key order, and line wrapping in the source YAML never affect
  the digest — a change to the *parsed value* changes the digest, not a
  change to any presentation byte. See ADR 0023 §10a–§10c for the exact
  algorithm, the exact scalar-resolution profile, and the exact hashed
  field set for each digest.
- These schemas are declarative documentation, not JSON Schema/YAML Schema
  documents with a validator binding — consistent with this repository's
  existing convention of normative-YAML-plus-prose contracts (see
  `experiments/run-control/0016-.../authorization-record.yaml` and
  `skills/workflow-planner/references/artifact-contracts.yaml`). A future
  phase (#118) may add a machine validator; this phase defines the contract
  it would validate against.
