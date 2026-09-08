# Sensemaking Skills v0.3 Productization Plan

**Status:** ACTIVE owner direction  
**Effective:** 2026-09-08  
**Base at pivot:** `main@5c2c807542f7e150d4a031430f59e297ed816b24`  
**Current integrated frontier:** P7 merged at `main@250a30ddd55e100a311a5ab17650a0f3176de605`  
**Primary objective:** turn the ratified agent-native control model into a usable campaign-based engineering product.  
**Canonical product model:** [`sensemaking-campaign.md`](sensemaking-campaign.md)

This document is the **versioned v0.3 delivery plan**. The durable definition of a Sensemaking Campaign belongs in [`sensemaking-campaign.md`](sensemaking-campaign.md).

## 1. Development-regime change

The repository is implementation/productization-first.

The default loop is:

```text
identify a user-visible capability
→ implement the smallest complete vertical slice
→ validate deterministically
→ dogfood in ordinary engineering use
→ repair observed friction
→ ship the slice
```

Formal experiments are reserved for consequential product uncertainties that implementation and dogfood evidence cannot reasonably resolve. Existing research remains evidence and keeps its actual claim ceilings.

## 2. Product boundary preserved

The productization program does not reverse the accepted agent-native control model.

- The active coding agent owns semantic control.
- Deterministic Python owns representation, persistence, validation, provenance, authority checks, integrity, and structural reconstruction.
- A validator passing does not make a semantic conclusion true.
- Capability availability does not select or authorize a capability.
- A handoff does not decide what the fresh agent should do next.
- Provenance/lineage does not establish semantic warrant.

The durable invariant remains:

```text
warranted responsibility
!= capability availability
!= execution authority
```

and for P8:

```text
provenance
!= semantic truth

consumed evidence
!= sufficient evidence
```

## 3. v0.3 north-star outcome

A coding agent can:

```text
start a Sensemaking Campaign
→ diagnose a repository through the agent-native Skill path
→ preserve and admit validated artifacts
→ record warranted responsibility and authority
→ inspect available capabilities
→ perform bounded work
→ record durable evidence
→ validate/reconcile the result
→ record a durable transition
→ inspect why that transition cites its evidence
→ hand the Campaign to a fresh agent
→ resume without conversation memory
→ continue or terminate honestly
```

A fresh agent should reconstruct the active Campaign from durable Campaign state and referenced canonical artifacts, not the previous chat transcript.

## 4. Campaign architecture

`campaign_semantics` remains the domain contract for Campaign state, responsibility, uncertainty, authority, transitions, handoffs, traces, and capability availability.

The product layer remains:

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

Lineage is a read-only reconstruction of identities, provenance, and explicit consumption links already present in durable Campaign records. It must not become a second decision system.

## 5. Milestone status

| Milestone | Status | Outcome |
|---|---|---|
| **P0 — Productization pivot** | **MERGED** | Implementation-first direction made durable; experiment-first development stopped as default. |
| **P1 — Durable campaign workspace** | **MERGED** | Isolated file-backed Campaign persistence with strict typed I/O and fail-closed filesystem boundaries. |
| **P2 — Campaign service** | **MERGED** | Deterministic lifecycle service with recoverable transition commits, reconstruction, defer/terminate, handoff, and resume primitives. |
| **P3 — Campaign CLI foundation** | **MERGED** | `campaign init/status/validate/history` with human and JSON surfaces plus stable exit semantics. |
| **P4 — Validated artifact ingestion** | **MERGED** | Canonically validated, content-addressed artifact admission with append-only receipts; raw artifact files do not automatically become evidence. |
| **P5 — Agent-authored decisions** | **MERGED** | Explicit `campaign advance/defer/close` decisions persist agent judgment without semantic routing. |
| **P6 — Real capability registry** | **MERGED** | Read-only agent-classified capability inspection with liveness, availability, and authority separation. |
| **P7 — Durable handoff/resume** | **MERGED** | Fresh-context reconstruction with integrity-bound handoff and installed-wheel proof. |
| **P8 — Artifact/evidence lineage** | **CURRENT** | Add stable evidence identity/provenance and explicit decision-consumption reconstruction. |
| **P9 — Reconciliation lifecycle** | PLANNED | Connect reconciliation/repair-verification outputs to explicit Campaign transitions. |
| **P10 — Harness adapters** | PLANNED | Improve setup for Claude Code, Codex, OpenCode, and generic agent environments. |
| **P11 — v0.3 qualification/release** | PLANNED | Prove the external golden path and ship the first usable Campaign-based release. |

