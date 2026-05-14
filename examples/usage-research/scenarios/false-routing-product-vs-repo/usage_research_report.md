# Usage Research Report (Scenario: False-Routing Product vs Repo)

## 1. Scenario Tested
**Scenario**: "False-Routing Product vs Repo"
**Fog**: A user asking for "better AI products" but actually confused about the repo's workflows.
**Objective**: Test if the sensemaking pipeline resists "product" keywords and correctly identifies the repository itself as the "Object Under Pressure."

## 2. Evaluation & Scoring

| Criterion | Score | Rationale |
| :--- | :--- | :--- |
| **Object Under Pressure Clarity** | 3/3 | Correctness: Identified `workflow-registry.yaml` and `skill-selection`. Resisted the temptation to name "Product Roadmap." |
| **Routing Accuracy** | 3/3 | Success: Recommended a workflow audit and disambiguation of intent within the repo's own capabilities. |
| **Handoff Readiness** | 3/3 | Clarity: Defined exactly what information is missing (which specific workflow matches which specific idea). |
| **Stopping Rule Quality** | 3/3 | Verifiability: The rule "Stop when we have identified a specific workflow... that accepts Raw Fog" is machine-verifiable. |
| **Hallucination Risk** | 3/3 | Discipline: No product details were invented. Intent was correctly flagged as the primary unknown. |

**Total Score: 15/15 (PASS)**

## 3. Observations & Friction Points
- **Keyword Gravity**: Despite the pass, there is a strong "gravitational pull" from the word "Product." A less sophisticated agent might have routed this to `to-prd`.
- **Instructional Gap**: The `problem-framer` instructions don't explicitly warn about "False Domain Routing." It relies on the agent's inherent reasoning.

## 4. Recommended Skill Edits
- **Skill**: `problem-framer`
    - **Edit**: Add a "Boundary Guard" rule: "If the user uses keywords from a specialized domain (PM, Engineering, UX) but expresses confusion about 'how to start' or 'which workflow to use', the `Object Under Pressure` MUST be the repository's own routing mechanism."
- **Skill**: `unknowns-mapper`
    - **Edit**: Refine the `Stopping Rule` examples to include "Selection of a specific entry from a registry" as a canonical success condition for meta-sensemaking tasks.

## 5. Conclusion
The pipeline demonstrated high precision in this test. It successfully avoided the most common failure mode for sensemaking systems: premature domain specialization. This confirms that the `Object Under Pressure` field is a critical semantic stabilizer.

**Note on Stability**: This report validates the *contractual and semantic validity* of the current skills for this scenario. It does not claim "production stability" in a general sense, but proves that for this specific class of ambiguity, the system is semantically useful.
