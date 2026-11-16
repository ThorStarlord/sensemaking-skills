# Git subprocess safety: configured helpers run while Sensemaking reads a checkout

**Question.** Can Sensemaking's Git subprocesses, when they read or index a checkout, run programs configured in that checkout's own Git configuration (`core.fsmonitor`, clean, smudge or process filters, textconv, external diff, hooks)?

**Trigger.** PR #877's security review, which asked for the mechanism to be tested rather than assumed.

**Answer.** Yes, in several reachable operations on the pre-repair code. The protected path (`worktree_context.inspect_worktree_context`) already disabled fsmonitor and configured filters, and two existing tests cover it. Other read paths did not, and the protected path itself still ran the repository's `post-index-change` hook. The repair routes the affected paths through the protection, disables repository hooks on it, and refuses one configuration shape the protection could not disable safely. This folder records the reproduction, the repair, the measured behaviour changes, and what remains.

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

`results/sm_results_before_repair.json` and `results/sm_results_after_repair.json`, from `harness/sm_tests.py`. Each row ran the real CLI on a fresh canary repository. The "before" run used `origin/main`'s source; the "after" run used the final worktree source. The fixture's mtime is in the year 2100, which guarantees that git re-hashes the file and rewrites the index, so the `post-index-change` canary can fire at all.

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

`results/clean_fixture_old_vs_final.json` (from `harness/clean_fixture_ab.py`) compares the build digest, the impact payload and the release payload on one clean fixture, `origin/main` against the final source. All are identical, with identical exit codes. The fixture has no knowledge claims (`build_claims: 0`), so the matching digest shows that the build path is identical, not that claim content is.

## The repair

- `worktree_context.guarded_git_text` is the existing protection, exposed as a helper. It disables fsmonitor, every configured clean, smudge or process filter (by name), and the repository's hooks. It sets `core.hooksPath` to the null device, because a diff against the worktree refreshes the index and would otherwise run `post-index-change`.
- `impact.py`, `stewardship_validation.py` and `release_authority.py` route their status, diff and ls-files calls through that helper.
- `knowledge_sources.py` adds `-c core.fsmonitor=false` to its `_git` helper and to the two calls in `_filtered_paths`. `ls-files` and `check-attr` run no filters, so only fsmonitor needed disabling there.
- `campaigns/target_snapshot.py` disables fsmonitor for its git calls and sets `GIT_OPTIONAL_LOCKS=0`. Clean and smudge filters are **not** disabled there (see below).
- A configured filter name containing `=` or a line break is refused. `-c name=` is split at its first `=`, so such a name would disable the wrong key.
- The guarded error includes Git's own reason. Before, it was dropped.
- The guard's timeout is 30 seconds. It was 20 in `worktree_context`, 15 in `impact.py` and 30 in `stewardship_validation.py`, and `release_authority.py` had no timeout.

Git's built-in text and end-of-line conversion is not an external filter driver, and it is not disabled. A CRLF worktree over an LF blob gives the same result through the guarded helper as through raw Git.

**Windows dependency.** On this machine the hooks override relies on Windows treating `nul` as a device name: the path does not resolve to a directory, so no hook can be found under it. The override was probed here. POSIX `/dev/null` was not tested.

## Measured behaviour changes

1. **Transforming filters (the git-lfs pattern).** For a file whose stored form comes from a transforming filter, the guarded status compares raw worktree bytes with the stored form, so it reports the file modified. Raw Git reports it clean, and so did `origin/main`'s unguarded `impact`, `stewardship_validation` and `release_authority` status. `results/tradeoff_probe.json` (from `harness/tradeoff_probe.py`) shows this: the stored blob is the filtered form, raw status is clean, and the guarded status is `M`. Affected callers: `impact-preview`, `knowledge-proposal-check` and `release audit`. They now fail closed on such repositories. `knowledge-build` already behaved this way, through `worktree_context`. This repository's three tracked `.gitattributes` files define no `filter=` attributes, so its own release audit is not affected.
2. **Required filters.** A driver marked `required` makes raw status fail, and it makes the guarded status fail too. Git's reason is now included in the error. This is a clearer message, not a new failure. `release_authority` still returns `None` on failure, as before.
3. **Filter names with `=`.** The refusal applies across every configuration scope, global and system included. One such name in the user's global configuration makes every guarded operation fail. This is fail-closed and rare. It is recorded as a known limitation, not changed here.
4. **Index writes.** Guarded status leaves `.git/index` unchanged (the guard sets `GIT_OPTIONAL_LOCKS=0`). A guarded diff may still refresh the index file, but the hook that refresh would run is suppressed. The campaign snapshot used to write the index through status; it no longer does.
5. **Campaign identity.** `results/identity_and_snapshot_probe.json` (from `harness/identity_and_snapshot_probe.py`) takes both snapshots of the same dirty plain repository, once with `origin/main` and once with the final source. No field differs, including `worktree_sha256`. Snapshots of different paths differ in `repository_id` and `repository_root`, which is expected.

