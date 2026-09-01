# Domain Alignment Report

## 1. Repository Analyzed
- **Path**: `H:\GithubRepositories\sensemaking-skills`
- **Description**: Agent-native engineering sensemaking and control layer for software-engineering agents. Active agent owns recursive control loop selecting warranted responsibilities (ADR 0013); Sensemaking constrains via evidence, bounded Skills, durable artifacts, validators, reconciliation, and authority boundaries. Validated product scope is `repository_sensemaking_brief` (ADR 0014); automatic fog-type-to-implementation routing is compatibility machinery, not ratified behavior.
- **CONTEXT.md**: `CONTEXT.md:1-362` | **ADRs**: `docs/adr/0001-0026` (26) | **Canonical vocab**: `docs/canonical-vocabulary.yaml:1-801` vs `src/sensemaking_skills/defaults/canonical-vocabulary.yaml`

## 2. Contradictions

### C1 — Source-of-truth map phantom path `skill-registry.yaml`
- **Term**: `Source-of-truth map`
- **Claim**: `CONTEXT.md:316-319` lists `| skill-registry.yaml | registered Skill/capability catalog |`
- **Reality**: Root file does not exist; catalog lives at `skills/workflow-planner/references/skill-registry.yaml:1` (package copy at `src/sensemaking_skills/defaults/skill-registry.yaml`)
- **Evidence**: `CONTEXT.md:319`; `Test-Path skill-registry.yaml` => False; `skills/workflow-planner/references/skill-registry.yaml:1`; `src/sensemaking_skills/config.py:32`
- **Resolution**: Update docs — FIXED this run: `CONTEXT.md:319` now points to `skills/workflow-planner/references/skill-registry.yaml`. Add CI drift check.

### C2 — Canonical vocabulary dual-copy drift (load-bearing)
- **Term**: `canonical-vocabulary`
- **Claim**: `docs/canonical-vocabulary.yaml:1-3` is authoritative; `CONTEXT.md:316` and `src/sensemaking_skills/validation.py:44` claim single truth, but validators load stale package defaults
- **Reality**: `docs/canonical-vocabulary.yaml` (801 lines) vs `src/sensemaking_skills/defaults/canonical-vocabulary.yaml` (717 lines) diverge; docs adds 5 gates (`review_audit_diagnosis:150`, `review_reconciliation:319`, `review_reconciliation_verified:324`, `review_findings:371`, `review_recommendation:381`), 5 artifact_ids (`work_claim`, `reconciliation_report`, `repair_verification_report`, `architectural_review_recommendation`, `proposed_direction` at `docs/canonical-vocabulary.yaml:421-661`), and `yolo_execution` flags (`compatibility_only:true` at `docs/canonical-vocabulary.yaml:418-419` absent in defaults)
- **Evidence**: `docs/canonical-vocabulary.yaml:150-419,421-661`; `src/sensemaking_skills/defaults/canonical-vocabulary.yaml:360-386`; `src/sensemaking_skills/validation.py:44`
- **Resolution**: Update code — regenerate `src/.../defaults/*` from `docs/` canonical source at build; add CI hash check (as flagged in ADR 0026:157-158).

### C3 — Skill registry ghost/deprecated consumers
- **Term**: `Skill` responsibilities
- **Claim**: `CONTEXT.md:126-134` lists 8 representative Skills as operational product
- **Reality**: `skills/workflow-planner/references/skill-registry.yaml:80-93` declares 44 entries; `triage:80-85` is `status: proposed` (STILL-PROPOSED, not implemented), `tdd:87-92` is `HISTORICAL/DEPRECATED`; `Test-Path skills/triage` and `skills/tdd` are False (only 17 dirs under `skills/`). Yet 7 workflows consume ghosts: `implementation-workflow:679-713`, `product-implementation-workflow:723-792`, `ui-implementation-workflow:831-893` sequence `triage->tdd`
- **Evidence**: `CONTEXT.md:126-134`; `skills/workflow-planner/references/skill-registry.yaml:80-93, 679-713`; `skills/workflow-planner/references/workflow-registry.yaml:665-721`; `skills/docs-aligner/SKILL.md` lists no `triage/tdd` implementation
- **Resolution**: Update docs — clarify operational set vs deprecated/proposed; or retire workflows that depend on unimplemented Skills.

