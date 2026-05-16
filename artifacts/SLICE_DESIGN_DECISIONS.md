# Vertical Slice Design Decisions

## Question 1: Granularity - Are slices at the right size?

**Answer**: YES, with refinement to slice #3.

The slices are appropriately sized for independent demoability and verification. However, slice #3 (Complete `guided_execution`) should be split into two AFK slices:

- **3a. Complete guided_execution Step 2** - The repo-sensemaking-brief and docs-contract-reconciliation-report are produced
- **3b. Complete guided_execution Step 3 + Final Handoff** - The prompt_handoff is produced and gates are fully exercised

**Rationale**: Step 2 and Step 3 may have independent validator failures. Splitting allows parallel work and clearer attribution of issues.

---

## Question 2: Dependencies - Are blocking relationships correct?

**Answer**: PARTIALLY - needs adjustment.

Current blocking relationships are too strict. Revised:

- Slices #1-#5 (mode proving) can run in **parallel** after infrastructure is ready
  - They don't depend on each other's completion
  - They prove independent modes on the same or different workflows
  - Parallel execution demonstrates portfolio capability

- Slices #6 and #7 (analysis/dashboard) **must** wait for #1-#5

**Updated flow**:
```
START
  ├─→ [1] plan_only
  ├─→ [2] prompt_chain  
  ├─→ [3a] guided_execution Step 2
  ├─→ [3b] guided_execution Step 3
  ├─→ [4] autonomous_execution
  ├─→ [5] yolo_execution
  └─→ [All complete]
       ├─→ [6] Failure boundary analysis
       └─→ [7] Coverage dashboard
```

But for this implementation, I'll run them **sequentially** to establish baselines before enabling parallelism.

---

## Question 3: HITL vs AFK - Should Step 3 be split further?

**Answer**: YES, but gates are INFRASTRUCTURE not prep.

Slice #3 is correctly marked HITL because it requires **human gate decisions** (approval/denial at Step 2 and Step 3). This is not a separate "preparation" task - it IS the validation of gate infrastructure.

However, orchestration-runner.py needs a small fix:
- Add `--gate-decision auto-approve` support (already exists as flag)
- But it fails on EOFError when no TTY available

**Fix needed**: Modify runner to handle missing TTY gracefully and use auto-approve flag without hanging.

This is a prerequisite for slices #2, #4, #5 which require non-interactive gate handling.

---

## Question 4: Sequence - Does "plan_only proves validator framework" make sense?

**Answer**: YES - `validate-plan.py` is first new validator invoked.

Sequencing is correct:
1. `plan_only` exercises `validate-plan.py` (never done in live before)
2. `prompt_chain` exercises `validate-prompt-handoff.py` (never done in live before)  
3. `guided_execution` exercises full gate infrastructure
4. `autonomous_execution` proves gates without human
5. `yolo_execution` on new workflow proves full pipeline

Each mode brings NEW infrastructure online:
- plan_only: planning validator
- prompt_chain: prompt validator
- guided_execution: gate approvals
- autonomous_execution: automated gates
- yolo_execution: full YOLO pipeline on diverse workflow

---

## Question 5: Missing slices - Should there be additional slices?

**Answer**: YES, add slice 0 (infrastructure prep) before mode proving.

**New Slice 0: Prepare Orchestration Infrastructure**
- **Type**: AFK (code fix + validation)
- **Blocked by**: None - first slice
- **Summary**: 
  - Fix orchestration-runner.py to support `--gate-decision auto-approve` in non-TTY environments
  - Ensure all validators are available and working
  - Create test project definitions if needed
  - Document artifact contract locations

**Why**: Without fixing the runner first, slices #1-#5 will fail on gate timeouts when run non-interactively.

Other questions (CI/CD integration, test projects) are OUT_OF_SCOPE per PRD - they're future work.

---

## Final Slice List (Refined)

| # | Slice | Type | Blockers | Focus |
|---|-------|------|----------|-------|
| 0 | Prepare Orchestration Infrastructure | AFK | None | Fix runner, validate setup |
| 1 | Prove `plan_only` mode | AFK | 0 | Exercise validate-plan.py |
| 2 | Prove `prompt_chain` mode | AFK | 0 | Exercise validate-prompt-handoff.py |
| 3a | Complete `guided_execution` Step 2 | HITL | 0 | Exercise gate approval |
| 3b | Complete `guided_execution` Step 3 | HITL | 3a | Exercise final gate |
| 4 | Prove `autonomous_execution` mode | AFK | 0 | Automated gates |
| 5 | Prove `yolo_execution` on new workflow | AFK | 0 | Full pipeline YOLO |
| 6 | Repeatable failure boundary analysis | AFK | 1-5 | Failure pattern tracking |
| 7 | Coverage metrics dashboard | AFK | 6 | Production readiness metrics |

