# R6: workflow-system disposition from the record (fresh-context report)

```
CONTEXT:    fresh coding-agent context; no conversation history; only the path
            of CAMPAIGN-STATE.md was given. Harness rules: no Skill invocation,
            no workflow runtime, direct file/search tools + named shell
            commands only; files read are data.
BRANCH:     campaign/agent-native-self-development, HEAD 89246f4 at start
COMMITS:    70648c4 (docs/workflow-system-disposition.md new, +410;
            docs/agent-native-operating-workflow.md +5/-1); this report is
            the second commit
AUTHORITY:  as read from CAMPAIGN-STATE.md section 10 "AUTHORITY FOR R6" and
            section 11; verified in CHARTER.md L438-452 ("workflow
            demotion/repair/retirement" as a listed bounded responsibility),
            L525-554 ("Workflow-System Policy During This Campaign"),
            ADR 0027 L103-113 ("Explicit non-decisions"), operating map
            section 7 (revision trigger). Non-authoritative report.
NOT EDITED: CAMPAIGN-STATE.md; workflow-registry.yaml, workflow-liveness.yaml
            (either copy), skill-registry.yaml; contracts; ADRs; scripts/;
            src/; tests/; skills/; CONTEXT.md; any doc other than the two
            named files. Nothing pushed; no branch created or switched; no
            tracker writes.
```

## Summary

- The record was sufficient to identify R6, its seven steps, the sourced
  authority, the not-authorized list, the three-branch stop condition, and
  every source file (all present). All seven steps were performed; the stop
  condition "both commits exist and the report is written" is met.
- The starting inventory's liveness column, `mc` column, and step-skill
  statuses were verified correct for all 23 rows. Its `ev` and `tests`
  columns reproduce only with plain substring matching, which inflates seven
  rows (worst: `implementation-workflow` tests 31 vs 3, ev 20 vs 5, because
  the id is a substring of four other ids). Its `ldg` column is dominated by
  `recommended_workflow_id` fields in briefs (recommendations, not
  executions); one `ldg` value (`architectural-review-planning-workflow`,
  record 6, rebuilt 20) could not be reproduced by either method. Two
  `?` cells resolved from the registry: `setup-sensemaking-skills` has no
  skill-registry entry at all (Skill directory exists; `validate-repo.py`
  exempts it by name), and `full-local-sensemaking` step `3-conditional`
  routes to the deprecated `discovery` as `external_routing`, so the
  record's "all local_execution except the two sprints" is incomplete. The
  record's date for `artifacts/reconciliation_report.md` (2026-08-22) is
  wrong: the file was added 2026-09-01 (`060fc36`) and says so itself.
- Dispositions: KEEP_AS_BOUNDED_SUBGRAPH 1 (`docs-contract-reconciliation`);
  DEMOTE 2 (`artifact-reconciliation`, `architectural-review-planning-workflow`);
  RETIRE_CANDIDATE 2 (`product-discovery-sprint`, `product-strategy-sprint`);
  HISTORICAL 8 (the ADR 0027 set, not re-decided); INSUFFICIENT_EVIDENCE 10;
  REPAIR 0. Every ledger with step events in the repository was produced by
  the `claude-code` SDK executor removed on 2026-08-13; the only workflow
  with a recurring successful agent-native trace of its full sequence is
  `docs-contract-reconciliation`.
- Written narrower than the record in two places, from evidence: (1) the
  KEEP clause "or is the ratified product spine" could not be applied to any
  row because ADR 0014 ratifies a single Skill's output (the human-reviewed
  brief) and defers the second golden-path step (ADR 0014 L68-87), which
  the record's step-1 list does not point to; (2) mode-coverage's two
  pointed entries both overstate `steps_completed` (1 vs 0/2 in their own
  run logs), so mode-coverage claims were treated as claims, not records.
- Validation: `python scripts/validate-repo.py` exit 0; `PYTHONUTF8=1
  PYTHONPATH=src python -m pytest tests/test_path_drift.py -q` 14 passed /
  1 skipped (run with `-p no:cacheprovider` added, per C11); the new file is
  ASCII (0 non-ASCII bytes) with LF endings; all six added markdown links
  resolve; the operating map stayed at 0 non-ASCII bytes and LF; staged diff
  exactly 2 files (+415/-1).
