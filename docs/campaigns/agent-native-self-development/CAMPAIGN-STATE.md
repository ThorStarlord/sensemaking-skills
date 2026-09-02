# Campaign: reliable agent-native, artifact-mediated self-development

```
STATUS:    ACTIVE development-campaign record (living document, v5 after R4)
AUTHORITY: non-authoritative. Not an ADR, not a contract, not a validator input,
           not a registered workflow, not a research-agenda ratification.
CHARTER:   docs/campaigns/agent-native-self-development/CHARTER.md
           (owner instruction, verbatim; the campaign's authority source)
NOT:       an EXP-NNNN governed experiment campaign (ADR 0023 two-lane machinery
           does not read this file; no approval envelope applies).
READS:     nothing in scripts/, src/, tests/, or .github/ reads this file.
BRANCH:    campaign/agent-native-self-development   (base: main @ f10b7da, 2026-09-02)
WORKTREE:  H:/GithubRepositories/smk-campaign
REMOTE:    see section 15 (push / PR / CI status is recorded there, not assumed)
RULE:      update after every consequential campaign responsibility. Facts in
           this file are claims; task specs include verification steps so a
           continuing context can catch errors here (R2 F1; R3 M2/M3; R4 F1/F2).
```

This file exists so that campaign reasoning does not live only in one
conversation's context. Four fresh contexts have so far continued the campaign
from this file alone: R1 (reconstruction), R2 (mechanical execution), R3
(judgment-class documentation), R4 (implementation-class code + tests with a
repair-vs-retire judgment). See section 8.

---

## 1. CAMPAIGN MISSION

Advance Sensemaking Skills toward **reliable agent-native, artifact-mediated
self-development**: an active coding agent uses repository evidence and durable
artifacts to determine the next warranted engineering responsibility, select an
appropriate capability, perform bounded work, validate the resulting evidence,
preserve authority boundaries, carry state across responsibilities, and
recursively continue until the active goal is satisfied or further action is
unwarranted. Full text, acceptance conditions, stopping rules, and report
format: `CHARTER.md`.

Campaign-level, not a monolithic rewrite. The campaign is controlled directly
by the active coding agent, **not** by `repo-sensemaker`, `using-sensemaking`,
registered workflows, workflow-runtime routing, fog routing, or hooks
(bootstrap constraint). Ordinary repository engineering infrastructure (tests,
validators, `validate-repo.py`, probe engine, CI, git, PRs) is used normally.

Control model owned by the agent:

```text
PRODUCT MISSION
  -> current repository / product state
  -> highest-leverage unresolved capability boundary
  -> decision-changing uncertainty
  -> ONE bounded responsibility
  -> bounded analysis / design / implementation / verification
  -> durable repository evidence
  -> validate
  -> update this record
  -> reassess from the mission
  -> continue / owner decision / blocker / complete
```

Operating pattern used since R1: the dispatcher context specifies the next
responsibility in section 10, commits, and dispatches a **fresh context** that
receives only this file's path; the fresh context performs the responsibility
and writes `Rn-*.md`; the dispatcher audits the diff against the spec
(claim reconciliation), updates this file, commits, pushes.

Campaign vocabulary (defined in `CHARTER.md`, not canonical repository
vocabulary): finding classes `CAMPAIGN_BLOCKING | CAMPAIGN_RELEVANT |
LOCAL_BUT_REAL | HISTORICAL_ONLY | DEFERRED | NO_ACTION_WARRANTED`;
reconstruction-failure classes `MISSING_DURABLE_STATE |
CAPABILITY_DISCOVERY_FAILURE | WARRANT_AMBIGUITY | AUTHORITY_AMBIGUITY |
PRODUCT_DIRECTION_AMBIGUITY | INCIDENTAL_CONTEXT_LOSS`; workflow dispositions
`KEEP_AS_BOUNDED_SUBGRAPH | REPAIR | DEMOTE | RETIRE_CANDIDATE | HISTORICAL |
INSUFFICIENT_EVIDENCE`.

---

## 2. CURRENT PRODUCT / CAPABILITY STATE (main @ f10b7da, 2026-09-02)

