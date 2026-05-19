# Intent Contract Hardening Tracker

**Date**: 2026-05-19  
**Status**: Two-tier contracts applied. Producer skills pending.  
**Goal**: Promote fields from `recommended` → `required` as each skill is patched.

---

## Hardening Stages

```
Stage 0: Contracts defined with recommended-only fields (✅ DONE)
  ├─ repository_sensemaking_brief: escalation fields → recommended
  ├─ prd: user_goal, scope_expansion → recommended
  └─ issue_list: user_goal, scope_expansion → recommended

Stage 1: Patch repo-sensemaker ✅ DONE
  └─ Promoted: source_intent_ref, user_implied_fog_type, primary_fog_type, diagnosis_conflict, escalation_recommended
  └─ Remaining recommended: escalation_target, escalation_reason, auto_escalation_allowed

Stage 2: Patch workflow-orchestrator ✅ DONE
  └─ Promoted: system_recommended_workflow, selected_workflow, routing_decision_method, routing_divergence
  └─ Updated SKILL.md with routing audit instructions (Section: Stage 2: Routing Audit)
  └─ Updated workflow-orchestration-template.md with routing fields documented
  └─ Created 3 fixtures: 01-routing-agreement, 02-routing-override, 03-tie-breaker
  └─ All 3 fixtures pass strict validation

Stage 3: Patch to-prd ✅ DONE
  └─ Promoted: source_intent_ref, user_goal_preserved_as, scope_expansion_proposed, scope_expansion_requires_approval
  └─ Created 3 fixtures: 01-goal-preserved, 02-scope-expansion-proposed, 03-scope-expansion-approved
  └─ All 3 fixtures pass strict validation

Stage 4: Patch to-issues ✅ DONE
  └─ Promoted: source_intent_ref, user_goal_preserved_as, scope_expansion_proposed, scope_expansion_status
  └─ Created 3 fixtures: 01-core-features-only, 02-core-plus-approved-expansion, 03-scope-divergence-escalation
  └─ All 3 fixtures pass strict validation
```

---

## Current State: Two-Tier Contracts

### repository_sensemaking_brief

**Required** (errors if missing):
```yaml
- source_intent_ref
- recommended_workflow_id
- recommended_execution_mode
- weakest_boundary
- required_inputs
- user_implied_fog_type       ✅ Stage 1 complete
- primary_fog_type            ✅ Stage 1 complete
- diagnosis_conflict          ✅ Stage 1 complete
- escalation_recommended      ✅ Stage 1 complete
```

**Recommended** (warnings only):
```yaml
- escalation_target           ← Still pending (optional for now)
- escalation_reason           ← Still pending (optional for now)
- auto_escalation_allowed     ← Still pending (optional for now)
```

---

### prd

**Required** (errors if missing):
```yaml
- source_intent_ref
```

**Recommended** (warnings only):
```yaml
- user_goal_preserved_as      ← to-prd needs patching
- scope_expansion_proposed    ← to-prd needs patching
- scope_expansion_requires_approval ← to-prd needs patching
```

---

### issue_list

**Required** (errors if missing):
```yaml
- source_intent_ref
```

**Recommended** (warnings only):
```yaml
- user_goal_preserved_as      ← to-issues needs patching
- scope_expansion_proposed    ← to-issues needs patching
- scope_expansion_status      ← to-issues needs patching
```

---

### workflow_orchestration_plan

**Required** (errors if missing):
```yaml
- artifact_id
- source_intent_ref
- chosen_workflow_id
- execution_mode
- system_recommended_workflow
- selected_workflow
- routing_divergence
- routing_decision_method
- escalation_recommended
- auto_escalation_allowed
- scope_expansion_requires_approval
- status
- initial_inputs
- steps
- approval_gates
- gate_behavior
- stop_conditions
- subset_run
- subset_reason
- included_steps
- excluded_steps
```

**Note**: All plan fields are required because `orchestration-runner` already emits them. ✅

---

## Validator Behavior

### Normal Mode (Default)
```bash
python scripts/validate-artifact.py repository_sensemaking_brief artifacts/brief.md
```

- Required fields missing → ERROR (exit 1)
- Recommended fields missing → WARNING (printed, exit 0)

Output:
```
WARNING MISSING_RECOMMENDED_FIELD: Recommended field missing: escalation_recommended
[OK] Artifact validation passed for artifacts/brief.md!
  (1 warnings - use --strict-recommended to promote to errors)
```

### Strict Mode
```bash
python scripts/validate-artifact.py repository_sensemaking_brief artifacts/brief.md --strict-recommended
```

- Required fields missing → ERROR (exit 1)
- Recommended fields missing → ERROR (exit 1)

Output:
```
ERROR MISSING_RECOMMENDED_FIELD: Recommended field missing: escalation_recommended
[FAIL] Artifact validation failed (errors above)
```

---

## Promotion Checklist

