# General Agency Model v0.1 — Memory, Externalization, and Exploration Policy Design

**Status:** proposed research/reference refinement  
**Date:** 2026-09-18  
**Scope:** conceptual architecture only  
**Current product boundary:** unchanged; ADR 0029 remains authoritative  
**Parent:** `docs/research/general-agency-model-v0.md`  
**Non-goal:** this design does not authorize a runtime, schema, database, planner, search service, memory service, or product-boundary expansion

## 1. Decision

Refine the General Agency Model with four tightly bounded additions:

1. **Memory / Provenance as a persistent substrate**, not a late sequential phase.
2. **Knowledge Externalization / Communication as a cross-cutting capability** distinct from memory.
3. **Exploration Policy as a conditional controller of iterative inquiry/search**, distinct from the exploration operator itself.
4. **Search State as a decision-relevant projection of persistent memory/provenance for the current search**, not a required schema.

The refinement also makes one existing control law explicit:

> **Capabilities become visible only when their expected decision value justifies their cognitive, persistence, coordination, and operational cost.**

This is a research-model refinement first. Product/runtime changes, if any, require a separate reconciliation and warrant decision.

## 2. Why refine v0

General Agency Model v0 already contains:

- metareasoning;
- a sufficiency gate;
- exploration / alternative generation;
- persistent state;
- provenance/currentness;
- resource-aware stopping;
- minimum necessary ascent.

Practical Agent Architecture v0 already contains:

- explicit persistence boundaries;
- challenge/exploration triggers;
- an “Exploration policy” section;
- ceremony-scaling guidance;
- resource-aware metareasoning.

The remaining conceptual gaps are narrower:

### 2.1 Persistent state is present but visually secondary

The v0 lifecycle is drawn primarily as a vertical/recursive cognitive cycle, while persistent state appears later as a separate section. This can suggest that memory is a late stage rather than a substrate read and written throughout the cycle.

### 2.2 Memory and externalization are not distinguished strongly enough

Memory/provenance answers:

> What happened, what is known, and why?

Knowledge externalization answers:

> What selected knowledge must be made explicit, durable, intelligible, and transferable to another actor?

These functions overlap but are not equivalent.

### 2.3 Exploration operator and exploration policy are conflated

The existing exploration operator asks:

> What plausible frame, option, explanation, or intervention is not represented?

A stronger exploration policy asks:

> Given search history, uncertainty, resources, and current promise, where should search effort go next?

The latter controls allocation among search modes such as exploit, explore, diagnose, challenge, recombine, restart, and verify.

### 2.4 Search history lacks a named decision-relevant projection

Iterative inquiry benefits from a compact conceptual search state, but v0 should not imply a new universal durable schema.

## 3. Approaches considered

### Approach A — Leave v0 unchanged

Treat memory/provenance, externalization, and search allocation as implicit consequences of existing metareasoning and persistent-state sections.

**Advantages**

- zero conceptual churn;
- lowest maintenance cost;
- avoids premature terminology.

**Disadvantages**

- leaves memory visually subordinate to the lifecycle;
- obscures the distinction between stored knowledge and transferable knowledge;
- leaves “exploration” ambiguous between generating alternatives and controlling search allocation.

**Disposition:** rejected. The new distinctions are explanatory, not merely terminological.

### Approach B — Conceptual refinement with no runtime commitment

Add the four bounded concepts to the General Agency research layer, explicitly reconcile them against Practical Agent Architecture and Sensemaking, and preserve all existing non-goals against premature machinery.

**Advantages**

- improves conceptual precision;
- preserves anti-ceremony behavior;
- reuses existing persistence/guidance surfaces;
- makes later empirical failures easier to classify;
- does not force schema/runtime changes.

**Disadvantages**

- adds terminology that must be carefully distinguished;
- risks future reification if non-goals are weakly stated.

**Disposition:** selected.

### Approach C — Formalize memory/search as first-class runtime machinery

Introduce generic state, search-tree persistence, exploration-policy runtime objects, and deterministic activation rules.

**Advantages**

- explicit machine surfaces;
- potentially useful for large automated search systems.

**Disadvantages**

- unsupported by current normal-use evidence;
- conflicts with the current product boundary;
- risks turning capabilities into mandatory ceremony;
- prematurely freezes abstractions that are still research concepts.

**Disposition:** rejected.

## 4. Revised architecture

The v0.1 model should be presented as:

```text
╔══════════════════════════════════════════════════════════╗
║ GOVERNANCE / AUTHORITY                                  ║
║ RISK / CONSEQUENCE / RESOURCES / TIME / REVERSIBILITY   ║
║                                                          ║
║   VALUE / PURPOSE                                        ║
║          ↓                                               ║
║   CONTEXT / SITUATION                                    ║
║          ↓                                               ║
║   STRATEGIC MODEL                                        ║
║          ↓                                               ║
║   DECISION FRAME                                         ║
║          ↓                                               ║
║   EPISTEMIC STATE                                        ║
║          ↓                                               ║
║   SUFFICIENCY GATE                                       ║
║       ↙           ↘                                      ║
║   INQUIRY          CHOICE                                ║
║      ↓                                                    ║
║   INQUIRY OBJECTIVE                                      ║
║      ↓                                                    ║
║   METAREASONING                                          ║
║      ↓                                                    ║
║   EXPLORATION POLICY  [only when iterative search exists]║
║      ↓                                                    ║
║   INVESTIGATION / SEARCH                                 ║
║      ↓                                                    ║
║   SEARCH EVALUATION                                      ║
║      └──────────────↺                                     ║
║                                                          ║
║               DECISION                                   ║
║                  ↓                                       ║
║               ACTION                                     ║
║                  ↓                                       ║
║               REALITY                                    ║
║                  ↓                                       ║
║            OBSERVATION                                   ║
║                  ↓                                       ║
║            VERIFICATION                                  ║
║                  ↓                                       ║
║         IMPACT / SENSEMAKING                             ║
║                  ↓                                       ║
║            BELIEF UPDATE ─────↺                          ║
║                                                          ║
║ ← CHALLENGE / EXPLORATION / COUNTERFACTUAL →             ║
║ ← KNOWLEDGE EXTERNALIZATION / COMMUNICATION →            ║
╠══════════════════════════════════════════════════════════╣
║ MEMORY / PROVENANCE SUBSTRATE                            ║
║ commitments • beliefs • evidence • uncertainty           ║
║ decisions • rationale • search history • results         ║
║ provenance • currentness • interventions                 ║
╚══════════════════════════════════════════════════════════╝
```

This is a reasoning relation, not a required runtime state machine.

## 5. Memory / Provenance as persistent substrate

### 5.1 Definition

Memory / Provenance preserves information required to reconstruct what the agent/system knew, decided, attempted, and why.

Candidate content remains:

- goals and commitments;
- beliefs and epistemic status;
- evidence and counter-evidence;
- unresolved uncertainty;
- decisions and rationale;
- provenance and currentness;
- intervention history;
- calibration where useful.

v0.1 adds **search history/results** as a possible persistent category when iterative search makes that history decision-relevant.

### 5.2 Read/write relationship

Every major part of the cognitive cycle may read from or write to persistent memory.

Examples:

```text
decision frame
-> reads prior commitments/decisions

investigation
-> reads prior attempts
-> writes observations/results

verification
-> writes verified evidence/provenance

sensemaking
-> updates decision-relevant interpretation

belief update
-> updates epistemic state

externalization
-> converts selected state into durable transferable artifacts
```

### 5.3 Non-identities

```text
memory != epistemic state
memory != documentation
memory != hidden chain-of-thought
memory != universal database
provenance != truth
stored != decision-relevant
```

## 6. Knowledge Externalization / Communication

### 6.1 Definition

Knowledge Externalization / Communication asks:

> **What selected knowledge should be made explicit, durable, intelligible, and transferable to another actor, in what representation, and with what provenance?**

Possible recipient actors include:

- future instances of the same agent;
- other agents/workers;
- developers;
- operators;
- users;
- auditors;
- decision owners;
- the future self of the current actor.

### 6.2 Externalization is not memory storage

A useful relation is:

```text
externalization
=
selection
+ compression
+ structuring
+ explanation
+ audience adaptation
+ provenance attachment
```

Raw logs may be memory/provenance while remaining poor externalized knowledge.

### 6.3 Example artifacts

- ADRs and RFCs;
- specifications;
- runbooks;
- tutorials;
- handoffs;
- evidence summaries;
- release notes;
- architecture maps;
- research notes;
- machine-readable contracts;
- operationalized knowledge such as executable examples or verified API specifications.

### 6.4 Adaptive externalization

Externalization is a capability, not a mandatory stage.

Make it explicit when one or more of the following are material:

- knowledge must survive context/session loss;
- another actor must continue the work;
- rediscovery cost is meaningful;
- the rationale behind a consequential decision must remain reconstructible;
- governance/audit requires durable evidence;
- operations/users need actionable knowledge;
- future search quality depends on preserving what was tried and learned.

Otherwise, ephemeral reasoning may remain ephemeral.

```text
reasoning result
!= durable artifact required
```

## 7. Exploration operator versus Exploration Policy

### 7.1 Exploration operator

The existing exploration operator remains lateral cognition:

> What plausible frame, option, explanation, or intervention is not yet represented?

It generates or discovers alternatives.

