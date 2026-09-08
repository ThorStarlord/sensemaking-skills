# Status

**Version:** 0.2.2  
**Last updated:** 2026-09-08  
**Current phase:** Productization / implementation  
**Primary program:** Sensemaking Skills v0.3 campaign-based productization  
**Current frontier:** P5 — agent-authored campaign decisions

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

The current integrated implementation frontier after P4 is:

```text
main@79b3aca042a4a526b35e09284e0093159f271bb1
```

That current `main` contains the exact qualified P4 tree and therefore includes the cumulative P0–P4 productization work.

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

## Current productization objective

The v0.3 north-star outcome is:

> A coding agent can start a durable Sensemaking Campaign on a real repository, consume validated agent-native diagnostic artifacts, record the warranted responsibility and authority, perform bounded work, validate/reconcile the result, hand the campaign to a fresh agent, and continue or terminate without relying on prior conversation memory.

The intended lifecycle is:

```text
user goal
→ campaign init
→ repository sensemaking
→ validated artifact admission
→ agent authors responsibility/authority decision
→ bounded capability / ordinary coding
→ validation / reconciliation
→ durable transition
→ handoff / continue / stop
```

## Current implementation frontier — P5

The next bounded slice is **P5 — Agent-authored decisions**.

Target commands:

```text
sensemaking-skills campaign advance
sensemaking-skills campaign defer
sensemaking-skills campaign close
```

The purpose is to let the active agent persist an explicit semantic decision using already-admitted evidence and explicit authority while reusing P2's deterministic lifecycle commit/reconstruction boundary.

P5 must preserve:

```text
admitted evidence
        ↓
AGENT judgment
        ↓
explicit decision contract
        ↓
CampaignService
        ↓
durable transition
```

It must **not** turn artifact fields, capability metadata, or validator output into automatic semantic routing.

## Semantic-control invariant

The implementation must preserve this separation:

```text
Agent:
  What does the evidence mean?
  Which responsibility is warranted?
  Which available capability should be selected?
  Does the result justify advance, defer, or close?

Deterministic machinery:
  Is the representation valid?
  Is state persisted safely?
  Does referenced evidence satisfy the current evidence contract?
  Does authority metadata permit the claimed action?
  Is the transition structurally reconstructible?
  What durable evidence and history exist?
```

Therefore:

```text
validator passed != conclusion is true
warranted responsibility != available capability
available capability != authorized capability
recommendation != execution authority
```

And:

```text
Campaign Controller != semantic router
```

## Remaining v0.3 sequence

1. **P5 — Agent-authored decisions** — CURRENT.
2. **P6 — Real capability registry**, without automatic ranking/routing.
3. **P7 — Durable handoff/resume UX**.
4. **P8 — Artifact/evidence lineage**.
5. **P9 — Reconciliation lifecycle**.
6. **P10 — Harness adapters**.
7. **P11 — External golden-path qualification and v0.3 release**.

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
| SkillOpt influence/adaptation and research boundary | `docs/research/skillopt-adaptation.md` |
| Agent-native operating model | `docs/agent-native-operating-workflow.md` |
| Decision vs orchestration boundary | `docs/decision-orchestration-boundary.md` |
| Campaign semantic contract | `docs/campaign-semantics.md`, `src/sensemaking_skills/campaign_semantics/` |
| Validated artifact ingestion | `docs/artifact-ingestion.md` |
| Workflow catalog/liveness | `docs/workflow-system-disposition.md`, ADR 0027 |
| Design decisions | `docs/adr/` — always read each ADR's status |
| Historical research/evidence | `experiments/`, `docs/research/`, `docs/campaigns/` |
| Installation and usage | `README.md`, `GETTING_STARTED.md`, `INSTALLATION.md` |
