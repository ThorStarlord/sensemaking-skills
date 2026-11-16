# Git subprocess safety: configured helpers run while Sensemaking reads a checkout

**Question.** Can Sensemaking's Git subprocesses, when they read or index a checkout, run programs configured in that checkout's own Git configuration (`core.fsmonitor`, clean, smudge or process filters, textconv, external diff, hooks)?

**Trigger.** PR #877's security review, which asked for the mechanism to be tested rather than assumed.

**Answer.** Yes, in several reachable operations on the pre-repair code. The protected path (`worktree_context.inspect_worktree_context`) already disabled fsmonitor and configured filters, and two existing tests cover it. Other read paths did not. The repair routes those paths through the same protection and refuses one configuration shape the protection could not disable safely. This folder records the reproduction, the repair, the measured behaviour changes, and what remains.

## Scope and trust assumption

The threat is a checkout whose `.git/config` or `.git/hooks` were supplied by someone else, for example an extracted archive or a shared folder. A `git clone` does not transfer a remote's local configuration, so a remote alone cannot plant these settings. Global and system configuration are treated as trusted. A repository's `.gitattributes` can name a filter, but the program it runs must be defined in configuration.

## Capability map (raw Git, negative control)

`results/neg_control.json`, from `harness/neg_control.py`. Each raw operation ran on a fresh canary repository.

| Raw operation | Canaries fired |
| --- | --- |
| `status --porcelain` | clean, fsmonitor, post-index-change |
| `ls-files -z` | fsmonitor |
| `ls-files --others` | fsmonitor |
| `diff --name-only` (worktree) | clean, fsmonitor, post-index-change |
| `diff -p` (two commits) | extdiff, smudge |
| `log -p -1` | smudge, textconv |
| `show HEAD:file` | none |
| `cat-file -p` | none |
| `check-attr` | fsmonitor |
| `rev-parse HEAD` | none |
| `worktree add --detach` | fsmonitor, post-checkout, post-index-change, smudge |

## Sensemaking operations, before and after the repair

`results/sm_results_before_repair.json` and `results/sm_results_after_repair.json`, from `harness/sm_tests.py`. Each row ran the real CLI on a fresh canary repository. The "before" run used `origin/main`'s source; the "after" run used the final worktree source.

| Operation | Before (canaries fired) | After |
| --- | --- | --- |
| `knowledge-build` (active checkout) | fsmonitor, post-index-change | none |
| `knowledge-build --temporary-checkout` (filter-attributed repo) | fsmonitor (then refused) | none (then refused) |
| `knowledge-build --temporary-checkout` (no filter attributes) | fsmonitor | none |
| `knowledge-audit --temporary-checkout` | fsmonitor, post-index-change | none |
| `knowledge-query --repo` | none | none |
| `impact-preview` | clean, fsmonitor, post-index-change | none |
| `knowledge-proposal-check` | clean, fsmonitor | none |
| `release audit` | clean, fsmonitor, post-index-change | none |

Exit codes are identical before and after for every row.

On a clean fixture, `results/clean_fixture_old_vs_final.json` records the build digest, the claim count, and sha256 digests of the impact and release payloads. All are identical between `origin/main` and the final source, with identical exit codes.

## The repair

- `worktree_context.guarded_git_text` is the existing protection, exposed as a helper. It disables fsmonitor, every configured clean, smudge or process filter (by name), and the repository's hooks (`core.hooksPath` set to the null device, because a diff against the worktree writes the index and runs `post-index-change`).
- `impact.py`, `stewardship_validation.py` and `release_authority.py` route their status, diff and ls-files calls through that helper.
- `knowledge_sources.py` adds `-c core.fsmonitor=false` to its `_git` helper and to the two calls in `_filtered_paths`. `ls-files` and `check-attr` run no filters, so only fsmonitor needed disabling there.
- `campaigns/target_snapshot.py` disables fsmonitor for its git calls and sets `GIT_OPTIONAL_LOCKS=0`. Clean and smudge filters are **not** disabled there (see below).
- A configured filter name containing `=` or a line break is refused. `-c name=` is split at its first `=`, so such a name would disable the wrong key.
- The guarded error includes Git's own reason. Before, it was dropped.
- The guard's timeout is 30 seconds (it was 20). `stewardship_validation` had 30 seconds before, and `release_authority` had no timeout.

Git's built-in text and end-of-line conversion is not an external filter driver, and it is not disabled. A CRLF worktree over an LF blob gives the same result through the guarded helper as through raw Git.

## Measured behaviour changes

