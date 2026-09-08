# Status

**Version:** 0.2.2  
**Last updated:** 2026-09-08  
**Current phase:** Productization / implementation  
**Primary program:** Sensemaking Skills v0.3 campaign-based productization  
**Current frontier:** P7 — durable handoff/resume UX

This is the repository's living status summary. It points at authoritative design sources and current implementation direction; it is not itself an ADR or an execution authorization.

## What the product is

Sensemaking Skills is an **agent-native engineering sensemaking and control layer for software-engineering agents**.

The central product abstraction is the **Sensemaking Campaign**: a durable engineering decision process carried across agent sessions. The canonical product model is:

[`docs/sensemaking-campaign.md`](docs/sensemaking-campaign.md)

The active coding agent owns the semantic control loop. Sensemaking constrains and preserves that loop with repository evidence, bounded responsibilities, durable artifacts, deterministic validators, reconciliation, repair verification, authority boundaries, typed campaign state, and reconstructible transition history.

It is not a centralized semantic router, autonomous project manager, or universal multi-agent orchestrator.

Current architectural authority remains grounded in the accepted ADRs and current operating docs, especially:

- ADR 0013 — the active coding agent owns the top-level control loop;
- ADR 0014 — the evidence-grounded repository-sensemaking brief is the ratified core product boundary and automatic downstream routing is deferred;
- ADR 0015 addendum — representation sufficiency / MODEL_WARRANT;
- ADR 0023 — experiment authorization separation;
- ADR 0026 / 0027 — execution authority is distinct from recommendation/selection, and workflow catalog identity is distinct from liveness;
- `docs/sensemaking-campaign.md` — canonical Campaign product model;
- `docs/agent-native-operating-workflow.md` — current operating map;
- `docs/decision-orchestration-boundary.md` — semantic decision vs deterministic orchestration boundary.

## Owner productization decision — 2026-09-08

The repository moved from **research/experiment-first development** to **implementation/productization-first development**.

The default development loop is now:

```text
identify a user-visible capability
→ implement the smallest complete vertical slice
→ validate deterministically
→ dogfood in ordinary engineering use
→ repair observed friction
→ ship the slice
```

Formal experiments are no longer the normal next step. They are reserved for consequential product uncertainties that ordinary implementation and dogfood evidence cannot resolve.

The versioned active delivery plan is:

[`docs/productization-v0.3.md`](docs/productization-v0.3.md)

## Integrated implementation baseline

The productization pivot began at:

```text
main@5c2c807542f7e150d4a031430f59e297ed816b24
```

The current integrated implementation frontier after P6 is:

```text
main@488358afaf9e34e58d467df9493b89ba281ea344
```

That merge has parents `b4c3c1205cb821038aa648e1ab5f7bf08109f81c` and exact-qualified P6 head `08fda8ade6d43dd8832288b402f83d8da4d1a9ad`, and its tree is exactly the qualified P6 tree `ad121976c863953f3ee2a332187bc0fb2b67c814`.

## What is implemented

### P0 — Productization pivot — MERGED

- implementation-first direction is durable;
- formal experiments are no longer the default active program;
- prior research remains preserved as evidence with its actual claim ceilings.

### P1 — Durable campaign workspace — MERGED

- isolated file-backed Campaign workspace;
- strict typed campaign load/dump boundaries;
- atomic current-state replacement;
- append-only transitions and append-preserving trace;
- fail-closed physical path containment;
- non-overwrite initialization and campaign identity checks.

### P2 — Campaign service — MERGED

- deterministic lifecycle service;
- recoverable transition + state commit intent;
- validation and reconstruction;
- defer/terminate primitives;
- handoff generation and resume/reconstruction;
- transition/state digest binding.

### P3 — Campaign CLI foundation — MERGED

Implemented:

```text
sensemaking-skills campaign init
sensemaking-skills campaign status
sensemaking-skills campaign validate
sensemaking-skills campaign history
```

Read-oriented commands expose human-readable and JSON surfaces with stable failure classes.

### P4 — Validated artifact ingestion — MERGED

Implemented:

```text
sensemaking-skills campaign ingest
```

