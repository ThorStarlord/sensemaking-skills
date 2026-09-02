# Status

**Version**: 0.2.2 (see [pyproject.toml](pyproject.toml), [CHANGELOG.md](CHANGELOG.md))
**Last updated**: 2026-09-02 (post PR #268 — Campaign 1 closure merged)

This file is the **single living status summary at the repo root**: what the
product is, where development currently is, and how to reconstruct that picture
without prior conversation context. It points at the authoritative documents;
it does not duplicate them. Dated phase/completion/deployment reports are
archived under `docs/archive/phase-reports/` and are not updated here.

## What the product is

An **agent-native engineering sensemaking and control layer for
software-engineering agents** (see [CONTEXT.md](CONTEXT.md)). An active coding
agent owns the recursive control loop (ADR 0013); Sensemaking constrains it with
repository evidence, bounded responsibilities, durable artifacts, validators,
reconciliation, repair verification, and authority boundaries. The ratified
external product scope is the validated, human-reviewed
`repository_sensemaking_brief` (ADR 0014). It is **not** a general
project-goal-to-implementation router, an autonomous multi-repo orchestrator, or
a general development operating system.

## Current product-validation priority

**Goal A — External Product Validation** is the current product-validation
strategy. Canonical protocol:
[docs/research/goal-a-external-product-validation-protocol.md](docs/research/goal-a-external-product-validation-protocol.md).

```text
Goal A       = ACTIVE   (A1 = ACTIVE, absolute product utility)
A2           = DEFERRED / UNAUTHORIZED
Goal B / E3  = FROZEN / DEFERRED
```

Protocol approval does **not** authorize episode execution. The first A1 episode
is **paused at an execution-substrate boundary** (an isolated producer sub-agent
cannot persist its own frozen brief, prove pinned provenance, or re-run the
probe engine; three substrates falsified). The stop boundary is durably recorded
as `experiments/evidence/0023-goal-a-run1-stop-boundary/` and tracked live in
**Issue #255**; the current owner rule is to halt Goal A in this environment
rather than build another harness. Resuming needs an owner/environment decision,
not a repo-code change. Reassessment:
[docs/research/goal-a-execution-readiness-reassessment-2026-08-31.md](docs/research/goal-a-execution-readiness-reassessment-2026-08-31.md).

## Current development direction

### Ratified / operative (do not re-decide without an ADR)

- **ADR 0013** — active coding agent owns the top-level control loop.
- **ADR 0014** — product boundary = validated, human-reviewed
  `repository_sensemaking_brief`; automatic downstream routing deferred.
- **ADR 0026 / 0027** — execution authority is separate from
  recommendation/selection; workflow registry identity is separate from
  liveness; consumers fail closed.
- **ADR 0015 addendum** — `representation_sufficiency` → `MODEL_WARRANT` gate.
- **ADR 0023** — two-lane experiment authorization.
- **Campaign 1** (agent-native, artifact-mediated self-development) —
  `CAMPAIGN_COMPLETE`, merged in **PR #268**. On the product surface: the
  responsibility-level continuation subsection in the operating map; the
  deterministic-machinery + hooks disposition in
  `docs/decision-orchestration-boundary.md`;
  `docs/workflow-system-disposition.md` (23 workflows classified); a lazy
  `workflow_liveness` resolver in `scripts/_validator_utils.py`. No ADR /
  contract / registry / `src/` change. Report:
  [docs/campaigns/agent-native-self-development/FINAL-REPORT.md](docs/campaigns/agent-native-self-development/FINAL-REPORT.md).

### In flight

- **Goal A / A1 episode** — see above; owner/environment decision pending
  (Issue #255).
- **Issue #218** — standing normal-use control-model evidence lane.
- **Issue #226** — blind gate-separation study of the compressed control
  hypothesis (`C6R`); `C6R` frozen until the preregistered result.
- **Semantic Control Map trial** — [docs/semantic-control-map.md](docs/semantic-control-map.md)
  + [docs/semantic-control-map-trial.md](docs/semantic-control-map-trial.md);
  EXPERIMENTAL, `CORE_PERSISTENCE_RATIFIED = false`, min close ~2026-09-28;
  nothing may depend on the map.
- **Campaign 2** (durable repository-level self-development) —
  `docs/campaigns/durable-repo-self-development/`; owner-launched; in progress.
- **Nine workflow-system-disposition owner decisions** —
  `docs/workflow-system-disposition.md` section 6; recorded, none applied.

### Deferred / explicitly out of scope

- A2 (incremental value vs baseline); Goal B / research-grade E3.
- Automatic fog-type→implementation routing as product behavior; a universal
  centralized orchestrator; one workflow encoding the whole loop; automatic
  external-mutation authority (`CONTEXT.md` "Current product boundaries and
  open edges").
- Domain-general control core / domain packs / decision-theory machinery —
  research questions only, non-ratified
  ([docs/research/control-model-research-agenda.md](docs/research/control-model-research-agenda.md)).
- New validator / schema / hook / runtime machinery — behind the "repeated
  real-use pressure + mechanically expressible boundary" gate
  (`CONTEXT.md` principle 10).
- PyPI publication / GA / "production deployment" — **not** a current goal;
  the plans in `roadmap.md` and the `CHANGELOG.md` "Deployment Timeline" footer
  are historical and superseded; ADR 0021 ("production readiness requirements")
  is SUPERSEDED, never Accepted.

### Highest-leverage warranted next boundary

Owner/environment decision on the Goal A execution substrate (Issue #255) — the
product's central unvalidated hypothesis (brief usefulness beyond this repo)
cannot advance without it, and it is not a repo-code deliverable. The
in-authority engineering backlog is deliberately small (the nine
workflow-system-disposition decisions; test-expectation debt D2b / D19; the
`docs/` reconstruction surface itself). The repository posture is **harden only
where pressured** — `CONTEXT.md` principle 10; Campaign 1 closed with "no
further product change is warranted by current evidence"; the research agenda's
2026-08-30 meta-finding records that sensemaking loops have saturated.

## Reconstructing current development direction

A fresh maintainer or coding-agent controller with no prior context should be
able to reconstruct the picture above from these sources, in this order:

1. **[CONTEXT.md](CONTEXT.md)** — product definition, top operating rule, core
   principles, authority model, "Current evidence strategy: Goal A", and
   "Current product boundaries and open edges" (what is *not* ratified).
2. **This file** — the ratified / in-flight / deferred summary and the
   highest-leverage next boundary, each pointing at its authoritative source.
3. **[docs/adr/](docs/adr/)** — read the `**Status**` line of every ADR you
   cite. ADRs 0017–0021 (and 0018) are **SUPERSEDED / never Accepted** — a
   title match is not a decision; see `docs/adr/README.md` for the status
   lifecycle.
4. **[docs/agent-native-operating-workflow.md](docs/agent-native-operating-workflow.md)**
   and **[docs/decision-orchestration-boundary.md](docs/decision-orchestration-boundary.md)**
   — the current control model and the decision-vs-orchestration ownership
   boundary.
5. **[docs/campaigns/](docs/campaigns/)** — each campaign's `CAMPAIGN-STATE.md`
   / `FINAL-REPORT.md` is the freshest strategic narrative for its scope
   (non-authoritative campaign records — evidence, not ratification).
6. **GitHub** — open issues (`gh issue list`) for live workstreams (#218, #226,
   #255) and recent merged PRs (`gh pr list --state merged`) for what most
   recently changed.

Do **not** anchor on: `roadmap.md`, `goal.md`, `00-user-intent.md`, or the
`CHANGELOG.md` "Deployment Timeline" footer — all predate the ADR 0013
agent-native pivot and describe a superseded PyPI/GA/autonomous-router plan.
Root `docs/*.md` files prefixed `PHASE-`, `STAGE-`, `WEEK1-`, `UI-ROUTING-`, or
`task-` are historical working notes, not current design; the current design
docs are those listed under "Where to look" below, and the report archive is
`docs/archive/phase-reports/`.

## Where to look

| Topic | Location |
| :--- | :--- |
| Architecture, principles, authority model, glossary, source-of-truth map | [CONTEXT.md](CONTEXT.md) |
| Current end-to-end operating map | [docs/agent-native-operating-workflow.md](docs/agent-native-operating-workflow.md) |
| Decision vs orchestration ownership boundary | [docs/decision-orchestration-boundary.md](docs/decision-orchestration-boundary.md) |
| Per-workflow disposition (23 registered workflows) | [docs/workflow-system-disposition.md](docs/workflow-system-disposition.md) |
| Non-ratified research directions | [docs/research/control-model-research-agenda.md](docs/research/control-model-research-agenda.md) |
| Product-validation strategy (Goal A) | [docs/research/goal-a-external-product-validation-protocol.md](docs/research/goal-a-external-product-validation-protocol.md), Issue #255 |
| Development campaigns (non-authoritative records) | [docs/campaigns/](docs/campaigns/) |
| Design decisions (read the Status line) | [docs/adr/](docs/adr/), [docs/adr/README.md](docs/adr/README.md) |
| Usage and install | [README.md](README.md), [GETTING_STARTED.md](GETTING_STARTED.md), [INSTALLATION.md](INSTALLATION.md) |
| Change history (released versions only) | [CHANGELOG.md](CHANGELOG.md) |
| Historical phase/completion reports | [docs/archive/phase-reports/](docs/archive/phase-reports/) |
