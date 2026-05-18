# Validation Workflow Process Documentation

A comprehensive guide to using the validation workflow system at decision gates to ensure quality code and documentation during development iterations.

---

## 1. Overview

### What the Validation Workflow Does

The validation workflow is an automated quality-assurance system that runs at decision gates—moments when your development iteration is complete and the team has agreed on the next direction. It performs three core functions:

1. **Validates the Repository State** — Ensures code quality, documentation completeness, and artifact integrity
2. **Identifies Changes** — Reports what changed in the codebase since the last validation
3. **Produces Actionable Reports** — Generates detailed findings that inform your next development steps

### When to Use It (Decision Gates)

The validation workflow is designed to run at natural stopping points in your development process:

- **Iteration Complete**: You've finished a planned set of work
- **Team Consensus**: The team has agreed "We know what to build next"
- **Stable State**: No work-in-progress (WIP) files or incomplete tasks
- **Time Since Last Validation**: At least a few hours have passed since the previous validation run
- **PRD/Requirements Ready**: You're starting a new phase of work and want to validate your foundation

### What It Produces

Each validation run generates:

- **Summary Report** — Quick overview of findings and recommendations
- **Error Analysis** — Detailed categorization of all errors found
- **Changes Identified** — Breakdown of code and documentation changes
- **Comparison Report** (optional) — Side-by-side comparison with previous run
- **Execution Log** — Complete audit trail of what was validated and when

---

## 2. When to Validate: Decision Gate Checklist

Before running validation, verify these conditions:

- [ ] **Development iteration is complete** — You've finished a planned set of features or bug fixes
- [ ] **Team has agreed on direction** — Everyone understands what needs to be built next
- [ ] **Current state is stable** — No uncommitted WIP, no broken tests, no dangling merge conflicts
- [ ] **At least a few hours since last validation** — Avoids unnecessary repeated runs
- [ ] **Artifacts are ready for review** — PRDs, documentation, or design artifacts exist
- [ ] **No urgent hotfixes pending** — Wait until hotfixes are complete and merged

**Example decision gate moments:**
- After completing feature development (ready for testing phase)
- Before starting a new product roadmap (ready for implementation planning)
- After a major refactoring (ready for validation of new architecture)
- When onboarding new requirements (ready to assess scope and feasibility)

---

## 3. Validation Modes

The validation workflow supports three modes, each suited to different needs:

### Mode 1: Guided Execution (Recommended Default)

**When to use**: For most production work and team-driven decisions

**What happens:**
- Runs all validators step-by-step
- Pauses at each gate for human review and approval
- Shows findings and asks: "Should we proceed with the next step?"
- Creates issues automatically if you approve
- Builds an audit trail of human decisions

**Characteristics:**
- Duration: 30–45 minutes
- Gates: Mandatory human approval at each step
- Risk: Low (humans review before each action)
- Best for: Production workflows, high-stakes changes, team collaboration

**When gate decisions are made:**
- **Approve**: "Yes, these findings are correct. Proceed with next step."
- **Deny**: "No, we disagree with these findings. Investigate and rerun."
- **Modify**: "Approve with changes" (some validators allow customization)

### Mode 2: Autonomous Execution

**When to use**: For well-established processes that have proven reliable

**What happens:**
- Runs all validators automatically without pausing
- Makes gate decisions based on pre-established criteria
- Auto-creates issues for all findings
- Logs all decisions in the run log
- Still creates an audit trail (but non-human)

**Characteristics:**
- Duration: 20–30 minutes
- Gates: Automated approval based on rules
- Risk: Medium (no human review, but auditable)
- Best for: Routine validations, CI/CD pipelines, low-risk iterations

**When to use autonomous mode:**
- Validation process has been exercised many times (proven reliable)
- Automated rules are well-understood by the team
- Issues generated will be reviewed before implementation
- Time is constrained and decisions are non-controversial

### Mode 3: Plan Only (Exploration)

**When to use**: For quick previews without commitment

**What happens:**
- Shows what validation would do without executing it
- Generates the execution plan
- Lists all validators that would run
- Shows artifacts that would be generated
- Takes no actions, creates no issues, makes no changes

**Characteristics:**
- Duration: 5–10 minutes
- Gates: None (no decisions needed)
- Risk: None (read-only, no mutations)
- Best for: Exploration, planning, understanding scope

**When to use plan-only mode:**
- First time running validation (understand what it does)
- Estimating how long validation will take
- Planning work before committing to execution
- Troubleshooting issues with the workflow itself

---

## 4. Quick Start (5 Minutes)

### Prerequisites

