# Strategic Outer Loop Precision v1 — Milestone Handoff

**Status:** milestone closeout record  
**Date:** 2026-09-11  
**Scope:** Level-4 product-boundary authority, Level-3 strategic reasoning/state, Level-3↔Level-4 transition semantics, Semantic Reasoning Model integration, and bounded mechanical representation support  
**Experiments:** none required or performed

## 1. Milestone objective

Make the Strategic Outer Loop precise enough that a fresh agent can reconstruct not only current strategic state, but also:

- what strategic decision a boundary is meant to support;
- why one credible boundary was selected over another without deterministic scoring;
- what uncertainty could invalidate the selection;
- what the smallest warranted intervention is;
- when repeated weak product-level signals should be preserved as Thesis Tension;
- what work may continue while Level-4 review is unresolved;
- how Level 3 must reconcile after a Level-4 disposition;
- which subset of these concepts is mechanically representable without turning validators into semantic controllers.

The four-level control architecture remains v0 and a frozen operational baseline.

## 2. Qualified package ledger

| Package | PR | Qualified head | Merge SHA | Qualification |
| --- | --- | --- | --- | --- |
| 1 — Level-4 Product Boundary Reconciliation | #363 | `f8227944bf414779a16584d1339e8a11bb4e90e5` | `136b80707007a65d8e44a59fe87c5b6043cf5c32` | Product Validation #925 PASS; Release Candidate Distribution #98 PASS |
| 2 — Level-3 Strategic Decision Model v1 | #364 | `d78f45d8b73906ab09811a0317aebb86dbef0a34` | `0a8dcb47a7ba4ffbd72ad8c1a1d32af1e9974fc5` | Product Validation #929 PASS; Release Candidate Distribution #101 PASS |
| 3 — Level-3 Durable State Refinement v1 | #365 | `3b2ab4d0e780bb123ae60444517549d4f4951135` | `4d3ef9464afd734709d4f73adeac42b394009fbb` | Product Validation #931 PASS; Release Candidate Distribution #102 PASS |
| 4 — Thesis Tension & L3↔L4 Transition Semantics | #366 | `b50977c1211cbffe2008a1413bebc3d1daada570` | `d3052555c6023a587552c5f05f3fff1290a90028` | Product Validation #933 PASS; Release Candidate Distribution #103 PASS |
| 5 — Semantic Reasoning Model Integration | #367 | `b8b981f4ce566c5e0c255b5a9cebe4d5a559ab7b` | `9db4ec41d4558132378c1fcf9292575cd616c02a` | Product Validation #935 PASS; Release Candidate Distribution #104 PASS |
| 6 — Mechanical Contract Reassessment | #368 | `7a0f3c6f6d2636e897a147548f7b0329e2ed9d3e` | `0fbbac421a023c2b49770eec8d55b8512e02ec13` | Product Validation #937 PASS; Release Candidate Distribution #105 PASS; retained Lab Validation #62 PASS |

Package 7 is the current closeout/reassessment package. Its exact-head CI evidence is intentionally left to the PR/merge record rather than self-pinning this document and forcing recursive metadata-only qualification commits.

## 3. Package outcomes

### Package 1 — Product-boundary authority

Owner-ratified Level-4 disposition: `SUPERSEDE`.

- ADR 0014 remains historical evidence for the July 2026 narrow repository-brief boundary.
- ADR 0029 is the current accepted product-boundary authority.
- Current scope is agent-native repository decision support/control with optional Campaign durability, continuation/reconstruction support, bounded multi-repository target mechanics, and higher-scope control contracts.
- The broader current boundary does not retroactively broaden historical Goal A evidence or claim ceilings.

### Package 2 — Level-3 strategic decision reasoning

Level 3 now makes this chain explicit:

```text
Strategic Frontier / candidate boundaries
-> Strategic Decision to Support
-> qualitative comparison
-> select or decline boundary
-> decision-changing uncertainty
-> sufficient evidence
-> warranted repository responsibility
-> smallest warranted intervention
```

