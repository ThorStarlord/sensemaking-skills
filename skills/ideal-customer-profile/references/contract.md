# Ideal-customer-profile methodology and ideal_customer_profile contract

**Methodological provenance:** adapted from `lucasgaravelli/pm-skills-claude-code@21cbb2903d740d10fc65c667aea97d3ee8657349`, `.claude/commands/ideal-customer-profile.md`.

Retain the useful four-part model (profile/demographics or firmographics, behaviors, Jobs to Be Done, needs/pain points), plus ideal-of-ideal indicators, disqualification criteria, and GTM implications. Treat every numeric firmographic, economic, usage, purchase, or pain claim according to evidence strength rather than filling the template.

Produce: `## Scope and evidence`, `## Profile`, `## Behaviors and buying context`, `## Jobs needs and pains`, `## Ideal-of-ideal and disqualifiers`, `## GTM implications`, `## Validation gaps`, `## Machine-readable handoff`.

```yaml
artifact_id: ideal_customer_profile
schema_version: "1"
status: hypothesis | evidence_backed | mixed
segment: "..."
evidence_window: "..."
evidence_refs: []
profile_claims:
  - id: ICP-C1
    dimension: "company_size"
    value: "..."
    evidence_status: hypothesis | inferred | observed | unknown
    evidence_refs: []
behaviors: []
jobs: []
pains: []
ideal_indicators:
  - id: ICP-I1
    statement: "..."
    evidence_status: hypothesis | inferred | observed | unknown
    evidence_refs: []
disqualifiers:
  - id: ICP-D1
    type: hard | soft
    statement: "..."
    evidence_status: hypothesis | inferred | observed | unknown
    evidence_refs: []
gtm_implications: []
unresolved_questions: []
```

All claim/indicator/disqualifier IDs are unique. Any `observed` claim requires evidence refs. `status: evidence_backed` requires at least one observed evidence-bearing claim and non-empty top-level evidence refs. A purely hypothesis-based profile must use `status: hypothesis`; the validator does not decide which customers are actually ideal.