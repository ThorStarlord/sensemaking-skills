# Sensemaking Skills v0.3 Productization Plan

**Status:** ACTIVE owner direction  
**Effective:** 2026-09-08  
**Base at pivot:** `main@5c2c807542f7e150d4a031430f59e297ed816b24`  
**Primary objective:** turn the ratified agent-native control model into a usable campaign-based engineering product.

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

## 5. Milestones

### P0 — Productization pivot

- make this productization direction durable;
- stop treating formal experiment execution as the active product-development program;
- preserve existing research evidence and explicit claim ceilings;
- do not merge incomplete research branches merely to close them.

### P1 — Durable campaign workspace

Deliver a file-backed campaign workspace outside the target repository by default/contract for v0.3.

Expected shape:

```text
CMP-XXXX/
├── campaign-state.yaml
├── campaign-policy.yaml          # optional
├── campaign-handoff.yaml         # optional/current handoff
├── trace.yaml
├── transitions/
├── artifacts/
└── evidence/
```

Storage invariants:

- `campaign-state.yaml` is a replaceable current snapshot;
- transition records are append-only;
- trace history is append-preserving;
- state replacement is atomic;
- initialization does not overwrite an existing workspace;
- when a target repository is supplied, the campaign workspace must not live inside that repository;
- every persisted semantic artifact passes the existing strict campaign-semantic loader before it is accepted.

P1 deliberately does **not** implement atomic state+transition lifecycle changes. That belongs to P2 so storage does not silently become the campaign controller.

### P2 — Campaign service

Add the deterministic lifecycle operations that compose store primitives safely:

- initialize;
- validate;
- atomically record transition + replacement state;
- defer responsibility;
- terminate;
- generate handoff;
- resume/reconstruct.

The service validates contracts and authority metadata but does not decide which responsibility is semantically warranted.

### P3 — Campaign CLI foundation

Expose real product commands rather than instruction-only wrappers:

```text
sensemaking-skills campaign init
sensemaking-skills campaign status
sensemaking-skills campaign validate
sensemaking-skills campaign history
```

### P4 — Validated artifact ingestion

Reuse the canonical artifact parser/validator boundary. Ingesting an artifact makes it durable evidence; it does not automatically select the next Skill or workflow.

### P5 — Agent-authored decisions

Add bounded commands/contracts for:

```text
campaign advance
campaign defer
campaign close
```

The machine prepares/validates the contract; the active agent supplies the semantic decision.

### P6 — Real capability registry

Populate responsibility-to-capability metadata while preserving the distinction:

```text
warranted responsibility
!= capability availability
!= execution authority
```

No ranking or automatic routing is introduced.

### P7 — Durable handoff/resume

Make `campaign handoff` and `campaign resume` a first-class experience. A fresh coding-agent context must be able to reconstruct the current campaign from the handoff and referenced artifacts.

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

## 6. Explicit non-goals for v0.3

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

## 7. Experiment disposition

Research and experimental scaffolds remain available as laboratories and historical evidence. They are not the default active program.

In particular, EXP-0006 may be stopped at its actual completed boundary. Preserve the diagnostic attempts, holdout freeze, contamination audit, and claim ceilings. Do not manufacture a Skill candidate merely to exercise the qualification mechanism.

## 8. Immediate implementation sequence

The first bounded implementation branch should deliver **P0 + P1** only:

1. make the pivot durable;
2. introduce the isolated campaign workspace abstraction;
3. introduce a file-backed `CampaignStore` using the existing strict semantic loaders/dumpers;
4. add regressions for isolation, non-overwrite, round-trip loading, atomic state replacement, append-only transitions, trace append behavior, campaign identity, and fail-closed contract corruption;
5. stop before semantic lifecycle/service or CLI behavior.

That boundary creates the smallest new product capability on which every later vertical slice can safely build.
