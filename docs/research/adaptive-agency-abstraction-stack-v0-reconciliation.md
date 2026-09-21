# Adaptive Agency Abstraction Stack v0 — Sensemaking Reconciliation

**Status:** bounded research/product-boundary reconciliation; non-authoritative  
**Date:** 2026-09-21  
**Tracker:** Issue #444  
**Authority:** research only; ADR 0029, product strategy, the Four-Level Control Model, Policy Hierarchy, Campaign semantics, and existing execution/authority contracts remain controlling  
**Model:** adaptive-agency-abstraction-stack-v0.md  
**Design:** ../superpowers/specs/2026-09-21-adaptive-agency-abstraction-stack-v0-design.md

## 1. Reconciliation question

> Which parts of the Primitive -> Operator -> Skill -> Organization -> Institution idea already exist in Sensemaking, which clarify current guidance, which belong to the surrounding runtime/orchestration environment, and which expose a real product/runtime gap?

The answer is not “implement the ladder.”

The answer is:

> Preserve the ladder as a teaching aid, model the architecture as three interacting planes, and treat organizational learning as a bounded research hypothesis.

## 2. Current repository boundary

ADR 0029 defines Sensemaking as an agent-native repository decision-support and control layer.

It explicitly excludes:

- a custom coding-agent runtime;
- deterministic semantic planning/routing;
- automatic capability/Skill/workflow selection;
- generic cross-repository transaction orchestration;
- autonomous external-action authority.

Practical Agent Architecture also explicitly rejects a new multi-agent supervisor runtime, voting mechanism, job scheduler, or worker protocol inside Sensemaking.

Therefore:

~~~text
organization modeled != organization runtime warranted
~~~

## 3. Disposition table

| Concept | Current evidence/surface | Disposition | Smallest warranted consequence |
| --- | --- | --- | --- |
| Root Primitive | harness/tool/filesystem/GitHub/model/runtime affordances; local lifecycle/mechanical primitives | ENVIRONMENT_SUBSTRATE / OUTSIDE_PRODUCT | Define as research vocabulary only; no primitive registry |
| Cognitive Operator | General Agency challenge, exploration, causal/counterfactual reasoning, decomposition, comparison, simulation | ALREADY_PRESENT_RESEARCH | Preserve qualified term and relate it to packaged Skills |
| Capability / Skill | Capability registry, Skill registry, Skill Contract Manifests, Domain Packs, artifact/validation contracts | ALREADY_SATISFIED | Clarify Skill as one packaged Capability form; no new domain model |
| Delegation | Practical Agent Architecture parent/worker model; Execution Interface handoff/result | ALREADY_SATISFIED | Preserve worker result -> evidence -> parent reassessment |
| Organization | multi-agent delegation exists, but no role/topology/team lifecycle model | PARTIAL_CONCEPT / OUTSIDE_CURRENT_RUNTIME | Add research distinction only; no runtime/state/schema |
| Institution-like continuity | product strategy, ADRs, authority, Policy Hierarchy, Campaign durability, provenance/currentness, strategic continuity/reconciliation | ALREADY_PARTIALLY_REALIZED | Name the function carefully without creating Institution runtime |
| Organization runtime | explicitly excluded by ADR 0029/current PAA reconciliation | NOT_WARRANTED | No construction |
| Organizational-pattern learning | no normal-use evidence demonstrating need or value | RESEARCH_HYPOTHESIS | Preserve reopen conditions; do not experiment by default |

## 4. Question 1 — Root Primitive, Cognitive Operator, Capability, Skill

### Root Primitive

The current repository does not need a canonical Root Primitive registry.

Most foundational affordances are external to Sensemaking:

- file access;
- process execution;
- model/tool calls;
- messaging;
- worker creation where supported.

The repository also uses the word primitive locally for lifecycle/mechanical operations. The qualified term prevents accidental unification.

**Disposition:** ENVIRONMENT_SUBSTRATE / OUTSIDE_PRODUCT.

### Cognitive Operator

