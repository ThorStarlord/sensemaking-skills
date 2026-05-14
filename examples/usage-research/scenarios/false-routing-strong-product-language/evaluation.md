# Evaluation Rubric (Scenario 003: Strong Product Language)

## Run Metadata
- **skill_under_test**: [problem-framer, unknowns-mapper]
- **skill_version_ref**: current-working-tree
- **run_type**: simulated
- **evaluator**: antigravity-agent
- **confidence**: medium

## Expected Failure Mode (Counterfactual)
A weak run would interpret "product strategy workflow" as a direct request to perform product management tasks. It would name a product artifact (like a PRD) as the Object Under Pressure and route toward implementation skills, bypassing the necessary meta-sensemaking step of defining the workflow itself within the repository boundaries.

## Scoring Rubric

| Criterion | 1 (Fail) | 2 (Partial) | 3 (Pass) |
| :--- | :--- | :--- | :--- |
| **Object Under Pressure Clarity** | Names a generic product artifact (PRD, Roadmap). | Identifies a "workflow" but misses the repo registry grounding. | Explicitly names `workflow-registry.yaml` or the repo's skill selection boundary. |
| **Routing Accuracy** | Routes to domain implementation (e.g., `to-prd`). | Routes to a generic "research" step. | Routes to repo-level sensemaking or workflow definition. |
| **Stopping Rule Quality** | Tautological or vague. | Measurable but not tied to registry evidence. | Verifiable and tied to selecting a specific workflow ID. |
| **Evidence Quality** | No excerpts provided. | Subjective claims without grounding. | Directly quotes generated artifact to justify scores. |

## Score Table
- **object_under_pressure**: 3/3 (Evidence: Named `workflow-registry.yaml` as the OUP.)
- **routing_accuracy**: 3/3 (Evidence: Recommended Registry Comparison over Domain Implementation.)
- **stopping_rule_quality**: 3/3 (Evidence: Tied to mapping artifacts to existing/new skills in a yaml file.)
- **evidence_quality**: 3/3 (Evidence: Full excerpts provided in the research report.)

**Total Score: 12/12**
