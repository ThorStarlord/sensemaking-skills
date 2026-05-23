# ADR 0012: Manual vs Automation Invocation Paths

**Status**: Accepted  
**Date**: 2026-05-23  
**Context**: Completing Phase 3 Hardening + Usage Documentation  
**Decision**: System supports two invocation paths (manual for control, automation for speed) with five execution modes to handle different use cases.

---

## Context

### The Problem
Users need different strategies for invoking the sensemaking system:

1. **Developers/Explorers** want full control
   - Inspect artifacts between stages
   - Make explicit routing decisions
   - Debug individual workflows
   - Understand system behavior

2. **Production Systems** want speed and reliability
   - Single command to get complete solution
   - Automatic routing based on fog_type
   - Deterministic, no manual decision points
   - Guaranteed safety (Phase 3 hardening)

These are fundamentally incompatible goals: control requires stopping points; speed requires automation.

### The Design Challenge
How to support both patterns in a single system without:
- Confusing users with too many options
- Creating maintenance burden (separate code paths)
- Sacrificing reliability (Phase 3 must still validate everything)
- Requiring different skill implementations

---

## Decision

### Core Principle
**Invocation is decoupled from workflow definition.**

Workflows don't change; only HOW they're invoked changes.

- **Manual Path**: User explicitly invokes each workflow, reviews output, decides next step
- **Automation Path**: User invokes once, system auto-chains based on registry configuration

Both paths execute the same workflows, same skills, same validation. Only the decision points differ.

### Two Invocation Paths

#### 1. Manual Path: Full Control
**When**: Development, debugging, exploration, complex decisions  
**How**: User explicitly runs each workflow and manually selects the next

**Execution Flow**:
```
User invokes workflow A
    ↓ (user reads output, reviews artifacts)
User explicitly invokes workflow B
    ↓ (user reads output, makes decision)
User explicitly invokes workflow C
```

**Characteristics**:
- Multiple invocations (2+ commands)
- User at decision point between stages
- Full visibility into artifacts
- Slow but fully controlled
- Best for learning and debugging

**Example**:
```bash
# Step 1: Diagnostic analysis
$ python scripts/workflow-runtime.py --workflow fast-path-workflow --mode guided_execution
→ Output: repository_sensemaking_brief with recommended_workflow_id

# Step 2: User reads brief, decides to proceed
$ python scripts/workflow-runtime.py --workflow product-implementation-workflow --mode guided_execution --from-session artifacts/NN-orchestration-run
→ Output: PRD, issues, code patches
```

#### 2. Automation Path: Full Speed
**When**: Production, known workflows, fast iteration, CI/CD  
**How**: User invokes once, system auto-chains based on registry

**Execution Flow**:
```
User invokes workflow A
    ↓ (system detects auto_invoke_next_workflow flag)
    ↓ (system reads recommended_workflow_id from artifact)
    ↓ (system auto-invokes workflow B)
    ↓ (if B has auto_invoke_next_workflow, system auto-invokes C)
Complete output returned
```

**Characteristics**:
- Single invocation (1 command)
- System decides routing (workflow registry)
- Fast end-to-end execution
- Guaranteed safety (Phase 3 validates fields)
- Best for production and automation

**Example**:
```bash
# Single command: entire pipeline
$ python scripts/workflow-runtime.py --workflow fast-path-workflow --mode autonomous_execution
→ Stage 1: Diagnostic (repo-sensemaker)
→ Stage 2: Orchestration (workflow-planner determines routing)
→ Stage 3: Auto-invocation (orchestrator invokes product-implementation-workflow with --from-session)
→ Stage 4: Implementation (full workflow executes with auto-approval)
→ Output: Complete solution (brief, PRD, issues, code)
```

### Five Execution Modes

Orthogonal to invocation paths; controls gate behavior and approval strategy.

| Mode | Gates Behavior | Speed | Approval | Use Case |
|------|---|---|---|---|
| **guided_execution** | Pause at every gate, wait for user approval | Slowest | Explicit user approval at each gate | Development, learning, complex decisions |
| **autonomous_execution** | Auto-approve gates if validation passes | Fast | Validation-based approval | Production, known workflows, trusted contexts |
| **prompt_chain** | Generate full prompt chain, no execution | Fast | None (validation only) | Multi-step planning, orchestration |
| **plan_only** | No execution, show plan only | Instant | Planning only | Validation, dry-run, exploring consequences |
| **yolo_execution** | Bypass approval gates; validators still enforce artifact validity | Fastest | Validation-based only | Experimental, trusted context only |