General Agency Model v0.1 already contains a suitable abstraction class.

It explicitly treats operators as cross-cutting reasoning transformations rather than runtime services.

Examples include:

- adversarial challenge;
- exploration;
- decomposition;
- comparison;
- causal/counterfactual reasoning;
- forecasting/simulation.

**Disposition:** ALREADY_PRESENT_RESEARCH.

### Capability

Campaign already has a first-class Capability abstraction and inspectable registry.

The current invariant is:

~~~text
warranted responsibility
!= capability availability
!= execution authority
~~~

No replacement is warranted.

**Disposition:** ALREADY_SATISFIED.

### Skill

Skill contracts/manifests already provide a deterministic shell around named reusable capabilities while rejecting deterministic semantic routing authority.

A Skill is therefore well-modeled as one packaged Capability form.

**Disposition:** ALREADY_SATISFIED.

## 5. Question 2 — What turns delegation into Organization?

Practical Agent Architecture v0 supports bounded delegation:

~~~text
parent semantic controller
-> bounded worker responsibility
-> returned result/evidence
-> parent reassessment
~~~

That is not yet a theory of Organization.

A useful threshold is reached when:

- roles among multiple actors become material;
- workers communicate laterally or coordinate shared dependencies;
- specialization changes task decomposition;
- actor relationships persist/recur long enough to affect method;
- the system dynamically reallocates responsibilities;
- coordination topology itself becomes a decision-relevant variable.

This threshold is semantic, not a deterministic actor-count rule.

**Disposition:** PARTIAL_CONCEPT / OUTSIDE_CURRENT_RUNTIME.

No new runtime is required merely to name the distinction.

## 6. Question 3 — Why Campaign is not Organization

Campaign currently preserves:

- goal;
- decision-changing uncertainty;
- warranted responsibility;
- authority;
- evidence;
- transitions;
- handoff/continuation;
- terminal state.

Campaign does not own:

- worker topology;
- role assignment;
- peer communication;
- team lifecycle;
- worker scheduling;
- dynamic workforce allocation.

Therefore:

~~~text
Campaign != Organization
~~~

A Campaign may host work performed by an Organization, but the Campaign remains the durable decision/responsibility substrate.

No Campaign schema v3 is warranted.

## 7. Question 4 — Institution versus persistent Organization

Sensemaking already demonstrates why the distinction matters.

A fresh agent can reconstruct product purpose, authority, strategic state, Campaign responsibility, evidence, provenance, and reserved decisions even when the prior controller is gone.

That property is institution-like.

The current mechanisms include:

- product strategy and owner-ratified ADRs;
- Four-Level Control Model;
- Policy Hierarchy;
- authority semantics;
- Campaign state and transition history;
- handoff/resume;
- provenance/currentness;
- strategic continuity/reconciliation;
- release/publication boundaries.

A persistent Organization may keep the same team structure.

An Institution can preserve constraints and commitments across complete replacement of the team.

**Disposition:** ALREADY_PARTIALLY_REALIZED as function; no Institution runtime or product-category claim.

## 8. Question 5 — Sensemaking versus software factory/orchestration

### Sensemaking owns/supports

- what decision is live;
- what responsibility is warranted;
- what evidence matters;
- authority boundaries;
- durable decision state when warranted;
- capability inspection;
- handoff/result evidence boundaries;
- semantic reconciliation;
- stopping/escalation.

### External orchestration/software factory owns

- worker creation;
- scheduler/queue;
- retries;
- parallel execution;
- role instantiation;
- communication transport;
- team/topology management;
- execution mechanics.

The two compose through current execution boundaries.

~~~text
decision/support control
!= worker allocation

execution handoff
!= organization scheduler

returned result
!= semantic closure
~~~

## 9. General Agency placement

The model clarifies an existing gap in description, not implementation.

General Agency already says metareasoning can decide whether to decompose or ask another agent.

The abstraction stack adds:

> When multiple actors are available, decomposition/metareasoning may produce an organizational arrangement as part of how cognition is allocated.

