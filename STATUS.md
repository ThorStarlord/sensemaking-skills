# Status

**Version:** 0.2.2  
**Last updated:** 2026-09-08  
**Current phase:** Productization / implementation  
**Primary program:** Sensemaking Skills v0.3 campaign-based productization  
**Current frontier:** P10 — harness adapters

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

The current integrated implementation frontier after P9 is:

```text
main@0f306cb9f05a70f2b27a64c05f65749534f9f0e1
```

That merge has parents:

```text
previous main
54691b934eb67d5fbedec1706ff63031210044a8

exact-qualified P9 head
7364f1140587e71c391f59c0362227aa35a1500c
```

and its tree is exactly the qualified P9 tree:

```text
02401cef805a541affb6f29bc66da886ffd7e9ab
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

## Current implementation frontier — P10

The next bounded slice is **P10 — Harness adapters**.

P10 improves Skill setup for Claude Code, Codex, OpenCode, and portable/generic Agent Skills locations without allowing agent-specific filesystem rules to become Campaign semantics.

The intended control shape is:

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

Compatibility remains for `agents`, `claude-superpowers`, `all`, and `custom`. Project scope requires an explicit existing `--project-root`; user-scope/project-scope options must not be silently mixed.

P10 must preserve:

```text
copied to declared discovery root
!= harness observed Skill
!= Skill selected
!= execution authorized
!= Campaign decision
```

It must not:

- detect the active coding-agent process;
- infer a project root from cwd/git/editor state;
- silently fall back among unrelated discovery roots;
- select or invoke a Skill after copying it;
- create or mutate Campaign state;
- imply that copied Skills are semantically available, warranted, or authorized;
- overwrite divergent installed Skill trees without explicit `--force`.

See [`docs/harness-adapters.md`](docs/harness-adapters.md).

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

1. **P10 — Harness adapters** — CURRENT.
2. **P11 — External golden-path qualification and v0.3 release**.

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
