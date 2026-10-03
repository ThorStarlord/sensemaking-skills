# Core Operator Vocabulary v0

**Status:** research/reference model; non-authoritative  
**Date:** 2026-09-22  
**Authority:** research only; not an ADR, product-strategy revision, runtime specification, schema, Skill Contract Manifest field, routing rule, workflow-selection rule, validator requirement, or implementation authorization  
**Current product boundary:** unchanged; ADR 0029 remains authoritative  
**Related research:** [Adaptive Agency Abstraction Stack v0](adaptive-agency-abstraction-stack-v0.md), [General Agency Model v0.1](general-agency-model-v0.1.md), [Sensemaking Control-Model Research Agenda](control-model-research-agenda.md)  
**Coverage audit:** [Core Operator Vocabulary v0 — 51-Skill Crosswalk](core-operator-vocabulary-v0-skill-crosswalk.md)

## 1. Purpose

This document asks:

> What is the smallest useful cognitive/operator vocabulary that can explain the current 51 canonical Skill packages without erasing their situated responsibilities, evidence rules, authority boundaries, artifact contracts, or stopping conditions?

The result is a **descriptive compression hypothesis**, not a new execution model.

The candidate kernel is:

~~~text
OBSERVE
FRAME
DECOMPOSE
MODEL
GENERATE
COMPARE
EVALUATE
VERIFY
SELECT
RECONCILE
COMMUNICATE
COORDINATE
~~~

The companion 51-Skill crosswalk found that all current canonical Skills can be described naturally using this vocabulary without requiring a thirteenth operator.

That result means only:

> The twelve terms are currently sufficient as explanatory vocabulary for the checked Skill set.

It does **not** establish that the vocabulary is universally complete, cognitively fundamental, objectively minimal, suitable for automatic routing, or required in Skill contracts.

## 2. Placement in the existing abstraction stack

Adaptive Agency Abstraction Stack v0 currently distinguishes:

~~~text
Root Primitive
      |
      v
Cognitive Operator
      |
      v
Capability / Skill
~~~

This document refines only the middle explanatory vocabulary.

It does not replace that model.

A useful descriptive expansion is:

~~~text
Root Primitive
      |
      v
Core Cognitive Operator
      |
      v
Capability Pattern
      |
      v
Situated Skill
~~~

where:

- **Root Primitive** is an environment/runtime affordance such as read, write, execute, communicate, tool/model call, or delegation;
- **Core Cognitive Operator** is a reusable reasoning transformation;
- **Capability Pattern** is a recurring composition of operators that explains a family of responsibilities;
- **Situated Skill** is a packaged capability specialized by domain, responsibility, evidence semantics, artifact contracts, authority, effects, and stopping rules.

Situated Skill is research vocabulary in this document. It is not a new schema type or release-contract category.

~~~text
Skill package
!= ontological claim that every packaged Skill is the same semantic kind

shared operators
!= interchangeable responsibilities

operator available
!= capability warranted
!= action authorized
~~~

## 3. The twelve operators

### 3.1 OBSERVE

Acquire decision-relevant information from an authorized surface.

Typical forms:

- inspect repository state;
- retrieve supplied evidence;
- read source material;
- measure an observed result;
- inventory artifacts or claims.

~~~text
OBSERVE
!= evidence is sufficient
!= interpretation is correct
!= authority to act
~~~

### 3.2 FRAME

Establish the question, target, scope, decision, or consequential uncertainty that governs the current reasoning.

Typical forms:

- define the problem under pressure;
- bind the target repository/segment/change;
- identify the decision being supported;
- set an evidence/currentness boundary;
- establish what is and is not in scope.

~~~text
FRAME
!= solve
!= select
~~~

### 3.3 DECOMPOSE

Break a whole into decision-relevant parts while preserving the relationship to the source whole.

Typical forms:

- split requirements into stories;
- separate claims, risks, assumptions, or affected surfaces;
- identify subproblems;
- refine a broad object into smaller work units.

~~~text
DECOMPOSE
!= independently authorize the parts
!= imply that every part deserves separate execution
~~~

### 3.4 MODEL

Construct a coherent representation from observations, assumptions, constraints, or prior artifacts.

Typical forms:

- synthesize evidence into a persona;
- build a journey, strategy, roadmap, or architectural representation;
- structure claims into a durable artifact;
- represent relationships among responsibilities, capabilities, or outcomes.

~~~text
MODEL
!= observed truth
!= ratified decision
~~~

### 3.5 GENERATE

