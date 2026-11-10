# Frontier Challenge 04: autonomous semantic continuity (2026-11-10)

**Result.**

- **Continuity of engineering context:** `POSITIVE`. This is observational, from one run.
- **Decision benefit from reviewed knowledge records:** `NOT DEMONSTRATED`.
- **Advantage over a source-only agent:** `NOT TESTED`.

A separately started, fresh-context session found the previous session's merged work through ordinary Git and GitHub. It checked the evidence it relied on and built a correct extension. Nothing shows that the reviewed records in `.sensemaking/knowledge/` changed any of its decisions: the same facts reached it first through PR text and a code docstring.

The owner-supplied challenge asked whether an autonomous agent can create engineering value and durable knowledge that stays correct, discoverable and consequential across genuinely independent sessions. This record keeps the narrower claim the evidence supports. The independent evaluation it rests on is [C-evaluation.md](2026-11-10-frontier-04-semantic-continuity-evidence/C-evaluation.md).

## Identities

| | Phase A (construction) | Phase B (re-entry) | Phase C (evaluation) |
| --- | --- | --- | --- |
| Session | desktop session `local_03a0f64e`, CLI `0587b931` | desktop session `local_95510b04`, CLI `957e2b45`, started by Phase A with `context: fresh` | fresh-context child subagent of Phase A |
| Model, effort | `claude-opus-5-5`, `xhigh` | same | same model |
| Source | `origin/main` `53b667c1` -> PR #798 merged `7e5bff39` | worktree from `7e5bff39` -> PR #799 merged `71746bd4` | read-only at `71746bd4` |
| Installed `using-sensemaking` | differed from `53b667c1` (missing the 2026-11-06 orientation and abductive guidance); loaded by the host | not invoked | not applicable |
| PATH CLI | `sensemaking-skills` on PATH is a uv-tool install pinned to `6f54a4a7`; both builders ran `PYTHONPATH=src python -m sensemaking_skills.cli` | same | same |

Phase A first took the PATH CLI for the editable install of the primary checkout; Phase B identified it correctly as a uv-tool install. That was a working belief, never retained.

## Phase A: what was built