- Working directory: Root of the repository (`"H:\GithubRepositories\sensemaking-skills"`)
- Python installed and in PATH
- All recent commits pushed to git (required for baseline comparison)

### Quickest Possible Run

```powershell
# Navigate to repo root
cd "H:\GithubRepositories\sensemaking-skills"

# Run validation in guided mode with baseline comparison (most useful)
python scripts/orchestration-runner.py docs-architecture --mode guided_execution --compare-baseline

# Or, to just preview what would happen:
python scripts/orchestration-runner.py docs-architecture --mode plan_only
```

### Expected Output

When validation succeeds, you'll see output like:

```
[Level 1] Validating repository structure...
✓ Repo structure is valid
✓ Git history is accessible

[Step 1/3] Executing: grill-with-docs
  Status: COMPLETED
  → Generated domain_alignment_findings.md

[Gate] Review findings?
  Summary: 2 improvements identified
  Approve? (yes/no): yes

[Step 2/3] Executing: to-prd
  Status: COMPLETED
  → Generated prd_from_findings.md

[VALIDATION COMPLETE]
Status: PASS
Next steps: Review artifacts/validation_summary.md
```

### After Running

1. Review the output in your terminal
2. Read `artifacts/validation_summary.md` for findings overview
3. Check `artifacts/error_analysis.md` if errors are listed
4. At each gate prompt, type `approve` or `deny`

That's it! You're now using the validation workflow.

---

## 5. Running Validation: Step-by-Step Guide

### Step 1: Prepare (Change to Repo Root)

```powershell
# Navigate to repository root
cd "H:\GithubRepositories\sensemaking-skills"

# Verify you're in the right place
pwd  # Should show: "H:\GithubRepositories\sensemaking-skills"
ls scripts/orchestration-runner.py  # Should exist
```

If you get "not found" errors, you're not in the right directory. Try:

```powershell
# Windows: Navigate from home
cd "H:\GithubRepositories\sensemaking-skills"

# Or use git to find the repo root
git rev-parse --show-toplevel
```

### Step 2: Choose Your Mode

Decide which mode fits your situation:

| Scenario | Use Mode | Time |
|----------|----------|------|
| First time running validation | `plan_only` | 5 minutes |
| Production work, team consensus | `guided_execution` | 30–45 minutes |
| Routine check, automated rules trusted | `autonomous_execution` | 20–30 minutes |
| Quick preview of what's changed | `plan_only` | 5 minutes |

### Step 3: Run the Script with Options

**Basic guided execution (most common):**

```powershell
python scripts/orchestration-runner.py docs-architecture --mode guided_execution
```

**With baseline comparison (shows what changed since last run):**

```powershell
python scripts/orchestration-runner.py docs-architecture --mode guided_execution --compare-baseline
```

**Autonomous mode (faster, less interaction):**

```powershell
python scripts/orchestration-runner.py docs-architecture --mode autonomous_execution
```

**Plan only (preview, no execution):**

```powershell
python scripts/orchestration-runner.py docs-architecture --mode plan_only
```

### Step 4: Review Output

Watch your terminal as the script runs. You'll see:

```
[Level 1] Validating repository structure...
✓ Repo structure is valid
✓ Git history is accessible

[Step 1/3] Executing: grill-with-docs
  Skill: grill-with-docs
  Input: domain_alignment_report.md
  → Generating domain_alignment_findings.md

[Gate] Review findings?
  Summary: 5 improvements identified
  Approve? (yes/no): _
```

At each gate, respond with:
- `yes` or `approve` — Continue to next step
- `no` or `deny` — Stop and review
- `show` — Display findings before deciding

### Step 5: Act on Findings

After validation completes:

1. **Read the summary**: `cat artifacts/validation_summary.md`
2. **Check for errors**: `cat artifacts/error_analysis.md` (if present)
3. **Review new issues**: Listed in the summary or created in GitHub
4. **Plan next steps**: Based on validation findings

---

## 6. Understanding Results

Each validation run produces several key output files, stored in the `artifacts/` directory. Some reports are generated for every run, while others are optional and only appear with specific flags (for example, `--compare-baseline` produces `comparison_report.md`).

### validation_summary.md (Start Here!)

**Purpose**: High-level overview of validation findings

**What it contains:**
- Execution mode and timestamp
- Overall result (PASS / FAIL / WARNINGS)
- Count of errors found, fixed, and existing
- Top 3 recommendations
- Next steps

**How to interpret:**
- **PASS**: All validators succeeded, no issues found
- **WARNINGS**: Validators found issues but they're not blockers
- **FAIL**: Critical issues that need attention before proceeding

