# Issue List: Core Features Only

**Scenario**: PRD includes only core features (no scope expansion); to-issues generates stories for goal-preserving scope.

---

## PRD Consumed

From product_requirements_document:
- user_goal_preserved_as: exact_match
- scope_expansion_proposed: false
- scope_expansion_status: exact_match

## Goal Preservation

This issue list implements exactly what the user asked for: core features with no expansion.

---

## Issues Generated

### Story 1: Task Creation
**ID**: TASK-001  
**Type**: Feature  
**Title**: Create tasks with title and optional description

**Acceptance Criteria**:
- User can input task title (required, max 100 chars)
- User can input optional description (max 500 chars)
- Task is created with auto-generated ID and timestamp
- Success message shows "Task created"

**Effort**: 2 days  
**Priority**: P0 (unblocks all other features)

---

### Story 2: Priority Management
**ID**: TASK-002  
**Type**: Feature  
**Title**: Assign priority levels to tasks

**Acceptance Criteria**:
- User can select priority: High, Medium, Low
- Priority can be set during creation or edited after
- Priority displays in task list view
- Default priority is Medium if not specified

**Effort**: 1 day  
**Priority**: P0 (required for list sorting)

---

### Story 3: Task Completion Tracking
**ID**: TASK-003  
**Type**: Feature  
**Title**: Mark tasks as complete and track status

**Acceptance Criteria**:
- User can click checkbox to mark task complete
- Completion timestamp is recorded
- Completed task shows checkmark or strikethrough
- User can restore task to incomplete status

**Effort**: 1.5 days  
**Priority**: P0 (core feature)

---

### Story 4: Task List View
**ID**: TASK-004  
**Type**: Feature  
**Title**: Display tasks in list view with sorting and filtering

**Acceptance Criteria**:
- List shows: Title, Priority badge, Completion status
- Default sort: By priority (High → Medium → Low), then by creation date
- Filter modes: "All tasks" and "Incomplete only"
- List updates immediately on task action

**Effort**: 2.5 days  
**Priority**: P1 (depends on TASK-001, TASK-002, TASK-003)

---

## Release Scope

**Total Issues**: 4 core stories  
**Total Effort**: 7 days  
**Priority**: All P0/P1  
**Timeline**: Week 1 (MVP scope)

---

## Out of Scope (Not Generated)

The following are NOT included in this issue list per PRD:
- Due dates
- Recurring tasks
- Task categories
- Persistence
- Multi-user support
- Mobile app
- Notifications

---

## Testing Plan

- Unit tests for task creation, priority assignment, completion tracking
- Integration tests for list rendering and updates
- Acceptance tests for each story's criteria
- No E2E tests for MVP (browser manual testing sufficient)

---

## Machine-Readable Handoff

```yaml
artifact_id: issue_list
schema_version: 1
source_intent_ref: ../../00-user-intent.md
user_goal_preserved_as: exact_match
scope_expansion_proposed: false
scope_expansion_status: exact_match
issues_generated: 4
issues:
  - id: TASK-001
    title: "Create tasks with title and optional description"
    type: feature
    effort_days: 2
    priority: P0
  - id: TASK-002
    title: "Assign priority levels to tasks"
    type: feature
    effort_days: 1
    priority: P0
  - id: TASK-003
    title: "Mark tasks as complete and track status"
    type: feature
    effort_days: 1.5
    priority: P0
  - id: TASK-004
    title: "Display tasks in list view with sorting and filtering"
    type: feature
    effort_days: 2.5
    priority: P1
    depends_on: [TASK-001, TASK-002, TASK-003]
created_at: "2026-05-19T19:00:00Z"
```

---

## Next Steps

1. **triage** — Prioritize stories (all P0/P1 for MVP)
2. **tdd** — Begin with TASK-001 (Task Creation)
3. Each story drives test-first development
