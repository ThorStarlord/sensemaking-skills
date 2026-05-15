# Skill Improvement Plan

## 1. Diagnosis
- **Failure Mode Class**: Class 8: Over-Maintenance
- **Defect Source**: fixture_defect
- **Recommended Action**: fixture_edit
- **Severity**: Medium
- **Summary**: Resolve the conflict between correct skill logic and a flawed evaluation fixture in Scenario 005.

## 2. Evidence
- **Source Report**: [usage_research_report.md](usage_research_report.md)
- **Evidence Snippet**:
> The `usage_research_report.md` indicates that the skill correctly identified the OUP as `skill-registry.yaml`. The reported "failure" is due to the evaluator fixture `flawed_expected_behavior.md` expecting `workflow-registry.yaml`.

## 3. Proposed Edits
- **Do Not Edit**: skills/problem-framer/SKILL.md

### Edit 1: Fix Flawed Evaluation Fixture
- **edit_type**: fixture_edit
- **failure_mode_class**: Class 8: Over-Maintenance
- **risk_level**: low
- **before_behavior**: Evaluator incorrectly expects `workflow-registry.yaml` for a "New Skill" task.
- **after_expected_behavior**: Evaluator expects `skill-registry.yaml`, matching the "Orchestration Shield" rule.
- **anti_overfitting_rationale**: Prevents the maintenance loop from "fixing the wrong thing" and ensures tests remain grounded in repository philosophy.
- **regression_risk**: None. Correcting a known-flawed test fixture.

## 4. Impact Assessment
- **Summary**: This change restores trust in the validation stack for Scenario 005. It prevents the `skill-maintainer` from making destructive edits to valid skill logic.

## 5. Verification Plan
- **Rerun Scenario**: Scenario 005
- **Success Criteria**: Validator reports PASS with the updated fixture.

## 6. Machine-readable plan
```yaml
artifact_id: skill_improvement_plan
scenario_id: 005-conflicting-fixes
edits:
  - id: 1
    edit_type: fixture_edit
    failure_mode_class: "Class 8: Over-Maintenance"
    target_file: "examples/usage-research/scenarios/005-conflicting-fixes/flawed_expected_behavior.md"
    risk_level: low
    rationale: "Align fixture with Orchestration Shield grounding rules."
```
