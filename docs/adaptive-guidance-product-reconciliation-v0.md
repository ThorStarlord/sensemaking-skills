# Adaptive Guidance Product Reconciliation v0

**Status:** bounded product-alignment audit  
**Date:** 2026-09-11  
**Authority:** Persona & Adaptive Guidance Model v0 in `docs/product-strategy.md` and `docs/product-operating-model.md`  
**Baseline:** `main` after Documentation Entry-Point Consolidation v1  
**Scope:** current agent-facing and user-facing Sensemaking surfaces; no runtime scoring, routing, schema migration, or empirical claim expansion

## 1. Purpose

This audit asks whether the existing shipped Sensemaking product correctly serves the clarified **high-delegation agent-assisted builder / repository owner**, beginner-first and expert-capable, without imposing unnecessary ceremony.

The governing design principle is:

> **Opinionated about engineering invariants, adaptive about process, progressive in disclosure.**

Documentation Entry-Point Consolidation v1 already clarified which document each audience should read. This audit does not undo that work. It asks the next question: **does the usage sequence taught by those entry points make the proportionality model clear?**

## 2. Evaluation model

| Factor | Question | Primary product effect |
| --- | --- | --- |
| **User supervision capability** | How able is the user, in this decision, to spot omissions and evaluate agent judgment? | Scaffolding / explanation |
| **Desired delegation** | How much repository-level engineering judgment does the user want the agent to exercise? | Agent decision ownership within granted authority |
| **Decision complexity** | How hard is it to determine the warranted responsibility? | Sensemaking / investigation rigor |
| **Consequentiality** | How costly, irreversible, authority-sensitive, or damaging could a wrong responsibility/action be? | Caution / evidence / validation / reconciliation |
| **Continuation complexity** | How much repository-specific decision state must survive time, sessions, agents, machines, or handoffs? | Campaign durability / provenance / resume |

Important non-identities:

```text
user supervision capability != permanent expertise class
desired delegation != granted authority
decision complexity != technical difficulty
decision complexity != consequentiality
continuation complexity != task size
more scaffolding != more visible machinery
```

No score, threshold, runtime mode, persona inference, or deterministic router is implied.

## 3. Alignment dispositions

- `ALIGNED` — current trigger, behavior, and presentation fit v0.
- `PRESENTATION_MISALIGNED` — capability is appropriate, but current Skill/docs framing encourages too much/too little ceremony or hides its situational purpose.
- `BEHAVIOR_MISALIGNED` — implementation mechanically forces behavior inconsistent with v0; a separate bounded implementation responsibility may be warranted.

```text
presentation mismatch != runtime defect
runtime defect != permission for broad redesign
```

## 4. Surface inventory and situational-purpose map

| Surface | Primary situational reason | Disposition | Reconciliation action |
| --- | --- | --- | --- |
| `using-sensemaking` | High delegation, missing-question risk, ambiguous responsibility | `PRESENTATION_MISALIGNED` | Add compact adaptive lens; detailed examples in a progressively loaded reference. |
| `repo-sensemaker` | Decision complexity / repository-wide uncertainty | `ALIGNED` | Preserve behavior; reference it as the decision-complexity escalation path. |
| Repository Sensemaking Brief validation | Evidence integrity / currentness | `ALIGNED` | No behavior change. |
| `README.md` | Public orientation and audience routing | `PRESENTATION_MISALIGNED` | Preserve the new audience map from Documentation Entry-Point Consolidation v1; add a proportionality map before Campaign onboarding. |
| `GETTING_STARTED.md` | Canonical human first-use path | `PRESENTATION_MISALIGNED` | Preserve its canonical role; teach goal -> responsibility clarity -> repository sensemaking -> Campaign only when durability is warranted. |
| `docs/sensemaking-campaign.md` | Canonical Level-2 durable model | `PRESENTATION_MISALIGNED` | Clarify Campaign as the central **durable** abstraction, not universal Sensemaking entry point. |
| Golden Path v1 docs | Campaign composition / discoverability | `PRESENTATION_MISALIGNED` | Preserve canonical workflow-composition ownership; add a pre-entry decision about whether Campaign durability is warranted. |
| shipped `golden-paths-v1.md` reference | Agent-facing Campaign composition | `PRESENTATION_MISALIGNED` | Mirror the same pre-entry gate. |
| Campaign initialization | Durable continuation state | `ALIGNED` | No behavior change. |
| Campaign preflight | Mechanical Campaign integrity | `ALIGNED` | No behavior change. |
| Campaign Doctor | Mechanical diagnosis | `ALIGNED` | No behavior change. |
| Campaign inspect / explain / diff | Reconstruction / observability | `ALIGNED` | No behavior change. |
| Resume Capsule / resume profiles | Continuation complexity | `ALIGNED` | No behavior change. |
| Campaign capability context | Capability inspection after responsibility selection | `ALIGNED` | No behavior change. |
| Artifact admission / evidence lineage | Durable evidence integrity | `ALIGNED` | No behavior change. |
| Campaign provenance / graph | Review and reconstruction burden | `ALIGNED` | No behavior change. |
| Campaign handoff / transfer / rebinding | Cross-context continuation | `ALIGNED` | No behavior change. |
| Campaign completion / archive | Reconstructible terminal state | `ALIGNED` | No behavior change. |
| `output-reconciler` | Consequential completed-work claims | `ALIGNED` | No behavior change. |
| `repair-verifier` | Consequential finding-specific closure | `ALIGNED` | No behavior change. |
| Strategy inspect / diff / handoff | Level-3 repository-evolution complexity | `ALIGNED` | No behavior change. |
| Multi-repository Campaign surfaces | Repository breadth + continuation complexity | `ALIGNED` | No behavior change. |