P4 establishes the trust boundary:

```text
artifact bytes
→ canonical validator router
→ selected validator
→ valid=true
→ content-addressed artifact
→ append-only admission receipt
→ campaign evidence
```

Therefore:

```text
file exists
!= validated artifact
!= admitted campaign evidence
```

Files merely placed under `artifacts/` are not automatically evidence. Raw `evidence/` semantics remain explicitly separate.

### P5 — Agent-authored decisions — MERGED

Implemented:

```text
sensemaking-skills campaign advance
sensemaking-skills campaign defer
sensemaking-skills campaign close
```

P5 preserves the semantic control boundary explicitly:

```text
admitted / durable evidence
        ↓
AGENT judgment
        ↓
typed decision contract
        ↓
existing CampaignService primitive
        ↓
recoverable state + transition + trace
```

Key properties:

- `advance` persists exactly one explicit next responsibility supplied by the agent;
- trigger evidence must already satisfy the campaign evidence contract and is bound to the installing transition;
- `defer` preserves its reason and optional reopening contract;
- `close` persists an explicit terminal classification and later advance fails closed;
- JSON surfaces expose exact replacement state plus committed transition;
- no P5 command ranks/selects capabilities, interprets artifact semantics, grants authority, or creates a second persistence path.

See [`docs/campaign-decisions.md`](docs/campaign-decisions.md).

### P6 — Real capability registry — MERGED

Implemented:

```text
sensemaking-skills campaign capabilities
```

P6 exposes real declared Skill/workflow capability metadata without semantic routing:

```text
active responsibility
        ↓
AGENT supplies responsibility classification
        ↓
deterministic capability lookup
        ↓
unranked candidates + availability + required-authority metadata
        ↓
AGENT chooses one / none / ordinary work
```

Key properties:

- catalog membership, runtime availability, and execution authority remain separate facts;
- current agent-native Skills are `external` rather than falsely claimed installed;
- workflow identities/liveness are cross-checked and `compatibility_only` workflows are unavailable;
- live Skill identities must actually ship;
- Skill output and mutation declarations are qualification-checked against canonical metadata;
- malformed catalog data fails closed;
- an unmapped responsibility classification returns an honest empty candidate set;
- no P6 surface ranks, recommends, selects, invokes, or authorizes a capability.

See [`docs/capability-registry.md`](docs/capability-registry.md).

## Current productization objective

The v0.3 north-star outcome is:

> A coding agent can start a durable Sensemaking Campaign on a real repository, consume validated agent-native diagnostic artifacts, record the warranted responsibility and authority, inspect available capabilities, perform bounded work, validate/reconcile the result, hand the campaign to a fresh agent, and continue or terminate without relying on prior conversation memory.

The intended lifecycle is:

```text
user goal
→ campaign init
→ repository sensemaking
→ validated artifact admission
→ agent authors responsibility/authority decision
→ capability inspection
→ agent-selected bounded capability / ordinary coding
→ validation / reconciliation
→ durable transition
→ handoff / continue / stop
```

## Current implementation frontier — P7

The next bounded slice is **P7 — Durable handoff/resume UX**.

The purpose is to productize the existing P2 handoff-generation and reconstruction primitives so a fresh coding-agent context can safely resume a Campaign from durable repository-independent state rather than prior chat memory.

Required control shape:

```text
current durable campaign state
        ↓
deterministic handoff generation
        ↓
self-contained reconstruction pointers + integrity bindings
        ↓
fresh agent / process
        ↓
strict resume validation
        ↓
AGENT reconstructs context and decides next action
```

P7 should reuse the canonical `CampaignHandoff` contract and existing `CampaignService.generate_handoff()` / `CampaignService.resume()` primitives. It should add first-class user surfaces such as:

```text
sensemaking-skills campaign handoff
sensemaking-skills campaign resume
```

P7 must preserve:

- current state remains the authority; the handoff is not a second source of truth;
- stale or tampered handoffs fail closed;
- handoff/resume does not infer unstored conversation context;
- active responsibility, authority, evidence refs, deferrals, terminal state, and transition history remain reconstructible;
- handoff generation and resume do not recommend a next responsibility/capability or grant authority;
- a genuinely fresh process can continue from durable campaign data without the old conversation.

