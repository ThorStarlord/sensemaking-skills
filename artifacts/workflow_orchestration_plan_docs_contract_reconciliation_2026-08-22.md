# Workflow Orchestration Plan

## 1. Brief consumed

Repository Sensemaking Brief (2026-08-22, this session): the `sensemaking-skills`
repository presents two incompatible product definitions. The ratified product
(ADR 0013/0014, `CONTEXT.md`, `README.md`, owner decision package 2026-07-26,
D1 = A) is an agent-native engineering sensemaking and control layer: the active
coding agent owns the loop, the deliverable is a human-reviewed
`repository_sensemaking_brief`, automatic fog-type routing is NOT ratified
(`CONTEXT.md:93`), and the CLI is utilities-only. The wayfinder-era surface
(`goal.md`, `docs/PRD-V1-Sensemaking.md`, `roadmap.md`,
`docs/CUSTOMER_ONBOARDING.md`, `docs/FAQ.md`, `GETTING_STARTED.md`,
`docs/canonical-vocabulary.yaml`, `skill-registry.yaml`,
`workflow-registry.yaml`, `skills/workflow-planner/SKILL.md`) describes a
production-ready auto-routing orchestrator: 44 registered skills (30
unimplemented), a fifth fog type `integration_fog`, `yolo_execution`, and
`auto_invoke_next_workflow` entries. Weakest boundary classified as Ghost
Features (documented product surface without implementation), driven by
Vocabulary Drift in the canonical registries. `recommended_workflow_id`:
`docs-contract-reconciliation`.

Note on `escalation_recommended`: the brief recorded `escalation_recommended:
true` in the sense of "owner review is required" (D6). This plan encodes that
human-review escalation through mandatory approval gates and
`scope_expansion_requires_approval: true`. At the plan level,
`escalation_recommended` is `false` because plan-level escalation semantics
mean workflow escalation (to `full-fog-workflow`), which is not warranted here:
the boundary is already diagnosed and the owner selected the narrower
`docs-contract-reconciliation`.

## 1.5. Problem classification (fog type)

- **product_fog**: conflicting product definitions, implied users, value
  propositions, interaction models, and scope boundaries carried in the
  repository's own authoritative files. Not a code-structure, docs-only, or UI
  problem.

## 2. Chosen workflow

`docs-contract-reconciliation` (registered in
`skills/workflow-planner/references/workflow-registry.yaml`).

## 3. Why this workflow

Its registered purpose is exactly this boundary: "Resolve drift between
documentation, registries, artifact contracts, templates, and validator rules"
(`workflow-registry.yaml`, `docs-contract-reconciliation` entry). It is the
only registered workflow whose step 2 is `sensemaking-docs-reconciler` — the
skill built for vocabulary/contract drift — followed by `repair-verifier`
(finding-specific closure) and `handoff`. Execution is `plan_only`: this plan
is decision support; no file is modified until the owner approves the
reconciliation patch (D6, `docs/OWNER-DECISION-PACKAGE-2026-07-26.md:263-345`).

Scope guardrails carried into every step (from the owner's instruction and the
ratified boundary):

1. **Do not erase the agent-native architecture.** `CONTEXT.md` architecture
   sections and `docs/decision-orchestration-boundary.md` are read-only
   references for this pass; the reconciliation removes wayfinder-era claims,
   not the decision/control-layer architecture.
2. **Distinguish ratified scope from thesis/research.** Every target file or
   claim is tagged RATIFIED / THESIS-RESEARCH / HISTORICAL (matrix in Section
   5). The research agenda (`docs/research/control-model-research-agenda.md`)
   stays as explicitly non-ratified research and is never folded into either
   "historical" or "ratified product".
3. **No ADR 0014 re-opening.** Reconciliation targets the ratified boundary;
   re-opening routing/pipeline scope requires new external proof plus a new
   owner decision (`docs/adr/0014-product-boundary.md:110-117`).
4. **Contract changes require explicit user approval of the new schema**
   (sensemaking-docs-reconciler Contract Approval rule).
5. **Deprecate before delete.** An enum or registry value may be removed only
   after confirming no validator/contract/consumer still parses it; otherwise
   mark it deprecated with a note (avoids both ghost-feature regrowth and
   validator breakage).
