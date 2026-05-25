# Phase 1: Ready for Implementation Checklist

**Purpose**: Gate for moving from planning to implementation  
**Status**: ⏳ PENDING (awaiting consistency review decisions)  
**Target**: All items must be ✅ before Task 1.1 begins

---

## Pre-Implementation Gates

### Gate 1: Consistency Review Complete
- [ ] Consistency review document read: `docs/phase-1-consistency-review.md`
- [ ] All CRITICAL inconsistencies understood
- [ ] All decisions made (see below)

### Gate 2: Decisions Made & Documented

#### Decision 1: validation_status Placement
**Question**: Should validation_status be stored IN the artifact file, or only in validator output?

- [ ] **PATH A (in artifact)**: Skills write validation_status to artifact after validating
  - Pro: Agents can check artifact validity later without re-running validator
  - Con: Tightly couples skills to validators; artifacts become part validator result
  
- [ ] **PATH B (output only)**: validation_status is only in validator output + run_log
  - Pro: Clean architecture (artifacts = pure data; validation = transient check)
  - Con: Agents can't check artifact validity by reading file alone

**Your decision**: PATH _____ (A or B)  
**Date decided**: _____________  
**Rationale**: _______________________________________________________________

---

#### Decision 2: Autonomy Definition
**Question**: Should agents be "fully autonomous" or "autonomous with graceful escalation"?

- [ ] **DEFINITION A (Fully Autonomous)**: Agent never asks user; handles all errors automatically; stops with error if stuck
  - Pro: True autonomy; user doesn't need to intervene
  - Con: Some errors require human judgment; agent may fail or produce wrong answers
  
- [ ] **DEFINITION B (Graceful Escalation)**: Agent tries auto-fix (3 retries), then asks user if stuck
  - Pro: More realistic; handles errors requiring human judgment
  - Con: Not "fully autonomous"; agent asks for input

**Your decision**: DEFINITION _____ (A or B)  
**Date decided**: _____________  
**Rationale**: _______________________________________________________________

---

### Gate 3: Artifacts Updated Based on Decisions

Once you make Decisions 1 & 2, the following artifacts must be updated before implementation:

#### If Decision 1 = PATH A (validation_status in artifact):
- [ ] Validator guide updated: show how to write validation_status to artifact
- [ ] Bootstrap skill examples: kept as-is (show validation_status in artifact)
- [ ] Checklist Task 1.4: add validation_status to artifact-contracts.yaml
- [ ] Helper scripts Task 2.2 & 2.3: return validation_status for agent to write back

#### If Decision 1 = PATH B (validation_status output only):
- [ ] Bootstrap skill examples: REWRITTEN to remove validation_status from artifact
- [ ] Bootstrap skill section "Handling Validation Errors": say "Read validator output" not "Read artifact field"
- [ ] Checklist Task 1.4: DO NOT add validation_status to artifact-contracts.yaml
- [ ] Validator guide: confirmed correct (no changes needed)

#### If Decision 2 = DEFINITION A (Fully Autonomous):
- [ ] Checklist Task 3.1 success criteria: REWRITTEN to "fully autonomous, never asks"
- [ ] Bootstrap skill escalation: REWRITTEN to not ask user (just stop with error)
- [ ] Bootstrap skill: remove "What would you like me to do?" template

#### If Decision 2 = DEFINITION B (Graceful Escalation):
- [ ] Checklist Task 3.1 success criteria: UPDATED to "autonomous OR graceful escalation"
- [ ] Bootstrap skill: confirmed correct (escalation template is appropriate)
- [ ] Add escalation examples to Checklist Task 3.1

#### All Paths:
- [ ] Bootstrap skill section "The Three-Step Diagnosis Pattern": clarify Phase 1 = diagnostic only
- [ ] Bootstrap skill: update routing examples to not mention Phase 2 workflows
- [ ] Checklist Task 1.4: add missing fields to workflow_orchestration_plan (fog_type, workflow_steps, routing_decision_method)
- [ ] Checklist Task 2.4: document retry count (3 attempts) in SKILL.md updates

---

### Gate 4: Implementation Blockers Cleared