### C4 — `yolo_execution` retired in docs, default in code
- **Term**: `execution_modes.yolo_execution`
- **Claim**: `docs/canonical-vocabulary.yaml:418-419` marks `yolo_execution` `compatibility_only:true` `status_note: Legacy compatibility mode retained (retired runner, ADR 0013)`; `CONTEXT.md:309` treats it as compatibility
- **Reality**: `src/sensemaking_skills/runner.py:72` defaults `execution_mode="yolo_execution"`; `runner.py:337` parent-session run uses `yolo_execution`; 6 workflows list `yolo_execution` as allowed (`full-local-sensemaking:496`, `fast-local-diagnostic:569`, `product-to-issues:302`)
- **Evidence**: `docs/canonical-vocabulary.yaml:413-419`; `src/sensemaking_skills/runner.py:72,337`; `skills/workflow-planner/references/workflow-registry.yaml:496,569`
- **Resolution**: Update code or docs — either ratify `yolo_execution` for local-first tooling or change `runner.py` default to `guided_execution`/`plan_only` and prune `allowed_execution_modes`.

### C5 — MODEL_WARRANT seam not wired to core package
- **Term**: `MODEL_WARRANT` / `representation_sufficiency`
- **Claim**: `CONTEXT.md:165-177` canonical addendum (ADR 0015) says `representation_sufficiency` is sole authority for `MODEL_WARRANT` (`sufficient->NO`, `insufficient_bounded->PARTIAL`, else `INCONCLUSIVE`), probes diagnostic, INCONCLUSIVE gates materialization/routing/NO_CHANGE
- **Reality**: `grep src/sensemaking_skills/*.py` (excluding `reasoning/`) yields 0 hits for `MODEL_WARRANT`/`representation_sufficiency`; implementation lives only in `src/sensemaking_skills/reasoning/evidence_probes.py:93-207`, `warrant_gate.py:76-89,109-114`, `vertical_slice.py:281-325` flagged as bounded/experimental slice; `registry.py:131-169` and `runner.py:208-289` never consult warrant before surfacing `recommended_workflow_id`
- **Evidence**: `CONTEXT.md:165-177`; `src/sensemaking_skills/reasoning/warrant_gate.py:11-16,76-89`; `src/sensemaking_skills/reasoning/evidence_probes.py:194-207`; `src/sensemaking_skills/registry.py:131`
- **Resolution**: Update docs — note `MODEL_WARRANT` lives in `sensemaking_skills.reasoning` experimental seam until wired into `scripts/workflow-runtime.py` / `runner.py`; prevent inference of `NO_CHANGE` from warrant alone.

### C6 — `workflow_orchestration_plan` REQUIRED vs provisional lifecycle
- **Term**: `workflow_orchestration_plan`
- **Claim**: `skills/workflow-planner/references/artifact-contracts.yaml:484-490` requires `primary_fog_type`, `chosen_workflow_id`, `workflow_steps`, `created_at`; `CONTEXT.md:213` calls plan optional planning artifact
- **Reality**: `docs/adr/0025-workflow-orchestration-plan-lifecycle.md:86-113` ratifies two-stage lifecycle: provisional skeleton before brief exists may omit `primary_fog_type`/`workflow_steps`/`created_at` with `plan_stage: provisional`; `artifact-contracts.yaml:514` note admits provisional may omit those fields. Required list contradicts lifecycle note and `scripts/workflow-runtime.py:2564-2568` pre-brief generation path
- **Evidence**: `artifact-contracts.yaml:484-514`; `docs/adr/0025-workflow-orchestration-plan-lifecycle.md:86-113`
- **Resolution**: Update docs/code — split contract into `provisional` vs `final` or move `primary_fog_type`/`workflow_steps`/`created_at` to conditional `recommended_machine_fields` with selector on `plan_stage`.

## 3. Fuzzy Language

