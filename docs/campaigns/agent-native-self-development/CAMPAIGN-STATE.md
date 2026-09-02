# Campaign: reliable agent-native, artifact-mediated self-development

```
STATUS:    CLOSING (v10: R8a done; R8b closure probe pending). Disposition in section 16.
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
           F1/F2; R5 F1-F3; R6 discrepancies 1-9; R7 F1-F5).
```

This file exists so that campaign reasoning does not live only in one
conversation's context. Seven fresh contexts have so far continued the campaign
from this file alone: R1 (reconstruction), R2 (mechanical execution), R3
(judgment-class documentation), R4 (implementation-class code + tests), R5
(four-file architecture reconciliation), R6 (evidence-gathering + classification
producing a new product document), R7 (product machinery + regression test). See
section 8.

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
| Top-level semantic control model | **EXPLICIT in docs**; agent owns loop; decision vs orchestration separated; warrant vocabulary defined | `CONTEXT.md`; `docs/decision-orchestration-boundary.md`; `docs/agent-native-operating-workflow.md`; ADR 0013 |
| Product boundary | Human-reviewed `repository_sensemaking_brief` is the ratified external scope; routing deferred | ADR 0014 |
| Warrant / recommendation / selection / execution authority | **Separated and ratified**; consumers fail closed | ADR 0026; ADR 0027; ADR 0018 SUPERSEDED |
| Workflow registry vs liveness | Identity and liveness separated; 8 of 23 `compatibility_only` | ADR 0027; `workflow-liveness.yaml` |
| **Workflow-system disposition** | **On the product surface since R6**: `docs/workflow-system-disposition.md` classifies all 23 registered workflows in campaign vocabulary with pinned evidence: KEEP_AS_BOUNDED_SUBGRAPH 1 (`docs-contract-reconciliation`), DEMOTE 2 (`artifact-reconciliation` -> evidenced two-step core; `architectural-review-planning-workflow` -> internal golden-path proof, ADR 0014 defers step 2), RETIRE_CANDIDATE 2 (`product-discovery-sprint`, `product-strategy-sprint`: every step `external_routing` to a deprecated Skill), HISTORICAL 8 (ADR 0027 set, not re-decided), INSUFFICIENT_EVIDENCE 10, REPAIR 0. Every ledger with step events was produced by the SDK executor removed 2026-08-13; the only workflow with a recurring agent-native trace of its full sequence is `docs-contract-reconciliation`. Nine implied owner decisions listed, none applied. Pointer added in operating map section 1 | commit `70648c4`; `R6-workflow-system-disposition.md` |
| Responsibility selection | **CONVENTION**; exercised by fresh contexts (R1 Q3; R4; R5; R6 dispositions) | operating map Reality map |
| Continuation across responsibilities | **On the product surface since R3**; demonstrated for mechanical (R2), judgment-docs (R3), implementation-class tests (R4), four-file architecture reconciliation (R5), evidence-gathering + classification (R6), **product machinery + regression test (R7)** | operating map section 2 subsection; `R1-*.md` .. `R7-*.md` |
| Continuation artifacts / U5 decision | Markdown record convention; no new artifact type; reopen conditions on the product surface | operating map section 6 bullet |
| Repository-level development-direction representation | This record; field set documented in the operating map | this file |
| Deterministic machinery | **Consolidated on the product surface since R5** (boundary doc section; Reality-map row); no retry policy exists in `workflow-runtime.py`. **Repaired by R7 (D12):** `scripts/_validator_utils.py` no longer hard-imports `workflow_liveness` at module load; a lazy resolver tries `sys.path`, then the sibling file, else raises a clear ImportError only when a liveness helper is called; public API unchanged; `validate-repo.py` exit 0 and `test-validators.py` 78/78 before and after; `validate-plan.py` still fails closed | commits `13d1a09`, `79e02c5` |
| Hooks | **Disposition on the product surface since R5**: none executable; none warranted; admissible future shape mechanical only; hook doc and CLAUDE.md truthful | commit `13d1a09` |
| CI on `main` | 13 jobs incl. `probe-gate` and `core-assertions`; green at `df46871` and `f10b7da` | `validation.yml`; `gh run list` |
| Real-use evidence of the operating loop | Workflow v0 dogfood on 2 repos; 3 normal-use episodes on Issue #218 (GitHub-only) | evidence 0021/0022; Issue #218 |
| Research lanes (non-ratified) | C6R (#226); semantic-control-map trial OPEN (min close 2026-09-28) with first real events from this campaign | `docs/research/control-model-research-agenda.md`; trial log |
| Goal A external validation | ACTIVE but halted in this environment | Issue #255; evidence 0023 |
| Repository visibility | public | `gh repo view` |

**Local qualification procedure (C11).** `PYTHONPATH=src python -m pytest
tests -q -p no:cacheprovider --ignore=tests/integration
--continue-on-collection-errors` in a clean worktree, compared like-for-like
against the same command on a clean `main @ f10b7da` worktree. Baseline
(Windows, Python 3.14): **2712 passed / 54 failed / 2 errors / 16 skipped /
5 xfailed** (failure set persisted by the dispatcher, 41 unique entries).
Linux CI is the referee for cross-platform claims. Candidate runs: `5a89f2a`
(after R6) 2718 / 53 / 1, 0 NEW, 2 FIXED; **`1b47d06` (after R7) 2723 passed /
51 failed / 1 error, 0 NEW, 4 FIXED** (D1; D2a; both mode-coverage tests).

---

## 3. COMPLETED CAMPAIGN RESPONSIBILITIES

| # | Responsibility | Result | Evidence |
|---|---|---|---|
| R0 | Reconstruct state; establish durable campaign record | this file v1 | `2bc8a2c` |
| R1 | Fresh-context reconstruction probe | Q1-Q5 `RECONSTRUCTED`; Q6 `PARTIAL`; Q7 five omissions; repairs at close-out | `R1-*.md`; `b4335c3` |
| R2 | Fresh-context mechanical trial (semantic-control-map bookkeeping) | exact diff; caught record error F1; **VERIFIED** | `R2-*.md`; `fa2dd68`, `9160a5b`; `2adfeaf` |
| R3 | Fresh-context judgment-docs trial (continuation pattern into the operating map) | +88/-3 one file; two record overstatements flagged; **VERIFIED** | `R3-*.md`; `6ff4a89`, `fbbb637`; `09bdf5e` |
| R4 | Fresh-context implementation-class trial (D1/D2) | repair / repair / revert-and-report; spec tension F1 flagged; **VERIFIED**; CI green | `R4-*.md`; `769a180`, `ac47191`; `e35ead1` |
| R5 | Fresh-context four-file architecture reconciliation (machinery + hooks) | +213/-83; three spec assumptions corrected from code; **VERIFIED** | `R5-*.md`; `13d1a09`, `c7afb57`; `89246f4` |
| R6 | Fresh-context workflow-system disposition: rebuilt the inventory from sources, classified 23 workflows with pinned evidence, wrote `docs/workflow-system-disposition.md` (+410) and one pointer sentence | 1 KEEP / 2 DEMOTE / 2 RETIRE_CANDIDATE / 8 HISTORICAL / 10 INSUFFICIENT_EVIDENCE / 0 REPAIR; nine discrepancies vs the dispatcher's starting inventory (substring inflation in `ev`/`tests`; `ldg` dominated by `recommended_workflow_id` mentions; wrong date for `artifacts/reconciliation_report.md` (2026-09-01, not 08-22); `full-local-sensemaking` step 3 routes to deprecated `discovery` via `external_routing`; `setup-sensemaking-skills` has no skill-registry entry; packaged catalog carries 20 of 23 ids and 7 of 8 overrides; mode-coverage's two pointed entries overstate `steps_completed`); no overlay/registry edit; 50 files / 60 calls. **Dispatcher audit: VERIFIED** (status block, definitions, criteria, all 23 rows, sections 5-8 read; the two DEMOTE calls carry their alternatives; `validate-repo.py` exit 0; `test_path_drift` green; pointer sentence exact) | `R6-workflow-system-disposition.md`; `70648c4`, `5a89f2a` |
| R6 close-out (dispatcher) | Audit; record v7; closure specified, then deferred one responsibility (record v8: R7 = D12) | `eb6c461`, `e702b31` | section 14 |
| R7 | Fresh-context **product-machinery** continuation: verified D12 against code and tests (hard import arrived in `4b42263`, 2026-09-01), replaced it with a lazy resolver in `scripts/_validator_utils.py` (+33/-4), added `tests/test_validator_utils_liveness_import.py` (three fresh-interpreter tests, ASCII/LF, encoding-safe) | Both `test_mode_coverage_aggregation.py` failures flip green; `test_validator_utils.py` collects again but `test_load_workflow_registry_loads_yaml` stays red for a **second, independent** cause the record did not know (expected dict predates ADR 0027's `liveness` annotation) -- editing existing tests was not authorized, so it flagged (F2) instead of forcing; `validate-repo.py` exit 0 and `test-validators.py` 78/78 before and after (output byte-identical except a timestamp); direct execution resolves the same `workflow_liveness` module object; `validate-plan.py` still rejects compatibility-only selections; results identical under cp1252 and utf-8. Judgment call recorded: proceeded rather than stopping under stop-condition 2 because the defect reproduction matched exactly and only pytest's reporting shape / the after-state prediction differed. 21 files / 46 calls. **Dispatcher audit: VERIFIED** (diff read in full; named selections re-run under both code pages: 1 failed / 45 passed / 1 skipped, the one being D19; `validate-repo.py` and `test-validators.py` re-run; stray egg-info modifications confirmed generated by test runs and discarded, not committed) | `R7-machinery-continuation.md`; `79e02c5`, `1b47d06` |
| R7 close-out (dispatcher) | Audit; record v9; R8 (closure) specified | this commit | section 14 |

---

## 4. EVIDENCE PRODUCED

- `docs/campaigns/agent-native-self-development/`: `CAMPAIGN-STATE.md`, `CHARTER.md`, `R1-*.md` .. `R6-*.md` (reports verbatim from the fresh contexts).
- Product-side changes: `docs/agent-native-operating-workflow.md` (R3 subsection + rows; R5 two rows; R6 pointer); `docs/decision-orchestration-boundary.md` (R5 section); `docs/workflow-system-disposition.md` (R6, new); `.claude/hooks/sessionstart.md` (R5); `CLAUDE.md` SessionStart section (R5); `docs/semantic-control-map.md`, `-trial-log.md`, `-trial.md`, `docs/enforcement-contract.md` (R2 + close-out); `tests/test_path_drift.py`, `tests/test_integration_external_repo.py` (R4); `scripts/_validator_utils.py`, `tests/test_validator_utils_liveness_import.py` (R7).
- `docs/campaigns/agent-native-self-development/R7-machinery-continuation.md` (verbatim).

---

## 5. CURRENTLY DEMONSTRATED CAPABILITIES

- Pre-campaign: agent-native brief production + validation on two repositories; responsibility selection without routing; claim reconciliation and repair verification; fail-closed authority on auto-invoke and liveness; probe-engine enforcement in CI.
- **(R1-R6)** Six consecutive record-mediated continuations into fresh contexts across five responsibility classes (reconstruction; mechanical; judgment-docs; implementation-class code + tests; multi-file architecture reconciliation; evidence-gathering + classification). Each fresh context respected every stated authority boundary, verified before acting, wrote narrower than the spec where evidence said less, and corrected the record from repository evidence where it was wrong.
- **(R7)** A fresh context changed the product's own deterministic machinery from the record alone: verified the defect against code and git, applied the simplest repair that preserved every public signature and ADR 0027's fail-closed liveness behavior, added fresh-interpreter regression tests, proved like-for-like equivalence of the validator harness, and refused to edit an existing test to make the record's predicted outcome come true.
- **(count basis)** Eight record-mediated handoffs (R0 -> R1 -> ... -> R7, each returning for audit); seven into fresh contexts; zero shape errors in the record; twenty-one record errors/overstatements caught by verification steps (R2: 1; R3: 2; R4: 2; R5: 3; R6: 9; R7: 5 incl. a wrong after-state prediction) -- none caused a wrong action; the ones that mattered were method errors in dispatcher-computed evidence, which the fresh contexts' verify-before-use steps caught.
- **(substrate)** Isolated sub-agent direct worktree writes persisted seven times (R1-R7) in this harness.

---

## 6. KNOWN MATERIAL GAPS

| id | Gap | Condition(s) | Class | Status |
|---|---|---|---|---|
| G1 | Implementation-class continuation | 4, 5 | CAMPAIGN_RELEVANT | **CLOSED (R4)**, limitation: small test-only change |
| G2 | Development-direction representation | 6 | CAMPAIGN_RELEVANT | LARGELY CLOSED; limitation: one campaign, one repository |
| G3 | Hooks | 8, 11 | CAMPAIGN_RELEVANT | **CLOSED (R5)** |
| G4 | Per-workflow disposition | 9 | CAMPAIGN_RELEVANT | **CLOSED (R6)** |
| G5 | Deterministic-script role | 7 | CAMPAIGN_RELEVANT | **CLOSED (R5)** |
| G6 | Semantic-control-map rows stale | 11 | CAMPAIGN_RELEVANT | **CLOSED** (R2 + close-out) |
| G7 | Authority grants unsourced | 5, 13 | CAMPAIGN_RELEVANT | **CLOSED** (R1 close-out) |
| G8 | GitHub-only evidence | 5, 13 | DEFERRED | documented limitation |
| G9 | Operating map did not represent continuation | 4, 6, 11 | CAMPAIGN_BLOCKING | **CLOSED (R3)** |
| G10 | Dispatcher-computed claims in task specs need verification by the continuing context (16 instances caught) | 5 | CAMPAIGN_RELEVANT | mitigated by C9; this is the pattern working; residual risk: a wrong dispatcher claim that a spec does not ask to verify |
| G11 | Two `active` workflows route every step to a deprecated Skill | 9 | CAMPAIGN_RELEVANT | **CLOSED as a recorded disposition (R6: RETIRE_CANDIDATE)**; overlay change = owner decision 3 |
| G12 | Final qualification of the campaign branch and the final report | 12, 13 | CAMPAIGN_BLOCKING | **R8a DONE**: like-for-like suite 0 NEW / 4 FIXED; CI green through `4336a53`; `FINAL-REPORT.md` committed; R8b closure probe + PR ready pending |
| G13 | Code change from durable state was test-only (R4) | 5, 11 | CAMPAIGN_RELEVANT | **CLOSED (R7)**: `scripts/_validator_utils.py` repaired + regression tests; limitation: one script, no `src/` change |

---

## 7. ACTIVE CONSTRAINTS

- C1 **Bootstrap constraint** (`CHARTER.md`).
- C2 **Authority** (section 11): dispatcher pushes/opens PRs; fresh contexts commit locally; merge to `main`, ADR/contract/registry/liveness ratification, and external tracker writes are **owner** actions.
- C3 **Semantic-control-map trial is OPEN**: no new rows; MECH refresh on triggers; log events.
- C4 **Goal A is halted**; no episodes; #218 episodes only from ordinary work with owner-authorized tracker writes.
- C5 **Windows cp1252**: ASCII console; explicit encodings; both code pages when encoding could matter.
- C6 **Worktree per session**: `H:/GithubRepositories/smk-campaign`.
- C7 **Machinery promotion rule** (operating map section 7).
- C8 **One responsibility at a time**.
- C9 **Task specs: verification steps, per-branch expected outcomes, and every dispatcher-computed claim marked as a claim to rebuild**; fresh contexts prefer repository evidence over this record and flag conflicts.
- C10 **Don't touch unrelated code**.
- C11 **Local qualification uses the worktree's own package** (`PYTHONPATH=src`) and a like-for-like clean-`main` baseline.

---

## 8. OPEN DECISION-CHANGING UNCERTAINTIES

| id | Uncertainty | Status |
|---|---|---|
| U1 | What continuation state does a fresh context fail to reconstruct? | **RESOLVED (R1)** |
| U2 | Outer vs inner loop state | **RESOLVED for this campaign's scale (R2-R6)** |
| U3 | Is any hook warranted? | **RESOLVED (R5)**: no |
| U4 | Which workflows have enough real traces for a disposition? | **RESOLVED (R6)**: 1 KEEP, 2 DEMOTE, 2 RETIRE_CANDIDATE, 8 HISTORICAL, 10 INSUFFICIENT_EVIDENCE |
| U5 | Continuation artifact form | **DECIDED FOR NOW**: Markdown record convention |
| U6 | Can a fresh context perform a bounded task from this record? | **RESOLVED (R2)**, extended R3-R6 |
| U7 | Implementation-class continuation | **RESOLVED (R4, R7)**: test-only change (R4) and product-machinery change with regression tests (R7), both from the record alone; not shown: `src/` changes, larger surfaces |
| U8 | Disposition of `tests/test_validate_brief_json.py` (D2b) | OPEN; DEFERRED (fixture/validator semantics) |
| U9 | The two all-deprecated `external_routing` sprints | **RESOLVED (R6): RETIRE_CANDIDATE**; overlay change = owner decision |
| U10 | Does the final durable state suffice for a fresh context to reconstruct the campaign's disposition, what remains, and which decisions are the owner's? | OPEN -> R8 closure probe |

---

## 9. CURRENT HIGHEST-LEVERAGE CAPABILITY BOUNDARY

**Closure** (G12, U10). Conditions 1-11 are met or largely met on the product
surface with stated limitations; conditions 12-13 require the complete
like-for-like qualification of the final campaign head, CI on that head, PR
readiness, a final fresh-context closure probe (U10), and the final report.
No further product change is warranted by current evidence: every remaining
open item is either an owner decision (section 11), a deferred non-campaign
finding (section 12), or a documented limitation.

---

## 10. CURRENT / NEXT WARRANTED RESPONSIBILITY

```text
R8  Closure: qualification, final report, closure probe, PR ready

CAMPAIGN CAPABILITY AFFECTED:   conditions 10-13; U10
BOUNDED RESPONSIBILITY:
  R8a (dispatcher, first): run the C11 full suite on the R7 head and compare
      it with the comparison script against the clean-main baseline (expect
      0 NEW failures; FIXED = D1, D2(a), the two mode-coverage tests); confirm
      exact-head CI green on the pushed R7 head; write FINAL-REPORT.md in this
      directory in the CHARTER.md "Final Campaign Report" format with the
      final numbers; add section 16 (closure summary) to this file; commit
      `campaign(R8):`; push.
  R8b (fresh context, dispatched after R8a's commit): closure probe -- given
      only this file's path, answer: (1) what is the campaign's disposition
      and why, and does the repository evidence support it; (2) which
      acceptance conditions are met, with what limitation each; (3) what
      remains open and who owns each item (agent / owner / deferred); (4) what
      a successor context should do first if the owner merges PR #268, and if
      the owner does not; (5) anything FINAL-REPORT.md or this record claims
      that the repository contradicts. Verdicts RECONSTRUCTED | PARTIAL |
      FAILED per question with the reconstruction-failure classes; report
      cost. Write R8-closure-probe.md; commit `campaign(R8):` with the
      trailer; do NOT edit this record, FINAL-REPORT.md, or any product file;
      do not push. The dispatcher audits it, records the result in section 16,
      corrects FINAL-REPORT.md only for factual errors the probe proves, and
      marks PR #268 ready for review.
AUTHORITY FOR R8 (sourced):     CHARTER.md "Final Campaign Report", "Git and
                                Change Discipline" (qualified PR head), "Owner
                                Decisions"; marking the PR ready for review is a
                                signal to the owner, not a merge.
NOT AUTHORIZED IN R8:           merging; editing ADRs, contracts, registries,
                                overlays, scripts, src/, Skills, tests; tracker
                                writes beyond the PR itself; new product changes.
STOP CONDITION:                 FINAL-REPORT.md committed; CI green on the final
                                head; closure probe committed and audited; PR
                                ready for review; disposition in section 16.
```

---

## 11. AUTHORITY: GRANTS, THEIR SOURCES, AND OWNER DECISIONS REQUIRED

| Grant / boundary | Source |
|---|---|
| Own the campaign end to end on the campaign branch | `CHARTER.md` "Campaign Mission" |
| Use ordinary engineering infrastructure | `CHARTER.md` "Important Bootstrap Constraint" |
| Push branches / open PRs / mark ready for review; qualify exact PR heads (dispatcher only) | `CHARTER.md` "Git and Change Discipline" |
| Branch-local reversible, non-ratified changes are agent-decidable; ratification is not | `CONTEXT.md` "Authority model"; `CHARTER.md` "Architecture Discipline" |
| Bounded implementation / test-harness improvement of named files | `CHARTER.md`; `AGENTS.md` rules 3-4 |
| Documentation / architecture reconciliation surfaced for owner review | operating map section 7; boundary doc header; `CHARTER.md` |
| Workflow classification + evidence (not registry/overlay edits) | `CHARTER.md` "Workflow-System Policy"; ADR 0027 non-decisions |
| MECH refresh of semantic-control-map rows; trial-log entries | `docs/semantic-control-map-trial.md` |
| Merge to `main` = owner; liveness overlay / ADR / contract changes = owner | ADR 0014/0026/0027 headers; `docs/adr/README.md`; `CONTEXT.md` |
| ADR status / owner decisions must not be falsified | `docs/adr/README.md`; `AGENTS.md` rule 5 |
| External tracker writes require explicit authority | operating map section 4 (ADR 0019 PROPOSED) |
| Ask the owner only for product preference, authority expansion, irreversible tradeoffs, external environment, material product-direction acceptance | `CHARTER.md` "Owner Decisions" |

Owner decisions required (the campaign's terminal state is OWNER_DECISION_REQUIRED
on item 1; items 2-3 are recommendations):

1. **Merge authority for PR #268** (the whole campaign branch; docs + two
   test-file repairs; no ADR, contract, registry, overlay, script, or `src/`
   change).
