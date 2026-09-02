# Campaign charter (owner instruction, verbatim)

```
SOURCE:    owner instruction delivered to the active coding agent in
           conversation on 2026-09-02, launching this campaign.
AUTHORITY: this is the campaign's authority source. It is the owner's
           instruction, not an ADR, contract, or ratified product decision.
           Repository policy (ADRs, CONTEXT.md, AGENTS.md) still governs
           what may be merged, ratified, or published.
STATUS:    committed verbatim (formatting normalized to Markdown) so that a
           fresh context can reconstruct the mission, vocabulary, acceptance
           conditions, stopping rules, and report format from durable state.
           R1 (docs/campaigns/agent-native-self-development/
           R1-fresh-context-reconstruction.md) classified its absence as
           MISSING_DURABLE_STATE.
```

---

You are the lead coding agent responsible for completing a bounded
product-development campaign in the `sensemaking-skills` repository.

## Campaign Mission

Advance Sensemaking Skills toward:

**Reliable agent-native, artifact-mediated self-development.**

The intended future product should allow an active coding agent to use
repository evidence and durable artifacts to determine the next warranted
engineering responsibility, select an appropriate capability, perform bounded
work, validate the resulting evidence, preserve authority boundaries, carry
state across responsibilities, and recursively continue until the active goal
is satisfied or further action is unwarranted.

This is a campaign-level mission, not a request for a monolithic rewrite.

You own the campaign from initial diagnosis through implementation,
qualification, and final closure.

Continue autonomously through multiple bounded tasks until the campaign-level
acceptance conditions are satisfied, an explicit owner decision is genuinely
required, or an external blocker makes further progress impossible.

Do not stop merely because one task, issue, commit, or pull request is
complete.

## Important Bootstrap Constraint

You are building Sensemaking Skills, but you are not using Sensemaking Skills'
own Skills or workflow/orchestration system to control this campaign.

Do not invoke or depend upon:

* `repo-sensemaker`;
* `using-sensemaking`;
* registered Sensemaking Skills workflows as the campaign controller;
* workflow-runtime routing;
* fog-to-workflow routing;
* Skill-to-Skill continuation mechanisms that are themselves under evaluation;
* the proposed hook system as a prerequisite for doing this work.

This campaign is controlled directly by you, the coding agent.

You MAY and SHOULD use normal repository engineering infrastructure where
appropriate, including:

* repository documentation;
* ADRs;
* issue and PR history;
* tests;
* pytest;
* linters;
* type checking;
* validators;
* `validate-repo.py`;
* artifact validation scripts;
* build/package checks;
* Git;
* GitHub CI;
* ordinary repository inspection and coding tools.

Do not confuse "do not use Sensemaking Skills as your orchestrator" with "do
not use the repository's normal engineering tools."

## Campaign Control Model

Own the following recursive loop:

```text
PRODUCT MISSION
      |
CURRENT REPOSITORY / PRODUCT STATE
      |
identify highest-leverage unresolved capability boundary
      |
identify decision-changing uncertainty
      |
select ONE warranted bounded responsibility
      |
perform bounded analysis / design / implementation / verification
      |
produce durable repository evidence
      |
validate
      |
update campaign state
      |
reassess the PRODUCT MISSION
      |
continue / owner decision / blocker / campaign complete
```

Never attempt the whole mission as one implementation task.

The mission may be high-scope and high-complexity.

Each responsibility should be kept as bounded as practical.

## Strategic Selection Rule

Before beginning each new repository-level task, ask:

What unresolved capability currently constrains progress toward the campaign
mission most?

Do NOT simply choose:

* the nearest visible bug;
* the easiest open issue;
* the first stale document found;
* arbitrary cleanup;
* whatever subsystem was most recently edited.

Distinguish:

```text
LOCAL DEFECT
from
CAMPAIGN-LIMITING CAPABILITY GAP
```