1. **Transforming filters (the git-lfs pattern).** For a file whose stored form comes from a transforming filter, the guarded status compares raw worktree bytes with the stored form, so it reports the file modified. The repository's own filter reports it clean, and so does raw Git. `origin/main`'s `impact`, `stewardship_validation` and `release_authority` ran unguarded status, so they reported it clean. Measured on this repository: raw Git and `origin/main` report clean, and the guarded helper reports `M`. Affected callers: `impact-preview`, `knowledge-proposal-check` and `release audit`. They now fail closed on such repositories. `knowledge-build` already behaved this way, through `worktree_context`. This repository's tracked `.gitattributes` define no `filter=` attributes, so its own release audit is not affected.
2. **Required filters.** A driver marked `required` makes raw status fail, and it makes the guarded status fail too. Git's reason is now included in the error. This is a clearer message, not a new failure. `release_authority` still returns `None` on failure, as before.
3. **Filter names with `=`.** The refusal applies across every configuration scope, global and system included. One such name in the user's global configuration makes every guarded operation fail. This is fail-closed and rare. It is recorded as a known limitation, not changed here.
4. **Index writes.** Guarded status and diff no longer write `.git/index`, because the guard sets `GIT_OPTIONAL_LOCKS=0`. The campaign snapshot had written it before. On a plain dirty repository, the snapshot's fields are identical before and after: `worktree_sha256`, `tree_sha`, `head_sha`, `dirty` and the rest (measured in the round-two probe). `repository_id` and `repository_root` differ only when the two copies are at different paths.

## Campaign target snapshot: partly closed, one decision remains

Before the repair, a snapshot of a filtered target fired the target's fsmonitor, its `post-index-change` hook and its clean filter (measured through `capture_target_snapshot`). After the repair it fires only the clean filter. The round-two probe measured this. `campaigns/target_snapshot.py` was not changed in round three.

Disabling its clean and smudge filters is **not** done. The snapshot's status output is part of a commit-pinned identity digest (`_worktree_digest`), and disabling those filters would change identities for targets with transforming filters. That is an identity-semantics decision for the owner.

## Review history

- **Round one** (commit `5af0a288`): an independent review found two blockers, the `=` bypass and the unguarded campaign snapshot, and one undisclosed behaviour change.
- **Round two** (`5fd4c4a7`): the `=` refusal, the snapshot's fsmonitor and hook suppression, and the identity check. A second review found a third blocker: the guarded diff still ran the repository's `post-index-change` hook. The reviewer's probe reproduced it: the round-two code fired `post-index-change` on `inspect`, and the final code fires nothing.
- **Round three** (this commit): the hook override described above, a year-2100 mtime on the canary fixture (the earlier fixture did not trigger index rewrites, so the matrix could not see the hook), and the corrected evidence in this folder.

**Harness defects found and fixed.** The repository copy of `sm_tests.py` once computed its source path one level too high. Its import silently fell back to an installed package. That is fixed, and the harness now asserts that the source tree exists. The earlier README also claimed hooks were disabled, which was untested for `post-index-change`. Both are corrected here.

## Not exercised

- `exploratory_execution/execution_identity.py` (`diff --quiet`, `status`) and `exploratory_execution/target_checkout.py` (`status`, `submodule status`) run unguarded. Their clean and fsmonitor execution is inferred from the raw control, not probed. They are not repaired here.
- `workspace_knowledge.py` diffs two commits, which reads no worktree, and passes `--no-textconv --no-ext-diff`. The second reviewer's probe found that the commit-to-commit diff fires nothing.
- `strategy_cli.py` and `stewardship_validation._head_pack` run `git show rev:path`. The raw control showed `show` fires nothing.

## Verification and policy

- Raw negative control, the Sensemaking matrix before and after, the clean-fixture comparison, and the identity check are described above, with their files in `results/`.
- Two independent fresh-context reviews reviewed the repair. The round-three hook fix was checked by re-running the reviewer's own probe against the round-two and final sources. It has not yet had a third independent review.
- Repository policy for construction PRs forbids adding or running unit tests locally. The existing suite, including the two worktree-context protection tests, runs in CI.
- No global or system Git configuration was changed. Canary repositories were created under the session scratch directory, never inside the repository.

## Reproduce

```bash
GITSAFETY_SCRATCH=/path/to/scratch python experiments/git-subprocess-safety/harness/neg_control.py
GITSAFETY_SCRATCH=/path/to/scratch python experiments/git-subprocess-safety/harness/sm_tests.py
```

`sm_tests.py` runs the worktree's `src` (three levels above the harness, at the worktree root) and asserts that it exists. To reproduce the "before" column, export `origin/main`'s `src` with `git archive origin/main src` and set `GITSAFETY_SRC` to the exported `src` directory.
