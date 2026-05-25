# Getting Started with Sensemaking Skills

This guide shows how to actually use the system in its current state (agent/Claude Code invocation).

---

## Prerequisites

- Python 3.11+
- Claude Code (for skill invocation), OR
- Command-line access to Python scripts

---

## Quick Start (5 minutes)

### Via Claude Code (Recommended)

1. **Clone and set up:**
   ```bash
   git clone https://github.com/ThorStarlord/sensemaking-skills.git
   cd sensemaking-skills
   # Copy skills to Claude Code
   cp -r skills/* ~/.claude/skills/
   ```

2. **In Claude Code, invoke the diagnostic skill:**
   ```
   /skill repo-sensemaker --repo /path/to/your/repository
   ```

3. **The skill will:**
   - Analyze your repository structure
   - Identify the "weakest boundary" (architecture/product/UI/docs issue)
   - Produce a 14-section diagnostic brief
   - Recommend implementation workflows

4. **Next, invoke workflow planning:**
   ```
   /skill workflow-planner
   ```

5. **Review the orchestration plan** that specifies:
   - Which workflow to run
   - What skills to invoke in sequence
   - What approval gates are needed

---

### Via Python Scripts (Direct)

**Validate a repository brief artifact:**
```bash
python scripts/validate-brief.py artifacts/repository_sensemaking_brief.md --json
```

**Validate a workflow plan artifact:**
```bash
python scripts/validate-plan.py artifacts/workflow_orchestration_plan.md --json
```

**Run the test suite (10 real repositories):**
```bash
python scripts/shadow-mode-runner.py
```

---

## Real-World Example

### Scenario: Analyze a New Repository

**Your problem:** You inherited a complex monorepo. You don't know where to start.

**Step 1: Run diagnostic**
```
/skill repo-sensemaker --repo /path/to/your/monorepo
```

**Output:** A brief that says:
```
Fog Type: ARCHITECTURE_FOG
Weakest Boundary: Tight coupling between services
Recommended Workflow: architecture-implementation-workflow
Evidence:
  - File: src/services/auth/user.py (imports 8 other services)
  - File: src/services/api/routes.py (orchestrates 5 services)
  - Pattern: Circular dependencies detected
```

**Step 2: Route to implementation workflow**
```
/skill workflow-planner
```

**Output:** An orchestration plan that says:
```
Selected Workflow: architecture-implementation-workflow
Workflow Steps:
  1. docs-aligner → Review domain docs
  2. to-prd → Create architecture PRD
  3. to-issues → Break into refactoring issues
  4. triage → Assign to sprint
  5. tdd → Implement with tests
```

**Step 3: Execute the workflow**
Follow the prompt instructions to invoke each skill in sequence.

---

## Understanding the Artifacts

### Repository Sensemaking Brief

14-section diagnostic artifact that includes:
1. Repository name and summary
2. Fog type classification (ui_fog, product_fog, docs_fog, architecture_fog)
3. Evidence citations (specific files and line numbers)
4. Weakest boundary (most critical issue)
5. Candidate workflows with justification
6. Risk assessment
7. Recommended next steps

**Example brief location:**
```
artifacts/repository_sensemaking_brief.md
```

### Workflow Orchestration Plan

10-section plan that specifies:
1. Which workflow to execute
2. Skill sequence and order
3. Input/output artifacts for each step
4. Approval gates (pause points)
5. Success criteria
6. Estimated time
7. Rollback procedure
8. Machine-readable YAML block

**Example plan location:**
```
artifacts/workflow_orchestration_plan.md
```

---

## Validation & Error Recovery

### Validating Artifacts

All artifacts are validated against contracts to ensure quality:

```bash
# Validate a brief
python scripts/validate-brief.py artifacts/repository_sensemaking_brief.md

# Validate a plan
python scripts/validate-plan.py artifacts/workflow_orchestration_plan.md

# Both together
python scripts/validate-and-report.py artifacts/
```

### Error Messages

If validation fails, you get:
```json
{
  "valid": false,
  "artifact_id": "repository_sensemaking_brief",
  "errors": [
    {
      "error_id": "repository_sensemaking_brief.fog_type.missing_field",
      "error_type": "missing_field",
      "field": "fog_type",
      "message": "Required field 'fog_type' is missing",
      "suggested_fixes": [
        "Add fog_type with one of: ui_fog, product_fog, docs_fog, architecture_fog"
      ]
    }
  ]
}
```

### Bounded Retry Logic

If an artifact fails validation:
1. System suggests a fix
2. You implement the fix
3. System revalidates (up to 3 attempts)
4. If still failing after 3 attempts, gracefully escalates with clear error message

This prevents infinite loops while giving the system a chance to self-correct.

---

## Common Workflows

### Workflow 1: Quick Diagnosis
```
repo-sensemaker → (Read brief) → workflow-planner → (Review plan)
Time: ~5 minutes
Output: Diagnosis and recommended next steps
```

### Workflow 2: Full Analysis
```
problem-framer → unknowns-mapper → repo-sensemaker → workflow-planner
Time: ~20 minutes
Output: Problem frame, unknowns map, diagnosis, plan
```

### Workflow 3: Implementation
```
docs-aligner → to-prd → to-issues → triage → tdd → (Your code)
Time: Days/weeks depending on scope
Output: Implemented feature with tests
```

---

## Troubleshooting

### "Skill not found"
**Solution:** Make sure you copied skills to `~/.claude/skills/`
```bash
cp -r skills/* ~/.claude/skills/
```

### "Validation failed with missing fields"
**Solution:** Check the error message for the exact field. The artifact contract defines what's required.

### "No repositories found"
**Solution:** Make sure `--repo` path exists and is readable:
```bash
ls -la /path/to/your/repo
```

### "Timeout (script took >30s)"
**Solution:** This is expected for large repos. The system respects a 30-second timeout to prevent hanging. Smaller repos run faster (~0.1-0.2s).

---

## Next Steps

1. **Try it on your repo:**
   ```
   /skill repo-sensemaker --repo /path/to/your/project
   ```

2. **Read the diagnostic brief** — this is the main output

3. **Follow the recommended workflow** from the orchestration plan

4. **For implementation:** Use the `tdd` skill to build features test-first

---

## More Information

- **[README.md](README.md)** — Project overview
- **[INSTALLATION.md](INSTALLATION.md)** — Detailed setup
- **[CONTEXT.md](CONTEXT.md)** — Architecture and philosophy
- **[API.md](API.md)** — Python API for direct integration

