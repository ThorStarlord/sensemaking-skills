# ADR 0007: Soft Context Routing — User Intent as Weighted Input, Not Authority

**Status**: Proposed  
**Date**: 2026-05-19  
**Context**: Automating workflow selection when user problem statement may differ from repo diagnosis  
**Decision**: Repository diagnosis determines default routing. User intent is weighted context that can influence interpretation and break ties in low-confidence cases. Explicit `--workflow` override is the only way user intent overrides diagnosis.

---

## Context

### The Original Question
When a user says "we need a login page redesign" but the codebase shows auth middleware is the real blocker, which wins for routing purposes? The user's stated goal or the system's diagnosis?

### The Design Challenge
We need to:
1. Preserve diagnostic integrity — the system's job is to identify the weakest boundary, not optimize the user's stated solution
2. Respect user intent — the user's concern is real and should not be silently dismissed
3. Allow user authority when they know better — expert users should be able to override the system
4. Record the reasoning — if system recommendation and user choice diverge, the audit trail must show why
5. Support both novice and expert workflows — no-args users get safe defaults; expert users get full override control

### The Anti-Pattern Considered
**"User problem statement overrides repo diagnosis by default"**
- Problem: System can be tricked into optimizing the wrong layer
- Problem: User gets what they asked for, not what they actually need
- Problem: Weakens the "Fog First" principle — diagnosis is bypassed by user assumption
- Problem: Example: "redesign login page" → system redesigns login page → auth debt remains → users still experience auth failures

**"User problem statement is ignored; only diagnosis matters"**
- Problem: User feels unheard; their stated concern is treated as irrelevant
- Problem: Routing decision feels arbitrary; no explanation of why the system chose differently
- Problem: Removes user agency; no way for expert to override system judgment
- Problem: Reduces trust in diagnostic system (users will distrust "black box" routing)

---

## Decision

### Core Rule
**User intent shapes the question. Repo diagnosis answers the question. Orchestrator routes from the diagnosis unless explicitly overridden.**

More precisely:
- **User intent** is evidence that influences interpretation and weighting of diagnostic signals
- **Repo diagnosis** determines the default recommended workflow
- **Explicit override** (`--workflow X`) is the only way user intent can directly override diagnosis
- **Low-confidence diagnosis** can be influenced by user intent (user intent acts as tie-breaker)

### Routing Authority Ladder

Routing decisions follow this precedence:

```text
1. Explicit --workflow override
   └─ User explicitly selects a workflow via CLI flag
   
2. Approved gate decision
   └─ Human approval at a gate overrides prior recommendations
   
3. High-confidence repo diagnosis
   └─ System diagnosis has high confidence (e.g., fog_type_confidence >= 0.8)
   └─ User intent is recorded but does not change selected workflow
   
4. Low-confidence diagnosis + user intent tie-breaker
   └─ System diagnosis has low confidence (fog_type_confidence < 0.8)
   └─ Multiple fog types are plausible
   └─ User intent (implied fog type) influences selection
   
5. Default fallback workflow
   └─ If all else fails, route to safest default (implementation-workflow)
```

### Implementation

#### 1. Routing Decision Fields in Orchestration Plan

The `workflow_orchestration_plan` includes all information needed to audit routing:

```yaml
user_problem_statement: "we need a login page redesign" (or null)
user_implied_fog_type: ui_fog | architecture_fog | product_fog | docs_fog | null

primary_fog_type: architecture_fog (from repo diagnosis)
secondary_fog_type: ui_fog | null (from repo diagnosis)
fog_type_confidence: 0.8 (numeric confidence, 0.0–1.0)

diagnosis_conflict: boolean (true if user_implied_fog_type != primary_fog_type)

system_recommended_workflow: implementation-workflow
selected_workflow: implementation-workflow (or different if override used)

routing_decision_method: diagnosis_primary_soft_context | intent_tiebreaker | user_explicit_override
routing_authority: system | approved_gate | user_override

routing_rationale: |
  [Explanation of how the routing decision was made]
```

#### 2. Decision Flows

**Case A: High-confidence diagnosis, no user intent conflict**

