# Campaign Productization v1 — Closeout Handoff

**Status:** repository-qualified closeout  
**Date:** 2026-09-11  
**Authority:** implementation/qualification record only; current strategic state remains `STATUS.md`  
**Experiments:** no new native-harness, user, comparative, or product-value experiment was performed  
**Campaign schema:** remains v2

## Purpose

This handoff records the owner-directed repository-only/hermetic construction sequence completed after the owner explicitly declined additional experiments as a prerequisite for continued building.

The sequence changes the construction gate, not the empirical evidence ceiling:

```text
explicit owner direction
-> may authorize bounded repository-only/hermetic construction

repository qualification
!= native-harness usefulness proof
!= portability proof
!= comparative superiority
!= general autonomous-development proof
```

## Delivered package ledger

| Package | PR | Merge SHA | Exact-head qualification |
| --- | --- | --- | --- |
| Campaign Preflight v0 | #341 | `80d94fa4956c6619226b7e2f6544267eeefe8a86` | Product Validation + Release Candidate Distribution PASS |
| Resume Capsule v1 | #342 | `a2f9c94372dc4c2069da5468e52b05e0979ebbc5` | Product Validation #876, Release Candidate Distribution #69, Lab Validation #35 PASS |
| Uncertainty History v0 | #343 | `130deed1deb01e2082fa82c90613812b87ca9c7d` | corrected exact head passed Product Validation #879, Release Candidate Distribution #71, Lab Validation #38 |
| Campaign Operability v1 | #344 | `3e283f19f808f0d7cc826143f6f09d5f7cbb3b97` | Product Validation #881, Release Candidate Distribution #72, Lab Validation #40 PASS |
| Extensibility & Simplification v1 | #345 | `4dc4ef13af7e5250d2502ecdab58b936e90aa99b` | Product Validation #883, Release Candidate Distribution #73, Lab Validation #42 PASS |

The first Uncertainty History candidate exposed a test-fixture mismatch: `Uncertainty.consequences` was supplied as a tuple although the canonical contract requires a mapping. The fixture was corrected; no runtime semantic repair was needed. The corrected head was requalified before merge.

## Delivered product surfaces

Campaign productization:

```text
campaign preflight
campaign resume-context --compact
campaign resume-context --include-preflight
campaign uncertainty-record
campaign uncertainty-history
```

Campaign operability:

```text
campaign doctor
campaign provenance --format markdown|json
campaign graph-integrity
```

Extensibility/developer ergonomics:

```text
semantic catalog
scripts/validate-candidate-directions.py
```

Repository simplification:

```text
campaign graph
campaign graph-integrity
        |
        v
shared CampaignProvenanceGraphService
```

The shared graph service removes parallel graph-construction logic while keeping rendering and integrity diagnostics separate at the CLI boundary.

## Preserved authority boundaries

The sequence deliberately did not introduce:

- Campaign schema v3;
- an `OuterLoopEngine` or `StrategicPlanner`;
- automatic responsibility selection or ranking;
- automatic uncertainty selection or ranking;
- automatic semantic repair;
- semantic causality inference from provenance edges;
- GitHub publication of generated Campaign provenance;
- native-harness execution controlled by Sensemaking;
- new operative experiment state.

Important non-identities remain:

```text
preflight PASS != should proceed
doctor clean != responsibility warranted
uncertainty history valid != lifecycle judgment semantically correct
uncertainty history != current active-uncertainty authority
semantic catalog hit != Skill selected
graph integrity PASS != semantic causality
generated provenance != published provenance
repository qualified != native-harness qualified
owner direction to build != empirical product-value proof
```

## Current disposition

The authorized sequence is complete.

```text
CAMPAIGN PRODUCTIZATION v1 = COMPLETE / REPOSITORY_QUALIFIED
CAMPAIGN OPERABILITY v1 = COMPLETE / REPOSITORY_QUALIFIED
EXTENSIBILITY & SIMPLIFICATION v1 = COMPLETE / REPOSITORY_QUALIFIED
EMPIRICAL CLAIM CEILINGS = UNCHANGED
NEXT PACKAGE = NOT SELECTED BY THIS CLOSEOUT
```

Future repository-only/hermetic construction may be authorized by a concrete mechanically expressible product/integrity need or explicit owner direction. Stronger empirical/native-harness claims still require the evidence specified by their own protocols.

## Current navigation

- Current Level-3 state: [`../STATUS.md`](../STATUS.md)
- Current Level-4 strategy: [`product-strategy.md`](product-strategy.md)
- Frozen control model: [`strategic-outer-loop.md`](strategic-outer-loop.md)
- Non-authoritative future possibilities: [`strategic-candidate-directions.md`](strategic-candidate-directions.md)
- Current operations/qualification runbook: [`operations-runbook.md`](operations-runbook.md)
- Campaign Preflight contract: [`campaign-preflight.md`](campaign-preflight.md)
- Resume Capsule v1 contract: [`resume-capsule-v1.md`](resume-capsule-v1.md)
- Uncertainty History contract: [`uncertainty-history.md`](uncertainty-history.md)
- Campaign Operability contract: [`campaign-operability-v1.md`](campaign-operability-v1.md)
- Extensibility & Simplification contract: [`extensibility-and-simplification-v1.md`](extensibility-and-simplification-v1.md)

This handoff is historical/implementation evidence after the closeout. If it later disagrees with `STATUS.md`, current code, or checked-in CI, those current authority surfaces govern their respective scopes.