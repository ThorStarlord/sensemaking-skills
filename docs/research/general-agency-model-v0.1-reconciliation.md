# General Agency Model v0.1 ↔ Sensemaking Reconciliation

**Status:** completed research/product-boundary reconciliation  
**Date:** 2026-09-18  
**Authority:** non-authoritative research reconciliation; ADR 0029 remains authoritative  
**Model:** `general-agency-model-v0.1.md`  
**Crosswalk:** `general-agency-sensemaking-crosswalk-v0.1.md`  
**Design:** `../superpowers/specs/2026-09-18-general-agency-model-v0.1-design.md`  
**Plan:** `../superpowers/plans/2026-09-18-general-agency-model-v0.1-reconciliation.md`

## 1. Reconciliation question

> Do the General Agency Model v0.1 additions expose a concrete current Sensemaking implementation gap, or are they already satisfied by existing durable state/control surfaces with at most bounded guidance clarification?

This document distinguishes conceptual value from product/runtime warrant.

A concept can improve the parent theory without justifying a new product feature.

## 2. Fixed disposition vocabulary

Each v0.1 concept receives exactly one implementation disposition:

```text
ALREADY_SATISFIED
GUIDANCE_GAP
DURABLE_STATE_GAP
DETERMINISTIC_ASSURANCE_GAP
OUTSIDE_PRODUCT
UNRESOLVED
```

Package-level disposition uses:

```text
NO_CHANGE_WARRANTED
GUIDANCE_ONLY_WARRANTED
ARCHITECTURE_REVIEW_REQUIRED
```

## 3. Summary

| v0.1 concept | Disposition | Current Sensemaking evidence | Smallest warranted intervention |
| --- | --- | --- | --- |
| **Memory / Provenance substrate** | `ALREADY_SATISFIED` | Campaign state/evidence/transitions, handoff/resume, STATUS, ADRs, target currentness, explicit PAA persistence rule | No new state/schema. Keep using existing durable surfaces when continuation warrants them. |
| **Knowledge Externalization / Communication** | `GUIDANCE_GAP` | Handoffs, ADRs, artifacts, reports and durable-continuation guidance exist, but canonical guidance frames persistence mainly around fresh-context reconstruction rather than the broader transferability question | Add a bounded externalization rule to the practical reference and a compact durable-continuation clarification in `using-sensemaking`. |
| **Exploration Policy** | `GUIDANCE_GAP` | Current guidance says when to explore/stop, but does not clearly say how an agent with meaningful search history should choose the next search mode | Add qualitative iterative-search allocation guidance only; no enum, score, runtime, or persistence requirement. |
| **Search State** | `ALREADY_SATISFIED` | Existing evidence/history/handoff/Campaign/strategic surfaces can preserve material attempts and outcomes when needed | Treat Search State as an on-demand projection. No `SearchState` schema. |
| **Adaptive Capability Activation** | `ALREADY_SATISFIED` | "use the lightest process", ceremony scaling, challenge/exploration triggers, Campaign conditionality, resource-aware stopping, minimum necessary ascent | No separate controller or new product surface. The new name is explanatory only. |

**Package-level disposition:** `GUIDANCE_ONLY_WARRANTED`.

No durable-state, deterministic-assurance, runtime, schema, public-API, or product-boundary change is established.

## 4. Memory / Provenance substrate

### 4.1 Current support

Practical Agent Architecture already states:

> Persist only what a fresh context needs to reconstruct a consequential decision.

Current durable surfaces include:

- Campaign state and handoff;
- Campaign evidence/transitions;
- strategic state / STATUS;
- semantic-state companions;
- ADRs;
- target snapshot/currentness;
- authority metadata;
- repository history and normal version-control provenance.

The canonical bootstrap likewise directs future contexts to read durable artifacts rather than depend on transient conversation memory.

### 4.2 Search history representability

When search history becomes material, existing surfaces can preserve:

- attempted responsibility/intervention;
- evidence returned;
- failed/rejected direction;
- uncertainty that remains;
- concise rationale;
- stop/reopen conditions;
- transition history.

Nothing in current normal-use evidence shows that a dedicated generic memory substrate is required to reconstruct consequential repository work.

### 4.3 Hidden reasoning boundary

Current PAA guidance already rejects hidden chain-of-thought persistence and prefers explicit conclusions, evidence, dependencies, rationale, and conditions needed for reconstruction.

That matches v0.1.

### 4.4 Disposition

`ALREADY_SATISFIED`

### 4.5 Smallest warranted intervention

None.

Do not add:

- `MemoryEngine`;
- universal belief store;
- generic vector memory;
- Campaign schema revision;
- private scratchpad persistence.

