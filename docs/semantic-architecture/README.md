# Sensemaking Semantic Architecture

**Status:** Canonical semantic-design foundation v0; Phase 9 operationalization and Phase 10 common-envelope experiment complete; first bounded Phase 15 conformance rule qualified  
**Scope:** Repository reasoning, evidence semantics, work semantics, product-change vocabulary, and evidence-triggered conformance checks  
**Executable status:** Existing Campaign contracts; optional companion `semantic_reasoning_profile` Level-3 representation; bounded Skill-registry liveness conformance. Other ontology concepts remain documentation unless explicitly mapped to executable machinery.

## Purpose

Sensemaking needs a shared semantic model so different Skills can reason about repositories with the same meanings for repository structure, evidence, claims, uncertainty, responsibility, capability, authority, change, and validation.

This directory defines that shared model without moving semantic control out of the active agent.

The central design problem is not to describe every software concept. It is to define the **minimal-but-sufficient semantic model needed to reason reliably about an unfamiliar repository, preserve the provenance of that reasoning, and state the limits of what has actually been established**.

## Canonical hierarchy

```text
Sensemaking Semantic Architecture
|
+-- Semantic Model
|   +-- Foundational concepts
|   +-- Repository ontology
|   +-- Software-architecture ontology
|   +-- Evidence and epistemic ontology
|   +-- Engineering-work ontology
|   +-- Product ontology
|       +-- Product-change taxonomy
|
+-- Reasoning Model
|   +-- observation -> evidence
|   +-- evidence -> claim
|   +-- claim -> uncertainty
|   +-- uncertainty -> responsibility
|   +-- responsibility -> capability
|   +-- result -> decision
|
+-- Capability / Skill Layer
|   +-- repo-sensemaker
|   +-- architectural-review
|   +-- repair-verifier / output-reconciler
|   +-- domain Skills
|
+-- Executable Substrate
    +-- probes
    +-- artifacts / validators
    +-- bounded conformance checks
    +-- Campaigns / provenance
    +-- handoff
```

The Capability / Skill Layer is explicit because operationalizing the Reasoning Model happens first through bounded Skill methodology, not through a central reasoning engine.

## Document map

| Document | Role |
|---|---|
| [`constitution.md`](constitution.md) | Permanent guardrails for semantic formalization. |
| [`problem-statement.md`](problem-statement.md) | Why a shared semantic architecture is needed and what failure modes it addresses. |
| [`competency-questions.md`](competency-questions.md) | Questions the semantic model must eventually support; primary acceptance tests for ontology scope. |
| [`concept-inventory.md`](concept-inventory.md) | Existing repository vocabulary and its current sources of authority. |
| [`ontology.md`](ontology.md) | Layered ontology of intent, software systems, evidence, knowledge, work, and product concepts. |
| [`product-change-taxonomy.md`](product-change-taxonomy.md) | Descriptive taxonomy for how product changes differ and create value. |
| [`relations-and-epistemics.md`](relations-and-epistemics.md) | Relationship semantics, evidence requirements, epistemic status, and prohibited inference. |
| [`reasoning-model.md`](reasoning-model.md) | Evidence-governed reasoning lifecycle. |
| [`execution-integration.md`](execution-integration.md) | Mapping to probes, Skills, artifacts, validators, Campaigns, and harnesses. |
| [`reference-scenarios.md`](reference-scenarios.md) | Concrete scenarios used to test whether the model is useful. |
| [`implementation-plan.md`](implementation-plan.md) | Phase states and promotion gates from vocabulary to executable contracts. |
| [`pilots/README.md`](pilots/README.md) | Phase 9 Reasoning Model operationalization and cross-Skill comparison. |
| [`common-semantic-contract.md`](common-semantic-contract.md) | Experimental Level-3 `semantic_reasoning_profile` representation contract. |
| [`phase-9-handoff.md`](phase-9-handoff.md) | Phase 9 delivered work and Phase 10 entry boundary. |
| [`phase-10/README.md`](phase-10/README.md) | Preregistered Phase 10 real-repository experiment. |
| [`phase-10/results.md`](phase-10/results.md) | Phase 10 evidence synthesis and Outcome A decision. |
| [`phase-10-handoff.md`](phase-10-handoff.md) | Qualified Phase 10 handoff, evidence, and deferred-phase dispositions. |
| [`phase-15/README.md`](phase-15/README.md) | Bounded Skill-registry liveness conformance pilot. |
| [`phase-15-handoff.md`](phase-15-handoff.md) | Qualification evidence and incremental Phase 15 boundary. |
| [`milestone-handoff.md`](milestone-handoff.md) | Original semantic-foundation milestone handoff. |

