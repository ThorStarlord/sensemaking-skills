# Stage 3 Complete: to-prd Scope Expansion Tracking ✅

**Date**: 2026-05-19  
**Status**: ✅ COMPLETE  
**Validation**: 3/3 fixtures pass (strict mode)  
**Fields Promoted**: 3/3 (user_goal_preserved_as, scope_expansion_proposed, scope_expansion_requires_approval)

---

## What Was Done

### 1. Created to-prd Skill
**File**: `skills/to-prd/SKILL.md`

New skill with instructions for:
- How to extract user goal from source_intent_ref
- How to determine scope expansion vs exact match vs divergence
- How to propose expansion features with rationale and effort estimates
- How to document approved expansions with timestamps
- How to escalate divergence cases
- Three scenarios with YAML examples showing different scope expansion states

### 2. Created PD Template
**File**: `skills/to-prd/references/prd-template.md`

Template includes:
- Executive Summary
- User Goal (as stated)
- Goal Preservation & Expansion section
- Features (organized by core + expansions)
- Out of Scope (explicit deferrals)
- Acceptance Criteria
- Non-Functional Requirements
- Approval Gate (if expansion proposed)
- Machine-Readable Handoff with all scope expansion fields

### 3. Created Three Test Fixtures
**File**: `examples/to-prd-fixtures/`

**01-goal-preserved.md** — Scope matches user's stated goal exactly
- Scenario: Discovery confirms user needs (task creation, priority, completion)
- No scope expansion proposed
- user_goal_preserved_as: exact_match
- scope_expansion_proposed: false

**02-scope-expansion-proposed.md** — Scope expansion discovered; awaiting user approval
- Scenario: Discovery revealed due dates and recurring tasks (not mentioned by user)
- Core features preserved; expansions proposed
- Includes approval gate: "Do you approve due dates? Do you approve recurring tasks?"
- user_goal_preserved_as: core_with_expansion
- scope_expansion_proposed: true
- scope_expansion_requires_approval: true
- scope_expansion_status: pending_user_approval

**03-scope-expansion-approved.md** — Scope expansion previously approved; now in development scope
- Scenario: User approved both expansions in workflow orchestrator
- All features (core + due dates + recurring) documented as development scope
- Includes approval timestamps
- user_goal_preserved_as: core_with_expansion
- scope_expansion_proposed: true
- scope_expansion_requires_approval: false (already approved, no longer needs approval)
- scope_expansion_status: approved_by_user

### 4. Promoted Fields in Contracts
**File**: `skills/workflow-orchestrator/references/artifact-contracts.yaml`

Moved 3 fields from `recommended_machine_fields` → `required_machine_fields` for prd:
- ✅ user_goal_preserved_as
- ✅ scope_expansion_proposed
- ✅ scope_expansion_requires_approval

Kept 3 fields as recommended (deferred to future stages):
- scope_expansion_status (optional—orchestrator decides)
- scope_expansion_details (optional—for clarity on proposed expansions)
- scope_expansion_approvals (optional—for tracking approved expansions)

### 5. Validation Results

**Validator Output**:
```
[PASS] Required fields present
[OK] All fields (required + recommended) present
```

All 3 fixtures pass in strict mode (--strict-recommended).

### 6. Updated Hardening Tracker
**File**: `docs/INTENT-HARDENING-TRACKER.md`

Marked Stage 3 as complete with details on what was promoted and accomplished.

---

## Stage 3 Scope Boundaries

### What to-prd Owns (Stage 3)
✅ Extract user goal from source_intent_ref  
✅ Determine if PRD addresses goal exactly or proposes expansion  
✅ Document core features (goal-preserving)  
✅ Propose expansion features with discovery rationale  
✅ Estimate effort and risk for each expansion  
✅ Set up approval gate for user to decide on expansions  
✅ Document approved expansions with timestamps  
✅ Emit the 3 Stage 3 scope expansion fields  
✅ Escalate divergence (when PRD would diverge from goal)  

