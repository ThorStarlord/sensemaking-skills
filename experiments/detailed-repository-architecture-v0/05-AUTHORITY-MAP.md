# 05 — AUTHORITY MAP (DETAILED_REPOSITORY_ARCHITECTURE_PROTOTYPE_V0)

**This map is load-bearing.** An ordinary dependency graph cannot answer:
*Who owns this fact? Who enforces it? Who may change it? Which source wins if
two representations disagree? Is a documented contract mechanically enforced?
Is implementation ahead of policy, or policy ahead of implementation?*

Columns:
- **DEFINES** — the source that defines the semantics of the fact
- **ENFORCES** — the mechanism that mechanically enforces it (or `— none —`)
- **RUNTIME-OWNS** — who owns runtime identity/path/state for it (if applicable)
- **WINS ON CONFLICT** — canonical source when representations disagree
- **POLICY vs IMPL** — is implementation ahead of policy, policy ahead of
  implementation, or aligned?
- grade

---

## A. The top-level control loop

| Field | Value |
|---|---|
| DEFINES | ADR 0013 (ACCEPTED) — active coding agent owns the recursive control loop |
| ENFORCES | — none (no machinery) — `AGW:391` "CONVENTION (no machinery)" |
| RUNTIME-OWNS | n/a — the runtime is explicitly *support machinery*, not the loop |
| WINS ON CONFLICT | ADR 0013, reinforced by `CONTEXT.md:13` and `docs/decision-orchestration-boundary.md` |
| POLICY vs IMPL | **policy ahead of impl** — the runtime still exposes whole-loop-ish sequencing (compatibility); the doctrine that it is not the controller is convention-only |
| grade | DEMONSTRATED |

## B. `repository_sensemaking_brief` contract

| Field | Value |
|---|---|
| DEFINES | `artifact-contracts.yaml` (structure) + ADR 0014 (product role) + ADR 0015 addendum (`representation_sufficiency` -> MODEL_WARRANT) + ADR 0024 (Section 15 `extended_analysis`) + `skills/repo-sensemaker/references/evidence-rules.md` Rule 7 (`collision_dedup_direction`) |
| ENFORCES | `validate-artifact.py` (generic: sections + required machine fields) **+** `validate-brief.py` (conditional/blocking rules) — a deliberate 2-validator split |
| RUNTIME-OWNS | output **path** (session-scoped, `_resolve_artifact_path`, passed as `expected_output_path`); the MODEL_WARRANT **decision** (opt-in seam) |
| WINS ON CONFLICT | for structure: `artifact-contracts.yaml`; for warrant semantics: ADR 0015 addendum + `CONTEXT.md:146-158`; for evidence discipline: `evidence-rules.md` |
| POLICY vs IMPL | **aligned, but fragile** — 5 defining sources, 2 enforcers; the contract file itself carries 4 long comment blocks reconciling them (lines 145-180). Historically defect-prone (see `06`, `11`). |
| grade | DEMONSTRATED |

## C. Artifact path resolution

| Field | Value |
|---|---|
| DEFINES | ADR 0010 (ACCEPTED) — one component owns path resolution; session-scoped |
| ENFORCES | `tests/` (path-containment tests) + `PreToolUse` gate proving `expected_output_path` containment; `src/sensemaking_skills/path_containment.py` |
| RUNTIME-OWNS | `workflow-runtime._resolve_artifact_path` — the single authoritative resolver |
| WINS ON CONFLICT | ADR 0010 + `CLAUDE.md` verification-discipline section ("Artifact *paths* are part of the contract, too") |
| POLICY vs IMPL | **aligned** — this is the cleanest authority seam in the repo; a past flat-path-vs-session-path mismatch is the reason it is now explicit |
| grade | DEMONSTRATED |

## D. Machine field names (routing reads)

