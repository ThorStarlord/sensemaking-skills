# 04 — ARTIFACT FLOWS (DETAILED_REPOSITORY_ARCHITECTURE_PROTOTYPE_V0)

Per durable artifact: **who produces it, who consumes it, who validates it, who
transforms/serializes it, what governs its contract.** Source of truth for
producer/consumer/verification: `skills/workflow-planner/references/artifact-contracts.yaml`
(`E-CONTRACT-file`). Source for path *resolution* discipline: ADR 0010
(`E-ADR-0010`). Field-name agreement is enforced by
`tests/test_field_contract_agreement.py` (`E-CLAUDEMD-fields`).

Legend: P=produces, C=consumes, V=validates, X=transforms/serializes,
G=governs contract.

---

## Core sensemaking chain (the ratified product core)

### `user_intent`  (`artifacts/user_intent.md`)
- **P** `workflow-runtime` (contract `produced_by: workflow-runtime`)
- **C** problem-framer, unknowns-mapper, repo-sensemaker, workflow-planner,
  docs-aligner, to-prd, to-issues, triage, handoff  (9 declared consumers —
  the widest fan-out artifact in the repo)
- **V** `validate-artifact.py user_intent` + `validate-user-intent.py`
- **G** artifact-contracts.yaml (required machine fields: artifact_id,
  intent_source, scope_mode, raw_problem_statement, created_at, immutable)
- **X** `user_intent_amendment` (`produced_by: orchestration-runner`) amends it
  via `amends_intent_ref`; `requires_reroute` signals re-planning.
- **Note:** `immutable: true` — amendments are additive, never in-place edits.

### `probe_report`  (`probe-report.yaml`)
- **P / X** `probe-repo.py` -> `repo_probes.probe_all()` (aggregates
  `probe_relationships.py`); serializes YAML; prints 7-line summary; exit 0
  (exit 2 only if repo-root missing)
- **C** repo-sensemaker (MANDATORY before brief synthesis), repair-verifier
  (re-probe for finding closure)
- **V** `validate-probe-report.py`
- **G** ADR 0004 (evidence tracking for trust)
- **Contract-relevant semantics:** a failed/errored observation is **not** an
  observed absence — the probe engine times out rather than raising; "documented
  but not independently verified" is the fallback label (`AGW:131`, `CONTEXT.md:182`).

### `repository_sensemaking_brief`  (`artifacts/repository_sensemaking_brief.md`)
- **P** repo-sensemaker
- **C** workflow-planner, prompt-handoff, sensemaking-docs-reconciler,
  output-reconciler
