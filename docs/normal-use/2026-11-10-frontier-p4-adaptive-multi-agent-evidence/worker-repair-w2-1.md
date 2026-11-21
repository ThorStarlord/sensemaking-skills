# W2 repair and extension round 1

Your eleven edits were read and accepted, including the two line-number
corrections you reported. The code worker has finished; the interface it built
matches the Interface section of your contract exactly, so nothing you wrote
needs to change for that reason.

Four items remain. Two are errors in the planner's contract, one is the
observation you raised, and one is new evidence found while the code was being
checked. Same worktree, same rules for the text, same fences, still
uncommitted.

## Items

| Item | File and site | Change |
| --- | --- | --- |
| R1 | `skills/repository-semantic-steward/references/knowledge-contract.md`, your S6 sentence | The sentence "No command reads dirty bytes." is wrong: `knowledge-proposal-check` exists to read a dirty or untracked proposal file. That wording came from the contract. Replace your two S6 sentences with one statement scoped to the four commands: none of `knowledge-build`, `knowledge-orient`, `knowledge-check-rules` and exact-source `knowledge-audit` reads dirty bytes; each reads a clean committed revision, from the active checkout when it is clean or from a temporary worktree with `--temporary-checkout`. Keep the rest of the paragraph |
| R2 | `skills/repository-semantic-steward/references/bootstrap.md` line 19, your S3 item | The item still says orient runs "against clean HEAD". Say "against the committed HEAD" |
| R3 | `docs/semantic-architecture/repository-bootstrap.md`, the sentence "The command refuses untracked/dirty source bytes and wrong HEAD." (your observation) | Make it true for both modes: without `--temporary-checkout` the command refuses untracked or dirty source bytes and a ref other than the checked-out HEAD |
| R4 | `docs/semantic-architecture/persistent-knowledge-cli.md`, at the end of the paragraph you added for S7 | Add two or three sentences with exactly this meaning and nothing more: the temporary worktree belongs to the same repository, so it uses that repository's Git configuration and checks out the same bytes as its ordinary checkout. A separate clone can differ: under another `core.autocrlf` setting its text files have other line endings, and `knowledge-audit` then reports every cited source as changed. Observed on one Windows host on 2026-11-10: 442 of 442 records reported changed from such a clone, against 139 of 442 from a worktree of the repository itself |

## Checks

Run C1 to C8 from your contract again on the final state, and repeat step 4
(the sweep) for the three files you touch in this round.

## Report

Reply with the same report format as before. Under `SITES`, list only R1 to
R4. Start with the `MODEL:` line.
