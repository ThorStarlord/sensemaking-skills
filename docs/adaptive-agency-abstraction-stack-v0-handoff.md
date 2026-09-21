# Adaptive Agency Abstraction Stack v0 — Milestone Handoff

**Status:** research/reference package complete on feature branch; integration pending PR #445 qualification/merge  
**Date:** 2026-09-21  
**Tracker:** Issue #444  
**Scope:** Root Primitive / Cognitive Operator / Capability-Skill / Organization / Institution research model, Sensemaking reconciliation, bounded General Agency and Practical Agent Architecture integration, and mechanical boundary checks  
**Authority:** owner-directed bounded research/reconciliation; ADR 0029 remains current product-boundary authority

## 1. Objective

Clarify the pedagogical ladder:

~~~text
Primitive -> Operator -> Skill -> Organization -> Institution
~~~

without collapsing capability composition, multi-agent coordination, and governance/persistence into one runtime hierarchy.

The implemented research shape is:

~~~text
Capability Plane
  Root Primitive -> Cognitive Operator -> Capability / Skill

Coordination Plane
  delegation -> role/team/cell -> Organization

Governance / Persistence Plane
  rules/policy/authority/provenance/continuity -> Institution
~~~

plus a distinct promotion/evolution ladder:

~~~text
ephemeral composition
-> candidate reusable operator
-> packaged capability / Skill
-> repeatable coordination pattern
-> institutionalized practice
~~~

## 2. What changed

Created:

- docs/superpowers/specs/2026-09-21-adaptive-agency-abstraction-stack-v0-design.md
- docs/superpowers/plans/2026-09-21-adaptive-agency-abstraction-stack-v0.md
- docs/research/adaptive-agency-abstraction-stack-v0.md
- docs/research/adaptive-agency-abstraction-stack-v0-reconciliation.md
- tests/test_adaptive_agency_abstraction_stack_v0.py
- this handoff

Updated:

- docs/research/general-agency-model-v0.1.md
- skills/using-sensemaking/references/practical-agent-architecture-v0.md
- STATUS.md

## 3. Main conclusions

### 3.1 Root Primitive

Root Primitive is an environment/harness affordance, not a new Sensemaking registry.

### 3.2 Cognitive Operator

General Agency Model v0.1 already contains the relevant reasoning abstraction class: challenge, exploration, decomposition, comparison, causal/counterfactual reasoning, and forecasting/simulation.

### 3.3 Capability / Skill

Current Sensemaking Capability/Skill contracts already satisfy the packaged-capability layer. Skill remains one capability form; no replacement domain model was introduced.

### 3.4 Organization

Current Sensemaking models bounded delegation and evidence return but does not own dynamic role/topology/worker allocation.

Organization is defined as materially multi-actor coordination in which roles, specialization, communication, or topology affect how the objective is pursued.

~~~text
Campaign != Organization
delegation != Organization automatically
~~~

### 3.5 Institution

Institution is modeled as durable governance/continuity capable of surviving actor replacement, not as a larger Organization.

Current Sensemaking has institution-like continuity surfaces—strategy, ADRs, authority, policies, Campaign state, provenance/currentness, strategic continuity, reconciliation—but this does not create an Institution runtime or product-category claim.

## 4. Product/runtime disposition

The reconciliation found no current runtime, schema, or product-boundary gap.

~~~text
RESEARCH_REFERENCE_COMPLETE
RUNTIME_GAP = NO_RUNTIME_GAP_ESTABLISHED
PRODUCT_BOUNDARY = NO_PRODUCT_BOUNDARY_CHANGE
CURRENT CONSTRUCTION RESPONSIBILITY = NONE
NEXT MODE = NORMAL_USE_VALIDATION
~~~

No OrganizationState, InstitutionState, team registry, communication graph, scheduler, worker allocator, organization compiler, critic service, multi-agent voting mechanism, or Campaign schema change was added.

## 5. Authority boundary preserved

The package makes the following laws explicit:

~~~text
research model != product expansion
organization modeled != organization runtime warranted
Campaign != Organization
capability growth != authority growth
agent-created abstraction != self-granted permission
repeated successful coordination != automatic canonical promotion
institution != autonomous agent collective
organization pattern != execution authority
~~~

Existing authority doctrine remains unchanged.

## 6. Organizational learning hypothesis

The package records one future research hypothesis:

> Real work may reveal reusable arrangements of agents, roles, communication links, challenge relationships, and verification structures, just as real work can reveal reusable Skills.

This hypothesis remains unvalidated.

A future organizational-pattern package requires repeated normal-use pressure or explicit owner direction. No synthetic swarm experiment is required or authorized by this milestone.

## 7. Validation evidence and ceiling

### Hosted PR validation

The RED-stage head containing the new documentation contract test but not the model/reconciliation/handoff was submitted through PR #445.

Product Validation and Release Candidate Distribution both returned PASS on that head.

That result **does not constitute RED proof for the new focused test**, because the current hosted PR suites did not exercise the newly added test file: the test would have raised missing-file errors had it been collected.

### Local focused pytest

A local exact-branch clone/test run could not be executed in the current tool environment because the container has no outbound DNS/network access to GitHub.

Therefore this handoff does **not** claim that tests/test_adaptive_agency_abstraction_stack_v0.py has been executed in this session.

### What can still be established

- GitHub records the exact branch changes and PR head.
- Existing hosted Product Validation / Release Candidate Distribution can provide broader repository integration evidence for each pushed PR head.
- The focused contract test is checked in for future full-suite/local execution.
- Repository qualification, even when green, establishes representation/integration coherence only; it does not establish empirical usefulness of emergent organization.

## 8. Reopen conditions

Reopen construction only if ordinary use or explicit owner direction establishes a decision-changing gap such as:

- repeated multi-agent episodes where current handoff/result semantics lose consequential coordination state;
- repeated inability to reconstruct why role/topology allocation materially changed the result;
- stable recurring team/cell patterns whose safe reuse requires a repository-owned contract;
- a real external software-factory integration that cannot preserve authority/evidence boundaries without a shared organizational representation;
- explicit Level-4 owner direction to expand the current product boundary.

Do not reopen because the research model names concepts that could be implemented.

## 9. Final disposition

~~~text
ISSUE_444_ADAPTIVE_AGENCY_ABSTRACTION_STACK_V0 = COMPLETE_RESEARCH_REFERENCE
RUNTIME_GAP = NO_RUNTIME_GAP_ESTABLISHED
PRODUCT_BOUNDARY = NO_PRODUCT_BOUNDARY_CHANGE
CURRENT CONSTRUCTION RESPONSIBILITY = NONE
PRIMARY CONSTRUCTION PROGRAM = NONE
NEXT MODE = NORMAL_USE_VALIDATION
~~~

The appropriate next step is ordinary use. Preserve evidence if real multi-agent work exposes recurring organizational friction; otherwise keep the model as bounded research/reference guidance.
