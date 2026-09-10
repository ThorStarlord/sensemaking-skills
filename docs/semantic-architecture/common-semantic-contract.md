# Experimental Common Semantic Contract — `semantic_reasoning_profile` v1

**Status:** Experimental Level 3 contract  
**Derived from:** Phase 9 Pilots A, B, and C  
**Validator:** `scripts/validate-semantic-reasoning-profile.py`  
**Campaign admission:** Not registered  
**Purpose:** Mechanically validate the smallest cross-Skill reasoning representation demonstrated by the first three semantic-alignment pilots.

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

That repetition is sufficient to implement a **standalone representation validator**. It is not sufficient to change Campaign state, force the profile into every Skill artifact, or create a Repository Semantic Map.

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

The profile is a **companion artifact** during the experiment:

```text
canonical Skill artifact
        +
semantic_reasoning_profile
```

It does not replace:

- `repository_sensemaking_brief`;
- `architectural_review_recommendation`;
- `repair_verification_report`;
- `reconciliation_report`.

Domain-specific enums and schemas remain authoritative for their local artifacts.

## Relationship to Campaigns

This contract is intentionally **not added to `validate-and-report.py` routing or the Campaign capability/admission catalog** in this milestone.

Before Campaign promotion, later evidence must show that the profile or a subset of it must survive across sessions as consequential control-plane state rather than merely comparative/debugging evidence.

## Phase 10 experiment

Phase 10 should now answer:

> Should the common semantic core remain an external companion profile, or should selected fields be embedded in multiple canonical analytical artifacts?

Measure:

- duplicated reasoning reconstruction;
- boilerplate added;
- cross-Skill ambiguity reduced;
- fresh-context usefulness;
- claim/currentness/evidence omissions caught;
- validator overreach incidents;
- token/coordination overhead.

Do not broaden the schema just because the ontology contains more concepts.

## Promotion / rejection criteria

Promote or embed fields only if repeated real episodes show material value. Narrow or retire the profile if it mostly duplicates domain artifacts or encourages agents to create fake claims/uncertainties to satisfy structure.

The success criterion is **more consistent warranted reasoning per unit of coordination overhead**, not ontology coverage.
