# ADR 0014: Product Boundary of Sensemaking Skills

**Status**: PROPOSED — draft for owner review, not yet accepted
**Date**: 2026-07-25
**Resolves**: Issue #29

---

## Context

Five possible scope definitions were on the table:
1. A repository analyzer that generates improvement suggestions
2. A planning system that converts repository understanding into implementation tasks
3. A general skill orchestration runtime
4. A decision-navigation system choosing between research, prototyping, review, planning, and execution
5. A complete agent-native software-development workflow

Issue #29 itself already stated a preferred definition. This ADR promotes that
preference to a decision, since #33, #34, #35, and #36 are all blocked on the
product boundary being settled and it is the single highest-leverage
unresolved question in the backlog.

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
*this product's own* skill chain, not arbitrary third-party workflows, and
the proven golden path (#28/#38/#39) stops at a validated recommendation
artifact plus (optionally) an implementation workflow invocation — it does
not own deployment, PR review, or production operations.

### In scope
- Fog classification and repository diagnosis (`repo-sensemaker`)
- Routing to the correct downstream workflow (`workflow-planner`)
- Producing validated, machine-readable handoff artifacts
- The proven golden path: intent → brief → architectural-review →
  recommendation → run log → exit 0 (#28)

### Out of scope (left to downstream consumers)
- Actually writing/reviewing/merging code
- Third-party issue-tracker sync (Jira, Linear, GitHub Issues API writes)
- Deployment, CI orchestration, or production monitoring
- General-purpose multi-repo orchestration

## Consequences

- #33 (workflow-routing policy) can now proceed: routing decisions are
  scoped to the workflows this product owns, not arbitrary external tools.
- #34 (findings → tracker tasks) is **in scope only as artifact production**
  (e.g. `issue_list.md`), not as automatic third-party tracker writes —
  that crosses into "downstream consumer" territory per this boundary.
- #35 (Wayfinder/prototypes) needs its own scope call informed by this
  boundary — see ADR 0020.

## Owner sign-off required

This is a product-direction decision. Before treating this as Accepted,
the repo owner should confirm or amend the boundary above.
