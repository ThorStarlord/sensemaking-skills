# Dynamic Chaining: Conditional Skill Steps Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enable workflows to conditionally route through research/discovery skills based on input fog clarity, determined by unknowns_map analysis.

**Architecture:** 
Workflows support conditional Skill Steps defined in workflow-registry.yaml. When unknowns-mapper produces an unknowns_map artifact with `research_needed == true`, the workflow executor inserts a discovery/research skill before proceeding to repo-sensemaker. The routing decision is based on a provisional heuristic: `research_needed = (unknowns_count >= 5) OR (clarity_assessment == "low")`. This is validated empirically in early value-production runs, then refined based on actual outcomes.

**Tech Stack:** YAML registries, Python validators, artifact contracts, workflow orchestration.

---

## File Structure

**Contracts & Registries:**
- `skills/workflow-orchestrator/references/artifact-contracts.yaml` — Add unknowns_map machine fields, wire up new validator
- `skills/workflow-orchestrator/references/workflow-registry.yaml` — Define conditional step schema in an example workflow

**Templates & Skill Docs:**
- `skills/unknowns-mapper/references/unknowns-map-template.md` — Add YAML block for machine-readable routing fields
- `skills/unknowns-mapper/SKILL.md` — Document the routing heuristic and machine fields

**Validators (new & modified):**
- `scripts/validate-unknowns-map.py` (new) — Validate unknowns_map machine fields (research_needed, clarity_assessment, unknowns_count)
- `scripts/validate-plan.py` (modify) — Add validation for conditional step routing logic

**Documentation:**
- `CONTEXT.md` — Document the implementation details and heuristic
- Implementation in workflow definitions themselves (no new infrastructure file needed)

---

## Task Breakdown

### Task 1: Extend unknowns_map artifact contract

**Files:**
- Modify: `skills/workflow-orchestrator/references/artifact-contracts.yaml`

**Context:** unknowns_map currently has no machine-readable fields. We need to declare the fields used for routing decisions so validators can enforce them.

- [ ] **Step 1: Add required_machine_fields to unknowns_map contract**

Open `artifact-contracts.yaml` and find the `unknowns_map` section (around line 24). Update it:

```yaml
  - id: unknowns_map
    produced_by: unknowns-mapper
    consumed_by:
      - repo-sensemaker
      - prompt-handoff
    required_sections:
      - knowns
      - unknowns
      - assumptions
      - risks
      - research_paths
      - stopping_rule
    required_machine_fields:
      - clarity_assessment
      - unknowns_count
      - assumptions_count
      - research_needed
    verification:
      generic_validator: "python scripts/validate-artifact.py unknowns_map {artifact_path}"
      specialized_validators:
        - "python scripts/validate-unknowns-map.py {artifact_path}"
      required_for_modes:
        - guided_execution
        - autonomous_execution
        - yolo_execution
```

- [ ] **Step 2: Verify syntax by checking artifact-contracts.yaml loads as valid YAML**

Run:
```bash
python -c "import yaml; yaml.safe_load(open('skills/workflow-orchestrator/references/artifact-contracts.yaml'))"
```

Expected: No output (file is valid YAML).

- [ ] **Step 3: Commit**

```bash
git add skills/workflow-orchestrator/references/artifact-contracts.yaml
git commit -m "feat: add machine fields to unknowns_map contract for routing decisions"
```

---

### Task 2: Extend unknowns-map template with YAML block

**Files:**
- Modify: `skills/unknowns-mapper/references/unknowns-map-template.md`

**Context:** The template shows the narrative sections but doesn't have a machine-readable YAML block. We need to add one showing the structure that unknowns-mapper will produce.

- [ ] **Step 1: Add machine-readable YAML block to template**

Append to the end of `unknowns-map-template.md`:

```markdown
## 7. Machine-readable routing

```yaml
clarity_assessment: "high"  # "high", "medium", "low" — overall fog clarity after analysis
unknowns_count: 3            # Number of explicit unknowns identified
assumptions_count: 2         # Number of unvalidated assumptions
research_needed: false       # true if (unknowns_count >= 5) OR (clarity_assessment == "low")
```

These fields are used for dynamic routing decisions in workflows. When `research_needed == true`, a discovery/research skill is inserted before proceeding to repo-sensemaker.
```

