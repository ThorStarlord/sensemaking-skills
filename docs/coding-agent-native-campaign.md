# Coding-Agent-Native Campaign Execution

**Status:** operator/agent reference for the `coding-agent-native-campaign` Skill
**Source of truth:** `skills/coding-agent-native-campaign/SKILL.md` (the Skill
text is executable guidance; this page is its human-oriented summary)
**Implementation:** `scripts/execution_infra/agent_native_campaign.py`,
`src/sensemaking_skills/exploratory_execution/conversation_approval.py`
**Related:** ADR 0013 (agent-native orchestration), ADR 0023 (two-lane
experiment authorization), `scripts/execution_infra/README.md`

## Purpose

Run an approved `coding_agent_native` experiment campaign where:

- the human authorizes it by replying with a standalone `approve` in the
  conversation;
- the coding agent itself performs every repository operation (no external
  model/provider API);
- an `approval.md` receipt records exactly what was approved;
- deterministic bookkeeping commands reserve, preserve, validate, and record
  each attempt.

Every result is `EXPLORATORY_NOT_CANONICAL_EVIDENCE`. It is not canonical
qualification evidence.

## Authority model

```text
approve (human, in conversation)   = the decision
approval.md                        = agent-written receipt of that decision
validate-approval                  = mechanical check of receipt vs envelope
execution window                   = separate mechanical gate
```

`approval.md` is **not** independent proof of human identity. The conversation
is the source of authority; the runtime only checks that the receipt matches
the exact campaign envelope before every step.

## Approval rules

A standalone `approve` authorizes the single campaign most recently presented
in the active conversation, if its digest is unchanged. The agent must refuse
to record approval, and execute nothing, when:

- more than one campaign is pending, or none was presented;
- the campaign changed after presentation;
- the policy digest cannot be resolved;
- `approve` appears inside a quotation, example, or hypothetical;
- the campaign has expired.

The refusal message is: `Approval is ambiguous: there are multiple or no
pending campaigns.`

Approval and the execution window are separate gates. `approved_at` may
precede `validity_window.not_before`, must not be in the future, and must not
exceed `validity_window.not_after`. `prepare` refuses until the window opens;
that refusal is the mechanical gate, not an error.

## Required policy fields

```yaml
execution_mode: "coding_agent_native"
execution_surface: "current_coding_agent"
external_provider_api_prohibited: true
allowed_models: []
```

## Receipt reference forms

Use exactly one:

| Form | When | `reference_kind` |
| --- | --- | --- |
| Legacy conversation pointer | Surface exposes a real `<session-id>#<message-id>` | omitted |
| Connector-native GitHub audit event | Platform IDs unavailable, GitHub writable | `agent_recorded_github_issue_comment` |

For the GitHub form the verifier accepts only a concrete
`https://github.com/<owner>/<repo>/issues/<n>#issuecomment-<id>` permalink with
the explicit `reference_kind`. It does not fetch the comment and does not
treat it as identity proof. Never fabricate a platform identifier to satisfy
the schema. The Skill contains the full receipt template.

## Command sequence

All commands run `python scripts/execution_infra/agent_native_campaign.py <cmd>`.

| Command | Purpose |
| --- | --- |
| `validate-approval` | Validate the receipt against the envelope; window-independent; no reservation or invocation. |
| `prepare` | Reserve an attempt, freeze instructions, record `INVOKED`. Refuses before the window opens. |
| `finalize` | Re-validate receipt and window, preserve raw output and artifact, validate, record terminal state. |
| `report` | Render the complete ledger-derived report (`--report-only` to skip other work). |

Common arguments: `--package-dir`, `--campaign-root`, `--framework-checkout`,
`--target-checkout-root`, `--allowed-approver`. `finalize` also takes
`--attempt-id` and `--artifact`.

Flow: present envelope -> human `approve` -> write `approval.md` ->
`validate-approval` -> (window opens) -> `prepare` -> agent performs
`repo-sensemaker` against the read-only target -> `finalize` -> repeat until
the ledger budget is exhausted -> `report` -> one results PR, stopping at
independent audit.

## Hard rules

- Never call an external model/provider API.
- Never fabricate an approval or a platform identifier.
- Never describe an agent-authored audit comment as human consent.
- Never modify the target checkout (read-only).
- Never hide, retry, or repair an attempt; failed, validation-failed, and
  interrupted attempts are recorded and reported identically.
- Never push to `main` or merge the results PR yourself.
- On any `REFUSED: ...`, record it and stop; do not edit policy, receipt, or
  ledger to bypass it.

## Where it has been used

Campaign packages live under `experiments/campaigns/` (for example
`EXP-0002-stage1-auteur-coding-agent-pilot`). See `experiments/README.md`.
