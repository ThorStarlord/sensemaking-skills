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

The 2026-09-11 Persona & Adaptive Guidance Model v0 clarification is an
owner-ratified Level-4 `REINTERPRET`, not a product-category pivot. Its design
preflight is [`persona-adaptive-guidance-design-preflight.md`](persona-adaptive-guidance-design-preflight.md).

The 2026-09-11 Product Boundary Reconciliation v1 is an owner-ratified Level-4
`SUPERSEDE`: ADR 0029 is now the current product-boundary authority, while ADR
0014 remains historical evidence for the narrower July 2026 boundary.

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

For the primary user, another failure mode is **missing-question risk**: the user
may not know, remember, or want to enumerate every engineering consideration the
coding agent should resolve before acting. Sensemaking should therefore supply
opinionated engineering judgment about the process without inventing owner
intent or exceeding authority.

## 3. Primary user and anti-persona

### Primary user: high-delegation agent-assisted builder / repository owner

This person uses coding agents for significant engineering work, can define a
desired product or repository outcome, and wants to delegate substantial
repository-level engineering judgment without manually selecting every
intermediate question, responsibility, or implementation step.

The product is **beginner-first, expert-capable**:

- a beginner may value Sensemaking because they cannot reliably detect every
  missing engineering consideration or supervise every repository decision;
- an experienced engineer may value the same control layer because they can
  supervise those decisions but prefer to delegate them, especially for
  unfamiliar, consequential, or long-horizon repository work.

The common design pressure is therefore **high desired delegation**, not a
permanent lack of expertise. Expertise is contextual: the same person may be
expert in one technology, unfamiliar with another, authoritative about product
intent, and unfamiliar with the current repository.

The desired outcome is:

> I can give a capable coding agent a repository-level goal and bounded
> authority, and it can surface considerations I may not know or want to
> specify, establish what responsibility is warranted, execute bounded work,
> validate it, preserve durable state when needed, and stop when human judgment
> or reserved authority is required.

### Secondary users

- Experienced software engineers using coding agents for complex or
  long-running repository work.
- Technical decision owner or reviewer.
- Sensemaking Skill author or contributor.
- A possible future engineering-team lead.

These users matter, but the product remains designed around high-delegation
repository work rather than around a fixed expertise label.

### Anti-persona

Sensemaking is not for a small deterministic task whose correct solution path is
already obvious: changing a button label, fixing a typo, renaming a method, or
adding a known test. It should not add ceremony where no consequential
uncertainty exists.

Nor should it force a knowledgeable user to consume beginner-oriented
explanation when concise evidence and control surfaces are sufficient. More
scaffolding and more visible machinery are not the same thing.

## 4. Job to Be Done

> When I delegate a consequential repository goal whose correct next engineering
> responsibility is uncertain, help my coding agent surface relevant
> considerations, establish sufficient evidence, determine the warranted
> responsibility, exercise the judgment I delegated within granted authority,
> execute bounded work when authorized, preserve decision context when the work
> spans contexts, and stop or escalate when appropriate.

Triggering situations include an unfamiliar repository, ambiguous architecture
problem, large refactor, modernization effort, uncertain roadmap,
contradictory documentation, technical-debt prioritization, repeated local
fixes, or long-running multi-context development.

The user should not need to know in advance that a repository brief, Campaign,
reconciliation pass, or other Sensemaking surface is the appropriate mechanism.
The active coding agent remains responsible for judging which level of support
is warranted; automatic routing is not implied.

## 5. Value proposition

Sensemaking adds repository-specific decision structure around a capable coding
agent:

```text
opinionated engineering guidance
+ evidence discipline
+ explicit uncertainty
+ warranted responsibility
+ authority boundaries
+ durable state when needed
+ specialized capabilities
+ mechanical qualification
```

It does not replace agent intelligence. It aims to make repository-level agent
judgment more grounded, durable, bounded, reconstructible, and easier to
delegate.

