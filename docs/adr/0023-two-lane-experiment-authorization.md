# ADR 0023: Two-Lane Experiment Authorization

**Status**: PROPOSED — awaiting independent adversarial review. This ADR
defines a governance and schema contract only. **It does not authorize any
experiment, campaign, or attempt, and it does not change runtime behavior.**
**Date**: 2026-08-02
**Proposes resolution for**: Issue #117 (Phase 1 of the two-lane experiment
authorization program, Issue #116).

---

## 1. Context and problem statement

ADR 0022 and `scripts/gate_a_authorization.py` define a canonical
authorization path ("Gate A") for a single, frozen, human-approved,
digest-bound provider invocation: exact record, exact digest, one invocation,
no retry, no fallback, independent review. Evidence 0016
(`experiments/run-control/0016-stage1-auteur-post-remediation-controlled-attempt/`)
is the concrete instance of that path and remains `PREPARED_NOT_RUN`.

That ceremony is correct for canonical evidence — output that is allowed to
support a readiness or validation claim. It is too costly for ordinary
exploratory engineering: trying several prompts, models, or configurations to
learn something, where any individual attempt succeeding or failing is not
itself a claim about repository readiness.

Issue #116 asks for a second, bounded lane: one human-approved *campaign
policy* that authorizes the coding agent to make multiple exploratory
attempts inside a strict, fully logged envelope, while keeping every
exploratory output permanently and unambiguously non-canonical.

This ADR is Phase 1 of that program: governance and schema contracts only.
No runtime component reads, validates, or enforces anything defined here yet.

## 2. Decision

Adopt a two-lane model:

- **Lane A (exploratory campaigns)**: one human-approved campaign policy
  authorizes a bounded number of attempts, executed under a namespace
  (`EXP-NNNN`) that is structurally distinct from canonical Evidence
  numbers. All outputs — successful, failed, interrupted, aborted — are
  preserved and permanently labeled `EXPLORATORY_NOT_CANONICAL_EVIDENCE`.
- **Lane B (canonical evidence)**: unchanged. The existing Gate A
  authorization-record / owner-approval / digest-binding model (ADR 0022,
  `scripts/gate_a_authorization.py`) continues to govern every canonical
  Evidence run, including Evidence 0016, exactly as today.

The lanes share no authorization artifact and no state transition. A
campaign policy is never accepted by the Gate A consumer, and a Gate A
authorization record is never accepted by a (future) campaign consumer.
Promotion from Lane A to Lane B is a new canonical run, never a relabeling
(§13).

