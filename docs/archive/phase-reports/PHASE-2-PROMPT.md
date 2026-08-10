# Phase 2 Launch Prompt

**For**: Fresh coding agent session

---

## Begin Phase 2 with workflow-planner.

Use:
- PHASE-1-FINAL-REPORT.md
- PHASE-1-HANDOFF.md
- validation_run_log.md
- skills/using-sensemaking/SKILL.md
- skills/workflow-planner/references/artifact-contracts.yaml

Constraints:
- Do not add more Phase 1 infrastructure.
- Preserve PATH B: validation output and run logs stay outside artifacts.
- Preserve bounded retry + graceful escalation.
- Treat Scenarios 4 and 5 as Phase 2 acceptance tests.

Phase 2 first goal:
Produce and validate `workflow_orchestration_plan`.

Deliver:
1. workflow-planner implementation status
2. generated orchestration_plan artifact
3. validate-and-report.py output
4. semantic_conflict test result
5. run-log excerpt
6. recommendation for next implementation workflow

---

**Context**: Phase 1 real-agent tests proved the diagnostic loop works. Phase 2 now hardens orchestration and implementation routing. See PHASE-1-FINAL-REPORT.md for evidence.
