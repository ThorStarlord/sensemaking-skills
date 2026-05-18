# Implementation Guide: validate-finance-system Skill

This document provides technical details for implementing and extending the validate-finance-system skill.

## Architecture Overview

The skill is implemented as a wrapper around the orchestration-runner.py that manages:
1. Workflow execution with multiple modes
2. Baseline comparison and caching
3. GitHub issue creation
4. Result aggregation and reporting

### Component Stack

```
┌─────────────────────────────────────────────┐
│  Claude Code / Agent Interface               │
│  (invoke skill via CLI or programmatic API) │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│  validate-finance-system.ps1                │
│  (CLI wrapper, mode routing, caching)       │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│  orchestration-runner.py                    │
│  (Workflow execution engine)                │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│  Workflow Steps:                            │
│  ├─ problem-framer skill                   │
│  ├─ unknowns-mapper skill                  │
│  ├─ repo-sensemaker skill                  │
│  └─ workflow-orchestrator skill             │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│  Outputs & Artifacts                        │
│  ├─ validation_summary.md                  │
│  ├─ error_analysis.md                      │
│  ├─ GitHub issues (optional)               │
│  └─ .validation-cache/latest               │
└─────────────────────────────────────────────┘
```

## Execution Modes

### Mode: plan_only
**Purpose**: Preview the workflow without executing it

**Behavior**:
- Loads and validates the workflow definition
- Displays execution plan (steps, dependencies, expected artifacts)
- Uses lenient validation (warnings only)
- No artifacts produced
- No side effects

**When to Use**:
- Understanding the validation process
- Previewing before first run
- Debugging workflow configuration

**Exit Code**: 0 on success, 1 on errors

### Mode: guided_execution
**Purpose**: Interactive validation with human-in-the-loop review

**Behavior**:
- Executes all workflow steps
- Pauses after error analysis for human review
- Allows manual selection of which errors to ticket
- Uses strict validation (fails on missing artifacts)
- Creates GitHub issues selectively (only reviewed errors)

**When to Use**:
- First-time validations
- Understanding errors before ticketing
- Manual triage and prioritization
- Decision gate reviews

**User Interactions**:
1. Review problem frame
2. Review unknowns map
3. Review error analysis
4. Select which errors to create tickets for
5. Approve corrective actions

**Exit Code**: 0 on success, 1 on validation errors

### Mode: autonomous_execution
**Purpose**: Fully automated validation without user interaction

**Behavior**:
- Executes all workflow steps without pauses
- Uses strict validation
- Automatically creates GitHub issues for all errors found (with --create-tickets)
- Updates baseline cache
- Generates comprehensive reports

**When to Use**:
- CI/CD pipelines
- Scheduled validations
- Large-scale error discovery
- Fully trusted validation logic

**Configuration**:
- `--create-tickets`: Auto-create GitHub issues for all errors
- `--compare-baseline`: Compare against baseline cache

**Exit Code**: 0 on success, 1 on validation errors, 2 on errors found but validation complete

## Key Features

### Baseline Comparison

When run with `--compare-baseline`:

**Behavior**:
1. Loads latest baseline from `.validation-cache/latest`
2. Compares current error analysis against baseline
3. Categorizes errors:
   - **NEW**: Errors in current but not baseline
   - **FIXED**: Errors in baseline but not current
   - **UNCHANGED**: Errors in both

**Output**:
- `comparison_report.md`: Side-by-side comparison
- `error_comparison.md`: Summary of changes

**Cache Location**: `.validation-cache/latest/`

**Cache Contents**:
- `problem_frame.md`
- `error_analysis.md`
- `changes_identified.md`
- `sensemaking_brief.md`
- Timestamp of validation run

### GitHub Issue Creation

When run with `--create-tickets`:

**Behavior**:
1. For each error in error analysis:
   - Create GitHub issue in target repository
   - Use error description as title
   - Include detailed context in body
   - Tag with validation labels

**Issue Format**:
```markdown
# Finance System Error: [Error Type]

**Severity**: [HIGH/MEDIUM/LOW]
**Component**: [finance-system]

## Description
[Detailed error description]

## Impact
[What this error affects]

## Reproduction
[How to reproduce the error]

## Related Evidence
- Problem Frame: [link to problem_frame.md]
- Error Analysis: [link to error_analysis.md]
```

