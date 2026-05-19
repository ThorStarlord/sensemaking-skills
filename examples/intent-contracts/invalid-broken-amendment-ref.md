---
artifact_id: user_intent_amendment
schema_version: 1
amends_intent_ref: 01-user-intent.md
clarification_type: scope_expansion
requires_reroute: true
created_at: "2026-05-19T15:00:00Z"
created_by: user
---

## Clarification

This amendment has the wrong amends_intent_ref. It points to 01-user-intent.md instead of 00-user-intent.md.

This should fail validation because amendments must always reference the original immutable intent artifact at 00-user-intent.md.
