# Sensemaking Skills v0.3 Productization Plan

**Status:** ACTIVE owner direction  
**Effective:** 2026-09-08  
**Base at pivot:** `main@5c2c807542f7e150d4a031430f59e297ed816b24`  
**Current integrated frontier:** P4 merged at `main@79b3aca042a4a526b35e09284e0093159f271bb1`  
**Primary objective:** turn the ratified agent-native control model into a usable campaign-based engineering product.  
**Canonical product model:** [`sensemaking-campaign.md`](sensemaking-campaign.md)

This document is the **versioned v0.3 delivery plan**. The durable definition of what a Sensemaking Campaign is belongs in [`sensemaking-campaign.md`](sensemaking-campaign.md).

## 1. Development-regime change

The repository is moving from research/experiment-first development to implementation/productization-first development.

The default loop is now:

```text
identify a user-visible capability
→ implement the smallest complete vertical slice
→ validate deterministically
→ dogfood in ordinary engineering use
→ repair observed friction
→ ship the slice
```

Formal experiments are no longer the normal next step. Use them only when two or more consequential product decisions remain plausible, ordinary implementation/dogfood evidence cannot reasonably distinguish them, and the distinction would materially change architecture or product direction.

Existing research artifacts remain evidence. They are not deleted, relabeled, or retroactively promoted. Incomplete experiments may be stopped by owner direction without manufacturing a candidate or a terminal scientific result.

## 2. Product boundary preserved

This pivot does **not** reverse the accepted agent-native control model.

- The active coding agent owns semantic control.
- Deterministic Python machinery owns representation, persistence, validation, provenance, authority checks, and structural reconstruction.
- A validator passing does not make a semantic conclusion true.
- Capability availability does not select a capability.
- Capability availability does not grant authority.
- Recommendation does not authorize execution.

The campaign layer must therefore consume agent-authored/agent-produced decisions and validated artifacts; it must not reproduce repository diagnosis or semantic routing inside Python.

The durable product-level invariant is:

```text
warranted responsibility
!= capability availability
!= execution authority
```

## 3. v0.3 north-star outcome

A coding agent can:

```text
start a Sensemaking Campaign
→ diagnose a repository with the existing agent-native Skill path
→ preserve the validated artifact
→ record the warranted responsibility and authority
→ perform bounded work
→ validate/reconcile the result
→ record a durable transition
→ hand the campaign to a fresh agent
→ resume without conversation memory
→ continue or terminate honestly
```

A fresh agent should be able to reconstruct the active campaign from durable campaign state plus referenced canonical artifacts, not from the prior chat transcript.

## 4. Campaign architecture

`campaign_semantics` remains the domain contract: what campaign state, responsibility, uncertainty, authority, transitions, handoffs, traces, and capability availability mean.

The v0.3 product layer is built around it:

```text
agent semantic judgment
        ↓
validated artifact / explicit decision
        ↓
CampaignService
        ↓
CampaignStore
        ↓
campaign_semantics typed contracts
        ↓
filesystem workspace
```

The store does not select work. The service does not become a semantic router. Registered capabilities remain inspectable candidates only.

For the version-independent product definition and full trust model, see [`sensemaking-campaign.md`](sensemaking-campaign.md).

## 5. Milestone status

