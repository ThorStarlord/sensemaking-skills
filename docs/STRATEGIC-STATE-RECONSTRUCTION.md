# Strategic State Reconstruction

**Date:** 2026-09-06  
**Status:** research material supporting the strategic foundation; not a product contract

This record reconstructs the strategy already present in the repository before
adding a canonical product strategy. It preserves contradictions instead of
silently resolving them by deleting history.

## Current

- The current architectural definition is an agent-native engineering
  sensemaking and control layer for software-engineering agents. The active
  coding agent owns the recursive control loop; Skills, artifacts, validators,
  reconciliation, repair verification, and authority boundaries constrain it.
  Evidence: [CONTEXT.md](../CONTEXT.md), [ADR 0013](adr/0013-agent-native-orchestration-primary.md).
- The ratified external product boundary is narrower: a human-reviewed,
  evidence-grounded `repository_sensemaking_brief`. Automatic routing,
  tracker synchronization, and deployment are deferred. Evidence: [ADR 0014](adr/0014-product-boundary.md).
- The current product-validation priority is Goal A/A1. It is active in the
  strategy, but the next compliant run is paused by a harness artifact-
  finalization and provenance blocker. Evidence: [STATUS.md](../STATUS.md) and
  [the 2026-08-31 reassessment](research/goal-a-execution-readiness-reassessment-2026-08-31.md).
- The operating rule is to resolve the nearest unresolved decision-changing
  uncertainty before committing to the eventual solution. Evidence:
  [CONTEXT.md](../CONTEXT.md) and [agent-native-operating-workflow.md](agent-native-operating-workflow.md).

## Historical

- `goal.md` describes an older two-skill core in which diagnosis classifies fog,
  routes to a workflow, and a planner sequences skills. It is retained as a
  historical north-star record, not current product authority.
- `roadmap.md` describes an earlier Phase 2/3/4/5 shipment and PyPI/GA plan.
  It is retained as historical planning evidence, not a current roadmap.
- Earlier phase and deployment reports under `docs/archive/phase-reports/` are
  historical by location and should not be used to infer current readiness.

## Contradictory

- The repository contains both broad control-layer language and the narrower
  ratified external brief boundary. These are compatible only when treated as
  separate layers: architecture and future-facing internal capability versus
  current externally validated product scope.
- Older documents present automatic workflow routing and autonomous sequencing
  as product behavior. ADR 0013 and ADR 0014 supersede that interpretation:
  the active agent selects responsibility, and the current external product
  does not claim automatic downstream routing.
- Historical release documents claim readiness or GA in places, while current
  status says Goal A external validation is still active and not ready for a
  compliant Run 1. The current status and dated Goal A protocol control.

## Implicit

- The primary user is an owner or maintainer delegating consequential repository
  work to a capable coding agent; this is implied by the agent-native loop,
  authority model, and handoff artifacts but was not previously stated in one
  strategy document.
- The product's differentiator is decision structure around a capable agent:
  evidence discipline, explicit uncertainty, warranted responsibility,
  authority boundaries, durable state, and mechanical qualification.
- Correct stopping, escalation, deferment, and no-change outcomes are valid
  product behavior, not failures to complete a workflow.
- The public repository can describe sanitized product claims and abstract
  conclusions, but private identities, security details, raw unpublished
  experiments, and sensitive commercial reasoning stay local.

## Unresolved

- Whether adaptive campaign execution materially reduces owner task-by-task
  routing remains a product hypothesis, not a committed feature roadmap.
- Whether Campaign State, Transition Record, and Campaign Handoff earn
  productization requires dogfood evidence; their existence in research or
  campaign records is not authorization to build them.
- Whether Sensemaking consistently outperforms a strong direct-agent baseline
  is not established; A2 is deferred/unauthorized.
- The Goal A substrate must be repaired and separately authorized before a
  compliant external episode can run.
- Whether the broader control concepts transfer beyond software engineering is
  a research question, not current product scope.

## Source-of-truth decision

The missing piece was not more historical evidence. It was a single current
document that separates product purpose and boundary from architecture,
research, and old shipment plans. The canonical map is now:

| Question | Authority |
| --- | --- |
| Product purpose, user, boundary, bets, and non-goals | [product-strategy.md](product-strategy.md) |
| Current value stream and responsibility ownership | [product-operating-model.md](product-operating-model.md) |
| Current validation state | [STATUS.md](../STATUS.md) and the current Goal A protocol |
| Architecture decisions | [docs/adr/](adr/) |
| Canonical vocabulary and artifact contracts | Existing registries/contracts named in [CONTEXT.md](../CONTEXT.md) |
| Empirical claims | Dated research and experiment evidence |
| Historical plans and completion reports | Explicitly marked historical records |

This reconstruction satisfies the precondition for creating the product
strategy: the existing strategic state is known, and the genuine gap is
consolidation plus authority alignment.