Produce materially distinct candidate explanations, hypotheses, options, paths, failure modes, or interventions that were not already supplied as fixed inputs.

Typical forms:

- generate hypotheses;
- explore alternative repository paths;
- imagine pre-mortem failures;
- propose solution candidates.

For this compressed vocabulary, General Agency's alternative-generation aspect of exploration is represented by GENERATE. Iterative Exploration Policy remains a separate control policy that allocates search and is not replaced by this term.

~~~text
GENERATE
!= warrant
!= selection
~~~

### 3.6 COMPARE

Relate two or more states, options, claims, or representations across decision-relevant dimensions.

Typical forms:

- compare competitors;
- diff prior and current repository state;
- compare strategic paths;
- compare a work claim with evidence;
- contrast candidate metrics or pricing models.

~~~text
COMPARE
!= EVALUATE
!= SELECT
~~~

Comparison may remain descriptive.

### 3.7 EVALUATE

Judge significance, sufficiency, fit, consequence, risk, plausibility, or decision relevance.

Typical forms:

- assess evidence strength;
- evaluate strategic fit;
- judge practical significance;
- assess readiness;
- challenge whether a path addresses the real problem.

~~~text
EVALUATE
!= SELECT automatically
!= authority
~~~

This separation is essential for owner-reserved and Level-4 decisions.

### 3.8 VERIFY

Test a bounded claim, condition, result, or closure criterion against evidence.

Typical forms:

- verify a repair closed a prior finding;
- verify an experiment result from supplied observations;
- verify a readiness condition;
- verify a work claim against durable repository evidence.

~~~text
VERIFY
!= universal semantic truth
!= RECONCILE
~~~

Verification answers whether a bounded claim is supported within the checked scope. It does not by itself determine what the prior strategic or responsibility model should now become.

### 3.9 SELECT

Choose one candidate, responsibility, path, recommendation, or next control move when semantic warrant and authority allow selection.

Typical forms:

- prioritize an initiative;
- select a proposed North Star Metric;
- choose the warranted next responsibility;
- choose among eligible workflow compositions.

~~~text
capability to SELECT
!= permission to SELECT in every situated Skill

evaluation complete
!= selection authorized
~~~

A Skill such as owner-decision-capsule may compare and evaluate options precisely because SELECT is reserved for the owner.

### 3.10 RECONCILE

Update the meaning or disposition of a prior model, claim set, responsibility, path, or closure state using returned evidence.

Typical forms:

- confirm/revise/retract prior strategic claims;
- determine whether a repaired finding remains open;
- align documentation/contracts with current implementation;
- update continuation or closure implications after evidence returns.

~~~text
VERIFY
answers: did the bounded claim hold?

RECONCILE
answers: what changes about the prior model because of the returned evidence?
~~~

### 3.11 COMMUNICATE

Adapt evidence, state, decisions, uncertainty, or outcomes into an audience-facing representation without silently changing their status.

Typical forms:

- stakeholder updates;
- release notes;
- competitive talk tracks;
- evidence packets.

~~~text
COMMUNICATE
!= publish authority
!= COORDINATE
~~~

### 3.12 COORDINATE

Connect capabilities, stages, artifacts, or actors while preserving responsibility, context, and authority boundaries.

Typical forms:

- handoff between Skills;
- recommend a workflow composition;
- resume a strategic episode at the correct semantic boundary;
- return delegated evidence to the controlling agent.

~~~text
COORDINATE
!= choose the work without semantic warrant
!= scheduler/runtime necessarily
!= authority expansion
~~~

## 4. Terms deliberately not promoted to core operators

The vocabulary stays useful only if it does not create a synonym for every familiar activity.

### Synthesize

Usually:

~~~text
OBSERVE + MODEL
~~~

### Classify

Usually:

~~~text
OBSERVE/COMPARE + MODEL
~~~

with a supplied or situated classification scheme.

### Challenge

Usually:

~~~text
GENERATE counterexamples
+ COMPARE
+ EVALUATE
~~~

The repository may continue to use CHALLENGE as a useful policy/control move. It does not need to become an additional core capability-composition operator in this compressed vocabulary.

### Forecast / simulate

Usually:

~~~text
MODEL
+ EVALUATE under explicit assumptions
~~~

### Plan

Usually:

~~~text
FRAME
+ GENERATE
+ COMPARE
+ EVALUATE
+ SELECT
+ MODEL a future sequence
~~~

Planning is therefore treated as a recurring capability pattern, not a root operator.

### Specify

Usually:

~~~text
DECOMPOSE + MODEL
~~~

