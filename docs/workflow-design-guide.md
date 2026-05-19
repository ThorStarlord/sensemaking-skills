# Workflow Design Guide

A step-by-step guide for designing new workflows in the sensemaking-skills orchestration system. Use this checklist to ensure your workflow follows the patterns and is production-ready.

---

## Pre-Design Phase

### 1. Define Your Purpose

Write **one sentence** describing what your workflow does. This should be clear enough that someone unfamiliar with the project understands immediately.

**Good examples:**
- "Transform a domain alignment report into a PRD, then into implementation issues"
- "Diagnose a repository's structure and produce a sensemaking brief"
- "Create a problem frame from raw customer feedback"

**Bad examples:**
- "Do analysis and generate output" (vague)
- "Multiple steps for implementation" (doesn't say what)
- "Workflow to improve the system" (improves what? how?)

**Your purpose**: ___________________________________________

### 2. Identify Your Input Artifact

What artifact does this workflow consume? (This is your starting point.)

Check: Does this artifact exist or will users provide it?

**Options:**
- External input (user provides raw content)
- Output from another workflow (feed them together)
- Generated on-demand (workflow produces its own input)

**Your input artifact**: ___________________________________________

**Source**: ___________________________________________

### 3. Identify Your Final Output Artifact

What artifact will this workflow produce? (This is your deliverable.)

Check: Who will consume this artifact? Which other workflows or users?

**Your output artifact**: ___________________________________________

**Consumers**: ___________________________________________

---

## Design Phase: Build Your Step Sequence

### 4. List Your Steps (Rough)

For each transformation needed to go from input → output, add a step.

Ask yourself: "What skill transforms X into Y?"

**Example for product-to-issues workflow:**

| Input | Skill | Output |
|-------|-------|--------|
| domain_alignment_report | to-prd | prd |
| prd | to-issues | issue_list |
| issue_list | triage | agent_brief |

**Your steps** (fill in the table):

| Input | Skill | Output |
|-------|-------|--------|
| ______________ | ______________ | ______________ |
| ______________ | ______________ | ______________ |
| ______________ | ______________ | ______________ |

### 5. Verify Each Step Transforms Meaningfully

For each step, ask: "Does the output contain information the input didn't?"

**Good transformations:**
- alignment_report → prd: Added "what to build" spec
- prd → issues: Added "specific, actionable tasks"
- issue_list → agent_brief: Added "agent assignments"

**Bad transformations (remove these):**
- prd → prd_formatted: Just prettier output, no new info
- issues → issue_summary: Same info, shorter version
- brief → brief_copy: Exact duplicate

**Fix**: Remove steps that don't transform. If you need formatting, do it in the previous step.

### 6. Check Artifact Chain Continuity

For each step, verify: **output of step N = input of step N+1**

**Example:**
```
Step 1: to-prd takes domain_alignment_report, produces prd ✓
Step 2: to-issues takes prd ✓ (matches Step 1 output)
Step 3: triage takes issue_list ✗ (Step 2 produced issue_list, but...)
        Wait, does Step 2 actually produce issue_list? Check! Yes ✓
```

**Your chain** (verify each link):
- Step 1 input (__) → Step 1 output (__)
- Step 2 input (__) should equal Step 1 output (__) ✓?
- Step 2 output (__) → Step 3 input (__) ✓?
- ...

### 7. List Available Skills

Check `skill-registry.yaml` for skills that produce each artifact you need.

**Example search:**
```bash
# Find skills that produce 'prd'
grep -B5 "artifact: prd" skills/workflow-planner/references/skill-registry.yaml
# Result: to-prd (in drafting ecosystem), prd (in product ecosystem)
```

**Question for each step**: Is there a registered skill for this transformation? If not, you may need to:
- Use an external skill (plugin)
- Create a new skill (bigger project)
- Reconsider the step

**Verification checklist:**
- [ ] All skills exist in skill-registry.yaml
- [ ] Each skill's input_artifact matches what you're feeding it
- [ ] Each skill's output_artifact matches what you expect

---

## Validation Phase: Prevent Design Mistakes

### 8. Check Against Separation Pattern

Does your workflow have **one clear purpose**, or does it mix multiple concerns?

**Test**: Can you split off any steps into a different workflow without losing coherence?

**Example (bad design caught)**:
- Original: docs-architecture did domain_alignment + PRD generation
- Problem: Two different purposes in one workflow
- Solution: Create product-to-issues as separate workflow for PRD
- Result: Now each workflow has one purpose ✓

**Your workflow**: Does every step advance toward ONE goal? Yes / No / Unclear

If unclear, ask: "Could I split this at the red line?"
```
Step 1: domain alignment ← CAN I SPLIT HERE?
Step 2: PRD generation ← Different purpose!
Step 3: issue generation ← Also different!
```

If yes, you may need to split into multiple workflows.

### 9. Check Against Composition Pattern

Does each step meaningfully transform its input?

**For each step, fill in:**

| Step | Input | Transformation | Output | Adds Value? |
|------|-------|---|--------|---------|
| 1 | alignment_report | Extract "what to build" spec | prd | Yes (adds spec) |
| 2 | prd | Break into actionable items | issue_list | Yes (adds tasks) |
| 3 | issue_list | Assign to agents | agent_brief | Yes (adds ownership) |

**Your steps:**

| Step | Input | Transformation | Output | Adds Value? |
|------|-------|---|--------|---------|
| 1 | __ | __ | __ | ? |
| 2 | __ | __ | __ | ? |
| 3 | __ | __ | __ | ? |

Any "No" answers? If so, remove or combine that step.

### 10. Define Execution Modes

Which execution modes will this workflow support?

**Options** (ordered by strictness):
- `plan_only` — Just generate the plan, don't execute
- `prompt_chain` — Generate prompts for manual execution
- `guided_execution` — Execute with human gates at each step (most common)
- `autonomous_execution` — Execute automatically with audit gates
- `yolo_execution` — Execute fully automated without gates (risky, rare)

**Question**: Which modes make sense for your workflow?
- Complex workflows with high stakes → guided_execution only
- Well-proven workflows with good automation → autonomous_execution
- Simple proof-of-concept → plan_only or prompt_chain

**Your workflow**: Will support _____________ execution mode(s)

### 11. Define Gates (Decision Points)

For each step in `guided_execution` mode, what decision points do you need?

A **gate** is a human approval point. Ask:
- "Before this step runs, should someone review and approve?"
- "What could go wrong at this step that we'd want to catch?"

**Example for product-to-issues:**
- Gate after Step 1 (to-prd): `review_prd` — Is the PRD good?
- Gate after Step 2 (to-issues): `review_issues` — Are the issues actionable?
- Gate after Step 3 (triage): `review_agent_brief` — Is the assignment clear?

**Your gates:**

| Step | Gate ID | Decision | Approval Criteria |
|------|---------|----------|------------------|
| 1 | __________ | ________ | ________ |
| 2 | __________ | ________ | ________ |
| 3 | __________ | ________ | ________ |

### 12. Check Against Validation Pattern

For each artifact, determine: Should validation be **strict** or **lenient**?

**Rule of thumb:**
- **Planning modes** (plan_only, prompt_chain) → lenient (artifacts don't exist yet)
- **Execution modes** (guided, autonomous, yolo) → strict (artifacts must be produced)

**Your validation strategy:**

| Artifact | Mode | Strictness | Reason |
|----------|------|-----------|--------|
| prd | guided_execution | Strict | Must exist before review gate |
| prd | plan_only | Lenient | Just planning, ok if not created |

---

## Implementation Phase: Register Your Workflow

### 13. Add to workflow-registry.yaml

```yaml
- id: your-workflow-id
  display_name: Your Workflow Display Name
  purpose: One sentence describing what this workflow does
  initial_inputs:
    - id: input_artifact_id
      type: artifact
      required: true
      description: Description of input
  allowed_execution_modes:
    - guided_execution
  steps:
    - id: 1
      skill: skill_name_1
      step_type: local_execution
      gate: gate_id_1
      input_artifact: input_artifact_1
      output_artifact: output_artifact_1
    - id: 2
      skill: skill_name_2
      step_type: local_execution
      gate: gate_id_2
      input_artifact: input_artifact_2
      output_artifact: output_artifact_2
```

### 14. Verify Workflow Registry Entry

Run syntax check:
```bash
python -c "import yaml; yaml.safe_load(open('skills/workflow-planner/references/workflow-registry.yaml'))"
# Expected: No output (valid YAML)
```

Test planning:
```bash
python scripts/workflow-runtime.py your-workflow-id --mode plan_only
# Expected: All steps listed, artifacts shown
```

### 15. Add Artifact Contracts

For each new output artifact, define a contract in `artifact-contracts.yaml`:

```yaml
prd:
  produced_by: to-prd
  consumed_by: [to-issues, product-discovery-sprint]
  required_sections: [Overview, Goals, Success Metrics, Requirements]
  required_machine_fields: [artifact_id, version, created_at]
  verification_commands:
    - python scripts/validate-prd.py <artifact_path>
  validators:
    level_2: validate-artifact.py
    level_3: validate-prd.py
```

---

## Testing Phase: Verify Your Design

### 16. Test Workflow Structure

```bash
# Verify workflow parses
grep -A 30 "id: your-workflow-id" skills/workflow-planner/references/workflow-registry.yaml

# Test orchestrator recognition
python scripts/workflow-runtime.py --list-workflows | grep your-workflow-id
# Expected: Workflow listed with purpose
```

### 17. Test Step Sequence

```bash
# Plan a run
python scripts/workflow-runtime.py your-workflow-id --mode plan_only

# Verify:
# - All steps listed in order
# - Artifacts flow correctly (step N output → step N+1 input)
# - No artifacts missing
# - Gates listed correctly
```

### 18. Test Artifact Validation

For each artifact your workflow produces:

```bash
# List available validators
python scripts/validate-workflow-design.py --list-codes

# Test validator on a sample artifact
python scripts/validate-artifact.py artifacts/sample_prd.md
# Expected: PASS (no errors)
```

### 19. Test Against Design Patterns

Run the workflow design validator:

```bash
python scripts/validate-workflow-design.py skills/workflow-planner/references/workflow-registry.yaml
# Expected: PASS (no design errors)
```

---

## Documentation Phase: Record Your Decisions

### 20. Document Your Workflow

Add a reference document in `docs/`:

**Filename**: `workflow-YOUR_WORKFLOW_ID.md`

**Contents**:
```markdown
# your-workflow-id Workflow

## Purpose
[One sentence purpose]

## Input
- Artifact: [artifact_id]
- Source: [where it comes from]

## Output
- Artifact: [artifact_id]
- Consumers: [who uses it]

## Steps
1. [skill]: [input] → [output]
2. [skill]: [input] → [output]

## Execution Modes
- [List supported modes]

## Gates
- [List gates and their decisions]

## Design Patterns Used
- [List which patterns this workflow demonstrates]
- Separation: Yes/No (does it have one clear purpose?)
- Composition: Yes/No (do steps meaningfully transform?)
- Validation: [Strict/Lenient per mode]

## References
- [Link to workflow-registry entry]
- [Link to relevant patterns]
```

---

## Checklist: Workflow Ready for Production

Before deploying your workflow, verify all these:

- [ ] **Purpose**: One clear, understandable sentence
- [ ] **Steps**: Each meaningful transformation, no pass-through steps
- [ ] **Artifacts**: Input/output well-defined, contracts exist
- [ ] **Skills**: All registered in skill-registry.yaml
- [ ] **Chain**: Output of step N matches input of step N+1
- [ ] **Separation**: Single purpose, not mixing concerns
- [ ] **Composition**: Each step adds semantic value
- [ ] **Modes**: Appropriate execution modes selected
- [ ] **Gates**: Clear approval points defined
- [ ] **Validation**: Strict/lenient rules clear
- [ ] **Registry**: Entered in workflow-registry.yaml with valid YAML
- [ ] **Syntax**: YAML parses without errors
- [ ] **Planning**: `workflow-runtime.py --mode plan_only` succeeds
- [ ] **Validation**: No design errors from validate-workflow-design.py
- [ ] **Documentation**: Workflow documented with purpose/steps/modes
- [ ] **Tests**: Workflow has positive (valid) test fixtures

---

## Example: Complete Workflow Design

Here's the product-to-issues workflow fully documented:

**Purpose Statement:**
"Transform a domain alignment report into a PRD, then into specific implementation issues and agent briefs"

**Step Sequence:**
1. to-prd: alignment_report → prd (transforms: overview → spec)
2. to-issues: prd → issue_list (transforms: spec → tasks)
3. triage: issue_list → agent_brief (transforms: tasks → assignments)

**Execution Mode**: guided_execution (human gates at each step)

**Gates**:
- review_prd: Approve PRD before issue generation
- review_issues: Approve issues before triage
- review_agent_brief: Approve assignments before handoff

**Validation**:
- Strict for execution mode (all artifacts must exist)
- No plan_only mode (requires actual execution)

**Pattern Compliance**:
- ✓ Separation: Single purpose (PRD → issues → briefs)
- ✓ Composition: Each step transforms meaningfully
- ✓ Strict Validation: Execution mode requires artifact production
- ✓ Evidence Tracking: Gates record approvals in run logs

**Result**: Clean, understandable, production-ready workflow

---

## Quick Reference

**Ask yourself these questions in order:**

1. What is my workflow's **one purpose**? (If you have multiple purposes, split into workflows)
2. What **input artifact** do I start with?
3. What **output artifact** do I produce?
4. What **skills** transform input → output? (Check skill-registry.yaml)
5. Does each step **meaningfully transform**? (No pass-throughs)
6. Is the **artifact chain continuous**? (Step 1 out = Step 2 in?)
7. What **execution modes** do I support? (plan_only / guided_execution / autonomous_execution)
8. Where are my **decision gates**? (Which steps need approval?)
9. Is my **validation strict or lenient**? (Execution mode = strict)
10. Have I **documented** the workflow and its decisions?

If you can answer all 10 with confidence, your workflow is ready for production.