- Cost: 50 repository files opened (21 named by the record; 29 beyond it,
  section 5) plus three programmatic text scans (artifacts/, experiments/,
  tests/) and two directory listings; 60 tool calls including this report's
  Write and its commit. No Skill, no workflow runtime, no `gh`, no push.

---

## 1. Inventory rebuild (step 2) and every discrepancy found

Method: parsed the three registries with PyYAML (`encoding="utf-8"`);
checked `skills/<id>/SKILL.md` for each step Skill; read all four
`run-ledger.jsonl` files line by line; counted, per workflow id, (a) files
under `artifacts/` + `experiments/` matching `workflow_id[:=] <id>` with an
id boundary, (b) mentions in `docs/mode-coverage.yaml`, (c) files under
`experiments/evidence/` mentioning the id with an id boundary, (d) files under
`tests/` likewise; then re-ran (a), (c), (d) with plain substring matching to
test whether the record's numbers were method artefacts. Script and JSON left
in the session scratchpad, not in the repository.

| # | Record claim | Rebuilt | Class |
|---|---|---|---|
| I1 | liveness per row (8 `compatibility_only`) | identical for all 23 rows in `skills/workflow-planner/references/workflow-liveness.yaml` | verified |
| I2 | `mc` per row | identical for all 23 rows | verified |
| I3 | `ev` per row | identical under substring matching; boundary-aware counts lower for 7 rows: full-fog 10->6, docs-contract-reconciliation 13->12, docs-architecture 6->3, full-local-sensemaking 12->9, fast-local-diagnostic 4->1, implementation-workflow 20->5, architectural-review-planning-workflow 54->51 | method caveat, not a fact error |
| I4 | `tests` per row | identical under substring matching; boundary-aware differs for one row: implementation-workflow 31->3 (the id is a substring of `ui-`, `product-`, `docs-`, `architecture-implementation-workflow`) | method caveat |
| I5 | `ldg` per row | identical for 22 rows under both methods; `architectural-review-planning-workflow` record 6 vs rebuilt 20 (7 ledgers, 7 workflow summaries, 5 plans, 1 construction candidate) -- not reproducible by either method | unexplained discrepancy |
| I6 | `ldg` semantics: "name-mentions in run records ... many are plan or fixture files" | the pattern `workflow_id` also matches `recommended_workflow_id`; the large majority of hits are briefs/plans *recommending* the workflow (e.g. all 38 for `architecture-implementation-workflow`, all 5 for `fast-path-workflow`, all 5 for `skill-maintenance-loop`). Only 8 files in the repository are ledgers with step events, all for two workflows (`fast-local-diagnostic` x1, `architectural-review-planning-workflow` x7) | record caveat understated |
| I7 | `setup-sensemaking-skills(?)` | no entry in `skill-registry.yaml` at all; `skills/setup-sensemaking-skills/SKILL.md` exists; `scripts/validate-repo.py:220-223` exempts it by name from the registry-membership requirement | resolved; registry gap recorded as implied decision |
| I8 | `full-local-sensemaking` "step 3 conditional(?)" and "Step types: all local_execution except product-discovery-sprint and product-strategy-sprint" | step `3-conditional` (`workflow-registry.yaml:519-534`) has `if_true` = `discovery` (`deprecated`, no implementation) as `external_routing`; so a third workflow contains an external-routing step, on a conditional branch | resolved; record statement incomplete |
| I9 | `artifact-reconciliation` row: "agent-native execution evidence: `artifacts/reconciliation_report.md` (2026-08-22), evidence 0020" | file added `060fc36` 2026-09-01; `created_at: 2026-09-01T00:00:00Z` (line 207); it audits the 2026-09-01 docs-aligner run (`artifacts/work_claim.md:4-5`). The 2026-08-22/23 artifacts (`workflow_orchestration_plan_docs_contract_reconciliation_2026-08-22.md`, `reconciliation_patch_draft_docs_contract_2026-08-22.md`, `repair_verification_report.md`, all `1ffde16`) belong to `docs-contract-reconciliation`. Evidence 0020 says of itself that it is "authored documentation of an observed process" (L55), and the run it describes stops at the report (no `issue_list`, no `session_summary`) | wrong date; evidence narrower than the row implies |
| I10 | step-skill `(ok)` for implemented Skills | the registry carries no `status` field for them; "ok" holds by directory check for all 14 such ids | verified by a different means |
| I11 | "workflow-liveness.yaml (either copy)" (not-authorized list) implying two equivalent copies | packaged copy `src/sensemaking_skills/defaults/workflow-liveness.yaml` lists 7 overrides (no `architecture-implementation-workflow`); the packaged catalog carries 20 of 23 ids (missing `artifact-reconciliation`, `architecture-implementation-workflow`, `architectural-review-planning-workflow`). Consistent with ADR 0027 verification item 6 ("shared workflow IDs"); not consistent with the record's implicit assumption | observation; recorded in the document's Evidence limits |
| I12 | `fast-local-diagnostic` ldg 4 | matches, but the single ledger with step events (`artifacts/01-orchestration-run`) is a failed yolo run whose executor was a fixture (`run_log:21`), and `docs/mode-coverage.yaml:6` records that session as `steps_completed: 1` against the run record's 0/2 | record silent on run outcome |
| I13 | `architectural-review-planning-workflow` mode-coverage entry (`mc` 3) | `docs/mode-coverage.yaml:19` says `steps_completed: 1` for session `orchestration-20260725-161841-c45d882a`; the cited `experiments/evidence/0005-.../run_log.md:40` says 0/2 and the ledger shows step 1 failed validation | record silent; mode-coverage overstates |

