# CLI Reference

**Status:** human-readable overview of the `sensemaking-skills` command line.
**Authority:** subordinate to the machine contracts
`docs/cli-contract-v1.0.yaml` and `docs/cli-json-contract-v1.0.yaml`. When this
page and a contract disagree, the contract and the code win. Regenerate exact
option lists with `sensemaking-skills <command> --help`.

Design rule shared by every command family: **the CLI performs mechanical
operations and never makes semantic decisions**. It does not select a
responsibility, rank options, choose a next action, or grant authority. The
active coding agent owns the control loop (ADR 0013).

```text
sensemaking-skills [--version] <command> ...
```

## Command families

| Command | Purpose | Detailed doc |
| --- | --- | --- |
| `setup-skills` | Copy packaged Skill trees to an explicitly chosen harness discovery root. No harness auto-detection. | `docs/harness-adapters.md`, `INSTALLATION.md` |
| `validate` | Validate a repository sensemaking brief or workflow plan (`--artifact`, `--json`). | `docs/validation-workflow.md` |
| `analyze` | Prepare the environment for agent-driven diagnosis (`--repo`, `--output`). Diagnosis itself is the `repo-sensemaker` Skill. | `skills/repo-sensemaker/SKILL.md` |
| `test` | Shadow-mode validation automation over sample repositories (`--repos`). | `docs/archive/phase-reports/` (historical) |
| `campaign` | Durable Campaign state, handoff/resume, execution companions, lineage, bundles, multi-target, provenance. | `docs/campaign-cli.md` |
| `strategy` | Inspect authored Level-3 strategic analyses. | `docs/strategic-continuity-v1.md` |
| `journey` | Read-only decision-journey projections. | `docs/decision-journey-productization-v1.md` |
| `organization` | Read-only role/capability topology. | `docs/capability-organization-tracer-v0.md` |
| `semantic` | Mechanical semantic substrate (catalog, conformance, probes, map build, companion state). | `docs/semantic-architecture/README.md` |
| `release` | Local release-authority audit. | `docs/release-authority-audit.md` |

## `campaign`

Grouped by intent (all read/write only durable Campaign state; none infers a
decision):

- **Lifecycle:** `init`, `advance`, `defer`, `close`, `closeout`, `archive`,
  `completion-receipt`.
- **Inspect:** `status`, `inspect`, `history`, `diff`, `inventory`, `explain`,
  `working-context`.
- **Integrity:** `validate`, `doctor`, `preflight`, `graph`, `graph-integrity`,
  `replay`.
- **Evidence:** `ingest`, `lineage`, `reconciliation`.
- **Continuity:** `handoff`, `resume`, `resume-context`, `resume-profile`.
- **Capabilities:** `capabilities`, `capability-context` (unranked candidates
  after the agent classifies a responsibility).
- **Execution companion:** `execution handoff|inspect|result|result-template|
  result-seal|result-import|export|factory-issue`.
- **Strategy bridge:** `strategy inspect|diff|handoff`.
- **Targets:** `target rebind|verify-rebind`;
  `multi-target add|relate|inspect|verify|refresh|rebind|graph|dependency-check|
  execution-view`.
- **Uncertainty history:** `uncertainty-record|relate|show|history|graph`.
- **Semantic companion:** `semantic-state`, `semantic-state-append`.
- **Bundles:** `bundle-export|verify|inspect|import|graph|resume-context`.
- **Provenance:** `provenance`, `provenance-publish` (preview by default;
  publishing is explicit).
- **Static guidance:** `workflow list|show` - golden paths only; never routes
  or executes.

## `strategy`

`inspect`, `paths`, `uncertainty`, `assumptions`, `compare`, `drift`, `history`,
`graph`. Projections of declared state; no strategic judgment.

## `journey`

`inspect`, `context`, `delta`, `impact-closure`, `guide`. `guide` shows static
guidance for one caller-selected intent and never routes.

## `organization`

`inspect`, `role`, `skill-profile`. Explicit topology only; no worker
allocation.

## `semantic`

`catalog`, `conformance`, `probe`, `map-build`, `state-append`, `state-show`.
Never decides semantic truth or Skill quality.

## `release`

`audit [--repo-root] [--json]`. Exit code 3 on error findings. See
`docs/release-authority-audit.md`.

## Exit codes and JSON

Exit-code and JSON-envelope semantics are normative in
`docs/cli-contract-v1.0.yaml` and `docs/cli-json-contract-v1.0.yaml`; campaign
commands additionally follow `docs/campaign-cli.md`. Console output is
ASCII-only by repository rule (Windows cp1252 safety).

## Scripts that are not CLI commands

Operator scripts (validators, ledger tools, execution infrastructure) are
indexed in `scripts/README.md`.
