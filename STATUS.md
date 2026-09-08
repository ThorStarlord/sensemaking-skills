# Status

**Version:** 0.2.2  
**Last updated:** 2026-09-08  
**Current phase:** Productization / implementation  
**Primary program:** Sensemaking Skills v0.3 campaign-based productization  
**Current frontier:** P8 — artifact/evidence lineage

This is the repository's living status summary. It points at authoritative design sources and current implementation direction; it is not itself an ADR or an execution authorization.

## What the product is

Sensemaking Skills is an **agent-native engineering sensemaking and control layer for software-engineering agents**.

The central product abstraction is the **Sensemaking Campaign**: a durable engineering decision process carried across agent sessions. The canonical product model is [`docs/sensemaking-campaign.md`](docs/sensemaking-campaign.md).

The active coding agent owns semantic control. Deterministic machinery owns representation, persistence, validation, provenance, authority checks, structural reconstruction, and mechanically decidable integrity constraints. The system is not a centralized semantic router, autonomous project manager, or universal multi-agent orchestrator.

Current architectural authority remains grounded in accepted ADRs and current operating docs, especially:

- ADR 0013 — the active coding agent owns the top-level control loop;
- ADR 0014 — the evidence-grounded repository-sensemaking brief is the ratified core product boundary and automatic downstream routing is deferred;
- ADR 0015 addendum — representation sufficiency / MODEL_WARRANT;
- ADR 0023 — experiment authorization separation;
- ADR 0026 / 0027 — execution authority is distinct from recommendation/selection, and workflow catalog identity is distinct from liveness;
- `docs/sensemaking-campaign.md` — canonical Campaign product model;
- `docs/agent-native-operating-workflow.md` — current operating map;
- `docs/decision-orchestration-boundary.md` — semantic decision vs deterministic orchestration boundary.

## Owner productization decision — 2026-09-08

The repository moved from research/experiment-first development to implementation/productization-first development.

The default loop is:

```text
identify a user-visible capability
→ implement the smallest complete vertical slice
→ validate deterministically
→ dogfood in ordinary engineering use
→ repair observed friction
→ ship the slice
```

Formal experiments are reserved for consequential uncertainties that ordinary implementation and dogfood evidence cannot resolve.

The versioned delivery plan is [`docs/productization-v0.3.md`](docs/productization-v0.3.md).

## Integrated implementation baseline

The productization pivot began at:

```text
main@5c2c807542f7e150d4a031430f59e297ed816b24
```

The current integrated implementation frontier after P7 is:

```text
main@250a30ddd55e100a311a5ab17650a0f3176de605
```

That merge has parents:

```text
previous main
0f2dcd61951d3d9020c587b6f21996cb3517eec7

exact-qualified P7 head
f791deb1f7bce85af9e615d65534549a54cc2ae0
```

and its tree is exactly the qualified P7 tree:

```text
67f5f1527748c1a005f328c52c6185058989ad7e
```

## What is implemented

### P0 — Productization pivot — MERGED

- implementation-first direction is durable;
- formal experiments are no longer the default active program;
- prior research remains preserved with actual claim ceilings.

### P1 — Durable campaign workspace — MERGED

- isolated file-backed Campaign workspace;
- strict typed Campaign load/dump boundaries;
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

See [`docs/artifact-ingestion.md`](docs/artifact-ingestion.md).

### P5 — Agent-authored decisions — MERGED

Implemented:

```text
sensemaking-skills campaign advance
sensemaking-skills campaign defer
sensemaking-skills campaign close
```

P5 preserves:

```text
admitted / durable evidence
        ↓
AGENT judgment
        ↓
typed decision contract
        ↓
CampaignService
        ↓
recoverable state + transition + trace
```

Key properties:

- `advance` persists one explicit next responsibility supplied by the agent;
- trigger evidence must satisfy the Campaign evidence contract and is bound to the installing transition;
- `defer` preserves its reason and optional reopening contract;
- `close` persists an explicit terminal classification;
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
- malformed catalog data fails closed;
- no P6 surface ranks, recommends, selects, invokes, or authorizes a capability.

See [`docs/capability-registry.md`](docs/capability-registry.md).

### P7 — Durable handoff/resume UX — MERGED

Implemented:

```text
sensemaking-skills campaign handoff
sensemaking-skills campaign resume
```

P7 turns the existing P2 handoff/reconstruction primitives into a first-class fresh-context product surface:

```text
current durable Campaign
        ↓
canonical P2 handoff generation
        ↓
P7 reconstruction integrity binding
        ↓
fresh agent / fresh process
        ↓
canonical P2 reconstruction
        ↓
P7 binding verification
        ↓
AGENT decides what to do next
```

Key properties:

- semantic `CampaignHandoff` schema remains unchanged;
- the P7 SHA-256 reconstruction binding covers state, ordered transitions, trace, current evidence refs, optional policy, and handoff guidance;
- the binding is an integrity checksum under the existing filesystem trust model, not a signature or authority grant;
- valid-shape edits to handoff guidance fail closed;
- unbound legacy/P2 handoffs are not silently treated as P7-bound handoffs;
- a lifecycle transition invalidates the old handoff;
- terminal Campaigns resume honestly without fabricated executable work;
- fresh-process and installed-wheel qualification prove resume without prior chat context;
- handoff guidance is context only and is never recommendation, selection, invocation, or execution authority.