### F1 — `workflow`
- **Term**: `workflow`
- **Current Usage**: Registry definition (`workflow-registry.yaml:1` 18 workflow_ids); diagnostic recommendation (`recommended_workflow_id` in `artifact-contracts.yaml:145-150`, `repo-sensemaker/SKILL.md:239-244`); selection audit (`chosen_workflow_id` vs `system_recommended_workflow` in `workflow-planner/SKILL.md:85-96`); planning artifact (`workflow_orchestration_plan` provisional vs finalized per ADR 0025); execution noun (`runner.py`, `workflow-runtime.py` invocation)
- **Proposed Canonical Term**: `workflow-definition`, `workflow-recommendation` (=`recommended_workflow_id`), `workflow-selection` (=`chosen_workflow_id`/`selected_workflow`), `workflow-execution` (runtime invocation), `workflow-orchestration-plan` artifact
- **_Avoid_**: Bare `workflow`, `next workflow`, `recommended workflow` without qualifier
- **Evidence**: `CONTEXT.md:142-144,161`; `skills/workflow-planner/references/workflow-registry.yaml:45,100,502,752`; `src/sensemaking_skills/registry.py:131-169`

### F2 — `validation` vs `reconciliation` vs `verification`
- **Term**: `validation/reconciliation/verification`
- **Current Usage**: `validation` = deterministic contract check (`CONTEXT.md:223-229`, `src/sensemaking_skills/validation.py:189-243`, `scripts/validate-brief.py`); `reconciliation` = claim vs evidence (`CONTEXT.md:231-235`, `skills/output-reconciler/SKILL.md:34` `verified|disputed|omitted`) and docs drift (`sensemaking-docs-reconciler/SKILL.md`); `verification` = finding-specific closure (`CONTEXT.md:237-242`, `skills/repair-verifier/SKILL.md` `closed|remaining`) conflated with campaign fail-closed `src/campaign_validation/validators.py:1`
- **Proposed Canonical Term**: `mechanical-validation`, `claim-reconciliation` (`work_claim`→`reconciliation_report`), `finding-repair-verification` (brief finding→`repair_verification_report` via fresh probe)
- **_Avoid_**: `verification` alone, `validate the reconciliation`, `verification of the brief`
- **Evidence**: `CONTEXT.md:241` `implemented != validated != reconciled != repair-verified`; `skills/output-reconciler/SKILL.md:19-34`; `src/sensemaking_skills/exploratory_execution/artifact_validator.py:42-79`

### F3 — `responsibility` vs `Skill` vs `workflow` vs `capability`
- **Term**: `responsibility/Skill/workflow/capability`
- **Current Usage**: `responsibility` = warranted class of work (`CONTEXT.md:328-331`, `skills/using-sensemaking/SKILL.md:151-169`); `Skill` = bounded implementation with `SKILL.md`+contract (`CONTEXT.md:123-124`, `src/sensemaking_skills/skills/base.py`); `workflow` = YAML subgraph sequencing Skills (`CONTEXT.md:143`); `capability`/`execution` used interchangeably in `docs/decision-orchestration-boundary.md:47-66`, `runner.py`
- **Proposed Canonical Term**: `warranted-responsibility`, `Skill` (capital S), `registered-workflow` (YAML), `execution-runtime` (`scripts/workflow-runtime.py`+`runner.py`)
- **_Avoid_**: `capability`, `responsibility workflow`, `skill workflow`, `orchestration` for post-selection work
- **Evidence**: `CONTEXT.md:122-144`; `skills/workflow-planner/references/skill-registry.yaml:7-291`

### F4 — `probe` vs `evidence` vs `observation`
- **Term**: `probe/evidence`
- **Current Usage**: `probe` = bounded empirical observation (`CONTEXT.md:336`, `skills/repo-sensemaker/SKILL.md:107-141` local probe engine vs `github_connector_exact_sha_v1`); umbrella `evidence` collapses `direct evidence | derived evidence | interpretation | hypothesis` (`CONTEXT.md:181-200`) while `repo-sensemaker/SKILL.md:90-104` mixes `file:lines`, `probe-report.yaml:field`, `relationships.findings` as "evidence"
- **Proposed Canonical Term**: `state-currency probe`→`probe-evidence`, `repository-evidence`, `derived-evidence`, `state-currency-check`
- **_Avoid_**: Unqualified `evidence`, `probe verification`
- **Evidence**: `CONTEXT.md:181-202,336`; `src/sensemaking_skills/reasoning/evidence_probes.py:38-63,111-207`

