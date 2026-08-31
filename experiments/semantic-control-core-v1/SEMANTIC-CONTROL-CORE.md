# SEMANTIC CONTROL CORE — V1 (THIN_SEMANTIC_CORE_CANDIDATE)

Represented repository state: `main @ ba8968ca1a12caa90ce7beb0ee5fd2dfac055f37`.
One authoritative row per consequential semantic concern. Evidence is
**referenced**, not copied. Grades: `D`=DEMONSTRATED, `d`=DERIVED,
`I`=INTERPRETIVE, `H`=HYPOTHESIS. Change-rate: `S`=slow, `M`=medium, `F`=fast.

> Inclusion test (authorization §11): a fact is here only if it is consequential,
> unsafe to reconstruct from one obvious source, slow-changing enough to
> maintain, carries authority/lifecycle/enforcement ambiguity, was used in V0
> reasoning, and its omission could produce a wrong responsibility or impact set.
> Everything else is left to `ON-DEMAND-PROJECTION-RECIPE.md`.

---

## 1. Authority-seam register

Columns: **Concern** · **Status** · **Defines** (semantics) · **Enforces**
(mechanism) · **Runtime owns** (identity/path/state) · **Wins on conflict** ·
**Policy vs impl** · **Grade / Rate**.

| # | Concern | Status | Defines | Enforces | Runtime owns | Wins on conflict | Policy vs impl | G/R |
|---|---|---|---|---|---|---|---|---|
| A1 | Top-level control loop | ACTIVE | ADR 0013 (Accepted) — active coding agent owns the recursive loop; runtime is support machinery | *nothing* — convention only (`AGW` Reality map: "CONVENTION (no machinery)") | runtime still exposes whole-loop-ish sequencing as **compatibility** | ADR 0013 + `CONTEXT.md` "top operating rule" + `decision-orchestration-boundary.md` | **policy ahead of impl** — doctrine that the runtime is not the controller is unenforced | D / S |
| A2 | `repository_sensemaking_brief` contract | ACTIVE | 5 sources: `artifact-contracts.yaml` (structure) + ADR 0014 (product role) + ADR 0015 addendum (`representation_sufficiency`→MODEL_WARRANT) + ADR 0024 (Section 15 `extended_analysis`) + `skills/repo-sensemaker/references/evidence-rules.md` Rule 7 (`collision_dedup_direction`) | `scripts/validate-artifact.py` (generic: sections + required machine fields) **+** `scripts/validate-brief.py` (conditional/blocking) — deliberate 2-validator split | output **path** (session-scoped `_resolve_artifact_path`, passed as `expected_output_path`) | structure→`artifact-contracts.yaml`; warrant semantics→ADR 0015 addendum + `CONTEXT.md` MODEL_WARRANT section; evidence discipline→`evidence-rules.md` | **aligned but fragile** — 5 definers, 2 enforcers; contract file carries ~4 reconciling comment blocks; historically defect-prone | D / M |
| A3 | Artifact path resolution | ACTIVE | ADR 0010 (Accepted) — one component resolves paths, session-scoped | `src/sensemaking_skills/path_containment.py` + path-containment tests + PreToolUse containment gate | `scripts/workflow-runtime.py::_resolve_artifact_path` (sole resolver); executors receive `expected_output_path`, must not recompute `artifacts/<id>.md` | ADR 0010 + `CLAUDE.md` verification-discipline ("paths are part of the contract") | **aligned** — cleanest seam; made explicit after a flat-path vs session-path success/NOT_FOUND mismatch | D / S |
| A4 | Automatic fog-type → implementation routing | SUPERSEDED (capability physically present) | ADR 0018 — **SUPERSEDED 2026-08-18, never Accepted**; no replacement automatic-routing policy Accepted | *none, by design* | `workflow-runtime.py` **can** execute `fast-path-workflow` / `full-fog-workflow` chains (`auto_invoke_next_workflow: true`) | ADR 0014 (routing deferred) + ADR 0026 + `CONTEXT.md` ("automatic routing not ratified"; "not automatically ratified merely because machinery exists") | **impl ahead of policy — largest divergence in the repo** | D / S |
| A5 | `auto_invoke_next_workflow` execution authority | ACTIVE ruling / compatibility field retained | ADR 0026 (Accepted 2026-08-24, PR #235) — compatibility metadata only; execution needs a **separate explicit authority event** | auto-invocation consumers "surface the candidate and fail closed" (no automatic child-workflow spawn) — `workflow-registry.yaml` header | 2 runtime consumers read the field; **2 registry mirrors** carry it (`skills/workflow-planner/references/` + `src/sensemaking_skills/defaults/`) | ADR 0026 | **now aligned** (fail-closed guard); field + mirrors + consumers still physically present; Issue #230 open tracker | D / S |
| A6 | MODEL_WARRANT / `representation_sufficiency` seam | ACTIVE, opt-in | ADR 0015 addendum + `CONTEXT.md` MODEL_WARRANT section — `representation_sufficiency` (producer judgment) maps deterministically: sufficient→NO, contract-valid insufficient_bounded→PARTIAL, inconclusive/missing/malformed→INCONCLUSIVE; FULL deferred | `scripts/validate-brief.py` (field shape) + the seam's own gate: INCONCLUSIVE blocks routing / representation materialization / NO_CHANGE terminalization | `workflow-runtime.py` computes the `WarrantRecord` **only when `warrant_enabled=True`** (constructor kwarg, default `False`), **after** validator PASS + reconciliation; logic in `src/sensemaking_skills/reasoning/` (`warrant_gate.py`, `vertical_slice.py`, `evidence_probes.py`) | ADR 0015 addendum + `CONTEXT.md`; the reasoning slice is research code, wired only through this opt-in hook | **aligned** — the field is declared OPTIONAL/ADDITIVE in `artifact-contracts.yaml`; absent/invalid fails closed | D / M |
| A7 | Stage-1 controlled model invocation (Gate A) | ACTIVE mechanism / PROPOSED placement | `scripts/gate_a_authorization.py` — capability, not flag: "no valid authorization capability, no path to the model invocation function"; `authorize()`→typed `AuthorizationDecision`; only `authorized=True` yields `AuthorizedInvocation` | `scripts/skill_executor.py` requires the `AuthorizedInvocation` object for Stage-1 invocations; `GateAAuthorizationRequired` raised otherwise; no boolean/env-var substitute | `gate_a_authorization.authorize()`; `src/sensemaking_skills/exploratory_authorization/` issues/registers capabilities | mechanism → the capability check (code); **placement** → undecided | **impl ahead of policy on placement** — ADR 0022 PROPOSED, awaiting independent adversarial review | D / M |

---

## 2. Lifecycle ledger — physical presence ≠ semantic authority

Only entries where something remains present after losing (or before gaining)
authority, and the confusion is consequential.

| Object | Lifecycle | Still physically present as | Do not read as | Grade / Rate |
|---|---|---|---|---|
| ADR 0018 (deterministic fog-type routing table) | SUPERSEDED, never Accepted | working `auto_invoke_next_workflow: true` chains in `workflow-registry.yaml` + runtime execution path | "routing is intended / ratified" (see A4) | D / S |
| ADRs 0017, 0019, 0020, 0021 | SUPERSEDED — historical proposals, never Accepted | files under `docs/adr/` with compound "SUPERSEDED — …" status strings | current policy | D / S |
| ADRs 0006, 0007, 0008, 0022 | PROPOSED | files under `docs/adr/` | Accepted decisions | D / S |
| `workflow-orchestrator/references/artifact-contracts.yaml` | DEPRECATED (2026-08-09), header says "No code should read this file" | **sole home** of `required_sections` / `required_machine_fields` for `prd` / `issue_list` / `agent_brief` / `code_patch` (INFRA-004); xfail tests in `tests/test_artifact_contracts_pm_engineering.py` | obsolete / safely deletable *now* | D / S |
| `src/sensemaking_skills/reasoning/` (+ `campaign_accounting/`, `campaign_validation/`) | research-only | real code under the product package `src/` | product authority — `control-model-research-agenda.md` status: "research hypotheses only; not an ADR, not a product contract" | D / M |
| `orchestration-runner.py` name | retired design (programmatic second-model runner, CLOSED 2026-08-13) | back-compat wrapper for `workflow-runtime.py` | a live alternative execution model (ADR 0013) | D / S |

Enforcement of ADR status vocabulary: `docs/adr/README.md` defines it;
`scripts/probe_relationships.py` reads every `docs/adr/NNN-*.md` `**Status**`
line and emits findings for unrecognized/missing/mismatched status. Grade D / S.

---

## 3. Enforcement-gap register

Categories (human-readable, not a controlled vocabulary):
`DECLARED_BUT_UNENFORCED` · `WEAKLY_ENFORCED` · `MULTIPLY_ENFORCED` ·
`DUPLICATED_AUTHORITY` · `IMPL_AHEAD_OF_POLICY` · `POLICY_AHEAD_OF_IMPL` ·
`MIRROR_DRIFT`.

| # | Gap | Category | Detail | Grade / Rate |
|---|---|---|---|---|
| G1 | Automatic fog-type routing | IMPL_AHEAD_OF_POLICY | runtime + registry implement a chain policy refuses to ratify (see A4) | D / S |
| G2 | Control loop / stop conditions / next-responsibility selection | DECLARED_BUT_UNENFORCED | `AGW` Reality map marks these CONVENTION with no machinery; the architecture's most consequential judgments are the least mechanically protected — by design (`harden only where pressured`) | D / S |
| G3 | `prd` / `issue_list` / `agent_brief` / `code_patch` contracts | DUPLICATED_AUTHORITY + DECLARED_BUT_UNENFORCED | live only in the DEPRECATED contracts copy; xfail-marked tests; canonical file never received the content (INFRA-004) | D / S |
| G4 | `repository_sensemaking_brief` contract | MULTIPLY_ENFORCED | `validate-artifact.py` (generic presence) + `validate-brief.py` (conditional/blocking); generic must **not** universally require `recommended_workflow_id` or valid `NO_REPOSITORY_CHANGE_WARRANTED` briefs fail | D / M |
| G5 | `workflow-registry.yaml` | DUPLICATED_AUTHORITY + MIRROR_DRIFT | `skills/workflow-planner/references/` (canonical per `CONTEXT.md` source-of-truth map) vs `src/sensemaking_skills/defaults/` differ at `ba8968c` (`src/` copy missing a `prior_evidence` input + a `repair-verifier` step); no copy-to-copy parity check among the validators | D / M |
| G6 | `auto_invoke_next_workflow` | POLICY_AHEAD_OF_IMPL | ADR 0026 ruling landed; field + 2 mirrors + 2 consumers physically remain, Issue #230 open (see A5) | D / S |
| G7 | `repair_verification_report` `unevaluable` verdict | DECLARED_BUT_UNENFORCED (contract gap) | a failed/errored probe observation is not an observed absence, but the contract has no field to record it; verdict proposed, not encoded (`AGW` §"Repair verification") | D / S |
| G8 | machine field names (routing reads) | MULTIPLY_ENFORCED (healthy) | `artifact-contracts.yaml` declares; `tests/test_field_contract_agreement.py` + `test_artifact_contract_agreement.py` + `test_auto_invoke_registry_agreement.py` guard that every field the runtime reads (`_WORKFLOW_ID_FIELDS` / `_FOG_TYPE_FIELDS`) is declared | D / M |

---

## 4. Research → product crossings

Only threads where a research conclusion currently reaches a product/runtime
path or is load-bearing to current product authority.

| Research source | Product/runtime consumer | Nature of crossing | Default / optional / guarded | Claim ceiling (to prevent over-read) | Grade / Rate |
|---|---|---|---|---|---|
| `docs/research/control-model-research-agenda.md` (C6R compressed control hypothesis) | `workflow-runtime.py` via `src/sensemaking_skills/reasoning/warrant_gate.py::run_seam_warrant` | the qualified vertical slice computes + records a `WarrantRecord` (MODEL_WARRANT decision) at the brief seam | **optional / guarded** — `warrant_enabled` constructor kwarg, default `False`; never mutates native evidence; NO→no representation, PARTIAL→minimal record | C6R: "compatible control behavior across a bounded synthetic suite + isolated model contexts." Does **not** establish real-world effectiveness, prevalence, productivity, optimality, model independence, or production readiness. #226 gate-separation study is open and freezes C6R until its preregistered result. | D / M |

No other research thread (semantic-authorities exercise, standalone-clone
proof, Path 1–4, Goal A, #218, PHB conditional-representation) currently wires
into a runtime path. PHB's 2026-08-30 meta-finding influenced *documentation*
(`CONTEXT.md` hardening line) but no code path. Everything else is discoverable
on demand — see the projection recipe.

---

## 5. How to keep this core honest

- Every row references source evidence; none copies large passages.
- `Rate` column: **13 of 15 load-bearing rows are `S` (slow) or `M` (medium)**.
  The only genuinely `F` (fast) facts V0 carried — current SHAs, ADR counts,
  file inventory, evidence-class rung tallies — are **deliberately absent**;
  the sole embedded SHA is the V1 snapshot provenance at the top.
- If answering a real question needs a fact not in these 5 sections, that is
  expected: go to `ON-DEMAND-PROJECTION-RECIPE.md`. The core is a map to the
  right authority question, not a substitute for repository evidence.
- Rule/symbol/test-level detail is intentionally **not** here (V0's known
  floor).
