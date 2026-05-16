# Roadmap: Sensemaking Skills

## Current Phase: Orchestrator Hardening Completion

**Status**: In progress — implementation plan ready, ~2.5 hours of work remaining.

The validator ecosystem is complete. Zero repeatable failures detected. The remaining work closes the last gap before real value-production runs are safe to execute.

### Remaining Tasks (do in order)

**1. Enforce strict artifact validation in execution modes** — `scripts/orchestration-runner.py`
- In `guided_execution`, `autonomous_execution`, `yolo_execution`: FAIL the step if a claimed output artifact is not produced.
- Add error code `ARTIFACT_NOT_FOUND`.
- Verify with: `python scripts/test-controlled-failures.py --test artifact-production-required`

**2. Remove premature PRD step from docs-architecture workflow** — `skills/workflow-orchestrator/references/workflow-registry.yaml`
- docs-architecture becomes 2 steps: `grill-with-docs` → `handoff`
- PRD generation does not belong here (PRD is consumed downstream, not in this workflow)

**3. Create product-to-issues workflow** — `skills/workflow-orchestrator/references/workflow-registry.yaml`
- New 3-step pipeline: `to-prd` → `to-issues` → `triage`
- `allowed_execution_modes: [guided_execution]`
- First real test of the full PRD → issues → agent brief chain

**4. Update mode-coverage.yaml** — `docs/mode-coverage.yaml`
- Record new runs for the 2-step docs-architecture and 3-step product-to-issues
- Prove PRD validation gap is resolved

---

## Next Phase: First Value-Production Runs

**Status**: Blocked on current phase completing.

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
