# EXP-0004-stage1-auteur-github-connector-pilot — GitHub-durable preparation package

**STATUS: PREPARATION ONLY. NOT OPERATIVE. NOT APPROVED. NOT EXECUTED.**

This is the successor experiment tracked by Issue #197 after the connector-native framework corrections in Issue #195 / PR #196. EXP-0004 does not repair, retry, reinterpret, or reuse EXP-0003. EXP-0003 approval and historical results PR #194 are not transferable.

## Frozen identity

- Campaign: `EXP-0004-stage1-auteur-github-connector-pilot`
- Framework SHA: `15763f036a1434387d77076b0fad3f5a796241ce` (merge of PR #196)
- Execution mode: `coding_agent_native`
- Execution surface / model identifier: `github_connector`
- Durability backend: `github_results_branch_v1`
- Validation backend: `github_actions_exact_head`
- Invocation boundary: `before_first_experiment_scoped_target_read`
- Target access mode: `github_connector_read_only`
- State-currency probe backend: `github_connector_exact_sha_v1`
- Target repository: `https://github.com/ThorStarlord/auteur.git`
- Target SHA: `0653defb05625f2fcde0ac32eac6e59ccf7eeb90`
- Artifact type: `repository_sensemaking_brief`
- Configuration ID: `0000000000000000000000000000000000000000000000000000000000000000` (preparation placeholder until canonical GitHub Actions discovery)
- Policy digest: `0000000000000000000000000000000000000000000000000000000000000000` (preparation placeholder until canonical GitHub Actions discovery)
- Classification: `EXPLORATORY_NOT_CANONICAL_EVIDENCE`
- Attempt slots: 3
- Concurrency: 1
- External provider API: prohibited
- Target mutation: prohibited
- Fallback: prohibited
- Repair/hidden retry: prohibited
- Automatic merge: prohibited
- Validity window: `2026-08-18T16:00:00Z` through `2026-08-25T16:00:00Z`

The final configuration ID and policy digest must be produced by the repository's canonical digest implementation in GitHub Actions, not computed in chat or on an executor host. The policy digest is frozen only after it binds the final configuration ID.

## Connector-native state-currency contract

Every repository-content read during a future authorized attempt must be pinned to the exact target SHA and follow `skills/repo-sensemaker/references/connector-native-probe.md` at the frozen framework revision. Decision-changing evidence preserves path, GitHub-supplied blob identity, and relevant line range. Live GitHub metadata is labeled separately from the immutable snapshot. Local-only Probe Engine metrics remain explicitly unmeasured unless an independently authorized deterministic remote adapter actually computes them; they are never approximated from prose inspection.

## GitHub-durable execution protocol

After this preparation package is validated and merged, the agent re-reads the complete frozen envelope from canonical `main` and presents it in the active conversation. A new standalone human `approve` is required; Issue #197, this preparation work, merge authorization, `proceed`, and EXP-0003 approval do not count.

Only after that approval receipt is recorded and validated may execution begin. Execution then:

1. creates the isolated EXP-0004 results branch and draft results PR before attempt 1;
2. writes the approval receipt and valid empty campaign state;
3. validates that exact approved/empty head before spending a slot;
4. commits `RESERVED` for the attempt before experiment-scoped target access;
5. commits `INVOKED` immediately before the first target read at the exact pinned SHA;
6. performs `repo-sensemaker` using `github_connector_exact_sha_v1` evidence only;
7. commits the raw/preserved artifact with `OUTPUT_CAPTURED`;
8. binds deterministic validation to that exact preserved head;
9. records `VALIDATION_PASSED` or `VALIDATION_FAILED` with the prior validated head and workflow run id;
10. repeats only if policy budget remains and no non-terminal attempt exists;
11. derives the aggregate report from durable GitHub history and stops at the results-PR audit boundary.

GitHub history and repository-resident state are authoritative. No Windows host, Task Scheduler state, local campaign root, local process state, or executor-local log is authoritative for determining whether an attempt occurred.

## Approval boundary

`approval-template.md` deliberately contains placeholders and is non-operative. After this package is merged and the final exact envelope is presented, only a new standalone `approve` in the active human conversation authorizes this exact campaign digest. The resulting future `approval.md` is an audit receipt; the conversation is the human decision authority.

No current file in this directory is an operative approval. No results branch, reservation, invocation, target read, attempt output, or aggregate report is created by preparation.

## Research success criterion

A replacement workspace must be able to reconstruct the complete campaign state from GitHub alone after any interruption. If two materially different invocation histories remain indistinguishable from GitHub, if machine-local evidence is required to resolve the state, or if connector-only evidence requires fabricated measurements, the hypothesis is unsupported/inconclusive.

Stop marker: `EXP_0004_PREPARATION_PR_READY_FOR_REVIEW`.