A local defect may still be selected if resolving it materially advances a
campaign capability.

Before accepting a new task, state internally:

```text
CAMPAIGN CAPABILITY AFFECTED:
CURRENT LIMITATION:
WHY THIS LIMITATION MATTERS TO THE MISSION:
BOUNDED RESPONSIBILITY:
EXPECTED EVIDENCE OF PROGRESS:
```

If you cannot explain how successful completion materially advances the
campaign mission, do not elevate the work into the active campaign merely
because it is useful cleanup.

## Candidate Architecture

Treat the following as the current candidate direction, not unquestionable
implementation requirements.

The campaign should investigate, refine, implement, or reject these ideas
according to repository evidence.

### 1. Agent-owned semantic control

The active coding agent should own semantic decisions about what engineering
responsibility becomes warranted next.

Do not assume a deterministic router should own the top-level process.

### 2. Artifact-mediated continuation

Durable, schema-constrained, mechanically validated artifacts should carry
important state between consequential engineering responsibilities.

Conversation history should not silently be the only place where necessary
continuation state exists.

### 3. Responsibility before capability

Conceptually distinguish:

```text
warrant
-> responsibility
-> capability / Skill / ordinary coding / bounded workflow
```

Do not treat Skill identity as the primary semantic classification.

### 4. Warrant and authority remain separate

Evidence can warrant a responsibility.

Evidence does not manufacture execution authority.

Preserve:

```text
recommendation
!= selection
!= execution authorization
```

and more generally:

```text
warrant
!= authority
```

### 5. Deterministic machinery supports mechanics

Scripts are appropriate for deterministic operations such as:

* schema validation;
* normalization;
* provenance;
* registry integrity;
* hashing;
* contract checking;
* lifecycle transitions;
* artifact discovery;
* mechanical continuation triggers.

Do not make deterministic scripts responsible for semantic engineering
judgment merely because they are easy to automate.

### 6. Hooks may provide liveness, not semantic judgment

A future continuation mechanism may look approximately like:

```text
artifact produced
-> validate
-> record durable state
-> wake/re-enter coding agent
-> coding agent reassesses next warranted responsibility
```

Do not assume the hook should directly encode:

```text
artifact X
-> execute Skill Y
```

unless evidence demonstrates that such routing is genuinely stable and
warranted.

### 7. Workflows are potentially bounded subgraphs

Do not assume predefined workflows should be the product-level controller.

A registered workflow may remain valuable when a recurring sequence is:

* stable;
* mechanically expressible;
* low in semantic ambiguity;
* repeatedly useful;
* measurably more reliable than ordinary agent execution.

Treat workflows as potential reusable bounded execution subgraphs unless
evidence warrants a stronger role.

### 8. Inner and outer control may be distinct

Investigate whether the product requires:

Outer repository-evolution loop

```text
product goal
-> capability state
-> select next consequential repository gap
-> create bounded task
```

and:

Inner task-execution loop

```text
task goal
-> uncertainty
-> warranted responsibility
-> capability
-> evidence
-> validation
-> reassessment
-> task closure
```

Do not force them into one abstraction if repository evidence shows they
require different state or semantics.

## Architecture Discipline

Do not treat the candidate architecture above as permission to rewrite the
repository wholesale.

For every substantial architectural modification:

1. inspect the current authoritative documentation and implementation;
2. identify what existing behavior would change;
3. distinguish current ratified behavior from historical/prototype behavior;
4. determine whether the change is actually needed for the campaign;
5. prefer the smallest coherent architectural transition;
6. update documentation/contracts when implementation changes product
   semantics;
7. add appropriate regression tests;
8. qualify the exact resulting candidate.

Avoid speculative infrastructure.

Do not build a framework merely because the framework would make the
architecture elegant.

## Scope vs. Complexity Discipline

Treat the campaign itself as high-scope and potentially high-complexity.

