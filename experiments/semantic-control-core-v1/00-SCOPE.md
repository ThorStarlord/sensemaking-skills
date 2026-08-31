# 00 — SCOPE: SEMANTIC CONTROL CORE V1 (compression prototype)

**Prototype id:** `SEMANTIC_CONTROL_CORE_V1` · terminology:
`THIN_SEMANTIC_CORE_CANDIDATE` (not `PERSISTENT_SEMANTIC_CORE`).

**Not:** product architecture, an ADR, a Skill, a workflow, persistence,
`repo-sensemaker` v2, PHB `FULL`, Goal A / #218 / #226 evidence, a new
experiment campaign.

## Starting-state guard (authorization Section 5)

| Fact | Value |
|---|---|
| Authorization canonical SHA | `ba8968ca1a12caa90ce7beb0ee5fd2dfac055f37` |
| `origin/main` at V1 start | `ba8968ca1a12caa90ce7beb0ee5fd2dfac055f37` — **no movement** |
| V1 branch | `research/semantic-control-core-v1` (worktree `H:/GithubRepositories/smk-scc-v1`), branched from canonical `main` @ `ba8968c` |
| V0 reference (read-only) | PR #244 · branch `research/detailed-repository-architecture-prototype-v0` · head `f7b0d344640721249aaa14c5bbf8061523bd26b7` · root `experiments/detailed-repository-architecture-v0/` (16 files, 2804 lines) |
| V0 parentage | **not** branched from, merged, or cherry-picked. V0 read through its committed head only. |

## The compression question (authorization Section 2)

V0 answered: *a deliberately rich repository representation exposes useful
decision-relevant information, but the useful information is sharply
concentrated.*

V1 asks: **can we discard most of V0 and preserve almost all of the observed
decision-relevant value in a very small semantic core, generating richer
detail only when a specific question requires it?**

## V0 finding being challenged (authorization Section 3 — to preserve)

- **A. Authority seams** — DEFINES / ENFORCES / RUNTIME-OWNS / WINS-ON-CONFLICT
  / POLICY-vs-IMPL.
- **B. Lifecycle / supersession** — especially where something is physically
  present after losing semantic authority.
- **C. Enforcement gaps** — declared-but-unenforced, multiply-enforced,
  duplicated authority, impl-ahead-of-policy, policy-ahead-of-impl, mirror drift.
- **D. Research → product crossings** — only where a research result actually
  reaches a runtime/product path.
- **E. On-demand cross-cutting impact** — "if semantic object X changes, which
  regions must be inspected?" — produced on demand, not stored.

## V1 files (target 3–6; this is 6)

| File | Role |
|---|---|
| `00-SCOPE.md` | this file |
| `SEMANTIC-CONTROL-CORE.md` | the thin core: authority-seam register + lifecycle ledger + enforcement-gap register + research→product edges. One authoritative row per concern. Markdown tables. |
| `ON-DEMAND-PROJECTION-RECIPE.md` | implementation-neutral procedure for answering questions the core cannot |
| `V1-FREEZE-MANIFEST.md` | represented SHA + SHA-256 of every frozen V1 artifact + freeze declaration |
| `COMPRESSION-EVALUATION.md` | V0 regression replay (10 cases) + 2 holdouts + 1 current-state projection drill + staleness classification |
| `SYNTHESIS.md` | the 12 synthesis answers + `V1_ARCHITECTURE_DISPOSITION` |

## What V1 tries to delete (authorization Section 4 — removable unless proven otherwise)

Exhaustive component enumeration · low-salience `does_not_own` lines · broad
STRUCTURAL `CALLS/DEPENDS_ON/CONTAINS` graphs · producer/consumer rows
trivially recoverable from registries · restated operating-flow prose · the
full research-claim map · per-experiment claim ceilings already in source
artifacts · current SHAs/counts/status detail that decays · hand-maintained
nested rich YAML · general overview material already in `CONTEXT.md` / `AGW`.

## Boundaries (authorization Sections 7, 26, 29–32)

No edit to `experiments/detailed-repository-architecture-v0/` (incl. the frozen
`EVIDENCE-INDEX.yaml` typo). No merge/close of PR #244. No product/runtime/
validator/probe/contract/PHB/ADR change. No infrastructure. No new campaign.
Markdown tables preferred; any YAML strict-parsed before freeze; one
authoritative row per fact; reference evidence, don't copy it.

## Epistemic grades (authorization Section 12)

`DEMONSTRATED` (direct repo evidence) · `DERIVED` (from ≥2 demonstrated facts) ·
`INTERPRETIVE` (contestable modeling judgment) · `HYPOTHESIS` (unresolved).
Every load-bearing V1 row carries one.
