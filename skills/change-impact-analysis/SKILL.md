---
name: change-impact-analysis
description: analyze a bounded contemplated or completed repository change to identify decision-relevant affected code/contracts/artifacts/tests/docs/claims/authority/release/cross-repository surfaces, required verification or reconciliation, and bounded follow-up responsibilities without authorizing or executing those changes.
---

# change-impact-analysis

Use when a change may have consequential effects beyond its immediate edited
files or when a completion/closure claim depends on reconciling affected surfaces.

Produce:

`artifacts/change_impact_analysis.md`

## Responsibility

Construct an evidence-grounded **change impact decision space**.

The active semantic agent decides what is materially affected. Deterministic
validation checks representation/reference boundaries only.

## Inputs

Use:

1. explicit target change statement;
2. change state: `CONTEMPLATED | IMPLEMENTED | VERIFIED`;
3. exact target repository/source identity when available;
4. bounded scope;
5. repository evidence and explicit relationship/contract surfaces;
6. prior strategic/Campaign/execution evidence when decision-relevant.

## Procedure

### 1. Establish change and scope

State exactly what is changing/changed and what authority exists.

### 2. Gather smallest sufficient impact evidence

Inspect only evidence capable of changing implementation, verification,
reconciliation, closure, or authority.

### 3. Identify affected surfaces

Use categories:

`code | contract | artifact | test | documentation | claim | decision |
authority | repository_boundary | release | external_dependency`.

For each item record evidence, material impact, semantic-review need,
verification/reconciliation need, and authority boundary.

### 4. Identify explicit cross-repository impact

Only for caller-selected/authorized repository scope. Never discover/add targets
automatically.

### 5. Reconcile claim/verification consequences

Ask:

- what claim becomes stale or stronger?
- what verification is now required?
- what documentation/contract must remain current?
- does authority change? (Usually no.)
- does this reopen Level 3 or require Level 4 review?

### 6. Nominate bounded follow-up responsibilities

Only when evidence warrants them. Do not create a backlog from every impact.

### 7. State closure effect

Choose:

`NO_CLOSURE_EFFECT | ADDITIONAL_VERIFICATION_REQUIRED |
RECONCILIATION_REQUIRED | OWNER_DECISION_REQUIRED |
STRATEGIC_REASSESSMENT_REQUIRED | THESIS_REVIEW_REQUIRED`.

This is semantic agent judgment.

### 8. Validate

```bash
python scripts/validate-artifact.py change_impact_analysis artifacts/change_impact_analysis.md
python scripts/validate-change-impact-analysis.py artifacts/change_impact_analysis.md
```

## Laws

```text
reference occurrence != material impact
impact identified != change required
change required != change authorized
verification requirement != verification result
follow-up candidate != backlog item
cross-repo impact != automatic scope expansion
mechanical PASS != semantic truth
```
