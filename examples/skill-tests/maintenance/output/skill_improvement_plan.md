# Skill Improvement Plan: repo-sensemaker (Scenario 005)

## 1. Diagnosis
- **Failure Mode Class**: Class 8: Over-Maintenance
- **Defect Source**: fixture_defect
- **Recommended Action**: fixture_edit
- **Severity**: Low
- **Summary**: The research report identifies a 100% mismatch between agent behavior and the expected behavior fixture. However, the agent's behavior is objectively correct (system diagnostic), while the fixture is flawed (incorrectly expecting a PRD). Any skill patch would result in "Over-Maintenance" and "Anti-Causal Confusion."

## 2. Evidence
- **Source Report**: [usage_research_report.md](usage_research_report.md)
- **Evidence Snippet**:
  > "The agent correctly identifies the user's intent as a request for a system registry entry... The scenario fixture incorrectly labels this as a 'Product Requirement Document' task."

## 3. Proposed Edits
- **Do Not Edit**: `skills/repo-sensemaker/SKILL.md`, `skills/workflow-orchestrator/references/skill-registry.yaml`

### [Scenario 005 Fixture](examples/usage-research/scenarios/005-conflicting-fixes/flawed_expected_behavior.md)
- **Edit Type**: fixture_edit
- **Risk Level**: low
- **Logic Change**: Replace the flawed expectation with the correct technical diagnostic expectation.
- **Behavioral Comparison**:
    - **Before**: Validator/Researcher flags a "failure" when the agent correctly answers a technical question.
    - **After**: Success criteria are aligned with actual system capabilities and user intent.
- **Anti-Overfitting Guard**: This change prevents the maintainer from adding unnecessary "PRD-first" instructions to the sensemaker which would degrade its diagnostic precision.
- **Regression Risk**: Low. Risk is limited to accidentally erasing the adversarial purpose of Scenario 005 if the corrected fixture no longer preserves the trap condition.

**Instruction Block / Patch**:
```diff
-# Flawed Expected Behavior (Scenario 005)
-The agent should identify that the user is confused and needs a PRD...
+# Corrected Expected Behavior (Scenario 005)
+The agent should provide the requested registry entry for 'problem-framer'.
```

## 4. Impact Assessment
- **Summary**: Prevents regression in diagnostic skills by protecting the maintainer from flawed evaluation evidence.
- **Verification Priority**: High (Scenario 005).

## 5. Verification Plan
- **Rerun Scenario**: Scenario 005
- **Success Criteria**: `usage-researcher` reports 100% semantic alignment with the updated fixture.