### Measure

Usually:

~~~text
OBSERVE
+ VERIFY and/or EVALUATE
~~~

### Stop / escalate / authorize / ratify / mutate

These are intentionally outside the cognitive-operator vocabulary.

- **STOP** is a control-policy disposition;
- **ESCALATE** is a governance/control transition;
- **AUTHORIZE** and **RATIFY** are authority acts;
- **MUTATE** is an execution/effect class.

They constrain or act upon operator use; they are not interchangeable with cognitive transformations.

## 5. Recurring capability patterns

The following families are descriptive compositions, not canonical runtime types.

### 5.1 Diagnosis

~~~text
OBSERVE
+ FRAME
+ MODEL
+ EVALUATE
~~~

Typical question:

> What is going on here, what matters, and where is the consequential weakness or structure?

Examples include repo-sensemaker, problem-framer, customer-modeling Skills, and portions of market/product analysis.

### 5.2 Decision-focused inquiry

~~~text
FRAME
+ GENERATE
+ EVALUATE
+ VERIFY
~~~

Typical question:

> What uncertainty matters, what could explain it, and what evidence would change the decision?

Examples include unknowns-mapper, discovery, hypothesis, experiment-design, and ab-test-analysis.

### 5.3 Evidence-grounded comparative judgment

~~~text
MODEL
+ COMPARE
+ EVALUATE
+ optional SELECT
~~~

Typical question:

> How do these alternatives differ, what matters, and—only when authorized—which should be preferred?

Examples include architectural-review, competitive-analysis, pricing, prioritize, north-star, and strategic repository analysis.

### 5.4 Specification refinement

~~~text
FRAME
+ DECOMPOSE
+ MODEL
~~~

Typical question:

> How should a broad intention be transformed into a more explicit and actionable representation while preserving traceability?

Examples include to-prd, user-stories, acceptance-criteria, and to-issues.

### 5.5 Planning / construction-path formation

~~~text
FRAME
+ GENERATE
+ COMPARE
+ EVALUATE
+ SELECT where authorized
+ MODEL sequence/path
~~~

Examples include strategy, roadmap, gtm, workflow-planner, and portions of strategic repository analysis.

### 5.6 Bounded verification

~~~text
OBSERVE
+ COMPARE
+ VERIFY
~~~

Examples include repair-verifier, readiness checks, measured experiment analysis, and portions of output-reconciler.

### 5.7 Evidence reconciliation

~~~text
bounded returned evidence
+ COMPARE with prior model
+ EVALUATE consequence
+ RECONCILE
~~~

Examples include output-reconciler, repair-verifier, sensemaking-docs-reconciler, and strategic-repository-reconciliation.

Communication and coordination remain cross-cutting operator families rather than being forced into these seven capability patterns.

## 6. What preserves situated responsibility

Operator composition alone is intentionally insufficient to define a Skill.

A situated Skill remains distinguished by at least:

1. **responsibility** — what bounded job it is serving;
2. **domain/problem space** — where its semantics apply;
3. **evidence contract** — what may count as observed, derived, inferred, hypothesized, ratified, unresolved, or insufficient;
4. **artifact contract** — what durable representation it produces or consumes;
5. **authority posture** — what may be recommended, selected, executed, ratified, or must remain reserved;
6. **effect boundary** — read-only analysis, repository mutation, or external action;
7. **control scope** — local, workflow, episode, Level 3, Level 4, or an explicit boundary between them;
8. **stopping conditions** — when the Skill must return, fail closed, escalate, or stop.

Therefore:

~~~text
same operator composition
!= same Skill

shared capability ancestry
!= merge candidate automatically
~~~

## 7. Governance remains orthogonal

The twelve operators answer:

> What reasoning transformation is being performed?

Governance answers:

> Under what authority, evidence, effect, and control boundary may that transformation occur?

A compact descriptive authority vocabulary is:

~~~text
ADVISE
SELECT_WITHIN_DELEGATION
EXECUTE_WITHIN_AUTHORITY
OWNER_RESERVED
LEVEL4_RESERVED
EXTERNAL_RESERVED
~~~

A compact effect vocabulary is:

~~~text
READ_ONLY
REPOSITORY_MUTATION
EXTERNAL_ACTION
~~~

A compact control-scope vocabulary is:

~~~text
LOCAL
WORKFLOW
EPISODE
LEVEL_3
LEVEL_4
~~~

These vocabularies are descriptive in this research document. They do not modify current Campaign authority semantics, Skill manifests, policies, or release contracts.

