# Customer-journey methodology and journey_map contract

**Methodological provenance:** adapted from `lucasgaravelli/pm-skills-claude-code@21cbb2903d740d10fc65c667aea97d3ee8657349`, `.claude/commands/customer-journey.md`.

Retain stage mapping, touchpoints, actions, questions, emotions, pain points, opportunities, Aha Moments, Moments of Truth, and Churn Triggers. The upstream seven-stage Awareness-to-Advocacy sequence is a heuristic: scoped journeys may use fewer or different stages.

Produce: `## Persona and scope`, `## Evidence inventory`, `## Journey stages`, `## Critical moments`, `## Opportunities and unknowns`, `## Machine-readable handoff`.

```yaml
artifact_id: journey_map
schema_version: "1"
status: hypothesis | evidence_backed | mixed
persona_ref: "..."
scope: "..."
stages:
  - id: STAGE-1
    name: "Onboarding"
    order: 1
    touchpoints: []
    actions: []
    questions: []
    emotions:
      - value: "uncertain"
        evidence_status: hypothesis | inferred | observed | unknown
        evidence_refs: []
    pain_points: []
    opportunities: []
    metrics:
      - name: "completion_rate"
        value: null
        evidence_status: unknown | proposed | observed
        evidence_refs: []
critical_moments:
  - id: MOMENT-1
    type: aha | moment_of_truth | churn_trigger
    stage_ref: STAGE-1
    statement: "..."
    evidence_status: hypothesis | inferred | observed | unknown
    evidence_refs: []
recommendations: []
unresolved_questions: []
```

Stage and critical-moment IDs are unique; stage order values are unique positive integers; critical moments must reference declared stages. Any `observed` emotion, metric, or critical moment requires evidence refs. `status: evidence_backed` requires at least one observed evidence-bearing journey claim; the validator does not decide whether the journey model is strategically useful.