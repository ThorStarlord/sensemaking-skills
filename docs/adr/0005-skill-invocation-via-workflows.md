# ADR 0005: Skill Invocation via Workflow Registry (No Direct Skill-to-Skill Calls)

**Status**: Accepted  
**Date**: 2026-05-19  
**Context**: Phase 5 Completion & Workflow Formalization  
**Decision**: Skills do not invoke other skills. Instead, workflows registered in `workflow-registry.yaml` are the unit of execution, and the orchestrator chains skills automatically based on artifact contracts.

---

## Context

### The Original Question
When repo-sensemaker completes and creates a handoff (section 13 of the brief), should it automatically invoke the next skill (workflow-orchestrator)?

### The Design Challenge
In a system with multiple diagnostic skills (problem-framer, unknowns-mapper, repo-sensemaker) and multiple orchestration paths (Fast Path vs. Full Fog Path), how do we:
1. Avoid manual invocation between steps (users shouldn't copy-paste prompts)?
2. Support different chaining patterns (sometimes 2 skills, sometimes 5)?
3. Keep skills reusable (same skill used in different workflows)?
4. Maintain clear artifact contracts (what flows between steps)?

### The Anti-Pattern Considered
**"Skills invoke the next skill as their last action"**
```
repo-sensemaker produces brief, then invokes workflow-orchestrator
  → workflow-orchestrator produces plan, then invokes prompt-handoff
    → prompt-handoff produces prompt, then invokes ??? (no next skill defined)
```

**Problems with this pattern**:
1. **Circular invocation risk**: Skill A calls B, B calls C, C might call A (hard to control)
2. **Skill coupling**: Each skill must know what comes next (reusability problem)
3. **No composition flexibility**: Can't reuse repo-sensemaker in fast-path AND full-fog-path without code changes
4. **Boundary violations**: Skills become orchestrators (violates single responsibility)
5. **Artifact verification gap**: Hard to validate what the next skill receives

---

## Decision

### Core Rule
**Skills are never invoked by other skills. Workflows are the unit of execution. The external orchestrator decides the sequence.**

### Implementation

1. **Workflows are registered in `workflow-registry.yaml`** with:
   - Unique workflow ID
   - Clear purpose (one sentence)
   - Ordered steps (skill → skill sequence)
   - Input requirements (external_context or artifact)
   - Approval gates between steps
   - Artifact flow (what flows between steps)

2. **Users invoke workflows** via:
   ```bash
   python scripts/orchestration-runner.py <workflow-id> --mode guided_execution
   ```

3. **Orchestrator chains skills automatically** based on:
   - Artifact contracts (output of step N → input of step N+1)
   - Execution mode (plan_only, guided_execution, autonomous_execution, yolo_execution)
   - Approval gates (mandatory user approval at defined gates)

4. **Two primary diagnostic workflows formalized**:

   **fast-path-workflow** (1 skill)
   ```yaml
   - id: fast-path-workflow
     purpose: Diagnose repository to identify weakest boundary and recommend workflows
     steps:
       - repo-sensemaker (input: repository_state) → repository_sensemaking_brief
   
   Outputs: Brief with sections 12-14 (recommended workflow, handoff, ready-to-copy prompts)
   User then: Invokes recommended workflow or runs workflow-orchestrator manually
   ```

   **full-fog-workflow** (4 skills)
   ```yaml
   - id: full-fog-workflow
     purpose: Comprehensively analyze vague problems and recommend implementation workflows
     steps:
       - problem-framer (input: raw_fog) → problem_frame
       - unknowns-mapper (input: problem_frame) → unknowns_map
       - repo-sensemaker (input: repository_state) → repository_sensemaking_brief
       - prompt-handoff (input: brief) → prompt_handoff
   
   Outputs: Problem analysis + repository diagnosis + ready-to-copy prompts
   User then: Invokes recommended workflow or runs workflow-orchestrator manually
   ```

### Execution Flow (Default: guided_execution)
1. User invokes: `orchestration-runner.py fast-path-workflow --mode guided_execution`
2. Orchestrator reads workflow definition from registry
3. For each step:
   - Orchestrator invokes the skill with required inputs
   - Skill executes and produces output artifact
   - Orchestrator validates artifact against contract
   - If gate defined: pauses and waits for user approval
   - If gate approved: proceeds to next step
4. Workflow completes when final step finishes or user denies a gate

### Key Guarantees
1. **Explicit Composition**: Workflow definition shows exactly what skills run in what order
2. **Artifact Validation**: Each artifact validated before next step consumes it
3. **Approval Gates**: User can intervene at defined decision points
4. **Reusability**: Same skill (e.g., repo-sensemaker) works in both fast-path and full-fog workflows
5. **No Skill Coupling**: Skills don't know about each other; orchestrator handles dependencies

---

## Design Correction: Restored Orchestrator as Workflow Step (Phase 5b)

**Initial Design (Phase 5 Incomplete)**
```yaml
fast-path-workflow:
  steps:
    - repo-sensemaker → brief  ✅

User then manually invokes workflow-orchestrator or implementation workflow
```

**Issue Discovered**: Manual invocation between diagnostic and implementation workflows breaks the automation requirement: "I want the entire process to be automated from the initial input."

**Final Design (Phase 5b Complete)**
```yaml
fast-path-workflow:
  steps:
    - repo-sensemaker → repository_sensemaking_brief
    - workflow-orchestrator → workflow_orchestration_plan  ✅

full-fog-workflow:
  steps:
    - problem-framer → problem_frame
    - unknowns-mapper → unknowns_map
    - repo-sensemaker → repository_sensemaking_brief
    - workflow-orchestrator → workflow_orchestration_plan  ✅

Configuration (in workflow-registry.yaml):
  auto_invoke_next_workflow: true
  auto_invoke_source: workflow_orchestration_plan.recommended_workflow_id
```

**Why This Works**:
1. **No recursion**: `orchestration-runner.py` is the ENGINE; `workflow-orchestrator` is a SKILL. Engine invokes skill, not itself
2. **Cleaner separation**: Diagnosis workflow identifies the problem; orchestration workflow selects the implementation path
3. **Full automation**: orchestration-runner detects auto_invoke_next_workflow flag after diagnostic workflow completes, reads recommended_workflow_id from the orchestration_plan, and automatically invokes the implementation workflow
4. **Three-stage automation**: User provides initial input → diagnostic workflow → orchestration skill → auto-invocation → implementation workflow (all without manual intervention)
5. **Flexibility**: Same diagnostic workflow works for both fast-path and full-fog; implementation routing is determined by fog_type classification in the orchestration_plan

### Auto-Invocation Implementation

When `auto_invoke_next_workflow: true` is set in a workflow definition:

1. **After workflow completes successfully**, orchestration-runner.py:
   - Checks `auto_invoke_next_workflow` and `auto_invoke_source` fields
   - Reads the source artifact (e.g., `workflow_orchestration_plan`)
   - Parses the YAML machine-readable section
   - Extracts `recommended_workflow_id`

2. **Automatically invokes next workflow**:
   - Runs: `python scripts/orchestration-runner.py {next_workflow_id} --mode {same_mode}`
   - Propagates execution mode (guided_execution → guided_execution, yolo_execution → yolo_execution, etc.)
   - Returns the exit code from the invoked workflow

3. **No manual intervention required**:
   - In `guided_execution` mode: Final gate pauses before auto-invocation; user can approve/deny the implementation workflow
   - In `autonomous_execution` and `yolo_execution` modes: Auto-invocation proceeds immediately without pausing

See [scripts/orchestration-runner.py](scripts/orchestration-runner.py) for the implementation of `_should_auto_invoke_next()`, `_extract_recommended_workflow()`, and `_invoke_next_workflow()`.

## Consequences

### Positive
1. **Clear Flow**: Workflow registry is the source of truth for skill sequences
2. **Artifact Safety**: Contracts enforced; each artifact has clear producer and consumer
3. **Composition Flexibility**: Add new workflows without modifying existing skills
4. **Approval Control**: Users decide between guided_execution (mandatory approval) and autonomous modes
5. **Testability**: Test workflows independently; test skills independently
6. **Reusability**: repo-sensemaker used in fast-path, full-fog, setup, and reconciliation workflows
7. **Auditability**: Run log documents exactly which skills ran, which gates approved/denied
8. **No Recursion Risk**: Diagnostic workflows produce analysis; orchestration is external
9. **Clear Separation**: Diagnosis (what's the problem?) vs. Orchestration (what to do about it?)

### Negative
1. **Workflow Proliferation**: System has many workflow definitions to maintain
2. **Two-Step Invocation**: Run diagnostic workflow first, then run implementation workflow
3. **No Implicit Chaining**: Can't just invoke repo-sensemaker and expect full pipeline
4. **Registry Maintenance**: Workflow registry must stay in sync with skill changes
5. **User Decision Point**: User must choose which implementation workflow to run (not automatic)

### Trade-offs
We chose **diagnostic workflows + external orchestration** over embedded orchestration because:
- **Recursion avoidance**: Orchestrator is external, not embedded in workflow steps
- **Separation of concerns**: Diagnosis workflow ≠ Orchestration workflow
- **Flexibility**: User can choose different implementation workflows based on brief recommendations
- **Artifact-driven handoff**: Brief itself is the API; no workflow-to-workflow invocation needed
- **Testability**: Can test diagnostic workflow independently; can test orchestration independently
- **Clarity**: Clear boundary between "what's the problem?" (diagnostic) and "what do we do?" (orchestration)

---

## Alternatives Considered

### Alternative 1: Skills Invoke the Next Skill
- Skills call each other: repo-sensemaker → workflow-orchestrator → prompt-handoff
- **Rejected because**:
  - Tight coupling; can't reuse repo-sensemaker in different workflows without code changes
  - No approval gates; user can't intervene between steps
  - Hard to compose different orderings (fast-path vs. full-fog require different code)
  - Circular invocation risk if workflows form loops

### Alternative 2: Implicit Skill Chaining Based on Artifact Type
- Orchestrator infers next skill from artifact type (if output is brief → invoke orchestrator)
- **Rejected because**:
  - Same artifact type might need different next skills in different contexts
  - Hard to validate; can't tell if inferred chaining is correct
  - No explicit control over skill sequence

### Alternative 3: Skill Dependencies in Skill Definitions
- Each skill lists its downstream skills; orchestrator reads this to chain
- **Rejected because**:
  - Modifies skills for orchestration concerns (violates separation of concerns)
  - Still creates tight coupling; can't easily change skill sequence
  - Harder to maintain; skill definitions become complex

### Alternative 4: Nested Workflows
- Workflows can invoke other workflows as steps
- **Rejected because**:
  - Adds orchestrator complexity (recursive invocation handling)
  - Harder to validate (what gates apply to nested workflows?)
  - Late binding makes artifact validation difficult

---

## Evidence

This decision was validated during Phase 5 and corrected in Phase 5b (workflow registry formalization):

### Initial Design Validation (Phase 5)
- Orchestrator skill invocation framework implemented
- All 5 execution modes proven (plan_only, prompt_chain, guided_execution, autonomous_execution, yolo_execution)
- Approval gates working correctly
- Artifact contracts validated
- 21+ independent workflow runs with zero repeatable failures

### Design Correction (Phase 5b: Workflow Registry Formalization)
- **Issue Found**: Including workflow-orchestrator as a step in diagnostic workflows creates recursion risk
- **Solution Applied**: Separated diagnostic workflows from orchestration
  - fast-path-workflow now produces repository_sensemaking_brief (1 step)
  - full-fog-workflow produces problem frame + unknowns map + brief + prompts (4 steps)
  - User/orchestrator chooses implementation workflow separately
- **Validation**: 
  - ✓ Recursion issue resolved
  - ✓ Workflows pass validate-repo.py checks
  - ✓ Artifact contracts match between steps
  - ✓ Clear handoff points via brief sections 12-14

### Real-World Validation
- Diagnostic workflows execute without recursion issues
- Brief artifacts contain all information needed for next workflow selection
- Ready-to-copy prompts enable manual workflow invocation
- Approval gates provide user control at each diagnostic step
- Design follows artifact-driven engineering principle: artifacts are the API between workflows

---

## Implications for Future Decisions

1. **Workflow Design**: Every new workflow must have a purpose and explicit step sequence
2. **Skill Development**: Skills should NOT decide what comes next; they produce artifacts
3. **Artifact Contracts**: Must be maintained for every artifact type and workflow
4. **Approval Gates**: Should be explicit in workflow definition, not decided by skills
5. **Composition**: Use workflow registry to compose skills; don't embed composition in skill code

---

## Related Documents

- **Pattern**: See `orchestration-patterns.md` → Pattern 2: Workflow Separation of Concerns
- **Guide**: `workflow-design-guide.md` → Designing Workflows
- **Reference**: `workflow-registry.yaml` → All registered workflows
- **Reference**: `artifact-contracts.yaml` → All artifact contracts
- **Status**: Phase 5 Complete (PHASE5_SKILL_INVOCATION.md)

---

## For Workflow Designers

When adding a new workflow:

1. **Write your workflow's purpose** (one sentence)
2. **List the skills** that advance this purpose
3. **Order them** by artifact dependency (what flows between steps)
4. **Define approval gates** where user decisions are needed
5. **Register in workflow-registry.yaml** with:
   - id: unique workflow ID
   - purpose: one-sentence purpose
   - initial_inputs: what the user provides
   - steps: skill sequence
   - allowed_execution_modes: which modes this workflow supports
   - gates: approval decision points

**Example workflow entry:**
```yaml
- id: my-workflow
  display_name: My Workflow Name
  purpose: Brief one-sentence description of what this workflow does
  initial_inputs:
    - id: input_context
      type: external_context
      description: What the user must provide
  allowed_execution_modes:
    - plan_only
    - guided_execution
  steps:
    - id: 1
      skill: skill-a
      input_source: input_context
      output_artifact: artifact_a
      gate: review_step_1
    - id: 2
      skill: skill-b
      input_artifact: artifact_a
      output_artifact: artifact_b
      gate: review_step_2
```

---

## Acceptance Criteria

This decision is accepted when:
- ✓ fast-path-workflow registered (2 skills: repo-sensemaker → workflow-orchestrator)
- ✓ full-fog-workflow registered (4 skills: problem-framer → unknowns-mapper → repo-sensemaker → workflow-orchestrator)
- ✓ Diagnostic workflows produce orchestration_plan with fog_type and recommended_workflow_id
- ✓ Orchestration-runner.py implements auto-invocation (reads auto_invoke_next_workflow and auto_invoke_source from workflow registry)
- ✓ Auto-invocation extracts recommended_workflow_id from orchestration_plan machine-readable section
- ✓ Auto-invocation invokes next workflow with same execution mode
- ✓ No recursion risk (orchestration-runner is engine; workflow-orchestrator is skill)
- ✓ Artifact contracts validated between all steps
- ✓ Approval gates work correctly in guided_execution mode
- ✓ README documents three-stage automation: diagnostic → orchestration → auto-invoked implementation
- ✓ No skills directly invoke other skills (only orchestration-runner engine invokes workflows)
- ✓ ADR documents design correction and auto-invocation implementation
- ✓ Validation (validate-repo.py) passes for all workflows

---

## Questions & Answers

**Q: What if a skill needs to decide what comes next?**  
A: That's a workflow decision, not a skill decision. The workflow designer decides the sequence. If you need conditional logic, use approval gates: the workflow pauses and asks the user to choose the next action.

**Q: Can skills be invoked individually?**  
A: Technically yes, but not the intended usage. The intended path is always via a workflow. Individual skill invocation is for debugging or specialized use cases, not production.

**Q: What if I want a skill to work in multiple workflows with different next steps?**  
A: Exactly! That's the benefit of this design. The same skill (e.g., repo-sensemaker) can be used in:
- fast-path-workflow (followed by workflow-orchestrator)
- full-fog-workflow (followed by workflow-orchestrator)
- setup-sensemaking-repo (followed by prompt-handoff)
The skill doesn't know or care which workflow it's in.

**Q: How do I add a new workflow without modifying skills?**  
A: Just register it in workflow-registry.yaml. The orchestrator reads the registry and handles everything. No skill code changes needed.

**Q: What about workflows that sometimes need different skill sequences?**  
A: Create separate workflows. Don't try to make one workflow do multiple things. Better to have fast-path-workflow and full-fog-workflow than one "mega-workflow" with optional steps.

**Q: Can workflows call other workflows?**  
A: Not yet (would require nested workflow support in orchestrator). For now, compose by artifact flow: workflow A produces artifact X → workflow B consumes artifact X.

---

## Conclusion

By making workflows the unit of execution and formalizing them in the registry, we achieve:
1. **Clear composition**: Exact skill sequence visible in workflow definition
2. **Loose coupling**: Skills don't know about each other
3. **Artifact safety**: Contracts enforced between steps
4. **Approval control**: Users decide between guided and autonomous modes
5. **Reusability**: Skills used across multiple workflows
6. **Auditability**: Full run logs document every decision

This design resolves the original question: **No, skills should not invoke other skills. The workflow orchestrator does the invoking.**
