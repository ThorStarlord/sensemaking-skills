# Erratum v1 - phase15 per-repository classification-tool defect

```
schema: post-hardening-decision-probe-v1/erratum-classification-tool-v1
type: append-only erratum. No historical artifact was edited; the hardening workstream
  stays closed and frozen.
chain: original report -> classification-tool defect discovered later -> corrected
  interpretation -> primary gate/disposition unchanged
date: 2026-08-07
```

## Original report

phase15-comparison-v1.yaml (repeated in final-disposition-v1.yaml and
phase19-evaluation-report-v1.yaml) published the per-repository summary:

```
IMPROVED 11 / UNCHANGED 10 / REGRESSED 4
```

## Defect discovered later (post-closure, during post-hardening-decision-probe-v1)

tools/phase15_compare.py:150-158 classifies each repository's state with a default
`state = "IMPROVED"` fallthrough that is never downgraded when the weakness-type label
regressed while fog stayed correct. Six repositories are therefore mislabeled IMPROVED
despite a boundary-type regression (correct -> wrong vs ground truth):

- backend-service   (Zero Validation -> Implicit Dependencies)
- full-stack        (Contract Mismatch -> Ghost Features)
- multi-language    (Ghost Features -> Implicit Dependencies)
- multi-executable  (Implicit Dependencies -> Ghost Features)
- hidden-coupling   (Implicit Dependencies -> Vocabulary Drift)
- strong-ui-fog     (Zero Validation -> Implicit Dependencies)

## Corrected interpretation

```
IMPROVED 5 / UNCHANGED 10 / REGRESSED 10
```

5 genuine improvements: tiny-lib, docs-heavy-code-light, adv-misleading-readme,
adv-unused-dep, adv-partial-impl. Boundary regressions 7 vs boundary improvements 3.

## Primary gate and disposition unchanged

The charter improvement gate failed independently of this classification, from the
frozen scorer directly:

```
unsupported_claim_rate    0.632 -> 0.633   FAIL (flat)
evidence_precision        0.844 -> 0.835   FAIL (flat)
weakest_boundary_accuracy 0.640 -> 0.440   FAIL (real decline)
```

Workstream remains CLOSED - REVISE. This erratum changes understanding of WHERE the
regression occurred (broader than the published 4 repos) and therefore what the next
probe must cover; it does not change WHETHER the gate failed or the disposition.

## Full analysis and consequence for the probe

See evidence-map-v1.md section 8 (corrected per-repository accounting) and
probe-design-v1.md section 2 (the contested set covers all 10 boundary-changed repos).