**Labels**:
- `validation-found` — Error discovered by validation workflow
- `finance-system` — Specific to finance system
- `severity-{high|medium|low}` — Based on error severity

**Configuration**:
- GitHub token from environment (GITHUB_TOKEN)
- Target repository from workflow metadata
- Issue labels configurable in workflow definition

**Error Handling**:
- Network failures don't block workflow
- Failed tickets are logged and reported
- Allows manual retry of failed ticketing

### Artifact Production

**Strict Mode** (execution modes):
- Validates that all artifacts exist
- Fails if any artifact missing
- Ensures data integrity
- Used in `guided_execution`, `autonomous_execution`

**Lenient Mode** (plan modes):
- Warns if artifacts don't exist
- Doesn't fail
- Allows planning ahead
- Used in `plan_only`

**Validation Rule**: orchestration-patterns.md Pattern 1

## Integration Points

### Claude Code Invocation

**Via Command Line**:
```powershell
./scripts/validate-finance-system.ps1 -Mode guided_execution -CompareBaseline
```

**Via Claude Skill**:
```yaml
skill: validate-finance-system
action: validate-guided
config:
  compare_baseline: true
```

### CI/CD Integration

**GitHub Actions Example**:
```yaml
- name: Validate Finance System
  run: |
    cd ${{ github.workspace }}
    ./scripts/validate-finance-system.ps1 `
      -Mode autonomous_execution `
      -CompareBaseline `
      -CreateTickets
```

### Programmatic API

**Python**:
```python
import subprocess
import json

result = subprocess.run([
    './scripts/validate-finance-system.ps1',
    '-Mode', 'autonomous_execution',
    '-CreateTickets'
], capture_output=True, text=True)

# Parse output_dir timestamp from stdout
validation_results = json.load(open('outputs/validation-TIMESTAMP/summary.json'))
```

**Agent Workflow**:
```yaml
orchestration:
  decision_gate:
    - validate_finance_system:
        mode: autonomous_execution
        create_tickets: true
        compare_baseline: true
    - if: validation_errors > 0
      then:
        - workflow_orchestrator:
            input: validation_errors
            action: select_corrective_actions
```

## Configuration

### Workflow Configuration

File: `docs/workflows/validation-finance-system.yaml`

**Key Settings**:
- `execution_config.mode` — Default execution mode
- `validation_rules` — Which patterns to enforce
- `workflow_steps` — Steps to execute
- `output_artifacts` — What to produce
- `output_artifacts.tickets.auto_create_github_issues` — Enable auto-ticketing

### Script Parameters

**validate-finance-system.ps1 Parameters**:

| Parameter | Type | Default | Purpose |
|-----------|------|---------|---------|
| `-Mode` | ValidateSet | `guided_execution` | Execution mode |
| `-CompareBaseline` | Switch | $false | Compare against baseline |
| `-CreateTickets` | Switch | $false | Auto-create GitHub issues |
| `-Force` | Switch | $false | Skip validation checks |

## Error Handling

### Validation Errors

**Strict Mode Failures**:
```
ERROR: ARTIFACT_NOT_FOUND: sensemaking_brief.md
  Expected to be produced by: analyze_repo step
  Status: FAILED
  Exit Code: 1
```

**Action**: 
- Check orchestration-runner.py logs
- Verify workflow YAML is correct
- Ensure dependencies are satisfied

### External Service Failures

**GitHub API Failures**:
```
WARNING: Failed to create issue for error "FinanceError001"
  GitHub API returned: 403 Forbidden
  Continuing with other tickets...
```

**Action**:
- Check GitHub token validity
- Verify repository access
- Retry failed tickets manually

### Resource Issues

**Timeout**:
```
WARNING: Analysis took longer than expected (> 5 minutes)
  Large repository may take additional time
  Continuing validation...
