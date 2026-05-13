# Example: Prompt Handoff (Problem to Repo Handoff)

## 1. Target Skill
`repo-sensemaker`

## 2. Context to Preserve
The problem frame identified that the "lack of automation" is specifically a lack of contract enforcement in the handoff between diagnosis and action.

## 3. Task
Perform a diagnostic audit of the current `repo-sensemaker` and `workflow-orchestrator` handoff logic.

## 4. Constraints
- Cite file-level evidence in Section 7.
- Use the 11-section Brief template.
- Do not implement the fix yet.

## 5. Inputs
- `skills/repo-sensemaker/SKILL.md`
- `skills/workflow-orchestrator/SKILL.md`

## 6. Expected Output
A Repository Sensemaking Brief that names the "handoff contract" as the weakest boundary.

## 7. Stop Condition
Stop once the Brief is saved to `docs/sensemaking/brief-001.md`.

---

## 8. Ready-to-copy Prompt
```markdown
/repo-sensemaker
Task: Audit the handoff logic between diagnosis and orchestration.
Context: The problem is a lack of contract enforcement (see Problem Frame).
Constraints: Cite files, use 11-section template, do not implement fix.
Stop Condition: Save to docs/sensemaking/brief-001.md and wait.
```

## Expected Behavior Checklist
- [x] Correctly targets `repo-sensemaker`.
- [x] Preserves the "contract enforcement" context.
- [x] Includes specific file inputs.
- [x] Provides a ready-to-copy prompt with a stop condition.