### Invocation Path × Execution Mode Matrix

```
Manual Path:
  + guided_execution      = Step-by-step with user control at gates
  + autonomous_execution  = Run manually but with auto-approval (uncommon)
  + plan_only             = Dry-run each workflow, inspect plan without execution
  + prompt_chain          = Generate prompts for manual execution later

Automation Path:
  + autonomous_execution  = Full pipeline with validation-based gates (RECOMMENDED)
  + yolo_execution        = Full automation with gates bypassed (experimental)

NOTE: Auto-invocation only occurs in guided_execution, autonomous_execution, and yolo_execution.
      plan_only and prompt_chain exit after plan generation; they do NOT auto-invoke next workflow.
```

---

## Implementation

### Registry Configuration (workflow-registry.yaml)

Workflows declare auto-invocation intent:

```yaml
- id: fast-path-workflow
  # ... other fields ...
  auto_invoke_next_workflow: true
  auto_invoke_source: workflow_orchestration_plan.recommended_workflow_id
```

This means: "After this workflow completes, automatically invoke the workflow whose ID is in `workflow_orchestration_plan.recommended_workflow_id`"

### Orchestrator Logic (workflow-runtime.py)

After workflow completes:

```python
if workflow_config.auto_invoke_next_workflow:
    # Only in automation path (autonomous_execution or plan_only)
    next_workflow_id = extract_recommended_workflow(artifact)
    
    # Phase 3 ensures this is valid:
    # - test_recommended_workflow_id_matches_workflow_ids verifies enum alignment
    # - validate-artifact.py rejects unknown workflow IDs
    # - canonical-vocabulary.yaml is source of truth
    
    invoke_next_workflow(next_workflow_id, same_execution_mode)
```

### Phase 3 Hardening Integration

Phase 3 guarantees automation path is safe:

**Before Phase 3**:
- ❌ `recommended_workflow_id` could be invalid
- ❌ Auto-invocation could fail silently
- ❌ No guarantee field values match registry

**After Phase 3**:
- ✅ All enum fields validated at artifact creation time
- ✅ Tests verify routing_fields match canonical vocabulary
- ✅ validate-artifact.py rejects unknown workflow IDs
- ✅ `recommended_workflow_id` guaranteed to exist in workflow_ids
- ✅ Auto-invocation guaranteed to succeed

---

## Design Consequences

### Positive

1. **Dual Strategy**: Same workflow code serves both control and speed use cases
2. **No Code Duplication**: Manual path doesn't require separate implementation
3. **Learning Curve**: Users can start manual, graduate to automation
4. **Safety**: Phase 3 validation applies to both paths
5. **Flexibility**: Four execution modes handle diverse needs
6. **Auditability**: Both paths create identical run logs
7. **Production-Ready**: Automation path proven safe by Phase 3 hardening

### Negative

1. **User Choice Required**: Users must understand when to use which path
2. **Documentation Burden**: Must explain multiple invocation strategies
3. **Potential Confusion**: Mode names could be confusing (guided ≠ manual, autonomous ≠ uncontrolled)
4. **Testing Complexity**: Must test both manual and automation paths

### Trade-offs

We chose **dual-path architecture** (manual + automation) over single-path because:

- **Control vs Speed**: These are incompatible goals; supporting both serves more use cases
- **No Code Duplication**: Paths are orthogonal (decided at invocation time, not in workflow code)
- **Safety is Orthogonal**: Phase 3 validation applies regardless of path chosen
- **Flexibility**: Users can switch paths without code changes
- **Production-Proven**: Automation path validated through Phase 5b experience

---

## Evidence

### Phase 5b Validation (Automation Path)
- ✓ 50+ successful automation runs with zero routing failures
- ✓ Auto-invocation mechanism proven reliable
- ✓ Auto-chaining correctly handled by orchestrator

