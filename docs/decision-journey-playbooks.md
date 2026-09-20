# Decision Journey Canonical Playbooks

These playbooks demonstrate composition. They are examples, not automatic routing rules.

## Playbook 1 — Open repository future -> build -> evidence -> reassess

1. Use `strategic-repository-analysis` to author the current-system model,
   construction paths, decision-changing uncertainty, and disposition.
2. If `BUILD` is semantically warranted, explicitly select the bounded
   responsibility.
3. Create/use Campaign durability only when continuation complexity warrants it.
4. Create an execution handoff from the already-selected responsibility.
5. Treat worker return as evidence, never as global closure.
6. Reconcile returned evidence.
7. If strategy changes, author a later strategic analysis and, when useful, an
   authored strategic decision delta.
8. Use `journey inspect` to reconstruct the declared round trip.

## Playbook 2 — Returned evidence invalidates a strategic assumption

1. Begin from an authored strategic analysis carrying explicit assumptions.
2. Execution returns evidence that materially challenges one assumption.
3. Learning/Reconciliation decides whether the evidence is decision-changing.
4. If Level 3 must reopen, author the later strategic analysis.
5. Author `strategic_decision_delta` only when the reason for the changed
   disposition is worth preserving durably.
6. Use `strategy compare` for mechanical representation differences and
   `journey delta` for the authored semantic explanation.

`
mechanical difference != semantic reason
reassessment trigger observed != assumption falsified
assumption falsified != replacement strategy selected
`

## Playbook 3 — Implemented change with adjacent closure consequences

1. Author `change_impact_analysis` around the bounded contemplated or completed
   change.
2. Execute/verify the authorized work.
3. Record observed evidence and reconciliation.
4. Author `change_evidence_closure` against the original impact analysis.
5. Use `journey impact-closure` to expose anticipated surfaces that are
   verified, unresolved, or still unaccounted for.
6. The semantic agent decides whether more work, closure, owner decision,
   strategic reassessment, or thesis review is warranted.

## Playbook 4 — Fresh high-delegation agent

Use the smallest explicit context profile that matches the already-known control
scope:

`bash
sensemaking-skills journey context --profile strategic ...
sensemaking-skills journey context --profile responsibility ...
sensemaking-skills journey context --profile execution ...
sensemaking-skills journey context --profile reassessment ...
`

Do not automatically promote from one profile to another. The profile is selected
by the caller because the control scope is a semantic decision.
