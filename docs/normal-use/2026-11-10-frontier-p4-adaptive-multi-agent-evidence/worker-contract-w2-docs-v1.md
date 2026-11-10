# Worker contract W2 (guidance and documentation), v1: `--temporary-checkout` on orient, check-rules and audit

You are the documentation worker for one bounded change. A planner wrote this
contract, will read your diff, and will have it independently reviewed against
the real CLI. A second worker is implementing the code in a different worktree
at the same time; you never touch code.

## Outcome

Six guidance and documentation files tell a coding agent one consistent thing:
the four commands that pin source to a commit read a clean committed revision,
and each can do that from a dirty checkout with `--temporary-checkout`. Today
the files contradict one another: one says "do not create a clean-room
development session" and then requires a naturally clean HEAD; another says to
use a separate clean worktree; a third says no build accepts a dirty checkout.

## Interface you are documenting (the single source of truth; state nothing beyond it)

- Commands with the flag: `semantic knowledge-build` (already has it),
  `semantic knowledge-orient`, `semantic knowledge-check-rules`,
  `semantic knowledge-audit`.
- With `--temporary-checkout`, the command reads the named commit
  (`--target-ref`; for audit, `--current-ref`) from a temporary detached
  `git worktree` outside the repository and removes it afterwards. The active
  checkout may be dirty (an untracked session receipt, for example) or at
  another commit. Only committed bytes are read; the same clean-source checks
  run inside the temporary checkout. The ref is any local commit given as a
  full 40-character SHA.
- With the flag, the JSON output of orient, check-rules and audit gains two
  keys: `source_checkout` with the value `temporary_worktree`, and
  `active_checkout` with `head`, `head_matches_source_ref`, `worktree_clean`,
  `modified_tracked_count`, `untracked_count` and `working_changes_read`
  (always `false`). Everything else in the output equals a clean-checkout run
  at the same commit.
- Without the flag nothing changes: a dirty checkout, or a ref that is not the
  checked-out HEAD, is refused as before. The refusal message now ends with a
  hint naming `--temporary-checkout`.
- Limits, the same as for `knowledge-build --temporary-checkout`: hooks, the
  filesystem monitor and configured external filters are disabled for the
  checkout; a commit whose attributes assign a filter to a tracked path is
  refused; a shallow clone has only the commits it has; an interrupted run can
  leave a worktree entry that `git worktree list` marks prunable. The flag
  costs one checkout of the commit.

## Where you work

- Worktree (yours alone): `H:/GithubRepositories/sensemaking-skills/.claude/worktrees/frontier-p4-docs`
  on branch `claude/temporary-checkout-pinned-readers-docs`, based on commit
  `baaec6b92f87a00dbcefdbf865da04f86d5ce59f`.
- Scratch (yours alone): `C:/Users/Admin/AppData/Local/Temp/claude/c52b3a57866998a2/3f8955cd-0fc9-4310-958a-c1184bb925fe/scratchpad/w2`.
- You edit exactly the six files named in the site table. Leave your change
  uncommitted; the planner commits after reading the diff.

## Sites (edit every one; line numbers are at the base commit)

`STEWARD` = `skills/repository-semantic-steward`, `DOCS` = `docs/semantic-architecture`.

| Site | File and line | What it says now | What it must say afterwards |
| --- | --- | --- | --- |
| S1 | `STEWARD/SKILL.md` line 32 (operating contract item 2) | build and audit require a clean checked-out committed revision; only build has `--temporary-checkout` | `knowledge-build`, `knowledge-orient`, `knowledge-check-rules` and exact-source `knowledge-audit` read a clean checked-out committed revision; when the active checkout is dirty (including an untracked session receipt) or another commit is needed, each accepts `--temporary-checkout`, which reads the committed revision from a temporary worktree and is an option, not a development gate. Keep, in your own flow, the existing statements that `knowledge-query --repo .` can query an existing committed index from the dirty active checkout, that `workspace_context` reports revision alignment and unindexed changes, and that neither queries nor worktree metadata index the working overlay |
| S2 | `STEWARD/SKILL.md` "Rule drift" bullet (lines 116-117) | check-rules reads committed bytes only | the same, plus one clause: add `--temporary-checkout` to run it from a dirty checkout |
| S3 | `STEWARD/references/bootstrap.md` line 19 | "use a separate clean worktree for index commands"; orient "against clean HEAD" | the worktree may be dirty; `knowledge-orient` and `knowledge-build` accept `--temporary-checkout` and then read the committed HEAD from a temporary worktree, so a hand-made clean worktree is unnecessary. Keep the rest of the item |
| S4 | `STEWARD/references/reconciliation.md` line 10 (procedure item 2) | audit only "at the naturally clean current HEAD" after a commit | keep the opening sentence about not creating a clean-room session; audit runs at a clean HEAD after an ordinary commit, or with `--temporary-checkout` while the checkout is dirty; either way only committed bytes are compared. Keep the rest of the item |
| S5 | `STEWARD/references/reconciliation.md` line 42 ("Architecture drift") | run check-rules "at the new clean HEAD" | run it at the new HEAD, adding `--temporary-checkout` while the checkout is dirty. Keep the rest of the bullet |
| S6 | `STEWARD/references/knowledge-contract.md` line 156 | "No `knowledge-build` operation accepts a dirty checkout; use a clean detached snapshot/worktree." | no command reads dirty bytes; the four commands read a clean committed revision, from the active checkout when it is clean or from a temporary worktree with `--temporary-checkout`. Keep the rest of the paragraph |
| S7 | `DOCS/persistent-knowledge-cli.md`, a new paragraph directly after the paragraph that ends "...copies objects instead." (line 69) | the flag is described for build only | a paragraph of 5 to 9 lines: orient, check-rules and audit accept the same flag (audit applies it to `--current-ref`), under the same checks and limits; the two output keys and their fields; the refusal hint |
| S8 | `DOCS/persistent-knowledge-cli.md` lines 77-78 (sentence before the audit example) | "while standing in a newer clean target checkout" | the audit also runs from a dirty checkout with `--temporary-checkout`. Leave the example command itself as it is |
| S9 | `DOCS/persistent-knowledge-cli.md` line 147 | "Use `knowledge-audit` for byte-level drift once the checkout is clean." | audit gives byte-level drift at a clean checkout, or with `--temporary-checkout` while it is dirty |
| S10 | `DOCS/persistent-knowledge-cli.md` lines 546-547 (orient section opening) | orient inspects "a clean Git checkout" | the same, plus: with `--temporary-checkout` it orients a dirty checkout at its committed HEAD |
| S11 | `DOCS/repository-bootstrap.md` line 38 and lines 98-99 | "On a **clean checkout**, pin the full Git HEAD"; rebuild "at the new clean HEAD" | both stay true and each gains the dirty-checkout alternative through `--temporary-checkout`; orientation still covers only the committed HEAD |

