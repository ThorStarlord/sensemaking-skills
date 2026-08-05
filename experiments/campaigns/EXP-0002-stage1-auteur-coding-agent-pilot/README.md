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
| Framework SHA | `253efe56d08f3e5c9a051bbba78efeaa606a6928` |
| `execution_mode` | `coding_agent_native` |
| `execution_surface` | `current_coding_agent` |
| `external_provider_api_prohibited` | `true` (zero external API cost by construction) |
| Target repository | `ThorStarlord/auteur` (`https://github.com/ThorStarlord/auteur.git`) |
| Target SHA | `0653defb05625f2fcde0ac32eac6e59ccf7eeb90` |
| Model / surface identifier | `current_coding_agent` (no external model; `allowed_models: []`) |
| Artifact type | `repository_sensemaking_brief` |
| Configurations | exactly 1 (see `configuration-identity.yaml`) |
| `configuration_id` | `f354644e6dcfbf93a85ba309518ad0e9b8da4f6771a31fd11a8a15af166d167b` |
| Attempts | 3 (`max_attempt_slots=3`, `max_attempts_per_configuration=3`) |
| Concurrency | 1 (serialized attempts; an active attempt holds the slot) |
| Classification | `EXPLORATORY_NOT_CANONICAL_EVIDENCE` |
| Prohibitions | fallback, hidden retry, target mutation, automatic repair, automatic merge, external provider API |
| `policy_digest` | `7121fa308899d02ca7365029bdd3d606744c4f00f8e58c762b64718d014b6290` (see `campaign-policy.sha256`) |
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

## What this package contains

No human approval, no operative `approval.yaml`, no reservation, no
ledger, no attempt output, no provider call, and no external API cost.
It cannot produce any of those through the normal runtime until a
genuine human approval comment exists for the exact `policy_digest`
above (post the comment on the campaign's GitHub issue; the agent never
posts it).

## Verification

- Policy and configuration validate with the real Phase 2 validators;
  both digests match; the configuration is authorized conjunctively by
  the policy.
- `tests/campaign_preparation/test_exp0002_package.py` proves package
  coherence, digest correctness, approval absence, drift resistance, and
  no execution residue.

Stop marker for preparation: `EXP_0002_PREPARATION_PR_READY_FOR_REVIEW` —
the package is ready to inspect, not ready to run.
