# ADR 0020: Whether Wayfinder and Prototypes Belong in the Core

**Status**: SUPERSEDED — historical proposal, never Accepted
**Date**: 2026-07-25
**Superseded on**: 2026-08-18
**Proposed resolution for**: Issue #35 (closed `not planned` / superseded)

## Current disposition

This July proposal is retained as historical rationale, but it is not current
product authority.

- ADR 0014's accepted product boundary does not make Wayfinder-style issue
  maps, prototype branch management, or generic planning orchestration part of
  the first-release core.
- ADR 0018's deterministic routing proposal was superseded and never Accepted.
  Under the current agent-native model, the active coding agent may select
  research or prototyping when warranted; it does not need a Wayfinder runtime
  primitive or universal prototype-routing rule to do so.
- Wayfinder-style maps may remain useful planning artifacts for humans or
  agents, but they are not consumed as core runtime authority by default.
- Prototype findings do not become canonical evidence merely because a
  prototype exists. They influence later decisions only insofar as preserved
  evidence supports the current warrant and any applicable evidence contract.
- Closing issue #35 did not retroactively accept this ADR. A future first-class
  prototype lifecycle or Wayfinder runtime requires recurring evidence of need
  and a new explicit product decision.

Everything below this point is the original July proposal and evidence note,
preserved for historical context.

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

---

## Hypothesis

Wayfinder-style decision maps and throwaway prototype branches remain
optional, planning-time human activities, not first-class runtime concepts
the orchestrator must own.

## Supporting evidence

- The proven golden path (PR #57, #59, #60, #62, #64, #65) never invokes,
  references, or depends on Wayfinder or any prototype-branch mechanism —
  the entire proof chain runs through `repo-sensemaker` and
  `architectural-review` only, consistent with Wayfinder being outside the
  core runtime.
- `git reset --hard` / `git clean -fd` rollback discipline is exercised in
  `scripts/test-controlled-failures.py` (pre-existing) and echoed in PR
  #65's own disposable-worktree/clone teardown discipline, supporting the
  claim that no special lifecycle tooling is needed for throwaway branches.

## Missing evidence

- Nothing in the merged campaign touches issue #27 (Wayfinder) or any
  prototype-promotion path; this ADR is a scope decision by omission
  ("nothing needed it, so it isn't in scope") rather than a decision tested
  by an attempt to bring Wayfinder in-scope and observing it fail.
- Per the task instructions for this revision, issue #27 / Wayfinder itself
  was read-only reference material and was not modified or re-evaluated in
  depth here.

## Experiment or review trigger

Revisit if a future feature needs prototype findings to become validated
evidence without a full `repository_sensemaking_brief.md` round-trip — that
would be the first real pressure-test of this boundary.

## Status rationale

Remains **Proposed**. Pure product-boundary decision; the merged campaign
neither touched nor was blocked by Wayfinder, so there is no new evidence
pushing this toward Provisional or Accepted — owner sign-off is required to
settle it either way.
