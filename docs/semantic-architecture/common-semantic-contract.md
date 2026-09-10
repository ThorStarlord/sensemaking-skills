# Experimental Common Semantic Contract — `semantic_reasoning_profile` v1

**Status:** Experimental Level 3 contract; retained as an optional companion artifact after Phase 10 Outcome A  
**Derived from:** Phase 9 Pilots A, B, and C  
**Further tested by:** Phase 10 Chess Mentor Engine, React incremental game, and ViralFactory episodes  
**Validator:** `scripts/validate-semantic-reasoning-profile.py`  
**Campaign admission:** Not registered  
**Purpose:** Mechanically validate the smallest cross-Skill reasoning representation demonstrated by the semantic-alignment pilots, for selective cross-artifact audit/reconstruction use.

## Decision

Phase 9 found a stable shared representation across:

- repository diagnosis (`repo-sensemaker`);
- inherited-evidence architectural recommendation (`architectural-review`);
- post-change verification/reconciliation (`repair-verifier` + `output-reconciler`).

The repeated core is:

```text
target/currentness
observations
material claims
claim epistemic status
evidence references
bounded scope / limits
uncertainties
explicit limits
```

That repetition was sufficient to implement a **standalone representation validator**. Phase 10 then tested whether the representation should remain companion-level or be embedded into canonical domain artifacts.

The qualified Phase 10 decision is **Outcome A**:

> Keep `semantic_reasoning_profile` v1 as an optional companion reasoning/audit/reconstruction artifact.

Phase 10 did **not** find sufficient evidence to change Campaign state, force the profile into every Skill artifact, or create a Repository Semantic Map.

## Why this is Level 3

The contract has an executable validator that can reject mechanically invalid representations. It can establish only properties such as:

```text
required fields exist
ids are unique
enums are recognized
evidence-ref fields have the required shape
claim scope/limits are represented
currentness status is represented
material claim statuses that require evidence actually cite evidence
```

It cannot establish:

```text
a claim is true
a source is sufficient
a chosen uncertainty is the most important one
a responsibility is warranted
an architectural relation is a violation
a repair succeeded
a Campaign should advance
```

Therefore:

```text
profile validator PASS
!= semantic reasoning is correct
```

## Contract

The v1 schema is unchanged by Phase 10.

```yaml
artifact_id: semantic_reasoning_profile
schema_version: 1
pilot_id: <non-empty stable episode/pilot identifier>
source_skill: <non-empty Skill/capability identity>
target:
  repository: <non-empty repository/target identity>
  ref: <non-empty exact snapshot/ref/inherited-artifact identity>
  access_mode: github_exact_sha | local_snapshot | inherited_artifact
currentness:
  status: pinned_snapshot | verified_current | inherited_currentness | unverified
  evidence_refs:
    - <zero or more refs; required non-empty unless status is unverified>
observations:
  - id: <unique non-empty id>
    statement: <non-empty mechanically/directly observed statement>
    method: direct_read | probe | git_metadata | validator_output | artifact_read | owner_statement | other
    evidence_refs:
      - <at least one non-empty ref>
claims:
  - id: <unique non-empty id>
    statement: <non-empty material claim>
    epistemic_status: OBSERVED | DERIVED | INFERRED | HYPOTHESIZED | RATIFIED | CONTRADICTED | SUPERSEDED | UNRESOLVED
    evidence_refs:
      - <refs required for all statuses except a genuinely evidence-seeking HYPOTHESIZED/UNRESOLVED claim>
    scope: <non-empty bounded scope>
    limits:
      - <zero or more non-empty non-claims>
uncertainties:
  - id: <unique non-empty id>
    question: <non-empty decision-relevant question>
    decision_relevance: <non-empty explanation>
    evidence_needed:
      - <zero or more bounded evidence needs>
    status: active | resolved | deferred
explicit_limits:
  - <at least one material non-claim/blind spot>
```

## Validator invariants

The validator is intentionally narrow.

### It rejects

