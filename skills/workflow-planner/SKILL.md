---
name: workflow-planner
description: read a repository sensemaking brief and produce a machine-readable workflow orchestration plan that the workflow runtime executes.
---

# workflow-planner

This skill produces a **workflow orchestration plan** artifact. It does **not** execute workflows, run steps, manage gates, validate artifacts, or invoke other skills. Those responsibilities belong to `workflow-runtime.py` (the Python execution engine).

The workflow runtime reads this plan to determine which workflow to execute and how to sequence its steps.

## Workflow

1. **Consume Brief**: Review the diagnostic brief from `repo-sensemaker`.
2. **Select Workflow**: Match the recommended path to an available workflow in `workflow-registry.yaml`.
3. **Plan**: Produce a Workflow Orchestration Plan with ordered steps and approval gates.
4. **Mode Selection**: Determine the execution mode (default: `plan_only`).

## Stage 2: Routing Audit

**Routing Audit Fields** track the gap between what the system recommended and what was actually selected.

### Recording Routing Decisions

**Step 1: Capture System Recommendation**
- Read `recommended_workflow_id` from the repository sensemaking brief
- Record this as `system_recommended_workflow` in the plan
- This is what repo-sensemaker diagnosed based on fog type and conflict analysis

**Step 2: Determine User Selection**
- If in `guided_execution` mode and the user is presented a choice, record their explicit selection
- If user explicitly overrides the recommendation, record the selected workflow
- If no override provided, selected workflow equals system recommendation

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

Always include `escalation_recommended` and `auto_escalation_allowed` from brief. Escalation recommendations are informational; users always control final selection unless auto_escalation is enabled.

## Plan Content

The plan must include a `recommended_workflow_id` field in its machine-readable section. The workflow runtime reads this field to determine which workflow to auto-invoke next.

Workflow routing logic (documented here; executed by the runtime):
- Parse orchestration plan's fog classification (`product_fog`, `architecture_fog`, `ui_fog`, `docs_fog`, or other)
- If `fog_type == "product"`: use `product-implementation-workflow`
- If `fog_type == "ui"` or `fog_type == "frontend"`: use `ui-implementation-workflow`
- If `fog_type == "docs"` or `fog_type == "documentation"`: use `docs-implementation-workflow`
- If `fog_type == "uncertain"` or unclassified: use default `implementation-workflow` (graceful degradation)
- Can override with explicit `recommended_implementation_workflow` field

Include a `fog_type_confidence` field in the machine-readable section. If classification is uncertain, set `fog_type_confidence: low`.

## Output Format

Every response must follow the [Workflow Orchestration Plan](references/workflow-orchestration-template.md) structure.

**CRITICAL**: Every plan MUST include the **Section 11: Machine-readable plan** YAML block containing `recommended_workflow_id`. Plans without this block are invalid and violate the artifact contract.

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
3. Call `scripts/create-artifact.py` to resolve the output path.
4. Produce the artifact at that exact path.
5. Call `scripts/validate-and-record.py`.
6. Only report completion if validation passes.
7. Never mark the next step complete yourself.