- [ ] No unresolved questions in three artifacts
- [ ] All examples are concrete (not hypothetical)
- [ ] All task success criteria are measurable
- [ ] All field names are consistent across documents
- [ ] All error types are defined consistently
- [ ] All retry/escalation rules are explicit

---

## Pre-Task 1.1 Verification

Before you start **Task 1.1: Create Bootstrap Skill Template**, verify:

### Verification 1: Bootstrap Skill is Implementable
- [ ] Read the bootstrap skill template: `skills/using-sensemaking/SKILL.md.template`
- [ ] All sections are complete (no large placeholders)
- [ ] Fog classification teaching is concrete (4 types, examples for each)
- [ ] Decision trees are clear (agents can follow them)
- [ ] Retry logic is explicit (3 times, then escalate)
- [ ] Escalation template is appropriate (for your chosen DEFINITION)

### Verification 2: Checklist is Clear
- [ ] Read the checklist: `docs/phase-1-agent-native-implementation-checklist.md`
- [ ] All tasks have clear dependencies
- [ ] All success criteria are measurable
- [ ] All time estimates are reasonable
- [ ] No circular dependencies

### Verification 3: Validator Guide is Usable
- [ ] Read the guide: `docs/validator-json-refactor-guide.md`
- [ ] JSON error format is clear (11 fields defined)
- [ ] Error types are explained (5 types with examples)
- [ ] Refactoring steps are detailed
- [ ] Template validator is complete

---

## Ready Signature

When all gates are passed and verifications done, sign off:

**I have read and understood all three Phase 1 artifacts and am ready to begin implementation.**

Name: _______________________________  
Date: _______________________________  
Decision 1 (validation_status): PATH _____ (A or B)  
Decision 2 (autonomy): DEFINITION _____ (A or B)  

---

## Common Blockers (and how to resolve them)

| Blocker | How to Resolve |
|---------|----------------|
| "I don't know which path to choose (A vs B)" | Read INCONSISTENCY #2 in consistency review; pro/con listed for each path |
| "I don't know which definition to choose (A vs B)" | Read INCONSISTENCY #4 in consistency review; realistic vs ideal discussed |
| "The artifacts have too many words" | You don't need to memorize them; just know where to find each section |
| "Some sections seem to contradict" | That's expected; consistency review documents all contradictions and how to resolve |
| "I'm not sure if [field/rule/error] is correct" | Check consistency review; if not listed there, ask before starting |
| "What if I change my mind after starting?" | Stop, update decision, notify. Rework is cheaper before implementation than after. |

---

## Sign-Off Summary

**This checklist is COMPLETE when:**

- ✅ You read consistency review
- ✅ You made Decision 1 (validation_status: PATH A or B)
- ✅ You made Decision 2 (autonomy: DEFINITION A or B)
- ✅ Artifacts were updated based on decisions
- ✅ All blockers cleared
- ✅ You verified implementations are feasible
- ✅ You signed off above

**Then and ONLY THEN:**
→ You can start Task 1.1 (Create Bootstrap Skill Template)  
→ Implementation begins  
→ Clock starts on Week 1 (3 weeks, 13 tasks)

---

## If You're Not Ready

If you need more time or have questions:

**Option 1: Ask clarifying questions**
- Email specific questions about Decisions 1 & 2
- I will provide more detail before you decide

**Option 2: Request revised versions**
- I will rewrite sections that seem unclear
- Resubmit when ready

**Option 3: Schedule a review session**
- Walk through each inconsistency together
- Make decisions interactively
- Then proceed with implementation

**No time pressure**: This gate exists to prevent rework. Taking 30 minutes now saves 3 hours during implementation.

---

## Next Actions

### If ready to decide immediately:
1. Read consistency review: `docs/phase-1-consistency-review.md`
2. Fill in Decisions 1 & 2 above
3. Reply with decisions
4. I update artifacts (1 hour)
5. You sign off
6. Start Task 1.1

### If need more time:
1. Read consistency review
2. Read side-by-side comparisons (INCONSISTENCY #2 and #4 have detailed pros/cons)
3. Decide when ready
4. Reply with decisions

**Timeline**: Decisions can be made in any timeframe; no rush. Implementation starts after artifacts are updated.
