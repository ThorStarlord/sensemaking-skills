# Semantic Control Map

```
STATUS: EXPERIMENTAL PERSISTENCE TRIAL
AUTHORITY: decision-support index only
NOT A SOURCE OF TRUTH

This map summarizes relationships among authoritative repository sources.
Its rows do not supersede ADRs, contracts, validators, CONTEXT.md, runtime
behavior, or measured repository evidence.

When this map conflicts with an authoritative source, the authoritative source
wins and the map is stale.

Absence of a row means NOT ASSESSED, not "no issue" and not "safe."

For questions outside represented rows, use the on-demand projection procedure
(this file, last section) against current repository evidence.
```

**Trial:** `docs/semantic-control-map-trial.md` · **Log:**
`docs/semantic-control-map-trial-log.md` · **Snapshot:** repository state at the
commit that introduced this file (see git blame); rows are refreshed on the
triggers in the trial doc, not on a schedule.

**Columns.** `Grade` `D`/`d`/`I`/`H` (DEMONSTRATED / DERIVED / INTERPRETIVE /
HYPOTHESIS) · `Rate` `S`/`M`/`F` (slow / medium / fast) · `Deriv` `MECH` (a
script over existing repo machinery could refresh it) / `JUDG` (irreducible
human/model call) / `MIX`.

**MIX rows** separate the two halves explicitly:
`FACT:` measured/derived state · `INTERP:` the judgment overlay ·
`judgment:` `affirmed | contested | superseded`, with the date + trigger of the
last review.

---

## A. Semantic authority