When a producer skill is patched, follow this sequence:

### 1. Patch the Skill
Update the skill to emit all required fields. Example for repo-sensemaker:
```python
# Add to skill output
machine_fields = {
    "escalation_recommended": high_uncertainty,
    "escalation_target": "full-fog-workflow" if escalation else None,
    "escalation_reason": "high_uncertainty" | "intent_diagnosis_conflict",
    "auto_escalation_allowed": False  # Default: users must approve
}
```

### 2. Create Passing Fixture
Add a test artifact to `examples/<skill-name>-fixtures/` that includes all fields:
```yaml
# examples/repo-sensemaker-fixtures/valid-brief-with-escalation.md
artifact_id: repository_sensemaking_brief
source_intent_ref: ../../00-user-intent.md
escalation_recommended: true
escalation_target: full-fog-workflow
escalation_reason: high_uncertainty
auto_escalation_allowed: false
...
```

Test with `--strict-recommended`:
```bash
python scripts/validate-artifact.py repository_sensemaking_brief \
  examples/repo-sensemaker-fixtures/valid-brief-with-escalation.md \
  --strict-recommended
```

### 3. Promote to Required in Contract
Update `artifact-contracts.yaml`:
```yaml
repository_sensemaking_brief:
  required_machine_fields:
    - escalation_recommended    # ← moved from recommended
    - escalation_target
    - escalation_reason
    - auto_escalation_allowed
  recommended_machine_fields: []  # empty now
```

### 4. Update This Tracker
Mark the stage as complete:
```
Stage 1: Patch repo-sensemaker ✅ DONE
```

---

## Testing Progression

```
Week 1: Two-tier contracts live + warning output
  ├─ Smoke tests pass (Step 2 ✅)
  ├─ Warnings show exactly what's missing
  └─ No breaking changes to existing integration tests

Week 2: Patch repo-sensemaker
  ├─ Update skill to emit escalation fields
  ├─ Promote fields: recommended → required
  └─ Verify all fixtures pass strict validation

Week 3: Patch workflow-orchestrator
  ├─ (Same pattern as repo-sensemaker)

Week 4: Patch to-prd, to-issues
  ├─ (Same pattern)

End State: All fields required, all producers emit them
  └─ Run with --strict-recommended passes everywhere
```

---

## Why Two-Tiers?

Coupling all changes (runner + contracts + validators + skills) in one go creates noise:
- Validators fail for N reasons simultaneously
- Unclear which skill is the bottleneck
- Hard to debug production integration issues

Two-tiers decouple the work:
- ✅ Contracts proven (fixtures pass)
- ✅ Runner works (smoke tests pass)
- ⏳ Skills update (one at a time, in order)
- ✅ Warnings show exactly what remains

This matches the principle: **"Harden only where pressured."** The pressure here is:
- Warnings tell us what to patch next
- Tests still pass (no noise)
- Clear bottleneck visibility

---

## Commands for Each Stage

### Stage 0 (Now)
```bash
# Prove fixtures work
python scripts/validate-user-intent.py examples/intent-contracts/valid-user-intent.md
python scripts/validate-user-intent-amendment.py examples/intent-contracts/valid-amendment.md

# Run smoke tests
python scripts/orchestration-runner.py "test" --mode plan_only

# See warnings
python scripts/validate-artifact.py repository_sensemaking_brief sample-brief.md
# → WARNING MISSING_RECOMMENDED_FIELD: Recommended field missing: escalation_recommended
```

### Stage 1 (repo-sensemaker patched)
```bash
# Test the patched skill
python scripts/validate-artifact.py repository_sensemaking_brief \
  artifacts/latest-brief.md \
  --strict-recommended  # Now passes ✅

# Update contract (move fields to required)
# (Edit artifact-contracts.yaml)

# Re-validate with strict mode
python scripts/validate-artifact.py repository_sensemaking_brief \
  artifacts/latest-brief.md \
  --strict-recommended  # Still passes ✅

# Update this tracker
# (Mark Stage 1 as complete)
```

---

## FAQ

**Q: Why not require all fields immediately?**  
A: That breaks integration tests before skills are ready. Warnings are visible pressure without blocking progress.

**Q: Can I promote fields selectively?**  
A: Yes. If one skill emits escalation_recommended but not escalation_target, promote the former first.

**Q: What if a skill partially emits fields?**  
A: Leave those fields recommended. Only promote once the skill emits all related fields. This keeps fixture tests clean.

**Q: How do I know when a skill is "done"?**  
A: When `python ... --strict-recommended` passes on its output artifacts.

---

## Summary

- ✅ Two-tier contracts live (Stage 0)
- ✅ Validators support recommended fields with warnings
- ⏳ Skills pending (Stages 1–4)
- 📊 Tracker shows exact bottleneck at each step
- 🚀 Ready for production integration testing

**Next**: Patch repo-sensemaker to emit escalation fields. (Stage 1)
