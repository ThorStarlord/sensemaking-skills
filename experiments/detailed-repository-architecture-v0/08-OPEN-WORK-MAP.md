# 08 — OPEN WORK MAP (DETAILED_REPOSITORY_ARCHITECTURE_PROTOTYPE_V0)

Open work **only where it materially intersects architectural ownership or an
unresolved decision.** Not a backlog dump. Each item: what is open, which
architectural boundary it sits on, who owns the decision, current state.

---

## OW-1 — `auto_invoke_next_workflow` bounded implementation (Issue #230)

- **Open:** ADR 0026 ratified the *policy* (compatibility metadata, not
  authority; fail closed) but Issue #230 "remains open as the tracker for the
  bounded implementation."
- **Boundary:** authority seam F (`05-AUTHORITY-MAP.md`) — registry flag vs
  execution authority. Two registry mirrors + two runtime consumers still carry
  the field.
- **Decision owner:** settled (ADR 0026); remaining work is mechanical (guard +
  eventual field removal or explicit-authority-event wiring).
- **State:** policy aligned, implementation partial.
- **grade:** DEMONSTRATED

## OW-2 — Gate A authorization consumer placement (ADR 0022)

- **Open:** ADR 0022 is **PROPOSED — awaiting independent adversarial review.**
- **Boundary:** authority seam G — the mechanism (`gate_a_authorization.py` +
  `skill_executor.py` capability requirement) is real and strict; *where the
  consumer should sit* is undecided.
- **Decision owner:** owner, after independent adversarial review.
- **State:** impl ahead of policy on placement.
- **grade:** DEMONSTRATED

## OW-3 — `repair_verification_report` `unevaluable` verdict

- **Open:** a formal `unevaluable` verdict category is *proposed but not
  encoded* in the `repair_verification_report` contract (`AGW:252`, `AGW:387`).
- **Boundary:** artifact contract C (`04-ARTIFACT-FLOWS.md`) + evidence model
  ("a failed/errored observation is not an observed absence"). Today the report
  can only say closed / remaining.
- **Decision owner:** owner / ADR process (contract change).
- **State:** contract gap, low current pressure.
- **grade:** DEMONSTRATED

## OW-4 — PM/engineering contracts stranded in a deprecated file (INFRA-004)

- **Open:** `required_sections` / `required_machine_fields` for `prd`,
  `issue_list`, `agent_brief`, `code_patch` live **only** in the DEPRECATED
  `workflow-orchestrator/references/artifact-contracts.yaml`; xfail-marked tests
  in `tests/test_artifact_contracts_pm_engineering.py`; header says "No code
  should read this file" and "Once ported (or confirmed obsolete), delete this
  file."
- **Boundary:** validation map §2 + §4 — a deprecated file is load-bearing for
  4 contracts.
- **Decision owner:** agent-decidable (port or confirm obsolete) within the
  reconciliation slice that owns contract wiring; deletion is the terminal step.
- **State:** deliberately out of scope of the slice that deprecated it; still open.
- **grade:** DEMONSTRATED

## OW-5 — Two `workflow-registry.yaml` copies with real drift

- **Open:** `skills/workflow-planner/references/` (canonical per
  `CONTEXT.md:299`) vs `src/sensemaking_skills/defaults/` differ at the
  construction SHA (missing `prior_evidence` input + a `repair-verifier` step in
  the `src/` copy). No copy-to-copy parity check among the 21 validators.
- **Boundary:** registry authority (`05-AUTHORITY-MAP.md` §"Multiply-governed").
- **Decision owner:** agent-decidable (sync or collapse to one) — but "which is
  canonical and why two exist" may need owner confirmation.
- **State:** silent drift.
- **grade:** DEMONSTRATED

## OW-6 — Automatic downstream routing (the standing deferral)

- **Open (by design):** ADR 0014 defers routing pending its *own* external
  proof; ADR 0018 (deterministic fog-type table) SUPERSEDED, never Accepted.
  Runtime + registry retain a working `fast-path-workflow` / `full-fog-workflow`
  chain with `auto_invoke_next_workflow: true`.
- **Boundary:** authority seam E — the largest impl-ahead-of-policy gap.
- **Decision owner:** owner, gated on external proof.
- **State:** intentionally unresolved; *not* a defect. Listed because it is the
  single most consequential unresolved architectural decision the repo carries.
- **grade:** DEMONSTRATED

## OW-7 — When should representation be materialized? (the question behind this prototype)

- **Open:** PHB (RC-8) established "conditional as default, FULL deferred" for
  the *sufficiency-gate* question, but the research agenda's meta-finding
  (`ba8968c`) says the next evidence must be **constructive** — build the rich
  representation and observe its value. That is exactly this V0.
- **Boundary:** upstream of the `representation_sufficiency` / MODEL_WARRANT
  gate (which this prototype must NOT modify).
- **Decision owner:** owner, after inspecting frozen V0 + observations
  (authorization Section 28).
- **State:** this prototype is the open work item; disposition is
  `12-SYNTHESIS.md` + owner review.
- **grade:** DEMONSTRATED

## OW-8 — `prompt_handoff` two-producer precedence

- **Open:** contract declares `produced_by: [prompt-handoff, handoff]`; no
  precedence rule; ADR 0009 governs naming only.
- **Boundary:** authority seam H.
- **Decision owner:** agent-decidable (add a precedence note) or
  sensemaking-docs-reconciler with user approval.
- **State:** latent, low blast radius.
- **grade:** DERIVED

---

## What is NOT listed here (and why)

- Ordinary feature backlog / PM sub-pipeline issues — no architectural-ownership
  intersection.
- Test flakiness, lint, docs typos — not architectural.
- Goal A episode execution — a *scope/authorization* state, not open
  architectural work (`RC-6`); explicitly out of this prototype.
- Issue #226 study completion — research continuation (`RC-4`), tracked there.

## Pattern across OW-1..OW-8

Six of eight open items are **"policy decided, mechanism lags"** or
**"mechanism exists, policy lags"** — i.e. *authority/lifecycle mismatches*,
not missing features. This is the class of problem a rich authority+lifecycle
representation is best positioned to surface, and the weakest for a plain
dependency graph. (Feeds `09` Q5 and `12` Q5.)