Example:

~~~text
owner-decision-capsule

operators:
  FRAME
  MODEL
  COMPARE
  EVALUATE
  COMMUNICATE

authority:
  OWNER_RESERVED

effect:
  READ_ONLY

critical boundary:
  SELECT is intentionally not performed
~~~

The same operator vocabulary can therefore explain similar cognitive structure without erasing different authority regimes.

## 8. Coordination remains orthogonal

Three current packaged Skills demonstrate increasing coordination scale:

~~~text
handoff
  -> local transfer

workflow-planner
  -> bounded workflow composition recommendation

strategic-sensemaking-loop
  -> episode-level resume/composition/control surface
~~~

All may use COORDINATE, but they remain distinct because their responsibility, scope, artifact semantics, and authority differ.

This document does not introduce:

- a scheduler;
- worker topology;
- automatic capability chaining;
- a planner;
- deterministic Skill selection.

## 9. Representation remains orthogonal

Current Semantic Architecture concepts such as:

~~~text
Observation
Evidence
Claim
EpistemicStatus
Uncertainty
Responsibility
Decision
Authority
Artifact
~~~

are not operators.

They are representations that operators may read, transform, compare, verify, reconcile, or communicate.

Therefore:

~~~text
operator vocabulary
!= semantic ontology replacement
~~~

The existing Semantic Architecture remains authoritative for its declared concepts and contract boundaries.

## 10. Coverage result

The companion audit checked all 51 canonical Skill packages currently on main.

Result:

~~~text
51 / 51 Skills naturally describable with the twelve operators
0 Skills requiring a thirteenth operator for explanatory coverage
0 recommendation to merge Skills based only on shared operators
0 manifest/schema/runtime/routing changes warranted by the audit
~~~

The result supports a bounded research claim:

> A relatively small operator vocabulary can explain substantial reuse beneath the current Skill catalog while the actual Skill identities remain justified by situated responsibility and governance boundaries.

It does not support:

~~~text
twelve operators = universal cognitive basis
twelve operators = objective mathematical minimum
operator overlap = redundant Skills
operator metadata = automatic routing input
operator coverage = semantic quality
~~~

## 11. Productization boundary

Do **not** add operators fields to Skill Contract Manifests merely because this map exists.

Do **not**:

- reorganize the Skill tree by operator;
- create one Skill per operator;
- merge Skills because they share an operator composition;
- add deterministic routing from operator metadata;
- add operator coverage to release gates;
- add a new runtime/controller;
- replace current Policy Hierarchy or General Agency vocabulary with this compression;
- treat this document as product authority.

The current Skill Contract Manifest boundary remains correct: deterministic shell metadata may describe identity, domain, responsibility, artifacts, shared semantic concepts, and repository mutation without claiming semantic routing authority.

## 12. Reopen conditions

Reconsider deeper productization only if normal use produces one or more repeated decision-changing pressures such as:

1. multiple current Skills cannot be described naturally without repeatedly inventing the same missing operator;
2. Skill authors repeatedly implement incompatible meanings for the same recurring cognitive transformation;
3. duplicated cross-Skill instruction burden causes observable maintenance defects or behavior drift;
4. agents repeatedly fail to discover or understand relevant capabilities because the current Skill/domain/responsibility surfaces are insufficient;
5. a shared Capability contract would remove demonstrated duplicated logic while preserving situated evidence and authority semantics;
6. a real use case requires operator/capability inspection for explanation or tooling and cannot be served by a read-only research projection;
7. current Skill identities repeatedly obscure meaningful capability ancestry in a way that changes engineering decisions.

Even then:

~~~text
repeated explanatory usefulness
!= automatic runtime formalization

shared operator
!= shared authority

operator metadata
!= automatic Skill selection
~~~

## 13. Current disposition

~~~text
Core Operator Vocabulary v0:
  RESEARCH_REFERENCE

operator set:
  12

51-Skill explanatory coverage:
  COMPLETE_FOR_CURRENT_CANONICAL_SET

new Skill identities:
  NONE

manifest changes:
  NONE

registry changes:
  NONE

runtime changes:
  NONE

routing authority changes:
  NONE

folder reorganization:
  NONE

current product boundary:
  UNCHANGED
~~~

The smallest useful current model is therefore:

~~~text
Root Primitives
      |
      v
12 Core Cognitive Operators
      |
      v
Recurring Capability Patterns
      |
      v
Situated Skills
~~~

with governance, coordination, and representation remaining orthogonal rather than being collapsed into the same hierarchy.
