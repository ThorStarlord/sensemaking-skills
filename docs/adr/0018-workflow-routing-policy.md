# ADR 0018: Workflow-Routing Policy

**Status**: SUPERSEDED — 2026-08-18; historical proposal, never Accepted
**Date**: 2026-07-25 (superseded 2026-08-18)
**Historical proposal for**: Issue #33

## 2026-08-18 disposition — superseded by agent-native responsibility selection

This ADR preserves a July proposal for deterministic workflow routing, but it
never became an Accepted repository decision. The proposal assumed that a
brief's `primary_fog_type` should deterministically select downstream work.
Later accepted agent-native architecture moved responsibility selection to the
**active coding agent**, using repository evidence and current uncertainty to
decide what responsibility is warranted next before choosing a Skill or
subflow.

`primary_fog_type` remains useful **diagnostic metadata**. It can help describe
the repository's weakest boundary, but it does not itself grant execution or
routing authority. Deterministic registered subflows may still exist after a
responsibility has already been selected; this disposition does not delete or
change existing runtime routing, compatibility mechanics, workflow registry
behavior, schemas, validators, Skills, artifact contracts, or Workflow-v0.

ADR 0017 is now superseded and is therefore no longer an operative readiness
gate for adding routing rows or other capabilities. No replacement automatic
routing policy is being Accepted here. The current governing distinction is:

> Decision selects the work. Orchestration coordinates already-selected work.
> Evidence determines what becomes warranted next.

Everything below is retained as the historical July proposal and rationale.

---

## Context

Once `repository_sensemaking_brief.md` exists, something must decide which
downstream workflow consumes it. The proven golden path — PR #57 (issue
#55), PR #59 (issue #58), PR #60 (issue #56), PR #62 (issue #61), PR #64
(issue #63), PR #65 (issue #51) — established the mechanics for exactly one
path (architectural-review); issue #39's original unverifiable claim is
superseded by this evidence and is not cited as authority here. This ADR
generalizes the routing rule using the product boundary from ADR 0014.

## Decision

Routing is a **deterministic function of the brief's `primary_fog_type`
field**, produced by `repo-sensemaker` and read by `workflow-planner`
(exactly as already implemented — see
`skills/workflow-planner/references/workflow-registry.yaml` and ADR 0005).
No routing decision is made by free-form model judgment at the
`workflow-planner` step; the mapping is a static table:

| `primary_fog_type` | Routed workflow |
|---|---|
| `architecture_fog` | `architectural-review-planning-workflow` (proven live, positive and negative paths: PR #57, #59, #60, #62, #64, #65) |
| other fog types | Deferred — no other fog-type -> workflow mapping is proven end-to-end yet; `workflow-planner` must report `escalation_recommended: true` rather than guess |

This intentionally does **not** attempt to define research/prototype/human-
grilling/task-generation routing in this ADR — those require their own
proven producer→consumer path first (per ADR 0017's readiness criteria)
before they can be added to the table. Adding a row to this table is the
acceptance bar for "this fog type is routable."

`workflow_orchestration_plan.md`'s `escalation_recommended` field (already
in the artifact contract) is the mechanism for "no confident route exists" —
already implemented and was the subject of the critical bug fix noted in
memory (escalation flag being ignored, since fixed).

## Consequences
- #34 (findings → tracker tasks) can only route to `to-issues`-style
  artifact production, per the ADR 0014 product boundary — not third-party
  tracker writes.
- #35 (Wayfinder/prototypes) is out of this routing table until it has a
  proven producer→consumer path of its own.
- Extending routing to a new fog type is a normal feature addition, gated
  by ADR 0017.

## Owner sign-off required
Product-direction decision; confirm or amend before treating as Accepted.

---

## Hypothesis

Routing from a brief's `primary_fog_type` to a downstream workflow is a
static, deterministic table lookup, not free-form model judgment; only
`architecture_fog` -> `architectural-review-planning-workflow` is populated
today, and every other fog type must escalate.

## Supporting evidence

- `skills/workflow-planner/references/workflow-registry.yaml` and the
  runtime's routing code already implement table-driven routing (ADR 0005),
  and `docs/mode-coverage.yaml`'s `workflow_families_proven` list contains
  exactly one entry, `architectural-review-planning-workflow` — matching
  this ADR's single populated table row.
- PR #65's evidence directly exercises this single route end-to-end,
  live, positive and negative, confirming the one populated row actually
  works as claimed.
- The `escalation_recommended` field is a declared, contract-tracked field
  (per ADR 0015) and its "was ignored, now fixed" history is documented in
  project memory as a resolved bug, not an open risk.

## Missing evidence

- No merged evidence exercises routing for any fog type other than
  `architecture_fog` — the "other fog types -> escalate" row is unproven by
  omission (nothing has been run to confirm escalation actually fires
  correctly for, say, a `logic_fog` or `intent_fog` brief).
- No evidence tests what happens if a brief's `primary_fog_type` is
  malformed or absent — an edge case this ADR's table doesn't address.

## Experiment or review trigger

Adding any new row to this table requires its own proven producer->consumer
path per ADR 0017 first. Revisit if `escalation_recommended` is observed
firing incorrectly (false positive/negative) in a future live run.

## Status rationale

Remains **Proposed**. The single populated row is evidence-backed, but the
ADR as a whole asserts a general routing *policy* (deterministic table,
escalate on no match) that extends beyond what's been tested — the general
mechanism claim needs owner sign-off even though its one worked example is
solid.
