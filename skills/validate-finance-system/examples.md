# Examples: validate-finance-system Skill

Practical examples of using the validate-finance-system skill in real workflows.

## Example 1: First-Time Validation After Development

**Scenario**: You've completed a feature iteration on the finance system and want to validate before merging.

**Goal**: Run validation, review errors, and manually decide which errors to create tickets for.

### Step 1: Run guided validation

```powershell
PS> cd H:\GithubRepositories\sensemaking-skills
PS> .\scripts\validate-finance-system.ps1 -Mode guided_execution

========================================
VALIDATION STARTUP
==========================================
OK Workflow config found: docs/workflows/validation-finance-system.yaml
OK Orchestrator script found: scripts/orchestration-runner.py
OK Python available: Python 3.11.5

========================================
EXECUTION PLAN
==========================================
Mode: guided_execution
- Frame problem space
- Map unknowns
- Analyze repository
- Orchestrate fixes
- [PAUSED] Review errors before ticketing

Starting execution...

[Step 1/4] problem-framer
  - Framing finance system validation...
  - Output: problem_frame.md ✓

[Step 2/4] unknowns-mapper
  - Mapping unknowns...
  - Output: unknowns_map.md ✓
  - Output: research_paths.md ✓

[Step 3/4] repo-sensemaker
  - Analyzing finance system code...
  - Output: sensemaking_brief.md ✓
  - Output: error_analysis.md ✓
  - Output: changes_identified.md ✓

========================================
ERRORS FOUND - HUMAN REVIEW REQUIRED
========================================

Found 5 errors in finance system:

1. FinanceError001: Missing null check in payment processor
   Severity: HIGH
   Location: metamorfose-edutech/src/finance/payment.py:123
   Impact: Could cause transaction failures

2. FinanceError002: Inefficient database query in report generation
   Severity: MEDIUM
   Location: metamorfose-edutech/src/finance/reports.py:456
   Impact: Reports take 30+ seconds to generate

3. FinanceError003: Missing audit log for refund operations
   Severity: HIGH
   Location: metamorfose-edutech/src/finance/refunds.py:789
   Impact: Compliance risk, no audit trail

4. FinanceError004: Race condition in balance calculation
   Severity: MEDIUM
   Location: metamorfose-edutech/src/finance/balance.py:234
   Impact: Occasional balance discrepancies

5. FinanceError005: Deprecated library in payment integration
   Severity: LOW
   Location: requirements.txt:42
   Impact: Security update available

========================================
CREATE TICKETS?
=========================================

Select which errors to create GitHub issues for (enter comma-separated numbers):
> 1,3

Creating tickets...
- Issue #1234 created: FinanceError001: Missing null check in payment processor
- Issue #1235 created: FinanceError003: Missing audit log for refund operations

========================================
VALIDATION COMPLETE
=========================================
Errors found: 5
Tickets created: 2
Skipped: 3 (for later triage)

Results saved to: outputs/validation-20260518-143022/
```

### Step 2: Review the detailed error analysis

```powershell
PS> cat outputs/validation-20260518-143022/error_analysis.md

# Error Analysis: Finance System Validation

## Executive Summary
Validation found 5 errors in the finance system, ranging from HIGH to LOW severity.

### High Severity (2)
- FinanceError001: Missing null check in payment processor
- FinanceError003: Missing audit log for refund operations

### Medium Severity (2)
- FinanceError002: Inefficient database query in report generation
- FinanceError004: Race condition in balance calculation

### Low Severity (1)
- FinanceError005: Deprecated library in payment integration

## Detailed Findings

### FinanceError001: Missing null check in payment processor

**Location**: metamorfose-edutech/src/finance/payment.py:123-145

**Description**:
The payment processing function doesn't check if payment_method is None before calling methods on it. This can cause AttributeError exceptions in production.

**Code**:
```python
def process_payment(amount, payment_method):
    # Missing: if payment_method is None: raise ValueError(...)
    result = payment_method.validate()  # Could fail here
    return payment_method.charge(amount)
```

**Impact**: 
- Transaction failures for certain payment scenarios
- Potential customer-facing errors
- Data consistency issues

**Recommendation**: Add null check and proper error handling

## [Additional detailed findings...]
```

