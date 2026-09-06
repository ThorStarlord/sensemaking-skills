---
approval_schema_version: "1"
status: "<STATUS>"
campaign_id: "EXP-0006-empirical-skill-qualification-diagnostic"
policy_digest: "<PRESENTED_DIGEST>"
approval_source: "active_human_conversation"
approval_text: "approve"
approved_at: "<APPROVED_AT>"
maximum_attempts: 3
concurrency: 1
automatic_merge: "prohibited"
external_provider_api_prohibited: true
classification: "EXPLORATORY_NOT_CANONICAL_EVIDENCE"
reference_kind: "<REFERENCE_KIND>"
reference: "<AUDIT_REFERENCE>"
---
Template only. `status`, digest, timestamp, reference kind, and reference remain placeholders. It cannot become operative until the exact frozen EXP-0006 envelope has passed preparation validation, is presented in the active conversation, and the human replies with a new standalone `approve`. After that decision, the connector-native path records exactly one agent-authored approval event on tracking Issue #274 and copies the concrete returned `#issuecomment-...` permalink into `approval.md`. The GitHub comment is an audit locator, not independent human-authored consent. Agreement to the research plan, `proceed`, PR review, or any prior campaign approval is not reusable authorization.
