# Frontier P5: multi-branch integration and semantic reconciliation (2026-11-10)

**Result.**

- **Candidate:** four of five open product pull requests are integrated on one branch, opened as draft [PR #806](https://github.com/ThorStarlord/sensemaking-skills/pull/806). `NOT MERGED`: merge authority was not granted.
- **Selection:** PRs 804, 801, 795 and 796 selected; PR 797 deferred; none rejected or superseded.
- **Textual conflicts:** two, both predicted before any branch existed and resolved as planned.
- **Semantic reconciliation:** three record-level problems that a clean textual merge leaves behind were found by reading the records, and reconciled. A bounded independent review then corrected three of the planner's reconciliation texts and found a fourth interaction the planner had missed.
- **Architecture:** the integration order, the two resolutions and the deferral survived a trial merge, real-CLI probes and review. Nothing was reversed.
- **Verification:** 16 of 16 cross-PR probes pass on the final head `e395fdd2`. Hosted CI passed in full at `7ae459d4`, whose code is the same; that was the first run of PR 795's tests against PR 796's code. Section 6 has the state at the final head.

The owner-supplied mission asked whether the planner can plan and supervise a coherent integration of independently developed changes with overlapping files, semantic commitments and historical decisions, with integration judgment as the subject.

## Identities

| | Planner | Worker | Reviewer |
| --- | --- | --- | --- |
| Model | `claude-fable-5-2`, effort `xhigh` (stated by the host) | `claude-haiku-5-5` (self-reported; `haiku` tier) | `claude-sonnet-5-5` (self-reported; `sonnet` tier) |
| Context | the desktop session that ran Frontier P4 | one background subagent, resumed twice | fresh, read-only subagent |
| Wrote | assessment, resolutions, record texts, probes, PR text, this record | four merges, every record and documentation edit | the review report |

- **Source:** `origin/main` `baaec6b9`. Heads: 795 `718ea34f`, 796 `de0f64e0`, 797 `ed783524`, 801 `9e0241f2`, 804 `a344381e`.
- **Continuity:** this session also ran P4 and wrote PR 804, so the planner knew that change in detail and the other four only from their sources. It loaded the per-user memory index and wrote nothing to it.
- **CLI:** every run used `PYTHONPATH=src python -m sensemaking_skills.cli`.

## 1. Selected, deferred, rejected, superseded

| PR | Disposition | Reason |
| --- | --- | --- |
| 804 `--temporary-checkout` on orient, check-rules, audit | selected | independent; passes its nine hosted checks |
| 801 `workspace-query` | selected | independent value; interacts with 804 in one line of the Steward Skill and in two records |
| 795 verification context for files no component owns | selected | an owner-requested outcome; edits the same function as 796 |
| 796 relevance candidates in `context-for` | selected | its own decision record names "PR 795 merges" as the trigger to re-inspect how the two compose |
| 797 query-recording facts in the receipt reader | deferred | no file or behavior in common with the other four; its description says the selected outcome was not delivered and raises an owner decision on query receipts; the only one that conflicts with `main` |

PR 797's conflict is in `architecture.json`, where its records and later merged records were appended at the same position. The ids are disjoint and the records unrelated, so it is a keep-both when the owner wants it.

## 2. Initial integration architecture and dependency order

| Interaction | Kind | Planned handling |
| --- | --- | --- |
| 804 with 801, Steward `SKILL.md` line 100 | textual | 801's sentence about `workspace-query` plus 804's corrected sentence |
| 795 with 796, `knowledge_architecture.py` | textual | keep both definition blocks; Git merges the rest of `context_for` |
| 801 and 804 each record "read from Git objects" as deferred | duplicate knowledge record | one record; 801's decision points at it |
| 804 rejects automatic fallback; 801's `workspace-query` does it | apparent semantic contradiction | scope the rejection to the four explicit-identity commands |
| 796's record waits on 795, which added no record | missing record, fired trigger | write the decision record; record the observed composition |
| 795's tests never ran against 796's code | verification gap | read the tests and predict; hosted CI on the candidate decides |
| 796 lists the hosted consumer's limit of 50 as a growth risk | cross-PR verification gap | replay the consumer's eleven queries on the combined records |

**Order:** 804, 801, 795, 796. No pair depends on another for correctness; the order only fixes which side of each conflict is "ours". One worker did the merges in sequence. Two parallel workers were considered and declined: the groups are independent, but the work is small and a join step would have cost more than it saved.

**Challenge before delegating.** A chained `git merge-tree` over the four heads, with no branch created, showed exactly the two predicted conflicts, no additional conflict from three-way adjacency, and no duplicate record id across packs. The planner read PR 795's added tests against PR 796's code and predicted they pass. No large-model critic was used on the plan; these checks answered the same questions for less.

## 3. Delegated responsibilities and results

| Step | Responsibility | Result |
| --- | --- | --- |
| [I1](2026-11-10-frontier-p5-multi-branch-integration-evidence/worker-contract-i1-merge-v1.md) | four merges with two prescribed resolutions; validators; the planner's probes | as specified; 15 of 16 probes, the one failure being the expected duplicate alternative |
| [I2](2026-11-10-frontier-p5-multi-branch-integration-evidence/worker-contract-i2-reconcile-v1.md) | four record and documentation reconciliations, one commit | as specified; 16 of 16 probes |
| I3 | three text corrections after review, one commit | as specified; 16 of 16 probes |

Record reconciliation was a second step on purpose: its text depended on how the merged code actually behaved. The planner made no source, record or documentation edit.

## 4. Newly discovered incompatibilities and invalid assumptions

| Finding | Found by | Disposition |
| --- | --- | --- |
| The two `context-for` routes match citations differently: 795 needs the exact `file:<path>` reference, 796 also accepts a `:line:` or `#` suffix. A verification claim citing a file with a suffix is listed as a candidate, not as verification context | reviewer | not repaired in code; stated in the record and the CLI reference. No verification claim in this repository's records uses a suffix (73 other claims do) |
| With both routes merged, `tests/test_semantic_knowledge.py` lists no candidates, where 796 alone listed three; they are now context through verified components | probes | expected composition; written into the PR, not the record |
| 796's new anchor makes `component:knowledge-store` a verified component for that test file | probes | as 796's author predicted |
| The planner's merged alternative said the object-versus-checkout byte difference "has since been observed" | reviewer | wrong: it was inferred; the lesson observed that checked-out bytes vary with Git configuration. Corrected |
| The planner's sentence "only citing records of other kinds are listed here" | reviewer | too strong, for the reason in the first row. Corrected |

## 5. Fundamental architectural changes

None. The selection, the order, both resolutions and the deferral were kept. The planner declined one change the review made possible: aligning 795's citation matching with 796's. Neither pull request's review or tests covered it, local tests are not run under the construction policy, and no real record is affected.

## 6. Verified combined outcome

| Level | Finding |
| --- | --- |
| Source compatibility | All four heads are ancestors of the candidate; no conflict marker; `ruff` clean on the five touched source files |
| Behavioral correctness | 16 of 16 probes on the real CLI at `e395fdd2`: the hosted consumer's eleven queries pass on the combined records (largest path 29 claims and 25 relations against 50); `workspace-query` carries both `context-for` extensions and equals the two-step context; the two routes report no record twice on owned and unowned files; an unowned, uncited file stays empty; limit-1 output keeps 795's support rule and discloses every omission; `--temporary-checkout` works on the combined code |
| Semantic consistency | `knowledge-proposal-check` valid for every pack; one Git-objects alternative; a file-first query on `semantic_cli.py` returns both decisions; the audit of `main` against the candidate lists as revised exactly the records the four pull requests and the reconciliation revised |
| Hosted verification | At `7ae459d4`, whose code is identical to the final head: all three workflows passed, including the full test suite, so PR 795's tests have now run against PR 796's code. At the final head `e395fdd2`, which changes one pack's text and one documentation sentence: the context consumer and the release distribution passed, and Product Validation was still running when this was written |
| Independent review | The reconciliation commit only, by a separate model. The merges and probes were not independently re-run |
| Authorized merge readiness | Not established. PR 806 is a draft, and merge is the owner's decision |

## 7. Independent review and unresolved limitations

The [reviewer](2026-11-10-frontier-p5-multi-branch-integration-evidence/reviewer-report.md) judged six claims: three sound, three needing repair, all three repaired. It called the deferral of PR 797 defensible. It did not run the CLI or the tests, and did not compare the new decision record's rejected alternatives with PR 795's note.

**Unresolved:**

- `decision:verification-relevance-for-unowned-files` was written by the integrator from PR 795's decision note. The owner should confirm it.
- The citation-matching seam between the two routes stays in the code.
- No hosted test exercises the two `context-for` extensions together; the probes do, and they are not part of the repository's suite.
- PR 797 still needs its rebase and the owner's decision on query receipts.

## 8. Planning failures, worker failures and recovered errors

| # | Failure | Found by | Class |
| --- | --- | --- | --- |
| 1 | Merged alternative dropped the builder's checkout assumptions and overclaimed an observation | reviewer | planning |
| 2 | A point-in-time observation written into a durable record | reviewer | planning |
| 3 | A documentation sentence stronger than the code | reviewer | planning |
| 4 | The citation-matching seam was missed when the planner read both implementations | reviewer | planning |
| 5 | The contract quoted a sentence as one line that wraps in the file, so the worker's first edit of it failed | worker | handoff |
| 6 | The contract did not say how to run a long command; the worker polled a background run for many tool calls | planner, from the usage report | handoff |
| 7 | The worker ran `py_compile` on a Markdown file, noticed, and moved on | worker | execution |

No worker result had to be redone. Every repair was to text the planner supplied.

## 9. Resource consumption

| Agent | Tokens (host-reported) | Tool calls | Run time |
| --- | --- | --- | --- |
| Worker, I1 | 88,642 | 17 | 220 s |
| Worker, I2 | 125,923 | 35 | 664 s |
| Worker, I3 | 134,888 | 5 | 191 s |
| Reviewer | 98,949 | 10 | 56 s |

- The worker's later figures probably include its resumed context, and its I2 figures include I1's; the host does not separate them.
- **Planner:** about 677,000 tokens in its context window when the reconciliation was delegated, carried over from P4. Currency cost per agent is not observable.
- **Counts:** two agents started; three worker steps; one review; two contracts and one repair message; three text repairs; no rework of a merge.
- **Wall time:** about 30 minutes from the mission's first command to the record, of which about 18 minutes was the worker running.
- **Large-model work avoided:** no pre-implementation critic, no parallel workers, no reviewer on the merges. The planner's own largest cost was reading five implementations and their records, which the mission required.

## 10. What this does and does not show

| Question | Finding |
| --- | --- |
| Can the planner tell a textual merge from a coherent product? | Yes, here. All three record-level problems were found before delegation by reading records, not diffs |
| Did the plan survive contact with the merged code? | Yes. Two conflicts predicted, two found; probes behaved as predicted |
| Was the planner's reconciliation text reliable? | No. Three of four reconciliations needed an independent correction |
| Did the planner find every interaction? | No. A separate model found the citation-matching seam |
| Is the integration complete? | No. It is prepared, probed, hosted-checked at a code-identical head and reviewed in part; the last hosted run on the final head and the owner's decision are outstanding |

**Highest demonstrated planning capability:** treating four individually passing changes as one product: predicting every textual conflict without building a branch, finding the duplicate record, the scoped contradiction and the fired trigger from the records themselves, and sequencing reconciliation after observed behavior instead of writing it from the pull requests' intentions.

**Remaining frontier:**

- Reconciliation text the planner writes about code it has only read is still overconfident; in P4 and here an independent reader corrected it.
- An integration in which two changes are behaviorally incompatible, so that one must be revised or declined.
- Independent re-execution of the merges and probes, not only review of the records.
- Integration across a change the planner did not also write.

## Observations for the owner (no action taken)

- Merging PR 806 with a merge commit marks PRs 804, 801, 795 and 796 as merged. Merging them one by one instead needs the two resolutions and the two reconciliation commits from this branch.
- The citation-matching seam is one line: `_test_evidence_verifications` compares the exact `file:<path>` string, where `_evidence_paths` strips a line or fragment suffix.
- PR 797 waits on your decision about query receipts, and then on a rebase.