### Step 3: Plan next steps

You've now created 2 tickets (HIGH severity) and identified 3 more for later triage. You can proceed with merging while planning to address the medium/low severity errors.

## Example 2: Autonomous Validation with Auto-Ticketing

**Scenario**: Running validation in a CI/CD pipeline after every successful build.

**Goal**: Fully automated validation that creates all tickets automatically.

### GitHub Actions Workflow

```yaml
# .github/workflows/validate-finance.yml
name: Validate Finance System

on:
  schedule:
    # Run after every successful build
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_run:
    workflows: ["Build & Test"]
    types: [completed]
    branches: [main]

jobs:
  validate:
    runs-on: windows-latest
    
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Run Validation
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          cd H:\GithubRepositories\sensemaking-skills
          .\scripts\validate-finance-system.ps1 `
            -Mode autonomous_execution `
            -CreateTickets `
            -CompareBaseline
      
      - name: Upload Results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: validation-results
          path: outputs/validation-*/
      
      - name: Post Validation Summary
        if: always()
        run: |
          $summary = Get-Content outputs/validation-*/validation_summary.md
          echo $summary
          echo "::notice::Validation complete - see artifacts for details"
```

### Script Execution

```powershell
PS> .\scripts\validate-finance-system.ps1 -Mode autonomous_execution -CreateTickets -CompareBaseline

========================================
VALIDATION STARTUP
==========================================
OK Workflow config found
OK Orchestrator script found
OK Python available

========================================
AUTONOMOUS EXECUTION (CI/CD MODE)
==========================================
Mode: autonomous_execution
Auto-create tickets: enabled
Compare baseline: enabled

Starting execution...

[Step 1/4] problem-framer ✓
[Step 2/4] unknowns-mapper ✓
[Step 3/4] repo-sensemaker ✓
[Step 4/4] workflow-orchestrator ✓

========================================
COMPARISON REPORT
==========================================

Comparing against baseline from 2026-05-17T20:30:00Z

NEW ERRORS (2):
- FinanceError006: New validation rule violation
- FinanceError007: Deprecated import detected

FIXED ERRORS (1):
- FinanceError001: Previously found missing null check (NOW FIXED!)

UNCHANGED ERRORS (3):
- FinanceError002: Still present
- FinanceError004: Still present
- FinanceError005: Still present

========================================
TICKET CREATION
==========================================

Created 5 issues in metamorfose-edutech:
✓ Issue #1236: FinanceError006: New validation rule violation
✓ Issue #1237: FinanceError007: Deprecated import detected
✓ Issue #1238: FinanceError002: Inefficient database query (updated)
✓ Issue #1239: FinanceError004: Race condition (updated)
✓ Issue #1240: FinanceError005: Deprecated library (updated)

Updated baseline cache: .validation-cache/latest/

========================================
VALIDATION COMPLETE
==========================================
Severity breakdown:
- HIGH: 2 errors
- MEDIUM: 2 errors
- LOW: 1 error

Exit code: 0 (validation complete, errors found)
```

### Results Interpretation

- **NEW errors**: Require attention before next merge
- **FIXED errors**: Good progress! Previous errors are resolved
- **UNCHANGED errors**: Persistent issues to track
- **Issues updated**: GitHub issues created/updated with latest findings
- **Baseline updated**: Next run will compare against these results

## Example 3: Baseline Comparison for Quality Metrics

**Scenario**: Tracking validation metrics over time to understand system health.

**Goal**: Compare current validation against baseline and track progress.

### Run validation with comparison

```powershell
PS> .\scripts\validate-finance-system.ps1 -Mode guided_execution -CompareBaseline

[... validation runs ...]

========================================
BASELINE COMPARISON
==========================================

Previous validation: 2026-05-17T20:30:00Z
Current validation:  2026-05-18T14:30:00Z
Time delta: 18 hours

Error Summary:
- Previous: 8 total errors (3 HIGH, 3 MEDIUM, 2 LOW)
- Current:  7 total errors (2 HIGH, 3 MEDIUM, 2 LOW)
- Change:   -1 total (✓ improved by 1)

