---
name: validate-finance-system
description: Run finance system validation workflow at decision gates using Full Fog Path. Automates validation, comparison, and GitHub issue creation.
---

# validate-finance-system

Automates validation of the finance system after each iteration using the Full Fog Path orchestration workflow. Executes at decision gates to identify errors, compare against baselines, and orchestrate corrective actions.

## When to Use

Use this skill when:
- **Decision gates**: Validating the finance system before committing changes or closing development phases
- **Error discovery**: Running comprehensive error analysis after significant feature development
- **Baseline comparison**: Comparing current state against known-good baseline validations
- **Autonomous fixing**: Automatically creating GitHub issues for validation errors found
- **Planning ahead**: Previewing what validation would do before executing

## Execution Modes

### Guided Validation (Default)
**Command**: `validate-finance-system --mode guided_execution`

Interactive validation mode where you review results before proceeding. Useful for:
- First-time validations on a new system
- Manual error review and triage
- Understanding what validation finds
- Selective issue creation

### Autonomous Validation
**Command**: `validate-finance-system --mode autonomous_execution --create-tickets`

Fully automated validation that creates GitHub issues automatically. Use when:
- Running in CI/CD pipelines
- Confident in validation logic
- Need rapid error discovery and ticketing
- Running scheduled validations

### Validation with Baseline Comparison
**Command**: `validate-finance-system --mode guided_execution --compare-baseline`

Compares current validation results against the latest baseline cache. Shows:
- What's new (errors not in baseline)
- What's fixed (errors no longer present)
- What's unchanged (persistent errors)

### Plan Only (Preview)
**Command**: `validate-finance-system --mode plan_only`

Previews the validation workflow without executing it. Shows:
- What validation steps will run
- What artifacts will be produced
- Estimated execution flow
- Resource requirements

## Workflow Overview

The validation workflow follows the Full Fog Path pattern:

```
1. Frame Problem          → Establish validation scope
2. Map Unknowns         → Identify research paths
3. Analyze Repository   → Find errors in finance system
4. Orchestrate Fixes    → Select corrective actions
5. Create Tickets       → Auto-create GitHub issues (optional)
```

Each step produces evidence artifacts that feed into the next step.

## Output Artifacts

### Reports
- `validation_summary.md` — High-level summary of validation results
- `error_comparison.md` — Comparison against baseline (if comparing)
- `changes_summary.md` — Summary of changes identified in the system

### Evidence
- `problem_frame.md` — Framed problem statement and scope
- `unknowns_map.md` — Map of unknowns in the finance system
- `research_paths.md` — Identified research paths to resolve unknowns
- `sensemaking_brief.md` — Repository state summary
- `error_analysis.md` — Detailed error findings
- `changes_identified.md` — Changes identified in the system
- `comparison_report.md` — Baseline comparison report (if comparing)
- `selected_workflow.md` — Selected workflow for corrections
- `corrective_actions.md` — Identified corrective actions
- `next_steps.md` — Next steps for implementation

### GitHub Issues
When using `--create-tickets`:
- Automatically creates GitHub issues in target repository
- Tags with `validation-found` and `finance-system` labels
- Links to detailed error analysis
- Includes reproduction context

## Usage Examples

### First-time validation after development
```bash
./skills/validate-finance-system/validate --mode guided_execution
```

Prompts you to review each error and decide whether to create a ticket.

### Autonomous validation with auto-ticketing
```bash
./skills/validate-finance-system/validate --mode autonomous_execution --create-tickets
```

Runs full validation pipeline and automatically creates tickets for all errors found.

### Validation with baseline comparison
```bash
./skills/validate-finance-system/validate --mode guided_execution --compare-baseline
```

Shows what's new, fixed, and persistent since the last validation.

### Preview validation without executing
```bash
./skills/validate-finance-system/validate --mode plan_only
```

Shows the validation plan without running it.

## Decision Gate Checklist

Use this checklist at decision gates to ensure quality validation:

- [ ] Understand the scope: What part of the finance system changed?
- [ ] Choose the validation mode: guided for first-time, autonomous for CI/CD
- [ ] Know your baseline: Have you validated this before?
- [ ] Review the summary: Did validation find expected errors?
- [ ] Triage issues: Which errors must be fixed before proceeding?
- [ ] Create tickets: Are they auto-created or manually created?
- [ ] Update cache: Should the latest results become the new baseline?

## Validation Modes Reference

| Mode | Interactive | Creates Tickets | Best For |
|------|-----------|-----------------|----------|
| `guided_execution` | Yes | Manual | First runs, manual review |
| `autonomous_execution` | No | Auto (with flag) | CI/CD, scheduled runs |
| `plan_only` | No | No | Preview, understanding flow |

## Integration Patterns

### With Decision Gates
Run validation at key decision points:
- After completing a feature iteration
- Before closing a development sprint
- Before merging to main branch

### With GitHub Actions
```yaml
- name: Validate Finance System
  run: ./scripts/validate-finance-system.ps1 -Mode autonomous_execution -CreateTickets
```

### With Claude Agent Workflows
```yaml
workflow:
  - skill: validate-finance-system
    action: validate-autonomous
    config:
      create_tickets: true
      compare_baseline: true
```

## Troubleshooting

### "Workflow configuration not found"
- Ensure `docs/workflows/validation-finance-system.yaml` exists
- Check that the file path is correct relative to your repository root
- Verify the YAML is well-formed

### "Python not available in PATH"
- The orchestration runner requires Python 3.x
- Install Python or update your PATH
- Validation can continue but orchestration features may be limited

### "GitHub issues not creating"
- Check GitHub credentials are configured
- Verify the target repository is accessible
- Check that `--create-tickets` flag is included
- Review ticket creation logs in outputs/

### "Baseline comparison shows all errors as new"
- Baseline cache may be outdated or missing
- Run with `--compare-baseline` to create a new baseline
- Use `.validation-cache/latest` to view the current baseline

### "Validation takes too long"
- Large repositories may take several minutes
- First run will be slower due to analysis
- Subsequent runs use cached comparison data
- Consider running in autonomous mode to avoid interactive delays

## Key Concepts

### Full Fog Path
The validation workflow follows the Full Fog Path pattern: Problem → Unknowns → Repository Analysis → Orchestration → Action. This ensures validation is comprehensive and evidence-driven.

### Strict Validation in Execution Modes
When running in `guided_execution` or `autonomous_execution` modes, validation is strict: all artifacts must exist and all checks must pass. Plan modes use lenient validation (warnings only).

### Baseline Caching
The validation system caches results in `.validation-cache/latest` to enable baseline comparison. Use `--compare-baseline` to see what changed since the last validation.

### Orchestration Integration
Validated errors feed into the orchestration system, which can automatically select and execute corrective workflows based on error severity and type.

## References

- [Validation Workflow Design](../../docs/workflows/validation-finance-system.yaml)
- [Orchestration Patterns](../../docs/orchestration-patterns.md)
- [Validation Guides](../../docs/validator-ecosystem/)