**Example:**
```markdown
# Validation Summary — docs-architecture workflow

Run ID: 2026-05-18T14:32:00Z
Mode: guided_execution
Status: WARNINGS

## Findings
- Errors found: 2
  - 1 new: Missing ADR for workflow changes
  - 1 existing: Outdated skill registry
- Errors fixed: 0

## Recommendations
1. Create ADR-0005 documenting workflow separation pattern
2. Update skill-registry.yaml with new skill definitions
3. Schedule validation re-run after fixes

## Next Steps
- Review error_analysis.md for details
- Create GitHub issues for each finding
- Complete fixes and rerun validation
```

### error_analysis.md (Detailed Errors)

**Purpose**: Complete categorization and analysis of all errors

**What it contains:**
- Each error with its code, category, and severity
- Which validator found it
- Suggested fix
- Link to related documentation

**Note on validators**: The examples shown (like `validate-workflow-design.py`) are actual validator scripts in the `scripts/` directory. Check that directory for the complete list of available validators and their actual filenames.

**Error categories:**
- `SCHEMA_VALIDATION` — Artifact doesn't match required format
- `MISSING_ARTIFACT` — Expected file doesn't exist
- `STALE_DOCUMENTATION` — Docs are outdated
- `INCOMPLETE_REQUIREMENT` — Required section is missing
- `DESIGN_VIOLATION` — Violates established pattern
- `ARTIFACT_CHAIN_BROKEN` — Step output doesn't match next step input

**How to interpret:**
Each error lists:
- **Code**: Stable identifier (e.g., `MISSING_ADR_0005`)
- **Severity**: `critical` | `high` | `medium` | `low`
- **Validator**: Which validator found it
- **Fix**: Suggested resolution

**Example:**
```markdown
## Error: MISSING_ADR

Code: MISSING_ADR_0005
Severity: high
Validator: validate-workflow-design.py
Message: ADR for workflow separation pattern not found

Current: docs/adr/ contains ADRs 0001-0004
Expected: ADR-0005 documenting separation pattern

Fix: Create docs/adr/0005-workflow-separation.md
See: docs/orchestration-patterns.md#Pattern 2

Status: NEW (first found in this run)
```

### changes_identified.md (What Changed)

**Purpose**: Summary of codebase changes since last baseline

**What it contains:**
- Files modified, added, deleted
- Lines changed per file
- Documentation updates
- Test coverage changes
- Schema/contract changes

**How to interpret:**
- Review listed changes to ensure they're intentional
- Check if documentation was updated to match code changes
- Verify tests were added for new functionality
- Flag any unexpected changes

**Example:**
```markdown
## Changes Identified

Comparison: main branch (2026-05-17) vs. current (2026-05-18)

### Files Modified (10)
- scripts/orchestration-runner.py (+45 lines, -12 lines)
- docs/orchestration-patterns.md (+23 lines, no deletions)
- skills/workflow-orchestrator/references/workflow-registry.yaml (+8 lines)

### Files Added (2)
- docs/validation-workflow.md (NEW, 400 lines)
- tests/test_validation_workflow.py (NEW, 120 lines)

### Files Deleted (0)

### Summary
- Total files touched: 12
- Documentation updated: yes (4 files)
- Tests added: yes
- Breaking changes: none detected
```

### comparison_report.md (Optional, With --compare-baseline)

**Purpose**: Side-by-side comparison with previous validation run

**What it contains:**
- Metrics from previous run
- Metrics from current run
- What improved, what regressed
- Trends over time

**How to interpret:**
- **Improved**: Fewer errors, better coverage, more tests
- **Regressed**: More errors, lower coverage, tests removed
- **Unchanged**: Same metrics as last run
- **Trends**: Patterns over multiple runs (improving? getting worse?)

**Example:**
```markdown
## Comparison: Previous Run vs. Current

| Metric | Previous | Current | Change |
|--------|----------|---------|--------|
| Total Errors | 8 | 2 | ✓ -75% |
| Tests Passing | 42 | 45 | ✓ +3 |
| Docs Coverage | 87% | 92% | ✓ +5% |
| Artifacts Valid | 18 | 20 | ✓ +2 |

## Trend Analysis
- Error rate improving: 8 → 6 → 4 → 2
- Test coverage consistently increasing
- Documentation keeping pace with changes
```

### run_log.md (Complete Audit Trail)

**Purpose**: Detailed log of every step, validator, and decision

**What it contains:**
- Timestamp of each major event
- Which validators ran and their results
- Gate decisions and approval notes
- Errors encountered and recovery actions
- Total execution time

