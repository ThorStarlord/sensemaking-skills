# Workflow-system disposition (campaign vocabulary, evidence-backed)

```
DATE:      2026-09-02
STATUS:    non-authoritative disposition record. Not an ADR, not a contract,
           not a validator input, not a registered workflow, not a Skill.
AUTHORITY: none of its own. ADR 0027 and the liveness overlay
           (skills/workflow-planner/references/workflow-liveness.yaml; packaged
           copy src/sensemaking_skills/defaults/workflow-liveness.yaml) remain
           the operative liveness authority. This document classifies the 23
           registered workflows in the campaign vocabulary defined in
           docs/campaigns/agent-native-self-development/CHARTER.md
           ("Workflow-System Policy During This Campaign") and records the
           execution evidence behind each classification.
CHANGES:   nothing. No registry, overlay, artifact contract, Skill, ADR,
           script, or test is changed by this document. Any liveness change it
           implies is an owner decision (ADR 0027 makes the overlay
           owner-ratified).
PRODUCED:  campaign responsibility R6 (docs/campaigns/agent-native-self-
           development/CAMPAIGN-STATE.md section 10), performed by a fresh
           context from the record plus repository state at
           campaign/agent-native-self-development @ 89246f4 (base main @
           f10b7da). The record's starting inventory was rebuilt from the
           sources before use; discrepancies are listed in the R6 report.
READS:     nothing in scripts/, src/, tests/, or .github/ reads this file.
```