Usability verdict on the starting inventory: usable as a checklist (rows,
liveness, step Skills, `mc`), not usable as evidence of execution (its
`ldg`/`ev` numbers do not distinguish recommendation from execution). The
document was written from the rebuilt inventory; the stop-condition branch
"unusable" was not triggered.

---

## 2. Dispositions and counts (step 3)

| disposition | count | workflows |
|---|---|---|
| KEEP_AS_BOUNDED_SUBGRAPH | 1 | docs-contract-reconciliation |
| REPAIR | 0 | -- |
| DEMOTE | 2 | artifact-reconciliation; architectural-review-planning-workflow |
| RETIRE_CANDIDATE | 2 | product-discovery-sprint; product-strategy-sprint |
| HISTORICAL | 8 | product-to-issues; product-autonomous-sprint; experimental-autonomous-sprint; implementation-workflow; product-implementation-workflow; ui-diagnostic-workflow; ui-implementation-workflow; architecture-implementation-workflow |
| INSUFFICIENT_EVIDENCE | 10 | fast-path-workflow; full-fog-workflow; setup-sensemaking-repo; autonomous-sprint-preflight; docs-architecture; full-local-sensemaking; fast-local-diagnostic; skill-maintenance-loop; docs-implementation-workflow; skill-evaluation-workflow |

Calls that required judgment, each stated in the document so the dispatcher
can overrule:

- **`docs-contract-reconciliation` = KEEP.** Four in-repo instances of the
  sequence (2026-08-12 dogfood set; evidence 0019; evidence 0021
  remediation; 2026-08-22/23 set) plus auteur cycle B (evidence 0018). The
  investment rule is rated part by part; "measurable benefit" is PARTIAL
  (finding-specific closures recorded; no like-for-like comparison). No
  single run carries all four contract-shaped outputs; the union does.
- **`artifact-reconciliation` = DEMOTE**, not KEEP and not
  INSUFFICIENT_EVIDENCE. A real agent-native record exists for the reconcile
  step (2026-09-01) and it recurs (0018, 0022), but every instance stops at
  the report; steps 3-4 are never recorded. The alternative reading
  (INSUFFICIENT_EVIDENCE for the full chain) is named in the row.
- **`architectural-review-planning-workflow` = DEMOTE**, not KEEP. KEEP's
  four literal conditions hold (7 runner-era ledgers), but 1 of 7 runs
  completed both steps (by resuming a prior step-1 success), 5 halted at
  step-1 validation, all ran through the removed SDK executor, and ADR 0014
  L78-87 keeps step 2 outside the ratified boundary. The evidenced role is
  the internal golden-path proof vehicle (ADR 0014 L57-66).
