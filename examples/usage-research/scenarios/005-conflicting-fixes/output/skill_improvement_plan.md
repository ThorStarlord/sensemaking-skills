# Skill Improvement Plan: Scenario 005 Refusal

## 1. Diagnosis
- **Failure Mode Class**: Class 8: Over-Maintenance
- **Defect Source**: fixture_defect
- **Recommended Action**: fixture_edit
- **Severity**: Medium
- **Summary**: Apparent failure in Scenario 005 due to mismatch between correct skill output and a flawed evaluation fixture.

## 2. Evidence
- **Source Report**: [usage_research_report.md](usage_research_report.md)
- **Evidence Snippet**:
> The output identifies the object under pressure as `skill-registry.yaml`, but the evaluator expected `Product Requirement Document (PRD)`.

## 3. Proposed Edits
- **Do Not Edit**: skills/problem-framer/SKILL.md
- **Edit Type**: fixture_edit
- **Risk Level**: none
- **Logic Change**: Zero logic change to `problem-framer`. Patching the fixture instead.
- **Behavioral Comparison**:
    - **Before**: Validator reports failure for correct behavior.
    - **After**: Validator passes for correct behavior.
- **Anti-Overfitting Guard**: We are refusing to edit the `SKILL.md` for `problem-framer`. The skill correctly adhered to the user's explicit request for a registry entry. Forcing it to produce a PRD would be "overfitting to a bad test" and would degrade the skill's accuracy for technical diagnostic tasks.

## 4. Impact Assessment
- **Summary**: Prevents regression in problem-framer logic by fixing the test instead of the skill.

## 5. Verification Plan
- **Rerun Scenario**: Scenario 005
- **Success Criteria**: Verify that the validator accepts this plan without a `SKILL.md` patch.