- [ ] **Step 2: Verify the markdown is valid**

Run:
```bash
grep -A 10 "Machine-readable routing" skills/unknowns-mapper/references/unknowns-map-template.md
```

Expected: Output shows the YAML block.

- [ ] **Step 3: Commit**

```bash
git add skills/unknowns-mapper/references/unknowns-map-template.md
git commit -m "docs: add machine-readable routing block to unknowns-map template"
```

---

### Task 3: Update unknowns-mapper SKILL.md to document routing

**Files:**
- Modify: `skills/unknowns-mapper/SKILL.md`

**Context:** The skill needs to document that it now outputs routing signals. Add a new section explaining the heuristic and what unknowns-mapper should produce.

- [ ] **Step 1: Add Routing Signals section to SKILL.md**

Find the "Boundary Rule" section (line 35). Insert before it:

```markdown
## Routing Signals

The unknowns_map now includes **machine-readable routing fields** that determine if downstream skills should be inserted into the workflow:

- **clarity_assessment**: Overall assessment of fog clarity ("high", "medium", "low")
- **unknowns_count**: Count of explicit unknowns
- **assumptions_count**: Count of unvalidated assumptions
- **research_needed**: Boolean flag (true if (unknowns_count >= 5) OR (clarity_assessment == "low"))

**Heuristic (Provisional):** If clarity is low or unknowns are numerous, `research_needed = true` signals that a discovery or research skill should be inserted before proceeding to repo-sensemaker. This heuristic is validated empirically in early value-production runs and refined based on outcomes.

**Responsibility:** unknowns-mapper is responsible for analyzing the problem frame and repository context, then making a judgment call on clarity and counting unknowns. The router (workflow executor) reads `research_needed` and makes the skill-insertion decision.
```

- [ ] **Step 2: Verify the edit looks good**

Run:
```bash
grep -A 15 "Routing Signals" skills/unknowns-mapper/SKILL.md
```

Expected: Output shows the new section with the heuristic explanation.

- [ ] **Step 3: Commit**

```bash
git add skills/unknowns-mapper/SKILL.md
git commit -m "docs: document routing signals and heuristic in unknowns-mapper"
```

---

### Task 4: Create validate-unknowns-map.py validator

**Files:**
- Create: `scripts/validate-unknowns-map.py`
- Test: (manual validation after Task 5)

**Context:** We need a specialized validator to check that unknowns_map has valid routing fields. This is a Level 3 validator that runs after the generic validator.

- [ ] **Step 1: Create the validator script**

Create `scripts/validate-unknowns-map.py`:

```python
"""Specialized validator for unknowns_map routing fields.

Checks that the machine-readable YAML block contains required routing fields
with valid values.
"""

import os
import sys
import re
import yaml
import argparse

from _validator_utils import format_error

# Stable error codes
UNKNOWNS_MAP_FILE_NOT_FOUND = "UNKNOWNS_MAP_FILE_NOT_FOUND"
MISSING_ROUTING_BLOCK = "MISSING_ROUTING_BLOCK"
PARSING_ERROR = "PARSING_ERROR"
MISSING_ROUTING_FIELD = "MISSING_ROUTING_FIELD"
INVALID_CLARITY_VALUE = "INVALID_CLARITY_VALUE"
INVALID_UNKNOWNS_COUNT = "INVALID_UNKNOWNS_COUNT"
INVALID_ASSUMPTIONS_COUNT = "INVALID_ASSUMPTIONS_COUNT"
INVALID_RESEARCH_NEEDED = "INVALID_RESEARCH_NEEDED"


def validate_unknowns_map(artifact_path: str, repo_root: str = ".") -> list[str]:
    """Validate unknowns_map routing fields. Returns list of error messages."""
    errors: list[str] = []

    if not os.path.exists(artifact_path):
        errors.append(format_error(UNKNOWNS_MAP_FILE_NOT_FOUND, f"File not found: {artifact_path}"))
        return errors

    with open(artifact_path, encoding="utf-8") as f:
        content = f.read()

    # Extract the routing YAML block
    routing_match = re.search(
        r"## 7\. Machine-readable routing\s+```yaml\s+(.*?)\s+```",
        content,
        re.DOTALL | re.IGNORECASE,
    )

    if not routing_match:
        errors.append(
            format_error(MISSING_ROUTING_BLOCK, "Missing 'Machine-readable routing' YAML block in section 7.")
        )
        return errors

    try:
        routing_data = yaml.safe_load(routing_match.group(1))
        if not isinstance(routing_data, dict):
            errors.append(format_error(PARSING_ERROR, "Routing block must be a YAML mapping, not a list."))
            return errors

        # Check required fields
        required_fields = ["clarity_assessment", "unknowns_count", "assumptions_count", "research_needed"]
        for field in required_fields:
            if field not in routing_data:
                errors.append(format_error(MISSING_ROUTING_FIELD, f"Missing routing field: {field}"))

        # Validate clarity_assessment
        clarity = routing_data.get("clarity_assessment")
        if clarity and clarity not in ["high", "medium", "low"]:
            errors.append(
                format_error(
                    INVALID_CLARITY_VALUE,
                    f"clarity_assessment must be 'high', 'medium', or 'low', got: {clarity}",
                )
            )

        # Validate unknowns_count is an integer >= 0
        unknowns_count = routing_data.get("unknowns_count")
        if unknowns_count is not None:
            if not isinstance(unknowns_count, int) or unknowns_count < 0:
                errors.append(
                    format_error(INVALID_UNKNOWNS_COUNT, f"unknowns_count must be non-negative integer, got: {unknowns_count}")
                )

        # Validate assumptions_count is an integer >= 0
        assumptions_count = routing_data.get("assumptions_count")
        if assumptions_count is not None:
            if not isinstance(assumptions_count, int) or assumptions_count < 0:
                errors.append(
                    format_error(
                        INVALID_ASSUMPTIONS_COUNT,
                        f"assumptions_count must be non-negative integer, got: {assumptions_count}",
                    )
                )

        # Validate research_needed is boolean
        research_needed = routing_data.get("research_needed")
        if research_needed is not None:
            if not isinstance(research_needed, bool):
                errors.append(
                    format_error(INVALID_RESEARCH_NEEDED, f"research_needed must be boolean, got: {research_needed}")
                )

    except Exception as e:
        errors.append(format_error(PARSING_ERROR, f"Failed to parse routing YAML: {e}"))

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Specialized validator for unknowns_map routing fields.")
    parser.add_argument("artifact_path", nargs="?", help="Path to the unknowns_map .md file")
    parser.add_argument("--repo-root", default=".", help="Root of the repository for file checks")
    parser.add_argument("--list-codes", action="store_true", help="List all error codes and exit")
    args = parser.parse_args(argv)

    if args.list_codes:
        codes = [
            UNKNOWNS_MAP_FILE_NOT_FOUND,
            MISSING_ROUTING_BLOCK,
            PARSING_ERROR,
            MISSING_ROUTING_FIELD,
            INVALID_CLARITY_VALUE,
            INVALID_UNKNOWNS_COUNT,
            INVALID_ASSUMPTIONS_COUNT,
            INVALID_RESEARCH_NEEDED,
        ]
        for code in codes:
            print(code)
        return 0

    if not args.artifact_path:
        parser.print_help()
        return 1

    errors = validate_unknowns_map(args.artifact_path, args.repo_root)
    if errors:
        for error in errors:
            print(error)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Verify the script has valid syntax**

Run:
```bash
python scripts/validate-unknowns-map.py --list-codes
```

Expected: Output lists all error codes (UNKNOWNS_MAP_FILE_NOT_FOUND, MISSING_ROUTING_BLOCK, etc.).

- [ ] **Step 3: Commit**

```bash
git add scripts/validate-unknowns-map.py
git commit -m "feat: add specialized validator for unknowns_map routing fields"
```

---

### Task 5: Add conditional step schema example to workflow-registry.yaml

**Files:**
- Modify: `skills/workflow-orchestrator/references/workflow-registry.yaml`

**Context:** Update an existing workflow to show the conditional step syntax. We'll modify the `full-local-sensemaking` workflow to demonstrate conditional routing after unknowns-mapper.

- [ ] **Step 1: Update full-local-sensemaking workflow with conditional step**

Open `workflow-registry.yaml` and find the `full-local-sensemaking` workflow (around line 301). Replace steps 2-3 with conditional routing:

```yaml
  - id: full-local-sensemaking
    display_name: Full Local Sensemaking
    purpose: Convert raw fog into a repository diagnosis and downstream handoff using only local executable skills.
    initial_inputs:
      - id: raw_fog
        type: external_context
        required: true
        description: High-level project description, ambiguous ideas, or strategic goals.
      - id: repository_state
        type: external_context
        required: true
        description: Current repository files, registries, templates, validator scripts, and git state.
    allowed_execution_modes:
      - plan_only
      - prompt_chain
      - guided_execution
      - autonomous_execution
      - yolo_execution
    requires_clean_worktree: true
    requires_run_log: true
    branch_policy:
      required: true
      pattern: "yolo/{workflow_id}/{timestamp}"
    steps:
      - id: 1
        skill: problem-framer
        step_type: local_execution
        gate: review_problem_frame
        input_source: raw_fog
        output_artifact: problem_frame
      - id: 2
        skill: unknowns-mapper
        step_type: local_execution
        gate: review_unknowns_map
        input_artifact: problem_frame
        output_artifact: unknowns_map
      - id: 3-conditional
        skill: ~  # Will be determined at runtime
        conditional: true
        decision_field: unknowns_map.research_needed
        if_true:
          skill: discovery
          step_type: external_routing
          gate: review_discovery
          input_artifact: unknowns_map
          output_artifact: discovery_findings
          next_step: 4
        if_false:
          next_step: 4
        condition_rule: "If unknowns_map.research_needed == true, insert discovery; else skip to repo-sensemaker"
      - id: 4
        skill: repo-sensemaker
        step_type: local_execution
        gate: review_sensemaking_brief
        input_artifact: unknowns_map
        input_source: repository_state
        output_artifact: repository_sensemaking_brief
      - id: 5
        skill: handoff
        step_type: local_execution
        gate: review_final_prompt
        input_artifact: repository_sensemaking_brief
        output_artifact: prompt_handoff
