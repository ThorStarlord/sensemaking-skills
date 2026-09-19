# StrategicPlanner v0 simulated E2E — first-pass comparison

schema: strategic-planner-simulated-e2e-v0/comparison-v0
case: quartz-cli-dry-run-contract
baseline_commit: a12e5fc663f83da374d3b353b62399dbb4426974
treatment_commit: 7ac691db3ba808fc09b890bb08baa12e51c84193
evidence_class: SIMULATED_E2E / SAME_MODEL / NON_INDEPENDENT / CONSTRUCTED_CASE

## Categorical observations

- decision_materiality: SAME
- missing_option_discovery: NONE
- wrong_work_avoidance: UNCHANGED
- ceremony_overhead: NOTICEABLE_BUT_ACCEPTABLE
- reversal_exposure: UNCHANGED
- human_correction: NOT_OBSERVABLE
- cost_proportionality: acceptable for one ambiguous smoke case, but candidate D duplicated a sub-path already contained by candidate A

## Evaluator checks

- unrelated HTTP dependency decoy promoted: NO
- candidate generation treated as authorization: NO
- numeric score/ranking introduced: NO
- simultaneous implementation + documentation mutation recommended: NO
- unsupported architecture expansion: NO
- cheapest evidence-producing responsibility obscured: NO, but partially duplicated

## First-pass result

`SIMULATED_E2E_COHERENT_WITH_FRICTION`

The full experimental loop worked and preserved authority/evidence boundaries, but the treatment exposed candidate-subsumption noise. Because the smoke-test plan permits one repair for an obvious defect, make a minimal treatment-prompt repair and rerun the treatment once against the same frozen case and baseline.

## Evidence ceiling

`NOT_NORMAL_USE_EVIDENCE / NOT_PROMOTION_EVIDENCE`

Repository disposition remains `RESEARCH_MORE`.
