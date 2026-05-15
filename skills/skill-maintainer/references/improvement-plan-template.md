# Skill Improvement Plan: [Target Skill Name]

## 1. Diagnosis
- **Failure Mode Class**: [Class 1: Input Ambiguity | Class 2: Wrong Routing | Class 3: Artifact Weakness | Class 4: Handoff Failure | Class 5: Boundary Violation | Class 6: Hallucinated Evidence | Class 7: Path Hygiene Error | Class 8: Over-Maintenance | Class 9: Validator Mismatch | Class 10: Status Overclaiming]
- **Severity**: [Low | Medium | High]
- **Summary**: Brief description of the behavioral gap identified in research.

## 2. Evidence
- **Source Report**: [Link to usage_research_report.md]
- **Evidence Snippet**:
  > "[Direct quote from Actual Behavior or Friction Points]"

## 3. Proposed Edits
### [Target Skill or File](path/to/file)
- **Edit Type**: [instruction_edit | template_edit | validator_edit | registry_edit | fixture_edit]
- **Risk Level**: [low | medium | high]
- **Logic Change**: [Briefly describe the change]
- **Behavioral Comparison**:
    - **Before**: [Failure mode observed]
    - **After**: [Expected behavioral improvement]
- **Anti-Overfitting Guard**: [Rationale for why this rule generalizes]
- **Regression Risk**: [What might break?]

**Instruction Block / Patch**:
```diff
+ [New Rule or Content]
```

## 4. Impact Assessment
- **Summary**: Overall impact of the proposed changes.
- **Verification Priority**: [Highest risk scenario to rerun]

## 5. Verification Plan
- **Rerun Scenario**: [ID of the scenario to rerun]
- **Success Criteria**: [Measurable evidence that the fix worked]