### What to-prd Does NOT Own
❌ Final scope decision (user makes this in guided_execution gate)  
❌ Story breakdown (to-issues owns this)  
❌ Prioritization (triage owns this)  
❌ Acceptance criteria detail (to-issues refines from PRD)  

**Split Preserved**: Document goal preservation. Propose expansion. User decides. to-issues implements what's approved.

---

## Three Scope Expansion States

### State 1: Exact Match (No Expansion)
- Scenario: Discovery confirms user's stated goal; no new features identified
- PRD addresses exactly what user asked for
- No approval needed
- user_goal_preserved_as: exact_match
- scope_expansion_proposed: false
- scope_expansion_status: exact_match

### State 2: Core + Expansion Proposed (Awaiting Approval)
- Scenario: Discovery reveals additional features beyond stated goal
- Core features preserve goal; expansions proposed with rationale
- User must approve before development starts
- user_goal_preserved_as: core_with_expansion
- scope_expansion_proposed: true
- scope_expansion_requires_approval: true
- scope_expansion_status: pending_user_approval

### State 3: Core + Expansion Approved (Ready for Development)
- Scenario: Expansions were already approved by user (in workflow-orchestrator gate)
- All features (core + approved expansions) documented for development
- PRD is development scope (no further approval needed)
- user_goal_preserved_as: core_with_expansion
- scope_expansion_proposed: true
- scope_expansion_requires_approval: false (already approved, gate passed)
- scope_expansion_status: approved_by_user

---

## Production Readiness

| Component | Status | Notes |
|-----------|--------|-------|
| Instructions | ✅ Updated | Scope expansion workflow documented with 3 scenarios |
| Template | ✅ Updated | Machine-readable fields documented with approval gate pattern |
| Fixtures | ✅ Passing | 3/3 pass strict validation (01-goal-preserved, 02-scope-expansion-proposed, 03-scope-expansion-approved) |
| Validator | ✅ Ready | Unambiguous [PASS]/[WARN]/[FAIL] output |
| Contracts | ✅ Updated | 3 scope expansion fields promoted to required |

---

## How to-prd Should Work (Post-Stage-3)

When producing a PRD:

```
1. Read source_intent_ref
   └─ Extract: user's original goal (exact quote)

2. Compare Intent vs Discovery
   ├─ Core features: Do they match stated goal?
   ├─ Additional features: Did discovery reveal beyond goal?
   └─ Divergence: Does PRD significantly diverge from goal?

3. Classify Goal Preservation
   ├─ If exact match: user_goal_preserved_as: exact_match
   ├─ If core + expansion: user_goal_preserved_as: core_with_expansion
   └─ If diverged: user_goal_preserved_as: diverged (escalate)

4. Document Features
   ├─ Core features (goal-preserving) with acceptance criteria
   └─ Expansion features (if any) with rationale, effort, risk, status

5. Set Expansion Flags
   ├─ scope_expansion_proposed: true if expansions identified
   ├─ scope_expansion_requires_approval: true if proposed (always)
   └─ scope_expansion_status: exact_match | pending_user_approval | approved_by_user

6. Emit YAML
   ├─ source_intent_ref: ../../00-user-intent.md
   ├─ user_goal_preserved_as: [classification]
   ├─ scope_expansion_proposed: [boolean]
   ├─ scope_expansion_requires_approval: [boolean]
   ├─ scope_expansion_status: [state]
   └─ scope_expansion_details: [if proposed]
```

---

## What Happens in Workflows

### Case A: Exact Match (No Expansion)
```
to-prd → [user_goal_preserved_as: exact_match, scope_expansion_proposed: false]
  ↓
to-issues → Generate stories for core features only
  ↓
triage → Prioritize stories
  ↓
tdd → Begin development with story 1
```

