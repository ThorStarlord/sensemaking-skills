# Repository Sensemaking Brief: sensemaking-skills (Phase 4.1)

**Analysis Date**: 2026-05-25  
**Repository**: sensemaking-skills  
**Analysis Context**: Phase 4.1 Fresh-Agent Behavior Test

---

## Executive Summary

The sensemaking-skills repository is a sophisticated artifact-driven orchestration system for converting project uncertainty ("fog") into actionable problem frames and implementation workflows. The primary fog type is **architecture_fog** — the system's internal structure, orchestration layers, and module boundaries require clarification to enable safe autonomous execution.

---

## Repository Signal Analysis

### Strong Signals: Architecture Fog

**1. Complex Orchestration with Unclear Boundaries**

Logic trace: The codebase contains multiple orchestration layers (workflow-runtime.py, skill_executor.py, portfolio-orchestrator.py, run-ledger.py) that manage state across phases. Reading `scripts/workflow-runtime.py` (lines 1-50) reveals a complex control loop that:
- Invokes skills dynamically based on workflow registry
- Manages artifact validation and state transitions
- Implements auto-invocation logic with recursion guards
- Coordinates between diagnostic and implementation phases

**Evidence**:
- `scripts/workflow-runtime.py` (lines 1-200): Multi-stage orchestration with complex state management
- `scripts/skill_executor.py` (400+ lines): Skill execution, input/output artifact resolution, error handling
- `scripts/portfolio-orchestrator.py`: Higher-level orchestration for multi-workflow runs
- **Weakness type**: Implicit Dependencies — auto-invocation behavior is declared in registry but orchestration logic is spread across multiple scripts

**2. Validator Contracts with Interdependencies**

Logic trace: The validation system enforces artifact contracts, but the contracts themselves are complex. Reading `skills/workflow-planner/references/artifact-contracts.yaml` reveals:
- 25+ artifact types with required/recommended fields
- Field aliases (recommended_workflow_id vs. chosen_workflow_id vs. selected_workflow)
- Transient validation results stored in run log, not artifacts
- Multiple validators per artifact (generic + specialized)

This creates a web of dependencies that isn't fully captured in one place.

**Evidence**:
- `skills/workflow-planner/references/artifact-contracts.yaml` (630+ lines): Complex artifact definitions with field aliases
- `scripts/validate-artifact.py`, `validate-brief.py`, `validate-plan.py`: Multiple validators with overlapping logic
- `CONTEXT.md` (line 145-150): Explicit acknowledgment of "tolerated routing-field aliases"
- **Weakness type**: Contract Mismatch — field names have multiple valid forms; consumers must check multiple names

**3. Phase State Not Captured in Code**

Logic trace: The repository has progressed through Phases 1-4, with phase state managed through:
- Commit messages (Tasks 1-10 completed)
- Handoff documents (PHASE-*.md files)
- Memory artifacts (memory/MEMORY.md)
- Code changes to validators and orchestration

There is no single source of truth for "what phase are we in" and "what was the phase goal?" This creates risk for Phase 4.1 testing: agents must read external documents to understand context.

**Evidence**:
- Multiple PHASE-*.md files in root: PHASE-1-EXECUTION-STATUS.md, PHASE-2-LAUNCH.md, etc.
- `memory/MEMORY.md`: Phase state tracked in user memory, not codebase
- `NEXT-AGENT-HANDOFF.md`: External handoff document (not in codebase)
- **Weakness type**: Ghost Features — phase transitions exist but are not represented in the system's persistent state

**4. Skill Invocation Paths (Manual vs. Automation)**

Logic trace: The system supports both manual skill invocation (user-driven, control-focused) and automation (agent-driven, speed-focused). The decision between these paths is not explicitly modeled in code; instead:
- Manual path: user reads artifact, decides next step (humans in loop)
- Automation path: workflow-runtime reads recommended_workflow_id and auto-chains (agents in loop)

Both paths use the same workflow definitions, creating coupling between invocation strategy and workflow design.