This ADR defines the contract. Phases 2–6 (Issues #118–#122) build the
runtime that enforces it.

## 3. Lane A definition — exploratory campaigns

- Governed by one human-approved **campaign policy** (§9, schema in
  `docs/experiments/schemas/two-lane-v1/campaign-policy.schema.md`).
- Permits multiple **attempts** within the policy's declared bounds
  (configuration allowlist, attempt/invocation ceilings, concurrency,
  expiry).
- Every attempt is preceded by a durable **reservation** (§8) before any
  provider invocation.
- Every attempt's terminal state — `VALIDATION_PASSED`,
  `VALIDATION_FAILED`, `PROVIDER_FAILED`, or `ABORTED_BEFORE_INVOCATION` —
  is preserved permanently; none are deleted, hidden, or overwritten.
- No hidden retry, silent repair, model fallback, target mutation, or
  automatic merge (§6, §7).
- All outputs carry `EXPLORATORY_NOT_CANONICAL_EVIDENCE` and live under a
  campaign namespace (`EXP-NNNN`), never a canonical Evidence number (§11).
- Outputs may inform, but never directly become, canonical evidence (§13).

## 4. Lane B definition — canonical evidence

Unchanged from ADR 0022 / Evidence 0016's existing contract:

- Exact frozen authorization record and immutable digest binding.
- Genuine human approval binding the exact record (`owner-approval.md`,
  identity-holder signed, not agent-authored).
- One invocation, no retry, no fallback, no repair, no target mutation.
- Independent review at an exact head.
- Eligible to support formal validation or readiness claims.

This ADR makes no change to `scripts/gate_a_authorization.py`, to the
Evidence 0016 record, or to the canonical invariants in ADR 0022. Lane B is
referenced here only to define the boundary Lane A must not cross.

## 5. Terminology

| Term | Definition |
|---|---|
| **Campaign** | A bounded collection of exploratory attempts authorized by one campaign policy + approval pair. Identified by `campaign_id` (namespace `EXP-NNNN`). |
| **Configuration** | The frozen, hashable set of every execution-relevant input for one kind of attempt: framework SHA, target repository + target SHA, model identifier, prompt/skill revision, validator revision, artifact type, and execution parameters that can affect output. Identified by `configuration_id` = digest of the canonical serialization (§10). |
| **Attempt** | Exactly one provider invocation lifecycle, from reservation to terminal state, under one configuration, within one campaign. Identified by a durable `attempt_id`, allocated at reservation time, never reused. |
| **Reservation** | The durable record created before an attempt reaches the provider. Always visible; may terminate as `ABORTED_BEFORE_INVOCATION` without ever consuming a provider-invocation slot. |
| **Retry / rerun** | Another attempt. Always a new `attempt_id`, always logged, never conflated with the attempt it follows. |
| **Exploratory result** | An attempt's output artifact. Useful for learning; not canonical evidence; always labeled `EXPLORATORY_NOT_CANONICAL_EVIDENCE`. |
| **Canonical promotion** | The process in §13: select and freeze a new canonical configuration, create a new canonical authorization record, obtain genuine human approval, run under Lane B, review independently. Produces new evidence; never changes an exploratory artifact's classification. |
| **Campaign policy** | The immutable, human-approved authority-and-limits document for a campaign (§9a). |
| **Campaign approval** | The human governance act binding a policy digest to a genuine approval (§9b, §12). |
| **Ledger / campaign summary** | The runtime-derived record of what actually happened under a campaign (§9f). |

## 6. Threat model and failure modes

Each threat states the control and which phase is responsible for
*enforcing* it. Phase 1 (this ADR) defines the contract only; it enforces
nothing at runtime.

| # | Threat | Control defined here | Enforced by |
|---|---|---|---|
| 1 | Agent self-authorization (agent grants itself a campaign) | Campaign approval requires a human-authored, out-of-band-verifiable approval record (§12); the agent may only prepare, digest, and validate | Phase 3 (#119) |
| 2 | Fabricated human identity | Approval provenance model distinguishes claimed identity from verifiable provenance from runtime-checkable fact (§12) | Phase 2 (#118) |
| 3 | Policy mutation after approval | Any change to the parsed normative value of a policy field invalidates the approval; new digest, new approval required (§9c) | Phase 2 (#118) |
| 4 | Configuration drift | New `configuration_id` on any execution-relevant field change (§10); attempts grouped only by identical configuration | Phase 2/4 (#118, #120) |
| 5 | Model substitution | Model identifier is a normative configuration field and a policy allowlist field; mismatch fails closed | Phase 3 (#119) |
| 6 | Target or framework drift | Target/framework SHA are normative configuration fields and policy allowlist fields | Phase 3 (#119) |
| 7 | Lane confusion (exploratory treated as canonical, or vice versa) | Disjoint schemas, disjoint namespaces (`EXP-NNNN` vs Evidence numbers), mandatory `EXPLORATORY_NOT_CANONICAL_EVIDENCE` label (§11) | Phase 2/6 (#118, #122) |
| 8 | Exploratory output presented as canonical | §13 canonical promotion always creates a new record; nothing renames an exploratory artifact | Phase 5/6 (#121, #122) — and this ADR as a documentation invariant |
| 9 | Hidden retries | Every attempt gets a new `attempt_id`; policy declares `fallback_prohibited` / `repair_prohibited` (§9a) | Phase 4 (#120) |
| 10 | Selective omission of failed attempts | Attempt result schema requires permanent preservation of every terminal state (§9e); ledger append-only (§9f) | Phase 4 (#120) |
| 11 | Attempt ID reuse | `attempt_id` is durable and unique per reservation; schema forbids reissue (§8, §9d) | Phase 4 (#120) |
| 12 | Reservation created after provider invocation | Reservation must exist and be durable *before* invocation; attempt result schema references `reservation_id` created strictly earlier (§8) | Phase 4 (#120) |
| 13 | Cost or invocation-budget exhaustion | Policy declares enforceable ceilings (attempt slots, provider invocations, per-configuration limits); §14 distinguishes pre-invocation-enforceable from post-invocation-measured | Phase 3/4 (#119, #120) |
| 14 | Campaign expiry | Policy declares a validity/expiry rule; expired campaigns transition to `EXPIRED` and accept no further reservations | Phase 2 (#118) |
| 15 | Concurrent execution beyond policy | Policy declares a `concurrency_ceiling`; ledger tracks in-flight attempts | Phase 4 (#120) |
| 16 | Ledger or result truncation | Campaign summary schema requires the ledger to be append-only and complete relative to reservations issued (§9f) | Phase 4 (#120) |
| 17 | Circular policy/snapshot hashes | No schema field requires a digest-hashed file to contain the commit SHA of the commit containing that file (§10, §15) | This ADR (documentation-level) |
| 18 | Mutable-ref dependence | Configuration identity is defined only over exact SHAs/digests, never branch names or `HEAD` | This ADR (documentation-level) + Phase 2 (#118) |
| 19 | Raw-output omission | Attempt result schema requires a reference to the raw provider output, not only a post-processed artifact | Phase 4 (#120) |
| 20 | Automatic merge or target mutation | Policy declares `target_mutation_prohibited` and `automatic_merge_prohibited` as immutable fields (§9a) | Phase 2/3 (#118, #119) |

## 7. Permanent invariants

1. Evidence 0016 remains unchanged and remains governed exclusively by Lane
   B / ADR 0022.
2. No exploratory output may be silently relabeled canonical. Canonical
   status is acquired only via a new run under §13.
3. Every provider invocation is preceded by a durable, permanently visible
   reservation.
4. Every attempt — successful, failed, interrupted, or aborted before
   invocation — is permanently represented in the ledger.
5. The coding agent cannot expand its own campaign authority: it may
   prepare, digest, and validate; it may not approve.
6. Lane A and Lane B artifacts are structurally non-interchangeable: no
   schema field, consumer, or namespace accepts both.
7. Target mutation, hidden fallback, silent retry, and automatic merge are
   forbidden in both lanes unless a future explicit policy revision changes
   them for Lane A specifically, through a new approved policy.
8. Any change to the parsed normative value of a campaign policy field
   (§9c) invalidates the existing campaign approval.
9. A terminal attempt state never reverts to an earlier state, and one
   `attempt_id` never represents more than one provider invocation.

## 8. Lifecycle / state model

### 8a. Campaign lifecycle

```
DRAFT -> AWAITING_HUMAN_APPROVAL -> APPROVED_NOT_STARTED -> ACTIVE
ACTIVE -> EXHAUSTED | EXPIRED | ABORTED | COMPLETED
```

Legal transitions:

| From | To | Trigger |
|---|---|---|
| `DRAFT` | `AWAITING_HUMAN_APPROVAL` | Policy prepared and digested by the agent, submitted for human review |
| `AWAITING_HUMAN_APPROVAL` | `DRAFT` | Human requests changes (parsed policy value changes -> new digest, per invariant 8) |
| `AWAITING_HUMAN_APPROVAL` | `APPROVED_NOT_STARTED` | Genuine human approval recorded, binding the exact policy digest |
| `APPROVED_NOT_STARTED` | `ACTIVE` | First reservation issued |
| `ACTIVE` | `EXHAUSTED` | Any policy ceiling (attempt slots, invocations, budget) reached |
| `ACTIVE` | `EXPIRED` | Validity window elapsed |
| `ACTIVE` | `ABORTED` | Human or policy-declared abort condition |
| `ACTIVE` | `COMPLETED` | Campaign owner marks intentional, in-bounds completion |
| `EXHAUSTED`, `EXPIRED`, `ABORTED`, `COMPLETED` | (none) | Terminal; no reservations, no re-approval-in-place. A new campaign requires a new policy + approval. |

A campaign never transitions from a terminal state back to `ACTIVE`. A
policy mutation while `AWAITING_HUMAN_APPROVAL` or later always produces a
new `policy_digest`, which is a new policy revision, never an edit in place
(invariant 8).

### 8b. Attempt lifecycle

```
RESERVED -> ABORTED_BEFORE_INVOCATION            [terminal]
RESERVED -> INVOKED
INVOKED  -> PROVIDER_FAILED                       [terminal]
INVOKED  -> OUTPUT_CAPTURED
OUTPUT_CAPTURED -> VALIDATION_FAILED               [terminal]
OUTPUT_CAPTURED -> VALIDATION_PASSED               [terminal]
```

`TERMINAL` is not a distinct enum value stored on an attempt; it is the
property held by `ABORTED_BEFORE_INVOCATION`, `PROVIDER_FAILED`,
`VALIDATION_FAILED`, and `VALIDATION_PASSED`. (The four are individually
named in the schema's `terminal_states` list so a consumer can check
membership without hardcoding the transition graph — see
`attempt-result.schema.md`.)

Rules (restated from Issue #117 and made binding here):

- `RESERVED` is entered exactly once, at reservation time, strictly before
  any provider call.
- `ABORTED_BEFORE_INVOCATION` is reachable only from `RESERVED`, never from
  `INVOKED` or later — a provider failure is never recorded as a
  pre-invocation abort, and a pre-invocation abort never silently becomes a
  provider failure.
- `INVOKED` is entered at most once per `attempt_id`. A second provider call
  is a new `attempt_id` with a new `RESERVED` state, never a re-entry to
  `INVOKED` on the same attempt.
- No terminal state transitions anywhere else.
- `attempt_id` is immutable and unique from allocation; it is never reused
  after any transition, terminal or not.

## 9. Policy-versus-runtime-state boundary

### 9a. Immutable policy fields (campaign policy)

Authority and limits, fixed at approval time, never edited in place:

`campaign_id`, `policy_schema_version`, `policy_digest`, `classification`
(always `EXPLORATORY_NOT_CANONICAL_EVIDENCE`), `allowed_framework_shas`,
`allowed_targets` (repository + SHA pairs), `allowed_models`,
`allowed_artifact_types`, `allowed_configuration_ids` (exact-ID-only
allowlist; see §9d), `max_attempt_slots`, `max_provider_invocations`,
`max_attempts_per_configuration`, `concurrency_ceiling`,
`cost_ceiling`/`token_ceiling`/`invocation_ceiling` (§14 — enforceability
varies by field), `validity_window` (start/expiry), `target_mutation_prohibited`
(must be `true`), `fallback_prohibited` (must be `true`),
`repair_prohibited` (must be `true`), `automatic_merge_prohibited` (must be
`true`), `preservation_requirements`, `logging_requirements`.

### 9b. Campaign approval fields

`approval_schema_version`, `campaign_id`, `policy_digest` (must exactly
match the policy being approved), `claimed_approver_identity`,
`approval_provenance` (§12), `approved_at`, `approval_statement` (explicit
consent text, not inferred from silence or repository write access).

### 9c. Policy mutation rule

A change to the parsed normative JSON-compatible value of any field in §9a
changes `policy_digest` unless both the prior and new source text resolve,
under the Two-Lane YAML Profile v1 (§10b), to the same parsed value and RFC
8785 produces the same canonical representation for it (§10a). Presentation-
only source changes — comments, indentation, line wrapping, mapping-key
order, or an equivalent single- versus double-quoting of an identical string
value — do not change `policy_digest`, because they do not change the parsed
value. A new `policy_digest` requires a new campaign approval
(§9b) referencing that exact digest. The prior approval remains on record
but no longer authorizes anything once a new policy digest exists for the
same `campaign_id`; it is not deleted, only superseded. Runtime-derived
state (§9f) is never written back into the policy document — the policy
file is append-never / edit-never after approval; a change is always a new
revision.

### 9d. Configuration identity (runtime-derived per attempt, immutable per value)

`configuration_id` (digest, §10), and its constituent normative fields
(framework SHA, target repository + SHA, model identifier, prompt/skill
revision, validator revision, artifact type, execution parameters). A
`configuration_id` is computed once, at reservation time, from these fields;
it is immutable thereafter and is not itself part of the policy.

**Configuration authorization is exact-ID-only for schema v1.** The policy's
`allowed_configuration_ids` field (§9a) is a non-empty, sorted, duplicate-free
list of exact `configuration_id` SHA-256 hex values — schema v1 defines no
configuration constraint expression, wildcard, pattern, predicate, range, or
inheritance mechanism, and no partial-object policy matching. A
`configuration_id` is authorized only when it is an exact member of that
list, *and* — independently and conjunctively, not as an alternative path —
its constituent fields each satisfy their own policy allowlist
(`allowed_framework_shas`, `allowed_targets`, `allowed_models`,
`allowed_artifact_types`). No allowlist can substitute for another: exact
`configuration_id` membership does not override a failing constituent-field
check, and passing every constituent-field check does not authorize a
`configuration_id` absent from `allowed_configuration_ids`. This redundancy
is intentional defense in depth. See
`campaign-policy.schema.md`'s "Configuration authorization" section for the
normative field definition and fail-closed rules.

### 9e. Attempt reservation / attempt result (runtime-derived)

Reservation: `reservation_id`/`attempt_id` (allocated together, 1:1),
`campaign_id`, `configuration_id`, `reserved_at`, `state`.

Result: `attempt_id`, `state` (§8b), `state_history` (ordered, append-only),
`provider_invoked_at` (nullable — absent for `ABORTED_BEFORE_INVOCATION`),
`raw_output_reference`, `validated_output_reference`, `validation_outcome`,
`cost_observed`/`tokens_observed` (post-hoc measurement, §14), `terminal_at`.

### 9f. Campaign summary / ledger (runtime-derived)

`campaign_id`, `campaign_state` (§8a), `reservations_issued` (count and
list), `provider_invocations_made`, `remaining_budget` (per declared
ceiling), `attempts` (full list, every state, append-only), `first_reserved_at`,
`last_activity_at`, `terminal_reason` (for `EXHAUSTED`/`EXPIRED`/`ABORTED`/
`COMPLETED`).

No field appears in both the policy and the ledger with conflicting
authority: policy fields are always the ceiling/allowlist; ledger fields are
always the observed/consumed value. A validator (future phase) compares them;
it never merges them into one document.

## 10. Digest and snapshot topology

### 10a. Canonical serialization algorithm (schema v1, normative)

`UTF-8, LF line endings, keys sorted, no trailing whitespace` is necessary
but not sufficient to guarantee byte-identical digests across independent
implementations: it does not pin down number formatting, boolean/null
representation, nested-structure ordering, string escaping, Unicode
normalization, duplicate-key handling, or YAML-specific constructs (tags,
anchors, aliases, merge keys). Schema v1 therefore defines exactly one
canonicalization algorithm, used identically by every digest in this ADR
(`configuration_id`, `policy_digest`, and any future schema-v1 digest that
claims to reuse "the canonical serialization"):

1. The source artifact may be authored as YAML, under exactly one pinned
   source-language profile: the **Two-Lane YAML Profile v1**, defined
   normatively in §10b. Schema v1 does not permit any other YAML profile,
   and it does not permit a consumer to choose between profiles or fall
   back to a YAML library's default scalar-resolution behavior.
2. The YAML document is parsed under the Two-Lane YAML Profile v1 and the
   restricted, fail-closed rules in §10b into a JSON-compatible data model:
   object (string keys only), array, string, JSON number, boolean, or
   `null`. No other value type is permitted after parsing.
3. The resulting data model — restricted to exactly the hashed field set
   for that digest (§10c) — is serialized using
   [RFC 8785, the JSON Canonicalization Scheme (JCS)](https://www.rfc-editor.org/rfc/rfc8785).
   JCS fully defines key ordering, whitespace, string escaping, and number
   formatting; schema v1 does not define a second, competing
   number-formatting or key-ordering rule on top of it.
4. SHA-256 is computed over the resulting UTF-8 bytes.
5. No trailing newline is included in the hashed bytes (JCS output has
   none; implementations must not append one before hashing).

Consumers **must not** hash the original YAML presentation bytes (comments,
indentation, quoting style, key order in the source file, and line wrapping
are all presentation-only and must not affect the digest — only the parsed,
restricted data model does). A validator that hashes raw YAML bytes instead
of the JCS output of the restricted data model does not implement this
contract.

Number semantics: JSON-number canonicalization follows RFC 8785's own
canonical number representation; schema v1 does not define a second,
custom number-formatting mechanism. An implementation must reject a numeric
value that cannot be represented under RFC 8785's data model (e.g.
non-finite values, see §10b) rather than silently coercing it. A numeric
value (`1`, `1.0`) and a string value (`"1"`) are distinct source values in
the parsed data model and must never be treated as equivalent or normalized
into one another, except exactly as RFC 8785 itself defines for its
canonical number representation. Conversely, the plain scalars `1` and
`1.0` both resolve, under the Two-Lane YAML Profile v1 (§10b), to the same
JSON number value and therefore canonicalize identically under RFC 8785 —
their different source spellings do not necessarily produce different
digests, and this ADR makes no such claim.

### 10b. Two-Lane YAML Profile v1 (fail-closed, every digest-bearing artifact)

RFC 8785 (JCS) fixes the *output* side of canonicalization. It does not fix
the *input* side: different conforming YAML implementations may resolve
identical plain scalars (`yes`, `on`, `01`, `2026-01-01`, ...) differently,
producing different parsed values — and therefore different digests — from
byte-identical YAML source. Schema v1 closes that gap by pinning exactly one
source-language profile, used identically by every digest-bearing artifact
in this ADR (`configuration_id`, `policy_digest`, and any future schema-v1
digest that claims to reuse "the canonical serialization").

#### Profile identity

**Name: Two-Lane YAML Profile v1.**

1. YAML syntax version is YAML 1.2.2.
2. YAML 1.1 resolution is forbidden.
3. Implementation-default or environment-dependent scalar resolution is
   forbidden — a digest producer or consumer may not rely on whatever its
   YAML library resolves a plain scalar to by default.
4. Scalar resolution is based on the YAML 1.2.2 JSON Schema, with the
   stricter number rule defined below (not the YAML 1.2 Core Schema).
5. Explicit YAML tags remain forbidden (restated from the construct list
   below).
6. A YAML directive that requests another YAML version (e.g. `%YAML 1.1`)
   is rejected.
7. A `%YAML 1.2` directive may be accepted or omitted; its presence or
   absence does not alter the required Two-Lane YAML Profile v1 behavior.
8. Every digest producer and consumer must apply this exact profile,
   regardless of what its underlying YAML library defaults to. **Schema v1
   does not use the YAML 1.2 Core Schema, and it does not permit a consumer
   to choose between Core Schema, JSON Schema, or its library's default —
   the JSON Schema profile above, plus the stricter number rule below, is
   the only legal choice.**

#### Scalar-resolution rules (lexical, fail-closed)

**Quoted scalars.** Single-quoted and double-quoted YAML scalars resolve to
JSON strings. Quoting style (single vs. double) never affects the resulting
string value. A value intended to be a string **must** be quoted — this
includes ordinary schema strings such as campaign IDs, classifications,
model identifiers, artifact types, roles, URLs, revision identifiers, and
RFC3339 timestamps.

**Plain (unquoted) scalars** are permitted only when they exactly match one
of these forms; any other plain scalar is invalid and must be rejected, not
silently converted to a string or to an alternate scalar type:

| Plain scalar | Resolves to |
|---|---|
| `null` | JSON `null` |
| `true` | JSON boolean `true` |
| `false` | JSON boolean `false` |
| a valid RFC 8259 JSON number (grammar below) | JSON number |

JSON-number grammar (RFC 8259), used verbatim as the plain-scalar number
test:

```
-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?
```

Therefore the following unquoted plain scalars are **rejected**, not
coerced to a string or to an alternate boolean/null/number interpretation:
`yes`, `no`, `on`, `off`, `Yes`, `No`, `True`, `False`, `TRUE`, `FALSE`,
`Null`, `NULL`, `~`, `01`, `-01`, `0o7`, `0x10`, `+1`, `.5`, `1.`, `.inf`,
`-.inf`, `.nan`, and any timestamp- or date-looking plain scalar (e.g.
`2026-01-01`). To represent any of these as strings, they must be quoted.

**Mapping keys are a separate lexical class from scalar values, governed by
their own grammar below — not by the plain-scalar rule above.** The
restricted plain-scalar rule (quoted-string-required, `null`/`true`/`false`/
number-only unquoted) applies to scalar *values*. It does not apply to
mapping keys. Unquoted schema field names such as `campaign_id:`,
`policy_digest:`, and `configuration_id:` are legal *only* because mapping
keys are governed by this separate mapping-key grammar — this is not an
exception to be inferred from examples, and Phase 2 must not invent its own
key grammar.

**Mapping-key grammar (normative):**

1. Every mapping key **must** be an unquoted, plain ASCII field-name token
   matching `^[a-z][a-z0-9_]*$`.
2. The resulting token **must** exactly match a field declared by the schema
   for that object (restated from §9a/§9c: unknown keys are rejected before
   hashing).
3. This rule applies recursively to every nested schema object, including
   (non-exhaustively) keys such as `repository`, `sha`, `amount`, `currency`,
   `not_before`, `not_after`, `mechanism`, and `reference`.
4. Quoted mapping keys (e.g. `"campaign_id":` or `'campaign_id':`) are
   **forbidden** in schema v1. Changing a key from unquoted to quoted form is
   **not** a permitted presentation-only change — quoted keys are simply
   invalid.
5. Numeric-looking, boolean-looking, null-looking, timestamp-looking, empty,
   Unicode, or otherwise nonconforming mapping keys are forbidden.
6. Complex YAML keys and the explicit-key indicator (`?`) are forbidden in
   key position.
7. Aliases, anchors, tags, and merge keys remain forbidden in key position,
   as well as in value position (restated below).
8. Duplicate keys are detected on the exact decoded field-name string
   *before* the object is constructed or any entry is discarded. A parser
   that silently keeps only the first or last occurrence of a duplicate key
   is nonconforming.
9. Source mapping-key *order* is presentation-only, because JCS sorts object
   keys (§10a). The *spelling and case* of a field name is normative: two
   different valid field-name tokens never normalize to the same key, and no
   Unicode normalization or case folding is applied to keys.

#### Permitted string-scalar styles (normative)

Schema v1 permits exactly two source-level styles for string values:

- single-line single-quoted scalars (e.g. `'exploratory'`);
- single-line double-quoted scalars (e.g. `"exploratory"`).

Schema v1 **rejects**, for string values:

- literal block scalars (`|`);
- folded block scalars (`>`);
- any chomping indicator (`|-`, `|+`, `>-`, `>+`);
- any explicit indentation indicator (e.g. `|2`, `>2`, `|2-`);
- multiline single-quoted scalars;
- multiline double-quoted scalars;
- arbitrary unquoted plain text (restated from the plain-scalar rule above).

A string value containing a newline must represent that newline using an
escape sequence inside a single-line double-quoted scalar (e.g. `"line
one\nline two"`), never via a block scalar. YAML escape processing produces
the resulting Unicode string before JCS runs (restated below); different
allowed single-line quoted presentations that decode to the same Unicode
string canonicalize identically. Block-scalar folding, chomping, and
indentation behavior is unavailable in schema v1 and must never be delegated
to a YAML library's default handling.

#### Conformance table (normative, not illustrative)

Accepted:

| YAML source | Parsed JSON value |
|---|---|
| `"yes"` | string `"yes"` |
| `"on"` | string `"on"` |
| `"01"` | string `"01"` |
| `"2026-01-01"` | string `"2026-01-01"` |
| `true` | boolean `true` |
| `false` | boolean `false` |
| `null` | `null` |
| `0` | number `0` |
| `-1` | number `-1` |
| `1.5` | number `1.5` |
| `1e3` | number `1000` |
| `"1"` | string `"1"` |

Rejected when unquoted: `yes`, `no`, `on`, `off`, `True`, `Null`, `~`, `01`,
`0o7`, `0x10`, `+1`, `.5`, `1.`, `.nan`, `.inf`, `2026-01-01`.

#### Number and JCS input domain

- Every number must be finite; `NaN`, positive infinity, and negative
  infinity are rejected (restated from the construct list below).
- Every number must be representable as an IEEE-754 binary64 value, as
  required by RFC 8785 / I-JSON. Overflow, underflow to an unintended
  value, or unsupported precision fails closed rather than silently
  altering authority.
- Negative zero (`-0`) is rejected for schema v1, so `-0` cannot collapse
  to the same JCS representation as `0`.
- Integer-valued policy fields (e.g. `max_attempt_slots`,
  `max_provider_invocations`, `max_attempts_per_configuration`,
  `concurrency_ceiling`, `token_ceiling`) must be integers in the
  interoperable safe-integer range `-9007199254740991` through
  `9007199254740991` inclusive. A field declared as integer must reject a
  fractional or exponential value even when that value is mathematically
  integral (e.g. `5.0` is rejected for an integer field, even though it
  equals `5`).
- Numeric strings are never coerced into numbers: string `"1"` and number
  `1` are distinct values, always.
- Number `1` and number `1.0` resolve to the same JSON numeric value for
  JCS purposes and therefore canonicalize identically (§10a); their
  different source spellings do not necessarily produce different digests.
- Schema v1 does not define a second number-serialization algorithm beyond
  RFC 8785.

#### String and Unicode rules

- Parsed Unicode strings are preserved exactly as required by RFC 8785. No
  Unicode normalization step is performed.
- Canonically equivalent but differently encoded Unicode sequences (e.g.
  NFC vs. NFD forms of the same visible text) remain different string
  values.
- Lone Unicode surrogates or otherwise invalid Unicode string data are
  rejected.
- YAML escape processing (for quoted scalars) occurs before JCS; JCS then
  serializes the resulting Unicode string value. Different YAML quoting or
  escape presentations that produce the same Unicode string value produce
  the same digest.

#### Structural rejections (fail-closed, every digest-bearing artifact)

In addition to the scalar-resolution rules above, parsing of any
digest-bearing schema-v1 artifact (campaign policy, configuration identity,
and any future schema-v1 artifact whose digest reuses this algorithm)
**must reject**:

- duplicate mapping keys;
- YAML aliases;
- YAML anchors;
- explicit YAML tags;
- merge keys (`<<`);
- non-string mapping keys;
- quoted, complex, or otherwise nonconforming mapping keys (restated from
  the mapping-key grammar above);
- literal (`|`) or folded (`>`) block scalars, in any chomping (`|-`, `|+`,
  `>-`, `>+`) or indentation-indicator form, and multiline quoted scalars
  (restated from the permitted string-scalar styles above);
- non-JSON scalar types (anything outside object/array/string/number/
  boolean/null);
- implicit timestamp/date objects (a YAML loader that auto-converts an
  RFC3339-looking scalar to a native date/datetime type instead of leaving
  it as a string — this is the timestamp-resolution behavior forbidden by
  the Two-Lane YAML Profile v1 above, restated here as a structural
  rejection);
- non-finite numbers (`NaN`, positive infinity, negative infinity);
- multiple YAML documents in one stream;
- implementation-specific custom types (e.g. `!!python/object`, `!!binary`
  used to smuggle a non-JSON type).

A parser that accepts any of the above, or that resolves a plain scalar
outside the exact forms permitted above, is not a conforming schema-v1
parser. This restriction exists so two independent implementations, given
the same source YAML, always produce the same restricted data model and
therefore the same digest — a YAML loader's default (non-fail-closed, or
YAML-1.1-flavored, or Core-Schema-flavored) behavior on any of these
constructs is implementation-defined and would silently break that
guarantee.

### 10c. Hashed field sets (normative, exact)

**Policy** (`policy_digest`): hash every required normative field listed in
§9a **except** `policy_digest` itself. Unknown top-level fields are
rejected before hashing (§9a fail-closed rule, restated in
`campaign-policy.schema.md`'s "Fail-closed rules"). `allowed_configuration_ids`
must already be lexicographically sorted before hashing — sort order is
part of the normative value, not a canonicalization step applied at hash
time. A change to any normative value changes `policy_digest` and
invalidates the approval bound to the prior digest (§9c).

**Configuration** (`configuration_id`): hash exactly these fields, no more
and no fewer:

- `configuration_schema_version`
- `framework_sha`
- `target_repository`
- `target_sha`
- `model_identifier`
- `prompt_or_skill_revision`
- `validator_revision`
- `artifact_type`
- `execution_parameters`

Explicitly excluded from the configuration hash: `configuration_id` itself
(the field being computed) and `campaign_id` (contextual, not
normative-to-the-hash — see `configuration-identity.schema.md`'s Identity
rule note). This exact list is the sole normative definition; it is
restated identically in `configuration-identity.schema.md` and must not be
described elsewhere only as "the fields in §9d" or any other indirect
reference that could drift from this list.

- **No circular dependency**: consistent with the existing Evidence 0016
  precedent (`authorization-record.yaml`'s documented treatment of
  `run_control_commit_sha` and `execution_framework_sha`), no digest-hashed
  file in this contract is required to contain the commit SHA of the commit
  that contains that same file. Where a snapshot commit can only be known
  after the commit exists (e.g. the commit that first introduces an
  approved policy file), that commit SHA is supplied as external,
  runtime-resolved provenance at consumption time — never pre-guessed or
  embedded inside the file whose bytes are being hashed.
- Configuration and policy snapshots are defined only over exact,
  already-immutable references: commit SHAs, not branch names; artifact
  digests, not paths alone. This is compatible with, and reuses, the
  existing `framework_root` / `target_root` / `artifact_root` topology from
  ADR 0022 and `scripts/gate_a_authorization.py`: a future campaign consumer
  resolves these roots the same way Gate A does, rather than defining a
  parallel resolution mechanism.

## 11. Exploratory classification

- Exploratory artifacts are identified by a **campaign namespace**,
  `EXP-NNNN` (e.g. `EXP-0001`), structurally disjoint from canonical
  Evidence numbers (`00NN` under `experiments/evidence/` or
  `experiments/run-control/`).
- Every exploratory output — the artifact, its metadata, and any summary
  referencing it — carries the literal classification string
  `EXPLORATORY_NOT_CANONICAL_EVIDENCE`.
- No successful exploratory output may be relabeled canonical. There is no
  schema field, state transition, or consumer defined in this contract that
  changes an exploratory artifact's classification in place.

## 12. Approval provenance model

Four distinct concepts, never conflated:

1. **Claimed identity field** (`claimed_approver_identity`): a string the
   approval record asserts — e.g. `ThorStarlord`. This is a claim, not a
   fact.
2. **Provenance used to verify that identity**: the out-of-band mechanism
   that could corroborate the claim — e.g. a signed commit, a GitHub review
   approval event tied to an authenticated account, a PR approval by an
   identity with owner/maintainer role. This ADR requires the approval
   record to *name* which provenance mechanism was used
   (`approval_provenance.mechanism`) and to *reference* the corroborating
   artifact (`approval_provenance.reference`, e.g. a commit SHA or a GitHub
   API review URL/id).
3. **What the current runtime can actually verify**: as of Phase 1, nothing
   — no runtime component reads or checks a campaign approval yet. A future
   consumer (Phase 3, #119) is scoped to verify provenance mechanically
   where possible (e.g. a signed commit's GPG/SSH signature, a GitHub review
   API response) and must fail closed when it cannot.
4. **What remains a governance assumption**: that the named human is who
   they claim to be, and that repository write access is not by itself
   proof of authorization. This ADR states explicitly: **repository write
   access, branch push capability, or the ability to open a PR are never
   sufficient evidence of campaign approval.** An approval record with no
   verifiable provenance reference is not a valid approval under this
   contract, even if it is syntactically well-formed.

The coding agent may prepare a policy, compute its digest, and prepare a
blank approval template. It may validate an existing approval's structure
and digest match. **It may not** fabricate a first-person human approval,
claim the identity of `ThorStarlord` or any other owner, populate an
operative approval on a human's behalf, or treat its own repository write
access as authorization. This mirrors, and does not weaken, the existing
`owner-approval.md` discipline used for Evidence 0016.

## 13. Canonical-promotion rules

Exploratory findings may inform a later canonical experiment. The
exploratory artifact is **never** promoted directly. Promotion means:

1. Select and freeze a new canonical `configuration_id` (§9d/§10) — it may
   reuse values learned from exploratory attempts, but it is computed fresh
   and independently.
2. Create a new canonical authorization record under the existing Gate A /
   Lane B contract (ADR 0022), with a new Evidence number.
3. Obtain genuine human approval for that exact record (`owner-approval.md`,
   per existing Evidence-0016-style discipline).
4. Perform the canonical run under Lane B, subject to Gate A's existing
   one-invocation, no-retry, no-fallback constraints.
5. Review the result independently, at an exact head.

This produces a new experiment and new evidence. It never rewrites the
`EXPLORATORY_NOT_CANONICAL_EVIDENCE` classification of the exploratory run
that informed it, and it never reuses an `EXP-NNNN` identifier as an
Evidence number.

## 14. Budget and concurrency semantics

Distinguish three categories per field, per Issue #117 requirement 8:

| Category | Meaning | Applies to |
|---|---|---|
| **Pre-invocation enforceable** | Can be checked and denied *before* a provider call | `max_attempt_slots`, `max_provider_invocations`, `max_attempts_per_configuration`, `concurrency_ceiling`, `validity_window` (expiry), `allowed_*` allowlists |
| **Post-invocation measured** | Only knowable after the provider responds | `tokens_observed`, `cost_observed`, wall-clock duration |
| **Unavailable / not hard-enforced** | Must not be presented as a hard pre-call control | Exact provider dollar cost *before* a call (most provider APIs do not expose this); this contract does **not** claim exact pre-call cost enforcement |

**Chosen canonical interpretation**: budget ceilings are enforced via
**invocation-count and reservation-count limits** (`max_attempt_slots`,
`max_provider_invocations`, `concurrency_ceiling`), which are exactly
knowable before a call, plus an optional conservative
`token_ceiling`/`cost_ceiling` field that a future consumer treats as a
**soft, post-hoc, monitored** limit — never as a claim that the campaign
mechanically stopped a specific call from exceeding an exact dollar amount.
No field in this contract claims exact pre-call cost enforcement. This is
the single canonical mechanism; the schemas do not define an alternative,
competing budget mechanism.

Reservation semantics (restated normatively from Issue #117 §3B):

- A reservation that aborts before provider invocation consumes one
  **attempt slot**, does **not** consume a provider-invocation slot, does
  **not** consume cost/token budget, and remains represented with an
  explicit terminal state (`ABORTED_BEFORE_INVOCATION`).
- An attempt that reaches the provider consumes one attempt slot, one
  provider-invocation slot, and applicable cost/token budget, regardless of
  whether the provider fails, output validation fails, or the artifact is
  unusable.

## 15. Compatibility with the artifact-root topology

This design reuses, rather than replaces, `framework_root` / `target_root` /
`artifact_root` as resolved by `scripts/gate_a_authorization.py` (ADR 0022,
PR #114/#113). A future campaign consumer resolves configuration snapshots
and policy/approval file locations against these same roots. No schema field
here introduces a parallel or conflicting root-resolution mechanism, and no
digest computation embeds a not-yet-existing commit SHA of its own containing
commit (§10) — the same circularity constraint the Evidence 0016 record
already documents for `run_control_commit_sha` and `execution_framework_sha`.

## 16. Consequences and trade-offs

- Two disjoint governance ceremonies now exist. This is intentional: Lane A
  trades per-attempt ceremony for a stronger up-front policy + budget bound;
  Lane B keeps maximum per-invocation ceremony for canonical claims.
- Nothing here is enforced yet. A campaign policy prepared today has no
  runtime consumer; `EXP-0001` cannot legally exist until Phase 3 (#119)
  ships an authorization capability, matching Issue #117's explicit
  out-of-scope list.
- The schemas add real documentation and review surface (six new contract
  documents) before any runtime code exists, which is the deliberate
  trade-off requested by Issue #116's delivery sequence.

## 17. Rejected alternatives

- **Reuse the Gate A schema for campaigns directly.** Rejected: Gate A's
  `invocation_limit: 1` / single-record model has no field for
  multi-attempt budgets, per-attempt states, or a ledger; overloading it
  would blur the one invariant Lane B depends on (exactly one invocation).
- **One combined policy+approval file.** Rejected: mirrors the Evidence 0016
  precedent of separating `authorization-record.yaml` from
  `owner-approval.md` — keeping the human-authored approval physically
  separate from the agent-preparable policy makes it structurally harder for
  an agent to fabricate both halves in one edit.
- **Store runtime ledger state inside the policy file.** Rejected explicitly
  by Issue #117's requirement 5 and by invariant 8 here — it would let
  runtime activity implicitly redefine authorized limits.
- **Allow exploratory campaigns to receive Evidence numbers directly, with a
  status flag distinguishing them.** Rejected: a shared numbering namespace
  with a mutable flag is exactly the "silent relabeling" surface invariant 2
  forbids; a structurally disjoint namespace (`EXP-NNNN`) removes the
  possibility entirely rather than policing it.
- **Claim exact pre-call cost enforcement.** Rejected per §14 — no
  provider-cost API guarantee exists to back that claim; overstating it
  would violate the "budget enforceability" requirement in Issue #117.
- **Generalized configuration constraint expressions (patterns, predicates,
  wildcards, ranges, partial-object matching) for `allowed_configuration_ids`.**
  Rejected for schema v1: a constraint language with no defined precedence
  or intersection semantics against the other policy allowlists left two
  competing authorization mechanisms with no single canonical
  interpretation, forcing Phase 2 (#118) to invent semantics this ADR should
  define. Schema v1 instead requires exact, pre-computed `configuration_id`
  membership only (§9d), checked conjunctively with the other allowlists. A
  future schema version may reconsider a constraint language, but only with
  an explicit precedence/intersection rule defined alongside it.
- **Prose-only canonical serialization ("UTF-8, LF line endings, sorted
  keys, no trailing whitespace") with no pinned number/boolean/nested-
  structure format.** Rejected: it does not uniquely define serialization
  of nested structures, strings, booleans, nulls, numbers, Unicode,
  duplicate keys, or YAML-specific constructs (tags, anchors, aliases,
  merge keys), so two independent implementations could compute different
  bytes — and therefore different digests — for the same semantic content.
  Schema v1 instead pins RFC 8785 (JCS) plus explicit fail-closed YAML
  input restrictions (§10a, §10b), so Phase 2 (#118) implements a single,
  fully specified algorithm rather than inventing the missing semantics
  itself.
- **Pin RFC 8785 (JCS) alone, without pinning YAML scalar resolution.**
  Rejected: RFC 8785 fixes only the canonical *output* of an already-parsed
  JSON-compatible value; it says nothing about how a YAML *input* scalar
  like `yes`, `01`, or `2026-01-01` should resolve. Different YAML
  implementations resolve these differently (YAML 1.1 booleans, Core vs.
  JSON Schema, implementation defaults), so byte-identical YAML source
  could parse to different values and therefore hash differently even with
  JCS pinned. Schema v1 additionally pins the Two-Lane YAML Profile v1
  (§10b): YAML 1.2.2 syntax, JSON-Schema-only scalar resolution, and an
  exact RFC 8259 number grammar for plain scalars, so no implementation
  choice remains.

## 18. Phase dependency sequence (Issues #118–#122)

1. **Phase 2 — #118, campaign policy and approval validators.** Structural +
   digest validation of the schemas defined here: policy digest binding,
   approval identity/status, expiry, allowlists, limits, and configuration
   hashing. No provider invocation.
2. **Phase 3 — #119, exploratory authorization capability and
   provider-boundary enforcement.** Mirrors ADR 0022's capability model for
   Lane A; this is where §12's provenance verification and §6 threats 1, 5,
   6, and 13 get real enforcement at the provider boundary.
3. **Phase 4 — #120, crash-safe attempt ledger, budgets, and raw-output
   preservation.** Implements §8b, §9e, §9f, and the remaining §6 ledger/
   accounting threats (9–16, 19).
4. **Phase 5 — #121, prepare `EXP-0001`.** Uses the schemas here to author
   (not run) the first real campaign policy, non-executable.
5. **Phase 6 — #122, execute and report `EXP-0001`.** Executes the approved
   campaign within its envelope and produces the campaign summary; explicitly
   out of scope for this ADR.

Each phase is a separate PR, independently reviewed at an exact head, merged
before the next dependent phase starts.

## 19. Evidence 0016 — explicit statement

Evidence 0016 (`experiments/run-control/0016-stage1-auteur-post-remediation-controlled-attempt/`)
is **unchanged** by this ADR: no file under that directory is modified,
`authorization-record.yaml` and its digest are untouched, and Evidence 0016
remains governed exclusively by Lane B / ADR 0022 / `scripts/gate_a_authorization.py`.

## 20. This ADR does not authorize an experiment

This ADR is a governance and schema contract. It does not create, approve,
or run any campaign or attempt. `EXP-0001` does not exist after this ADR
merges. No provider is invoked as a result of this document. Runtime
enforcement is deferred to Phases 2–6 (#118–#122) as listed in §18.

## Status rationale

PROPOSED, not Accepted. Promotion condition: an independent reviewer
confirms (a) the six schema contracts in
`docs/experiments/schemas/two-lane-v1/` are internally coherent with this
ADR and with each other, (b) no field appears with conflicting authority in
both policy and ledger, (c) no digest computation is circular, (d) the
lifecycle vocabulary in §8 matches Issue #117's required states exactly, and
(e) Evidence 0016 and Evidence 0015 have empty diffs on this branch.