Marginal value does not require a different final patch on every task. It may
also come from surfacing a consideration the user did not know to request,
reducing an avoidable wrong turn, preserving decision context, respecting an
authority boundary, or reaching justified closure with less user routing.
Comparative superiority over a capable direct agent remains unestablished.

### Evidence ceilings

| Claim | Current status |
| --- | --- |
| Repository diagnosis value | Supported, bounded by repository and experiment evidence |
| Artifact-mediated fresh-context continuation | Supported, with demonstrated ceilings |
| Comparative superiority over a capable direct agent | Mixed / not established |
| Adaptive multi-step campaign autonomy | Hypothesis; not a current construction prerequisite |
| General autonomous software development | Not established |

The current external product-validation priority is Goal A/A1. Its protocol,
admissibility rules, and independent evaluator semantics remain canonical for
the narrower brief/diagnosis claim they were designed to test. Superseding ADR
0014 as the current product boundary does not retroactively broaden that
protocol's evidentiary scope.

Current repository construction may continue under the ratified build-first
policy when architecture/integrity remains mechanically informative. New
product-value or comparative experiments are not prerequisites for the current
outer-loop foundation and require explicit owner direction when resumed.

## 6. Positioning and boundary

### Probably is

- Repository decision support.
- Repository sensemaking.
- Opinionated engineering guidance for high-delegation agent-assisted work.
- Artifact-mediated agent continuation.
- Bounded adaptive work around selected responsibilities.
- Optional durable Campaign support when continuation complexity warrants it.
- Bounded multi-repository target/relationship support without automatic orchestration.
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
- Autonomous merge, release, deployment, or publication authority.
- General-purpose cross-repository transaction coordination.
- A user-competence scoring or grading system.

The current external product boundary is ratified by
[`adr/0029-current-product-boundary.md`](adr/0029-current-product-boundary.md).
ADR 0014 remains historical evidence for the narrower July 2026 boundary and
for experiments/protocols that were explicitly conducted against that earlier
scope. The broader current boundary does not expand empirical claim ceilings or
turn every available product surface into mandatory ceremony.

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
15. **Opinionated about engineering invariants, adaptive about process,
    progressive in disclosure.** Stable principles should proactively protect
    evidence, responsibility, authority, and closure boundaries, while visible
    ceremony and durable machinery should scale only when the situation warrants
    them.
16. **Higher desired delegation increases the amount of judgment the user wants
    the agent to exercise; it does not increase the agent's granted authority.**
17. Beginner-first guidance should surface missing considerations without
    requiring the user to understand Sensemaking's internal machinery. Experts
    should be able to consume concise evidence/control surfaces without losing
    the same invariants.

## 8. Strategic non-goals

The following are not current build commitments: a custom coding-agent runtime,
central deterministic semantic router, HTN planner, generic autonomous-agent
platform, mandatory multi-agent swarm, automatic critic voting, semantic truth
oracle, `OuterLoopEngine`, automatic Strategic Frontier ranking, automatic
product-thesis revision, autonomous Campaign generation, autonomous merge or
release authority, cross-repository transaction/deployment coordinator,
user-expertise scoring, deterministic task-complexity or consequentiality
scoring, automatic persona inference, beginner/expert runtime modes, automatic
Campaign thresholds, or campaign/strategy infrastructure larger than
demonstrated need.

Reconsider a non-goal only when repository/product evidence shows that its
absence is decision-changing and a smaller intervention cannot address the
problem. Major reversal of a strategic non-goal is a Level-4 decision.

## 9. Hypotheses and bets

