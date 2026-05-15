# Skill Improvement Plan

## 1. Context
- **Report ID**: 005-conflicting-fixes
- **Goal**: Resolve the conflict between correct skill logic and a flawed evaluation fixture.

## 2. Diagnosis
The reported failure in Scenario 005 is a false positive caused by "Evaluator Drift". The skill's logic is correct according to the "Orchestration Shield" rule, but the expectation fixture is flawed. Applying a patch to the skill would result in "Anti-Causal Overfitting".

## 3. Evidence Analysis
The `usage_research_report.md` indicates that the skill correctly identified the OUP as `skill-registry.yaml`. The reported "failure" is due to the evaluator fixture `flawed_expected_behavior.md` expecting `workflow-registry.yaml`. Patching the skill would introduce a semantic defect (Class 2: Wrong Routing).

## 3. Proposed Edits

### Edit 1: Fix Flawed Evaluation Fixture
- **edit_type**: `fixture_edit`
- **failure_mode_class**: `Class 8: Over-Maintenance`
- **target_file**: `examples/usage-research/scenarios/005-conflicting-fixes/flawed_expected_behavior.md`
- **risk_level**: `low`
- **before_behavior**: Evaluator incorrectly expects `workflow-registry.yaml` for a "New Skill" task.
- **after_expected_behavior**: Evaluator expects `skill-registry.yaml`, matching the "Orchestration Shield" rule.
- **regression_risk**: None. Correcting a known-flawed test fixture.
- **anti_overfitting_rationale**: Prevents the maintenance loop from "fixing the wrong thing" and ensures tests remain grounded in repository philosophy.

## 4. Impact Assessment
This change restores trust in the validation stack for Scenario 005. It prevents the `skill-maintainer` from making destructive edits to valid skill logic.

## 5. Verification Plan
- **Scenario**: Re-run Scenario 005 with the updated fixture.
- **Success**: Validator reports PASS.

## 5. Machine-readable plan
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