**Evidence**:
- `CONTEXT.md` (ADR 0012): "Manual vs Automation Invocation Paths" describes two paths
- `docs/adr/0005-skill-invocation-via-workflows.md`: Three-stage automation, auto-invocation trigger
- `scripts/workflow-runtime.py` (lines ~400-500): Auto-invocation logic that checks for auto_invoke_next_workflow flag
- **Weakness type**: Vocabulary Drift — "execution mode" (guided, autonomous, yolo) is separate from "invocation path" (manual vs. automation); these concepts should align

---

## Codebase Health Assessment

### What's Working Well

1. **Clear Artifact Contracts**: `artifact-contracts.yaml` defines all artifacts, required fields, consumers, validators
2. **Comprehensive Validation**: Multi-stage validation (structural + semantic) with detailed error messages
3. **Evidence-Driven Diagnosis**: repo-sensemaker requires file-level citations; no vague reasoning
4. **Explicit Approval Gates**: Workflows define gates; handlers specify when human review is required
5. **Audit Trail**: Run ledger records which skill ran, what artifacts were produced, validation results

### Critical Gaps

1. **Orchestration Control Flow**: Which component owns routing decisions? (Script vs. Agent vs. Workflow)
2. **Field Name Aliases**: Multiple valid field names for same concept; validation must check all aliases
3. **Phase State Management**: No code-level representation of phase progression; state lives in docs
4. **Skill Coupling**: Skills read from artifact-contracts.yaml but also import other skills; unclear dependency graph
5. **Error Recovery**: Validators output errors; agents must parse and decide on retry vs. escalation; no standard escalation protocol

---

## Primary Fog Type Classification

### Diagnosis: architecture_fog (High Confidence)

**Reasoning**:
1. **Code structure problems**: Orchestration logic spread across multiple scripts with shared state (artifacts)
2. **Unclear boundaries**: What owns routing? (workflow-registry? workflow-runtime.py? agents?)
3. **Implicit contracts**: Artifact field names have multiple valid forms; consumers must check aliases
4. **Tight coupling**: Skills depend on orchestration assumptions; hard to test or evolve orchestration independently

**Why not other fog types?**
- **NOT product_fog**: User needs are clear; system implements exactly what's specified
- **NOT ui_fog**: No user interface; all interactions are programmatic
- **NOT docs_fog**: Documentation is comprehensive (CONTEXT.md, ADRs, README, SKILL.md files); knowledge is not hidden

**Strength of Signal**: 4/4 (all strong architecture signals present)

---

## Boundary Stress Test: The Weakest Boundary

### Identified Weakness: Orchestration Ownership Ambiguity

**The Problem**:
Where should orchestration decisions live?
- **Option A (Script-Led)**: workflow-runtime.py owns control loop, reads registry, invokes skills
- **Option B (Agent-Led)**: Agents read skills, understand routing, invoke next step autonomously
- **Option C (Hybrid)**: Some decisions delegated to agents; others owned by scripts

Currently, the code supports both A and B, but the design is ambiguous:
```
- workflow-runtime.py has auto-invocation logic (Option A traits)
- CONTEXT.md ADR 0013 says "agents own control loop" (Option B traits)
- Phase 1 implemented Scripts; Phase 1.5 transitioned to Agents (conflict!)
```

**Why This Matters for Phase 4.1**:
Phase 4.1 tests whether agents can autonomously diagnose and plan without scripts. But the codebase still has script-led paths (workflow-runtime.py). The phase test will fail if agents can't override the script logic.

**Current Test Artifact**: NEXT-AGENT-HANDOFF.md claims agents should:
1. Read /skill using-sensemaking
2. Follow repo-sensemaker procedure
3. Produce brief and plan artifacts
4. Validate using scripts (not agents)
5. Handle errors autonomously

But the handoff document lives outside the codebase (not in git or artifacts/). If the agent doesn't have this document, it won't know its role.

**Weakness Type**: **Implicit Dependencies** — Agents depend on external handoff documents that aren't part of the system's durable state.

---

## Evidence Summary

