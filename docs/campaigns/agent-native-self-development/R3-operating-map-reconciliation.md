# R3: operating-map reconciliation (fresh-context report)

```
STATUS:     campaign evidence, produced verbatim by the R3 fresh context.
            Not edited by the dispatcher. Non-authoritative.
CONTEXT:    a coding-agent context with NO conversation history about the
            campaign, given only the path of CAMPAIGN-STATE.md and the
            worktree H:/GithubRepositories/smk-campaign.
TASK:       CAMPAIGN-STATE.md section 10, R3 (continuation-pattern
            reconciliation into docs/agent-native-operating-workflow.md),
            steps 1-6.
DATE:       2026-09-02
BRANCH:     campaign/agent-native-self-development (HEAD at start: 2adfeaf)
COMMITS:    6ff4a8907ab9b4c19dd886c6d3891ad448eacffd  campaign(R3): reconcile
            demonstrated continuation pattern into the operating map
            + the commit that adds this report (second `campaign(R3):` commit)
```

## Summary

- The record was sufficient to identify R3, its six steps, its sourced
  authority, its explicit not-authorized list, and its stop condition. All
  six steps were performed; none were skipped. Step-2 verification passed
  on all three points (the map text read as described; the retirement-plan
  reopen trigger is about prior *reconciliation-report* identity, which
  R1/R2 did not exercise and which is left unresolved; every R1/R2 fact
  written into the map was checked against the two report files).
- Exactly one product file changed: `docs/agent-native-operating-workflow.md`
  (+88/-3): a dated `####` subsection under section 2 CONTINUATION (the
  existing principle and cross-run-identity text kept verbatim), three
  Reality-map rows, and one section-6 bullet. No other file was edited; no
  machinery, Skill, schema, validator, or hook was added; ADRs, contracts,
  registries, CONTEXT.md, and CAMPAIGN-STATE.md untouched.
- One spec item needed per-row narrowing from evidence: step 3(c) asks for
  "(exercised by fresh contexts in campaign R1/R2)" on two rows *only if the
  exact passage can be cited*. Each row is supported by exactly one report:
  "Next responsibility selection" by R1 (Q3 alternatives table, Q5) and
  "Stop conditions" by R2 (sections 5 A2/A4/A5 and 8). The parenthetical was
  written per row with that attribution rather than "R1/R2" on both. Flagged
  in section 3 (M1).
- Two further record-vs-report discrepancies were found and handled by
  writing only what the reports support: the record calls all five R1 Q7
  omissions `MISSING_DURABLE_STATE`, while the R1 report labels only item 4
  that way (M2); the record's "three continuations" count (U5) has no stated
  basis, so the map bullet spells out the three handoffs it counts (M3). No
  wrong fact was found in the record for R3's scope.
- Validation: `validate-repo.py` exit 0; `PYTHONUTF8=1 pytest
  tests/test_path_drift.py` = 14 passed / 1 skipped (no red); the three
  markdown links added all resolve; the file remains LF and pure ASCII;
  `git diff --stat` = one file.
- Cost: 8 repository files opened (5 fully, 3 by excerpt), 24 tool calls
  including this report's Write and commit. Beyond the record's step-1 list
  only `CHARTER.md` was read (to confirm the authority grants the record
  cites). No Skill, no workflow runtime, no `gh`, no push.

## 1. Quoted before / after of each changed passage

File: `docs/agent-native-operating-workflow.md`. Line numbers are those of
the file after commit `6ff4a89`.

### (a) Section 2 "CONTINUATION" -- dated subsection added (lines 320-396)

Before (lines 308-318, unchanged; insertion point was the `---` that
followed them):

```text
Current reality (recorded in the retirement-plan closure): typed fan-in
`CONTRACT_CLOSED`; prior-report selection `CONVENTION` (the caller supplies
which prior report); overall loop `CONVENTION_CLOSED`.

Operating rule (recorded 2026-08-13, carried into normal use): when a
continuation feels awkward, preserve the actual handoff, preserve the
candidate prior reports, record what the agent could and could not
reconstruct, and do not design the fix yet. Reopen trigger: at least one
real agent-native continuation cannot reconstruct the intended prior report
from durable repository state without relying on conversational/session
memory.

---
```

After (the paragraph above is verbatim; the following block is inserted
between it and the `---`):