### 7.2 Exploration Policy

Exploration Policy is a specialized metareasoning controller:

> **Given the current search state, evidence, uncertainty, resources, and history, where should search effort go next?**

It may select among search modes such as:

- **EXPLOIT** — refine the current best;
- **EXPLORE** — try a materially different direction;
- **ADVERSARIAL** — search for falsification/counterexample;
- **DIAGNOSTIC** — investigate why an attempt failed;
- **COMBINATORIAL** — recombine useful components;
- **RESTART** — abandon the local search region;
- **VERIFY** — spend effort confirming that a promising result is real.

### 7.3 Conditional activation

Exploration Policy becomes explicit only when iterative search exists.

Likely triggers include:

- multiple meaningful prior attempts;
- repeated local failure;
- a suspiciously narrow option family;
- local-optimum risk;
- ambiguous failure attribution;
- meaningful search budget allocation;
- a need to choose between exploitation and divergence.

For a one-shot, obvious, reversible task, the policy may collapse to an implicit direct inquiry.

```text
exploration capability exists
!= explicit exploration controller required
```

### 7.4 Relationship to metareasoning

```text
METAREASONING
What cognitive/search method is worth using?

EXPLORATION POLICY
Given that iterative search is warranted, where should search effort go next?
```

The policy is subordinate to metareasoning and remains bounded by authority, risk, resources, and stopping conditions.

## 8. Search State

### 8.1 Definition

Search State is a decision-relevant projection of memory/provenance for the current investigation.

Candidate content:

- attempts made;
- outcomes/scores where meaningful;
- promising branches;
- abandoned branches and reasons;
- failures/crashes;
- failure attribution hypotheses;
- unresolved search uncertainty;
- remaining budget;
- verified results;
- relevant search provenance.

### 8.2 Search State is not automatically persistent

For trivial searches it may exist only in active reasoning.

Persist it only when continuation, delegation, reconstruction, or search cost makes persistence useful.

### 8.3 Non-goals

This concept does not imply:

- `SearchState.json`;
- a generic search-tree database;
- numeric branch scoring;
- a universal exploration API;
- deterministic search routing.

## 9. Adaptive Capability Activation

v0.1 names an existing control principle:

> **A cognitive capability being available does not imply that invoking it is warranted.**

Activation remains governed by:

- metareasoning;
- sufficiency;
- expected decision improvement;
- reasoning/information/delay/opportunity cost;
- consequence;
- reversibility;
- authority;
- continuation complexity.

Conceptually:

```text
available capability
        ↓
metareasoning + control envelopes
        ↓
expected decision value worth cost?
     ↙                     ↘
   yes                      no
activate                   remain implicit / skip
```

This applies to:

- challenge;
- exploration;
- exploration policy;
- forecasting;
- delegation;
- persistence;
- externalization;
- verification depth;
- strategic ascent.

## 10. Relationship between memory, externalization, and exploration

These additions form a useful cumulative-learning loop:

```text
attempt
↓
observation / evaluation
↓
memory + provenance
↓
selected knowledge externalization when warranted
↓
future actor reconstructs search history
↓
exploration policy allocates next search effort
↓
new attempt
↺
```

This can improve system-level continuity and search quality without implying model-weight learning or a generic autonomous runtime.

## 11. Relationship to existing Sensemaking

The expected mapping is:

### Memory / Provenance

Likely existing domain-specialized surfaces:

- Campaign state;
- evidence/provenance/currentness;
- transition history;
- STATUS;
- handoff/resume;
- ADRs;
- strategic-state artifacts.

Initial expectation: **no generic memory implementation gap established**.

### Knowledge Externalization

Likely existing domain-specialized surfaces:

- repository artifacts;
- ADRs;
- handoffs;
- Campaign projections;
- reports;
- Skills/reference docs;
- status/reconciliation records.

Initial expectation: likely **conceptual/crosswalk clarification**, with any product guidance gap to be established by reconciliation rather than assumed.

### Exploration Policy

Current support includes:

- exploration triggers/stopping in Practical Agent Architecture v0;
- Strategic Frontier alternatives;
- challenge/exploration guidance in `using-sensemaking`;
- resource-aware stopping.

The new distinction is between:

```text
exploration operator
!=
search-allocation policy
```

Initial expectation: primarily **model-owned guidance**. A durable search-state or runtime implementation would require repeated normal-use evidence of iterative-search failure.

## 12. Required reconciliation before any implementation

After the research/reference refinement is drafted, reconcile each addition against current Sensemaking using the existing disposition vocabulary:

```text
ALREADY_SATISFIED
GUIDANCE_GAP
DURABLE_STATE_GAP
DETERMINISTIC_ASSURANCE_GAP
OUTSIDE_PRODUCT
UNRESOLVED
```

