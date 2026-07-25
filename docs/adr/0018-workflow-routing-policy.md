# ADR 0018: Workflow-Routing Policy

**Status**: PROPOSED — draft for owner review, not yet accepted
**Date**: 2026-07-25
**Resolves**: Issue #33 (was blocked by #28, #29 — both now resolved: #28 closed, #29 drafted in ADR 0014)

---

## Context

Once `repository_sensemaking_brief.md` exists, something must decide which
downstream workflow consumes it. The proven golden path (#28/#38/#39)
established the mechanics for exactly one path (architectural-review); this
ADR generalizes the routing rule using the product boundary from ADR 0014.

## Decision

Routing is a **deterministic function of the brief's `primary_fog_type`
field**, produced by `repo-sensemaker` and read by `workflow-planner`
(exactly as already implemented — see
`skills/workflow-planner/references/workflow-registry.yaml` and ADR 0005).
No routing decision is made by free-form model judgment at the
`workflow-planner` step; the mapping is a static table:

| `primary_fog_type` | Routed workflow |
|---|---|
| `architecture_fog` | `architectural-review-planning-workflow` (proven, #28/#38/#39) |
| other fog types | Deferred — no other fog-type → workflow mapping is proven end-to-end yet; `workflow-planner` must report `escalation_recommended: true` rather than guess |

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
