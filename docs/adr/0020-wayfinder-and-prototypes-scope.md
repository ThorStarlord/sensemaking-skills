# ADR 0020: Whether Wayfinder and Prototypes Belong in the Core

**Status**: PROPOSED — draft for owner review, not yet accepted
**Date**: 2026-07-25
**Resolves**: Issue #35 (was blocked by #29, #33 — both drafted in ADR 0014, ADR 0018)

---

## Context

Wayfinder-style decision maps (this very issue map, #27) and prototype
tickets raise the question of whether decision-mapping and
throwaway-branch prototyping should be first-class runtime concepts.

## Decision

**Remain optional, not core**, per the ADR 0014 product boundary: the
product's job is diagnosis → routing → validated artifact production for
one proven fog type at a time (ADR 0018). Decision-mapping across many
open strategic questions (what Wayfinder is doing right now, in this issue
map) is a *planning-time* activity for the repo owner, not a *runtime*
capability the orchestrator needs to own.

- Issue-tracker maps (like #27) relate to runtime artifacts only loosely:
  they group related ADRs/issues for human tracking, they are not consumed
  by any validator or workflow step.
- Prototype findings do **not** automatically become validated evidence —
  a prototype branch's findings must go through the same evidence policy
  (ADR 0016) and be captured in a real `repository_sensemaking_brief.md`
  before they count as evidence.
- Uncertainty threshold for "prototype instead of ordinary planning" is
  deliberately left as a human judgment call, not a formula — this avoids
  over-specifying a rarely-exercised path per ADR 0017's "don't build
  infrastructure without proven need."
- Throwaway branches are disposed via ordinary git branch deletion; no
  special runtime lifecycle management is needed (matches the
  `git reset --hard` / `git clean -fd` rollback pattern already proven in
  `scripts/test-controlled-failures.py`).

## Consequences
- No Wayfinder-specific runtime code is in scope.
- If prototype→evidence promotion becomes a recurring need, that's a
  future ADR revision with its own proven producer→consumer path (ADR
  0017), not a default assumption.

## Owner sign-off required
Product-direction decision; confirm or amend before treating as Accepted.
