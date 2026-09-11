# Sensemaking Skills Product Strategy

**Status:** current product hypothesis and strategic authority  
**Updated:** 2026-09-11  
**Control level:** Level 4 — Product Thesis / Strategy Revision  
**Scope:** public repository strategy; empirical claims retain the ceilings of their source evidence

This document answers what Sensemaking Skills is trying to make valuable. It is
the current Level-4 product-thesis authority surface. It does not replace ADRs,
artifact contracts, validators, dated research, or the Level-3 operational state
in `STATUS.md`.

Major strategy changes follow
[`product-thesis-revision.md`](product-thesis-revision.md). Repository-level
execution of this strategy is governed by the Strategic Repository Evolution
Loop in [`strategic-outer-loop.md`](strategic-outer-loop.md).

## 1. Product purpose

Sensemaking Skills exists to improve repository-level decisions when a capable
coding agent cannot safely determine the correct next engineering
responsibility from the user's request alone.

This is the current product hypothesis, not eternal truth. It should change when
material evidence or explicit owner direction shows that the problem, user, or
intervention is wrong.

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
| Adaptive multi-step campaign autonomy | Hypothesis; not a current construction prerequisite |
| General autonomous software development | Not established |

The current external product-validation priority is Goal A/A1. Its protocol,
admissibility rules, and independent evaluator semantics remain canonical. The
2026-08-31 reassessment records that the next compliant run remains paused at a
harness artifact-finalization/provenance boundary; this is not a product verdict
and does not authorize a run.

Current repository construction may continue under the ratified build-first
policy when architecture/integrity remains mechanically informative. New
product-value or comparative experiments are not prerequisites for the current
outer-loop foundation and require explicit owner direction when resumed.

## 6. Positioning and boundary

### Probably is

- Repository decision support.
- Repository sensemaking.
- Artifact-mediated agent continuation.
- Bounded adaptive work around selected responsibilities.
- Durable strategic-state reconstruction for repository evolution, while the
  active agent retains semantic control.

### Is not currently

- A coding model or general coding agent.
- A custom agent runtime.
- A workflow-orchestration engine that owns the product control loop.
- A deterministic semantic planner or central semantic router.
- An autonomous software factory.
- A replacement for GitHub or CI.
- Automatic architecture authority.
- Automatic product-strategy revision authority.
- Autonomous merge or release authority.

The broader agent-native control architecture in `CONTEXT.md` is an internal
architectural model. The ratified external product scope remains the validated,
human-reviewed `repository_sensemaking_brief` defined by ADR 0014. The
four-level control model does **not** silently expand that external product
boundary.

## 7. Strategic principles

1. Evidence precedes a consequential transition.
2. Resolve the nearest decision-changing uncertainty appropriate to the current
   control level.
3. A responsibility exists because its result changes a decision.
4. Recommendation, selection, authorization, and ratification are different
   states.
5. Capability availability does not imply capability appropriateness.
6. Agents own semantic judgment; deterministic mechanisms own mechanical facts
   and invariants.
7. Solved questions stop generating work.
8. Deferred work does not become a TODO merely because it exists.
9. Correct stopping is successful behavior.
10. External boundaries are recorded rather than fabricated around.
11. Productize demonstrated needs, not speculative machinery.
12. Preserve evidence ceilings and do not manufacture work to keep a campaign
    or strategic loop active.
13. Lower control levels may execute higher-level commitments but may not
    silently redefine them.
14. Product-thesis revision is slower and more authority-sensitive than ordinary
    repository evolution.

## 8. Strategic non-goals

The following are not current build commitments: a custom coding-agent runtime,
central deterministic semantic router, HTN planner, generic autonomous-agent
platform, mandatory multi-agent swarm, automatic critic voting, semantic truth
oracle, `OuterLoopEngine`, automatic Strategic Frontier ranking, automatic
product-thesis revision, autonomous Campaign generation, autonomous merge or
release authority, or campaign/strategy infrastructure larger than demonstrated
need.

Reconsider a non-goal only when repository/product evidence shows that its
absence is decision-changing and a smaller intervention cannot address the
problem. Major reversal of a strategic non-goal is a Level-4 decision.

## 9. Hypotheses and bets

