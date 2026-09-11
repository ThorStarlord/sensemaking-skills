# Adaptive Guidance Product Reconciliation v0

**Status:** COMPLETE / INTEGRATED / SHIPPED-GUIDANCE-ALIGNED  
**Date:** 2026-09-11  
**Authority:** Persona & Adaptive Guidance Model v0 in `docs/product-strategy.md` and `docs/product-operating-model.md`  
**Integrated baseline:** `main` after PR #360  
**Scope:** current agent-facing and user-facing Sensemaking surfaces; no runtime scoring, routing, schema migration, or empirical claim expansion

## 1. Purpose

This reconciliation asked whether the existing shipped Sensemaking product correctly serves the clarified **high-delegation agent-assisted builder / repository owner**, beginner-first and expert-capable, without imposing unnecessary ceremony.

The governing design principle is:

> **Opinionated about engineering invariants, adaptive about process, progressive in disclosure.**

The result is a product-alignment closeout, not a new runtime architecture. The existing mechanics support proportional use; the material gaps were how the product was taught, sequenced, and packaged as agent guidance.

## 2. Evaluation model

| Factor | Question | Primary product effect |
| --- | --- | --- |
| **User supervision capability** | How able is the user, in this decision, to spot omissions and evaluate agent judgment? | Scaffolding / explanation |
| **Desired delegation** | How much repository-level engineering judgment does the user want the agent to exercise? | Agent decision ownership within granted authority |
| **Decision complexity** | How hard is it to determine the warranted responsibility? | Sensemaking / investigation rigor |
| **Consequentiality** | How costly, irreversible, authority-sensitive, or damaging could a wrong responsibility/action be? | Caution / evidence / validation / reconciliation |
| **Continuation complexity** | How much repository-specific decision state must survive time, sessions, agents, machines, or handoffs? | Campaign durability / provenance / resume |

Important non-identities remain:

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
- `PRESENTATION_MISALIGNED` — capability is appropriate, but Skill/docs/UX framing encourages too much/too little ceremony or hides its situational purpose.
- `BEHAVIOR_MISALIGNED` — implementation mechanically forces behavior inconsistent with v0; a separate bounded implementation responsibility may be warranted.

```text
presentation mismatch != runtime defect
runtime defect != permission for broad redesign
```

No `BEHAVIOR_MISALIGNED` finding was established in this milestone.

## 4. Final surface map