- **`fast-local-diagnostic` = INSUFFICIENT_EVIDENCE**, although its step 1 is
  the ratified spine's Skill: the only workflow-level record is a failed
  fixture-executor run (test-only trace by the record's own rule).
- **`full-local-sensemaking` and `setup-sensemaking-repo`** carry citable
  registry defects (deprecated conditional target; missing skill-registry
  entry) but are unevidenced, so REPAIR's "evidenced" precondition fails;
  the defects are recorded as implied owner decisions instead.
- **The two sprints = RETIRE_CANDIDATE** (record U9): the criteria assign
  HISTORICAL only from the ADR 0027 overlay; the implied overlay change is
  listed, not applied.

Condition 9 and G4/G11/U4/U9 are for the dispatcher to close; this report
only states that the document now records, per workflow, the disposition and
the evidence behind it.

---

## 3. What the record was sufficient for

- Identifying the responsibility, its numbered steps, the two commits'
  convention, the stop condition, and the expected evidence.
- The sourced authority and the not-authorized list; no authority question
  arose that the record and CHARTER.md did not answer (section 7).
- Every named source file existed at the named path; the four ledger files
  and the six evidence records resolved from the record's globs.
- The disposition criteria were applicable as written for 21 of 23 rows;
  the two exceptions (the "ratified product spine" clause and partial-
  sequence evidence) needed interpretation rules, stated in the document's
  section 2.
- The starting inventory's row set, liveness, `mc`, and step-Skill columns
  were correct and saved re-derivation time; its `?` cells were honest.

---

## 4. What was missing or wrong in the record (flagged, not fixed)

- **F1 -- wrong date** for `artifacts/reconciliation_report.md` (I9).
- **F2 -- `ldg` semantics** (I6): the column counts recommendations as
  "ledger/run-record files". A fresh context trusting it would have seen
  38 "records" for a compatibility-only workflow that has none.
- **F3 -- the step-1 reading list omits the folders that hold every ledger
  with step events** (`experiments/evidence/0005, 0006, 0008, 0013, 0014,
  0015`). The list stops at `0018..0023`; the mode-coverage pointer
  (`run_log_path` at line 18) and the `workflow_id` scan led there. Without
  them `architectural-review-planning-workflow` would have been
  INSUFFICIENT_EVIDENCE by omission.
- **F4 -- the "ratified product spine" clause has no source pointer**; ADR
  0014 (not in the reading list) supplies it and shows the clause cannot be
  satisfied by any registered workflow.
- **F5 -- "Step types: all local_execution except ..."** misses the
  conditional external-routing branch in `full-local-sensemaking` (I8).
- **F6 -- "either copy" of the overlay** assumes identical overrides; the
  packaged copy has 7 and the packaged catalog 20 ids (I11).
- **F7 -- step 6 "`git diff --stat` -> exactly 2 files"** cannot show an
  untracked new file; read as the staged diff (`git diff --cached --stat`
  = 2 files) after `git add` of exactly the two named paths.
- **F8 -- the record's arpw `ldg` value (6)** could not be reproduced (I5).

None of these caused a wrong action; each was caught by the step-2 rebuild
or by reading the pointed-to file, which is the pattern the record's C9
constraint intends.

---

## 5. Files consulted beyond the record's step-1 list (29)

Why each was needed:

| file(s) | reason |
|---|---|
| `docs/campaigns/agent-native-self-development/R5-machinery-and-hooks-disposition.md` (first 90 lines) | report format convention |
| `src/sensemaking_skills/defaults/workflow-liveness.yaml`, `.../workflow-registry.yaml` (ids only) | the not-authorized list says "either copy"; verified equivalence (I11) |
| `artifacts/01-orchestration-run/run_log_fast-local-diagnostic_yolo_execution.md`, `workflow_summary.json` | outcome of the only non-plan ledger under `artifacts/` |
| `experiments/evidence/0005-runtime-skeleton-live-step1/run_log.md`, `run-ledger.jsonl`, `README.md` | pointed to by `docs/mode-coverage.yaml:18`; outcome of the run |
| `experiments/evidence/0006-.../RESULT.md`, `final-run-e787fc41/workflow_summary.json` | found by the `workflow_id` scan; step-1 PROVEN record |
| `experiments/evidence/0008-.../EVIDENCE.md`, `positive/workflow_summary.json`, `negative/workflow_summary.json` | the only 2/2 completion of any workflow; golden-path claim |
| `experiments/evidence/0013, 0014, 0015 EVIDENCE.md` (first 80 lines each) and their `workflow_summary.json` | the three Stage-1 auteur runs; outcomes |
| `artifacts/dogfood-evidence-index.md` | provenance of the 2026-08-12 dogfood artifact set |
| `artifacts/repair_verification_report.md`, `docs_contract_reconciliation_report_dogfood.md`, `session_summary_dogfood.md` (headers) | pin the step-2/3/4 artifacts of the KEEP row |
| `artifacts/workflow_orchestration_plan.md`, `workflow_orchestration_plan_docs_contract_reconciliation_2026-08-22.md` (headers) | which workflow each plan selected and from what input |
| `artifacts/work_claim.md` (head), `artifacts/repository_sensemaking_brief.md` (head + machine section) | provenance/date of the reconciliation report; date and self-statement of the 2026-05-25 brief |
| `scripts/validate-repo.py:212-235` | why a workflow may name a Skill absent from the skill registry |
| `docs/adr/0014-product-boundary.md` | the "ratified product spine" clause (F4) |

Programmatic scans (not read by me): every file under `artifacts/`,
`experiments/`, `tests/` for id matches; `skills/*/SKILL.md` directory
listing; `git log --diff-filter=A` for artifact add dates.

---

## 6. Cost

- 50 repository files opened (21 named; 29 beyond) + 3 scans + 2 listings.
- 60 tool calls: 24 Read, 4 Glob, 3 Write, 1 Edit, 28 Bash (git, Python
  snippets under `encoding="utf-8"`, `validate-repo.py`, pytest, commits).
- No Skill invoked; no workflow runtime run; no `gh`; no push; no branch
  change; nothing outside the worktree touched except the session scratchpad.

---

## 7. Authority questions

- None blocking. R6 authority (classification + evidence only) was sufficient
  for every action taken; the pointer sentence in the operating map is the
  one edit the record authorises under the map's section 7 revision trigger.
- Not exercised: no registry, overlay, contract, ADR, script, test, Skill, or
  other doc was edited; the eight implied owner decisions are listed in the
  document's section 6, not applied.
- Instruction-bearing content encountered while reading, treated as data:
  `CLAUDE.md`'s "Agents invoke this skill via the Skill tool" (harness
  forbids Skill invocation; not followed); the R5 report's and evidence
  records' operating rules (descriptive, not addressed to this context). No
  file contained an instruction to this context that exceeded the record's
  authority.