- **V** `validate-artifact.py repository_sensemaking_brief` (generic: required
  sections `evidence`, `recommended_workflow`; required machine fields
  artifact_id, primary_fog_type, evidence, created_at, immutable)
  **+** `validate-brief.py` (conditional/blocking):
  - `recommended_workflow_id` required for ACTION briefs, **authoritatively
    optional** under EXPLICIT `outcome = NO_REPOSITORY_CHANGE_WARRANTED`
  - `recommended_workflow_id: null` valid **only** with
    `escalation_recommended: true`
  - `collision_dedup_direction` **blocking** when the brief recommends
    renumber/dedup of a colliding ID (evidence-rules Rule 7 / Issue #171)
  - `weakness_type` required-but-non-blocking (D2); `weakness_type_explanation`
    required only when `weakness_type = Other` (D4), non-blocking warning
- **X (opt-in seam)** `workflow-runtime` reads `representation_sufficiency`
  (dict) + `outcome` and computes a `WarrantRecord` (MODEL_WARRANT =
  NO/PARTIAL/INCONCLUSIVE; FULL deferred). Runs ONLY after validator PASS +
  reconciliation, and only when `warrant_enabled` (`E-RT-1438`, `E-RT-routefields`).
- **X (routing read)** `workflow-runtime._WORKFLOW_ID_FIELDS =
  (recommended_workflow_id, chosen_workflow_id, selected_workflow)` and
  `_FOG_TYPE_FIELDS = (primary_fog_type, user_implied_fog_type)` — every one of
  these must be declared in artifact-contracts.yaml (`E-RT-routefields`,
  `E-CLAUDEMD-fields`).
- **G** artifact-contracts.yaml + ADR 0014 (product core) + ADR 0015 addendum
  (`representation_sufficiency` -> MODEL_WARRANT mapping) + ADR 0024 (Section 15
  `extended_analysis` classification) + evidence-rules.md Rule 7.
- **Contract note:** validation results are NOT stored in the artifact — see
  `validators/run_log.md`. PATH B (transient validation): no `validation_status`
  field.
- **Authority concentration:** this single artifact's contract is co-governed by
  **5 independent sources** (contracts file, ADR 0014, ADR 0015 addendum, ADR
  0024, evidence-rules.md) and enforced by **2 validators** with a deliberate
  split. See `05-AUTHORITY-MAP.md` row B.

### `workflow_orchestration_plan`  (`artifacts/plan_{workflow_id}.md`)
- **P** workflow-planner
- **C** user, agents (autonomous_execution)
- **V** `validate-artifact.py` + `validate-plan.py` — but **only the finalized
  plan** must pass
- **X** `workflow-runtime.generate_plan()` emits a PROVISIONAL skeleton
  (`plan_stage: provisional`) at Phase 2 *before the brief exists* (may omit
  primary_fog_type / workflow_steps / created_at);
  `workflow-runtime.finalize_plan(brief_path)` consumes the brief's real
  `primary_fog_type` -> canonical plan.
- **G** artifact-contracts.yaml + ADR 0025 (two-stage lifecycle) + ADR 0005
  (skill invocation via workflows)
- **Authority note:** the plan is a **recommendation, not execution authority**
  (`CONTEXT.md:194`, ADR 0026). `recommended_workflow_id` inside it does not
  authorize `auto_invoke_next_workflow`.

---

## Audit / verification chain

### `work_claim`  (`artifacts/work_claim.md`)
- **P** task-requester (external; promoted into the pipeline so output-reconciler
  can cite it)
- **C** output-reconciler (REQUIRED fan-in input)
- **V** `validate-artifact.py work_claim` (required sections: source, claims;
  machine fields incl. immutable)
- **G** artifact-contracts.yaml; `immutable: true`

### `reconciliation_report`  (`artifacts/reconciliation_report.md`)
- **P** output-reconciler — re-derives each claim from durable artifacts,
  classifies `verified | disputed | omitted`, disposes each disputed/omitted
  `fix | defer(reason) | file`
- **C** to-issues, handoff
- **V** `validate-artifact.py reconciliation_report`
- **G** artifact-contracts.yaml; prototype `experiments/evidence/0018`
- **Fan-in (resolved "artifacts are the API" question):**
  `output-reconciler <- work_claim (required) + repository_sensemaking_brief
  (required) + prior_evidence (recommended)` (`AGW:342-351`)

### `docs_contract_reconciliation_report`  (`artifacts/docs_contract_reconciliation_report.md`)
- **P** sensemaking-docs-reconciler
- **C** repair-verifier (REQUIRED input), prompt-handoff
- **V** `validate-artifact.py docs_contract_reconciliation_report` (13 required
  sections)
- **G** artifact-contracts.yaml
- **Registered subgraph:** `docs-contract-reconciliation` workflow

### `repair_verification_report`  (`artifacts/repair_verification_report.md`)
- **P** repair-verifier — re-probes; checks each original brief finding against
  fresh `probe-report.yaml`; `findings_closed` / `findings_remaining` with
  disposition
- **C** handoff
- **V** `validate-artifact.py repair_verification_report`
- **G** artifact-contracts.yaml
- **Contract gap (DEMONSTRATED):** a formal `unevaluable` verdict category is
  *proposed but NOT encoded* in this contract (`AGW:252`, `AGW:387`). A
  failed/errored probe observation is not an observed absence, but the report
  has no field to say so.

---

## Handoff / continuation

### `prompt_handoff`  (`artifacts/prompt_handoff.md`)
- **P** `prompt-handoff` **AND** `handoff` (contract declares **two producers** —
  see `05-AUTHORITY-MAP.md` row H for the ambiguity this creates)
- **C** external_agent
- **V** `validate-artifact.py` + `validate-prompt-handoff.py`
- **G** artifact-contracts.yaml + ADR 0009 (handoff skill naming convention)

### `session_summary`  (`artifacts/session_summary.md`)
- **P** handoff
- **C** workflow-planner
- **Continuation reality (recorded, retirement-plan closure):** typed fan-in
  `CONTRACT_CLOSED`; prior-report selection is `CONVENTION` (the caller supplies
  which prior report); overall loop `CONVENTION_CLOSED` (`AGW:308-318`).

---

## Product-management sub-pipeline (present, lower architectural salience)

`persona -> discovery_findings -> opportunity_map -> hypothesis_statement ->
prd -> issue_list -> agent_brief -> code_patch`, plus `north_star_metric ->
okr_list -> roadmap -> stakeholder_update`, plus a UI sub-chain
(`ui_specification -> ui_flows -> screen_specs`). All governed by the same
artifact-contracts.yaml and generic validator. Architecturally these are
**bounded PM/UI responsibilities reusing the same contract+validator spine**;
none are on the ratified product core path (ADR 0014).

---

## Cross-cutting observations (feed 09 / 12)

1. **`user_intent` is a fan-out hub (9 consumers); `repository_sensemaking_brief`
   is a fan-in + fan-out hub (4 consumers, and a fan-in target for
   output-reconciler).** These two nodes carry most of the artifact-graph
   centrality. A change to either contract has the widest blast radius.
2. **Two artifacts have >1 declared producer** (`prompt_handoff`;
   `user_intent` vs `user_intent_amendment` split by lifecycle). Multi-producer
   is a latent contract-authority ambiguity.
3. **The `probe_report` is consumed by two skills for *different* purposes**
   (diagnosis vs finding-closure) — the same serialized artifact, two
   consumer contracts, one validator.
4. **The transform edges all live in the runtime** (`generate_plan` /
   `finalize_plan` / warrant seam). No skill transforms another skill's
   artifact — skills only produce and consume. This is a clean structural
   invariant worth preserving.
