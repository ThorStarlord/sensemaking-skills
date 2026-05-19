# ADR 0008: Routing Divergence and Action Audit Trail

**Status**: Proposed  
**Date**: 2026-05-19  
**Context**: Tracking when system recommendations diverge from selected action (override, escalation, scope expansion)  
**Decision**: Every workflow decision records system recommendation vs. selected action separately. Divergences are explicit, auditable, and require recorded rationale.

---

## Context

### The Original Question
When the system recommends one workflow but the user (or an execution mode) chooses another, how should the system record this? What counts as a divergence? When should divergence require approval?

### The Design Challenge
We need to track:
1. **Routing divergence**: System recommended workflow A, but workflow B was selected
2. **Escalation**: Fast-path recommended further analysis, so system (or human) approved escalating to full-fog
3. **Scope expansion**: Implementation discovered additional work beyond user-stated intent; should it be approved?
4. **Intent re-scoping**: User changed their mind mid-workflow about what the problem is; what happens to prior approval?

All of these are "differences between system recommendation and action taken" and should be auditable.

### The Anti-Pattern Considered
**"Different recommendation vs. selected action is implicit or unrecorded"**
- Problem: Audit trail is broken; can't tell why a different workflow ran
- Problem: No clear approval boundary; unclear whether divergence was intentional
- Problem: Scope expansion happens silently; user doesn't know extra work was added
- Problem: Intent changes mid-run with no approval invalidation; execution proceeds as if intent unchanged

---

## Decision

### Core Rule
**Record the difference between system recommendation and selected action separately. Divergence is explicit, auditable, and tracked with decision rationale.**

### Audit Invariant

Every workflow execution includes:

```yaml
# Workflow recommendation (system's default)
system_recommended_workflow: implementation-workflow

# Selected action (what actually runs)
selected_workflow: implementation-workflow

# Divergence flag (true if they differ)
routing_divergence: boolean

# How the divergence occurred
routing_decision_method: |
  diagnosis_primary_soft_context |  # System diagnosis won
  intent_tiebreaker |               # User intent broke a tie
  user_explicit_override |          # User --workflow flag
  approved_gate |                   # Human approval at gate overrode prior
  escalation_approved |             # Escalation was approved
  scope_expansion_approved          # Scope expansion was approved

# Detailed rationale for the decision
routing_rationale: string (multi-line explanation)
```

This invariant ensures:
- You can always see what the system recommended
- You can always see what was actually selected
- You can always see why they diverged (if they did)
- No divergence is silent or implicit

### Escalation Tracking

When a workflow detects uncertainty that suggests deeper analysis is needed, it signals escalation:

```yaml
escalation_recommended: boolean
escalation_target: workflow_id | null (e.g., full-local-sensemaking)
escalation_reason: high_uncertainty | intent_diagnosis_conflict | insufficient_evidence | user_requested
escalation_triggers:
  - unknowns_count >= threshold
  - clarity_assessment: low
  - diagnosis_conflict: true
auto_escalation_allowed: false  # KEY: escalation is recommended, not automatic
requires_user_approval: boolean (true unless in yolo_execution mode)
```

**Critical rule**: Fast-path workflow recommends escalation but does NOT auto-chain by default. The user or an explicit execution mode (e.g., `--execute` flag) must approve escalation. This preserves the "smallest useful diagnostic artifact" principle.

Behavior by execution mode:
```text
plan_only                 → halt after escalation recommendation
prompt_chain              → halt; return recommended escalation command
guided_execution          → pause; ask user for approval before escalating
autonomous_execution      → auto-escalate with escalation_approved recorded
yolo_execution            → auto-escalate silently (no approval gate)
```

### Scope Expansion Tracking

When implementation workflows (to-prd, to-issues) discover work beyond the user's stated intent, they surface it explicitly:

```yaml
user_goal_preserved_as: string (how this artifact addresses the user's intent)
user_goal_addressed_in: |
  primary | secondary | appendix (how central is it to the deliverable?)

scope_expansion_proposed: list
  - ticket_id: "add session management cleanup"
    priority: medium
    belongs_to_user_goal: false
    rationale: "reduces auth brittleness, complements primary work"
    requires_approval: true

scope_expansion_requires_approval: boolean
selected_scope_expansion_items: list | null
scope_expansion_status: proposed | approved | deferred | rejected
```

**Critical rule**: Scope expansion is proposed, not silently committed. Selected implementation issues stay within the approved workflow unless a gate explicitly approves expansion. The approval gate records which expansion items were selected.

### Intent Re-scoping Mid-Workflow

If the user clarifies or changes their intent during a workflow run (ADR 0006 amendment), the approval state is affected:

```yaml
intent_amendment_ref: 00b-user-clarification.md | null
prior_approval_status: approved | invalid
approval_invalidated: boolean
reroute_required: boolean
current_workflow_status: running | paused | halted
next_action: continue_with_amendment | replan | new_run
```

**Critical rule**: If intent changes (creates an amendment), prior approval becomes invalid unless the amendment is explicitly marked "non-routing" (e.g., clarification of the same problem, not a scope change).

Behavior by execution mode when intent amendment invalidates approval:
```text
plan_only              → regenerate plan (auto-replan)
guided_execution       → pause; ask for approval to continue or replan
autonomous_execution   → halt (cannot continue with invalid approval)
yolo_execution         → hard stop (never silently continue past intent change)
```

---

## Consequences

**Positive:**
- Audit trail is complete: system recommendation, selected action, decision rationale are all recorded
- Divergences are explicit, never silent
- Scope expansion is intentional, not sneaky
- Intent changes invalidate approval reliably
- Escalation respects user authority (recommended but not automatic by default)

**Negative:**
- Adds more fields to artifact schema (routing_divergence, escalation_recommended, scope_expansion_proposed, etc.)
- Requires validators to check that routing_decision_method is valid
- Requires execution logic to check for intent amendments and invalidate approval
- Adds approval gates for escalation and scope expansion (slower in guided mode)

**Mitigations:**
- Fields are optional/conditional (only populate if divergence/escalation/expansion exists)
- Validators are added incrementally (Phase 1–5)
- Validators check structure first; semantic enforcement deferred to value-production runs

---

## Examples

### Example 1: Escalation (Fast-path recommends full-fog)

```yaml
# In fast-path artifact:
escalation_recommended: true
escalation_target: full-local-sensemaking
escalation_reason: high_uncertainty
escalation_triggers:
  - unknowns_count: 8 (>= 5)
  - clarity_assessment: low
auto_escalation_allowed: false
requires_user_approval: true

# User sees:
# "Fast-path diagnosis found high uncertainty.
#  Recommend escalation to full-fog for deeper analysis.
#  Command: workflow-runtime.py --workflow full-local-sensemaking"

# User can then:
# A) Run the recommended command (guided_execution)
# B) Stay with fast-path results (override escalation)
# C) Ask for autonomous escalation (set a flag)
```

### Example 2: Routing divergence (High-confidence diagnosis, user override)

```yaml
user_problem_statement: "we need a login page redesign"
primary_fog_type: architecture_fog
fog_type_confidence: 0.9
system_recommended_workflow: implementation-workflow
selected_workflow: ui-implementation-workflow
routing_divergence: true
routing_decision_method: user_explicit_override
routing_authority: user_override

routing_rationale: |
  System diagnosed architecture_fog (auth middleware) as the weakest boundary.
  User explicitly selected ui-implementation-workflow via --workflow flag.
  User override accepted. Proceeding with UI workflow.
  Note: Recommend returning to architecture work after login redesign completes.
```

### Example 3: Scope expansion (to-issues proposes cleanup tasks)

```yaml
user_goal_preserved_as: "stabilize auth middleware"

scope_expansion_proposed:
  - ticket_id: "Session cache cleanup"
    priority: medium
    belongs_to_user_goal: false
    rationale: "reduces auth brittleness"
    requires_approval: true
  - ticket_id: "Add error recovery flow"
    priority: low
    belongs_to_user_goal: true
    rationale: "improves user experience during auth failures"

scope_expansion_requires_approval: true
selected_scope_expansion_items:
  - "Add error recovery flow"
scope_expansion_status: approved
```

### Example 4: Intent re-scoping mid-workflow

```yaml
# Original intent:
# 00-user-intent.md:
#   raw_problem_statement: "improve dashboard performance"

# Mid-workflow user says: "Actually, that's not the real problem.
#                           We need to rethink the data model."

# System creates:
# 00b-user-clarification.md:
#   amends_intent_ref: 00-user-intent.md
#   raw_clarification: "Actually, we need to rethink the data model"
#   clarification_type: scope_expansion
#   requires_reroute: true

# Artifact chain records:
intent_amendment_ref: 00b-user-clarification.md
prior_approval_status: invalid
approval_invalidated: true
reroute_required: true
current_workflow_status: paused
next_action: replan

# System pauses execution and asks user:
# "Your intent has changed. Prior approval is no longer valid.
#  Approve to:
#  A) Continue with original plan (assume clarification is context only)
#  B) Pause and replan from fast-path (new scope)
#  C) Start a new run with new intent"
```

---

## Related Decisions

- **ADR 0006**: User Intent as Durable Artifact (how intent amendments work)
- **ADR 0007**: Soft Context Routing (how routing decisions are made)
