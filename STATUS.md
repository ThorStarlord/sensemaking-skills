# Status

**Version:** 0.2.2  
**Last updated:** 2026-09-08  
**Current phase:** Productization / implementation  
**Primary program:** Sensemaking Skills v0.3 campaign-based productization  
**Current frontier:** P9 — reconciliation lifecycle

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

The current integrated implementation frontier after P8 is:

```text
main@e1b900c32d932d5e4b5c0366c0972143c36b1982
```

That merge has parents:

```text
previous main
842bf7d14cff71ec96efa270fa54adbe4243f586

exact-qualified P8 head
5baf360027c7c6e46d95f17fa03608e9303dd55d
```

and its tree is exactly the qualified P8 tree:

```text
77b2b076d4082b7aa66fdd98b88c92e12d3091a8
```

## What is implemented

### P0 — Productization pivot — MERGED

Implementation-first direction is durable. Prior research remains preserved with its actual claim ceilings.

### P1 — Durable campaign workspace — MERGED

Isolated file-backed Campaign persistence, strict typed load/dump boundaries, atomic current-state replacement, append-only transitions, append-preserving trace, fail-closed physical path containment, and non-overwrite initialization.

### P2 — Campaign service — MERGED

Deterministic lifecycle service with recoverable transition + state commit intent, structural validation/reconstruction, defer/terminate primitives, handoff generation, resume, and transition/state digest binding.

### P3 — Campaign CLI foundation — MERGED

Implemented:

```text
sensemaking-skills campaign init
sensemaking-skills campaign status
sensemaking-skills campaign validate
sensemaking-skills campaign history
```

### P4 — Validated artifact ingestion — MERGED

Implemented:

```text
sensemaking-skills campaign ingest
```

Trust boundary:

```text
artifact bytes
→ canonical validator router
→ selected validator
→ valid=true
→ content-addressed artifact
→ append-only admission receipt
→ Campaign evidence
```

Therefore:

```text
file exists
!= validated artifact
!= admitted Campaign evidence
```

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
durable evidence
→ AGENT judgment
→ typed decision contract
→ CampaignService
→ recoverable state + transition + trace
```

No P5 command ranks/selects capabilities, interprets artifact semantics, grants authority, or creates a second persistence path.

See [`docs/campaign-decisions.md`](docs/campaign-decisions.md).

### P6 — Real capability registry — MERGED

Implemented:

```text
sensemaking-skills campaign capabilities
```

Catalog membership, runtime availability, and execution authority remain separate facts. Results are deterministic and unranked; P6 never selects or invokes work.

See [`docs/capability-registry.md`](docs/capability-registry.md).

### P7 — Durable handoff/resume UX — MERGED

Implemented:

```text
sensemaking-skills campaign handoff
sensemaking-skills campaign resume
```

P7 integrity-binds fresh-context reconstruction without changing the semantic `CampaignHandoff` schema or inventing next action, responsibility, capability, or authority.

See [`docs/campaign-handoff-resume.md`](docs/campaign-handoff-resume.md).

### P8 — Artifact/evidence lineage — MERGED

Implemented:

```text
sensemaking-skills campaign lineage
```

P8 makes exact evidence identity and explicit transition consumption reconstructible without making lineage a semantic decision system.

Control shape:

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

Key properties:

- raw `evidence/**` cited by an authored decision is snapshotted by SHA-256 before lifecycle commit;
- P4 admitted artifacts reuse their existing content-addressed identity and admission provenance;
- cited admission receipts preserve exact consumed bytes plus validator/artifact provenance;
- unadmitted files under `artifacts/` remain non-evidence;
- every P8-authored `advance`, `defer`, or `close` decision gets a bound consumption receipt, including explicit zero-evidence decisions;
- pre-P8/direct-P2 transitions without receipts remain honestly `legacy_unbound`;
- orphan precommit intents never become false committed consumption edges;
- tampered/ambiguous lineage fails closed;
- `campaign lineage` is read-only and contains no recommendation, ranking, semantic-sufficiency, or authority inference.

See [`docs/campaign-lineage.md`](docs/campaign-lineage.md).

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
→ work evidence
→ reconciliation / repair verification
→ agent authors continuation/defer/close decision
→ durable transition
→ lineage inspection
→ handoff
→ fresh-context resume
→ continue / stop
```

## Current implementation frontier — P9

The next bounded slice is **P9 — Reconciliation lifecycle**.

P9 should connect the repository's existing `output-reconciler` and `repair-verifier` artifact semantics to the durable Campaign lifecycle without allowing either artifact or its validator to decide the Campaign transition automatically.

Existing research/product concepts already distinguish:

```text
mechanical validation
!= reconciliation
!= repair verification
!= semantic continuation decision
```

The intended P9 control shape is:

```text
bounded work / work claim
        ↓
agent selects reconciliation responsibility
        ↓
reconciliation_report is produced and admitted through P4
        ↓
optional authorized repair
        ↓
repair_verification_report is produced and admitted through P4
        ↓
AGENT interprets the admitted reconciliation evidence
        ↓
explicit Campaign advance / defer / close decision
        ↓
P8 records exact evidence consumption lineage
```

P9 should make the intermediate reconciliation state mechanically inspectable and require an explicit agent-authored disposition. It must not map artifact fields such as `verified`, `disputed`, `closed`, or `remaining` directly to a Campaign transition.

A useful initial surface should remain narrow and deterministic, for example:

```text
sensemaking-skills campaign reconciliation --workspace <CMP> [--json]
```

or an equivalent typed service that reports mechanically present reconciliation evidence and whether an explicit disposition is still required.

P9 should reuse:

- P4 admitted artifact receipts and exact artifact identity;
- P5 authored decisions;
- P6 capability metadata for `output_reconciliation` / `repair_verification` responsibilities;
- P8 evidence-consumption lineage;
- existing `reconciliation_report` and `repair_verification_report` artifact contracts;
- existing semantic vocabulary distinguishing validation, reconciliation, and verification.

P9 must preserve:

```text
reconciliation report admitted
!= reconciliation semantically accepted

repair verification report admitted
!= repair sufficient

finding closed mechanically
!= Campaign goal achieved

finding remaining
!= automatic defer/close
```

It must not:

- parse a reconciliation verdict into an automatic Campaign decision;
- grant repair authority from a finding or recommendation;
- infer that all `verified` claims justify continuation;
- infer that all `remaining` findings require closure;
- bypass P4 artifact admission;
- create a second transition log;
- weaken P8 lineage or P2 reconstruction;
- turn `output-reconciler` or `repair-verifier` into a semantic router.

## Semantic-control invariant

Agent:

- What does reconciliation evidence mean?
- Is repair warranted and authorized?
- Is repair verification sufficient for the blocked decision?
- Should the Campaign advance, defer, or close?

Deterministic machinery:

- Is the reconciliation/verification artifact admitted evidence?
- What exact artifact identity/provenance does it have?
- Which reconciliation stage is mechanically represented?
- Is an explicit disposition recorded?
- Which transition explicitly consumed the evidence?
- Is history reconstructible?

Therefore:

```text
validator passed != conclusion is true
warranted responsibility != available capability
available capability != authorized capability
recommendation != execution authority
handoff != semantic recommendation
lineage != semantic warrant
reconciliation evidence != Campaign decision
```

And:

```text
Campaign Controller != semantic router
```

## Remaining v0.3 sequence

1. **P9 — Reconciliation lifecycle** — CURRENT.
2. **P10 — Harness adapters**.
3. **P11 — External golden-path qualification and v0.3 release**.

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
→ reconcile / verify repair
→ explicitly disposition the reconciliation
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
| Artifact/evidence lineage | `docs/campaign-lineage.md` |
| SkillOpt influence/adaptation and research boundary | `docs/research/skillopt-adaptation.md` |
| Agent-native operating model | `docs/agent-native-operating-workflow.md` |
| Decision vs orchestration boundary | `docs/decision-orchestration-boundary.md` |
| Campaign semantic contract | `docs/campaign-semantics.md`, `src/sensemaking_skills/campaign_semantics/` |
| Validated artifact ingestion | `docs/artifact-ingestion.md` |
| Workflow catalog/liveness | `docs/workflow-system-disposition.md`, ADR 0027 |
| Design decisions | `docs/adr/` — always read each ADR's status |
| Historical research/evidence | `experiments/`, `docs/research/`, `docs/campaigns/` |
| Installation and usage | `README.md`, `GETTING_STARTED.md`, `INSTALLATION.md` |
