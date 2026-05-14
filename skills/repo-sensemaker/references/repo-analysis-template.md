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

## 7. Evidence
File-level evidence supporting the diagnosis (cites specific files and line ranges).

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: path/to/file.ext
    lines: 10-15
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
One workflow candidate, if appropriate (e.g., from `workflow-orchestrator`).

## 13. Machine-readable handoff
```yaml
recommended_workflow_id: 
recommended_execution_mode: plan_only
weakest_boundary: 
required_inputs:
  - repository_sensemaking_brief
```

## 14. Ready-to-copy prompt
Prompt for `workflow-orchestrator` or another downstream skill.
