# Reasoning Model

**Status:** Canonical semantic reasoning lifecycle, v0  
**Purpose:** Define how Sensemaking should move from repository state to evidence-grounded decisions without turning deterministic infrastructure into a semantic controller.

## Core loop

```text
Intent + Target
      |
      v
Bound current repository state
      |
      v
Collect observations
      |
      v
Construct evidence catalog
      |
      v
Identify entities and relations
      |
      v
Author claims with epistemic status
      |
      v
Detect contradiction / uncertainty
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
Advance / defer / close
      |
      v
Persist transition + handoff
```

## Stage 0 — Bind intent and scope

Inputs:

- user/owner request;
- Campaign mission if one exists;
- explicit constraints;
- authority boundary;
- target repository.

Outputs:

- Goal/Mission;
- scope boundary;
- initial SuccessConditions where explicit;
- TargetSnapshot or equivalent currentness boundary.

### Authority split

Deterministic machinery may bind target identity and state. The agent interprets the user's semantic goal. Explicit user/owner intent should be preserved separately from agent inference.

## Stage 1 — Collect observations

The agent or a bounded probe gathers source-grounded observations.

Examples:

```text
file path exists
module imports another module
README states architecture rule
workflow invokes command X
test T passes
Git worktree is dirty
```

Observations should preserve:

- source;
- method;
- scope;
- currentness;
- exact bytes/identity where relevant.

### Rule

Do not embed a strong semantic conclusion in an observation merely because it is convenient.

Bad:

```text
Observation: architecture is tightly coupled.
```

Better:

```text
Observed: package A imports 17 internal modules from package B.
Inferred claim: this may represent broad coupling across the stated A/B boundary.
```

## Stage 2 — Construct the evidence catalog

Evidence is organized so later claims can cite what informed them.

Evidence may include:

- observations;
- probe results;
- source excerpts;
- test/runtime output;
- historical commits;
- issues/PRs;
- artifact bytes;
- owner statements;
- ratified architecture decisions.

The catalog does not need to be a new runtime store initially. Existing Campaign evidence and Skill artifacts may serve this role.

## Stage 3 — Build a bounded semantic map

The agent identifies only the entities and relations necessary to answer current competency questions.

Example:

```text
SoftwareCapability: authentication
realizedBy -> Component: auth-service

Component: auth-service
exposes -> Interface: TokenIssuer

dependency: web -> auth-service
crossesBoundary -> application/domain boundary
```

### Rule

The semantic map is demand-driven, not exhaustive. Do not model the entire repository when the decision concerns one bounded subsystem.

## Stage 4 — Author claims

Claims connect evidence to meaning.

A useful claim states:

```text
subject
proposition
evidence
scope/currentness
epistemic status
counter-evidence or uncertainty when material
```

Example:

```text
Claim:
  The web package bypasses the public auth interface and depends directly
  on auth implementation details.

Evidence:
  import observations E12-E18
  public-interface declaration E19

Status:
  INFERRED

Currentness:
  target snapshot S04
```

## Stage 5 — Detect contradictions and uncertainties

Sensemaking should distinguish:

```text
Contradiction
= two material claims/sources cannot both hold in overlapping scope

Uncertainty
= unresolved question whose answer could affect a decision
```

A contradiction may generate an uncertainty, but they are not identical.

Example:

```text
Observed claim:
  package web imports auth/internal.py

Ratified claim:
  architecture decision D1 says web may depend only on auth/public.py

Contradiction:
  observed dependency conflicts with ratified dependency rule

Uncertainty:
  is internal.py usage temporary compatibility code or unintended drift?
```

## Stage 6 — Select consequential uncertainty

This remains an **agent semantic responsibility**.

The agent asks:

1. Could any credible unresolved uncertainty change the next action, scope, authority path, or stop/continue decision?
2. Which uncertainty has the highest decision relevance now?
3. What evidence could materially change the answer?

Do not automatically rank uncertainty by a generic score until repeated evidence demonstrates a safe, useful model.

