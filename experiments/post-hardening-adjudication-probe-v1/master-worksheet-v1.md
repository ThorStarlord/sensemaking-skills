# Master adjudication worksheet v1 - post-hardening blinded comparison

Packet: experiments/post-hardening-adjudication-probe-v1/packets/<repo-id>/
Read order per packet: fixture/ -> brief-A.md -> brief-B.md. Record answers below or in each packet's worksheet.md.
Keep sealed-key.yaml closed until all 16 rows below are complete.

## Canonical weakness types (for Q1)
- Zero Validation: functionality exists but nothing checks it
- Contract Mismatch: declared interface vs actual behavior disagree
- Implicit Dependencies: hidden coupling / ordering / environment assumptions
- Ghost Features: documented product surface with no reachable implementation
- Vocabulary Drift: docs describe code as it used to be
- Safety Gaps: consequential operations without gates
- Orphaned Examples: examples/docs pointing at removed code
- Other / undecidable

## Per-repo questions
- Q1: most defensible weakness type (one of the above)
- Q2: more useful/accurate brief (A / B / no material difference)
- Q3: defensibility of each brief's chosen type (defensible / partially / not defensible)
- Q4: A/B difference material or cosmetic (material / cosmetic / cannot tell)
- Q5 (fog-relevant packets only, marked *): fog label defensible/useful, or wrong axis?
- Q6: blinding check (A / B / not sure)

| # | Packet | Q1 type | Q2 (A/B/none) | Q3-A | Q3-B | Q4 | Q5* | Q6 | min | conf |
|---|--------|---------|---------------|------|------|----|-----|----|-----|------|
| 1 | backend-service |  |  |  |  |  |  |  |  |  |
| 2 | full-stack |  |  |  |  |  |  |  |  |  |
| 3 | multi-language |  |  |  |  |  |  |  |  |  |
| 4 | poorly-documented * |  |  |  |  |  |  |  |  |  |
| 5 | multi-executable |  |  |  |  |  |  |  |  |  |
| 6 | hidden-coupling |  |  |  |  |  |  |  |  |  |
| 7 | strong-ui-fog |  |  |  |  |  |  |  |  |  |
| 8 | tiny-lib |  |  |  |  |  |  |  |  |  |
| 9 | unusual-layout * |  |  |  |  |  |  |  |  |  |
| 10 | adv-unused-dep |  |  |  |  |  |  |  |  |  |
| 11 | web-frontend * |  |  |  |  |  |  |  |  |  |
| 12 | generated-heavy * |  |  |  |  |  |  |  |  |  |
| 13 | adv-misleading-readme * (calibration) |  |  |  |  |  |  |  |  |  |
| 14 | docs-heavy-code-light * (calibration) |  |  |  |  |  |  |  |  |  |
| 15 | monorepo (calibration) |  |  |  |  |  |  |  |  |  |
| 16 | stale-readme (calibration) |  |  |  |  |  |  |  |  |  |

Rows 1-12: primary contested set (10 boundary-changed + 2 fog-only flips). Rows 13-16: calibration.
When the table is complete, open sealed-key.yaml, map A/B to baseline/candidate, and apply the
precommitted decision rules in experiments/post-hardening-decision-probe-v1/probe-design-v1.md section 6.
