# Sensemaking Skills v0.3 Productization Plan

**Status:** ACTIVE owner direction  
**Effective:** 2026-09-08  
**Base at pivot:** `main@5c2c807542f7e150d4a031430f59e297ed816b24`  
**Current integrated frontier:** P10 merged at `main@d833095ab9b37bd9a93d39d286b358061eb913e5`  
**Current implementation frontier:** P11 — external golden-path qualification and v0.3 release  
**Primary objective:** turn the ratified agent-native control model into the first usable Campaign-based release.  
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
- Packaging a validator runtime does not create new semantic validator authority.

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

Lineage is a reconstruction of identities, provenance, and explicit consumption links. Reconciliation lifecycle state may summarize mechanically present reconciliation evidence, but must never become a second semantic decision system. Harness adapters and release packaging remain infrastructure outside this semantic core.

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
| **P10 — Harness adapters** | **MERGED** | Explicit Skill discovery-root setup for Claude Code, Codex, OpenCode, and portable/generic environments without harness auto-detection. |
| **P11 — v0.3 qualification/release** | **CURRENT** | Make the distribution self-contained, prove the frozen external golden path through a real harness, prove fresh-context resume, then qualify/release v0.3.0. |

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

P11 release hardening derives the same canonical repository validator code/contracts into the built wheel so installed ingestion no longer needs a separate framework checkout in normal use. The admission receipt continues to bind the exact router and selected validator bytes that actually ran.

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

P8 distinguishes raw evidence, admitted artifacts, and admission receipts while preserving exact byte identity and historical claim ceilings. A P8-authored zero-evidence decision receives an explicit empty bound receipt. Historical/direct-P2 transitions without receipts remain `legacy_unbound`. Orphan precommit intents do not create false committed consumption edges.

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

### P10 — Harness adapters — MERGED

Implemented explicit setup targets through the existing `setup-skills` command:

```text
agents/generic
claude
codex
opencode
claude-superpowers
all
custom
```

Canonical adapter roots distinguish user and project scope. Codex user scope honors `$CODEX_HOME/skills` while project scope uses `.agents/skills`; OpenCode project scope uses `.opencode/skills`; Claude project scope uses `.claude/skills`.

P10 is deterministic setup infrastructure only:

```text
copied to declared discovery root
!= harness observed Skill
!= Skill selected
!= execution authorized
!= Campaign decision
```

See [`harness-adapters.md`](harness-adapters.md).

## 7. Current implementation frontier — P11

P11 is **v0.3 external qualification and release**. It is not a new semantic product layer.

### Goal

Prove that the integrated P0–P10 product can complete its canonical lifecycle from a real installed distribution, on a real external repository, through a real supported coding-agent harness, and across a genuine fresh-context boundary.

Required release sequence:

```text
P10 integrated
→ remove release-portability blockers
→ freeze qualification protocol
→ freeze exact candidate/target/harness attempt
→ real external golden path
→ fresh-context reconstruction proof
→ repair observed blockers through new attempts
→ freeze v0.3.0 release metadata
→ build + exact-head qualify final distribution
→ merge
→ release
→ clean production-install verification
```

### P11-A — P10 integration — COMPLETE

P10 was merged from exact-qualified head:

```text
d1676b6f0209eee4c5e2c9fdb7aae07baaa74a1a
```

into:

```text
main@d833095ab9b37bd9a93d39d286b358061eb913e5
```

The merge tree is exactly the qualified P10 tree:

```text
6143b47f31ccdab2e1bde9be12a31bef9864e71f
```

### P11-B — Self-contained artifact validation — IMPLEMENTED / REQUALIFICATION PENDING

The pre-P11 release blocker was:

```text
pip install sensemaking-skills
→ campaign ingest still required --framework-root
→ separate Sensemaking source checkout required
```

P11 changes deployment to:

```text
canonical repository scripts/ + skills/
→ build-time derived validator_runtime/
→ installed wheel
→ campaign ingest without --framework-root
→ canonical router / selected validator
→ unchanged P4 admission receipt/provenance
```

The repository-root `scripts/` and `skills/` trees remain the single maintained sources. Build-time derivation avoids a second hand-maintained validator implementation.

