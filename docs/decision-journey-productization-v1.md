# Decision Journey Productization v1

**Status:** COMPLETE / INTEGRATED / NORMAL_USE_HANDOFF (Issue #432)  
**Scope:** product composition over existing Level-3/Level-2/Level-1 surfaces  
**Authority:** read-only mechanical reconstruction plus explicitly authored semantic companions  
**Non-goal:** no planner, router, new control level, or alternate state authority

## Purpose

Sensemaking already has strategic analysis, Strategic Continuity, Campaign durability,
execution handoff/result, reconciliation, change-impact analysis, and protected
authority boundaries. Decision Journey Productization v1 makes those surfaces
usable as one reconstructible product journey:

```
strategy
  -> bounded responsibility
  -> Campaign / execution handoff
  -> worker result / evidence
  -> reconciliation
  -> strategic reassessment
```

The commands do not infer missing semantic links. Missing declared links remain
visible as diagnostics.

## Commands

```bash
sensemaking-skills journey inspect ...
sensemaking-skills journey context --profile strategic|responsibility|execution|reassessment ...
sensemaking-skills journey delta ...
sensemaking-skills journey impact-closure ...
sensemaking-skills journey guide --intent ...
```

## Package A — Round-Trip Decision Journey

```journey inspect``` accepts explicitly supplied strategic artifacts, Campaign
workspace, strategic reconciliation artifacts, change-impact artifacts, an
optional returned strategic analysis, and an optional ```decision_journey```
manifest.

Example manifest:

```yaml
artifact_id: decision_journey
journey_id: JOURNEY-1
strategic_origin_ref: SRA-1
campaign_id: CMP-1
execution_handoff_ids: [H-1]
execution_result_ids: [R-1]
strategic_reconciliation_refs: [REC-1]
change_impact_refs: [CIA-1]
strategic_return_ref: SRA-2
```

The manifest is a companion index. It is not a state machine and does not
authorize any transition.

```
mechanical reconstruction != causal truth
missing link != semantic failure
journey complete != responsibility correctly chosen
```

## Package B — Progressive Context Packs

The caller selects one profile:

- ```strategic``` — authored strategic analysis projection;
- ```responsibility``` — mission, responsibility, uncertainty, authority, targets, stop conditions;
- ```execution``` — selected responsibility, targets, evidence, latest handoff/result;
- ```reassessment``` — returned result, reconciliation state, change-impact evidence, optional returned strategy.

```
profile selected by caller != automatic routing
context pack != recommendation
less context != less semantic responsibility
```

## Package C — Authored Strategic Decision Delta

Mechanical ```strategy compare``` remains separate from semantic explanation.
When a strategic judgment changes and the reason deserves durable continuity,
the semantic author may create:

```yaml
artifact_id: strategic_decision_delta
delta_ref: DELTA-1
prior_analysis_ref: SRA-1
current_analysis_ref: SRA-2
continuity_disposition: REVISE
unchanged_commitments:
  - "Product purpose remains unchanged."
new_evidence_refs:
  - "evidence:E-1"
assumption_changes:
  - assumption_id: ASSUMPTION-1
    effect: INVALIDATED
    reason: "Returned evidence contradicted the premise."
decision_change: "BUILD -> INVESTIGATE"
semantic_reason: "The dependency must be resolved before construction."
semantic_truth_established: false
strategy_selected_by_delta: false
implementation_authorized_by_delta: false
```

```journey delta``` checks only reference/boundary consistency. The explanation
itself remains authored semantic judgment.

## Package D — Change -> Evidence -> Closure

A completed or in-progress change-impact episode may add:

```yaml
artifact_id: change_evidence_closure
closure_ref: CEC-1
change_impact_ref: CIA-1
observed_evidence_refs:
  - "test:contract-regression"
verified_surface_ids: [IMPACT-1]
unresolved_surface_ids: [IMPACT-2]
reconciliation_refs: [REC-1]
closure_disposition: READY_TO_REASSESS
semantic_reason: "One anticipated surface remains unresolved."
closure_inferred_by_artifact: false
followup_execution_authorized_by_artifact: false
semantic_truth_established: false
```

```journey impact-closure``` reports:

- anticipated surface IDs;
- verified surface IDs;
- unresolved surface IDs;
- anticipated surfaces still unaccounted for;
- the authored closure disposition.

It does not turn an unaccounted surface into automatic failure or authorize
follow-up work.

## Package E — Beginner-First Guided UX

```journey guide``` takes one explicit caller-selected intent and points to the
existing capability/entry point. The mapping is static and inspectable.

The command never:

- observes user intent implicitly;
- invokes a Skill;
- creates a Campaign;
- selects work;
- grants authority.

Canonical examples are in ```docs/decision-journey-playbooks.md```.

## Claim ceilings

```
journey projection valid != semantic journey correct
decision delta valid != strategic change warranted
impact closure valid != closure warranted
guide suggestion != capability invocation
mechanical composition != product-value proof
```
