# ADR 0027: Workflow registry identity is separate from current liveness

**Status:** Accepted  
**Date:** 2026-09-01  
**Decision source:** issue #263, Option B explicitly owner-ratified  
**Evidence:** `artifacts/workflow_executability_consumer_analysis.md`

## Context

The workflow registry has accumulated two legitimate responsibilities that were previously conflated:

1. preserve stable workflow IDs and historical/compatibility definitions used by artifacts, documentation, and reconciliation; and
2. describe workflows that are currently eligible for recommendation, selection, planning, and execution.

Those responsibilities are not equivalent.

The qualified analysis in `artifacts/workflow_executability_consumer_analysis.md` confirmed eight registered workflows with at least one `local_execution` dependency whose Skill is explicitly proposed or deprecated and has no current installed implementation. Existing planning and validation machinery treated registry membership as sufficient evidence of current liveness.

Deleting those workflow definitions would discard useful provenance. Treating them as current capabilities would continue overstating what the product can execute.

## Decision

Workflow identity and workflow liveness are separate contracts.

```text
registered != currently selectable
historical identity != live capability
plan-valid structure != executable capability
recommendation != execution authority
```

### Catalog identity

`workflow-registry.yaml` remains the catalog of stable workflow identities and definitions. Historical and compatibility workflow IDs stay representable there unless a separate migration explicitly retires their identity.

The canonical workflow ID vocabulary remains a catalog vocabulary. An ID can therefore be structurally known even when it is not currently selectable.

### Liveness overlay

Current liveness is declared separately in:

- `skills/workflow-planner/references/workflow-liveness.yaml` for the repository/runtime-facing catalog; and
- `src/sensemaking_skills/defaults/workflow-liveness.yaml` for the packaged default catalog.

The liveness vocabulary is intentionally narrow:

- `active` — eligible for current recommendation, selection, planning, and execution, subject to the normal authority model;
- `compatibility_only` — retained for identity/provenance/compatibility but ineligible for current recommendation, selection, planning, or execution.

The default is `active`. This preserves compatibility for external/custom workflow registries that predate ADR 0027: a new workflow without an explicit override remains current unless its owner says otherwise.

### Initial compatibility-only set

The evidence-qualified initial set is:

- `product-to-issues`
- `product-autonomous-sprint`
- `experimental-autonomous-sprint`
- `implementation-workflow`
- `product-implementation-workflow`
- `ui-diagnostic-workflow`
- `ui-implementation-workflow`
- `architecture-implementation-workflow`

This classification does not delete those definitions and does not decide how or whether their intended responsibilities should later be restored.

### Consumer behavior

Current operational consumers must fail closed on non-active workflows.

- Repository diagnosis may preserve or discuss compatibility workflow IDs as historical evidence, but must not emit them as a current actionable recommendation.
- Workflow planning must not silently substitute another active workflow when a former default is compatibility-only. If no active workflow is warranted, preserve that absence and escalate/return control to Sensemaking or the owner rather than inventing a route.
- Orchestration/runtime execution must refuse compatibility-only workflow selection.
- Plan validation must reject a compatibility-only workflow as a current executable plan while catalog/registry validation continues to preserve and structurally validate the historical definition.
- Package consumers must be able to distinguish the complete catalog from the currently selectable subset.

Liveness does not grant execution authority. An `active` workflow is merely eligible to be selected; ADR 0026 and the agent-native authority model still govern whether execution is authorized.

### Validation boundary

Validation has two different questions:

1. **Catalog validity:** Is the historical/current workflow definition structurally coherent and is its liveness declaration well-formed?
2. **Current capability validity:** Is the workflow active and therefore eligible for a current plan or execution request?

A compatibility-only workflow may pass catalog validity while correctly failing current capability validity.

## Consequences

### Positive

- Historical workflow IDs and provenance remain durable.
- Current planning no longer implies that proposed/deprecated missing Skills are live capabilities.
- Runtime and validation can fail closed without reviving `tdd`, implementing `triage`, or deleting historical workflows.
- External/custom workflows remain active by default, avoiding an unnecessary migration burden.

### Costs

- Consumers must distinguish catalog lookup from current-selectability lookup.
- Tests and examples that intentionally exercise a former current workflow may need to identify themselves as historical fixtures or move to an active workflow.
- A future decision is still required if an owner wants to redesign, restore, or permanently retire any compatibility-only workflow.

## Explicit non-decisions

ADR 0027 does **not**:

- revive `tdd`;
- implement `triage`;
- replace missing Skills one-for-one;
- choose new implementation workflows for product/UI/architecture fog;
- authorize automatic routing;
- create a general-purpose lifecycle framework for Skills, artifacts, or arbitrary entities;
- make `active` equivalent to execution authorization.

## Verification

The implementation of this ADR must prove at minimum that:

1. all eight evidence-qualified workflows remain present in the catalog;
2. all eight resolve to `compatibility_only`;
3. unlisted workflows resolve to `active` by default;
4. current planning/runtime selection cannot execute a compatibility-only workflow;
5. catalog validation continues to inspect compatibility definitions rather than deleting or ignoring them;
6. the packaged defaults expose the same liveness semantics for shared workflow IDs.
