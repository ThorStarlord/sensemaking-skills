# Adaptive Agency Abstraction Stack v0

**Status:** research/reference model; non-authoritative  
**Date:** 2026-09-21  
**Tracker:** Issue #444  
**Authority:** research only; not an ADR, product-strategy revision, runtime specification, schema, Skill contract, routing rule, worker-allocation policy, or implementation authorization  
**Current product boundary:** unchanged; ADR 0029 remains authoritative  
**Design:** ../superpowers/specs/2026-09-21-adaptive-agency-abstraction-stack-v0-design.md

## 1. Purpose

This document refines the pedagogical ladder:

~~~text
Primitive
-> Operator
-> Skill
-> Organization
-> Institution
~~~

into a more precise account of how reusable intelligence can be composed, coordinated, and preserved.

The central conclusion is:

> The five terms are useful together, but they do not form one literal implementation hierarchy.

The first three primarily describe **capability composition**. Organization primarily describes **coordination among multiple actors**. Institution primarily describes **persistent governance, continuity, and authority across actors and time**.

The model therefore has two parts:

1. a three-plane structural model; and
2. a separate promotion/evolution ladder.

## 2. Core non-identities

~~~text
research model != product expansion
organization modeled != organization runtime warranted
Campaign != Organization
capability growth != authority growth
agent-created abstraction != self-granted permission
repeated successful coordination != automatic canonical promotion
institution != autonomous agent collective
~~~

Existing Sensemaking laws also remain in force:

~~~text
capability available != capability selected
selected != authorized
mechanically valid != semantically correct
worker success != global closure
~~~

## 3. Structural model

### 3.1 Capability Plane

The Capability Plane describes increasingly reusable ways an agent can act or reason.

~~~text
Root Primitive
      |
      v
Cognitive Operator
      |
      v
Capability / Skill
~~~

This is a composition relation, not a mandatory runtime stack.

A Skill may call tools directly, compose several operators, or remain mostly methodological. A Cognitive Operator may be used transiently without becoming a Skill.

### 3.2 Coordination Plane

The Coordination Plane describes how multiple agents or actors arrange work.

~~~text
single actor
   |
delegation
   |
team / cell / peer relationship
   |
Organization
~~~

The defining feature is not actor count alone. It is that role allocation, communication structure, specialization, or coordination relationships materially affect how the objective is pursued.

### 3.3 Governance / Persistence Plane

The Governance / Persistence Plane describes structures that survive individual actions or actors.

~~~text
rules / norms
     |
policy / authority
     |
provenance / precedent / continuity
     |
Institution
~~~

An Institution is not simply an Organization with more members. It is a persistent governance structure that can preserve commitments, roles, authority boundaries, decision procedures, and knowledge across participant replacement.

## 4. Root Primitive

A **Root Primitive** is an affordance supplied by the governed environment/runtime that an agent may invoke without reconstructing its lower-level implementation at that moment.

Examples may include:

- read;
- write;
- execute;
- communicate;
- call a model or tool;
- delegate or spawn when the harness exposes that affordance.

The term is deliberately qualified as Root Primitive because the repository already uses “primitive” for several local mechanical or lifecycle operations.

Root Primitive is relative to the agent-facing abstraction boundary. A filesystem read may be primitive to an agent while being implemented by many lower-level operating-system operations.

~~~text
root primitive available
!= primitive warranted for current work
!= authority to use primitive for any purpose
~~~

Sensemaking does not need to own or catalog every Root Primitive. Most are supplied by the surrounding harness, operating environment, connected services, or software factory.

## 5. Cognitive Operator

A **Cognitive Operator** is a reusable reasoning transformation that can act at multiple stages of agency.

General Agency Model v0.1 already identifies examples such as:

- adversarial challenge;
- exploration / alternative generation;
- causal reasoning;
- counterfactual reasoning;
- decomposition;
- comparison;
- simulation / forecasting.

A Cognitive Operator is usually lighter than a Skill.

For example:

~~~text
decomposition
= Cognitive Operator

repo-sensemaker
= Skill that may use decomposition, comparison, evidence evaluation,
  domain knowledge, artifact rules, and stopping conditions
