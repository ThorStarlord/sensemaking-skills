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

## Later Phase: Low-Level Decision Automation

**Status**: Not started. Begins after value-production runs expose real routing gaps.

Currently: the user must know which workflow to invoke. The goal is for `repo-sensemaker` to infer project type and select the workflow automatically from a plain-language goal description.

Work in this phase:
- Improve `repo-sensemaker` routing logic to classify project type from raw input (SaaS / game / visual novel / content / etc.)
- Eliminate the need for explicit `type:` field in input
- Test with diverse project descriptions to verify correct workflow selection

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
