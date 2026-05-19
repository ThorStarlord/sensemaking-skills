# Product Requirements Document: Scope Expansion Approved

**Scenario**: Scope expansion was proposed, user approved selected features, now included in development scope.

---

## Executive Summary

This PRD addresses the user's stated goal AND approved scope expansions. All features (core + approved expansion) are included in the development scope.

## User Goal (As Stated)

"Enable users to manage their daily task lists with clear priorities and completion tracking."

## Goal Preservation and Approved Expansion

**user_goal_preserved_as**: core_with_expansion  
**scope_expansion_proposed**: true  
**scope_expansion_requires_approval**: true  
**scope_expansion_status**: approved_by_user

The core goal is preserved. User approved 2 out of 2 proposed expansions:
- ✅ **Due Dates**: APPROVED
- ✅ **Recurring Tasks**: APPROVED

---

## Features: Core + Approved Expansions

### Core Feature Set (Original Goal)

#### Feature 1: Task Creation
Allow users to create new tasks with optional description.

**Requirements**:
- Input: Task title (required), description (optional)
- Output: Task created with timestamp
- Storage: In-memory list (MVP scope)

#### Feature 2: Priority Management
Allow users to assign priority levels to tasks.

**Requirements**:
- Priority levels: High, Medium, Low
- Applies to all tasks (core + expanded)

#### Feature 3: Completion Tracking
Allow users to mark tasks as complete.

**Requirements**:
- Mark complete / restore to incomplete
- Track completion timestamp
- Display completion status in list view

#### Feature 4: Task List View
Display all tasks in a list view with sorting and filtering.

**Requirements**:
- Show: Title, priority, completion status
- Sort: By priority (high→low), then by creation date
- Filter: Show all, show incomplete only

### Approved Expansion 1: Task Due Dates

**Approval**: ✅ APPROVED by user on 2026-05-19 at 18:30

**Rationale**: Discovery revealed users want to set when tasks are due. 8/10 interviewed users requested this feature.

**Features**:
- Add optional due date field to tasks
- Show due date in list view (MM/DD format)
- Highlight overdue tasks with red background
- Add sort option: by due date (upcoming first)
- Display relative due date (e.g., "Today", "Tomorrow", "5 days from now")

**Requirements**:
- Due date field is optional (tasks without due dates still work)
- Overdue detection: tasks with due_date < today are overdue
- Sort priority: due date ascending (soonest first)
- Red highlight applied to tasks where due_date < today

**Effort**: 2-3 days development  
**Risk Mitigations**: Date picker tested with multiple browsers; timezone handling limited to local time

#### Feature 4.1: List View Updates (Due Dates)

Modified list view includes:
- **Column 1**: Task title
- **Column 2**: Priority (High/Medium/Low badge)
- **Column 3**: Due date (if set) — MM/DD format
- **Column 4**: Completion status
- **Overdue styling**: Red background for tasks with due_date < today

#### Feature 4.2: Task Sorting (Due Dates)

Add new sort option to list view:
- **Sort by Due Date**: Tasks sorted by due_date ascending (upcoming first)
- **Within due date**: Sort by priority (high→low)

### Approved Expansion 2: Recurring Tasks

**Approval**: ✅ APPROVED by user on 2026-05-19 at 18:30

**Rationale**: Discovery revealed users have repeating tasks (daily standup, weekly review). 6/10 interviewed users requested this feature.

**Features**:
- Recurrence pattern: Daily, Weekly, Monthly
- Auto-generate next occurrence when task marked complete
- Show recurrence badge in list view (e.g., "Daily")
- Allow manual recurrence editing/deletion

**Requirements**:
- Recurrence field is optional
- Available patterns: Daily, Weekly, Monthly
- When recurring task marked complete:
  - Original task marked complete
  - New task created with same title, priority, pattern
  - New due date calculated based on pattern (today + 1 day for Daily, etc.)
- Recurrence badge displayed next to title

**Effort**: 3-4 days development  
**Risk Mitigations**: Recurrence math tested with edge cases (leap years, month boundaries); timezone limited to local time