## Stage 7 — Select warranted responsibility

The agent translates the decision-changing uncertainty or established condition into a bounded responsibility.

Examples:

```text
repository_sensemaking
architectural_review
problem_framing
repair_verification
documentation_alignment
product_specification
research_synthesis
```

A responsibility should identify:

- what decision is blocked;
- scope;
- trigger evidence;
- authority;
- success conditions;
- dependencies.

This aligns directly with the existing Campaign `Responsibility` contract.

## Stage 8 — Inspect capability and authority

Only after selecting the responsibility should the agent inspect available capabilities.

```text
warranted responsibility
!= available capability
!= authorized capability
```

Deterministic capability lookup may report declared compatibility and availability. The agent decides which available capability is semantically appropriate. Authority is checked independently.

## Stage 9 — Perform bounded work

The chosen Skill/tool/engineering action operates within the declared responsibility and authority scope.

Possible outputs:

```text
Artifact
Observation set
Repository Change
External result
Validation evidence
No-result / blocker evidence
```

A no-result may be semantically valuable if it narrows uncertainty honestly.

## Stage 10 — Validate mechanics and admit evidence

Validators establish only their declared contracts.

Examples:

```text
artifact has required structure
artifact references resolvable evidence
transition chain reconstructs
exact bytes match recorded digest
target snapshot matches expected identity
```

Validation result is evidence for later semantic judgment; it is not the judgment itself.

## Stage 11 — Evaluate the result semantically

The agent now asks:

```text
What did the new evidence actually establish?
What remains uncertain?
Did the responsibility's success conditions become satisfied?
Did the work introduce new contradictions?
Does evidence justify advance, defer, or close?
```

Important separation:

```text
Capability execution completed
!= Responsibility satisfied
!= Goal achieved
```

## Stage 12 — Author a decision and durable transition

The agent chooses:

```text
advance
defer
close
```

and cites the evidence informing that decision.

The deterministic Campaign layer persists the transition, checks integrity, and preserves the target/evidence lineage.

## Stage 13 — Handoff and fresh-context reconstruction

A later agent reconstructs:

- mission and explicit intent;
- current target state;
- current responsibility;
- current consequential uncertainty;
- authority;
- established/relevant claims;
- evidence and contradictions;
- transition history;
- deferred work;
- stop/continuation boundaries.

The later agent must not require the prior conversation to know why the Campaign is in its current state.

## Reasoning object flow

The preferred semantic chain is:

```text
EvidenceSource
  -> Observation
  -> Evidence
  -> Claim
  -> EpistemicStatus
  -> Contradiction / Uncertainty
  -> Responsibility
  -> SensemakingCapability
  -> Artifact / Change / Evidence
  -> Validation
  -> Decision
  -> Transition
```

Not every task requires every object. The chain exists to prevent hidden jumps in reasoning.

## Allowed deterministic derivations

Examples suitable for deterministic implementation when supported by bounded probes/contracts:

```text
Git metadata -> TargetSnapshot
source parser -> import edge
canonical serialization -> content digest
schema validation -> structural PASS/FAIL
known memberships + edge -> boundary-crossing relation
transition log -> reconstructibility result
complete-scope search + zero matches -> bounded absence observation
```

## Semantic operations reserved to agent/human judgment

By default:

```text
identify consequential uncertainty
classify semantically meaningful Component
infer SoftwareCapability realization
interpret architectural intent unless ratified
judge whether dependency crossing is a violation
select warranted Responsibility
select semantically appropriate Capability
judge whether repair succeeded
prioritize ProductChange
judge whether evidence justifies closure
```

A future proposal may mechanize a narrower subset only with empirical evidence and an explicit authority decision.

## Stopping rule

Sensemaking should stop investigating when:

1. the decision-changing uncertainty has enough evidence for a bounded decision;
2. remaining uncertainty would not change the next action within current scope/authority; or
3. further evidence is unavailable, outside authority, or not worth the current decision cost.

This rule protects the system from turning ontology-driven reasoning into analysis paralysis.