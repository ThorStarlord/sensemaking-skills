# Getting Started with Sensemaking Skills

This guide shows how to use the system. There are two paths: agent-native (recommended for diagnostics) and CLI utilities.

---

## Prerequisites

- Python 3.11+
- Claude Code (for agent-native skill invocation), OR
- sensemaking-skills CLI (for validation and utilities)

---

## Quick Start (5 minutes)

### Via Claude Code or Agent (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ThorStarlord/sensemaking-skills.git
   cd sensemaking-skills
   ```

2. **Open the repository in Claude Code or your agent environment.**

3. **Ask the agent to read the bootstrap skill:**
   ```
   Read the file `skills/using-sensemaking/SKILL.md` and follow its instructions.
   ```

4. **Ask the agent to run the diagnostic:**
   ```
   Use `skills/repo-sensemaker/SKILL.md` to analyze my repository at `/path/to/my/repo`.
   Produce a `repository_sensemaking_brief` artifact and save it to `artifacts/`.
   Then validate it by running `python scripts/validate-and-report.py artifacts/repository_sensemaking_brief.md`.
   ```

5. **Ask the agent to create the workflow plan:**
   ```
   Use `skills/workflow-planner/SKILL.md` to convert the brief into a `workflow_orchestration_plan`.
   Validate it by running `python scripts/validate-and-report.py artifacts/workflow_orchestration_plan.md`.
   ```

#### Optional: Install Skills into Claude Code

If your Claude Code environment supports local skill installation:

```bash
mkdir -p ~/.claude/skills
cp -R skills/* ~/.claude/skills/
```

Restart Claude Code. If skill invocation works in your environment, you may be able to use:

```
/skill repo-sensemaker
/skill workflow-planner
```

**If those commands don't work**, use the method above: ask the agent to read the SKILL.md files directly. Both methods work equally well.

---

### Via CLI (New in 0.2.1)

If you've installed sensemaking-skills via `pip install -e .`:

```bash
# Prepare a repository for diagnosis
sensemaking-skills analyze --repo /path/to/your/repo

# Then open the repository in Claude Code and follow the agent-native path above

# After the agent creates artifacts, validate them:
sensemaking-skills validate --artifact artifacts/repository_sensemaking_brief.md

# Run the test suite:
sensemaking-skills test
```

**Note:** The CLI provides utilities for setup and validation. The actual diagnosis requires Claude Code and the agent-native skills.

### Validate Artifacts with Python Scripts

You can also validate directly without the CLI:

**Validate a brief:**
```bash
python scripts/validate-and-report.py artifacts/repository_sensemaking_brief.md
```

**Validate a plan:**
```bash
python scripts/validate-and-report.py artifacts/workflow_orchestration_plan.md
```

**Run tests:**
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

