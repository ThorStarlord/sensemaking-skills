# Stage 1 Readiness: repo-sensemaker Acceptance Criteria

**Date**: 2026-05-19  
**Status**: ✅ READY FOR IMPLEMENTATION  
**Acceptance**: 3/3 fixtures passing, validator unambiguous, fields identified

---

## What Is Stage 1?

Patch `repo-sensemaker` (the first diagnostic skill) to emit intent-aware fields.

This enables the first real feedback loop: **intent → diagnosis → routing decision**.

---

## Acceptance Criteria: 3 Passing Fixtures

All fixtures must pass `python scripts/validate-artifact.py repository_sensemaking_brief <file>` without strict mode.

### ✅ Fixture 1: Clean Intent
**File**: `examples/repo-sensemaker-fixtures/01-clean-intent.md`

**Scenario**: User intent aligns with codebase structure.

**Key Fields**:
```yaml
user_implied_fog_type: product_fog
primary_fog_type: product_fog
diagnosis_conflict: false
escalation_recommended: false
```

**Status**: [PASS] All fields present ✅

---

### ✅ Fixture 2: Conflict Case
**File**: `examples/repo-sensemaker-fixtures/02-conflict-intent.md`

**Scenario**: User wants UI redesign, but architecture issues are blocking.

**Key Fields**:
```yaml
user_implied_fog_type: ui_fog
primary_fog_type: architecture_fog
diagnosis_conflict: true
escalation_recommended: true
escalation_target: full-fog-workflow
escalation_reason: intent_diagnosis_conflict
```

**Status**: [PASS] All fields present ✅

---

### ✅ Fixture 3: Insufficient Evidence
**File**: `examples/repo-sensemaker-fixtures/03-insufficient-evidence.md`

> **Historical note (2026-09-01)**: this record documents a 2026-05-19 pass
> result under a vocabulary that no longer applies — `primary_fog_type:
> unknown` is not a canonical value under the current
> `docs/canonical-vocabulary.yaml`. See the fixture file's own historical
> banner. Not a claim about current `validate-brief.py` behavior.

**Scenario**: Repository is new/generic with no clear business context.

**Key Fields**:
```yaml
user_implied_fog_type: unknown
primary_fog_type: unknown
diagnosis_conflict: false
escalation_recommended: true
escalation_target: full-fog-workflow
escalation_reason: insufficient_evidence
```

**Status**: [PASS] All fields present ✅

---

## Fields repo-sensemaker Must Emit

### Required Fields (enforce immediately)
These fields repo-sensemaker can **reliably determine** from code analysis:

```yaml
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: product_fog | ui_fog | docs_fog | architecture_fog | unknown
primary_fog_type: product_fog | ui_fog | docs_fog | architecture_fog | mixed | unknown
diagnosis_conflict: true | false
escalation_recommended: true | false
```

### Fields to Emit But May Be Nullable
These repo-sensemaker should emit when known, but **don't penalize if null**:

```yaml
secondary_fog_type: <optional, can be null>
escalation_target: full-fog-workflow | null
escalation_reason: high_uncertainty | intent_diagnosis_conflict | insufficient_evidence | none
auto_escalation_allowed: false  # Default: users must approve
```

**Rationale**: repo-sensemaker can recommend escalation (problem detection), but workflow selection and target decision-making belong to workflow-orchestrator.

---

## Promotion Plan

### Before Implementing repo-sensemaker
1. Read this checklist
2. Review the 3 fixtures to understand expected output
3. Run fixtures through validator to see what "passing" looks like

### While Implementing
1. Emit all fields identified above
2. Test against the 3 fixtures
3. Ensure validator passes for all 3 scenarios

### After Implementation
1. Run validator in normal mode (warnings allowed):
   ```bash
   python scripts/validate-artifact.py repository_sensemaking_brief artifacts/brief.md
   # Expected: [PASS] + [OK] or [WARN] for optional fields
   ```

2. Once ready for strict validation:
   ```bash
   python scripts/validate-artifact.py repository_sensemaking_brief artifacts/brief.md --strict-recommended
   # Expected: [PASS] + [OK] (no warnings)
   ```

