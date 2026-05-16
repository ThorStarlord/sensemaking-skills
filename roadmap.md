# Roadmap: Sensemaking Skills

## Completed Phase: Orchestrator Hardening Completion

**Status**: ✅ Complete — all 4 tasks finished 2026-05-16.

The validator ecosystem is complete. Zero repeatable failures detected. All production-readiness gaps closed.

### Completed Tasks

**1. Enforce strict artifact validation in execution modes** ✅
- `ARTIFACT_NOT_FOUND` error code enforced in execution modes (lines 445-454, orchestration-runner.py)
- Added `artifact-production-required` test to controlled failure suite (10 tests now pass)

**2. Remove premature PRD step from docs-architecture workflow** ✅
- docs-architecture streamlined to 2 steps: `grill-with-docs` → `handoff`
- to-prd moved to product-to-issues workflow

**3. Create product-to-issues workflow** ✅
- 3-step pipeline: `to-prd` → `to-issues` → `triage`
- Mode restricted to `guided_execution` (production-ready constraint)
- Full PRD → issues → agent brief chain proven end-to-end

**4. Update mode-coverage.yaml** ✅
- Mode coverage updated with 10 controlled failure tests (up from 9)
- 2-step docs-architecture and 3-step product-to-issues runs recorded
- PRD validation gap resolved

---

## Current Phase: First Value-Production Runs

**Status**: Ready to start — no blockers.

Run real projects through the pipeline — not system-proving tests. Pick one real project and run it end-to-end.

Goals for this phase:
- At least 3-5 runs where the output artifacts are useful to someone outside the system
- Let `analyze-run-failures.py` detect organic failure patterns
- Add hardening only if a repeatable failure boundary emerges

Suggested first run:
```bash
python scripts/orchestration-runner.py product-to-issues --mode guided_execution
```

---

## Completed Phase: Low-Level Decision Automation

**Status**: ✅ Complete — all tasks finished 2026-05-16.

Automatic project classification and workflow routing now eliminates manual workflow selection.

### Completed Tasks

**1. Created project-classifier skill definition** ✅
- Defined skill interface in `skills/project-classifier/SKILL.md`
- Created output template in `skills/project-classifier/references/project-classification-template.md`
- Supports 7 project types: SaaS, Content, Tool, Consumer, Enterprise, Marketplace, Research

**2. Implemented automatic router (`scripts/router.py`)** ✅
- Keyword-based classification with confidence scoring
- Automatic workflow selection from registry
- Mode recommendation based on confidence
- Tested on 5 diverse real-world project scenarios (all 100% confidence)

**3. Created classification validator** ✅
- `scripts/validate-project-classification.py` validates classifier logic
- Tests against test projects with confidence output
- Results saved to JSON for analysis

**4. Documented routing system** ✅
- `docs/ROUTING_GUIDE.md`: User guide with examples
- `docs/PHASE2_SUMMARY.md`: Implementation details and performance metrics
- Troubleshooting and integration guidance included

---

## Current Phase: Scale and Parallelism

**Status**: Ready to start — no blockers.

Enable multiple projects to run through orchestration pipelines simultaneously without coordination overhead.

Goals for this phase:
- Implement parallel skill invocation across multiple projects
- Add interactive vs. autonomous mode toggle to input contract
- Implement auto-completion detection without manual gate approval
- Enable multi-project portfolio routing

Suggested first run:
```bash
python scripts/orchestration-runner.py --mode autonomous_execution --parallel 3
```

---

## Optional Phase: Scale and Parallelism

**Status**: Not started. Low priority until single-project automation is solid.

- Parallel skill invocation across multiple projects
- Interactive vs. autonomous mode toggle in the input contract
- Auto-completion detection without human confirmation gate

---

## Hardening Policy

> Do not add hardening infrastructure until a repeatable failure boundary is detected by `analyze-run-failures.py` across independent runs.

Current state: zero repeatable failures. The system is working as designed.
