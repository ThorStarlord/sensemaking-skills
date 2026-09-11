# B7 Semantic Reference Resolution & Integrity Audit v0

**Document type:** Design preflight / construction gate decision

**Status:** COMPLETE — `BUILD`

**Assessed checkout:** `main` at `4fbfb99ded103c094b5d34cf43d70612a56c3a0d`

**Assessed:** 2026-09-10

**Mode:** Read-only repository analysis and design consolidation

**Implementation status:** Not implemented by this preflight

## Decision

```text
BUILD B7
```

B7 is authorized as one bounded construction package because the repository
already has a meaningful, mechanically authoritative non-parent reference
family: Campaign evidence, including admitted artifacts and admission receipts.

This decision does not claim that agents need reference auditing, that it
improves decision quality, or that it has demonstrated user value. It claims
only that a concrete integrity boundary is visible and can be implemented from
existing authoritative state without inventing semantic objects or universal
namespaces.

After B7 is implemented and mechanically qualified, reassess the Construction
Diminishing-Returns Gate from zero. No B8 or later package is pre-authorized.

## 1. Scope and permanent boundary

B7 answers:

> Given a recorded `SemanticStateEntry` reference and authoritative state that
> already exists, what can be mechanically established about its resolution?

B7 may establish:

```text
exact identity existence
addressability under an existing contract
unique versus ambiguous resolution
missing internal identity
integrity effect of a resolution result
```

B7 must not establish:

```text
semantic support
truth or correctness
evidence relevance
currentness or supersession
decision relevance
responsibility warrant
authority precedence
Skill selection or routing
```

The key invariants are:

```text
reference occurrence != reference resolution
reference resolution != semantic support
not_addressable != invalid
resolved != current
```

## 2. Repository evidence inspected

The preflight inspected the following current authorities and behavior:

| Repository surface | Finding |
| --- | --- |
| `semantic_architecture.models.SemanticStateEntry` | Stores `artifact_ref`, `target_ref`, `evidence_refs`, `claim_refs`, `uncertainty_refs`, `parent_entry_ids`, and optional `semantic_profile_ref`. |
| `semantic_architecture.state.SemanticStateStore` | Validates JSONL shape, SHA-256 chaining, entry identity, and parent topology. It does not resolve outbound artifact/evidence/claim/uncertainty/profile references. |
| `campaigns.store.CampaignStore.evidence_refs()` | Authoritative Campaign evidence inventory. Raw regular files below `evidence/` are exposed; artifact files become evidence only through valid admission receipts with matching content digests; admission receipts themselves are exposed. |
| `campaigns.lineage` | Independently resolves Campaign evidence paths, distinguishes raw evidence/admitted artifacts/admission receipts, validates physical containment, admission provenance, and immutable bytes. |
| `campaigns.artifacts` and `campaigns.admission` | Define content-addressed admitted artifact identity and reject arbitrary files under `artifacts/` as evidence. |
| `campaign_observability_cli.py` | `campaign explain` reports exact reference occurrences; `campaign semantic-state` reports companion records and chain diagnostics. Neither currently reports outbound reference resolution. |
| `tests/test_semantic_substrate.py` | Existing tests accept opaque values such as `brief.md`, `review.md`, and `C1` while testing chain integrity and parent topology. This demonstrates present opacity, not a recorded production incident. |
| `STATUS.md` and build-first policy | B1–B6 are repository-qualified; native-harness/product-value claims remain unproven; construction remains allowed for a concrete mechanically testable integrity capability. |

## 3. Standalone primitive

The conceptual contract is:

```text
SemanticStateEntry or semantic-state log
        +
existing authoritative resolver context
        ↓
SemanticReferenceAudit
```

The future implementation should keep mechanical semantics in a reusable
library module, conceptually:

```text
src/sensemaking_skills/semantic_architecture/reference_audit.py
```

The library must not depend on Click or make presentation decisions. Campaign
adapters construct resolver context from existing Campaign services and pass it
to the primitive.

The result has three independent dimensions:

```yaml
resolution: resolved | dangling | ambiguous | not_addressable
reference_class: campaign_internal | external_declared | legacy_opaque | unknown
integrity_effect: pass | fail | informational
```

`reference_class` is preferred over `qualification`. The repository already
uses “qualification” for repository, native-harness, portability, and
promotion maturity, so reusing it for reference address spaces would create
avoidable ambiguity.

`reference_class` may be omitted when no existing authority can establish it.
B7 must not infer `external_declared` merely from a URL-like or unfamiliar
string.

`AMBIGUOUS` remains reserved in the result vocabulary, but is explicitly
deferred from B7 v0 emission and qualification. Current authoritative
resolvers either deduplicate identities or guarantee uniqueness, so B7 v0
must not manufacture an ambiguity source merely to exercise the enum.

