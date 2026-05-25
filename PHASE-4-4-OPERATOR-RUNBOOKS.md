# Phase 4.4: Operator Runbooks

**Date**: 2026-05-25  
**Purpose**: Provide operators with procedures for deploying and managing the sensemaking-skills orchestration system  
**Status**: Ready for production deployment

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Getting Started](#getting-started)
3. [Running a Diagnostic](#running-a-diagnostic)
4. [Understanding Results](#understanding-results)
5. [Troubleshooting](#troubleshooting)
6. [Escalation Procedures](#escalation-procedures)
7. [Performance Tuning](#performance-tuning)
8. [Disaster Recovery](#disaster-recovery)
9. [Monitoring and Alerting](#monitoring-and-alerting)
10. [Common Scenarios](#common-scenarios)

---

## System Overview

### What This System Does

The sensemaking-skills orchestration system automatically diagnoses repository architecture issues and produces implementation plans:

1. **Phase 1 (Agent Diagnostics)**: Analyzes repository to identify primary "fog type"
2. **Phase 2 (Orchestration)**: Maps fog type to implementation workflow
3. **Phase 3 (Workflow Execution)**: Executes workflow steps to address the issue

### The Four Fog Types

| Fog Type | Definition | Example Problem | Solution |
|----------|-----------|-----------------|----------|
| **product_fog** | Product requirements unclear | Features not spec'd | Product-implementation workflow |
| **ui_fog** | UI/UX layer confused | Components scattered | UI-implementation workflow |
| **docs_fog** | Documentation misaligned | Code docs out of sync | Docs-implementation workflow |
| **architecture_fog** | Architecture unclear | Layer boundaries fuzzy | Architecture-implementation workflow |
| **mixed_fog** | Multiple issues competing | 2+ fog types equally strong | Full-fog-workflow (comprehensive) |

### When Escalation Happens

The system escalates to `full-fog-workflow` when:
- Evidence is insufficient (<3 strong signals)
- Multiple fog types compete equally (tie)
- User intent conflicts with code signals
- System confidence is low (<50%)

---

## Getting Started

### Prerequisites

- Python 3.8+
- Repository to analyze
- ~5 minutes execution time

### Basic Usage

```bash
# 1. Invoke the diagnostic skill
/skill using-sensemaking

# 2. Read the bootstrap skill (teaches the system)
# This teaches you:
#   - What fog types are
#   - How diagnosis works
#   - What to expect from results

# 3. Follow the skill to diagnose your repo
# The skill guides you through:
#   - Reading repo-sensemaker skill
#   - Analyzing your repository
#   - Producing repository_sensemaking_brief artifact
#   - Validating the brief

# 4. Invoke orchestration planner
python3 scripts/workflow-planner.py artifacts/repository_sensemaking_brief.md \
  --output artifacts/workflow_orchestration_plan.md

# 5. Execute the plan
python3 scripts/orchestration-runner.py artifacts/workflow_orchestration_plan.md
```

### Output Files

After running the system:

```
artifacts/
├── repository_sensemaking_brief.md          (Phase 1: Diagnosis)
├── workflow_orchestration_plan.md           (Phase 2: Plan)
├── [workflow-specific artifacts]            (Phase 3: Results)
└── validation_run_log.md                    (All validation results)
```

---

## Running a Diagnostic

### Step-by-Step

#### Step 1: Prepare Environment

```bash
# Verify Python is installed
python3 --version

# Verify you have access to the repository
ls -la /path/to/repo
```

#### Step 2: Read Bootstrap Skill

```bash
# This teaches you the system
/skill using-sensemaking

# Key concepts you'll learn:
# - 4 fog types
# - 3-step diagnosis pattern
# - How to validate artifacts
# - When to escalate
```

#### Step 3: Run Phase 1 Diagnostics

```bash
# The agent reads the repo-sensemaker skill
# and follows the procedure to analyze the repo

# This produces:
artifacts/repository_sensemaking_brief.md

# The brief contains:
# - Primary fog type (product/ui/docs/architecture)
# - Evidence (file-level citations)
# - Confidence score
# - Escalation recommendation (if needed)
```

#### Step 4: Validate the Brief

```bash
# Check if the brief is valid
python3 scripts/validate-and-report.py \
  artifacts/repository_sensemaking_brief.md

# Expected output:
# {
#   "valid": true,
#   "artifact_id": "repository_sensemaking_brief",
#   "errors": [],
#   "validation_timestamp": "2026-05-25T..."
# }

# If invalid, see Troubleshooting section
```

#### Step 5: Generate Orchestration Plan

```bash
# This maps fog type to implementation workflow
python3 scripts/workflow-planner.py \
  artifacts/repository_sensemaking_brief.md \
  --output artifacts/workflow_orchestration_plan.md

# Verify success:
# "Workflow plan created: ..."
```

#### Step 6: Validate the Plan

```bash
# Check if the plan is valid and routes correctly
python3 scripts/validate-and-report.py \
  artifacts/workflow_orchestration_plan.md

# Expected output:
# {
#   "valid": true,
#   "artifact_id": "workflow_orchestration_plan",
#   "errors": [],
#   "validation_timestamp": "2026-05-25T..."
# }
```

#### Step 7: Execute the Plan

```bash
# Run the selected workflow
python3 scripts/orchestration-runner.py \
  artifacts/workflow_orchestration_plan.md

# This executes the workflow steps and produces
# domain-specific implementation artifacts
```

---

## Understanding Results

### Reading the Brief

**Section 1: Executive Summary**
- Says what the primary problem is
- Confidence level (50%-100%)

**Section 2: Evidence**
- File-level citations supporting diagnosis
- Why each file points to the fog type

**Section 3: Recommendations**
- Which workflow to use
- Whether escalation is recommended

**Example Interpretation**:

```yaml
primary_fog_type: product_fog
confidence_score: 75
evidence:
  - "src/features/payment.py: Feature without product spec"
  - "docs/README.md: Mentions features but doesn't specify them"
  - "src/models/Order.py: Domain model unclear boundaries"
recommended_workflow_id: product-implementation-workflow
escalation_recommended: false
```

**Meaning**: "This repo has 75% confidence of product-fog (unclear product requirements). Use product-implementation-workflow. No escalation needed."

### Reading the Plan

**Section 1: Brief Consumed**
- What the brief said

**Section 2: System Recommendation**
- Default workflow for this fog type

**Section 3: Workflow Selection**
- Which workflow was chosen
- Why (routing_decision_method)

**Section 4-N: Workflow Steps**
- What will happen next
- Which skill will run
- What artifacts it will produce

**Example Interpretation**:

```yaml
chosen_workflow_id: product-implementation-workflow
routing_decision_method: diagnosis_primary_soft_context
workflow_steps:
  - step 1: to-prd (write Product Requirements Document)
  - step 2: to-issues (create GitHub issues from PRD)
  - step 3: triage (prioritize issues)
```

**Meaning**: "Run product-implementation workflow. It will produce a PRD, create issues, and prioritize them."

---

## Troubleshooting

### Issue: Brief Validation Fails

**Symptom**: `"valid": false` with errors

**Diagnostic**:
```bash
# Check the error_id
python3 scripts/validate-and-report.py \
  artifacts/repository_sensemaking_brief.md | grep error_id
```

**Common Errors**:

1. **error_id**: `repository_sensemaking_brief.evidence.missing_field`
   - **Problem**: No evidence provided
   - **Solution**: Brief must have evidence array with file citations
   - **Action**: Rerun diagnostics; agent must cite evidence

2. **error_id**: `repository_sensemaking_brief.primary_fog_type.unknown_value`
   - **Problem**: Fog type is not one of the four standard types
   - **Solution**: Change to product_fog, ui_fog, docs_fog, or architecture_fog
   - **Action**: Check brief and correct the fog type manually

3. **error_id**: `repository_sensemaking_brief.recommended_workflow_id.unknown_workflow`
   - **Problem**: Workflow doesn't exist in registry
   - **Solution**: Check if workflow is registered in workflow-registry.yaml
   - **Action**: Verify workflow exists or use a valid workflow ID

**If Auto-Fix Needed**:
```bash
# Manually correct the brief
# Edit: artifacts/repository_sensemaking_brief.md
# Change the problematic field
# Re-validate: python3 scripts/validate-and-report.py ...
```

### Issue: Plan Validation Fails

**Symptom**: Routing seems wrong or semantic conflict detected

**Diagnostic**:
```bash
# Check what the error is
python3 scripts/validate-and-report.py \
  artifacts/workflow_orchestration_plan.md | grep error_id
```

**Common Errors**:

1. **error_id**: `workflow_orchestration_plan.chosen_workflow_id.semantic_conflict`
   - **Problem**: Fog type doesn't match chosen workflow
   - **Example**: product_fog shouldn't route to ui-implementation-workflow
   - **Solution**: Either change fog_type or change chosen_workflow_id
   - **Action**: Use correct mapping (see "The Four Fog Types" table)

**Auto-Fix by Setting Manual Override**:
```yaml
# In the plan YAML:
routing_decision_method: manual_override
# This signals: "I know this diverges, but I approve it"
```

### Issue: Escalation Recommended, But Not Using Full-Fog-Workflow

**Symptom**: Brief says `escalation_recommended: true`, but plan uses specific workflow

**Diagnostic**:
```bash
# Check brief
grep "escalation_recommended\|recommended_workflow_id" \
  artifacts/repository_sensemaking_brief.md

# Check plan
grep "chosen_workflow_id\|escalation" \
  artifacts/workflow_orchestration_plan.md
```

**Common Cause**: 
- Brief has `escalation_recommended: true` but didn't set `recommended_workflow_id: full-fog-workflow`
- Or the planner version is old (pre-fix)

**Solution**:
1. Verify your workflow-planner.py has the escalation fix (line 98-106)
2. If brief doesn't recommend full-fog-workflow when escalation_recommended=true, regenerate brief

### Issue: Performance is Slow (>5 seconds)

**Symptom**: Workflow-planner takes >5 seconds

**Diagnostic**:
```bash
# Measure execution time
time python3 scripts/workflow-planner.py \
  artifacts/repository_sensemaking_brief.md \
  --output artifacts/workflow_orchestration_plan.md

# Check artifact size
ls -lh artifacts/repository_sensemaking_brief.md
```

**Expected Baseline**:
- <5 KB brief: ~0.27 seconds
- 10-100 KB brief: ~0.3 seconds
- 100+ KB brief: ~0.5 seconds

**If Slower**:
1. Check if registry file is corrupted
2. Verify Python version (3.8+ required)
3. Check disk I/O performance

---

## Escalation Procedures

### When Escalation Is Recommended

The system recommends escalation when:
- Evidence count is low (<3 signals)
- Multiple fog types compete equally
- Confidence score is low (<50%)
- User intent conflicts with code signals

### What "Escalation" Means

**Escalation = Use full-fog-workflow instead of single-fog workflow**

Instead of:
- product-implementation-workflow, or
- ui-implementation-workflow, etc.

Use:
- **full-fog-workflow** (comprehensive multi-domain analysis)

### When to Escalate

**Automatic Escalation** (let the system handle it):
```yaml
# In brief:
escalation_recommended: true
recommended_workflow_id: full-fog-workflow

# The planner will automatically use full-fog-workflow
# No manual action needed
```

**Manual Escalation** (when you're not confident in the diagnosis):
```yaml
# Override the brief:
# In plan, change chosen_workflow_id to full-fog-workflow
# AND set routing_decision_method: manual_override
```

### Handling Escalation Results

When running full-fog-workflow:
1. Expect longer execution time (all 4 domains analyzed)
2. Expect more comprehensive output
3. Results will address multiple fog types
4. Use results to prioritize which domain to tackle first

**Example Output Structure** (full-fog-workflow):
```
artifacts/
├── product-domain-findings.md
├── ui-domain-findings.md
├── docs-domain-findings.md
├── architecture-domain-findings.md
└── prioritized-recommendations.md
```

---

## Performance Tuning

### Baseline Performance

Expected performance (from Phase 4.2-4.3 measurements):

```
Artifact Size   Workflow-Planner Time   Agent Diagnostics
-----------     ---------------------   -----------------
< 5 KB          0.27s                   3-5 min
5-25 KB         0.29s                   3-5 min
25-100 KB       0.31s                   3-5 min
> 100 KB        0.5s                    5-10 min (larger repo)
```

### Total Pipeline Time

```
Phase 1 (Diagnostics)        3-5 minutes   <- Mostly agent thinking time
Phase 2 (Planner)            <1 second     <- Script execution
Phase 2 (Validation)         <1 second     <- Script validation
Phase 3 (Workflow)           1-10 minutes  <- Depends on workflow
-----------                  -----------
TOTAL                        5-25 minutes
```

### Optimization Levers (If Needed)

1. **Skip validation logging** (saves <1s):
   ```bash
   # Instead of:
   python3 scripts/record-validation.py ...
   # Just check stdout
   ```

2. **Run phase 1 on subset** (if repo >5000 files):
   ```bash
   # Instead of analyzing all files:
   # Focus on: src/, docs/, key architecture files
   # Saves 1-2 minutes of agent time
   ```

3. **Cache workflow registry** (if running many analyses):
   ```bash
   # Current: loads registry for each run
   # Could: pre-load registry in memory
   # Saves: <0.1s per run
   ```

### No Optimization Needed For

- Performance is well under SLO (<5s for workflow-planner)
- Scaling is linear (no exponential blow-up)
- Memory usage is minimal

---

## Disaster Recovery

### Scenario 1: Interrupted Diagnostics

**Problem**: Agent diagnostic stopped mid-way

**Recovery**:
```bash
# The brief is incomplete/missing
# Option 1: Re-run diagnostics
/skill using-sensemaking
# ... follow procedure again ...

# Option 2: Check partial output
ls -la artifacts/repository_sensemaking_brief*
```

### Scenario 2: Corrupted Artifacts

**Problem**: Artifact file is incomplete/corrupted

**Recovery**:
```bash
# Check validity
python3 scripts/validate-and-report.py artifacts/...

# If invalid, delete and regenerate
rm artifacts/repository_sensemaking_brief.md
/skill using-sensemaking  # Re-run diagnostics
```

### Scenario 3: Plan Divergence

**Problem**: Plan disagrees with brief recommendation

**Recovery**:
```bash
# Check what happened
grep "routing_decision_method\|routing_divergence" \
  artifacts/workflow_orchestration_plan.md

# If manual_override, this is intentional (someone changed it)
# If it was auto-chosen, verify the brief's recommended_workflow_id
```

### Scenario 4: Lost validation_run_log

**Problem**: Validation log got deleted

**Recovery**:
```bash
# Regenerate by re-validating
python3 scripts/validate-and-report.py \
  artifacts/repository_sensemaking_brief.md | \
  python3 scripts/record-validation.py

python3 scripts/validate-and-report.py \
  artifacts/workflow_orchestration_plan.md | \
  python3 scripts/record-validation.py

# Log is now rebuilt
```

---

## Monitoring and Alerting

### Health Checks

Run these periodically:

```bash
# Check Python version
python3 --version

# Check registry is valid
python3 -c "import yaml; \
  yaml.safe_load(open('skills/workflow-planner/references/workflow-registry.yaml'))"

# Check validators work
python3 scripts/validate-artifact.py --help

# Quick smoke test
python3 scripts/workflow-planner.py artifacts/repository_sensemaking_brief.md \
  --output /tmp/test_plan.md && echo "OK"
```

### Key Metrics to Monitor

| Metric | Target | Warning |
|--------|--------|---------|
| Workflow-planner time | <0.5s | >2s |
| Validation time | <1s | >3s |
| Escalation rate | <20% | >50% |
| Plan success rate | 100% | <95% |

### Alerting Rules

1. **If validation fails**: Artifact may be malformed → re-run diagnostics
2. **If planner >5s**: Repo may be very large → consider subset analysis
3. **If escalation >50%**: Many repos have mixed concerns → expected
4. **If routing divergence**: Manual override in place → verify intentional

---

## Common Scenarios

### Scenario 1: "Should I use full-fog-workflow?"

**Decision Tree**:
```
Does the brief say escalation_recommended: true?
├─ YES: Use full-fog-workflow (let system handle it)
└─ NO: Stick with fog-type-specific workflow

Are you unsure about the fog type?
├─ YES: Use full-fog-workflow (comprehensive analysis)
└─ NO: Use fog-type-specific workflow

Are you seeing mixed signals (multiple fog types)?
├─ YES: Use full-fog-workflow (addresses all)
└─ NO: Use fog-type-specific workflow
```

### Scenario 2: "The brief doesn't match my expectations"

**Action**:
```
1. Check confidence_score
   ├─ <50%: System is uncertain (consider escalation)
   └─ >75%: System is confident (trust the diagnosis)

2. Read the evidence
   ├─ Do the file citations make sense?
   ├─ Are they specific enough?
   └─ Do they support the fog_type conclusion?

3. Check your intent
   ├─ Did you tell the agent what the problem is?
   ├─ Or did the agent infer it?
   └─ User intent helps choose between tied fog types

4. If still unsure: Escalate to full-fog-workflow
```

### Scenario 3: "Validation keeps failing"

**Action**:
```
1. Check the error_id from validator
   python3 scripts/validate-and-report.py artifacts/...

2. Read the suggested_fixes
   (The error message includes what to do)

3. Manually edit the artifact to fix
   vim artifacts/repository_sensemaking_brief.md

4. Re-validate
   python3 scripts/validate-and-report.py artifacts/...

5. If still failing: Delete and re-generate
   rm artifacts/repository_sensemaking_brief.md
   /skill using-sensemaking
```

---

## FAQ

**Q: Can I run this on a 10,000-file repository?**  
A: Phase 1 (agent diagnostics) might hit context limits. Recommendation: Run on subset of files (src/, key files). Phase 2-3 are unaffected by size.

**Q: What if my repository has NO fog? (perfect alignment)**  
A: The system may still identify a weak signal. If confidence is very high, any workflow will work fine. If confidence is low, escalate to full-fog.

**Q: Can I use this system interactively?**  
A: Yes. Skills support guided_execution mode where users make choices at gates. See CONTEXT.md for execution modes.

**Q: What's the cost to run this?**  
A: ~$0.005-0.010 per repository (from Phase 4.2 cost analysis). Mostly agent diagnostics.

**Q: Can I run this system in CI/CD?**  
A: Yes. Use autonomous_execution mode (agents run without human gates). Set up monitoring to catch escalations and routing issues.

**Q: What if two fog types are equally strong?**  
A: System picks one (arbitrary) and sets escalation_recommended=true. Use full-fog-workflow for comprehensive analysis.

---

## Support and Escalation

### If Something Goes Wrong

1. Check validation output: `python3 scripts/validate-and-report.py ...`
2. Read suggested_fixes from error message
3. Check this troubleshooting section
4. Check CONTEXT.md for architecture details
5. If still stuck: Review PHASE-4-3-FINDINGS.md (known issues)

### Reporting Issues

Include:
- Error message (full output)
- error_id from validator
- Repository characteristics (size, fog type)
- Steps to reproduce
- Environment (Python version, OS)

---

**Runbook Version**: 1.0  
**Last Updated**: 2026-05-25  
**Next Review**: After Phase 4.5 (Production Gate)