### F5 — `gate` vs `approval` vs `mode`
- **Term**: `gate/approval/mode`
- **Current Usage**: 50 `gate_id`s with alternates (`review_unknowns` vs `review_unknowns_map` in `docs/canonical-vocabulary.yaml:149-389`); 5 `execution_modes` where `yolo_execution` is `compatibility_only:true` (`docs/canonical-vocabulary.yaml:390-419`) but `runner.py:72` defaults to it; `workflow-planner/SKILL.md:110` says default `plan_only` while vocab says `guided_execution default:true`
- **Proposed Canonical Term**: `gate-id` (canonical, delete alternates), `execution-mode` (`plan_only|prompt_chain|guided_execution|autonomous_execution|yolo_execution` compatibility-only), `gate-outcome` (`approved|denied|needs_revision|none`)
- **_Avoid_**: `gate` for mode, `approval` for warrant, `yolo` for autonomous
- **Evidence**: `docs/canonical-vocabulary.yaml:149-419`; `skills/workflow-planner/references/execution-modes.md:1-40`

## 4. Undocumented Concepts

### U1 — MODEL_WARRANT
- **Concept**: `MODEL_WARRANT`
- **Definition**: Deterministic task-relative gate (`NO|PARTIAL|INCONCLUSIVE`, `FULL` deferred) computed from authoritative `representation_sufficiency`; diagnostic probes are telemetry only.
- **Where Found**: `src/sensemaking_skills/reasoning/vertical_slice.py:194` `Warrant` enum; `src/sensemaking_skills/reasoning/evidence_probes.py:194-207` authoritative mapping; `src/sensemaking_skills/reasoning/warrant_gate.py:76-89` seam wrapper; `CONTEXT.md:165-177` addendum describes but glossary omitted until this run
- **Relationships**: Derived from `Representation Sufficiency`; drives `Warrant Gate`; orthogonal to `NO_REPOSITORY_CHANGE_WARRANTED`; gates PARTIAL materialization

### U2 — Representation Sufficiency
- **Concept**: `representation_sufficiency`
- **Definition**: Producer-authored assessment `{status, rationale, needed_representation}` that is the sole authority for `MODEL_WARRANT`.
- **Where Found**: `src/sensemaking_skills/reasoning/evidence_probes.py:93-101,136-142,194-207`; `skills/repo-sensemaker/SKILL.md:143-170`; `skills/workflow-planner/references/artifact-contracts.yaml:150-157`
- **Relationships**: Input to `derive_probes`/`probes_to_warrant`; `PARTIAL` requires non-empty `rationale`+`needed_representation`

### U3 — NO_REPOSITORY_CHANGE_WARRANTED
- **Concept**: `NO_REPOSITORY_CHANGE_WARRANTED`
- **Definition**: Affirmative terminal outcome that no repository change is warranted; mutually exclusive with any `recommended_workflow_id`.
- **Where Found**: `src/sensemaking_skills/reasoning/vertical_slice.py:30-32,414-431`; `skills/repo-sensemaker/SKILL.md:248-261`; `src/sensemaking_skills/reasoning/warrant_gate.py:109-114`
- **Relationships**: Orthogonal to `MODEL_WARRANT` (`CONTEXT.md:172-174`, `warrant_gate.py:109-114`)

### U4 — State-Currency Probe & Probe Report
- **Concept**: `State-Currency Probe`
- **Definition**: Deterministic current-state measurement (`verification_gap.vg`, `context_entropy.ce`, `fixtures_coverage`) that outranks documented claims; failure is `unmeasured` not clean.
- **Where Found**: `skills/repo-sensemaker/SKILL.md:109-142`; `skills/repo-sensemaker/references/evidence-rules.md:9-12`; `scripts/probe-repo.py`; `src/sensemaking_skills/exploratory_execution/artifact_validator.py:77-79` requires `--probe-report` path
- **Relationships**: Cited as `probe-report.yaml:verification_gap.vg` in `evidence_excerpts`; validator fails closed when unmeasured

