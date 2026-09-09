# Status

**Version:** 0.2.2  
**Last updated:** 2026-09-09  
**Current phase:** Productization / release qualification  
**Primary program:** Sensemaking Skills v0.3 campaign-based productization  
**Current frontier:** P11 — external golden-path qualification and v0.3 release

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

The current integrated implementation frontier after P10 is:

```text
main@d833095ab9b37bd9a93d39d286b358061eb913e5
```

That merge has parents:

```text
previous main
0f306cb9f05a70f2b27a64c05f65749534f9f0e1

exact-qualified P10 head
d1676b6f0209eee4c5e2c9fdb7aae07baaa74a1a
```

and its tree is exactly the qualified P10 tree:

```text
6143b47f31ccdab2e1bde9be12a31bef9864e71f
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

P11 release hardening now derives the canonical validator runtime into the built distribution so normal installed-wheel ingestion no longer needs a separate Sensemaking source checkout. This changes deployment portability, not P4 semantic authority or provenance.

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

### P9 — Reconciliation lifecycle — MERGED

Implemented:

```text
sensemaking-skills campaign reconciliation
```

P9 reconstructs admitted reconciliation/repair-verification evidence through P4 provenance and correlates it with exact P8 transition-consumption edges.

Mechanical states are:

```text
disposition_required
disposition_recorded
legacy_unbound
```

`disposition_recorded` means an explicit Campaign transition consumed the exact report. It does not mean the report was correct, reconciliation is semantically complete, or the transition was the right decision. Verdict-like report content never automatically mutates Campaign state.

See [`docs/campaign-reconciliation.md`](docs/campaign-reconciliation.md).

### P10 — Harness adapters — MERGED

Implemented explicit, deterministic Skill setup for Claude Code, Codex, OpenCode, and portable/generic Agent Skills roots through the existing `setup-skills` command.

The first-class adapter roots are:

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

P10 preserves:

```text
copied to declared discovery root
!= harness observed Skill
!= Skill selected
!= execution authorized
!= Campaign decision
```

There is no active-harness auto-detection and no Campaign semantic mutation.

See [`docs/harness-adapters.md`](docs/harness-adapters.md).

## Current productization objective — P11

The v0.3 north-star outcome is:

> A coding agent can start a durable Sensemaking Campaign on a real repository, consume validated diagnostic artifacts, record warranted responsibility and authority, inspect available capabilities, perform bounded work, validate/reconcile the result, hand the Campaign to a fresh agent, and continue or terminate without relying on prior conversation memory.

The required external golden path is:

```text
start
→ repository diagnosis
→ validated artifact admission
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

P11 has two distinct kinds of evidence:

1. **Mechanical release portability** — CI/fresh-wheel proofs that the built distribution contains the deterministic runtime needed by the golden path.
2. **Real product qualification** — one frozen external-repository run through one real supported coding-agent harness, including fresh-context resume.

The first cannot substitute for the second.

### P11 release-portability prerequisite

P11 now makes `campaign ingest` self-contained in normal installed-distribution use:

```text
canonical repository scripts/ + skills/
→ build-time derived validator_runtime/
→ installed wheel
→ campaign ingest without --framework-root
→ unchanged P4 admission receipt/provenance
```

The repository-root validator and Skill trees remain the single maintained sources. An explicit `--framework-root` is retained only as a development/compatibility override and fails closed when invalid.

A fresh-wheel regression proves valid admission, invalid rejection, exact router/validator SHA-256 provenance, evidence reconstruction, and explicit bad-override failure from outside the source checkout.

### P11 external qualification protocol

The execution authority is [`docs/v0.3-external-qualification-protocol.md`](docs/v0.3-external-qualification-protocol.md).

The protocol requires, before execution:

- exact Sensemaking candidate SHA/tree and wheel digest;
- exact external target SHA/tree and bounded goal;
- real harness identity;
- immutable attempt manifest;
- prohibited-manual-repair policy;
- a genuine fresh-context boundary with no prior-chat reasoning supplied.

A failed attempt is preserved as FAIL and repaired through a new product candidate/new attempt. It is never edited in place into a PASS.

P11 is **not complete** until the real harness/external-repository attempt passes and the final release candidate receives exact-head release qualification.

## Semantic-control invariant

Agent:

- What responsibility is warranted?
- Which available capability, if any, should be selected?
- Is execution authorized?
- What does reconciliation evidence mean?
- Should the Campaign advance, defer, or close?

Deterministic machinery:

- Is an artifact admitted evidence?
- What exact identity/provenance does it have?
- Which transition explicitly consumed it?
- Is reconciliation disposition mechanically represented?
- Which explicit harness/scope destination did the caller request?
- Does the installed Skill tree match the packaged bytes?
- Is Campaign history reconstructible?

Therefore:

```text
validator passed != conclusion is true
warranted responsibility != available capability
available capability != authorized capability
recommendation != execution authority
handoff != semantic recommendation
lineage != semantic warrant
reconciliation evidence != Campaign decision
harness discovery path != Skill selection or authority
```

And:

```text
Campaign Controller != semantic router
```

## Remaining v0.3 sequence

1. **P11-B release portability** — implemented; current branch requires final exact-head requalification after protocol/status reconciliation.
2. Freeze one exact release-candidate/target/harness attempt manifest.
3. Execute the real external golden path through the real harness.
4. Execute the fresh-context resume proof without prior-chat memory.
5. Repair only observed blockers through new candidate bytes/new attempt identities.
6. After PASS, reconcile version/release metadata to `0.3.0`, build wheel + sdist, run metadata/distribution checks, and exact-head qualify the final P11 candidate.
7. Merge/release only under explicit owner authorization.

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
| v0.3 external qualification protocol | `docs/v0.3-external-qualification-protocol.md` |
| Agent-authored campaign decisions | `docs/campaign-decisions.md` |
| Capability registry inspection | `docs/capability-registry.md` |
| Durable handoff/resume | `docs/campaign-handoff-resume.md` |
| Artifact/evidence lineage | `docs/campaign-lineage.md` |
| Reconciliation lifecycle | `docs/campaign-reconciliation.md` |
| Coding-agent harness adapters | `docs/harness-adapters.md` |
| SkillOpt influence/adaptation and research boundary | `docs/research/skillopt-adaptation.md` |
| Agent-native operating model | `docs/agent-native-operating-workflow.md` |
| Decision vs orchestration boundary | `docs/decision-orchestration-boundary.md` |
| Campaign semantic contract | `docs/campaign-semantics.md`, `src/sensemaking_skills/campaign_semantics/` |
| Validated artifact ingestion | `docs/artifact-ingestion.md` |
| Workflow catalog/liveness | `docs/workflow-system-disposition.md`, ADR 0027 |
| Design decisions | `docs/adr/` — always read each ADR's status |
| Historical research/evidence | `experiments/`, `docs/research/`, `docs/campaigns/` |
| Installation and usage | `README.md`, `GETTING_STARTED.md`, `INSTALLATION.md` |