| id | Concern | Defines / owns / tie-break | Enforces | Impl vs policy | Evidence | Grade | Rate | Deriv |
|---|---|---|---|---|---|---|---|---|
| SA1 | Top-level control-loop ownership | ADR 0013 (Accepted, ratified 2026-08-13) — active coding agent is the loop; `workflow-runtime.py`/`skill_executor.py` = separate automation/compat path | none (convention) | **FACT:** runtime still exposes whole-loop-style sequencing. **INTERP:** whether that is "policy ahead of impl" (V1) or "aligned" (independent reconstruction) is contested. **judgment:** contested — reviewed 2026-08-31, trigger PR #248 `CONTEXT.md` product-scope language; both readings retained. | ADR 0013 + amendment; `CONTEXT.md`; `docs/decision-orchestration-boundary.md` | D (I on the impl/policy cell) | S | MIX |
| SA2 | `repository_sensemaking_brief` contract — concentration + structure authority | **5 definers**: `skills/workflow-planner/references/artifact-contracts.yaml` + ADR 0014 + ADR 0015 addendum + ADR 0024 + `skills/repo-sensemaker/references/evidence-rules.md` Rule 7. **Structure authority** = `scripts/brief_skeleton.py` (`reconcile()` splices model text only into pre-declared holes) | `scripts/validate-artifact.py` (generic) + `scripts/validate-brief.py` (conditional/blocking) — deliberate split | **FACT:** 5 definers, 2 enforcers, ~4 reconciling comment blocks in the contract file. **INTERP:** aligned but fragile. **judgment:** affirmed — 2026-08-31, initial construction | contract L117-188; `scripts/brief_skeleton.py` | D | M | MIX |
| SA3 | Artifact physical path (session-scoped) | ADR 0010 (Accepted) — runtime `_resolve_artifact_path` is sole owner; executors write `context["expected_output_path"]`, never recompute `artifacts/<id>.md` | `tests/test_executor_path_handoff.py` | **FACT:** one resolver, one handoff test. **INTERP:** cleanest seam; aligned. **judgment:** affirmed — 2026-08-31, initial construction | ADR 0010 | D | S | MIX |
| SA4 | Automatic fog-type → implementation routing | ADR 0018 — **SUPERSEDED 2026-08-18, never Accepted**; no replacement policy Accepted | none (by design) | **impl ahead of policy — largest divergence**: runtime can execute `fast-path`/`full-fog` chains | ADR 0018 disposition; ADR 0014; `CONTEXT.md` L93/L127 | D | S | JUDG |
| SA5 | `auto_invoke_next_workflow` execution authority | ADR 0026 (Accepted 2026-08-24, PR #235) — compatibility metadata only; execution needs a separate explicit authority event | consumers fail closed; `tests/test_auto_invoke_authority_gating.py` | **FACT:** field + 2 registry mirrors + 3 runtime consumers still present; Issue #230 open. **INTERP:** now aligned (guard). **judgment:** affirmed — 2026-08-31, initial construction | ADR 0026; `workflow-registry.yaml` header | D | S | MIX |
| SA6 | MODEL_WARRANT / `representation_sufficiency` | `CONTEXT.md` "MODEL_WARRANT authority (canonical; ADR 0015 addendum)" — producer supplies `representation_sufficiency`, mapped deterministically; INCONCLUSIVE gates routing/materialization/NO_CHANGE | `scripts/validate-brief.py`; `tests/test_warrant_*.py`; runtime seam | **FACT:** `workflow-runtime.py` `warrant_enabled: bool = False` (opt-in, off by default). **INTERP:** policy = canonical, runtime = opt-in — a tension. **judgment:** affirmed — 2026-08-31, initial construction | `CONTEXT.md` MODEL_WARRANT section; `scripts/workflow-runtime.py:226,294,1450` | D (I on the tension) | M | MIX |
| SA7 | Stage-1 controlled model invocation (Gate A) | `scripts/gate_a_authorization.py` — capability, not flag; `authorize()`→`AuthorizationDecision`; only `authorized=True` yields `AuthorizedInvocation` | `scripts/skill_executor.py` requires the capability; `GateAAuthorizationRequired` otherwise | **FACT:** mechanism implemented; ADR 0022 PROPOSED; ADR 0023 (two-lane) Accepted but governance-only; Evidence 0016 `PREPARED_NOT_RUN`. **INTERP:** mechanism real, placement undecided. **judgment:** affirmed — 2026-08-31, initial construction | ADR 0022 header; ADR 0023 §1-2 | D | M | MIX |
| SA8 | Which `workflow-registry.yaml` is canonical | **UNDECIDED** — no file declares canonical. `src/sensemaking_skills/registry.py` loads `src/…/defaults/`; `scripts/workflow-runtime.py` + tests treat `skills/workflow-planner/references/` as authoritative | only `tests/test_auto_invoke_registry_agreement.py`, `auto_invoke` subset only | **FACT:** copies have drifted (SE6); `docs/enforcement-contract.md` §6 says equality "cannot be decided" until the contract is written. **INTERP:** whether "undecided" is a defect. **judgment:** affirmed — 2026-08-31, initial construction | `docs/enforcement-contract.md` §6; both files | D | M | MIX |
| SA9 | Machine field *names* in artifacts | `skills/workflow-planner/references/artifact-contracts.yaml` = canonical | `tests/test_field_contract_agreement.py` — **excluded from the `core-assertions` CI gate on `main`** (needs full SDK deps; refreshed 2026-09-02: still in no CI step — `validation.yml` L720 lists 7 files, not this one) | partial — legacy DEPRECATED copy still sole home of 4 schemas (SL5) | canonical file top comment; `docs/enforcement-contract.md` §3 + 2026-09-02 addendum; `.github/workflows/validation.yml` `core-assertions` job | D | S | MECH |
| SA10 | Canonical vocabulary **+ its enforcement state** | `docs/canonical-vocabulary.yaml` = single source (ADR 0011); validators normalize aliases → canonical | `tests/test_path_drift.py` + `scripts/validate-artifact.py::_validate_enum_fields` + `scripts/validate-fog-type-normalization.py` — **`test_path_drift.py` is GREEN on `main`** (refreshed 2026-09-02: `core-assertions` `success` at `df46871` and `f10b7da`; see SE2) | doc-vs-doc: `docs/HARDENING_STATUS.md` still asserts a 5-type fog taxonomy incl. `integration_fog`, contradicting the 4-type registry | ADR 0011; `docs/canonical-vocabulary.yaml`; `docs/HARDENING_STATUS.md:17` | D | S | MECH |
| SA11 | Product scope vs "production ready" | ADR 0014 (Accepted, owner-ratified 2026-07-26) — human-reviewed brief; routing/tracker-sync/deploy out of scope; **GA not claimed** (`STATUS.md`) | owner decision package 2026-07-26 | **FACT:** `STATUS.md` says GA not claimed; `docs/PHASE-4-5-PRODUCTION-GATE` / project records say "PRODUCTION READY"; that claim rests on **ADR 0021 = SUPERSEDED / never-Accepted**. **INTERP:** the two records conflict. **judgment:** affirmed — reviewed 2026-08-31, trigger PR #248 `CONTEXT.md` product-scope language (explicitly reaffirms ADR 0014 scope); initial construction 2026-08-31 | ADR 0014 header; `STATUS.md:12-24`; ADR 0021 status | D | M | MIX |
| SA12 | Product version authority | `0.2.2` agrees across `package.json`, `pyproject.toml`, `src/sensemaking_skills/__init__.py`; probe emits `conflicting_values` as **evidence-only, never blocking** | `tests/test_cli.py` `TestCLIBasic::test_cli_version` asserts the **current** `0.2.2` → GREEN on `main` (refreshed 2026-09-02: `core-assertions` `success` at `f10b7da`; the older-string assertion recorded in `enforcement-contract.md` §5 is historical) | authority undecided: which declaration is canonical remains a policy decision; probe `conflicting_values` stays evidence-only | `docs/enforcement-contract.md` §4-5 + 2026-09-02 addendum; `tests/test_cli.py` | D | M | MECH |
| SA13 | Which CI findings may block a merge | `scripts/gate_relationship_findings.py` = **sole** decider; promotion rule = mechanically-decidable AND `requires_semantic_review: False`; current blocking set = `missing_reference`, `missing_status_line` only | `tests/test_gate_relationship_findings.py` | the gate + `probe-gate`/`core-assertions` CI jobs are **on `main`** (refreshed 2026-09-02: gate commit `e1db7dc`, 2026-08-11, on `main`'s first-parent history; present at trial start `df46871`; `main` run 33588124719 @ `f10b7da` green). Blocking set unchanged: `missing_reference`, `missing_status_line` (SE1) | `docs/enforcement-contract.md` §4 + 2026-09-02 addendum; `scripts/gate_relationship_findings.py:46-49`; `.github/workflows/validation.yml` L672-736 | D | S | MECH |

## E. Enforcement mismatches

| id | Contract / expectation | Reality | Evidence | Grade | Rate | Deriv |
|---|---|---|---|---|---|---|
| SE1 | Repo has extensive verification machinery | **Refreshed 2026-09-02 (row was stale from construction):** `probe-gate` (Probe Engine + `validate-probe-report.py` + `gate_relationship_findings.py`) and `core-assertions` (7 pytest files incl. `test_path_drift`, `test_cli`) have been on `main` since gate commit `e1db7dc` (2026-08-11 — the `feat/enforcement-gate` tip, on `main`'s first-parent line; no merge commit, no PR), i.e. before trial start `df46871` (2026-08-31). The `validate` job now also runs one pytest step (3 external-repo evidence-citation files, L624). **Residual mismatch:** `test_field_contract_agreement.py` still runs in **no** CI step (SA9); the `validation.yml` L14 comment ("does not execute a single pytest test") is stale | `.github/workflows/validation.yml` L602-736; `docs/enforcement-contract.md` §1-3 (historical) + 2026-09-02 addendum; `git log --first-parent`; `main` run 33588124719 @ `f10b7da` | D | M | MECH |
| SE2 | Canonical-vocabulary coverage + gate-name canonicality | **Refreshed 2026-09-02 (row was stale from construction):** `tests/test_path_drift.py` is **GREEN on `main`** — `core-assertions` `success` at trial start `df46871` (run 33422969527, 2026-08-31) and at `f10b7da` (run 33588124719, 2026-09-02); local utf-8 run 2026-09-02 @ `b4335c3` together with `tests/test_cli.py`: 23 passed / 1 skipped, no new red. The 5 failures mapped in `enforcement-contract.md` §5 (vocab coverage gaps, non-canonical gate names, fog-type naming) no longer reproduce (test file last changed pre-trial at `1ffde16`, 2026-08-23; exact packaged-mirror check added `82a4010`, 2026-09-01). Known environment-only red: under Windows cp1252, `test_fog_type_consistency_in_docs` errors with `UnicodeDecodeError` (`read_text()` without encoding, L154) — an encoding defect, not a vocabulary failure; Linux CI unaffected | `docs/enforcement-contract.md` §5 (historical) + 2026-09-02 addendum; CI runs 33422969527 / 33588124719; `git log -- tests/test_path_drift.py` | D | M | MECH |
| SE3 | Every artifact type has a schema in the canonical contracts file | `prd`/`issue_list`/`agent_brief`/`code_patch` `required_sections`/`required_machine_fields` exist **only** in the DEPRECATED `workflow-orchestrator/references/artifact-contracts.yaml`; `tests/test_artifact_contracts_pm_engineering.py` marks 5 tests `xfail` to encode the gap | legacy file L1-13; xfail tests | D | S | MECH |
| SE4 | `repository_sensemaking_brief` single enforcement | **multiply-enforced**: `validate-artifact.py` (generic presence) + `validate-brief.py` (conditional/blocking); generic must **not** universally require `recommended_workflow_id` or valid `NO_REPOSITORY_CHANGE_WARRANTED` briefs fail | contract L145-148 notes | D | M | MIX |
| SE5 | `weakness_type` = controlled-vocab deterministic field | enforced only by **free-prose substring match** (`scripts/validate-brief.py` ~L279-286) — the prose-brittle pattern ADR 0015 explicitly warns against; ratified as required-but-non-blocking (D2-D4) | ADR 0015 addendum | D | S | MECH |
| SE6 | Two `workflow-registry.yaml` copies agree | only `auto_invoke` subset checked. Full `diff`: `skills/…` copy has an `artifact-reconciliation` workflow, `prior_evidence` inputs, a `repair-verifier` step the `src/…/defaults/` copy lacks. No full-equality check (contract undefined — SA8) | `diff`; `tests/test_auto_invoke_registry_agreement.py` docstring | D | M | MECH |
| SE7 | `auto_invoke_next_workflow` alignment | **policy ahead of impl** — ADR 0026 ruling landed; field + 2 registry mirrors + 3 runtime consumers (`src/sensemaking_skills/runner.py`, `registry.py`, `scripts/workflow-runtime.py`) physically remain; Issue #230 open tracker | ADR 0026 §1; grep | D | S | MECH |
| SE8 | `repair_verification_report` can record an un-observable finding | **no `unevaluable` verdict** — proposed, not encoded in the contract; a failed/errored probe observation has no field. (Independent reconstruction missed this; V1 had it.) | `docs/agent-native-operating-workflow.md` §"Repair verification"; contract L755-776 | D | S | JUDG |
| SE9 | Control loop / stop conditions / next-responsibility selection | **CONVENTION, no machinery** — `docs/agent-native-operating-workflow.md` Reality map; by design (`harden only where pressured`) | `docs/agent-native-operating-workflow.md` Reality map | D | S | JUDG |
| SE10 | Vendored/installed skill copies mirror repo skills | `distribution-drift.yaml`: 15 checked, 10 synced, **5 `line_ending_only`** hash-mismatch (0 content drift): `docs-aligner`, `sensemaking-docs-reconciler`, `setup-sensemaking-skills`, `to-issues`, `to-prd` | `distribution-drift.yaml` | D | F | MECH |

## L. Lifecycle / supersession — physical presence ≠ semantic authority

| id | Item still present | Authority state | Evidence | Grade | Rate | Deriv |
|---|---|---|---|---|---|---|
| SL1 | **ADRs 0005 & 0012** | still `**Status**: Accepted`, but their core mechanism (orchestrator auto-chains skills / `auto_invoke` as authority) is superseded in effect. **ADR 0013 line ~258**: "ADR 0012 … now superceded by skill-led model"; **ADR 0025 line ~22**: "ADR 0005 (Accepted, historical …)". Status lines never updated. Now surfaced by the advisory `stale_accepted_adr_candidate` probe finding | `scripts/probe_relationships.py` (`stale_accepted_adr_candidate`); ADR 0013:255-258; ADR 0025:22 | D | S | MECH |
| SL2 | ADRs 0017, 0018, 0019, 0020, **0021** | SUPERSEDED — "historical proposal, never Accepted" (2026-08-18). 0021 is what the "PRODUCTION READY" record (SA11) rests on | `**Status**` lines; disposition sections | D | S | MECH |
| SL3 | ADRs 0006, 0007, 0008, 0022 | PROPOSED, never Accepted; partial implementation exists anyway (`scripts/gate_a_authorization.py` for 0022; routing-divergence-audit fields from 0008 in `SKILL.md`) | `**Status**` lines | D | S | MECH |
| SL4 | ADRs 0024 & 0025 | ACCEPTED (owner 2026-08-10 / 2026-08-23) but each header: "merge to `main` is a separate action, pending". 0024's fields **are** in the canonical contract at this commit (landed); 0025's conformance test fails on `main`, #232 open | ADR 0024/0025 headers; `artifact-contracts.yaml:163-179` | D | M | MIX |
| SL5 | `workflow-orchestrator/references/artifact-contracts.yaml` | DEPRECATED (2026-08-09), header "No code should read this file" — yet **sole home** of 4 PM/engineering schemas (SE3); still read by `tests/test_path_drift.py`, `tests/test_skill_hygiene_canonical_wiring.py` | legacy file L1-13 | D | S | MECH |
| SL6 | `src/sensemaking_skills/reasoning/` (+ `campaign_accounting/`, `campaign_validation/`) | research-only code **inside the product package**; `reasoning/__init__.py` self-declares "NOT the production orchestrator path". Yet imported by `scripts/workflow-runtime.py` + `scripts/validate-brief.py` via the `warrant_gate` "production-seam" wrapper | `src/sensemaking_skills/reasoning/__init__.py`; `warrant_gate.py`; import grep | D | M | MECH |
| SL7 | `orchestration-runner.py` name | retired programmatic-model-invocation runner (ADR 0013; atomic cut 2026-08-13 — SDK/API executors + 14 test files removed). Deterministic infra (path resolution, validation, gates, planning, sessions) kept | `docs/2026-08-programmatic-runner-retirement-plan.md` Steps 5-7 | D | S | MECH |
| SL8 | `docs/ROUTING_GUIDE`, `docs/run-ledger-guide`, `docs/PORTFOLIO_OPERATIONS`, `docs/PRODUCT-CONTRACT-REVIEW` | still describe the **retired** runner; doc re-scope explicitly **deferred** in the retirement plan | retirement-plan "Documentation reconciliation" section | D | S | MECH |
| SL9 | ADR status vocabulary | `docs/adr/README.md` defines PROPOSED/PROVISIONAL/ACCEPTED/SUPERSEDED/REJECTED; `scripts/probe_relationships.py` reads every ADR `**Status**` line, flags unrecognized/missing/mismatch | `docs/adr/README.md`; `scripts/probe_relationships.py` | D | S | MECH |
| SL10 | ~30 root `PHASE-*.md`, `run_day{3,4,5}_tests.py`, `test_phase3_*.py`, `docs/archive/` | historical build scaffolding, marked HISTORICAL/SUPERSEDED, retained deliberately, no current authority; volume is a navigation hazard | file listing; retirement-plan doc buckets | D | S | MECH |

## R. Research → product / runtime crossings

| id | Crossing | Reaches runtime how | Mode | Evidence | Grade | Rate | Deriv |
|---|---|---|---|---|---|---|---|
| SR1 | MODEL_WARRANT gate (from `experiments/product-hypothesis-b/`) | `sensemaking_skills.reasoning.warrant_gate.run_seam_warrant` called by `scripts/workflow-runtime.py` (~L1450) after the brief step; when active, INCONCLUSIVE blocks routing/materialization/NO_CHANGE | **GUARDED + OPT-IN** — `warrant_enabled=False` default; wrapper never raises; no evidence mutation | `scripts/workflow-runtime.py:226,294,1438-1473`; `src/sensemaking_skills/reasoning/warrant_gate.py` docstring | D | M | MECH |
| SR2 | `extended_analysis` Section 15 brief fields | declared in canonical `artifact-contracts.yaml`, spliced by `brief_skeleton.reconcile()`, checked non-blockingly by `validate-brief.py`. Lineage: `prototype/repo-sensemaker-vnext` PR #164 (never merged) → `candidate/` → ADR 0024 (Accepted). A 5th field (`discovery_confidence`) was falsified in stress-test and removed | **OPTIONAL, model-constrained, non-blocking**; explicitly **not** read by routing (`_WORKFLOW_ID_FIELDS`/`_FOG_TYPE_FIELDS`) | ADR 0024 §1; `artifact-contracts.yaml:163-179` | D | S | MECH |
| SR3 | four-type fog taxonomy (research diagnostic construct) | emitted as `primary_fog_type` into brief/plan | **DE-AUTHORIZED crossing** — "diagnostic metadata" only; grants no routing/execution authority (ADR 0018 disposition + 0026 + `CONTEXT.md`) | `CONTEXT.md` fog section; ADR 0018 disposition | D | S | JUDG |
| SR4 | two-lane experiment authorization (ADR 0023) | schema files + `EXP-NNNN` namespace present | **NOT YET CROSSED** — "No runtime component reads, validates, or enforces anything defined here yet"; scaffolding invites the assumption it is live | ADR 0023 §1 final line, §2 | D | M | MECH |
| SR-neg | every other research thread | C6R hypothesis proper, warrant-as-primitive, domain-general transfer, Paths 1-4, Goal A, #218 — **do not wire into any runtime path**; research-agenda status "hypotheses only, not an ADR, not a roadmap commitment" | `docs/research/control-model-research-agenda.md` status; import grep finds no runtime consumer | D | M | MECH |

---

## Row inventory (this snapshot)

| Section | Rows | MECH | JUDG | MIX |
|---|---|---|---|---|
| A. Semantic authority | 13 | 5 | 1 | 7 |
| E. Enforcement mismatches | 10 | 7 | 2 | 1 |
| L. Lifecycle / supersession | 10 | 9 | 0 | 1 |
| R. Research → product crossings | 5 | 4 | 1 | 0 |
| **Total** | **38** | **25 (66%)** | **4 (11%)** | **9 (24%)** |

The entire Lifecycle section is mechanically derivable (ADR `**Status**` lines,
file-header greps, `diff`s, `distribution-drift.yaml`). The irreducible-judgment
rows cluster in policy-vs-impl framing (SA4, SR3), the `unevaluable`-gap call
(SE8), and control-loop-unenforced-by-design (SE9), plus the judgment overlays
on the 9 MIX rows.

---

## On-demand projection procedure (for questions no row covers)

1. **Locate the authority, not the code.** Grep `docs/adr/` for the concept;
   read the matching ADR **and its `**Status**` line**. Then check `CONTEXT.md`,
   `docs/decision-orchestration-boundary.md`, `docs/enforcement-contract.md` for
   a later disposition — a superseding note often lives in a *newer* ADR's
   "Depends on" list, not the old ADR.
2. **Separate declared from enforced.** Find the enforcer (`tests/test_*`,
   `scripts/validate-*.py`, `scripts/gate_*.py`); confirm it exists **and runs
   in `.github/workflows/validation.yml` on `main`** — many named tests do not.
   If it does not run in CI, treat the contract as advisory.
3. **Check for a second copy.** Registries/contracts here are duplicated
   (`skills/…/references/` vs `src/sensemaking_skills/defaults/` vs
   `workflow-orchestrator/references/`). `diff` them; find which the runtime
   actually loads. If no file declares canonical, that is the answer — undecided.
4. **Check research lineage.** If the concept appears under `experiments/` or
   `docs/research/`, trace whether anything in `scripts/` or `src/` imports it,
   and whether the call is default-on, opt-in (`*_enabled=False`), or guarded.
5. **Carry authority + lifecycle + grade** on every relationship you
   materialize. **Stop** when you can name the defining source, the enforcing
   mechanism (or its absence), the winning side of any conflict, and the
   lifecycle state. Do not enumerate call graphs or module inventories.
6. **Record the projection locally**; do not add it to this map. Promotion
   default = NO (repeated usefulness + stable semantics required).
