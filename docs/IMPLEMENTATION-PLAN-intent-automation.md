# Implementation Plan: User Intent Automation System

**Status**: Ready to Execute  
**Date**: 2026-05-19  
**Scope**: Five phases to add durable user intent artifact and soft-context routing to orchestration runner  
**Dependencies**: ADR 0006, ADR 0007, ADR 0008, updated CONTEXT.md  

---

## Overview

This plan adds user intent as a first-class durable artifact and integrates soft-context routing into the workflow orchestrator. Execution flows from diagnostic input → intent artifact → routing decision → implementation, with every divergence recorded and auditable.

**Success Criteria:**
- [ ] `orchestration-runner.py` accepts no-args, `--problem`, and `--workflow` flags
- [ ] `00-user-intent.md` is created for every run
- [ ] `source_intent_ref` propagates through diagnostic artifacts (brief, plan)
- [ ] Orchestration plan records `system_recommended_workflow` vs `selected_workflow` separately
- [ ] Validators check intent artifact structure and reference integrity
- [ ] Documentation and code are aligned (no drift)

---

## Phase 0: Align Plan Schema (Preparatory)

**Objective**: Ensure `validate-plan.py` and `orchestration-runner.py` agree on orchestration-plan format before adding intent routing fields.

**Current State**: Plan output from runner may not match validator expectations (Section 11 format mismatch noted during grilling).

### Changes

#### 0.1 — Verify Plan Format Consistency
- [ ] Read `orchestration-runner.py` (orchestration-plan generation)
- [ ] Read `validate-plan.py` (orchestration-plan validation)
- [ ] Identify format divergence (YAML block vs. Section 11 format)
- [ ] Document findings in `docs/PLAN-SCHEMA-ALIGNMENT.md`

#### 0.2 — Align `initial_inputs` Schema
- [ ] Current: `initial_inputs` is a flat mapping (e.g., `repository_state: <path>`)
- [ ] Expected by validator: list of objects with `id`, `type`, `required` fields
- [ ] Update runner to generate validator-compatible format
- [ ] Update `validate-plan.py` to accept both formats (backward compat) or standardize on one

#### 0.3 — Add `orchestration-plan` to `artifact-contracts.yaml` if missing
- [ ] Verify `orchestration-plan` has a contract entry in `artifact-contracts.yaml`
- [ ] Ensure required sections and machine fields are documented
- [ ] Add new fields: `intent_ref`, `routing_divergence`, `system_recommended_workflow`, `selected_workflow`, `routing_decision_method`

### Validation
```bash
# Run this after changes:
python scripts/validate-plan.py artifacts/*/04-*.md
```

**Owner**: (Implementation phase)  
**Effort**: 1–2 hours (investigation + alignment)

---

## Phase 1: Add User Intent Artifact Contract

**Objective**: Register `user_intent` as a first-class durable artifact in the system.

### Changes

#### 1.1 — Add `user_intent` contract to `artifact-contracts.yaml`

```yaml
- id: user_intent
  produced_by: orchestration-runner
  consumed_by:
    - problem-framer
    - unknowns-mapper
    - repo-sensemaker
    - workflow-orchestrator
    - docs-aligner
    - to-prd
    - to-issues
    - triage
    - handoff
  required_sections:
    - raw_intent
    - scope_mode
    - intent_source
    - constraints
    - non_goals
    - machine_readable_intent
  required_machine_fields:
    - artifact_id: user_intent
    - intent_source: user_problem_statement | repo_inferred | imported_ticket
    - scope_mode: soft | hard | advisory
    - raw_problem_statement: string | null
    - created_at: ISO 8601 timestamp
    - immutable: true
  verification:
    generic_validator: "python scripts/validate-artifact.py user_intent {artifact_path}"
    specialized_validators:
      - "python scripts/validate-user-intent.py {artifact_path}"
```

#### 1.2 — Create `scripts/validate-user-intent.py`

Validator checks:
- Required fields present and typed correctly
- `intent_source` is one of allowed values
- `scope_mode` is one of allowed values
- If `raw_problem_statement` is null, `intent_source` must be `repo_inferred`
- If `raw_problem_statement` is not null, `intent_source` should not be `repo_inferred`
- `created_at` is valid ISO 8601 timestamp
- `immutable: true` is present (fail if false)
- No syntax errors in YAML block

