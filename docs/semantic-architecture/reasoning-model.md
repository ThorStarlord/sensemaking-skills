# Reasoning Model

**Status:** Canonical semantic reasoning lifecycle, v1 control-scope integration  
**Purpose:** Define how Sensemaking moves from repository/product state to evidence-grounded decisions without turning deterministic infrastructure into a semantic controller.

## Core loop

```text
Intent + Target
      |
      v
Bound current state
      |
      v
Collect observations
      |
      v
Construct evidence catalog
      |
      v
Identify entities and relations as needed
      |
      v
Author claims with epistemic status
      |
      v
Detect contradiction / uncertainty
      |
      v
Agent identifies the decision being supported
      |
      v
Agent selects consequential uncertainty
      |
      v
Agent selects warranted responsibility
      |
      v
Inspect declared capabilities + authority
      |
      v
Perform bounded work
      |
      v
Produce artifact / change / evidence
      |
      v
Mechanical validation + admission
      |
      v
Agent judges semantic result
      |
      v
Author scope-appropriate decision
      |
      v
Persist/reconcile durable state when warranted
```

This semantic lifecycle can operate at more than one control scope. The
Strategic Outer Loop answers **at what decision scope the agent is reasoning**;
this Reasoning Model answers **how evidence is transformed into bounded semantic
judgment at that scope**.

```text
semantic reasoning model != control level
same reasoning grammar != same authority
Level-3 decision != Level-4 thesis decision
```

## Stage 0 — Bind intent and scope

Inputs may include user/owner request, Campaign mission, strategic decision,
explicit constraints, authority boundary, and target repository/product state.

Outputs include a bounded Goal/Mission or decision, scope, explicit success
conditions where applicable, authority, and a currentness/identity boundary.

Deterministic machinery may bind identity and state. The agent interprets
semantic intent. Explicit user/owner intent remains distinct from agent
inference.

## Stage 1 — Collect observations

The agent or bounded probe gathers source-grounded observations, for example:

```text
file path exists
module imports another module
README states architecture rule
workflow invokes command X
test T passes
Git worktree is dirty
owner ratified ADR 0029
repeated Campaigns hit the same product-boundary ambiguity
```

Observations preserve source, method, scope, currentness, and exact
bytes/identity when relevant.

Do not hide semantic conclusions inside observations merely because convenient.

```text
Observed: package A imports 17 internal modules from package B.
Inferred claim: this may represent broad coupling across the stated A/B boundary.
```

## Stage 2 — Construct the evidence catalog

Evidence may include observations, probe results, source excerpts, test/runtime
output, commits, issues/PRs, artifact bytes, owner statements, ratified ADRs,
Campaign results, and product/repository behavior records.

The catalog does not require a new runtime store. Existing Campaign evidence,
ADRs, handoffs, STATUS, and Skill artifacts may carry the evidence appropriate
to the current control scope.

## Stage 3 — Build a bounded semantic map

Identify only entities/relations required by the current decision. The semantic
map is demand-driven, not exhaustive.

Example:

```text
SoftwareCapability: authentication
realizedBy -> Component: auth-service

Component: auth-service
exposes -> Interface: TokenIssuer

dependency: web -> auth-service
crossesBoundary -> application/domain boundary
```

At Level 3 or 4, the bounded map may instead relate product commitments,
capabilities, strategic boundaries, decisions, evidence ceilings, and affected
responsibilities without pretending those relations are mechanically inferred.

## Stage 4 — Author claims

Claims connect evidence to meaning. A useful claim states subject, proposition,
evidence, scope/currentness, epistemic status, and counter-evidence/uncertainty
when material.

Example:

```text
Claim:
  The web package bypasses the public auth interface.
Evidence:
  import observations E12-E18 + public-interface declaration E19
Status:
  INFERRED
Currentness:
  target snapshot S04
```

At Level 3 a claim may be "a material repository boundary exists." At Level 4
a claim may be "a ratified product commitment may no longer match current
product behavior." The broader scope does not make the claim more certain.

## Stage 5 — Detect contradictions and uncertainties

```text
Contradiction
= two material claims/sources cannot both hold in overlapping scope

Uncertainty
= unresolved question whose answer could affect a decision
```