Breakdown:
┌─────────────────────────────────────────────┐
│ Error Category  │ Previous │ Current │ Delta │
├─────────────────────────────────────────────┤
│ HIGH Severity   │    3     │    2    │  -1  │
│ MEDIUM Severity │    3     │    3    │   0  │
│ LOW Severity    │    2     │    2    │   0  │
└─────────────────────────────────────────────┘

NEW ERRORS (1):
- FinanceError007: Deprecated import (NEW)

FIXED ERRORS (2):
- FinanceError001: Missing null check (FIXED)
- FinanceError003: Missing audit log (FIXED)

PERSISTENT ERRORS (5):
- FinanceError002: Database query inefficiency
- FinanceError004: Race condition
- FinanceError005: Deprecated library
- FinanceError006: Validation rule violation
- FinanceError008: Documentation gap

Progress Metrics:
- Fix rate: 2 errors fixed / 1 new = 2:1 ratio (✓ positive trend)
- Days to fix: ~18 hours (fast resolution)
- System health: IMPROVING
```

### Extract metrics for dashboard

```python
# scripts/extract-metrics.py
import json
import yaml
from pathlib import Path

def extract_metrics():
    comparison = json.load(open('outputs/validation-*/comparison_report.json'))
    
    metrics = {
        'timestamp': comparison['timestamp'],
        'total_errors': len(comparison['current']['errors']),
        'high_severity': len(comparison['current']['high']),
        'medium_severity': len(comparison['current']['medium']),
        'low_severity': len(comparison['current']['low']),
        'new_errors': len(comparison['new']),
        'fixed_errors': len(comparison['fixed']),
        'unchanged_errors': len(comparison['unchanged']),
        'trend': 'improving' if len(comparison['fixed']) > len(comparison['new']) else 'degrading'
    }
    
    print(json.dumps(metrics, indent=2))

if __name__ == '__main__':
    extract_metrics()
```

Output for dashboard:
```json
{
  "timestamp": "2026-05-18T14:30:00Z",
  "total_errors": 7,
  "high_severity": 2,
  "medium_severity": 3,
  "low_severity": 2,
  "new_errors": 1,
  "fixed_errors": 2,
  "unchanged_errors": 5,
  "trend": "improving"
}
```

## Example 4: Planning Mode (Preview Workflow)

**Scenario**: Want to understand what validation does before running it.

**Goal**: Preview the workflow without executing it.

### Run plan mode

```powershell
PS> .\scripts\validate-finance-system.ps1 -Mode plan_only

========================================
VALIDATION PLAN (PREVIEW MODE)
==========================================

Workflow: finance-system-validation
Description: Validates finance system after each iteration using Full Fog Path
Version: 1.0

Execution Mode: plan_only (no actual execution)
Validation Strategy: LENIENT (warnings only, no failures)

========================================
PLANNED STEPS
==========================================

[Step 1] Frame Problem
  Type: problem_framer skill
  Input: Repository context + validation scope
  Output: problem_frame.md
  Expected Artifacts: 1

[Step 2] Map Unknowns
  Type: unknowns_mapper skill
  Dependencies: Frame Problem
  Input: problem_frame.md
  Output: unknowns_map.md, research_paths.md
  Expected Artifacts: 2

[Step 3] Analyze Repository
  Type: repo_sensemaker skill
  Dependencies: Map Unknowns
  Input: problem_frame.md, unknowns_map.md
  Output: sensemaking_brief.md, error_analysis.md, changes_identified.md
  Comparison: Enabled (against .validation-cache/latest/)
  Output: comparison_report.md
  Expected Artifacts: 4

[Step 4] Orchestrate Fixes
  Type: workflow_orchestrator skill
  Dependencies: Analyze Repository
  Input: sensemaking_brief.md, error_analysis.md
  Output: selected_workflow.md, corrective_actions.md, next_steps.md
  Expected Artifacts: 3

========================================
EXPECTED OUTPUTS
==========================================

Reports (user-facing):
- validation_summary.md (1-page summary)
- error_comparison.md (comparison with baseline)
- changes_summary.md (summary of changes)

Evidence (detailed analysis):
- problem_frame.md (problem framing)
- unknowns_map.md (unknowns analysis)
- research_paths.md (research directions)
- sensemaking_brief.md (repository state)
- error_analysis.md (detailed errors)
- changes_identified.md (system changes)
- comparison_report.md (baseline comparison)
- selected_workflow.md (recommended workflow)
- corrective_actions.md (actions to take)
- next_steps.md (implementation plan)

