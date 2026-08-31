# PR #242 Close Note — Product Hypothesis B (Conditional Representation) — 33530fd

**Branch:** `phb-conditional-representation-candidate` @ `33530fd` (c104a81 + H3 vg fix)
**Research program:** `docs/research/control-model-research-agenda.md` — detailed-architecture question: do we need detailed map by default or only when warranted?
**Experiment:** Product Hypothesis B — `materialize additional representation only when warranted` (PARTIAL, FULL deferred, CONTEXT.md:146-159)

## What was proven (evidence-backed)
- Dogfood brief on sensemaking-skills: `vg 0.67 Contract Mismatch` identified as weakest boundary, `ce 0.05` clean, `fixtures 1.0`
- H1: PARTIAL rarely needs FULL — supported (sensemaking-skills → SUFFICIENT, auteur 296 docs/109 historical → INSUFFICIENT_BOUNDED needing PARTIAL, neither needed FULL)
- H2: Warrant stability — predicted 30-40% disagreement, observed 0% (2 pairs, 4/4 agreed, correctly diverged by repo) — warrant more stable than guessed on these cases, but n=2 too small to harden schema (CONTEXT.md:321)
- H3: vg credibility debt — `vg 0.67 → 0.0` via `.github/workflows/validation.yml:639` Level 6, probe `ci_enforcement()` 6/6 overlap, exact-head CI green on 33530fd (all tests pass) — repair-verified

## What this does NOT claim
- FULL detailed architecture not needed yet, not proven unnecessary universally
- Warrant schema not promoted — agenda defers until repeated stable semantics + manual burden
- Domain-general control kernel not extracted — H4 (generalization) still open (tested on 1 framework + 1 product, need more)

## Verdict for PR #242
**Experiment done as bounded vertical slice.** Conditional representation (shallow → PARTIAL when needed, FULL deferred) is viable and measurably cheaper than always-detailed. PR can close/merge as experiment, research program stays open.

## Next warranted slices (if you continue research)
- H4: Test conditional on 1 truly non-framework product repo (different domain)
- Need 3+ more H2 pairs to claim warrant stability for schema promotion
- Do not promote to workflow/schema until hardening rule met

Artifacts: `artifacts/hypotheses-conditional-representation.md` (H1-H3 verified), `artifacts/probe-report-auteur.yaml`, brief `c104a81` dogfood