## 4. Field-resolution matrix

| Field | Existing authoritative source | B7 v0 behavior | Non-resolution effect |
| --- | --- | --- | --- |
| `parent_entry_ids` | `SemanticStateStore` known entry IDs and existing parent checks | Reuse and surface existing result; do not replace the current validator | Missing/future/self parent is an existing integrity failure |
| `evidence_refs` | `CampaignStore.evidence_refs()`; Campaign lineage for kind/provenance/bytes | Resolve exact raw evidence, admitted artifact, or admission-receipt refs when Campaign context is present | `dangling` or `ambiguous` is a failure only for an established Campaign-internal form; opaque legacy strings are informational |
| `artifact_ref` | Campaign admission/artifact identity where the exact content-addressed admitted ref exists | Resolve only an exact admitted artifact identity already exposed by Campaign evidence/admission state | Missing admitted artifact or inconsistent admission is a failure; arbitrary filename resemblance is not resolution |
| `uncertainty_refs` | Current Campaign `active_uncertainty.id` only | Resolve an exact current Campaign uncertainty when the Campaign state establishes it | Other values are `not_addressable`; B7 does not create an uncertainty-history registry |
| `claim_refs` | No universal addressable Claim registry | Report `not_addressable` unless a future existing domain contract supplies an authoritative resolver | Informational, not a dangling-reference failure |
| `semantic_profile_ref` | No sufficiently strong canonical resolver identified in current contracts | Report `not_addressable` unless an existing profile artifact identity is explicitly supplied by authoritative context | Informational, not semantic-profile invalidity |
| `target_ref` | Campaign TargetSnapshot binding and existing append-time target checks | Report the exact target identity and binding status only | Currentness and supersession remain out of scope; a resolvable target is not evidence currentness |

### Resolution semantics

```text
resolved
  An existing authority identifies exactly one addressable target.

dangling
  The reference belongs to an established internal namespace, but its target
  is absent or fails the existing identity contract.

ambiguous
  More than one distinct authoritative target satisfies the reference.
  Equivalent duplicate provenance records already canonicalized by an existing
  authority do not become ambiguity merely because they have multiple receipts.

  B7 v0 does not currently emit this state. It becomes eligible only when an
  existing authoritative resolver can mechanically produce multiple valid
  matches.

not_addressable
  Current contracts do not provide a valid resolver for this reference.
```

The distinction between `dangling` and `not_addressable` is mandatory. A value
such as `brief.md` must not be declared corrupt merely because B7 cannot prove
what namespace owns it. A content-addressed `artifacts/<artifact-id>/<digest>`
reference that fails existing admission checks may be diagnosed as dangling.

### Integrity-effect semantics

```text
resolved + established internal identity
  -> pass

dangling or ambiguous + established internal identity
  -> fail

not_addressable + legacy_opaque, external_declared, or unknown class
  -> informational
```

An invalid semantic-state chain prevents trustworthy outbound resolution and
must surface the existing chain diagnostics. B7 must not weaken or replace
`SemanticStateStore.validate()`.

## 5. Minimum viable resolvers

### Campaign evidence — BUILD gate satisfied

Campaign evidence is the first meaningful non-parent resolver family.
`CampaignStore.evidence_refs()` already provides the authoritative inventory:

```text
evidence/<path>
  -> raw regular Campaign evidence

artifacts/<artifact-id>/<content-addressed-file>
  -> only when a valid admission receipt exists and its digest matches

admissions/<artifact-id>/<receipt>.yaml
  -> valid admission receipt belonging to the Campaign
```

The store enforces containment, regular-file requirements, receipt validity,
Campaign identity, artifact identity, and digest agreement. The lineage layer
adds exact consumption/provenance and immutable-byte checks. B7 can therefore
audit meaningful non-parent references by consuming existing authority rather
than implementing a second evidence catalog.

### Other fields

The remaining fields do not block B7:

- `parent_entry_ids` are already mechanically resolved by the chain validator.
- `artifact_ref` can use the admitted-artifact subset of Campaign evidence.
- `uncertainty_refs` can use the exact current uncertainty identity only.
- `claim_refs` and `semantic_profile_ref` can honestly report
  `not_addressable`.
- `target_ref` can report identity without attempting currentness.

If implementation discovers that the Campaign evidence family cannot be
resolved without inventing a new identity or namespace, this BUILD decision is
revoked and the preflight becomes `ABORT` under the rule in Section 9.

## 6. Consumer boundary

B7 v0 has exactly two planned Campaign integrations:

```text
campaign semantic-state
  -> show chain diagnostics plus reference-audit totals/details

campaign explain --ref <exact-ref>
  -> show existing occurrences plus resolution result for those occurrences
```

`campaign explain` is a rendering/integration surface, not the owner of
resolution semantics.