| Surface | Primary situational reason | Final disposition | Integrated result |
| --- | --- | --- | --- |
| `using-sensemaking` | High delegation, missing-question risk, ambiguous responsibility | `ALIGNED` | Core control loop now includes a compact five-factor adaptive lens; detailed examples live in a progressively loaded reference. |
| `repo-sensemaker` | Decision complexity / repository-wide uncertainty | `ALIGNED` | Remains independently invokable, diagnostic, and evidence-grounded; no Campaign prerequisite or implementation authority added. |
| Repository Sensemaking Brief validation | Evidence integrity / currentness | `ALIGNED` | Mechanical validation remains distinct from semantic truth. |
| `README.md` | Public orientation and audience routing | `ALIGNED` | Preserves Documentation Entry-Point Consolidation v1 and now teaches Sensemaking-first proportionality before Campaign onboarding. |
| `GETTING_STARTED.md` | Canonical human first-use path | `ALIGNED` | Teaches direct work -> repository sensemaking when needed -> Campaign when durable continuation is useful. |
| `docs/sensemaking-campaign.md` | Canonical Level-2 durable model | `ALIGNED` | Campaign is now the central **durable** abstraction, not the universal Sensemaking entry point; lifecycle begins only after Campaign is warranted/initialized. |
| Golden Path v1 docs | Campaign composition / discoverability | `ALIGNED` | Four existing flows preserved; explicit pre-entry gate clarifies when Campaign durability is useful. |
| shipped `golden-paths-v1.md` reference | Agent-facing Campaign composition | `ALIGNED` | Mirrors the same proportional entry guidance without becoming a router. |
| legacy `SKILL.md.template` | Historical compatibility only | `ALIGNED / RETIRED-AS-AUTHORITY` | Old Phase-1 fog-to-workflow routing instructions were removed; file now points to canonical `SKILL.md` and current references. |
| Campaign initialization | Durable continuation state | `ALIGNED` | Records target identity/state without inferring uncertainty, responsibility, capability, or authority. |
| Campaign preflight | Mechanical Campaign integrity | `ALIGNED` | Still reports mechanical facts only; `preflight PASS != should proceed`. |
| Campaign Doctor | Mechanical diagnosis | `ALIGNED` | Remains diagnostic and non-semantic. |
| Campaign inspect / explain / diff | Reconstruction / observability | `ALIGNED` | Read-only projections; no semantic next-action selection. |
| Resume Capsule / resume profiles | Continuation complexity | `ALIGNED` | Reconstruct durable state; tests assert no recommended next action. |
| Campaign capability context | Capability inspection after responsibility selection | `ALIGNED` | Availability/compatibility remains unranked and non-authoritative. |
| Artifact admission / evidence lineage | Durable evidence integrity | `ALIGNED` | Preserves provenance without turning admission into warrant. |
| Campaign provenance / graph | Review and reconstruction burden | `ALIGNED` | Projects recorded structure without asserting semantic correctness. |
| Campaign handoff / transfer / rebinding | Cross-context continuation | `ALIGNED` | Preserves/verifies state; does not discover repositories or bless drift. |
| Campaign completion / archive | Reconstructible terminal state | `ALIGNED` | `campaign close` remains the semantic terminal decision; closeout mechanically summarizes an already-terminal Campaign. |
| `output-reconciler` | Consequential completed-work claims | `ALIGNED` | Trigger remains a material handoff or consequential claim, not every tiny edit. |
| `repair-verifier` | Consequential finding-specific closure | `ALIGNED` | Remains finding-specific and asks whether the original diagnosis is closed under fresh observation. |
| Strategy inspect / diff / handoff | Level-3 repository-evolution complexity | `ALIGNED` | Transports already-authored strategic state/decisions without selecting the Strategic Frontier or next responsibility. |
| Multi-repository Campaign surfaces | Repository breadth + continuation complexity | `ALIGNED` | Explicit targets/relations and mechanical checks remain non-inferential. |

## 5. Package 1 — product audit

Package 1 established that the material mismatch was presentation rather than runtime behavior.

Integrated through PR #359:

- exact candidate head: `f73794e5fb873210ac24500ad37f7e0fd94e3722`;
- merged result: `9ac6dd22696d6d8cc4e321dd70f7dc1f31d28616`;
- Product Validation #916: PASS;
- Release Candidate Distribution #92: PASS.

The audit preserved the separate Documentation Entry-Point Consolidation v1 work already integrated on `main` and narrowed the issue from entry-point ownership to **proportional usage sequencing**.

## 6. Package 2 — shipped guidance alignment

Package 2 aligned the product surfaces identified by the audit:

- `skills/using-sensemaking/SKILL.md` now teaches the five contextual factors compactly while preserving the responsibility-first loop;
- `skills/using-sensemaking/references/adaptive-guidance-v0.md` provides progressively loaded examples and anti-patterns;
- README and Getting Started are Sensemaking-first and Campaign-when-warranted;
- `docs/sensemaking-campaign.md` defines Campaign as the central durable Level-2 abstraction rather than a universal entry point;
- both Golden Path references describe Campaign composition and include a qualitative pre-entry gate;
- no runtime code, API, schema, Campaign flow projection, scoring model, or automatic routing was added.

Integrated through PR #360:

- exact candidate head: `6c99323e66771803d352b5d563e2aa65c085fa80`;
- merged result: `bce82e19101c4263437d97e7a53030e8e6b0ef64`;
- Product Validation #919: PASS;
- Release Candidate Distribution #94: PASS;
- installed-wheel/harness-adapter regression lane: PASS;
- repository/Skill contracts and strategic-state/candidate-direction validation: PASS.

### Emergent finding F6 — stale shipped template

While checking the complete `using-sensemaking` bundle, Package 2 found that `skills/using-sensemaking/SKILL.md.template` still contained obsolete Phase-1 instructions that translated fog classification into workflow routing. The repository build copies the complete root Skill tree into installed `skill_trees`, so that legacy file was distributed even though `SKILL.md` was canonical.

**Classification:** `PRESENTATION_MISALIGNED`, not a runtime-routing defect.

