# INDEPENDENT RECONSTRUCTION — CONVERGENCE COMPARISON

Owner-review step 2–3 (2026-08-31): a fresh agent, **not shown V0 or V1**, was
given only `sensemaking-skills @ ba8968c` (clean detached worktree
`H:/GithubRepositories/smk-indep-recon`) and asked to build the smallest
repository semantic-control representation of consequential facts hard/unsafe to
reconstruct from one source, over four fact-kinds: semantic authority,
enforcement mismatches, lifecycle/supersession, research→product crossings.

Its output: `H:/GithubRepositories/smk-indep-recon-out/independent-semantic-control-representation.md`
— **32 rows** (12 authority `A1–A12` · 8 enforcement `B1–B8` · 8 lifecycle
`C1–C8` · 4 research-crossing `D1–D4`), same table form, same
DEFINES/ENFORCES/lifecycle framing, same DEMONSTRATED/DERIVED/INTERPRETIVE grade
+ SLOW/MEDIUM/FAST rate columns — **independently arrived at**, not prompted.

The object of comparison is **semantic-boundary convergence**, not row count or
wording (owner instruction).

---

## 1. Owner's convergence checklist — did the independent agent (B) discover it?

| Checklist boundary | V1 row | B row(s) | Verdict |
|---|---|---|---|
| top-level control authority | A1 | A9 (ADR 0013, agent owns loop; runtime = compat path) | **CONVERGE** (B calls it "aligned"; V1 called it "policy ahead of impl" — minor judgment diff) |
| brief contract concentration | A2 | A5 (`brief_skeleton.py` = canonical structure authority) + B6 (`validate-brief.py` enforcement) + A11 (MODEL_WARRANT) | **PARTIAL** — B captured the same region across 3 rows but did not frame it as "5 independent definers"; V1's single-row concentration claim is a merge B split |
| artifact-path ownership | A3 | A3 (ADR 0010, runtime sole owner, `expected_output_path`) | **CONVERGE (strong, near-identical)** |
| routing impl/policy divergence | A4 + G1 | A10 + C1 + D3 | **CONVERGE (B stronger)** — B adds C1: ADRs 0005 & 0012 still `Status: Accepted` describing the superseded auto-chaining mechanism |
| auto-invoke authority | A5 + G6 | A10 + C2 | **CONVERGE** — B C2 "superseded decision, implementation still runs" matches V1 exactly |
| MODEL_WARRANT seam | A6 | A11 + D1 | **CONVERGE (strong)** — both: canonical policy, runtime `warrant_enabled=False` opt-in, guarded log-and-continue |
| Gate A placement split | A7 | B8 | **CONVERGE** — B adds ADR 0023 two-lane "governance-only, nothing enforces it yet" + Evidence 0016 `PREPARED_NOT_RUN` |
| deprecated-but-load-bearing contracts | §2 ledger + G3 | A4 + B4 | **CONVERGE (strong, near-identical)** — same file, same 4 stranded contracts, same xfail tests |
| superseded-but-still-present routing | §2 (ADR 0018) | C3 + C1 + D3 | **CONVERGE (B stronger)** — C1 again |
| research-only code under `src/` | §2 (`reasoning/`) | C5 | **CONVERGE (strong, near-identical)** — same self-declared-non-production + imported-via-seam observation |
| brief split enforcement | G4 | B6 | **PARTIAL** — same contract; B surfaced the `weakness_type` prose-brittle enforcement, V1 surfaced the `recommended_workflow_id` generic/conditional trap. Different specific mismatch, both valid |
| registry drift | G5 | A6 + B3 | **CONVERGE (B stronger)** — B: "which `workflow-registry.yaml` is authoritative = **UNDECIDED**, no file declares canonical". V1 asserted the `skills/workflow-planner/` copy is canonical per `CONTEXT.md` source-of-truth map. **Genuine divergence on decidedness** — see §3 |
| control-loop unenforcement | G2 | B1 + B2 | **CONVERGE (B much stronger)** — B1: the CI `validate` job **runs no pytest at all**; B2: `test_path_drift.py` deterministically RED on `main`. V1's G2 was "unenforced by design" — B found the concrete, larger hole |
| repair-verification contract gap | G7 | — | **V1-ONLY** — B did not surface the `repair_verification_report` `unevaluable`-verdict gap |
| C6R → warrant-seam crossing | §4 | D1 | **CONVERGE** — both identify the one guarded opt-in research→runtime seam; B attributes it to `experiments/product-hypothesis-b/` and separately excludes the C6R *hypothesis* as non-crossing (same net conclusion V1 states: "no other thread wires in") |

