# Issue List: Core + Approved Expansion

**Scenario**: PRD includes core features AND approved scope expansions; to-issues generates stories for full development scope.

---

## PRD Consumed

From product_requirements_document:
- user_goal_preserved_as: core_with_expansion
- scope_expansion_proposed: true
- scope_expansion_status: approved_by_user (user approved due dates and recurring tasks)

## Scope Status

This issue list implements the core features PLUS user-approved expansions. All features are in development scope.

---

## Issues Generated: Core Features

### Story 1: Task Creation
**ID**: TASK-001  
**Type**: Feature  
**Title**: Create tasks with title and optional description

**Acceptance Criteria**:
- User can input task title (required, max 100 chars)
- User can input optional description (max 500 chars)
- User can optionally set due date (date picker)
- User can optionally set recurrence pattern
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
- If task has recurrence, completion generates next occurrence

**Effort**: 2 days (updated for recurring task handling)  
**Priority**: P0 (core feature)

---

### Story 4: Task List View
**ID**: TASK-004  
**Type**: Feature  
**Title**: Display tasks in list view with sorting and filtering

**Acceptance Criteria**:
- List shows: Title, Priority badge, Due date (if set), Recurrence badge (if set), Completion status
- Default sort: By priority (High → Medium → Low), then by creation date
- Sort options: By priority, by due date (upcoming first), by creation date
- Filter modes: "All tasks", "Incomplete only", "Overdue only"
- Overdue tasks highlighted in red
- Recurrence badge shows next to title (e.g., "Daily", "Weekly")
- List updates immediately on task action

**Effort**: 3.5 days (updated for due date and recurrence display)  
**Priority**: P1 (depends on all other core stories)

---

## Issues Generated: Approved Expansions

### Story 5: Task Due Dates
**ID**: TASK-005  
**Type**: Feature (Approved Expansion)  
**Title**: Set and track task due dates

**Acceptance Criteria**:
- User can set optional due date when creating or editing task
- Date picker allows selection from today forward
- Due dates display in MM/DD format in list view
- Overdue tasks (due_date < today) highlighted in red background
- "Sort by due date" option shows upcoming tasks first
- Relative date display: "Today", "Tomorrow", "3 days from now"
- Tasks without due dates display blank in due date column

**Effort**: 2.5 days  
**Priority**: P1 (approved expansion)  
**Approved**: Yes (user approved on 2026-05-19)

---

### Story 6: Recurring Tasks
**ID**: TASK-006  
**Type**: Feature (Approved Expansion)  
**Title**: Create and manage recurring tasks

**Acceptance Criteria**:
- User can set recurrence pattern: None (default), Daily, Weekly, Monthly
- Recurrence pattern selectable during task creation
- When completed, recurring task auto-generates next occurrence:
  - Daily: tomorrow at same time
  - Weekly: next week (same day of week)
  - Monthly: same day next month
- New occurrence has same title, priority, due date offset, recurrence pattern
- Recurrence badge displays in list view (e.g., "Daily", "Weekly")
- User can edit or delete recurrence after task creation
- Completed recurring task stays in list as complete; next occurrence is separate

**Effort**: 3.5 days  
**Priority**: P2 (approved expansion, lower priority for MVP)  
**Approved**: Yes (user approved on 2026-05-19)

---

## Release Scope

**Total Issues**: 6 stories (4 core + 2 approved expansion)  
**Breakdown**:
- P0 stories (must-have core): 3
- P1 stories (core list + due dates): 2
- P2 stories (recurring tasks): 1

**Total Effort**: 14-15 days  
**Timeline**: Week 1-2 (MVP + approved expansions)

---

## Phasing Strategy

### Phase 1: Core Features (5-7 days)
Stories: TASK-001, TASK-002, TASK-003, TASK-004
- Delivers basic task list management
- Unblocks QA and user testing

### Phase 2: Due Dates (2-3 days)
Stories: TASK-005
- Adds date-based task management
- Low risk; isolated feature
- Can be tested independently

### Phase 3: Recurring Tasks (3-4 days)
Stories: TASK-006
- Most complex feature
- Depends on completion tracking (TASK-003)
- High value; frequently requested

---

## Out of Scope (Not Generated)

The following are NOT included in this issue list:
- Task categories / tags
- Persistence / data storage
- Multi-user support
- Mobile app
- Notifications
- Integrations

---

## Machine-Readable Handoff

```yaml
artifact_id: issue_list
schema_version: 1
source_intent_ref: ../../00-user-intent.md
user_goal_preserved_as: core_with_expansion
scope_expansion_proposed: true
scope_expansion_status: approved_by_user
issues_generated: 6
core_issues_count: 4
expansion_issues_count: 2
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
    effort_days: 2
    priority: P0
  - id: TASK-004
    title: "Display tasks in list view with sorting and filtering"
    type: feature
    effort_days: 3.5
    priority: P1
    depends_on: [TASK-001, TASK-002, TASK-003]
  - id: TASK-005
    title: "Set and track task due dates"
    type: feature_expansion
    effort_days: 2.5
    priority: P1
    expansion_status: approved_by_user
  - id: TASK-006
    title: "Create and manage recurring tasks"
    type: feature_expansion
    effort_days: 3.5
    priority: P2
    expansion_status: approved_by_user
    depends_on: [TASK-003]
created_at: "2026-05-19T19:15:00Z"
```

---

## Next Steps

1. **triage** — Prioritize and sequence stories per phasing strategy
2. **tdd** — Begin with TASK-001 (Task Creation)
3. QA gates after each phase to validate before next