```yaml
user_problem_statement: "improve dashboard performance"
user_implied_fog_type: architecture_fog
primary_fog_type: architecture_fog
fog_type_confidence: 0.9
diagnosis_conflict: false
system_recommended_workflow: implementation-workflow
selected_workflow: implementation-workflow
routing_decision_method: diagnosis_primary_soft_context
routing_authority: system
routing_rationale: |
  User and diagnosis agree on architecture_fog.
  High repo evidence confidence (0.9).
  Routing to implementation-workflow.
```

**Case B: High-confidence diagnosis, user intent differs**

```yaml
user_problem_statement: "we need a login page redesign"
user_implied_fog_type: ui_fog
primary_fog_type: architecture_fog
fog_type_confidence: 0.9
diagnosis_conflict: true
system_recommended_workflow: implementation-workflow
selected_workflow: implementation-workflow
routing_decision_method: diagnosis_primary_soft_context
routing_authority: system
routing_rationale: |
  User requested ui_fog (login redesign).
  Repo evidence strongly indicates architecture_fog (auth middleware debt) is binding.
  High confidence (0.9) in diagnosis.
  Recommend stabilizing auth architecture first, then returning to login redesign.
  User can override with --workflow ui-implementation-workflow.
```

**Case C: Low-confidence diagnosis, user intent acts as tie-breaker**

```yaml
user_problem_statement: "improve user experience"
user_implied_fog_type: ui_fog
primary_fog_type: mixed
secondary_fog_type: ui_fog
fog_type_confidence: 0.4
diagnosis_conflict: false (both point to ui_fog)
system_recommended_workflow: ui-implementation-workflow
selected_workflow: ui-implementation-workflow
routing_decision_method: intent_tiebreaker
routing_authority: system
routing_rationale: |
  Repo evidence is weak/ambiguous (confidence 0.4).
  Multiple fog types are plausible (mixed diagnosis).
  User intent points to ui_fog.
  Using user intent as tie-breaker.
  Routing to ui-implementation-workflow.
```

**Case D: User explicit override**

```bash
workflow-runtime.py \
  --problem "we need a login page redesign" \
  --workflow ui-implementation-workflow
```

```yaml
user_problem_statement: "we need a login page redesign"
user_implied_fog_type: ui_fog
primary_fog_type: architecture_fog
fog_type_confidence: 0.9
diagnosis_conflict: true
system_recommended_workflow: implementation-workflow
selected_workflow: ui-implementation-workflow
routing_decision_method: user_explicit_override
routing_authority: user_override
override_reason: user_selected_workflow_explicitly
routing_rationale: |
  User explicitly selected ui-implementation-workflow via --workflow flag.
  System recommended implementation-workflow (architecture_fog).
  User override accepted. Audit trail preserved.
```

#### 3. Soft Scope Mode (Default)

In `--scope soft` (the default):
- User intent is context, not veto
- System diagnosis can surface broader/different concerns
- If diagnosis diverges from user intent, routing shows the conflict but follows diagnosis (unless override used)
- Implementation workflows receive full context (intent + diagnosis) and can propose scope expansion

#### 4. Hard Scope Mode (Escape Hatch)

In `--scope hard`:
- User intent defines the boundary for analysis
- System findings outside that boundary are recorded as "out of scope"
- Only issues directly relevant to user-stated concern are escalated to implementation
- Diagnostic conflicts are recorded but do not influence routing unless user explicitly approves

---

## Consequences

**Positive:**
- System can diagnose the actual weakest boundary without being overridden by user assumption
- Audit trail is clear: routing decision records system recommendation vs. user selection
- User agency is preserved: `--workflow` override is always available for experts
- Low-confidence cases can be guided by user intent without requiring override
- Soft scope (default) feels human-centered: user's goal is preserved while system offers better alternative

**Negative:**
- Adds routing_decision fields to orchestration_plan schema
- Requires validators to verify that routing_decision_method is one of the allowed values
- Users might initially feel overridden if diagnosis differs from their stated concern (needs clear communication)

**Mitigations:**
- Routing rationale is explicit and clear
- User can always override with `--workflow`
- Guided execution mode includes a gate before implementation starts, allowing user to approve or override routing

---

## Related Decisions

- **ADR 0006**: User Intent as Durable Artifact (how intent is preserved and propagated)
- **ADR 0008**: Routing Divergence Audit (how to record and validate routing decisions)