```

Key changes:
- Step 3 is now a conditional step with `conditional: true`
- `decision_field` points to `unknowns_map.research_needed`
- `if_true` branch: runs discovery, outputs discovery_findings, then goes to step 4
- `if_false` branch: skips to step 4
- Step 4 (repo-sensemaker) now starts after the conditional logic resolves

- [ ] **Step 2: Verify the YAML is valid**

Run:
```bash
python -c "import yaml; yaml.safe_load(open('skills/workflow-orchestrator/references/workflow-registry.yaml'))" && echo "YAML is valid"
```

Expected: "YAML is valid" printed.

- [ ] **Step 3: Verify the conditional step structure**

Run:
```bash
python -c "
import yaml
data = yaml.safe_load(open('skills/workflow-orchestrator/references/workflow-registry.yaml'))
workflow = next(w for w in data['workflows'] if w['id'] == 'full-local-sensemaking')
conditional_step = next(s for s in workflow['steps'] if s.get('conditional'))
print(f\"Conditional step found: {conditional_step.get('id')}\")
print(f\"Decision field: {conditional_step.get('decision_field')}\")
print(f\"If true skill: {conditional_step['if_true'].get('skill')}\")
"
```

Expected: Output shows "Conditional step found: 3-conditional", decision_field, and skill name.

- [ ] **Step 4: Commit**

```bash
git add skills/workflow-orchestrator/references/workflow-registry.yaml
git commit -m "feat: add conditional step schema to workflow-registry (full-local-sensemaking example)"
```

---

### Task 6: Extend validate-plan.py to validate conditional steps

**Files:**
- Modify: `scripts/validate-plan.py`

**Context:** The plan validator needs to check that conditional steps reference valid skills and have correct structure.

- [ ] **Step 1: Read validate-plan.py to understand current structure**

Run:
```bash
head -50 scripts/validate-plan.py
```

Note: We'll add conditional step validation to the existing validator.

- [ ] **Step 2: Add conditional step validation function**

Open `scripts/validate-plan.py` and add this function after the imports:

```python
def _validate_conditional_step(step: dict, workflow_id: str, repo_root: str) -> list[str]:
    """Validate a conditional skill step. Returns list of error messages."""
    errors: list[str] = []
    
    if not step.get("conditional"):
        return errors
    
    # Load skill registry
    skill_registry = load_skill_registry(repo_root)
    if not skill_registry:
        errors.append(format_error("SKILL_REGISTRY_NOT_FOUND", "skill-registry.yaml not found"))
        return errors
    
    valid_skill_ids = {s.get("id") for eco in skill_registry.get("ecosystems", {}).values() 
                       for s in eco.get("skills", [])}
    
    # Check decision_field exists
    decision_field = step.get("decision_field")
    if not decision_field:
        errors.append(format_error("MISSING_DECISION_FIELD", 
                                   f"Step {step.get('id')}: conditional step missing 'decision_field'"))
    
    # Check if_true branch
    if_true = step.get("if_true", {})
    if_true_skill = if_true.get("skill")
    if if_true_skill and if_true_skill not in valid_skill_ids:
        errors.append(format_error("HALLUCINATED_SKILL", 
                                   f"Step {step.get('id')}: if_true skill '{if_true_skill}' not found in skill registry"))
    
    # Check if_false branch (if it has a skill, not just next_step)
    if_false = step.get("if_false", {})
    if_false_skill = if_false.get("skill")
    if if_false_skill and if_false_skill not in valid_skill_ids:
        errors.append(format_error("HALLUCINATED_SKILL",
                                   f"Step {step.get('id')}: if_false skill '{if_false_skill}' not found in skill registry"))
    
    # Check that either if_true or if_false has a next_step or skill
    if_true_has_path = if_true.get("next_step") or if_true.get("skill")
    if_false_has_path = if_false.get("next_step") or if_false.get("skill")
    
    if not if_true_has_path:
        errors.append(format_error("INVALID_CONDITIONAL_BRANCH",
                                   f"Step {step.get('id')}: if_true branch must have 'skill' or 'next_step'"))
    
    if not if_false_has_path:
        errors.append(format_error("INVALID_CONDITIONAL_BRANCH",
                                   f"Step {step.get('id')}: if_false branch must have 'skill' or 'next_step'"))
    
    return errors
```

- [ ] **Step 2: Update step validation loop to call conditional step validator**

Find the loop that validates workflow steps in `validate_plan.py` (around line ~100-150, depends on file). Update it to call the new function:

```python
# In the steps validation loop:
for step in workflow.get("steps", []):
    if step.get("conditional"):
        errors.extend(_validate_conditional_step(step, workflow_id, repo_root))
    else:
        # Existing validation for non-conditional steps
        ...
```

- [ ] **Step 3: Test the validator on the updated workflow**

Run:
```bash
python scripts/validate-plan.py full-local-sensemaking --repo-root .
```

Expected: Validator runs without errors (or shows expected validation failures if any).

- [ ] **Step 4: Commit**

```bash
git add scripts/validate-plan.py
git commit -m "feat: add conditional step validation to validate-plan.py"
```

---

### Task 7: Update CONTEXT.md with implementation details

**Files:**
- Modify: `CONTEXT.md`

**Context:** Document the implementation so future readers understand how dynamic chaining works.

- [ ] **Step 1: Add implementation section to CONTEXT.md**

Find the "## Automation & Validation (scripts/)" section and add after it:

```markdown
## Dynamic Chaining Implementation

**Overview:** Workflows support conditional routing of Skill Steps based on artifact signals. The primary decision point is the clarity of the initial raw_fog input, detected by unknowns-mapper and encoded in the unknowns_map routing fields.

**Routing Signal:** unknowns_map.research_needed (boolean)
- Determined by: `(unknowns_count >= 5) OR (clarity_assessment == "low")`
- If true: A discovery or research skill is inserted into the workflow
- If false: The workflow skips to repo-sensemaker

**Provisional Heuristic:** The thresholds (5 unknowns, "low" clarity) are initial estimates. They are validated empirically in early value-production runs, then refined using repeatable failure analysis.

**Conditional Step Schema:** Workflows can define conditional steps with if_true/if_false branches:
```yaml
- id: 3-conditional
  conditional: true
  decision_field: unknowns_map.research_needed
  if_true:
    skill: discovery
    gate: review_discovery
    input_artifact: unknowns_map
    output_artifact: discovery_findings
    next_step: 4
  if_false:
    next_step: 4
```

**Machine Fields on unknowns_map:**
- clarity_assessment: "high" | "medium" | "low"
- unknowns_count: integer (count of unknowns)
- assumptions_count: integer (count of unvalidated assumptions)
- research_needed: boolean (routing decision)

**Validators:**
- `validate-unknowns-map.py` — Validates unknowns_map routing fields are present and well-typed
- `validate-plan.py` — Validates conditional step logic references real skills
```

- [ ] **Step 2: Verify the edit**

Run:
```bash
grep -A 5 "Dynamic Chaining Implementation" CONTEXT.md
```

Expected: Output shows the new section.

- [ ] **Step 3: Commit**

```bash
git add CONTEXT.md
git commit -m "docs: document dynamic chaining implementation in CONTEXT.md"
```

---

### Task 8: Create test fixtures for conditional workflows

**Files:**
- Create: `examples/skill-tests/unknowns-map-routing/`
- Create: `examples/skill-tests/unknowns-map-routing/valid-research-needed-true.md`
- Create: `examples/skill-tests/unknowns-map-routing/valid-research-needed-false.md`
- Create: `examples/skill-tests/unknowns-map-routing/invalid-missing-research-needed.md`

**Context:** We need test fixtures to prove the validator works. These will be used by the validator verification suite.

- [ ] **Step 1: Create test directory**

Run:
```bash
mkdir -p examples/skill-tests/unknowns-map-routing
```

- [ ] **Step 2: Create valid fixture (research_needed=true)**

Create `examples/skill-tests/unknowns-map-routing/valid-research-needed-true.md`:

```markdown
# Unknowns Map

## 1. Knowns
- User wants to build a payment system
- System must support recurring billing

## 2. Unknowns
- Payment gateway selection (Stripe? PayPal?)
- Compliance requirements by region
- Fraud detection approach
- Refund workflow design
- Tax calculation rules

## 3. Assumptions
- We'll use a third-party gateway (not build in-house)
- PCI compliance is required
- Users are in US and EU only

## 4. Risks
- If we choose the wrong gateway, migration is expensive
- If we miss compliance, we face regulatory penalties
- If fraud detection is weak, chargebacks will be high

## 5. Research Paths
- Research Stripe vs PayPal vs Square: feature matrix, pricing, compliance support
- Investigate PCI DSS requirements for our architecture
- Interview 3 existing payment system maintainers about fraud lessons learned
- Document refund policy requirements from legal

## 6. Stopping Rule
Stop when we have: (1) identified 2-3 viable gateways with cost/feature comparison, (2) confirmed PCI compliance path with legal, (3) documented refund workflow from legal review.

## 7. Machine-readable routing

```yaml
clarity_assessment: "low"
unknowns_count: 5
assumptions_count: 3
research_needed: true
```
```

- [ ] **Step 3: Create valid fixture (research_needed=false)**

Create `examples/skill-tests/unknowns-map-routing/valid-research-needed-false.md`:

```markdown
# Unknowns Map

## 1. Knowns
- We're adding a dark mode toggle to the UI
- Dark mode must support all existing pages
- CSS variables are already set up for theming

## 2. Unknowns
- Exact toggle placement in navbar
- Animation duration preference

## 3. Assumptions
- Users will prefer a toggle in the top-right
- Animation should be 200ms

## 4. Risks
- If animation is too slow, perceived performance suffers

## 5. Research Paths
- Check competitor dark mode implementations (3 examples)
- Test animation timing with 3 users

## 6. Stopping Rule
Stop when we have tested animation timing and confirmed toggle placement with 3 users.

## 7. Machine-readable routing

```yaml
clarity_assessment: "high"
unknowns_count: 2
assumptions_count: 2
research_needed: false
```
```

- [ ] **Step 4: Create invalid fixture (missing research_needed)**

Create `examples/skill-tests/unknowns-map-routing/invalid-missing-research-needed.md`:

```markdown
# Unknowns Map

## 1. Knowns
- We're refactoring the API

## 2. Unknowns
- Which endpoints need versioning

## 3. Assumptions
- None

## 4. Risks
- Breaking changes could affect clients

## 5. Research Paths
- Audit client usage of each endpoint

## 6. Stopping Rule
Stop when we've audited all endpoints.

## 7. Machine-readable routing

```yaml
clarity_assessment: "medium"
unknowns_count: 1
assumptions_count: 0
```
```

(Missing `research_needed` field — validator should catch this)

- [ ] **Step 5: Run validator on all three fixtures**

Run:
```bash
python scripts/validate-unknowns-map.py examples/skill-tests/unknowns-map-routing/valid-research-needed-true.md
echo "Expected: exit code 0"
echo ""
python scripts/validate-unknowns-map.py examples/skill-tests/unknowns-map-routing/valid-research-needed-false.md
echo "Expected: exit code 0"
echo ""
python scripts/validate-unknowns-map.py examples/skill-tests/unknowns-map-routing/invalid-missing-research-needed.md
echo "Expected: exit code 1 with MISSING_ROUTING_FIELD error"
```

Expected: First two pass (exit 0), third fails (exit 1) with MISSING_ROUTING_FIELD error.

- [ ] **Step 6: Commit**

```bash
git add examples/skill-tests/unknowns-map-routing/
git commit -m "test: add fixtures for unknowns-map routing field validation"
```

---

### Task 9: Validate that existing workflows still pass validation

**Files:**
- No changes (verification only)

**Context:** Ensure we didn't break existing workflows with our validator changes.

- [ ] **Step 1: Run validate-repo.py to check all workflows**

Run:
```bash
python scripts/validate-repo.py
```

Expected: No errors about workflows (may have other unrelated errors, but no workflow validation failures).

- [ ] **Step 2: Verify all workflows in registry are still valid**

Run:
```bash
python -c "
import yaml
data = yaml.safe_load(open('skills/workflow-orchestrator/references/workflow-registry.yaml'))
print(f\"Total workflows: {len(data.get('workflows', []))}\")
for workflow in data['workflows']:
    print(f\"  - {workflow.get('id')}\")
"
```

Expected: Lists all workflows without errors.

- [ ] **Step 3: If any workflows fail validation, fix them**

(This is unlikely; the conditional step is only in the example we added. But if it happens, update the workflow YAML.)

---

## Self-Review

**Spec coverage:**
- ✅ Workflows support conditional Skill Steps based on artifact signals
- ✅ Primary decision point: unknowns_map.research_needed (clarity and unknowns count)
- ✅ Provisional heuristic: (unknowns_count >= 5) OR (clarity_assessment == "low")
- ✅ Routing logic in workflow definition (Task 5)
- ✅ Artifact contracts updated (Task 1)
- ✅ Validators created (Task 4, Task 6)
- ✅ Documentation updated (Task 3, Task 7)
- ✅ Test fixtures created (Task 8)
- ✅ Existing workflows validated (Task 9)

**Placeholder scan:** No "TBD", "TODO", "fill in details", etc. All code is complete.

**Type consistency:** 
- clarity_assessment values: "high", "medium", "low" (consistent across template, validator, docs)
- unknowns_count, assumptions_count: integers >= 0 (consistent)
- research_needed: boolean (consistent)
- Conditional step schema uses if_true/if_false with skill/next_step fields (consistent)

**Gap check:** No gaps identified. All requirements from the docs-aligner session are covered.

---

## Execution

Plan complete and saved to `docs/superpowers/plans/2026-05-17-dynamic-chaining.md`.

**Two execution options:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — Execute tasks in this session using superpowers:executing-plans, batch execution with checkpoints

Which approach would you prefer?

