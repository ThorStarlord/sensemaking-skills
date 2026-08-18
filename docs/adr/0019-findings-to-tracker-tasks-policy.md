# ADR 0019: When Findings Become Recommendations versus Tracker Tasks

**Status**: SUPERSEDED — historical proposal, never Accepted
**Date**: 2026-07-25
**Superseded on**: 2026-08-18
**Proposed resolution for**: Issue #34 (closed `not planned` / superseded)

## Current disposition

This July proposal is retained as historical rationale, but it is not current
product authority.

- ADR 0014's accepted product boundary keeps generic tracker synchronization
  and direct third-party tracker writes outside the core product unless they
  are separately re-ratified.
- ADR 0018's deterministic product-level routing proposal was superseded and
  never Accepted. The active coding agent selects the warranted engineering
  responsibility; compatibility routing paths or deterministic subflows do
  not own that decision by default.
- Therefore there is no universal `finding -> tracker task` conversion policy.
  Findings and validated artifacts inform the next warranted action. Task
  creation may happen later inside an explicitly selected implementation
  responsibility or downstream consumer, but it is not automatically
  triggered by every finding and is not a core tracker-write contract.
- Closing issue #34 did not retroactively accept this ADR. A future proposal
  for direct tracker integration or deterministic task-generation authority
  requires fresh evidence and a new explicit product decision.

Everything below this point is the original July proposal and evidence note,
preserved for historical context.

---

## Context

Per ADR 0014's product boundary, third-party issue-tracker writes are
proposed as explicitly **out of scope** for this product — the handoff
artifact is the integration point, actual sync is a downstream consumer's
job. If ADR 0014 is accepted, this would resolve most of #34's open
questions by removing the "automatic tracker write" option from
consideration.

## Decision

- Every finding remains a **recommendation** (informational, in
  `repository_sensemaking_brief.md` / `architectural_review_recommendation.md`)
  until it enters an explicit implementation workflow (per ADR 0018's
  routing table).
- **Task generation** (`issue_list.md`, `agent_brief.md`) happens only as
  part of an already-routed implementation workflow's steps (`to-issues`,
  `triage`) — never automatically from a bare finding.
- Generated tasks are **artifacts in this repo's session**, not writes to
  an external tracker. "Which issue tracker is canonical" is therefore not
  this product's decision to make — it's whatever the downstream consumer
  uses to import `issue_list.md`.
- **Approval**: every implementation-workflow step that produces
  `issue_list.md` already has a `gate: review` per the golden-path gate
  mechanism (proven for `architectural-review-planning-workflow`'s own
  gates in PR #65; issue #28's narrow-scope decision) — this is the
  existing human-approval point; no new approval mechanism is needed.
  Note: no merged evidence exercises an `issue_list.md`-producing step
  specifically — this reasons by analogy to the proven gate mechanism, not
  a direct proof of task-generation gating.
- **Low-value task floods**: prevented structurally — tasks only get
  generated for a fog type with a proven route (ADR 0018), not for every
  observation in a brief.

## Consequences
- No new tracker-integration code is in scope from this decision.
- If a future need arises for direct tracker writes, that is a product
  boundary change requiring a new ADR 0014 revision first.

## Owner sign-off required
Product-direction decision; confirm or amend before treating as Accepted.

---

## Hypothesis

Findings stay recommendations until routed into an implementation workflow;
task generation happens only inside an already-routed workflow's own steps,
never automatically from a bare finding; generated tasks are artifacts, not
tracker writes.

## Supporting evidence

- ADR 0014's product boundary (out-of-scope: third-party tracker writes)
  is itself evidence-adjacent via the golden path's demonstrated shape
  (diagnosis -> routing -> artifact, stopping short of external side
  effects) — PR #65's recommendation artifact is written to the session
  directory and validated, with no tracker write anywhere in the traced
  tool calls (`tool-call-trace.jsonl` shows only `SkillInvocation` and
  `Read`).
- The routing precondition (ADR 0018: only `architecture_fog` is routable)
  structurally limits when task generation could even begin, supporting
  the "low-value task floods" consequence.

## Missing evidence

- Nothing in the merged campaign touches `to-issues`, `triage`, or
  `issue_list.md` generation at all — this entire ADR is inference from the
  product boundary and the gate mechanism proven elsewhere, not a directly
  exercised path.
- No evidence exists for the approval-gate behavior specifically on a
  task-generation step (see the note added above).

## Experiment or review trigger

Revisit once a workflow that actually produces `issue_list.md` is run live
and gated end-to-end — that would be the first direct evidence for this
ADR's core claims.

## Status rationale

Remains **Proposed**. This is a product-strategy choice (how findings
convert to actionable tasks) with no direct supporting evidence from the
merged campaign — everything cited here is inference from adjacent, proven
mechanisms, not a proof of this ADR's own subject matter.