~~~

Use the qualified phrase Cognitive Operator rather than naked Operator because the repository also uses operator terminology for human/operational concerns.

A bounded descendant research projection now tests whether the current canonical Skill set can be explained with a smaller shared operator vocabulary without turning those operators into routing metadata or runtime authority. See [Core Operator Vocabulary v0](core-operator-vocabulary-v0.md) and its [51-Skill Crosswalk](core-operator-vocabulary-v0-skill-crosswalk.md).

That projection is intentionally subordinate to this abstraction stack:

~~~text
operator vocabulary
!= Skill Contract Manifest extension
!= automatic Skill selection
!= replacement for General Agency / Policy Hierarchy vocabulary
~~~

## 6. Capability and Skill

A **Capability** is an available bounded means of performing some responsibility.

A **Skill** is one important packaged capability form.

A Skill may combine:

- one or more Cognitive Operators;
- domain knowledge;
- tools;
- evidence rules;
- artifact contracts;
- method steps;
- boundary guards;
- stopping conditions;
- validation expectations.

~~~text
Cognitive Operator
!= Skill

Skill
is-a kind of Capability

Capability available
!= capability selected
!= capability authorized
~~~

This model does not replace the existing Campaign Capability model or Skill Contract Manifest model.

It explains their place in a wider capability-composition picture.

## 7. What turns delegation into Organization?

Delegation is necessary for many multi-agent organizations, but delegation alone is not enough.

A bounded relationship such as:

~~~text
Parent
  |
  +-> Worker: verify one claim
~~~

may remain ordinary delegation.

Organizational behavior appears when multi-actor relationships themselves become materially important to work decomposition or execution.

Signals include:

- role specialization;
- peer-to-peer communication;
- multiple workers sharing or handing off subproblems;
- persistent or dynamically reassigned responsibilities;
- coordination rules;
- reusable team/cell structures;
- topology that changes because the problem changes;
- an actor coordinating other actors rather than merely returning a result to one parent.

For example:

~~~text
                 Parent
             /      |      \
        Builder   Critic   Verifier
            \       |       /
             \---- evidence
~~~

can be an organizational pattern when those relationships are material to the method rather than three unrelated tool calls.

Therefore:

~~~text
delegation
!= Organization automatically

many agents
!= Organization automatically

Organization
= material multi-actor coordination structure
~~~

## 8. Campaign is not Organization

Campaign and Organization answer different questions.

Campaign answers:

> What consequential responsibility is live, why does the work exist, what decision is blocked, what evidence and authority constrain it, and how can continuation be reconstructed?

Organization answers:

> How are multiple intelligent actors arranged and coordinated to pursue the work?

Therefore:

~~~text
Campaign != Organization
Campaign durability != organizational persistence
execution handoff != organizational topology
worker result != organizational governance
~~~

A Campaign can be executed by a single agent.

An Organization can execute work that is not represented as a Sensemaking Campaign.

An Organization may operate inside a Campaign without the Campaign schema needing to model team topology.

## 9. Institution

An **Institution** is a persistent system of purpose, roles/rules, authority, decision procedures, memory/provenance, norms, and continuity that can survive replacement of individual participants.

A useful test is:

> If the current agents disappeared and new agents entered, what durable structures would allow the new actors to reconstruct what matters, what they may do, which commitments remain binding, what evidence exists, and how decisions are ratified?

Institution-like mechanisms can include:

- governing purpose;
- authority boundaries;
- explicit policies;
- precedent and decision history;
- durable evidence and provenance;
- role definitions;
- ratification procedures;
- continuity/currentness checks;
- escalation and reserved-decision rules.

Institution is not synonymous with a large or persistent Organization.

~~~text
persistent Organization
= stable coordinated actors/roles over time

Institution
= durable governance/continuity that can constrain or outlive particular actors
~~~

The two may overlap.

## 10. Sensemaking as institution-like control infrastructure

Current Sensemaking already contains several institution-like control surfaces:

- product strategy;
- ADRs;
- Four-Level Control Model;
- Policy Hierarchy;
- Campaign responsibility/authority/evidence state;
- handoff and continuation;
- provenance/currentness;
- Strategic Frontier and Strategic Continuity;
- reconciliation;
- release/publication authority boundaries.

