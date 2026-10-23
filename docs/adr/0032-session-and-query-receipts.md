# ADR 0032: Session and Query Receipts

**Status**: PROPOSED (2026-10-23). Requested in a working session; repository-owner ratification pending  
**Date**: 2026-10-23  
**Supersedes**: none  
**Level**: Level 2 operating contract for `using-sensemaking` and `repository-semantic-steward`

## Context

Every subordinate Skill writes a validated artifact (`repository_sensemaking_brief`,
`strategic_repository_analysis`, ...), but the control loop that selects them,
`using-sensemaking`, wrote nothing by default. `repository-semantic-steward`
persisted reviewed knowledge only when RECONCILE added some. RECALL and AUDIT
left no trace at all.

The 2026-10-23 observation session made the cost concrete
(`artifacts/history/2026-10-23-repository-sensemaking-brief-observation.md`,
`artifacts/history/2026-10-23-strategic-repository-analysis.md`). The session's
most consequential results were:

- a contract-violating legacy brief producer;
- an owner decision about it;
- a RECALL miss showing that reviewed knowledge covers only the knowledge
  plane itself.

All three existed only in conversation and a scratch directory that is
discarded with the container. Specifically:

- the owner question would not survive a headless run, which has no chat;
- the RECALL miss could not be rediscovered by a later session, which would
  not know the query had been asked;
- nothing would let a later session detect a *pattern* of misses.

The opposite failure, documentation theater, is also real. The owner's
"simplify hard" verdict (`STATUS.md`) and ADR 0031's success condition ("better
decisions in later, genuinely separate engineering episodes, not more ontology
rows") rule out per-session essays.

## Decision

1. **`using-sensemaking` always leaves a `sensemaking_session_receipt`**:
   - location: `.sensemaking/receipts/<session_ref>.session.yaml` in the target
     repository;
   - opened `in_progress` once goal and authority are known, updated at
     checkpoints, finalized and immutable at stop;
   - an interrupted session therefore leaves a visible tombstone.
2. **`repository-semantic-steward` records every invocation in a
   `semantic_query_receipt`** (`<session_ref>.query.yaml`):
   - pinned refs, every query and its outcome, and source checks;
   - every decision-relevant `MISS` / `NOT_ASSESSED` with what was needed and
     how it was resolved;
   - RECONCILE dispositions including `NO_MODEL_CHANGE`.
3. **Receipts are typed YAML records, not documents.** Text fields are capped
   (300/120 characters); references must be repository-relative.
   `scripts/validate-receipt.py` enforces both and is routed by
   `scripts/validate-and-report.py` / `sensemaking-skills validate`.
4. **Receipts have a consumer.** At session start `using-sensemaking` runs
   `scripts/summarize-receipts.py`. It reports:
   - unfinished sessions and open questions;
   - the last stop and next responsibility;
   - pending and repeated knowledge misses.

   RECONCILE reads the same misses.
5. **Persistence is explicit.** A receipt survives only when committed and
   pushed or uploaded by the host. Without that authority the receipt says
   `working_tree_only` and the session reports the loss. No authority is
   widened to persist a receipt.
6. **Receipts record authority and never grant it.** `action_authorized_by_receipt`,
   `action_authorized` and `semantic_truth_established` are fixed to `false`.
   Receipts are not ingested by the semantic knowledge index.

## Consequences

- The product boundary, Grounding Pack contract and stewardship direction
  stay as recorded in their own ADRs; receipts add an operating record beneath
  them.
- Every session, including a narrow one, produces a small commit-bound file. A
  narrow task yields a narrow receipt (empty lists are valid), but read-only
  sessions now create a write. This is the accepted price of crash-resilient
  stop state.
- Owner questions gain a durable home without a Campaign. A Campaign or
  `owner_decision_capsule` is still used when continuation complexity or
  tradeoffs warrant one; the receipt points to it.
- Negative knowledge becomes countable across sessions, which gives ADR 0031's
  longitudinal evaluation something to measure.
- Validation proves shape and pointer integrity only, not that recorded
  decisions were right.

## Alternatives considered

- **No default artifact; rely on existing triggered surfaces** (the prior
  design). Rejected: the triggers depend on judgment at exactly the moment a
  session is ending, and the observation session shows the judgment failing.
- **Narrative session report.** Rejected as documentation theater: unbounded,
  unvalidatable, and a context burden for the next agent.
- **Record misses as reviewed knowledge directly.** Rejected: it would promote
  unreviewed session observations into the knowledge plane. Receipts feed
  RECONCILE; review still gates knowledge.

## Reassessment triggers

- Receipts accumulate but `summarize-receipts.py` output never changes a later
  session's decision. In that case the consumer is not real; reconsider.
- Receipt size or count becomes a review burden: tighten caps, or batch
  receipts per branch.
- Hosts provide a durable run store. Then prefer `host_uploaded` over commits.