Do NOT execute it as a high-scope/high-complexity monolith.

Continuously decompose the campaign into smaller bounded responsibilities.

Prefer execution units that are:

* low or moderate in surface area;
* conceptually coherent;
* independently verifiable;
* reversible when possible;
* protected by explicit interfaces or contracts where sufficiently mature.

Do not freeze speculative interfaces merely for decomposition convenience.

Freeze only boundaries supported strongly enough by product/repository
evidence.

## Durable Campaign State

Maintain a durable campaign record inside the repository in an appropriate
non-authoritative research/development location unless a current canonical
artifact already serves this purpose.

Do not immediately create a complex formal schema.

Begin with the smallest useful representation.

At minimum preserve:

```text
CAMPAIGN MISSION

CURRENT PRODUCT / CAPABILITY STATE

COMPLETED CAMPAIGN RESPONSIBILITIES

EVIDENCE PRODUCED

CURRENTLY DEMONSTRATED CAPABILITIES

KNOWN MATERIAL GAPS

ACTIVE CONSTRAINTS

OPEN DECISION-CHANGING UNCERTAINTIES

CURRENT HIGHEST-LEVERAGE CAPABILITY BOUNDARY

CURRENT / NEXT WARRANTED RESPONSIBILITY

AUTHORITY OR OWNER DECISIONS REQUIRED

DEFERRED NON-CAMPAIGN FINDINGS

CAMPAIGN ACCEPTANCE STATUS
```

Update this state after every consequential repository-level responsibility.

This record exists so that campaign reasoning does not live exclusively in
transient context.

Do not over-engineer it before repeated use demonstrates stable fields.

## Handling Findings

You will encounter defects that are real but not campaign-critical.

Classify them rather than automatically expanding scope.

Use categories such as:

```text
CAMPAIGN_BLOCKING
CAMPAIGN_RELEVANT
LOCAL_BUT_REAL
HISTORICAL_ONLY
DEFERRED
NO_ACTION_WARRANTED
```

Do not turn repository search hits into backlog automatically.

Do not repair historical evidence merely because it contains obsolete
vocabulary.

Do not create work merely to make the repository look clean.

## Responsibility Execution

For each active bounded responsibility:

### 1. Establish the decision

What decision must this work support?

### 2. Identify the uncertainty

What unresolved fact could make the apparent action wrong?

### 3. Gather the cheapest sufficient evidence

Prefer:

* repository evidence for repository facts;
* tests/probes for behavioral uncertainty;
* owner decisions for true preference/authority questions;
* external evidence only when the repository cannot answer the question.

### 4. Act only when warranted

Possible bounded responsibilities include:

* product-definition clarification;
* architecture reconciliation;
* domain-model refinement;
* artifact-contract design;
* continuation-state design;
* Skill/capability metadata improvement;
* workflow demotion/repair/retirement;
* bounded implementation;
* migration;
* test-harness improvement;
* verification;
* documentation reconciliation;
* issue/PR closure.

Do not force work into these labels if another description is more accurate.

### 5. Validate

Use the strongest relevant objective referee available.

Examples:

```text
pytest
validators
repo validation
schema validation
lint
type check
build
exact-head CI
targeted behavioral probe
fresh-context reconstruction
```

Do not substitute mechanical validation for semantic correctness when semantic
correctness remains the actual question.

### 6. Update campaign state

Record what changed and why.

### 7. Reassess from the campaign level

Do not automatically continue with the nearest follow-up.

Return mentally to:

What capability now constrains the campaign mission most?

The answer may be somewhere else in the repository.

## Fresh-Context and Artifact Sufficiency

One central product property under investigation is whether durable
repository state can support continuation without requiring a single enormous
conversation context.

Whenever architecturally appropriate, test whether a new coding-agent context
could reconstruct:

* the campaign mission;
* the current capability state;
* why the current task was selected;
* what has already been established;
* what remains uncertain;
* what responsibility is warranted next;
* what authority is available.

