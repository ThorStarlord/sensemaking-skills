# Independent reviewer report (Frontier P4, 2026-11-10)

This is the report of the independent reviewer, preserved as it was returned.
The reviewer was a fresh-context subagent given
[reviewer-brief-v1.md](reviewer-brief-v1.md). It reviewed head
`3c6ba4fcd99a4c4d4392d12d82ceb48d79cf20e0`, before the repair round that its
findings caused. Its first attempt was cut off by the account's usage limit
before it had run anything but reads; it was resumed once. Host-reported
usage: 129,868 tokens, 23 tool calls, 458 s.

---

REVIEWER IDENTITY: claude-opus-5-5

VERDICT: ACCEPT_WITH_REPAIRS. The CLI behaves correctly and fails closed on every path I tried, but the Steward `SKILL.md` still contradicts itself on clean checkouts (condition 9), and a few smaller guidance and output inconsistencies remain.

ACCEPTANCE CONDITIONS:

1. PASS. In a detached worktree of 3c6ba4fc with an untracked file, unflagged `knowledge-audit` exits 1 with `dirty or untracked worktree ... (pass --temporary-checkout ...)`. Flagged, it exits 0. Its JSON equals the clean-worktree audit on every key; the only extra keys are `active_checkout` and `source_checkout`. Counts against my own index of 53b667c1 (`--temporary-checkout`, 222 claims): 219 records changed, 223 unchanged.
2. PASS. Flagged `knowledge-check-rules` from the dirty worktree gives the same `rule_assessments` and `findings` as the clean run; the only extra keys are the two disclosure keys.
3. PASS. Scratch repo at a path with a space (`.../reviewer/target repo`), untracked `notes.txt`. Flagged orient exits 0 with `tracked_file_count` 2 (README.md, src). `notes.txt` and the temporary path appear nowhere in the output.
4. PASS (weakly). Every flagged output has `active_checkout.worktree_clean=false`, `untracked_count`, `modified_tracked_count` and `working_changes_read=false`. These are fields only; no plain-language limit sentence is added (Finding 5).
5. PASS. I appended to CONTEXT.md, staged an edit to STATUS.md (a cited file) and deleted a tracked doc. The flagged `--limit 500` audit was byte-for-byte the same as the clean audit, with `modified_tracked_count` 3.
6. PASS. An md5 of `git status --porcelain` plus `git worktree list --porcelain` was identical before and after every run. That includes three failures: an unsupported `--db` schema, a filter refusal, and an unborn HEAD. No `sensemaking-index-*` directory was left in %TEMP%.
7. PASS. A tag (`v1`), a 12-character SHA and `HEAD` were all refused with `must be a full 40-character Git SHA`. The all-zero SHA was refused with `not a local commit`. A commit with `*.py filter=evil` and a configured smudge command was refused with `assigns Git filters to tracked paths`, and the smudge never ran (no pwned.txt).
8. PASS. On a clean worktree, base source (baaec6b9) and new source give byte-identical JSON for audit, check-rules and orient (orient md5 f4764619...). The flagged orient minus the two disclosure keys also matches that hash.
9. FAIL. `skills/repository-semantic-steward/SKILL.md:100` still says "Only orientation/build (and source audit) require a clean checked-out source revision." That contradicts line 32, where all four commands accept `--temporary-checkout` as "not a development gate". The `decision:`/`inv:` records were revised; bootstrap.md and reconciliation.md are consistent.

FINDINGS:

1. SHOULD_FIX. SKILL.md:100 (and the example block, lines 91-97). An agent reading the CLI section from a dirty checkout is told orient, build and audit "require" a clean checkout. Line 100 also leaves out check-rules, which still refuses unflagged; that omission predates this change. This is the self-contradiction the outcome was meant to remove. Holding back for PR 801 leaves the core Skill inconsistent if this merges first. Evidence: read lines 32 and 100 side by side. Direction: have PR 801 adopt the wording "read a clean committed revision; add `--temporary-checkout` from a dirty checkout", or make a one-line edit here and resolve the conflict in 801.
2. NOTE. semantic_cli.py, the knowledge-build path (lines 157-168). The unflagged build refusal gets no flag hint, because it is not routed through `_refusal`. Build also always emits `source_checkout` (`"active_checkout"` when unflagged) and no `active_checkout` object. The three new commands omit `source_checkout` when unflagged and use `active_checkout` as an object key, so the same word is a value in one command and a key in another. Evidence: reading the code. Direction: align the four commands, or document the difference.
3. NOTE. semantic_cli.py, `_temporary_checkout_disclosure`. The disclosure is computed after the source read and runs `git rev-parse HEAD` on the active checkout. With an unborn HEAD (orphan branch) the read succeeds, then the whole command fails with the opaque `cannot inspect local Git repository worktree`. Evidence: reproduced in the scratch repo; cleanup was correct. Direction: tolerate an unborn HEAD (`head: null`), or document it.
4. NOTE. knowledge-audit with the flag. The full worktree checkout happens before the DB, schema and indexed-ref checks, so a bad `--db` or `--indexed-ref` pays for a whole checkout before it is refused. Evidence: code order, `_pinned_source` wraps `audit_knowledge_sources`. Direction: open and validate the snapshot first if cost matters.
5. NOTE. persistent-knowledge-cli.md, the flag help, and `lesson:separate-clone-changes-audited-bytes`. "Only committed bytes are read" really means checked-out bytes after eol conversion. In a repository whose effective `core.autocrlf` is true, the temporary worktree also produces CRLF. My default clone (autocrlf inherited as true) gave 442/442 changed both unflagged and flagged. The docs do say the worktree "uses that repository's configuration", so this is honest. The lesson's "every cited source reads as changed" overgeneralises one observation (a file without newlines would not change). Its "139 of 442" is the count against the base baaec6b9 (I reproduced it there); against HEAD it is 219, and the scope note does not name the ref. Direction: name the ref in the scope note, and soften "every".
6. NOTE. knowledge-proposal-check limits. Its limit text "Full semantic knowledge indexing requires an exact clean committed Git HEAD" is now loosely stale. This predates the change and is not in the diff.
7. NOTE. tests. No test covers `--temporary-checkout` for any command, `knowledge-build` included. The CLAUDE.md construction phase allows this, but conditions 5-7 currently rest on manual probes only.

DESIGN ASSESSMENT: An opt-in flag that reuses `temporary_commit_checkout` is the right choice. It keeps the fail-closed default that hosted tests pin, adds no second byte path, and the context manager cleaned up correctly on every failure I triggered. Declining an automatic fallback is well argued: callers would silently lose the fact that their edits were not read. Deferring a Git-object reader is right, because it would have to reproduce the eol conversion every existing fingerprint already includes. I would have computed the active-checkout disclosure before the checkout, so a broken HEAD fails cheaply and clearly. I would also have given all four commands one shared output shape (`source_checkout` always present, `active_checkout` when flagged). And I would have made the one-line SKILL.md:100 fix here instead of leaving a known contradiction in the core Skill.

HOSTED TEST PREDICTION: These should all pass.

- `test_architecture_rule_checker.py:147` and `test_repository_bootstrap.py:216-217` check the substring `dirty or untracked`, which is preserved with the hint appended. The direct `snapshot()` ValueError is unchanged.
- `test_repository_semantic_steward.py:75-85` checks `knowledge-query --repo .`, `clean checked-out` (lines 32 and 100) and `dirty active checkout` (line 100). The `inv:` id, kind, evidence files and the `cap:semantic-queries constrained_by` relation are unchanged.
- `test_sensemaking_receipts.py:258` needles are untouched.
- `test_architecture_queries.py:173`: the new relations do not change knowledge-store ownership, layer or context.
- `knowledge-proposal-check` on stewardship.json returns VALID: 31 claims, 43 relations.

NOT VERIFIED: pytest (policy); a repository with a submodule; a shallow clone under the flag; two concurrent runs; a real interrupt (Ctrl-C or kill); very large checkout timeouts; the Linux CI byte behaviour.

Merge-tree against the four PR heads: no new conflict. PR 797's existing architecture.json conflict with main is unchanged; 801, 796 and 795 merge cleanly.

Interruption check: before resuming I found no half-made worktree, no `sensemaking-index-` entry, no prunable entry and no reviewer directory, because I had run only reads before the cut. The planner's `review/cleanwt` worktree is still registered and I did not touch it. I created and removed three detached worktrees (dirty, clean, basesrc). Afterwards the worktree list has no reviewer entry, and the code worktree is clean at 3c6ba4fc. One self-inflicted slip: I ran `git stash -u` and then `stash pop` inside my own standalone scratch repo. It is its own repository, so the shared stash stack was not affected, and the before/after comparison for condition 3 was redone after the pop. A standalone clone (`crlfclone`) and the scratch repo stay in the reviewer scratch directory.

COMMANDS: about 25 tool calls. Notable ones: `knowledge-build --temporary-checkout` for 53b667c1 into reviewer/old.sqlite; the dirty-vs-clean audit and check-rules diffs; the staged/modified/deleted fingerprint test; the default CRLF clone audit (442/442 changed, flagged and unflagged); orient negatives (tag, short SHA, zero SHA, `HEAD`, subdirectory, bad DB, filter plus smudge, ref other than HEAD, unborn HEAD); base-vs-new md5 comparisons; `knowledge-proposal-check`; `git merge-tree --write-tree` against 4 heads; worktree and status snapshots.
