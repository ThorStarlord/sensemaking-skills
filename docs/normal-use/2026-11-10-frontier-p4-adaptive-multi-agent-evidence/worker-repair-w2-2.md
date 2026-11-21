# W2 repair round 2

Your round-1 repairs were accepted and committed, and hosted CI passed on the
result. An independent reviewer then read the six files against the real CLI.
Five items follow. One reverses a planner decision (the fence on `SKILL.md`
line 100), three follow from small interface changes the code worker is making
now, and one is a wrapping slip from round 1.

## State of your worktree

`H:/GithubRepositories/sensemaking-skills/.claude/worktrees/frontier-p4-docs`
is clean: the planner committed your edits as one commit on your branch. Work
on top of it and leave the new change uncommitted.

## Interface changes since your contract (now part of the single source of truth)

- `active_checkout` has a seventh field, `note`: a fixed sentence saying that
  the active checkout was not read and that its uncommitted and untracked
  changes are not part of the result.
- `knowledge-build`'s refusal, when its flag is absent, now ends with the same
  hint naming `--temporary-checkout`. `knowledge-build` otherwise behaves as
  before: it reports `source_checkout` in both modes (`active_checkout` or
  `temporary_worktree`) and has no `active_checkout` object. The other three
  commands add their two keys only with the flag.
- Source fingerprints are taken from the bytes Git checks out, after any
  line-ending conversion that the repository's configuration applies.

## Items

`STEWARD` = `skills/repository-semantic-steward`, `DOCS` = `docs/semantic-architecture`.

| Item | File and site | Change |
| --- | --- | --- |
| R5 | `STEWARD/SKILL.md` line 100, its first sentence only (the bold one beginning "**Only orientation/build") | The reviewer found that this sentence still contradicts line 32, so the fence is lifted for this one sentence. Replace it with exactly: ``**Orientation, build, rule checks and source audit read a clean checked-out source revision; from a dirty checkout, add `--temporary-checkout`.**`` Lines 85-99 and the rest of line 100 stay byte-identical |
| R6 | `DOCS/persistent-knowledge-cli.md`, the paragraph you added for S7, the list of `active_checkout` fields | Add `note` to the list, with what it says |
| R7 | The same paragraph, after the sentence about the refusal hint | Add: `knowledge-build` reports `source_checkout` in both modes and has no `active_checkout` object; these three commands add their two keys only with the flag; `knowledge-build`'s refusal ends with the same hint |
| R8 | The same paragraph, the separate-clone sentences you added in round 1 | Start a new paragraph (one blank line) at "The temporary worktree belongs". Say that fingerprints are taken from the bytes Git checks out, after any line-ending conversion the repository's configuration applies. Replace "reports every cited source as changed" with "reports cited text files as changed". Name the revisions in the observation: it was an audit of an index of commit `53b667c1` run at commit `baaec6b9` |
| R9 | `DOCS/repository-bootstrap.md`, the sentence beginning "Without `--temporary-checkout`, the command refuses" | It is one long physical line in a file wrapped at about 78 columns. Rewrap that paragraph to the file's width; change no words |

## Checks

Run C1 to C8 from your contract on the final state. For C8, the fence in
`STEWARD/SKILL.md` is now lines 85-99 plus everything on line 100 after its
first sentence. For C5, confirm the three pinned phrases are still present
after R5.

## Report

Reply with the same report format as before. Under `SITES`, list only R5 to
R9, quoting the final text of each. Start with the `MODEL:` line.