## 6. Implemented milestone contracts

### P0 — Productization pivot — MERGED

Delivered implementation-first direction while preserving historical research and claim ceilings.

### P1 — Durable campaign workspace — MERGED

Current workspace shape includes:

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

Important invariants include isolated workspace placement, strict typed Campaign I/O, append-only transition history, atomic state replacement, fail-closed physical containment, and non-overwrite initialization.

### P2 — Campaign service — MERGED

Implemented deterministic initialize/validate/transition/defer/terminate/handoff/resume operations with durable commit intent and crash recovery. The service validates mechanically decidable contracts but never decides which responsibility is semantically warranted.

### P3 — Campaign CLI foundation — MERGED

Implemented:

```text
sensemaking-skills campaign init
sensemaking-skills campaign status
sensemaking-skills campaign validate
sensemaking-skills campaign history
```

CLI reconstruction goes through `CampaignService`, not a second history implementation.

### P4 — Validated artifact ingestion — MERGED

Implemented:

```text
sensemaking-skills campaign ingest
```

Trust boundary:

```text
artifact bytes
→ canonical validate-and-report.py router
→ selected validator
→ valid=true
→ content-addressed artifact
→ append-only admission receipt
→ Campaign evidence
```

Important invariant:

```text
file under artifacts/
!= validated artifact
!= admitted campaign evidence
```

Admission receipts bind exact artifact digest, validator identity, router/validator digests, validation result, and Campaign identity. See [`artifact-ingestion.md`](artifact-ingestion.md).

### P5 — Agent-authored decisions — MERGED

Implemented:

```text
sensemaking-skills campaign advance
sensemaking-skills campaign defer
sensemaking-skills campaign close
```

P5 makes the semantic decision boundary explicit:

```text
admitted / durable evidence
        ↓
agent semantic judgment
        ↓
typed decision
        ↓
CampaignService lifecycle primitive
        ↓
recoverable CampaignState + TransitionRecord + trace
```

Transition evidence is explicit durable consumption context supplied by the authored decision. P5 does not rank/select capabilities or infer semantic conclusions. See [`campaign-decisions.md`](campaign-decisions.md).

### P6 — Real capability registry — MERGED

Implemented:

```text
sensemaking-skills campaign capabilities
```

P6 exposes declared capability metadata only after the agent supplies a responsibility classification. Results are deterministic and unranked; availability is not authority; capability inspection never selects or invokes work. See [`capability-registry.md`](capability-registry.md).

### P7 — Durable handoff/resume — MERGED

Implemented:

```text
sensemaking-skills campaign handoff
sensemaking-skills campaign resume
```

P7 reuses the canonical P2 `CampaignHandoff` and `CampaignService` primitives rather than introducing another handoff state machine.

The P7 reconstruction checksum binds:

```text
protocol identity
CampaignState
ordered TransitionRecords
CampaignTrace
current evidence refs
optional CampaignPolicy
CampaignHandoff
```

The checksum is stored as a YAML comment, leaving the semantic `CampaignHandoff` schema unchanged. It detects stale/edited/unbound handoffs under the existing filesystem trust model but is not a signature or authority grant.

P7 proves fresh service/process reconstruction and installed-wheel `init → advance → handoff → resume` outside a source checkout. It never infers unstored conversation context, a next responsibility, capability choice, or authority.

See [`campaign-handoff-resume.md`](campaign-handoff-resume.md).

## 7. Current implementation frontier — P8

The next bounded implementation slice is **P8 — Artifact/evidence lineage**.

### Goal

Make durable Campaign history answer:

> What exact evidence supported this authored decision/transition, what immutable identity does each evidence item have, and what provenance establishes how it entered the Campaign?

P8 must expose identity/provenance/consumption facts without deciding whether the evidence was semantically persuasive or sufficient.

### Existing facts P8 should reuse

P8 should build on the contracts already shipped:

- P4 content-addressed admitted artifacts;
- P4 append-only admission receipts;
- raw `evidence/` files protected by the existing physical-containment boundary;
- P5 `TransitionRecord.evidence` as explicit transition-consumption references;
- responsibility trigger evidence where it remains durably represented;
- trace transition/state digest bindings;
- P7 reconstruction of current state/history/evidence refs.

Do not create a parallel semantic ledger if these records already contain the required fact.

