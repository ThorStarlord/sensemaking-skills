---
name: workflow-planner
description: read a repository sensemaking brief and produce a machine-readable workflow orchestration plan (a planning recommendation for the active agent, not execution authority).
---

# workflow-planner

This skill produces a **workflow orchestration plan** artifact. It does **not** execute workflows, run steps, manage gates, validate artifacts, or invoke other skills. Under the ratified agent-native model (ADR 0013), the active agent owns the control loop; the plan is a planning recommendation, not execution authorization.

If the active agent selects a registered workflow for execution, `workflow-runtime.py` (the Python execution engine) is bounded orchestration/compatibility machinery: it reads the plan's `chosen_workflow_id` to sequence the selected workflow's steps. Workflow selection remains the agent's (or user's) decision; a plan recommendation never by itself authorizes execution.

## Workflow

1. **Consume Brief**: Review the diagnostic brief from `repo-sensemaker`.
2. **Recommend Workflow**: Map the recommended path to an available workflow in `workflow-registry.yaml`, as a recommendation.
3. **Plan**: Produce a Workflow Orchestration Plan with the chosen workflow, ordered steps, and approval gates.
4. **Mode Selection**: Determine the execution mode (default: `plan_only`).

## Stage 2: Routing Audit

**Routing Audit Fields** track the gap between what the system recommended and what was actually chosen. In `guided_execution` mode these fields document the human/agent decision; they record a recommendation, they do not confer execution authority.

### Recording Routing Decisions

**Step 1: Capture System Recommendation**
- Read `recommended_workflow_id` from the repository sensemaking brief
- Record this as `system_recommended_workflow` in the plan
- This is the planning recommendation repo-sensemaker derived from fog type and conflict analysis — a recommendation, not execution authority

**Step 2: Determine User/Agent Selection**
- If in `guided_execution` mode and the user is presented a choice, record their explicit selection
- If user explicitly overrides the recommendation, record the selected workflow
- If no override provided, the selection equals the system recommendation
- Record the final selection as `selected_workflow` and the plan's authoritative field `chosen_workflow_id`

**Step 3: Calculate Routing Divergence**
- `routing_divergence: true` if `system_recommended_workflow != selected_workflow`
- `routing_divergence: false` if they match

**Step 4: Record Decision Method**
Valid `routing_decision_method` values:
- `diagnosis_primary_soft_context` — System recommendation based on primary fog type; user intent confirmed (no override)
- `diagnosis_mixed_tiebreak_to_user_intent` — Diagnosis showed mixed fog; user intent broke the tie
- `user_explicit_override` — User explicitly selected different workflow than system recommended
- `escalation_recommended_accepted` — System recommended escalation to full-fog-workflow; user accepted
- `escalation_recommended_rejected` — System recommended escalation; user stayed with narrower workflow

**Example Scenarios:**

*Scenario A: Agreement (no override)*
```yaml
system_recommended_workflow: product-implementation-workflow
selected_workflow: product-implementation-workflow
routing_divergence: false
routing_decision_method: diagnosis_primary_soft_context
```

*Scenario B: User Override*
```yaml
system_recommended_workflow: full-fog-workflow
selected_workflow: product-implementation-workflow
routing_divergence: true
routing_decision_method: user_explicit_override
```

*Scenario C: Tie-breaker to User Intent*
```yaml
system_recommended_workflow: product-implementation-workflow
selected_workflow: product-implementation-workflow
routing_divergence: false
routing_decision_method: diagnosis_mixed_tiebreak_to_user_intent
```

### Escalation in Routing Audit

When `escalation_recommended: true` in the brief:
- System recommends full-fog-workflow or other escalation path
- Record `system_recommended_workflow: full-fog-workflow` (or appropriate escalation)
- If user accepts: selected matches system, `routing_divergence: false`, `decision_method: escalation_recommended_accepted`
- If user rejects: selected is narrower workflow, `routing_divergence: true`, `decision_method: escalation_recommended_rejected`

