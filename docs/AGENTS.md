# Agent Decision Tree: When to Invoke Skills Directly vs. Orchestrator

## Quick Decision

**Ask yourself: How many skills will I chain together?**

- **1-3 skills** -> Call skills directly (faster, less overhead)
- **4+ skills** -> Use workflow-orchestrator (context carriage, approval gates, run logs)
- **User says "don't wait"** -> Call skills directly (even if 4+)

---

## Detailed Criteria

### Case 1: Direct Skill Invocation (1-3 Skills)

**When:** Single task with a small skill chain.

**Examples:**
- Run TDD on a single GitHub issue → `tdd` skill directly
- Diagnose one broken test → `diagnose` skill directly
- Generate PRD from discovery findings → `to-prd` → `to-issues` (2 skills) → call directly
- Generate agent briefs from issues → `triage` → `tdd` (2 skills) → call directly

**Why:** Direct invocation is faster. No approval gates, no run-log serialization, minimal context overhead.

**Trade-offs:**
- ✅ Faster
- ✅ Simpler
- ❌ No audit trail
- ❌ Context is implicit (in your prompt, not in an artifact)
- ❌ If interrupted, restart loses state

---

### Case 2: Orchestrator (4+ Skills)

**When:** Complex workflow with many dependent skills. Or when audit trail / approval gates matter.

**Examples:**
- Full diagnostic pipeline: `problem-framer` → `unknowns-mapper` → `repo-sensemaker` → `to-prd` → `to-issues` → `triage` → `tdd` (7 skills)
- Multi-stage design: `ui-brief` → `visual-calibration` → `blueprint` → `design-system` → `screen-spec` (5 skills)
- Cross-cutting analysis with approval checkpoints

**Why:** Orchestrator carries context automatically, enforces validation at each step, provides run logs.

**Trade-offs:**
- ✅ Audit trail
- ✅ Approval gates (if needed)
- ✅ Run logs
- ✅ State preserved if interrupted
- ❌ Slower (more ceremony)
- ❌ More verbose output
- ❌ Requires feature branches (in yolo_execution mode)

---

### Case 3: Direct Invocation (User Says "Don't Wait")

**When:** User explicitly says "go without my input" or "don't wait for approval."

**Applies even if:** 4+ skills, complex workflow, normally-orchestrated task.

**Why:** User has approved the risk of no checkpoints. Speed is the priority.

**How to invoke:**
- User instruction: "proceed without my input" → use direct skills
- User instruction: "execute autonomously" with skill list → interpret as orchestrator delegation
- User instruction: "don't wait for approval on each step" → direct invocation

**Trade-off:** You get speed; you lose checkpoints and audit trail.

---

## Decision Tree Flowchart

```
Start
├─ How many skills in the chain?
│  ├─ 1-3 skills?
│  │  └─ CALL DIRECTLY (faster)
│  └─ 4+ skills?
│     ├─ User says "don't wait"?
│     │  └─ CALL DIRECTLY (user approved speed over checkpoints)
│     └─ Need audit trail / approvals?
│        └─ USE ORCHESTRATOR (guided_execution or autonomous_execution)
└─ Proceed
```

---

## Examples

### Example 1: TDD on Single Issue (Direct)

**Task:** Implement feature described in GitHub issue #123.

**Skills needed:**
1. `triage` (read issue, create agent brief)
2. `tdd` (implement with tests)

**Decision:** 2 skills → **CALL DIRECTLY**

**Execution:**
```
User: "Implement issue #123 using TDD. Use the triage skill to create a brief, then tdd to code it."
→ Agent reads issue
→ Agent invokes triage skill → produces agent_brief
→ Agent invokes tdd skill (input: agent_brief) → produces code_patch
→ Done
```

No orchestration overhead needed.

---

### Example 2: Full Diagnostic Pipeline (Orchestrator)

**Task:** Understand a broken codebase deeply and produce an implementation plan.

**Skills needed:**
1. `problem-framer` (frame the problem)
2. `unknowns-mapper` (identify unknowns)
3. `repo-sensemaker` (analyze the repo)
4. `to-prd` (produce PRD)
5. `to-issues` (decompose into issues)
6. `triage` (produce agent briefs)
7. `tdd` (implement first issue)

**Decision:** 7 skills, complex dependencies → **USE ORCHESTRATOR**

**Execution:**
```
User: "Diagnose why the auth service is broken. Produce a plan and implement the first fix."
→ Agent invokes workflow-orchestrator with workflow_id: "diagnose_and_plan"
→ Orchestrator runs: problem-framer → unknowns-mapper → repo-sensemaker → to-prd → to-issues → triage
→ User approves issues (if guided_execution)
→ Orchestrator continues: tdd (first issue)
→ Done (with full run log and audit trail)
```

Orchestrator ensures each step validates before the next one starts.

---

### Example 3: Fast Iteration (User Override)

**Task:** Same as Example 2, but user says "don't wait."

**Decision:** Normally orchestrator (7 skills), but user says "don't wait" → **CALL DIRECTLY**

**Execution:**
```
User: "Diagnose the auth service. Produce a plan and implement the first fix. 
       Don't wait for my approval; proceed autonomously."
→ Agent invokes skills sequentially without orchestrator gates
→ Artifacts still produced (PRD, issues, agent brief, code patch)
→ But no approval checkpoints, no run logs, faster feedback loop
→ Done (faster than Example 2, but without audit trail)
```

User took the trade-off (speed vs. auditability) explicitly.

---

## Related

- [Artifact Contracts](../skills/workflow-planner/references/artifact-contracts.yaml) -- What artifacts each skill produces/consumes
- [Execution Modes](../skills/workflow-planner/references/execution-modes.md) -- Details on orchestrator modes (guided, autonomous, yolo)
- [Skill Registry](../skills/workflow-planner/references/skill-registry.yaml) -- Available skills and their interfaces
