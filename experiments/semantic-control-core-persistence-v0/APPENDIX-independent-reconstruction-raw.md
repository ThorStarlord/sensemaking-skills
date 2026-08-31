# Independent Semantic-Control Representation — `sensemaking-skills` @ `ba8968c`

## Method

I inspected, in this order: (1) `CONTEXT.md` and `CLAUDE.md` for the declared operating
model and the repo's own "artifacts are the API" enforcement rules; (2) every file in
`docs/adr/` — headers plus full text of the load-bearing ones — and extracted every
`**Status**` line to separate Accepted / Proposed / Superseded; (3) `docs/enforcement-contract.md`
and `docs/2026-08-programmatic-runner-retirement-plan.md` for the CI-gate map and the runner
lifecycle; (4) `docs/decision-orchestration-boundary.md` for the decision-vs-orchestration
authority split; (5) the duplicated authoritative files — the two `artifact-contracts.yaml`
copies and the two `workflow-registry.yaml` copies — diffed against each other, plus their
partial enforcer tests; (6) version declarations (`package.json`, `pyproject.toml`,
`__init__.py`); (7) `docs/canonical-vocabulary.yaml` vs `docs/HARDENING_STATUS.md` vs
`skills/workflow-planner/SKILL.md` for fog-taxonomy agreement; (8) `src/sensemaking_skills/reasoning/`
and its call sites in `scripts/workflow-runtime.py` / `scripts/validate-brief.py` for
research-into-runtime crossings; (9) `docs/research/` index and `experiments/` names.
I stopped when further reading was only re-confirming rows already graded DEMONSTRATED, and
when remaining questions were plainly answerable by ordinary `grep` (import graphs, file
inventories, per-workflow step lists) and therefore out of scope per the task's exclusion test.
Historical checks against PR/commit boundaries rely on the ADR/plan prose that cites them;
I did not replay `git log` for each.

**Standing finding:** the governance surface here is unusually large for the amount of
product — 26 ADRs, a separate enforcement contract, a retirement plan, a research agenda,
a decision/orchestration boundary doc, and several "ACCEPTED but merge-to-main pending"
records. Much of the consequential knowledge is *which of two present representations
currently holds authority*, not *what the code does*.

---

## 1. Semantic authority