## Three levels of formalization

Sensemaking distinguishes three levels. A concept MUST NOT silently cross them.

### Level 1 — Vocabulary

Shared definitions for agents and humans.

Example: `reinforcing product change` is a useful phrase even if no runtime field represents it.

### Level 2 — Ontology

Explicit entities, relationships, constraints, and epistemic meaning.

Example: `ProductChange reinforces ProductCapability` is an ontology relation once repeated reasoning needs that distinction.

### Level 3 — Executable semantic contract

Schema fields, validators, deterministic probes, registries, or bounded conformance invariants that encode only a mechanically decidable subset of semantics.

A Level-3 validator can answer `is this representation or declared relation mechanically consistent?`; it does not automatically answer `is this semantic conclusion true?`.

Phase 9 produced the first new bounded example: `semantic_reasoning_profile` v1 has an executable standalone validator for representation shape, evidence-reference requirements, currentness status, IDs, and epistemic enums. It is **not** registered into Campaign admission and explicitly cannot establish semantic truth.

Phase 10 retained that contract but rejected mandatory embedding based on observed duplication pressure. Retention of a Level-3 companion contract is not promotion into the control plane.

The first Phase 15 pilot added a second kind of Level-3 behavior: a narrow conformance rule that compares explicit Skill-registry liveness claims with canonical Skill-tree existence. It validates consistency only and likewise emits `semantic_truth_established: false`.

## Phase 9 result — Reasoning Model operationalization

The first contrasting pilots covered:

```text
repo-sensemaker
    direct diagnosis / currentness

architectural-review
    inherited evidence / architecture judgment

repair-verifier + output-reconciler
    post-change verification / reconciliation
```

Across all three, the stable common core was:

```text
target/currentness
observations or inherited observations
material claims
epistemic status
evidence references
bounded scope / claim limits
uncertainty
explicit limits / non-claims
```

Skill-specific semantics such as fog/weakness taxonomies, `Component`/`Layer`/`Boundary`, architectural decision enums, repair `closed/remaining`, and reconciliation `verified/disputed/omitted` remain local rather than being flattened into the common contract.

## Phase 10 result — keep the common profile companion-level

Phase 10 tested the same profile in three additional real-repository reasoning episodes:

```text
Chess Mentor Engine
    repo-sensemaker / direct diagnosis

React incremental game
    output-reconciler / immutable snapshot + live PR currentness

ViralFactory
    PM pre-mortem / canonical risk_analysis + companion profile
```

The result is **Outcome A**:

> Keep `semantic_reasoning_profile` as an optional companion audit/reconstruction artifact.

The strongest positive evidence came from currentness-sensitive reconciliation: an immutable exact-SHA handoff and mutable live PR metadata must not be silently collapsed into one current-state claim.

The strongest negative embedding evidence came from PM `risk_analysis`: the domain artifact already represents evidence status, evidence refs, uncertainty, mitigation, recommendation boundaries, and unresolved questions. Copying the whole common profile into that schema would create duplicate canonical representation.

Therefore the profile is useful primarily when reasoning crosses artifacts, evidence surfaces, Skills, domains, or fresh contexts. It is not a required envelope for every analytical artifact.

## Phase 15 first result — trigger-driven liveness conformance

After Phase 10 closed, the next-phase audit found no demonstrated trigger for Phases 11–14, but repeated maintenance work had exposed one narrow conformance defect class: compatibility Skill-registry liveness notes could lag the canonical Skill tree.

PR #325 qualified `scripts/validate-skill-registry-liveness.py` and its rejection suite. The checker can reject:

```text
status: proposed while skills/<id>/SKILL.md exists
an explicit no-current-implementation note while that SKILL.md exists
a wrong current-canonical skills/<id>/ reference
a broken current-canonical skills/<id>/ reference
duplicate registry Skill IDs
```

It intentionally accepts a historical `status: deprecated` entry when the note correctly distinguishes old invocation metadata from a current canonical Skill implementation.