Related: [ADR 0027](adr/0027-workflow-registry-liveness.md) (liveness);
[ADR 0014](adr/0014-product-boundary.md) (ratified product boundary);
[operating map](agent-native-operating-workflow.md) section 1 (registered
workflows as subgraphs); [executability analysis](../artifacts/workflow_executability_consumer_analysis.md)
(the evidence behind ADR 0027); [CHARTER.md](campaigns/agent-native-self-development/CHARTER.md)
("Candidate Architecture" item 7; "Workflow-System Policy During This
Campaign").

---

## 1. Definitions

- **registered**: the id has an entry in
  `skills/workflow-planner/references/workflow-registry.yaml` (23 entries at
  the revision above; the packaged catalog
  `src/sensemaking_skills/defaults/workflow-registry.yaml` carries 20 of them,
  see section 8). Registration preserves identity and provenance only
  (ADR 0027 "Catalog identity").
- **liveness** (`active` | `compatibility_only`): declared in
  `workflow-liveness.yaml`; default `active`; `compatibility_only` = retained
  for identity/provenance, ineligible for current recommendation, selection,
  planning, or execution (ADR 0027 "Liveness overlay"). Eight overrides at
  `workflow-liveness.yaml:14-21`. Liveness is not execution authority
  (ADR 0027; ADR 0026 as summarised at `workflow-registry.yaml:1-7`).
- **step_type**: `local_execution` = the step names a Skill the active agent
  is expected to have installed locally; `external_routing` = the step
  delegates outward and makes no claim of local executability
  (`workflow_executability_consumer_analysis.md` section 2 and line 67). One
  step is **conditional** (`full-local-sensemaking` step `3-conditional`,
  `workflow-registry.yaml:519-534`): its `if_true` branch is an
  `external_routing` step to `discovery`.
- **skill status** (from `skill-registry.yaml`): entries with no `status`
  field are treated here as implemented **only when** `skills/<id>/SKILL.md`
  exists (checked: 17 Skill directories exist); `proposed` = referenced but
  not implemented (`triage`, `skill-registry.yaml:79-85`); `deprecated` = no
  implementation under `skills/` (`tdd` and the UI and product-management
  entries, `skill-registry.yaml:86-113, 118-291`); **not in registry** =
  `setup-sensemaking-skills`, which has a Skill directory but no
  `skill-registry.yaml` entry (`scripts/validate-repo.py:220-223` exempts it
  by name).
- **execution evidence classes** (what a pointer in section 3 can be):
  1. *run ledger line* -- an event line in a `run-ledger.jsonl` (`run_started`,
     `step_started`, `artifact_created`, `validation_completed`,
     `step_completed`, `run_completed`); a run counts as executed only if it
     has step events, and as completed only if `run_completed` carries
     `status: completed`;
  2. *run log / workflow summary* -- `run_log*.md` / `workflow_summary.json`
     written by the runtime for the same session;
  3. *mode-coverage entry* -- a line in `docs/mode-coverage.yaml`. Only the
     two entries under `mode_coverage:` (lines 2-26) carry a `run_log_path`;
     the `workflows_executed` and `live_invocations` lists (lines 80-95,
     122-134, 140-263) are historical claims with no pointer. Claims without
     a pointer are listed but do not count as records;
  4. *evidence record* -- `experiments/evidence/NNNN-*/EVIDENCE.md` (or
     `README.md` / `RESULT.md` in the older folders) that names the workflow
     and describes a run of it;
  5. *agent-native artifact* -- a contract-shaped artifact under `artifacts/`
     (carrying an `artifact_id`) produced by the active agent reading a
     Skill's `SKILL.md` directly (ADR 0013). Agent-native executions leave no
     ledger by design, so this class is the only trace they have;
  6. *recommendation mention* -- a `recommended_workflow_id:` field in a
     brief or plan. This is **not** execution evidence for the named
     workflow. Most `workflow_id` hits in the repository are of this kind;
  7. *plan-only / test-only trace* -- a `plan_only` ledger (one `run_started`
     line, no step events), a run whose executor was a fixture, a
     shadow-mode / scenario / `test_*` artifact, or an evaluation-design
     construction candidate. These **do not count** (record criteria).

---

## 2. Disposition criteria (stated before the table)

The classes are the campaign charter's: `KEEP_AS_BOUNDED_SUBGRAPH | REPAIR |
DEMOTE | RETIRE_CANDIDATE | HISTORICAL | INSUFFICIENT_EVIDENCE`. The
criteria below are the ones the campaign record specified for R6; the
interpretation rules that follow them were needed to apply the criteria to
the evidence actually found and are stated so they can be audited.

- **KEEP_AS_BOUNDED_SUBGRAPH** = `active` + every step's Skill is implemented
  + at least one real execution record (ledger, evidence record, or
  agent-native artifact) + the sequence has recurred or is the ratified
  product spine. The charter's investment rule (recurring responsibility
  sequence + stable ordering + sufficiently low semantic ambiguity +
  measurable reliability/cost benefit; `CHARTER.md` lines 544-551) is applied
  only to justify KEEP, and each of its four parts is rated separately.
- **INSUFFICIENT_EVIDENCE** = `active` + implemented Skills + no real
  execution record (plan_only or test-only traces do not count).
- **HISTORICAL** = `compatibility_only` per ADR 0027. Not re-decided here.
- **RETIRE_CANDIDATE** = `active` but every step routes to a deprecated or
  unimplemented Skill.
- **REPAIR** = `active`, evidenced, with a specific defect that can be cited.
- **DEMOTE** = `active` with evidence that its role is narrower than the
  registry implies (cited).

Interpretation rules used:

1. A recommendation mention (class 6) never satisfies "real execution
   record".
2. plan_only ledgers, fixture-executor runs, scenario/shadow-mode/test
   artifacts, and construction candidates (class 7) never satisfy it.
3. A mode-coverage claim without a run-log pointer is listed as a claim; it
   does not satisfy it. Where a mode-coverage entry does carry a pointer, the
   pointed-to record governs when the two disagree.
4. The **ratified product spine** is what ADR 0014 ratifies as in scope:
   `repo-sensemaker` producing a validated, human-reviewed
   `repository_sensemaking_brief` (ADR 0014 lines 68-76). It is a single
   Skill, not a registered workflow; routing and the second golden-path step
   are explicitly deferred (ADR 0014 lines 78-87). No registered workflow is
   therefore "the ratified product spine" as such; the clause could not be
   used to satisfy KEEP for any row.
5. A record that shows one step's Skill exercised outside the registered
   sequence is evidence for the Skill, not for the workflow. Where such
   partial records recur and show the workflow's practical role to be a
   proper subset of its registered steps, that is DEMOTE evidence
   (cited per row).
6. Runner-era records (2026-05 to 2026-07, `--executor claude-code`, an
   executor removed on 2026-08-13 by
   `docs/2026-08-programmatic-runner-retirement-plan.md` lines 179-193) are
   real execution records for exactly what their ledgers show. They are not
   reproducible with the retained runtime (`dry-run` / `prompt-chain` only)
   and they do not evidence agent-native use.
7. Where "evidenced" is a precondition (REPAIR, DEMOTE), the evidence is
   pinned to a file and line range. Where it could not be pinned, the row is
   INSUFFICIENT_EVIDENCE, and any defect observed in the registry definition
   is recorded in the rationale and in section 6 instead of producing REPAIR.

---

## 3. Per-workflow disposition (23 rows)

Registry line ranges refer to `skills/workflow-planner/references/workflow-registry.yaml`
(`WR:`); skill-registry lines to `skills/workflow-planner/references/skill-registry.yaml`
(`SR:`); `MC:` = `docs/mode-coverage.yaml`; `EV:` = `experiments/evidence/`;
`OM:` = `docs/agent-native-operating-workflow.md`. "implemented" means no
`status` field in `SR` and `skills/<id>/SKILL.md` exists.

| id | liveness | step skills (status) | execution evidence (pointers) | disposition | rationale |
|---|---|---|---|---|---|
| `fast-path-workflow` (WR:9-46) | active | 1 repo-sensemaker (implemented, SR:17); 2 workflow-planner (implemented, SR:22); both local_execution; `auto_invoke_next_workflow` WR:45-46 is compatibility metadata (WR:1-7) | No ledger. Claim: MC:133 "fast-path-workflow (guided_execution)" under orchestration-runner.py, no pointer. All `workflow_id` hits are recommendation mentions: `artifacts/repository_sensemaking_brief.md:213` (2026-05-25; its own text at line 138 says no real agent had completed a Phase 1 cycle), `artifacts/repository_sensemaking_brief_scenario{2,3,5}.md` (Phase-4 test scenarios), `EV:0022-workflow-v0-repeated-use/auteur-repository-sensemaking-brief.md` (the closest-match fabrication recorded as F1, EV:0022 EVIDENCE.md:115-121, later fixed) | INSUFFICIENT_EVIDENCE | active, both Skills implemented, no real execution record; only claims, test scenarios, and recommendation mentions |
| `full-fog-workflow` (WR:47-101) | active | 1 problem-framer (SR:7); 2 unknowns-mapper (SR:12); 3 repo-sensemaker (SR:17); 4 workflow-planner (SR:22); all implemented, local_execution; auto-invoke WR:100-101 compatibility metadata | No ledger. Claims: MC:123-125 (orchestration-runner: prompt_chain, yolo, guided), no pointer. `artifacts/workflow_orchestration_plan.md:14-25` is a plan selecting this workflow from `artifacts/shadow_mode_test_brief_escalation.md` (a shadow-mode test brief; both added 6bfe439, 2026-05-25). No evidence record names a run | INSUFFICIENT_EVIDENCE | active, implemented, no real execution record |
| `setup-sensemaking-repo` (WR:102-133) | active | 1 setup-sensemaking-skills (Skill directory exists; **not in SR**; `validate-repo.py:220-223` exempts it by name); 2 repo-sensemaker (SR:17); 3 handoff (SR:47); all local_execution | plan_only only: MC:82, MC:151, MC:174. No ledger, no evidence record, no artifact | INSUFFICIENT_EVIDENCE | active, implemented, no real execution record. Registry gap noted (section 6, item 4), not a REPAIR because unevidenced |
| `docs-contract-reconciliation` (WR:134-184) | active | 1 repo-sensemaker (SR:17); 2 sensemaking-docs-reconciler (SR:32); 3 repair-verifier (SR:42); 4 handoff (SR:47); all implemented, local_execution; `prior_evidence` input WR:144-151 added from evidence 0018 | Evidence records: EV:0019 EVIDENCE.md:5-6 (self-dogfood run of this workflow), :20-28 (findings), :30-51 (six repairs executed and validated); EV:0018 EVIDENCE.md:20-24 (auteur cycle B: brief -> plan -> 5 commits -> PR #72 merged), :101; EV:0021 EVIDENCE.md:54-56, :159-204 (authorised narrow reconciliation of CONTEXT.md executed, validated, CLOSED). Agent-native artifacts: `artifacts/repository_sensemaking_brief_dogfood.md` (recommends this workflow; 8edf1aa 2026-08-12), `artifacts/docs_contract_reconciliation_report_dogfood.md:1-30` (`artifact_id docs_contract_reconciliation_report`), `artifacts/session_summary_dogfood.md:1-15` (`artifact_id session_summary`), `artifacts/dogfood-evidence-index.md:15-41` (validators pass); `artifacts/workflow_orchestration_plan_docs_contract_reconciliation_2026-08-22.md:1-30` (plan choosing this workflow; 1ffde16 2026-08-23), `artifacts/reconciliation_patch_draft_docs_contract_2026-08-22.md`, `artifacts/repair_verification_report.md:1-15` (`artifact_id repair_verification_report`; PARTIAL CLOSURE with `findings_closed` / remaining). Claims: MC:93 (workflow-runtime guided_execution, no pointer), MC:142, 169, 197, 231. Product surface: OM:240-243 (registered subgraph, step 3), OM:464 (REAL + dogfooded), OM:484-485 | KEEP_AS_BOUNDED_SUBGRAPH | active; all four Skills implemented; multiple real execution records; the sequence recurred in-repo (2026-08-12 dogfood set, 0019 on 2026-08-13, 0021 remediation on 2026-08-14, 2026-08-22/23 set) and once externally (auteur cycle B). Investment rule: recurring = yes; stable ordering = yes (brief -> reconciliation -> verification -> handoff); low ambiguity = yes (mechanical drift classes: version, stale claim, fixture coverage, contract field); measurable benefit = PARTIAL (finding-specific closures are recorded in 0019 and `repair_verification_report.md`; no like-for-like comparison against unstructured agent work exists). Limitation: no single run carries all four contract-shaped outputs; the union of runs does |
| `artifact-reconciliation` (WR:185-237) | active | 1 repo-sensemaker (SR:17); 2 output-reconciler (SR:37); 3 to-issues (SR:74); 4 handoff (SR:47); all implemented, local_execution | Evidence record: EV:0020 EVIDENCE.md:7-11 (the observed pattern is this workflow's operating pattern), :33-45 (four-step encoding), :47-51 (prototypes = evidence records 0018 and 0019), :55-56 (authored documentation of an observed process, not a run record). Agent-native artifacts: `artifacts/work_claim.md:1-10` (`artifact_id work_claim`; docs-aligner run 2026-09-01) and `artifacts/reconciliation_report.md:1-35`, `:200-208` (`artifact_id reconciliation_report`; `created_at: 2026-09-01`; added 060fc36 2026-09-01) = step 2. No `issue_list` and no `session_summary` artifact exists for that run (no such `artifact_id` under `artifacts/` besides the docs-contract dogfood handoff); recommendations are carried inline at `:200-206`. Earlier instances also stop at the report: EV:0018 EVIDENCE.md:97-106 (findings filed directly as GitHub issues), EV:0022 EVIDENCE.md:334-357 (inline reconciliation + repair verification for F1). Product surface: OM:226-232, OM:463. No ledger (agent-native by design); no mode-coverage entry | DEMOTE | active; all Skills implemented; a real agent-native record exists for the reconcile step and it has recurred (0018, 0022, 2026-09-01). Every recorded instance stops at the reconciliation report: steps 3-4 (`to-issues`, `handoff`) have never been recorded for this workflow, and ADR 0014 lines 101-104 already confines `issue_list` to artifact production. The evidenced role is the two-step core (claim/brief -> `reconciliation_report`), narrower than the registered four-step chain. Alternative reading, not chosen: INSUFFICIENT_EVIDENCE for the full chain |
| `autonomous-sprint-preflight` (WR:238-264) | active | 1 repo-sensemaker (SR:17); 2 handoff (SR:47); implemented, local_execution | plan_only only: MC:83, MC:152, MC:175. No ledger, evidence record, or artifact. Its purpose (WR:240-241) is to gate "Autonomous Sprint", whose two registered forms are `compatibility_only` (ADR 0027 lines 55-57) | INSUFFICIENT_EVIDENCE | active, implemented, no real execution record; purpose now points at compatibility-only workflows (section 6, item 5) |
| `docs-architecture` (WR:265-290) | active | 1 docs-aligner (SR:63); 2 handoff (SR:47); implemented, local_execution | Claims: MC:84 (plan_only), MC:88 (guided_execution), MC:153, MC:176 -- no pointer. Step-1 Skill outputs exist agent-natively but outside this workflow: `artifacts/domain_alignment_report.md` (docs-aligner autonomous run 2026-09-01, `gate: none`, per `artifacts/work_claim.md:4-5`; file first added be8c407 2026-05-16), `artifacts/domain_alignment_report_run2.md`, `artifacts/docs_aligner_dogfood_evaluation.md` -- produced in the reconciliation lane, no `session_summary`. `EV:0013-.../repository_sensemaking_brief.md` recommends it (mention) | INSUFFICIENT_EVIDENCE | active, implemented, no record of the registered two-step sequence; docs-aligner is evidenced as a Skill (rule 5) |
| `product-to-issues` (WR:291-324) | compatibility_only (overlay :14; ADR 0027 line 55) | 1 to-prd (SR:69); 2 to-issues (SR:74); 3 triage (**proposed**, SR:79-85, no implementation) | Claim: MC:89 (plan_only). No ledger or record | HISTORICAL | per ADR 0027; not re-decided |
| `product-discovery-sprint` (WR:325-367) | active (no override) | 1 persona (SR:118-124); 2 discovery (SR:125-131); 3 interview-synthesis (SR:132-138); 4 opportunity-tree (SR:146-152); 5 hypothesis (SR:153-159); **all `deprecated`, none under `skills/`; all `external_routing`** | Claims only: MC:149, MC:164 (guided_execution), MC:186-188, MC:211 (all five steps validated via dispatcher) -- 2026-05-era, no run record in the repository. `workflow_executability_consumer_analysis.md:67` scopes the two external-routing sprints out of ADR 0027's set as "separate compatibility/product questions" | RETIRE_CANDIDATE | active but every step routes to a deprecated, unimplemented Skill (record G11 / U9). Implied owner decision: section 6, item 1 |
| `product-strategy-sprint` (WR:368-410) | active (no override) | 1 lean-canvas (SR:208-214); 2 north-star (SR:222-228); 3 okr (SR:201-207); 4 roadmap (SR:194-200); 5 stakeholder-update (SR:271-277); **all `deprecated`, none under `skills/`; all `external_routing`** | Claims only: MC:85, MC:154 (plan_only). No run record | RETIRE_CANDIDATE | as above (G11 / U9) |
| `product-autonomous-sprint` (WR:411-476) | compatibility_only (overlay :15) | 1-7 persona, discovery, opportunity-tree, hypothesis, prd (SR:167-173), user-stories (SR:174-180), acceptance-criteria (SR:181-187) -- all deprecated; 8 handoff (SR:47) | Claims: MC:86, MC:155, MC:177 (plan_only) | HISTORICAL | per ADR 0027 |
| `full-local-sensemaking` (WR:477-554) | active | 1 problem-framer; 2 unknowns-mapper; `3-conditional` -> `if_true` = discovery (**deprecated**, SR:125-131) as `external_routing` (WR:519-534); 4 repo-sensemaker; 5 workflow-planner; 6 handoff; the five named local Skills implemented; auto-invoke WR:502-505 compatibility metadata | plan_only ledgers: `artifacts/02-orchestration-run/run-ledger.jsonl:1`, `03-.../run-ledger.jsonl:1`, `04-.../run-ledger.jsonl:1` (single `run_started` line each, 2026-05-23/25) with `plan_full-local-sensemaking.md` plans. Claims: MC:90, MC:94 (workflow-runtime plan_only, yolo), MC:128-131 (orchestration-runner yolo, guided, autonomous), MC:148, 163, 185, 201, 210, 217, 222, 241 (validator coverage "steps 1-4") -- no run record. EV:0021 EVIDENCE.md:206 (CONTEXT.md keeps a legacy CLI-path caveat on its DEFAULT entry); retirement plan lines 106-119 (default mode now plan_only) | INSUFFICIENT_EVIDENCE | active, named local Skills implemented, no real execution record (plan_only only). Defect observed, not a REPAIR because unevidenced: the conditional branch targets a deprecated Skill (section 6, item 3) |
| `fast-local-diagnostic` (WR:555-586) | active | 1 repo-sensemaker (SR:17); 2 handoff (SR:47); implemented, local_execution | Ledger: `artifacts/01-orchestration-run/run-ledger.jsonl:1-6` (yolo_execution, 2026-05-23; `validation_completed` failed, `run_completed` failed); `run_log_fast-local-diagnostic_yolo_execution.md:8, 21-27, 40` (`runtime: fixture`; artifact path `examples/repo-sensemaker/repository_sensemaking_brief-fixture.md`; steps completed 0/2); `workflow_summary.json:5-12`. MC:2-14 records this same session with `steps_completed: 1` (MC:6) -- contradicted by the run record. Further claims without pointer: MC:81, 91, 92, 95, 126-127, 132, 141-145, 168-172, 215-221. Agent-native brief production is well evidenced (EV:0021, EV:0022 briefs) but not as this workflow (no `session_summary`). `experiments/product-interaction-p2-v1/repo-sensemaker-investigation-v1.md` recommends it (mention) | INSUFFICIENT_EVIDENCE | active, implemented; the only workflow-level record is a failed run whose executor was a fixture (test-only trace, rule 2). Step 1 is the ratified spine's Skill, but the two-step sequence as registered has no real record (rule 4). Mode-coverage overstatement: section 6, item 6 |
| `experimental-autonomous-sprint` (WR:587-637) | compatibility_only (overlay :16) | 1 docs-aligner; 2 to-prd; 3 to-issues; 4 triage (proposed); 5 tdd (**deprecated**, SR:86-92); 6 handoff | Claims: MC:87, MC:156, MC:178 (plan_only) | HISTORICAL | per ADR 0027 |
| `skill-maintenance-loop` (WR:638-664) | active | 1 skill-maintainer (SR:51); 2 handoff (SR:47); implemented, local_execution | Claims only: MC:147, 162, 184, 209, 240 (guided_execution), MC:245-253 ("production artifact") -- no pointer; no `skill_improvement_plan` artifact is tracked under `artifacts/`. `workflow_id` hits are recommendation mentions: `EV:0006-.../RESULT.md:8`, `EV:0006-.../final-run-e787fc41/repository_sensemaking_brief.md`, `EV:0008-.../{positive,negative}/...` | INSUFFICIENT_EVIDENCE | active, implemented, no real execution record in the repository |
| `implementation-workflow` (WR:665-721) | compatibility_only (overlay :17) | 1 docs-aligner; 2 to-prd; 3 to-issues; 4 triage (proposed); 5 tdd (deprecated); 6 handoff | Claim: MC:129 (orchestration-runner guided_execution). EV:0021 EVIDENCE.md:170-175 (registry presence check only). Recommendation mentions in `EV:0015-.../raw/repository_sensemaking_brief.md` and `experiments/results/EXP-0005-.../attempts/*/repository-sensemaking-brief.md` | HISTORICAL | per ADR 0027 |
| `product-implementation-workflow` (WR:722-792) | compatibility_only (overlay :18) | 1 docs-aligner; 2 discovery (deprecated); 3 opportunity-tree (deprecated); 4 to-prd; 5 to-issues; 6 triage (proposed); 7 tdd (deprecated); 8 handoff | Recommendation mentions only (`artifacts/shadow_mode_test_conflict.md`, `artifacts/shadow_mode_test_error_retry.md`, `experiments/post-hardening-adjudication-probe-v1/packets/*/brief-*.md`, product/solution interaction investigations). EV:0021 EVIDENCE.md:173-175 (presence check) | HISTORICAL | per ADR 0027 |
| `ui-diagnostic-workflow` (WR:793-829) | compatibility_only (overlay :19) | 1 docs-aligner; 2 ui-brief (**deprecated**, SR:93-99); `auto_invoke_next_workflow_id` WR:823-829 is compatibility metadata | Recommendation mentions only (post-hardening packets `strong-ui-fog`, `web-frontend`; one e3 construction candidate) | HISTORICAL | per ADR 0027 |
| `ui-implementation-workflow` (WR:830-893) | compatibility_only (overlay :20) | 1 docs-aligner; 2 ui-flow (SR:100-106); 3 ui-screen-spec (SR:107-113) -- deprecated; 4 to-issues; 5 triage (proposed); 6 tdd (deprecated); 7 handoff | Recommendation mentions only (`artifacts/repository_sensemaking_brief_scenario4.md`, `artifacts/scenario5_*`, `artifacts/shadow_mode_test_brief_001.md`, `artifacts/test_plan_failure_attempt_3.md`, e3 candidates). EV:0022 EVIDENCE.md:38-39 (auteur's vendored validator warns about this workflow's unregistered artifacts -- external) | HISTORICAL | per ADR 0027 |
| `docs-implementation-workflow` (WR:894-929) | active | 1 docs-aligner (SR:63); 2 to-prd (SR:69); 3 handoff (SR:47); all implemented, local_execution | None: no ledger, no mode-coverage entry, no evidence record, no `prd` artifact under `artifacts/`. All `workflow_id` hits are recommendation mentions (`artifacts/workflow_orchestration_plan_scenario4.md` -- test scenario; post-hardening packets; one e3 candidate). EV:0021 EVIDENCE.md:173-175 (presence check). `workflow_executability_consumer_analysis.md:116` records that `workflow-planner` SKILL.md offers it for docs fog | INSUFFICIENT_EVIDENCE | active, implemented, no real execution record; it is the only implementation-workflow left `active` after ADR 0027 |
| `architecture-implementation-workflow` (WR:930-986) | compatibility_only (overlay :21) | 1 docs-aligner; 2 to-prd; 3 to-issues; 4 triage (proposed); 5 tdd (deprecated); 6 handoff | 38 `workflow_id` hits, all recommendation mentions (`artifacts/repository_sensemaking_brief_phase4_1*.md`, `artifacts/scenario5_*`, `artifacts/test_brief_failure_attempt_*`, `artifacts/workflow_orchestration_plan_phase4_1*.md`, post-hardening packets, e3 candidates, product-interaction investigations). Absent from the packaged catalog and packaged overlay (section 8) | HISTORICAL | per ADR 0027 |
| `skill-evaluation-workflow` (WR:987-1023) | active | 1 usage-researcher (SR:55); 2 skill-maintainer (SR:51); 3 handoff (SR:47); implemented, local_execution | None: no ledger, no mode-coverage workflow entry (MC:254-263 is validator coverage of `usage_research_report` on standalone scenarios), no evidence record, no tracked artifact. One `workflow_id` hit in `experiments/evaluation-design-e3-autonomous-task-v2/construction/tranche1/candidates/T1H-K9W.md` (construction candidate) | INSUFFICIENT_EVIDENCE | active, implemented, no real execution record |
| `architectural-review-planning-workflow` (WR:1024-1061) | active | 1 repo-sensemaker (SR:17); 2 architectural-review (SR:27); implemented, local_execution; `auto_invoke_next_workflow: false` | All records are runner-era (`--executor claude-code`, removed 2026-08-13; rule 6): EV:0005 `run-ledger.jsonl:1-6`, `run_log.md:8, 21, 40`, `README.md:46-55, 105` (guided, 2026-07-25; step 1 failed validation; 0/2); EV:0006 `RESULT.md:3-9` (LIVE STEP 1 PROVEN: brief validated), `:22-24, 48-55` (step 2 auto-cascaded and failed on missing `proposed_direction`; `final-run-e787fc41/workflow_summary.json` status failed); EV:0008 `EVIDENCE.md:84-86, 114` (positive run resumed from 0006's step 1; step 2 completed and validated; ledger `status: completed`, exit 0; `positive/workflow_summary.json` "2/2 steps completed"), `:137-139, 162` (negative run fails closed as designed), `:164-173` (golden path justified for this workflow only); EV:0013 `EVIDENCE.md:3, 32, 69`, EV:0014 `EVIDENCE.md:5-13`, EV:0015 `raw/workflow_summary.json` (three controlled Stage-1 runs on auteur, step 1 only, all STAGE 1 FAIL on structural validation). MC:15-26 (`steps_completed: 1` at MC:19 vs 0/2 in the cited run log), MC:134, MC:268-270. ADR 0014 lines 57-66 (golden path proven internally for exactly this workflow), 78-87 (step 2 deferred, not ratified). No agent-native run is recorded; OM:175-181 maps architecture uncertainty to the `architectural-review` Skill | DEMOTE | KEEP's four literal conditions hold (active; both Skills implemented; real ledgers; recurred across 7 runs), but the investment rule fails: 1 of 7 runs completed both steps (and only by resuming a prior step-1 success), 5 halted at step-1 validation, every run was an internal harness or controlled-experiment proof through an executor since removed, and ADR 0014 keeps step 2 outside the ratified boundary. Evidenced role: the internal golden-path proof vehicle; current entry to the responsibility is the Skill via agent selection. Mode-coverage overstatement: section 6, item 6 |

---

## 4. Counts

| disposition | count | workflows |
|---|---|---|
| KEEP_AS_BOUNDED_SUBGRAPH | 1 | docs-contract-reconciliation |
| REPAIR | 0 | -- |
| DEMOTE | 2 | artifact-reconciliation; architectural-review-planning-workflow |
| RETIRE_CANDIDATE | 2 | product-discovery-sprint; product-strategy-sprint |
| HISTORICAL | 8 | product-to-issues; product-autonomous-sprint; experimental-autonomous-sprint; implementation-workflow; product-implementation-workflow; ui-diagnostic-workflow; ui-implementation-workflow; architecture-implementation-workflow |
| INSUFFICIENT_EVIDENCE | 10 | fast-path-workflow; full-fog-workflow; setup-sensemaking-repo; autonomous-sprint-preflight; docs-architecture; full-local-sensemaking; fast-local-diagnostic; skill-maintenance-loop; docs-implementation-workflow; skill-evaluation-workflow |
| total | 23 | |

Of the 15 `active` workflows: 1 KEEP, 2 DEMOTE, 2 RETIRE_CANDIDATE, 10
INSUFFICIENT_EVIDENCE. Of the 13 active workflows whose steps are all
implemented, exactly one (`docs-contract-reconciliation`) has a recurring
successful trace of its full registered sequence.

---

## 5. Migration path / retained roles

No migration is performed by this document. The retained roles, and how each
is entered inside the agent-owned loop, are:

- **The loop is the agent's, workflows are subgraphs.** The operating map,
  section 1 (`agent-native-operating-workflow.md:45-49`), states that the
  control loop belongs to the active coding agent (ADR 0013), that the
  runtime/scripts are deterministic support machinery, and that registered
  workflows are potentially subgraphs inside the loop, not the whole loop.
  Entry into any workflow happens at the loop's SELECT NEXT RESPONSIBILITY
  stage (map section 1 diagram; section 2 "NEXT-SKILL SELECTION"): the agent
  chooses the responsibility from the reviewed brief, then the Skill or
  bounded workflow that serves it. Nothing routes into a workflow
  automatically (ADR 0014 defers routing; ADR 0026 makes auto-invoke fields
  compatibility metadata; consumers fail closed).
- **KEEP -- `docs-contract-reconciliation`.** Retained as the bounded subgraph
  for the responsibility "docs / implementation disagreement" (map
  section 2 table, line 180) and for repair verification of a prior finding
  (map lines 240-243: "Registered subgraph: docs-contract-reconciliation
  workflow step 3"). Entered when BRIEF REVIEW establishes a drift finding
  with `uncertainty.source = repository_evidence` and repair is authorised
  (finding != authorisation, map section 4). Performed agent-natively: the
  agent reads the four step Skills' `SKILL.md` in registry order and
  produces the contracted artifacts; the runtime is used for path
  resolution, plan generation (`plan_only` default, retirement plan
  lines 106-119), and validation dispatch only. Each output is validated on
  production (map section 2 "VALIDATION"). No new investment (schema,
  automation, hook) is claimed: the measurable-benefit part of the
  investment rule is only partially met (section 3 rationale).
- **DEMOTE -- `artifact-reconciliation`.** Its evidenced core (work claim or
  brief -> `output-reconciler` -> `reconciliation_report`) remains the
  operational form of the loop's OUTPUT RECONCILIATION stage (map
  lines 221-232) and is entered whenever a material work claim or handoff
  is made. Steps 3-4 remain registered but unevidenced; whether to narrow
  the registered definition is an owner decision (section 6, item 7).
- **DEMOTE -- `architectural-review-planning-workflow`.** The responsibility
  it wraps (architecture uncertainty -> `architectural-review`) is entered
  as a Skill via agent selection (map line 177). The workflow definition is
  retained as the internal golden-path proof vehicle (ADR 0014 lines 57-66)
  and as the target of the runtime's resume/gate/precondition evidence
  (EV:0008). Whether the registry description should say so is an owner
  decision (section 6, item 8).
- **RETIRE_CANDIDATE -- the two external-routing sprints.** No retained role
  is evidenced; both remain `active` by overlay default until the owner
  decides (section 6, item 1). Nothing on the product surface enters them.
- **HISTORICAL -- the eight compatibility-only workflows.** Retained for
  identity and provenance only (ADR 0027 "Catalog identity"); consumers fail
  closed on them; not entered.
- **INSUFFICIENT_EVIDENCE -- the ten remaining active workflows.** They stay
  `active` under ADR 0027's default and remain selectable subject to the
  authority model; this document neither promotes nor demotes them. The path
  from INSUFFICIENT_EVIDENCE to KEEP is the charter's: recover the workflow
  from repeated successful real traces (agent-native artifacts or evidence
  records that name the workflow and show its sequence), not from a
  prospective catalog. The path to REPAIR or DEMOTE is a pinned defect or a
  pinned narrower role on a real trace.

---

## 6. Implied owner decisions, not applied

None of the following is performed here; each is a registry, overlay,
contract, or documentation change outside R6's authority.

1. **Liveness of the two external-routing sprints.** `product-discovery-sprint`
   and `product-strategy-sprint` are RETIRE_CANDIDATE: add them to the
   `compatibility_only` overrides in both overlay copies, or retire their
   identities through a separate migration. ADR 0027's initial set was
   scoped to `local_execution` dependencies
   (`workflow_executability_consumer_analysis.md:67`), so the overlay is
   internally consistent today while still declaring these two selectable.
2. **The product-management ecosystem.** 28 `deprecated` entries under
   `skill-registry.yaml:115-291` (plus `tdd` and three UI Skills under
   `:86-113`) are retained so historical workflow references reconcile. The
   options are: keep as historical catalog (current posture), or retire the
   identities together with the workflows that reference them. ADR 0027's
   non-decision "create a general-purpose lifecycle framework" bounds any
   answer.
3. **`full-local-sensemaking` step `3-conditional`.** Its `if_true` branch
   routes to `discovery` (deprecated, `external_routing`,
   `workflow-registry.yaml:519-534`). Remove the branch, retarget it, or
   record it as compatibility metadata.
4. **`setup-sensemaking-skills` registry entry.** The Skill exists under
   `skills/` but has no `skill-registry.yaml` entry; `validate-repo.py:220-223`
   exempts it by name. Add an entry, or keep the exemption and document it.
5. **`autonomous-sprint-preflight` purpose.** It gates "Autonomous Sprint"
   workflows that are now `compatibility_only`. Keep, retarget, or demote once
   a real trace exists.
6. **`docs/mode-coverage.yaml` claims.** The two entries that carry a
   `run_log_path` both record `steps_completed: 1` where the cited run log
   and ledger record 0/2 (`mode-coverage.yaml:6` vs
   `artifacts/01-orchestration-run/run_log_fast-local-diagnostic_yolo_execution.md:40`;
   `mode-coverage.yaml:19` vs `experiments/evidence/0005-runtime-skeleton-live-step1/run_log.md:40`).
   The `workflows_executed` and `live_invocations` lists carry no pointers.
   Whether to annotate the file as historical claims is a documentation
   decision.
7. **`artifact-reconciliation` definition.** Narrow the registered sequence
   to its evidenced core, or keep steps 3-4 pending a trace that records
   them.
8. **`architectural-review-planning-workflow` description.** Whether the
   registry description should identify it as the internal golden-path
   proof (ADR 0014) rather than a general selectable workflow, and whether
   ADR 0014's deferral of step 2 should be revisited -- which ADR 0014
   lines 78-87 say requires external proof.
9. **Packaged catalog and overlay divergence.** The packaged catalog carries
   20 of the 23 ids and 7 of the 8 overrides (section 8). Whether this is
   intended is a packaging decision.

---

## 7. What this document does not do

ADR 0027's "Explicit non-decisions", restated (ADR 0027 lines 103-113): this
document does **not** revive `tdd`; implement `triage`; replace missing
Skills one-for-one; choose new implementation workflows for product, UI, or
architecture fog; authorise automatic routing; create a general-purpose
lifecycle framework for Skills, artifacts, or arbitrary entities; or make
`active` equivalent to execution authorisation.

In addition, this document does not: change any liveness value; delete,
revive, or edit any workflow or Skill; re-decide the eight compatibility-only
workflows; ratify a workflow as the product spine (ADR 0014 governs); promote
any convention to machinery (operating map section 7 rule); or treat a
disposition as authorisation to act on it.

---

## 8. Evidence limits

What could not be established, and why:

- **Agent-native executions leave no ledger.** Under ADR 0013 the active
  agent reads Skills directly; the only durable trace is a contract-shaped
  artifact or an evidence record. Absence of a ledger is therefore not
  absence of use, and an artifact under `artifacts/` does not by itself say
  which registered workflow, if any, it was produced under. Rows were
  classified on what the artifacts and records say, not on inference.
- **Runner-era records are not reproducible.** All ledgers with step events
  (`artifacts/01-orchestration-run`, evidence 0005/0006/0008/0013/0014/0015)
  were produced by the `claude-code` SDK executor removed on 2026-08-13
  (retirement plan lines 179-193). They evidence what happened then; they
  cannot be re-run with the retained `dry-run` / `prompt-chain` executors.
- **`docs/mode-coverage.yaml` is largely unpointed.** Of its many
  "executed" claims, only two carry a `run_log_path`, and both overstate
  `steps_completed` relative to their run records (section 6, item 6). The
  remaining claims (2026-05-16 to 2026-05-17 sessions) could not be tied to
  any file in the repository.
- **`workflow_id` search hits are mostly recommendations.** Of the files under
  `artifacts/` and `experiments/` that name a workflow in a `workflow_id`-like
  field, the large majority do so as `recommended_workflow_id` in a brief or
  plan. The record's `ldg` column counted these; they were separated here.
  `architecture-implementation-workflow`'s 38 hits are all of this kind.
- **Test and scenario artifacts dominate `artifacts/`.** Phase-4 scenario
  briefs, shadow-mode test briefs, `test_*_attempt_*` files, and
  evaluation-design construction candidates name workflows without
  executing them.
- **External and GitHub-only evidence.** Auteur-side runs (evidence 0018
  cycle B; 0022 vendoring reconciliation, `docs/reviews/...` in auteur) and
  the Issue #218 normal-use episodes are not in this repository and were
  cited only where an in-repo evidence record describes them.
- **Untracked artifacts were not consulted.** `mode-coverage.yaml:245-253`
  refers to a `skill-maintenance-loop` "production artifact"; no
  `skill_improvement_plan` artifact is tracked under `artifacts/` at this
  revision.
- **Packaged catalog and overlay.** `src/sensemaking_skills/defaults/workflow-registry.yaml`
  carries 20 ids (missing `artifact-reconciliation`,
  `architecture-implementation-workflow`,
  `architectural-review-planning-workflow`) and its overlay lists 7
  overrides (no `architecture-implementation-workflow`). ADR 0027's
  verification item 6 is phrased for "shared workflow IDs", so this is
  consistent with the ADR as written, but the campaign record's "either copy"
  wording assumed both copies carry the same eight.
- **`setup-sensemaking-skills`** has no `skill-registry.yaml` entry, so its
  "status" here is a directory check, not a registry status.
- **Measurable benefit** (charter investment rule, fourth part) has not been
  measured for any workflow against unstructured agent execution; the KEEP
  row states this as PARTIAL rather than met.

---

## 9. Sources consulted for this document

`docs/campaigns/agent-native-self-development/CAMPAIGN-STATE.md` (sections 2,
6, 8, 10 incl. the starting inventory) and `CHARTER.md`;
`docs/adr/0027-workflow-registry-liveness.md`; `docs/adr/0014-product-boundary.md`;
`artifacts/workflow_executability_consumer_analysis.md`;
`skills/workflow-planner/references/{workflow-registry,workflow-liveness,skill-registry}.yaml`;
`src/sensemaking_skills/defaults/{workflow-registry,workflow-liveness}.yaml`;
`skills/*/SKILL.md` (directory listing); `scripts/validate-repo.py:215-235`;
`docs/mode-coverage.yaml`; `artifacts/0[1-4]-orchestration-run/*`;
`experiments/evidence/0005, 0006, 0008, 0013, 0014, 0015` (run records and
summaries) and `0018..0023/EVIDENCE.md`; `artifacts/reconciliation_report.md`,
`work_claim.md`, `repair_verification_report.md`,
`docs_contract_reconciliation_report_dogfood.md`, `session_summary_dogfood.md`,
`dogfood-evidence-index.md`, `workflow_orchestration_plan*.md`,
`repository_sensemaking_brief*.md` (headers and machine sections);
`docs/agent-native-operating-workflow.md` (section 1, section 2, Reality
map); `docs/2026-08-programmatic-runner-retirement-plan.md`; git history for
artifact add dates.
