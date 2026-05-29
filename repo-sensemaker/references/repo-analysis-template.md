# Repository Sensemaking Brief Template

**Date:** [YYYY-MM-DD]  
**Analyst:** [Agent Name]  
**Repository:** [Repo URL]

---

## 1. Repository Goal

What is this repository *supposed* to do? What is the user/team trying to achieve?

---

## 2. Current Shape

Describe the existing architecture, key modules, and data flow. Include major frameworks, patterns, and dependencies.

**Organize by layer or responsibility:**
- Frontend/API/Backend
- Key frameworks and libraries
- Data flow
- Infrastructure

---

## 3. Strong Signals

What evidence indicates the repository is healthy and solving its goal?

- ✅ Signal 1: [Evidence + source]
- ✅ Signal 2: [Evidence + source]
- ✅ Signal 3: [Evidence + source]

Cite what's working well, not just what's broken.

---

## 4. Missing Pieces

What's absent, broken, or incomplete that prevents the repository from fully achieving its goal?

**Organize by impact:**

### Critical (blocks goal)
- [Missing piece 1]: [Why it matters]
- [Missing piece 2]: [Why it matters]

### Important (degrades goal)
- [Missing piece 3]: [Why it matters]

### Nice-to-have (improves but doesn't block)
- [Missing piece 4]: [Why it matters]

---

## 5. Improvement Opportunities

What could be added or changed to make the repository more resilient, maintainable, or performant?

List 3-5 opportunities beyond the missing pieces. Think about:
- Developer experience
- Operational resilience
- Performance
- Maintainability
- Security

---

## 6. Weakest Boundary

Every codebase has a "weakest point" — the boundary between components that's most fragile, least tested, or most likely to break under change.

**Identify the single weakest boundary:**

- **What boundary?** (E.g., "API ↔ Database layer")
- **Why it's weak:** [Evidence]
- **What breaks if this boundary fails?** [Downstream impact]
- **How is it currently tested?** [Is testing adequate?]

This is often the best place to start improving the codebase.

---

## 7. Evidence

<!-- mode: investigative | durable -->
<!-- Set mode based on consumer:
     - investigative: human reading this brief directly (include line numbers, code snippets)
     - durable: downstream skills (to-prd, to-issues) will consume this (file paths only, grep-verifiable)
     See evidence-rules.md for details.
-->

Cite specific evidence for claims above. Organize by section or claim.

### Strong Signals Evidence
- [Signal 1]: [File + evidence]
- [Signal 2]: [File + evidence]

### Missing Pieces Evidence
- [Missing piece 1]: [File + evidence, why verified]

### Weakest Boundary Evidence
- [Boundary description]: [File + evidence]

---

## 8. Evidence Excerpts

If investigative mode: Include short code snippets showing problems.

If durable mode: Omit this section (not needed for downstream consumers).

---

## 9. Why This Boundary Matters

Explain why the weakest boundary is the right place to focus. What downstream impact does it have?

---

## 10. Candidate Next Steps

List 3-5 possible next steps (skills, workflows, analyses) that could address the missing pieces or strengthen the weak boundary.

---

## 11. Recommended Next Step

Which one candidate should we do first? Why?

---

## 12. Recommended Workflow

What workflow should we execute to address the recommended next step?

Examples:
- `problem-framer` → `unknowns-mapper` → `to-prd`
- `repo-sensemaker` → `to-issues` → `tdd`
- `workflow-orchestrator` (with specific execution mode)

---

## 13. Machine-Readable Handoff

```yaml
artifact_id: repository_sensemaking_brief_[REPO_NAME]_[DATE]
artifact_type: repository_sensemaking_brief
created_date: [YYYY-MM-DD]
evidence_mode: investigative | durable
repository_url: [URL]
repository_goal: [One-liner]
weakest_boundary: [Boundary description]
recommended_workflow_id: [workflow-id]
recommended_execution_mode: [guided_execution|autonomous_execution|yolo_execution]
ready_to_copy_prompt: |
  [If this brief is being handed off to another skill,
   paste the exact prompt that should be copied into that skill's input.]
```

---

## 14. Ready to Copy (Prompt Handoff)

If this brief is being consumed by another skill or agent, provide the exact prompt to copy:

```
[Paste exact prompt here — e.g., for to-prd, for workflow-orchestrator, etc.]
```

---

## Related

- [Evidence Rules](evidence-rules.md) — Explains investigative vs. durable modes
- [Artifact Contracts: repository_sensemaking_brief](../../workflow-orchestrator/references/artifact-contracts.yaml) — Required structure
