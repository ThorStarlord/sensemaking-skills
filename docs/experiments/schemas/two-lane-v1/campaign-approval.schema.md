# Schema: Campaign Approval (v1)

The human governance act binding an exact `policy_digest` to a genuine
approval. See ADR 0023 §9b, §12. Physically separate from the campaign
policy document, mirroring the existing Evidence 0016 precedent of
separating `authorization-record.yaml` from `owner-approval.md`.

**This schema is not enforced by any runtime component in this phase. No
operative campaign approval may be created under Issue #117 — see the
`EXAMPLE_ONLY_NOT_AUTHORIZATION` marker requirement below.**

## Required fields

| Field | Type | Description |
|---|---|---|
| `approval_schema_version` | string | Must be `"1"`. |
| `campaign_id` | string | Must exactly match the `campaign_id` of the policy being approved. |
| `policy_digest` | string (sha256 hex) | Must exactly match the policy document's `policy_digest`. An approval whose `policy_digest` does not match the current policy is invalid for that policy (ADR 0023 §9c). |
| `claimed_approver_identity` | string | The identity the approval asserts (e.g. a GitHub handle). This is a **claim**, per ADR 0023 §12 item 1 — not by itself proof. |
| `approval_provenance` | object{mechanism, reference[, repository, issue_number, comment_id, comment_body_sha256]} | §12 item 2. `mechanism` names how the claim could be corroborated (e.g. `signed_commit`, `github_issue_comment_approval`). `reference` points at the corroborating artifact (commit SHA, comment URL). Required; an approval with `mechanism: "none"` is a template, not an operative approval. The four additional fields are REQUIRED when `mechanism` is `github_issue_comment_approval` (Lane A beta, Model B — see ADR 0023 §21): `repository` (governed repo), `issue_number`, `comment_id`, and `comment_body_sha256` (sha256 hex of the exact comment body), and are absent/ignored for other mechanisms. |
| `approval_statement` | string | Explicit, first-person consent text authored by the approving human. Must not be inferred from silence, from a merge, or from repository write access (ADR 0023 §12 item 4). |
| `approved_at` | string (RFC3339) | |
| `status` | string | Conversation-approval profile only: must be exactly `approved`. |
| `approval_source` | string | Conversation-approval profile only: must be exactly `active_human_conversation` — the human's standalone `approve` in the active conversation is the authority; the receipt is agent-recorded and is not independent proof of identity. |
| `approval_text` | string | Conversation-approval profile only: must be exactly `approve`. |
| `maximum_attempts` | integer | Conversation-approval profile only: must not exceed the policy `max_attempt_slots`. |
| `concurrency` | integer | Conversation-approval profile only: must not exceed the policy `concurrency_ceiling`. |
| `automatic_merge` | string | Conversation-approval profile only: must be exactly `prohibited`, and the policy must prohibit automatic merge. |
| `external_provider_api_prohibited` | boolean | Conversation-approval profile only: must be exactly `true`, and the policy must declare `external_provider_api_prohibited: true`. |
| `classification` | string | Conversation-approval profile only: must equal the policy classification. |
| `reference` | string | Conversation-approval profile only: points at the conversation record (e.g. session/message id). Required. |
| `marker` | string | Must be exactly `EXAMPLE_ONLY_NOT_AUTHORIZATION` in every example or template shipped in this repository under `docs/experiments/schemas/`. An operative approval (outside this schema-contract directory) omits this field entirely; its presence marks a document as non-operative. |

## What this schema does NOT define

- Any mechanism for the coding agent to populate `claimed_approver_identity`,
  `approval_statement`, or `approved_at` on a human's behalf. Per ADR 0023
  §12, the agent may prepare a **blank template** (all four fields empty or
  a placeholder) but must never fill them in with real values. Under the
  Lane A beta amendment (ADR 0023 §21, Model B), trusted framework code MAY
  transcribe these fields from a verified human-authored GitHub approval
  comment (mechanical transcription, never agent-authored consent); the
  fields are still never authored by the agent.
- Any claim that `approval_provenance` is currently verified by running
  code. As of Phase 1, nothing in this repository checks
  `approval_provenance.reference`. That verification is explicitly deferred
  to Phase 3 (#119) — see ADR 0023 §12 item 3.

## Fail-closed rules

- `policy_digest` mismatch against the referenced policy: the approval does
  not authorize that policy.
- Missing `approval_provenance.reference`: invalid, non-operative.
- `approval_statement` empty or absent: invalid, non-operative.
- Unknown `approval_schema_version`: reject.

## Blank template (agent-preparable) — EXAMPLE_ONLY_NOT_AUTHORIZATION

```yaml
approval_schema_version: "1"
campaign_id: "EXP-0000-EXAMPLE"
policy_digest: "0000000000000000000000000000000000000000000000000000000000000000"
claimed_approver_identity: "<HUMAN-FILLS-IN-EXACT-GITHUB-HANDLE>"
approval_provenance:
  mechanism: "<HUMAN-FILLS-IN e.g. signed_commit | github_review_approval>"
  reference: "<HUMAN-FILLS-IN e.g. commit SHA or review URL>"
approval_statement: "<HUMAN-FILLS-IN first-person consent text>"
approved_at: "<HUMAN-FILLS-IN RFC3339 timestamp>"
marker: "EXAMPLE_ONLY_NOT_AUTHORIZATION"
```

## Illustrative filled example — EXAMPLE_ONLY_NOT_AUTHORIZATION

This is a non-operative illustration only, using unmistakable placeholder
values. It must never be treated as a real approval.

```yaml
approval_schema_version: "1"
campaign_id: "EXP-0000-EXAMPLE"
policy_digest: "0000000000000000000000000000000000000000000000000000000000000000"
claimed_approver_identity: "example-owner-handle"
approval_provenance:
  mechanism: "signed_commit"
  reference: "000000000000000000000000000000000000c0de"
approval_statement: "EXAMPLE ONLY. This illustrates the shape of a filled approval; it is not a real consent statement and authorizes nothing."
approved_at: "2026-01-01T00:00:00+00:00"
marker: "EXAMPLE_ONLY_NOT_AUTHORIZATION"
```

Both examples above are authored under the Two-Lane YAML Profile v1 (ADR
0023 §10b): every string-valued field, including `mechanism`, is quoted.
