# Phase 1 Real-Agent Orchestration Test: Ready to Execute

**Status**: Test infrastructure complete, ready for agent execution  
**Date**: 2026-05-24  
**Location**: `test-results/phase1/`  

---

## What's Ready

✅ **Test Orchestrator** (`tests/phase1-test-orchestrator.py`)
- Creates test environment
- Generates execution guides
- Documents all 5 scenarios
- Creates results template

✅ **Test Fixtures** (5 scenarios, 5 test repositories)
- `scenario1-valid-product-fog/` - Simple valid case (product fog signals clear)
- `scenario2-missing-evidence/` - Agent needs to add analysis (architecture fog)
- `scenario3-semantic-conflict/` - Misaligned fog/workflow (needs correction)
- `scenario4-ambiguous-fog/` - Multiple fog signals (needs human judgment)
- `scenario5-unfixable/` - Unclear problem (requires domain knowledge)

✅ **Execution Guides**
- `test-results/phase1/TEST-PLAN-SUMMARY.md` - Overview of all scenarios
- `test-results/phase1/EXECUTION-GUIDE.md` - Step-by-step instructions
- `test-results/phase1/SCENARIO-X/manifest.json` - Scenario documentation

✅ **Results Template**
- `test-results/phase1/results/test-results.json` - Pre-created structure for recording outcomes

✅ **All Phase 1 Infrastructure in Place**
- Validators (5 scripts with unified JSON schema)
- Bootstrap skill (using-sensemaking/SKILL.md)
- SessionStart hook (will surface reminder)
- Validation logging (record-validation.py)

---

## How to Execute

### Step 1: Start Fresh Agent Session
```bash
# Open Claude Code or Cursor
# Create a new session (no prior context)
# Repo: sensemaking-skills
```

### Step 2: Run Scenario 1 (Happy Path)
```
User: "Diagnose this repository using sensemaking-skills. 
       Read the bootstrap skill if you haven't seen it yet. 
       Follow the three-step diagnosis pattern."
```

Agent will:
1. Read `skills/using-sensemaking/SKILL.md` (SessionStart surfaces it)
2. Understand fog classification + retry logic
3. Invoke repo-sensemaker skill
4. Produce `repository_sensemaking_brief`
5. Call `validate-and-report.py`
6. Parse JSON response
7. Call `record-validation.py`
8. Report: "Diagnosis complete"

### Step 3: Capture Results
After Scenario 1:
1. Copy agent's transcript
2. Save `repository_sensemaking_brief.md` artifact
3. Note `validate-and-report.py` JSON output
4. Extract `validation_run_log.md` entry
5. Record in `test-results/phase1/results/scenario-1-result.md`

### Step 4: Proceed to Remaining Scenarios
Repeat Steps 2-3 for scenarios 2-5 (if needed)

---

## What to Look For

### Scenario 1 Success Indicators
- [ ] Agent reads skill without being asked where it is
- [ ] Agent produces valid `repository_sensemaking_brief`
- [ ] `validate-and-report.py` returns `valid: true`
- [ ] `record-validation.py` creates run-log entry
- [ ] Agent completes Phase 1 without errors

### Scenario 1 Failure Points (If Test Fails)
- Did agent skip reading the skill?
- Did agent not understand fog classification?
- Did agent not know how to invoke validate-and-report.py?
- Did agent fail to parse JSON?
- Did agent crash on error handling?

Each failure point tells you exactly what to fix.

---

## Expected Artifacts

After Scenario 1, you should have:

```
artifacts/
  repository_sensemaking_brief.md
  validation_run_log.md (with 1 entry)

validate-and-report.py output (in transcript):
{
  "valid": true,
  "artifact_id": "repository_sensemaking_brief",
  "artifact_path": "...",
  "validator": "validate-brief.py",
  "errors": [],
  "validation_timestamp": "2026-05-24T..."
}
```

---

## Decision Framework