| Field | Value |
|---|---|
| DEFINES | `artifact-contracts.yaml` (`required_machine_fields` / `recommended_machine_fields`) |
| ENFORCES | `tests/test_field_contract_agreement.py` + `test_artifact_contract_agreement.py` + `test_auto_invoke_registry_agreement.py` — every field in `_WORKFLOW_ID_FIELDS` / `_FOG_TYPE_FIELDS` must be declared |
| RUNTIME-OWNS | `workflow-runtime._WORKFLOW_ID_FIELDS`, `_FOG_TYPE_FIELDS` (the reader side) |
| WINS ON CONFLICT | `artifact-contracts.yaml` — "Producers and consumers must agree on field names — do not read fields from memory" (`CLAUDE.md`) |
| POLICY vs IMPL | **aligned** — the test is the enforcement; note ADR 0024 `extended_analysis.*` fields are declared but **deliberately NOT** in the routing reader sets |
| grade | DEMONSTRATED |

## E. Automatic fog-type -> implementation routing

| Field | Value |
|---|---|
| DEFINES | ADR 0018 — **SUPERSEDED 2026-08-18, never Accepted**; no replacement automatic-routing policy is Accepted |
| ENFORCES | — none (and deliberately so) — |
| RUNTIME-OWNS | `workflow-runtime` *can* execute a fog-type -> workflow chain (`fast-path-workflow` / `full-fog-workflow` `auto_invoke_next_workflow: true`) |
| WINS ON CONFLICT | ADR 0014 (routing deferred) + ADR 0026 (registry flag is compatibility metadata, NOT authority) + `CONTEXT.md:127` + `CONTEXT.md:335` |
| POLICY vs IMPL | **impl ahead of policy** — runtime + registry contain a working route that policy explicitly refuses to ratify. This is the single largest architecture-to-policy divergence in the repo. |
| grade | DEMONSTRATED |

## F. `auto_invoke_next_workflow` execution authority

