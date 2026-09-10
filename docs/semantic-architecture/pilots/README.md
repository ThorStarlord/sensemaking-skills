# Phase 9 — Reasoning Model Operationalization & Skill Semantic-Alignment Pilots

**Status:** Three-pilot comparison completed; experimental common Level-3 profile extracted  
**Scope:** `repo-sensemaker`, `architectural-review`, `repair-verifier`, `output-reconciler`

## Purpose

These pilots operationalize the canonical Reasoning Model in real Skill contracts without introducing a central reasoning engine.

```text
Reasoning Model (design)
        |
        v
Pilot A — repository diagnosis
        |
        v
Pilot B — inherited-evidence architecture judgment
        |
        v
Pilot C — post-change verification/reconciliation
        |
        v
cross-Skill comparison
        |
        v
smallest repeated executable representation
```

## Files

- [`reasoning-profile-template.md`](reasoning-profile-template.md) — human/comparative reasoning instrument.
- [`pilot-a-repo-sensemaker.md`](pilot-a-repo-sensemaker.md) + [`pilot-a-profile.yaml`](pilot-a-profile.yaml) — direct repository diagnosis/currentness pilot.
- [`pilot-b-architectural-review.md`](pilot-b-architectural-review.md) + [`pilot-b-profile.yaml`](pilot-b-profile.yaml) — inherited-evidence architecture pilot.
- [`pilot-c-repair-reconciliation.md`](pilot-c-repair-reconciliation.md) + [`pilot-c-profile.yaml`](pilot-c-profile.yaml) — post-change outcome/repair pilot.
- [`../common-semantic-contract.md`](../common-semantic-contract.md) — first experimental Level-3 extraction and Phase 10 boundary.

## Stable cross-Skill core found

All three pilots needed:

```text
target/currentness
observations or inherited observations
material claims
epistemic status
evidence references
bounded scope / claim limits
decision-relevant uncertainty
explicit limits / non-claims
```

The pilots did **not** justify putting Skill-specific vocabularies into the common core. Fog/weakness types, Component/Layer/Boundary, architectural verdicts, repair `closed/remaining`, reconciliation `verified/disputed/omitted`, and Campaign transitions retain their local contracts.

## Result

Phase 9 supports a standalone `semantic_reasoning_profile` v1 representation validator. The profile remains an experimental companion artifact and is not registered for Campaign admission.

This is Reasoning Model operationalization, not reasoning automation:

```text
shared reasoning protocol
!= central semantic controller
```