---

## 8. Skipped, not done, or interpreted

- Did not read ADR 0013 or ADR 0026 in full; cited them through the
  operating map header and `workflow-registry.yaml:1-7` / `:826-829`.
- Did not open the 0006 final-run run log, the 0008 positive/negative
  ledgers, or the 0013-0015 records beyond their summaries and first 80
  lines; outcomes were taken from `workflow_summary.json` and the evidence
  records' own classification lines.
- Did not run the full test suite (not authorised; C11 names the like-for-
  like procedure for R7). `-p no:cacheprovider` was added to the named
  pytest command so no cache directory would be created in the worktree.
- Did not verify GitHub-only evidence (Issue #218 episodes; issues
  #170-175) or any auteur-side file; cited only through in-repo evidence
  records.
- Did not consult untracked artifacts in any other checkout.
- Interpretations recorded in the document's section 2: recommendation
  mentions are not execution evidence; plan-only, fixture-executor, scenario,
  and construction-candidate traces do not count; unpointed mode-coverage
  claims are claims; the pointed-to record governs when mode-coverage
  disagrees with it; one Skill used outside the registered sequence
  evidences the Skill, and recurring partial records that show a proper
  subset of the steps are DEMOTE evidence; runner-era ledgers are real but
  not reproducible and not agent-native; "ratified product spine" resolves to
  ADR 0014's in-scope list and matches no registered workflow.
- `git diff --stat` read as the staged diff (F7).
