# Artifacts Organization Guide

## Problem
Artifacts folder becomes cluttered after multiple runs:
- All files at root level
- No clear grouping by project or run
- Hard to find related artifacts
- No ordering/versioning system

## Proposed Solution

Organize by **run/project** with **numbered artifacts** to show pipeline sequence:

```
artifacts/
├── runs/
│   ├── 2026-05-17-01-metamorfose-finance/
│   │   ├── 01-problem-frame.md
│   │   ├── 02-unknowns-map.md
│   │   ├── 03-sensemaking-brief.md
│   │   ├── 04-orchestration-plan.md
│   │   └── 05-run-analysis.md
│   │
│   ├── 2026-05-17-02-metamorfose-classes/
│   │   ├── 01-problem-frame.md
│   │   ├── 02-unknowns-map.md
│   │   ├── 03-sensemaking-brief.md
│   │   ├── 04-grilled-findings.md
│   │   └── README.md (summarizes this run)
│   │
│   └── 2026-05-17-03-metamorfose-[next-system]/
│       ├── 01-problem-frame.md
│       └── ...
│
├── meta-analyses/
│   ├── 01-comparative-routing-analysis.md
│   └── 02-next-phase-decision-framework.md
│
├── templates/
│   ├── problem-frame-template.md
│   ├── unknowns-map-template.md
│   └── ... (reference templates)
│
└── README.md (top-level index)
```

## Numbering Convention

**Artifacts within a run** (show pipeline sequence):
1. `01-problem-frame.md` — Output from problem-framer skill
2. `02-unknowns-map.md` — Output from unknowns-mapper skill
3. `03-sensemaking-brief.md` — Output from repo-sensemaker skill
4. `04-orchestration-plan.md` — Output from workflow-orchestrator skill
5. `05-run-analysis.md` — Post-run analysis and lessons learned
6. `06-grilled-findings.md` — If grill-with-docs was executed

**Run folder naming**:
```
YYYY-MM-DD-NN-project-name

YYYY-MM-DD = date of the run
NN         = sequence number (01, 02, 03...)
project    = target system/project name
```

Example:
- `2026-05-17-01-metamorfose-finance` — First run on May 17, finance system
- `2026-05-17-02-metamorfose-classes` — Second run on May 17, classes system
- `2026-05-20-01-[next-project]` — First run on May 20 on a different project

## Benefits

✅ **Organized**: Each run is self-contained in its own folder  
✅ **Discoverable**: Date + sequence + project name is self-documenting  
✅ **Numbered**: Shows artifact sequence (1-6) and run sequence (01, 02...)  
✅ **Scalable**: Easy to add new runs without cluttering root  
✅ **Auditable**: Clear which artifacts belong together  

## Folder Structure Rules

- **Run folders go in `/runs/`** — Never at artifacts root
- **One folder per run** — All artifacts for that run stay together
- **Sequential numbering per run** — Starts at 01 for each new run
- **README per run** (optional) — Summarizes the run and next steps
- **Meta-analyses go in `/meta-analyses/`** — Comparative analyses, decision frameworks, lessons learned
- **Templates go in `/templates/`** — Reference materials and artifact templates

## Example README Inside Run Folder

```markdown
# Metamorfose Finance UI - Run Analysis
**Date**: 2026-05-17  
**Project**: Metamorfose Edutech Finance Subsystem  
**Artifacts**: 05 files  

## Summary
Sensemaking pipeline analysis of finance UI complexity. Identified implicit dashboard-aggregation contract as weakest boundary. Recommended product-discovery-sprint to extract domain spec.

## Files
1. **problem-frame.md** — Problem statement: lack of spec-driven architecture
2. **unknowns-map.md** — 9 unknowns mapped; research_needed = true
3. **sensemaking-brief.md** — Diagnostic brief identifying weakest boundary
4. **orchestration-plan.md** — 3-phase workflow recommendation
5. **run-analysis.md** — Validation of dynamic chaining heuristic

## Key Findings
- unknowns_count: 9 (triggers research)
- clarity_assessment: medium
- Weakest boundary: dashboard ↔ aggregation layer implicit contract
- Recommended workflow: product-discovery-sprint

## Next Steps
- Execute product-discovery-sprint with finance operators
- Test if domain spec matches operator mental models
- Measure effectiveness of spec-driven refactoring

## Related Runs
- 2026-05-17-02-metamorfose-classes (comparable analysis on simpler system)
```

## Migration Path

If you want to reorganize existing artifacts:

```bash
# 1. Create run folders
mkdir -p artifacts/runs/2026-05-17-01-metamorfose-finance
mkdir -p artifacts/runs/2026-05-17-02-metamorfose-classes
mkdir -p artifacts/meta-analyses

# 2. Move finance artifacts
mv artifacts/metamorfose-finance-*.md artifacts/runs/2026-05-17-01-metamorfose-finance/
cd artifacts/runs/2026-05-17-01-metamorfose-finance
mv metamorfose-finance-problem-frame.md 01-problem-frame.md
mv metamorfose-finance-unknowns-map.md 02-unknowns-map.md
mv metamorfose-finance-sensemaking-brief.md 03-sensemaking-brief.md
mv metamorfose-finance-orchestration-plan.md 04-orchestration-plan.md
mv metamorfose-finance-run-analysis.md 05-run-analysis.md

# 3. Move classes artifacts
cd ../../
mv artifacts/metamorfose-classes-*.md artifacts/runs/2026-05-17-02-metamorfose-classes/
cd artifacts/runs/2026-05-17-02-metamorfose-classes
mv metamorfose-classes-problem-frame.md 01-problem-frame.md
mv metamorfose-classes-unknowns-map.md 02-unknowns-map.md
mv metamorfose-classes-sensemaking-brief.md 03-sensemaking-brief.md
mv metamorfose-grilled-classes-findings.md 04-grilled-findings.md

# 4. Move meta-analyses
cd ../../
mv artifacts/metamorfose-comparative-routing-analysis.md artifacts/meta-analyses/01-comparative-routing-analysis.md
mv artifacts/NEXT-PHASE-DECISION-FRAMEWORK.md artifacts/meta-analyses/02-next-phase-decision-framework.md
```

## When to Use Each Folder

| Folder | Contains | Example |
|--------|----------|---------|
| `runs/` | All artifacts from a specific sensemaking run | `2026-05-17-01-metamorfose-finance/` |
| `meta-analyses/` | Cross-run analyses, frameworks, lessons learned | comparative-routing-analysis.md |
| `templates/` | Reference templates for artifacts | problem-frame-template.md |
| (root) | Only high-level README and organization guides | README.md, ORGANIZATION-GUIDE.md |

## Future Growth

After 10+ runs, you might further organize:

```
artifacts/
├── runs/
│   ├── 2026-05-17/
│   │   ├── 01-metamorfose-finance/
│   │   ├── 02-metamorfose-classes/
│   │   └── 03-metamorfose-[system]/
│   ├── 2026-05-20/
│   │   ├── 01-[project]/
│   │   └── 02-[project]/
│   └── 2026-06-01/
│       └── ...
├── meta-analyses/
├── templates/
└── README.md
```

But for now, the flat `runs/` folder with date-prefixed subfolders is sufficient.
