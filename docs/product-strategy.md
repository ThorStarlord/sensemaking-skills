# Sensemaking Skills Product Strategy

**Status:** current product hypothesis and strategic authority  
**Updated:** 2026-09-06  
**Scope:** public repository strategy; empirical claims retain the ceilings of their source evidence

This document answers what Sensemaking Skills is trying to make valuable. It
does not replace ADRs, artifact contracts, validators, or dated research.

## 1. Product purpose

Sensemaking Skills exists to improve repository-level decisions when a capable
coding agent cannot safely determine the correct next engineering
responsibility from the user's request alone.

This is the current product hypothesis, not eternal truth. It should change when
normal use shows that the problem, user, or intervention is wrong.

## 2. Problem

Coding agents are increasingly good at executing known implementation tasks.
They are less reliably grounded when repository work involves ambiguous goals,
competing consequential boundaries, incomplete owner intent, contradictory
documentation, long-running work across fresh contexts, or authority limits.

The failure mode is often not poor implementation. It is choosing or continuing
the wrong responsibility: implementing prematurely, solving a local symptom,
following stale architecture, inventing work, making claims beyond evidence,
or continuing when the right outcome is to stop or ask the owner.

## 3. Primary user and anti-persona

### Primary user: AI-native repository owner / maintainer

This person uses coding agents for significant engineering work and wants to
delegate repository-level goals without manually selecting every intermediate
step. They worry about premature implementation, stale context, ignored
uncertainty, authority crossings, and unsupported completion claims.

The desired outcome is:

> I can give a capable coding agent a repository-level goal and bounded
> authority, and it can establish what responsibility is warranted, execute
> bounded work, validate it, preserve durable state, and stop when human
> judgment is required.

### Secondary users

- Technical decision owner or reviewer.
- Sensemaking Skill author or contributor.
- A possible future engineering-team lead.

These users matter, but the product is not optimized around them yet.

### Anti-persona

Sensemaking is not for a small deterministic task whose correct solution path is
already obvious: changing a button label, fixing a typo, renaming a method, or
adding a known test. It should not add ceremony where no consequential
uncertainty exists.

## 4. Job to Be Done

> When I face a consequential repository problem whose correct next engineering
> responsibility is uncertain, help my coding agent establish relevant
> evidence, determine the warranted responsibility, execute bounded work when
> authorized, and stop or escalate when appropriate.

Triggering situations include an unfamiliar repository, ambiguous architecture
problem, large refactor, modernization effort, uncertain roadmap,
contradictory documentation, technical-debt prioritization, repeated local
fixes, or long-running multi-context development.

## 5. Value proposition

Sensemaking adds durable repository-specific decision structure around a capable
coding agent:

```text
evidence discipline
+ explicit uncertainty
+ warranted responsibility
+ authority boundaries
+ durable state
+ specialized capabilities
+ mechanical qualification
```

It does not replace agent intelligence. It aims to make repository-level agent
judgment more grounded, durable, bounded, and reconstructible.

### Evidence ceilings

| Claim | Current status |
| --- | --- |
| Repository diagnosis value | Supported, bounded by repository and experiment evidence |
| Artifact-mediated fresh-context continuation | Supported, with demonstrated ceilings |
| Comparative superiority over a capable direct agent | Mixed / not established |
| Adaptive multi-step campaign autonomy | Hypothesis; next major test |
| General autonomous software development | Not established |

The current external product-validation priority is Goal A/A1. Its protocol,
admissibility rules, and independent evaluator semantics are canonical. The
2026-08-31 reassessment records that the next compliant run remains paused at a
harness artifact-finalization/provenance boundary; this is not a product
verdict and does not authorize a run.

## 6. Positioning and boundary

### Probably is

- Repository decision support.
- Repository sensemaking.
- Artifact-mediated agent continuation.
- Bounded adaptive work around selected responsibilities.

### Is not currently

- A coding model or general coding agent.
- A custom agent runtime.
- A workflow-orchestration engine that owns the product control loop.
- A deterministic semantic planner or central semantic router.
- An autonomous software factory.
- A replacement for GitHub or CI.
- Automatic architecture authority.
- Autonomous merge or release authority.