```text
#### Responsibility-level continuation from a durable record (demonstrated 2026-09-02)

The cross-run-identity status above is unchanged. A narrower form of
continuation -- one bounded responsibility handed from one coding-agent
context to a fresh one through a durable Markdown record -- has been
demonstrated in real use inside the campaign directory
[`docs/campaigns/agent-native-self-development/`](campaigns/agent-native-self-development/CAMPAIGN-STATE.md).
Two fresh contexts, given only the repository worktree and the path of
`CAMPAIGN-STATE.md` (no conversation history, no Skill invocation, no
workflow runtime), did the following:

- **R1** ([report](campaigns/agent-native-self-development/R1-fresh-context-reconstruction.md))
  reconstructed the mission, the capability state, why the current task had
  been selected over the visible alternatives, what was established vs.
  uncertain, and the warranted next action: questions Q1-Q5 `RECONSTRUCTED`,
  authority (Q6) `PARTIAL`, five omissions listed (Q7); cost 39 files /
  25 tool calls.
- **R2** ([report](campaigns/agent-native-self-development/R2-continuation-trial.md))
  performed a seven-step, three-file documentation responsibility from the
  record alone: established the record's facts from git and CI before
  writing, refreshed the named rows, ran the named validators, committed
  under the required convention, declined plausible-but-unlisted edits
  (report section 5 A2/A4/A5), and wrote a candid report; cost 9 files /
  36 tool calls. Its verification step exposed one wrong fact in the record
  (gate provenance, report M1/F1); it wrote the git-established facts and
  flagged the conflict instead of silently correcting the record.

Durable state that proved necessary (all of it in the record, none of it in
conversation memory):

- the mission;
- a capability-state table with a repository evidence pointer per row;
- known gaps and active constraints;
- authority: every grant traced to a durable source, plus an explicit
  not-authorized list;
- a task spec with numbered steps, verification steps (not only
  assertions), a stop condition, the commit convention, and the expected
  evidence;
- open decision-changing uncertainties and deferred findings;
- remote / integration status (push, PR, CI) recorded, never assumed;
- an append-only responsibility trace.

Beyond the record, the fresh contexts needed only repository state, mostly
named by the record (protocol docs, table conventions, git/CI facts; R2
section 6 F7) -- no conversation state.

Failure classes observed, and how each was repaired at the following
close-out:

- `AUTHORITY_AMBIGUITY` (R1 Q6, narrow: a merge rule sourced to an
  out-of-repository standing instruction; push/PR delegation asserted only
  by the record; no source for who authorizes implementing candidate
  machinery on the branch) -> source every grant: the record now cites a
  durable source per grant (its section 11) and the owner instruction is
  committed verbatim (`CHARTER.md`).
- `MISSING_DURABLE_STATE` (R1 Q7: the charter and a cited standing
  instruction were not in the repository; push/PR status was not recorded;
  some cited evidence lives only in GitHub issues) -> commit the authority
  text; record push/CI status in the record; mark GitHub-only evidence as
  such.
- Not in the taxonomy: durable state that was present but *wrong* on one
  fact (R2 M1). No schema would have caught it; the spec's own "establish
  from git" step did. Task specs therefore carry verification steps.

Not needed at this scale: a continuation schema, a validator, a new artifact
type, or a hook. Both continuation events were explicit dispatches; the
record plus the report sufficed; zero shape errors were observed. Reopen
conditions (campaign record U5/U3): a fresh context fails on a *missing or
malformed section* rather than a wrong fact; more than one dispatcher must
produce such records; or a recurrent continuation event that a manual step
keeps missing is observed (hook).

Observed limitation: documentation-level responsibilities only.
Implementation-class continuation (code + tests + CI) from durable state is
untested (campaign record U7). Nothing here exercises the cross-run
prior-report identity trigger above, which stays unresolved.
```

### (b) Section 5 Reality map, row "Continuation" (line 468)

Before:

```text
| Continuation | typed inputs + durable artifacts | CONVENTION_CLOSED (retirement plan) | prior-report identity deliberately unresolved |
```

After (status cell only; "Existing support" and "What not to assume" cells
verbatim):

```text
| Continuation | typed inputs + durable artifacts | CONVENTION -- responsibility-level continuation DEMONSTRATED (campaign R1/R2, 2026-09-02); cross-run prior-report identity still CONVENTION_CLOSED; machinery not earned | prior-report identity deliberately unresolved |
```

### (c) Section 5 Reality map, rows "Next responsibility selection" (line 461) and "Stop conditions" (line 469)

Before:

```text
| Next responsibility selection | agent judgment + skill catalog | CONVENTION / unratified automation (ADR 0018 SUPERSEDED) | do not restore automatic routing by accident |
| Stop conditions | this document (first consolidation) | CONVENTION (no machinery) | "no more things to investigate" is not done |
```

After:

```text
| Next responsibility selection | agent judgment + skill catalog | CONVENTION / unratified automation (ADR 0018 SUPERSEDED); exercised by a fresh context in campaign R1 (report Q3 alternatives table, Q5) | do not restore automatic routing by accident |
| Stop conditions | this document (first consolidation) | CONVENTION (no machinery); exercised by a fresh context in campaign R2 (report sections 5 A2/A4/A5 and 8: stopped at the spec's stop condition, declined unlisted edits) | "no more things to investigate" is not done |
```

Exact passages relied on (step 3(c) condition):

- R1 Q3 "Competing alternatives visible in the repository, and why each was
  not selected" table (seven alternatives) and Q3(c) "I did not need
  conversation context to see why R1 beats the alternatives"; R1 Q5(a)
  selects the concrete next action and proposes the G6 bookkeeping task
  ("That is my suggestion, not the record's") -- which became R2.
- R2 section 8, first bullet: "R2 is one responsibility with a stop
  condition; the harness forbids pushing. Stopped at the stop condition."
  R2 section 5 A2 ("Chose the conservative reading: not edited"), A4 ("Not
  added"), A5 ("not authorized in R2 ... not edited").

### (d) Section 6 "What is deliberately not here" -- one bullet added (lines 485-492)

Before: the list ended with the "Registered workflows stay subgraphs" bullet.

After (appended):

```text
- **No continuation schema, validator, or hook** -- three record-mediated
  handoffs (campaign R0 -> R1, R1 -> R2, R2 -> close-out audit; two of them
  into fresh contexts) produced zero shape errors and one fact error, which
  an in-spec verification step caught and no schema would have; the
  machinery promotion rule (section 7) is not met. Reopen conditions as in
  section 2 "CONTINUATION": a failure on a missing or malformed section
  rather than a wrong fact; more than one producer of such records; or a
  recurrent continuation event that a manual step keeps missing.
```

Not changed, deliberately: the document's header (`Status: v0`, "evidence
0016-0020"), section 7's cross-run-identity example (still accurate), the
"Existing support" cell of the Continuation row (spec names only the status
cell), and every other line.

## 2. What the record was sufficient for

| Need | Sufficient? | Where |
|---|---|---|
| Which responsibility is current | yes | section 10 header `R3` |
| Why it is warranted | yes | section 10 CAMPAIGN CAPABILITY AFFECTED / CURRENT LIMITATION / WHY IT MATTERS; sections 6 (G9), 9, 13 rows 4/6/11 |
| The exact reading list | yes | step 1, with section names; all seven sources exist where named (retirement plan L137, CONTEXT.md L266, SKILL.md L419) |
| What to verify before writing | yes | step 2 (a)-(c) |
| What to write, where, and what to keep verbatim | yes | step 3 (a)-(d), including the content outline for the subsection |
| What NOT to touch | yes, explicit | step 3 last paragraph; NOT AUTHORIZED IN R3 |
| Validation commands and expected results | yes | step 4 |
| Commit convention, no push, no record edit | yes | step 5 |
| Report contents | yes | step 6 |
| Authority for each mutation | yes, sourced | AUTHORITY FOR R3 (charter list item "documentation reconciliation" = `CHARTER.md` L451; "one coherent commit" = L581; map section 7 revision trigger = map L416-418; "NOT a canonical orchestration specification" = map L5) |
| Stop condition | yes | STOP CONDITION |
| Constraints (no Skills, ASCII, worktree, LF/arrows) | yes | section 7 C1/C5/C6; step 3 "Keep the document's voice, ASCII arrows" |
| Reopen conditions to carry into the map | yes | U5 and U3 rows, as the spec directs |

I did not need any conversation memory, any owner clarification, or any
GitHub access. R1 and R2 were read in full (R2 beyond the four named
sections, because the "Stop conditions" citation lives in R2 sections 5 and
8, which step 1 does not list).

## 3. What was missing, wrong, or ambiguous (flagged, not fixed)

| # | Item | Kind | Resolution |
|---|---|---|---|
| M1 | Step 3(c) says to add "(exercised by fresh contexts in campaign R1/R2)" to two rows "only if you can cite the exact R1/R2 passage". For "Next responsibility selection" only R1 contains such a passage (Q3, Q5); for "Stop conditions" only R2 does (sections 5, 8). R1 has no passage saying it stopped at a stop condition; R2 identified the current responsibility but did not select among alternatives | spec condition satisfiable only per row | wrote the parenthetical per row with the single supporting report cited, instead of "R1/R2" on both. Evidence over spec wording; flagged here and in the commit message |
| M2 | Record section 3 (R1 row) says "Q7 five omissions, all `MISSING_DURABLE_STATE`". The R1 report's summary table gives Q7 no class, and in the body only item 4 (GitHub-only #218 evidence) is labelled `MISSING_DURABLE_STATE`; item 1 (substrate collision with evidence 0023) is an unflagged risk, not missing state | record classification broader than the report's own | the map subsection names the omissions that are missing-durable-state by content (charter / standing instruction absent; push/PR status unrecorded; GitHub-only evidence) and does not assert "all five". Record not edited (prohibited) |
| M3 | Record U5 says "three continuations, zero shape errors, one fact error" and step 3(d) repeats "three continuations"; neither states what is being counted (condition 5 says three *contexts*: dispatcher, fresh, fresh). Only two continuations into fresh contexts are evidenced by report files | count basis unstated | the section-6 bullet spells out the three handoffs it counts (R0 -> R1, R1 -> R2, R2 -> close-out audit) and says "two of them into fresh contexts", so the product surface does not overclaim. The close-out audit is evidenced by commit `2adfeaf` and record section 3 |
| M4 | Step 3(a) asks for "a pointer" and step 4 for a grep of "the markdown links you added"; the document previously contained zero markdown links (every path is backticked) | minor voice question | added three relative markdown links (`campaigns/agent-native-self-development/...`), backtick-labelled where a path is shown, so step 4's link check is meaningful. Small deviation from the document's prior style; all three targets verified to exist |
| M5 | AUTHORITY FOR R3 says "PR #268 is the surfacing". Nothing in R3 requires confirming the PR; it lives only in GitHub (record G8) | GitHub-only fact | not verified (no `gh` used); not relied on for any edit. The map's section 7 trigger ("surface it for owner review") is satisfied by the dispatcher's push/PR step, which is outside R3 |
| M6 | Step 3(a) names a "subsection" but the document has no heading level below `###` | formatting | used `####` under `### CONTINUATION`; no other heading-level change |
| M7 | Step 1 lists R2 "sections Summary, 1, 2, 6 F7"; the citation the spec requires for 3(c) is in R2 sections 5 and 8 | reading list slightly short for the spec's own condition | read R2 in full (one file, 205 lines); no cost issue |

No `AUTHORITY_AMBIGUITY`, `CAPABILITY_DISCOVERY_FAILURE`,
`PRODUCT_DIRECTION_AMBIGUITY`, or `INCIDENTAL_CONTEXT_LOSS` arose. No fact
in the record was found wrong for R3's scope: the operating map's text,
the retirement plan's trigger wording, the section names in CONTEXT.md and
the bootstrap SKILL.md, and the map's section 7 revision trigger all read
exactly as the record describes.

## 4. Files consulted beyond the record, and why

Named by the record (step 1) -- required inputs, not "beyond":
`R1-fresh-context-reconstruction.md` (full), `R2-continuation-trial.md`
(full; see M7), `docs/agent-native-operating-workflow.md` (full),
`docs/2026-08-programmatic-runner-retirement-plan.md` L130-189 ("Project
closure"), `CONTEXT.md` L260-304 ("Stop and continuation conditions"),
`skills/using-sensemaking/SKILL.md` L415-464 (section 14).

Beyond the step-1 list:

| File / source | Why |
|---|---|
| `docs/campaigns/agent-native-self-development/CHARTER.md` (full) | the record's AUTHORITY FOR R3 block cites it; read to confirm "documentation reconciliation" is in the Responsibility Execution list (L451), the "one coherent commit or PR per meaningful bounded responsibility" rule (L581), and that ordinary infrastructure is permitted (L65-81), before mutating a product doc |
| git (`status`, `log`, `diff`, `commit`) | branch/base confirmation (charter "confirm current branch/base"), commit-message convention of `fa2dd68`/`9160a5b`/`2adfeaf`, diff inspection |
| directory listing of the campaign directory | to confirm the report filename was free |

Not consulted: any ADR, `AGENTS.md`, `CLAUDE.md` body, evidence files, the
semantic-control-map or its trial docs, any Skill, registry, contract,
validator source, or test source (the validators and test were *run*, not
read). No GitHub queries.

## 5. Commands run and results

| Step | Command | Result |
|---|---|---|
| 0 | `git status --short --branch`; `git log --oneline -6` | clean; on `campaign/agent-native-self-development`, HEAD `2adfeaf`, tracking origin |
| 2 | byte check of the map (`python`) | LF, 0 non-ASCII bytes, trailing newline; 0 markdown links before editing |
| 4 | `python scripts/validate-repo.py` | "Validation passed!", exit 0 |
| 4 | `PYTHONUTF8=1 python -m pytest tests/test_path_drift.py -q` | 14 passed, 1 skipped, exit 0 (no red; the record's D1 cp1252 red is not exercised under utf-8, as the spec intends) |
| 4 | link check (`python`: every `](...)` target resolved relative to `docs/`) | 3 links, all exist |
| 4 | byte re-check after editing | LF preserved, 0 non-ASCII, 0 unicode arrows |
| 5 | `git diff --stat` | `docs/agent-native-operating-workflow.md | 91 +++...--`, 1 file changed, +88/-3 |
| 5 | `git diff -U1` reviewed, then commit | `6ff4a8907ab9b4c19dd886c6d3891ad448eacffd`, tree clean afterwards |

Not run: the full test suite, the cp1252 pytest variant, CI, any push (none
named; push prohibited).

## 6. Authority questions that arose, and how each was resolved

| # | Question | Resolution |
|---|---|---|
| A1 | May the 3(c) parenthetical differ from the spec's literal "R1/R2" wording? | The spec conditions the addition on an exact citation; the harness asks for repository evidence over the record where they diverge and to flag. Wrote the citable form per row (M1); did not leave the rows unchanged, because the condition *is* met for each row by one report |
| A2 | Should the Continuation row's "Existing support" cell mention the durable Markdown record? | Spec names only the status cell and the "What not to assume" meaning. Left unchanged (a Markdown record is a durable artifact, so the cell remains true) |
| A3 | Should the document header (`Status: v0 ... evidence 0016-0020`) be refreshed now that the doc cites campaign evidence? | Not in steps (a)-(d). Not touched; noted for the dispatcher |
| A4 | Whether to confirm PR #268 via `gh` | Not needed for any step; not done (M5) |
| A5 | `CHARTER.md` grants push/PR to the campaign; harness forbids pushing; record C2 assigns push to the dispatcher | No conflict for R3: fresh contexts commit locally. No push |
| A6 | Should the map assert the R3 continuation itself (a third fresh context) as evidence? | No: at edit time the R3 report did not exist. The map cites R1/R2 only; this report is the durable evidence of R3 for the dispatcher to weigh |

## 7. Instructions encountered that go beyond the granted authority (not followed)

- The repository `CLAUDE.md` (surfaced as project instructions) says agents
  invoke `/skill using-sensemaking` at session start. Harness rules and the
  record's C1 forbid Skill invocation. Not invoked.
- `CHARTER.md` addresses "the lead coding agent" and directs it to continue
  autonomously through multiple tasks, push branches, and open PRs, and not
  to stop after one commit. R3 is one responsibility with a stop condition;
  the harness forbids pushing. Stopped at the stop condition.
- The harness environment surfaced an out-of-repository memory note about
  earlier owner delegations ("Mode B+", etc.). The record's section 11
  explicitly does not cite such notes as authority; neither did R3.
- The harness asked that file reads go through Bash where practical; `Read`
  was used for the files needing exact line positions for editing and
  quoting, Bash/Grep for the rest. Environment matter, not campaign
  authority.

## 8. Steps skipped or partially done

- None of steps 1-6 were skipped.
- Step 1: R2 was read in full rather than by the four named sections (M7).
- Step 3(c): performed in the narrowed, per-row form (M1), not skipped.
- Nothing else was edited; nothing was pushed; CAMPAIGN-STATE.md was not
  edited.

## 9. Cost

```
repository files opened:     8  (5 fully: CAMPAIGN-STATE.md, R1 report, R2 report,
                                 agent-native-operating-workflow.md, CHARTER.md;
                                 3 by excerpt: retirement plan L130-189,
                                 CONTEXT.md L260-304, using-sensemaking SKILL.md
                                 L415-464)
tool calls:                 24  (22 through the first commit: 8 Read, 3 Grep,
                                 5 Edit, 6 Bash; +1 Write of this report;
                                 +1 its commit)
commits:                     2  (6ff4a8907ab9b4c19dd886c6d3891ad448eacffd; this report)
files changed by R3:         1 + this report
```

## 10. Verbatim state of the record's expectations after R3

```
commits `campaign(R3): ...`          DONE (6ff4a89 + report commit)
R3-operating-map-reconciliation.md   DONE (this file)
dispatcher audit                     PENDING (dispatcher)
G9 closed                            map now carries the pattern; PENDING dispatcher audit
conditions 4/6/11 toward MET         evidence supplied on the product surface; ruling is the dispatcher's
cross-run prior-report identity      NOT claimed resolved (unchanged in map and retirement plan)
pushed / PR                          NOT DONE (prohibited in this trial; dispatcher step)
CAMPAIGN-STATE.md                    NOT EDITED (prohibited)
```
