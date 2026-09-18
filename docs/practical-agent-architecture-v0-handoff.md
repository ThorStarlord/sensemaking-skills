# General Agency / Practical Agent Architecture v0 — Milestone Handoff

**Status:** milestone closeout record  
**Date:** 2026-09-18  
**Scope:** General Agency Model v0 research reference, Sensemaking reconciliation, warrant-centered Practical Agent Architecture v0, and canonical agent-facing guidance integration  
**Current disposition:** `GUIDANCE_ONLY_WARRANTED`  
**Next mode:** normal-use validation; no dedicated architecture-construction package selected

## 1. Milestone objective

Clarify whether current Sensemaking can be understood as a software-engineering specialization of a broader value-directed agency model, then determine the smallest practical architecture needed to make that model operational without creating a generic agent runtime.

The work intentionally separated:

```text
General Agency theory
!= Practical Agent Architecture
!= Sensemaking product boundary
!= execution/orchestration environment
```

The final operational architecture is:

```text
semantic agent judgment
        |
target-specific warrant
        |
existing durable decision substrate
        |
deterministic assurance
        |
external execution / orchestration
        |
reality / evidence
        |
semantic reassessment
```

Authority constrains every transition.

## 2. Qualified package ledger

| Package | PR | Qualified head | Merge SHA | Qualification |
| --- | --- | --- | --- | --- |
| General Agency Model v0 research package | #374 | `ea6419b6bdf0307aaa29bf10740efc1ba9f44962` | `09688aa03fd4f1eb5b16438a26078bdd3582345b` | Product Validation PASS; Release Candidate Distribution PASS |
| Practical Agent Architecture v0 guidance package | #376 | `3cb809b4d463739021a3c7ff6462f77f464d5ee5` | `e244ab0edce4f4fe3e1dec87a86ab28b5364bb5f` | Product Validation PASS; Release Candidate Distribution PASS; Repository and Skill contracts PASS; skill-hygiene checks PASS |

A prerequisite release-baseline reconciliation was merged separately in PR #375 before the General Agency package was rebased and qualified. It repaired inherited public-API/release-contract drift and did not change the General Agency or Practical Agent Architecture design.

## 3. General Agency Model v0 outcome

The research package established a coherent candidate parent grammar:

```text
value / purpose
-> context / situation
-> strategy
-> decision frame
-> epistemic state
-> sufficiency
-> inquiry / option generation
-> forecast / evaluation
-> decision
-> action
-> reality
-> observation
-> verification
-> impact assessment
-> sensemaking
-> belief update
-> selective reassessment
```

Cross-cutting structures include:

- adversarial challenge;
- exploration / alternative generation;
- causal and counterfactual reasoning;
- authority / governance;
- risk / consequence;
- resources / attention;
- constraints;
- time horizon;
- reversibility;
- durable commitments/evidence/provenance.

The bounded research interpretation is:

> Sensemaking remains repository decision support but may be understood as a software-engineering-domain realization of a broader value-directed agency model.

This remains a research interpretation. ADR 0029 remains the current product-boundary authority.

## 4. Practical Agent Architecture v0 outcome

The selected architecture is **warrant-centered and hybrid**.

It explicitly rejects one-runtime-component-per-cognitive-node.

The five ownership zones are:

1. **Semantic Agency Plane** — model-owned judgment.
2. **Warrant / Decision Control** — what is justified now, for which target.
3. **Durable Decision Substrate** — only explicit state required for reconstruction.
4. **Deterministic Assurance** — mechanically decidable facts and integrity.
5. **Execution / Orchestration** — coordinate already-selected work.

These are ownership boundaries, not mandatory services, classes, databases, or runtime engines.

Core law:

> **Decision selects the work. Orchestration coordinates the work. Evidence determines what becomes warranted next.**

## 5. Reconciliation result

The repository reconciliation classified current needs as follows:

| Area | Disposition |
| --- | --- |
| Semantic Agency Plane | `GUIDANCE_GAP` |
| Warrant / Decision Control | `GUIDANCE_GAP` |
| Durable Decision Substrate | `ALREADY_SATISFIED` |
| Deterministic Assurance | `ALREADY_SATISFIED` |
| Execution / Orchestration | `GUIDANCE_GAP` at the agent-facing interface |
| Authority / Governance | `ALREADY_SATISFIED` |

Final implementation disposition:

```text
GUIDANCE_ONLY_WARRANTED
```

No evidence established a need for:

- Campaign schema changes;
- generic `AgentState`;
- `Warrant` runtime type;
- `warrant_gap` field;
- new public API;
- generic semantic validator;
- planner/runtime;
- automatic Skill selection;
- automatic Campaign creation;
- automatic critic voting;
- option or warrant scoring.

## 6. Canonical guidance integrated

`skills/using-sensemaking/SKILL.md` now teaches the compact practical loop:

```text
Orient
-> name the consequential decision / contemplated warrant target
-> locate the nearest decision-changing warrant gap
-> select responsibility
-> perform or delegate bounded work
-> ground returned evidence
-> validate mechanics
-> update warrant
-> continue / stop / escalate / verify / ask owner
```

The detailed agent reference adds:

- warrant target/dependency guidance;
- challenge versus exploration;
- resource-aware stopping;
- delegation/subagent evidence return;
- mechanical-versus-semantic boundaries;
- persistence guidance;
- normative/value-conflict handling;
- progressive disclosure.

Key preserved distinctions:

```text
warrant != confidence score
warrant != authorization
worker recommendation != parent decision
worker success != global closure
mechanically valid != semantically correct
practical architecture used != Campaign required
```

## 7. Claim ceilings

This milestone establishes architecture/reconciliation/guidance coherence inside the current repository-domain product.

It does not establish:

- a universal theory of intelligence;
- optimality of the General Agency Model;
- cross-domain runtime completeness;
- native-harness usefulness;
- comparative superiority;
- product-market value;
- that warrant-centered guidance measurably improves outcomes;
- a need for a generic autonomous-agent runtime.

Those claims require evidence not produced by this milestone.

## 8. Current Level-3 posture

```text
CURRENT HIGHEST-LEVERAGE CONSTRUCTION BOUNDARY
NONE SELECTED

CURRENT IMPLEMENTATION DISPOSITION
GUIDANCE_ONLY_WARRANTED

CURRENT WARRANTED REPOSITORY RESPONSIBILITY
NONE

NEXT MODE
NORMAL_USE_VALIDATION
```

The repository should now stop constructing additional agency architecture and use the guidance during ordinary consequential work.

## 9. Normal-use validation rule

Do not create a new synthetic experiment merely to exercise every concept.

Use ordinary repository work and watch for **repeated** decision-changing pressure.

Potential reopen evidence includes:

- repeated loss of live warrant dependencies across contexts;
- repeated failure to reconstruct a consequential decision;
- repeated worker/orchestrator responsibility drift;
- repeated premature convergence that current exploration guidance does not prevent;
- repeated weak-evidence commitment that current challenge guidance does not prevent;
- repeated over-investigation of cheap reversible work;
- repeated under-investigation of consequential irreversible work;
- a concrete mechanically decidable assurance gap;
- a durable-state reconstruction gap current Campaign/strategic/semantic surfaces cannot express.

A single awkward case is not enough by itself.

```text
one awkward case
!= architecture gap

repeated decision failure
traceable to the same missing structure
= candidate bounded responsibility
```

## 10. Continuation rule

Use current Sensemaking normally.

Keep trivial reversible tasks lightweight.

Make warrant, challenge, exploration, delegation, and durable state more explicit only when consequence, ambiguity, irreversibility, continuation complexity, or authority sensitivity warrants it.

Do not begin:

```text
Practical Agent Architecture v1
WarrantEngine
AgentState
OuterLoopEngine
StrategicPlanner
automatic critic swarm
automatic option ranking
generic cognition database
automatic Campaign generator
generic autonomous-agent runtime
```

unless new evidence creates a concrete decision-changing need.

The next repository-construction package should originate from **normal-use evidence or explicit owner direction**, not from the existence of additional imaginable architecture.
