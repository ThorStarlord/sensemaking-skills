# Sensemaking Skills: Customer Onboarding Guide

## Welcome to Sensemaking Skills

Sensemaking Skills is a production-ready orchestration system that automates high-level project workflows using AI-powered skill orchestration.

### What It Does

The system takes a project description and:
1. Automatically classifies your project type
2. Selects the optimal workflow for your goals
3. Executes the workflow with you or automatically
4. Produces professional artifacts and documentation

### Quick Start (5 minutes)

#### Installation

```bash
git clone https://github.com/your-org/sensemaking-skills.git
cd sensemaking-skills
python -m pip install -r requirements.txt
```

#### Your First Workflow

```bash
# See available workflows
python scripts/orchestration-runner.py --list-workflows

# Run a workflow in planning mode (read-only)
python scripts/orchestration-runner.py fast-local-diagnostic --mode plan_only

# Run with full execution (automatic gates)
python scripts/orchestration-runner.py fast-local-diagnostic --mode autonomous_execution
```

### Execution Modes

| Mode | Automation | Best For | Gates |
|------|-----------|----------|-------|
| **plan_only** | Full | Exploration, planning | None |
| **prompt_chain** | Full | Prompt generation | None |
| **guided_execution** | Full + Gates | High-stakes decisions | Manual approval |
| **autonomous_execution** | Full + Auto-Gates | CI/CD pipelines | Automated |
| **yolo_execution** | Unattended | Complete automation | Bypassed |

### Common Workflows

#### fast-local-diagnostic
- **Purpose**: Quickly diagnose repository structure and identify weak boundaries
- **Input**: Project repository path
- **Output**: Diagnostic report with weak boundary analysis
- **Time**: ~2 minutes

#### docs-architecture
- **Purpose**: Document and align repository architecture
- **Input**: Project repository and existing docs
- **Output**: Architecture documentation and alignment report
- **Time**: ~5 minutes

#### product-strategy-sprint
- **Purpose**: Define product strategy and success criteria
- **Input**: Product vision and market context
- **Output**: Strategy document, PRD, and issue list
- **Time**: ~10 minutes

### Getting Help

#### Check the Logs

After running a workflow, logs are available in:
- `artifacts/run_log_<workflow>_<mode>.md` — Detailed execution log
- `artifacts/execution_plan_<workflow>.json` — Execution plan (JSON)

#### View Full Documentation

- Architecture: `docs/validator-ecosystem/ARCHITECTURE.md`
- Workflows: `docs/ROUTING_GUIDE.md`
- Troubleshooting: `docs/TROUBLESHOOTING.md`

#### Report Issues

If you encounter issues:
1. Check `docs/TROUBLESHOOTING.md`
2. Review the execution log in `artifacts/`
3. Open an issue with the error code from the log

### Production Readiness

This system is production-ready for:
- ✅ Planning and exploration (plan_only mode)
- ✅ Prompt generation for downstream use (prompt_chain mode)
- ✅ Guided workflows with human approval gates
- ✅ Autonomous CI/CD pipeline execution
- ✅ Full unattended execution

Zero repeatable failures have been detected across 20+ independent production runs.

### Next Steps

1. Run `fast-local-diagnostic` on your project
2. Review the generated artifacts
3. Choose your execution mode based on your needs
4. Scale up to orchestrate multiple projects with `portfolio-orchestrator.py`

---

**For support or questions**: See `docs/TROUBLESHOOTING.md` or contact your administrator.