### Case B: Expansion Proposed (Awaiting Approval)
```
to-prd → [user_goal_preserved_as: core_with_expansion, scope_expansion_proposed: true, status: pending_user_approval]
  ↓
[APPROVAL GATE] User decision: Approve or decline expansions?
  ├─ User approves: → scope_expansion_status: approved_by_user → to-issues generates all stories
  └─ User declines: → scope_expansion_status: core_only → to-issues generates core stories only
  ↓
to-issues → Generate approved stories
  ↓
triage → Prioritize
  ↓
tdd → Development
```

### Case C: Divergence (Escalation)
```
to-prd → [user_goal_preserved_as: diverged]
  ↓
[ESCALATION] PRD diverges from stated goal
  ↓
Escalate to user/orchestrator: Is new direction acceptable?
  ├─ User accepts: Revise intent, proceed
  └─ User declines: Return to discovery; find path that preserves goal
```

---

## Next Stage (Stage 4)

**Target**: `to-issues`

**Fields to promote** (when to-issues is patched):
```yaml
source_intent_ref
user_goal_preserved_as
scope_expansion_status
```

**Stage 4 success criterion**: to-issues produces valid issue lists with scope tracking for 3 scenarios:
1. Issues for core features only (no expansion)
2. Issues for core + approved expansion features
3. Rejection of divergent scope (escalation case)

---

## Stage 3 Summary

```
✅ Scope expansion instructions in place (to-prd SKILL.md)
✅ Output template updated with scope expansion fields
✅ 3/3 fixtures pass strict validation
✅ 3 scope expansion fields promoted to required
✅ Validator output is unambiguous
✅ Scope boundaries preserved (document goal, propose expansion, user decides)
✅ Three scope states clearly defined (exact match, pending approval, approved)

Ready for Stage 4: to-issues scope expansion status tracking
```

---

## Files Modified

1. `skills/to-prd/SKILL.md` — New skill with scope expansion workflow
2. `skills/to-prd/references/prd-template.md` — New template with scope expansion structure
3. `examples/to-prd-fixtures/01-goal-preserved.md` — Created exact match fixture
4. `examples/to-prd-fixtures/02-scope-expansion-proposed.md` — Created pending approval fixture
5. `examples/to-prd-fixtures/03-scope-expansion-approved.md` — Created approved expansion fixture
6. `skills/workflow-orchestrator/references/artifact-contracts.yaml` — Promoted 3 prd fields to required
7. `docs/INTENT-HARDENING-TRACKER.md` — Updated status, marked Stage 3 complete

**Verification**: `git diff skills/ examples/ docs/` shows all changes are isolated to intention.

---

## Backward Compatibility

Stage 3 is **backwards-incompatible** for to-prd:
- New required fields must be emitted
- Old PRDs (without scope expansion fields) will fail validation
- Migration path: Re-run to-prd with patched skill to regenerate PRDs with new fields

---

## Success Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Fixtures passing (strict mode) | 3/3 | 3/3 ✅ |
| Scope expansion fields documented | 3 | 3 ✅ |
| Scope expansion states defined | 3 | 3 ✅ |
| Scope boundaries clear | Yes | Yes ✅ |
| Validator output unambiguous | Yes | Yes ✅ |

---

## Lessons Learned

1. **Goal preservation is crucial** — Separating "core" (what user asked for) from "expansion" (what discovery found) makes user approval straightforward.

2. **Scope expansion always needs approval** — Even when proposed, expansion features are conditional. User always decides unless auto_expansion is enabled.

3. **Escalation is a safety net** — If PRD would diverge from stated goal, escalate rather than silently including divergent scope. User re-approves.

4. **Three states cover all cases** — Exact match, pending approval, approved. No ambiguity about PRD status.

5. **Discovery drives expansion** — Expansion isn't arbitrary; it's grounded in discovery findings (user interviews, evidence). This justifies approval requests.

---

## Ready for Production

Stage 3 is complete and ready for:
- ✅ Real PRD generation with scope expansion tracking
- ✅ User approval gates for expansion features
- ✅ Goal preservation visibility throughout workflow
- ✅ Hardening final stage (4: to-issues)

**Next**: Proceed to Stage 4 (to-issues scope expansion status).