[PR #798](https://github.com/ThorStarlord/sensemaking-skills/pull/798) came from real friction on this host. A dry run of `setup-skills --target claude --scope user` reported 24 of 52 Skills as diverged and 4 as missing, including the entrypoint. It said nothing about which copies held local edits, and `--force` replaces all of them.

The PR adds a per-root install record (`.sensemaking-skills-install.json`) and classifies a divergent copy as `outdated`, `changed` or `unrecorded`. It also adds `--update`, which replaces only `outdated` copies.

**Errors and rework, all before merge:**

1. Phase A added names to the frozen `setup_skills.__all__` and changed `copy_skill`'s signature. Hosted CI caught it (run 42759558168, one failure in 3,634 tests). The fix moved the new helpers behind private names.
2. A separate reviewer subagent found four more defects, all fixed: a temporary file that a planted link could redirect, a junctioned Skill directory classified as `outdated`, wrong refusal counts, and a stale doc line.
3. A Python rewrite turned `architecture.json` and the byte-pinned `INSTALLATION.md` into CRLF files. Phase A caught and reverted it.

**Uncorrected until Phase C:** the PR said "27 of 52" diverged; the dry run shows 24. The PR description now carries a dated correction.

## Retained knowledge and its basis

The records were added in `.sensemaking/knowledge/architecture.json` at `7e5bff39`.

| Record | Basis | Phase C check at `7e5bff39` |
| --- | --- | --- |
| `component:distribution-setup` (REVISE) | code | correct; pinned to an intermediate commit |
| `decision:install-record-classifies-divergent-skill-copies` | delegated design, real CLI runs | correct; `known_limits` overstated the `--sync` case |
| `alternative:per-skill-install-marker` (rejected) | the fingerprint covers every file | correct |
| `alternative:replace-outdated-skill-copies-by-default` (deferred) | documented fail-closed default | correct |
| `rule:frozen-public-python-api` | Phase A's own CI failure, the manifest and the contract test | correct |
| `verification:public-api-contract-test` | test source and the CI failure | correct |

Two consequential items lived only in the PR #798 description:

- this host's unrecorded root is still refused by `--update`;
- the rejected "historical fingerprint catalogue" alternative.

These turned out to be the clearest influence on Phase B.

## Phase B: setup and what happened

The [brief](2026-11-10-frontier-04-semantic-continuity-evidence/phase-b-brief.md) described only the real problem: stale installed Skills, refresh them without losing local edits. It named no PR, record, mechanism or experiment.

**Selection confound:** Phase A chose this task knowing that its own change left this host's root unserved.

**Channels checked:**

- The shared auto-memory index carried no Phase A content; it was last written before Phase A began.
- The app's side-session notes folder was empty when Phase B started.
- The worktree name the app assigned, `cross-session-fresh-b-0f261e`, came from an earlier experiment. It is a framing cue, not content.

Timeline (UTC, from the transcript):

| Time | What happened |
| --- | --- |
| 05:14:19 | 21 s in: `git log` and `gh pr view 798`. #798 was the head merge. |
| 05:14:52 | Direction set from the PR text and `setup_skills.py`: "this host has none yet … check whether those copies match past packaged versions in Git history". |
| 05:15 to 05:28 | Own discovery: 13 copies match a commit exactly, 10 differ only in CRLF, 1 has a nested duplicate directory. |
| 05:30:01 | First read of the knowledge records, by the IDs the PR body listed. |
| 05:30:07 onward | Implementation. The frozen-API constraint came from Phase A's code comment; Phase B checked the manifest and the test itself. |
| 05:40:43 | Merged [PR #799](https://github.com/ThorStarlord/sensemaking-skills/pull/799). `--update` now also replaces an unrecorded copy that equals a committed version. The full suite was pending and passed 32 s later. |

Phase B never invoked a Sensemaking Skill or the Steward's RECALL before deciding, and wrote no session receipt. It ran `knowledge-build` and `context-for` only to confirm its own new records could be retrieved.

It reconciled the records consistently: it revised the component, added a decision linked to Phase A's, and recorded a rejected backfill alternative. It left Phase A's decision statement saying unrecorded copies need `--force`, which #799 made untrue.

It also updated a shared memory file with PR 798/799 facts. Any later "fresh" session on this host starts with them.

**Interventions:** the owner sent "Tente novamente" after Phase B's usage limit, and "the credits are refreshed" to Phase A. Neither carried task content.

## Corrections made after Phase C

- REVISE `decision:install-record-classifies-divergent-skill-copies`:
  - the statement now scopes the `--force` requirement for unrecorded copies to this decision alone and names the PR #799 decision;
  - `known_limits` now states when a `--sync` copy reads as `changed`.
- PR #798's description: the "27 of 52" correction above.

## What this does and does not show

| Owner distinction | Finding |
| --- | --- |
| Retrieval vs use | Records were retrieved and used as reconciliation targets, but only after the design was set. |
| Use vs decision benefit | No Phase B decision is shown to have changed because of a record. |
| Source validity vs semantic correctness | The records were valid and essentially correct. One became stale through Phase B's own change, and Phase B did not revise it. A false figure in PR text survived until Phase C. |
| Coding success vs continuity | The coding task succeeded. Continuity ran through Git, PR text and code comments, not through the knowledge mechanism. |
| Independent instance vs child subagent | Phase B was a separately instantiated session with fresh context, though not independently commissioned. The reviewer and the evaluator were child subagents of Phase A. |
| Usefulness vs causal superiority | No matched source-only comparison was run. A source-only agent would have seen the same head merge, PR text and docstring, so no advantage of the records can be claimed. |

**Confounds:** same model and effort; Phase A chose the task and wrote both briefs; recency made #798 the obvious entry; n = 1.

## Costs

Figures are from the evaluator, which deduplicated tokens by message ID.

| | Wall time | Tool calls | Output tokens | Cost |
| --- | --- | --- | --- | --- |
| Phase A build | 30 min | 159 | 118,826 | $12.56, with the reviewer |
| Phase A reviewer | 7.4 min, in parallel | 37 | 35,229 | (included above) |
| Phase B | 28 min, about 18.5 active | 98 | 71,311 | $5.17 |
| Phase C evaluator | about 16 min | 72 | not separated | not separated |

## What a later run needs

- A record can only change a decision if it is reached before the decision. Here the fresh agent's first moves were `git log` and the PR description, and it never ran RECALL or `context-for` before designing.
- The facts Phase B used were all in the PR description and a code docstring. This is evidence for writing decision notes and docstrings well. It is not evidence that the knowledge graph adds anything they do not.
- To test whether records themselves help, the decisive fact must exist only in a record and not in code or PR text, or a matched source-only session must run. Both are the conditional diagnostics in the [unfamiliar-case design](../superpowers/specs/2026-11-05-unfamiliar-case-semantic-transfer-design.md). Neither is an automatic next step.
- Independence on this host has channels besides Git: the auto-memory index every session loads, the app's side-session notes folder, and reused worktree names. Check them before and after each run.

**Open, minor (from Phase C, PR #799):**

- With only `historical` refusals, the summary still suggests `--force`.
- The Git history lookup runs on every source-checkout run, about 0.5 s per unrecorded copy.

**Owner's choice:** refreshing the real `~/.claude/skills` root with `--dry-run --update`, then `--update`, and inspecting `strategic-repository-analysis` by hand.
