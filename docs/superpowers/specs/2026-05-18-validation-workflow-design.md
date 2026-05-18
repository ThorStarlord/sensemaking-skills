# Finance System Validation Workflow Design

**Date:** 2026-05-18  
**Status:** Approved  
**Scope:** Orchestration-First validation system for metamorfose-edutech finance system  

---

## Overview

This design describes a **repeatable, three-layer validation workflow** that runs at decision gates during the finance system development cycle. The workflow uses the Full Fog Path (problem-framer → unknowns-mapper → repo-sensemaker → workflow-orchestrator) to:

- Find **new errors** introduced since the last iteration
- Identify **what changed** (improvements, regressions, fixes)
- Generate **actionable artifacts** (reports, evidence, tickets) for review

The system is designed to be:
- **Repeatable** — Same inputs produce comparable results
- **Auditable** — All decisions and evidence captured
- **Extensible** — Config-driven, no code changes needed to modify behavior
- **Integrated** — Leverages existing orchestration patterns and validators

---

## System Architecture

### High-Level Design

```
Development Iteration Complete
    ↓
Decision Gate: "We know what to build next"
    ↓
Trigger Validation Workflow
    ↓
orchestration-runner.py
├─ Loads: validation-workflow.yaml (source of truth config)
├─ Executes Full Fog Path:
│   ├─ problem_framer: Re-frame the problem with current context
│   ├─ unknowns_mapper: Map research paths and assumptions
│   ├─ repo_sensemaker: Analyze repo, compare to previous run
│   └─ workflow_orchestrator: Select corrective workflow
├─ Tracks: Evidence, decisions, artifacts
└─ Outputs: Reports, error tickets, evidence artifacts
    ↓
Three-Layer Interface:
├─ Automation: CLI script (validate-finance-system)
├─ Skill: Claude invocable skill (validate-finance-system)
└─ Documentation: Process guide
    ↓
Review & Act
└─ Use artifacts and tickets to drive next iteration
```

### Design Principles

**1. Source of Truth is Configuration**
- `validation-workflow.yaml` is the single source of truth
- Versioned, auditable, human-readable
- No code changes needed to modify workflow behavior

**2. Reuse Existing Infrastructure**
- Uses `orchestration-runner.py` (existing)
- Applies patterns documented in `docs/orchestration-patterns.md`
- Validates evidence using `scripts/validate-workflow-design.py`
- Leverages ADR decisions from `docs/adr/`

**3. Strict Validation in Execution Mode**
- Uses `guided_execution` mode (human reviews before proceeding)
- Fails fast if artifacts are missing
- Evidence is preserved at each step

**4. Comparison-First Approach**
- `repo_sensemaker` compares current analysis to previous run
- Explicitly identifies: new errors, fixed issues, regressions
- Changes become first-class output

---

## Workflow Configuration

### File Location
`docs/workflows/validation-finance-system.yaml`

### Configuration Structure

The validation workflow is defined in YAML with metadata, execution config, and Full Fog Path steps.

Key sections:
- **metadata** — Workflow name, target repo, trigger type
- **execution_config** — Mode (guided/autonomous), validation rules
- **workflow_steps** — problem_framer → unknowns_mapper → repo_sensemaker → orchestrator
- **output_artifacts** — Reports, evidence, and tickets

---

## Three Implementation Layers

### Layer 1: Automation (CLI Script)

**File:** `scripts/validate-finance-system.ps1`

**Purpose:** Repeatable CLI invocation of the validation workflow

**Usage:**
```powershell
.\scripts\validate-finance-system.ps1 -Mode guided_execution -CompareBaseline
```

**Options:**
- `-Mode {plan_only | guided_execution | autonomous_execution}`
- `-CompareBaseline` — Diff against previous run
- `-CreateTickets` — Auto-create GitHub issues for new errors
- `-Force` — Skip validation checks

### Layer 2: Skill Interface

**Name:** `validate-finance-system`

**Type:** Orchestration Skill

**Trigger:** User requests validation or mentions decision gate

**Available Actions:**
1. **validate-guided** — Guided mode, human review before fixes
2. **validate-autonomous** — Autonomous mode, auto-create tickets
3. **validate-compare** — Guided + comparison to baseline
4. **validate-plan** — Plan without executing

### Layer 3: Documentation

**File:** `docs/validation-workflow.md`

**Sections:**
- Overview and when to validate
- Running validation (step-by-step)
- Understanding results
- Troubleshooting
- Customization

---

## Baseline Cache Management

The validation workflow maintains a baseline cache for comparisons:

**Cache Location:** `.validation-cache/`

**Structure:**
```
.validation-cache/
├─ latest/                    (Symlink to most recent successful run)
│  ├─ sensemaking_brief.md
│  ├─ error_analysis.md
│  └─ changes_identified.md
├─ run-2026-05-15-143022/
├─ run-2026-05-18-091433/
└─ manifest.json             (Metadata: dates, statuses, triggers)
```

**How it works:**
1. After each successful validation run, artifacts are copied to `.validation-cache/run-{timestamp}/`
2. Symlink `latest` always points to the most recent successful run
3. `repo_sensemaker` uses `baseline_dir: ".validation-cache/latest"` for comparison
4. Manifest tracks run history for troubleshooting and metrics

---

## Success Criteria

A successful validation run produces:

✓ **problem_frame.md** — Re-framed problem with current context  
✓ **unknowns_map.md** — Research paths and assumptions  
✓ **sensemaking_brief.md** — Repository analysis from repo-sensemaker  
✓ **error_analysis.md** — New errors found, previous errors status  
✓ **changes_identified.md** — What changed since last run  
✓ **comparison_report.md** — Side-by-side with previous run  
✓ **selected_workflow.md** — Which corrective workflow was chosen  
✓ **validation_summary.md** — Executive summary for review  

And optionally:
- GitHub issues created for new errors (if --create-tickets)
- Evidence artifacts organized for handoff

---

## Integration with Existing Systems

This workflow applies existing orchestration patterns:

1. **Strict vs. Lenient Validation** (Pattern 1) — Guided execution mode uses strict validation
2. **Separation of Concerns** (Pattern 2) — Each step has single responsibility
3. **Composition** (Pattern 3) — Workflow composes existing components
4. **Evidence-First Design** (Pattern 4) — All decisions recorded in artifacts

---

## File Locations

```
docs/
├─ workflows/
│  └─ validation-finance-system.yaml          (Source of truth config)
├─ validation-workflow.md                     (Process documentation)
└─ superpowers/specs/
   └─ 2026-05-18-validation-workflow-design.md (This document)

scripts/
└─ validate-finance-system.ps1                (Automation layer)

skills/
└─ validate-finance-system/                   (Skill interface)
   ├─ manifest.yaml
   ├─ implementation.md
   └─ examples.md

outputs/
└─ validation-{timestamp}/                    (Run outputs, generated)
   ├─ problem_frame.md
   ├─ error_analysis.md
   ├─ comparison_report.md
   └─ validation_summary.md
```
