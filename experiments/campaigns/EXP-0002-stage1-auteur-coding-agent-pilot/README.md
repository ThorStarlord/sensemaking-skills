# EXP-0002-stage1-auteur-coding-agent-pilot — coding-agent-native preparation package

**STATUS: PREPARATION ONLY. NOT OPERATIVE. NOT APPROVED. NOT EXECUTED.**

This directory is a *proposal package* for the first coding-agent-native
exploratory campaign (ADR 0023 section 21e, Issue #116/#122): the coding
agent itself performs `repo-sensemaker` against Auteur — no external
model/provider API is used at any point.

## Pinned values

| Input | Value |
|---|---|
| `campaign_id` | `EXP-0002-stage1-auteur-coding-agent-pilot` |
| Framework repository | `ThorStarlord/sensemaking-skills` |
| Framework SHA | `805b7ee285c7520ae3ca9dd5538138275b9abe64` |
| `execution_mode` | `coding_agent_native` |
| `execution_surface` | `current_coding_agent` |
| `external_provider_api_prohibited` | `true` (zero external API cost by construction) |
| Target repository | `ThorStarlord/auteur` (`https://github.com/ThorStarlord/auteur.git`) |
| Target SHA | `0653defb05625f2fcde0ac32eac6e59ccf7eeb90` |
| Model / surface identifier | `current_coding_agent` (no external model; `allowed_models: []`) |
| Artifact type | `repository_sensemaking_brief` |
| Configurations | exactly 1 (see `configuration-identity.yaml`) |
| `configuration_id` | `da6f8538515854c4c30f1595f401065c2e203646ce4e1c0899e676649735d14a` |
| Attempts | 3 (`max_attempt_slots=3`, `max_attempts_per_configuration=3`) |
| Concurrency | 1 (serialized attempts; an active attempt holds the slot) |
| Classification | `EXPLORATORY_NOT_CANONICAL_EVIDENCE` |
| Prohibitions | fallback, hidden retry, target mutation, automatic repair, automatic merge, external provider API |
| `policy_digest` | `267fc060d20eed0f1e7f627e0e940e35de1ac3b085509637f4d3087a7f9a0908` (see `campaign-policy.sha256`) |
| Validity window | `2026-08-18T00:00:00Z` .. `2026-08-25T00:00:00Z` |

`cost_ceiling`/`token_ceiling` are `null`: with
`external_provider_api_prohibited: true` and `allowed_models: []` there is
no external spend surface, so the external cost is zero **by
construction** (a numeric ceiling of `0` would block every reservation
under the `>=` enforcement check and is therefore not used).

## Execution protocol

The campaign runs through the two-phase bookkeeping protocol in
`scripts/execution_infra/agent_native_campaign.py` (prepare / finalize /
report) orchestrated by the `coding-agent-native-campaign` skill: the
coding agent reads the frozen attempt instructions, performs
`repo-sensemaker` against the read-only target checkout at the pinned
SHA, delivers the brief, and finalize validates and records it. Every
attempt is durably reserved, INVOKED, preserved, and reported; the
provider-loop runner refuses this campaign.

## Approval protocol (conversation)

The campaign uses the conversation approval (ADR 0023 section 21e, Issue
#116): a standalone `approve` from the human in the active conversation
authorizes this exact `policy_digest`. The agent records the decision in
`approval.md` (see `approval-template.md` for the exact receipt
contract); the conversation is the authority, and the file is an audit
receipt, not independent proof of identity. No GitHub comment, capture
script, API token, or live revalidation is involved.

1. This preparation PR is reviewed and merged (the merged
   `policy_digest` above is the digest the human must approve).
2. The agent presents the full envelope in the conversation (campaign
   id, digest, limits, prohibitions, window); there must be exactly one
   pending campaign with an unchanged digest.
3. The human replies with a standalone `approve`. Nothing else counts
   (a reaction, a merge, silence, or `approve` inside a question or
   quote does not).
4. The agent writes `approval.md` in this directory with the exact
   receipt contract.
5. `prepare`/`finalize` validate the receipt against the exact campaign
   id, policy digest, attempt limit, concurrency, no-auto-merge rule,
   external-provider prohibition, classification, and window before
   every step.
6. Only then may the campaign execute -- and execution is a separate,
   future task.

## What this package contains

No human approval, no operative `approval.md`, no reservation, no
ledger, no attempt output, no provider call, and no external API cost.
It cannot produce any of those through the normal runtime until the
human's standalone `approve` is recorded as the operative `approval.md`
binding the exact `policy_digest` above.

## Verification

- Policy and configuration validate with the real Phase 2 validators;
  both digests match; the configuration is authorized conjunctively by
  the policy.
- `tests/campaign_preparation/test_exp0002_package.py` proves package
  coherence, digest correctness, approval absence, drift resistance, and
  no execution residue.

Stop marker for preparation: `EXP_0002_PREPARATION_PR_READY_FOR_REVIEW` —
the package is ready to inspect, not ready to run.
