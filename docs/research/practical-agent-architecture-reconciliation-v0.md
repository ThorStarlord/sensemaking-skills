# Practical Agent Architecture v0 — Sensemaking Reconciliation

**Status:** bounded repository reconciliation / non-authoritative  
**Date:** 2026-09-17  
**Authority:** research/reconciliation only; does not modify ADR 0029, runtime authority, schema, public API, Campaign semantics, or product strategy  
**Design:** `../superpowers/specs/2026-09-17-practical-agent-architecture-v0-design.md`

## 1. Research question

> **Which parts of Practical Agent Architecture v0 are already satisfied by current Sensemaking, which require only agent-facing guidance, and which—if any—expose a genuine representation or deterministic-assurance gap?**

This reconciliation treats absence of a first-class runtime component as **not a gap by itself**.

The architecture zones are ownership boundaries. They do not require one service, class, schema, or process per concept.

## 2. Disposition vocabulary

This reconciliation uses exactly these dispositions:

```text
ALREADY_SATISFIED
GUIDANCE_GAP
DURABLE_STATE_GAP
DETERMINISTIC_ASSURANCE_GAP
OUTSIDE_PRODUCT
UNRESOLVED
```

The standard for a runtime/state/assurance gap is deliberately stronger than “the design names a concept.” A gap exists only when current Sensemaking cannot preserve the intended decision/control behavior through its existing agent guidance, durable state, validation, or external orchestration boundary.

## 3. Five-zone coverage

| Zone | Current Sensemaking surfaces | Disposition | Evidence-based conclusion |
| --- | --- | --- | --- |
| **Semantic Agency Plane** | `skills/using-sensemaking/SKILL.md`; Semantic Reasoning Model; Level-3 Strategic Outer Loop; Level-4 Product Thesis guidance; adaptive guidance | `GUIDANCE_GAP` | Core semantic ownership already belongs to the active agent. The new architecture mainly clarifies explicit warrant targets/dependencies plus challenge/exploration and resource-aware stopping. |
| **Warrant / Decision Control** | recursive `update warrant` loop in `using-sensemaking`; `warrant-as-control-primitive.md`; `uncertainty-selection.md`; decision/closure/authority distinctions | `GUIDANCE_GAP` | Warrant already exists as a product-design concept and operating verb, but the canonical bootstrap does not yet teach the compact target/dependency form or the distinction between challenge and exploration. |
| **Durable Decision Substrate** | CampaignState; Responsibility; Uncertainty; Authority; TransitionRecord; CampaignHandoff; semantic-state companion; STATUS/Strategic Frontier; target snapshot/currentness; ADRs | `ALREADY_SATISFIED` | Current repository-domain continuation can preserve explicit consequential decision state without a new generic cognitive-state schema. Existing additive companions also show the repository can extend persistence without rewriting CampaignState. |
| **Deterministic Assurance** | schemas, validators, hashes, target identity/currentness, evidence admission, reference integrity, transition integrity, CI, artifact digests | `ALREADY_SATISFIED` | The architecture-level boundary already exists and ADR 0029 explicitly states `mechanically valid != semantically correct`. No new generic assurance service is warranted. |
| **Execution / Orchestration** | Skills/tools/workflows; Campaign bounded execution; agent-native workflow guidance; decision-versus-orchestration research and canonical boundary | `GUIDANCE_GAP` | The architectural ownership boundary is already explicit: decision selects work, orchestration coordinates work, evidence returns upward. Canonical agent guidance can make failed/delegated result handling more explicit. |
| **Authority / Governance** | Authority semantics; owner-ratified Level 4; protected merge/release/publication boundaries; strategic state authority vocabulary | `ALREADY_SATISFIED` | Sensemaking already separates capability, recommendation, authorization, execution, ratification, and closure. Practical Agent Architecture should reuse this rather than add another authority layer. |

## 4. Surface-by-surface reconciliation

### 4.1 Warrant target and dependencies

**Current support**

`skills/using-sensemaking/SKILL.md` already uses:

```text
ground evidence
-> validate mechanics
-> update warrant
-> continue / stop / escalate / verify / ask owner
```

`docs/research/warrant-as-control-primitive.md` already defines warrant as target-specific and defeasible and explicitly rejects:

- scalar confidence;
- permission-token semantics;
- synonymy with authority;
- automatic propagation from one target to another.

`docs/research/uncertainty-selection.md` already defines the nearest decision-changing uncertainty as the earliest unresolved premise capable of invalidating or materially redirecting the contemplated action.

**Observed gap**