- wrong artifact identity or schema version;
- missing required top-level keys;
- unsupported target/currentness/method/status values;
- duplicate observation, claim, or uncertainty IDs;
- malformed string-list fields;
- observations without evidence refs;
- evidence-grounded claim statuses without evidence refs;
- non-empty currentness claims without currentness evidence, except explicitly `unverified`;
- an empty `explicit_limits` list.

### It accepts

- semantically incorrect claim text if the representation is structurally valid;
- competing claims;
- hypotheses with no evidence yet when explicitly labeled `HYPOTHESIZED`;
- unresolved claims with no current evidence when explicitly labeled `UNRESOLVED`;
- any reasonable domain vocabulary inside statements/scope/limits.

That acceptance behavior is important: the validator must not pretend it can understand semantic truth.

## Relationship to canonical Skill artifacts

The profile remains a **companion artifact**:

```text
canonical Skill/domain artifact
        +
optional semantic_reasoning_profile
```

It does not replace:

- `repository_sensemaking_brief`;
- `architectural_review_recommendation`;
- `repair_verification_report`;
- `reconciliation_report`;
- PM or other domain-specific artifacts such as `risk_analysis`.

Domain-specific enums and schemas remain authoritative for their local artifacts.

## When to use the companion profile

Phase 10 demonstrated enough value to retain optional use when one or more of these conditions applies:

- reasoning spans multiple artifacts or evidence surfaces with different currentness semantics;
- a fresh context needs a compact warrant/provenance index;
- an experiment or review compares reasoning across Skills/domains;
- local domain vocabulary makes cross-domain audit unnecessarily expensive.

The React Phase 10 episode showed the clearest positive case: an exact-SHA handoff and live mutable PR metadata needed separate currentness treatment before continuation.

## When not to require it

Do not require the profile merely because an analytical artifact exists.

Phase 10 showed substantial duplication when strong domain artifacts already contain the relevant semantics. In particular, PM `risk_analysis` already represents evidence status, evidence refs, uncertainty, mitigations, recommendation boundaries, and unresolved questions. Repeating those fields in a second mandatory representation would add ceremony without increasing semantic authority.

The profile should therefore remain absent when:

- the canonical artifact already carries the decision-changing evidence/currentness/uncertainty/limits;
- no cross-artifact or fresh-context reconstruction need exists; and
- the second representation would mostly restate domain-local semantics.

## Relationship to Campaigns

This contract remains intentionally **outside `validate-and-report.py` routing and the Campaign capability/admission catalog**.

Phase 10 demonstrated reconstruction value, but not that Campaign correctness requires this profile or any subset of it to survive as consequential control-plane state.

Before Campaign promotion, later evidence must independently show that a stable subset must survive across sessions as consequential state rather than merely comparative/debugging evidence.

## Phase 10 evidence

Phase 10 used three additional real-repository episodes:

- Chess Mentor Engine — direct `repo-sensemaker` reasoning;
- React incremental game — `output-reconciler` currentness reconciliation across immutable repository snapshot and live PR metadata;
- ViralFactory — PM `pre-mortem`, comparing canonical `risk_analysis` with the companion profile.

The experiment found:

- selective cross-artifact/fresh-context reconstruction value;
- one material currentness-sensitive case in the React episode;
- moderate-to-high duplication with strong local artifacts;
- no reason to transfer semantic judgment into the validator;
- no repeated missing field across at least two domain artifacts sufficient to justify selective embedding.

See `phase-10/results.md` and `phase-10-handoff.md`.

## Future promotion / rejection criteria

Reconsider selective embedding only if at least two later contrasting domain artifacts repeatedly omit the same decision-changing field and companion reconstruction is insufficient or operationally costly.

Narrow or retire the profile if later evidence shows it mostly duplicates domain artifacts, encourages fake claims/uncertainties, or costs more coordination than it saves.

Do not broaden the schema merely because the ontology contains more concepts.

The success criterion remains **more consistent warranted reasoning per unit of coordination overhead**, not ontology coverage.