| Capability | State | Evidence (repository) |
|---|---|---|
| Top-level semantic control model | **EXPLICIT in docs**; agent owns loop; decision vs orchestration separated; warrant vocabulary defined | `CONTEXT.md`; `docs/decision-orchestration-boundary.md`; `docs/agent-native-operating-workflow.md` (v0); ADR 0013 (Accepted, ratified 2026-08-13) |
| Product boundary | Human-reviewed `repository_sensemaking_brief` is the ratified external scope; routing deferred | ADR 0014 (Accepted, narrowed 2026-07-26) |
| Warrant / recommendation / selection / execution authority | **Separated and ratified**; auto-invoke is compatibility metadata; consumers fail closed | ADR 0026 (Accepted 2026-08-24); `tests/test_auto_invoke_authority_gating.py`; ADR 0018 SUPERSEDED |
| Workflow registry vs liveness | Identity and liveness separated; 8 of 23 registered workflows `compatibility_only`; planner/runtime/validator fail closed on non-active | ADR 0027 (Accepted 2026-09-01); `skills/workflow-planner/references/workflow-liveness.yaml`; PR #265 |
| Responsibility selection | **CONVENTION** (agent judgment + skill catalog); no machinery; automatic routing deliberately unratified; exercised by fresh contexts (R1 Q3; R4 repair-vs-retire) | operating workflow Reality map (R3-updated row); `using-sensemaking` SKILL.md sections 5-7 |
| Continuation across responsibilities | **On the product surface since R3** (operating map section 2 subsection + Reality map row). Demonstrated for mechanical (R2), judgment-class documentation (R3), and **implementation-class code + tests with a repair-vs-retire judgment (R4)** responsibilities. Cross-run prior-report identity deliberately left unresolved (not exercised) | operating map (commit `6ff4a89`); `R1-*.md` .. `R4-*.md` |
| Continuation artifacts that exist | `user_intent`, `session_summary`, `prompt_handoff`, `work_claim`, `reconciliation_report`, `repair_verification_report`. **Decision (U5): no new artifact type for continuation; Markdown record convention**, stated on the product surface with reopen conditions | `skills/workflow-planner/references/artifact-contracts.yaml`; operating map section 6 bullet |
| Repository-level development-direction representation | This record is the first representation; the operating map documents the field set that proved necessary. Fresh contexts selected and performed the named responsibility and could explain why it beat alternatives | this file; operating map section 2 subsection; R1 Q3; R2/R3/R4 section 1 of each report |
| Deterministic machinery | validators (`validate-output.py` dispatch -> `validate-artifact.py` + specialized), probe engine, `gate_relationship_findings.py`, `run-ledger.py`, `workflow-runtime.py` (paths/plan/gates/sessions), `workflow_liveness.py`, `validate-repo.py`, `probe_skill_distribution.py`. Used as referees by every fresh context (R2 probe+pytest+validate-repo; R3 validate-repo+pytest; R4 pytest both code pages+validate-repo); judgment stayed with the agent. Role described across the retirement plan, the boundary doc, `CONTEXT.md`; **not consolidated (G5 -> R5)** | `scripts/`; retirement plan classification tables; R2-R4 "Commands run" |
| CI on `main` | 13 jobs in `.github/workflows/validation.yml` incl. `probe-gate` and `core-assertions` (7 pytest files). Gate commit `e1db7dc` (2026-08-11) is on `main`'s first-parent line (no PR). `main` CI green at `df46871` and `f10b7da` | `validation.yml`; `git log --first-parent`; `gh run list` |
| Hooks | `.claude/hooks/sessionstart.md` is a Markdown description of a SessionStart bootstrap reminder (routing-era prose); `.claude/settings.json` is `{}` (no executable hook); skills are discovered because they are copied to `~/.claude/skills/` (`setup_skills.py`, `INSTALLATION.md`), and `CLAUDE.md` is the actual session-start injection surface. No continuation/liveness hook exists; R1-R4 continuation events were explicit dispatches, none missed; the operating map says "no hook at this scale" with reopen conditions. **Disposition not yet written on the product surface; hook doc still stale (G3 -> R5)** | those files; operating map section 6 bullet |
| Real-use evidence of the operating loop | Workflow v0 dogfood on 2 repos (`KEEP_WITH_WATCH_ITEMS`); 3 normal-use episodes as **GitHub issue comments on Issue #218** (GitHub-only); recurring boundary there: PR-head qualification did not bind the integration base | `experiments/evidence/0021`, `0022`; Issue #218 |
| Real execution evidence per active workflow (for U4) | run ledgers/mode coverage/evidence exist for: `fast-local-diagnostic`, `full-local-sensemaking`, `full-fog-workflow`, `fast-path-workflow`, `docs-contract-reconciliation` (guided; dogfooded 2026-08, evidence 0018/0019), `architectural-review-planning-workflow` (golden path, 2026-07-25), `docs-architecture`, `setup-sensemaking-repo`, `product-strategy-sprint`, `skill-maintenance-loop`, `docs-implementation-workflow`; `artifact-reconciliation` has agent-native execution evidence (`artifacts/reconciliation_report.md`, 2026-08-22) but no run ledger; `autonomous-sprint-preflight`, `product-discovery-sprint`, `skill-evaluation-workflow` have plan_only or test-only traces | `docs/mode-coverage.yaml`; `artifacts/0[1-4]-orchestration-run/run-ledger.jsonl`; `experiments/evidence/`; `artifacts/reconciliation_report.md` |
| Research lanes (non-ratified) | C6R (#226 open); warrant-as-primitive; uncertainty-selection; PHB meta-finding (2026-08-30); semantic-control-map persistence trial OPEN (min close 2026-09-28) -- this campaign supplied its first consultation, over-read, and MECH-refresh events | `docs/research/control-model-research-agenda.md`; `docs/semantic-control-map-trial-log.md` |
| Goal A external validation | ACTIVE but **halted in this environment** | Issue #255; evidence 0023 |
| Repository visibility | public (`ThorStarlord/sensemaking-skills`) | `gh repo view` |

**Local qualification procedure (C11).** The package is installed editable
from the shared `main` checkout, so any other worktree imports *that*
checkout's `src/` unless `PYTHONPATH=src` is set; Gate A tests detect this
and fail closed (13 collection errors). Therefore every local full-suite run
is `PYTHONPATH=src python -m pytest tests -q -p no:cacheprovider
--ignore=tests/integration --continue-on-collection-errors`, in a clean
worktree, and compared like-for-like against the same command on a clean
`main @ f10b7da` worktree. Windows/Python 3.14 baseline without
`PYTHONPATH=src`: 2204 passed / 34 failed / 15 errors (13 = Gate A guard);
Linux CI on the same commit is green, so CI is the referee for
cross-platform claims and the local run is a like-for-like diff only. The
`PYTHONPATH=src` baseline run is in progress at R4 close-out.

---

## 3. COMPLETED CAMPAIGN RESPONSIBILITIES

| # | Responsibility | Result | Evidence |
|---|---|---|---|
| R0 | Reconstruct current product/capability state; select first bounded responsibility; establish durable campaign record | this file v1 | commit `2bc8a2c` |
| R1 | Fresh-context reconstruction probe | Q1-Q5 `RECONSTRUCTED`; Q6 `PARTIAL` (narrow `AUTHORITY_AMBIGUITY`); Q7 five omissions (four missing-durable-state by content, one substrate risk); 39 files / 25 calls. Close-out: charter committed; authority sourced; push/CI status recorded | `R1-fresh-context-reconstruction.md`; commit `b4335c3` |
| R2 | Fresh-context mechanical continuation trial (semantic-control-map bookkeeping, 7 steps) | All steps performed; exact diff; caught record error F1 (gate provenance); 9 files / 36 calls. **Audit VERIFIED** | `R2-continuation-trial.md`; `fa2dd68`, `9160a5b`; close-out `2adfeaf` |
| R3 | Fresh-context judgment-class documentation trial (continuation pattern into the operating map) | One product file +88/-3; cross-run identity left unresolved; two record overstatements flagged; 8 files / 24 calls. **Audit VERIFIED** | `R3-operating-map-reconciliation.md`; `6ff4a89`, `fbbb637`; close-out `09bdf5e` |
| R4 | Fresh-context **implementation-class** trial: repair or retire two local test defects from this record, with a repair-vs-retire judgment | Reproduced D1/D2 exactly before changing anything. D1: repaired (`encoding="utf-8"` x3; 1 failed -> 0 under cp1252). D2(a): repaired, import lines only, after establishing from git that the root re-export was removed two days after the test was written and both classes are live (5 passed both code pages). D2(b): path fixed, then 5/13 failed for validator-fixture drift, **reverted per the spec's own branch** and reported; validators untouched. Core-assertions set green under utf-8 (99 passed); `validate-repo.py` exit 0; diff 2 files +5/-5, all under `tests/`. Flagged a real tension in the spec (F1: step-5 expectation ignored the revert branch) and an understatement in the D2 row (F2). 14 files / 40 calls. **Dispatcher audit: VERIFIED** (diff read line by line; named suites re-run by the dispatcher under both code pages with `PYTHONPATH=src`: 28 passed / 1 skipped and 99 passed / 1 skipped; D2(b) confirmed byte-identical to base) | `R4-implementation-continuation.md`; commits `769a180`, `ac47191` |
| R4 close-out (dispatcher) | Audit; record v5; qualification procedure (C11); R5 specified | this commit | section 14 |

---

## 4. EVIDENCE PRODUCED

- `docs/campaigns/agent-native-self-development/CAMPAIGN-STATE.md` (this file), `CHARTER.md`, `R1-*.md`, `R2-*.md`, `R3-*.md`, `R4-*.md` (all reports verbatim from the fresh contexts).
- Product-side changes so far: `docs/agent-native-operating-workflow.md` (R3); `docs/semantic-control-map.md` rows SE1/SE2/SA13/SA9 + SA10/SA12; `docs/semantic-control-map-trial-log.md` sections A-D; `docs/semantic-control-map-trial.md` step-4 selector; `docs/enforcement-contract.md` addendum (R2 + close-out); `tests/test_path_drift.py`, `tests/test_integration_external_repo.py` (R4).

---

## 5. CURRENTLY DEMONSTRATED CAPABILITIES

(Demonstrated = real use with durable evidence, not merely documented.)

- Agent-native `repository_sensemaking_brief` production + mechanical validation on two structurally different repositories (evidence 0021, 0022).
- Responsibility selection without automatic routing; stop at owner/authority boundary (evidence 0022; #218 episodes 001, 003; #255).
- Claim reconciliation and finding-specific repair verification (evidence 0018-0020; `artifacts/reconciliation_report.md`).
- Fail-closed authority on `auto_invoke_next_workflow` and compatibility-only workflow selection (ADR 0026/0027 test suites).
- Deterministic probe-engine enforcement in CI (`probe-gate`, `core-assertions`).
- **(R1)** A fresh context reconstructed campaign state from the record + repository with no conversation memory.
- **(R2)** A fresh context performed a mechanical multi-file responsibility from the record alone and corrected a wrong fact in the record from git evidence.
- **(R3)** A fresh context performed a judgment-class documentation responsibility, narrowing the spec where the evidence supported less and keeping an unresolved item unresolved.
- **(R4)** A fresh context performed an **implementation-class** responsibility from the record alone: reproduced before changing, changed code, ran the named test selections under both code pages, exercised a repair-vs-retire judgment on two files with different outcomes (repair / repair / revert-and-report), and stopped at the spec's boundary when its own branch said revert.
- **(count basis)** Five record-mediated handoffs (R0 -> R1 -> R2 -> R3 -> R4, each returning to the dispatcher for audit); four into fresh contexts; zero shape errors in the record; four record errors/overstatements caught by the continuing contexts' verification steps (R2 F1, R3 M2/M3, R4 F1/F2) -- none caused a wrong action.
- **(substrate)** In this harness an isolated sub-agent's direct file write to the worktree persisted four times (R1-R4). Narrows, for this harness only, the "isolated sub-agent direct write BLOCKED" finding of evidence 0023 / Issue #255.

---

## 6. KNOWN MATERIAL GAPS

| id | Gap | Condition(s) | Class | Status |
|---|---|---|---|---|
| G1 | Continuation from a durable record for implementation-class responsibilities | 4, 5 | CAMPAIGN_RELEVANT | **CLOSED (R4)** with limitation: a small test-only change (no `src/` change, no new test written); larger implementation-class continuations remain unobserved |
| G2 | Repository-level development direction was not represented before this campaign | 6 | CAMPAIGN_RELEVANT | LARGELY CLOSED: this record + operating map subsection; limitation: one campaign, one repository |
| G3 | Role of hooks: no executable hook; hook doc prose stale (routing-era); no disposition sentence on the product surface for the bootstrap "hook" or for the admissible future hook shape | 8, 11 | CAMPAIGN_RELEVANT | OPEN -> R5 |
| G4 | Per-workflow disposition in campaign vocabulary not recorded | 9 | CAMPAIGN_RELEVANT | OPEN -> R6 |
| G5 | Deterministic-script role not consolidated in one place | 7 | CAMPAIGN_RELEVANT | OPEN -> R5 |
| G6 | Semantic-control-map rows stale from construction | 11 | CAMPAIGN_RELEVANT | **CLOSED** (R2 + close-out) |
| G7 | Authority grants not sourced in the repository | 5, 13 | CAMPAIGN_RELEVANT | **CLOSED** (R1 close-out) |
| G8 | Some cited evidence lives only in GitHub | 5, 13 | DEFERRED | documented limitation |
| G9 | Product operating map did not represent the demonstrated continuation pattern | 4, 6, 11 | CAMPAIGN_BLOCKING | **CLOSED** (R3) |
| G10 | The record's task specs have twice stated expected outcomes that ignored one of their own decision branches (R4 F1) or understated a defect (R4 F2). Neither caused a wrong action, but each cost report text | 5 | CAMPAIGN_RELEVANT | mitigated by C9 refinement; watch for recurrence |

---

## 7. ACTIVE CONSTRAINTS

- C1 **Bootstrap constraint** (`CHARTER.md`): no `repo-sensemaker`, `using-sensemaking`, registered workflows, runtime routing, fog routing, Skill-to-Skill continuation mechanisms under evaluation, or hooks as the campaign controller.
- C2 **Authority** (section 11): the dispatcher pushes and opens PRs (charter); fresh contexts commit locally and do not push; merge to `main`, ADR acceptance, canonical contract/registry ratification, and external tracker writes are **owner** actions. Never falsify owner decisions or ADR `**Status**` lines.
- C3 **Semantic-control-map trial is OPEN**: no new rows; MECH refresh on triggers only; log consultation/over-read events.
- C4 **Goal A is halted** in this environment (#255); no episodes. Issue #218 episodes only from ordinary work and only by an owner-authorized tracker write.
- C5 **Windows cp1252**: console output ASCII-only; explicit encodings in file I/O; run pytest under the default code page and under `PYTHONUTF8=1` to separate encoding reds from real reds. CI runs on Linux (utf-8).
- C6 **Worktree per session**: `H:/GithubRepositories/smk-campaign`; never the shared `main` checkout.
- C7 **Machinery promotion rule** (operating map section 7).
- C8 **One responsibility at a time**: while a fresh-context responsibility runs, the dispatcher does not edit files it may read and does not open a second responsibility.
- C9 **Task specs must contain verification steps, not only assertions, and their expected outcomes must be stated per decision branch** (R4 F1: a "clean collection" expectation contradicted the spec's own revert branch). Fresh contexts prefer repository evidence over this record where they conflict, and flag rather than silently correct.
- C10 **Don't touch unrelated code** (`AGENTS.md` rule 4): implementation-class responsibilities name their files.
- C11 **Local qualification uses the worktree's own package**: `PYTHONPATH=src` for every pytest run in a worktree; like-for-like against a clean `main` worktree run with the same command (section 2).

---

## 8. OPEN DECISION-CHANGING UNCERTAINTIES

| id | Uncertainty | Source | Cheapest sufficient evidence | Status |
|---|---|---|---|---|
| U1 | What continuation state does a fresh context fail to reconstruct? | empirical | R1 | **RESOLVED (R1)** |
| U2 | Do the outer loop and the inner loop need different durable state? | repository_evidence + trace | R2-R4 traces | **RESOLVED for this campaign's scale (R2, R3, R4).** One record carried both for mechanical, judgment-docs, and implementation-class bounded responsibilities: sections 6-10 = outer-loop rationale; the numbered step spec in section 10 (verification steps, sourced authority, not-authorized list, per-branch expected outcomes, stop condition) = inner-loop state. Untested: responsibilities large enough to need their own multi-file task state; more than one dispatcher |
| U3 | Is any hook warranted beyond a documented bootstrap? | empirical | recurrent continuation event a manual step keeps missing | OPEN but evidence is consistent across R1-R4: none observed. Remaining work is the product-surface disposition (G3 -> R5) |
| U4 | Which registered workflows have enough real traces for a disposition other than `INSUFFICIENT_EVIDENCE`? | repository_evidence | inventory -> disposition doc | EVIDENCE GATHERED; disposition pending (G4 -> R6) |
| U5 | Continuation state: existing contracts, a new artifact type, or a Markdown record? | repository_evidence | U2 + cost of a new artifact type | **DECIDED FOR NOW: Markdown record convention**, on the product surface with reopen conditions |
| U6 | Can a fresh context perform (not only reconstruct) a bounded task from this record? | empirical | R2 | **RESOLVED (R2)**; extended by R3 (judgment) and R4 (code) |
| U7 | Does the pattern hold for an implementation-class responsibility? | empirical | R4 | **RESOLVED (R4): yes** for a small test-only change incl. reproduce-first, repair-vs-retire judgment, and revert-on-mismatch discipline. Not shown: `src/` changes, new tests, larger surfaces |
| U8 | What is the disposition of `tests/test_validate_brief_json.py` (D2b): refresh its fixtures/expectations to the current validator ruleset, or retire it? `tests/fixtures/brief-valid.md` is also referenced by other live tests | repository_evidence | check whether those other tests expect `brief-valid.md` to pass the current validator; if none does, the fixture is historical | OPEN; DEFERRED (not campaign-limiting; not in CI) |

---

## 9. CURRENT HIGHEST-LEVERAGE CAPABILITY BOUNDARY

**Conditions 7 and 8 on the product surface** (G3, G5). The continuation
property is now demonstrated across all three responsibility classes and is
documented in the operating map. The charter's remaining architectural
questions -- what deterministic scripts own and must not own, and what hooks
are for (if anything) -- are answered by evidence (ADR 0013/0026/0027, the
retirement plan, enforcement-contract section 4, and R2-R4's use of scripts as
referees with judgment left to the agent) but are stated nowhere in one place,
and the one hook document the repository has is wrong about its own mechanism.
After R5: R6 (workflow disposition, condition 9), then R7 (full qualification +
final report, conditions 12-13).

---

## 10. CURRENT / NEXT WARRANTED RESPONSIBILITY

```text
R5  Disposition of deterministic machinery and hooks on the product surface
    (documentation reconciliation; performed by a fresh context from this record)

CAMPAIGN CAPABILITY AFFECTED:   bounded role of deterministic scripts (condition 7);
                                defined, evidence-supported role of hooks
                                (condition 8); docs agree with implementation
                                (condition 11)
CURRENT LIMITATION:             the script role is scattered across four documents;
                                no product document states what hooks are and are
                                not for; .claude/hooks/sessionstart.md claims a
                                mechanism that does not exist and teaches
                                routing-era behavior
WHY IT MATTERS TO THE MISSION:  the candidate architecture (CHARTER.md items 5-6)
                                asks exactly these two questions; the evidence now
                                exists; leaving it scattered means a product user's
                                agent cannot find the answer
BOUNDED RESPONSIBILITY:         steps for the fresh context:
  1. read this file (sections 2 rows "Deterministic machinery" and "Hooks", 6
     G3/G5, 7, 8 U3, 10); CHARTER.md "Candidate Architecture" items 5, 6 and
     "Hooks Policy During This Campaign"; .claude/hooks/sessionstart.md (full);
     .claude/settings.json; CLAUDE.md (the "SessionStart hook" section only);
     docs/decision-orchestration-boundary.md (full); docs/agent-native-operating-
     workflow.md sections 1, 5, 6; docs/2026-08-programmatic-runner-retirement-
     plan.md "Responsibility classification" tables; docs/enforcement-contract.md
     section 4; docs/adr/0013 "Amendment (2026-08-13)"; docs/adr/0026 section 2;
     docs/adr/0027 "Consumer behavior"; src/sensemaking_skills/setup_skills.py
     module docstring; INSTALLATION.md lines ~105-120; the "Commands run" /
     "Files consulted" sections of R2-*.md, R3-*.md, R4-*.md (which scripts fresh
     contexts used as referees).
  2. VERIFY before writing (if any check fails materially, write the report and
     stop): (a) `.claude/settings.json` is `{}` and `grep -rn hooks .claude/`
     finds no configured hook (only the Markdown description); (b) the hook doc
     still contains the routing-era phrases "picks correct workflow" /
     "auto-fix vs. escalate" / "recommended_workflow" (quote them); (c) quote
     the boundary doc's "Current ownership model" table header and the operating
     map's Reality-map rows you will touch; (d) each script you list in the
     machinery table exists under scripts/ (ls).
  3. edit docs/decision-orchestration-boundary.md: add ONE new section titled
     "## Deterministic machinery and hooks" placed after "## Current ownership
     model" and before "## Architectural guardrails", containing:
     (a) a table "What deterministic scripts own" -- one row per responsibility
         class, not per script: contract/schema validation (validate-output.py
         dispatch, validate-artifact.py + specialized validators; ADR 0013
         amendment item 2); measured repository state (probe-repo.py,
         repo_probes.py, probe_relationships.py; CONTEXT.md "Evidence model");
         mechanical gate policy (gate_relationship_findings.py; enforcement-
         contract section 4: blocks only mechanically decidable findings that
         need no semantic review); artifact path resolution + run ledger
         (workflow-runtime.py, run-ledger.py; ADR 0010); registry integrity and
         liveness (validate-repo.py, workflow_liveness.py; ADR 0027);
         distribution drift (probe_skill_distribution.py); bounded execution
         coordination of an already-selected responsibility incl. retry/wait/
         fail (workflow-runtime.py; this document's "Execution and orchestration
         layer"). Each row: responsibility, script(s), authority source.
     (b) a table "What deterministic scripts must not own": responsibility
         selection and uncertainty selection (ADR 0013; guardrail 4);
         stop/continue/escalate decisions (operating map "STOP CONDITIONS");
         authority decisions incl. spawning a next workflow without a separate
         explicit authority event (ADR 0026); semantic interpretation of
         findings (`requires_semantic_review: True` never blocks; enforcement-
         contract section 4); routing from fog type to implementation (ADR 0018
         SUPERSEDED, ADR 0014). Each row with its source.
     (c) one paragraph of evidence: in campaign R2-R4 every fresh context used
         those scripts as referees (name which) and every judgment (what to
         refresh, repair vs retire, what to leave unresolved) stayed with the
         agent; cite the report sections.
     (d) a subsection "### Hooks" stating, from evidence: mechanism truth (no
         Claude Code hook is configured in .claude/settings.json; the file
         .claude/hooks/sessionstart.md is a Markdown description; the bootstrap
         is discoverable because skills are copied to ~/.claude/skills and
         CLAUDE.md points at it); current disposition (no continuation or
         liveness hook is warranted: R1-R4 continuation events were explicit
         dispatches, none missed, the durable record sufficed -- cite the
         operating map section 2 subsection and section 6 bullet); the only
         admissible future hook shape per the repository's authority model
         (mechanical: detect artifact -> validate -> register provenance/state
         -> signal the agent to reassess; never "artifact X -> execute Skill Y",
         per ADR 0026 and guardrail 4); and the reopen condition (a recurrent
         continuation event that a manual step keeps missing, observed in real
         use). Keep the document's voice and ASCII arrows.
  4. edit docs/agent-native-operating-workflow.md section 5 Reality map only:
     add two rows, "Deterministic machinery" and "Hooks", each with Existing
     support / Current status / What not to assume, pointing at the new
     boundary-doc section. No other change to that file.
  5. edit .claude/hooks/sessionstart.md: correct the mechanism claims (no
     executable hook; description of a convention; how the bootstrap is
     actually discovered) and replace the routing-era teaching bullets with
     the current bootstrap's language (responsibility before Skill;
     `recommended_workflow_id` is a recommendation, not execution authority;
     validation is not closure) -- cite skills/using-sensemaking/SKILL.md
     sections rather than restating them. Keep the file, its frontmatter, and
     its structure; if `trigger: session-start` is misleading, add a
     `note:` line rather than deleting it. Do not add a hook.
  6. edit CLAUDE.md, the "SessionStart hook" section ONLY: add one or two
     sentences stating that no executable hook is configured and that the
     bootstrap reaches agents through this file plus the installed
     `using-sensemaking` skill, with a pointer to the new boundary-doc
     section. Do not touch any other CLAUDE.md section.
  7. validate: `python scripts/validate-repo.py` (exit 0);
     `grep -rln "sessionstart\|\.claude/hooks" tests/` and run any test file
     found, before and after your edits (report both results; if a test
     encodes the stale prose, do NOT edit the test -- revert the conflicting
     sentence and report); `PYTHONUTF8=1 PYTHONPATH=src python -m pytest
     tests/test_path_drift.py -q` (expect green); confirm every markdown link
     you added resolves relative to its file; confirm the four edited files
     stay ASCII and keep their line endings.
  8. `git diff --stat` -> expect exactly 4 files (or 3 if step 7 forced a
     revert of the CLAUDE.md sentence -- say which); commit on
     campaign/agent-native-self-development with subject prefix `campaign(R5):`
     and trailer `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`;
     do NOT push; do NOT edit CAMPAIGN-STATE.md.
  9. write docs/campaigns/agent-native-self-development/R5-machinery-and-hooks-disposition.md
     (second `campaign(R5):` commit): quoted before/after of each changed
     passage; what this record was sufficient for; what was missing/wrong
     (flag, do not silently fix); files consulted beyond the record and why;
     tool-call count; authority questions and resolutions; anything skipped.
AUTHORITY FOR R5 (sourced):     CHARTER.md ("architecture reconciliation" and
                                "documentation reconciliation" are listed bounded
                                responsibilities; "Hooks Policy": establish
                                manually what is needed before building -- done in
                                R1-R4); docs/decision-orchestration-boundary.md
                                header ("architecture clarification ... does not
                                introduce a new runtime, registered workflow,
                                Skill, routing table, or automation contract" --
                                the addition is in kind); operating map section 7
                                revision trigger; CLAUDE.md is project
                                documentation surfaced for owner review in PR #268.
NOT AUTHORIZED IN R5:           configuring any hook in .claude/settings.json;
                                adding or editing scripts, src/, tests/, Skills
                                (incl. skills/using-sensemaking/SKILL.md),
                                contracts, registries, ADRs, CONTEXT.md; editing
                                CLAUDE.md outside its SessionStart section; any
                                other doc; pushing; merging; tracker writes;
                                editing CAMPAIGN-STATE.md.
STOP CONDITION:                 both commits exist and the report is written; OR
                                a step-2 check fails materially -> report and stop
                                without editing; OR step 7 finds a test encoding
                                the stale prose -> revert only the conflicting
                                sentence(s), report, and still commit the rest.
EXPECTED EVIDENCE OF PROGRESS:  commits `campaign(R5): ...`; the R5 report;
                                dispatcher audit incl. exact-head CI; G3 and G5
                                closed; conditions 7 and 8 MET on the product
                                surface (if step 7 forced a revert, condition 8
                                is PARTIAL and the conflict is recorded in the
                                report for the dispatcher).
```

---

## 11. AUTHORITY: GRANTS, THEIR SOURCES, AND OWNER DECISIONS REQUIRED

| Grant / boundary | Source |
|---|---|
| Own the campaign end to end on the campaign branch; continue autonomously through multiple bounded tasks | `CHARTER.md` "Campaign Mission" |
| Use ordinary engineering infrastructure (tests, validators, probe engine, git, GitHub CI, PRs) | `CHARTER.md` "Important Bootstrap Constraint" |
| Push branches / open PRs; qualify exact PR heads (dispatcher only) | `CHARTER.md` "Git and Change Discipline" |
| Branch-local implementation of reversible, non-ratified changes is agent-decidable; ratification is not | `CONTEXT.md` "Authority model"; `CHARTER.md` "Architecture Discipline" |
| Bounded implementation / test-harness improvement of named files; a local defect may be selected when it advances a campaign capability | `CHARTER.md` "Responsibility Execution", "Strategic Selection Rule"; `AGENTS.md` rules 3-4 |
| Documentation / architecture reconciliation of the operating map and boundary doc, surfaced for owner review | `docs/agent-native-operating-workflow.md` section 7; boundary doc header; `CHARTER.md` |
| MECH refresh of semantic-control-map rows; trial-log entries | `docs/semantic-control-map-trial.md` "Row maintenance" |
| Merge to `main` = owner | ADR 0014/0026/0027 headers; `docs/adr/README.md`; `CONTEXT.md` non-identities; the charter grants no merge authority |
| ADR status / owner decisions must not be falsified | `docs/adr/README.md`; `AGENTS.md` rule 5 |
| External tracker writes require explicit authority | operating map section 4 (ADR 0019 PROPOSED) |
| Ask the owner only for product preference, authority expansion, irreversible tradeoffs, external environment, or material product-direction acceptance | `CHARTER.md` "Owner Decisions" |

Owner decisions required (none blocking the next responsibility):

1. **Merge authority for the campaign PR (#268)** -- standing.
2. **Whether to record the R1-R4 substrate observation on Issue #255** (an
   external tracker write). Recommended but not required.

---

## 12. DEFERRED NON-CAMPAIGN FINDINGS

| id | Finding | Class | Disposition |
|---|---|---|---|
| D1 | `tests/test_path_drift.py` `read_text()` without encoding (cp1252 red) | LOCAL_BUT_REAL | **CLOSED (R4, `769a180`)** |
| D2 | (a) `tests/test_integration_external_repo.py` stale root import -- **CLOSED (R4)**. (b) `tests/test_validate_brief_json.py`: the underscore script path never existed on any branch; after a path fix the file fails 5/13 because its fixtures/expectations predate four newer validator rule families (`HALLUCINATED_WORKFLOW_ID`, `weakness_type` x2, `EVIDENCE_QUOTE_NOT_FOUND` on `tests/fixtures/brief-valid.md`). Not a path defect; a fixture/expectation drift. Not in CI | LOCAL_BUT_REAL | (b) DEFERRED -> U8 (refresh vs retire is a fixture/validator-semantics decision; `brief-valid.md` is shared with other tests) |
| D3 | `roadmap.md` stale | HISTORICAL_ONLY | no action |
| D4 | `docs/HARDENING_STATUS.md` 5-type fog taxonomy | HISTORICAL_ONLY | no action |
| D5 | `docs/candidate/architecture-decision.md:7` dangling link | HISTORICAL_ONLY | no action |
| D6 | `unevaluable` verdict category not in contract | DEFERRED | needs a real case |
| D7 | normal-use lane "0 episodes" is a dated snapshot | NO_ACTION_WARRANTED | none |
| D8 | `validation.yml` line 14 comment stale | LOCAL_BUT_REAL | deferred (fires trial triggers) |
| D9 | Map row SE10 vs current probe output; trigger not fired | INSUFFICIENT_EVIDENCE | leave |
| D10 | Trial protocol step-4 selector | LOCAL_BUT_REAL | **fixed at R2 close-out** |
| D11 | `tests/test_owner_approval_artifact.py` and `tests/test_run_control_0016_draft_package.py` `rglob` the repo root; pathological on the shared checkout's ~76k untracked files; fine in a clean worktree/CI | LOCAL_BUT_REAL (environment) | deferred; run suites in clean worktrees (C11) |
| D12 | `tests/test_mode_coverage_aggregation.py::test_validator_passes_after_legitimate_update` fails on `main`: `scripts/validate-mode-coverage.py` run as a subprocess cannot import `workflow_liveness` via `scripts/_validator_utils.py` (`ModuleNotFoundError`). Pre-existing on `main`; not in CI | LOCAL_BUT_REAL | deferred; candidate for a future implementation-class continuation |
| D13 | `tests/test_integration_external_repo.py` prints U+2713 (fails with `pytest -s` on cp1252); `src/sensemaking_skills/config.py:133` opens YAML without encoding (R4 section 11) | LOCAL_BUT_REAL, low | deferred |
| D14 | Local Windows/Python 3.14 baseline on clean `main @ f10b7da`: 34 failed / 15 errors (13 errors = Gate A guard without `PYTHONPATH=src`; others incl. `test_invocation_paths` x4, `test_stage1_auteur_prep_package` x5, `test_state_honesty_guard` x2, `test_workflow_planner_skill_fog_contract` x3, `test_generate_plan_conformance` x2, brief-skeleton/validator-chain tests). Linux CI green on the same commit | LOCAL_BUT_REAL (environment/platform) | not campaign scope; like-for-like diff only (C11) |

---

## 13. CAMPAIGN ACCEPTANCE STATUS

| # | Condition | Status after R4 | Basis |
|---|---|---|---|
| 1 | Top-level semantic control model explicit and coherent | MET | CONTEXT.md, boundary doc, ADR 0013; R1 Q1/Q2 |
| 2 | Role of active coding agent clear | MET | ADR 0013 + amendment |
| 3 | Warrant / responsibility / capability / authority not conflated | MET | ADR 0026/0027; every fresh context respected every boundary (R2-R4) |
| 4 | Durable artifacts can carry continuation state across responsibilities | MET (mechanical, judgment-docs, implementation-class), on the product surface | R1-R4; operating map section 2 subsection |
| 5 | One realistic multi-responsibility task continued from durable state without hidden conversation memory | MET: R0 -> R1 -> R2 -> R3 -> R4 across five contexts with this record as the only shared state, incl. one code change; limitation: small surfaces, single dispatcher | R1-R4 reports |
| 6 | Repository-level development direction representable for consequential capability selection | LARGELY MET; limitation: one campaign, one repository | this record; operating map |
| 7 | Role of deterministic scripts bounded and coherent | LARGELY MET by evidence, not consolidated on the product surface | G5 -> R5 |
| 8 | Role of hooks defined and evidence-supported | PARTIAL: evidence complete (no hook warranted; admissible shape known); disposition and hook-doc repair pending | G3 -> R5 |
| 9 | Old workflow system has a clear disposition | PARTIAL | ADR 0027; inventory in section 2; G4 -> R6 |
| 10 | Existing useful functionality not destroyed | MET so far (docs + 2 test files; `validate-repo.py` green; CI green on every pushed head so far) | section 15 |
| 11 | Tests, validators, contracts, docs, implementation agree sufficiently | PARTIAL | G3 (-> R5); D2(b)/U8; D8/D12 minor |
| 12 | Repository passes appropriate complete qualification | PARTIAL | `main` CI green at base; PR #268 CI green at `b4335c3`, `2adfeaf`, `09bdf5e`; `ac47191` pending; full-suite like-for-like pending (R7) |
| 13 | Remaining material limitations explicitly documented | IN PROGRESS | this file |

Disposition after R4: **CONTINUE** (R5).

---

## 14. Responsibility trace (append-only)

```text
2026-09-02  R0  reconstruction + campaign record v1                     -> next: R1
2026-09-02  R1  fresh-context reconstruction probe (Q1-Q5 ok; Q6 partial;
                5 omissions, repaired at close-out; record v2)          -> next: R2
2026-09-02  R2  fresh-context continuation trial: map rows refreshed;
                caught record error F1 (gate provenance)                -> audit
2026-09-02  R2  close-out: audit VERIFIED; SA10/SA12; protocol; record v3 -> next: R3
2026-09-02  R3  fresh-context judgment-class trial: continuation pattern
                reconciled into the operating map (+88/-3)              -> audit
2026-09-02  R3  close-out: audit VERIFIED; record corrections; record v4 -> next: R4
2026-09-02  R4  fresh-context implementation-class trial: D1 repaired,
                D2(a) repaired, D2(b) reverted-and-reported; spec
                tension F1 flagged                                       -> audit
2026-09-02  R4  close-out: audit VERIFIED; C9/C11; record v5             -> next: R5
```

---

## 15. Remote / integration status (updated by the dispatcher, never assumed)

```text
pushed:        ac47191 (R4) -> origin/campaign/agent-native-self-development
               this close-out commit: pushed after this commit
PR:            #268 (draft) https://github.com/ThorStarlord/sensemaking-skills/pull/268
last main CI:  Validator Ecosystem completed/success @ f10b7da (2026-09-02T03:43Z)
campaign CI:   b4335c3 success (33591059541); 2adfeaf success (33592107833);
               09bdf5e success (33592941441); ac47191 in progress at R4 close-out
merged:        nothing (owner decision)
```