A contradiction may generate uncertainty, but they are not identical. A
repeated weak product-level signal may be preserved as a Thesis Tension without
yet becoming a decision-changing Level-4 contradiction.

## Stage 6 — Identify the decision being supported

Before selecting an uncertainty/responsibility, state the decision whose answer
could change.

At Level 2 this may already be represented by `decision_blocked`. At Level 3 it
is the **Strategic Decision to Support**. At Level 4 it is the thesis question
about an affected strategic commitment.

```text
observation != decision
boundary != decision
uncertainty is consequential because it can change a decision
```

Making the decision explicit prevents hidden jumps from interesting evidence to
unwarranted work.

## Stage 7 — Select consequential uncertainty

This remains an **agent semantic responsibility**.

Ask:

1. Could a credible unresolved uncertainty change the decision, scope, authority path, or stop/continue result?
2. Which uncertainty is decision-relevant now?
3. What evidence could materially change the answer?

Do not automatically rank uncertainty with a generic score.

## Stage 8 — Select warranted responsibility

Translate the decision-changing uncertainty or established condition into a
bounded responsibility.

Examples include `repository_sensemaking`, `architectural_review`,
`problem_framing`, `repair_verification`, `documentation_alignment`,
`product_specification`, and `research_synthesis`.

A responsibility identifies the decision supported, scope, trigger evidence,
authority, success conditions, and dependencies. At Level 3 it additionally
serves a selected strategic boundary and should be the smallest intervention
sufficient for the strategic decision.

## Stage 9 — Inspect capability and authority

Only after responsibility selection should the agent inspect capabilities.

```text
warranted responsibility
!= available capability
!= authorized capability
```

Deterministic lookup may report declared compatibility/availability. The agent
selects semantic appropriateness. Authority is independent.

## Stage 10 — Perform bounded work

The selected Skill/tool/engineering action operates within the responsibility
and authority scope. Outputs may include an artifact, observations, repository
change, external result, validation evidence, or no-result/blocker evidence.

A no-result can be valuable if it narrows uncertainty honestly.

## Stage 11 — Validate mechanics and admit evidence

Validators establish only declared mechanical contracts, such as required
artifact structure, resolvable evidence refs, reconstructible transition chain,
exact-byte digest, or target identity/currentness.

Validation is evidence for later semantic judgment; it is not the judgment.

## Stage 12 — Evaluate the result semantically

Ask:

```text
What did the evidence establish?
What remains uncertain?
Did success/closure conditions become satisfied?
Did new contradictions appear?
Did the strategic or thesis rationale survive?
What decision is now warranted?
```

```text
Capability execution completed
!= Responsibility satisfied
!= Goal achieved
!= Strategic Decision resolved
!= Product Thesis validated
```

## Stage 13 — Author a scope-appropriate decision

At Level 2, common Campaign decisions are `advance`, `defer`, or `close`.

At Level 3, outcomes may include continue, no-change, reject, defer, owner
decision, thesis-review escalation, or stop.

At Level 4, explicit dispositions are `REAFFIRM`, `REINTERPRET`, `REVISE`,
`RETIRE`, or `SUPERSEDE`, with owner ratification where authority is reserved.

Do not collapse these vocabularies into one universal runtime enum.

## Stage 14 — Persist / reconcile / hand off

Persist only the durable state warranted by the current control scope:

- Level 2: Campaign transitions, evidence, handoff/resume state;
- Level 3: current strategic projection in `STATUS.md` plus linked evidence;
- Level 4: canonical product strategy, ADR/revision record, and downstream
  reconciliation requirement.

A later agent should not require the previous conversation to know why the
current decision state exists.

## Reasoning object flow

The preferred semantic chain is:

```text
EvidenceSource
  -> Observation
  -> Evidence
  -> Claim
  -> EpistemicStatus
  -> Contradiction / Uncertainty
  -> DecisionBeingSupported
  -> Responsibility
  -> SensemakingCapability
  -> Artifact / Change / Evidence
  -> Validation
  -> Decision
  -> DurableTransitionOrReconciliation
```

`DecisionBeingSupported` is a conceptual reasoning role, not a new required
runtime entity. Existing representations such as `decision_blocked`, Strategic
Decision to Support, or affected Level-4 commitment may instantiate it.

Not every task requires every object. The chain exists to prevent hidden jumps.