## Campaign target snapshot: partly closed, one decision remains

`results/identity_and_snapshot_probe.json` records the canaries fired by a snapshot of a filtered target. `origin/main` fires the clean filter, fsmonitor and the `post-index-change` hook. The final source fires only the clean filter.

Disabling its clean and smudge filters is **not** done. The snapshot's status output is part of a commit-pinned identity digest (`_worktree_digest`), and disabling those filters would change identities for targets with transforming filters. That is an identity-semantics decision for the owner.

## Review history

- **Round one** (commit `5af0a288`): an independent review found two blockers, the `=` bypass and the unguarded campaign snapshot, and one undisclosed behaviour change.
- **Round two** (`5fd4c4a7`): the `=` refusal, the snapshot's fsmonitor and hook suppression, and the identity check. A second review found a third blocker: the guarded diff still ran the repository's `post-index-change` hook. The reviewer's probe reproduced it: the round-two code fired `post-index-change` on `inspect`, and the final code fires nothing.
- **Round three** (`0dd57c27`, and this commit): the hook override, a 30-second timeout, a year-2100 mtime on the canary fixture (the earlier fixture did not trigger index rewrites, so the matrix could not see the hook), and the evidence generators in `harness/`. A narrow review of this round found the code sound and two documentation blockers, both corrected here: the claim that guarded diff never writes the index, and the understated residual exposure below.

**Harness defects found and fixed.** The repository copy of `sm_tests.py` once computed its source path one level too high. Its import silently fell back to an installed package. That is fixed, and the harness now asserts that the source tree exists. The earlier README also claimed hooks were disabled, which was untested for `post-index-change`. Both are corrected here.

## Not exercised, and residual exposure

- **`exploratory_execution/execution_identity.py`** runs unguarded `git diff --quiet <sha>` and `git status`. A reviewer's probe found that `diff --quiet <sha>` fires fsmonitor and `post-index-change` in a canary repository. This is not in the stored matrix, and the callers are not repaired here.
- **`exploratory_execution/target_checkout.py`** runs unguarded `status` and `submodule status`. It is not probed. Assume the same exposure as the first bullet until it is.
- **`workspace_knowledge.py`** diffs two commits, which reads no worktree, and passes `--no-textconv --no-ext-diff`. The reviewer's probe found that this commit-to-commit diff fires nothing.
- **`strategy_cli.py`** and **`stewardship_validation._head_pack`** run `git show rev:path`. The raw control shows `show` fires nothing.

## Verification and policy

- Raw negative control, the Sensemaking matrix before and after, the clean-fixture comparison, the trade-off probe and the identity-and-snapshot probe are in `results/`, each produced by a script in `harness/`.
- Three independent fresh-context reviews have examined this work. The round-three hook fix was checked by re-running the reviewer's own probe against the round-two and final sources. The narrow round-three review's documentation blockers are corrected in this commit. That commit has not had a further independent review.
- The suite's two worktree-context tests cover fsmonitor and the clean filter only. Nothing in the suite checks the hook. The hook is verified only by the harness in this folder.
- Repository policy for construction PRs forbids adding or running unit tests locally. The existing suite runs in CI.
- No global or system Git configuration was changed. Canary repositories were created under the session scratch directory, never inside the repository.

## Reproduce

```bash
export GITSAFETY_SCRATCH=/path/to/scratch
python experiments/git-subprocess-safety/harness/neg_control.py
python experiments/git-subprocess-safety/harness/sm_tests.py
export GITSAFETY_OLD_SRC=/path/to/exported/origin-main/src
python experiments/git-subprocess-safety/harness/clean_fixture_ab.py
python experiments/git-subprocess-safety/harness/tradeoff_probe.py
python experiments/git-subprocess-safety/harness/identity_and_snapshot_probe.py
```

`sm_tests.py` runs the worktree's `src` (three levels above the harness, at the worktree root) and asserts that it exists. To reproduce the "before" column, export `origin/main`'s source with `git archive origin/main src`, and set `GITSAFETY_SRC` to the exported `src` directory. The other generators that compare against `origin/main` take `GITSAFETY_OLD_SRC` in the same way.
