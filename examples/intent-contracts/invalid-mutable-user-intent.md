---
artifact_id: user_intent
schema_version: 1
intent_source: user_problem_statement
scope_mode: soft
raw_problem_statement: "We need to stabilize our authentication middleware"
immutable: false
created_at: "2026-05-19T14:30:00Z"
created_by: user
repo_state_used: main-branch-2026-05-19
constraints: []
non_goals: []
clarifications: []
---

## Raw Intent

User wants to improve authentication. This artifact has immutable: false, which violates the immutability contract.

This fixture should be rejected by validate-user-intent.py because intent artifacts must have immutable: true.
