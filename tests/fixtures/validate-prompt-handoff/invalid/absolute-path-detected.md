---
validator_case: negative
expected_error_contains: "ABSOLUTE_PATH_DETECTED"
---

# Prompt Handoff

## 1. Target Skill
`repo-sensemaker`

## 2. Context to Preserve
Read from /Users/admin/projects/config.json.

## 3. Task
Do the thing.

## 4. Constraints
None.

## 5. Inputs
- `skills/repo-sensemaker/SKILL.md`

## 6. Expected Output
Some detailed output that is long enough.

## 7. Stop Condition
Stop when the analysis is complete and the results are saved.

---

## 8. Ready-to-copy Prompt
```markdown
/target
Task: Do the thing.
```
