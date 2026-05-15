# Skill Improvement Plan: problem-framer

## 1. Diagnosis
- **Failure Mode Class**: Class 2: Wrong Routing
- **Defect Source**: consumer_skill_defect
- **Recommended Action**: skill_edit
- **Severity**: High
- **Summary**: Ambiguous "product" keywords in raw fog trigger premature routing to implementation workflows, even when the user explicitly asks for repository/workflow guidance.


## 2. Evidence
- **Source Report**: [usage_research_report.md](usage_research_report.md)
- **Evidence Snippet**:
  > "The term 'AI Product' is highly evocative. In 1/3 internal tests, the agent still attempted to mention a 'Product Roadmap' in the Success Definition, showing that domain keywords still bleed into the framing."

## 3. Proposed Edits
### [problem-framer](../../../skills/problem-framer/SKILL.md)
- **Edit Type**: instruction_edit
- **Risk Level**: medium
- **Logic Change**: Implement a Domain Keyword Guard that explicitly redirects the Object Under Pressure (OUP) to the repository registry when navigation confusion co-occurs with domain keywords.
- **Behavioral Comparison**:
    - **Before**: Agent creates a "Product Roadmap" success condition based on the "AI Product" keyword.
    - **After**: Agent creates a "Identify correct workflow from registry" success condition.
- **Anti-Overfitting Guard**: This logic applies to any domain-heavy keywords (Engineering, Marketing, etc.) when the core problem is navigation/orchestration uncertainty.
- **Regression Risk**: Low. The guard only triggers when explicit navigation confusion is present.

**Instruction Block / Patch**:
```diff
+ Domain Keyword Guard: If the user uses domain-heavy keywords (e.g., 'Product', 'Engineering') but explicitly mentions confusion about 'how to start' or 'which workflow', the Object Under Pressure MUST be the repository's own routing or registry files.
```

## 4. Impact Assessment
- **Summary**: Will force the agent to ignore domain noise and focus on the orchestration bottleneck during the framing phase.
- **Verification Priority**: Scenario 002

## 5. Verification Plan
- **Rerun Scenario**: False-Routing Product vs Repo (Scenario 002)
- **Success Criteria**: The `problem_frame.md` identifies `workflow-registry.yaml` as the OUP without mentioning roadmaps or PRDs in the success definition.