The reconciliation must answer:

1. Does current Sensemaking already provide a domain specialization?
2. Is the gap only explanatory/guidance-level?
3. Does normal-use evidence establish a missing durable state?
4. Is any missing fact actually mechanically decidable?
5. Would implementing machinery violate ADR 0029 or current evidence ceilings?
6. Does the change preserve progressive disclosure and low ceremony?

No product/runtime work follows automatically from a conceptual addition.

## 13. Acceptance scenarios

The refined model should explain all of these without forcing unnecessary machinery.

### A. Trivial reversible correction

Expected:

```text
direct inquiry
-> bounded action
-> verification
-> stop
```

No explicit search state, exploration policy, or durable externalization required.

### B. Ambiguous authority interpretation

Expected:

```text
decision frame
-> inspect provenance/current authority
-> adjudicate
-> bounded action or NO_CHANGE_WARRANTED
```

### C. Repeated implementation search

Several approaches have been tried and results differ.

Expected:

```text
search history
-> exploration policy
-> exploit / explore / diagnose / verify choice
-> next attempt
```

Persist search state only if continuation warrants it.

### D. Fresh-agent continuation

A future agent must continue a consequential search.

Expected:

```text
memory/provenance
-> externalized concise search/decision state
-> reconstruction
-> informed next search allocation
```

No hidden chain-of-thought required.

### E. High-consequence irreversible decision

Expected:

- stronger verification;
- challenge;
- possible exploration;
- explicit authority;
- externalized rationale/provenance when continuation/governance warrants it.

### F. Documentation-heavy release workflow

Expected:

Documentation remains a domain-specific subcycle using observation, verification, sensemaking, externalization, provenance, governance, and sufficiency. It does not become a universal vertical `DOCUMENTATION` node.

## 14. Evidence ceilings

This refinement may establish:

- conceptual coherence;
- clearer separation of persistence, externalization, exploration, and search allocation;
- a better vocabulary for future normal-use observations;
- compatibility with current anti-ceremony principles.

It does not establish:

- that a generic memory architecture improves outcomes;
- that explicit exploration policies improve Sensemaking repository work;
- that search history should always be persisted;
- that documentation/externalization should always occur;
- that current Sensemaking requires new state or runtime machinery;
- cross-domain product value;
- recursive self-improvement;
- model learning.

## 15. Explicit non-goals

Do not infer authorization for:

- `MemoryEngine`;
- `KnowledgeExternalizationService`;
- `SearchState` schema;
- generic search-tree persistence;
- `ExplorationPolicy` runtime class;
- numeric exploration/exploitation scoring;
- automatic search routing;
- automatic documentation generation;
- generic vector-memory infrastructure;
- a universal cognition database;
- Practical Agent Architecture v1;
- Campaign schema changes;
- public API changes;
- product-boundary expansion.

## 16. Planned research package after spec approval

If this design is approved, the next implementation plan should be limited to research/reference reconciliation:

1. create a successor General Agency Model v0.1 research reference while preserving v0 as historical baseline;
2. create/update a v0.1 General Agency ↔ Sensemaking crosswalk;
3. reconcile the four additions against Practical Agent Architecture v0 and current Sensemaking;
4. change canonical product/Skill guidance only if that reconciliation establishes a bounded guidance gap;
5. decline runtime/schema/product changes unless independently warranted by repeated normal-use evidence.

Expected likely disposition:

```text
RESEARCH_MODEL_REFINEMENT_WARRANTED

product/runtime implementation
-> NOT ESTABLISHED
```

## 17. Design invariants

1. Memory/provenance is persistent substrate, not mandatory visible ceremony.
2. Externalization is distinct from storage and is audience/continuation-sensitive.
3. Exploration operator generates alternatives; exploration policy allocates iterative search.
4. Search state is a projection, not a mandatory schema.
5. Metareasoning controls activation; available capability does not imply warranted activation.
6. Control envelopes continue to constrain cognition and action.
7. Minimum necessary ascent remains in force.
8. Hidden chain-of-thought is never a persistence requirement.
9. Existing Sensemaking surfaces are reused before inventing generic machinery.
10. Conceptual refinement does not expand product authority.

## 18. Summary

General Agency Model v0.1 should sharpen the model from:

```text
cognitive cycle
+ operators
+ control envelopes
+ persistent state
```

to:

```text
core cognitive cycle
+ conditional inquiry/search controller
+ lateral cognitive operators
+ control envelopes
+ persistent memory/provenance substrate
+ adaptive knowledge externalization
+ explicit anti-ceremony activation law
```

The purpose is not to make the architecture larger.

The purpose is to make it more precise about **what persists, what becomes transferable, where search effort goes, and when any of those capabilities should remain implicit**.
