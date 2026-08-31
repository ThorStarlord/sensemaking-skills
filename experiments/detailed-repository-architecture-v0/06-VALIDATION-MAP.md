# 06 — VALIDATION MAP (DETAILED_REPOSITORY_ARCHITECTURE_PROTOTYPE_V0)

Which validator / qualification suite protects which contract; where a declared
contract has **no enforcement**; where **multiple enforcement authorities**
exist. `CLAUDE.md` rule: *a validator rule must trace to a real consumer* —
enforcing a convention nothing consumes produces false failures.

`scripts/validate-*.py`: **21 scripts.** Dispatch entrypoint:
`scripts/validate-output.py` -> generic `scripts/validate-artifact.py` +
specialized validators. Structured JSON errors (`AGW:201-213`).

---

## 1. Contract -> enforcer table

| Contract / behavior | Declared in | Enforced by | Enforcement kind | grade |
|---|---|---|---|---|
| Generic artifact shape (sections, machine fields, controlled vocab, ref resolution, path/contract) | `artifact-contracts.yaml` | `validate-artifact.py` | generic, per artifact id | DEMONSTRATED |
| `repository_sensemaking_brief` conditional/blocking rules | `artifact-contracts.yaml` notes + `evidence-rules.md` Rule 7 + ADR 0015 addendum | `validate-brief.py` | specialized | DEMONSTRATED |
| `workflow_orchestration_plan` (finalized only) | `artifact-contracts.yaml` + ADR 0025 | `validate-plan.py` | specialized | DEMONSTRATED |
| `user_intent` | `artifact-contracts.yaml` | `validate-user-intent.py` + `validate-user-intent-amendment.py` | specialized | DEMONSTRATED |
| `unknowns_map` | `artifact-contracts.yaml` | `validate-unknowns-map.py` | specialized | DEMONSTRATED |
| `problem_frame` | `artifact-contracts.yaml` | `validate-alignment.py` | specialized (shared) | DEMONSTRATED |
| `prd` | `artifact-contracts.yaml` (canonical) **+ legacy copy for `required_sections`** | `validate-prd.py` | specialized | DEMONSTRATED |
| `prompt_handoff` | `artifact-contracts.yaml` | `validate-prompt-handoff.py` | specialized | DEMONSTRATED |
| `architectural_review_recommendation` | `artifact-contracts.yaml` | `validate-architectural-review-recommendation.py` | specialized | DEMONSTRATED |
| `usage_research_report` | `artifact-contracts.yaml` | `validate-usage-research-report.py` | specialized | DEMONSTRATED |
| `skill_improvement_plan` | `artifact-contracts.yaml` | `validate-skill-improvement-plan.py` | specialized | DEMONSTRATED |
| `probe_report` | ADR 0004 | `validate-probe-report.py` | specialized | DEMONSTRATED |
| run log format | `AGW:308` conventions | `validate-run-log.py` | specialized | DEMONSTRATED |
| Producer/consumer **field-name** agreement (routing reads) | `artifact-contracts.yaml` | `tests/test_field_contract_agreement.py` + `test_artifact_contract_agreement.py` + `test_auto_invoke_registry_agreement.py` | pytest guard | DEMONSTRATED |
| ADR `**Status**` vocabulary | `docs/adr/README.md` | `scripts/probe_relationships.py` (probe finding, not a hard gate) | probe / advisory | DEMONSTRATED |
| Canonical enumerated vocabulary | `docs/canonical-vocabulary.yaml` | ADR 0011 + controlled-vocab checks in `validate-*.py` | cross-cutting | DEMONSTRATED |
| fog-type normalization | canonical vocab | `validate-fog-type-normalization.py` | specialized | DEMONSTRATED |
| execution-mode coverage | `artifact-contracts.yaml` `required_for_modes` | `validate-mode-coverage.py` | specialized | DEMONSTRATED |
| target-repo validation (external repo) | — | `tests/test_workflow_runtime_target_repo_validation.py` + `validate-repo.py` | pytest + script | DEMONSTRATED |
| relationship / gate findings | — | `scripts/gate_relationship_findings.py` | script | INTERPRETIVE |
| Stage-1 model-invocation authorization | `gate_a_authorization.py` docstring | `skill_executor.py` capability requirement (`GateAAuthorizationRequired`) | capability, fail-closed | DEMONSTRATED |
| campaign artifact immutability / canonicalization | `campaign_validation/` schemas | `campaign_validation/{immutable,jcs,schema_validation}.py` | research-infra suite | DEMONSTRATED |

---

## 2. Declared contract with NO / WEAK mechanical enforcement