| # | Concern | Definer / owner / tie-break | Enforcement | Implementation vs policy | Evidence | Grade | Rate |
|---|---|---|---|---|---|---|---|
| A1 | All enum values (fog types, gates, modes, workflow/artifact IDs) | `docs/canonical-vocabulary.yaml` = single source of truth; validators normalize aliases → canonical; canonical form wins | 3-layer: `tests/test_path_drift.py`, `scripts/validate-artifact.py::_validate_enum_fields` (`INVALID_ENUM_VALUE`), `validate-fog-type-normalization.py` | aligned in principle; layer-1 currently RED (see B2) | ADR 0011 (Accepted) | DEMONSTRATED | SLOW |
| A2 | Fog-type taxonomy size | `canonical-vocabulary.yaml` + `skills/workflow-planner/SKILL.md:98` define exactly **4** (`product_fog`,`ui_fog`,`architecture_fog`,`docs_fog`); `integration_fog` explicitly non-canonical; 4-def wins | validator fixture `tests/fixtures/validate-brief/invalid/integration-fog-brief.md` treats `integration_fog` as INVALID | **DOC-vs-DOC conflict:** `docs/HARDENING_STATUS.md:17,227` still asserts a 5-type taxonomy incl. `integration_fog` "defined by" the registry — stale, contradicts the registry it cites | `canonical-vocabulary.yaml:9-44`; `HARDENING_STATUS.md:17` | DEMONSTRATED | SLOW |
| A3 | Where an artifact physically lives (session-scoped path) | Runtime is sole owner: `OrchestrationRunner._resolve_artifact_path`; executors must write to `context["expected_output_path"]`, never recompute `artifacts/<id>.md` | `tests/test_executor_path_handoff.py` (real runtime↔executor handoff) | aligned | ADR 0010 (Accepted) | DEMONSTRATED | SLOW |
| A4 | Machine field *names* in artifacts | `skills/workflow-planner/references/artifact-contracts.yaml` = canonical; `workflow-orchestrator/references/artifact-contracts.yaml` = explicitly DEPRECATED header ("No code should read this file") | `tests/test_field_contract_agreement.py` (routing field reads only) | **partial:** legacy copy is still the *only* place `prd`/`issue_list`/`agent_brief`/`code_patch` schema exists (see B4) | canonical file top comment; legacy file lines 1-13 | DEMONSTRATED | SLOW |
| A5 | Canonical *structure* (sections) of `repository_sensemaking_brief` | `scripts/brief_skeleton.py` — named "canonical brief-structure authority"; `reconcile()` splices model content only into pre-declared holes, discards the rest | referenced by `validate-brief.py`, `weakness_type_safeguard` | aligned | runner-retirement-plan Step-4 table | DEMONSTRATED | SLOW |
| A6 | Which `workflow-registry.yaml` is authoritative | **UNDECIDED.** Packaged `src/sensemaking_skills/registry.py` loads `src/sensemaking_skills/defaults/…`; tests + `scripts/workflow-runtime.py` treat `skills/workflow-planner/references/…` as "the runtime-loaded registry". No file declares canonical; equality contract deliberately not written | only `tests/test_auto_invoke_registry_agreement.py`, and only for the `auto_invoke` subset | copies **have drifted** (see B3) | `enforcement-contract.md` §6 ("first establish which representation is canonical… Until the contract says what equality means, CI cannot decide it") | DEMONSTRATED | MEDIUM |
| A7 | Product version | `0.2.2` agrees across `package.json`, `pyproject.toml`, `src/sensemaking_skills/__init__.py` | probe emits `conflicting_values` as **evidence-only, never blocking** — "which declaration is authoritative … policy decision not yet made" | `tests/test_cli.py::test_cli_version` asserts an *older* string → deterministically RED on main (known-wrong assertion, repair is a separate decision) | `enforcement-contract.md` §4, §5 | DEMONSTRATED | MEDIUM |
| A8 | Product scope | ADR 0014 (ACCEPTED, owner-ratified 2026-07-26, interpretation A): a human-reviewed repository-analysis assistant producing an evidence-grounded brief. Routing, tracker-sync, deployment **out of scope**. ADR + `CONTEXT.md` win | owner decision package `docs/OWNER-DECISION-PACKAGE-2026-07-26.md` | **policy-vs-memory conflict:** user auto-memory / `docs/PHASE-4-5-PRODUCTION-GATE` say "PRODUCTION READY — APPROVED FOR DEPLOYMENT"; `CONTEXT.md` + `STATUS.md` say GA not claimed, Goal A episodes not run | ADR 0014 header; `STATUS.md:12-24` | DEMONSTRATED | MEDIUM |
| A9 | Execution model / control-loop ownership | ADR 0013 (Accepted, *ratified* 2026-08-13): the active coding agent is the runtime; `workflow-runtime.py` / `skill_executor.py` are a separate automation/compat path, *not* the semantic definition of Skill execution | amendment prose; retirement plan | aligned | ADR 0013 amendment (2026-08-13) | DEMONSTRATED | SLOW |
| A10 | Downstream routing / execution authority | No artifact field, recommendation, or registry boolean grants execution authority. `recommended_workflow_id`, `primary_fog_type`, `auto_invoke_next_workflow` are recommendation / compatibility metadata only | ADR 0026 (Accepted, merged PR #235); `tests/test_auto_invoke_authority_gating.py` | ADR 0005 & 0012 (still "Accepted") describe the *opposite* mechanism — see C1 | ADR 0026 header; `CONTEXT.md` L93; `decision-orchestration-boundary.md` guardrail 2 | DEMONSTRATED | SLOW |
| A11 | `MODEL_WARRANT` / `representation_sufficiency` | `CONTEXT.md` "MODEL_WARRANT authority (canonical; ADR 0015 addendum)": producer supplies `representation_sufficiency`, mapped deterministically (sufficient→NO, insufficient_bounded→PARTIAL, else→INCONCLUSIVE); INCONCLUSIVE gates routing / materialization / NO_CHANGE | `scripts/workflow-runtime.py::_run_seam_warrant`; several `tests/test_warrant_*.py` | **policy = canonical, runtime = opt-in:** `workflow-runtime.py:226` `warrant_enabled: bool = False` — the gate is off unless explicitly enabled | `CONTEXT.md` MODEL_WARRANT section; `workflow-runtime.py:226,294,1450` | INTERPRETIVE | MEDIUM |
| A12 | Which CI findings may block a merge | `scripts/gate_relationship_findings.py` is the **only** place that decides. Promotion rule: mechanically decidable AND `requires_semantic_review: False`. Current blocking set = `missing_reference`, `missing_status_line` only. Semantic interpretation stays in `repo-sensemaker` | `tests/test_gate_relationship_findings.py` | this whole gate lives on unmerged branch `feat/enforcement-gate` (see B1) | `enforcement-contract.md` §4 | DEMONSTRATED | SLOW |

---

## 2. Enforcement mismatches

| # | Contract | Enforcement reality | Evidence | Grade | Rate |
|---|---|---|---|---|---|
| B1 | Repo has extensive verification machinery (Probe Engine, ~large pytest class) | The CI `validate` job **runs no pytest at all**; Probe Engine, relationship probes, `test_path_drift`, `test_field_contract_agreement`, `test_cli` etc. run in **no** CI step. The `probe-gate` + `core-assertions` jobs that fix this exist only on branch `feat/enforcement-gate` (based on `main@08f091b`), merge "awaiting separate authorization" | `enforcement-contract.md` §1-3, header | DEMONSTRATED | MEDIUM |
| B2 | Canonical-vocabulary coverage + canonical gate names | `tests/test_path_drift.py` deterministically **RED on main**: 5 failures — vocab coverage gaps (workflows, artifacts), non-canonical gate names `review_findings` / `review_recommendation` in the workflow registry, fog-type naming inconsistency in docs. Repair is a separate un-taken decision | `enforcement-contract.md` §5 | DEMONSTRATED | MEDIUM |
| B3 | Two `workflow-registry.yaml` copies must agree | Only `tests/test_auto_invoke_registry_agreement.py` enforces agreement, and only on the *`auto_invoke` subset*. Full diff shows real drift: the `skills/…` copy contains an `artifact-reconciliation` workflow, `prior_evidence` inputs, and a `repair-verifier` step that the packaged `src/…/defaults/` copy lacks. No full-equality check exists (contract undefined) | `diff` of the two files; `test_auto_invoke_registry_agreement.py` docstring; `enforcement-contract.md` §6 | DEMONSTRATED | MEDIUM |
| B4 | Every artifact type has a schema in the canonical contracts file | `prd`, `issue_list`, `agent_brief`, `code_patch` `required_sections`/`required_machine_fields` exist **only** in the DEPRECATED `workflow-orchestrator/references/artifact-contracts.yaml`; port to canonical never done; `tests/test_artifact_contracts_pm_engineering.py` marks 5 tests `xfail` to encode the gap. Legacy file still read by `test_path_drift.py`, `test_skill_hygiene_canonical_wiring.py` | legacy file lines 1-13; xfail test lines 15-29 | DEMONSTRATED | SLOW |
| B5 | Producer/consumer field-name agreement | `tests/test_field_contract_agreement.py` enforces it — but is **deliberately excluded** from the `core-assertions` CI gate ("needs the full SDK dependency set… a future promotion") | `enforcement-contract.md` §3 | DEMONSTRATED | MEDIUM |
| B6 | `weakness_type` is a controlled-vocabulary deterministic field | Owner-ratified (ADR 0015 D2-D4) as **required metadata but non-blocking**; enum includes `Other`+explanation; historically enforced only by substring match against free prose (`scripts/validate-brief.py:279-286`), the exact prose-brittle pattern the ADR warns against | ADR 0015 addendum | DEMONSTRATED | SLOW |
| B7 | Vendored/installed skill copies mirror the repo skills | `distribution-drift.yaml`: 15 checked, 10 synced, **5 with `line_ending_only` drift** (hash mismatch, 0 content drift) — `docs-aligner`, `sensemaking-docs-reconciler`, `setup-sensemaking-skills`, `to-issues`, `to-prd`. `--sync` flag exists; `STATUS.md` claims global skills now synchronized | `distribution-drift.yaml`; `STATUS.md` "Current state" | DEMONSTRATED | FAST |
| B8 | Gate A: no provider invocation without a digest-bound owner authorization record | ADR 0022 is **PROPOSED**; the authorization contract was ratified (PR #107) "specified but unenforced"; `scripts/gate_a_authorization.py` now implements it; canonical Evidence 0016 remains `PREPARED_NOT_RUN`. ADR 0023 (two-lane, Accepted) is governance/schema only — "No runtime component reads, validates, or enforces anything defined here yet" | ADR 0022 header; ADR 0023 §1, §2 | DEMONSTRATED | MEDIUM |

---

## 3. Lifecycle / supersession

| # | Item still physically present | Authority state | Evidence | Grade | Rate |
|---|---|---|---|---|---|
| C1 | ADR 0005 & ADR 0012 | Both **still `Status: Accepted`**, but their core mechanism ("orchestrator chains skills automatically" / `auto_invoke_next_workflow` as authority) is superseded *in effect* by ADR 0013/0014/0026 + `CONTEXT.md` + boundary doc. ADR 0026 says so explicitly; 0005/0012 status lines were never updated | ADR 0026 "Depends on" note re 0005; ADR 0005:6,59; ADR 0012:90-93 | DEMONSTRATED | SLOW |
| C2 | `auto_invoke_next_workflow` runtime path | Superseded decision, **implementation still runs**: consumed by `src/sensemaking_skills/runner.py`, `registry.py`, `scripts/workflow-runtime.py`; mirrored across both registry copies. ADR 0026 keeps it as "compatibility / historical transition metadata", NOT execution authority | ADR 0026 §1; grep of consumers | DEMONSTRATED | SLOW |
| C3 | ADRs 0017, 0018, 0019, 0020, 0021 | **SUPERSEDED — "historical proposal, never Accepted"** (dispositioned 2026-08-18). 0021 ("production readiness requirements") is the one whose supersession makes the "PRODUCTION READY" memory (A8) stale | grep of `**Status**` lines; ADR 0017/0018 disposition sections | DEMONSTRATED | SLOW |
| C4 | ADRs 0006, 0007, 0008, 0022 | **Proposed**, never Accepted; partial implementation exists anyway (`scripts/gate_a_authorization.py` implements 0022; routing-divergence audit fields from 0008 appear in `SKILL.md`) | `**Status**` grep | DEMONSTRATED | SLOW |
| C5 | `src/sensemaking_skills/reasoning/` | Experimental research vertical slice living **inside the product package**. Its own `__init__.py`: "NOT the production orchestrator path; production-runtime integration is deferred. See `experiments/product-hypothesis-b/implementation/…`". Yet it *is* imported by `scripts/workflow-runtime.py` and `scripts/validate-brief.py` via the `warrant_gate` "production-seam" wrapper | `reasoning/__init__.py:1-6`; `warrant_gate.py:1-19`; import grep | DEMONSTRATED | MEDIUM |
| C6 | `scripts/workflow-runtime.py`, `scripts/skill_executor.py` | Programmatic **model-invocation** responsibility retired (ADR 0013; retirement-plan Steps 5-7 "collapsed into one atomic cut", executed 2026-08-13 — SDK/API executors, CI `claude-agent-sdk` installs, 14 test files removed). The **deterministic infra kept** (path resolution, validation, gates, planning, sessions). Doc re-scope for `ROUTING_GUIDE`, `run-ledger-guide`, `PORTFOLIO_OPERATIONS`, `PRODUCT-CONTRACT-REVIEW` explicitly **deferred** — still describe the retired runner | retirement-plan Step-5 evidence + "Documentation reconciliation" section | DEMONSTRATED | SLOW |
| C7 | ADR 0024 & ADR 0025 | **ACCEPTED** (owner 2026-08-10 / 2026-08-23) but each header: "Merge to `main` is a separate repository action, pending and not part of this record." 0024's `extended_analysis` fields *are* present in the canonical contract at this commit (so 0024 landed); 0025's `test_generate_plan_conformance.py` is cited as failing on main, issue #232 open as the implementation tracker | ADR 0024/0025 headers; `artifact-contracts.yaml:163-179` | DEMONSTRATED | MEDIUM |
| C8 | Root `run_day3_tests.py` … `run_day5_tests.py`, `test_phase3_poc.py`, `test_phase3_comprehensive.py`, `docs/PHASE-*.md` (~30 files), `docs/archive/` | Historical build scaffolding, marked HISTORICAL / SUPERSEDED, retained deliberately, no current authority. Volume is itself a navigation hazard | file listing; retirement-plan doc-reconciliation buckets | DEMONSTRATED | SLOW |

---

## 4. Research → product / runtime crossings

| # | Crossing | Reaches runtime how | Mode | Evidence | Grade | Rate |
|---|---|---|---|---|---|---|
| D1 | `MODEL_WARRANT` gate (from `experiments/product-hypothesis-b/`) | `sensemaking_skills.reasoning.warrant_gate.run_seam_warrant` called by `workflow-runtime.py::_run_seam_warrant` (~L1450) after brief step; when active, `MODEL_WARRANT == INCONCLUSIVE` blocks routing / representation materialization / NO_CHANGE terminalization | **GUARDED + OPT-IN**: `warrant_enabled=False` default; wrapper never raises, log-and-continue, no evidence mutation, `NO`→no representation | `workflow-runtime.py:226,294,1438-1473,1831-1937`; `reasoning/warrant_gate.py` docstring | DEMONSTRATED | MEDIUM |
| D2 | `extended_analysis` Section 15 brief fields (`domain`, `consequential_boundary`, `uncertainty`, `owner_intent_state`) | Lineage: `prototype/repo-sensemaker-vnext` PR #164 (exploratory, never merged) → `candidate/sensemaking-vnext` → ADR 0024 (ACCEPTED). Declared in canonical `artifact-contracts.yaml`, harvested/spliced by `brief_skeleton.reconcile()`, checked non-blockingly by `validate-brief.py` | **OPTIONAL, model-constrained, non-blocking**; explicitly NOT read by `workflow-runtime.py` routing (`_WORKFLOW_ID_FIELDS`/`_FOG_TYPE_FIELDS`); any routing use needs a new per-field owner decision. A 5th field (`discovery_confidence`) was falsified by the stress-test and removed | ADR 0024 §1; `artifact-contracts.yaml:163-179` | DEMONSTRATED | SLOW |
| D3 | Four-type fog taxonomy (research diagnostic construct) | Emitted into `repository_sensemaking_brief` / `workflow_orchestration_plan` as `primary_fog_type` etc. | **DE-AUTHORIZED crossing**: present as "diagnostic metadata" only; ADR 0018 disposition + ADR 0026 + `CONTEXT.md` state it grants no routing/execution authority | `CONTEXT.md` fog section; ADR 0018 disposition | DEMONSTRATED | SLOW |
| D4 | Two-lane experiment authorization (ADR 0023) | Schema files + `EXP-NNNN` namespace convention present | **NOT YET CROSSED**: "No runtime component reads, validates, or enforces anything defined here yet" — governance-only. Included because the code scaffolding invites the assumption that it is live | ADR 0023 §1 final line, §2 | DEMONSTRATED | MEDIUM |

---

## Expansion procedure for a question this representation does not cover

1. **Locate the authority, not the code.** Grep `docs/adr/` for the concept; read the
   matching ADR *and its `**Status**` line* (Accepted / Proposed / Superseded / "merge
   pending"). Then check `CONTEXT.md`, `docs/decision-orchestration-boundary.md`, and
   `docs/enforcement-contract.md` for a later disposition that overrides it. A superseding
   note frequently lives in a *different, newer* ADR's "Depends on" list, not in the old ADR.
2. **Separate declared from enforced.** For any contract, find the enforcer
   (`tests/test_*`, `scripts/validate-*.py`, `scripts/gate_*.py`) and confirm it (a) exists
   and (b) runs in `.github/workflows/validation.yml` on `main` — many named tests do not.
   If it does not run in CI, treat the contract as advisory.
3. **Check for a second copy.** Registries/contracts here are duplicated
   (`skills/…/references/` vs `src/sensemaking_skills/defaults/` vs
   `workflow-orchestrator/references/`). `diff` the copies; determine which the runtime
   actually loads (`registry.py::_load_package_defaults`, `workflow-runtime.py` loader);
   if no file declares canonical, that is the answer — it is undecided.
4. **Check research lineage.** If the concept name appears under `experiments/` or
   `docs/research/`, trace whether anything in `scripts/` or `src/sensemaking_skills/`
   imports it, and whether the call is default-on, opt-in (`*_enabled=False`), or guarded
   (try/except log-and-continue).
5. **Stop** when you can name: the defining source, the enforcing mechanism (or its
   absence), the winning side of any conflict, and the lifecycle state. Do not enumerate
   call graphs or module inventories — those are ordinary inspection and were excluded here.

---

## Include / exclude calls I was unsure about

- **Probe Engine → `repo-sensemaker` feed** (`scripts/probe-repo.py`): a genuine
  research-origin component feeding the product, but it is default, load-bearing, and
  cheaply visible from `CONTEXT.md`'s own evidence-model section — excluded as ordinary
  architecture; only its semantic rule ("a probe that cannot evaluate a fact is not
  evidence of absence") is authority-like, and that is already in `CONTEXT.md`.
- **Row D4 (two-lane not-yet-crossed)**: strictly a *non*-crossing, but included because
  the presence of `EXP-NNNN` schema scaffolding actively misleads a reader into thinking
  it is enforced.
- **`docs/research/` agenda contents** (`C6R`, warrant-as-primitive, domain-general
  transfer): excluded — explicitly "research hypotheses only, not an ADR, not a roadmap
  commitment"; nothing crosses to runtime, so they fail the consequential-to-decisions test.
- **Per-ADR PR/commit boundary citations**: kept only where an ADR's own text names the
  commit/PR (0013, 0023, 0026); I did not independently replay history to verify each.
- **`CHANGELOG.md` / `roadmap.md` / `STATUS.md` drift**: `STATUS.md` is current and used
  as evidence (A8); `roadmap.md` and the many root PHASE files were folded into C8 rather
  than given rows, to keep length down.