## 5. Findings

### F1 — Shipped bootstrap lacks the adaptive lens

**Disposition:** `PRESENTATION_MISALIGNED`.

`using-sensemaking` correctly teaches the core control loop, responsibility-before-Skill, evidence discipline, authority, and stopping. A fresh agent reading only the shipped Skill is not yet explicitly told how the five contextual factors affect the amount of scaffolding, investigation, validation, and durability.

Required compact mapping:

```text
lower user supervision capability
-> more proactive scaffolding

higher desired delegation
-> resolve more repository-answerable questions independently
   within granted authority

higher decision complexity
-> stronger repository sensemaking / investigation

higher consequentiality
-> stronger evidence / validation / reconciliation

higher continuation complexity
-> stronger case for durable Campaign state
```

### F2 — Entry-point ownership is improved; first-use sequencing remains Campaign-forward

**Disposition:** `PRESENTATION_MISALIGNED`.

Documentation Entry-Point Consolidation v1 correctly establishes:

```text
GETTING_STARTED.md = human how-to entry point
using-sensemaking/SKILL.md = coding-agent instructions
agent-workflow-golden-path-v1.md = workflow composition
operations-runbook.md = maintainer qualification
```

That is now `ALIGNED` and must be preserved.

The remaining mismatch is sequencing: the first-use path still introduces Skills + Campaign CLI, Golden Paths, and Campaign initialization before it teaches the simpler proportionality question: **does this work need Campaign durability at all?**

Desired teaching order:

```text
repository goal
-> is the responsibility clear and locally evidenced?
   -> yes: direct bounded work
   -> no: repository sensemaking
-> does the work need durable continuation?
   -> yes: Campaign
-> are claims/repairs consequential?
   -> reconciliation / repair verification when warranted
```

### F3 — Campaign is the central durable abstraction, not the universal entry point

**Disposition:** `PRESENTATION_MISALIGNED`.

`docs/sensemaking-campaign.md` correctly defines Campaign as a durable engineering decision process across sessions. The mismatch is its universal-sounding lifecycle (`user goal -> campaign initialization`) and unqualified wording that Campaign is the central product abstraction.

The corrected product relation is:

```text
Sensemaking control doctrine
-> applies proportionally

Campaign
-> central durable Level-2 abstraction
-> becomes valuable primarily when continuation complexity warrants persistent state
```

No Campaign data-model redesign is implied.

### F4 — Golden Paths are Campaign composition paths, not the universal Sensemaking path

**Disposition:** `PRESENTATION_MISALIGNED`.

The four current Golden Paths are sound. The missing pre-entry decision is:

```text
Is durable Campaign state warranted?
NO  -> bounded Sensemaking / ordinary work without Campaign ceremony
YES -> use the relevant Campaign composition path
```