Always include `escalation_recommended` and `auto_escalation_allowed` from brief. `escalation_recommended` informs the human/agent decision; it does not itself authorize automatic escalation. Users/agents always control final selection.

## Plan Content

The plan must include a `chosen_workflow_id` field in its machine-readable section. This is the plan's authoritative workflow-selection field — the workflow the active agent (or user) chose. `recommended_workflow_id` belongs to the repository sensemaking brief as a planning recommendation; the plan records that recommendation as `system_recommended_workflow` and the final selection as `chosen_workflow_id` / `selected_workflow`.

Workflow selection mapping (a planning recommendation / selection aid, not automatic execution authority):
- Read `primary_fog_type` from repository sensemaking brief (always canonical form per canonical-vocabulary.yaml)
- If primary fog suggests `product_fog`: consider `product-implementation-workflow`
- If primary fog suggests `ui_fog`: consider `ui-implementation-workflow`
- If primary fog suggests `docs_fog`: consider `docs-implementation-workflow`
- If primary fog suggests `architecture_fog`: consider `implementation-workflow` with architecture focus
- If fog_type is unclassified: default recommendation is `implementation-workflow` (graceful degradation)
- Can prefer an explicit `recommended_workflow_id` from the brief if it provides an alternative
- The active agent (or user) then selects the workflow; the plan records that decision as `chosen_workflow_id`. A recommendation is not execution authorization.

**CRITICAL**: The four canonical fog types are `product_fog`, `ui_fog`, `docs_fog`, `architecture_fog`. `integration_fog` is NOT a canonical fog type in this model. 
Validators normalize aliases (e.g., "ui" -> "ui_fog", "product" -> "product_fog") before artifact storage. 
Downstream consumers (including this skill) always receive and must emit canonical values only.
Reference `docs/canonical-vocabulary.yaml` for fog type definitions and aliases.

## Output Format

Every response must follow the [Workflow Orchestration Plan](references/workflow-orchestration-template.md) structure.

**CRITICAL**: Every plan MUST include the **Section 11: Machine-readable plan** YAML block containing `chosen_workflow_id`. Plans without this block are invalid and violate the artifact contract.

## Boundary Rules

- **Plan-only Mode**: Default to `plan_only` mode unless explicitly requested otherwise. In `plan_only` mode, set Section 9 to: `N/A - mode is plan_only. No prompt chain generated.`
- **Machine Verifiability**: Every plan MUST generate Section 11 (Machine-readable plan). Failure to do so renders the artifact non-verifiable.
- **Handoff Compliance**: The plan's recommended workflow must reference only workflows registered in `workflow-registry.yaml`.
- **Path Normalization**: All artifact paths in the plan MUST use relative paths. Never use absolute `file:///` links.

## References
- [Canonical Vocabulary Registry](../../docs/canonical-vocabulary.yaml) — Authoritative fog types and routing field definitions
- [Workflow Orchestration Template](references/workflow-orchestration-template.md)
- [Skill Registry](references/skill-registry.yaml)
- [Workflow Registry](references/workflow-registry.yaml)
- [Artifact Contracts](references/artifact-contracts.yaml)
- [Execution Modes](references/execution-modes.md)

## Execution Protocol

When executing as part of a workflow run:

1. Read the provided run_id, step_id, input artifacts, and expected artifact_id.
2. Call `scripts/run-ledger.py start-step`.
3. The runtime already resolved the output path and passed it as `expected_output_path` in context — use that path verbatim. Never call `scripts/create-artifact.py` (or otherwise recompute a path) during a runtime-invoked run; that path-recomputation is what caused a prior run to overwrite a tracked framework artifact (see ADR 0010, issue #40).
4. Produce the artifact at that exact path.
5. Call `scripts/validate-and-record.py`.
6. Only report completion if validation passes.
7. Never mark the next step complete yourself.