2. **Whether to record the R1-R6 substrate observation on Issue #255**
   (isolated sub-agent direct worktree writes persisted six times in this
   harness).
3. **Liveness-overlay and registry decisions implied by
   `docs/workflow-system-disposition.md` section 6** (nine items), foremost:
   `product-discovery-sprint` and `product-strategy-sprint` ->
   `compatibility_only`; `full-local-sensemaking` step 3 branch to deprecated
   `discovery`; `setup-sensemaking-skills` registry entry; `mode-coverage.yaml`
   overstated `steps_completed`; packaged catalog/overlay divergence (20 of 23
   ids, 7 of 8 overrides).

---

## 12. DEFERRED NON-CAMPAIGN FINDINGS

| id | Finding | Class | Disposition |
|---|---|---|---|
| D1 | `test_path_drift.py` encoding | LOCAL_BUT_REAL | **CLOSED (R4)** |
| D2 | (a) stale root import -- **CLOSED (R4)**; (b) `test_validate_brief_json.py` fixture/expectation drift | LOCAL_BUT_REAL | (b) DEFERRED -> U8 |
| D3 | `roadmap.md` stale | HISTORICAL_ONLY | no action |
| D4 | `docs/HARDENING_STATUS.md` 5-type fog taxonomy | HISTORICAL_ONLY | no action |
| D5 | dangling link in `docs/candidate/architecture-decision.md` | HISTORICAL_ONLY | no action |
| D6 | `unevaluable` verdict category not in contract | DEFERRED | needs a real case |
| D7 | normal-use lane "0 episodes" is a dated snapshot | NO_ACTION_WARRANTED | none |
| D8 | `validation.yml` line 14 comment stale | LOCAL_BUT_REAL | deferred (fires trial triggers) |
| D9 | Map row SE10 vs current probe output | INSUFFICIENT_EVIDENCE | leave |
| D10 | Trial protocol step-4 selector | LOCAL_BUT_REAL | **fixed at R2 close-out** |
| D11 | Two tests `rglob` the repo root | LOCAL_BUT_REAL (environment) | deferred; C11 |
| D12 | `_validator_utils.py` hard top-level `import workflow_liveness` (fails when loaded as a package path or from a copied file) | LOCAL_BUT_REAL | **CLOSED (R7, `79e02c5`)** |
| D13 | U+2713 prints; `config.py:133` encoding | LOCAL_BUT_REAL, low | deferred |
| D14 | Local Windows/Python 3.14 baseline reds (54 failed / 2 errors with `PYTHONPATH=src`); Linux CI green. Campaign head after R7 expected: 52 failed / 1 error (D1, D2a, two mode-coverage tests fixed; D19 newly visible) -- R8a verifies | LOCAL_BUT_REAL (environment) | like-for-like diff only |
| D15 | Boundary doc "retry" example is hypothetical | NO_ACTION_WARRANTED | none |
| D16 | `docs/task-1-2-sessionstart-hook-testing.md` dated task doc | HISTORICAL_ONLY | no action |
| D17 | `docs/mode-coverage.yaml`: the two pointed entries overstate `steps_completed` (1 vs 0/2 in their own run logs); unpointed "executed" lists (R6 section 6 item 6) | LOCAL_BUT_REAL | deferred; owner decision 3 |
| D18 | Packaged `workflow-registry.yaml` carries 20 of 23 ids; packaged overlay 7 of 8 overrides (R6 section 8) -- consistent with ADR 0027's "shared workflow IDs" wording | INSUFFICIENT_EVIDENCE (intent) | owner decision 3 |
| D19 | `tests/test_validator_utils.py::test_load_workflow_registry_loads_yaml` expects `{"workflows": [{"id": "test"}]}` but `load_workflow_registry` has annotated each workflow with `liveness` since ADR 0027 (`4b42263`); the test was masked by D12 and now fails on its own (R7 F2). One-line expectation update; editing existing tests was outside R7's grant | LOCAL_BUT_REAL | deferred; small separate decision (same class as U8) |

