# Validation Workflow Process Documentation

## 1. Overview

The validation workflow is an automated system for verifying the integrity, consistency, and completeness of documentation and code artifacts within the sensemaking-skills project. It provides structured validation across multiple phases of development, ensuring that all deliverables meet predefined quality standards before integration into the main codebase.

The validation workflow is designed for developers and technical leads who need to ensure documentation accuracy, verify architectural decisions are properly implemented, and maintain consistency across the project's knowledge base. It produces detailed validation reports that identify gaps, inconsistencies, and actionable improvement areas.

The workflow generates four primary output files: a comprehensive validation report, a summary of issues discovered, a list of recommended actions, and evidence logs documenting all validation activities. These outputs serve as both immediate feedback for the current work and permanent records for project history and learning.

## 2. Decision Gate Checklist

Trigger validation workflow when:

- [ ] New documentation has been added to the project (guides, ADRs, architecture documents)
- [ ] Existing documentation has been modified or updated
- [ ] Phase deliverables are ready for review before merging to main branch
- [ ] Conducting regular scheduled validation runs (weekly, monthly)
- [ ] Changes affect multiple documentation sections or components
- [ ] Architecture decisions need verification against implementation
- [ ] Cross-referencing between documents needs validation
- [ ] Code examples in documentation require validation
- [ ] Links and references in documentation need checking
- [ ] Documentation consistency across similar sections needs verification

## 3. Validation Modes

### Guided Execution (30-45 minutes)

Interactive validation mode where the system prompts for inputs at key decision points. The operator reviews each validation phase before proceeding to the next stage. This mode is ideal for understanding the validation process, debugging specific issues, or conducting thorough quality reviews.

**Best for:** Initial validation setups, quality assurance reviews, learning the system

**Typical workflow:**
- Step 1: Review preparation with user confirmation
- Step 2: User provides configuration inputs
- Step 3: Validation phase-by-phase with intermediate reviews
- Step 4: Results review with actionable recommendations
- Step 5: Optional re-validation with adjustments

### Autonomous Execution (20-30 minutes)

Fully automated validation run using predefined configuration. The system executes all validation phases without waiting for user input, using default settings and previously established parameters. Results are generated automatically and stored for review.

**Best for:** Scheduled runs, CI/CD integration, batch validation operations

**Typical workflow:**
- Configuration loaded automatically
- All validation phases execute sequentially
- Results compiled and stored automatically
- Notifications sent upon completion

### Plan Only (5 minutes)

Lightweight mode that generates a validation plan without executing the actual validation. This mode shows what would be validated, which documents would be checked, and which rules would be applied. Useful for understanding scope before committing to full validation.

**Best for:** Planning, scoping work, preview of validation scope

**Typical workflow:**
- Configuration reviewed
- Validation plan generated
- Scope and estimated duration shown
- No actual validation occurs

## 4. Quick Start

**One-command quickstart:**

```bash
./run-validation.sh --mode=guided --config=default
```

This command launches the guided validation workflow with default settings, prompting you through each phase and generating complete validation reports.

**Alternative for autonomous mode:**

```bash
./run-validation.sh --mode=autonomous --config=default --quiet
```

**For plan-only mode:**

```bash
./run-validation.sh --mode=plan-only --config=default
```

## 5. Running Validation (Step-by-Step)

### Step 1: Preparation and Prerequisites

Before starting validation, verify your environment is ready:

- Ensure you are in the project root directory
- Confirm git repository is clean (no uncommitted changes in files you're validating)
- Review recent changes to understand context
- Ensure you have read access to all documentation files
- Check that `run-validation.sh` script exists and is executable

**Command:**
```bash
cd /path/to/sensemaking-skills
git status
ls -la run-validation.sh
```

### Step 2: Configure Validation Scope

Define what you want to validate and how strictly:

- Choose validation mode (guided/autonomous/plan-only)
- Select target scope: all documents, specific sections, recent changes
- Set strictness level: lenient, standard, or strict
- Specify output format: markdown, JSON, HTML
- Optional: define custom validation rules

**Command for guided mode:**
```bash
./run-validation.sh --mode=guided --scope=all --level=standard
```

### Step 3: Execute Validation Phases

The validation system runs through sequential phases:

1. **Document Structure Validation** - Verify all documents follow proper markdown structure and formatting
2. **Reference Validation** - Check all cross-references and links point to valid locations
3. **Content Consistency** - Verify terminology and patterns are used consistently
4. **Architecture Alignment** - Check that documentation aligns with actual implementation
5. **Evidence Verification** - Validate that claims in documentation are backed by evidence

Each phase generates intermediate reports. In guided mode, you review each phase before proceeding.

**Command:**
```bash
./run-validation.sh --mode=autonomous --phase=all --verbose
```

### Step 4: Review Validation Results

After validation completes, examine the output files:

- **validation-report.md** - Comprehensive findings with detailed analysis
- **validation-issues.json** - Structured list of all issues discovered
- **validation-recommendations.md** - Prioritized action items
- **validation-evidence.log** - Complete audit trail of all checks

Read through the summary section first to understand high-level findings, then drill into specific issues as needed.

### Step 5: Act on Recommendations and Re-validate

Address the most critical issues identified in validation results:

1. Fix high-priority issues (blocking document completeness)
2. Address medium-priority issues (consistency and clarity)
3. Consider low-priority suggestions (polish and optimization)
4. Re-run validation to verify fixes

**Command to re-validate after changes:**
```bash
./run-validation.sh --mode=autonomous --compare=previous
```

## 6. Understanding Results

### Output File 1: validation-report.md

**Purpose:** Comprehensive validation report with detailed findings and analysis

**Contents:**
- Executive summary with key metrics
- Detailed findings organized by validation phase
- Evidence for each finding
- Specific locations of issues in source documents
- Severity assessment for each issue
- Recommended actions with implementation guidance

**Example entry:**
```
### Missing Cross-Reference [Medium Priority]

Location: docs/architecture-decisions/phase-2-workflow-redesign.md, line 45

Issue: References "orchestration patterns" but link to docs/patterns/orchestration-patterns.md is broken.

Evidence: Target file does not exist at specified path.

Recommendation: Update link to correct location or verify if document needs to be created.
```

### Output File 2: validation-issues.json

**Purpose:** Structured data format of all issues for programmatic processing

**Structure:**
```json
{
  "validation_metadata": {
    "timestamp": "2026-05-18T14:30:00Z",
    "scope": "all_documents",
    "severity_levels": ["critical", "high", "medium", "low"]
  },
  "issues": [
    {
      "id": "doc-001",
      "type": "missing_reference",
      "severity": "medium",
      "file": "docs/architecture-decisions/phase-2.md",
      "line": 45,
      "message": "Broken link to orchestration patterns",
      "suggested_fix": "Update path or create missing document"
    }
  ],
  "summary": {
    "total_issues": 12,
    "critical": 0,
    "high": 3,
    "medium": 5,
    "low": 4
  }
}
```

### Output File 3: validation-recommendations.md

**Purpose:** Actionable recommendations prioritized by impact and effort

**Contents:**
- Quick wins (low effort, high impact)
- Critical path items (blocking other work)
- Consistency improvements
- Documentation completeness items
- Infrastructure improvements
- Implementation timeline suggestions

**Example:**
```
### Quick Wins (1-2 hours total)

1. Fix 3 broken links in Phase 2 ADR document
2. Update outdated timestamps in evidence tracking
3. Standardize heading levels in guides section

### Critical Path (blocks Phase 3 validation)

1. Complete orchestration patterns documentation
2. Add missing examples to guide templates
```

### Output File 4: validation-evidence.log

**Purpose:** Complete audit trail of validation execution

**Contents:**
- Timestamp of each validation check
- Files examined
- Rules applied
- Pass/fail results for each check
- Performance metrics
- Error logs if any

**Example:**
```
[2026-05-18 14:30:15] START: Document Structure Validation
[2026-05-18 14:30:15] CHECK: docs/patterns/orchestration-patterns.md - markdown-structure
[2026-05-18 14:30:16] PASS: All headings properly formatted
[2026-05-18 14:30:16] CHECK: docs/patterns/orchestration-patterns.md - required-sections
[2026-05-18 14:30:17] FAIL: Missing "Implementation Example" section
[2026-05-18 14:30:45] END: Document Structure Validation - 34 files checked, 2 issues found
```

## 7. Troubleshooting

### Issue 1: "Permission Denied" on run-validation.sh

**Problem:** Script is not executable

**Solution:**
```bash
chmod +x run-validation.sh
./run-validation.sh --mode=plan-only
```

**Why it happens:** Git may not preserve execute permissions when cloning. Set it explicitly and re-run.

---

### Issue 2: "File Not Found" Errors During Validation

**Problem:** Validation script cannot locate documentation files

**Solution:**
1. Verify you're in the correct project directory:
```bash
pwd
# Should output: /path/to/sensemaking-skills
```

2. Check that files actually exist:
```bash
ls -la docs/
ls -la docs/patterns/
ls -la docs/guides/
```

3. If files are in git but not on disk, check git status:
```bash
git status
git log --oneline docs/
```

**Why it happens:** Files may be ignored in .gitignore, or you may be in a different directory. Ensure documentation files are committed to git.

---

### Issue 3: "Configuration Not Found" or Invalid Config

**Problem:** Validation script cannot load configuration

**Solution:**
1. List available configurations:
```bash
ls -la config/validation/
```

2. Verify config file exists and is valid:
```bash
cat config/validation/default.yml
```

3. If using custom config, ensure path is correct:
```bash
./run-validation.sh --mode=plan-only --config=/full/path/to/config.yml
```

**Why it happens:** Config file may be in wrong location or have invalid syntax. Check file paths are absolute.

---

### Issue 4: Validation Runs but Produces No Output

**Problem:** Script completes but no result files are generated

**Solution:**
1. Check if output directory exists:
```bash
ls -la artifacts/validation/
mkdir -p artifacts/validation/
```

2. Run with verbose output to see what's happening:
```bash
./run-validation.sh --mode=guided --verbose
```

3. Check for errors in the log:
```bash
tail -50 artifacts/validation/validation-evidence.log
```

**Why it happens:** Output directory may not exist or may not have write permissions. Create directory and ensure proper permissions.

---

### Issue 5: Validation Takes Longer Than Expected

**Problem:** Autonomous mode is running slowly

**Solution:**
1. Check system resources:
```bash
# View memory and CPU usage
top
# Or on Windows:
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 5
```

2. Run with faster settings:
```bash
./run-validation.sh --mode=autonomous --threads=4 --parallel
```

3. Limit scope to reduce processing:
```bash
./run-validation.sh --mode=autonomous --scope=recent --depth=shallow
```

**Why it happens:** Large document sets or slow disks can increase validation time. Use parallel processing or limit scope for faster results.

## 8. Customization

### Customizing for Different Repositories

If running validation in a different repository with different structure:

1. **Create custom configuration file:**
```yaml
# config/validation/custom-repo.yml
project:
  name: "different-project"
  doc_root: "documentation/"  # Change from default "docs/"
  exclude_patterns:
    - "*.tmp"
    - "archive/"

validation:
  enabled_checks:
    - structure
    - references
    - consistency
    - custom_rules
```

2. **Run with custom config:**
```bash
./run-validation.sh --mode=autonomous --config=custom-repo
```

### Modifying Validation Frequency

**For weekly validation:**
```bash
# Create cron job (Linux/Mac)
0 9 * * 1 cd /path/to/project && ./run-validation.sh --mode=autonomous

# Or use scheduled task (Windows)
# Schedule at 9 AM every Monday
schtasks /create /tn "ProjectValidation" /tr "C:\path\to\run-validation.sh" /sc WEEKLY /d MON /st 09:00
```

**For daily validation:**
```bash
# Change frequency in cron/scheduled task
0 9 * * * cd /path/to/project && ./run-validation.sh --mode=autonomous
```

### Adding Custom Validation Rules

1. **Create rules file:**
```yaml
# config/validation/custom-rules.yml
custom_rules:
  - name: "Team naming convention"
    description: "Verify all team names follow convention"
    pattern: "Team [A-Z][a-z]+ [A-Z][a-z]+"
    severity: "medium"
    files: ["docs/**/*.md"]

  - name: "Evidence pattern"
    description: "Check that evidence sections contain citations"
    pattern: "## Evidence.*\\[.*\\]"
    severity: "high"
    files: ["docs/decisions/**/*.md"]
```

2. **Enable custom rules:**
```bash
./run-validation.sh --mode=autonomous --rules=custom-rules
```

## 9. FAQ

**Q: How often should I run validation?**
A: Run validation before merging to main branch, and consider weekly or monthly scheduled runs for ongoing quality assurance. Run whenever documentation scope changes significantly.

**Q: Can I run validation on just a subset of documents?**
A: Yes, use the `--scope` parameter: `./run-validation.sh --mode=autonomous --scope=docs/patterns` to validate only the patterns directory.

**Q: What should I do if validation finds hundreds of issues?**
A: Don't try to fix everything at once. Filter by severity: address critical issues first, then high-priority items. Use recommendations file to identify quick wins. Consider breaking fixes into separate work items.

**Q: Is validation required before every commit?**
A: Not every commit, but recommended before pull requests to main. Use pre-commit hooks to run plan-only mode automatically on staged changes.

**Q: How do I know if my fixes actually resolved the issues?**
A: Re-run validation with the `--compare=previous` flag to see before/after comparison. Look for reduced issue count in summary metrics.

**Q: Can validation run in CI/CD pipeline?**
A: Yes, validation is designed for CI/CD integration. Use `--mode=autonomous --quiet` for pipeline runs. Set exit codes based on severity levels to fail builds on critical issues.

**Q: What if validation reports false positives?**
A: Review the specific issue evidence in validation-evidence.log. If it's a real false positive, update validation rules or configuration to exclude that pattern. Document the exception and rationale.

## 10. Related Documentation

- **[Orchestration Patterns Guide](../patterns/orchestration-patterns.md)** - Understanding the validation orchestration system
- **[Evidence Tracking ADR](../architecture-decisions/adr-evidence-tracking.md)** - Decision record on evidence collection methodology
- **[Documentation Structure Guide](../guides/documentation-structure.md)** - How to structure documents for validation
- **[Phase Workflow Guides](../guides/)** - Phase-specific validation requirements and workflows
- **[Validation Configuration Reference](../architecture-decisions/adr-validation-configuration.md)** - Technical reference for configuration options
- **[Troubleshooting Guide](../guides/troubleshooting.md)** - Common issues and solutions across all workflows

---

**Last updated:** 2026-05-18
**Maintained by:** Project Team
**Version:** 1.0