A future `DURABLE_STATE_GAP` would require repeated normal-use cases where materially necessary decision/search state cannot be reconstructed from current explicit surfaces.

## 5. Knowledge Externalization / Communication

### 5.1 Current support

Sensemaking already externalizes knowledge through:

- ADRs;
- Campaign state and handoffs;
- repository sensemaking artifacts;
- reconciliation reports;
- STATUS;
- Skills/reference documentation;
- release/qualification records.

The PAA reference also says to persist reconstructible decision state rather than private thought.

### 5.2 What is not yet explicit enough

Current canonical guidance is strongest on this question:

> What must survive into a fresh context?

v0.1 introduces a broader but still practical question:

> What selected knowledge must become intelligible and transferable to another actor, even when raw durable state already exists?

Examples include:

- concise rationale needed by a future maintainer;
- operational instruction needed by an operator;
- decision evidence needed by an auditor;
- bounded search history needed by a delegated worker;
- user-facing knowledge whose rediscovery cost is meaningful.

Current guidance does not state that transferability is distinct from storage, nor does it explicitly warn against externalizing every reasoning result.

### 5.3 Why this is guidance, not state

The missing part is semantic selection:

```text
what should be externalized?
for whom?
in what representation?
when is the transfer value worth the cost?
```

Those are model-owned judgments.

Existing repository artifacts already provide the destination surfaces.

No new state store or deterministic validator is required.

### 5.4 Disposition

`GUIDANCE_GAP`

### 5.5 Smallest warranted intervention

Detailed practical guidance should state:

```text
Externalize decision-relevant knowledge when:
- continuation crosses context or actor boundaries;
- rediscovery would be meaningfully costly;
- consequential rationale/evidence must remain reconstructible;
- governance/operations/user transfer requires it;
- future search quality depends on preserved attempts/results.

reasoning result
!= durable artifact required
```

The canonical bootstrap should receive only a compact durable-continuation clarification.

### 5.6 Rejected heavier interventions

Do not add:

- `KnowledgeExternalizationService`;
- mandatory documentation phase;
- automatic documentation generator;
- universal artifact generator;
- requirement to persist every result.

## 6. Exploration Policy

### 6.1 Existing support

Current guidance already distinguishes challenge from exploration and says to explore when:

- current options are weak;
- only one consequential option exists;
- repeated attempts fail;
- the frame causes circular investigation;
- the problem category may be wrong;
- local optimization may hide a better boundary;
- an important opportunity is absent.

It also says to stop when additional alternatives are unlikely to change the decision or search cost exceeds likely improvement.

### 6.2 The remaining gap

That guidance answers:

```text
Should exploration become explicit?
When should exploration stop?
```

It does not clearly answer:

```text
Given meaningful search history,
what kind of next search move should receive effort?
```

v0.1 makes that distinction useful for iterative search.

A repository agent may need to choose qualitatively among:

- exploit the current best;
- explore a materially different direction;
- challenge/falsify the current best;
- diagnose why a failed attempt failed;
- recombine useful components;
- restart from a different frame;
- verify a promising result before further optimization.

### 6.3 Why this is guidance, not orchestration

The choice depends on semantic interpretation of:

- failure attribution;
- promise of current branches;
- local-optimum risk;
- uncertainty;
- consequence;
- cost;
- remaining budget.

A deterministic workflow should not silently select those modes.

The result should remain an agent-owned judgment that may then delegate bounded work.

### 6.4 Disposition

`GUIDANCE_GAP`

### 6.5 Smallest warranted intervention

Add a small iterative-search section to the PAA reference:

```text
When multiple meaningful attempts create a real search history,
use that history to decide whether the next move should
exploit / explore / challenge / diagnose / recombine / restart / verify.

For one-shot/local work, keep this implicit.
No enum or score is required.
```

Add only a compact trigger-level sentence to `using-sensemaking` if needed for discoverability.

### 6.6 Rejected heavier interventions

Do not add:

- `ExplorationPolicy` runtime class;
- search-mode enum as public contract;
- numeric exploration/exploitation score;
- automatic branch ranking;
- search-tree service;
- automatic Skill/workflow routing.

Repeated consequential search failures traceable to poor search allocation would be required before reconsidering stronger machinery.

## 7. Search State

### 7.1 Current support

The candidate Search State content is already representable through existing explicit state:

- attempts and outcomes -> evidence / transition history / repository history;
- promising or abandoned branches -> rationale / strategic alternatives / handoff;
- failure attribution -> claims / uncertainty / evidence;
- remaining search uncertainty -> decision-relevant uncertainty;
- verified results -> evidence/verification records;
- provenance/currentness -> existing provenance surfaces.

