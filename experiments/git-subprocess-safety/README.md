# Git subprocess safety: configured helpers run while Sensemaking reads a checkout

**Question.** Can Sensemaking's Git subprocesses, when they read or index a checkout, run programs configured in that checkout's own Git configuration (`core.fsmonitor`, clean, smudge or process filters, textconv, external diff, hooks)?

**Trigger.** PR #877's security review, which asked for the mechanism to be tested rather than assumed.

**Answer.** Yes, in several reachable operations. The protected path (`worktree_context.inspect_worktree_context`) already disabled these, and two existing tests cover it. Other read paths did not. This folder records the reproduction, the repair, and what remains.

## Scope and trust assumption

The threat is a checkout whose `.git/config` or `.git/hooks` were supplied by someone else, for example an extracted archive or a shared folder. A `git clone` does not transfer a remote's local configuration, so a remote alone cannot plant these settings. Global and system configuration are treated as trusted. The repository's own `.gitattributes` names a filter, but the program it runs must be defined in configuration.

## Capability map (raw Git, negative control)

`results/neg_control.json`, from `harness/neg_control.py`. Each raw operation was run on a fresh canary repository.

| Raw operation | Canaries fired |
| --- | --- |
| `status --porcelain` | clean, fsmonitor |
| `ls-files -z` | fsmonitor |
| `ls-files --others` | fsmonitor |
| `diff --name-only` (worktree) | clean, fsmonitor |
| `diff -p` (two commits) | extdiff, smudge |
| `log -p -1` | smudge, textconv |
| `show HEAD:file` | none |
| `cat-file -p` | none |
| `check-attr` | fsmonitor |
| `rev-parse HEAD` | none |
| `worktree add --detach` | fsmonitor, post-checkout, smudge |

## Sensemaking operations, before and after the repair

`results/sm_results_before_repair.json` and `results/sm_results_after_repair.json`, from `harness/sm_tests.py`. Each row ran the real CLI on a fresh canary repository.

| Operation | Before | After |
| --- | --- | --- |
| `knowledge-build` (active checkout) | fsmonitor | none |
| `knowledge-build --temporary-checkout` (filter-attributed repo) | fsmonitor (then refused) | none (then refused) |
| `knowledge-build --temporary-checkout` (no filter attributes) | fsmonitor | none |
| `knowledge-audit --temporary-checkout` | fsmonitor | none |
| `knowledge-query --repo` | none | none |
| `impact-preview` | clean, fsmonitor | none |
| `knowledge-proposal-check` | clean, fsmonitor | none |
| `release audit` | clean, fsmonitor | none |

Exit codes were the same before and after for every row. On a clean fixture, the successful outputs are identical before and after: the build digest (`e384ee60…`), the impact payload, and the release payload.

## The repair

- `worktree_context.guarded_git_text` is the existing protection (fsmonitor disabled and every configured clean, smudge or process filter disabled by name), exposed as a helper.
- `impact.py`, `stewardship_validation.py` and `release_authority.py` route their status, diff and ls-files calls through it.
- `knowledge_sources.py` adds `-c core.fsmonitor=false` to its `_git` helper and to the two calls in `_filtered_paths`. `ls-files` and `check-attr` do not run filters, so only fsmonitor needed disabling there.

Git's built-in text and end-of-line conversion is not an external filter driver. It is not disabled. A CRLF worktree over an LF blob reports the same result through the guarded helper as through raw Git.

## Measured trade-off (behaviour change)

For a file whose stored form is produced by a transforming filter (the git-lfs pattern), the guarded helper reports the file as modified, because it compares raw worktree bytes with the stored form. The repository's own filter would report it clean. Measured: raw Git and the old helper report clean; the guarded helper reports `M`.

Affected callers: `impact-preview`, `knowledge-proposal-check` and `release audit`. They now fail closed on such repositories. This matches the existing behaviour of `knowledge-build`. The Sensemaking repository itself defines no `filter=` attributes, so its own release audit is unaffected.

## Campaign target snapshot: partly closed, one decision remains

`campaigns/target_snapshot.py` runs `git status` on target repositories. Before the repair it fired the target's fsmonitor, its `post-index-change` hook and its clean filter (`results/`, round-two probe). The repair disables fsmonitor and optional index locks for its calls (`GIT_OPTIONAL_LOCKS=0` also stops the index write that runs `post-index-change`). After the repair only the clean filter fires.

Disabling clean and smudge filters here is **not** done, because the snapshot's status output is part of a commit-pinned identity digest (`_worktree_digest`). Disabling them would change identities for targets with transforming filters. That is an identity-semantics decision for the owner.

Identity preservation, measured: the same repository, snapshotted by the old and the new code, gives identical values for every field, including `worktree_sha256`, on a dirty repository (no filter attributes).

## Round two: review findings and their repair

An independent review of the first repair found two blockers and one undisclosed behaviour change:

1. **Filter names containing `=`.** `-c name=` is split at its first `=`, so a driver named `a=b` disabled the wrong key. Measured before the fix: the guard let `clean` run through status and through the temporary build. The fix refuses such configuration in `_configured_external_filters`. After the fix a canary repository with a driver named `a=b` produces no canary firing, and both the guarded status and the temporary build refuse with an explicit error.
2. **Campaign target snapshot.** Addressed as described above.
3. **Required filters and transforming filters.** Documented in `guarded_git_text`. The guarded error now includes Git's own reason (for example `clean filter 'r' failed`), which was dropped before.

**Harness defect found and fixed during round two.** `sm_tests.py` in the repository had computed its source path one directory too high. Its import silently fell back to an installed package, so a run appeared to succeed on the wrong code. The path is corrected, and the harness now asserts that the source tree exists. The results in `results/sm_results_after_repair.json` were produced by this corrected harness against the worktree's `src`.

## Not exercised

- `exploratory_execution/execution_identity.py` and `target_checkout.py` run unguarded `status`. Reviewed by source only.
- `workspace_knowledge.py` diffs two commits, which reads no worktree, and passes `--no-textconv --no-ext-diff`. Reviewed by source only.
- `strategy_cli.py` and `stewardship_validation._head_pack` run `git show rev:path`. The raw control showed `show` fires nothing.

## Verification and policy

- Canary reproduction before and after the repair, and the raw negative control, are above.
- Repository policy for construction PRs forbids adding or running unit tests locally. The existing suite, including the two worktree-context protection tests, runs in CI.
- No global or system Git configuration was changed. Canary repositories were created under the session scratch directory, never inside the repository.

## Reproduce

```bash
GITSAFETY_SCRATCH=/path/to/scratch python experiments/git-subprocess-safety/harness/neg_control.py
GITSAFETY_SCRATCH=/path/to/scratch python experiments/git-subprocess-safety/harness/sm_tests.py
```

`sm_tests.py` runs the worktree's `src` (three levels above the harness, at the worktree root) and asserts that it exists. To reproduce the "before" column, export `origin/main`'s `src` into a separate tree (for example with `git archive`) and point `SRC` at it.
