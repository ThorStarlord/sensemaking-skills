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

## Conclusion for research program
- For this slice, **PARTIAL sufficient** — building FULL did not reveal a new failure or change the workflow. This supports the conditional model (H1) on this repo, but as a *single spike* it does not generalize.
- Repository full of `experiments/*` and `artifacts/*` is itself evidence: more briefs would not have revealed this; only building one FULL slice did.
- If you repeated this on 2 more subsystems (e.g., `structure` vs `genre_pipeline`) and still got 0 decision change, you'd have durable evidence that detailed architecture is rarely warranted by default — exactly the hardening rule (`CONTEXT.md:321`).

## Recommendation
Do not promote FULL to formal schema/workflow yet. Keep conditional as default; next warranted spike (if any) is on a different subsystem to test if result replicates.
