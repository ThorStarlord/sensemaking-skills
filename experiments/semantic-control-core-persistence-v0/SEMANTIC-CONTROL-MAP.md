# SEMANTIC CONTROL MAP — merged candidate (persistence prototype v0)

Represents `sensemaking-skills @ ba8968ca1a12caa90ce7beb0ee5fd2dfac055f37`.
Merge of V1's 22 rows (`research/semantic-control-core-v1`) + agent B's
non-duplicate independent additions (`smk-indep-recon-out/…`, zero V0/V1
exposure). One authoritative row per semantic concern. Evidence **referenced**,
not copied.

Columns: **Grade** `D`/`d`/`I`/`H` (DEMONSTRATED/DERIVED/INTERPRETIVE/HYPOTHESIS)
· **Rate** `S`/`M`/`F` (slow/medium/fast) · **Deriv** =
`MECH` (a script over existing repo machinery could refresh it) /
`JUDG` (irreducible human/model call) / `MIX`.

---

## A. Semantic authority

| id | Concern | Defines / owns / tie-break | Enforces | Impl vs policy | Evidence | Grade | Rate | Deriv |
|---|---|---|---|---|---|---|---|---|
| SA1 | Top-level control-loop ownership | ADR 0013 (Accepted, ratified 2026-08-13) — active coding agent is the loop; `workflow-runtime.py`/`skill_executor.py` = separate automation/compat path | none (convention) | **contested judgment**: V1 "policy ahead of impl" (runtime still exposes whole-loop sequencing); B "aligned" | ADR 0013 + amendment; `CONTEXT.md`; `decision-orchestration-boundary.md` | D (I for the impl/policy cell) | S | JUDG |
| SA2 | `repository_sensemaking_brief` contract — concentration + structure authority | **5 definers**: `artifact-contracts.yaml` + ADR 0014 + ADR 0015 addendum + ADR 0024 + `evidence-rules.md` Rule 7. **Structure** authority = `scripts/brief_skeleton.py` ("canonical brief-structure authority"; `reconcile()` splices model text only into pre-declared holes) | `validate-artifact.py` (generic) + `validate-brief.py` (conditional/blocking) — deliberate split | aligned but fragile (5 definers, 2 enforcers, ~4 reconciling comment blocks in the contract file) | contract L117-188; `brief_skeleton.py`; runner-retirement-plan Step-4 | D | M | MIX |
| SA3 | Artifact physical path (session-scoped) | ADR 0010 (Accepted) — runtime `_resolve_artifact_path` is sole owner; executors write `context["expected_output_path"]`, never recompute `artifacts/<id>.md` | `tests/test_executor_path_handoff.py` (real runtime↔executor handoff) | aligned (cleanest seam) | ADR 0010 | D | S | MIX |
| SA4 | Automatic fog-type → implementation routing | ADR 0018 — **SUPERSEDED 2026-08-18, never Accepted**; no replacement policy Accepted | none (by design) | **impl ahead of policy — largest divergence**: runtime can execute `fast-path`/`full-fog` chains | ADR 0018 disposition; ADR 0014; `CONTEXT.md` L93/L127 | D | S | JUDG |
| SA5 | `auto_invoke_next_workflow` execution authority | ADR 0026 (Accepted 2026-08-24, PR #235) — compatibility metadata only; execution needs a separate explicit authority event | consumers fail closed; `tests/test_auto_invoke_authority_gating.py` | now aligned (guard); field + 2 registry mirrors + 3 runtime consumers still present | ADR 0026; `workflow-registry.yaml` header | D | S | MIX |
| SA6 | MODEL_WARRANT / `representation_sufficiency` | `CONTEXT.md` "MODEL_WARRANT authority (canonical; ADR 0015 addendum)" — producer supplies `representation_sufficiency`, mapped deterministically; INCONCLUSIVE gates routing/materialization/NO_CHANGE | `validate-brief.py`; `tests/test_warrant_*.py`; runtime seam | **policy = canonical, runtime = opt-in**: `workflow-runtime.py` `warrant_enabled: bool = False` | `CONTEXT.md` MODEL_WARRANT section; `workflow-runtime.py:226,294,1450` | D (I for the tension) | M | MIX |
| SA7 | Stage-1 controlled model invocation (Gate A) | `scripts/gate_a_authorization.py` — capability, not flag; `authorize()`→`AuthorizationDecision`; only `authorized=True` yields `AuthorizedInvocation` | `skill_executor.py` requires the capability; `GateAAuthorizationRequired` otherwise | **mechanism real, placement undecided** — ADR 0022 PROPOSED; ADR 0023 (two-lane) Accepted but governance-only ("nothing reads/enforces it yet"); Evidence 0016 `PREPARED_NOT_RUN` | ADR 0022 header; ADR 0023 §1-2 | D | M | MIX |
| SA8 | Which `workflow-registry.yaml` is canonical | **UNDECIDED** — no file declares canonical. `src/sensemaking_skills/registry.py` loads `src/…/defaults/`; `workflow-runtime.py` + tests treat `skills/workflow-planner/references/` as authoritative. `enforcement-contract.md` §6: equality "cannot be decided" until the contract is written | only `test_auto_invoke_registry_agreement.py`, `auto_invoke` subset only | copies **have drifted** (see SE6) | `enforcement-contract.md` §6; both files | D | M | MIX |
| SA9 | Machine field *names* in artifacts | `skills/workflow-planner/references/artifact-contracts.yaml` = canonical | `tests/test_field_contract_agreement.py` — but **excluded from the `core-assertions` CI gate** (needs full SDK deps) | partial — legacy DEPRECATED copy still sole home of 4 schemas (SL5) | canonical file top comment; `enforcement-contract.md` §3 | D | S | MECH |
| SA10 | Canonical vocabulary **+ its enforcement state** | `docs/canonical-vocabulary.yaml` = single source (ADR 0011); validators normalize aliases → canonical | `test_path_drift.py` + `validate-artifact.py::_validate_enum_fields` + `validate-fog-type-normalization.py` — **but `test_path_drift.py` is RED on `main`** (see SE2) | doc-vs-doc: `HARDENING_STATUS.md` still asserts a 5-type fog taxonomy incl. `integration_fog`, contradicting the 4-type registry | ADR 0011; `canonical-vocabulary.yaml:9-44`; `HARDENING_STATUS.md:17` | D | S | MECH |
| SA11 | Product scope vs "production ready" | ADR 0014 (Accepted, owner-ratified 2026-07-26) — human-reviewed brief; routing/tracker-sync/deploy out of scope; **GA not claimed** (`STATUS.md`) | owner decision package 2026-07-26 | **policy-vs-record conflict**: project memory / `docs/PHASE-4-5-PRODUCTION-GATE` say "PRODUCTION READY — APPROVED FOR DEPLOYMENT"; that claim rests on **ADR 0021 = SUPERSEDED / never-Accepted** | ADR 0014 header; `STATUS.md:12-24`; ADR 0021 status | D | M | MIX |
| SA12 | Product version authority | `0.2.2` agrees across `package.json`, `pyproject.toml`, `__init__.py`; probe emits `conflicting_values` as **evidence-only, never blocking** ("which declaration is authoritative — policy decision not yet made") | `tests/test_cli.py::test_cli_version` asserts an **older** string → deterministically RED on `main` | authority undecided; test assertion known-wrong, repair is a separate decision | `enforcement-contract.md` §4-5 | D | M | MECH |
| SA13 | Which CI findings may block a merge | `scripts/gate_relationship_findings.py` = **sole** decider; promotion rule = mechanically-decidable AND `requires_semantic_review: False`; current blocking set = `missing_reference`, `missing_status_line` only | `tests/test_gate_relationship_findings.py` | the whole gate lives on **unmerged** branch `feat/enforcement-gate` (see SE1) | `enforcement-contract.md` §4 | D | S | MECH |

## E. Enforcement mismatches

| id | Contract / expectation | Reality | Evidence | Grade | Rate | Deriv |
|---|---|---|---|---|---|---|
| SE1 | Repo has extensive verification machinery | The CI `validate` job **runs no pytest**. Probe Engine, relationship probes, `test_path_drift`, `test_field_contract_agreement`, `test_cli` run in **no** CI step. The jobs that fix this (`probe-gate`, `core-assertions`) exist only on branch `feat/enforcement-gate`, merge "awaiting separate authorization" | `enforcement-contract.md` §1-3 | D | M | MECH |
| SE2 | Canonical-vocabulary coverage + gate-name canonicality | `tests/test_path_drift.py` **RED on `main`** — 5 failures (vocab coverage gaps for workflows/artifacts, non-canonical gate names `review_findings`/`review_recommendation` in the registry, fog-type naming inconsistency in docs). Repair is a separate un-taken decision | `enforcement-contract.md` §5 | D | M | MECH |
| SE3 | Every artifact type has a schema in the canonical contracts file | `prd`/`issue_list`/`agent_brief`/`code_patch` `required_sections`/`required_machine_fields` exist **only** in the DEPRECATED `workflow-orchestrator/references/artifact-contracts.yaml`; `tests/test_artifact_contracts_pm_engineering.py` marks 5 tests `xfail` to encode the gap | legacy file L1-13; xfail tests | D | S | MECH |
| SE4 | `repository_sensemaking_brief` single enforcement | **multiply-enforced**: `validate-artifact.py` (generic presence) + `validate-brief.py` (conditional/blocking); generic must **not** universally require `recommended_workflow_id` or valid `NO_REPOSITORY_CHANGE_WARRANTED` briefs fail | contract L145-148 notes | D | M | MIX |
| SE5 | `weakness_type` = controlled-vocab deterministic field | enforced only by **free-prose substring match** (`validate-brief.py:279-286`) — the prose-brittle pattern ADR 0015 explicitly warns against; ratified as required-but-non-blocking (D2-D4) | ADR 0015 addendum | D | S | MECH |
| SE6 | Two `workflow-registry.yaml` copies agree | only `auto_invoke` subset checked. Full diff: `skills/…` copy has an `artifact-reconciliation` workflow, `prior_evidence` inputs, a `repair-verifier` step the `src/…/defaults/` copy lacks. No full-equality check (contract undefined — SA8) | `diff`; `test_auto_invoke_registry_agreement.py` docstring | D | M | MECH |
| SE7 | `auto_invoke_next_workflow` alignment | **POLICY_AHEAD_OF_IMPL** — ADR 0026 ruling landed; field + 2 registry mirrors + 3 runtime consumers (`runner.py`, `registry.py`, `workflow-runtime.py`) physically remain; Issue #230 open tracker | ADR 0026 §1; grep | D | S | MECH |
| SE8 | `repair_verification_report` can record an un-observable finding | **no `unevaluable` verdict** — proposed, not encoded in the contract; a failed/errored probe observation has no field. (V1-only; independent agent B missed this) | `AGW` §"Repair verification"; contract L755-776 | D | S | JUDG |
| SE9 | Control loop / stop conditions / next-responsibility selection | **CONVENTION, no machinery** — `AGW` Reality map; the most consequential judgments are the least mechanically protected (by design, `harden only where pressured`) | `AGW` Reality map | D | S | JUDG |
| SE10 | Vendored/installed skill copies mirror repo skills | `distribution-drift.yaml`: 15 checked, 10 synced, **5 `line_ending_only`** hash-mismatch (0 content drift): `docs-aligner`, `sensemaking-docs-reconciler`, `setup-sensemaking-skills`, `to-issues`, `to-prd`. `STATUS.md` claims synchronized | `distribution-drift.yaml` | D | F | MECH |

## L. Lifecycle / supersession — physical presence ≠ semantic authority

| id | Item still present | Authority state | Evidence | Grade | Rate | Deriv |
|---|---|---|---|---|---|---|
| SL1 | **ADRs 0005 & 0012** | still `Status: Accepted`, but their core mechanism (orchestrator auto-chains skills / `auto_invoke` as authority) is superseded in effect by ADR 0013/0014/0026 + `CONTEXT.md`. ADR 0026 "Depends on" note says so; 0005/0012 status lines never updated | ADR 0026 depends-on; ADR 0005:6,59; ADR 0012:90-93 | D | S | MECH |
| SL2 | ADRs 0017, 0018, 0019, 0020, **0021** | SUPERSEDED — "historical proposal, never Accepted" (2026-08-18). 0021 is what the "PRODUCTION READY" record (SA11) rests on | `**Status**` grep; disposition sections | D | S | MECH |
| SL3 | ADRs 0006, 0007, 0008, 0022 | PROPOSED, never Accepted; partial implementation exists anyway (`gate_a_authorization.py` for 0022; routing-divergence-audit fields from 0008 in `SKILL.md`) | `**Status**` grep | D | S | MECH |
| SL4 | ADRs 0024 & 0025 | ACCEPTED (owner 2026-08-10 / 2026-08-23) but each header: "merge to `main` is a separate action, pending". 0024's fields **are** in the canonical contract at this commit (landed); 0025's conformance test fails on `main`, #232 open | ADR 0024/0025 headers; `artifact-contracts.yaml:163-179` | D | M | MIX |
| SL5 | `workflow-orchestrator/references/artifact-contracts.yaml` | DEPRECATED (2026-08-09), header "No code should read this file" — yet **sole home** of 4 PM/engineering schemas (SE3); still read by `test_path_drift.py`, `test_skill_hygiene_canonical_wiring.py` | legacy file L1-13 | D | S | MECH |
| SL6 | `src/sensemaking_skills/reasoning/` (+ `campaign_accounting/`, `campaign_validation/`) | research-only code **inside the product package**; `reasoning/__init__.py` self-declares "NOT the production orchestrator path". Yet imported by `workflow-runtime.py` + `validate-brief.py` via the `warrant_gate` "production-seam" wrapper | `reasoning/__init__.py:1-6`; `warrant_gate.py:1-19`; import grep | D | M | MECH |
| SL7 | `orchestration-runner.py` name | retired programmatic-model-invocation runner (ADR 0013; atomic cut 2026-08-13 — SDK/API executors + 14 test files removed). Deterministic infra (path resolution, validation, gates, planning, sessions) kept | retirement-plan Steps 5-7 | D | S | MECH |
| SL8 | `docs/ROUTING_GUIDE`, `run-ledger-guide`, `PORTFOLIO_OPERATIONS`, `PRODUCT-CONTRACT-REVIEW` | still describe the **retired** runner; doc re-scope explicitly **deferred** in the retirement plan | retirement-plan "Documentation reconciliation" | D | S | MECH |
| SL9 | ADR status vocabulary | `docs/adr/README.md` defines PROPOSED/PROVISIONAL/ACCEPTED/SUPERSEDED/REJECTED; `scripts/probe_relationships.py` reads every ADR `**Status**` line, flags unrecognized/missing/mismatch | `docs/adr/README.md`; `probe_relationships.py` | D | S | MECH |
| SL10 | ~30 root `PHASE-*.md`, `run_day{3,4,5}_tests.py`, `test_phase3_*.py`, `docs/archive/` | historical build scaffolding, marked HISTORICAL/SUPERSEDED, retained deliberately, no current authority; volume is a navigation hazard | file listing; retirement-plan doc buckets | D | S | MECH |

## R. Research → product / runtime crossings

| id | Crossing | Reaches runtime how | Mode | Evidence | Grade | Rate | Deriv |
|---|---|---|---|---|---|---|---|
| SR1 | MODEL_WARRANT gate (from `experiments/product-hypothesis-b/`) | `reasoning.warrant_gate.run_seam_warrant` called by `workflow-runtime.py::_run_seam_warrant` (~L1450) after the brief step; when active, INCONCLUSIVE blocks routing/materialization/NO_CHANGE | **GUARDED + OPT-IN** — `warrant_enabled=False` default; wrapper never raises; no evidence mutation | `workflow-runtime.py:226,294,1438-1473`; `warrant_gate.py` docstring | D | M | MECH |
| SR2 | `extended_analysis` Section 15 fields (`domain`, `consequential_boundary`, `uncertainty`, `owner_intent_state`) | declared in canonical `artifact-contracts.yaml`, spliced by `brief_skeleton.reconcile()`, checked non-blockingly by `validate-brief.py`. Lineage: `prototype/repo-sensemaker-vnext` PR #164 (never merged) → `candidate/` → ADR 0024 (Accepted). A 5th field (`discovery_confidence`) was falsified in stress-test and removed | **OPTIONAL, model-constrained, non-blocking**; explicitly **not** read by routing (`_WORKFLOW_ID_FIELDS`/`_FOG_TYPE_FIELDS`) | ADR 0024 §1; `artifact-contracts.yaml:163-179` | D | S | MECH |
| SR3 | four-type fog taxonomy (research diagnostic construct) | emitted as `primary_fog_type` into brief/plan | **DE-AUTHORIZED crossing** — "diagnostic metadata" only; grants no routing/execution authority (ADR 0018 disposition + 0026 + `CONTEXT.md`) | `CONTEXT.md` fog section; ADR 0018 disposition | D | S | JUDG |
| SR4 | two-lane experiment authorization (ADR 0023) | schema files + `EXP-NNNN` namespace present | **NOT YET CROSSED** — "No runtime component reads, validates, or enforces anything defined here yet"; scaffolding invites the assumption it is live | ADR 0023 §1 final line, §2 | D | M | MECH |
| SR-neg | every other research thread | C6R hypothesis proper, warrant-as-primitive, domain-general transfer, Paths 1-4, Goal A, #218 — **do not wire into any runtime path**; research-agenda status "hypotheses only, not an ADR, not a roadmap commitment" | `control-model-research-agenda.md` status; import grep finds no runtime consumer | D | M | MECH |

---

## Row inventory

| Section | Rows | MECH | JUDG | MIX |
|---|---|---|---|---|
| A. Semantic authority | 13 | 4 (SA9, SA10, SA12, SA13) | 2 (SA1, SA4) | 7 |
| E. Enforcement mismatches | 10 | 6 | 2 (SE8, SE9) | 2 (SE4 + …) |
| L. Lifecycle / supersession | 10 | 10 | 0 | 0 |
| R. Research → product crossings | 5 | 4 | 1 (SR3) | 0 |
| **Total** | **38** | **~24 (63%)** | **~7 (18%)** | **~7 (18%)** |

The lifecycle section is **entirely mechanically derivable** (ADR `**Status**`
lines, file-header greps, `diff`s, retirement-plan section names). The
irreducible-judgment rows cluster in semantic authority: policy-vs-impl calls
(SA1, SA4), the `unevaluable`-gap call (SE8), control-loop-unenforced-by-design
(SE9), the fog-taxonomy de-authorization framing (SR3). ~63% of the map could be
refreshed by a script over machinery the repo already has.
