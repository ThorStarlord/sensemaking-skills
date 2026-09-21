# Adaptive Agency Abstraction Stack v0 — Research/Reconciliation Design

**Status:** proposed bounded research/reference design  
**Date:** 2026-09-21  
**Tracker:** Issue #444  
**Target repository:** `ThorStarlord/sensemaking-skills`  
**Authority:** owner-directed research/reconciliation package only; not an ADR, product-strategy revision, runtime specification, schema change, Skill contract, routing rule, execution authority, or implementation authorization for a multi-agent organization runtime  
**Current product boundary:** ADR 0029 remains authoritative

## 1. Purpose

This package formalizes the conceptual relationship among:

```text
Root Primitive
-> Cognitive Operator
-> Capability / Skill
-> Organization
-> Institution
```

without treating those concepts as one literal implementation hierarchy.

The package exists because current Sensemaking already contains:

- cognitive operators in General Agency Model v0.1;
- Skill/capability contracts and registries;
- bounded parent/worker delegation in Practical Agent Architecture v0;
- durable Campaign, authority, provenance, policy, continuity, and strategic-control surfaces;
- an explicit external orchestration / software-factory boundary.

What is missing is a compact model explaining how those pieces relate and where organizational formation belongs.

## 2. Design conclusion

The original five-rung ladder is pedagogically useful but ontologically incomplete.

The canonical research interpretation for v0 is a **three-plane structural model** plus a separate **promotion/evolution ladder**.

### 2.1 Structural model

```text
GOVERNANCE / PERSISTENCE PLANE
Institution
- purpose
- authority
- policy
- provenance
- precedent
- continuity
- ratification / reserved decisions

COORDINATION PLANE
Organization
- multiple agents / actors
- role allocation
- communication topology
- specialization
- delegation
- coordination lifecycle

CAPABILITY PLANE
Capability / Skill
        ^
Cognitive Operator
        ^
Root Primitive
```

These planes interact but are not interchangeable.

### 2.2 Evolutionary promotion ladder

```text
ephemeral composition
-> candidate reusable operator
-> packaged capability / Skill
-> repeatable coordination pattern
-> institutionalized practice
```

Promotion means increasing reuse, externalization, validation, and persistence. It does **not** imply increasing authority.

## 3. Terminology

### 3.1 Root Primitive

A **Root Primitive** is an affordance supplied by the governed environment/runtime that an agent may invoke without reconstructing its lower-level implementation.

Examples may include:

- read;
- write;
- execute;
- communicate;
- invoke a model/tool;
- delegate/spawn when the harness exposes that affordance.

Root Primitive is a research-level term. This package does not create a Primitive registry or claim that Sensemaking owns the runtime substrate.

```text
root primitive available
!= primitive warranted for current work
!= authority to use primitive for any purpose
```

### 3.2 Cognitive Operator

A **Cognitive Operator** is a reusable reasoning transformation that can be applied at multiple stages of agency.

Existing General Agency examples include:

- adversarial challenge;
- exploration / alternative generation;
- causal reasoning;
- counterfactual reasoning;
- decomposition;
- comparison;
- simulation / forecasting.

Use the qualified phrase **Cognitive Operator** rather than naked `Operator` because the repository also uses operator terminology for human/operational concerns.

### 3.3 Capability / Skill

A **Capability** is an available bounded means of performing some responsibility. A **Skill** is one important packaged capability form: a named reusable methodology that may compose cognitive operators, domain knowledge, tools, artifact contracts, stopping rules, and boundary guards.

```text
Cognitive Operator
!= Skill

Skill
is-a kind of Capability

Capability available
!= capability selected
!= capability authorized
```

This design does not replace the existing Capability domain model.

### 3.4 Organization

An **Organization** is a materially multi-actor coordination structure in which work allocation, communication, specialization, or role relationships become part of how the objective is pursued.

Delegation alone does not establish an Organization.

A minimal distinction is:

```text
parent delegates bounded task to worker
= delegation

multiple actors coordinate through role/topology relationships
that materially affect decomposition or execution
= organizational behavior
```

Organization may be temporary. Persistence across contexts is not required for the concept.

### 3.5 Institution

An **Institution** is a persistent system of purpose, roles/rules, authority, decision procedures, memory/provenance, norms, and continuity that can survive replacement of individual participants.

Institution is not merely a larger Organization.

```text
large team
!= institution

persistent governance + continuity across actor replacement
= institution-like structure
```

Sensemaking already contains institution-like control surfaces, but this package does not reclassify the product itself as an autonomous institution or create an Institution runtime.