```

**Action**:
- For large repos, expect 5-10 minute execution
- Run in autonomous mode to avoid timeouts from user interaction
- Consider breaking into smaller validation scopes

## Extending the Skill

### Adding New Validation Steps

1. Add step to `docs/workflows/validation-finance-system.yaml`:
```yaml
- id: "custom_check"
  type: "custom_skill"
  description: "Run custom validation"
  depends_on: ["analyze_repo"]
  inputs:
    - name: "error_analysis"
      source: "analyze_repo"
  outputs:
    - name: "custom_report.md"
```

2. Implement the skill following the sensemaking-skills pattern

3. Update artifact list in workflow YAML

4. Test with `--mode plan_only` first

### Adding New Execution Modes

1. Add mode validation to script:
```powershell
[ValidateSet('plan_only', 'guided_execution', 'autonomous_execution', 'new_mode')]
```

2. Add mode handling in orchestration-runner.py:
```python
elif self.mode == "new_mode":
    # Custom logic for new mode
```

3. Document mode in SKILL.md

4. Add integration examples

### Customizing Issue Templates

Edit the ticket creation logic in orchestration-runner.py to customize:
- Issue title format
- Issue body template
- Label assignment logic
- Assignment logic

## Performance Considerations

### Execution Time

**Typical Times**:
- `plan_only`: < 1 second
- `guided_execution`: 5-10 minutes (depends on repo size)
- `autonomous_execution`: 5-10 minutes (no interactive delays)

**Optimization**:
- First run slowest (full analysis)
- Subsequent runs faster (cached comparison)
- Large repos (10k+ files) may take 15+ minutes

### Memory Usage

**Typical Usage**:
- Skill loader: ~50 MB
- Orchestration runner: ~100-200 MB
- Large repo analysis: ~500 MB+

**Optimization**:
- Run on machine with 2+ GB free RAM
- Limit repository size analyzed (use focus setting)

### Caching

**What's Cached**:
- Latest baseline in `.validation-cache/latest/`
- Workflow analysis results in `.validation-cache/analyses/`

**Cache Lifecycle**:
- Updated after each successful run
- Use `.validation-cache/latest/` for baseline comparison
- Older caches in `.validation-cache/` can be archived

## Testing

### Unit Testing

Test individual validation steps:
```bash
python -m pytest scripts/test-validators.py -v
```

### Integration Testing

Test full workflow:
```bash
./scripts/validate-finance-system.ps1 -Mode plan_only
./scripts/validate-finance-system.ps1 -Mode guided_execution  # Manual review
```

### Regression Testing

Compare against baseline:
```bash
./scripts/validate-finance-system.ps1 -Mode autonomous_execution -CompareBaseline
# Check comparison_report.md for regressions
```

## Monitoring & Observability

### Log Output

**Locations**:
- Console output: Real-time execution trace
- `outputs/validation-TIMESTAMP/execution.log`: Full execution log
- `outputs/validation-TIMESTAMP/errors.log`: Error summary

**Log Levels**:
- INFO: Progress updates
- WARNING: Non-blocking issues
- ERROR: Validation failures

### Success Indicators

**Successful Validation**:
- Exit code 0
- All artifacts produced
- `validation_summary.md` exists
- No FAILED validation rules

**Issues Found**:
- Exit code 0 (validation completed)
- `error_analysis.md` contains errors
- GitHub issues created (if --create-tickets)
- `error_comparison.md` shows breakdown

### Metrics

Track over time:
- Total errors found
- New errors per run
- Fixed errors per run
- Validation execution time
- Average error severity

## Security Considerations

### GitHub Token Handling

- Token read from environment: `GITHUB_TOKEN`
- Never logged or displayed
- Token must have repo write permission
- Rotate token if exposed

### Input Validation

- Workflow YAML validated before execution
- Path traversal prevention in file operations
- GitHub API calls signed and authenticated

### Artifact Access

- All artifacts output to `outputs/validation-TIMESTAMP/`
- Directory isolation prevents data leakage
- Consider access controls on outputs/ directory

## References

- [Orchestration Patterns](../orchestration-patterns.md)
- [Validation Workflow Definition](../workflows/validation-finance-system.yaml)
- [Orchestration Runner Implementation](../scripts/orchestration-runner.py)
- [Full Fog Path Methodology](../philosophy/)