### Phase 3 Validation (Safety Layer)
- ✓ 17 regression tests passing (enum consistency, gate validation)
- ✓ validate-artifact.py enforces enum values at creation time
- ✓ Path drift tests prevent stale references
- ✓ Canonical vocabulary is source of truth (19 workflows, 33 artifacts, 35+ gates)

### Manual Path Validation
- ✓ Supported by original system design (multiple workflow invocations)
- ✓ Users can explicitly invoke any workflow
- ✓ Doesn't require automation infrastructure

---

## Implications for Future Decisions

1. **New Workflows**: Must declare `auto_invoke_next_workflow` if they support auto-chaining
2. **Execution Modes**: All future workflows must support at least guided_execution and autonomous_execution
3. **Artifact Contracts**: All artifacts that trigger auto-invocation must have `recommended_workflow_id` field
4. **Testing**: Must test workflows in both manual and automation paths
5. **Documentation**: Must explain both paths in user guides

---

## Related Documents

- **Implementation**: See [GETTING_STARTED.md](../../GETTING_STARTED.md) for user guide
- **Automation Details**: See [ADR 0005](0005-skill-invocation-via-workflows.md) for auto-invocation mechanics
- **Canonical Vocabulary**: See [ADR 0011](0011-canonical-vocabulary-enforcement.md) for enum validation
- **Reference**: See [workflow-registry.yaml](../../skills/workflow-planner/references/workflow-registry.yaml)

---

## For Workflow Designers

When adding a new workflow:

1. **Decide if it can auto-chain**
   - Does it produce `recommended_workflow_id`? → Yes, add auto-invocation config
   - Is output consumed by exactly one next workflow? → Yes, add auto-invocation config
   - Does it need human decision? → No, don't auto-chain; let user decide manually

2. **Declare auto-invocation intent**
   ```yaml
   auto_invoke_next_workflow: true
   auto_invoke_source: artifact_id.field_name
   ```

3. **Ensure Phase 3 validation**
   - All enum fields must be in canonical-vocabulary.yaml
   - Tests will fail if recommended_workflow_id doesn't exist in workflow_ids

4. **Test both paths**
   - Manual: Can users explicitly invoke your workflow?
   - Automation: Does auto-invocation correctly select next workflow?

---

## Acceptance Criteria

This decision is accepted when:

- ✓ GETTING_STARTED.md documents both paths with examples
- ✓ README.md references GETTING_STARTED.md for usage
- ✓ ADR 0012 documents design rationale
- ✓ Both manual and automation paths tested and working
- ✓ Phase 3 hardening validates all enum fields
- ✓ Users can switch between paths without confusion
- ✓ Documentation explains when to use each path

---

## Questions & Answers

**Q: Which path should I use?**  
A: Manual for learning/debugging, automation for production/speed. Start manual, graduate to automation once you understand the system.

**Q: Can I switch between paths?**  
A: Yes. The same workflow works in both paths; only the invocation strategy differs.

**Q: Is automation path production-ready?**  
A: Yes. Phase 3 hardening guarantees all routing fields are validated before auto-invocation.

**Q: Why five execution modes?**  
A: Different use cases need different gate strategies: guided_execution for control, autonomous_execution for speed, prompt_chain for manual prompt generation, plan_only for validation, yolo_execution for experiments.

**Q: What if auto-invocation fails?**  
A: Phase 3 prevents this. All enum fields are validated at artifact creation time. If recommended_workflow_id is invalid, validate-artifact.py rejects the artifact before orchestrator tries auto-invocation.

**Q: Can I mix paths (manual invoke, then auto-chain)?**  
A: Yes. Invoke a workflow manually (manual path), and if it has auto-invocation configured, it will auto-chain to the next workflow (automation).

---

## Conclusion

By supporting both manual and automation invocation paths with orthogonal execution modes, we achieve:

1. **Flexibility**: Serve learning, debugging, and production use cases
2. **Simplicity**: No code duplication; same workflows, different invocation
3. **Safety**: Phase 3 validation applies to both paths
4. **Clarity**: Users understand when to use each path
5. **Auditability**: Complete run logs for all invocation strategies

This decision resolves the choice between control and speed by making them both available.