See [`docs/campaign-handoff-resume.md`](docs/campaign-handoff-resume.md).

## Current productization objective

The v0.3 north-star outcome is:

> A coding agent can start a durable Sensemaking Campaign on a real repository, consume validated diagnostic artifacts, record warranted responsibility and authority, inspect available capabilities, perform bounded work, validate/reconcile the result, hand the Campaign to a fresh agent, and continue or terminate without relying on prior conversation memory.

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
→ handoff
→ fresh-context resume
→ continue / stop
```

## Current implementation frontier — P8

The next bounded slice is **P8 — Artifact/evidence lineage**.

P8 should make the Campaign able to answer mechanically:

> Which immutable evidence supported this decision/transition, what is the exact identity of that evidence, and what provenance establishes how it entered the Campaign?

Required control shape:

```text
durable evidence / admitted artifact
        ↓
stable identity + digest + provenance
        ↓
agent-authored decision references evidence
        ↓
transition persists the consumption link
        ↓
read-only lineage reconstruction
```

P8 should reuse current facts wherever possible:

- P4 content-addressed artifacts and admission receipts;
- raw `evidence/` records under the existing physical-containment contract;
- P5 `TransitionRecord.evidence` consumption references;
- trace transition digests;
- current Campaign reconstruction.

P8 must preserve:

```text
provenance != semantic truth
consumed evidence != sufficient evidence
artifact identity != recommendation
lineage != semantic inference
```

It must not:

- infer why evidence is persuasive;
- invent evidence-consumption links not explicitly present in durable records;
- rank evidence or capabilities;
- mutate historical transition meaning;
- treat a validator pass as proof that the evidence supports a conclusion;
- create a second semantic decision log beside transitions/trace.

## Semantic-control invariant

The implementation must preserve this separation:

```text
Agent:
  What does the evidence mean?
  Which responsibility is warranted?
  Which evidence should support an authored decision?
  Which available capability should be selected?
  Does the result justify advance, defer, or close?

Deterministic machinery:
  Is the representation valid?
  Is state persisted safely?
  Does referenced evidence satisfy the Campaign evidence contract?
  What immutable identity/digest/provenance does each evidence ref have?
  Which transition explicitly consumed which evidence refs?
  Is history reconstructible?
  Does the handoff bind exactly to the reconstructible current state?
```

Therefore:

```text
validator passed != conclusion is true
warranted responsibility != available capability
available capability != authorized capability
recommendation != execution authority
handoff != semantic recommendation
lineage != semantic warrant
```

And:

```text
Campaign Controller != semantic router
```

## Remaining v0.3 sequence

1. **P8 — Artifact/evidence lineage** — CURRENT.
2. **P9 — Reconciliation lifecycle**.
3. **P10 — Harness adapters**.
4. **P11 — External golden-path qualification and v0.3 release**.

## Research and experiment disposition

Prior research remains useful evidence and is preserved. It is not the default active product program.

EXP-0006 / Empirical Skill Qualification v1 remains stopped at its actual completed boundary under the owner productization pivot. Preserve the D attempts, frozen Q/T holdout identity/integrity record, contamination audit, and actual claim ceilings. Do not manufacture a candidate or continue Q/T execution merely to complete the mechanism.

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
→ inspect evidence lineage
→ handoff
→ resume in a fresh context
→ stop honestly
```

with deterministic reconstruction and without requiring prior conversation as hidden input or manually repairing Campaign/artifact state.

## Where to look

| Topic | Source |
|---|---|
| Product definition, principles, authority model | `CONTEXT.md` |
| Canonical Sensemaking Campaign product model | `docs/sensemaking-campaign.md` |
| Active v0.3 delivery plan | `docs/productization-v0.3.md` |
| Agent-authored campaign decisions | `docs/campaign-decisions.md` |
| Capability registry inspection | `docs/capability-registry.md` |
| Durable handoff/resume | `docs/campaign-handoff-resume.md` |
| SkillOpt influence/adaptation and research boundary | `docs/research/skillopt-adaptation.md` |
| Agent-native operating model | `docs/agent-native-operating-workflow.md` |
| Decision vs orchestration boundary | `docs/decision-orchestration-boundary.md` |
| Campaign semantic contract | `docs/campaign-semantics.md`, `src/sensemaking_skills/campaign_semantics/` |
| Validated artifact ingestion | `docs/artifact-ingestion.md` |
| Workflow catalog/liveness | `docs/workflow-system-disposition.md`, ADR 0027 |
| Design decisions | `docs/adr/` — always read each ADR's status |
| Historical research/evidence | `experiments/`, `docs/research/`, `docs/campaigns/` |
| Installation and usage | `README.md`, `GETTING_STARTED.md`, `INSTALLATION.md` |