## Level-3 instantiation — Strategic Repository Evolution

At Level 3, the shared reasoning grammar becomes:

```text
OBSERVATION
current product/repository capability condition
        |
        v
EVIDENCE
repository facts / qualified artifacts / owner decisions / evidence ceilings
        |
        v
CLAIM
one or more material strategic boundaries exist
        |
        v
STRATEGIC DECISION TO SUPPORT
what consequential repository/product decision depends on resolving them?
        |
        v
QUALITATIVE COMPARISON
mission relevance / decision value / blocking / resolvability /
error consequence / deferral / reversibility / authority / dependency
        |
        v
DECISION-CHANGING UNCERTAINTY
what could make the boundary selection wrong or premature?
        |
        v
WARRANTED REPOSITORY RESPONSIBILITY
        |
        v
SMALLEST WARRANTED INTERVENTION + AUTHORITY
        |
        v
LEVEL-2 / LEVEL-1 WORK
        |
        v
VALIDATED RESULT / EVIDENCE
        |
        v
STRATEGIC ADJUDICATION
continue / close / defer / reject / no change /
owner decision / thesis review / stop
```

The qualitative comparison is agent reasoning, not a deterministic score. The
Strategic Frontier is decision-relevant possibility state, not an input queue.

## Level-4 instantiation — Product Thesis / Strategy Revision

At Level 4, the same grammar operates over slower-changing commitments:

```text
OBSERVATIONS
repeated repository/product behavior + owner direction
        |
        v
EVIDENCE
qualified repository results / product evidence / owner statements
        |
        v
CLAIM
an existing product-thesis commitment may be wrong, stale, or ambiguous
        |
        +-- weak recurring signal -> preserve THESIS TENSION when useful
        |
        v
THESIS DECISION TO SUPPORT
is the affected commitment still the right strategic commitment?
        |
        v
THESIS UNCERTAINTY / CONTRADICTION
        |
        v
AFFECTED COMMITMENT + BOUNDED ALTERNATIVES
        |
        v
ATTRIBUTED RECOMMENDATION
        |
        v
OWNER RATIFICATION WHEN RESERVED
        |
        v
REAFFIRM / REINTERPRET / REVISE / RETIRE / SUPERSEDE
        |
        v
MANDATORY LEVEL-3 RECONCILIATION
```

The Semantic Reasoning Model does not decide which Level-4 alternative wins and
does not grant owner authority. It only supplies a consistent evidence-to-
decision grammar.

## Relationship between semantic model and control model

```text
Semantic Architecture Reasoning Model
= evidence-to-decision grammar

Four-Level Control Model
= decision scope + authority ownership

Reasoning Model can instantiate at Level 2, 3, or 4
!= those levels are the same thing
```

The same word `decision` therefore has scope-specific authority. A Level-3
strategic decision cannot revise the product thesis; a Level-4 thesis disposition
does not directly authorize implementation.

## Allowed deterministic derivations

Suitable examples when supported by bounded contracts include:

```text
Git metadata -> TargetSnapshot
source parser -> import edge
canonical serialization -> content digest
schema validation -> structural PASS/FAIL
known memberships + edge -> boundary-crossing relation
transition log -> reconstructibility result
complete-scope search + zero matches -> bounded absence observation
Markdown anchor contract -> representation PASS/FAIL
```

## Semantic operations reserved to agent/human judgment

By default:

```text
identify consequential uncertainty
identify Strategic Decision to Support
compare frontier candidates semantically
classify meaningful Component / capability realization
interpret architecture intent unless ratified
judge whether dependency crossing is a violation
select warranted Responsibility / Capability
judge whether repair succeeded
prioritize ProductChange
judge whether evidence justifies closure
classify Thesis Tension materiality
judge whether Level-4 review is required
select Level-4 disposition
```

A future proposal may mechanize a narrower subset only with a separately
justified mechanical contract and authority decision.

## Stopping rule

Stop investigating when:

1. decision-changing uncertainty has enough evidence for a bounded decision;
2. remaining uncertainty would not change action within scope/authority; or
3. further evidence is unavailable, outside authority, or not worth the current decision cost.

At Level 3, absence of a warranted strategic boundary is a valid stop. At Level
4, absence of a decision-changing thesis issue is a reason to return control to
Level 3 rather than manufacture strategy work.
