# Empirical Skill Qualification v1 — Final Report

**Status:** `TEMPLATE_NOT_EXECUTED`  
**Classification:** `EXPLORATORY_NOT_CANONICAL_EVIDENCE`

> Fill this report only from preserved experiment records. Do not backfill missing
> evidence from memory, candidate-author rationale, or desired outcomes.

## 1. Research question

Does held-out baseline-vs-candidate qualification detect useful improvements or
regressions that the existing Skill-maintenance verification process would not?

## 2. Baseline identity

- Framework repository:
- Baseline framework SHA:
- Target Skill:
- Baseline Skill digest:
- Validator/harness revisions:
- Model/provider configuration:
- Authorization/campaign reference:

## 3. Corpus construction

- Diagnostic set (D):
- Qualification set (Q):
- Untouched test set (T):
- Case-source rationale:
- Known limitations / sampling constraints:

## 4. Split integrity

- Frozen case-manifest digest:
- D/Q/T overlap check:
- Q hidden until candidate freeze: `PASS | FAIL | CANNOT_VERIFY`
- T hidden until Q disposition: `PASS | FAIL | CANNOT_VERIFY`
- Blinding-seed / assignment-map provenance:
- Leakage incidents, if any:

If split integrity materially failed, stop comparative claims here and record an
`INCONCLUSIVE` research outcome.

## 5. Baseline behavior

Summarize baseline mechanical validity and semantic behavior without using candidate
results to reinterpret the baseline after the fact.

## 6. Trigger failure / pressure

- Observed pressure:
- Source cases:
- Why it matters:
- Existing maintenance-process expectation:

## 7. Defect attribution

- Failure-mode class:
- Defect source:
- Was current Skill instruction sufficient?:
- `SKILL_CHANGE | NO_SKILL_CHANGE | INCONCLUSIVE`:
- Evidence:

If `NO_SKILL_CHANGE`, explain which executor/harness/fixture/validator/environment or
other non-Skill cause best accounts for the observation and stop candidate mutation.

## 8. Candidate generation

- Candidate ID:
- Baseline SHA/digest:
- Candidate SHA/digest:
- Source `usage_research_report`:
- Source `skill_improvement_plan`:
- Predicted benefit:
- Candidate-author context boundary:

## 9. Candidate edit budget

- Target Skills modified:
- Files modified:
- Instruction regions modified:
- Full rewrite avoided: `PASS | FAIL`
- Registry unchanged: `PASS | FAIL`
- Artifact contract unchanged: `PASS | FAIL`
- Validator unchanged: `PASS | FAIL`
- Workflow unchanged: `PASS | FAIL`

Any out-of-budget change requires a new candidate identity or experiment disposition;
it must not be silently absorbed into the current candidate.

## 10. Qualification methodology

- Baseline/candidate execution comparability:
- Blind evaluator identity/context:
- Frozen rubric:
- Judgment-commit mechanism:
- Unblinding mechanism:
- Qualification dimensions used:

Do not collapse the qualification vector into one scalar score.

## 11. Q results

For each case preserve the blind judgment and normalized post-unblinding record.

- Mechanical validity:
- Evidence grounding:
- Decision quality:
- Boundary/authority compliance:
- Original-defect behavior:
- Correct-negative preservation:
- Regression materiality:
- Aggregate candidate disposition:

`IMPROVED | EQUIVALENT | MIXED | REGRESSED | INCONCLUSIVE`

Only `IMPROVED` is eligible to proceed to T. Eligibility is not promotion authority.

## 12. T results

If Q did not produce `IMPROVED`, write `NOT_OPENED_BY_PROTOCOL` and do not inspect T.

Otherwise record the same qualification vector used for Q and select one:

- `GENERALIZATION_SUPPORTED`
- `LOCAL_FIX_ONLY`
- `REGRESSION_DETECTED`
- `NO_MATERIAL_DIFFERENCE`
- `INCONCLUSIVE`

## 13. Regressions

List every observed regression, including rejected-candidate evidence. Distinguish
material regressions from cosmetic or non-consequential differences.

## 14. Current-process counterfactual

Would the current Skill-maintenance promotion criteria have made the same apparent
candidate decision before held-out Q/T qualification?

Classify one:

- `CURRENT_PROCESS_AND_NEW_PROCESS_AGREE`
- `NEW_PROCESS_CATCHES_REGRESSION`
- `NEW_PROCESS_ADDS_CONFIDENCE_ONLY`
- `NEW_PROCESS_REJECTS_UNNECESSARY_CHANGE`
- `NEW_PROCESS_ADDS_NO_VALUE`
- `NEW_PROCESS_CREATES_EXCESSIVE_COST`

Explain the evidence for the counterfactual. Do not infer a counterfactual when the
existing process was not sufficiently instantiated to support one.

## 15. Cost / complexity

Record non-authoritative telemetry where available:

- Provider/model invocations:
- Tokens/cost:
- Latency:
- Tool calls:
- Human/evaluator effort:
- Repository machinery added solely for the experiment:

## 16. Limitations

Include at minimum:

- single-Skill limitation;
- corpus-selection limitations;
- model/harness dependence;
- evaluator uncertainty;
- any non-determinism;
- whether the experiment supports only local, not cross-Skill, claims.

## 17. Disposition

Select exactly one:

- `NO_FURTHER_WORK_WARRANTED`
- `REPLICATE`
- `NARROW_MECHANISM_WARRANTED`
- `PRODUCTIZATION_CANDIDATE`

### Warrant

State the minimum evidence supporting the disposition and the evidence that would
falsify or weaken it.

## 18. Reopen conditions

Define concrete evidence that would justify another cycle. Avoid generic conditions
such as "more data would be useful."

## Rejected candidates

For every rejected candidate preserve:

- candidate ID;
- proposed change;
- why it appeared reasonable;
- qualification disposition;
- observed regressions or insufficiency;
- reusable lesson.

## Claim boundary

State exactly what the experiment establishes. Explicitly state what it does **not**
establish, including automatic Skill optimization, promotion authority, cross-Skill
generality, or permission to relabel exploratory outputs as canonical evidence.