### U5 — Gate & Execution Mode Typology
- **Concept**: `Gate` / `Execution Mode`
- **Definition**: ~50 `gate_id`s (`review_repository_brief`, `review_workflow_plan`, `none` sentinel) with `allowed_outcomes [approved,denied,needs_revision]` and 5 `execution_modes` (`plan_only`, `prompt_chain`, `guided_execution` default, `autonomous_execution`, `yolo_execution` compatibility-only) governing `gates_honored`.
- **Where Found**: `docs/canonical-vocabulary.yaml:149-419`; `skills/workflow-planner/SKILL.md:12-45`; `skills/workflow-planner/references/execution-modes.md`
- **Relationships**: `gates_honored` flag per mode; `auto-approval` criteria `validation_passed and no_severity_warnings`

### U6 — Weakness Type Taxonomy
- **Concept**: `Weakness Type`
- **Definition**: Closed vocabulary for weakest-boundary shape: `Vocabulary Drift`, `Contract Mismatch`, `Ghost Features`, `Safety Gaps`, `Implicit Dependencies`, `Zero Validation`, `Orphaned Examples`, or `Other` with explanation.
- **Where Found**: `skills/repo-sensemaker/references/weakness-types.md:1-11`; `skills/repo-sensemaker/SKILL.md:92-93`; `src/sensemaking_skills/exploratory_execution/artifact_validator.py:57-72`; `skills/workflow-planner/references/artifact-contracts.yaml:143-144,178`
- **Relationships**: Must agree between brief Section 6 prose `**Weakness type:**` and Section 13 `weakness_type` machine field

## 5. ADR Candidates
All three ADR conditions were tested per candidate (hard to reverse + surprising without context + real trade-off). None met all three as warranting a new ADR file in this autonomous `gate:none` pass; candidates are logged for owner triage.

### AC1 — Two-Lane YAML Profile v1 strictness
- **Decision**: Layer A token reject (anchors/aliases/tags/multi-doc) + Layer B stripped implicit resolvers with custom JSON-number grammar and key regex `^[a-z][a-z0-9_]*$`
- **Evidence**: `src/sensemaking_skills/campaign_validation/yaml_profile.py:77-284`
- **Alternatives**: `yaml.safe_load` YAML 1.1, JSON-only, StrictYAML
- **Reversibility**: Hard — source-form legality for every digest-bearing artifact; relaxing re-opens malleability
- **ADR Status**: `not_created` — already traceable to ADR 0023 §10b; incremental grammar refinement is an addendum to ADR 0023, not a new ADR in this domain-alignment pass

### AC2 — Validator-owned sealed dataclasses (closure sentinel provenance)
- **Decision**: `CampaignPolicy/Approval/ConfigurationIdentity/AttemptReservation/ExploratoryInvocationCapability` private construction via `object.__new__` + closure sentinel `is` check
- **Evidence**: `src/sensemaking_skills/campaign_validation/models.py:112-138`; `src/sensemaking_skills/exploratory_authorization/models.py:142-165`
- **Alternatives**: Bare `isinstance` checks, cryptographic signatures, process boundary only
- **Reversibility**: Hard — downstream `is_genuine_*` gates trust
- **ADR Status**: `not_created` — exploratory campaign plane is `optional` per `CONTEXT.md:294-295` (not core CLI surface); documenting now would broaden product scope without owner ratification

### AC3 — Append-only hash-chained ledger + concurrency ceiling 1
- **Decision**: `experiments/campaigns/<campaign_id>/ledger.jsonl` with `GENESIS_HASH`, JCS SHA-256 chain, cross-process lock, `concurrency_ceiling = min(declared,1)`
- **Evidence**: `src/sensemaking_skills/campaign_accounting/ledger.py:33-180`; `src/sensemaking_skills/campaign_accounting/reservation.py:238-244`
- **Alternatives**: SQLite, git commits, in-memory accounting
- **Reversibility**: Very hard — source of truth for budget/recovery
- **ADR Status**: `not_created` — Phase 4 campaign accounting is not part of ratified Goal A product boundary (`CONTEXT.md:60-69`); new ADR would require owner authorization