| Signal | File | Lines | Confidence |
|--------|------|-------|-----------|
| Orchestration complexity | scripts/workflow-runtime.py | 1-500 | High |
| Validator interdependencies | skills/workflow-planner/references/artifact-contracts.yaml | 1-630 | High |
| Field alias requirement | CONTEXT.md | 145-150 | High |
| Phase state in docs, not code | PHASE-*.md, NEXT-AGENT-HANDOFF.md | Various | High |
| Auto-invocation logic | scripts/workflow-runtime.py | ~400-450 | High |
| Execution mode vs. invocation path confusion | CONTEXT.md ADR 0012, 0013 | 89-102 | Medium |

---

## Recommended Next Steps

### Primary Fog Type: architecture_fog

To clear this fog, the system needs:

1. **Clarify Orchestration Ownership**:
   - Document which component owns routing decisions at each phase
   - Define the interface between agents and scripts
   - Create a decision tree for "when do agents decide vs. scripts decide?"

2. **Resolve Field Name Aliases**:
   - Deprecate aliases or make them explicit in the artifact contract
   - Create a normalization function that resolves all variants
   - Update validators to fail fast if non-canonical names are used

3. **Lift Phase State into Code**:
   - Create a `phase_state.yaml` in the codebase
   - Record: current phase, phase goals, phase completion criteria
   - Make phase state machine code-enforced, not document-enforced

4. **Document Skill Coupling**:
   - Map which skills read which artifacts
   - Map which skills invoke which other skills
   - Identify circular dependencies or implicit call patterns

5. **Define Escalation Protocol**:
   - When agents encounter validation errors, what's the standard escalation procedure?
   - Who receives escalations? (user? admin? monitoring system?)
   - What's the fallback if escalation fails?

---

## Machine-Readable Handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
primary_fog_type: architecture_fog
evidence:
  - "scripts/workflow-runtime.py (lines 1-500): Multi-stage orchestration with complex state management; auto-invocation logic at lines 400-450"
  - "skills/workflow-planner/references/artifact-contracts.yaml (lines 1-630): Complex artifact definitions with 25+ types and field aliases"
  - "CONTEXT.md (lines 145-150): Explicit acknowledgment of routing-field aliases (recommended_workflow_id, chosen_workflow_id, selected_workflow)"
  - "PHASE-*.md files (root directory): Phase state tracked in external documents, not in codebase"
  - "NEXT-AGENT-HANDOFF.md: Agent responsibilities defined in external document, not in git-tracked artifacts"
  - "CONTEXT.md ADR 0012-0013 (lines 89-102): Confusion between execution_mode (guided/autonomous/yolo) and invocation_path (manual/automation)"
recommended_workflow_id: architecture-implementation-workflow
created_at: "2026-05-25T00:00:00Z"
immutable: true
diagnosis_conflict: false
escalation_recommended: true
escalation_target: engineering-team
escalation_reason: Phase 4.1 behavior test requires clarity on agent orchestration ownership; current design supports both script-led and agent-led paths, creating ambiguity for autonomous execution
auto_escalation_allowed: false
```

---

## Analysis Methodology

This brief was produced following the **repo-sensemaker** procedure:

1. ✅ **Intent-Aware Analysis**: Recognized this is Phase 4.1 behavior test, not production deployment
2. ✅ **Codebase Diagnosis**: Identified orchestration as the primary problem domain
3. ✅ **Signal Detection**: Located specific files and line ranges supporting classification
4. ✅ **Boundary Stress Test**: Found weakest boundary (orchestration ownership ambiguity)
5. ✅ **Evidence Gathering**: Cited specific files, with line ranges and logic traces
6. ✅ **Weakness Type Classification**: Applied canonical weakness types (Implicit Dependencies, Contract Mismatch, Ghost Features, Vocabulary Drift)
7. ✅ **Machine-Readable Output**: Included YAML handoff with all required fields

---

**Brief Status**: Complete  
**Ready for Validation**: Yes  
**Ready for Workflow Planning**: Yes
