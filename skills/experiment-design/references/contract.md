# Experiment-design methodology and experiment_plan contract

**Methodological provenance:** adapted from `lucasgaravelli/pm-skills-claude-code@21cbb2903d740d10fc65c667aea97d3ee8657349`, `.claude/commands/experiment-design.md`.

Retain pretotyping, skin-in-the-game, own-data/YODA, behavior-over-opinion, controlled A/B design, primary/guardrail metrics, preregistration, kill criteria, and analysis planning. Treat numerical thresholds from upstream examples as examples, not defaults.

Produce: `## Hypothesis and riskiest assumption`, `## Method and exposure`, `## Metrics and evidence plan`, `## Decision and kill criteria`, `## Analysis and authority`, `## Risks and unknowns`, `## Machine-readable handoff`.

```yaml
artifact_id: experiment_plan
schema_version: "1"
status: designed
hypothesis_ref: "..."
experiment_type: pretotype | usability | ab_test | other
target_population: "..."
intervention: "..."
primary_metric: {name: "...", baseline: null, baseline_status: unknown, evidence_refs: []}
guardrails: []
sample_plan: {size: null, status: unknown, method: "..."}
duration_plan: {value: null, status: unknown}
decision_criteria: {go: "...", no_go: "...", investigate: "..."}
kill_criteria: []
analysis_method: "..."
execution_authority_ref: null
unresolved_questions: []
```

`status` is always `designed`; this artifact has no result/winner field. Observed baselines require evidence refs. External execution authority is separate and may remain null.