---

## 13. CAMPAIGN ACCEPTANCE STATUS

| # | Condition | Status after R6 | Basis |
|---|---|---|---|
| 1 | Top-level semantic control model explicit and coherent | MET | CONTEXT.md, boundary doc (+R5 section), ADR 0013 |
| 2 | Role of active coding agent clear | MET | ADR 0013 + amendment |
| 3 | Warrant / responsibility / capability / authority not conflated | MET | ADR 0026/0027; every fresh context respected every boundary (R2-R6) |
| 4 | Durable artifacts carry continuation state across responsibilities | MET across five responsibility classes | R1-R6; operating map |
| 5 | One realistic multi-responsibility task continued from durable state | MET: R0 -> R7 across eight contexts with this record as the only shared state, incl. a product-machinery change with regression tests; limitation: one script + tests, no `src/`, single dispatcher | R1-R7 reports |
| 6 | Development direction representable for consequential capability selection | LARGELY MET; limitation: one campaign, one repository | this record; operating map |
| 7 | Role of deterministic scripts bounded and coherent | **MET (R5)** | boundary doc section |
| 8 | Role of hooks defined and evidence-supported | **MET (R5)** | boundary doc "Hooks"; hook doc; CLAUDE.md |
| 9 | Old workflow system has a clear disposition | **MET (R6)**: retained bounded role (1 KEEP), narrowed roles (2 DEMOTE), retirement candidates (2), historical (8), explicit reason for the rest remaining unresolved (10 INSUFFICIENT_EVIDENCE with the evidence limits stated) and the owner decisions implied | `docs/workflow-system-disposition.md` |
| 10 | Existing useful functionality not destroyed | **MET**: `validate-repo.py` green on every head; `test-validators.py` 78/78 unchanged by R7; CI green on every pushed head through `4336a53`; like-for-like suite at the R7 head: 0 NEW, 4 FIXED | section 15; FINAL-REPORT.md section 6 |
| 11 | Tests, validators, contracts, docs, implementation agree sufficiently | LARGELY MET; residual pre-existing items D2(b), D8, D17, D18, D19 (none in CI) | section 12 |
| 12 | Repository passes appropriate complete qualification | **MET** for a qualified PR head: exact-head CI green on all 11 pushed heads; like-for-like full suite 2723 / 51 / 1 vs baseline 2712 / 54 / 2 with 0 NEW failures; not integrated (owner decision) | FINAL-REPORT.md section 6 |
| 13 | Remaining material limitations explicitly documented | **MET**: FINAL-REPORT.md section 9 (product limitations; engineering debt; unvalidated hypotheses; owner decisions; environment blockers; intentionally deferred) + this file sections 6, 8, 11, 12 | FINAL-REPORT.md |