3. Promote fields from `recommended` → `required` in artifact-contracts.yaml:
   ```yaml
   required_machine_fields:
     - source_intent_ref
     - user_implied_fog_type
     - primary_fog_type
     - diagnosis_conflict
     - escalation_recommended
   
   recommended_machine_fields:
     - secondary_fog_type
     - escalation_target
     - escalation_reason
     - auto_escalation_allowed
   ```

4. Update INTENT-HARDENING-TRACKER.md to mark Stage 1 complete

---

## Testing Progression

### Phase 1: Fixture Validation
```bash
python scripts/validate-artifact.py repository_sensemaking_brief \
  examples/repo-sensemaker-fixtures/01-clean-intent.md
# → [PASS] + [OK] ✅
```

### Phase 2: Real Artifact Validation
```bash
python scripts/validate-artifact.py repository_sensemaking_brief \
  artifacts/latest-brief-output.md
# → [PASS] + [WARN] (if optional fields missing) or [OK] (if all present)
```

### Phase 3: Strict Validation (final gate)
```bash
python scripts/validate-artifact.py repository_sensemaking_brief \
  artifacts/latest-brief-output.md \
  --strict-recommended
# → [PASS] + [OK] ✅ (ready to promote to required)
```

---

## What repo-sensemaker Cannot Know

These fields are **out of scope** for repo-sensemaker:

- `system_recommended_workflow` ← workflow-orchestrator decides this
- `selected_workflow` ← user/system decides this
- `scope_expansion_proposed` ← to-prd/to-issues decides this
- `routing_decision_method` ← workflow-orchestrator decides this

repo-sensemaker's role: **Diagnose the codebase. Detect problems. Recommend escalation.**

---

## Validator Output Examples

### Passing Output (normal mode)
```
[PASS] Required fields present
[OK] All fields (required + recommended) present
```

### Passing With Warnings (normal mode)
```
[PASS] Required fields present
[WARN] MISSING_RECOMMENDED_FIELD: Recommended field missing: secondary_fog_type
[WARN] MISSING_RECOMMENDED_FIELD: Recommended field missing: escalation_target

  • 2 recommended field(s) missing
  • Use --strict-recommended to promote warnings to errors
```

### Failing (missing required field)
```
[FAIL] Artifact validation failed:
  ERROR MISSING_MACHINE_FIELDS: Could not find a single YAML block containing all required machine fields: ['source_intent_ref', 'user_implied_fog_type', ...]
```

### Strict Mode (--strict-recommended with warnings)
```
[FAIL] Artifact validation failed:
  ERROR MISSING_RECOMMENDED_FIELD: Recommended field missing: secondary_fog_type
```

---

## Checklist for repo-sensemaker Implementation

- [ ] Read this document
- [ ] Review all 3 fixtures
- [ ] Run fixtures through validator
- [ ] Update repo-sensemaker prompt/template to emit required fields
- [ ] Implement fog type detection (product, ui, docs, architecture, mixed, unknown)
- [ ] Implement conflict detection (user implied vs diagnosed)
- [ ] Implement escalation decision logic
- [ ] Test against all 3 fixtures
- [ ] Run validator in normal mode (warnings OK)
- [ ] Run validator in --strict-recommended mode (must pass)
- [ ] Promote fields from recommended → required in artifact-contracts.yaml
- [ ] Update INTENT-HARDENING-TRACKER.md

---

## Why This Matters

repo-sensemaker is the first skill that **understands intent and diagnoses reality**.

This is where the system discovers conflicts, gaps, and unknowns. Getting this right enables the rest of the intent propagation chain.

**Success criterion**: repo-sensemaker output is honest about what it knows and what it doesn't.

---

## Summary

✅ 3 fixtures ready  
✅ Validator clear (unambiguous red/yellow/green output)  
✅ Field list finalized (honest about what repo-sensemaker can detect)  
✅ Promotion path clear (normal mode → strict mode → required)  

**Ready to implement Stage 1.** 🚀