| Milestone | Status | Outcome |
|---|---|---|
| **P0 — Productization pivot** | **MERGED** | Implementation-first direction made durable; experiment-first program stopped as default. |
| **P1 — Durable campaign workspace** | **MERGED** | Isolated file-backed campaign persistence with strict typed I/O and fail-closed filesystem boundaries. |
| **P2 — Campaign service** | **MERGED** | Deterministic lifecycle service with recoverable transition commits, reconstruction, defer/terminate, handoff, and resume primitives. |
| **P3 — Campaign CLI foundation** | **MERGED** | `campaign init/status/validate/history` with human and JSON surfaces plus stable exit semantics. |
| **P4 — Validated artifact ingestion** | **MERGED** | Canonically validated, content-addressed artifact admission with append-only receipts; raw artifact files do not automatically become evidence. |
| **P5 — Agent-authored decisions** | **CURRENT** | Add explicit `campaign advance/defer/close` decision surfaces without semantic routing. |
| **P6 — Real capability registry** | PLANNED | Expose responsibility-to-capability metadata while preserving availability/authority separation. |
| **P7 — Durable handoff/resume** | PLANNED | Productize fresh-agent reconstruction as a first-class user experience. |
| **P8 — Artifact/evidence lineage** | PLANNED | Add stable provenance and consumption links across artifacts, evidence, decisions, and transitions. |
| **P9 — Reconciliation lifecycle** | PLANNED | Connect reconciliation/repair-verification outputs to explicit campaign transitions. |
| **P10 — Harness adapters** | PLANNED | Improve setup for Claude Code, Codex, OpenCode, and generic agent environments. |
| **P11 — v0.3 qualification/release** | PLANNED | Prove the external golden path and ship the first usable campaign-based release. |

## 6. Implemented milestone contracts

### P0 — Productization pivot — MERGED

Delivered:

- productization direction made durable;
- formal experiment execution removed as the default product-development program;
- prior research preserved with actual claim ceilings;
- incomplete research branches stopped without manufacturing results.

### P1 — Durable campaign workspace — MERGED

The file-backed campaign workspace is isolated from the target repository by contract for v0.3.

Current control/evidence shape includes:

```text
CMP-XXXX/
├── campaign-state.yaml
├── campaign-policy.yaml          # optional
├── campaign-handoff.yaml         # optional/current handoff
├── trace.yaml
├── transitions/
├── artifacts/
├── admissions/
└── evidence/
```

Storage invariants include:

- `campaign-state.yaml` is a replaceable current snapshot;
- transition records are append-only;
- trace history is append-preserving;
- state replacement is atomic;
- initialization does not overwrite an existing workspace;
- when a target repository is supplied, the campaign workspace must not live inside that repository;
- persisted semantic artifacts pass the existing strict campaign-semantic loader before acceptance;
- physical path containment fails closed on symlink/reparse escapes.

### P2 — Campaign service — MERGED

Implemented deterministic lifecycle operations:

- initialize;
- validate;
- record transition + replacement state through a durable transaction/recovery boundary;
- defer responsibility;
- terminate;
- generate handoff;
- resume/reconstruct.

The service validates contracts and authority metadata but does not decide which responsibility is semantically warranted.

### P3 — Campaign CLI foundation — MERGED

Implemented:

```text
sensemaking-skills campaign init
sensemaking-skills campaign status
sensemaking-skills campaign validate
sensemaking-skills campaign history
```

Read-oriented commands expose human-readable and machine-readable (`--json`) output. CLI reconstruction goes through `CampaignService`, not a second history implementation.

### P4 — Validated artifact ingestion — MERGED

Implemented:

```text
sensemaking-skills campaign ingest
```

The trust boundary is:

```text
artifact bytes
→ canonical validate-and-report.py router
→ selected specialized or generic validator
→ valid=true
→ content-addressed artifact copy
→ append-only admission receipt
→ campaign evidence
```

Important invariants:

```text
file under artifacts/
!= validated artifact
!= admitted campaign evidence
```

- raw `evidence/` files preserve the earlier direct-evidence semantics;
- files merely dropped under `artifacts/` are not admitted evidence;
- validation is performed on an immutable snapshot of the exact bytes later copied;
- admission receipts bind artifact digest, validator identity, router/validator digests, validation result, and campaign identity;
- receipt is written last, so an interrupted write can leave an orphan artifact but cannot create false evidence status;
- pre-P4 arbitrary artifact files are not silently grandfathered as validated evidence.

See [`artifact-ingestion.md`](artifact-ingestion.md) for the implemented P4 contract.

## 7. Current implementation frontier — P5

The next bounded implementation slice is **P5 — Agent-authored decisions**.

### Goal

Allow the active coding agent to explicitly persist a semantic campaign decision after inspecting admitted evidence, current responsibility, authority, and campaign state.

Target product surfaces:

```text
sensemaking-skills campaign advance
sensemaking-skills campaign defer
sensemaking-skills campaign close
```

### Required boundary

The active agent supplies the decision. Deterministic machinery validates and persists it.

```text
admitted evidence
        ↓
agent semantic judgment
        ↓
explicit decision contract
        ↓
CampaignService
        ↓
TransitionRecord + CampaignState + trace
```

P5 must **not**:

- infer which responsibility is warranted;
- infer whether evidence semantically supports a conclusion;
- rank or select a Skill/capability;
- convert artifact fields into automatic routing;
- grant execution authority;
- create a semantic truth validator.

### P5 acceptance direction

A complete P5 slice should prove at least:

1. the agent can explicitly author `advance`, `defer`, and `close` decisions;
2. referenced evidence must already satisfy the current evidence contract;
3. authority metadata remains explicit and mechanically coherent;
4. a terminal campaign cannot be advanced accidentally;
5. decision persistence uses P2's recoverable lifecycle commit rather than a second write path;
6. a fresh process reconstructs the same authored decision and history;
7. CLI JSON output is stable enough for an agent harness to consume without prose scraping;
8. no command emits an automatic semantic recommendation.

Stop P5 before capability selection/routing logic. That belongs to the later capability-registry integration and still remains agent-controlled.

## 8. Remaining planned milestones

### P6 — Real capability registry

Populate responsibility-to-capability metadata while preserving the distinction:

```text
warranted responsibility
!= capability availability
!= execution authority
```

No ranking or automatic routing is introduced.

### P7 — Durable handoff/resume

Make `campaign handoff` and `campaign resume` a first-class experience. A fresh coding-agent context must be able to reconstruct the current campaign from durable state and referenced artifacts without requiring prior chat memory.

### P8 — Artifact/evidence lineage

Add stable artifact identities/digests and consumption/provenance links so a campaign can answer why a decision was made and which immutable evidence supported it.

### P9 — Reconciliation lifecycle

Connect existing output-reconciliation and repair-verification responsibilities to campaign transitions without treating mechanical validation as semantic truth.

### P10 — Harness adapters

Improve setup for Claude Code, Codex, OpenCode, and generic agent Skill locations without placing agent-specific semantics inside the campaign core.

### P11 — v0.3 qualification/release

v0.3 means the first usable campaign-based Sensemaking release, not completion of every research direction.

Required golden path:

```text
start
→ consume diagnosis
→ record responsibility
→ bind authority
→ inspect available capability
→ record work evidence
→ transition
→ handoff
→ fresh-agent resume
→ stop honestly
```

## 9. Explicit non-goals for v0.3

Do not build unless later product pressure warrants it:

- centralized semantic router;
- HTN/generic planner;
- Skill ranking algorithm;
- critic/voting swarm;
- self-modifying Skills;
- autonomous SkillOpt loop;
- campaign server/database/cloud service;
- generic semantic truth validator;
- automatic external mutation authority;
- full multi-repository campaign engine.

## 10. Experiment disposition

Research and experimental scaffolds remain available as laboratories and historical evidence. They are not the default active program.

In particular, EXP-0006 stopped at its actual completed boundary under the owner productization pivot. Preserve its diagnostic attempts, holdout freeze, contamination audit, and claim ceilings. Do not manufacture a Skill candidate merely to exercise the qualification mechanism.

The provenance and disposition of SkillOpt-influenced Skill-quality ideas are recorded in [`research/skillopt-adaptation.md`](research/skillopt-adaptation.md). That note does not insert Skill optimization into the v0.3 milestone sequence, authorize EXP-0006, or change the Campaign product boundary.

## 11. Definition of v0.3 done

The first campaign-based release is ready when a real external-repository run can demonstrate:

```text
start
→ repository diagnosis
→ validated artifact admission
→ agent-authored responsibility/authority decision
→ available capability inspection
→ bounded work
→ durable evidence
→ transition
→ handoff
→ fresh-context resume
→ justified continuation or terminal stop
```

with deterministic reconstruction and **without manual campaign/artifact repair or prior conversation memory as hidden input**.