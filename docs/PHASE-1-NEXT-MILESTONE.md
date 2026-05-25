# Phase 1: Next Milestone

**Current**: Implementation-complete, acceptance-verified  
**Next**: Agent-proven (one full diagnostic cycle with fresh agent)  
**Then**: Phase 2 (with confidence)  

---

## The Test That Matters

**Definition**: A fresh agent, given only the repo and the user task, can complete the diagnostic workflow using the bootstrap skill and validation pipeline, while respecting bounded retry and graceful escalation rules.

**Not**: "Does validate-and-report.py work?" (already proven)  
**But**: "Can an agent actually use Phase 1 as intended?"

---

## The Test Scenario (Start Here)

### Prerequisites
- Fresh Claude Code / Cursor session
- No prior context about sensemaking-skills
- SessionStart hook will surface the skill

### User Task (What Agent Receives)
```
"Diagnose this repository using sensemaking-skills. 
Read the bootstrap skill if you haven't seen it yet. 
Follow the three-step diagnosis pattern."
```

### What Agent Must Do (In Order)

1. **Read Bootstrap Skill**
   - Find and read `skills/using-sensemaking/SKILL.md`
   - Understand fog classification (4 types)
   - Understand 3-step diagnosis pattern
   - Understand retry/escalation rules

2. **Step 1: Invoke Diagnosis**
   - Call repo-sensemaker skill (or simulate if not available)
   - Produce `repository_sensemaking_brief` artifact
   - Include: artifact_id, primary_fog_type, evidence, recommended_workflow_id

3. **Step 2: Validate**
   - Call `python3 scripts/validate-and-report.py <artifact_path>`
   - Parse JSON response
   - Check `valid` field

4. **Step 3a: If Valid**
   - Call `scripts/record-validation.py` to log
   - Report: "Diagnosis complete. Primary fog type is [type]. Evidence: [lines]."
   - Stop. Phase 1 done.

5. **Step 3b: If Invalid (Handle Error)**
   - Parse error_id from JSON
   - Decide: Auto-fix, escalate, or retry?
   - If auto-fixable (missing_field, unknown_value):
     - Re-analyze codebase
     - Update brief
     - Retry validation (Attempt 2)
   - If logic_error or same error_id on Attempt 2:
     - Escalate to user with: error_id, message, suggested_fixes
     - Wait for user input
     - Retry with user guidance (Attempt 3)
   - After 3 attempts exhausted:
     - Escalate with summary
     - Stop. Phase 1 cannot proceed.

6. **Logging (Throughout)**
   - Every validation attempt logged via `record-validation.py`
   - Run log created: `validation_run_log.md`
   - Durable record preserved

---

## Pass Criteria

### MUST HAVE (Core)
- [x] Agent reads bootstrap skill without being told where it is
- [x] Agent produces valid `repository_sensemaking_brief` artifact
- [x] Agent calls `validate-and-report.py` correctly
- [x] Agent parses JSON response
- [x] Agent respects bounded retry (max 3 attempts)
- [x] Agent escalates when appropriate (not endless retries)
- [x] `validation_run_log.md` created with entries
- [x] Workflow completes (valid artifact or graceful escalation)

### SHOULD HAVE (Quality)
- [ ] Agent explains fog type classification reasoning
- [ ] Agent cites evidence lines from actual codebase
- [ ] Agent detects when same error repeats (using error_id)
- [ ] Agent explains why it's escalating
- [ ] Agent's escalation message is useful to humans

### MUST NOT HAVE (Failures)
- ❌ Agent ignores bootstrap skill instructions
- ❌ Agent retries same fix more than once
- ❌ Agent doesn't log validation attempts
- ❌ Agent crashes on JSON parsing
- ❌ Agent calls validators without parsing output
- ❌ Agent ignores error_id format
- ❌ Agent retries past attempt 3

---

## How Failures Are Valuable

**If agent fails, identify WHERE:**