## 4. Campaign is not Organization

Campaign answers:

> What consequential decision/responsibility is live, why does the work exist, what evidence/authority constrains it, and how can continuation be reconstructed?

Organization answers:

> How are multiple intelligent actors arranged and coordinated to pursue the work?

Therefore:

```text
Campaign
!= Organization

Campaign durability
!= organizational persistence

execution handoff
!= organizational topology

worker result
!= organizational governance
```

An Organization may operate within a Campaign. A Campaign may be executed by one agent and therefore have no multi-agent organization at all.

No Campaign schema change follows from this distinction.

## 5. Placement against existing architecture

### 5.1 General Agency Model

General Agency Model v0.1 already contains Cognitive Operators and decomposition/metareasoning. The new model clarifies that **organization is a possible allocation/coordination consequence of metareasoning and decomposition when multiple actors are available**.

Organization is not added as a mandatory lifecycle stage.

Institution is treated as an outer governance/persistence substrate, not as a new sequential cognitive phase.

### 5.2 Practical Agent Architecture

Practical Agent Architecture v0 already defines parent/worker delegation and returned-evidence semantics.

The bounded extension is interpretive:

```text
delegation
-> may remain one parent / one worker

delegation + material multi-actor role/topology adaptation
-> organizational behavior

organizational behavior
-> still subordinate to purpose, warrant, authority, and evidence-return rules
```

No scheduler, supervisor, worker-allocation engine, communication bus, or organization state store is added.

### 5.3 Sensemaking product

Sensemaking owns/supports:

- decision support;
- evidence/warrant/authority discipline;
- durable Campaign and strategic state when warranted;
- capability inspection;
- execution handoff/result boundaries;
- provenance/currentness;
- reconciliation;
- owner/Level-4 reserved-decision boundaries.

Sensemaking does not currently own:

- dynamic workforce allocation;
- agent spawning policy;
- communication topology optimization;
- team lifecycle management;
- worker scheduling;
- organization runtime.

Those remain primarily the responsibility of the external harness / software-factory / orchestration environment unless future evidence and Level-4 authority change the product boundary.

### 5.4 Software factory / orchestration

External orchestration may instantiate:

- workers;
- subagents;
- queues;
- schedulers;
- retries;
- role assignments;
- communication channels;
- parallel execution.

Sensemaking-informed control supplies the decision context those mechanisms must not silently redefine.

## 6. Capability growth versus authority growth

This is the central boundary law.

An agent may, when permitted by its environment:

- compose existing affordances;
- discover a useful reasoning pattern;
- write a helper/tool using already-granted permissions;
- propose a new Skill;
- discover a recurring team/coordination pattern;
- propose that pattern for reuse.

None of those operations automatically grant new authority.

```text
capability growth
!= authority growth

agent-created abstraction
!= self-granted permission

new tool
!= new credential

new organizational pattern
!= new execution authority

reusable pattern
!= canonical pattern
```

Authority expansion remains governed by existing owner/policy contracts.

## 7. Promotion model

A useful composition can become increasingly durable only through evidence and governance.

### Stage 0 — Ephemeral composition

The active agent combines available primitives/operators for one decision.

No persistence is required.

### Stage 1 — Candidate operator

A repeated reasoning transformation appears reusable.

The candidate remains local/research-level unless explicitly preserved.

### Stage 2 — Candidate packaged capability / Skill

The pattern is named, bounded, given input/output/stop semantics, and tested against real evidence.

Current Skill-maintenance rules remain applicable: structural/high-risk changes can require explicit owner approval.

### Stage 3 — Candidate organizational pattern

Repeated coordination among multiple actors exhibits a stable role/topology pattern that appears useful beyond one episode.

Examples could include a builder/challenger/verifier cell or a research/implementation/verification arrangement.

This stage is a **pattern description**, not a runtime object or permission grant.

### Stage 4 — Institutionalized practice

A coordination or capability pattern becomes part of persistent governance/process only after the appropriate authority ratifies it and the repository records its durable rules, boundaries, and evidence ceiling.

```text
repeated successful coordination
!= automatic canonical promotion
```

## 8. Organizational learning hypothesis

The package records, but does not validate, this future hypothesis:

> A sufficiently capable agent system may improve not only by learning better Skills, but by learning which arrangements of agents, roles, communication links, and verification relationships work for recurring problem classes.

A possible future cycle is:

```text
real work
-> coordination pattern observed
-> evidence preserved
-> repeated usefulness
-> candidate organizational pattern
-> bounded validation
-> authorized reusable template
-> normal use
-> reconciliation / retirement / revision
```