6. **No Skill-logic mutation.** `sensemaking-docs-reconciler`'s No-Side-Effects
   rule (`skills/sensemaking-docs-reconciler/SKILL.md:22`) excludes skill
   logic, implementation code, and workflow-execution behavior from this
   workflow. The `skills/workflow-planner/SKILL.md` routing-semantics
   contradiction (5 fog types, fog-to-workflow routing, auto-invoke language)
   is follow-up finding F4: not modified here; routed to an independently
   authorized skill-maintenance/repair responsibility.

## 4. Skills in sequence

1. **repo-sensemaker** (drift diagnosis) — the brief already exists from the
   preceding invocation; re-validate it against the current tree rather than
   regenerate, unless the owner prefers a fresh run. Output:
   `repository_sensemaking_brief` (this session's brief).
2. **sensemaking-docs-reconciler** (audit, challenge, resolve, mutate) — produce
   the tagged scope inventory (Section 5 matrix), propose the reconciliation
   patch per tag, and present it for approval. NO mutation before approval.
3. **repair-verifier** (finding-specific closure) — re-probe the tree after the
   approved patch; verify each original finding (ghost skills, `integration_fog`,
   `yolo_execution`, auto-invoke, production-ready claims) no longer reproduces;
   remaining findings are fixed or deferred with a reason.
4. **handoff** (durable continuation) — emit `session_summary` so the next
   agent/run reconstructs state from artifacts, not conversation memory.

## 5. Inputs and outputs

| Step | Skill | Input | Output | Gate |
|---|---|---|---|---|
| 1 | repo-sensemaker | repository_state, prior_evidence | repository_sensemaking_brief (exists) | review_drift_diagnosis |
| 2 | sensemaking-docs-reconciler | repository_sensemaking_brief | docs_contract_reconciliation_report | review_reconciliation_patch |
| 3 | repair-verifier | docs_contract_reconciliation_report, repository_state | repair_verification_report | review_reconciliation_verified |
| 4 | handoff | repair_verification_report | session_summary | review_next_prompt |

### Scope classification matrix (deliverable of step 2, approved before mutation)

Tags: **[R]** ratified current scope — keep, remove only contradictions.
**[T]** current architectural thesis / research — keep, labeled research.
**[H]** historical wayfinder-era — mark HISTORICAL/SUPERSEDED, never delete.
**[A]** align/repair — edit to remove contradiction (needs approval).

| Target | Tag | Disposition |
|---|---|---|
| `CONTEXT.md` | R | Keep. Glossary-level edits only (sensemaking-docs-reconciler Mutate Rules); architecture/ownership/product-boundary sections untouched. |
| `docs/decision-orchestration-boundary.md` | R | Read-only reference for this pass. |
| `docs/agent-native-operating-workflow.md` | R | Read-only reference. |
| `docs/research/control-model-research-agenda.md` | T | Keep as research hypotheses only; preserve "not an ADR / product contract / roadmap commitment" status; never fold into historical. |
| `docs/adr/0013`, `0014`, `0023` | R | Untouched (already ratified/accepted). |
| `docs/adr/0017`, `0018`, `0019`, `0020`, `0021` | H | Already SUPERSEDED (2026-08-18); audit for docs still citing them as live authority (e.g. routing policy) and re-point to `docs/decision-orchestration-boundary.md`. |
| `goal.md` | H | Mark HISTORICAL (wayfinder-era North Star: raw goal to executed implementation). |
| `roadmap.md` | H | Mark HISTORICAL or re-scope to current (v0.2.2; readiness D7/D8); point to `STATUS.md`/`CHANGELOG.md`. |
| `docs/PRD-V1-Sensemaking.md` | H | Mark HISTORICAL (five-skill meta-routing pipeline); superseded by ADR 0014 + `CONTEXT.md`. |
| `docs/CUSTOMER_ONBOARDING.md` | H/A | Remove "production-ready orchestration system", `orchestration-runner.py` examples, autonomous/yolo claims, "zero repeatable failures" claim; if kept, rewrite to the agent-native path, else HISTORICAL. |
| `docs/FAQ.md` | A | Remove "production-ready? Yes" (lines 108-109); correct CLI/usage answers; fix unsupported "Core team" claim; else HISTORICAL. |
| `GETTING_STARTED.md` | A | Remove `tdd`/`triage` references (lines 176-177, 295, 335); correct brief/plan section descriptions to the real 14-section template; re-scope implementation example; else HISTORICAL. |
| `docs/canonical-vocabulary.yaml` | A | Owner decision (2026-08-22): REMOVE `integration_fog` from the active enum (`fog_types` 46-53, decision tree 72-74, `primary_fog_type.values` 79, `secondary_fog_types.values` 86) — do not retain it to keep tests green. Mark `yolo_execution` (line 422) compatibility-only, not ratified behavior. Contract change — approval required. |
| `src/sensemaking_skills/defaults/canonical-vocabulary.yaml` | A | Same removals (lines 46, 74, 79, 86) — the runtime `CanonicalVocabulary` loads this packaged default (`validation.py:42-55`); changing only the docs copy would leave executable behavior inconsistent. Plus `tests/test_validation.py:40` (assert removal) and `tests/test_path_drift.py:143` (docstring). |
| `tests/fixtures/validate-brief/valid/integration-fog-brief.md` | A | Move to `invalid/` as a negative fixture (`validator_case: negative`) — the 5th type becomes rejected, not accepted. |
| `skills/workflow-planner/references/skill-registry.yaml` | A | Owner decision: deprecate-before-delete, but classify — 30 unimplemented ids split into STILL-PROPOSED (`prompt-handoff`, `triage`; current-doc consumer refs) vs HISTORICAL/DEPRECATED (28: `tdd`, `ui-brief`, `persona`, `opportunity-tree`, `gtm`, `battlecard`, ...); keep the 18 implemented skills. Approval required. |
| `skills/workflow-planner/references/workflow-registry.yaml` | A | Annotate `auto_invoke_next_workflow: true` entries (lines 38-39, 93-94, 495-496, 816-817) as compatibility-only, per `CONTEXT.md:93`; keep workflow ids as bounded subgraphs; do not delete (validators/tests reference them). |
| `skills/workflow-planner/SKILL.md` | — | NO MUTATION in this workflow — lines 87-100 contain actual Skill routing semantics; `sensemaking-docs-reconciler` forbids modifying skill logic/implementation/workflow-execution behavior (`SKILL.md:22`). Contradiction recorded as follow-up F4: route to `skill-maintainer` / owner-authorized skill repair. |
| `skills/workflow-planner/references/execution-modes.md` | A | Mark `yolo_execution` deprecated/compat (runner retirement, ADR 0013); align mode table with retained modes (`plan_only`, `prompt_chain`, `guided_execution`; `autonomous_execution` as documented-compat). |
| `skills/workflow-planner/references/artifact-contracts.yaml` | A | Verify enum alignment after vocabulary reconciliation (e.g. `primary_fog_type`); confirm `weakness_type` field (D3 = B) matches the brief skeleton; adjust only with approval. |
| `docs/ROUTING_GUIDE.md`, `docs/PORTFOLIO_OPERATIONS.md`, `docs/run-ledger-guide.md` | H | Deferred (owner decision 2026-08-22): record as follow-up candidates; optional HISTORICAL banner only where discoverable enough to be mistaken for current guidance (candidate: `ROUTING_GUIDE.md`). |
| `docs/UI-ROUTING-IMPROVEMENTS.md`, `docs/ui-routing-test-plan.md`, `docs/UI-ROUTING-TESTING-RESULTS.md` | H | Deferred: historical implementation records, useful as evidence; no rewrite; optional banner if discoverable. |
| `README.md` | R/A | Verify no wayfinder claims remain; update stale "Roadmap to User-Ready" checkboxes (lines 337-354) or remove, per `roadmap.md`/`STATUS.md`. |
| "production ready" phrasing across `README.md:10`, `docs/*` | A | Align with owner-ratified constraint (`docs/OWNER-DECISION-PACKAGE-2026-07-26.md:195`): allowed only for what is "externally exercised", not general GA claims. |

## 6. Approval gates

All gates pause for a user decision (`pause_for_user_decision`):

- `review_drift_diagnosis` — owner confirms the brief/finding set before any
  reconciliation patch is drafted.
- `review_reconciliation_patch` — owner approves the tagged matrix and each
  concrete edit (mandatory for registry/contract/skill changes per the
  Contract Approval rule; D6 requires human approval of every final artifact).
- `review_reconciliation_verified` — owner reviews the repair-verification
  report (original findings closed/deferred with reason).
- `review_next_prompt` — owner approves the durable handoff.

## 7. Stop conditions

- `validator_failure` — any produced artifact fails its contract validator;
  repair within the bounded retry policy or stop.
- `gate_denial` — owner rejects a patch; record disposition, do not proceed.
- `step_failure` — a step cannot produce its contracted output.
- `user_interrupt` — owner stops the run.
- `scope_guard_trigger` — any proposed edit that would erase/rewrite
  `CONTEXT.md` architecture sections or `docs/decision-orchestration-boundary.md`,
  fold research-agenda hypotheses into ratified product scope (or vice versa),
  or re-open ADR 0014 scope — stop and escalate to the owner.

## 8. Execution mode

`plan_only` — generate the plan and the reconciliation patch proposal only; no
repository mutation. The registered workflow allows `plan_only`, `prompt_chain`,
and `guided_execution`; `plan_only` is selected per the owner's instruction.

## 9. Prompt chain

N/A - mode is plan_only. No prompt chain generated.

## 10. Run log template

```markdown
# Run log — docs-contract-reconciliation (plan_only)
- date, branch, base SHA
- input: repository_sensemaking_brief (ref), repository_state
- step 1 (repo-sensemaker): brief re-validation result
- step 2 (sensemaking-docs-reconciler): tagged matrix; proposed edits;
  approval decisions per file (approved / denied / revised)
- step 3 (repair-verifier): findings_closed / findings_remaining with
  dispositions; probe-report refs
- step 4 (handoff): session_summary ref
- validator results for every artifact; deviations and why
```

## 11. Machine-readable plan

```yaml
artifact_id: workflow_orchestration_plan
schema_version: 1
source_intent_ref: 00-user-intent.md
primary_fog_type: product_fog
chosen_workflow_id: docs-contract-reconciliation
execution_mode: plan_only
status: ready
system_recommended_workflow: docs-contract-reconciliation
selected_workflow: docs-contract-reconciliation
routing_divergence: false
routing_decision_method: manual_override
escalation_recommended: false
auto_escalation_allowed: false
scope_expansion_requires_approval: true
initial_inputs:
  - id: repository_state
    type: external_context
    required: true
    description: "Current repository files, registries, templates, validator scripts, and git state."
  - id: prior_evidence
    type: external_context
    required: false
    description: "Repository Sensemaking Brief (2026-08-22), retirement plan, owner decision package 2026-07-26, product-contract review."
workflow_steps:
  - step_id: 1
    skill: repo-sensemaker
    step_type: local_execution
    input_source: repository_state
    output_artifact: repository_sensemaking_brief
    gate: review_drift_diagnosis
    status: pending
    description: "Confirm/refresh the drift diagnosis (brief exists from the preceding invocation); owner confirms findings."
  - step_id: 2
    skill: sensemaking-docs-reconciler
    step_type: local_execution
    input_artifact: repository_sensemaking_brief
    output_artifact: docs_contract_reconciliation_report
    gate: review_reconciliation_patch
    status: pending
    description: "Produce the tagged scope matrix and reconciliation patch per tag; present for owner approval; no mutation before approval."
  - step_id: 3
    skill: repair-verifier
    step_type: local_execution
    input_artifact: docs_contract_reconciliation_report
    input_source: repository_state
    output_artifact: repair_verification_report
    gate: review_reconciliation_verified
    status: pending
    description: "Re-probe after the approved patch; verify original findings no longer reproduce; fix or defer remaining with a reason."
  - step_id: 4
    skill: handoff
    step_type: local_execution
    input_artifact: repair_verification_report
    output_artifact: session_summary
    gate: review_next_prompt
    status: pending
    description: "Emit durable session_summary so the next agent/run reconstructs state from artifacts."
approval_gates:
  - review_drift_diagnosis
  - review_reconciliation_patch
  - review_reconciliation_verified
  - review_next_prompt
gate_behavior:
  review_drift_diagnosis: pause_for_user_decision
  review_reconciliation_patch: pause_for_user_decision
  review_reconciliation_verified: pause_for_user_decision
  review_next_prompt: pause_for_user_decision
stop_conditions:
  - validator_failure
  - gate_denial
  - step_failure
  - user_interrupt
  - scope_guard_trigger
subset_run: false
subset_reason: null
included_steps: []
excluded_steps: []
created_at: "2026-08-22T20:20:57Z"
```