| Hypothesis | Current status |
| --- | --- |
| Repository sensemaking improves ambiguous repository decisions | Supported, bounded |
| Durable artifacts support fresh-context continuation | Supported |
| Responsibility-first thinking is better than workflow-first thinking | Emerging hypothesis |
| Opinionated guidance can add value by surfacing considerations a high-delegation user did not know or want to specify | Product hypothesis; not comparatively established |
| Adaptive process rigor can reduce unnecessary ceremony while preserving stable engineering invariants | Product hypothesis; no formal routing/tiers authorized |
| Durable Level-3 strategic state can reduce development-direction reconstruction ambiguity | Supported in bounded self-development campaigns; broader value not established |
| Adaptive campaign execution reduces owner routing | Not yet demonstrated |
| Campaign State materially improves continuation | Hypothesis |
| Claim Evidence Register generalizes beyond Clause B | Hypothesis |
| Sensemaking consistently beats a capable direct-agent baseline | Not established |
| A custom execution runtime is required | No evidence |
| A deterministic strategic planner is required | No evidence |

## 10. Success measures

Measure decision quality and delegation quality rather than inventory:

- grounded central diagnosis;
- appropriate next responsibility;
- useful surfacing of decision-relevant considerations the user did not need to
  enumerate explicitly;
- honest uncertainty handling;
- correct evidence-dependent transitions before owner intervention;
- reduced manual routing of ordinary next steps where evidence eventually
  supports that claim;
- proportional use of scaffolding, process rigor, and durable machinery rather
  than mandatory ceremony;
- correct escalation, deferment, no-change, and thesis-review decisions;
- correct reconstruction by a fresh agent;
- correct distinction between Level-4 thesis state, Level-3 strategic state,
  Level-2 Campaign state, and Level-1 execution state;
- decision-bearing claims supported by appropriate evidence;
- correct separation of desired delegation from granted authority;
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

The Persona & Adaptive Guidance Model v0 sharpens that question rather than
answering it empirically. The primary user is now explicitly interpreted as a
high-delegation agent-assisted builder, while the amount of scaffolding, process
rigor, and durable Campaign machinery is expected to vary with contextual
supervision capability and the problem's decision, consequentiality, and
continuation characteristics. These are agent-reasoned factors, not a routing
schema.

That unresolved product question is **not** a prerequisite for
repository-grounded construction. The Strategic Outer Loop foundation remains
integrated and frozen as a control baseline. Any subsequent runtime package must
still be selected afresh by Level 3 from concrete pressure, an explicit owner
direction, or a mechanically decidable reconstruction/integrity need.

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

The Persona & Adaptive Guidance Model v0 change uses `REINTERPRET`: the existing
primary-user commitment remains materially the same, while its high-delegation,
beginner-first/expert-capable meaning is made explicit.

Product Boundary Reconciliation v1 uses `SUPERSEDE`: ADR 0014 remains historical
and ADR 0029 becomes the current boundary authority. Product purpose, agent-owned
semantic judgment, major strategic non-goals, Campaign schema, and empirical
claim ceilings are not expanded by the act of supersession itself.

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

- Current product-boundary authority: [ADR 0029](adr/0029-current-product-boundary.md)
- Product-boundary reconciliation record: [product-boundary-reconciliation-v1.md](product-boundary-reconciliation-v1.md)
- Historical July 2026 product boundary: [ADR 0014](adr/0014-product-boundary.md)
- Persona/adaptive-guidance reinterpretation preflight: [persona-adaptive-guidance-design-preflight.md](persona-adaptive-guidance-design-preflight.md)
- Four-level control model: [strategic-outer-loop.md](strategic-outer-loop.md)
- Level-3 state contract: [strategic-state-contract.md](strategic-state-contract.md)
- Level-4 revision contract: [product-thesis-revision.md](product-thesis-revision.md)
- Non-authoritative future possibilities: [strategic-candidate-directions.md](strategic-candidate-directions.md) — idea memory only; not Strategic Frontier membership or implementation authorization
- Current operating model: [product-operating-model.md](product-operating-model.md)
- Current Level-3 status and development direction: [STATUS.md](../STATUS.md)
- Architecture authority: [ADR index](adr/README.md), especially ADRs 0013 and 0029
- Operating workflow: [agent-native-operating-workflow.md](agent-native-operating-workflow.md)
- Research hypotheses: [control-model research agenda](research/control-model-research-agenda.md)
- Goal A protocol: [external product-validation protocol](research/goal-a-external-product-validation-protocol.md)
