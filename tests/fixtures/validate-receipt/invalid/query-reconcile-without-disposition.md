---
validator_case: negative
expected_error_contains: RECEIPT_MODE_EVIDENCE
---
artifact_id: semantic_query_receipt
schema_version: 1
session_ref: 2026-10-24-fixture-owner-stop
state: final
created_at: '2026-10-24T09:05:00Z'
updated_at: '2026-10-24T09:10:00Z'
target_repository: example/app
modes:
- RECALL
- RECONCILE
decision: Which component owns the legacy export endpoint.
cli_identity:
  sensemaking_source_ref: null
  invocation_prefix: sensemaking-skills
  version_output: null
index:
  indexed_ref: '1111111111111111111111111111111111111111'
  current_head: '1111111111111111111111111111111111111111'
  worktree_clean: true
  uncommitted_changes_not_indexed: false
queries:
- id: QY-1
  operation: search
  terms:
  - export endpoint
  subject: null
  expect_kinds: []
  target_ref: '1111111111111111111111111111111111111111'
  result:
    hit_count: 1
    claim_ids:
    - cap:export
    truncated: false
    not_assessed_kinds: []
  outcome: HIT
  decision_relevant: true
- id: QY-2
  operation: explain
  terms: []
  subject: cap:export
  expect_kinds:
  - component
  target_ref: '1111111111111111111111111111111111111111'
  result:
    hit_count: 1
    claim_ids:
    - cap:export
    truncated: false
    not_assessed_kinds:
    - component
  outcome: NOT_ASSESSED
  decision_relevant: true
source_checks:
- claim_id: cap:export
  sources:
  - docs/api.md:10-20
  result: SUPPORTED
misses:
- id: M-1
  query_ref: QY-2
  needed_for: Owning component of the export capability.
  kind: NOT_ASSESSED
  resolved_by: 'Source inspection: src/export/router.py:1-40'
  follow_up: DEFERRED
  proposal_ref: null
reconcile: []
persistence: committed
action_authorized: false
semantic_truth_established: false
immutable: true
