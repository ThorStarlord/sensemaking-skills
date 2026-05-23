# Installation Guide

Get up and running with sensemaking-skills in minutes. Choose your installation path and follow the quickstart to analyze your repository.

---

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install sensemaking-skills
```

Verify installation:
```bash
sensemaking-skills --help
```

### Option 2: Install from GitHub

Clone the repository and install in development mode:

```bash
git clone https://github.com/dimmi-andreus/sensemaking-skills.git
cd sensemaking-skills
pip install -e .
```

For development (includes testing tools):
```bash
pip install -e ".[dev]"
```

---

## Quickstart: Analyze Your Repository

### 1. Initialize Configuration

Create a sensemaking configuration file in your repository:

```bash
sensemaking-skills init --repo /path/to/your/repo
```

This creates `sensemaking-config.yaml` with default analysis settings.

### 2. Run Analysis Workflow

Execute the default diagnostic workflow:

```bash
sensemaking-skills analyze --repo /path/to/your/repo
```

This performs:
- **Repository Structure Analysis**: Maps code organization, imports, and dependencies
- **Fog Type Detection**: Classifies the problem as product_fog, ui_fog, docs_fog, or architecture_fog
- **Weakness Identification**: Locates the weakest boundary in the codebase
- **Workflow Recommendation**: Suggests the best implementation workflow

### 3. Check Results

Find the generated artifacts in the `.sensemaking/artifacts/` directory:

```bash
# View the diagnostic brief
cat /path/to/your/repo/.sensemaking/artifacts/repository_sensemaking_brief.md

# View recommended workflow
cat /path/to/your/repo/.sensemaking/artifacts/workflow_orchestration_plan.md
```

---

## Manual Path: Full Control

Use the **manual path** when you want to inspect artifacts between stages and make explicit decisions at each step.

### Flow

```
1. Run diagnostic workflow
2. Review output artifacts
3. Decide next step
4. Run implementation workflow
5. Review and approve changes
```

### Example: Analyze Then Implement

```bash
# Step 1: Run diagnostic workflow with explicit pauses
sensemaking-skills analyze --repo /path/to/repo \
  --workflow fast-path-workflow \
  --mode guided_execution

# Output: Repository Sensemaking Brief (with fog_type and recommended workflow)

# Step 2: Read the brief and results
cat .sensemaking/artifacts/repository_sensemaking_brief.md

# Step 3: Manually invoke the recommended implementation workflow
sensemaking-skills run-workflow \
  --repo /path/to/repo \
  --workflow product-implementation-workflow \
  --mode guided_execution \
  --from-session .sensemaking/artifacts

# Output: PRD, issues, code patches (with gates for approval)
```

### Manual Invocation with `--from-session`

When running a follow-up workflow, use `--from-session` to reuse artifacts from the prior diagnostic run:

```bash
sensemaking-skills run-workflow \
  --repo /path/to/repo \
  --workflow product-implementation-workflow \
  --mode guided_execution \
  --from-session .sensemaking/artifacts
```

This passes the problem statement, fog type, and repository context from the diagnostic phase, so the implementation workflow doesn't need to re-analyze.

---

## Automation Path: Full Speed

Use the **automation path** for end-to-end runs with automatic progression through all stages.

### Flow

```
1. Single command invocation
2. System auto-chains all workflows
3. Final output includes everything: diagnosis + plan + PRD + issues + code
```

### Example: Single Command, Complete Analysis & Implementation

```bash
# Single command: everything runs automatically
sensemaking-skills analyze --repo /path/to/repo \
  --workflow full-local-sensemaking \
  --mode autonomous_execution

