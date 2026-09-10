# Phase 9 Pilot B — architectural-review

**Pilot status:** Completed on pinned repository/Skill evidence  
**Source Skill:** `skills/architectural-review/`  
**Target repository:** `ThorStarlord/sensemaking-skills`  
**Pinned target ref:** `8109b0a7133abb8363f808d01292f5f7375d766f`  
**Purpose:** Test the Reasoning Model in a downstream Skill that inherits diagnosis/evidence and makes an architectural recommendation.

## Question under test

Does the Pilot A comparison core remain useful when a Skill does not re-probe the repository, and can architectural entities/relations be reasoned about without upgrading structural observations into architectural truth?

## Before alignment

`architectural-review` already had several strong boundaries:

- it consumes `repository_sensemaking_brief` rather than re-diagnosing the repository;
- it evaluates a caller-supplied proposed direction;
- it returns `investigate_first` when the brief is insufficient;
- it separates proposal evaluation from the original fog diagnosis;
- it requires specific rather than generic risks.

The main semantic ambiguity was the phrase **"trust the brief as the authoritative fog classification and evidence base"**. As written, it could be misread as permission to flatten all upstream claims into equal-strength truth. The Skill also lacked an explicit distinction between a mechanically supported dependency relation and an inferred architecture violation.

## Competency questions exercised

- CQ-CUR-2 — What currentness boundary is inherited from an upstream artifact?
- CQ-ARC-1 — What counts as a Component/Layer/Boundary for the current decision?
- CQ-ARC-3 — Which dependency relation is observed or derived?
- CQ-ARC-5 — What evidence establishes intended architecture?
- CQ-EPI-1 — Which architectural statements are observed, inferred, hypothesized, or ratified?
- CQ-EPI-4 — What does conflicting current structure and ratified intent establish?
- CQ-UNC-2 — Which missing evidence should force `investigate_first`?
- CQ-WRK-3 — Is capability execution authorized without changing diagnosis responsibility?

## Observed reasoning seams

### Seam A — inherited evidence versus ratified truth

The Skill should preserve upstream provenance:

```text
brief says X with evidence E and status INFERRED
-> architectural-review may consume X as an inherited claim
-> it does not become RATIFIED because a downstream Skill consumed it
```

The review remains scoped: it does not re-diagnose X, but it may determine that the inherited warrant is insufficient for the proposed architectural decision.

### Seam B — dependency versus violation

A source/import relation may be mechanically established while the architectural judgment requires additional evidence:

```text
DERIVED: A depends on B
RATIFIED/DOCUMENTED: boundary rule says A may depend only on interface I
INFERRED: A -> B conflicts with the intended boundary
JUDGMENT: proposal addresses / fails to address that conflict
```

This is the first pilot to exercise `Component`, `Layer`, `Boundary`, `Contract`, and `DependencyRelation` semantics.

### Seam C — proposal risk versus current defect

A proposal may create a plausible future risk without the repository currently exhibiting that failure. Pilot B therefore distinguishes current evidence-backed risk from `HYPOTHESIZED` proposal-contingent risk.

## Alignment applied

`skills/architectural-review/SKILL.md` now:

- narrows "authoritative brief" language to workflow-input authority rather than semantic truth;
- preserves inherited currentness and epistemic distinctions;
- forbids inferring architecture intent from directory shape alone;
- requires architecture-violation claims to establish the relevant boundary/contract/intent;
- makes risk status and explicit limits part of material reasoning;
- states that validator PASS is mechanical, not architectural correctness.

A new `references/semantic-reasoning-alignment.md` gives bounded architectural examples without changing the existing recommendation artifact schema.

## Invalid inference jumps prevented

1. `brief contains claim C -> C is ratified truth`.
2. `A imports B -> architecture violation`.
3. `folder named domain -> canonical Domain Layer exists`.
4. `proposal could create risk R -> R is a current observed defect`.
5. `recommendation validates -> architectural verdict is correct`.

## Cross-pilot comparison with Pilot A

Stable across both pilots:

```text
target/currentness
evidence provenance
material claims
epistemic status
uncertainty
explicit limits
```

Different establishment mode:

```text
Pilot A: currentness and observations are primarily direct/probed.
Pilot B: currentness and evidence are primarily inherited from an upstream artifact.
```

Architecture-specific concepts that should remain outside the common core:

```text
Component
Layer
Boundary
Contract
DependencyRelation
architectural risk
```

## Coordination overhead

Moderate but bounded. The Skill already reasons about evidence and risk; the new burden is preserving inherited warrant and making structural-versus-semantic transitions explicit only where they affect the verdict.

## Candidate common fields after two pilots

Two contrasting Skills now reuse:

- `target/currentness`;
- `observations` or inherited observations;
- `claims` with epistemic status and evidence refs;
- `uncertainties`;
- `explicit_limits`.

This satisfies the implementation plan's minimum cross-Skill repetition threshold for an **experimental** common representation, but a third repair/reconciliation pilot is still needed before deciding its final minimal shape.

## Result

**Pilot B supports an experimental common semantic profile.** It also confirms that common semantics should describe warrant/provenance rather than architecture-specific entity graphs.

## Explicit limits

- This pilot does not establish a universal component model.
- It does not give validators authority to classify architectural violations.
- It does not change `architectural_review_recommendation` fields.
- It does not authorize direct repository re-diagnosis from architectural-review.