#### Feature 5.1: Recurring Task Creation

New field in task creation form:
- **Recurrence pattern**: None (default), Daily, Weekly, Monthly
- If pattern selected: task recurs after completion

#### Feature 5.2: Recurring Task Execution

When user marks recurring task complete:
1. Mark original task complete (add completion timestamp)
2. Generate next occurrence:
   - **Daily**: tomorrow at same time
   - **Weekly**: next week (same day of week) at same time
   - **Monthly**: next month (same day) at same time
3. New task has same: title, priority, due date (if set), recurrence pattern
4. Show recurrence badge on both original and new task

---

## Out of Scope (Even With Expansions)

The following remain deferred:

- **Task categories/tags**: Separate initiative
- **Persistence**: In-memory only (data storage v2)
- **Multi-user support**: Single user only
- **Mobile app**: Web interface only
- **Notifications**: Deferred to v2
- **Integrations**: Standalone tool
- **Task dependencies**: Not requested in discovery

---

## Acceptance Criteria

### Core Features (Goal-Preserving)

- [ ] User can create tasks with title and optional description
- [ ] User can set task priority (High/Medium/Low)
- [ ] User can mark tasks complete
- [ ] User can view task list sorted by priority
- [ ] User can filter: all tasks or incomplete only

### Due Dates (Approved Expansion)

- [ ] User can set optional due date on task
- [ ] Due dates display in list view (MM/DD format)
- [ ] Overdue tasks highlight with red background
- [ ] Sort by due date option available
- [ ] Relative date display works (Today, Tomorrow, X days from now)

### Recurring Tasks (Approved Expansion)

- [ ] User can set recurrence pattern (None, Daily, Weekly, Monthly)
- [ ] Completed recurring task creates next occurrence
- [ ] Recurrence badge displays in list view
- [ ] New occurrence has correct due date based on pattern
- [ ] Can edit/delete recurrence after task is created

---

## Non-Functional Requirements

- **Performance**: Task list renders in <500ms with 100+ tasks
- **Accessibility**: WCAG 2.1 Level AA
- **Browser Support**: Chrome 90+, Firefox 88+, Safari 14+
- **Data**: In-memory; persists only during session

---

## Development Timeline

| Phase | Scope | Effort | Duration |
|-------|-------|--------|----------|
| Phase 1: Core | 4 features | 5-6 days | Week 1 |
| Phase 2: Due Dates | Approved expansion 1 | 2-3 days | Week 2 early |
| Phase 3: Recurring | Approved expansion 2 | 3-4 days | Week 2 late |
| Phase 4: QA & Polish | Testing, bug fixes | 2-3 days | Week 3 early |

**Total Timeline**: 12-16 days from start to release-ready

---

## Machine-Readable Handoff

```yaml
artifact_id: prd
schema_version: 1
source_intent_ref: ../../00-user-intent.md
user_goal_preserved_as: core_with_expansion
scope_expansion_proposed: true
scope_expansion_requires_approval: true
scope_expansion_status: approved_by_user
scope_expansion_approvals:
  - feature: task_due_dates
    status: approved
    approved_by: user
    approved_at: "2026-05-19T18:30:00Z"
  - feature: recurring_tasks
    status: approved
    approved_by: user
    approved_at: "2026-05-19T18:30:00Z"
core_features_count: 4
expansion_features_count: 2
total_features_count: 6
estimated_timeline_days: 12-16
created_at: "2026-05-19T18:45:00Z"
```

---

## What Happens Next

1. **to-issues** generates stories for core features (4) + approved expansions (2) = 6 core stories
2. **triage** prioritizes stories:
   - Phase 1: Core features (highest priority, unblocks others)
   - Phase 2: Due Dates (moderate priority, commonly requested)
   - Phase 3: Recurring Tasks (moderate priority, commonly requested)
3. **tdd** begins development with story 1 (Task Creation)
4. Each story includes acceptance criteria from this PRD
5. Release plan reflects 12-16 day timeline (assuming available capacity)
