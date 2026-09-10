# Phase 10 Episode 2 — React incremental game / handoff reconciliation

**Source capability:** `output-reconciler` reasoning discipline  
**Target:** `ThorStarlord/React_incremental_game_prototype@d2c6a156833266fa633c704749aa99ee3ba72881`  
**Additional live surface:** PRs #66 and #68 at episode query time  
**Companion profile:** `episode-2-react-incremental-profile.yaml`

## Episode result

This episode tests the profile under a condition the canonical handoff itself warns about: repository content is immutable at the pinned SHA, while PR state can continue changing independently.

The exact-SHA `STATUS.md` says M25 remains the product authority, human product validation is unproven, valid V2 participant evidence was not collected, and M26 is not authorized. It also explicitly instructs future sessions to re-read PR state rather than trust the handoff snapshot.

The live reconciliation found:

- PR #66 remains open and draft; its current body still records no Observation 001 and no participant evidence;
- PR #68 remains open and unmerged; its current body still records the prelaunch isolation stop rather than participant evidence or a V2 verdict.

So the substantive product-evidence ceiling remains supported within the inspected scope.

## What the profile added

This episode shows the strongest Phase 10 value so far:

- immutable exact-SHA evidence and live mutable GitHub metadata are represented separately rather than collapsed into one idea of "current";
- the derived claim is explicitly bounded to the snapshot plus the live PR surfaces actually inspected;
- the profile forces the continuation-relevant uncertainty to remain visible: valid evidence could exist outside those surfaces;
- a fresh context can see immediately why "handoff says PR X was open" is not sufficient current-state evidence.

This is not merely formatting. A stale PR-state assumption could authorize or block the wrong next action.

## What it duplicated

`output-reconciler` already has strong native concepts for baseline, currentness, like-for-like checks, `verified | disputed | omitted`, uncertainty, and limits. The React handoff also explicitly tells future sessions to reconcile live PR state.

Therefore the profile duplicates much of the *local reasoning method*, even though it provides a useful cross-artifact summary.

## Embedding assessment

The episode does **not** show that the entire common profile belongs inside `reconciliation_report`. The local artifact already represents claim classifications and evidence.

It does show one reusable pressure worth preserving across analytical workflows: **target/currentness provenance must distinguish immutable snapshot evidence from time-varying external metadata when both affect a decision**.

That distinction is already conceptually present in the Reasoning Model and can remain in the companion profile unless another domain artifact repeatedly lacks it.

**Episode signal:** favors **Outcome A — keep companion**, with high currentness/reconstruction value and moderate duplication.

## Measured/observed experiment notes

- Material omission/staleness risk caught: **yes — live PR state required independent verification before continuation**.
- Fresh-context utility: **high**.
- Domain-semantic duplication: **moderate** because output-reconciler already models currentness and bounded verification.
- Validator overreach observed: **none**.
- Local-only Probe Engine metrics: **unmeasured on connector surface**.
- Exact token overhead: **not instrumented**; the profile is additional coordination cost, but the currentness distinction was decision-relevant enough to justify the companion artifact in this episode.

## Non-claim

This reconciliation does not prove that no human/product evidence exists anywhere. It establishes only that the inspected durable repository and live PR surfaces still support the handoff's current evidence ceiling.