Disposition after R8a: **CAMPAIGN_COMPLETE** (see section 16; R8b probe result appended there when audited).

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
2026-09-02  R5  fresh-context 4-file architecture reconciliation         -> audit
2026-09-02  R5  close-out: VERIFIED; record v6                          -> next: R6
2026-09-02  R6  fresh-context workflow-system disposition (+410); nine
                inventory discrepancies vs the dispatcher's table        -> audit
2026-09-02  R6  close-out: VERIFIED; record v7                          -> next: R7
2026-09-02  --  re-specified: closure deferred one responsibility (G13);
                R7 = D12 machinery continuation; R8 = closure; record v8   -> next: R7
2026-09-02  R7  fresh-context product-machinery continuation: lazy
                workflow_liveness resolver + regression tests; flagged the
                record's wrong after-state prediction (D19)               -> audit
2026-09-02  R7  close-out: VERIFIED; record v9                          -> next: R8
2026-09-02  R8a dispatcher closure: like-for-like suite (0 NEW / 4 FIXED);
                CI green through 4336a53; FINAL-REPORT.md; record v10    -> next: R8b
```

---

## 15. Remote / integration status (updated by the dispatcher, never assumed)

```text
pushed:        4336a53 (R7 close-out) -> origin/campaign/agent-native-self-development
               this R8a commit: pushed after this commit