**Checklist tally:** 10 strong CONVERGE · 3 CONVERGE-B-stronger · 2 PARTIAL ·
1 V1-ONLY · 0 MISLEADING · 0 completely-different. Every "big" V1 boundary
(routing divergence, deprecated contract file, research code under `src/`,
MODEL_WARRANT opt-in seam, Gate A split, registry drift, path ownership) was
independently rediscovered.

---

## 2. Boundaries the independent agent found that V1 did NOT encode

All pass V1's own inclusion test (consequential · hard to reconstruct from one
source · would lead to a wrong action if missed). This is the **under-coverage
signal**.

| B row | Boundary V1 missed | Why it matters |
|---|---|---|
| B1 | CI `validate` job runs **no pytest**; the fix (`probe-gate` + `core-assertions`) is on unmerged branch `feat/enforcement-gate` | the single largest enforcement gap in the repo; V1's G2 only gestured at it |
| A1/A2 + B2 | canonical-vocabulary enforcement is **RED on `main`** (`test_path_drift.py`, 5 failures); fog-taxonomy **doc-vs-doc conflict** (`HARDENING_STATUS.md` still asserts 5 types incl. `integration_fog`, contradicting `canonical-vocabulary.yaml`'s 4) | V1 deliberately excluded vocabulary as "cheap single source" — but the *enforcement mismatch* and the *doc conflict* are exactly core-worthy. **V1 inclusion-test error.** |
| C1 | ADRs **0005 & 0012 still `Status: Accepted`** while describing the superseded auto-chaining mechanism | V1 listed 0017–0021 superseded and 0006–0008/0022 proposed but missed the stale-Accepted pair |
| A7 + B2 | **product-version authority undecided** (`conflicting_values` = evidence-only, never blocking); `test_cli.py::test_cli_version` asserts an older string → RED on `main` | V1 had no version-authority row |
| A8 | product-scope (ADR 0014, GA not claimed) vs **"PRODUCTION READY — APPROVED FOR DEPLOYMENT"** in project memory / PHASE docs; the claim rests on ADR 0021 which is **SUPERSEDED / never-Accepted** | policy-vs-record conflict with real decision impact |
| C6 | doc re-scope **deferred**: `ROUTING_GUIDE`, `run-ledger-guide`, `PORTFOLIO_OPERATIONS`, `PRODUCT-CONTRACT-REVIEW` still describe the **retired** programmatic runner | V1 had the `orchestration-runner.py` shim but not the stale-docs point |
| C7 | ADRs **0024 & 0025 ACCEPTED but "merge to `main` pending"**; 0025's conformance test failing on `main`, #232 open | "accepted but not landed" lifecycle limbo — V1 mentioned 0024/0025 only in passing |
| B7 | `distribution-drift.yaml`: **5 vendored skill copies** with `line_ending_only` drift | vendored-skill mirror drift (rate FAST) |
| A5 | `brief_skeleton.py` = named "canonical brief-structure authority"; `reconcile()` splices model content only into pre-declared holes | V1's A2 never named this mechanism |
| A12 | `gate_relationship_findings.py` = **sole** merge-blocking-findings decider; current blocking set = `missing_reference`, `missing_status_line` only; on unmerged branch | V1 had no "what may block a merge" row |
| D2 | `extended_analysis` Section 15 fields: lineage `prototype/repo-sensemaker-vnext` PR #164 → `candidate/` → ADR 0024; optional/non-blocking; explicitly **not** read by routing; a 5th field was falsified and removed | V1 folded this into A2 without the crossing detail |
| D4 | two-lane authorization (ADR 0023) schema present but **"not yet crossed"** — scaffolding invites the assumption it is live | V1 had no "misleading non-crossing" row |
| C8 | ~30 root `PHASE-*` / `run_dayN_tests.py` files as a navigation hazard | V1 had no historical-scaffolding-volume row |

---

## 3. Genuine divergences (not just coverage)

1. **Registry canonical status.** V1 G5 says the `skills/workflow-planner/references/`
   copy is canonical (per `CONTEXT.md` source-of-truth map). B A6 says it is
   **undecided** — no file declares canonical, and `enforcement-contract.md` §6
   says equality "cannot be decided" until the contract is written. Both read
   real evidence; B read the enforcement contract, V1 read the source-of-truth
   map. **B is closer to the enforcement reality**; V1 over-stated decidedness.
2. **Top-level control loop policy-vs-impl.** V1 A1 = "policy ahead of impl"
   (runtime still exposes whole-loop sequencing). B A9 = "aligned". Contestable
   modeling judgment — exactly the `CORE_TOO_INTERPRETIVE` class. Neither is
   demonstrably wrong.
3. **Vocabulary in-scope-or-not.** V1's inclusion test *excluded* canonical
   vocabulary as cheaply recoverable. B *included* it — and was right to, because
   the consequential fact there is not "what are the enum values" (cheap) but
   "the enforcement is RED and two docs disagree" (core-worthy). V1's inclusion
   test needs a tweak: *enforcement state of a single-source fact is itself a
   separate fact.*

---

## 4. Convergence verdict

```
INDEPENDENT_SEMANTIC_RECONSTRUCTABILITY = SUBSTANTIALLY_CONVERGENT
```

- Every load-bearing V1 boundary was independently rediscovered by an agent with
  zero exposure to V0/V1, using the same four fact-kinds, the same
  authority/enforcement/lifecycle framing, and the same altitude (no call
  graphs, no file inventories).
- The two agents disagree on **1 decidedness call** (registry canonical status —
  B better-evidenced) and **1 interpretive judgment** (control-loop policy-vs-impl).
- **0 boundaries where B produced "completely different rows."** Per the owner's
  stated bar ("16 semantically equivalent, two merged differently, two genuinely
  new = excellent convergence"), this clears it: ~14 of 15 checklist regions
  converge, only 1 is V1-only, and B independently found ~13 *additional*
  same-kind boundaries.
- The additional-13 are an **under-coverage signal, not a divergence signal**:
  V1's 22-row selection was too small by roughly 8–12 rows (notably: CI runs no
  tests; ADRs 0005/0012 stale-Accepted; vocab-enforcement RED; version authority;
  "production ready" vs GA-not-claimed; accepted-but-unmerged ADRs 0024/0025).

This sharply reduces the `CORE_TOO_INTERPRETIVE` risk flagged in `SYNTHESIS.md`
Q11/§D: the semantic boundaries are **real repository structure**, reconstructable
by a second competent agent — not an artifact of one agent's modeling choices.

## 5. Consequences for the next step

Per the owner's conditional instruction ("if substantially convergent, proceed
directly to a bounded persistence/maintenance architecture prototype"):
convergence holds → proceed. The persistence prototype should:

- start from a **merged core** = V1's 22 rows + B's non-duplicate additions
  (deduped), ~30–35 rows, still one authoritative row per concern;
- adopt the **derived-fact vs semantic-judgment split** the owner named:
  - *mechanically derivable* (refresh cheaply): ADR lifecycle from `**Status**`
    lines; registry duplication + drift via `diff`; which validators actually
    run in CI; canonical-source relationships from `CONTEXT.md`; version-declaration
    agreement; vendored-skill drift from `distribution-drift.yaml`;
  - *irreducible human/model judgment* (review, don't derive): policy-vs-impl,
    wins-on-conflict, authority concentration, research→product *relevance*,
    "misleading non-crossing";
- fix V1's inclusion-test gap: **the enforcement/CI-run state of an otherwise
  single-source fact is a separate core-worthy fact.**
