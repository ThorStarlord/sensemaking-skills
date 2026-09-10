# Phase 9 Pilot A — repo-sensemaker

**Pilot status:** Completed on pinned repository evidence  
**Source Skill:** `skills/repo-sensemaker/`  
**Target repository:** `ThorStarlord/sensemaking-skills`  
**Pinned target ref:** `8109b0a7133abb8363f808d01292f5f7375d766f`  
**Access surface:** read-only GitHub exact-SHA inspection plus current Skill-contract reconciliation  
**Purpose:** Test whether the Reasoning Model clarifies repository diagnosis without changing the canonical brief schema.

## Question under test

Can `repo-sensemaker` consistently distinguish mechanically observed repository state from semantic diagnosis, preserve currentness, and make the decision-changing uncertainty visible without adding a universal reasoning schema?

## Before alignment

The Skill already contained unusually strong evidence discipline:

- mandatory state-currency verification;
- exact-SHA connector-native probing;
- explicit distinction between documented and independently verified current state;
- `representation_sufficiency` as a model-authored judgment rather than a repository fact;
- relationship findings explicitly described as evidence candidates rather than diagnoses;
- Logic trace from evidence to weakest-boundary conclusion.

The remaining ambiguity was primarily **epistemic vocabulary**, not missing evidence infrastructure. Material claims could be written as prose without a shared label distinguishing `OBSERVED`, `DERIVED`, `INFERRED`, `RATIFIED`, or `UNRESOLVED`. Fog type and weakness type were also easy to mistake for the underlying consequential uncertainty.

## Competency questions exercised

- CQ-CUR-1 — What exact repository state does a claim describe?
- CQ-EVI-1 — What evidence supports the material claim?
- CQ-EVI-4 — What does a deterministic probe actually establish?
- CQ-EPI-1 — Which statements are observed, derived, inferred, or ratified?
- CQ-EPI-4 — What does a contradiction establish and not establish?
- CQ-UNC-1 — What unresolved question could change the next decision?
- CQ-UNC-4 — What evidence would resolve or materially narrow the uncertainty?
- CQ-DOC-2 — Is a documented current-state claim independently verified?
- CQ-WRK-1 — What responsibility is warranted by the evidence rather than by capability availability?

## Observed reasoning seams

### Seam A — probe result versus diagnosis

`repo-sensemaker` already says that relationship findings are evidence candidates, not diagnoses. The semantic model makes the next step explicit:

```text
mechanical relationship finding
-> OBSERVED / DERIVED evidence
-> agent review of scope/currentness/authority
-> INFERRED diagnostic claim
```

This prevents a probe from appearing to make an architectural or product judgment.

### Seam B — currentness versus documentary truth

A README/STATUS/roadmap statement can be a valid observation about documentation while still being unverified as current repository state. The Reasoning Model gives those two claims separate status rather than forcing one source to disappear.

### Seam C — fog classification versus consequential uncertainty

`architecture_fog` is useful classification metadata, but it does not answer a question such as:

> Is the apparent dependency-boundary drift intentional compatibility behavior or an unintended architecture violation?

The latter is the decision-changing uncertainty. Pilot A therefore keeps fog/weakness taxonomies while forbidding them from substituting for a specific unresolved question.

## Alignment applied

`skills/repo-sensemaker/references/evidence-rules.md` now adds explicit rules for:

- observation versus inference;
- material claim epistemic status;
- currentness as part of warrant;
- completeness requirements for absence claims;
- explicit limits/non-claims.

`skills/repo-sensemaker/references/semantic-reasoning-alignment.md` defines the full semantic chain while preserving the existing brief schema.

## Invalid inference jumps prevented

1. `probe emitted relationship finding -> therefore architectural defect exists`.
2. `documentation states X -> therefore X is current`.
3. `zero matches in searched subset -> therefore entity/behavior does not exist`.
4. `primary_fog_type = architecture_fog -> therefore the consequential uncertainty has been identified`.
5. `weakness type selected -> therefore supporting claim is observed fact`.

## Concepts used

High-value shared concepts:

```text
Target/currentness
Observation
Evidence
Claim
EpistemicStatus
Contradiction
Uncertainty
Responsibility
ExplicitLimit
```

Useful but Skill-specific concepts:

```text
fog type
weakness type
representation sufficiency
weakest boundary
```

## Concepts not warranted for common execution

Pilot A did not justify universal executable forms of:

- `Component`;
- `Layer`;
- `ProductCapability`;
- automatic confidence scores;
- automatic uncertainty priority;
- automatic workflow selection.

## Coordination overhead

Low. Most of the model maps onto evidence/currentness machinery the Skill already had. The primary added burden is labeling decision-changing claims only when the distinction matters; no new required section or machine field was added to `repository_sensemaking_brief`.

## Candidate common fields

Pilot A suggests the following comparison core is useful:

```text
target/currentness
observations
material claims + epistemic status + evidence refs
uncertainties
explicit limits
```

This is only one pilot and is not sufficient to promote a common contract by itself.

## Result

**Pilot A supports continuing Phase 9.** The Reasoning Model clarifies pre-existing repo-sensemaker behavior with low additional ceremony. The strongest improvement is separating `mechanically present evidence` from `semantic diagnosis` and making consequential uncertainty explicit.

## Explicit limits

- This pilot did not run a native external coding-agent harness.
- It tests repository/Skill reasoning semantics, not end-user task quality.
- It does not establish that the common profile should enter Campaign schema.
- It does not claim that all repo-sensemaker outputs now use epistemic labels exhaustively; the rule is decision-relative rather than boilerplate-driven.
