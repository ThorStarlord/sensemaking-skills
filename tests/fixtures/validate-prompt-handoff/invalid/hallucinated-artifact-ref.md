---
validator_case: negative
expected_error_contains: "HALLUCINATED_ARTIFACT_REF"
---

# Prompt Handoff

## 1. Target Skill
`repo-sensemaker`

## 2. Context to Preserve
Some context.

## 3. Task
Do the thing.

## 4. Constraints
None.

## 5. Inputs
- `nonexistent/path/to/file.md`

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