Template:
```python
#!/usr/bin/env python3
"""Validates user_intent artifact structure and field types."""
import sys
import yaml
from pathlib import Path
from _validator_utils import load_artifact, report_error, report_ok

def validate_user_intent(artifact_path):
    """Validate user_intent artifact."""
    artifact = load_artifact(artifact_path)
    
    errors = []
    
    # Check required fields
    required = [
        'artifact_id', 'intent_source', 'scope_mode', 
        'raw_problem_statement', 'created_at', 'immutable'
    ]
    for field in required:
        if field not in artifact:
            errors.append(f"Missing required field: {field}")
    
    # Validate intent_source
    allowed_sources = ['user_problem_statement', 'repo_inferred', 'imported_ticket']
    if 'intent_source' in artifact and artifact['intent_source'] not in allowed_sources:
        errors.append(f"Invalid intent_source: {artifact['intent_source']}")
    
    # Validate scope_mode
    allowed_modes = ['soft', 'hard', 'advisory']
    if 'scope_mode' in artifact and artifact['scope_mode'] not in allowed_modes:
        errors.append(f"Invalid scope_mode: {artifact['scope_mode']}")
    
    # Validate problem_statement consistency
    if artifact.get('intent_source') == 'repo_inferred' and artifact.get('raw_problem_statement') is not None:
        errors.append("repo_inferred intent should have raw_problem_statement: null")
    
    if artifact.get('immutable') is not True:
        errors.append("immutable field must be true for user_intent")
    
    if errors:
        report_error(artifact_path, errors)
        return False
    
    report_ok(artifact_path, "user_intent validation passed")
    return True

if __name__ == '__main__':
    if not validate_user_intent(sys.argv[1]):
        sys.exit(1)
```

### Validation
```bash
python scripts/validate-user-intent.py artifacts/*/00-user-intent.md
```

**Owner**: (Implementation phase)  
**Effort**: 1–2 hours

---

## Phase 2: Update Orchestration Runner CLI and Intent Creation

**Objective**: Support no-args default, `--problem`, and optional problem statement; create intent artifact for every run.

### Changes

#### 2.1 — Update CLI to accept workflow and problem arguments

```bash
# Current behavior (still works):
orchestration-runner.py fast-local-diagnostic --mode guided_execution

# New behavior (Phase 2):
orchestration-runner.py                                              # Default to fast-local-diagnostic
orchestration-runner.py --problem "we need a login redesign"       # With problem statement
orchestration-runner.py "we need a login redesign"                 # Positional shorthand
orchestration-runner.py --workflow full-local-sensemaking          # Explicit workflow
orchestration-runner.py --workflow full-local-sensemaking --problem "..."  # Both
orchestration-runner.py --problem "..." --scope hard               # With scope mode
```

#### 2.2 — Update `orchestration-runner.py` argument parsing

In `main()` / CLI setup, add:
```python
parser.add_argument(
    'problem',
    nargs='?',
    default=None,
    help='Optional user problem statement or goal'
)
parser.add_argument(
    '--workflow',
    default=None,
    help='Override default workflow (e.g., full-local-sensemaking)'
)
parser.add_argument(
    '--scope',
    choices=['soft', 'hard', 'advisory'],
    default='soft',
    help='How strictly the problem statement constrains analysis'
)
```

#### 2.3 — Create intent artifact before running workflow

Add method `_create_user_intent_artifact()` to runner:

```python
def _create_user_intent_artifact(self, problem_statement, scope_mode):
    """Create 00-user-intent.md artifact."""
    
    intent_source = 'repo_inferred' if problem_statement is None else 'user_problem_statement'
    
    intent_yaml = {
        'artifact_id': 'user_intent',
        'schema_version': 1,
        'intent_source': intent_source,
        'scope_mode': scope_mode,
        'raw_problem_statement': problem_statement,
        'immutable': True,
        'created_at': datetime.utcnow().isoformat() + 'Z',
        'created_by': 'orchestration-runner',
        'repo_state_used': True,
        'constraints': [],
        'non_goals': [],
        'clarifications': []
    }
    
    # Write to artifacts/<run-number>/00-user-intent.md
    artifact_dir = self._resolve_artifact_dir()
    intent_path = artifact_dir / '00-user-intent.md'
    
    with open(intent_path, 'w') as f:
        f.write('# User Intent\n\n')
        f.write('---\n')
        yaml.dump(intent_yaml, f, default_flow_style=False)
        f.write('---\n')
    
    return intent_path
```

Call this at the start of `run()`, before invoking any workflow.

