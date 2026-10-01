# Repository Sensemaking Brief

## 1. Repository goal

This repository is a meta-routing framework for AI-agent repository diagnosis and workflow orchestration.

## 2. Current shape

Two parallel routing mechanisms exist for turning a `repository_sensemaking_brief` into a `workflow_orchestration_plan`: (a) `scripts/workflow-runtime.py`'s own `generate_plan()`/`_extract_recommended_workflow()` logic, invoked as part of the live automated pipeline, and (b) a standalone script, `scripts/workflow-planner.py` (282 lines), which reads a brief file directly via CLI and prints/writes a plan.

## 3. Strong signals

`scripts/workflow-runtime.py`'s routing path is actively exercised by the current test suite (`tests/test_generate_plan_conformance.py`, `tests/integration/test_autonomous_execution_integration.py`, and others) and is what real, current runs go through.

## 4. Missing pieces

`scripts/workflow-planner.py` has no current test coverage (`grep -rl "workflow-planner\.py\|workflow_planner\b" tests/` returns zero files) and is not referenced by any current skill, registry, ADR, or `CONTEXT.md`. Its most recent commit is `2849043` (2026-05-25), over two months before this brief's `created_at`. Extensive documentation describing it as "production-verified" and part of an active "Phase 2" pipeline step exists — but every file making that claim (`PHASE-4-1-COMPLETE.md`, `PHASE-4-2-PERFORMANCE-MEASUREMENT.md`, `DEPLOYMENT-GUIDE-2026-05-25.md`, and a dozen others) is itself dated 2026-05-25 and untouched since. That documentation describes a state, not the current one.

## 5. Improvement opportunities

Either restore `scripts/workflow-planner.py` to the live routing path (if the two-mechanism split is intentional and current) or remove it and its associated PHASE-4-era documentation as historical, no longer describing this repository's actual operation.

## 6. Weakest boundary

**Weakness type:** Ghost Features

`scripts/workflow-planner.py` presents as a live, working, tested pipeline component (per extensive historical documentation still present in the repo root) but has zero current callers, zero current test coverage, and zero references from any currently-authoritative source (skills, registries, ADRs, `CONTEXT.md`).

## 6.5. Problem classification (fog type)

Fog type is recorded in the machine-readable handoff block (Section 13), not here.

## 7. Evidence

<!-- mode: investigative -->
`git log -1 --format="%H %ai %s" -- scripts/workflow-planner.py` returns `2849043e00... 2026-05-25 15:55:52 -0300 docs: record pre-deployment code verification complete` -- the file has not been touched since. `grep -rln "workflow-planner\.py|workflow_planner\b" tests/` returns no files. `grep -rln "workflow-planner\.py" skills/ docs/adr/ docs/canonical-vocabulary.yaml CONTEXT.md` also returns no files. By contrast, `grep -rn "workflow-planner\.py"` across the whole repository returns 60+ matches, all confined to root-level files dated 2026-05-25 (`PHASE-4-*.md`, `DEPLOYMENT-*.md`, `SESSION-COMPLETE-*.md`, etc.) describing it as tested and deployed.

Logic trace: a script with extensive historical "production-verified" documentation but zero current test coverage, zero current callers, and zero references from any currently-authoritative source is either quietly superseded (by `workflow-runtime.py`'s own routing logic, which the current test suite does exercise) or quietly broken and undetected -- either way, the historical documentation's claims about it no longer describe verified current state, which is exactly the gap PR #165's state-currency discipline is meant to catch.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: scripts/workflow-planner.py
    lines: L1-L10
    quote: "see file/lines"
    supports_claim: "the standalone script exists, 282 lines, reads a brief and produces a plan"
  - file: PHASE-4-1-COMPLETE.md
    lines: L17
    quote: "see file/lines"
    supports_claim: "historical documentation (2026-05-25) describes it as a verified pipeline step"
```

## 9. Why this boundary matters

An agent or human following the still-present historical runbooks (`PHASE-4-4-OPERATOR-RUNBOOKS.md`, `NEXT-AGENT-HANDOFF.md`) would invoke a script that no current test protects and no current registry acknowledges -- if it silently drifted out of sync with the brief schema those docs assume, nothing would catch it before a human ran it manually.

## 10. Candidate next steps

1. Confirm with a live invocation whether `scripts/workflow-planner.py` still runs at all against a current brief.
2. If it still works and the split is intentional, add current test coverage and a current reference (skill/registry/ADR).
3. If it's superseded, remove it and archive/mark the PHASE-4-era docs as historical.

## 11. Recommended next step

Confirm current runnability first (cheapest probe), then decide removal vs. re-integration based on that result -- this is a repository-evidence question about current state, not an owner-preference question.

## 12. Recommended workflow

See `recommended_workflow_id` in Section 13.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "scripts/workflow-planner.py: no current test coverage, no current callers"
  - "git log (scripts/workflow-planner.py): last touched 2026-05-25, 2849043"
  - "PHASE-4-1-COMPLETE.md and 60+ similar matches: all dated 2026-05-25, describe it as production-verified"
recommended_workflow_id: implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: scripts/workflow-planner.py -- stale documentation vs. current dead-code status
weakness_type: Ghost Features
weakness_type_explanation: null
created_at: "2026-08-10T00:00:00Z"
immutable: true
```
