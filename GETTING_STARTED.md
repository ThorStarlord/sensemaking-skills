# Getting Started: Running Sensemaking Skills

A quick guide to using the sensemaking system. Choose your path based on your needs: **manual path** for control, or **automation path** for speed.

---

## Installation (One-Time Setup)

```bash
# 1. Clone the repository
git clone https://github.com/your-org/sensemaking-skills.git
cd sensemaking-skills

# 2. Install dependencies
python -m pip install -r requirements.txt

# 3. Verify installation
python scripts/workflow-runtime.py --list-workflows
```

---

## Two Paths: Manual vs Automation

### 🎮 Manual Path: Full Control

**When to use**: You want to inspect artifacts between stages, make explicit decisions about routing, or debug workflows.

**How it works**:
1. User explicitly runs a workflow
2. Reviews output and chooses next step
3. User manually invokes next workflow
4. Repeat as needed

**Example: Fast Path + Product Implementation**

```bash
# Step 1: Run diagnostic workflow
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode guided_execution

# Output will show:
# - Repository analysis (fog_type: product_fog)
# - Recommended workflow: product-implementation-workflow
# - User must read and approve at gates

# Step 2: User reads brief and manually invokes next workflow
python scripts/workflow-runtime.py --workflow product-implementation-workflow --mode guided_execution

# Step 3: Implementation workflow runs
# - docs-aligner → discovery → opportunity-tree → to-prd → to-issues → triage → tdd
# - Final output: PRD, issues, code patches
```

**Available Workflows for Manual Invocation**:

```
Diagnostic Workflows:
  - fast-path-workflow          Fast analysis + routing (1-2 min)
  - full-fog-workflow           Comprehensive analysis (5-10 min)
  - fast-local-diagnostic       Quick repository audit (1 min)
  - full-local-sensemaking      Deep local analysis (5 min)

Implementation Workflows:
  - product-implementation-workflow    Product requirements workflow
  - ui-implementation-workflow         UI/UX specification workflow
  - docs-implementation-workflow       Documentation workflow
  - implementation-workflow            Architecture/code workflow

Strategy Workflows:
  - product-discovery-sprint     User research → opportunities
  - product-strategy-sprint      Lean canvas → roadmap
  - product-autonomous-sprint    Full product workflow (autonomous)

Specialized Workflows:
  - docs-contract-reconciliation Align docs with code
  - autonomous-sprint-preflight  Prepare for autonomous agents
  - skill-maintenance-loop       Improve a skill
```

**List all workflows**:
```bash
python scripts/workflow-runtime.py --list-workflows
```

---

### ⚡ Automation Path: Full Speed

**When to use**: You want end-to-end automation, are in production, or want the fastest path from problem → solution.

**How it works**:
1. User runs diagnostic workflow once
2. System automatically detects `auto_invoke_next_workflow` flag
3. System reads `recommended_workflow_id` from artifact
4. System automatically invokes implementation workflow (no user action)
5. Complete output returned (problem → plan → PRD → issues → code)

**Example: Single Command, Full Automation**

```bash
# Single invocation: entire pipeline runs automatically
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode autonomous_execution

# System automatically:
# Stage 1: repo-sensemaker analyzes repository
# Stage 2: workflow-planner determines recommended_workflow_id (product-implementation-workflow)
# Stage 3: AUTO-INVOKES product-implementation-workflow with same mode
# Stage 4: Implementation workflow executes with auto-approval at gates
# Returns: Final artifacts (brief, plan, PRD, issues, code patches)
```

**Or use the default diagnostic workflow** (recommended entry point):

```bash
# Default workflow auto-routes to implementation based on fog_type
python scripts/workflow-runtime.py --mode autonomous_execution

# Same as above - analyzes repository and automatically invokes appropriate
# implementation workflow (product/ui/docs/architecture) based on detected fog type
# Workflow defaults to full-local-sensemaking if not specified
```

---

## Execution Modes

Control user approval and automation with execution modes:

| Mode | Gates | Speed | User Control | Use Case |
|------|-------|-------|--------------|----------|
| **guided_execution** | Pause at every gate (user approves each step) | Slowest | Full control | Development, exploration, learning |
| **autonomous_execution** | Auto-approve if validation passes | Fast | Medium (rules-based) | Known workflows, production with guardrails |
| **prompt_chain** | Generate full prompt chain for manual execution | Fast | None (planning only) | Multi-step planning, orchestration setup |
| **plan_only** | No execution, just show plan | Instant | Planning only | Validation, seeing what would happen |
| **yolo_execution** | Bypass approval gates; validators still enforce artifact validity | Fastest | None (validation-based) | Experimental, trusted contexts only |

