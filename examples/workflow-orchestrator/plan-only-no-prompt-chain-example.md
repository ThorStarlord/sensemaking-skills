# Example: Plan-only Hygiene

## 1. Brief consumed
Diagnosis: Ambiguous PRD for the `analytics` module.
Weakest Boundary: Requirement clarity.
Recommended Workflow: `product-discovery-sprint`

## 2. Chosen workflow
`product-discovery-sprint`

## 3. Why this workflow
Transforms product fog into a validated opportunity and testable hypothesis.

## 4. Skills in sequence
1. `persona`
2. `discovery`
3. `interview-synthesis`
4. `opportunity-tree`
5. `hypothesis`

## 5. Inputs and outputs
- `persona`: Produces persona definition.
- `discovery`: Produces discovery findings.
- `interview-synthesis`: Produces synthesis report.
- `opportunity-tree`: Produces opportunity map.
- `hypothesis`: Produces hypothesis statement.

## 6. Approval gates
- **Gate 1**: Review persona.
- **Gate 2**: Review discovery.
- **Gate 3**: Review patterns.
- **Gate 4**: Review opportunity tree.
- **Gate 5**: Review hypothesis.

## 7. Stop conditions
- User abort.

## 8. Execution mode
`plan_only`

## 9. Prompt chain
N/A - mode is plan_only. No prompt chain generated.

## 10. Run log template
N/A - mode is plan_only.

## 11. Machine-readable plan

```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: product-discovery-sprint
execution_mode: plan_only
status: COMPLETED
subset_run: false

initial_inputs:
  - id: repository_sensemaking_brief
    type: artifact
    required: true

steps:
  - id: 1
    skill: persona
    step_type: external_routing
    gate: review_persona
    input_artifact: repository_sensemaking_brief
    output_artifact: persona_definition
    status: PENDING
  - id: 2
    skill: discovery
    step_type: external_routing
    gate: review_discovery
    input_artifact: persona_definition
    output_artifact: discovery_findings
    status: PENDING
  - id: 3
    skill: interview-synthesis
    step_type: external_routing
    gate: review_patterns
    input_artifact: discovery_findings
    output_artifact: synthesis_report
    status: PENDING
  - id: 4
    skill: opportunity-tree
    step_type: external_routing
    gate: review_opportunity_tree
    input_artifact: synthesis_report
    output_artifact: opportunity_map
    status: PENDING
  - id: 5
    skill: hypothesis
    step_type: external_routing
    gate: review_hypothesis
    input_artifact: opportunity_map
    output_artifact: hypothesis_statement
    status: PENDING

approval_gates:
  - review_persona
  - review_discovery
  - review_patterns
  - review_opportunity_tree
  - review_hypothesis

gate_behavior:
  review_persona: human_approval
  review_discovery: human_approval
  review_patterns: human_approval
  review_opportunity_tree: human_approval
  review_hypothesis: human_approval

stop_conditions:
  - user_abort
```