#### 2.4 — Store intent path in run context

Add to runner:
```python
self.user_intent_path = intent_path  # Available to workflows and validators
```

### Validation
```bash
# No-args:
python scripts/orchestration-runner.py --list-workflows
python scripts/orchestration-runner.py --mode plan_only

# With problem:
python scripts/orchestration-runner.py --problem "test problem" --mode plan_only

# Check artifact created:
ls -la artifacts/*/00-user-intent.md
```

**Owner**: (Implementation phase)  
**Effort**: 2–3 hours

---

## Phase 3: Update Workflow Registry and Inputs

**Objective**: Declare `user_intent` as an input to diagnostic workflows so validators know it's expected.

### Changes

#### 3.1 — Update `workflow-registry.yaml` for `fast-local-diagnostic`

```yaml
- id: fast-local-diagnostic
  purpose: Lean diagnostic workflow to identify weakest boundary
  initial_inputs:
    - id: user_intent
      type: artifact
      required: true
      description: User's problem statement and scope (created by runner)
    - id: repository_state
      type: external_context
      required: true
      description: Git repository on disk
  steps:
    # steps remain unchanged
  auto_invoke_next_workflow: true
  auto_invoke_source: workflow_orchestration_plan.recommended_workflow_id
```

#### 3.2 — Update `workflow-registry.yaml` for `full-local-sensemaking`

```yaml
- id: full-local-sensemaking
  purpose: Comprehensive diagnostic workflow for deep uncertainty
  initial_inputs:
    - id: user_intent
      type: artifact
      required: true
      description: User's problem statement and scope (created by runner)
    - id: repository_state
      type: external_context
      required: true
      description: Git repository on disk
  steps:
    # steps remain unchanged
  auto_invoke_next_workflow: true
  auto_invoke_source: workflow_orchestration_plan.recommended_workflow_id
```

#### 3.3 — Update `validate-plan.py` to check `initial_inputs` against registry

Ensure plan's `initial_inputs` matches workflow registry declaration:

```python
def validate_initial_inputs(plan, workflow_config):
    """Check that plan initial_inputs match workflow registry."""
    expected = workflow_config.get('initial_inputs', [])
    actual = plan.get('initial_inputs', {})
    
    for input_spec in expected:
        input_id = input_spec['id']
        if input_id not in actual:
            if input_spec.get('required'):
                raise ValidationError(f"Missing required input: {input_id}")
    
    return True
```

### Validation
```bash
python scripts/validate-repo.py  # Checks registry consistency
python scripts/orchestration-runner.py --list-workflows | grep initial_inputs
```

**Owner**: (Implementation phase)  
**Effort**: 1–2 hours

---

## Phase 4: Add Intent Propagation to Downstream Artifacts

**Objective**: Require `source_intent_ref` in diagnostic and implementation artifacts so intent chain is auditable.

### Changes

#### 4.1 — Add `source_intent_ref` to `artifact-contracts.yaml` for:
- `repository_sensemaking_brief`
- `workflow_orchestration_plan`
- `prd`
- `issue_list`
- `agent_brief`
- `prompt_handoff` / `session_summary`

Example:
```yaml
- id: repository_sensemaking_brief
  # ... existing fields ...
  required_machine_fields:
    # ... existing fields ...
    - source_intent_ref: path/to/user_intent.md  # ADD THIS
    - user_implied_fog_type: string | null        # ADD THIS
```

#### 4.2 — Update each artifact producer to include `source_intent_ref`

For skills that produce artifacts (repo-sensemaker, workflow-orchestrator, to-prd, to-issues, etc.):
- Accept `user_intent_path` as input or context
- Read `user_intent.md` to extract `raw_problem_statement` and `user_implied_fog_type`
- Include in output artifact:
  ```yaml
  source_intent_ref: ../../00-user-intent.md
  user_goal_preserved_as: "..."  (how this artifact honors user intent)
  ```

#### 4.3 — Update validators to check `source_intent_ref` exists and is valid

In `validate-artifact.py`:
```python
def check_required_refs(artifact, artifact_contracts):
    """Verify that artifact_type has all required_refs populated and pointing to real files."""
    contract = artifact_contracts.get(artifact['artifact_id'], {})
    required_refs = contract.get('required_refs', [])
    
    for ref_field in required_refs:
        if ref_field not in artifact:
            raise ValidationError(f"Missing required reference: {ref_field}")
        
        ref_path = artifact[ref_field]
        if not Path(ref_path).exists():
            raise ValidationError(f"Referenced file does not exist: {ref_path}")
    
    return True
```