### AC4 — Shared lexical+physical path containment anchored to `framework_root`
- **Decision**: Single `path_containment.py` reused by Gate A and campaign_validation; `anchor_output_path` interprets relatives as `framework_root/value` never `os.getcwd()`; `resolve_containment` finds nearest ancestor via `lexists`+`resolve(strict=False)` and fails closed on symlink/colon/alias
- **Evidence**: `src/sensemaking_skills/path_containment.py:225-369`; `src/sensemaking_skills/campaign_validation/fs_adapter.py:38-82`
- **Alternatives**: `Path.resolve()`+prefix check, per-caller containment, OS sandbox
- **Reversibility**: Hard — security boundary bypass re-introduced by naive `Path(value)` against CWD
- **ADR Status**: `not_created` — represents hardening already pressured and characterized by `tests/test_path_containment_extraction_characterization.py`; track as decision log rather than new ADR until Cross-context reuse is ratified

## 6. Glossary Mutations
| Action | Term | Before | After | Section |
|---|---|---|---|---|
| `updated` | `Workflow` | `a registered, mechanically expressible sequence/subgraph; not automatically the top-level control loop` | Qualified forms: `workflow-definition` / `workflow-recommendation` / `workflow-selection` / `workflow-execution`; bare `workflow` flagged ambiguous | `## Domain language` |
| `updated` | `Warrant` | `the current justification for a responsibility, claim, or action from evidence + unresolved uncertainty + authority` | Added disambiguation: distinct from `MODEL_WARRANT` (system gate) and `gate-approval` | `## Domain language` |
| `updated` | `Probe` | `bounded empirical observation used when repository text alone cannot establish reality` | Qualified: `state-currency probe`→`probe-evidence` vs `repository-evidence` vs `derived-evidence`; never infer FALSE from absence | `## Domain language` |
| `updated` | `Validation/Reconciliation/Repair verification` | Three bare terms | Sharpened to `mechanical-validation`, `claim-reconciliation`, `finding-repair-verification` with artifact mappings | `## Domain language` |
| `updated` | `Orchestration Plan` | `optional procedural planning artifact; recommendation, not authority` | Added `provisional` vs `canonical` lifecycle per ADR 0025 | `## Domain language` |
| `added` | `MODEL_WARRANT` | — | `deterministic task-relative gate (NO|PARTIAL|INCONCLUSIVE; FULL deferred) computed from authoritative representation_sufficiency; probes are telemetry only` | `## Domain language` |
| `added` | `Representation Sufficiency` | — | `producer-authored judgment {status, rationale, needed_representation} sole authority for MODEL_WARRANT` | `## Domain language` |
| `added` | `NO_REPOSITORY_CHANGE_WARRANTED` | — | `affirmative terminal outcome: no repository change warranted; exclusive with recommended_workflow_id; orthogonal to MODEL_WARRANT` | `## Domain language` |
| `added` | `Weakness Type` | — | `closed taxonomy for weakest-boundary shape (7 types + Other with explanation)` | `## Domain language` |
| `added` | `Extended Analysis` | — | `optional Section 15 multi-fog disclosure (domain, consequential_boundary, uncertainty, owner_intent_state); routing-inert, non-blocking` | `## Domain language` |
| `added` | `Gate` | — | `human approval checkpoint (gate_id) with outcomes approved|denied|needs_revision|none; sentinel none means no gate` | `## Domain language` |
| `added` | `Execution Mode` | — | `plan_only|prompt_chain|guided_execution(default)|autonomous_execution|yolo_execution(compatibility-only)` | `## Domain language` |

Also: Source-of-truth map fix — `CONTEXT.md:319` `skill-registry.yaml` → `skills/workflow-planner/references/skill-registry.yaml`.

## 7. ADRs Created
None. All ADR-eligible candidates either belong to exploratory campaign plane (optional, not Goal A product scope per `CONTEXT.md:60-69,294-295`) or are incremental addenda to existing ADRs (0023 §10, 0025, 0026). Per ADR Eligibility (hard to reverse + surprising + real trade-off), creating ADRs in a `gate:none` autonomous step without owner authorization would expand scope; candidates are logged in §5 for owner triage via `sensemaking-docs-reconciler` or explicit ADR session.

## 8. Summary
- Contradictions found: 6
- Fuzzy terms sharpened: 5
- Undocumented concepts discovered: 6
- ADRs created: 0
- Glossary entries added: 7
- Glossary entries updated: 5
- Source-of-truth path fixes: 1
