# EXP-0005-stage1-auteur-github-connector-pilot — GitHub-durable preparation package

**STATUS: PREPARATION ONLY. NOT OPERATIVE. NOT APPROVED. NOT EXECUTED.**

This fresh successor experiment is tracked by Issue #201 after the connector-native approval-reference framework correction in Issue #199 / PR #200. EXP-0005 does not repair, retry, reinterpret, or reuse EXP-0004. EXP-0003/EXP-0004 approvals and historical result artifacts are not transferable.

## Frozen identity

- Campaign: `EXP-0005-stage1-auteur-github-connector-pilot`
- Framework SHA: `c9cb29d467eee82d1d9cc4d4fb89a184c26f27e7` (merge of PR #200)
- Execution mode: `coding_agent_native`
- Execution surface / model identifier: `github_connector`
- Durability backend: `github_results_branch_v1`
- Validation backend: `github_actions_exact_head`
- Invocation boundary: `before_first_experiment_scoped_target_read`
- Target access mode: `github_connector_read_only`
- State-currency probe backend: `github_connector_exact_sha_v1`
- Approval reference kind: `agent_recorded_github_issue_comment`
- Approval audit repository: `ThorStarlord/sensemaking-skills`
- Approval audit tracking issue: `#201`
- Target repository: `https://github.com/ThorStarlord/auteur.git`
- Target SHA: `0653defb05625f2fcde0ac32eac6e59ccf7eeb90`
- Artifact type: `repository_sensemaking_brief`
- Configuration ID: `0000000000000000000000000000000000000000000000000000000000000000` (discovery placeholder; final preparation head must replace it)
- Policy digest: `0000000000000000000000000000000000000000000000000000000000000000` (discovery placeholder; final preparation head must replace it)
- Classification: `EXPLORATORY_NOT_CANONICAL_EVIDENCE`
- Attempt slots: 3
- Concurrency: 1
- External provider API: prohibited
- Target mutation: prohibited
- Fallback: prohibited
- Repair/hidden retry: prohibited
- Automatic merge: prohibited
- Validity window: `2026-08-18T19:00:00Z` through `2026-08-25T19:00:00Z`

The zero identities are deliberate preparation-time discovery placeholders only. GitHub Actions must first compute and freeze the canonical configuration ID; only after the real configuration identity is bound into policy may GitHub Actions compute and freeze the final policy digest. A head containing either zero placeholder is not releasable and may not be approved or executed.

## Connector-native approval contract

After this preparation package is validated and merged, the agent re-reads the complete frozen envelope from canonical `main` and presents it in the active conversation. A new standalone human `approve` is required; Issue #201, preparation work, merge authorization, `proceed`, and all EXP-0003/EXP-0004 approvals do not count.

After a valid standalone `approve`, and before an operative `approval.md` is written, the agent adds exactly one top-level comment to tracking Issue #201. That comment identifies itself as an **agent-recorded conversation approval event**, transcribes the exact campaign id, exact presented policy digest, `approval_text: approve`, and approval timestamp, and explicitly states that it is an agent-authored durable audit locator rather than independent human-authored consent. The connector-returned concrete issue-comment permalink is copied exactly into `approval.md` with `reference_kind: agent_recorded_github_issue_comment`.

The conversation is the authorization authority. The GitHub comment and `approval.md` are durable audit artifacts only. No platform session/message identifier may be inferred or fabricated.

## Connector-native state-currency contract

Every repository-content read during a future authorized attempt must be pinned to the exact target SHA and follow `skills/repo-sensemaker/references/connector-native-probe.md` at the frozen framework revision. Decision-changing evidence preserves path, GitHub-supplied blob identity, and relevant line range. Live GitHub metadata is labeled separately from the immutable snapshot. Local-only Probe Engine metrics remain explicitly unmeasured unless an independently authorized deterministic remote adapter actually computes them; they are never approximated from prose inspection.

## GitHub-durable execution protocol

Only after the approval audit event and receipt are recorded and validated may execution begin. Execution then:

1. creates the isolated EXP-0005 results branch and draft results PR before attempt 1;
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

## Preparation validation contract

Preparation tests must prove, without creating real approval state, that the exact intended connector-native receipt shape validates when it contains a concrete issue-comment permalink on Issue #201. They must also prove the shipped template remains non-operative and that the immutable preparation directory contains no operative approval, ledger, attempts, or results state.

## Research success criterion

A replacement workspace must be able to reconstruct the complete campaign state from GitHub alone after any interruption. If two materially different invocation histories remain indistinguishable from GitHub, if the approval audit event cannot be recorded truthfully, if machine-local evidence is required to resolve state, or if connector-only evidence requires fabricated measurements, the hypothesis is falsified or bounded inconclusive as the evidence warrants.

Stop marker: `EXP_0005_PREPARATION_PR_READY_FOR_REVIEW`.