# Output: Full pipeline completes with:
# - Repository Sensemaking Brief
# - Workflow Orchestration Plan
# - PRD (if product_fog detected)
# - Implementation Issues (if appropriate workflow invoked)
# - Code patches (if TDD workflow included)
```

### Benefits

- **No manual steps**: System auto-chains based on fog type
- **Deterministic routing**: Uses machine-readable workflow registry
- **Production-ready**: Exit code 0 on success, 2 on failure, 3 if paused
- **Audit trail**: Run log records all decisions and approvals

---

## Execution Modes

| Mode | Gates | Speed | Best For | When to Use |
|------|-------|-------|----------|-------------|
| `guided_execution` | Pause at every gate (user approves) | Slowest | Development, exploration | Learning the system, high-value decisions |
| `autonomous_execution` | Auto-approve all valid gates | Fast | Production, CI/CD | Unattended runs, automation |
| `plan_only` | No execution, show plan only | Instant | Validation, dry-run | What-if analysis, planning |

### Execution Mode Examples

**Guided Mode** - Pause at each step for approval:
```bash
sensemaking-skills analyze --repo /path/to/repo --mode guided_execution
```

**Autonomous Mode** - Full automation with auto-approval:
```bash
sensemaking-skills analyze --repo /path/to/repo --mode autonomous_execution
```

**Plan Only** - See the plan without executing:
```bash
sensemaking-skills analyze --repo /path/to/repo --mode plan_only
```

---

## Customization

### Using Custom Skills

To use custom diagnostic or implementation skills alongside built-in ones, see [EXTENDING.md](EXTENDING.md) for:
- Creating custom skills
- Defining custom workflows
- Overriding canonical vocabulary
- Composing mixed skill chains

### Configuration Options

Edit `sensemaking-config.yaml` to customize:

```yaml
# Repository root for analysis
repo_root: /path/to/repo

# Output directory for artifacts
artifacts_dir: .sensemaking/artifacts

# Execution mode
execution_mode: guided_execution

# Skills to load
skills:
  enabled:
    - repo-sensemaker
    - workflow-planner
  disabled: []

# Custom vocabulary overrides
vocabulary:
  fog_types:
    - product_fog
    - ui_fog
    - docs_fog
    - architecture_fog
```

See [docs/configuration.md](docs/configuration.md) for full configuration reference.

---

## Troubleshooting

### "Configuration file not found"

**Error**: `Configuration file not found: repo/sensemaking-config.yaml`

**Solution**: Initialize the repository first:
```bash
sensemaking-skills init --repo /path/to/repo
```

### "Workflow not found"

**Error**: `Workflow not found: xyz-workflow`

**Solution**: List all available workflows:
```bash
sensemaking-skills list-workflows
```

Then use a workflow ID from the list.

### "Skill executor failed"

**Error**: `Skill executor failed: Claude API returned error`

**Solutions**:
1. Verify your Anthropic API key is set: `echo $ANTHROPIC_API_KEY`
2. Check your API quota and usage at https://console.anthropic.com
3. Try again with `--mode plan_only` to skip execution
4. Check the run log: `cat .sensemaking/logs/latest.log`

### "Artifacts directory not found"

**Error**: `Artifacts directory not found: .sensemaking/artifacts`

**Solution**: Ensure the diagnostic workflow completed successfully:
```bash
# Verify artifacts exist
ls -la .sensemaking/artifacts/

# Or re-run the workflow
sensemaking-skills analyze --repo /path/to/repo --mode guided_execution
```

### Increasing Verbosity

To see detailed logs and debug output:

```bash
# Set environment variable
export DEBUG=true

# Then run your command
sensemaking-skills analyze --repo /path/to/repo
```

---

## Next Steps

- **Learn by Example**: See [GETTING_STARTED.md](GETTING_STARTED.md) for step-by-step walkthroughs
- **Extend the System**: See [EXTENDING.md](EXTENDING.md) to add custom skills and workflows
- **API Integration**: See [API.md](API.md) to use sensemaking-skills in Python code
- **Full Reference**: See [README.md](README.md) for complete feature overview

---

## Support

- **Issues**: Report bugs at https://github.com/dimmi-andreus/sensemaking-skills/issues
- **Discussions**: Ask questions at https://github.com/dimmi-andreus/sensemaking-skills/discussions
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute improvements

---

## License

MIT License - See [LICENSE](LICENSE) for details.