Total Artifacts: 13

GitHub Issues: 0 (plan mode doesn't create issues)
Baseline Cache: Read only (plan mode doesn't update cache)

========================================
RESOURCE ESTIMATES
==========================================

Execution Time: ~5-10 minutes
Memory Usage: ~300-500 MB
Disk Space: ~2-5 MB for artifacts
Network: GitHub API calls for context (no issue creation)

========================================
CONFIGURATION
==========================================

Source: docs/workflows/validation-finance-system.yaml
Target: metamorfose-edutech (finance-system focus)
Validation Rules: strict_validation_in_execution_mode
                  separation_of_concerns
                  composition_boundaries

Exit Code: 0 (plan successful)

Use --mode guided_execution or --mode autonomous_execution to execute this plan.
```

## Decision Gate Checklist

Use this checklist at your decision gates to ensure thorough validation:

### Pre-Validation (Plan)

- [ ] **Understand scope**
  - [ ] What part of finance system changed?
  - [ ] How many files were modified?
  - [ ] Were there breaking changes?

- [ ] **Prepare environment**
  - [ ] Python 3.x is installed?
  - [ ] Required skills are available?
  - [ ] Have 500MB+ free disk space?

### During Validation

- [ ] **Monitor execution**
  - [ ] All workflow steps completed?
  - [ ] No unexpected errors?
  - [ ] Check console output for warnings?

- [ ] **Review errors**
  - [ ] Read error_analysis.md carefully
  - [ ] Understand impact of HIGH severity errors
  - [ ] Assess if errors are blockers

### Post-Validation (Triage)

- [ ] **Analyze results**
  - [ ] How many errors were found?
  - [ ] Severity breakdown: HIGH/MEDIUM/LOW?
  - [ ] Are errors new or persistent?

- [ ] **Make decision**
  - [ ] Can we merge with these errors?
  - [ ] Which errors must be fixed first?
  - [ ] Which can be tracked for later?

- [ ] **Track progress**
  - [ ] Issues created for HIGH severity?
  - [ ] Assigned to responsible team members?
  - [ ] Updated baseline for next validation?

### Post-Decision

- [ ] **Follow up**
  - [ ] Monitor ticket resolution
  - [ ] Next validation scheduled?
  - [ ] Lessons learned documented?

## Interpreting Results

### Error Severity Levels

**HIGH** (blocker):
- Causes transaction failures
- Affects data integrity
- Creates compliance risks
- Impacts multiple systems
- Action: Fix before proceeding

**MEDIUM** (important):
- Causes performance issues
- Degrades user experience
- Increases technical debt
- Requires optimization
- Action: Plan to fix soon

**LOW** (nice-to-have):
- Deprecation warnings
- Code quality improvements
- Documentation gaps
- Refactoring opportunities
- Action: Track for future work

### Comparison Report Interpretation

- **NEW**: Something broke or was changed
  - Review recent commits
  - May indicate incomplete implementation
  
- **FIXED**: Progress! Something improved
  - Celebrate the win
  - Track who fixed it
  
- **UNCHANGED**: Persistent issues
  - May indicate accepted technical debt
  - Consider prioritizing fixes
  
- **TREND**: Positive vs Degrading
  - Improving: More fixed than new ✓
  - Degrading: More new than fixed ⚠
  - Stable: Roughly equal

## Common Workflows

### "I just want to validate my changes"
```powershell
.\scripts\validate-finance-system.ps1 -Mode guided_execution
```

### "Run validation and create all tickets automatically"
```powershell
.\scripts\validate-finance-system.ps1 -Mode autonomous_execution -CreateTickets
```

### "Compare current state to last validation"
```powershell
.\scripts\validate-finance-system.ps1 -Mode guided_execution -CompareBaseline
```

### "Preview what validation will do"
```powershell
.\scripts\validate-finance-system.ps1 -Mode plan_only
```

### "In CI/CD, validate with tickets and baseline"
```powershell
.\scripts\validate-finance-system.ps1 -Mode autonomous_execution -CompareBaseline -CreateTickets
```
