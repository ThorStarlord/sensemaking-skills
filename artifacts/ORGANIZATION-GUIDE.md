# Artifacts Organization Guide

## Problem
Artifacts folder becomes cluttered after multiple runs:
- All files at root level
- No clear grouping by project or run
- Hard to find related artifacts
- No ordering/versioning system

## Solution: Single-Sequence Numbered Runs

Organize future pipeline runs into a flat numbered sequence at `artifacts/` root:

```
artifacts/
├── 01-metamorfose-finance/          ← NN-project-name
│   ├── 01-problem-frame.md          ← NN-file-name.md (pipeline sequence)
│   ├── 02-unknowns-map.md
│   ├── 03-sensemaking-brief.md
│   ├── 04-orchestration-plan.md
│   ├── 05-run-analysis.md
│   └── README.md
│
├── 02-metamorfose-classes/
│   ├── 01-problem-frame.md
│   ├── 02-unknowns-map.md
│   ├── 03-sensemaking-brief.md
│   ├── 04-grilled-findings.md
│   └── README.md
│
├── 03-[next-run-name]/              ← each new run gets next integer
│   ├── 01-problem-frame.md
│   ├── 02-unknowns-map.md
│   └── ...
│
├── meta-analyses/                   ← cross-run analyses and frameworks
│   ├── 01-comparative-routing-analysis.md
│   └── 02-next-phase-decision-framework.md
│
├── ORGANIZATION-GUIDE.md
└── README.md                        ← index and navigation
```

### Run Folder Naming

```
NN-project-name

NN      = sequence number (01, 02, 03...) — monotonic across time
project = target system/project name (kebab-case)
```

**No date prefix** — date metadata goes in the run's README.md or content, not the folder name. This avoids unnecessarily long folder names and keeps the numbering clean.

### Artifact Numbering Within a Run

Files within a run folder are numbered to show pipeline sequence:

| # | File | Produced By |
|---|------|-------------|
| 01 | `01-problem-frame.md` | problem-framer |
| 02 | `02-unknowns-map.md` | unknowns-mapper |
| 03 | `03-sensemaking-brief.md` | repo-sensemaker |
| 04 | `04-orchestration-plan.md` | workflow-orchestrator |
| 05 | `05-run-analysis.md` | Post-run analysis |
| 06 | `06-grilled-findings.md` | docs-aligner (optional) |

### Future: After 10+ Runs

If the sequence grows large, you can nest by decade without breaking links:
```
artifacts/
├── 01-09/                         ← first 9 runs grouped
│   ├── 01-metamorfose-finance/
│   └── 02-metamorfose-classes/
├── 10-19/                         ← next decade
│   ├── 10-[project]/
│   └── ...
└── ...
```

Only do this when the flat list becomes unwieldy — not before.

## Historical Artifacts

Files at the `artifacts/` root (outside numbered run folders) are **pre-organization historical artifacts** — run logs, plans, reports, and experiment outputs from earlier development phases. They are:

- **Left in place** — not migrated into the new structure
- **Not load-bearing for future runs** — new runs follow the numbered convention
- **Referenced by mode-coverage.yaml and docs** — moving them would require updating those references without real benefit

## When to Use Each Location

| Location | Contains | Example |
|----------|----------|---------|
| `NN-project-name/` | All artifacts from one pipeline run | `01-metamorfose-finance/` |
| `meta-analyses/` | Cross-run analyses, frameworks | `01-comparative-routing-analysis.md` |
| (root) | Historical pre-organization artifacts | `coverage_dashboard.md`, `run_log_*.md` |

## Adding a New Run

1. Check the highest existing number (e.g., `02`)
2. Next run gets `03-[project-name]/`
3. Create the folder and produce artifacts as `NN-file-name.md`
4. Create a `README.md` inside summarizing the run
5. Update `artifacts/README.md` navigation table

## Skill Output Convention

Skills (via the workflow-orchestrator) produce future run artifacts following:
```
artifacts/NN-project-name/NN-file-name.md
```

The orchestrator's path normalization rule enforces this. See `skills/workflow-orchestrator/SKILL.md`.
