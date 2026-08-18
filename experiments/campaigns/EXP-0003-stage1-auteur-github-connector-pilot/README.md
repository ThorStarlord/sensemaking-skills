# EXP-0003-stage1-auteur-github-connector-pilot — GitHub-durable preparation package

**STATUS: PREPARATION ONLY. NOT OPERATIVE. NOT APPROVED. NOT EXECUTED.**

This is the successor experiment defined by Issue #191 and the merged Phase-A control-plane contract. EXP-0003 does not reopen, retry, or reinterpret EXP-0002.

## Frozen identity

- Campaign: `EXP-0003-stage1-auteur-github-connector-pilot`
- Framework SHA: `5704a2614222cd1705e0bf7e5174d1418c5d6240` (merge of PR #192)
- Execution mode: `coding_agent_native`
- Execution surface / model identifier: `github_connector`
- Durability backend: `github_results_branch_v1`
- Validation backend: `github_actions_exact_head`
- Invocation boundary: `before_first_experiment_scoped_target_read`
- Target repository: `https://github.com/ThorStarlord/auteur.git`
- Target SHA: `0653defb05625f2fcde0ac32eac6e59ccf7eeb90`
- Artifact type: `repository_sensemaking_brief`
- Classification: `EXPLORATORY_NOT_CANONICAL_EVIDENCE`
- Attempt slots: 3
- Concurrency: 1
- External provider API: prohibited
- Target mutation: prohibited
- Fallback: prohibited
- Repair/hidden retry: prohibited
- Automatic merge: prohibited
- Validity window: `2026-08-18T12:00:00Z` through `2026-08-25T12:00:00Z`

The final `configuration_id` and `policy_digest` are produced by the repository's canonical digest implementation under GitHub Actions and must replace the preparation placeholders before this package is review-ready.

## GitHub-durable execution protocol

After this preparation package is validated and merged, the agent presents the complete frozen envelope in the active conversation. A new standalone human `approve` is required; earlier agreement to the research design or preparation does not count.

Only after that approval receipt is recorded and validated may execution begin. Execution then:

1. creates the isolated results branch and draft results PR before attempt 1;
2. writes valid empty campaign state;
3. commits `RESERVED` for the attempt before experiment-scoped target access;
4. commits `INVOKED` immediately before the first target read at the exact pinned SHA;
5. performs `repo-sensemaker` using connector reads only;
6. commits the raw/preserved artifact with `OUTPUT_CAPTURED`;
7. binds deterministic validation to that exact preserved head;
8. records `VALIDATION_PASSED` or `VALIDATION_FAILED` with the prior validated head and workflow run id;
9. repeats only if policy budget remains and no non-terminal attempt exists;
10. derives the aggregate report from the durable GitHub history and stops at the results-PR audit boundary.

GitHub history and repository-resident state are authoritative. No Windows host, Task Scheduler state, local campaign root, local process state, or executor-local log is authoritative for determining whether an attempt occurred.

## Approval boundary

`approval-template.md` deliberately contains placeholders and is non-operative. After this package is merged and the final exact envelope is presented, only a standalone `approve` in the active human conversation authorizes this exact campaign digest. The resulting `approval.md` is an audit receipt; the conversation is the human decision authority.

No current file in this directory is an operative approval. No results branch, reservation, invocation, attempt output, or aggregate report is created by preparation.

## Research success criterion

A replacement workspace must be able to reconstruct the complete campaign state from GitHub alone after any interruption. If two materially different invocation histories remain indistinguishable from GitHub, or machine-local evidence is required to resolve the state, the successor hypothesis is unsupported/inconclusive.

Stop marker: `EXP_0003_PREPARATION_ONLY_AWAITING_DIGEST_FREEZE`.