An explicit `--framework-root` remains an authoritative development/compatibility override. If it is malformed, ingestion fails closed rather than silently falling back to the installed runtime.

A preliminary exact-head Validator Ecosystem run on the repaired portability bytes passed both Python campaign lanes with **569 tests**, plus the existing Two-Lane/path-containment and installed-distribution regressions. The current branch also includes the frozen protocol/status reconciliation, so it must receive a new exact-head run before P11-B is called frozen/qualified.

### P11-C — External golden-path protocol — FROZEN

The qualification authority is:

[`v0.3-external-qualification-protocol.md`](v0.3-external-qualification-protocol.md)

It requires each attempt to freeze, before substantive execution:

- Sensemaking candidate commit/tree;
- wheel filename and SHA-256;
- runtime OS/Python;
- real coding-agent harness identity/version;
- P10 adapter target/scope;
- external repository branch/commit/tree;
- bounded engineering goal;
- Campaign identity/workspace;
- prohibition on manual Campaign/artifact/validator repair;
- fresh-context rule forbidding prior-chat reasoning from being supplied to the new agent.

A changed candidate or target starts a new attempt. A failed run is preserved as FAIL; product repair occurs on new bytes/new attempt identity. The attempt is never edited in place into a PASS.

### P11-D — External golden path — REQUIRED NEXT

The real attempt must execute:

```text
start
→ repository diagnosis via real agent-native repo-sensemaker Skill
→ validated artifact admission from installed distribution
→ agent-authored responsibility/authority decision
→ capability inspection
→ bounded work
→ durable evidence
→ reconciliation / repair verification
→ explicit reconciliation disposition
→ durable transition
→ lineage inspection
→ handoff
→ fresh-context resume
→ justified continuation or terminal stop
```

The target must be a real repository other than `sensemaking-skills` and remain frozen for the attempt.

P10 filesystem setup alone does not satisfy the harness requirement. P11 needs evidence that a real supported harness actually observed/invoked the Skill through its native Skill mechanism.

### P11-E — Fresh-context proof — REQUIRED

After handoff, the original semantic context ends. The fresh agent may receive the target repository, Campaign workspace, installed candidate, and durable handoff reference. It may not receive the old chat transcript, private reasoning summary, or manual semantic coaching that substitutes for durable Campaign state.

An honest stop such as `evidence_insufficient`, `owner_decision_required`, or `authority_boundary_reached` can be valid if warranted. Qualification does not force work merely to produce activity.

### P11-F — Release freeze after PASS

Only after a real external PASS:

1. reconcile package version consistently to `0.3.0`;
2. update README, STATUS, CHANGELOG, productization docs, and publishing instructions;
3. build wheel + sdist;
4. run metadata/distribution checks;
5. run the complete exact-head Validator Ecosystem;
6. freeze candidate SHA/tree and distribution digests;
7. record the successful external attempt identity/evidence;
8. mark the P11 PR ready only after all qualification evidence is durable.

### P11 must preserve

```text
validator passed != semantic truth
admitted evidence != warranted responsibility
capability availability != selection or authority
reconciliation evidence != semantic disposition
lineage != semantic warrant
handoff != semantic recommendation
Skill copied != harness observed/invoked Skill
```

### P11 must not

- introduce a central semantic router;
- rank or auto-select capabilities;
- make validator output a semantic transition rule;
- repair a failed qualification workspace/artifact manually and call it PASS;
- smuggle prior-agent reasoning across the fresh-context boundary;
- claim all repositories/harnesses from one qualifying run;
- bump/release `0.3.0` before the real golden-path PASS;
- infer release or merge authority from CI success alone.

## 8. P11 external qualification claim ceiling

A successful attempt supports only:

> One exact Sensemaking Skills candidate completed the canonical Campaign golden path on one frozen external repository through one real supported coding-agent harness, with deterministic reconstruction, no manual Campaign/artifact repair, and no prior conversation memory supplied to the fresh-context agent.

The protocol explicitly rejects stronger generalization.

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

The required qualification authority is [`v0.3-external-qualification-protocol.md`](v0.3-external-qualification-protocol.md).
