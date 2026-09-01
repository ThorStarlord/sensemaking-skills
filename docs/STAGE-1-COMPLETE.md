# Stage 1 Complete: repo-sensemaker Intent-Aware ✅

**Date**: 2026-05-19  
**Status**: ✅ COMPLETE  
**Validation**: 3/3 fixtures pass (normal + strict modes)  
**Fields Promoted**: 5/5 required, 3/3 remaining optional

---

> **⚠️ Historical document (flagged non-normative 2026-09-01).** This is a
> dated 2026-05-19 phase-completion record, not the current `repo-sensemaker`
> contract. Field lists, examples, and validation claims below describe a
> since-superseded contract — `mixed`/`unknown` are not canonical
> `primary_fog_type` values today, and `secondary_fog_type` has been retired
> with no replacement (see the repo-sensemaker product-definition
> adjudication). Do not treat anything below as current instructions or as a
> claim about current validator behavior. Current authority lives in
> `docs/canonical-vocabulary.yaml`,
> `skills/workflow-planner/references/artifact-contracts.yaml`,
> `skills/repo-sensemaker/references/repo-analysis-template.md`,
> `skills/repo-sensemaker/SKILL.md`, and the current validators.

## What Was Done

### 1. Updated repo-sensemaker Instructions
**File**: `skills/repo-sensemaker/SKILL.md`

Added "Stage 1: Intent-Aware Analysis" section that explains:
- How to extract user intent (implied fog type)
- How to diagnose codebase (actual fog type)
- How to detect conflicts between intent and diagnosis
- Which 5 fields are required to emit

### 2. Updated Output Template
**File**: `skills/repo-sensemaker/references/repo-analysis-template.md`

Added machine-readable section with Stage 1 fields and complete example:
```yaml
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: product_fog | ui_fog | docs_fog | architecture_fog | unknown
primary_fog_type: product_fog | ui_fog | docs_fog | architecture_fog | mixed | unknown
diagnosis_conflict: true | false
escalation_recommended: true | false
```

### 3. Promoted Fields in Contracts
**File**: `skills/workflow-orchestrator/references/artifact-contracts.yaml`

Moved 5 Stage 1 fields from `recommended_machine_fields` → `required_machine_fields`:
- ✅ source_intent_ref
- ✅ user_implied_fog_type
- ✅ primary_fog_type
- ✅ diagnosis_conflict
- ✅ escalation_recommended

Kept 3 fields as recommended (deferred to future stages):
- escalation_target (optional—orchestrator decides this)
- escalation_reason (optional—for clarity)
- auto_escalation_allowed (optional—default: false)

### 4. Updated Hardening Tracker
**File**: `docs/INTENT-HARDENING-TRACKER.md`

Marked Stage 1 as complete, updated field status.

---

## Validation Results

### Fixture Test: All Pass ✅

| Fixture | Scenario | Required Fields | Recommended Fields | Strict Mode |
|---------|----------|-----------------|-------------------|------------|
| 01-clean-intent.md | User intent aligns with codebase | ✅ PASS | ✅ All present | ✅ PASS |
| 02-conflict-intent.md | User wants UI, code needs architecture | ✅ PASS | ✅ All present | ✅ PASS |
| 03-insufficient-evidence.md | No business context, unclear direction | ✅ PASS | ✅ All present | ✅ PASS |

> **Historical note (2026-09-01)**: the 03-insufficient-evidence.md PASS
> above was recorded 2026-05-19 under a vocabulary that no longer applies
> (`primary_fog_type: unknown` is not a canonical value today). Not a claim
> about current `validate-brief.py` behavior; see the fixture's own
> historical banner.

### Validator Output

**Normal Mode**:
```
[PASS] Required fields present
[OK] All fields (required + recommended) present
```

**Strict Mode** (--strict-recommended):
```
[PASS] Required fields present
[OK] All fields (required + recommended) present
```

---

## Stage 1 Scope Boundaries

### What repo-sensemaker Owns (Stage 1)
✅ Analyze code structure  
✅ Detect what fog type the code signals  
✅ Compare user intent vs code diagnosis  
✅ Recommend escalation when conflict detected  
✅ Emit the 5 Stage 1 fields  

### What repo-sensemaker Does NOT Own
❌ Workflow routing decision (workflow-orchestrator owns this)  
❌ Workflow ID selection (orchestrator selects final workflow)  
❌ Scope expansion (to-prd/to-issues own this)  

**Split Preserved**: Diagnosis ≠ Action. repo-sensemaker diagnoses. Orchestrator routes.

---

## Production Readiness

