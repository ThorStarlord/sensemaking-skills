# Issue List: Scope Divergence (Escalation)

**Scenario**: PRD scope diverged from stated goal; to-issues does NOT generate stories. Escalation to user required.

---

## PRD Consumed

From product_requirements_document:
- user_goal_preserved_as: diverged
- scope_expansion_proposed: N/A
- scope_expansion_status: N/A (escalation, not normal flow)

## Issue Generation Status

⚠️ **ESCALATION**: PRD scope diverged from user's stated goal.

No issues generated. Escalation required before proceeding.

---

## What Happened

**User's Stated Goal** (from intent):
"Enable users to manage their daily task lists with clear priorities and completion tracking."

**PRD Scope** (divergence detected):
"Build a complex collaborative workflow engine with multi-user support, real-time sync, integrations with calendar and project management tools."

**Analysis**:
The PRD scope is fundamentally different from the stated goal. The user asked for a simple task list; the PRD proposes a complex enterprise platform. This is divergence, not expansion.

---

## Why Escalation Matters

✋ **Do not generate stories for diverged scope.**

Generating issues based on diverged scope would commit development to a different product than what the user asked for. This violates the intent preservation principle.

---

## Escalation Options

### Option 1: Return to Discovery
- Go back to discovery findings
- Find a path that addresses both user's stated goal AND critical findings
- Revise PRD to preserve core goal while proposing expansion (not divergence)
- Re-submit PRD for approval

### Option 2: User Confirms New Direction
- Present diverged PRD to user
- User explicitly approves new direction ("Yes, I want this instead")
- Update intent to reflect new goal
- Regenerate PRD with new intent as reference
- Proceed with new scope

### Option 3: Narrow PRD to Stated Goal
- Keep scope focused on stated goal only
- Defer complex features to v2 roadmap
- Identify MVP path that delivers stated goal
- Revise PRD with narrower scope
- Generate issues for focused MVP

---

## Escalation Gate

⚠️ **ACTION REQUIRED**

**Current State**:
- Intent: "Simple task list with priorities and completion tracking"
- PRD: "Enterprise workflow platform with multi-user, sync, integrations"
- Status: **DIVERGENCE DETECTED**

**Choose One**:

1. **Return to Discovery**
   - "I want to stay focused on simple task list. Help me find a path that delivers that."
   - Action: Revise PRD to preserve goal; propose only non-divergent expansions
   
2. **Confirm New Direction**
   - "I want to build the enterprise platform instead. Update my goal accordingly."
   - Action: Revise intent; regenerate PRD; proceed with new scope
   
3. **Narrow to MVP**
   - "Keep it simple. Just the basic task list. Save complex features for later."
   - Action: Narrow PRD to stated goal only; minimize scope

**Do not proceed to issue generation until divergence is resolved.**

---

## Machine-Readable Handoff

```yaml
artifact_id: issue_list
schema_version: 1
source_intent_ref: ../../00-user-intent.md
user_goal_preserved_as: diverged
scope_expansion_proposed: N/A
scope_expansion_status: diverged
issues_generated: 0
escalation_required: true
escalation_reason: "PRD scope diverged from stated user goal"
escalation_details:
  user_goal: "Simple task list with priorities and completion tracking"
  prd_scope: "Enterprise workflow platform with multi-user, sync, integrations"
  analysis: "Scope is fundamentally different; not an expansion but a new product"
escalation_options:
  - option: "return_to_discovery"
    description: "Find path that preserves goal and addresses critical findings"
    action: "Revise PRD to propose only non-divergent expansions"
  - option: "confirm_new_direction"
    description: "User approves diverged scope as new goal"
    action: "Update intent; regenerate PRD; proceed with new scope"
  - option: "narrow_to_goal"
    description: "Keep scope focused on stated goal only"
    action: "Revise PRD with narrower scope; defer complex features to v2"
decision_required_from: user
created_at: "2026-05-19T19:30:00Z"
```

---

## What Happens Next (When Escalation Resolved)

**If Option 1 (Return to Discovery)**:
- Go back to workflow
- Revise discovery findings / opportunity map
- Regenerate PRD with preserved goal
- Re-submit for validation
- Proceed to issue generation

**If Option 2 (Confirm New Direction)**:
- Update source intent to reflect new goal
- Regenerate PRD from new intent
- Treat new scope as authoritative
- Generate issues for new scope

**If Option 3 (Narrow to MVP)**:
- Revise PRD to remove divergent features
- Focus on stated goal features only
- Save complex features for future roadmap
- Generate issues for focused scope

---

## No Issues Generated (Escalation Status)

This issue list is empty because scope divergence must be resolved before development commitment.

**Status**: ⏸️ **PAUSED** — Awaiting user decision on escalation