| Item | Status | Evidence | grade |
|---|---|---|---|
| **`prd` / `issue_list` / `agent_brief` / `code_patch` `required_sections` + `required_machine_fields`** | Live **only** in the **DEPRECATED** `workflow-orchestrator/references/artifact-contracts.yaml` (INFRA-004); never ported to the canonical file; covered by **xfail-marked** tests in `tests/test_artifact_contracts_pm_engineering.py`. The deprecated header says "No code should read this file." So these four contracts are declared in a file that is simultaneously deprecated *and* the sole source of that content. | `E-CONTRACT-dupe-header` | DEMONSTRATED |
| **`repair_verification_report` `unevaluable` verdict** | Proposed but NOT encoded in the contract; a failed/errored probe observation has no field to record it | `AGW:252`, `AGW:387` | DEMONSTRATED |
| **Automatic fog-type routing** | No enforcement — *by design* (policy refuses to ratify it). Not a gap; a deliberate non-enforcement. | `CONTEXT.md:127,335`, ADR 0018 SUPERSEDED | DEMONSTRATED |
| **Top-level control loop / stop conditions** | "CONVENTION (no machinery)" — the operating map is the only artifact; nothing enforces stop-condition discipline | `AGW:391` | DEMONSTRATED |
| **Next-responsibility selection** | "CONVENTION / unratified automation" — agent judgment, deliberately un-enforced | `AGW:383` | DEMONSTRATED |
| **prompt_handoff producer precedence** | Contract names two producers; no validator distinguishes | `04` row, `05` row H | DERIVED |
| **Promotion / durability lifecycle** | "CONVENTION / partially formalized" — `promotion-criteria.md` six gates apply to *skill improvements* only; general artifact promotion is doctrine | `AGW:388` | DEMONSTRATED |

---

## 3. Multiple enforcement authorities for one contract

| Contract | Enforcer 1 | Enforcer 2 | Split rationale | Risk |
|---|---|---|---|---|
| `repository_sensemaking_brief` | `validate-artifact.py` (generic: presence) | `validate-brief.py` (conditional: `recommended_workflow_id` semantics, `collision_dedup_direction` blocking, `representation_sufficiency`/`outcome`) | generic must NOT universally require `recommended_workflow_id` (contract lines 146-148) — that would break `NO_REPOSITORY_CHANGE_WARRANTED` briefs | if generic drifts toward requiring the field, valid no-change briefs fail (this class of defect is called out in `CLAUDE.md` verification discipline) |
| machine field names | `artifact-contracts.yaml` (declaration) | 3 pytest agreement tests (`test_field_contract_agreement`, `test_artifact_contract_agreement`, `test_auto_invoke_registry_agreement`) | contract is data; tests are the guard | adding a runtime field-read alias without a matching contract entry breaks the guard (explicitly warned in `CLAUDE.md`) |
| `workflow_orchestration_plan` | `validate-artifact.py` | `validate-plan.py` | only the finalized plan must pass; provisional skeleton exempt (ADR 0025) | validating the provisional skeleton as canonical is a category error the contract note guards against |
| canonical vocabulary | ADR 0011 (policy) | controlled-vocab checks embedded in many `validate-*.py` | one policy, many enforcement points | a new enum value must be added to `canonical-vocabulary.yaml` *and* reach every embedded check |

---

## 4. Registry duplication (enforcement-relevant)

| Registry | Copy A (canonical) | Copy B | Drift observed? | grade |
|---|---|---|---|---|
| `artifact-contracts.yaml` | `skills/workflow-planner/references/` | `workflow-orchestrator/references/` (**DEPRECATED header, 2026-08-09**) | **Yes, intentional** — Copy B uniquely holds 4 PM/engineering contracts (INFRA-004); Copy A is the only file live code reads | DEMONSTRATED |
| `workflow-registry.yaml` | `skills/workflow-planner/references/` (named canonical in `CONTEXT.md:299`) | `src/sensemaking_skills/defaults/` | **Yes** — Copy B is missing the `prior_evidence` input and a `repair-verifier` step present in Copy A (`diff` at construction SHA) | DEMONSTRATED |

Both duplications are real and both carry drift. Neither has an automated
sync check surfaced in the 21 validators (`test_auto_invoke_registry_agreement.py`
checks auto-invoke field agreement between registry and runtime, not
copy-to-copy content parity). grade: DERIVED.

---

## 5. What this map exposes (feeds `09` / `12`)

1. **Enforcement is strong at the artifact-shape layer and absent at the
   control-loop layer.** Every durable artifact has a validator; the decisions
   *about* artifacts (trigger, responsibility selection, stop) have none. This
   is deliberate (`harden only where pressured`) but means the architecture's
   most consequential judgments are the least mechanically protected.
2. **One contract (`brief`) carries most of the conditional-enforcement
   complexity.** The 2-validator split plus 4 reconciling comment blocks in the
   contract file is where enforcement bugs have clustered.
3. **A deprecated file is load-bearing.** `workflow-orchestrator/references/artifact-contracts.yaml`
   is simultaneously "no code should read this" and the sole home of 4
   contracts. That is an authority/lifecycle contradiction a dependency graph
   would not surface.
4. **Two registries have two copies with real drift and no parity check.**
