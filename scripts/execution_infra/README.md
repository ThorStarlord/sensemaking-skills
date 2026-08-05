# scripts/execution_infra — governed campaign execution (Phase 6 correction)

**Approach B.** The first Phase 6 attempt treated the production verifier,
provider adapter, and runner as "external infrastructure" versioned
separately from the campaign configuration, with digests recorded only
*after* execution. An independent exact-head review (PR #129,
`PR_129_REQUEST_CHANGES`) showed that was wrong: those modules decide the
prompt, the provider, target access, tools, settings, the validator, and
output interpretation — every one of them an execution-relevant input.
Per ADR 0023 §5, a configuration is *the frozen, hashable set of every
execution-relevant input*; recording a digest after the run is
auditability, not prior human authorization.

The correction moves the real execution path INTO the pinned framework:

| Concern | Resolution |
|---|---|
| Provider call gated | `campaign_accounting.permit.ProviderPermit` — a one-shot, registry-backed permit issued by the Phase 4 durable boundary **after** the durable `INVOKED` transition and consumed atomically before provider entry. `exploratory_execution.ClaudeProvider.__call__` refuses — **before importing `claude_agent_sdk`** — any call without a genuine, consumed, attempt-bound permit. |
| Approval provenance | `exploratory_execution.ProductionSignedCommitVerifier` binds: trusted repository (normalized origin), governed protected branch (`refs/remotes/origin/main`), `git verify-commit`, signer fingerprint registered in the **framework-governed** approver registry (`approver-registry.yaml`, part of the pinned tree) mapped to `claimed_approver_identity`, the signed commit's `approval.yaml` blob byte-identical to the operative approval, and signed-document `campaign_id`/`policy_digest`/identity/statement agreement. |
| Configuration binding | The runner constructs the verifier, provider, and validator from the pinned framework + validated configuration; the real campaign **rejects any injected component**. `ClaudeProvider` additionally verifies its own model/target/SHA/framework/artifact against the invocation context at call time. |
| Target integrity | `exploratory_execution.TargetCheckout` materializes the approved repository at the exact SHA, verified origin, clean index/worktree, no untracked files, no submodules; re-verified before every attempt; the provider's `cwd` is the target checkout. |
| Filesystem contract | The provider has **no Write tool** (Read/Glob/Grep only), no ambient settings (`setting_sources=[]`), performs no artifact persistence, and creates no output paths. It returns `ProviderResponse(raw bytes, tokens, cost)`; the Phase 4 recorder preserves the raw request, raw output, artifact, and validation result. |
| Framework drift | `framework_tree_unchanged` proves the checkout is byte-identical to the pin across committed tree, index, working tree, AND untracked files — full tree, no path carve-out, checked pre-run and after every attempt. |
| Lifecycle | Clock re-read before every attempt; window re-checked per attempt; remaining slots derived from the ledger (resume-safe); mint failure after reservation → durable `ABORTED_BEFORE_INVOCATION` + stop. |
| Report | `build_execution_report` emits every Issue #122 field: authorized/reserved/invocation counts, every attempt ID and state, structural and substantive pass rates (pinned validator classification), failure categories, interrupted/aborted attempts, drift status, cost/token totals, per-attempt artifact paths, no-omission statement, and `EXPLORATORY_NOT_CANONICAL_EVIDENCE`. |

## Files

- `runner.py` — `GovernedCampaignRunner` (thin orchestrator) +
  `build_execution_report`. Refuses the real campaign on any injected
  component, any unpinned/unclean framework checkout, any unverified
  target, a closed window, or a missing approval file.
- The execution machinery itself lives in
  `src/sensemaking_skills/exploratory_execution/` and is bound by
  `framework_sha` (a normative configuration field and a policy allowlist
  member) **before** execution.

## Operational sequence

The approver registry ships inside the pinned framework tree, so every
registry change is a framework change: registering an approver produces a
NEW framework SHA, and the campaign package must be re-pinned to it
before any approval can bind. The correct order is therefore:

1. The human approver supplies their real OpenPGP fingerprint (never
   invented by an agent; e.g. `gpg --fingerprint <key-id>` on the machine
   holding the signing key).
2. A framework governance PR registers
   `fingerprint -> claimed_approver_identity` in
   `src/sensemaking_skills/exploratory_execution/approver-registry.yaml`,
   is independently reviewed at its exact head, and is merged. The merge
   produces a NEW framework SHA.
3. The campaign package is re-pinned to that new SHA in a separate
   preparation revision (new `configuration_id`, new `policy_digest`,
   refreshed `validity_window`), independently reviewed, and merged.
4. Only then does the human sign the operative `approval.yaml` against
   the new exact `policy_digest`: a signed commit on the governed
   protected ancestry whose signer fingerprint is the one registered in
   step 2, and whose `claimed_approver_identity` matches the registry
   mapping for that fingerprint.
5. An operator runs the campaign inside the new window:
   `GovernedCampaignRunner` with the real package, the pinned framework
   checkout, and the genuine `allowed_approver_identities`.
6. The complete execution report is delivered as a results PR and
   independently audited (Issue #122).

The registry cannot be updated "after pinning" and the old pin reused:
`framework_tree_unchanged` requires the execution checkout to be
byte-identical to the pin across the committed tree, index, working tree,
and untracked files, and any registry edit changes the tree. Registration
must precede the final repin; approval must follow it.

No human approval, no provider call, and no campaign reservation are
created by this repository's code, CI, or tests.
