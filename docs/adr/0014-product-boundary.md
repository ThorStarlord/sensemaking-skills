# ADR 0014: Product Boundary of Sensemaking Skills

**Status**: PROPOSED — draft for owner review, not yet accepted
**Date**: 2026-07-25
**Proposes resolution for**: Issue #29

---

## Context

Five possible scope definitions were on the table:
1. A repository analyzer that generates improvement suggestions
2. A planning system that converts repository understanding into implementation tasks
3. A general skill orchestration runtime
4. A decision-navigation system choosing between research, prototyping, review, planning, and execution
5. A complete agent-native software-development workflow

Issue #29 itself already stated a preferred definition. This ADR formalizes
that preference as the proposed product boundary for owner review, since
#33, #34, #35, and #36 are all blocked on the product boundary being settled
and it is the single highest-leverage unresolved question in the backlog.

## Decision

Sensemaking Skills is **a pre-implementation intelligence and
workflow-orchestration system** that helps agents:
1. understand a repository,
2. identify the weakest boundary,
3. choose the correct type of work, and
4. produce validated artifacts for downstream execution.

This matches option 4 (decision-navigation) bounded by option 2 (produces
tasks/artifacts, doesn't have to execute them). It explicitly does **not**
claim to be a general orchestration runtime (option 3) or a complete
end-to-end dev workflow (option 5) — `workflow-runtime.py` orchestrates
*this product's own* skill chain, not arbitrary third-party workflows.

**Evidence note (corrects the original draft):** the original text here cited
"#28/#38/#39" as the proof for the golden path. Issue #39's claim was a
free-text issue comment with no committed, reviewable evidence and was
superseded by issue #51, which required durable evidence and was closed only
once PR #57 (issue #55), PR #59 (issue #58), PR #62 (issue #61), PR #64
(issue #63), and PR #65 (issue #51 itself) landed on `main`. The golden path
that is actually proven today is: intent -> `repo-sensemaker` (live, PR #59)
-> `repository_sensemaking_brief.md` (APPROVED) -> `architectural-review`
Step 2, both the positive path (recommendation produced and validated) and
the negative path (missing `proposed_direction.md` correctly fails closed)
(PR #65) -> run log / exit code. This is proven for exactly one workflow,
`architectural-review-planning-workflow`; it stops at a validated
recommendation artifact — it does not own deployment, PR review, or
production operations, and it has not been run against an external
repository (see ADR 0017).

### In scope
- Fog classification and repository diagnosis (`repo-sensemaker`)
- Routing to the correct downstream workflow (`workflow-planner`)
- Producing validated, machine-readable handoff artifacts
- The proven golden path (narrowly, for `architectural-review-planning-workflow`
  only): intent -> brief -> architectural-review -> recommendation -> run log
  -> exit 0, with both the positive and missing-input negative path proven
  live (PR #57, #59, #60, #62, #64, #65; issue #28 historical scope decision,
  issue #51 evidence remediation)

### Out of scope (left to downstream consumers)
- Actually writing/reviewing/merging code
- Third-party issue-tracker sync (Jira, Linear, GitHub Issues API writes)
- Deployment, CI orchestration, or production monitoring
- General-purpose multi-repo orchestration

## Consequences

- #33 (workflow-routing policy) can be drafted against a stable scope once
  this boundary is proposed: routing decisions are scoped to the workflows
  this product owns, not arbitrary external tools (see ADR 0018, itself
  Proposed pending this ADR's acceptance).
- #34 (findings → tracker tasks), if this boundary is accepted, would be
  **in scope only as artifact production** (e.g. `issue_list.md`), not as
  automatic third-party tracker writes — that crosses into "downstream
  consumer" territory per this boundary.
- #35 (Wayfinder/prototypes) needs its own scope call informed by this
  boundary — see ADR 0020.

## Owner sign-off required

This is a product-direction decision. Before treating this as Accepted,
the repo owner should confirm or amend the boundary above.

---

## Hypothesis

Sensemaking Skills' scope is bounded to diagnosis -> routing -> validated
artifact production (option 4 bounded by option 2), and explicitly excludes
acting as a general orchestration runtime or a complete dev workflow.

## Supporting evidence

- The proven golden path (PR #57, #59, #60, #62, #64, #65; issues #55, #58,
  #56, #61, #63, #51) demonstrates the "diagnosis -> routing -> validated
  artifact" shape end-to-end for one workflow, consistent with this
  boundary's description of what the product does.
- `workflow-runtime.py` orchestrates only this product's own skill chain
  (confirmed by the runtime code path exercised in PR #65's evidence) — no
  evidence anywhere in the merged campaign shows it orchestrating arbitrary
  third-party workflows.

## Missing evidence

- No merged evidence tests the *boundary* itself (i.e., what happens when
  someone tries to use the runtime for a third-party workflow, or asks the
  product to write code/deploy/sync a tracker). The boundary is a scope
  *decision*, not something the campaign observed being violated or upheld.
- This is a single-workflow proof, not proof that the boundary holds across
  the other three implementation workflows or any downstream-consumer
  interaction.

## Experiment or review trigger

Revisit if: (a) a second implementation workflow is proven and needs its own
scope check against this boundary, or (b) the owner decides to bring
tracker-sync or deployment in-scope (which would require a new ADR revision
here, not a reinterpretation of this one).

## Status rationale

Remains **Proposed**. This is a product-direction decision (which of five
scope options the product commits to), not something evidence can settle by
itself — the golden path shows the product *can* work within option 4/2, but
does not prove the owner has committed to excluding options 3 and 5 going
forward. Owner sign-off is still required.