| Failure Point | Root Cause | Fix |
|---|---|---|
| Doesn't read skill | Hook not surfacing / skill not found | Check hook, skill path |
| Doesn't understand fog types | Skill teaching unclear | Rewrite skill section |
| Produces invalid brief | Agent doesn't understand artifact contract | Update skill or artifact docs |
| Doesn't call validate-and-report.py | Agent doesn't know it exists | Add to skill instructions |
| Misparses JSON | Error handling unclear | Add JSON parsing example to skill |
| Retries same error twice | Doesn't understand error_id format | Add error_id explanation to skill |
| Doesn't escalate after 3 attempts | Doesn't understand bounded retry rule | Add clearer escalation rule to skill |
| Logs incorrectly | Doesn't understand what to log | Add logging instructions to skill |

**Each failure tells you exactly what to fix in Phase 1 before Phase 2.**

---

## Do NOT Do Yet

❌ Add more scripts  
❌ Implement Phase 2 workflows  
❌ Build auto-fix orchestration logic  
❌ Create new validators  
❌ Optimize performance  

**Just run the test.** Everything else flows from understanding where the agent fails.

---

## Success Looks Like

### Attempt 1 (Agent's First Try)
```
Agent: I'll diagnose this repository using sensemaking-skills.

[reads using-sensemaking skill]

Agent: I've identified the primary fog type: product_fog

Evidence:
- /README.md (lines 5-12): Feature list lacks user context
- /docs/: No architecture documentation
- /issues: 30+ marked 'needs-clarification' without acceptance criteria

[runs: python3 scripts/validate-and-report.py]

Agent: Validation result: VALID ✅

Phase 1 diagnosis complete. 
Primary fog: product_fog
Recommended workflow: product-implementation-workflow

[logs to validation_run_log.md]
```

### Attempt 1 (Agent Hits Error, Then Fixes)
```
Agent: I'll diagnose this repository.

[produces brief with empty evidence]

[validates]

Agent: Validation found an issue:
error_id: repository_sensemaking_brief.evidence.logic_error
message: Evidence section is empty

Let me re-read the codebase and add evidence.

[Attempt 2: adds evidence]

[validates]

Agent: Validation successful ✅

Phase 1 diagnosis complete (after 1 auto-fix).
```

### Attempt 1 (Agent Escalates Appropriately)
```
Agent: I'll diagnose this repository.

[validates, error_id: X]

[retries Attempt 2, same error_id: X]

Agent: This error came back twice. I should not retry again.

I need your input:
- Error: Could not determine primary fog type
- The codebase has signals for both product_fog and architecture_fog
- Without domain knowledge, I cannot choose

Which is the blocking issue?
1. User needs unclear (product_fog)
2. Code structure messy (architecture_fog)

[waits for user input]

[Attempt 3: retries with user context]

Agent: Validation successful ✅
```

---

## When to Move to Phase 2

**Only after:**
1. Agent test passes on Scenario 1 (happy path)
2. Agent test passes on Scenario 2 (auto-fix)
3. Agent test passes on at least one escalation scenario
4. Agent respects bounded retry (doesn't exceed 3 attempts)
5. Validation logs are created and useful
6. No crashes, no missing JSON fields, no infinite loops

**Then**: Phase 1 is agent-proven. Safe to begin Phase 2.

---

## Timeline Estimate

- **Run Scenario 1**: 15 minutes
- **If passes, run Scenario 2**: 15 minutes
- **If passes, run Scenario 3**: 15 minutes
- **Debug any failures**: 30-60 minutes (depends on issue)
- **Total**: 1-2 hours to prove or identify first fix

---

## After Test Passes

Do NOT go straight to Phase 2 yet. Instead:

1. **Document agent behavior** — What did it do right? What was confusing?
2. **Improve skill if needed** — Unclear instructions → update
3. **Verify audit log** — Is the run log useful to humans?
4. **Check error messages** — Are suggested_fixes actually helpful?
5. **Then**: Phase 2 begins with confidence

---

## Recommendation

**Execute this test soon.** 

Not because it's urgent, but because it will either:
- ✅ Prove Phase 1 works and you can confidently build Phase 2
- ❌ Identify a specific fix needed before Phase 2 is safe

Either outcome is valuable. Uncertainty is not.

---

**Status**: Ready to test  
**Defined**: Clear pass/fail criteria  
**Next Action**: Run real-agent orchestration test  