| Hypothesis | Current status |
| --- | --- |
| Repository sensemaking improves ambiguous repository decisions | Supported, bounded |
| Durable artifacts support fresh-context continuation | Supported |
| Responsibility-first thinking is better than workflow-first thinking | Emerging hypothesis |
| Durable Level-3 strategic state can reduce development-direction reconstruction ambiguity | Supported in bounded self-development campaigns; broader value not established |
| Adaptive campaign execution reduces owner routing | Not yet demonstrated |
| Campaign State materially improves continuation | Hypothesis |
| Claim Evidence Register generalizes beyond Clause B | Hypothesis |
| Sensemaking consistently beats a capable direct-agent baseline | Not established |
| A custom execution runtime is required | No evidence |
| A deterministic strategic planner is required | No evidence |

## 10. Success measures

Measure decision quality rather than inventory:

- grounded central diagnosis;
- appropriate next responsibility;
- honest uncertainty handling;
- correct evidence-dependent transitions before owner intervention;
- reduced manual routing of ordinary next steps where evidence eventually
  supports that claim;
- correct escalation, deferment, no-change, and thesis-review decisions;
- correct reconstruction by a fresh agent;
- correct distinction between Level-4 thesis state, Level-3 strategic state,
  Level-2 Campaign state, and Level-1 execution state;
- decision-bearing claims supported by appropriate evidence;
- owner preference for the Sensemaking-assisted result over asking a strong
  coding agent directly, when/if comparative validation is explicitly resumed.

Comparative preference remains a product question, not an assumption.

## 11. Product-level strategic frontier

This section records product-thesis questions and strategic bets. The current
repository-development frontier belongs to Level 3 and is projected in
`STATUS.md`.

The major unresolved product question remains:

> Does agent-controlled adaptive repository/campaign execution materially
> improve the primary user's ability to delegate ambiguous repository work
> without manual task-by-task routing?

That question is **not** a prerequisite for repository-grounded construction.
The documentation-first Strategic Outer Loop foundation is now integrated; it
makes Level-4 product-thesis authority and Level-3 repository-evolution state
explicit without adding automatic planning authority. Any subsequent outer-loop
runtime package must be selected afresh by Level 3 from a concrete
mechanically-decidable reconstruction or integrity need.

Any candidate product commitment should still answer:

1. Which user/problem does it serve?
2. What consequential decision improves?
3. What evidence or existing contract warrants considering it?
4. What is the smallest warranted intervention before architecture commitment?
5. Does deciding it require Level-4 owner ratification, or can Level 3 proceed
   within existing strategy?

## 12. Level-4 revision semantics

This document is the Level-4 authority surface, but editing it is not equivalent
to ordinary documentation cleanup.

Consequential product-thesis review should end in one explicit disposition:

```text
REAFFIRM
REINTERPRET
REVISE
RETIRE
SUPERSEDE
```

The detailed contract is
[`product-thesis-revision.md`](product-thesis-revision.md).

The active agent may identify thesis-level tension, gather evidence, formulate
alternatives, and draft a recommendation. Major changes to product mission,
primary user, external product boundary, strategic non-goals, or public claim
ceilings remain owner-reserved unless authority is explicitly delegated.

After a ratified Level-4 change, Level 3 must reassess the Strategic Frontier
rather than blindly continue the previous repository responsibility.

## 13. Public/private boundary

Public strategy may include the product problem, persona, JTBD, positioning,
principles, non-goals, public hypotheses, and sanitized experimental or
repository conclusions. Keep private target identities, private repository
findings, security details, raw unpublished experiments, and sensitive
commercial reasoning local. Public claims must not imply evidence beyond the
underlying record.

## 14. Authority and related documents

- Four-level control model: [strategic-outer-loop.md](strategic-outer-loop.md)
- Level-3 state contract: [strategic-state-contract.md](strategic-state-contract.md)
- Level-4 revision contract: [product-thesis-revision.md](product-thesis-revision.md)
- Non-authoritative future possibilities: [strategic-candidate-directions.md](strategic-candidate-directions.md) — idea memory only; not Strategic Frontier membership or implementation authorization
- Current operating model: [product-operating-model.md](product-operating-model.md)
- Current Level-3 status and development direction: [STATUS.md](../STATUS.md)
- Architecture authority: [ADR index](adr/README.md), especially ADRs 0013 and 0014
- Operating workflow: [agent-native-operating-workflow.md](agent-native-operating-workflow.md)
- Research hypotheses: [control-model research agenda](research/control-model-research-agenda.md)
- Goal A protocol: [external product-validation protocol](research/goal-a-external-product-validation-protocol.md)
