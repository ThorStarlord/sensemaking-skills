# Workflow Orchestration Plan

## 1. Brief Consumed

**Repository**: (from brief)
**Primary Fog Type**: architecture_fog
**Source Brief**: artifacts/repository_sensemaking_brief_phase4_1.md

---

## 2. System Recommendation

Based on fog type classification:
- Fog Type: `architecture_fog`
- Recommended Workflow: `architecture-implementation-workflow`

---

## 3. Workflow Selection

**Selected Workflow**: `architecture-implementation-workflow`
**Routing Decision Method**: `diagnosis_primary_soft_context`
**Routing Divergence**: false

---

## 4. Why This Workflow

The `architecture-implementation-workflow` is designed to address architecture_fog by:
- Identifying the root cause of the identified problem
- Producing diagnostic outputs and implementation artifacts
- Preparing the repository for the next phase of work

---

## 5. Workflow Steps

The selected workflow includes the following steps:

| Step | Skill | Input | Output | Gate | Description |
|------|-------|-------|--------|------|-------------|
| 1 | docs-aligner | context_artifacts | domain_alignment_report | review | Domain alignment - refine understanding and create CONTEXT.md |
| 2 | to-prd | domain_alignment_report | prd | review | Architecture spec - define refactoring strategy and module boundaries |
| 3 | to-issues | prd | issue_list | review | Implementation decomposition - break into issues |
| 4 | triage | issue_list | agent_brief | review | Issue preparation - create agent briefs |
| 5 | tdd | agent_brief | code_patch | review | Implementation - execute TDD cycles |
| 6 | handoff | code_patch | session_summary | session_close | Completion summary - document session |

---

## 6. Execution Mode

**Recommended Mode**: `plan_only`
**Auto-Invocation**: Enabled (workflow runtime will read `recommended_workflow_id` and invoke next workflow)

---

## 7. Approval Gates

Steps in this workflow include approval gates. Each gate requires user or automated approval before proceeding.

---

## 8. Next Steps

After this plan is approved and executed:
1. Execute the selected workflow (`architecture-implementation-workflow`)
2. Produce diagnostic/implementation artifacts
3. Continue to Phase 3 implementation (if applicable)

---

## 9. Escalation Handling

If the selected workflow encounters issues:
- Attempted fixes will be recorded in validation logs
- Escalation will occur after 3 failed attempts
- Escalation messages will include detailed error context and suggested next steps

---

## 10. Decision Rationale

The routing decision was made using `diagnosis_primary_soft_context`:
- System recommendation based on fog type: `architecture-implementation-workflow`
- Selected workflow: `architecture-implementation-workflow`
- Divergence detected: false

---

## 11. Machine-readable plan

```yaml
artifact_id: workflow_orchestration_plan
schema_version: 1
primary_fog_type: architecture_fog
chosen_workflow_id: architecture-implementation-workflow
routing_decision_method: diagnosis_primary_soft_context
routing_divergence: false
escalation_recommended: true
auto_escalation_allowed: false
created_at: "2026-05-25T05:21:12.817410Z"
immutable: true
workflow_steps:
  - step_id: 1
    skill: docs-aligner
    input_artifact: context_artifacts
    output_artifact: domain_alignment_report
    gate: review
    description: "Domain alignment - refine understanding and create CONTEXT.md"
  - step_id: 2
    skill: to-prd
    input_artifact: domain_alignment_report
    output_artifact: prd
    gate: review
    description: "Architecture spec - define refactoring strategy and module boundaries"
  - step_id: 3
    skill: to-issues
    input_artifact: prd
    output_artifact: issue_list
    gate: review
    description: "Implementation decomposition - break into issues"
  - step_id: 4
    skill: triage
    input_artifact: issue_list
    output_artifact: agent_brief
    gate: review
    description: "Issue preparation - create agent briefs"
  - step_id: 5
    skill: tdd
    input_artifact: agent_brief
    output_artifact: code_patch
    gate: review
    description: "Implementation - execute TDD cycles"
  - step_id: 6
    skill: handoff
    input_artifact: code_patch
    output_artifact: session_summary
    gate: session_close
    description: "Completion summary - document session"
```
