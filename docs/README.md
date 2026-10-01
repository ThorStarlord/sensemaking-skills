# docs/ index

`docs/` holds several hundred files from many phases. This page separates
**current** documents from **historical** ones so you can read the right
thing first. It is navigation only and grants no authority.

Rule of thumb: prefer files linked from the root `README.md`, the ADR index,
and the sections marked **Current** below. A document that opens with a
`HISTORICAL` or `SUPERSEDED` banner (many pre-ADR-0013 files do) is preserved
evidence, not current guidance. Where two documents disagree, ADR 0029, ADR
0013, and the canonical contracts win.

## Start here

| Need | Read |
| --- | --- |
| First use as a human | `../GETTING_STARTED.md`, `../INSTALLATION.md`, `FAQ.md`, `TROUBLESHOOTING.md` |
| Which Skill does what | [`skill-catalogue.md`](skill-catalogue.md) |
| Which system owns which question | [`system-capability-atlas-v1.md`](system-capability-atlas-v1.md) |
| Agent operating map | [`agent-native-operating-workflow.md`](agent-native-operating-workflow.md), [`decision-orchestration-boundary.md`](decision-orchestration-boundary.md) |
| Commands | [`cli-reference.md`](cli-reference.md), [`campaign-cli.md`](campaign-cli.md) |
| Product thesis and boundary | [`product-strategy.md`](product-strategy.md), [`adr/0029-current-product-boundary.md`](adr/0029-current-product-boundary.md) |
| Decisions | [`adr/README.md`](adr/README.md) (index with statuses) |
| Maintaining and qualifying | [`operations-runbook.md`](operations-runbook.md), [`maintainer-guide-v1.0.md`](maintainer-guide-v1.0.md) |

## Current

### Control model and strategy
`strategic-outer-loop.md`, `policy-hierarchy-v0.md`, `strategic-state-contract.md`,
`product-thesis-revision.md`, `product-operating-model.md`,
`adaptive-semantic-control-architecture-v0.md`, `strategic-continuity-v1.md`,
`strategic-repository-sensemaking-v1.md`, `strategic-sensemaking-loop-v1.md`,
`strategic-reconciliation-and-decision-packets-v1.md`,
`multi-repository-strategic-sensemaking-v1.md`.

### Campaigns and execution
`sensemaking-campaign.md`, `agent-workflow-golden-path-v1.md`, the
`campaign-*.md` files, `execution-interface-agent-factorization-v1-handoff.md`,
`external-executor-interchange-v1.md`,
[`coding-agent-native-campaign.md`](coding-agent-native-campaign.md),
`harness-adapters.md`, `resume-capsule-v1.md`, `decision-journey-productization-v1.md`.

### Semantic architecture and product management
`semantic-architecture/README.md`, `capability-registry.md`,
`capability-organization-tracer-v0.md`, `product-management/README.md`
(PM domain, ADR 0028).

### Contracts, validation, and release
`canonical-vocabulary.yaml`, `cli-contract-v1.0.yaml`,
`cli-json-contract-v1.0.yaml`, `public-api-v1.0.yaml`, `public-surface-v1.0.md`,
`validation-workflow.md`, `enforcement-contract.md`, `error-boundaries-v1.0.md`,
`release-v1.0-contract.md`, `release-v1.0-checklist.md`, `PUBLISHING.md`,
[`release-authority-audit.md`](release-authority-audit.md), `qualification-evidence.md`.

### Philosophy and research
`philosophy/`, `research/` (hypotheses; **not** ratified architecture unless an
ADR says so - see `research/control-model-research-agenda.md`).

## Historical or compatibility (read for context only)

| Location | What it is |
| --- | --- |
| `archive/` | Phase reports, deployment checklists, and CI snapshots. Fully historical. |
| `archive/orphaned-2026-09-30/` | Unreferenced docs archived by the owner-ratified Stage 1 simplification (zero inbound references; archived, not deleted; one-command restore). See its README. |
| `PHASE-*.md`, `PHASE2_SUMMARY.md`, `PHASE3_SUMMARY.md`, `PHASE5_*`, `STAGE-*.md`, `WEEK1-*`, `IMPLEMENTATION-*.md`, `VERDICT-SUMMARY.md`, `phase-1-*.md`, `task-*.md` | Phase-era plans/reports from the runner-led product. |
| `ISSUES-V1.md`, `CUSTOMER_ONBOARDING.md`, `DEPLOYMENT_GUIDE.md`, `PORTFOLIO_OPERATIONS.md`, `UI-ROUTING-*.md`, `ROUTING_GUIDE.md` | Runner/routing-era operating guides; check each file's banner before relying on it. |
| `superpowers/` | Dated implementation plans and specs. |
| `campaigns/`, `candidate/`, `normal-use/`, `triage/`, `validator-ecosystem/` | Records of specific campaigns, trials, and design efforts. |
| `2026-08-programmatic-runner-retirement-plan.md` | Closed retirement record for the programmatic runner (ADR 0013). |

These are not moved into `archive/` here because tests and cross-references
depend on their current paths.

## Root-level historical records

The repository root carries a few non-documentation records. Treat them as
historical evidence, not current guidance:

| Root path | What it is | Status |
| --- | --- | --- |
| `release-v1.0.yaml` | The machine-readable 1.0 release/support contract. | **Current, load-bearing.** Read by validators, CI, `MANIFEST.in`, and the release tests. |
| `adoption-finalization.md` | Probe Engine relationship-integration adoption record (2026-08-12). | Historical record. |
| `integration-design.md`, `integration-report.md` | Cross-artifact relationship-probe design and experiment report. | Historical records. |
| `integration-run-auteur.yaml`, `integration-run-sensemaking-skills.yaml` | Raw probe-run outputs from that experiment. | Immutable evidence. |

**Decision (2026-09-29, delegated by the owner):** leave the historical
records in place rather than move them. They are cited by immutable probe
reports and campaign records (`artifacts/*.yaml`,
`experiments/evidence/**`, `docs/campaigns/**`), so relocating them would
invalidate evidence citations for no benefit. `release-v1.0.yaml` stays at the
root because it is a load-bearing machine contract. The same reasoning applies
to the `PHASE-*` / `STAGE-*` / `IMPLEMENTATION-*` files above: they stay in
place, marked historical here.

## Adding a document

Put it in the group above that fits, give it a status line, and add it here if
it is meant to be current. If it supersedes something, add a `SUPERSEDED`
banner to the old file rather than deleting it.