**How to interpret:**
- Use for debugging if something unexpected happened
- Shows which validators caught which issues
- Proves which gates approved which steps
- Useful for compliance/audit trails

---

## 7. Troubleshooting

### Problem: "Script not found"

**Error message:**
```
python: can't open file 'scripts/orchestration-runner.py': [Errno 2] No such file or directory
```

**Cause**: You're not in the repository root directory

**Solution**:
```powershell
# Navigate to the correct directory
cd "H:\GithubRepositories\sensemaking-skills"

# Verify the script exists
ls scripts/orchestration-runner.py

# If still not found, find the repo root
git rev-parse --show-toplevel
```

### Problem: "Orchestration runner failed"

**Error message:**
```
VALIDATION_FAILED: orchestration-runner encountered an error
...stderr output...
```

**Causes**:
1. Python dependencies not installed
2. Invalid YAML in workflow registry
3. Skill not found

**Solutions**:

**Check Python dependencies:**
```powershell
python -c "import yaml; import sys; print(f'Python {sys.version} OK')"
```

**Validate workflow registry:**
```powershell
python -c "import yaml; yaml.safe_load(open('skills/workflow-orchestrator/references/workflow-registry.yaml'))"
# Should print nothing if valid
```

**Check if skill exists:**
```powershell
grep -i "grill-with-docs" skills/workflow-orchestrator/references/skill-registry.yaml
# Should list the skill definition
```

### Problem: "No baseline found" (First run)

**Error message:**
```
Warning: No previous baseline found for comparison
Running in comparison mode but --compare-baseline specified
```

**Cause**: First time running validation on this machine/branch

**Solution**:
This is normal! Just means there's nothing to compare to yet.
- Run without `--compare-baseline` on first run:
  ```powershell
  python scripts/orchestration-runner.py docs-architecture --mode plan_only
  python scripts/orchestration-runner.py docs-architecture --mode guided_execution
  ```
- The second run will have a baseline for comparison

### Problem: "GitHub authentication failed"

**Error message:**
```
Error: Failed to authenticate with GitHub API
Could not create GitHub issues
```

**Cause**:
- GitHub token not set
- Token is expired
- Not connected to internet

**Solutions**:

**Set GitHub token (Windows):**
```powershell
# Option 1: Set environment variable
$env:GITHUB_TOKEN = "your_github_token_here"

# Option 2: Use GitHub CLI
gh auth login
gh auth status  # Verify
```

**Generate GitHub token:**
1. Go to https://github.com/settings/tokens
2. Create "Personal access token (classic)"
3. Scopes needed: `repo`, `workflow`
4. Copy token and set `GITHUB_TOKEN` environment variable

**Verify connection:**
```powershell
gh api user --jq '.login'
# Should print your GitHub username
```

### Problem: "Gate timed out waiting for response"

**Error message:**
```
GATE_TIMEOUT: No response to gate decision within 300 seconds
```

**Cause**: Gate was waiting for human input but timeout was reached

**Solution**:
```powershell
# When gate prompts appear, respond immediately:
# At prompt: "Approve? (yes/no): "
# Type: yes
# Press: Enter

# If you need more time to review, use --skip-gates flag
python scripts/orchestration-runner.py docs-architecture --mode autonomous_execution
```

---

## 8. Customization

### Running on Different Repositories

The validation workflow is designed for the sensemaking-skills repository but can be adapted:

```powershell
# Specify a different repo root
python scripts/orchestration-runner.py docs-architecture --mode guided_execution --repo-root "C:\other-repo"

# Must have compatible:
# - scripts/orchestration-runner.py
# - workflow-registry.yaml
# - artifact-contracts.yaml
```

### Changing Validation Frequency

By default, validation can run multiple times per day. To enforce minimum intervals:

Edit `.claude/settings.json`:
```json
{
  "validation": {
    "min_frequency_hours": 6,
    "schedule": "manual"
  }
}
```

### Modifying Workflow Configuration

To change which validators run, edit `skills/workflow-orchestrator/references/workflow-registry.yaml`:

```yaml
- id: docs-architecture
  steps:
    - skill: grill-with-docs
      validators:
        - validate-repo.py
        - validate-output.py  # Add/remove validators here
```

### Running Custom Validation Scripts

Add your own validators:

```powershell
# Create your validator
Write-Host "Creating custom validator..."
@"
#!/usr/bin/env python3
import sys
# Your validation logic
print("PASS")
sys.exit(0)
"@ | Out-File "scripts/validate-custom.py"

# Reference in workflow-registry.yaml
validators:
  - validate-custom.py
```