The canonical agent bootstrap does not yet combine these into one explicit operational prompt:

```text
What exactly am I trying to justify now?
What must be true for that target to be warranted?
Which unresolved premise could materially change the next action?
```

**Decision effect**

Making the target explicit reduces hidden jumps from:

```text
evidence -> interesting conclusion -> action
```

and instead preserves:

```text
evidence -> target-specific warrant -> bounded action / inquiry / stop
```

**Disposition:** `GUIDANCE_GAP`

**Smallest warranted intervention:** add explicit warrant-target/dependency guidance to the using-sensemaking reference/bootstrap.

**Rejected heavier intervention:** no `Warrant` Python class, score, enum, state-machine node, or persistent `warrant_gap` field.

---

### 4.2 Adversarial challenge

**Current support**

Current Sensemaking already contains:

- contradiction detection;
- counter-evidence;
- falsification;
- invalidation evidence;
- repair verification;
- architectural review;
- result/claim reconciliation.

**Observed gap**

These mechanisms are distributed and purpose-specific. The canonical bootstrap does not teach a compact cross-cutting rule for when to challenge a consequential frame, claim, forecast, option, or closure decision.

**Decision effect**

A bounded challenge rule can reduce premature confidence without making criticism mandatory on every task.

**Disposition:** `GUIDANCE_GAP`

**Smallest warranted intervention:** document qualitative challenge triggers and require challenge output to return as evidence rather than authority.

**Rejected heavier intervention:** no automatic critic process, critic quorum, majority vote, veto service, or adversarial score.

---

### 4.3 Exploration / alternative generation

**Current support**

Sensemaking already uses:

- Strategic Frontier candidates;
- Level-4 alternatives;
- competing responsibilities;
- uncertainty mapping;
- architectural review;
- problem framing.

**Observed gap**

Current guidance is stronger on challenging an existing responsibility than on recognizing option poverty:

> a decision can be wrong because the available options are incomplete even when the comparison among those options is reasonable.

**Decision effect**

Explicit exploration guidance can help when:

- only one consequential option exists;
- repeated attempts fail;
- the frame is unstable;
- local optimization may be hiding a better responsibility boundary.

**Disposition:** `GUIDANCE_GAP`

**Smallest warranted intervention:** explain exploration as a distinct semantic operator and give qualitative triggers.

**Rejected heavier intervention:** no automatic frontier generator, search budget engine, option ranker, or deterministic “novelty” mechanism.

---

### 4.4 Resource-aware stopping

**Current support**

Existing doctrine already includes:

- cheapest sufficient evidence;
- smallest warranted intervention;
- stop when remaining uncertainty would not change action;
- consider consequence, reversibility, deferral cost, and evidence cost;
- Campaign only when continuation complexity warrants it.

**Observed gap**

The current bootstrap does not state the general metareasoning principle as directly as the Practical Agent Architecture:

```text
continue reasoning when expected decision improvement
is worth more than reasoning + information + delay + opportunity cost
```

**Decision effect**

This clarification helps prevent both:

- over-investigation on cheap reversible tasks;
- under-investigation on consequential irreversible decisions.

**Disposition:** `GUIDANCE_GAP`

**Smallest warranted intervention:** qualitative stopping guidance only.

**Rejected heavier intervention:** no numeric VOI/VOC calculation, decision-cost score, or automatic threshold.

---

### 4.5 Delegation / subagent evidence return

**Current support**

Sensemaking already distinguishes:

```text
warranted responsibility
!= available capability
!= authorized capability
```

and treats Skills/tools/workflows as ways to perform an already-selected responsibility.

The canonical decision/orchestration law is already:

> **Decision selects the work. Orchestration coordinates the work. Evidence determines what becomes warranted next.**

**Observed gap**

The canonical bootstrap can state more explicitly that:

```text
worker result
-> evidence for the active semantic controller

worker recommendation
!= parent decision

worker success
!= global closure

retry/fallback policy
!= permission to change responsibility
```

**Decision effect**

This matters as more work is delegated to subagents, coding agents, schedulers, and software-factory infrastructure.

**Disposition:** `GUIDANCE_GAP`

**Smallest warranted intervention:** add the evidence-return rule to the practical reference and canonical bootstrap.

**Rejected heavier intervention:** no new multi-agent supervisor runtime, agent-voting mechanism, job scheduler, or worker protocol inside Sensemaking.

---

### 4.6 Durable decision state

**Current support**

The repository already has typed and durable structures for repository-domain continuation:

- `CampaignState`;
- `Responsibility`;
- `Uncertainty`;
- `Authority`;
- `TransitionRecord`;
- `CampaignHandoff`;
- evidence/artifact references;
- target snapshots/currentness;
- uncertainty history/relationships;
- semantic-state companions;
- Strategic Frontier / STATUS;
- ADRs and owner-ratified decisions.

Importantly, the repository already uses additive companion artifacts when a new persistence need does not belong in `CampaignState`.

**Observed gap**

No current repository decision demonstrates that a new domain-general cognitive-state object is required.

The Practical Agent Architecture names concepts such as commitments, rationale, stop/reopen conditions, and beliefs, but current Sensemaking already stores the repository-specific subset that is worth reconstructing.

**Decision effect**

Adding a generic state schema now would increase ontology and compatibility surface without resolving an observed reconstruction failure.

**Disposition:** `ALREADY_SATISFIED`

**Smallest warranted intervention:** no state/schema change. Guidance should say to use current Campaign/strategic/semantic durable surfaces when continuation warrants them.

**Rejected heavier intervention:** universal `AgentState`, `WarrantState`, belief database, or Campaign schema revision.

---

### 4.7 Deterministic assurance

**Current support**

ADR 0029 already establishes the permanent boundary:

```text
mechanically valid != semantically correct
```

Current deterministic surfaces include:

- schemas;
- validators;
- digests;
- evidence/reference resolution;
- target identity/currentness;
- transition integrity;
- capability declaration lookup;
- artifact admission;
- CI and exact-head qualification.

**Observed gap**

No architecture-wide deterministic check is missing.

Future mechanically decidable gaps may emerge from concrete work, but the Practical Agent Architecture does not itself create one.

**Decision effect**

Adding generic “agency assurance” machinery would risk semantic promotion from representation to decision.

**Disposition:** `ALREADY_SATISFIED`

**Smallest warranted intervention:** no deterministic machinery.

**Rejected heavier intervention:** general warrant validator, semantic sufficiency validator, deterministic decision checker, or universal agency conformance engine.

---

### 4.8 Orchestration interface

**Current support**

Sensemaking already treats:

- registered workflows as bounded subgraphs;
- Campaign execution as bounded coordination after responsibility selection;
- retries/waits as execution policy;
- failures/results as evidence returned to the active agent.

Existing research found the decision/orchestration distinction coherent across bounded repository-grounded episodes.

**Observed gap**

The interface is conceptually present but can be made easier for agents to remember:

```text
selected responsibility
+ authority envelope
+ expected evidence
-> execution/orchestration
-> result/evidence
-> semantic reassessment
```

**Decision effect**

Clarification reduces the risk that orchestration fallback silently selects a different engineering responsibility.

**Disposition:** `GUIDANCE_GAP` for the agent-facing interface; architecture itself is already satisfied.

**Smallest warranted intervention:** guidance only.

**Rejected heavier intervention:** generic orchestration protocol/runtime in Sensemaking.

---

### 4.9 Authority / governance

**Current support**

Current product doctrine explicitly distinguishes:

```text
finding != authorization to fix
recommendation != owner decision
capability available != capability selected
validated != owner-ratified
promoted != merged
```

Level 4 is owner-ratified product-thesis authority. Strategic state distinguishes:

```text
AUTHORIZED NOW
OWNER-RATIFIED DECISIONS REQUIRED
EXTERNAL AUTHORITY REQUIRED
```

**Observed gap**

None at the architecture level.

**Disposition:** `ALREADY_SATISFIED`

**Smallest warranted intervention:** reference existing authority rules from the practical-agent guidance.

**Rejected heavier intervention:** new authority engine, policy score, or inferred permission layer.

## 5. Scenario pressure tests

### Scenario A — trivial reversible engineering task

**Need:** keep ceremony low.

**Current support:** adaptive guidance already says clear + local + low consequence + one context → direct bounded work + relevant tests.

**New guidance value:** warrant can remain implicit unless a consequential decision is actually blocked.

**New persistent state required?** No.

**New deterministic machinery required?** No.

**Result:** current product supports the scenario; practical guidance clarifies that the architecture should collapse away.

---

### Scenario B — ambiguous repository responsibility

**Need:** make the live decision and uncertainty explicit before implementation.

**Current support:** repository sensemaking, Decision Being Supported, consequential uncertainty, responsibility-before-Skill.

**New guidance value:** explicitly name the warrant target/dependencies.

**New persistent state required?** No, unless continuation complexity independently warrants Campaign.

**New deterministic machinery required?** No.

**Result:** guidance improves the interface; current structures suffice.

---