### If Scenario 1 PASSES
Agent successfully:
- Found and read the skill
- Understood fog classification
- Invoked validation pipeline
- Logged results
- Completed Phase 1

**Next**: Run Scenarios 2-5 to verify error handling

### If Scenario 1 FAILS at a Specific Point
- **Skipped skill** → Fix: Make skill discovery clearer in hook
- **Misunderstood fog types** → Fix: Rewrite fog classification section
- **Didn't call validate-and-report.py** → Fix: Add to skill instructions
- **Crashed on JSON parsing** → Fix: Add error handling examples to skill
- **Didn't log results** → Fix: Add logging instructions to skill

**Next**: Fix the specific gap, rerun Scenario 1

### If All 5 Scenarios PASS
Agent successfully:
- Reads and understands bootstrap skill
- Produces valid artifacts
- Validates with unified pipeline
- Handles validation errors with bounded retry
- Escalates appropriately when stuck
- Logs results durably

**Next**: Phase 1 is agent-proven. Begin Phase 2.

---

## Key Files to Reference During Test

1. **Agent Will Read**: `skills/using-sensemaking/SKILL.md`
2. **Agent Will Call**: `scripts/validate-and-report.py`
3. **Agent Will Call**: `scripts/record-validation.py`
4. **Agent Will Produce**: `artifacts/repository_sensemaking_brief.md`
5. **You Will Check**: `validation_run_log.md`

---

## Test Environment Details

```
test-results/phase1/
├── TEST-PLAN-SUMMARY.md          (5 scenarios overview)
├── EXECUTION-GUIDE.md             (step-by-step instructions)
├── scenario-1/
│   └── manifest.json
├── scenario-2/
│   └── manifest.json
├── scenario-3/
│   └── manifest.json
├── scenario-4/
│   └── manifest.json
├── scenario-5/
│   └── manifest.json
└── results/
    └── test-results.json          (results template)
```

---

## No More Planning

**Do not add:**
- More infrastructure
- New validators
- Architecture docs
- Phase 2 code

**Just execute the test.**

The test will tell you what, if anything, needs to be fixed.

---

## Time Estimate

- Scenario 1: 5-10 minutes
- Scenario 2-5: 5 minutes each (if Scenario 1 passes)
- Total: 25-30 minutes for full test

---

## Readiness Checklist

- [x] Test orchestrator created
- [x] Test fixtures prepared (5 repositories)
- [x] Execution guides written
- [x] Results template created
- [x] Phase 1 infrastructure ready (validators, skill, hook)
- [x] Decision framework defined
- [x] Failure points identified

**Status**: Ready to execute. Open a fresh agent session and run Scenario 1. ✅

---

**Next Action**: Follow the handoff prompt below to run the test.

---

## Handoff Prompt (Copy to Fresh Agent Session)

```
Execute the Phase 1 real-agent orchestration test plan.

Use:
- docs/phase-1-real-agent-orchestration-test-plan.md
- docs/PHASE-1-NEXT-MILESTONE.md
- test-results/phase1/EXECUTION-GUIDE.md

Constraints:
- Do not add new infrastructure.
- Do not start Phase 2.
- Do not create new architecture docs unless the test reveals a concrete gap.

Goal:
Determine whether a fresh agent can complete one full Phase 1 diagnostic cycle using:
- SessionStart bootstrap reminder
- using-sensemaking skill
- repository_sensemaking_brief
- validate-and-report.py
- record-validation.py
- bounded retry
- graceful escalation

Deliver:
1. scenarios executed
2. artifacts produced
3. validator JSON outputs
4. run-log excerpts
5. failures or behavior gaps
6. final recommendation:
   - Phase 1 agent-proven, ready for Phase 2
   - or Phase 1 needs targeted fixes before Phase 2

Decision gate: PASS -> Phase 1 agent-proven, begin Phase 2
             FAIL -> Fix only the exposed gap, then rerun the test
```

---

**Created**: 2026-05-24  
**Status**: Ready for execution  
**Test Type**: Real-agent orchestration (5 scenarios)  

