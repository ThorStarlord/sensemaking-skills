# Worker contract W1 (code), v1: `--temporary-checkout` for orient, check-rules and audit

You are the implementation worker for one bounded code change. A planner wrote
this contract, will read your diff, and will have your work independently
reviewed. A second worker is editing documentation in a different worktree at
the same time; you never touch documentation.

## Outcome

Three semantic CLI commands accept `--temporary-checkout` and then read their
committed revision from a temporary detached worktree, so they succeed while
the active checkout is dirty or at another commit:

    semantic knowledge-orient
    semantic knowledge-check-rules
    semantic knowledge-audit

Today each one refuses with
`Error: dirty or untracked worktree: source bytes cannot be pinned` as soon as
the checkout has one untracked file. `semantic knowledge-build` already has
this flag; you extend the same mechanism to its three siblings.

## Where you work

- Worktree (yours alone): `H:/GithubRepositories/sensemaking-skills/.claude/worktrees/frontier-p4-code`
  on branch `claude/temporary-checkout-pinned-readers`, based on commit
  `baaec6b92f87a00dbcefdbf865da04f86d5ce59f`.
- Scratch (yours alone, outside every checkout):
  `C:/Users/Admin/AppData/Local/Temp/claude/c52b3a57866998a2/3f8955cd-0fc9-4310-958a-c1184bb925fe/scratchpad/w1`.
  Scratch repositories, index files, probe scripts and captured output live there.
- Run the CLI from source, in Git Bash:
  `cd <worktree> && PYTHONPATH=src python -m sensemaking_skills.cli semantic ...`
  (the `sensemaking-skills` executable on PATH is a stale install).
- You edit exactly one file: `src/sensemaking_skills/semantic_cli.py`.
- Leave your change uncommitted. The planner commits after reading the diff.

## Fixed decisions (build to these)

- **D1 Flag.** Each of the three commands gets a click flag
  `--temporary-checkout`. Its help text says, in ASCII, that the named ref is
  read from a temporary detached worktree outside `--repo`, that the active
  checkout may be dirty or at another commit, and that only committed bytes
  are read. The ref option is `--target-ref` for orient and check-rules and
  `--current-ref` for audit.
- **D2 Mechanism.** Use the existing context manager
  `temporary_commit_checkout(repo_root, ref)` (already imported in
  `semantic_cli.py`). Inside it, run the command's existing logic unchanged,
  with the yielded checkout path in place of `repo_root`. Audit materializes
  `--current-ref` only; its indexed side comes from the database.
- **D3 Ref rule.** With the flag, the ref is any local commit given as a full
  40-character SHA; it need not equal the active HEAD. Every refusal that
  `temporary_commit_checkout` and the inner functions already make stays in
  force.
- **D4 Default unchanged.** Without the flag, a successful command prints
  byte-for-byte what it prints today.
