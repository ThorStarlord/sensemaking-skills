# Artifact-Driven Agentic Engineering

## The Core Thesis
**Artifacts are the API between skills.**

In traditional agentic workflows, state is maintained in the ephemeral context of a chat session. This leads to "context drift," where the agent's reasoning degrades over time, or "hallucinated handoffs," where one skill guesses what the previous skill intended.

Artifact-Driven Engineering replaces "conversation memory" with **durable, validated artifacts**. Each step in a workflow must produce a structured output (Markdown, YAML, JSON) that satisfies a specific contract. The next skill in the chain consumes this artifact, not the conversation history.

## Systems Engineering vs. Software Engineering
This repository treats agent development as a **Systems Engineering** discipline.

| Discipline | Focus | In this Repo |
|------------|-------|--------------|
| **Software Engineering** | Building the components (Scripts, Regsitries, Validators). | `scripts/`, `skill-registry.yaml` |
| **Systems Engineering** | Designing the whole loop (Handoffs, Safety Gates, Human-in-the-loop). | `workflow-registry.yaml`, `CONTEXT.md` |
| **Reliability Engineering** | Ensuring the system fails safely and recovers correctly. | `skill_improvement_plan.md`, Anti-Causal Confusion Rule |

## The Failure Taxonomy
We anticipate failure by classifying errors into predictable classes rather than treating every bug as a surprise. 
> See [docs/philosophy/AGENTIC_FAILURE_MODES.md](docs/philosophy/AGENTIC_FAILURE_MODES.md) for the full taxonomy and FMEA analysis.

1. **Input Fog:** The raw request is too vague to frame.
2. **Routing Error:** The system selects the wrong workflow or skill.
3. **Artifact Weakness:** The output of a skill lacks the detail needed for the next step.
4. **Handoff Failure:** The consumer skill cannot parse or understand the upstream artifact.
5. **Boundary Violation:** A skill attempts work outside its defined instruction set.
6. **Over-Maintenance:** A repair skill attempts to fix a "correct" instruction to satisfy a "flawed" fixture.

## The Anti-Causal Confusion Rule
To prevent **Over-Maintenance**, the maintenance loop enforces a strict classification gate:

> **Before recommending a patch to a skill's logic (`SKILL.md`), the system must prove that the defect is NOT in the test fixture, the validator, the registry, or the human's interpretation.**

This prevents the system from "overfitting" its logic to pass flawed tests, ensuring that the `SKILL.md` files remain general and robust.

## Governance and Safety
*   **Isolated Execution:** Tasks should only write to assigned `examples/skill-tests/` paths.
*   **Durable Audit Trails:** Every task must produce a `TEST-RUN-LOG.md` to document its reasoning and evidence.
*   **Contract Validation:** Every artifact is checked by a Level-1 (Structural) or Level-2 (Generic) validator before it can be promoted to a stable workflow.