This pilot establishes a bounded consistency relation, not semantic Skill truth, qualification, or native-harness support.

Phase 15 is now **incremental / trigger-driven**: one rule is qualified; later rules require their own observed defect and qualification evidence.

## Reasoning and conformance maturity

```text
Reasoning Model specified                  yes
first cross-Skill adoption                 yes
cross-domain companion experiment          yes
optional companion profile                 retained
mandatory artifact embedding               not warranted
first bounded conformance drift rule        qualified
broad semantic linter                       not warranted
central reasoning engine                    no / not warranted
Campaign-schema semantic promotion          deferred
Repository Semantic Map                     deferred
```

## Authority boundary

The semantic architecture preserves the Campaign control boundary:

```text
Agent owns:
- semantic interpretation;
- consequential uncertainty selection;
- warranted responsibility selection;
- semantic capability selection;
- judgment about whether evidence justifies a conclusion.

Deterministic machinery owns:
- repository identity and mechanically observable state;
- structural validation;
- persistence and integrity;
- exact-byte provenance;
- declared capability metadata;
- bounded consistency checks over explicit contracts;
- authority metadata checks;
- reconstructible transition history;
- validation of explicitly promoted mechanical semantic representations.
```

Therefore:

```text
observation != interpretation
artifact valid != claim true
relation detected != architectural intent established
capability available != capability warranted
repository changed != repair succeeded
ontology term documented != runtime-enforced concept
semantic profile valid != reasoning semantically correct
registry liveness valid != Skill semantically correct
canonical Skill tree exists != native harness observed/invoked Skill
companion reconstruction value != Campaign promotion warrant
Phase N complete != Phase N+1 authorized
one Phase 15 rule qualified != broad Phase 15 authorized
```

## Ontology admission rule

A candidate concept should enter the shared ontology only when all of the following are true:

1. it answers at least one demonstrated competency question;
2. at least two meaningful reasoning situations need the distinction, unless the distinction protects a critical safety/authority boundary;
3. its meaning can be stated independently of one Skill implementation;
4. its relationship to evidence and authority is clear;
5. it does not duplicate an existing canonical concept under another name.

Executable promotion requires the additional evidence described in [`implementation-plan.md`](implementation-plan.md).

## Non-goals

This initiative does **not** authorize:

- a universal ontology of all software engineering;
- a mandatory knowledge graph for every Campaign;
- automatic semantic routing;
- automatic architecture judgment;
- confidence scores treated as truth probabilities;
- ontology-driven autonomous mutation authority;
- replacing source evidence with a generated semantic map;
- encoding the entire ontology in YAML/JSON before real Skills demonstrate the need;
- a central Reasoning Engine that ranks uncertainty, selects responsibility/capability, or decides Campaign disposition;
- mandatory use of `semantic_reasoning_profile` in every domain artifact;
- a generic documentation/prose truth checker;
- broad conformance rules without observed maintenance defects.

## Relationship to the Campaign

The Campaign remains the durable decision process. The semantic architecture supplies a shared language for what Campaign participants mean.

The intended relationship is:

```text
repository / external source
        |
        v
observations and evidence
        |
        v
shared semantic vocabulary
        |
        v
agent-authored claims and uncertainty
        |
        v
responsibility / capability / authority
        |
        v
Campaign decision and durable transition
```

The ontology does not replace Campaign evidence. The experimental semantic profile remains outside Campaign state. The Phase 15 liveness checker is a repository CI conformance rule, not Campaign state or routing authority.

## Current frontier

Phase 10 is complete and the first evidence-triggered Phase 15 conformance rule is qualified. No broad later semantic phase is automatically active.

The next architecture package must be justified by observed repository/product pressure and the relevant trigger in [`implementation-plan.md`](implementation-plan.md). In particular:

- Phase 11 waits for repeated demand for a new mechanical semantic relation;
- Phase 12 waits for repeated costly reconstruction of the same repository entities/relations;
- Phase 13 waits for demonstrated consequential cross-session control-plane state;
- Phase 14 waits for at least two genuinely independent domain implementations exposing a reusable domain-pack boundary;
- additional Phase 15 rules wait for new observed maintenance/conformance defects.

Preserving the current architecture unchanged is a valid outcome when none of those triggers is demonstrated.