The broader agent-native control architecture in `CONTEXT.md` is an internal
architectural model. The ratified external product scope remains the validated,
human-reviewed `repository_sensemaking_brief` defined by ADR 0014. Do not
silently promote architecture or research into external product scope.

## 7. Strategic principles

1. Evidence precedes a consequential transition.
2. Resolve the nearest decision-changing uncertainty.
3. A responsibility exists because its result changes a decision.
4. Recommendation, selection, and authorization are different states.
5. Capability availability does not imply capability appropriateness.
6. Agents own semantic judgment; deterministic mechanisms own mechanical facts
   and invariants.
7. Solved questions stop generating work.
8. Deferred work does not become a TODO merely because it exists.
9. Correct stopping is successful behavior.
10. External boundaries are recorded rather than fabricated around.
11. Productize demonstrated needs, not speculative machinery.
12. Preserve evidence ceilings and do not manufacture work to keep a campaign
    active.

## 8. Strategic non-goals

The following are not current build commitments: a custom coding-agent runtime,
central deterministic semantic router, HTN planner, generic autonomous-agent
platform, mandatory multi-agent swarm, automatic critic voting, semantic truth
oracle, autonomous merge/release authority, or campaign infrastructure larger
than demonstrated need.

Reconsider a non-goal only when real campaigns show that its absence is
decision-changing and a smaller intervention cannot address the problem.

## 9. Hypotheses and bets

| Hypothesis | Current status |
| --- | --- |
| Repository sensemaking improves ambiguous repository decisions | Supported, bounded |
| Durable artifacts support fresh-context continuation | Supported |
| Responsibility-first thinking is better than workflow-first thinking | Emerging hypothesis |
| Adaptive campaign execution reduces owner routing | Not yet demonstrated |
| Campaign State materially improves continuation | Hypothesis |
| Claim Evidence Register generalizes beyond Clause B | Hypothesis |
| Sensemaking consistently beats a capable direct-agent baseline | Not established |
| A custom execution runtime is required | No evidence |

## 10. Success measures

Measure decision quality rather than inventory:

- grounded central diagnosis;
- appropriate next responsibility;
- honest uncertainty handling;
- correct evidence-dependent transitions before owner intervention;
- reduced manual routing of ordinary next steps;
- correct escalation, deferment, and no-change decisions;
- correct reconstruction by a fresh agent;
- decision-bearing claims supported by appropriate evidence;
- owner preference for the Sensemaking-assisted result over asking a strong
  coding agent directly.

The last measure is a product question, not an assumption. A2 is not currently
authorized to answer it comparatively.

## 11. Strategic frontier

The next warranted product question is:

> Does agent-controlled adaptive campaign execution materially improve the
> primary user's ability to delegate ambiguous repository work without manual
> task-by-task routing?

The smallest candidate concepts are Warranted Responsibility,
Decision-Changing Uncertainty, explicit Authority, correct Stopping, and
possibly Campaign State, Transition Record, and Campaign Handoff. These are
not automatically authorized features. Each must answer:

1. Which user/problem does it serve?
2. What consequential decision improves?
3. What observed behavior warrants building it?
4. What is the smallest test before architecture commitment?

## 12. Public/private boundary

Public strategy may include the product problem, persona, JTBD, positioning,
principles, non-goals, public hypotheses, and sanitized experimental
conclusions. Keep private target identities, private repository findings,
security details, raw unpublished experiments, and sensitive commercial
reasoning local. Public claims must not imply evidence beyond the underlying
record.

## 13. Authority and related documents

- Current operating model: [product-operating-model.md](product-operating-model.md)
- Current status and validation state: [STATUS.md](../STATUS.md)
- Architecture authority: [ADR index](adr/README.md), especially ADRs 0013 and 0014
- Operating workflow: [agent-native-operating-workflow.md](agent-native-operating-workflow.md)
- Research hypotheses: [control-model research agenda](research/control-model-research-agenda.md)
- Goal A protocol: [external product-validation protocol](research/goal-a-external-product-validation-protocol.md)

