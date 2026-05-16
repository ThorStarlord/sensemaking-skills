---
validator_case: negative
expected_error_contains: "UNKNOWN_TARGET_SKILL"
---

# Prompt Handoff

## 1. Target Skill
`totally-nonexistent-skill-id`

## 2. Context to Preserve
Some context.

## 3. Task
Do the thing.

## 4. Constraints
None.

## 5. Inputs
- `skills/repo-sensemaker/SKILL.md`

## 6. Expected Output
Some output.

## 7. Stop Condition
Stop when done.

---

## 8. Ready-to-copy Prompt
```markdown
/target
Task: Do the thing.
```