These mechanisms can preserve decision context across fresh agents and enforce distinctions among recommendation, selection, authorization, execution, and ratification.

The bounded claim is:

> Sensemaking provides institution-like continuity for repository decision support.

This does not establish:

~~~text
Sensemaking = universal institution engine
Sensemaking = autonomous agent collective
institution-like continuity = organizational runtime
~~~

## 11. Placement in General Agency

Organization is best treated as a possible consequence of decomposition and metareasoning when:

- multiple actors are available;
- decomposition produces separable or specialized responsibilities;
- communication among those actors can improve outcomes;
- the coordination cost is justified.

Organization is not a mandatory lifecycle node.

The General Agency lifecycle can remain valid for:

- one agent;
- one agent using tools;
- one parent delegating bounded work;
- a multi-agent organization.

Institution belongs primarily in the governance/persistence envelope rather than after Action as another sequential stage.

## 12. Placement in Practical Agent Architecture

Practical Agent Architecture v0 already gives the parent semantic controller ownership of:

- current decision frame;
- warrant target;
- delegation purpose;
- integration of returned evidence;
- final semantic reassessment.

It allows workers to receive bounded responsibilities and return evidence.

Adaptive Agency Abstraction Stack v0 adds only the interpretive distinction:

~~~text
bounded delegation
-> may stay a parent/worker relation

material adaptive roles/topology/peer coordination
-> organizational behavior
~~~

All existing authority rules survive.

~~~text
organization pattern != execution authority
organization role != permission grant
subagent capability != delegated authority expansion
~~~

## 13. Where Organization belongs operationally

Under current ADR 0029, dynamic organization formation belongs primarily to the external harness / software-factory / orchestration environment.

That environment may provide:

- worker creation;
- scheduling;
- queues;
- retries;
- role assignment;
- communication channels;
- parallel execution;
- topology changes.

Sensemaking-informed control can provide:

- current decision;
- warranted responsibility;
- authority boundary;
- evidence requirements;
- success/stop conditions;
- reassessment after returned evidence.

The boundary remains:

~~~text
Sensemaking
-> supports what work is warranted and under what authority

external orchestration
-> coordinates already-selected work

workers / organizations
-> return evidence

semantic controller
-> reassesses
~~~

## 14. Capability growth versus authority growth

A capable agent may discover useful abstractions.

Within granted authority it may be able to:

- compose existing tools;
- define an ephemeral procedure;
- write a helper tool using existing permissions;
- identify a recurring Cognitive Operator;
- propose a new Skill;
- discover a recurring organizational pattern;
- propose that pattern for reuse.

None of those operations grant new authority.

~~~text
capability growth != authority growth
agent-created abstraction != self-granted permission
new tool != new credential
new Skill != automatic selection
new organizational pattern != new execution authority
~~~

Authority expansion remains governed separately by the owner, policy, or another legitimate authority surface.

## 15. Promotion / Evolution Ladder

The structural planes describe what a thing is.

The **Promotion / Evolution Ladder** describes how useful behavior can become progressively reusable and durable.

### 15.1 Ephemeral composition

One agent combines available primitives/operators for one decision.

No persistence is required.

### 15.2 Candidate reusable operator

A reasoning transformation recurs often enough to be named or preserved.

Its recurrence does not by itself establish generality.

### 15.3 Packaged capability / Skill

A recurring method receives:

- a clear responsibility;
- inputs;
- outputs;
- boundary guards;
- stopping conditions;
- qualification/validation where appropriate.

It becomes a candidate reusable capability.

### 15.4 Repeatable coordination pattern

Multiple actors repeatedly exhibit a useful arrangement of:

- roles;
- communication;
- delegation;
- review;
- verification;
- decomposition.

The pattern may be documented as a candidate organizational pattern.

### 15.5 Institutionalized practice

A pattern becomes part of durable governance/process only when the appropriate authority ratifies it and its boundaries, evidence ceiling, maintenance expectations, and retirement/revision conditions are preserved.

