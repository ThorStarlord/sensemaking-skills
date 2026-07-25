# ADR 0019: When Findings Become Recommendations versus Tracker Tasks

**Status**: PROPOSED — draft for owner review, not yet accepted
**Date**: 2026-07-25
**Resolves**: Issue #34 (was blocked by #29, #33 — both drafted in ADR 0014, ADR 0018)

---

## Context

Per ADR 0014's product boundary, third-party issue-tracker writes are
explicitly **out of scope** for this product — the handoff artifact is the
integration point, actual sync is a downstream consumer's job. This
resolves most of #34's open questions by removing the "automatic tracker
write" option from consideration.

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
  `issue_list.md` already has a `gate: review` per the golden path (#28) —
  this is the existing human-approval point; no new approval mechanism is
  needed.
- **Low-value task floods**: prevented structurally — tasks only get
  generated for a fog type with a proven route (ADR 0018), not for every
  observation in a brief.

## Consequences
- No new tracker-integration code is in scope from this decision.
- If a future need arises for direct tracker writes, that is a product
  boundary change requiring a new ADR 0014 revision first.

## Owner sign-off required
Product-direction decision; confirm or amend before treating as Accepted.