| Component | Status | Notes |
|-----------|--------|-------|
| Instructions | ✅ Updated | Intent-aware workflow documented |
| Template | ✅ Updated | Machine-readable fields added with example |
| Contracts | ✅ Updated | 5 fields promoted to required |
| Fixtures | ✅ Passing | 3/3 pass normal + strict mode |
| Validator | ✅ Ready | Unambiguous [PASS]/[WARN]/[FAIL] output |

---

## How repo-sensemaker Should Work (Post-Stage-1)

When analyzing a repository with intent:

```
1. Read 00-user-intent.md
   └─ Extract: user_implied_fog_type

2. Analyze codebase
   └─ Detect: primary_fog_type, secondary_fog_type

3. Compare
   └─ diagnosis_conflict = (user_implied != primary)?

4. Escalation Logic
   └─ escalation_recommended = conflict || insufficient_evidence || high_uncertainty

5. Emit YAML
   ├─ source_intent_ref: ../../00-user-intent.md
   ├─ user_implied_fog_type: [from intent]
   ├─ primary_fog_type: [from diagnosis]
   ├─ diagnosis_conflict: [boolean]
   └─ escalation_recommended: [boolean]
```

---

## What Happens in Workflows

### Normal Case (No Conflict)
```
repo-sensemaker → [primary_fog_type: product_fog, conflict: false]
  ↓
workflow-orchestrator → Selects: product-implementation-workflow
  ↓
Product workflow runs
```

### Conflict Case (Diagnosis ≠ Intent)
```
repo-sensemaker → [user_implied: ui_fog, primary: architecture_fog, conflict: true, escalate: true]
  ↓
workflow-orchestrator → Recommends: full-fog-workflow
  ↓
User/system decides: escalate or override
  ↓
Full-fog workflow runs (if escalated)
```

### Insufficient Evidence Case
```
repo-sensemaker → [primary: unknown, escalate: true, reason: insufficient_evidence]
  ↓
workflow-orchestrator → Recommends: full-fog-workflow
  ↓
User/system decides: escalate or override
  ↓
Full-fog workflow runs (if escalated)
```

---

## Next Stage (Stage 2)

**Target**: `workflow-planner`

**Fields to promote** (when orchestrator is patched):
```yaml
system_recommended_workflow
selected_workflow
routing_decision_method
routing_divergence
```

**Stage 2 success criterion**: Orchestrator produces valid plans with routing audit fields for the intent scenarios.

---

## Stage 1 Summary

```
✅ Intent-aware instructions in place
✅ Output template updated with 5 required fields
✅ 5 fields promoted from recommended → required
✅ 3/3 fixtures pass strict validation
✅ Validator output is unambiguous (green vs yellow vs red)
✅ Scope boundaries preserved (diagnosis ≠ action)

Ready for Stage 2: workflow-orchestrator routing fields
```

---

## Files Modified

1. `skills/repo-sensemaker/SKILL.md` — Added intent-aware analysis workflow
2. `skills/repo-sensemaker/references/repo-analysis-template.md` — Added Stage 1 YAML fields and example
3. `skills/workflow-orchestrator/references/artifact-contracts.yaml` — Promoted 5 fields to required
4. `docs/INTENT-HARDENING-TRACKER.md` — Updated status, marked Stage 1 complete

**Verification**: `git diff skills/ docs/` shows all changes are isolated to intention.

---

## Backward Compatibility

Stage 1 is a **backwards-incompatible change** for repo-sensemaker:
- New required fields must be emitted
- Old briefs (without these fields) will fail validation

**Migration path**: 
- Old briefs can be re-generated by running repo-sensemaker again
- No data loss (intent analysis is deterministic from code)

---

## Success Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Fixtures passing (normal mode) | 3/3 | 3/3 ✅ |
| Fixtures passing (strict mode) | 3/3 | 3/3 ✅ |
| Required fields documented | 5 | 5 ✅ |
| Scope boundaries clear | Yes | Yes ✅ |
| Validator output unambiguous | Yes | Yes ✅ |

---

## Lessons Learned

1. **Intent comparison is diagnostic, not prescriptive** — repo-sensemaker detects conflicts but doesn't resolve them. The orchestrator and user do.

2. **Fog type classification is learned from codebase signals** — Not from the user's implied intent. This is the core of the diagnosis.

3. **Escalation is a recommendation** — The system recommends full-fog when it detects uncertainty or conflict, but the user/orchestrator makes the final call.

4. **Optional fields can wait** — escalation_target, escalation_reason are nice-to-have; the core 5 fields carry all the signal needed for routing.

---

## Ready for Production

Stage 1 is complete and ready for:
- ✅ Real workflow execution (with intent context)
- ✅ Conflict detection and escalation routing
- ✅ Intent propagation through downstream artifacts
- ✅ Hardening remaining stages (2-4)

**Next**: Proceed to Stage 2 (workflow-orchestrator routing fields).
