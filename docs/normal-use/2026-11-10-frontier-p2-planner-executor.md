# Frontier P2: planner and lightweight executor (2026-11-10)

**Result.**

- **Responsibility:** built, reviewed and opened as [PR #801](https://github.com/ThorStarlord/sensemaking-skills/pull/801). `NOT MERGED`: merge authority was not granted in this session.
- **Worker outcome:** the lower-cost worker wrote every source and documentation edit in two iterations. Its first pass met all 18 contract checks and all 50 runnable checks of the planner's independent review.
- **Where the defects came from:** review found six defects. Five were gaps in the planner's contract; one was a worker error in a help string. All six were repaired in the second iteration.
- **Is cheaper execution better?** `NOT TESTED`. No control arm ran, so nothing here compares outcome or cost with a planner-only or worker-only run.

The owner-supplied mission asked whether a stronger model can design and supervise a substantial engineering implementation that a lower-cost model executes, and asked that the planner's judgment be the subject, not its code volume.

## Identities

| | Planner, architect, reviewer | Implementation worker |
| --- | --- | --- |
| Model | `claude-fable-5-2` (stated by the host) | `claude-haiku-5-5` (self-reported; requested as the Agent tool's `haiku` tier) |
| Instance | desktop Code session, one context | one background subagent, resumed once with its context |
| Wrote | selection, contract, review harness, knowledge records, PR text, `STATUS.md` note, this record | all five source and documentation files of the change |
| Source | `origin/main` `baaec6b9` -> branch `claude/workspace-knowledge-query`, head `9e0241f2` | the same worktree; it did not commit |

- **Installed Skill:** the host-loaded `using-sensemaking` copy was older than `baaec6b9` (42,291 bytes against 46,031).
- **CLI:** every run used `PYTHONPATH=src python -m sensemaking_skills.cli`; the `sensemaking-skills` on PATH is a stale tool install.
- **Shared memory:** this session loaded the per-user memory index, which carries facts about earlier PRs. It wrote nothing to it.

## What was selected, and why

`STATUS.md` names the PATH-1 decision-changing uncertainty as whether accreted knowledge is reached before a decision. Three sources pointed at one concrete obstacle:

- The RECALL reference tells agents to prefer raw records when an index is missing, and says routine edits should not need an index-building stage.
- The [Frontier 04 record](2026-11-10-frontier-04-semantic-continuity.md) observed a fresh session that never queried before designing.
- A live run at `baaec6b9` needed two commands and eight identity arguments: 5.7 s to build on a clean checkout, 15.1 s through a temporary checkout, and 3.6 s per query.

The selected responsibility was a zero-setup command, `semantic workspace-query`, that resolves those arguments itself and keeps a derived index per commit.

**Candidates set aside:**

- A pull-request-time check for records made stale by a change. It needs a new hook or CI commitment, which is a ratification matter. The selected command serves the same need on request with `--operation workspace-impact --ref <base>`.
- The two minor `setup-skills` follow-ups from Frontier 04. They are small repairs and repeat the previous session's subsystem.
- Guidance only. The setup cost would remain.

**Design alternatives** are recorded in `.sensemaking/knowledge/architecture.json` by PR #801: optional identity arguments on `knowledge-query` (rejected), a snapshot built from Git objects (deferred), and a throwaway index per call (rejected).

**Recall before design.** A `context-for` query on the files to be touched returned `rule:frozen-public-python-api`, `inv:index-snapshot-vs-working-overlay` and `decision:index-from-temporary-worktree` with its rejected alternatives. All three became contract invariants. This is one same-session instance of a record reaching a design before it was set; it is not independent evidence.

## The contract

[worker-contract-v1.md](2026-11-10-frontier-p2-planner-executor-evidence/worker-contract-v1.md) holds:

- 14 fixed decisions and eight invariants;
- five permitted files, with line fences that keep clear of draft PRs 795, 796 and 797;
- what the worker may decide and when it must stop and report;
- an 18-check verification matrix on the real CLI, with no unit tests, under the construction policy;
- a literal report format.

## What the worker did

| Iteration | Input | Output | Usage reported by the host |
| --- | --- | --- | --- |
| 1 | contract v1 | new module, the command, three documentation edits; 18 of 18 checks reported as passing; three disclosed deviations; one question about exception types | 166,735 tokens, 28 tool calls, 515 s |
| 2 | [repair message](2026-11-10-frontier-p2-planner-executor-evidence/worker-repair-1.md) with six items, each with evidence | all six repaired; six verification steps reported as passing | 199,596 tokens, 20 tool calls, 170 s |

The second token figure may include the resumed context of the first; the host does not separate them.

**Deviations, all accepted:**

1. An out-of-range derived label falls back to the directory name instead of raising.
2. An explicit label is stripped of surrounding whitespace.
3. The POSIX directory mode is applied to the two cache directories, not to their ancestors.

The worker stayed inside the five files, changed no existing line of `semantic_cli.py`, reported its own two invocation mistakes, and raised an observation that a reused cache is trusted as written. That observation became a documented limit.

## Review and defect attribution

The planner read the full diff, ran its own [review harness](2026-11-10-frontier-p2-planner-executor-evidence/planner-review-harness.py.txt) against the real CLI (50 pass, 0 fail, 1 not run, before and after the repair), and then ran four probes aimed at what the contract had not asked for.

| # | Defect | Found by | Attribution |
| --- | --- | --- | --- |
| 1 | A malformed origin with embedded credentials printed the token and host in the label | planner probe | planning: the label rule in the contract produced it |
| 2 | A Windows junction in the cache path was accepted and redirected the database | planner probe | planning: the contract said "symlink" although Frontier 04 had already flagged junctions |
| 3 | A cache file with a valid header and no tables failed with a bare SQLite message | planner probe | planning: the contract named one exception type |
| 4 | `rules-for` with a backslash path silently returned no rules | planner probe | planning: path normalization was scoped to one operation |
| 5 | `--help` did not mention the cache side effect | diff reading | handoff: the requirement was in the planner's notes, not in the contract |
| 6 | The `--term` help named the wrong operation | diff reading | execution |

No defect was traced to the contract being ignored or misread.

**Review limits:**

- The planner wrote both the contract and the harness, so they share blind spots.
- Symlink refusal and POSIX paths were never run.
- The worker's question about wider exception handling was answered without a change: the CLI entry point already reports any exception as a one-line error, and three malformed-record probes surfaced as `ValueError`.

## Plan revisions

One planner intervention carried four revisions to fixed decisions, each with the probe output that made the earlier text insufficient:

- the label derivation (credentials);
- the link check (junctions);
- the cache probe's exception handling;
- path normalization for `rules-for`.

No architectural decision was reversed, and no investigation or second review was delegated.

## Costs

| | Observed | Not observable here |
| --- | --- | --- |
| Worker | the usage figures above; about 11.4 min of wall time over two iterations | currency cost |
| Planner | about 454,000 tokens in the context window when the PR was opened; one repair message; three small follow-up commits | cumulative billed tokens, currency cost, exact planning time |

The planner's context held far more tokens than the worker reported. The planner's share was reading, selection and review; the worker's share was the edits and their verification.

## What this does and does not show

| Question | Finding |
| --- | --- |
| Can the lower-cost model execute a tightly specified, composition-style change in this codebase? | Yes, once, with a clean first pass against the contract. |
| Was the initial contract sufficient? | No. Five of six defects were contract gaps, found only by review probes. |
| Where did the planner add value? | Selection from source evidence; three constraints recovered before design; fences around three in-flight PRs; adversarial review. |
| Does the split beat a single model on outcome or cost? | `NOT TESTED`. No planner-only or worker-only control ran. |
| Does `workspace-query` make agents consult records earlier? | `NOT TESTED`. |
| Was the responsibility completed under repository policy? | Own `claude/<topic>` branch, decision note, real-path verification, knowledge reconciled, unit tests `NOT_RUN` by policy, hosted CI pending when this was written, merge left to the owner. |

**Confounds:**

- n = 1.
- The planner chose a task that composes existing functions, which favors a contract-driven worker.
- One vendor's model family on both sides.
- The planner knew the repository's conventions from records and earlier session notes.

## What a later run needs

- A control: the same contract executed by the planner model, or the same responsibility given to the worker without a contract, to compare outcome and cost.
- A reviewer that did not write the contract.
- A task that is not mostly composition, to see where the lower-cost model's limit lies.
