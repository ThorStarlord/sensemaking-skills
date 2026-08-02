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
| `approval_provenance` | object{mechanism, reference} | §12 item 2. `mechanism` names how the claim could be corroborated (e.g. `signed_commit`, `github_review_approval`). `reference` points at the corroborating artifact (commit SHA, review URL/id). Required; an approval with `mechanism: "none"` is a template, not an operative approval. |
| `approval_statement` | string | Explicit, first-person consent text authored by the approving human. Must not be inferred from silence, from a merge, or from repository write access (ADR 0023 §12 item 4). |
| `approved_at` | string (RFC3339) | |
| `marker` | string | Must be exactly `EXAMPLE_ONLY_NOT_AUTHORIZATION` in every example or template shipped in this repository under `docs/experiments/schemas/`. An operative approval (outside this schema-contract directory) omits this field entirely; its presence marks a document as non-operative. |

## What this schema does NOT define

- Any mechanism for the coding agent to populate `claimed_approver_identity`,
  `approval_statement`, or `approved_at` on a human's behalf. Per ADR 0023
  §12, the agent may prepare a **blank template** (all four fields empty or
  a placeholder) but must never fill them in with real values.
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
campaign_id: EXP-0000-EXAMPLE
policy_digest: "0000000000000000000000000000000000000000000000000000000000000000"
claimed_approver_identity: "<HUMAN-FILLS-IN-EXACT-GITHUB-HANDLE>"
approval_provenance:
  mechanism: "<HUMAN-FILLS-IN e.g. signed_commit | github_review_approval>"
  reference: "<HUMAN-FILLS-IN e.g. commit SHA or review URL>"
approval_statement: "<HUMAN-FILLS-IN first-person consent text>"
approved_at: "<HUMAN-FILLS-IN RFC3339 timestamp>"
marker: EXAMPLE_ONLY_NOT_AUTHORIZATION
```

## Illustrative filled example — EXAMPLE_ONLY_NOT_AUTHORIZATION

This is a non-operative illustration only, using unmistakable placeholder
values. It must never be treated as a real approval.

```yaml
approval_schema_version: "1"
campaign_id: EXP-0000-EXAMPLE
policy_digest: "0000000000000000000000000000000000000000000000000000000000000000"
claimed_approver_identity: "example-owner-handle"
approval_provenance:
  mechanism: signed_commit
  reference: "0000000000000000000000000000000000c0de"
approval_statement: "EXAMPLE ONLY. This illustrates the shape of a filled approval; it is not a real consent statement and authorizes nothing."
approved_at: "2026-01-01T00:00:00+00:00"
marker: EXAMPLE_ONLY_NOT_AUTHORIZATION
```
