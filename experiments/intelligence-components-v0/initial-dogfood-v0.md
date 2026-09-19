# StrategicPlanner v0 — initial retrospective dogfood

schema: experimental-intelligence-components-v0/initial-dogfood-v0
issue: #395
status: same-context retrospective sanity check
independent: false
hindsight_contaminated: true
comparative_superiority_claim: NOT_SUPPORTED

## Purpose

This package applies the StrategicPlanner v0 treatment qualitatively to four real historical repository decisions. The evaluator knows the historical outcomes, so the result can reveal ceremony, obvious failure modes, and plausible activation boundaries, but cannot establish prospective performance or superiority.

## Case 1 — release-identity-drift

Baseline historical path:
- initial framing emphasized release/documentation reconciliation;
- after examining exact source identity, qualification provenance, and publication state, the responsibility changed to release-identity/provenance repair.

Treatment candidate set:
- reconcile docs around RC1 as current candidate;
- advance immediately to a new frozen RC2 candidate;
- move current source to a development identity toward RC2 while preserving RC1 as historical exact-source provenance;
- assess final 1.0.0 readiness directly.

Observation:
- decision_materiality: MATERIALLY_DIFFERENT_PLAUSIBLE
- missing_option_discovery: MATERIAL_OPTION_SURFACED
- wrong_work_avoidance: PLAUSIBLY_AVOIDED
- ceremony_overhead: PROPORTIONAL
- reversal_exposure: LOWER (plausible, not prospectively demonstrated)
- human_correction: NOT_OBSERVABLE
- cost_proportionality: extra candidate comparison is justified by the broad release-authority ambiguity.

Interpretation: this is the strongest positive signal, but it is also the most hindsight-contaminated case. It supports a prospective test, not promotion.

## Case 2 — stale-authority-reference

Baseline historical path:
- inspect the local current-facing reference;
- replace the superseded ADR pointer with current authority;
- validate and stop.

Treatment candidate set:
- make the direct bounded reference repair;
- broaden into a current-document authority audit;
- open a new Campaign/currentness mechanism.

Observation:
- decision_materiality: SAME
- missing_option_discovery: ONLY_COSMETIC_ALTERNATIVES
- wrong_work_avoidance: UNCHANGED
- ceremony_overhead: DISPROPORTIONATE
- reversal_exposure: UNCHANGED
- human_correction: NOT_OBSERVABLE
- cost_proportionality: planner candidate generation is unnecessary for a local, well-evidenced, reversible edit.

Interpretation: StrategicPlanner should not be an always-on prerequisite. The current control loop scales down better.

## Case 3 — goal-a-environment-blocker

Baseline historical path:
- three substrates were falsified;
- owner halt rule prohibited Harness v4;
- next responsibility became an external environment/owner decision rather than repository construction.

Treatment candidate set:
- attempt another repository-side harness repair;
- move to a host/environment with independent credentials;
- weaken independence requirements;
- stop and await an owner/environment change.

Observation:
- decision_materiality: BETTER_SUPPORTED
- missing_option_discovery: NONE
- wrong_work_avoidance: UNCHANGED
- ceremony_overhead: NOTICEABLE_BUT_ACCEPTABLE
- reversal_exposure: UNCHANGED
- human_correction: NOT_OBSERVABLE
- cost_proportionality: planner makes the rejected alternatives explicit, but the baseline already reaches the correct stop boundary.

Interpretation: explicit candidate generation improves auditability more than decision quality here.

## Case 4 — execution-interface-boundary

Baseline historical path:
- preserve Sensemaking as decision/control plane;
- add bounded handoff/result contracts and projections;
- do not build a scheduler or execution engine.

Treatment candidate set:
- generic execution handoff/result contracts;
- AI Software Factory-specific integration first;
- scheduler/queue runtime inside Sensemaking;
- guidance-only handoff with no durable contract.

Observation:
- decision_materiality: BETTER_SUPPORTED
- missing_option_discovery: MATERIAL_OPTION_SURFACED
- wrong_work_avoidance: PLAUSIBLY_AVOIDED
- ceremony_overhead: PROPORTIONAL
- reversal_exposure: LOWER (plausible, not prospectively demonstrated)
- human_correction: NOT_OBSERVABLE
- cost_proportionality: explicit alternatives help protect the product boundary on a broad design decision.

Interpretation: the treatment appears useful when multiple materially different architectural boundaries are credible.

## Cross-case pattern

Observed pattern:

- broad, ambiguous, high-leverage decisions: planner candidate generation can expose material alternatives and make boundary tradeoffs explicit;
- narrow, direct, reversible decisions: the same machinery is ceremony;
- blocker cases with strong existing constraints: the planner mostly improves explanation/auditability rather than the selected responsibility.

This supports an activation hypothesis rather than an always-on architecture:

Use StrategicPlanner-like candidate generation only when the active agent faces multiple credible repository-level boundaries, unstable framing, or a consequential/irreversible choice where missing an alternative would matter.

Do not activate it merely because a task is complex in implementation.

## Disposition

RESEARCH_MORE

Reason:

The experiment produced a plausible signal on strategic ambiguity and a clear negative signal on bounded work, which is useful information. But all four cases are retrospective, same-context, and hindsight-contaminated. The evidence is insufficient for PROMOTE_CORE or PROMOTE_OPTIONAL.

## Next evidence required

Before building WarrantEngine v0 or promoting StrategicPlanner:

1. capture the baseline decision before treatment on a naturally occurring prospective Level-3 decision;
2. apply StrategicPlanner v0 without changing the evidence available;
3. record whether it surfaces a genuinely decision-changing option/uncertainty;
4. record ceremony and whether the active agent's final responsibility changes;
5. repeat only when ordinary repository work naturally provides a suitable ambiguous case.

Do not manufacture tasks to populate the experiment.
