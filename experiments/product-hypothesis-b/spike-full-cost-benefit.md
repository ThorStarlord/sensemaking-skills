# Spike: FULL Detailed Architecture vs PARTIAL — Cost/Benefit

**Date:** 2026-08-30
**Hypothesis tested:** H1 — "We need detailed architecture by default" vs "PARTIAL (add detail only when warranted) is sufficient"
**Method:** One throwaway FULL slice on `auteur` `author_decisions` subsystem (consequences.py/context.py/models.py), compared to PARTIAL baseline (narrative-architecture.md + 2 ADRs)

## PARTIAL baseline (already done)
- Read: `docs/narrative-architecture.md:1-40` layers 0-4, plus `probe-report-auteur.yaml:54` (296 docs/109 historical, 376 churn)
- Decision: `architecture_fog` — docs sprawl + churn in author_decisions → `docs-aligner` + `to-prd`
- Cost: ~5 min, 3 files, 0 code

## FULL prototype (throwaway)
- Built: `spike-full-auteur-graph.py` — 42 lines, 22 nodes (layers + scopes + 4 files), 5 edges, mapped L1 Identity (models.py) → L3 Realization projection (context.py M2 fail-closed) → L3 consumer (consequences.py)
- Files read: narrative-architecture.md, models.py, context.py, consequences.py, ADR 004/010/015 — 5 files, 18 min
- Graph confirmed: churn is *contained* in L1→L3 fail-closed M2 contract, not systemic Layer 0/2 drift.

## Result
- **Did FULL change next warranted responsibility?** **No** — still `architecture_fog`, still `docs-aligner`, only narrowed scope to `author_decisions` M2 contract.
- **Cost:** 18 min / 42 lines / 5 files for 0 decision change
- **Benefit delta:** Narrower scope (whole-repo → subsystem) — useful nuance, but not decision-changing per `CONTEXT.md:146` warrant criteria

## Replication #2 — structure subsystem (2026-08-30, spike-full-structure-graph.py)
- Built: 38 lines, 27 nodes, 3 edges — `analyzer.py` (L2 diagnostics run_all_diagnostics), `bible_audit.py` cross-layer, `proposal_models.py` L2 plans
- Files: 5, 15 min
- Graph: structure analyzer is well-bounded L2 diagnostics with fail-closed rules (diagnostics.py); churn c996f84 is additive F3 thematic contribution, not systemic drift
- Did FULL change decision? **No** — still architecture_fog → docs-aligner, narrowed to structure L2 proposal/diagnostic contract

## Replication #3 — genre_pipeline subsystem (2026-08-30, spike-full-genre-pipeline-graph.py)
- Built: 35 lines, 22 nodes, 3 edges — `runtime.py` orchestration, `identity.py` L1 compilation, `registry.py` L0 vocabularies
- Files: 5, 14 min
- Graph: cross-cutting orchestration per narrative-architecture.md ("Validation, orchestration... operate across layers"), correctly separated L0 registry vs runtime — no layer violation
- Did FULL change decision? **No** — still architecture_fog → docs-aligner, narrowed to genre_pipeline orchestration boundary

## Aggregate (3/3 replications)
- Total FULL cost: 42+38+35 = 115 lines, 47 min, 15 files read
- Total PARTIAL cost: ~5 min each (15 min)
- Decision change: **0/3** (CONTEXT.md:321 hardening bar met for "conditional as default" — repeated useful responsibility with stable semantics but no decision change, so formal FULL schema not warranted)
- All 3 show same pattern: FULL yields *narrower scope nuance*, not new workflow

## Conclusion for research program
- **PARTIAL sufficient as default** — 3/3 replications support H1 with durable evidence. Building FULL is measurable but not warrant-changing for these subsystems.
- Repository `experiments/*` sprawl confirmed: diagnosis loops saturated; constructive spikes were the only evidence that moved the question.
- Do not promote FULL to formal schema/workflow; keep conditional + warrant gate per CONTEXT.md:146-159.

## Recommendation
Hardening met — document "conditional as default" in research agenda as warranted pattern, keep FULL deferred until a future spike shows decision change.