Qualitative lenses include mission relevance, decision value, blocking power, resolvability, consequence of error, deferral cost, reversibility, authority availability, dependency, and smallest warranted intervention.

```text
qualitative comparison != deterministic ranking
agent judgment != unexplained intuition
```

During qualification two stable documentation contracts were briefly regressed (`**Version:** v0` and the phrase `frozen operational baseline`). The tests caught both. They were restored without weakening any assertion; reasoning precision v1 is now explicitly layered over the frozen v0 control architecture.

### Package 3 — Current strategic projection

`STATUS.md` was reduced from an accumulating milestone ledger to a current Level-3 projection. Detailed historical evidence remains in ADRs, handoffs, dated audits, and Git/PR history.

The projection now explicitly carries the current Strategic Decision to Support, invalidation evidence, and smallest warranted intervention while preserving release/strategic anchors.

### Package 4 — Thesis transition semantics

A documentation-level **Thesis Tension** preserves material recurring signals that are not yet decision-changing enough for Level-4 review.

When thesis review is actually required:

```text
thesis-dependent strategic advancement
-> HOLD until Level-4 disposition + Level-3 reconciliation

independently warranted unaffected work
-> may continue if authorized
```

Every material Level-4 disposition requires Level-3 reconciliation before thesis-dependent work resumes.

### Package 5 — Shared reasoning grammar

The Semantic Architecture Reasoning Model now explicitly instantiates at Levels 3 and 4.

```text
Semantic Reasoning Model
= evidence-to-decision grammar

Four-Level Control Model
= decision scope + authority ownership

same reasoning grammar != same authority
```

`DecisionBeingSupported` is a conceptual reasoning role, not a new runtime entity.

### Package 6 — Bounded mechanical support

Mechanical reassessment found exactly two newly stable representation facts:

1. `### Current strategic decision to support` must occur as a Level-3 STATUS anchor.
2. current Level-3 state must point at `docs/adr/0029-current-product-boundary.md`.

The strategy inspect/diff/handoff surfaces now project/transport the already-authored Strategic Decision while explicitly reporting that the tool did not select it.

Not mechanized: priority, decision quality, Thesis Tension materiality, Level-4 escalation judgment, thesis-dependency judgment, or post-review semantic classification.

## 4. Final Level-3 reassessment

`docs/strategic-outer-loop-precision-v1-reassessment.md` applies the refined decision model to the post-Package-6 repository.

Result:

```text
CURRENT HIGHEST-LEVERAGE BOUNDARY
NONE SELECTED

CURRENT WARRANTED REPOSITORY RESPONSIBILITY
NONE

LEVEL-3 OUTCOME
NO_FURTHER_REPOSITORY_WORK_WARRANTED

ACTION
STOP
```

The remaining candidate directions either lack concrete current warrant, require Level-4 review, expand external authority/scope, are owner-deferred empirical work, or would improperly mechanize semantic judgment.

## 5. Claim ceilings

This milestone establishes repository/control-model coherence and mechanical representation properties only.

It does not establish:

- native-harness usefulness;
- genuine second-harness portability;
- comparative superiority;
- product-market value;
- that the qualitative Level-3 lenses improve outcomes;
- general autonomous software-development capability.

No new empirical experiment was performed.

## 6. Non-goals preserved

```text
NO StrategicPlanner / OuterLoopEngine
NO automatic Strategic Frontier ranking
NO priority / expertise / complexity / consequentiality scoring
NO automatic responsibility / capability / Skill / workflow / repository selection
NO automatic Level-4 escalation or thesis revision
NO automatic Campaign generation
NO Campaign schema v3 for convenience
NO strategic-state database
NO universal decision graph
NO cross-repository transaction/deployment coordinator
NO new experiment
```

## 7. Continuation rule

Use the refined model during ordinary repository work. Reopen repository construction only from concrete normal-use/product/integrity/reconstruction pressure or explicit owner direction.

The candidate reservoir remains idea memory, not a standing implementation queue.