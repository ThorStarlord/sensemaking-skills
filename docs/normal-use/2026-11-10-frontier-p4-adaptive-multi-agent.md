# Frontier P4: adaptive multi-agent engineering (2026-11-10)

**Result.**

- **Responsibility:** built, independently reviewed, repaired and opened as [PR #804](https://github.com/ThorStarlord/sensemaking-skills/pull/804). `NOT MERGED`: merge authority was not granted in this session.
- **Admission:** a fresh-context operator subagent chose the task, not the planner. Its independence is context-level only; no owner or separate operator admitted it. The operator placed the task at the lower edge of "substantial".
- **Workers:** two lower-cost workers wrote every source and documentation edit, concurrently, in separate worktrees. The code worker took two iterations and the documentation worker three.
- **Where the defects came from:** 16 defects or failures were recorded. Eleven trace to the planner's decisions or contract text, two to worker execution, one to the host and two to review tooling or evidence.
- **Adaptation:** three plan revisions, each caused by evidence; the core architecture was never reversed.
- **Is the split better or cheaper than one model?** `NOT TESTED`. No control arm ran.

The owner-supplied mission asked whether the planner can direct a multi-stage engineering mission through lower-cost implementation workers while adapting to new evidence, failures and changing constraints, with the planner's judgment as the subject.

## Identities

| | Planner | Operator | Workers W1 and W2 | Reviewer |
| --- | --- | --- | --- | --- |
| Model | `claude-fable-5-2`, effort `xhigh` (stated by the host) | `claude-opus-5-5` (self-reported; requested as the `opus` tier) | `claude-haiku-5-5` (self-reported; requested as the `haiku` tier) | `claude-opus-5-5` (self-reported) |
| Context | one desktop Code session | fresh, read-only subagent | two background subagents, each resumed with its context | fresh, read-only subagent, resumed once |
| Wrote | contracts, repair messages, knowledge records, probes, PR text, this record | the admission report | all source and documentation edits | the review report |

- **Source:** `origin/main` `baaec6b9` -> branch `claude/temporary-checkout-pinned-readers`, head `a344381e`.
- **Skill:** the planner read the checked-in `using-sensemaking` by hand: the whole file at a stale local revision, then its diff to `baaec6b9`. No host-loaded copy was used.
- **CLI:** every run used `PYTHONPATH=src python -m sensemaking_skills.cli`; the `sensemaking-skills` on PATH is a stale install.
- **Shared memory:** the session loaded the per-user memory index, which carries notes about earlier PRs, so the planning context was not fully fresh. It wrote nothing to it.
- **Model identity:** worker, operator and reviewer models are self-reports from their own system prompts. A one-command probe confirmed the `haiku` tier before any work was delegated.

## 1. The engineering responsibility

The mission supplied no admitted task. The planner started an operator subagent on a different model with seven admission criteria, a read-only mandate and no hint of what the planner would pick. Its [report](2026-11-10-frontier-p4-adaptive-multi-agent-evidence/operator-admission-report.md) admitted one outcome:

> `knowledge-orient`, `knowledge-audit` and `knowledge-check-rules` can be used on committed revisions while the checkout has uncommitted or untracked files, keep reading only committed bytes, say plainly that working changes were not read, and the guidance that contradicts itself on this point becomes consistent.

It also wrote nine acceptance conditions, which the planner kept away from the workers and gave to the reviewer.

**The planner's check before accepting it:**

- All three commands failed in the planner's own worktree, whose only change was the session receipt.
- None had a `--temporary-checkout` flag, and no open PR touched them.
- `STATUS.md` names RECALL -> BUILD -> RECONCILE as the current construction responsibility, and the receipt contract makes every session's checkout dirty.

**Limits of the admission:** the operator was started by the planner's session and read the same repository. The task composes an existing mechanism, as the P2 task did.

## 2. Initial architecture and plan

**Recall before design.** A `context-for` query on five files returned `decision:index-from-temporary-worktree`, two rejected alternatives, `inv:index-snapshot-vs-working-overlay` and `rule:frozen-public-python-api`. The design extends that recorded decision; it adds no mechanism.

**Decisions the planner reserved:**

| Decision | Reason |
| --- | --- |
| Opt-in `--temporary-checkout`, not an automatic fallback | three hosted tests assert the dirty-checkout refusal; the recorded decision says the clean-source check stays unchanged |
| Reuse `temporary_commit_checkout`, not a Git-object reader | fingerprints are taken from checked-out bytes; a second byte path would have to agree with every existing index |
| Default output byte-identical; two new keys only under the flag | the operator's condition 8 |
| A neutral `active_checkout` block, not the existing `workspace_context` | in an audit, `workspace_context.indexed_ref` would have named the current ref next to a top-level `indexed_ref` |
| Fences around regions that PRs 801, 796 and 795 edit | avoid new merge conflicts |

**What the planner found that the operator had not:** the three tests that pin the refusal, three literal phrases a hosted test requires in the Steward `SKILL.md`, and the record properties another test checks.

**Delegated to the workers:** helper names and shape, step order, option placement, sentence wording.

**Stated as invalidating the plan:** a need to change a file outside the contract, or a fixed decision that the code could not satisfy.

## 3. Worker task decomposition

| Worker | Responsibility | Scope | Contract |
| --- | --- | --- | --- |
| W1 | the flag, disclosure and hint | `src/sensemaking_skills/semantic_cli.py` | [8 decisions, 7 invariants, 11 real-CLI rows](2026-11-10-frontier-p4-adaptive-multi-agent-evidence/worker-contract-w1-code-v1.md) |
| W2 | one consistent clean-checkout rule | six guidance and documentation files, 11 sites | [interface, site table, fences, 8 checks](2026-11-10-frontier-p4-adaptive-multi-agent-evidence/worker-contract-w2-docs-v1.md) |

The two ran concurrently because the planner had fixed the interface they shared: flag name, payload keys and hint text. Each had its own worktree, so the code worker's "checkout untouched" checks could not be disturbed by documentation edits. Neither committed; the planner committed after reading each diff.

**Not delegated:** the knowledge records, integration, the PR text and this record. The planner made no source or documentation edit.

## 4. Consequential implementation discoveries

| Discovery | Found by | Effect |
| --- | --- | --- |
| This host's system `core.autocrlf` is `true`. A plain clone checks out CRLF, and `knowledge-audit` from it reported 442 of 442 records changed, against 139 of 442 from a worktree of the repository | planner, while building a clean reference | the "separate clean clone" workaround gives a wrong audit here; plan revision 1 |
| The operator's own evidence run used such a clone, and its condition 1 named a clean clone as the reference | planner | the reviewer was told, with the evidence, and verified it |
| A refusal sentence in `repository-bootstrap.md` was missing from the planner's site list | W2 | added in repair round 1 |
| Computing the disclosure first would have changed the error for a malformed ref | W1, during its repair round | W1 added a ref check that keeps the existing message, and reported it |
| The reviewer was cut off by the account's usage limit before it ran anything but reads | host | resumed with its context; it found nothing half-made |

## 5. Plan revisions

| # | Revision | Evidence that caused it |
| --- | --- | --- |
| 1 | Add a documentation statement and a lesson record on why a separate clone is not equivalent; tell the reviewer that a default clone is not a valid reference | the 442 against 139 measurement |
| 2 | Reverse the fence on `SKILL.md` line 100 and accept a one-line conflict with PR 801 | the reviewer's failed condition 9: the core Skill still contradicted itself |
| 3 | Build the disclosure before the checkout, add a `note`, give `knowledge-build` the hint | reviewer findings 2, 3 and the weak pass on condition 4 |

**Kept against a finding:** default output stays byte-identical, so `knowledge-build` reports `source_checkout` always and the other three only with the flag. The audit still pays for its checkout before validating `--db`. Both are stated in the PR.

**Never revised:** the opt-in flag and the reused worktree mechanism. The reviewer agreed with both.

## 6. Actual integrated outcome

| State | Finding |
| --- | --- |
| Implemented | Six commits on `claude/temporary-checkout-pinned-readers`, head `a344381e`: one source file, six guidance files, one knowledge pack |
| Checked by the planner | 19 of 19 real-CLI probes on the final code; seven repository validators and `ruff` before and after; `knowledge-proposal-check` valid |
| Independently verified | At `3c6ba4fc` only: eight of nine conditions passed. The three repair commits after it were not independently re-reviewed |
| Hosted CI | All nine checks passed at `3c6ba4fc` and again at the final head `a344381e`, including the full test suite. No hosted test exercises the new flag |
| Integrated | No. PR #804 is open and unmerged |
| User-beneficial | Used once in this session: the new audit, run from a dirty checkout at the base commit, flagged exactly the three records the planner had revised. Use by another agent is `NOT TESTED` |

After the record change, `context-for` on `semantic_cli.py` returns the decision, four alternatives and the invariant. Before it, that path returned none of them, which the query receipt records as a miss.

## 7. Independent review findings and repairs

The [reviewer](2026-11-10-frontier-p4-adaptive-multi-agent-evidence/reviewer-report.md) received the operator's conditions, the claimed design and the host facts, and not the planner's verification rows. Verdict: `ACCEPT_WITH_REPAIRS`.

| # | Finding | Severity | Disposition |
| --- | --- | --- | --- |
| 1 | `SKILL.md` line 100 still says orient, build and audit require a clean checkout | SHOULD_FIX | repaired (revision 2) |
| 2 | `knowledge-build` refusal has no hint; output shape differs across the four commands | NOTE | hint added; shape difference documented |
| 3 | Disclosure runs after the checkout; an unborn HEAD fails late and tersely | NOTE | order repaired; the terse message stays |
| 4 | Audit pays for the checkout before validating `--db` | NOTE | accepted limit |
| 5 | The lesson says "every cited source" and its counts name no revision | NOTE | repaired in the record and the reference |
| 6 | `knowledge-proposal-check` limit text is loosely stale | NOTE | predates the change; not touched |
| 7 | No test covers the flag on any of the four commands | NOTE | left under the construction policy |

The reviewer also confirmed the line-ending claim on its own clone, and found that the flag does not help there: a clone under another `core.autocrlf` reports text files changed with or without it. The lesson now says so.

## 8. All defects and failures, by class

| # | Defect or failure | Found by | Class |
| --- | --- | --- | --- |
| 1 | Contract sentence "no command reads dirty bytes" is false; `knowledge-proposal-check` reads a dirty file | planner, reading the diff | planning |
| 2 | "against clean HEAD" survived in `bootstrap.md` | planner, reading the diff | handoff |
| 3 | A refusal sentence missing from the site list | W2 | planning |
| 4 | Two line numbers in the contract off by one | W2 | handoff |
| 5 | One sentence left as an over-long line | planner, reading the diff | execution |
| 6 | `SKILL.md` line 100 fenced and left contradictory | reviewer | planning |
| 7 | Disclosure placed after the checkout | reviewer | planning |
| 8 | Disclosure had fields but no plain sentence | reviewer | planning |
| 9 | `knowledge-build` refusal without the hint | reviewer | planning |
| 10 | Lesson and reference overgeneralized one observation | reviewer | planning |
| 11 | Audit validates `--db` after the checkout | reviewer | planning |
| 12 | The repair message for item 7 would have changed a malformed-ref error | W1 | handoff |
| 13 | W1 ran one row against the stale installed package, noticed and reran it | W1 | execution |
| 14 | Reviewer stopped by the usage limit | host | environmental |
| 15 | A planner probe assumed the worktree HEAD was still the base commit and reported two false failures | planner | review |
| 16 | The operator's evidence audit ran in a CRLF clone without noticing that every record read as changed | planner | review |

No defect came from a worker ignoring or misreading its contract. As in P2, most were gaps in what the planner specified.

## 9. Resource usage and interventions

| Agent | Tokens (host-reported) | Tool calls | Run time |
| --- | --- | --- | --- |
| Operator | 144,201 | 41 | 470 s |
| Worker-tier probe | 68,365 | 1 | 6 s |
| W1, iteration 1 | 119,145 | 21 | 207 s |
| W1, repair 1 | 143,442 | 15 | 158 s |
| W2, iteration 1 | 110,484 | 9 | 127 s |
| W2, repair 1 | 120,404 | 3 | 37 s |
| W2, repair 2 | 133,921 | 3 | 56 s |
| Reviewer | 129,868 | 23 | 458 s |

- The figures for resumed agents probably include their earlier context; the host does not separate them. A one-command probe alone cost 68,365 tokens, so each spawn carries about that much before doing any work.
- **Planner:** about 523,000 tokens in its context window when the PR was marked ready. Cumulative billed tokens and currency cost per agent are not observable here.
- **Wall time:** about 3 h 15 min from session start to this record, of which about 2 h 15 min was spent stopped at the account's usage limit.
- **Counts:** five agents started; two worker tasks; five worker iterations; one environmental retry; two contracts, three repair messages and one reviewer brief from the planner; three plan revisions.

**What needed the larger model, on this evidence:**

- checking the admission against source and open PRs;
- finding the test pins that settled opt-in against automatic fallback;
- recognizing that an all-records-changed audit was a line-ending artifact and what it implied for the design, the reviewer and the records;
- weighing the reviewer's finding against the planner's own fence and reversing it.

**What a lower-cost worker did or could have done:**

- Did: every code and documentation edit, their real-CLI verification, and catching one consequence of a planner instruction.
- Could have, untested here: running the probes, validators and merge checks, assembling the evidence files, and generating the query receipt.
- Unknown: authoring the knowledge records and performing the independent review on a cheaper tier.

## 10. What this does and does not show

| Question | Finding |
| --- | --- |
| Can the planner hold a sound design steady while revising its own decisions on evidence? | Yes, three times in one run, on a small task |
| Did concurrency under a fixed interface work? | Yes. Neither worker waited on the other, and no rework came from interface drift in the first pass |
| Was the initial plan sufficient? | No. Eleven of sixteen recorded defects were the planner's |
| Did independent review change the outcome? | Yes. It failed one condition the planner had knowingly left failing, and four of its findings were repaired |
| Does the split beat a single model on outcome or cost? | `NOT TESTED` |
| Does the new flag make agents run RECONCILE's checks more often? | `NOT TESTED` |

**Confounds:**

- n = 1, one vendor's model family on every side.
- The task sits at the lower edge of substantial and composes an existing mechanism; it did not force an architectural reversal.
- The operator and reviewer were started by the planner's session.
- The repair commits rest on planner probes and hosted CI, not on a second independent review.

**Highest demonstrated adaptive-planning capability:** under a task chosen by another agent, the planner kept a small, recorded architecture intact through delegation while changing three of its own decisions when measurement or independent review contradicted them, and it classified failures by cause instead of retrying them.

**Next unresolved frontier:**

- a task that forces the architecture itself to change mid-flight;
- a control arm, so that cost and outcome can be compared with one model doing the same contract;
- contract quality: in P2 and here, most defects were in what the planner specified. An independent reader of the contract before dispatch is untested;
- admission by an owner or a separately instantiated operator;
- independent re-review of repairs.

## Observations for the owner (no action taken)

- PR 801 and PR 804 both edit `SKILL.md` line 100. Whichever merges second needs a one-line resolution; PR 804's description gives the resolved sentence.
- No hosted test exercises `--temporary-checkout` on any of the four commands, `knowledge-build` included.
- Source fingerprints depend on the checkout's line-ending configuration. An index built in one clone and audited in another with a different `core.autocrlf` reports text files as changed. This predates the change and is now recorded as a lesson.
- The `knowledge-proposal-check` limit text still says full indexing needs a clean committed HEAD.