This is a hypothesis for future normal-use evidence.

It does not authorize:

- synthetic swarm experiments;
- a team-template registry;
- an automatic organization compiler;
- an organization critic runtime;
- self-modifying orchestration.

## 9. Institution-like Sensemaking surfaces

Sensemaking already contains persistent governance/continuity mechanisms that are institution-like in function:

- product strategy and ADR authority;
- Four-Level Control Model;
- Policy Hierarchy;
- authority and reserved-decision semantics;
- Campaign state / transitions / handoff;
- provenance and currentness;
- Strategic Frontier and strategic continuity;
- decision reconciliation;
- release and publication boundaries.

The research claim is limited:

> These surfaces provide institution-like continuity for repository decision support.

It does **not** follow that Sensemaking is a general institution engine or that every institution requires these exact mechanisms.

## 10. Required crosswalk questions

The reconciliation artifact must answer:

1. What is the difference between Root Primitive, Cognitive Operator, Capability, and Skill?
2. What turns delegation into Organization?
3. Why is Campaign not Organization?
4. What makes Institution different from a persistent Organization?
5. Which concepts belong to Sensemaking versus the external software-factory/orchestration layer?

It must additionally classify whether any concrete product/runtime gap is exposed.

## 11. Required boundary laws

The following statements must remain explicit in the final package:

```text
research model != product expansion
organization modeled != organization runtime warranted
Campaign != Organization
capability growth != authority growth
agent-created abstraction != self-granted permission
repeated successful coordination != automatic canonical promotion
institution != autonomous agent collective
```

Also preserve existing product laws:

```text
capability available != capability selected
selected != authorized
mechanically valid != semantically correct
worker success != global closure
```

## 12. Files and integration

Create:

- `docs/research/adaptive-agency-abstraction-stack-v0.md`
- `docs/research/adaptive-agency-abstraction-stack-v0-reconciliation.md`
- `docs/adaptive-agency-abstraction-stack-v0-handoff.md`
- `tests/test_adaptive_agency_abstraction_stack_v0.py`

Modify only where required for bounded integration:

- `docs/research/general-agency-model-v0.1.md`
- `skills/using-sensemaking/references/practical-agent-architecture-v0.md`
- `STATUS.md`
- `.github/workflows/validation.yml` — include the focused boundary test in Product Validation
- `.github/workflows/release-candidate.yml` — include the focused boundary test in release-baseline qualification

The workflow edits only make the new documentation contract executable in existing qualification lanes; they add no product/runtime authority.

The new test is representation/boundary assurance only. It must not claim semantic correctness or empirical usefulness.

## 13. Validation

Repository-local verification should establish:

- the research model contains the three planes and promotion ladder;
- Campaign/Organization non-identity is explicit;
- capability/authority separation is explicit;
- General Agency and Practical Agent Architecture point to the new model without promoting it into runtime authority;
- STATUS records the package as research/reference and returns to `NO_CHANGE / NORMAL_USE`;
- existing policy/control contract tests remain green;
- the focused abstraction-boundary test is exercised by both Product Validation and Release Candidate Distribution.

No synthetic multi-agent experiment is required.

## 14. Non-goals

This package does not authorize or introduce:

- `OrganizationState`, `InstitutionState`, or generic `AgentState`;
- organization/team registry;
- communication-graph schema;
- automatic worker spawning;
- scheduler/queue/retry engine;
- team optimizer;
- organization compiler;
- organization critic service;
- multi-agent voting;
- automatic Skill/team selection;
- new Campaign schema;
- product strategy or ADR 0029 change;
- automatic authority expansion;
- autonomous merge/release/deploy/publication;
- experimental proof of emergent-organization value.

## 15. Claim ceiling and completion disposition

Successful repository qualification establishes only that the conceptual model is internally consistent with the current Sensemaking architecture and that the required boundary statements are mechanically present.

It does not establish:

- emergent organization superiority;
- generality outside the reviewed architecture;
- usefulness of organizational-pattern learning;
- a need for a Sensemaking organization runtime;
- a product-boundary change.

Expected terminal disposition:

```text
RESEARCH_REFERENCE_COMPLETE
RUNTIME_GAP = NO_RUNTIME_GAP_ESTABLISHED
PRODUCT_BOUNDARY_CHANGE = NONE
CURRENT CONSTRUCTION RESPONSIBILITY = NONE
NEXT MODE = NORMAL_USE_VALIDATION
```
