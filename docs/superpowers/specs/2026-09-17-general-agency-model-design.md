# General Agency Model v0 — Research Architecture Design

**Status:** proposed architectural research design  
**Date:** 2026-09-17  
**Target repository:** `ThorStarlord/sensemaking-skills`  
**Branch:** `research/general-agency-model-v0`  
**Authority:** design/research only; not an ADR, product-strategy revision, runtime specification, schema change, Skill contract, routing rule, or implementation authorization

## 1. Purpose

Sensemaking already contains several partially orthogonal models:

- the Four-Level Control Model defines decision scope and authority ownership;
- the Semantic Architecture Reasoning Model defines an evidence-to-decision grammar;
- Campaign/Responsibility/Authority semantics define bounded continuation and execution support;
- Level 3 governs Strategic Repository Evolution;
- Level 4 governs Product Thesis / Strategy Revision.

Recent reasoning has exposed a plausible parent abstraction:

> a value-directed intelligent agent repeatedly relates purpose, context, strategy, decision framing, epistemic state, inquiry, action, observation, verification, learning, and revision under authority, risk, resource, and memory constraints.

This design tests whether that parent abstraction genuinely clarifies the existing Sensemaking architecture without silently turning Sensemaking into a generic agent runtime or expanding the current product boundary.

## 2. Design classification

This is an **architectural research package**.

It is not a bounded feature and not a runtime spike. The outputs are conceptual/reference artifacts whose purpose is to establish:

1. whether the proposed General Agency Model is internally coherent;
2. whether it maps naturally onto existing Sensemaking concepts;
3. where the models are intentionally non-equivalent;
4. what conceptual gaps, if any, are exposed;
5. whether any later Level-4 product-thesis disposition is warranted.


### 2.1 Prior bounded transfer evidence

This package is not the repository's first test of domain-general control ideas.

`docs/research/path-4-domain-transfer-results.md` records a completed eight-case synthetic AI-research transfer study with proposed disposition `TRANSFER_COHERENT`. Its bounded result is evidence that several current Sensemaking control concepts can remain coherent after software-engineering-specific semantics are replaced, including decision-changing uncertainty, evidence-bounded claims, evidence/authority separation, and the decision/orchestration boundary.

That prior result does **not** establish the broader General Agency Model proposed here. It did not test a full value-to-action-to-learning lifecycle, explicit option generation/forecasting, lateral adversarial/exploratory operators, or the proposed control-envelope/persistent-state decomposition.

Package 1 and Package 2 must therefore treat Path 4 as **prior bounded evidence and a non-duplication constraint**, not rerun the same transfer claim.

## 3. Current authority boundary

The current product boundary remains ADR 0029:

> Sensemaking Skills is an agent-native repository decision-support and control layer for software-engineering agents.

This package must preserve the existing non-goals against:

- a generic autonomous-agent platform;
- a deterministic semantic planner;
- `StrategicPlanner` or `OuterLoopEngine`;
- automatic Strategic Frontier ranking;
- automatic responsibility/capability/Skill selection;
- automatic product-thesis revision;
- autonomous merge/release/deployment/publication authority.

The new model therefore starts as a **non-authoritative research/reference layer above the current product model**.

## 4. Architectural hypothesis

The working hypothesis is:

> Sensemaking may be a software-engineering-domain instantiation of a broader value-directed adaptive agency model, while remaining a repository-specific product unless and until a separately warranted Level-4 decision changes that boundary.

The relationship under test is:

```text
GENERAL THEORY OF INTELLIGENT AGENCY
        |
        | may inform
        v
PRACTICAL AGENT ARCHITECTURE
        |
        | may specialize as
        v
SENSEMAKING FOR SOFTWARE ENGINEERING
        |
        | may operate within
        v
SOFTWARE-FACTORY EXECUTION / ORCHESTRATION
```

These layers are not interchangeable.

```text
theory != runtime
runtime != product
product != orchestration environment
semantic judgment != mechanical validation
capability != authority
```

## 5. Proposed General Agency Model v0

The core lifecycle to study is:

```text
VALUE / PURPOSE
        |
        v
CONTEXT / SITUATION MODEL
        |
        v
STRATEGIC MODEL
        |
        v
DECISION FRAME
        |
        v
EPISTEMIC STATE
        |
        v
SUFFICIENCY GATE
      /             \
     /               \
INQUIRE              CHOOSE
   |                    |
QUESTION /          OPTION SPACE
UNCERTAINTY              |
   |                 FORECAST /
METAREASONING        EVALUATION
   |                    |
INVESTIGATION           |
     \                 /
      \               /
          DECISION
             |
             v
           ACTION
             |
             v
           REALITY
             |
             v
        OBSERVATION
             |
             v
        VERIFICATION
             |
             v
      IMPACT ASSESSMENT
             |
             v
        SENSEMAKING
             |
             v
        BELIEF UPDATE
             |
             +-----------------> reassess as warranted
```

The model is deliberately not a mandatory phase-gated workflow. A case may enter from a goal, an observation, an anomaly, an external event, or a pre-existing decision.

## 6. Directional flows

The research model distinguishes three principal movements.

### 6.1 Top-down control

```text
purpose -> strategy -> decision -> inquiry/choice -> action
```

Question:

> Given what matters, what should be done?

### 6.2 Bottom-up learning

```text
reality -> observation -> verification -> sensemaking -> belief revision
```

Question:

> Given what happened, what should now be believed?

Evidence should propagate upward only as far as necessary to explain or resolve the discrepancy.

### 6.3 Lateral cognition

```text
challenge <-> current model <-> alternatives
```

Questions include:

- Why might the current belief/strategy/value be wrong?
- What alternative frame, hypothesis, option, or interpretation has not been considered?

Adversarial review and exploration are operators, not mandatory sequential nodes.

## 7. Cross-cutting structures

### 7.1 Cognitive operators

Candidate operators:

- adversarial challenge;
- exploration / alternative generation;
- causal reasoning;
- counterfactual reasoning;
- decomposition;
- comparison;
- verification;
- simulation / forecasting.

An operator does not automatically deserve a runtime service or schema entity.

### 7.2 Control envelopes

Candidate control envelopes:

- authority / governance;
- risk / consequence;
- resources / attention / cost of delay;
- constraints;
- time horizon;
- reversibility / commitment.

These alter thresholds and permitted actions across several lifecycle stages.

### 7.3 Persistent state

Candidate persistent state:

- goals / commitments;
- beliefs and epistemic status;
- supporting and counter-evidence;
- unresolved uncertainty;
- decisions and rationale;
- provenance/currentness;
- history of attempted interventions;
- calibration / confidence where appropriate.

The design does not authorize a new database or universal state schema.

## 8. Decision-relevant uncertainty and stopping

The model should retain Sensemaking's existing discipline:

> uncertainty matters because resolving it could change a decision.

The sufficiency gate asks whether further information is worth obtaining before acting.

A bounded stop is warranted when:

1. decision-changing uncertainty is sufficiently resolved for the current scope;
2. remaining uncertainty would not change action;
3. further evidence is unavailable, outside authority, or not worth its cost/delay;
4. the action is sufficiently cheap/reversible that additional investigation has lower expected value than acting.

Zero uncertainty is not required.

## 9. Adversarial reasoning

Adversarial review is treated as a cross-cutting operator:

```text
PROPOSAL
   |
CHALLENGE
   |
ADJUDICATION
   |
RETAIN / REVISE / REJECT
```

It may act on:

- proposed values or their prioritization;
- strategic models;
- decision frames;
- beliefs and causal models;
- selected questions;
- reasoning methods;
- option sets;
- forecasts;
- action decisions;
- observations and interpretations;
- impact claims.

At the value layer, the model must distinguish empirical challenge from normative contestation. Evidence can test instrumental claims about a value but does not mechanically settle every conflict among legitimate values.

## 10. Package decomposition

### Package 1 — General Agency Model v0

Planned artifact:

`docs/research/general-agency-model-v0.md`

It should define:

- terminology;
- core lifecycle;
- natural entry points;
- top-down, bottom-up, and lateral flows;
- vertical nodes versus operators versus envelopes versus persistent state;
- uncertainty/sufficiency/stopping;
- option generation and forecasting;
- adversarial challenge and exploration;
- authority/risk/resource/time constraints;
- memory/provenance;
- explicit non-goals;
- strongest permitted claims.

### Package 2 — Sensemaking Reconciliation v0

Planned artifact:

`docs/research/general-agency-sensemaking-crosswalk-v0.md`

It should include:

1. concept-by-concept crosswalk;
2. exact correspondences;
3. partial correspondences;
4. explicit non-equivalences;
5. candidate gaps;
6. four stress-test scenarios;
7. Level-4 implications;
8. bounded disposition.

The stress tests should include:

- a trivial reversible task;
- an ambiguous repository problem;
- strategic repository evolution;
- a product-thesis contradiction requiring possible upward escalation.

### Package 3 — Practical Agent Architecture v0

**Not authorized by this design alone.**

It may be designed only after Packages 1–2 show that the parent model adds explanatory value rather than vocabulary duplication.

A later design would ask which theoretical concepts need:

- model reasoning instructions;
- deterministic representation;
- persistent state;
- tool interfaces;
- multi-agent delegation;
- validation;
- owner-reserved authority.

## 11. Reconciliation rules

The research artifacts must obey these rules:

1. Reuse existing Sensemaking vocabulary when meanings already match.
2. Record non-equivalence instead of forcing tidy analogies.
3. Do not redefine canonical terms from research documents.
4. Do not change ADR 0029, `product-strategy.md`, `strategic-outer-loop.md`, or the Semantic Reasoning Model merely to make the crosswalk cleaner.
5. Do not create a product roadmap from conceptual gaps.
6. Candidate gaps are hypotheses until a current consequential decision warrants action.
7. Generality claims must preserve evidence ceilings.
8. Domain-general theory must not be inferred merely from successful software-domain mapping.

## 12. Validation and review

Because this package is conceptual, validation is primarily semantic and referential.

Before review:

- scan for unresolved placeholders;
- verify no contradictions between the parent model and stated product-boundary preservation;
- verify every claimed Sensemaking correspondence points to a current canonical concept;
- check that research language does not imply product authority;
- check that theory/runtime/product/orchestration remain distinct;
- check that candidate gaps are not written as implementation requirements;
- verify Markdown links/paths are valid when introduced.

No empirical experiment, runtime benchmark, schema migration, or release qualification is required for Packages 1–2.

## 13. Success criteria

Packages 1–2 succeed if a fresh reader can answer:

1. What does the General Agency Model claim?
2. What does it explicitly not claim?
3. How is it different from the Four-Level Control Model?
4. How is it different from the Semantic Reasoning Model?
5. Which concepts map naturally to current Sensemaking?
6. Which mappings are partial or invalid?
7. What does the model reveal that current Sensemaking leaves implicit?
8. Does any discovered difference actually warrant changing the product?
9. What evidence would be required before building generic agent machinery?

## 14. Initial expected Level-4 posture

The initial hypothesis is **REINTERPRET or NO PRODUCT CHANGE**, not automatic `REVISE` or `SUPERSEDE`.

A plausible reinterpretation, if supported, is:

> Sensemaking remains repository decision support but can be understood as a software-engineering-domain realization of a broader value-directed agency model.

That wording must remain research-only until a separate Level-4 review ratifies it.

## 15. Explicit non-goals

This package does not authorize:

- implementation of a general-agent runtime;
- a new planner, scheduler, workflow engine, or orchestration layer;
- a universal cognitive-state database;
- automatic value/objective selection;
- automatic normative adjudication;
- deterministic semantic ranking/scoring;
- automatic adversarial multi-agent voting;
- automatic strategy or thesis revision;
- product-category expansion;
- repository renaming;
- merging Sensemaking with a software-factory repository;
- changing existing release/support claims.

## 16. Next gate

After this design is committed, the owner reviews it.

If approved, the next authorized work is **Package 1 + Package 2 research documentation only**.

Any practical agent architecture or runtime implementation requires a subsequent design/review step.
