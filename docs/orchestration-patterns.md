# Orchestration Patterns

This document captures the key design patterns discovered through implementing and fixing the sensemaking-skills orchestration system. These patterns prevent common mistakes and guide the design of new workflows.

---

## Pattern 1: Strict vs. Lenient Validation

### The Pattern

Different execution modes require different validation rigor:

- **Plan Modes** (`plan_only`, `prompt_chain`) — Artifacts don't exist yet; validation should be **lenient** (warn only)
- **Execution Modes** (`guided_execution`, `autonomous_execution`, `yolo_execution`) — Artifacts must be produced; validation should be **strict** (fail on missing artifacts)

### When to Use

Use this pattern whenever your validator needs to work across multiple execution modes. Ask: "Does this artifact exist yet, or is it being planned?"

**Example**: workflow-runtime.py validates artifact production:
```python
# Strict in execution modes - fail if artifact missing
if self.mode in ("guided_execution", "autonomous_execution", "yolo_execution"):
    if not artifact_file_exists:
        self.errors.append(f"ARTIFACT_NOT_FOUND: {artifact}")
        return FAILED
# Lenient in plan modes - just warn
else:
    print(f"~ Artifact not yet produced (expected after execution)")
```

### When NOT to Use

Don't use lenient validation in production execution pipelines. A lenient validator that should fail gives users false confidence.

### Trade-offs

- **Strict**: Catches errors early but requires artifacts to actually exist
- **Lenient**: Allows planning ahead but misses silent failures

### Reference

See ADR: [0001-strict-validation-in-execution-modes.md](adr/0001-strict-validation-in-execution-modes.md)

---

## Pattern 2: Workflow Separation of Concerns

### The Pattern

Each workflow should have **one clear purpose**. Don't mix unrelated transformations in the same workflow.

**Anti-pattern (avoided)**:
```yaml
docs-architecture:
  steps:
    - docs-aligner        # Purpose: domain alignment
      → domain_alignment_report
    - to-prd                 # Purpose: PRD generation ❌ MIXING CONCERNS
      → prd
    - handoff                # Purpose: prepare prompt
      → prompt_handoff
```

**Correct pattern**:
```yaml
docs-architecture:
  steps:
    - docs-aligner        # Purpose: domain alignment
      → domain_alignment_report
    - handoff                # Purpose: prepare prompt
      → prompt_handoff

product-to-issues:           # ✅ DEDICATED PURPOSE
  steps:
    - to-prd                 # Purpose: PRD generation (proper home)
      → prd
    - to-issues              # Purpose: issue generation
      → issue_list
    - triage                 # Purpose: assignment → briefs
      → agent_brief
```

### Why It Matters

When workflows mix concerns:
1. Output artifacts don't have clear consumers (prd from docs-architecture wasn't consumed there)
2. Skills don't know where their output goes (to-prd wasn't sure if its PRD would be used)
3. Validators get confused (does prd need to exist in this workflow? depends!)
4. New developers can't understand the intent

### When to Use

Use this when designing a new workflow:
1. Write the workflow's **purpose statement** (one sentence)
2. Identify each step's **input → transformation → output**
3. Ask: "If I remove this step, is the workflow still coherent?"
4. If yes, the workflow has a clear purpose
5. If no, split into multiple workflows

### When NOT to Use

Don't split workflows for convenience when they're genuinely one transformation chain. Example: `prd → issues → briefs` is one coherent chain (not three separate workflows) because each step meaningfully transforms the input.

### Trade-offs

- **Unified workflows**: Simpler for users, but can hide mixing of concerns
- **Separated workflows**: Clearer intent, but requires more workflow definitions

### Reference

See ADR: [0002-workflow-separation-of-concerns.md](adr/0002-workflow-separation-of-concerns.md)

---

## Pattern 3: Artifact Composition & Chaining

### The Pattern

Each step in a workflow should meaningfully transform its input artifact to produce a semantically different output.

**Good composition** (each step transforms):
```
domain_alignment_report  (document: what we know about domain)
         ↓ to-prd
       prd              (document: what to build)
         ↓ to-issues
    issue_list          (list: specific tasks)
         ↓ triage
    agent_brief         (document: assignment to agent)
```

**Bad composition** (pass-through, no transformation):
```
domain_alignment_report
         ↓ copy-and-rename
    prd_draft           (same content, different name) ❌
         ↓ format-prettily
    prd                 (still same content) ❌
```

### Why It Matters

Meaningful transformation means:
1. Each skill adds value (clarity, specificity, actionability)
2. Validators can check that transformation happened (prd != alignment_report)
3. Users understand why each step exists
4. Skills are reusable (to-prd works with any alignment_report)

### Composition Rules

1. **Input ≠ Output**: The output artifact is semantically different from the input
2. **No Pass-Through Steps**: Every step should transform, not just rename/format
3. **Artifact Contracts Match**: Step's output_artifact must match next step's input_artifact
4. **Clear Intent**: You can explain what each step does in one sentence

### When to Use

Use when designing a workflow's step sequence. For each step, ask:
- "What does this step know that the previous step didn't?"
- "If I skip this step, can the next step work with the input directly?"

If the answer is "no, it adds essential information," the step is valid. If "yes, this is just reformatting," consider removing it.