The canonical Golden Path document remains static composition guidance. The CLI must not choose a flow.

### F5 — No behavior-level mismatch is established

**Disposition:** runtime/mechanical layer `ALIGNED`.

Current contracts support all of the following:

- Skills can be used without Campaign state.
- `repo-sensemaker` is independently invokable and stops at a diagnostic artifact.
- Campaign initialization records state but does not infer uncertainty, responsibility, capability, or authority.
- Preflight and Doctor remain mechanical.
- Resume/inspect/provenance remain projections, not recommendation engines.
- Reconciliation is triggered by material claims rather than every tiny edit.
- Repair verification is finding-specific.
- Completion/archive require an explicit semantic terminal decision and do not infer success.

Therefore this audit does **not** warrant runtime/API/schema changes.

## 6. Beginner-first / expert-capable implications

### Beginner-first

Increase missing-question scaffolding without requiring the user to understand internal machinery first.

Good user-facing example:

> I am checking the existing authentication boundary first because that determines where this change belongs.

Bad product direction:

> Choose a Campaign rigor mode and rate your expertise.

### Expert-capable

Keep the same doctrine compact when the user can supervise the decision:

> Auth ownership is ambiguous between packages A/B; checking the current boundary before selecting implementation responsibility.

More scaffolding and more exposed mechanism remain separate decisions.

## 7. Package 2 — warranted shipped-guidance alignment

Bounded scope:

1. update `skills/using-sensemaking/SKILL.md` with a compact adaptive-guidance lens;
2. add `skills/using-sensemaking/references/adaptive-guidance-v0.md` with examples and anti-patterns;
3. update `README.md` while preserving its newly consolidated audience map;
4. update `GETTING_STARTED.md` while preserving its canonical human-entry role;
5. clarify `docs/sensemaking-campaign.md` as the central durable abstraction rather than the universal entry path;
6. add a Campaign pre-entry gate to `docs/agent-workflow-golden-path-v1.md` and the shipped `golden-paths-v1.md` reference;
7. preserve all semantic/mechanical/authority boundaries.

No runtime code, APIs, schemas, workflow projection data, formal Campaign modes, or automatic routing are authorized by Package 2.

## 8. Package 3 — mechanics reassessment gate

After Package 2 is integrated, re-check:

```text
Skills operate without Campaign state
repo-sensemaker operates independently
Campaign is optional until durable continuation is warranted
preflight and Doctor remain mechanical only
Resume surfaces avoid recommending action
Golden Paths remain static navigation
reconciliation remains selective for consequential claims
repair verification remains finding-specific
completion requires explicit semantic terminal decision
```

If these remain true, Package 3 is a documentation closeout / `STOP`, not runtime implementation.

If a concrete behavior mismatch appears, create exactly one separate bounded responsibility with evidence, tests, compatibility limits, and explicit non-goals.

## 9. Candidate-reservoir disposition

Keep Progressive Campaign Rigor tiers `DEFERRED / REQUIRES_EVIDENCE`.

```text
adaptive guidance
+ existing proportional mechanics
+ improved shipped guidance
!= formal LIGHT / STANDARD / HEAVY Campaign modes
```

A presentation fix is evidence **against** prematurely formalizing new runtime tiers unless later normal use shows a recurring behavior-level burden that guidance cannot solve.

## 10. Explicit non-goals

```text
NO Persona Model v1
NO additional persona dimensions
NO user expertise score
NO competence inference
NO delegation enum
NO decision-complexity score
NO consequentiality score
NO automatic Campaign threshold
NO LIGHT / STANDARD / HEAVY modes
NO workflow router
NO automatic Skill selection
NO Campaign schema v3
NO StrategicPlanner / OuterLoopEngine
NO broad Campaign redesign
NO broad documentation cleanup
NO new empirical experiment
NO unrelated candidate feature
```

## 11. Package 1 conclusion

The shipped mechanics are compatible with Persona & Adaptive Guidance Model v0. The current mismatch is how the existing product is taught and framed, even after the separate entry-point consolidation work improved documentation ownership.

**Warranted next responsibility:** bounded **shipped-guidance alignment**, followed by a fresh mechanics reassessment. No runtime implementation is currently warranted.