If this cannot be reconstructed from durable state, classify the missing
information before designing infrastructure to solve it.

Distinguish failures such as:

```text
MISSING_DURABLE_STATE
CAPABILITY_DISCOVERY_FAILURE
WARRANT_AMBIGUITY
AUTHORITY_AMBIGUITY
PRODUCT_DIRECTION_AMBIGUITY
INCIDENTAL_CONTEXT_LOSS
```

Repair demonstrated recurrent deficiencies rather than speculative ones.

## Workflow-System Policy During This Campaign

The current workflow system is under architectural reconsideration.

Do not delete it merely because the campaign uses a different control model.

Do not expand it merely because an existing use case does not fit.

As real responsibility traces accumulate, classify workflows as:

```text
KEEP_AS_BOUNDED_SUBGRAPH
REPAIR
DEMOTE
RETIRE_CANDIDATE
HISTORICAL
INSUFFICIENT_EVIDENCE
```

A workflow earns new investment when repeated real execution demonstrates:

```text
recurring responsibility sequence
+ stable ordering
+ sufficiently low semantic ambiguity
+ measurable reliability/cost benefit
```

Prefer recovering workflows from successful repeated traces over inventing
broad workflow catalogs prospectively.

## Hooks Policy During This Campaign

Do not build hooks merely because they are part of the candidate
architecture.

First establish manually what continuation event and state actually need to
exist.

If hook automation becomes warranted, initially restrict hooks to mechanical
responsibilities such as:

```text
detect artifact
-> validate artifact
-> register provenance/state
-> signal coding agent to reassess
```

Semantic next-responsibility selection remains agent-owned unless repeated
evidence demonstrates a legitimately deterministic transition.

## Git and Change Discipline

Work incrementally.

Prefer one coherent commit or PR per meaningful bounded responsibility when
practical.

Before modifying code:

* confirm current branch/base;
* inspect relevant tests and contracts;
* understand current behavior.

After modifying code:

* run focused tests;
* run required repository-level qualification;
* inspect the diff;
* verify no generated/unrelated files leaked into the change.

Do not merge a candidate solely because targeted tests pass if repository
policy requires broader qualification.

Where exact-head CI exists, distinguish:

```text
tested locally
qualified PR head
integrated state on main
```

Do not make stronger claims than the evidence supports.

## Owner Decisions

Do not ask the owner questions that repository evidence can answer.

Ask for an owner decision only when progress genuinely depends upon:

* product preference;
* authority expansion;
* an irreversible tradeoff not resolved by current policy;
* external credentials/environment;
* acceptance of a material product-direction choice.

Before asking, present:

```text
DECISION REQUIRED:
WHY REPOSITORY EVIDENCE CANNOT RESOLVE IT:
OPTIONS:
CONSEQUENCES:
RECOMMENDED OPTION, IF ANY:
```

Do not stop for minor uncertainty when a conservative bounded action remains
available.

## Campaign Acceptance Conditions

The campaign is not complete because individual fixes have landed.

Continue until the strongest currently supportable version of the following
is true:

1. The top-level semantic control model is explicit and internally coherent.
2. The role of the active coding agent is clear.
3. Warrant, responsibility, capability selection, and authority are not
   conflated.
4. Durable artifacts can carry consequential continuation state across
   responsibilities.
5. At least one realistic multi-responsibility task can be continued from
   durable state without depending materially on hidden conversation memory.
6. Repository-level development direction can be represented sufficiently for
   the agent to select consequential capability work rather than merely the
   nearest local defect.
7. The role of deterministic scripts is bounded and coherent.
8. The intended role of hooks, if hooks remain warranted, is defined and
   supported by evidence.
9. The old workflow system has a clear disposition:
   * retained bounded roles;
   * migration path;
   * or explicit reason for remaining unresolved.