**Repair:** PR #360 retained the filename only as a compatibility pointer and removed its obsolete routing instructions. Installed-wheel qualification passed on the exact repaired head.

## 7. Package 3 — fresh mechanics reassessment

After PR #360 was integrated, the mechanics were re-checked from fresh `main` instead of inferring alignment from documentation changes.

| Question | Fresh result | Evidence class |
| --- | --- | --- |
| Can Skills operate without Campaign state? | `YES` | Skill invocation/distribution remains independent; Campaign is optional guidance rather than a prerequisite. |
| Can `repo-sensemaker` operate independently? | `YES` | Its Skill contract remains diagnostic and bounded to a repository sensemaking brief; no Campaign requirement or implementation authority was introduced. |
| Is Campaign optional until durable continuation is useful? | `YES` | No runtime/API/schema change in PR #360; Campaign initialization remains an explicit caller action. |
| Do preflight and Doctor remain mechanical? | `YES` | Preflight implementation explicitly refuses responsibility inference, capability ranking, or a should-proceed conclusion; Doctor remains a bounded mechanical diagnostic. |
| Do Resume surfaces avoid recommending action? | `YES` | Resume Capsule contract and tests explicitly exclude `recommended_next_action` / semantic recommendations. |
| Do Golden Paths remain static navigation? | `YES` | CLI payloads retain `flow_selected_by_tool=false`, `steps_executed=false`, `responsibility_selected=false`, and `capability_selected=false`; tests cover these invariants. |
| Is reconciliation selective for consequential claims? | `YES` | Canonical operating workflow still triggers output reconciliation for a material handoff or consequential claim, not every tiny edit. |
| Is repair verification finding-specific? | `YES` | `repair-verifier` remains scoped to asking whether an original diagnosis reproduces after the claimed repair. |
| Does completion require an explicit semantic terminal decision? | `YES` | Completion tests require an existing terminal decision before closeout; the CLI explicitly reports that completion receipts do not close a Campaign or prove the terminal decision correct. |

### Package 3 conclusion

```text
BEHAVIOR_MISALIGNED findings = 0
runtime/API/schema fix warranted = NO
formal Campaign rigor tiers warranted = NO
Persona Model v1 warranted = NO
next package from this milestone = STOP
```

The correct Package 3 action is documentation/strategic closeout, not a runtime implementation package.

## 8. Beginner-first / expert-capable result

The shipped guidance now preserves the intended asymmetry:

```text
lower user supervision capability
-> more proactive scaffolding
-> not more mandatory visible machinery

higher user supervision capability
-> more concise explanation
-> same engineering invariants

higher desired delegation
-> agent resolves more repository-answerable questions
-> still inside granted authority
```

The product therefore remains beginner-first without creating a permanent beginner persona mode, and expert-capable without weakening evidence or authority discipline.

## 9. Candidate-reservoir disposition

Progressive Campaign Rigor tiers remain:

```text
LONG_HORIZON + REQUIRES_EVIDENCE
```

The reconciliation found that existing mechanics already permit proportional use and that the observed burden could be repaired through shipped guidance. That currently **weakens rather than strengthens** the case for formal `LIGHT / STANDARD / HEAVY` runtime modes.

Reopen only if normal use repeatedly demonstrates a behavior-level burden that aligned guidance cannot solve, for example:

- existing Campaign semantics mechanically force avoidable ceremony;
- a recurring consumer cannot express a mechanically bounded qualification profile without manual reconstruction;
- continuation requirements repeatedly exceed what the single Campaign model can represent without semantic duplication.

A future observation must still pass Level-3 responsibility selection before implementation.

## 10. Explicit non-goals preserved

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

## 11. Final disposition

Persona & Adaptive Guidance — Existing Product Reconciliation v0 is complete when this closeout is integrated and exact-head repository qualification passes.

The milestone demonstrates a useful design discipline:

```text
product-theory reinterpretation
-> audit existing product
-> fix presentation mismatches
-> re-check mechanics
-> no behavior gap
-> STOP
```

The next step is **normal repository use**, not another adaptive-guidance construction wave. Future work should come from concrete repository/product pressure or explicit owner direction and must remain inside the existing evidence and authority boundaries.
