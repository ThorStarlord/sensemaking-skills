# Skill Improvement Plan: System Diagnostics & Registry Guard

## 1. Diagnosis
- **Failure Mode**: Registry Obscurity / Intent Misattribution
- **Severity**: High
- **Summary**: Agent blames user vagueness for execution failures that are actually caused by malformed registry entries.

## 2. Evidence
- **Source Report**: [usage_research_report.md](usage_research_report.md)
- **Evidence Snippet**:
  > "The agent incorrectly concluded that the user's 'Raw Fog' was too vague and suggested re-running problem-framer, despite the user citing a specific (albeit broken) workflow by name."

## 3. Proposed Edits

### [problem-framer](../../../skills/problem-framer/SKILL.md)
- **Edit Type**: instruction_edit
- **Risk Level**: low
- **Logic Change**: Add a "System Defect Guard" to prevent misattribution of errors.
- **Behavioral Comparison**:
    - **Before**: "User's fog is missing steps."
    - **After**: "The requested workflow exists but seems to have missing steps in the registry. Auditing registry..."
- **Anti-Overfitting Guard**: This applies to any scenario where a named system entity (workflow, skill, artifact) is cited but fails to execute.
- **Regression Risk**: None.

**Instruction Block / Patch**:
```diff
+ System Defect Guard: If a user cites a specific workflow or skill by name but reports an execution error (e.g., 'missing steps', 'invalid I/O'), do NOT assume user confusion. The Object Under Pressure MUST be the corresponding registry entry.
```

### [workflow-registry.yaml](../../../skills/workflow-orchestrator/references/workflow-registry.yaml)
- **Edit Type**: registry_edit
- **Risk Level**: high
- **Logic Change**: Fix the malformed `product-discovery-sprint` entry.
- **Behavioral Comparison**:
    - **Before**: Workflow has missing mandatory `steps`.
    - **After**: Workflow has complete, valid step sequence.
- **Anti-Overfitting Guard**: N/A (Direct fix).
- **Regression Risk**: High (Registry change). Requires human approval.

**Instruction Block / Patch**:
```diff
-   id: product-discovery-sprint
-   # [Malformed content]
+   id: product-discovery-sprint
+   steps: [...] # [Valid content]
```

## 4. Impact Assessment
- **Summary**: Ensures the system can self-diagnose structural defects rather than gaslighting the user into re-framing already clear problems.
- **Verification Priority**: Scenario 004

## 5. Verification Plan
- **Rerun Scenario**: 004-broken-registry
- **Success Criteria**: `problem_frame.md` correctly identifies `workflow-registry.yaml` as the OUP and points to the malformed entry.
