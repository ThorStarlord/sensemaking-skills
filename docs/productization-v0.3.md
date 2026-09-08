# Sensemaking Skills v0.3 Productization Plan

**Status:** ACTIVE owner direction  
**Effective:** 2026-09-08  
**Base at pivot:** `main@5c2c807542f7e150d4a031430f59e297ed816b24`  
**Current integrated frontier:** P5 merged at `main@d1b925a17620fc98b2bbcdc528feb32feacc9d6e`  
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
→ inspect available capabilities
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
| **P5 — Agent-authored decisions** | **MERGED** | Explicit `campaign advance/defer/close` decisions persist agent judgment without semantic routing. |
| **P6 — Real capability registry** | **CURRENT** | Expose responsibility-to-capability metadata while preserving availability/authority separation and agent-owned selection. |
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
typed advance / defer / close decision
        ↓
existing CampaignService lifecycle primitive
        ↓
recoverable CampaignState + TransitionRecord + trace
```

Important P5 invariants include:

- `advance` installs exactly one explicit next responsibility supplied by the agent;
- responsibility trigger evidence is bound to the installing transition and must already satisfy the campaign evidence contract;
- `defer` preserves the canonical optional reopening contract instead of fabricating a condition;
- `close` persists an explicit `TerminalState` and later advance attempts fail closed;
- JSON success surfaces expose the exact replacement state and committed transition;
- P5 reuses P2 recovery/transaction machinery rather than creating another persistence path;
- no P5 command emits an automatic semantic recommendation or capability selection.

See [`campaign-decisions.md`](campaign-decisions.md) for the implemented P5 contract.

## 7. Current implementation frontier — P6

The next bounded implementation slice is **P6 — Real capability registry**.

### Goal

Allow the active coding agent to inspect real capability metadata relevant to an explicitly classified responsibility while preserving the permanent separation:

```text
warranted responsibility
!= available capability
!= authorized capability
```

P6 should answer:

> Which registered capabilities claim compatibility with this agent-classified responsibility, and what are their current availability and authority properties?

P6 must **not** answer:

> Which capability should the agent choose?

### Required boundary

The agent remains responsible for semantic classification and selection. Deterministic machinery may load, normalize, validate, and enumerate declared capability metadata.

```text
active responsibility
        ↓
agent supplies responsibility classification
        ↓
capability metadata lookup
        ↓
unranked inspectable candidates
        ↓
agent chooses one / none / ordinary work
```

### P6 implementation direction

Reuse the existing campaign-semantic capability contracts rather than create another capability model:

- `Capability`;
- `CapabilityAvailability`;
- `RegisteredCapability`;
- `CapabilityRegistry`;
- `AvailabilityStatus`.

Populate them from current Skill/workflow metadata and liveness declarations through a bounded adapter/loader. Prefer explicit declarative metadata over semantic inference from prose such as `purpose` or responsibility statements.

Initial product surface should be read-oriented and agent-consumable, for example:

```text
sensemaking-skills campaign capabilities
```

The exact command contract is implementation-owned, but qualification must prove that enumeration is deterministic and unranked, empty results are honest, liveness/availability remain fail closed, and authority metadata is exposed without manufacturing authorization.

### P6 must not

- infer a responsibility type from free-form responsibility prose;
- rank candidates;
- emit a `best` or `recommended` capability;
- invoke a Skill/workflow automatically;
- treat catalog membership as availability;
- treat availability as execution authorization;
- promote proposed/deprecated/compatibility-only entries into current capability availability;
- create semantic routing inside Python.

## 8. Remaining planned milestones

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