### 7.2 No dedicated durable object is established

For small work, Search State can remain transient.

For cross-context consequential work, existing Campaign/handoff/evidence surfaces can preserve the material subset.

Creating a new Search State schema would risk:

- a second truth system;
- duplication with Campaign evidence/transitions;
- mandatory ceremony for simple inquiry;
- premature freezing of a research concept.

### 7.3 Disposition

`ALREADY_SATISFIED`

### 7.4 Smallest warranted intervention

None at the state/schema layer.

The Exploration Policy guidance may refer to "search history" or "material prior attempts" without creating a new persisted type.

### 7.5 Reopen condition

A `DURABLE_STATE_GAP` requires repeated normal-use evidence that materially necessary search history cannot be reconstructed using existing durable surfaces.

## 8. Adaptive Capability Activation

### 8.1 Current support

The current canonical Skill already says:

- use the lightest process that preserves invariants;
- adapt visible scaffolding and rigor to complexity/consequence/continuation;
- do not create a Campaign merely because a task is large;
- use challenge/exploration only when triggered;
- stop investigating when the next warranted action is stable;
- use the lightest explicit structure that preserves the decision boundary.

The PAA reference says:

> More architecture does not mean more ceremony for every task.

The two recent normal-use probes also behaved consistently with this law:

1. trivial stale-authority correction -> minimal inspection/action/verification;
2. ambiguous authority reference -> explicit warrant distinction, but still no Campaign, critic, or strategic escalation.

These are encouraging examples, not proof of optimal activation.

### 8.2 Disposition

`ALREADY_SATISFIED`

### 8.3 Smallest warranted intervention

No separate controller, score, stage, or runtime.

The v0.1 term **Adaptive Capability Activation** is useful explanatory vocabulary for behavior that current guidance already implements.

### 8.4 Reopen evidence

Reconsider only from repeated:

- over-activation: simple work receives excessive critique/persistence/strategic ceremony;
- under-activation: consequential ambiguous work repeatedly omits needed challenge/exploration/verification/durability.

## 9. Deterministic assurance assessment

No new `DETERMINISTIC_ASSURANCE_GAP` is established.

Existing deterministic machinery can already verify mechanically decidable facts such as:

- schema/contract structure;
- reference/currentness integrity;
- target identity;
- exact-head identity;
- configured test results;
- provenance links where mechanically represented.

It should not decide:

- what knowledge is worth externalizing;
- which search mode is semantically warranted;
- whether search history is decision-relevant;
- whether a capability should become visible.

```text
representation valid
!= externalization warranted

search history exists
!= next search mode selected

capability available
!= capability warranted
```

## 10. Product-boundary assessment

ADR 0029 remains coherent.

The package does not require:

- new product purpose;
- new user/JTBD;
- general agent runtime;
- automatic responsibility/Skill/workflow selection;
- automatic product-thesis revision;
- autonomous external authority;
- generic memory/search product.

No Level-4 canonical revision is warranted.

## 11. Package-level disposition

### `GUIDANCE_ONLY_WARRANTED`

The smallest warranted implementation package is:

1. preserve the v0.1 research model and crosswalk;
2. add bounded Knowledge Externalization guidance to the practical reference;
3. add bounded iterative-search / Exploration Policy guidance to the practical reference;
4. add only compact discoverability-level wording to the canonical `using-sensemaking` Skill;
5. leave durable state, deterministic assurance, runtime, schema, public API, Campaign semantics, and ADR 0029 unchanged.

## 12. Explicit rejected machinery

This reconciliation does **not** warrant:

- `MemoryEngine`;
- `KnowledgeExternalizationService`;
- `SearchState` schema;
- `SearchState.json`;
- generic vector memory;
- generic search-tree persistence;
- `ExplorationPolicy` runtime class;
- deterministic capability activator;
- numeric exploration/exploitation scoring;
- automatic search routing;
- automatic documentation generation;
- automatic Skill/workflow selection;
- automatic Campaign generation;
- new Campaign truth system;
- Campaign schema change;
- Practical Agent Architecture v1;
- public API change;
- product-boundary expansion.

## 13. Acceptance check

The package remains valid only if the final guidance preserves:

```text
trivial + local + reversible
-> keep most architecture implicit

iterative search with meaningful history
-> make search-allocation judgment explicit

cross-context / cross-actor transfer where knowledge matters
-> externalize the selected decision-relevant subset

continuation complexity
-> use existing durable state when warranted
```

The purpose is greater precision, not greater mandatory process.
