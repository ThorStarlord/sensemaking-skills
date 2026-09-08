# Sensemaking Skills v0.3 Productization Plan

**Status:** ACTIVE owner direction  
**Effective:** 2026-09-08  
**Base at pivot:** `main@5c2c807542f7e150d4a031430f59e297ed816b24`  
**Current integrated frontier:** P8 merged at `main@e1b900c32d932d5e4b5c0366c0972143c36b1982`  
**Current implementation frontier:** P9 — reconciliation lifecycle  
**Primary objective:** turn the ratified agent-native control model into a usable campaign-based engineering product.  
**Canonical product model:** [`sensemaking-campaign.md`](sensemaking-campaign.md)

This document is the versioned v0.3 delivery plan. The durable definition of a Sensemaking Campaign belongs in [`sensemaking-campaign.md`](sensemaking-campaign.md).

## 1. Development-regime change

The repository is implementation/productization-first.

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
- Reconciliation evidence does not decide the Campaign transition.

The durable invariant remains:

```text
warranted responsibility
!= capability availability
!= execution authority
```

and:

```text
provenance
!= semantic truth

consumed evidence
!= sufficient evidence

reconciliation evidence
!= semantic disposition
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
→ reconcile/verify the result
→ explicitly disposition that evidence
→ record a durable transition
→ inspect exact transition/evidence lineage
→ hand the Campaign to a fresh agent
→ resume without conversation memory
→ continue or terminate honestly
```

A fresh agent should reconstruct the active Campaign from durable Campaign state and referenced canonical artifacts, not the previous chat transcript.

## 4. Campaign architecture

`campaign_semantics` remains the domain contract for Campaign state, responsibility, uncertainty, authority, transitions, handoffs, traces, and capability availability.

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

Lineage is a reconstruction of identities, provenance, and explicit consumption links. Reconciliation lifecycle state may summarize mechanically present reconciliation evidence, but must never become a second semantic decision system.

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
| **P8 — Artifact/evidence lineage** | **MERGED** | Exact evidence-byte identity, provenance, and explicit transition-consumption reconstruction. |
| **P9 — Reconciliation lifecycle** | **CURRENT** | Connect admitted reconciliation/repair-verification evidence to explicit Campaign disposition without automatic semantic transitions. |
| **P10 — Harness adapters** | PLANNED | Improve setup for Claude Code, Codex, OpenCode, and generic agent environments. |
| **P11 — v0.3 qualification/release** | PLANNED | Prove the external golden path and ship the first usable Campaign-based release. |

## 6. Implemented milestone contracts

### P0 — Productization pivot — MERGED

Delivered implementation-first direction while preserving historical research and claim ceilings.

### P1 — Durable campaign workspace — MERGED

Current workspace foundations include current state, optional policy/handoff, trace, transitions, artifacts, admissions, and raw evidence under strict physical-containment rules.

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
!= admitted Campaign evidence
```

See [`artifact-ingestion.md`](artifact-ingestion.md).

### P5 — Agent-authored decisions — MERGED

Implemented:

```text
sensemaking-skills campaign advance
sensemaking-skills campaign defer
sensemaking-skills campaign close
```

```text
durable evidence
→ agent semantic judgment
→ typed decision
→ CampaignService lifecycle primitive
→ recoverable CampaignState + TransitionRecord + trace
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

P7 reuses canonical P2 handoff/reconstruction primitives and integrity-binds fresh-context reconstruction without changing the semantic `CampaignHandoff` schema. See [`campaign-handoff-resume.md`](campaign-handoff-resume.md).

### P8 — Artifact/evidence lineage — MERGED

Implemented:

```text
sensemaking-skills campaign lineage
```

P8 records/reconstructs mechanically verifiable provenance and explicit evidence consumption while leaving semantic judgment to the active agent.

```text
durable Campaign evidence
        ↓
exact byte identity + provenance
        ↓
append-only precommit consumption intent
        ↓
existing P2 lifecycle commit
        ↓
TransitionRecord.evidence + trace digest
        ↓
read-only lineage reconstruction
```

P8 distinguishes:

- raw `evidence/**` — exact consumed bytes are snapshotted by SHA-256;
- admitted artifacts — reuse P4 content-addressed identity and admission provenance;
- admission receipts — preserve exact consumed receipt bytes plus validator/artifact provenance.

A P8-authored zero-evidence decision receives an explicit empty bound receipt. Historical/direct-P2 transitions without P8 receipts remain `legacy_unbound`. Orphan precommit intents do not create false committed consumption edges.

See [`campaign-lineage.md`](campaign-lineage.md).

## 7. Current implementation frontier — P9

The next bounded implementation slice is **P9 — Reconciliation lifecycle**.

### Goal

Make a durable Campaign able to answer mechanically:

> What reconciliation or repair-verification evidence currently exists for the work under review, and has an explicit agent-authored Campaign disposition consumed that evidence yet?

P9 connects existing reconciliation artifacts to the Campaign control loop while preserving the distinction between measurement and semantic judgment.

### Existing repository concepts P9 should reuse

The repository already has two specialized agent-native responsibilities:

1. `output-reconciler`
   - responsibility type: `output_reconciliation`;
   - output artifact: `reconciliation_report`;
   - compares a work claim against durable repository evidence;
   - classifies claims such as `verified`, `disputed`, or `omitted`;
   - recommendations/dispositions remain evidence for a later decision, not automatic Campaign transitions.

2. `repair-verifier`
   - responsibility type: `repair_verification`;
   - output artifact: `repair_verification_report`;
   - re-measures original findings against fresh repository evidence;
   - records `findings_closed` and `findings_remaining`;
   - remaining findings require explicit handling rather than silent approval.

P9 should also reuse:

- P4 artifact admission as the only promotion path from artifact bytes to admitted Campaign evidence;
- P5 explicit `advance`, `defer`, and `close` decisions;
- P6 capability metadata for reconciliation and repair-verification responsibilities;
- P8 exact evidence-consumption lineage;
- current `TransitionRecord` and trace identity;
- existing artifact IDs and artifact contracts rather than introducing competing formats.

### Required control shape

```text
bounded work / durable work claim
        ↓
AGENT decides reconciliation is warranted
        ↓
output-reconciler produces reconciliation_report
        ↓
P4 validates + admits exact report
        ↓
optional authorized repair responsibility
        ↓
repair-verifier produces repair_verification_report
        ↓
P4 validates + admits exact report
        ↓
P9 mechanically reconstructs current reconciliation evidence/stage
        ↓
AGENT interprets that evidence
        ↓
explicit P5 advance / defer / close decision
        ↓
P8 binds exact consumed reconciliation evidence
```

### Initial product surface

Prefer a narrow read-only agent-consumable command:

```text
sensemaking-skills campaign reconciliation \
  --workspace <CMP> \
  [--json]
```

The command should reconstruct facts such as:

- admitted `reconciliation_report` evidence refs and exact artifact identity;
- admitted `repair_verification_report` evidence refs and exact artifact identity;
- whether each report has been explicitly consumed by a committed Campaign transition;
- which transition consumed it, when mechanically reconstructible;
- whether reconciliation evidence exists but no explicit Campaign disposition has yet consumed it;
- whether an earlier report has been superseded mechanically by a later admitted report of the same artifact kind, if this can be established without semantic inference.

If the implementation cannot establish a relation mechanically, it must report uncertainty/absence rather than infer it.

### Disposition requirement

P9 should make this state explicit:

```text
admitted reconciliation evidence
+ no committed transition consumes it
= disposition_required
```

This is a mechanical statement about durable records only. It does not prescribe what the disposition should be.

Once a P5 authored transition explicitly consumes the reconciliation evidence, P8 should remain the source of truth for the exact evidence-consumption edge.

### Artifact verdict fields are not transition rules

P9 must never implement mappings like:

```text
all reconciliation claims verified
→ auto-advance

any disputed claim
→ auto-defer

all repair findings closed
→ auto-close goal_achieved

any finding remaining
→ auto-close external_blocker
```

Those are semantic decisions for the active coding agent.

### P9 must preserve

```text
artifact validated
!= artifact semantically accepted

reconciliation report admitted
!= reconciliation complete

repair verification report admitted
!= repair sufficient

finding closed mechanically
!= Campaign goal achieved

finding remaining
!= automatic defer/close

reconciliation evidence available
!= authority to repair
```

### P9 must not

- interpret reconciliation prose/findings into a semantic Campaign decision;
- infer repair authorization from recommendations/findings;
- automatically invoke `output-reconciler` or `repair-verifier`;
- bypass P4 artifact admission;
- mutate P8 consumption lineage during read-only inspection;
- create a second semantic transition ledger;
- alter P2 crash/recovery semantics;
- grant capability availability or execution authority;
- treat validator success as evidence that the reconciliation conclusion is true.

### Qualification direction

A qualified P9 candidate should prove at least:

1. admitted `reconciliation_report` evidence is mechanically discoverable by exact P4 provenance;
2. admitted `repair_verification_report` evidence is mechanically discoverable by exact P4 provenance;
3. an unadmitted file with either artifact-like name is ignored as reconciliation evidence;
4. a report not consumed by any committed transition is reported as `disposition_required` (or an equivalent mechanically explicit state);
5. after an explicit P5 transition consumes the report, P9 points to the exact P8-bound transition/evidence relation;
6. verdict content such as `verified/disputed/closed/remaining` does not automatically change Campaign state;
7. multiple reports are ordered/differentiated only by mechanically available durable provenance, never semantic preference;
8. stale/tampered admission/lineage state fails closed through existing P4/P8 integrity checks;
9. P9 inspection is deterministic and read-only;
10. JSON output contains no recommended action, selected capability, inferred authority, semantic score, or automatic disposition;
11. fresh-process reconstruction works from durable Campaign files alone;
12. the installed wheel exposes the P9 surface without source checkout.

## 8. Remaining planned milestones

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
→ reconciliation / repair verification
→ explicit reconciliation disposition
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
→ reconciliation / repair verification
→ explicit reconciliation disposition
→ transition
→ lineage inspection
→ handoff
→ fresh-context resume
→ justified continuation or terminal stop
```

with deterministic reconstruction and **without manual Campaign/artifact repair or prior conversation memory as hidden input**.
