---
validator_case: negative
expected_error_contains: EXPANSION_WITHOUT_APPROVAL
---
# Invalid PRD: expansion without approval

## 1. Executive Summary
Expansion proposed but requires_approval is false.

## 2. User Goal
Build a dashboard.

## 3. Goal Preservation and Expansion
Core with expansion.

## 4. Features
- Charts
- Reports (expansion)

## 5. Out of Scope
Notifications.

## 6. Acceptance Criteria
- Charts render

## 7. Non-Functional Requirements
- Fast

## 8. Machine-Readable Handoff
```yaml
source_intent_ref: ../../00-user-intent.md
user_goal_preserved_as: core_with_expansion
scope_expansion_proposed: true
scope_expansion_requires_approval: false
```