---

## 9. FAQ

### How long does validation take?

| Mode | Duration | Variables |
|------|----------|-----------|
| plan_only | 5–10 minutes | Network latency only |
| guided_execution | 30–45 minutes | Waiting for gate approvals |
| autonomous_execution | 20–30 minutes | Number of artifacts to validate |

Factors that affect duration:
- Number of artifacts to validate (more = longer)
- Network connectivity (GitHub API calls)
- Waiting time at gates (human decision time)
- Complexity of validations (schema checks take longer)

**Speed tips:**
- Use `plan_only` for quick previews
- Use `autonomous_execution` when gates take too long
- Pre-prepare approvals (know what you'll approve before running)

### Can I run it multiple times per day?

**Yes, but:**
- First run should be plan_only or guided_execution to understand the workflow
- Subsequent runs can be autonomous if you trust the results
- Recommend running no more than every 2-3 hours (enough time for meaningful changes)

**Scheduling:**
```powershell
# Run every 4 hours
while ($true) {
    python scripts/orchestration-runner.py docs-architecture --mode autonomous_execution
    Start-Sleep -Seconds 14400  # 4 hours in seconds
}
```

### What if I disagree with an error?

**You have two options:**

1. **Deny the gate**: At the gate prompt, type `no` to reject the validation
   - Investigate the error in error_analysis.md
   - Determine if it's a real issue or false positive
   - Fix the code or the validator rule

2. **Modify the validator**: Edit the validator rule to match your standard
   - Find the validator in `scripts/validate-*.py`
   - Adjust the rule that caught the error
   - Re-run validation

**Example:**
```powershell
# Error: "ADR file missing"
# Disagree: "We don't need an ADR for this change"

# Option 1: Tell the validator to be lenient
# Edit workflow-registry.yaml, change strictness

# Option 2: Create the ADR to satisfy the validator
# Create docs/adr/0005-something.md

# Then re-run
python scripts/orchestration-runner.py docs-architecture --mode guided_execution
```

### Can I customize the workflow?

**Yes, at several levels:**

1. **Skip gates** (autonomous mode):
   ```powershell
   --mode autonomous_execution
   ```

2. **Change validators** (edit workflow-registry.yaml):
   ```yaml
   validators:
     - validate-repo.py     # Add/remove specific validators
     - validate-custom.py
   ```

3. **Modify validation rules** (edit validator scripts):
   - Edit `scripts/validate-*.py`
   - Change error thresholds, patterns, rules
   - Test with sample artifacts first

4. **Create custom workflow** (new workflow definition):
   - Add to workflow-registry.yaml
   - Define new artifact contracts
   - Register validators

### What happens to old validation runs?

**Stored in**: `artifacts/validation_*_*.md`

**Retention**:
- Last 10 runs kept automatically
- Older runs can be archived manually
- Full audit trail in `artifacts/run_logs/`

**Cleanup:**
```powershell
# Archive old runs (older than 30 days)
Get-ChildItem artifacts/validation_*.md -OlderThan (Get-Date).AddDays(-30) | Move-Item -Destination artifacts/archive/

# Or delete permanently
Get-ChildItem artifacts/validation_*.md -OlderThan (Get-Date).AddDays(-60) | Remove-Item
```

---

## 10. Related Documentation

- **[Orchestration Patterns](orchestration-patterns.md)** — Design patterns used by the validation workflow
- **[Workflow Design Guide](workflow-design-guide.md)** — How to design new workflows
- **[Architecture Decision Records](adr/)** — Technical decisions behind the system
  - ADR-0001: Strict vs. Lenient Validation
  - ADR-0002: Workflow Separation of Concerns
  - ADR-0003: Artifact Composition Pattern
  - ADR-0004: Evidence Tracking for Trust

---

## Summary

The validation workflow is your automated quality checkpoint. Use it to:

1. **Ensure quality** at natural decision gates
2. **Catch issues early** before they compound
3. **Create audit trails** for compliance and learning
4. **Guide your next steps** with data-driven recommendations

**Most common workflow:**
1. Complete development iteration (hour of work)
2. Run `orchestration-runner.py docs-architecture --mode guided_execution --compare-baseline` (30–45 minutes)
3. Review artifacts in `artifacts/validation_summary.md` (5 minutes)
4. Approve or deny findings at gates (inline with execution)
5. Create GitHub issues from findings (automatic)
6. Use findings to plan next iteration

**Key principle**: Validation is not a gate that blocks you—it's a tool that informs you. The goal is to validate early, often, and learn from the results.