~~~text
repeated successful coordination
!= automatic canonical promotion
~~~

## 16. Organizational learning hypothesis

This model records a future research hypothesis:

> Agent systems may improve not only by learning better capabilities, but by learning which arrangements of roles, agents, communication links, challenge relations, and verification structures work for recurring problem classes.

A possible evidence-driven lifecycle is:

~~~text
real work
-> coordination pattern observed
-> evidence preserved
-> repeated usefulness
-> candidate organizational pattern
-> bounded validation
-> authorized reusable pattern
-> normal use
-> reconciliation / revision / retirement
~~~

This package does not establish that such learning is useful.

It does not authorize synthetic swarm experiments merely to demonstrate the concept.

## 17. Why this is not one literal ladder

The original ladder mixes different questions.

### Capability question

> What reusable thing can the agent do?

~~~text
Root Primitive
-> Cognitive Operator
-> Capability / Skill
~~~

### Coordination question

> How are multiple actors arranged?

~~~text
single agent
-> delegation
-> team/cell
-> Organization
~~~

### Governance question

> What persists and constrains actors over time?

~~~text
rule
-> policy
-> authority/precedent/continuity
-> Institution
~~~

These dimensions can combine in many ways.

A sophisticated Skill can be used by one agent with no Organization.

A large Organization can use only simple Skills.

An Institution can govern many Organizations.

A temporary Organization can exist with minimal institutional persistence.

## 18. Five direct answers

### 18.1 Root Primitive vs Cognitive Operator vs Capability vs Skill

- Root Primitive: environment-supplied affordance.
- Cognitive Operator: reusable reasoning transformation.
- Capability: available bounded means of performing work.
- Skill: packaged named capability that may compose operators, tools, domain knowledge, and contracts.

### 18.2 What turns delegation into Organization?

Delegation becomes organizational when multi-actor role allocation, communication topology, specialization, or coordination relationships materially shape how the objective is pursued.

### 18.3 Why is Campaign not Organization?

Campaign is durable decision/responsibility state. Organization is actor-coordination structure. Either can exist without the other.

### 18.4 What makes Institution different from persistent Organization?

A persistent Organization preserves coordinated roles/actors. An Institution preserves governance, authority, rules, precedent, memory, and continuity that can survive actor replacement and constrain multiple organizations.

### 18.5 What belongs to Sensemaking versus external orchestration?

Sensemaking currently owns/supports decision, warrant, evidence, authority, continuity, capability inspection, handoff/result boundaries, and reconciliation. External orchestration owns worker allocation, scheduling, communication topology, dynamic team formation, and execution mechanics unless a future Level-4 decision changes the product boundary.

## 19. Reopen conditions

Revisit the model or product boundary only if ordinary use produces concrete pressure such as:

- repeated multi-agent work where parent/worker semantics cannot reconstruct consequential coordination;
- recurring coordination failures that materially change responsibility or authority;
- repeated successful team/cell patterns whose reuse cannot be represented safely outside Sensemaking;
- an explicit owner decision to make organizational control part of the product;
- evidence that Campaign/Execution Interface boundaries are insufficient because organizational state itself becomes decision-relevant.

Do not reopen from conceptual elegance alone.

## 20. Non-goals

This research model does not authorize or introduce:

- OrganizationState;
- InstitutionState;
- generic AgentState;
- team/role registry;
- communication graph schema;
- automatic worker spawning;
- scheduler/queue/retry engine;
- team optimizer;
- organization compiler;
- organization critic service;
- multi-agent voting;
- automatic Skill or team selection;
- Campaign schema change;
- automatic authority expansion;
- autonomous merge/release/deploy/publication;
- synthetic proof of emergent organization value.

## 21. Evidence ceiling

This model is a conceptual synthesis grounded in the current Sensemaking architecture.

It does not prove:

- the universal validity of the three-plane model;
- that emergent organizations outperform fixed workflows;
- that organizational-pattern learning improves real systems;
- that Sensemaking should implement an organization runtime;
- that institution-like repository mechanisms transfer unchanged to other domains.

Its current role is to sharpen vocabulary, preserve boundaries, and create a coherent place for future evidence.