- **D5 Disclosure.** With the flag, the JSON payload gains exactly two
  top-level keys:
  - `"source_checkout": "temporary_worktree"`
  - `"active_checkout"`: an object with exactly these keys:
    `head` (string, the active checkout's HEAD SHA),
    `head_matches_source_ref` (bool), `worktree_clean` (bool),
    `modified_tracked_count` (int), `untracked_count` (int),
    `working_changes_read` (always `false`).

  Take the values from the existing
  `inspect_worktree_context(repo_root, ref)` (already imported), called on the
  **active** checkout with the ref that was read. It returns `current_head`,
  `head_matches_indexed_ref`, `worktree_clean`, `modified_tracked_count` and
  `untracked_count`. Every other key and value of the payload equals what the
  unflagged command prints in a clean checkout of the same commit.
- **D6 Hint.** When the flag is absent and the command fails with the message
  `dirty or untracked worktree: source bytes cannot be pinned` or
  `target_ref does not equal the checked-out Git HEAD`, the printed error is
  that original message followed by
  ` (pass --temporary-checkout to read the committed revision from a temporary worktree)`.
  Every other error message, and every error raised while the flag is
  present, is printed as it is today.
- **D7 Ref help.** The help strings of `--target-ref` (orient, check-rules)
  and `--current-ref` (audit) say that any local commit is accepted with
  `--temporary-checkout`, in the style of `knowledge-build`'s `--target-ref`
  help. The `--repo` help of check-rules stays truthful for both modes.
- **D8 Build untouched.** `knowledge-build`'s code, options, output and
  errors stay exactly as they are.

## Invariants (hold on every path)

- **I1 Committed bytes only.** The flagged path opens file contents only
  inside the temporary checkout. On the active checkout it reads Git metadata
  and status only (that is all `inspect_worktree_context` does).
- **I2 Active checkout untouched.** `git status --porcelain --untracked-files=all`
  prints the same before and after every command, and afterwards
  `git worktree list` has no entry under a `sensemaking-index-` temporary
  directory. This holds on success and on failure.
- **I3 One-line errors.** Every failure of the flagged path surfaces as the
  usual `Error: <message>` with a non-zero exit code, never a traceback.
- **I4 Authority flags.** `semantic_truth_established` and `action_authorized`
  stay `false` wherever they appear.
- **I5 Text.** ASCII only in the source file and in every string it prints or
  raises. LF line endings.
- **I6 Private helpers.** Any helper you add is module-private (leading
  underscore) and lives in `semantic_cli.py`.
- **I7 Fence.** The `knowledge-build`, `knowledge-query` and
  `knowledge-view-export` command functions, and the blank lines between
  `knowledge-query` and `knowledge-view-export`, stay byte-identical. Another
  open pull request inserts code exactly there.

## Yours to decide

Helper names and shape, whether the three commands share one private helper,
the order of internal steps, where the options sit among the decorators, and
docstring wording.

## Stop and report, instead of improvising, when

- the outcome seems to need a change outside `semantic_cli.py`;
- a fixed decision or invariant conflicts with what the code can do;
- a verification row still fails after two honest repair attempts.

## Steps

1. Read `src/sensemaking_skills/semantic_cli.py` lines 1-200 and 380-410,
   `temporary_commit_checkout` and `verified_tracked_sources` in
   `src/sensemaking_skills/semantic_architecture/knowledge_sources.py`, and
   `src/sensemaking_skills/semantic_architecture/worktree_context.py`.
   Done when you can say which existing call each command makes with
   `repo_root`.
2. Implement D1-D8 under I1-I7. Done when `git diff --stat` lists only
   `src/sensemaking_skills/semantic_cli.py`.
3. Run every verification row below on the real CLI. This repository's policy
   for this phase is real-path checks only: do not write or run unit tests
   (`pytest`). Done when every row is PASS, or is reported FAIL / NOT RUN with
   its output.
4. Reply with the report in the exact format at the end. Your reply is the
   deliverable; write nothing else after it.

## Verification rows

Scratch repository `S`: `git init` under your scratch directory, set a local
`user.name` and `user.email`, commit three tracked files (`README.md`,
`src/app.py`, `tests/test_app.py`); call the commit `C1`. Use repository
identity `example/scratch`.

| Row | Do | PASS when |
| --- | --- | --- |
| V1 | In clean `S` at `C1`, run orient and check-rules without the flag; save both JSON outputs | exit 0; no `source_checkout` or `active_checkout` key |
| V2 | Add an untracked file to `S`; run orient and check-rules without the flag | non-zero exit; stderr is the original dirty message followed by the D6 hint |
| V3 | Also modify one tracked file in `S` (uncommitted); run orient and check-rules with the flag | exit 0; after removing the two D5 keys, each JSON equals its V1 output; `active_checkout` is `head == C1`, `head_matches_source_ref true`, `worktree_clean false`, `modified_tracked_count 1`, `untracked_count 1`, `working_changes_read false` |
| V4 | Commit the changes in `S` as `C2`; run orient with the flag and `--target-ref C1` | exit 0; `target_ref` is `C1`; `tracked_file_count` is 3; `head_matches_source_ref false`. Without the flag the same call fails with the HEAD-mismatch message plus the D6 hint |
| V5 | In your (dirty) worktree: build an index of the real repository at `53b667c1` (resolve the full SHA with `git rev-parse`) using `knowledge-build --temporary-checkout --db <scratch>/old.sqlite --repository ThorStarlord/sensemaking-skills`; then run audit with `--indexed-ref <that SHA> --current-ref baaec6b92f87a00dbcefdbf865da04f86d5ce59f --temporary-checkout` | exit 0; `record_count` > 0; `source_status_counts` present; both D5 keys present; `worktree_clean false` |
| V6 | In your worktree, run check-rules with the flag at `baaec6b9...`, and audit without the flag | flagged check-rules: exit 0 with a non-empty `rule_assessments`; unflagged audit: dirty message plus hint |
| V7 | Around every flagged command in V3-V6 capture `git status --porcelain --untracked-files=all` before and after, and `git worktree list` after | status identical; no `sensemaking-index-` entry |
| V8 | With the flag in `S`: `--target-ref abc`; `--target-ref` of 40 zeros; `--repo S/src` | each fails with a one-line `Error:` and no traceback; V7 conditions hold afterwards |
| V9 | Scratch repository `F`: commit a `.gitattributes` containing `*.txt filter=demo` and a `a.txt`; run orient with the flag | refused with the existing "assigns Git filters" message; no worktree entry left |
| V10 | `--help` of the three commands and of `knowledge-build` | the three list `--temporary-checkout` and the D7 wording; build's help equals the help printed from the unmodified reference worktree named below |
| V11 | `python -m ruff check --select E4,E7,E9,F src/sensemaking_skills/semantic_cli.py`; `git ls-files --eol src/sensemaking_skills/semantic_cli.py`; an ASCII check of the file; `git diff --stat` | ruff clean; `w/lf`; ASCII; one file changed |

The unmodified reference worktree for V10 is
`H:/GithubRepositories/sensemaking-skills/.claude/worktrees/frontier-p4-planner`
(read-only for you).

## Report format (reply with exactly these sections)

```
MODEL: <the exact model id stated in your own system prompt>
FILES CHANGED: <git diff --stat output>
DESIGN: <up to 6 bullets: helpers you added and why>
VERIFICATION:
<one line per row: V<n> | PASS/FAIL/NOT RUN | the decisive output excerpt>
DEVIATIONS FROM CONTRACT: <none, or each with its reason>
OBSERVATIONS OUTSIDE SCOPE: <things you noticed and did not change>
OPEN QUESTIONS: <none, or each question>
```
