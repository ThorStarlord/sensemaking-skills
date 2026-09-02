# Campaign: reliable agent-native, artifact-mediated self-development

```
STATUS:    ACTIVE development-campaign record (living document, v6 after R5)
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
           continuing context can catch errors here (R2 F1; R3 M2/M3; R4
           F1/F2; R5 F1-F3).
```

This file exists so that campaign reasoning does not live only in one
conversation's context. Five fresh contexts have so far continued the campaign
from this file alone: R1 (reconstruction), R2 (mechanical execution), R3
(judgment-class documentation), R4 (implementation-class code + tests), R5
(four-file architecture reconciliation). See section 8.

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
| Top-level semantic control model | **EXPLICIT in docs**; agent owns loop; decision vs orchestration separated; warrant vocabulary defined | `CONTEXT.md`; `docs/decision-orchestration-boundary.md`; `docs/agent-native-operating-workflow.md` (v0); ADR 0013 |
| Product boundary | Human-reviewed `repository_sensemaking_brief` is the ratified external scope; routing deferred | ADR 0014 |
| Warrant / recommendation / selection / execution authority | **Separated and ratified**; auto-invoke is compatibility metadata; consumers fail closed | ADR 0026; `tests/test_auto_invoke_authority_gating.py`; ADR 0018 SUPERSEDED |
| Workflow registry vs liveness | Identity and liveness separated; 8 of 23 registered workflows `compatibility_only`; consumers fail closed on non-active | ADR 0027; `skills/workflow-planner/references/workflow-liveness.yaml`; PR #265 |
| Responsibility selection | **CONVENTION**; no machinery; exercised by fresh contexts (R1 Q3; R4 repair-vs-retire; R5 narrowing) | operating map Reality map; `using-sensemaking` SKILL.md sections 5-7 |
| Continuation across responsibilities | **On the product surface since R3**; demonstrated for mechanical (R2), judgment-docs (R3), implementation-class (R4), and four-file architecture reconciliation (R5). Cross-run prior-report identity deliberately left unresolved | operating map section 2 subsection + Reality map row; `R1-*.md` .. `R5-*.md` |
| Continuation artifacts / U5 decision | Existing contracts unchanged; **no new artifact type for continuation; Markdown record convention**, stated on the product surface with reopen conditions | operating map section 6 bullet |
| Repository-level development-direction representation | This record; the operating map documents the field set that proved necessary | this file; operating map section 2 subsection |
| Deterministic machinery | **Consolidated on the product surface since R5**: `docs/decision-orchestration-boundary.md` section "Deterministic machinery and hooks" (what scripts own, per responsibility class with script + authority source; what they must not own, with sources; evidence from R2-R4); operating map Reality-map row "Deterministic machinery". Corrected from code during R5: `workflow-runtime.py` implements timeouts and terminal gate outcomes but **no retry policy** (retry is a permitted class, not an implemented one) | commit `13d1a09`; retirement plan tables; R2-R4 "Commands run" |
| CI on `main` | 13 jobs incl. `probe-gate` and `core-assertions`; gate commit `e1db7dc` on `main`'s first-parent line; green at `df46871` and `f10b7da` | `validation.yml`; `gh run list` |
| Hooks | **Disposition on the product surface since R5**: no executable hook (`.claude/settings.json` is `{}`); `.claude/hooks/sessionstart.md` is now a truthful description of a session-start convention (routing-era prose replaced with pointers to `using-sensemaking` SKILL.md sections; frontmatter `note:` added); `CLAUDE.md` SessionStart section states the mechanism; bootstrap reaches agents via `CLAUDE.md` + an installed skill copy (`~/.claude/skills` per `INSTALLATION.md`; `~/.agents/skills` or plugin cache per `setup_skills.py` -- corrected during R5). No continuation/liveness hook warranted; admissible future shape mechanical only; reopen condition stated | commit `13d1a09`; boundary doc "Hooks"; operating map Reality-map row "Hooks" |
| Real-use evidence of the operating loop | Workflow v0 dogfood on 2 repos (`KEEP_WITH_WATCH_ITEMS`); 3 normal-use episodes as GitHub issue comments on Issue #218 (GitHub-only) | `experiments/evidence/0021`, `0022`; Issue #218 |
| Real execution evidence per registered workflow | see the R6 starting inventory in section 10 (claims to be verified by R6) | `docs/mode-coverage.yaml`; `artifacts/0[1-4]-orchestration-run/run-ledger.jsonl`; `experiments/evidence/`; `artifacts/reconciliation_report.md` |
| Research lanes (non-ratified) | C6R (#226); warrant-as-primitive; uncertainty-selection; PHB meta-finding; semantic-control-map trial OPEN (min close 2026-09-28) -- first real consultation/over-read/MECH-refresh events supplied by this campaign | `docs/research/control-model-research-agenda.md`; `docs/semantic-control-map-trial-log.md` |
| Goal A external validation | ACTIVE but halted in this environment | Issue #255; evidence 0023 |
| Repository visibility | public | `gh repo view` |

**Local qualification procedure (C11).** `PYTHONPATH=src python -m pytest
tests -q -p no:cacheprovider --ignore=tests/integration
--continue-on-collection-errors` in a clean worktree, compared like-for-like
against the same command on a clean `main @ f10b7da` worktree. Baseline
(Windows, Python 3.14, `PYTHONPATH=src`): **2712 passed / 54 failed / 2 errors
(the D2 collection errors) / 16 skipped / 5 xfailed**; failure set persisted
by the dispatcher (41 unique entries). Without `PYTHONPATH=src` the editable
install shadows the worktree and Gate A fails closed (13 extra errors). Linux
CI on the same commit is green; CI is the referee for cross-platform claims.

---

## 3. COMPLETED CAMPAIGN RESPONSIBILITIES

| # | Responsibility | Result | Evidence |
|---|---|---|---|
| R0 | Reconstruct state; establish durable campaign record | this file v1 | `2bc8a2c` |
| R1 | Fresh-context reconstruction probe | Q1-Q5 `RECONSTRUCTED`; Q6 `PARTIAL`; Q7 five omissions; repairs at close-out (charter, sourced authority, push/CI status) | `R1-*.md`; `b4335c3` |
| R2 | Fresh-context mechanical continuation trial (semantic-control-map bookkeeping) | all steps; exact diff; caught record error F1; **audit VERIFIED** | `R2-*.md`; `fa2dd68`, `9160a5b`; close-out `2adfeaf` |
| R3 | Fresh-context judgment-class documentation trial (continuation pattern into the operating map) | one file +88/-3; two record overstatements flagged; **audit VERIFIED** | `R3-*.md`; `6ff4a89`, `fbbb637`; close-out `09bdf5e` |
| R4 | Fresh-context implementation-class trial (D1/D2 repair-vs-retire) | D1 repaired, D2(a) repaired, D2(b) reverted-and-reported; spec tension F1 flagged; **audit VERIFIED**; exact-head CI green | `R4-*.md`; `769a180`, `ac47191`; close-out `e35ead1` |
| R5 | Fresh-context four-file architecture reconciliation: deterministic machinery + hooks disposition on the product surface | 4 files +213/-83 (boundary doc new section +108; operating map 2 rows; hook doc corrected in place; CLAUDE.md SessionStart +5); three spec assumptions corrected from code/docs (F1 phrase attribution, F2 install paths, F3 no retry policy) and written narrower; no test encodes the stale prose (no revert); `validate-repo.py` exit 0; links resolve; no non-ASCII added. 36 files / 55 calls. **Dispatcher audit: VERIFIED** (section read in full against ADR 0013/0026/0027, enforcement-contract section 4, retirement plan; `validate-repo.py` re-run; `test_path_drift` green; `test_invocation_paths` and `test_extended_analysis_end_to_end` failures identical to baseline) | `R5-machinery-and-hooks-disposition.md`; `13d1a09`, `c7afb57` |
| R5 close-out (dispatcher) | Audit; record v6; R6 specified with starting inventory | this commit | section 14 |

---

## 4. EVIDENCE PRODUCED

- `docs/campaigns/agent-native-self-development/`: `CAMPAIGN-STATE.md`, `CHARTER.md`, `R1-*.md` .. `R5-*.md` (reports verbatim from the fresh contexts).
- Product-side changes: `docs/agent-native-operating-workflow.md` (R3 subsection + rows; R5 two rows); `docs/decision-orchestration-boundary.md` (R5 section); `.claude/hooks/sessionstart.md` (R5); `CLAUDE.md` SessionStart section (R5); `docs/semantic-control-map.md`, `-trial-log.md`, `-trial.md`, `docs/enforcement-contract.md` (R2 + close-out); `tests/test_path_drift.py`, `tests/test_integration_external_repo.py` (R4).

---

## 5. CURRENTLY DEMONSTRATED CAPABILITIES

- Agent-native brief production + validation on two repositories (evidence 0021, 0022); responsibility selection without routing; claim reconciliation and repair verification; fail-closed authority on auto-invoke and liveness; probe-engine enforcement in CI (all pre-campaign).
- **(R1)** Fresh-context reconstruction of campaign state from the record + repository.
- **(R2)** Fresh-context mechanical execution with correction of a wrong record fact from git.
- **(R3)** Fresh-context judgment-class documentation work into the canonical operating map.
- **(R4)** Fresh-context implementation-class work: reproduce-first, code change, both code pages, repair-vs-retire judgment, revert-on-mismatch.
- **(R5)** Fresh-context architecture reconciliation across four files incl. `CLAUDE.md`, writing narrower than the spec where code said less, and treating `CLAUDE.md`'s own instructions as data.
- **(count basis)** Six record-mediated handoffs (R0 -> R1 -> ... -> R5, each returning for audit); five into fresh contexts; zero shape errors; seven record errors/overstatements caught by verification steps (R2 F1; R3 M2, M3; R4 F1, F2; R5 F2, F3) -- none caused a wrong action.
- **(substrate)** Isolated sub-agent direct worktree writes persisted five times (R1-R5) in this harness.

---

## 6. KNOWN MATERIAL GAPS

| id | Gap | Condition(s) | Class | Status |
|---|---|---|---|---|
| G1 | Implementation-class continuation | 4, 5 | CAMPAIGN_RELEVANT | **CLOSED (R4)**, limitation: small test-only change |
| G2 | Development-direction representation | 6 | CAMPAIGN_RELEVANT | LARGELY CLOSED; limitation: one campaign, one repository |
| G3 | Role of hooks undefined; hook doc stale | 8, 11 | CAMPAIGN_RELEVANT | **CLOSED (R5)** |
| G4 | Per-workflow disposition in campaign vocabulary not recorded | 9 | CAMPAIGN_RELEVANT | OPEN -> R6 |
| G5 | Deterministic-script role not consolidated | 7 | CAMPAIGN_RELEVANT | **CLOSED (R5)** |
| G6 | Semantic-control-map rows stale | 11 | CAMPAIGN_RELEVANT | **CLOSED** (R2 + close-out) |
| G7 | Authority grants unsourced | 5, 13 | CAMPAIGN_RELEVANT | **CLOSED** (R1 close-out) |
| G8 | GitHub-only evidence | 5, 13 | DEFERRED | documented limitation |
| G9 | Operating map did not represent continuation | 4, 6, 11 | CAMPAIGN_BLOCKING | **CLOSED (R3)** |
| G10 | Record task specs carry assumptions that fresh contexts must correct from evidence (7 instances) | 5 | CAMPAIGN_RELEVANT | mitigated by C9; none caused a wrong action; this is the pattern working, not failing |
| G11 | Two `active` workflows (`product-discovery-sprint`, `product-strategy-sprint`) consist entirely of `external_routing` steps to Skills the skill registry marks `deprecated` (no implementation). ADR 0027's compatibility-only set was scoped to `local_execution` dependencies, so it is internally consistent, but the liveness overlay still declares these two selectable | 9 | CAMPAIGN_RELEVANT | OPEN -> R6 (disposition + implied owner decision; no overlay edit) |

---

## 7. ACTIVE CONSTRAINTS

- C1 **Bootstrap constraint** (`CHARTER.md`).
- C2 **Authority** (section 11): dispatcher pushes/opens PRs; fresh contexts commit locally; merge to `main`, ADR/contract/registry/liveness ratification, and external tracker writes are **owner** actions. Never falsify owner decisions or ADR `**Status**` lines.
- C3 **Semantic-control-map trial is OPEN**: no new rows; MECH refresh on triggers; log events.
- C4 **Goal A is halted**; no episodes; #218 episodes only from ordinary work with owner-authorized tracker writes.
- C5 **Windows cp1252**: ASCII console; explicit encodings; pytest under both code pages when encoding could matter.
- C6 **Worktree per session**: `H:/GithubRepositories/smk-campaign`.
- C7 **Machinery promotion rule** (operating map section 7).
- C8 **One responsibility at a time**.
- C9 **Task specs: verification steps, per-branch expected outcomes; fresh contexts prefer repository evidence over this record and flag conflicts.** Corollary from R5: spec every "existing behavior" claim as something to verify (retry policy, install paths, phrase locations were all assumptions).
- C10 **Don't touch unrelated code** (`AGENTS.md` rule 4).
- C11 **Local qualification uses the worktree's own package** (`PYTHONPATH=src`) and a like-for-like clean-`main` baseline.

---

## 8. OPEN DECISION-CHANGING UNCERTAINTIES

| id | Uncertainty | Status |
|---|---|---|
| U1 | What continuation state does a fresh context fail to reconstruct? | **RESOLVED (R1)** |
| U2 | Outer vs inner loop state | **RESOLVED for this campaign's scale (R2-R5)**: one record carries both; the numbered step spec is the inner-loop state |
| U3 | Is any hook warranted? | **RESOLVED (R5)**: no continuation/liveness hook at this scale; admissible future shape and reopen condition on the product surface |
| U4 | Which registered workflows have enough real traces for a disposition other than `INSUFFICIENT_EVIDENCE`? | EVIDENCE GATHERED (starting inventory in section 10) -> R6 |
| U5 | Continuation artifact form | **DECIDED FOR NOW**: Markdown record convention |
| U6 | Can a fresh context perform a bounded task from this record? | **RESOLVED (R2)**, extended R3-R5 |
| U7 | Implementation-class continuation | **RESOLVED (R4)** for a small test-only change |
| U8 | Disposition of `tests/test_validate_brief_json.py` (D2b) | OPEN; DEFERRED (fixture/validator semantics) |
| U9 | Are the two all-deprecated `external_routing` sprints (G11) `RETIRE_CANDIDATE` or `HISTORICAL`, and should the liveness overlay change? | OPEN -> R6 records the disposition and the implied owner decision; overlay change is owner-ratified (ADR 0027) |

---

## 9. CURRENT HIGHEST-LEVERAGE CAPABILITY BOUNDARY

**Condition 9: a clear disposition of the old workflow system** (G4, G11, U4,
U9). Conditions 1-8 are met on the product surface (with stated limitations).
After R6: R7 = full like-for-like qualification of the campaign branch, CI,
PR readiness, final report (conditions 10-13).

---

## 10. CURRENT / NEXT WARRANTED RESPONSIBILITY

```text
R6  Workflow-system disposition
    (documentation; performed by a fresh context from this record)

CAMPAIGN CAPABILITY AFFECTED:   condition 9 (old workflow system has a clear
                                disposition: retained bounded roles, migration
                                path, or explicit reason for remaining
                                unresolved); condition 11
CURRENT LIMITATION:             ADR 0027 settles registry identity vs liveness and
                                names eight compatibility-only workflows; nothing
                                records, per registered workflow, whether it is a
                                kept bounded subgraph, repair/demote/retire
                                candidate, historical, or evidence-insufficient,
                                with the execution evidence behind that call
WHY IT MATTERS TO THE MISSION:  CHARTER.md "Workflow-System Policy": classify
                                workflows from real responsibility traces; prefer
                                recovering workflows from repeated successful
                                traces over prospective catalogs; do not delete or
                                expand the system merely because the campaign
                                uses a different control model
BOUNDED RESPONSIBILITY:         steps for the fresh context:
  1. read this file (sections 2, 6 G4/G11, 8 U4/U9, 10 incl. the starting
     inventory below); CHARTER.md "Candidate Architecture" item 7 and
     "Workflow-System Policy During This Campaign"; docs/adr/0027 (full);
     artifacts/workflow_executability_consumer_analysis.md sections 2, 4, 8, 9;
     skills/workflow-planner/references/workflow-registry.yaml,
     workflow-liveness.yaml, skill-registry.yaml (status/status_note fields);
     docs/mode-coverage.yaml; artifacts/0[1-4]-orchestration-run/run-ledger.jsonl
     (workflow_id fields); experiments/evidence/0018..0023 EVIDENCE.md (which
     workflow, if any, each exercised); artifacts/reconciliation_report.md
     (header); docs/agent-native-operating-workflow.md section 1 and Reality
     map; docs/2026-08-programmatic-runner-retirement-plan.md "Responsibility
     classification".
  2. VERIFY: rebuild the per-workflow inventory yourself from those sources --
     liveness; each step's step_type, skill id, and the skill's registry
     status; and every execution-evidence pointer (a run ledger line, a
     mode-coverage entry, an evidence record, or an agent-native artifact) --
     then diff it against the starting inventory below and list every
     discrepancy in the report. The starting inventory is a claim, not a fact.
  3. write docs/workflow-system-disposition.md (new file; ASCII; dated
     2026-09-02) with: (a) a status block: non-authoritative; ADR 0027 and
     workflow-liveness.yaml remain the operative liveness authority; this
     document classifies in campaign vocabulary and records evidence; it
     changes no registry, overlay, contract, or Skill; any liveness change is
     an owner decision; (b) definitions: registered / active (liveness) /
     step_type local_execution vs external_routing / skill status / execution
     evidence classes; (c) the disposition criteria, stated BEFORE the table:
     KEEP_AS_BOUNDED_SUBGRAPH = active + every step's Skill is implemented +
     at least one real execution record (ledger, evidence record, or
     agent-native artifact) + the sequence has recurred or is the ratified
     product spine; INSUFFICIENT_EVIDENCE = active + implemented Skills + no
     real execution record (plan_only or test-only traces do not count);
     HISTORICAL = compatibility_only per ADR 0027 (do not re-decide);
     RETIRE_CANDIDATE = active but every step routes to a deprecated/
     unimplemented Skill; REPAIR = active, evidenced, with a specific defect
     you can cite; DEMOTE = active with evidence that its role is narrower
     than the registry implies (cite). Apply the charter's investment rule
     (recurring sequence + stable ordering + low semantic ambiguity +
     measurable benefit) only to justify KEEP; (d) the 23-row table: id |
     liveness | step skills (status) | execution evidence (pointers) |
     disposition | rationale; (e) "Migration path / retained roles": which
     KEEP workflows are bounded subgraphs inside the agent-owned loop and how
     they are entered (cite operating map section 1); (f) "Implied owner
     decisions, not applied": e.g. adding the RETIRE_CANDIDATE workflows to the
     compatibility-only overlay; what to do with the product-management
     ecosystem; (g) "What this document does not do": ADR 0027 "Explicit
     non-decisions" list, restated; (h) "Evidence limits": what could not be
     established (e.g. agent-native executions with no ledger).
  4. edit docs/agent-native-operating-workflow.md section 1 only: after the
     sentence that names registered workflows as potential subgraphs, add one
     sentence pointing at docs/workflow-system-disposition.md. No other change.
  5. validate: `python scripts/validate-repo.py` (exit 0); `PYTHONUTF8=1
     PYTHONPATH=src python -m pytest tests/test_path_drift.py -q` (green);
     every markdown link you added resolves relative to its file; the new file
     is ASCII and LF; no non-ASCII added to the operating map.
  6. `git diff --stat` -> exactly 2 files; commit on
     campaign/agent-native-self-development with subject prefix `campaign(R6):`
     and trailer `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`;
     do NOT push; do NOT edit CAMPAIGN-STATE.md.
  7. write docs/campaigns/agent-native-self-development/R6-workflow-system-disposition.md
     (second `campaign(R6):` commit): inventory discrepancies found in step 2;
     per-disposition counts; what this record was sufficient for; what was
     missing/wrong (flag, do not silently fix); files consulted beyond the
     record; tool-call count; authority questions; anything skipped.
AUTHORITY FOR R6 (sourced):     CHARTER.md ("workflow demotion/repair/retirement"
                                is a listed bounded responsibility, but here as
                                classification + evidence only; "Workflow-System
                                Policy During This Campaign"); ADR 0027 (liveness
                                authority; its "Explicit non-decisions" bound
                                what this document may claim); operating map
                                section 7 revision trigger (one pointer sentence).
NOT AUTHORIZED IN R6:           editing workflow-registry.yaml, workflow-
                                liveness.yaml (either copy), skill-registry.yaml,
                                contracts, ADRs, scripts, src/, tests/, Skills,
                                CONTEXT.md, any other doc; deleting or reviving
                                any workflow or Skill; pushing; merging; tracker
                                writes; editing CAMPAIGN-STATE.md.
STOP CONDITION:                 both commits exist and the report is written; OR
                                the step-2 rebuild shows the starting inventory is
                                unusable -> still write the document from your own
                                verified inventory and flag the discrepancies; OR
                                a required source file is missing -> report and
                                stop.
EXPECTED EVIDENCE OF PROGRESS:  commits `campaign(R6): ...`; the R6 report;
                                dispatcher audit incl. exact-head CI; G4 and G11
                                closed (G11 as a recorded disposition + implied
                                owner decision, not an overlay edit); U4 and U9
                                resolved; condition 9 MET.
```

**R6 starting inventory (dispatcher-computed 2026-09-02; claims to verify).**
Columns: liveness; `ldg` = count of ledger/run-record files under
`artifacts/` + `experiments/` naming the id as `workflow_id`; `mc` = mentions in
`docs/mode-coverage.yaml`; `ev` = evidence files under `experiments/evidence/`
mentioning the id; `tests` = test files mentioning the id; step skills with
skill-registry status (`ok` = implemented; `proposed`/`deprecated` per registry;
`?` = not resolved by the dispatcher's script). Step types: all
`local_execution` except `product-discovery-sprint` and `product-strategy-sprint`
(`external_routing`).

| workflow | liveness | ldg | mc | ev | tests | step skills (status) |
|---|---|---|---|---|---|---|
| fast-path-workflow | active | 5 | 1 | 6 | 7 | repo-sensemaker(ok), workflow-planner(ok) |
| full-fog-workflow | active | 2 | 3 | 10 | 6 | problem-framer(ok), unknowns-mapper(ok), repo-sensemaker(ok), workflow-planner(ok) |
| setup-sensemaking-repo | active | 0 | 3 | 1 | 2 | setup-sensemaking-skills(?), repo-sensemaker(ok), handoff(ok) |
| docs-contract-reconciliation | active | 8 | 5 | 13 | 18 | repo-sensemaker(ok), sensemaking-docs-reconciler(ok), repair-verifier(ok), handoff(ok) |
| artifact-reconciliation | active | 0 | 0 | 1 | 0 | repo-sensemaker(ok), output-reconciler(ok), to-issues(ok), handoff(ok); agent-native execution evidence: `artifacts/reconciliation_report.md` (2026-08-22), evidence 0020 |
| autonomous-sprint-preflight | active | 0 | 3 | 1 | 1 | repo-sensemaker(ok), handoff(ok) |
| docs-architecture | active | 1 | 4 | 6 | 1 | docs-aligner(ok), handoff(ok) |
| product-to-issues | compatibility_only | 0 | 1 | 1 | 2 | to-prd(ok), to-issues(ok), triage(proposed) |
| product-discovery-sprint | active | 0 | 5 | 1 | 2 | persona, discovery, interview-synthesis, opportunity-tree, hypothesis (all deprecated; external_routing) |
| product-strategy-sprint | active | 0 | 2 | 1 | 2 | lean-canvas, north-star, okr, roadmap, stakeholder-update (all deprecated; external_routing) |
| product-autonomous-sprint | compatibility_only | 0 | 3 | 1 | 2 | persona, discovery, opportunity-tree, hypothesis, prd, user-stories, acceptance-criteria (deprecated), handoff(ok) |
| full-local-sensemaking | active | 6 | 14 | 12 | 15 | problem-framer(ok), unknowns-mapper(ok), step 3 conditional(?), repo-sensemaker(ok), workflow-planner(ok), handoff(ok) |
| fast-local-diagnostic | active | 4 | 26 | 4 | 7 | repo-sensemaker(ok), handoff(ok) |
| experimental-autonomous-sprint | compatibility_only | 0 | 3 | 4 | 2 | docs-aligner(ok), to-prd(ok), to-issues(ok), triage(proposed), tdd(deprecated), handoff(ok) |
| skill-maintenance-loop | active | 5 | 10 | 6 | 1 | skill-maintainer(ok), handoff(ok) |
| implementation-workflow | compatibility_only | 4 | 1 | 20 | 31 | docs-aligner(ok), to-prd(ok), to-issues(ok), triage(proposed), tdd(deprecated), handoff(ok) |
| product-implementation-workflow | compatibility_only | 7 | 0 | 2 | 17 | docs-aligner(ok), discovery(deprecated), opportunity-tree(deprecated), to-prd(ok), to-issues(ok), triage(proposed), tdd(deprecated), handoff(ok) |
| ui-diagnostic-workflow | compatibility_only | 4 | 0 | 2 | 3 | docs-aligner(ok), ui-brief(deprecated) |
| ui-implementation-workflow | compatibility_only | 8 | 0 | 4 | 8 | docs-aligner(ok), ui-flow(deprecated), ui-screen-spec(deprecated), to-issues(ok), triage(proposed), tdd(deprecated), handoff(ok) |
| docs-implementation-workflow | active | 8 | 0 | 3 | 8 | docs-aligner(ok), to-prd(ok), handoff(ok) |
| architecture-implementation-workflow | compatibility_only | 38 | 0 | 6 | 12 | docs-aligner(ok), to-prd(ok), to-issues(ok), triage(proposed), tdd(deprecated), handoff(ok) |
| skill-evaluation-workflow | active | 1 | 0 | 1 | 0 | usage-researcher(ok), skill-maintainer(ok), handoff(ok) |
| architectural-review-planning-workflow | active | 6 | 3 | 54 | 5 | repo-sensemaker(ok), architectural-review(ok) |

Known caveats the dispatcher could not resolve: `ldg` counts name-mentions in
run records, not necessarily completed executions (many `workflow_id` hits
under `experiments/` are plan or fixture files); `mc` counts mentions
including historical `orchestration-runner.py` runs; `setup-sensemaking-skills`
status was not resolved by the dispatcher's script (the Skill directory exists
under `skills/`); `full-local-sensemaking` step 3 is a conditional step whose
target the script did not resolve. The executability analysis's recommended
decision (its section 9, option 2) was subsequently ratified as ADR 0027.

---

## 11. AUTHORITY: GRANTS, THEIR SOURCES, AND OWNER DECISIONS REQUIRED

| Grant / boundary | Source |
|---|---|
| Own the campaign end to end on the campaign branch | `CHARTER.md` "Campaign Mission" |
| Use ordinary engineering infrastructure | `CHARTER.md` "Important Bootstrap Constraint" |
| Push branches / open PRs; qualify exact PR heads (dispatcher only) | `CHARTER.md` "Git and Change Discipline" |
| Branch-local reversible, non-ratified changes are agent-decidable; ratification is not | `CONTEXT.md` "Authority model"; `CHARTER.md` "Architecture Discipline" |
| Bounded implementation / test-harness improvement of named files | `CHARTER.md`; `AGENTS.md` rules 3-4 |
| Documentation / architecture reconciliation surfaced for owner review | operating map section 7; boundary doc header; `CHARTER.md` |
| Workflow classification + evidence (not registry/overlay edits) | `CHARTER.md` "Workflow-System Policy"; ADR 0027 non-decisions |
| MECH refresh of semantic-control-map rows; trial-log entries | `docs/semantic-control-map-trial.md` |
| Merge to `main` = owner; liveness overlay / ADR / contract changes = owner | ADR 0014/0026/0027 headers; `docs/adr/README.md`; `CONTEXT.md` |
| ADR status / owner decisions must not be falsified | `docs/adr/README.md`; `AGENTS.md` rule 5 |
| External tracker writes require explicit authority | operating map section 4 (ADR 0019 PROPOSED) |
| Ask the owner only for product preference, authority expansion, irreversible tradeoffs, external environment, material product-direction acceptance | `CHARTER.md` "Owner Decisions" |

Owner decisions required (none blocking the next responsibility):

1. **Merge authority for the campaign PR (#268)** -- standing.
2. **Whether to record the R1-R5 substrate observation on Issue #255.**
3. **(after R6) Liveness-overlay changes implied by the workflow disposition**
   (e.g. `product-discovery-sprint`, `product-strategy-sprint` ->
   `compatibility_only`) -- ADR 0027 makes the overlay owner-ratified.

---

## 12. DEFERRED NON-CAMPAIGN FINDINGS

| id | Finding | Class | Disposition |
|---|---|---|---|
| D1 | `test_path_drift.py` encoding | LOCAL_BUT_REAL | **CLOSED (R4)** |
| D2 | (a) stale root import -- **CLOSED (R4)**; (b) `test_validate_brief_json.py` fixture/expectation drift vs current validator | LOCAL_BUT_REAL | (b) DEFERRED -> U8 |
| D3 | `roadmap.md` stale | HISTORICAL_ONLY | no action |
| D4 | `docs/HARDENING_STATUS.md` 5-type fog taxonomy | HISTORICAL_ONLY | no action |
| D5 | dangling link in `docs/candidate/architecture-decision.md` | HISTORICAL_ONLY | no action |
| D6 | `unevaluable` verdict category not in contract | DEFERRED | needs a real case |
| D7 | normal-use lane "0 episodes" is a dated snapshot | NO_ACTION_WARRANTED | none |
| D8 | `validation.yml` line 14 comment stale | LOCAL_BUT_REAL | deferred (fires trial triggers) |
| D9 | Map row SE10 vs current probe output | INSUFFICIENT_EVIDENCE | leave |
| D10 | Trial protocol step-4 selector | LOCAL_BUT_REAL | **fixed at R2 close-out** |
| D11 | Two tests `rglob` the repo root; pathological on the shared checkout | LOCAL_BUT_REAL (environment) | deferred; C11 |
| D12 | `validate-mode-coverage.py` subprocess cannot import `workflow_liveness` via `_validator_utils.py` (one test fails on `main`) | LOCAL_BUT_REAL | deferred; candidate for a future implementation-class continuation |
| D13 | U+2713 prints in `test_integration_external_repo.py`; `config.py:133` opens YAML without encoding | LOCAL_BUT_REAL, low | deferred |
| D14 | Local Windows/Python 3.14 baseline: 54 failed / 2 errors with `PYTHONPATH=src` (34/15 without); Linux CI green | LOCAL_BUT_REAL (environment) | like-for-like diff only (C11) |
| D15 | Boundary doc's "Execution and orchestration layer" gives "retry" as an example of an established execution-control policy; `workflow-runtime.py` implements none (R5 F3). Now stated in the new section; the example paragraph itself was left as-is (it says "may", not "does") | NO_ACTION_WARRANTED | none |
| D16 | `docs/task-1-2-sessionstart-hook-testing.md` still describes the hook as "created and registered" | HISTORICAL_ONLY (dated task doc) | no action |

---

## 13. CAMPAIGN ACCEPTANCE STATUS

| # | Condition | Status after R5 | Basis |
|---|---|---|---|
| 1 | Top-level semantic control model explicit and coherent | MET | CONTEXT.md, boundary doc (+R5 section), ADR 0013 |
| 2 | Role of active coding agent clear | MET | ADR 0013 + amendment |
| 3 | Warrant / responsibility / capability / authority not conflated | MET | ADR 0026/0027; every fresh context respected every boundary (R2-R5) |
| 4 | Durable artifacts carry continuation state across responsibilities | MET (mechanical, judgment-docs, implementation-class, multi-file architecture docs) | R1-R5; operating map |
| 5 | One realistic multi-responsibility task continued from durable state | MET: R0 -> R5 across six contexts with this record as the only shared state; limitation: small surfaces, single dispatcher | R1-R5 reports |
| 6 | Development direction representable for consequential capability selection | LARGELY MET; limitation: one campaign, one repository | this record; operating map |
| 7 | Role of deterministic scripts bounded and coherent | **MET (R5)** on the product surface, with evidence | boundary doc section; Reality-map row |
| 8 | Role of hooks defined and evidence-supported | **MET (R5)**: none executable; none warranted; admissible shape + reopen condition; hook doc and CLAUDE.md truthful | boundary doc "Hooks"; Reality-map row; `.claude/hooks/sessionstart.md`; `CLAUDE.md` |
| 9 | Old workflow system has a clear disposition | PARTIAL | ADR 0027; G4/G11 -> R6 |
| 10 | Existing useful functionality not destroyed | MET so far (`validate-repo.py` green; CI green on every pushed head: `b4335c3`, `2adfeaf`, `09bdf5e`, `ac47191`, `e35ead1`) | section 15 |
| 11 | Tests, validators, contracts, docs, implementation agree sufficiently | LARGELY MET; residual: D2(b)/U8, D8, D12 (all pre-existing, not in CI) | section 12 |
| 12 | Repository passes appropriate complete qualification | PARTIAL: CI green on every pushed head; R5 head not yet pushed; full-suite like-for-like pending (R7) | section 15; C11 |
| 13 | Remaining material limitations explicitly documented | IN PROGRESS | this file; final report at R7 |

Disposition after R5: **CONTINUE** (R6).

---

## 14. Responsibility trace (append-only)

```text
2026-09-02  R0  reconstruction + campaign record v1                     -> next: R1
2026-09-02  R1  fresh-context reconstruction probe; record v2           -> next: R2
2026-09-02  R2  fresh-context mechanical trial; caught record error F1  -> audit
2026-09-02  R2  close-out: VERIFIED; record v3                          -> next: R3
2026-09-02  R3  fresh-context judgment-docs trial (operating map)       -> audit
2026-09-02  R3  close-out: VERIFIED; record v4                          -> next: R4
2026-09-02  R4  fresh-context implementation-class trial (D1/D2)        -> audit
2026-09-02  R4  close-out: VERIFIED; C9/C11; record v5                  -> next: R5
2026-09-02  R5  fresh-context 4-file architecture reconciliation
                (machinery + hooks disposition); 3 spec assumptions
                corrected from code                                     -> audit
2026-09-02  R5  close-out: VERIFIED; record v6; R6 specified            -> next: R6
```

---

## 15. Remote / integration status (updated by the dispatcher, never assumed)

```text
pushed:        e35ead1 (R4 close-out) -> origin/campaign/agent-native-self-development
               R5 commits 13d1a09, c7afb57 + this close-out: pushed after this commit
PR:            #268 (draft) https://github.com/ThorStarlord/sensemaking-skills/pull/268
last main CI:  Validator Ecosystem completed/success @ f10b7da (2026-09-02T03:43Z)
campaign CI:   b4335c3, 2adfeaf, 09bdf5e, ac47191, e35ead1: all completed/success
merged:        nothing (owner decision)
```