PR:            #268 (draft) https://github.com/ThorStarlord/sensemaking-skills/pull/268
last main CI:  Validator Ecosystem completed/success @ f10b7da (2026-09-02T03:43Z)
campaign CI:   b4335c3, 2adfeaf, 09bdf5e, ac47191, e35ead1, 89246f4, 5a89f2a,
               eb6c461, e702b31, 1b47d06, 4336a53: completed/success (11 heads)
merged:        nothing (owner decision)
```

---

## 16. Closure summary (R8)

```text
DISPOSITION:            CAMPAIGN_COMPLETE  (FINAL-REPORT.md section 10)
QUALIFIED HEAD:         1b47d06 (last product change) / 4336a53 (last record change
                        before closure) -- exact-head CI green on both
LIKE-FOR-LIKE:          baseline main@f10b7da 2712 passed / 54 failed / 2 errors
                        -> campaign 1b47d06 2723 passed / 51 failed / 1 error;
                        0 NEW failures; 4 FIXED (D1, D2a, two mode-coverage tests)
INTEGRATION:            not merged; owner decision 1 (PR #268)
CLOSURE PROBE (R8b):    pending at v10 -- result appended below when audited
```

Acceptance conditions: 1-3 MET (pre-existing); 4, 5, 7, 8, 9 MET on the
product surface with stated limitations; 6 LARGELY MET (one campaign, one
repository); 10, 12 MET for a qualified PR head; 11 LARGELY MET (residual
pre-existing items D2b, D8, D17, D18, D19, none in CI); 13 MET.

Owner decisions (section 11): merge PR #268; optional Issue #255 note; the
nine registry/overlay/documentation items implied by
`docs/workflow-system-disposition.md` section 6.

Successor guidance: if the owner merges, the next warranted product work is
the owner-decided subset of the nine disposition items and the two small test
expectation fixes (D2b, D19); if the owner does not merge, the branch remains a
qualified, reversible candidate and this record + FINAL-REPORT.md are the
durable evidence. Either way, the semantic-control-map trial closes on its
own schedule (min 2026-09-28) with the events this campaign logged.