Resume Capsule integration is explicitly out of B7 v0. It may be reconsidered
only after later use demonstrates that resolution status improves fresh-context
reconstruction.

Summary counters must avoid a misleading generic `unresolved` total. Report at
least:

```text
resolved
dangling
ambiguous
not_addressable
integrity_failures
informational
```

## 7. Negative and rejection cases

B7 implementation qualification must cover at least:

1. Existing raw Campaign evidence ref resolves as `resolved / campaign_internal / pass`.
2. Existing admitted artifact ref resolves as `resolved / campaign_internal / pass`.
3. Missing `evidence/<path>` becomes `dangling / campaign_internal / fail`.
4. Content-addressed artifact without valid admission becomes `dangling / campaign_internal / fail`.
5. Opaque legacy `brief.md` becomes `not_addressable / legacy_opaque / informational`.
6. Opaque claim `C1` becomes `not_addressable / unknown / informational`.
7. Exact current `active_uncertainty.id` resolves only when Campaign state establishes it.
8. An unknown uncertainty value does not become a dangling internal reference without an established namespace.
9. Missing, future, or self-parent references preserve existing parent diagnostics.
10. Corrupt semantic-state chain refuses trustworthy outbound resolution and surfaces chain diagnostics.
11. `AMBIGUOUS` remains reserved but explicitly deferred in B7 v0 because no
    current authoritative resolver can mechanically produce multiple valid
    matches; no synthetic ambiguity fixture or namespace is permitted.
12. No Campaign resolver context means Campaign-dependent references are `not_addressable`; B7 must not guess from the filesystem.
13. Filename resemblance never promotes a file to canonical artifact identity.
14. Resolution never emits semantic support, truth, relevance, currentness, or responsibility claims.

## 8. Explicit non-goals

B7 does not introduce:

```text
universal reference URI scheme
universal SemanticReferenceRegistry
universal Claim or Evidence runtime objects
uncertainty-history storage
currentness or supersession propagation
decision-chain reconstruction
authority-precedence resolution
Campaign schema v3
SemanticStateEntry schema v2
Resume Capsule changes
Repository Change Semantics
Semantic Map diff
new probes or language expansion
Qualification Kit
automatic ranking, routing, or Skill selection
```

`SemanticStateStore.validate()` retains its current meaning: structural and
hash-chain integrity of the companion log. B7 adds a separate outbound
reference audit; it does not silently turn every audit finding into a chain
validation failure.

## 9. Abort gate

The B7 implementation must stop before production code if its design requires
any of the following:

```text
inventing a universal reference namespace
creating a Claim, Evidence, or Uncertainty registry
guessing local versus external ownership from string shape
making every opaque legacy value fail validation
duplicating Campaign evidence/admission/lineage authority
answering currentness, support, truth, or semantic relevance
```

The decisive abort condition is:

```text
Only parent_entry_ids are resolvable,
and every meaningful non-parent resolver requires invented semantics.
```

If that condition occurs:

```text
ABORT B7
→ Construction Diminishing-Returns Gate reached
→ move toward empirical/native-harness validation
```

The condition is not currently present because Campaign evidence already has
an authoritative addressable contract.

## 10. Future implementation boundary

This preflight authorizes design-to-implementation handoff only for the
following bounded package:

| Future surface | Responsibility |
| --- | --- |
| `src/sensemaking_skills/semantic_architecture/reference_audit.py` | Pure reference-audit models and field-specific mechanical resolution |
| `src/sensemaking_skills/campaign_observability_cli.py` | Render audit results through `campaign semantic-state` and `campaign explain` |
| `tests/test_semantic_reference_audit.py` | Primitive contract, status semantics, and negative cases |
| Existing Campaign observability tests | CLI integration and non-recommendation boundaries |
| Documentation adjacent to this preflight | Record actual implementation behavior and qualification evidence |

No file above is modified by this preflight. Implementation must reuse current
Campaign evidence/admission/lineage authority and preserve Campaign schema v2.

## 11. Post-B7 decision

After implementation and exact-head mechanical qualification:

```text
reassess from zero
```

Ask only:

```text
Is there another concrete, currently consumed,
mechanically decidable product or integrity gap?
```

If no, or if the next choice depends primarily on whether agents benefit from
the new capability, invoke empirical/native-harness validation. Do not maintain
a presumptive B8/B9 queue.

## Final preflight outcome

```yaml
decision: BUILD
package: B7 Semantic Reference Resolution & Integrity Audit v0
mode: standalone primitive with Campaign rendering adapters
meaningful_non_parent_resolver: campaign_evidence
new_universal_namespace: false
campaign_schema_change: false
semantic_authority_added: false
resume_capsule_change: false
post_b7_queue_pre_authorized: false
ambiguous_v0: explicitly_deferred_unreachable_under_current_authorities
```