10. Existing useful functionality is not casually destroyed during
    architectural transition.
11. Tests, validators, contracts, docs, and implementation agree sufficiently
    with the resulting architecture.
12. The repository passes the appropriate complete qualification for the
    changes made.
13. Remaining material limitations are explicitly documented rather than
    hidden behind "complete."

These acceptance conditions may be refined if evidence shows that some are
incorrectly formulated.

Do not satisfy them performatively.

If the evidence contradicts an assumption in this prompt, update the
architecture rather than forcing reality to match the prompt.

## Campaign Stopping Rules

STOP the campaign only when one of these is true:

**COMPLETE** -- Campaign acceptance conditions are materially satisfied and the
resulting repository state is qualified.

**OWNER_DECISION_REQUIRED** -- A consequential product/authority decision
cannot be resolved from repository evidence and no safe bounded work remains
before that decision.

**EXTERNAL_BLOCKER** -- Required credentials, external systems, unavailable
infrastructure, or another genuine environment dependency prevents meaningful
continuation.

**CAMPAIGN_PREMISE_INVALIDATED** -- Evidence demonstrates that the mission or
core candidate architecture is materially wrong and continuing implementation
would be wasteful. In that case, stop with a detailed evidence-grounded
recommendation rather than forcing the campaign through the original
assumptions.

Do NOT stop simply because:

* one issue is closed;
* one PR is merged;
* one subsystem works;
* context is becoming large;
* another reasonable task exists;
* a local fix appears satisfactory.

If context pressure becomes material, checkpoint all necessary durable
campaign state and continue from that durable state using an appropriate
fresh context rather than silently dropping campaign memory.

## Final Campaign Report

When the campaign reaches a legitimate stopping condition, produce:

1. **Mission outcome** -- What was achieved relative to the campaign mission?
2. **Architecture before and after** -- What product/control model existed at
   the start? What model now exists?
3. **Responsibility trace** -- List the major bounded responsibilities
   actually performed in order. Do not retrospectively invent a cleaner
   workflow than what really occurred.
4. **Repository changes** -- Major files, contracts, ADRs, scripts, Skills,
   workflows, hooks, tests, and other implementation surfaces changed.
5. **Evidence** -- For each major architectural claim, point to the repository
   evidence supporting it.
6. **Qualification** -- Report targeted tests, full tests, validators,
   lint/type/build checks, CI, integration state, and any failures or
   exceptions.
7. **Workflow-system disposition** -- What was kept, demoted, repaired,
   retired, or left unresolved?
8. **Artifact-mediated continuation result** -- What continuation state proved
   necessary? Could fresh contexts reconstruct it? What gaps remain?
9. **Remaining limitations** -- Separate: known product limitations;
   engineering debt; unvalidated hypotheses; owner decisions; environment
   blockers; intentionally deferred work.
10. **Campaign disposition** -- Use exactly one:

```text
CAMPAIGN_COMPLETE
OWNER_DECISION_REQUIRED
EXTERNAL_BLOCKER
CAMPAIGN_PREMISE_INVALIDATED
```

Explain why.

## Final Operating Principles

Keep these principles active throughout the campaign:

Own the campaign, but execute one bounded responsibility at a time.

Preserve the global mission without carrying the entire repository history in
working context.

Strategic decomposition chooses the task; bounded execution solves the task.

Evidence warrants responsibilities. Authority permits actions.

Responsibility comes before capability selection.

Artifacts are durable state and context-compression boundaries, not
bureaucratic paperwork.

Deterministic machinery should validate and coordinate what is deterministic.

Agent reasoning should remain responsible for semantic decisions that are not
actually deterministic.

Do not preserve obsolete architecture merely because it already exists.

Do not replace it until evidence supports the replacement.

Do not optimize for touching many files. Optimize for making the product
materially more coherent and capable.

Continue until the campaign mission is materially achieved, genuinely blocked,
or invalidated.
