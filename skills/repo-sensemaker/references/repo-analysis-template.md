# Repository Sensemaking Brief

## 1. Repository goal
What this repo appears to be trying to accomplish.

## 2. Current shape
Main folders, files, skills, workflows, examples, and references.

## 3. Strong signals
What is already working or conceptually strong.

## 4. Missing pieces
What is absent, incomplete, or implied but not implemented.

## 5. Improvement opportunities
Useful refinements that are not urgent blockers.

## 6. Weakest boundary
The most ambiguous, unproven, unsafe, or unenforced part of the repo.

**You MUST classify the boundary using one of the recognized weakness types** (see
[Weakness Types](weakness-types.md)): `Vocabulary Drift`, `Contract Mismatch`,
`Ghost Features`, `Safety Gaps`, `Implicit Dependencies`, `Zero Validation`, or
`Orphaned Examples`. State it explicitly on its own line:

`**Weakness type:** <one of the recognized types>`

## 6.5. Problem classification (fog type)
Classify the primary type of uncertainty or problem:
- **product_fog**: Vague user needs, unclear feature requirements, undocumented workflows
- **ui_fog**: Navigation complexity, screen design issues, interaction patterns unclear
- **docs_fog**: Missing documentation, unclear specifications, knowledge gaps
- **architecture_fog**: Code structure problems, design issues, unclear boundaries (default if unclear)

This classification determines which implementation workflow will be used downstream.

## 7. Evidence
File-level evidence supporting the diagnosis (cites specific files and line ranges,
e.g. `scripts/validate-brief.py:46`).

**Logic trace (required):** Show the diagnostic reasoning that connects the cited
evidence to the weakest boundary — i.e., the chain from observed signals to your
conclusion. Begin this paragraph with the literal words "Logic trace:".

## 8. Evidence excerpts
Each excerpt's `lines` field is a single line or a range. Use either the `Lx` /
`Lx-Ly` form (e.g. `L18`, `L25-L30`) or bare numbers (e.g. `18`, `25-30`) — both
are accepted. Every excerpt must include all four fields: `file`, `lines`,
`quote`, `supports_claim`.

```yaml
evidence_excerpts:
  - file: path/to/file.ext
    lines: L10-L15
    quote: "..."
    supports_claim: "..."
```

## 9. Why this boundary matters
What breaks if this remains weak.

## 10. Candidate next steps
2–5 possible next moves.

## 11. Recommended next step
The smallest concrete action with highest leverage.

## 12. Recommended workflow
One workflow candidate from the official `workflow-registry.yaml`. Do not invent workflow IDs.

## 13. Machine-readable handoff

### Stage 1: Intent-Aware Fields (Required)
```yaml
artifact_id: repository_sensemaking_brief
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: product_fog | ui_fog | docs_fog | architecture_fog | unknown
primary_fog_type: product_fog | ui_fog | docs_fog | architecture_fog | mixed | unknown
diagnosis_conflict: true | false
escalation_recommended: true | false
```

### Standard Fields
```yaml
recommended_workflow_id: # MUST match an ID in workflow-registry.yaml
recommended_execution_mode: plan_only | guided_execution
weakest_boundary: 
required_inputs:
  - user_intent
  - repository_state
```

### Complete Example
```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
recommended_workflow_id: product-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: analytics_feedback_gap
required_inputs:
  - user_intent
  - repository_state
user_implied_fog_type: product_fog
primary_fog_type: product_fog
diagnosis_conflict: false
escalation_recommended: false
created_at: "2026-05-19T16:00:00Z"
```

## 14. Ready-to-copy prompt
Prompt for `workflow-planner` or another downstream skill.
