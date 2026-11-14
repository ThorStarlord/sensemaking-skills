# Worker repair I3: three text corrections after independent review

Your reconciliation commit was accepted as applied. An independent reviewer
then found that three of the planner's texts say more than their evidence
supports. All three are the planner's wording, not your edits. Same worktree,
same rules; one commit; no push; no `pytest`.

## Edits

### R1. `.sensemaking/knowledge/stewardship.json`, claim `alternative:read-committed-bytes-from-git-objects`

Set `statement` to:

`Deferred alternative: read committed bytes from Git objects instead of checking the commit out, for index building (including the first call of workspace-query) and for orient, check-rules and audit. It would remove the checkout cost, roughly 10 s of a 15 to 20 s first call on the development host. The builder reads and fingerprints files from a checkout, and its tracked-file, symlink and filter checks assume one; source fingerprints are taken from checked-out bytes, which Git can convert (line endings, filters), so an object reader would be a second byte path that has to agree with every index already built.`

Set `attributes.scope` to:

`Deferred 2026-11-10 for how a commit is materialized, by the temporary-checkout change and by the workspace-query change; the two records were merged into this one during integration. That object bytes differ from checkout bytes is inferred from the source and was not run; lesson:separate-clone-changes-audited-bytes observed the related fact that checked-out bytes vary with Git configuration`

### R2. Same file, claim `decision:relevance-candidates-separate-from-context`

Set `attributes.composition` to:

`Integrated on 2026-11-10 with decision:verification-relevance-for-unowned-files. On a file no component owns, a verification claim that names the file by exact path is returned in verification_refs, and the records linked from verified components are returned in their categories, so none of them is listed as a candidate; the capability route starts from owning components only and adds nothing there. Candidates exclude every record a category holds, including records the category cut at its limit, which are counted only in that category's omission total. The two routes match citations differently: the verification route needs the exact file: reference, while the citation route also accepts a line or fragment suffix, so a verification claim that cites the file with a suffix is listed as a candidate`

### R3. `docs/semantic-architecture/persistent-knowledge-cli.md`, the "Citation route" bullet

The bullet's last sentence, which you added, reads: `There, verification claims
that name the file are returned in `verification_refs` by the
verification-relevance route, so only citing records of other kinds are listed
here.` It wraps across lines in the file. Replace it with these two sentences,
rewrapped to about 78 columns:

`There, a verification claim that names the file by exact path is returned in `verification_refs` by the verification-relevance route and is not listed here. The two routes match citations differently: that route needs the exact `file:<path>` reference, while this one also accepts a `:line:` or `#` suffix, so a verification claim that cites the file with a suffix is listed here as a candidate.`

## Checks

| Check | Command | PASS when |
| --- | --- | --- |
| C1 | `PYTHONPATH=src python -m sensemaking_skills.cli semantic knowledge-proposal-check --repo . --proposal .sensemaking/knowledge/stewardship.json --json` | `SEMANTIC_KNOWLEDGE_PROPOSAL_VALID` |
| C2 | `git diff --stat`; `git ls-files --eol` on the two files; non-ASCII byte count of the pack | exactly two files; both `w/lf`; 0 |
| C3 | `python scripts/validate-docs-currentness.py --repo-root .`, `python scripts/validate-skill-hygiene.py`, `python scripts/validate-repo.py` | each exits 0 |
| C4 | commit both files with the message below | committed; `git status --porcelain` empty |
| C5 | rerun the probes in the foreground, as one command with a long timeout, into `<scratch>/run3` | 16 PASS, 0 FAIL, 2 INFO; copy the whole table |

Commit message:

```
knowledge: state only what the reconciliation evidence supports

Independent review of the reconciliation commit:

- The Git-objects alternative regains the point that the builder's
  tracked-file, symlink and filter checks assume a checkout, and no longer
  says the object-versus-checkout difference was observed. It was inferred;
  the lesson observed that checked-out bytes vary with Git configuration.
- The composition note drops a point-in-time observation and states two
  things the code does: candidates exclude records a category cut at its
  limit, and the two context-for routes match citations differently.
- The CLI reference says the same about the citation route.

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Report

Same format as your last report: `MODEL`, `EDITS` (R1 to R3), `COMMIT`,
`CHECKS` (C1 to C4), `PROBE TABLE`, `DEVIATIONS FROM CONTRACT`,
`OBSERVATIONS`, `OPEN QUESTIONS`.
