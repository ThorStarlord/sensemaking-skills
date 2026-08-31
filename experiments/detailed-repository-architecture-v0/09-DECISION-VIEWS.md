# 09 — PROSPECTIVE DECISION VIEWS (DETAILED_REPOSITORY_ARCHITECTURE_PROTOTYPE_V0)

Current architecture questions that genuinely matter to `sensemaking-skills`,
answered against **frozen V0** (`ba8968c`). No synthetic scenarios. Answers are
not converted into implementation work (authorization Section 18).

Per question: **ANSWER** · **REPRESENTATION_ELEMENTS_USED** ·
**RAW_EVIDENCE_STILL_NEEDED** · **grade**.

---

## Q1 — Where are the strongest current semantic-authority concentrations?

- **ANSWER:** Ranked in `05-AUTHORITY-MAP.md`:
  1. `repository_sensemaking_brief` contract — **5 defining sources**
     (contracts file, ADR 0014, ADR 0015 addendum, ADR 0024, evidence-rules.md
     Rule 7), **2 enforcers** with a deliberate generic/conditional split,
     widest artifact fan-out (4 consumers + a fan-in target), historically
     defect-prone.
  2. Automatic fog-type routing — 1 defining source (SUPERSEDED), 0 enforcers,
     largest impl-ahead-of-policy gap.
  3. MODEL_WARRANT / `representation_sufficiency` seam — the research→product
     boundary passes straight through it; the authorization forbids changing it.
- **REPRESENTATION_ELEMENTS_USED:** authority seams (DEFINES/ENFORCES counts),
  concentration ranking, artifact-flow centrality.
- **RAW_EVIDENCE_STILL_NEEDED:** none for the ranking; the exact reconciling
  comment blocks in `artifact-contracts.yaml:145-180` if editing the contract.
- **grade:** DERIVED (ranking) over DEMONSTRATED (each seam).

## Q2 — Which artifact contracts have multiple independently-changing owners?