| Field | Value |
|---|---|
| DEFINES | ADR 0026 (ACCEPTED 2026-08-24, PR #235 `e5a2e73`) — compatibility metadata only; execution needs a SEPARATE explicit authority event |
| ENFORCES | the auto-invocation consumers "surface the candidate and fail closed (no automatic child-workflow spawn)" in the absence of such an event (`workflow-registry.yaml` header, `E-WFREG-head`) |
| RUNTIME-OWNS | two runtime consumers read the field; two registry copies mirror it (`skills/workflow-planner/references/` and `src/sensemaking_skills/defaults/`) |
| WINS ON CONFLICT | ADR 0026 |
| POLICY vs IMPL | **now aligned** (as of ADR 0026) — but the field, both mirrors, and both consumers still exist, so the alignment is "fail-closed guard," not "removed." Issue #230 remains the open tracker for the bounded implementation. |
| grade | DEMONSTRATED |

## G. Stage-1 controlled model invocation

| Field | Value |
|---|---|
| DEFINES | `gate_a_authorization.py` docstring — "no valid authorization capability, no path to the model invocation function"; enforcement by *capability*, not flag |
| ENFORCES | `skill_executor.py` requires an `AuthorizedInvocation` object for Stage-1 invocations; `GateAAuthorizationRequired` raised otherwise; no boolean/env-var/module flag can substitute |
| RUNTIME-OWNS | `gate_a_authorization.authorize()` -> typed `AuthorizationDecision`; `exploratory_authorization/` issues/registers capabilities |
| WINS ON CONFLICT | the capability check itself (code); **placement** is still debated by ADR 0022 (PROPOSED, awaiting independent adversarial review) |
| POLICY vs IMPL | **impl ahead of policy on placement** — the mechanism is real and strict; where the consumer *should* sit is an open ADR. |
| grade | DEMONSTRATED |

## H. `prompt_handoff` producer identity

| Field | Value |
|---|---|
| DEFINES | `artifact-contracts.yaml` — `produced_by: [prompt-handoff, handoff]` (two producers) |
| ENFORCES | generic validator checks structure, not which skill wrote it |
| RUNTIME-OWNS | path resolution only |
| WINS ON CONFLICT | undefined — the contract names two producers with no precedence rule |
| POLICY vs IMPL | **latent ambiguity** — ADR 0009 governs *naming* but not which of two skills is canonical producer for a given run. Low current blast radius; flagged for `08` / `09`. |
| grade | DERIVED |

## I. ADR status vocabulary

| Field | Value |
|---|---|
| DEFINES | `docs/adr/README.md` — PROPOSED / PROVISIONAL / ACCEPTED / SUPERSEDED / REJECTED |
| ENFORCES | `scripts/probe_relationships.py` — reads every `docs/adr/NNN-*.md` `**Status**` line; findings for unrecognized/missing status and status-claim mismatch |
| RUNTIME-OWNS | n/a |
| WINS ON CONFLICT | `docs/adr/README.md` |
| POLICY vs IMPL | **aligned** — one of the few doc-level contracts with a real automated enforcer. Note several ADRs use compound status strings ("ACCEPTED (revised, narrowed) — ...") the probe must tolerate. |
| grade | DEMONSTRATED |

## J. Canonical enumerated vocabulary

| Field | Value |
|---|---|
| DEFINES | `docs/canonical-vocabulary.yaml` |
| ENFORCES | ADR 0011 + controlled-vocab checks in `validate-*.py` |
| WINS ON CONFLICT | `docs/canonical-vocabulary.yaml` |
| POLICY vs IMPL | **aligned** |
| grade | DEMONSTRATED |

## K. Research claims vs product behavior

| Field | Value |
|---|---|
| DEFINES | `docs/research/control-model-research-agenda.md` — Status line: "research hypotheses only ... not an ADR, not a product contract, not a roadmap commitment" |
| ENFORCES | — none — (discipline only; the "machinery-promotion rule" is a convention) |
| RUNTIME-OWNS | `reasoning/` slice is real code, wired to the runtime **only** via the opt-in `warrant_enabled` seam |
| WINS ON CONFLICT | ADRs + `CONTEXT.md` — research "may support claims but may not authorize product behavior" (`authorization Section 10`, matched by `CONTEXT.md:36-38`, `E-RESAGENDA-status`) |
| POLICY vs IMPL | **aligned by intent, porous by construction** — real research code (`reasoning/`, `campaign_*`) sits inside the product package `src/sensemaking_skills/`. Nothing mechanically prevents a future caller from wiring it deeper. |
| grade | DEMONSTRATED |

---

## Authority concentration ranking (feeds `09-DECISION-VIEWS.md` Q1)

| Rank | Concentration | Defining sources | Enforcers | Why it matters |
|---|---|---|---|---|
| 1 | `repository_sensemaking_brief` contract | 5 | 2 | widest artifact fan-out; most co-governance; historically defect-prone |
| 2 | automatic fog-type routing | 1 (SUPERSEDED) | 0 | largest impl-ahead-of-policy gap |
| 3 | MODEL_WARRANT / representation_sufficiency seam | ADR 0015 addendum + CONTEXT.md + reasoning/ slice | runtime seam (opt-in) | research-to-product boundary passes straight through; the authorization explicitly forbids changing it |
| 4 | `auto_invoke_next_workflow` | ADR 0026 | fail-closed guard | 2 registry mirrors + 2 consumers still present |
| 5 | artifact path resolution | ADR 0010 | tests + PreToolUse gate | cleanest seam; included as the positive control |

## Multiply-governed / multiply-enforced facts

- **brief contract**: 5 definers, 2 enforcers (row B)
- **routing**: policy says "no", runtime says "can" (row E) — a genuine
  authority conflict, currently resolved only by documentation
- **Gate A placement**: mechanism (code) vs placement (ADR 0022 PROPOSED) —
  split authority (row G)
- **prompt_handoff producer**: two declared producers, no precedence (row H)
- **workflow-registry.yaml**: two physical copies
  (`skills/workflow-planner/references/` + `src/sensemaking_skills/defaults/`) —
  which is canonical? `CONTEXT.md:299` names the `skills/workflow-planner/`
  copy in the source-of-truth map; the `src/` copy is a `defaults/` mirror.
  grade: DERIVED.
