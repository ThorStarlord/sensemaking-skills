# Persona & Adaptive Guidance Model v0 — Design Preflight

**Status:** owner-ratified Level-4 reinterpretation preflight  
**Date:** 2026-09-11  
**Level-4 disposition:** `REINTERPRET`  
**Runtime impact:** none  
**Schema impact:** none  
**Empirical claim impact:** none

## 1. Decision

Clarify the existing Sensemaking Skills product thesis around the user who most benefits from delegated repository judgment and around the factors that should influence how much guidance, rigor, and durability the active coding agent uses.

The current product purpose remains unchanged: Sensemaking exists to improve repository-level decisions when a capable coding agent cannot safely determine the correct next engineering responsibility from the user's request alone.

This change is a `REINTERPRET`, not a strategic pivot. The existing primary-user commitment already describes an AI-native repository owner who delegates consequential repository work without manually choosing every intermediate step. The clarified primary design persona is:

> **High-delegation agent-assisted builder / repository owner** — a person who can define desired product or repository outcomes and wants a capable coding agent to exercise substantial engineering judgment without requiring the user to identify every intermediate question, responsibility, or implementation step.

The design stance is **beginner-first, expert-capable**. A beginner may need the system because they cannot reliably supervise every engineering decision; an expert may need the same system because they prefer not to supervise every engineering decision.

## 2. Canonical distinctions

### Persona vs contextual expertise

The primary persona is relatively stable. Expertise is contextual.

```text
primary persona
!= permanent expertise classification
```

A user may be expert in one technology, unfamiliar with another, expert about product intent, and unfamiliar with the current repository. Sensemaking therefore must not persist or infer a global beginner/intermediate/expert identity merely from one task.

### Desired delegation vs granted authority

```text
desired delegation
!= granted authority
```

Desired delegation describes how much engineering judgment the user wants the agent to exercise independently. It never grants merge, release, deployment, destructive mutation, publication, or other reserved authority merely because the user asked the agent to "handle everything."

### Decision complexity vs technical difficulty

Decision complexity is the difficulty of determining the warranted repository responsibility. It may be high even when the eventual code change is small, and low even when implementation itself is technically difficult.

Relevant signals may include ambiguity, number of plausible responsibilities, repository breadth, architecture uncertainty, evidence-source breadth, and authority boundaries.

### Consequentiality vs complexity

Consequentiality is the cost, irreversibility, authority sensitivity, or damage potential of a wrong responsibility or action.

```text
decision complexity
!= consequentiality
```

A mechanically small action can still be highly consequential.

### Continuation complexity vs task size

Continuation complexity is how much repository-specific decision state must survive across time, sessions, agents, machines, or handoffs for work to remain reliable.

This is the factor most directly related to the value of durable Campaign state. Campaign is not justified merely because a task is large.

## 3. Opinionated guidance

Sensemaking is intentionally opinionated about engineering invariants and defaults. It should proactively account for considerations the user may not know or want to specify, including current repository reality, consequential uncertainty, scope, authority, existing implementation, evidence, validation, and justified closure.

The governing design principle is:

> **Opinionated about engineering invariants, adaptive about process, progressive in disclosure.**

Stable opinions include:

- do not fabricate evidence;
- repository reality outranks stale plans;
- resolve consequential uncertainty before unsupported commitment;
- choose responsibility before capability;
- recommendation does not imply authorization;
- validation does not establish semantic truth;
- implementation does not establish verified closure;
- solved questions should stop generating work.

Adaptive process choices include:

- whether repository sensemaking is materially useful;
- whether a Campaign is warranted;
- how much explanation/scaffolding to expose;
- how much evidence needs durable capture;
- whether formal reconciliation or repair verification is worth the cost;
- whether a handoff/resume surface is necessary.

Stable doctrine therefore does not imply mandatory ceremony.

## 4. Situational adaptation model

The following are semantic reasoning concepts for the active coding agent, not machine-scored variables:

| Factor | Meaning | Primarily influences |
| --- | --- | --- |
| **User supervision capability** | Contextual ability to spot omissions, understand repository constraints, and evaluate agent judgment | Scaffolding and explanation |
| **Desired delegation** | How much engineering judgment the user wants the agent to exercise independently | Agent decision ownership within authority |
| **Decision complexity** | Difficulty of determining the warranted repository responsibility | Sensemaking/investigation rigor |
| **Consequentiality** | Cost, irreversibility, authority sensitivity, or harm from a wrong action | Caution, evidence, validation, reconciliation |
| **Continuation complexity** | Amount of state that must survive contexts, agents, time, or transport | Campaign durability, provenance, handoff/resume |

Conceptual relationship:

```text
user supervision capability
        -> scaffolding

desired delegation
        -> agent decision ownership within granted authority

decision complexity + consequentiality
        -> process rigor

continuation complexity
        -> durability / Campaign value
```

These relationships are judgment prompts, not deterministic routing rules or thresholds.

## 5. Progressive disclosure

Beginner support should increase decision scaffolding without proportionally increasing visible system complexity.

Internally, the agent may use repository briefs, Campaign state, evidence, provenance, and reconciliation. Externally, a beginner may only need a concise explanation of the consequential issue and the recommended next action. An expert may prefer compact access to the underlying evidence and control surfaces.

```text
more guidance
!= more visible machinery
```

There is no `beginner_mode` or `expert_mode` in v0.

## 6. Campaign interpretation

Campaign exists to preserve repository-specific decision context when the problem's continuation complexity makes transient context unreliable.

Current preferred behavior is progressive without formal tiers:

```text
narrow + locally evidenced work
-> direct bounded work

ambiguous repository responsibility
-> repository sensemaking / bounded evidence

high consequence
-> stronger validation / reconciliation as warranted

high continuation complexity
-> Campaign / durable state / provenance / handoff
```

The existing idea of LIGHT/STANDARD/QUALIFIED Campaign rigor remains an evidence-gated candidate. This reinterpretation does not authorize formal rigor tiers.

## 7. Non-goals

This milestone does **not** authorize:

```text
user expertise scores
task/decision complexity scores
consequentiality scores
delegation enums persisted in Campaign
continuation-complexity scores
automatic persona inference
beginner/expert runtime modes
automatic Campaign thresholds
deterministic Skill routing
LLM competence grading
Campaign schema v3
a new Outer Loop runtime
StrategicPlanner / OuterLoopEngine
automatic authority inference
a behavioral or comparative experiment
new native-harness claims
```

No deterministic mechanism may convert these semantic concepts into an assertion about what the agent should do unless a narrower mechanically decidable contract is separately warranted and ratified.

## 8. Documentation changes authorized by this preflight

Reconcile only current authority/operating surfaces:

1. `docs/product-strategy.md` — primary persona, JTBD/value proposition, opinionated-guidance principle.
2. `docs/product-operating-model.md` — situational adaptation model and delegation/authority distinction.
3. `docs/agent-native-operating-workflow.md` — practical adaptive-ceremony guidance without routing thresholds.
4. `docs/strategic-candidate-directions.md` — reconcile Progressive Campaign Rigor against the v0 model without promotion.
5. `STATUS.md` — record the ratified Level-4 reinterpretation and perform Level-3 reconciliation.

Historical research, prior handoffs, and dated audits remain historically accurate and should not be rewritten merely to use the new wording.

## 9. Acceptance criteria

- Product purpose, external product boundary, strategic non-goals, Campaign schema, and empirical claim ceilings remain unchanged.
- Primary persona is clarified as high-delegation and agent-assisted, with beginner-first / expert-capable positioning.
- Opinionated guidance is explicit but does not imply paternalism, automatic routing, or authority expansion.
- User supervision capability, desired delegation, decision complexity, consequentiality, and continuation complexity are defined as contextual reasoning factors.
- Desired delegation is explicitly non-identical to granted authority.
- Campaign is associated primarily with continuation complexity, not mandatory use for every consequential task.
- Progressive disclosure is established without runtime persona modes.
- Strategic Candidate Directions remains non-authoritative and Progressive Campaign Rigor remains evidence-gated.
- `STATUS.md` preserves all Strategic State Contract v0 anchors and exactly one `THESIS_REVIEW_REQUIRED` marker.
- Repository validation passes without weakening existing validators.
- Post-merge Level-3 reassessment selects no follow-on construction package unless independent concrete pressure is observed.