### Example: Same Workflow, Different Modes

```bash
# Mode 1: Guided - Pause at each step for user approval
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode guided_execution
# -> Pauses after repo-sensemaker for user to review
# -> Pauses after workflow-planner for user to approve routing
# -> User must then manually invoke implementation workflow

# Mode 2: Autonomous - Auto-approve and auto-chain
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode autonomous_execution
# -> No pauses; automatically chains to implementation workflow
# -> Returns complete solution (PRD, issues, code)

# Mode 3: Prompt Chain - Generate full prompt chain
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode prompt_chain
# -> Generates prompts for manual execution of each step
# -> No actual skill execution; good for understanding workflow

# Mode 4: Plan Only - Just show the plan, don't execute
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode plan_only
# -> Shows what WOULD happen, no actual skill execution
# -> Fast validation before committing

# Mode 5: YOLO - Maximum speed with gates bypassed
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode yolo_execution
# -> Bypasses approval gates; validators still enforce artifact validity
# -> Use only in trusted, experimental contexts
```

---

## Real-World Examples

### Scenario 1: Product Team Building New Feature (Manual Path)

```bash
# Step 1: Understand the problem
python scripts/workflow-runtime.py --workflow full-fog-workflow --mode guided_execution
# Pauses: "Approve problem frame? [Y/n]"
# Pauses: "Approve unknowns map? [Y/n]"
# Pauses: "Approve repository brief? [Y/n]"
# Pauses: "Approve workflow plan? [Y/n]"
# User reads brief, sees: "product_fog detected - recommend product-implementation-workflow"

# Step 2: User decides to proceed with product workflow
python scripts/workflow-runtime.py --workflow product-implementation-workflow --mode guided_execution
# Executes: docs-aligner → discovery → opportunity-tree → to-prd → to-issues → triage → tdd
# Pauses at each gate for user to review output and approve next step
```

### Scenario 2: CI/CD Pipeline (Automation Path)

```bash
# In GitHub Actions or Jenkins:
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode autonomous_execution
# - Analyzes repository
# - Automatically routes to appropriate implementation workflow
# - Returns PRD + issues + code patches
# - All without human intervention
```

### Scenario 3: Quick Diagnostic for Multiple Projects (Automation Path)

```bash
# Check 5 projects quickly
for project in project-a project-b project-c project-d project-e; do
  cd $project
  python ../scripts/workflow-runtime.py fast-local-diagnostic --mode autonomous_execution
  echo "--- Completed: $project ---"
done
```

### Scenario 4: Debug a Specific Skill (Manual Path)

```bash
# Run fast-path to understand repository
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode guided_execution

# Then manually invoke workflow-planner to debug routing
python scripts/workflow-runtime.py --workflow full-fog-workflow --mode plan_only
# Shows plan without execution, so you can validate logic
```

---

## Command Reference

### Basic Commands

```bash
# List all available workflows
python scripts/workflow-runtime.py --list-workflows

# Run a workflow (with optional problem statement)
python scripts/workflow-runtime.py --workflow <workflow-id>

# Run with explicit mode
python scripts/workflow-runtime.py --workflow <workflow-id> --mode <mode>

# Run with problem statement and custom mode
python scripts/workflow-runtime.py "Your problem here" --workflow <workflow-id> --mode <mode>

# Run with custom repo root
python scripts/workflow-runtime.py --workflow <workflow-id> --repo-root /path/to/repo
```

### Execution Mode Flags

```bash
# Guided mode (user approves each gate)
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode guided_execution

# Autonomous mode (auto-approve valid gates, auto-chain)
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode autonomous_execution

# Prompt chain mode (generate prompts for manual execution)
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode prompt_chain

# Plan only (show plan, don't execute)
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode plan_only

# YOLO mode (bypass gates, full automation, experimental only)
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode yolo_execution
```

---

## How Phase 3 Hardening Makes Automation Safe

**Phase 3 completed in this session** adds validation layer that guarantees automation won't fail silently.

**Before Phase 3** (risky):
- ❌ `recommended_workflow_id` could be invalid
- ❌ Auto-invocation could crash
- ❌ Routing field values weren't validated

**After Phase 3** (safe):
- ✅ All enum fields validated at artifact creation time
- ✅ `recommended_workflow_id` guaranteed to be valid workflow
- ✅ `primary_fog_type` guaranteed to be canonical form
- ✅ `routing_decision_method` matches audit-trail values
- ✅ All gates exist in canonical vocabulary
- ✅ Auto-invocation guaranteed to succeed

**What this means for automation path**: You can confidently use `--mode autonomous_execution` knowing the system will validate every field before auto-chaining to the next workflow. No silent failures.