### When NOT to Use

Don't over-compose by adding unnecessary transformations just to have more steps. A 2-step workflow that meaningfully transforms is better than a 5-step workflow with filler.

### Reference

See ADR: [0003-artifact-composition-pattern.md](adr/0003-artifact-composition-pattern.md)

---

## Pattern 4: Evidence Tracking for Trust

### The Pattern

Record which validators exercised which artifacts and which gates approved steps. This creates an audit trail proving the system works.

**Evidence entry** (mode-coverage.yaml):
```yaml
- mode: guided_execution
  workflow_id: product-to-issues
  validators_exercised:
    - level_1: validate-repo.py
    - dispatcher: validate-output.py (prd)
    - dispatcher: validate-output.py (issue_list)
    - dispatcher: validate-output.py (agent_brief)
  gates_exercised: true
  gates_note: 3 approved, 0 denied
  hardening_triggered: none
  notes: Full pipeline proven end-to-end; all artifacts validated
```

### Why It Matters

Without evidence:
- You can't tell if a success was real or lucky
- You don't know which parts were actually validated
- New operators don't know what to trust

With evidence:
- You can point to specific validators that checked specific artifacts
- You know which gates caught problems (or didn't)
- You have proof the system works as designed

### Tracking Requirements

1. **Machine-Produced**: Evidence should come from workflow-runtime.py, not hand-written
2. **Artifact-Specific**: Record which validators ran for which artifacts
3. **Gate-Specific**: Record which gates approved/denied and why
4. **Hardening-Triggered**: Record if validators found issues that caused hardening
5. **Session-Traced**: Link evidence to a specific workflow run

### When to Use

Use after every workflow execution in production/test modes:
1. Run completes
2. workflow-runtime.py logs which validators ran
3. Update mode-coverage.yaml with the evidence
4. Next time someone questions the system, show the evidence

### When NOT to Use

Don't create fake evidence. If a validator didn't run, don't claim it did. If a gate didn't actually approve, don't claim it did.

### Reference

See ADR: [0004-evidence-tracking-for-trust.md](adr/0004-evidence-tracking-for-trust.md)

---

## Applying These Patterns

### For Workflow Design

1. State your workflow's **purpose** (one sentence)
2. List each **step's transformation** (input → skill → output)
3. Check each step against **Composition Pattern**:
   - Does it meaningfully transform?
   - Is the output consumed by the next step?
4. Verify against **Separation Pattern**:
   - Does every step align with the stated purpose?
   - Could any step be moved to a different workflow?
5. Run through **Validation Pattern**:
   - What validators apply to each artifact?
   - Should they be lenient (planning) or strict (execution)?
6. Plan **Evidence Tracking**:
   - Which validators will you exercise?
   - What gates will you need?

### For Skill Design

1. Understand where your skill appears (which workflows use it?)
2. Verify your **input artifact** is what you expect
3. Verify your **output artifact** will be consumed by next step
4. Check you don't **mix concerns** (one skill, one purpose)
5. Document your **boundaries** (what you will/won't do)

### For Validator Design

1. Decide on **validation rigor** (strict vs. lenient)
2. Define **error codes** (stable, reusable)
3. Test with **positive fixtures** (valid artifacts)
4. Test with **negative fixtures** (invalid artifacts showing each error)
5. Document **execution modes** (which modes invoke which validators?)

---

## Common Mistakes to Avoid

| Mistake | Pattern | Solution |
|---------|---------|----------|
| Artifact missing in execution mode | Strict vs. Lenient | Use strict validation in execution modes |
| PRD generation mixed with domain alignment | Separation | Move PRD generation to separate workflow |
| Steps that don't transform input | Composition | Remove pass-through steps or group with meaningful steps |
| No record of what was validated | Evidence | Update mode-coverage.yaml after each run |
| Skill does too many things | Separation | Split into multiple skills or constrain to one purpose |
| Validator runs in wrong mode | Strict vs. Lenient | Check mode before validating strictly |

---

## Real-World Example: product-to-issues

This workflow demonstrates all four patterns:

**Separation of Concerns** ✓
- Purpose: "Transform domain alignment into implementation briefs"
- Separated from docs-architecture (which has different purpose)

**Composition & Chaining** ✓
- Step 1: alignment_report → **to-prd** → prd (transforms: overview → spec)
- Step 2: prd → **to-issues** → issue_list (transforms: spec → tasks)
- Step 3: issue_list → **triage** → agent_brief (transforms: tasks → assignment)
- Each step meaningfully transforms

**Strict Validation** ✓
- Execution mode: guided_execution (production use)
- Each step's output validated strictly (artifact must exist)
- Gates enforce human review at each stage

**Evidence Tracking** ✓
- mode-coverage.yaml records:
  - Which validators ran (validate-output.py for prd, issue_list, agent_brief)
  - Gates exercised (3 gates, all approved)
  - Hardening status (none triggered)

---

## Further Reading

- `CONTEXT.md` — Overall system philosophy and domain terms
- `workflow-design-guide.md` — Step-by-step guide for designing new workflows
- `docs/adr/` — Detailed rationale for each pattern
- `skill-registry.yaml` — Registry of all available skills and their purposes