### Required control shape

```text
durable evidence
        ↓
stable ref + SHA-256 identity + provenance classification
        ↓
agent-authored decision references evidence
        ↓
TransitionRecord.evidence preserves explicit consumption
        ↓
deterministic read-only lineage reconstruction
```

### Initial product surface

Prefer a read-only agent-consumable surface such as:

```text
sensemaking-skills campaign lineage --workspace <CMP> [--json]
```

A useful lineage envelope should distinguish at least:

- raw Campaign evidence;
- admitted artifacts;
- admission receipts;
- exact SHA-256 identity of evidence bytes;
- artifact/admission relationship;
- transition ID and transition digest;
- explicit transition → evidence consumption edges.

If provenance cannot be established mechanically, fail closed rather than guess.

### P8 must preserve

```text
artifact exists
!= artifact admitted

admitted artifact
!= semantic truth

transition cites evidence
!= evidence sufficient

lineage
!= recommendation
```

### P8 must not

- interpret artifact findings;
- infer whether cited evidence logically supports the decision;
- invent consumption edges that are not present in durable Campaign records;
- rank evidence;
- rank/select capabilities;
- grant authority;
- rewrite historical transitions;
- make lineage a second source of semantic truth;
- grandfather arbitrary `artifacts/` files as evidence;
- weaken P4 admission validation or P2 reconstruction integrity.

### Qualification direction

A qualified P8 candidate should prove at least:

1. raw `evidence/` files receive stable content digests without changing their existing evidence semantics;
2. admitted artifacts expose the exact P4 artifact digest and admission receipt provenance;
3. orphan/unadmitted files under `artifacts/` do not appear as evidence lineage;
4. transition → evidence edges come exactly from `TransitionRecord.evidence`;
5. each transition exposes the digest already bound in the Campaign trace, or fails if trace integrity is defective;
6. digest drift in raw/admitted evidence is detected under the existing trust model;
7. lineage output is deterministic and read-only;
8. no output field implies recommendation, ranking, semantic sufficiency, or authority;
9. a fresh process can reconstruct lineage from durable Campaign files alone;
10. the installed distribution exposes the product surface without requiring a source checkout.

## 8. Remaining planned milestones

### P9 — Reconciliation lifecycle

Connect existing output-reconciliation and repair-verification responsibilities to explicit Campaign transitions without treating mechanical validation as semantic truth.

### P10 — Harness adapters

Improve setup for Claude Code, Codex, OpenCode, and generic agent Skill locations without placing agent-specific semantics inside the Campaign core.

### P11 — v0.3 qualification/release

Required golden path:

```text
start
→ repository diagnosis
→ validated artifact admission
→ agent-authored responsibility/authority decision
→ available capability inspection
→ bounded work
→ durable evidence
→ transition
→ lineage inspection
→ handoff
→ fresh-context resume
→ justified continuation or terminal stop
```

## 9. Explicit non-goals for v0.3

Do not build unless later product pressure warrants it:

- centralized semantic router;
- HTN/generic planner;
- Skill ranking algorithm;
- critic/voting swarm;
- self-modifying Skills;
- autonomous SkillOpt loop;
- Campaign server/database/cloud service;
- generic semantic truth validator;
- automatic external mutation authority;
- full multi-repository Campaign engine.

## 10. Experiment disposition

Research and experimental scaffolds remain laboratories/historical evidence rather than the default active program.

EXP-0006 remains stopped at its actual completed boundary under the owner productization pivot. Preserve its diagnostic attempts, frozen holdout identity/integrity record, contamination audit, and claim ceilings. Do not manufacture a Skill candidate merely to exercise the qualification mechanism.

The provenance/disposition of SkillOpt-influenced Skill-quality ideas remains recorded in [`research/skillopt-adaptation.md`](research/skillopt-adaptation.md). That note does not insert Skill optimization into the v0.3 milestone sequence or alter the Campaign boundary.

## 11. Definition of v0.3 done

The first Campaign-based release is ready when a real external-repository run demonstrates:

```text
start
→ repository diagnosis
→ validated artifact admission
→ agent-authored responsibility/authority decision
→ available capability inspection
→ bounded work
→ durable evidence
→ transition
→ lineage inspection
→ handoff
→ fresh-context resume
→ justified continuation or terminal stop
```

with deterministic reconstruction and **without manual Campaign/artifact repair or prior conversation memory as hidden input**.
