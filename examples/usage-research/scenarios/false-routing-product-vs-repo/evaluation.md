# Evaluation Rubric (Scenario: False-Routing Product vs Repo)

| Criterion | 1 (Fail) | 2 (Partial) | 3 (Pass) |
| :--- | :--- | :--- | :--- |
| **Object Under Pressure Clarity** | Names a generic product concept. | Names the project but misses the repo boundary. | Clearly identifies the `workflow-registry` or `skill-selection` as the bottleneck. |
| **Routing Accuracy** | Routes to PM/Engineering skills. | Routes to a generic "research" step. | Corrects the user and routes to repo-level sensemaking. |
| **Handoff Readiness** | No clear handoff or missing prerequisites. | Defines technical prerequisites for a product, not the repo. | Defines exactly what context is missing to select a workflow. |
| **Stopping Rule Quality** | Tautological ("stop when done"). | Vague but measurable ("read docs"). | Verifiable and tied to workflow selection evidence. |
| **Hallucination Risk** | Invents product details not in the fog. | Assumptions are noted but not flagged as high-risk. | Correctly identifies "intent" as the primary unknown. |

## Score Table
- **object_under_pressure**: 3/3
- **routing_accuracy**: 3/3
- **handoff_readiness**: 3/3
- **stopping_rule_quality**: 3/3
- **hallucination_risk**: 3/3

**Total Score: 15/15**
