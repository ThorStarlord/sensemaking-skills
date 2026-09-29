# Architecture Decision Records — Status Lifecycle

This directory holds ADRs for this repository. The ADR probe
(`scripts/probe_relationships.py`, part of the Probe Engine) reads the
`**Status**` line of every `docs/adr/NNN-*.md` and emits findings for
unrecognized or missing statuses and for status-claim mismatches; the status
vocabulary below is the canonical convention it validates against. This file
exists to define the convention so authors and reviewers use the same
vocabulary.

## Statuses

- **PROPOSED**: a candidate decision awaiting owner acceptance and/or
  evidence. Not yet operative.
- **PROVISIONAL**: implemented and evidence-supported, but awaiting a stated
  promotion condition (e.g. owner ratification or external validation)
  before it becomes the operative decision. Not yet Accepted — still write
  as pending, not settled.
- **ACCEPTED**: the operative repository decision. Only an Accepted ADR
  should use `Resolves: Issue #NN` in its header; Proposed and Provisional
  ADRs use `Proposes resolution for:` / `Provisionally addresses:` instead
  (see existing ADRs for examples).
- **SUPERSEDED** / **REJECTED**: reserved for ADRs later replaced or turned
  down, if that need arises. Not otherwise defined further here.

A Provisional ADR's "Status rationale" section should state an explicit,
checkable promotion condition — not just "more evidence needed."

## Index

Statuses below are copied from each ADR's own `**Status**` line. If they
disagree, the ADR file is authoritative.

| ADR | Title | Status |
| --- | --- | --- |
| [0001](0001-strict-validation-in-execution-modes.md) | Strict Validation in Execution Modes | Accepted |
| [0002](0002-workflow-separation-of-concerns.md) | Workflow Separation of Concerns | Accepted |
| [0003](0003-artifact-composition-pattern.md) | Artifact Composition Pattern | Accepted |
| [0004](0004-evidence-tracking-for-trust.md) | Evidence Tracking for Trust | Accepted |
| [0005](0005-skill-invocation-via-workflows.md) | Skill Invocation via Workflow Registry | Accepted |
| [0006](0006-intent-as-durable-artifact.md) | User Intent as Immutable Durable Artifact | Proposed |
| [0007](0007-soft-context-routing.md) | Soft Context Routing | Proposed |
| [0008](0008-routing-divergence-audit.md) | Routing Divergence and Action Audit Trail | Proposed |
| [0009](0009-handoff-skill-naming-convention.md) | Handoff Skill Naming Convention | Accepted |
| [0010](0010-runtime-owns-artifact-path-resolution.md) | Runtime Owns Artifact Path Resolution | Accepted |
| [0011](0011-canonical-vocabulary-enforcement.md) | Canonical Vocabulary Enforcement | Accepted |
| [0012](0012-invocation-paths.md) | Manual vs Automation Invocation Paths | Accepted |
| [0013](0013-agent-native-orchestration-primary.md) | Agent-Native Orchestration as Primary Model | Accepted |
| [0014](0014-product-boundary.md) | Product Boundary of Sensemaking Skills | Superseded by 0029 |
| [0015](0015-deterministic-vs-model-variable-fields.md) | Deterministic versus Model-Variable Artifact Fields | Accepted (ratified addendum) |
| [0016](0016-evidence-policy-for-findings.md) | Evidence Policy for Repository Findings | Accepted (ratified addendum) |
| [0017](0017-readiness-criteria-for-new-features.md) | Readiness Criteria for Adding New Features | Superseded (never Accepted) |
| [0018](0018-workflow-routing-policy.md) | Workflow-Routing Policy | Superseded (never Accepted) |
| [0019](0019-findings-to-tracker-tasks-policy.md) | Findings vs Tracker Tasks | Superseded (never Accepted) |
| [0020](0020-wayfinder-and-prototypes-scope.md) | Wayfinder and Prototypes Scope | Superseded (never Accepted) |
| [0021](0021-production-readiness-requirements.md) | Production-Readiness Requirements | Superseded (never Accepted) |
| [0022](0022-gate-a-authorization-consumer-placement.md) | Gate A Authorization Consumer Placement | Proposed |
| [0023](0023-two-lane-experiment-authorization.md) | Two-Lane Experiment Authorization | Accepted |
| [0024](0024-extended-analysis-field-classification.md) | Extended-analysis Field Classification | Accepted |
| [0025](0025-workflow-orchestration-plan-lifecycle.md) | Two-stage `workflow_orchestration_plan` Lifecycle | Accepted |
| [0026](0026-workflow-execution-authority.md) | Execution Authority for `auto_invoke_next_workflow` | Accepted |
| [0027](0027-workflow-registry-liveness.md) | Workflow Registry Identity vs Liveness | Accepted |
| [0028](0028-agent-agnostic-product-management-domain.md) | Product Management as an Agent-Agnostic Campaign Domain | Accepted |
| [0029](0029-current-product-boundary.md) | Current Product Boundary | Accepted (current boundary) |

For the current product boundary read ADR 0029, not 0014.
