# Artifacts Index

This directory contains sensemaking pipeline outputs, organized by run and analysis type.

## Folder Structure

### `runs/`

Self-contained artifacts from each sensemaking run, organized by date and project:

- **`2026-05-17-01-metamorfose-finance/`** — Finance UI sensemaking (5 artifacts)
  - Problem: Lack of spec-driven architecture
  - Finding: Implicit dashboard-aggregation contract as weakest boundary
  - Recommended: product-discovery-sprint
  
- **`2026-05-17-02-metamorfose-classes/`** — Classes system sensemaking (4 artifacts + grill-with-docs execution)
  - Problem: Under-specified data model and relationships
  - Finding: Documentation drift (storage strategy hidden, not missing)
  - Recommended: docs-architecture workflow

Each run folder contains:
- `01-problem-frame.md` — Raw problem statement
- `02-unknowns-map.md` — Mapped uncertainties with routing signals
- `03-sensemaking-brief.md` — Diagnostic brief with weakest boundary analysis
- `04-orchestration-plan.md` or `04-grilled-findings.md` — Recommended workflow or downstream validation
- `05-run-analysis.md` — Post-run analysis (where applicable)
- `README.md` — Run summary and next steps

### `meta-analyses/`

Cross-run analyses, comparative frameworks, and decision guidance:

- `01-comparative-routing-analysis.md` — Comparison of Finance vs. Classes systems; validates routing heuristic
- `02-next-phase-decision-framework.md` — Strategic guidance for Phase 4: Options A-D with tradeoffs

### `templates/`

Reference templates for artifact creation (future):

- (To be populated as templates are documented)

## Numbering Convention

**Artifacts within a run** (show pipeline sequence):
1. `01-problem-frame.md` — Output from problem-framer skill
2. `02-unknowns-map.md` — Output from unknowns-mapper skill
3. `03-sensemaking-brief.md` — Output from repo-sensemaker skill
4. `04-orchestration-plan.md` — Output from workflow-orchestrator skill
5. `05-run-analysis.md` — Post-run analysis and lessons learned
6. `06-grilled-findings.md` — If grill-with-docs was executed

**Run folder naming**: `YYYY-MM-DD-NN-project-name`
- `YYYY-MM-DD` = date of the run
- `NN` = sequence number (01, 02, 03...)
- `project` = target system/project name

## Quick Navigation

| Run | Date | Problem Type | Unknowns | Status |
|-----|------|--------------|----------|--------|
| Metamorfose Finance | 2026-05-17 | Implementation-driven (complex) | 9 | ✅ Recommended product-discovery-sprint |
| Metamorfose Classes | 2026-05-17 | Design-incomplete (simple) | 8 | ✅ Validated via grill-with-docs |

## Routing Signals

Both runs validated the dynamic chaining heuristic:

**research_needed = (unknowns_count >= 5) OR (clarity_assessment == "low")**

- Finance: unknowns_count=9, clarity="medium" → research_needed=true ✅
- Classes: unknowns_count=8, clarity="high" → research_needed=true ✅

## See Also

- `ORGANIZATION-GUIDE.md` — How this structure was designed and how to add new runs
- Root artifacts (historical) — Previous experimental phases and analysis (pre-Phase 2)

---

**Last updated**: 2026-05-17  
**Phases complete**: Phase 1 (Dynamic Chaining), Phase 2 (Value-Production Runs), Phase 3 (Workflow Validation), Phase 4 (Decision Framework), Phase 5 (Organization)
