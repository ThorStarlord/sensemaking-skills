# ADR 0006: User Intent as Immutable Durable Artifact

**Status**: Proposed  
**Date**: 2026-05-19  
**Context**: Automating workflow entry point from user problem statements  
**Decision**: Every workflow run begins with an immutable `user_intent` artifact. Later clarifications are append-only amendments, never mutations.

---

## Context

### The Original Question
When a user runs `orchestration-runner.py --problem "..."`, where should that intent live? As runtime metadata? As a durable artifact? Should the system allow the user to refine or clarify it mid-workflow?

### The Design Challenge
In a system with multiple execution modes (plan_only, guided_execution, autonomous_execution, yolo_execution) and approval gates at critical points, we need to:
1. Preserve the exact problem statement the user provided (auditability)
2. Allow diagnostic interpretation without mutating the original (traceability)
3. Support user clarifications or re-scoping mid-run (flexibility)
4. Make intent visible to downstream skills (to-prd, to-issues, handoff) so implementers know the user's goal
5. Distinguish between "user said this" vs. "system inferred this" (audit trail)

### The Anti-Pattern Considered
**"Intent is runtime metadata, not a durable artifact"**
- Problem: No audit trail; easy to lose original problem statement during workflow execution
- Problem: Downstream skills (to-prd, to-issues) cannot reference user intent explicitly; they operate blind to the original goal
- Problem: If user re-scopes mid-workflow, no way to know what changed from what

**"Intent artifact is mutable"**
- Problem: Audit trail collapses; can't verify what the user originally said vs. what they clarified
- Problem: Invalidates approval gates — if intent changes, prior approval based on old intent is no longer valid, but the system cannot detect this

---

## Decision

### Core Rule
**User intent is immutable. Every run creates a durable `00-user-intent.md` artifact. Later clarifications become separate amendment artifacts (`00b-user-clarification.md`, `00c-user-clarification.md`, etc.), never edits to the original.**

### Implementation

#### 1. User Intent Artifact Schema

Every workflow run creates a `00-user-intent.md` with this structure:

```yaml
# Machine-readable intent
---
artifact_id: user_intent
schema_version: 1
intent_source: user_problem_statement | repo_inferred | imported_ticket
scope_mode: soft | hard | advisory
raw_problem_statement: string | null
immutable: true
created_at: timestamp (ISO 8601)
created_by: runner | user_name
repo_state_used: boolean
constraints: []
non_goals: []
clarifications: []
---
```

**Field semantics:**
- `intent_source`: How the intent was provided
  - `user_problem_statement`: User provided via CLI `--problem` or positional arg
  - `repo_inferred`: System inferred from git state (no user problem provided)
  - `imported_ticket`: Loaded from issue tracker or context file
- `scope_mode`: How strictly the problem statement constrains execution
  - `soft` (default): Intent is context; system diagnosis can surface broader/different concerns
  - `hard`: Intent defines the only scope to analyze; system findings outside scope are appendix-only
  - `advisory`: Intent is primary scope; system can surface conflicts but execution stays within scope unless approved
- `raw_problem_statement`: Exact text provided by user, or null if repo_inferred
- `immutable: true`: Marker that this artifact is never edited
- `created_at`: When intent was created (workflow start)
- `created_by`: Who/what created it (runner timestamp, or user name if provided)
- `repo_state_used`: Whether code/git state was considered
- `constraints`: Hard constraints on the problem (if any user specified them)
- `non_goals`: Explicitly out-of-scope items (if user specified them)
- `clarifications`: List of amendment artifact refs that refine this intent

#### 2. No-Arguments Behavior

When the user runs:
```bash
orchestration-runner.py
```
without a problem statement, the system still creates `00-user-intent.md` with:
```yaml
intent_source: repo_inferred
raw_problem_statement: null
repo_state_used: true
```
This ensures every run has a consistent intent artifact, even if it's empty.

#### 3. Intent Amendments

If the user clarifies or re-scopes intent during a workflow run:
```bash
User says: "Actually, that's not the problem."
```

The system creates a separate amendment artifact (`00b-user-clarification.md`, etc.):

```yaml
# Machine-readable amendment
---
artifact_id: user_intent_amendment
schema_version: 1
amends_intent_ref: 00-user-intent.md
raw_clarification: string
clarification_type: scope_refinement | scope_expansion | out_of_scope_addition
requires_reroute: boolean
created_at: timestamp
created_by: user
---
```

The original `00-user-intent.md` remains unchanged. The amendment is listed in `clarifications: [00b-user-clarification.md]` only if you re-read the original after amendment creation.

Actually, no: amendments are immutable separate files. The original artifact is never re-read. Downstream artifacts reference both via:
```yaml
source_intent_ref: 00-user-intent.md
source_intent_amendment_refs:
  - 00b-user-clarification.md
```

#### 4. Propagation Through Artifact Chain

Every downstream artifact must include:
```yaml
source_intent_ref: path/to/00-user-intent.md
source_intent_amendment_refs: [ ]  # if amendments exist
user_goal_preserved_as: string (optional, how this artifact honors user intent)
```

Examples:
- `problem_frame` references intent and records how it interprets the user's statement
- `repository_sensemaking_brief` references intent and records if diagnosis conflicts with it
- `workflow_orchestration_plan` references intent and records routing decision rationale
- `prd` references intent and records how the product plan addresses the user's goal
- `issue_list` references intent and records how tickets map back to user concern

#### 5. Immutability Boundary

This rule is firm:
```text
00-user-intent.md is NEVER edited.
Clarifications create NEW amendments.
Amendments are NEVER edited once created.
Downstream artifacts ALWAYS reference source intent(s) via explicit field.
```

This ensures that any point in the workflow can see:
1. What the user originally said (00-user-intent.md)
2. What they clarified (00b-user-clarification.md, etc.)
3. How the system interpreted it (problem_frame)
4. How the system diagnosed differently (brief)
5. What decision was made and why (orchestration_plan)

---

## Consequences

**Positive:**
- Audit trail is unbreakable: every artifact points back to the original intent
- Approval gates can detect intent changes and invalidate prior approval
- Downstream skills (to-prd, to-issues) can see the user's goal AND the system's diagnosis side-by-side
- Debugging is clear: if an artifact seems misaligned with user intent, the reference chain shows where the decision was made

**Negative:**
- Adds three new artifact types to the system (user_intent, user_intent_amendment, and implicit upstream artifact refs)
- Requires validators to check that source refs exist and are correct
- Requires workflow registry to declare user_intent as an input

**Mitigations:**
- Validators are added incrementally (Phase 1–5)
- Structural validation (refs exist) is enforced first; semantic validation (intent truly honored) is deferred to value-production runs

---

## Related Decisions

- **ADR 0007**: Soft Context Routing (how user intent influences workflow selection)
- **ADR 0008**: Routing Divergence Audit (how to record when user intent and system diagnosis conflict)