## Rules for the text

- **Pinned phrases.** Hosted tests assert that `STEWARD/SKILL.md` contains the
  literal strings `` `knowledge-query --repo .` ``, `clean checked-out` and
  `dirty active checkout`, and every existing `(references/<name>.md)` link.
  All of them are still present when you finish.
- **Fences.** Other open pull requests edit these regions; leave them
  byte-identical: `STEWARD/SKILL.md` lines 85-100; `STEWARD/references/reconciliation.md`
  lines 33-37; `STEWARD/references/knowledge-contract.md` line 75;
  `DOCS/persistent-knowledge-cli.md` lines 152-162, 338-363 and 383-463
  (numbers at the base commit; S7 shifts later lines down, so locate the
  regions by their text).
- **Shape.** An item that is one physical line today stays one physical line.
  `persistent-knowledge-cli.md` and `repository-bootstrap.md` wrap prose at
  about 78 columns; follow each file's existing wrapping. Change only the
  sentences a site names.
- **Style.** Plain declarative sentences in the voice of the surrounding
  text. Added text is ASCII. LF line endings.
- **Truth.** Every statement about behavior comes from the Interface section
  above. State no measurements, test results or behaviors that are not there.

## Stop and report, instead of improvising, when

- a site's current text differs from the "says now" column in a way that
  changes what the edit should be;
- a site cannot be made accurate without editing a fenced region or a seventh
  file;
- the Interface section seems to contradict something the files say.

## Steps

1. Read each site with enough surrounding text to match its voice. Done when
   you have located all eleven sites.
2. Edit the eleven sites. Done when `git diff --stat` lists exactly the six
   files.
3. Run the checks below. Done when each is PASS or reported with its output.
4. Sweep: run
   `grep -n -i -E "clean (worktree|checkout|head)|separate clean|clean-room|naturally clean" skills/repository-semantic-steward/SKILL.md skills/repository-semantic-steward/references/bootstrap.md skills/repository-semantic-steward/references/reconciliation.md skills/repository-semantic-steward/references/knowledge-contract.md docs/semantic-architecture/persistent-knowledge-cli.md docs/semantic-architecture/repository-bootstrap.md`
   and account for every hit in the report: either it is one of your edits, it
   sits in a fence, or you say why it is still accurate.
5. Reply with the report in the exact format at the end. Your reply is the
   deliverable; write nothing else after it.

## Checks

| Check | Command (from your worktree, Git Bash) | PASS when |
| --- | --- | --- |
| C1 | `python scripts/validate-docs-currentness.py --repo-root .` | exit 0 |
| C2 | `python scripts/validate-skill-hygiene.py` | exit 0 |
| C3 | `python scripts/validate-repo.py` | exit 0 |
| C4 | `python scripts/validate-product-boundary.py` | exit 0 |
| C5 | `grep -c` for each of the three pinned phrases in `STEWARD/SKILL.md` | each count is at least 1 |
| C6 | `git diff --stat` and `git ls-files --eol` on the six files | six files; every one `w/lf` |
| C7 | `git diff -U0 \| grep "^+" \| LC_ALL=C grep -n -P "[^\x00-\x7F]"` | prints nothing |
| C8 | `git diff -U0` hunks compared with the fences | no hunk touches a fenced line |

## Report format (reply with exactly these sections)

```
MODEL: <the exact model id stated in your own system prompt>
FILES CHANGED: <git diff --stat output>
SITES:
<one line per site: S<n> | DONE or NOT DONE | the new sentence or clause, quoted>
CHECKS:
<one line per check: C<n> | PASS/FAIL/NOT RUN | decisive output>
SWEEP: <each remaining grep hit: file:line | edit / fence / still accurate because ...>
DEVIATIONS FROM CONTRACT: <none, or each with its reason>
OBSERVATIONS OUTSIDE SCOPE: <things you noticed and did not change>
OPEN QUESTIONS: <none, or each question>
```