### Validation
```bash
# After running a workflow, check intent propagation:
grep -l "source_intent_ref" artifacts/*/0*.md
# Should find references in brief, plan, and downstream artifacts
```

**Owner**: (Implementation phase)  
**Effort**: 3–4 hours (updating multiple artifact producers)

---

## Phase 5: Add Routing Decision Fields to Orchestration Plan

**Objective**: Record system recommendation vs. selected workflow, routing method, and rationale in every orchestration plan.

### Changes

#### 5.1 — Update `artifact-contracts.yaml` for `workflow_orchestration_plan`

Add required machine fields:
```yaml
required_machine_fields:
  # ... existing fields ...
  - system_recommended_workflow: string (workflow_id)
  - selected_workflow: string (workflow_id)
  - routing_divergence: boolean
  - routing_decision_method: string (diagnosis_primary_soft_context | intent_tiebreaker | user_explicit_override | approved_gate | escalation_approved)
  - routing_rationale: string (multi-line explanation)
  - fog_type_confidence: number (0.0–1.0)
  - intent_ref: string (path to user_intent.md)
  - diagnosis_conflict: boolean
  - escalation_recommended: boolean
  - auto_escalation_allowed: boolean
  - scope_expansion_requires_approval: boolean
```

#### 5.2 — Update `workflow-orchestrator` skill to populate routing fields

When the skill produces the orchestration plan, it should:
1. Read `user_intent.md` to get `user_implied_fog_type`
2. Compare with repo diagnosis (`primary_fog_type`)
3. Determine `routing_decision_method` based on:
   - High confidence (>= 0.8) → `diagnosis_primary_soft_context`
   - Low confidence (< 0.8) + matching intent → `intent_tiebreaker`
   - Explicit `--workflow` flag → `user_explicit_override`
4. Record `system_recommended_workflow` (what system would choose)
5. Record `selected_workflow` (what will actually run, accounting for overrides)
6. Calculate `routing_divergence: true` if they differ
7. Write detailed `routing_rationale` explaining the decision

#### 5.3 — Update `validate-plan.py` to check routing invariants

```python
def validate_routing_fields(plan):
    """Verify routing decision fields are consistent."""
    
    errors = []
    
    # Check required fields exist
    required = ['system_recommended_workflow', 'selected_workflow', 'routing_divergence', 'routing_decision_method']
    for field in required:
        if field not in plan:
            errors.append(f"Missing routing field: {field}")
    
    # Check divergence consistency
    diverges = plan['system_recommended_workflow'] != plan['selected_workflow']
    if diverges != plan['routing_divergence']:
        errors.append("routing_divergence must be true if system_recommended != selected")
    
    # Check routing_decision_method is valid
    allowed_methods = [
        'diagnosis_primary_soft_context',
        'intent_tiebreaker',
        'user_explicit_override',
        'approved_gate',
        'escalation_approved'
    ]
    if plan['routing_decision_method'] not in allowed_methods:
        errors.append(f"Invalid routing_decision_method: {plan['routing_decision_method']}")
    
    # Check that override is recorded if divergence exists
    if diverges and plan['routing_decision_method'] == 'diagnosis_primary_soft_context':
        errors.append("Divergence exists but routing_decision_method does not explain it")
    
    # Check escalation fields
    if plan.get('escalation_recommended'):
        if 'escalation_target' not in plan:
            errors.append("escalation_recommended: true requires escalation_target")
        if plan.get('auto_escalation_allowed') and 'escalation_trigger' not in plan:
            errors.append("auto_escalation_allowed: true requires escalation_trigger")
    
    return errors
```

#### 5.4 — Update run log format to record routing decisions

When a workflow runs, the run log should include:
```yaml
workflow_execution:
  selected_workflow: implementation-workflow
  system_recommended_workflow: architecture-workflow
  routing_divergence: false
  routing_decision_method: diagnosis_primary_soft_context
```

### Validation
```bash
# Run a workflow and check orchestration plan:
python scripts/orchestration-runner.py fast-local-diagnostic --mode plan_only
python scripts/validate-plan.py artifacts/*/04-orchestration-plan.md

# Check routing fields populated:
grep "routing_divergence\|routing_decision_method" artifacts/*/04-*.md
```

**Owner**: (Implementation phase)  
**Effort**: 3–4 hours (logic + validation)

