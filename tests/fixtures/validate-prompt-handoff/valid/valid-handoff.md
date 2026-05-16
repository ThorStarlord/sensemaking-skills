---
validator_case: positive
---

# Prompt Handoff

## 1. Target Skill
`repo-sensemaker`

## 2. Context to Preserve
The problem frame identified that the lack of automation is specifically a lack of contract enforcement in the handoff.

## 3. Task
Perform a diagnostic audit of the current repo-sensemaker and workflow-orchestrator handoff logic.

## 4. Constraints
- Cite file-level evidence.
- Do not implement the fix yet.

## 5. Inputs
- `skills/repo-sensemaker/SKILL.md`
- `skills/workflow-orchestrator/SKILL.md`

## 6. Expected Output
A Repository Sensemaking Brief that identifies the weakest boundary.

## 7. Stop Condition
Stop once the Brief is saved to docs/sensemaking/brief-001.md.

---

## 8. Ready-to-copy Prompt
```markdown
/repo-sensemaker
Task: Audit the handoff logic.
Context: The problem is a lack of contract enforcement.
```
