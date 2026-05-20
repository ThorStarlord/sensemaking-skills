# Negative: workflow-planner fails to escalate on intent conflict

## Scenario

The user says "We need a UI redesign" (ui_fog). repo-sensemaker detects architecture_fog (state management is broken) and sets `diagnosis_conflict: true` in the brief. workflow-planner ignores the conflict and routes to `fast-path-workflow` instead of escalating to `full-fog-workflow`.

## Diagnosis

- **Failure class**: Conflict Not Escalated
- **Skill**: workflow-planner
- **Evidence**: The orchestration plan's Section 11 has `escalation_recommended: true` but `system_recommended_workflow: fast-path-workflow` instead of `full-fog-workflow`
- **Why it's wrong**: validate-plan.py will reject this with `CONFLICT_NOT_ESCALATED`. The system must recommend full-fog-workflow when escalation is indicated, even if the user ultimately chooses a narrower path.

## Expected behavior

```
ERROR CONFLICT_NOT_ESCALATED: escalation_recommended is true but system_recommended_workflow is 'fast-path-workflow', expected 'full-fog-workflow'
```

## Corrected behavior

The plan should either:
1. **Escalate**: Set `system_recommended_workflow: full-fog-workflow` and let user accept or reject
2. **Override with audit**: Set `escalation_recommended: false` only if diagnosis_conflict was explicitly resolved (not recommended unless user overrides)