### Scenario C — long-running multi-agent repository change

**Need:** parent semantic control, bounded workers, durable continuation, evidence return.

**Current support:** Campaign state/handoff, explicit responsibility, capability/authority, agent-native orchestration boundary.

**New guidance value:** worker result → evidence → parent reassessment becomes explicit.

**New persistent state required?** Existing Campaign state is sufficient for current repository-domain needs.

**New deterministic machinery required?** No architecture-wide addition.

**Result:** guidance-only gap.

---

### Scenario D — strategic repository choice

**Need:** alternatives, evaluation, challenge, no deterministic ranking.

**Current support:** Strategic Frontier, Level-3 qualitative lenses, decision-changing uncertainty, smallest warranted intervention.

**New guidance value:** distinguish option generation/exploration from challenge and comparison.

**New persistent state required?** Existing strategic state.

**New deterministic machinery required?** No.

**Result:** guidance-only clarification.

---

### Scenario E — product-thesis contradiction

**Need:** evidence ascends only as far as necessary; Level-4 authority remains explicit.

**Current support:** Thesis Tension, Level-4 review, `REAFFIRM / REINTERPRET / REVISE / RETIRE / SUPERSEDE`, owner ratification.

**New guidance value:** none requiring new machinery; practical reference can restate minimum-necessary ascent.

**New persistent state required?** Existing product strategy/ADR/state surfaces.

**New deterministic machinery required?** No.

**Result:** already satisfied.

---

### Scenario F — external protected action

**Need:** technical warrant without execution authority.

**Current support:** existing authority doctrine and protected merge/release/publication boundaries.

**New guidance value:** warrant-target wording makes the distinction easier to state.

**New persistent state required?** No generic addition.

**New deterministic machinery required?** Existing approval-reference validation when applicable.

**Result:** already satisfied with guidance reinforcement.

---

### Scenario G — failed worker/tool

**Need:** failed execution returns evidence rather than silently selecting new responsibility.

**Current support:** decision/orchestration boundary and agent semantic reassessment.

**New guidance value:** explicitly teach:

```text
execution failure -> evidence -> semantic reassessment
```

**New persistent state required?** Only existing evidence/transition state if continuation is durable.

**New deterministic machinery required?** No.

**Result:** guidance-only gap.

---

### Scenario H — adversarial review

**Need:** critic supplies counter-evidence/alternatives without automatic authority.

**Current support:** several specialized review/falsification mechanisms.

**New guidance value:** generic trigger/ownership rule.

**New persistent state required?** Only material challenge evidence/results when decision-relevant.

**New deterministic machinery required?** No.

**Result:** guidance-only gap.

## 6. Implementation disposition

### `GUIDANCE_ONLY_WARRANTED`

The repository evidence does not establish a durable-state, deterministic-assurance, runtime, schema, or public-API gap.

The smallest warranted implementation package is:

1. create a detailed Practical Agent Architecture agent reference under `skills/using-sensemaking/references/`;
2. integrate a compact warrant/challenge/exploration/delegation/stopping layer into `skills/using-sensemaking/SKILL.md`;
3. add at most one non-duplicative adaptive-guidance clarification if needed after the canonical Skill edit.

## 7. Explicitly declined work

This reconciliation does **not** warrant:

- Campaign schema changes;
- a new `AgentState`;
- a new `Warrant` Python type;
- a `warrant_gap` field;
- new semantic decision validators;
- new public API;
- a planner/runtime;
- `StrategicPlanner`;
- `OuterLoopEngine`;
- automatic critic orchestration;
- critic voting;
- automatic option generation/ranking;
- automatic warrant scoring;
- automatic Skill selection;
- automatic Campaign creation;
- product-boundary revision.

## 8. Evidence ceiling

This reconciliation establishes only a repository-design conclusion:

> Current Sensemaking already contains the principal control, durability, assurance, orchestration, and authority boundaries needed to express Practical Agent Architecture v0 for repository-domain work. The remaining near-term gap is primarily how those boundaries are taught to the active agent.

It does not establish:

- optimality of the architecture;
- cross-domain runtime completeness;
- general autonomous-agent capability;
- comparative superiority;
- that no future state/assurance gap can emerge.

## 9. Next authorized package

Because the disposition is `GUIDANCE_ONLY_WARRANTED`, the next bounded implementation is limited to:

```text
agent-facing practical architecture reference
+
compact using-sensemaking integration
+
optional non-duplicative adaptive-guidance clarification
```

Any discovery that requires Python/runtime/schema/API changes should stop this package and return to architectural review.