- **ANSWER:** Two clear cases.
  (a) `repository_sensemaking_brief`: 5 independent owners that have each
  changed on their own cadence (ADR 0015 addendum and ADR 0024 landed months
  apart; evidence-rules Rule 7 came from Issue #171). (b) `prd` / `issue_list` /
  `agent_brief` / `code_patch`: split between the canonical contracts file and
  the **deprecated** `workflow-orchestrator/references/` copy (INFRA-004) —
  ownership is not just multiple, it is *contradictory* (one owner says "delete
  me").
- **REPRESENTATION_ELEMENTS_USED:** `05` multiply-governed list, `06` §4
  registry-duplication table, `02` `duplicate_at` fields, `08` OW-4.
- **RAW_EVIDENCE_STILL_NEEDED:** git history of `artifact-contracts.yaml` to
  confirm independent change cadence (V0 asserts it as DERIVED).
- **grade:** DEMONSTRATED (that multiple owners exist) / DERIVED (independent cadence).

## Q3 — Which product responsibilities repeatedly cross Skill / runtime / validator boundaries?

- **ANSWER:** Three.
  (1) **Brief production** — repo-sensemaker (produce) → runtime (path
  resolution + opt-in warrant seam + routing-field reads) → validate-artifact +
  validate-brief (enforce, split). (2) **Plan production** — workflow-planner
  (produce) → runtime (`generate_plan` provisional / `finalize_plan` canonical,
  ADR 0025) → validate-plan (only finalized). (3) **Repair verification** —
  repair-verifier (produce) → probe engine (re-probe) → its own contract (no
  `unevaluable` verdict). Each is a skill-owned artifact whose *lifecycle* is
  co-managed by the runtime and split-enforced.
- **REPRESENTATION_ELEMENTS_USED:** `04` X (transform) edges all in the runtime;
  `03` structural + validation edges; `01` "load-bearing pairs".
- **RAW_EVIDENCE_STILL_NEEDED:** none for identification.
- **grade:** DEMONSTRATED.

## Q4 — Which research conclusions still influence canonical product behavior?

- **ANSWER:** Exactly **one** — RC-1 (`C6R` compressed control hypothesis) via
  the single opt-in seam `reasoning/warrant_gate.py` → `workflow-runtime`
  `warrant_enabled`. Every other research thread (RC-2..RC-8) is upstream of
  product behavior: they inform ADRs / CONTEXT.md / priorities but do not wire
  into a runtime path. RC-8 (PHB conditional representation) influenced a
  *documentation* hardening (`CONTEXT.md:321`) but no code path.
- **REPRESENTATION_ELEMENTS_USED:** `07` "current canonical relevance" rows,
  `03` RESEARCH family + the `infra.reasoning-slice CALLS`/`DERIVES_FROM` edges,
  `05` row K.
- **RAW_EVIDENCE_STILL_NEEDED:** confirm `warrant_enabled` default (V0 says
  opt-in / off-by-default; grep of call sites shows it is a constructor kwarg
  `warrant_enabled: bool = False`).
- **grade:** DEMONSTRATED.

## Q5 — Which currently-live areas have the greatest architecture-to-documentation divergence?

- **ANSWER:** Ranked:
  1. Automatic fog-type routing — runtime + registry implement a chain the
     canonical docs (ADR 0014/0018/0026, CONTEXT.md) explicitly refuse to
     ratify. **Impl ahead of policy.**
  2. `auto_invoke_next_workflow` — now doctrinally aligned (ADR 0026) but the
     field + 2 mirrors + 2 consumers physically remain.
  3. Gate A consumer placement — mechanism real, ADR 0022 still PROPOSED.
     **Impl ahead of policy on placement.**
  4. Two `workflow-registry.yaml` copies with real content drift, no parity
     check.
  5. Deprecated contract file still canonical for 4 PM/engineering artifacts.
- **REPRESENTATION_ELEMENTS_USED:** `05` POLICY-vs-IMPL column (the single
  most productive column in V0), lifecycle grades, `06` §4, `08`.
- **RAW_EVIDENCE_STILL_NEEDED:** none to rank; specifics per item to act.
- **grade:** DERIVED.

## Q6 — Which relationships would have to change if `representation_sufficiency` semantics changed?

- **ANSWER:** V0 lets you enumerate the blast radius without changing anything:
  - `03`: edge `E-ADR-0015 ... representation_sufficiency -> MODEL_WARRANT`,
    edge `runtime CALLS infra.reasoning-slice (opt-in seam)`, edge
    `infra.reasoning-slice DERIVES_FROM doc.control-model-research-agenda`.
  - `04` brief row: the `X (opt-in seam)` transform, the `representation_sufficiency`
    + `outcome` reads, the INCONCLUSIVE→routing-block.
  - `05` row B (RUNTIME-OWNS = MODEL_WARRANT decision) + row K + concentration #3.
  - `02`: `runtime.workflow-runtime`, `infra.reasoning-slice`,
    `validator.brief`, `registry.artifact-contracts` (declares the field
    OPTIONAL/ADDITIVE), ADR 0015.
  So: **1 ADR, 1 contract declaration, 1 validator, 1 runtime seam, 1 research
  module, and the 3 warrant-mapping edges.** ~9 nodes/edges.
- **REPRESENTATION_ELEMENTS_USED:** cross-family edge tracing (authority +
  artifact + research + structural touching one field).
- **RAW_EVIDENCE_STILL_NEEDED:** `validate-brief.py` internals for the exact
  parse; `warrant_gate.py` / `vertical_slice.py` for the mapping logic. V0
  scopes the search; it does not replace reading those three files.
- **grade:** DERIVED. *This is the clearest example of V0 doing something a
  dependency graph cannot: assembling a cross-cutting impact set for a single
  contract field.*

## Q7 — Which architectural regions are expensive to understand because the needed relationships are scattered?

- **ANSWER:**
  - **The research→product boundary** — scattered across `CONTEXT.md:146-158`,
    `warrant_gate.py` docstring, `control-model-research-agenda.md`, ADR 0015
    addendum, and runtime code. V0 `05` row K + `07` + the reasoning-slice
    edges collapse it to one place.
  - **The routing-deferral position** — ADR 0014 + 0018 (superseded) + 0026 +
    CONTEXT.md:127/335 + registry flags + runtime chain. V0 `05` row E is the
    single assembly point.
  - **Continuation / cross-run identity** — `AGW:308-318` + retirement-plan
    closure + session_summary contract. V0 covers this only partially (`04`
    session_summary row) — a known thin spot.
- **REPRESENTATION_ELEMENTS_USED:** authority seams as assembly points,
  research-claim map.
- **RAW_EVIDENCE_STILL_NEEDED:** continuation seam still needs the
  retirement-plan doc.
- **grade:** DEMONSTRATED / INTERPRETIVE (which regions are "expensive").

## Q8 — Which current concerns can be answered almost entirely from V0, and which force raw investigation immediately?

- **Almost entirely from V0:** "Is routing ratified?" · "Who owns artifact
  paths?" · "Which research influences product?" · "What's the blast radius of
  a brief-contract field change?" · "Where are the impl/policy divergences?" ·
  "Is `auto_invoke_next_workflow` an authority?" · "Which file defines the
  `prd` contract and is it deprecated?"
- **Force raw investigation immediately:** any question at the level of a
  specific validator *rule* (RC#3), a specific symbol / call site, exact error
  taxonomy (`PROBE_REPORT_NOT_FOUND`), the *contents* of a stranded contract,
  the mapping logic inside `vertical_slice.py`, and anything about test
  behavior. V0 is a **map to the right file + the right question**, not a
  substitute for the file.
- **grade:** DEMONSTRATED.

---

## What these views collectively show

1. **The POLICY-vs-IMPL column and the authority-seam assembly points are where
   V0 pays off.** Q1, Q2, Q5, Q6, Q7 are all answered primarily from `05`.
2. **Cross-cutting impact analysis (Q6) is the single capability V0 has that
   raw inspection makes genuinely expensive.** Every other answer is "V0 saved
   assembly time"; Q6 is "V0 assembled something a human would likely get
   *wrong* by omission."
3. **V0 never fully closes a question that needs rule/symbol-level detail.** It
   consistently narrows the search to one file and one question. That is the
   THIN_PERSISTENT_CORE_PLUS_ON_DEMAND_DETAIL shape showing through.