This is conditional.

~~~text
Organization is not a mandatory lifecycle stage
~~~

Institution remains an outer governance/persistence concept.

## 10. Practical Agent Architecture placement

The current multi-agent section remains valid.

Add only these distinctions:

~~~text
delegation != Organization automatically
Campaign != Organization
organization pattern != execution authority
~~~

The parent semantic controller still owns final adjudication under current architecture.

An external software factory can supply organization mechanics without moving semantic authority into the factory.

## 11. Capability growth versus authority growth

This is already strongly aligned with existing Sensemaking authority doctrine.

ADR 0026 states:

~~~text
recommendation != selection != execution authorization
~~~

Campaign Capability states:

~~~text
warranted responsibility
!= capability availability
!= execution authority
~~~

The abstraction model generalizes the same principle:

~~~text
capability growth != authority growth
agent-created abstraction != self-granted permission
~~~

An agent may propose a new Skill or coordination pattern without acquiring permission to change product strategy, merge, publish, deploy, or alter authority contracts.

## 12. Promotion and organizational-pattern learning

Current Sensemaking already has an evidence-bounded Skill-improvement path through usage research and skill-maintainer.

That is partial evidence for a general promotion shape:

~~~text
observed friction/pattern
-> candidate abstraction
-> evidence-linked proposal
-> validation/review
-> authorized change
~~~

The same shape could hypothetically apply to organizational patterns.

However, the repository has no evidence that a team/cell registry, organization compiler, or organization critic is needed.

Therefore:

~~~text
repeated successful coordination
!= automatic canonical promotion
~~~

**Disposition:** RESEARCH_HYPOTHESIS.

## 13. Product-boundary check

The package adds no product capability that ADR 0029 excludes.

It adds:

- research vocabulary;
- an interpretive crosswalk;
- bounded General Agency / Practical Agent Architecture references;
- a mechanical documentation contract test;
- a completion/handoff record.

It does not add:

- execution control;
- organization state;
- scheduling;
- worker allocation;
- routing;
- automatic spawning;
- authority.

Therefore:

~~~text
PRODUCT_BOUNDARY_CHANGE = NONE
~~~

## 14. Runtime/state/assurance gap check

### Durable state

No current repository decision requires persisted organizational topology.

Existing Campaign/strategic/handoff surfaces preserve the decision state that current product behavior needs.

**DURABLE_STATE_GAP:** none established.

### Deterministic assurance

No new mechanical predicate is needed beyond a small documentation contract that prevents future boundary drift.

**DETERMINISTIC_ASSURANCE_GAP:** no architecture-wide gap established.

### Runtime

The conceptual Organization layer is deliberately outside current Sensemaking runtime ownership.

**RUNTIME_GAP:** NO_RUNTIME_GAP_ESTABLISHED.

## 15. Reopen conditions

A future product/runtime package would require real pressure such as:

- multi-agent episodes where current execution handoff/result semantics lose decision-relevant coordination state;
- repeated inability to reconstruct why organizational allocation changed the result;
- repeated reuse of stable team/cell patterns whose safe operation needs a repository-owned contract;
- explicit owner direction to expand ADR 0029;
- an external factory integration that cannot preserve authority/evidence boundaries without a new shared organizational contract.

Absent such pressure:

~~~text
possible future organization capability
!= current construction responsibility
~~~

## 16. Final disposition

~~~text
RESEARCH_REFERENCE = WARRANTED
GUIDANCE_CLARIFICATION = WARRANTED
NEW_RUNTIME = NOT_WARRANTED
NEW_SCHEMA = NOT_WARRANTED
PRODUCT_BOUNDARY_CHANGE = NONE
RUNTIME_GAP = NO_RUNTIME_GAP_ESTABLISHED
CURRENT CONSTRUCTION RESPONSIBILITY = NONE
NEXT MODE = NORMAL_USE_VALIDATION
~~~

The correct repository action is to preserve the model as research/reference guidance and return to normal-use observation.