## Semantic-control invariant

The implementation must preserve this separation:

```text
Agent:
  What does the evidence mean?
  Which responsibility is warranted?
  How should that responsibility be classified for capability inspection?
  Which available capability should be selected?
  Does the result justify advance, defer, or close?

Deterministic machinery:
  Is the representation valid?
  Is state persisted safely?
  Does referenced evidence satisfy the current evidence contract?
  What registered capabilities declare compatibility?
  What are their mechanical availability/liveness properties?
  What authority metadata is declared?
  Is the transition structurally reconstructible?
  Does the handoff bind exactly to the reconstructible current state?
```

Therefore:

```text
validator passed != conclusion is true
warranted responsibility != available capability
available capability != authorized capability
recommendation != execution authority
handoff != semantic recommendation
```

And:

```text
Campaign Controller != semantic router
```

## Remaining v0.3 sequence

1. **P7 — Durable handoff/resume UX** — CURRENT.
2. **P8 — Artifact/evidence lineage**.
3. **P9 — Reconciliation lifecycle**.
4. **P10 — Harness adapters**.
5. **P11 — External golden-path qualification and v0.3 release**.

## Research and experiment disposition

Prior research remains useful evidence and is preserved. It is no longer the default active product program.

### EXP-0006 / Empirical Skill Qualification v1

The experiment stopped at the actual completed boundary under the owner's productization pivot.

Preserve:

- the three D attempts and their exact outcomes;
- the frozen Q/T holdout identity and integrity record;
- the candidate-context contamination audit;
- the fact that no candidate was authored before the contamination event;
- all existing exploratory/non-canonical claim ceilings.

Do not manufacture a Skill candidate or continue Q/T execution merely to complete the experimental mechanism. Do not relabel incomplete work as a completed scientific conclusion.

### Goal A and other research lanes

Goal A, the standing normal-use evidence lane, control-model studies, and other research artifacts remain available as evidence/research surfaces. They are not the primary development queue unless a later owner decision explicitly reactivates them.

## Explicit non-goals for v0.3

Do not build by default:

- centralized semantic routing;
- HTN/generic planning;
- Skill ranking;
- critic/voting swarms;
- self-modifying Skills;
- autonomous SkillOpt optimization;
- campaign server/database/cloud backend;
- universal semantic truth validation;
- automatic external mutation authority;
- full multi-repository campaign control.

## Definition of v0.3 success

The first campaign-based release is successful when a real agent can:

```text
start
→ consume diagnosis
→ admit validated artifact
→ record responsibility
→ bind authority
→ inspect available capability
→ record work evidence
→ transition
→ handoff
→ resume in a fresh context
→ stop honestly
```

with deterministic state reconstruction and without requiring the prior conversation as hidden input or manually repairing campaign/artifact state.

## Where to look

| Topic | Source |
|---|---|
| Product definition, principles, authority model | `CONTEXT.md` |
| Canonical Sensemaking Campaign product model | `docs/sensemaking-campaign.md` |
| Active v0.3 delivery plan | `docs/productization-v0.3.md` |
| Agent-authored campaign decisions | `docs/campaign-decisions.md` |
| Capability registry inspection | `docs/capability-registry.md` |
| SkillOpt influence/adaptation and research boundary | `docs/research/skillopt-adaptation.md` |
| Agent-native operating model | `docs/agent-native-operating-workflow.md` |
| Decision vs orchestration boundary | `docs/decision-orchestration-boundary.md` |
| Campaign semantic contract | `docs/campaign-semantics.md`, `src/sensemaking_skills/campaign_semantics/` |
| Validated artifact ingestion | `docs/artifact-ingestion.md` |
| Workflow catalog/liveness | `docs/workflow-system-disposition.md`, ADR 0027 |
| Design decisions | `docs/adr/` — always read each ADR's status |
| Historical research/evidence | `experiments/`, `docs/research/`, `docs/campaigns/` |
| Installation and usage | `README.md`, `GETTING_STARTED.md`, `INSTALLATION.md` |