---

## Testing Strategy

### Unit Tests
```bash
# Validate-user-intent.py
pytest tests/test_validate_user_intent.py -v

# Routing decision logic
pytest tests/test_routing_decisions.py -v
```

### Integration Tests
```bash
# Full flow: no-args → intent → diagnostic → routing
python scripts/orchestration-runner.py --mode plan_only
ls -la artifacts/*/00-user-intent.md  # Created ✓
grep "source_intent_ref" artifacts/*/03-*.md  # Propagated ✓

# With problem statement
python scripts/orchestration-runner.py --problem "test problem" --mode plan_only
grep "user_problem_statement" artifacts/*/00-user-intent.md  # Recorded ✓

# With explicit workflow override
python scripts/orchestration-runner.py --workflow full-local-sensemaking --mode plan_only
grep "routing_divergence: true" artifacts/*/04-*.md  # Recorded ✓
```

### Validator Tests
```bash
# Structural validation
python scripts/validate-artifact.py user_intent artifacts/*/00-user-intent.md
python scripts/validate-user-intent.py artifacts/*/00-user-intent.md
python scripts/validate-plan.py artifacts/*/04-*.md

# Reference integrity
python scripts/validate-output.py artifacts/*/03-*.md  # Checks source_intent_ref exists
```

---

## Rollout Order

**Week 1**: Phase 0 + Phase 1–2 (foundation + CLI)
**Week 2**: Phase 3–4 (workflow registry + propagation)
**Week 3**: Phase 5 + testing + documentation updates

---

## Rollback Plan

If a phase introduces a critical bug:
1. Revert the phase's commits
2. Re-run Phase 0 validation
3. Skip the broken phase in next iteration; schedule follow-up

---

## Success Metrics

- [ ] `orchestration-runner.py` with no args runs fast-local-diagnostic
- [ ] `--problem` and `--workflow` flags are honored
- [ ] User intent artifact is created in every run
- [ ] Validators pass for all artifact types
- [ ] Routing decisions are recorded and auditable
- [ ] Downstream artifacts reference user intent
- [ ] All existing tests still pass
- [ ] Documentation (ADRs + CONTEXT.md) is accurate and complete

---

## Questions / Open Items

1. **Workflow ID aliases**: Should we add friendly CLI aliases (`fast-path`, `full-fog`) that map to registry IDs (`fast-local-diagnostic`, `full-local-sensemaking`)? Yes (document mapping in CLI help).

2. **Intent amendments mid-workflow**: Should orchestration-runner support `00b-user-clarification.md` creation? Defer to Phase 6 (requires pause/re-plan logic).

3. **Scope mode enforcement**: Should `--scope hard` affect which validators run? Defer to Phase 6 (scope expansion logic).

4. **Testing in CI**: Should CI run integration tests for all phases? Yes; add to existing CI pipeline.

---

## Files to Create / Modify

### New Files
- `scripts/validate-user-intent.py`
- `docs/PLAN-SCHEMA-ALIGNMENT.md` (Phase 0 findings)

### Modified Files
- `artifact-contracts.yaml` (add user_intent, update plan fields)
- `orchestration-runner.py` (CLI + intent creation + registry lookups)
- `workflow-registry.yaml` (add user_intent to initial_inputs)
- `validate-plan.py` (check routing fields, initial_inputs)
- `validate-artifact.py` (check source_intent_ref)
- Skills that produce artifacts: repo-sensemaker, workflow-orchestrator, to-prd, to-issues, etc. (add intent propagation)
- `CONTEXT.md` (already updated with ADR references)
- Test files: `tests/test_validate_user_intent.py`, `tests/test_routing_decisions.py`

---

## Estimated Total Effort

- **Phase 0**: 1–2 hours
- **Phase 1**: 1–2 hours
- **Phase 2**: 2–3 hours
- **Phase 3**: 1–2 hours
- **Phase 4**: 3–4 hours
- **Phase 5**: 3–4 hours
- **Testing**: 2–3 hours
- **Documentation**: 1–2 hours

**Total**: 15–22 hours (assuming no major blockers)

---

## Dependencies & Prerequisites

- [ ] Merge/review ADR 0006, 0007, 0008
- [ ] CONTEXT.md updated with new domain terms ✓
- [ ] Existing validators and workflows are stable (no active refactoring)
- [ ] CI/test infrastructure is in place
- [ ] Team agrees on naming (workflow IDs, field names, etc.)