See [docs/HARDENING_STATUS.md](docs/HARDENING_STATUS.md) for details.

---

## Output Location

All artifacts are saved to:
```
artifacts/
├── NN-project-name/           Run folder with numbered artifacts
│   ├── 01-user-intent.md      User's original problem statement
│   ├── 02-problem-frame.md    Structured problem (full-fog only)
│   ├── 03-unknowns-map.md     Unknowns and research paths (full-fog only)
│   ├── 04-brief.md            Repository sensemaking brief
│   ├── 05-plan.md             Workflow orchestration plan
│   ├── 06-prd.md              Product requirements document
│   ├── 07-issues.md           Implementation issues
│   ├── 08-code.md             Code patches
│   └── run_log.md             Execution log (all decisions, gates)
└── run_log_<timestamp>.md     Historical execution records
```

---

## Troubleshooting

### "Artifact not found" Error
- **Cause**: Skill execution failed
- **Fix**: Check previous artifact for error messages; run in `--mode plan_only` to debug

### "Unknown fog type" Error
- **Cause**: validate-artifact.py rejected non-canonical fog type (Phase 3)
- **Fix**: Use canonical forms (product_fog, ui_fog, architecture_fog, docs_fog, integration_fog)

### Auto-invocation Didn't Trigger
- **Cause**: Workflow doesn't have `auto_invoke_next_workflow: true` in registry
- **Fix**: Use `--mode autonomous_execution` to enable auto-approval, or manually invoke next workflow

### Gate Approval Stuck
- **Cause**: Waiting for user input in guided_execution mode
- **Fix**: Type `y` + Enter to approve, or `n` to deny and stop

### Slow Execution
- **Cause**: Running in guided_execution mode (waiting for user at each step)
- **Fix**: Use `--mode autonomous_execution` for faster execution

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for more issues.

---

## Next Steps

### For Learning
1. Run `fast-path-workflow --mode plan_only` to see what would happen
2. Run `fast-path-workflow --mode guided_execution` to execute with control
3. Read the brief output to understand fog_type classification
4. Review [docs/CONTEXT.md](docs/CONTEXT.md) for design principles

### For Production
1. Run `fast-path-workflow --mode autonomous_execution` for full automation
2. Monitor artifacts in `artifacts/` folder
3. Configure CI/CD to run workflows on schedule
4. See [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)

### For Customization
1. Add new workflows to [skills/workflow-planner/references/workflow-registry.yaml](skills/workflow-planner/references/workflow-registry.yaml)
2. Define new artifact contracts in [skills/workflow-planner/references/artifact-contracts.yaml](skills/workflow-planner/references/artifact-contracts.yaml)
3. See [docs/workflow-design-guide.md](docs/workflow-design-guide.md)

---

## Key Concepts Quick Reference

| Term | Meaning |
|------|---------|
| **Fog** | Uncertainty about the problem (product/UI/docs/architecture) |
| **Fog Type** | Category of uncertainty (product_fog, ui_fog, etc.) |
| **Workflow** | Ordered sequence of skills that processes fog into artifacts |
| **Skill** | Individual agent that produces one artifact |
| **Gate** | User approval point (pause in guided_execution) |
| **Artifact** | Durable output document (brief, PRD, issues, code) |
| **Auto-Invocation** | Automatic chaining to next workflow (autonomous_execution) |
| **Execution Mode** | How the workflow runs (guided/autonomous/plan/yolo) |

---

## More Documentation

- **[CONTEXT.md](CONTEXT.md)** — Engineering principles and design decisions
- **[docs/orchestration-patterns.md](docs/orchestration-patterns.md)** — Workflow composition patterns
- **[docs/workflow-design-guide.md](docs/workflow-design-guide.md)** — How to design new workflows
- **[docs/HARDENING_STATUS.md](docs/HARDENING_STATUS.md)** — Contract/naming drift prevention (Phase 3)
- **[docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)** — Production deployment
- **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** — Common issues and solutions

---

## Questions?

For detailed information:
- **Workflow reference**: See [skills/workflow-planner/references/workflow-registry.yaml](skills/workflow-planner/references/workflow-registry.yaml)
- **Artifact contracts**: See [skills/workflow-planner/references/artifact-contracts.yaml](skills/workflow-planner/references/artifact-contracts.yaml)
- **Canonical vocabulary**: See [docs/canonical-vocabulary.yaml](docs/canonical-vocabulary.yaml)
- **Design philosophy**: See [docs/philosophy/ARTIFACT_DRIVEN_AGENTIC_ENGINEERING.md](docs/philosophy/ARTIFACT_DRIVEN_AGENTIC_ENGINEERING.md)
