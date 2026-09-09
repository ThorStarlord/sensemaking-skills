# Sensemaking Skills v0.3 Productization Plan

**Status:** ACTIVE owner direction  
**Effective:** 2026-09-08  
**Base at pivot:** `main@5c2c807542f7e150d4a031430f59e297ed816b24`  
**Current integrated frontier:** P9 merged at `main@0f306cb9f05a70f2b27a64c05f65749534f9f0e1`  
**Current implementation frontier:** P10 — harness adapters  
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
- Harness setup/discovery-root mapping does not establish runtime Skill availability, selection, or execution authority.

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

Skill copied to discovery root
!= Skill selected or authorized
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

Lineage is a reconstruction of identities, provenance, and explicit consumption links. Reconciliation lifecycle state may summarize mechanically present reconciliation evidence, but must never become a second semantic decision system. Harness adapters remain packaging/setup infrastructure outside this semantic core.

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
| **P9 — Reconciliation lifecycle** | **MERGED** | Admitted reconciliation/repair-verification evidence is mechanically correlated with explicit P8-bound Campaign disposition without semantic auto-routing. |
| **P10 — Harness adapters** | **CURRENT** | Explicit Skill discovery-root setup for Claude Code, Codex, OpenCode, and portable/generic environments without harness auto-detection. |
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

### P9 — Reconciliation lifecycle — MERGED

Implemented:

```text
sensemaking-skills campaign reconciliation
```

P9 is a read-only reconstruction over P4 admission provenance and P8 consumption edges. It identifies admitted `reconciliation_report` / `repair_verification_report` evidence and reports whether an explicit exact-byte-bound Campaign transition has consumed each report.

Mechanical states are:

```text
disposition_required
disposition_recorded
legacy_unbound
```

`disposition_recorded` means only that an explicit Campaign transition consumed the exact report. It does not claim that the report was correct, reconciliation is semantically complete, or the transition was the right decision. Report verdict content never becomes an automatic transition rule.

See [`campaign-reconciliation.md`](campaign-reconciliation.md).

## 7. Current implementation frontier — P10

The next bounded implementation slice is **P10 — Harness adapters**.

### Goal

Make the packaged Skill trees installable into major coding-agent discovery roots through one explicit, deterministic setup surface while keeping harness-specific concerns outside Campaign semantics.

The required control shape is:

```text
caller explicitly selects harness + scope
        ↓
deterministic adapter resolves declared discovery root
        ↓
exact packaged Skill tree copied
        ↓
existing drift check
        ↓
explicit --force required for replacement
```

P10 must not detect which harness is running or infer which Skill should be used.

### Initial product surface

Extend the existing setup command rather than create a second installer:

```text
sensemaking-skills setup-skills \
  --target agents|generic|claude|codex|opencode|claude-superpowers|all|custom \
  [--scope user|project] \
  [--project-root <repo>] \
  [--skills-dir <custom-root>] \
  [--dry-run] \
  [--force]
```

### Adapter contract

P10 should encode the currently documented discovery roots explicitly:

```text
generic user       ~/.agents/skills
generic project    <project>/.agents/skills

Claude user        ~/.claude/skills
Claude project     <project>/.claude/skills

Codex user         $CODEX_HOME/skills (default ~/.codex/skills)
Codex project      <project>/.agents/skills

OpenCode user      ~/.config/opencode/skills
OpenCode project   <project>/.opencode/skills
```

`agents` remains a compatibility alias for `generic`. The historical `claude-superpowers`, `all`, and `custom` targets remain available.

Codex `CODEX_HOME` is explicit environment configuration. Reading it is not active-harness detection.

### P10 must preserve

```text
copied to declared discovery root
!= harness observed Skill
!= Skill selected
!= execution authorized
!= Campaign decision
```

It must also preserve the existing fail-closed drift rule:

```text
missing -> copy
current -> no-op success
different -> preserve installed bytes + report failure
--force -> explicit replacement
```

Project scope requires an explicit existing `--project-root`; it must not infer the repository from cwd, git, an editor, or a running harness.

### P10 must not

- auto-detect Claude Code, Codex, OpenCode, or another active agent process;
- silently fall back among unrelated harness discovery roots;
- select or invoke a Skill after copying it;
- imply that copied Skills were observed by the current harness;
- grant capability availability or execution authority;
- create or mutate Campaign state;
- place harness-specific filesystem semantics inside `campaign_semantics`;
- bypass existing packaged Skill-tree drift checks;
- overwrite a divergent Skill tree without explicit `--force`.

### Qualification direction

A qualified P10 candidate should prove at least:

1. `agents` remains a compatibility alias for `generic`;
2. Claude user/project discovery roots resolve deterministically;
3. Codex personal `$CODEX_HOME/skills` and project `.agents/skills` are represented separately;
4. OpenCode native user/project roots resolve deterministically;
5. project scope fails closed without an explicit existing project root;
6. incompatible setup options fail closed rather than being silently ignored;
7. `all` deduplicates shared project roots deterministically;
8. exact complete packaged Skill trees are copied;
9. divergent installed trees remain untouched without `--force`;
10. dry-run creates no destination state;
11. no setup path creates Campaign state or semantic selection/authority output;
12. pre-P10 compatibility targets remain available;
13. the installed wheel exposes the P10 setup surface without source checkout.

See [`harness-adapters.md`](harness-adapters.md).

## 8. Remaining planned milestones

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
