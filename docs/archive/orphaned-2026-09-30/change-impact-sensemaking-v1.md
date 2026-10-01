# Change-Impact Sensemaking v1

**Status:** canonical engineering analysis contract  
**Control scope:** consequence/reconciliation analysis around a contemplated or completed repository change  
**Authority:** semantic-agent authored; no change authorization is granted by the artifact

## Purpose

Change-Impact Sensemaking asks:

> If this bounded change is contemplated or has occurred, which repository/product
> surfaces may need semantic review, mechanical verification, documentation
> reconciliation, authority review, or follow-up work before the relevant claim
> can safely close?

It sits beside execution rather than above strategy:

```text
bounded contemplated/completed change
        ↓
evidence-grounded affected surfaces
        ↓
semantic review / verification / reconciliation needs
        ↓
authority-sensitive consequences
        ↓
bounded follow-up responsibilities, when warranted
```

It is useful when the central implementation can be correct while adjacent
contracts, tests, documentation, claims, release surfaces, or cross-repository
interfaces may become stale.

## Scope

The analysis starts from an explicit change target and declared scope. It may use:

- repository evidence;
- explicit dependency/semantic maps;
- artifact/manifest/contract references;
- tests and CI contracts;
- ADR/product strategy authority;
- prior strategic/Campaign/execution artifacts;
- explicit multi-repository relationships when selected repositories are in scope.

It does not automatically crawl unrelated repositories or treat every reference
as decision-relevant impact.

## Impact categories

A decision-relevant affected surface may be classified as:

```text
code
contract
artifact
test
documentation
claim
decision
authority
repository_boundary
release
external_dependency
```

Categories organize the artifact; they do not determine severity or priority.

Each impact item states:

- stable surface ID;
- category;
- target reference;
- impact statement;
- evidence references;
- whether semantic review is required;
- verification/reconciliation needed;
- authority boundary when relevant.

## Impact reasoning

The semantic agent distinguishes:

```text
reference exists
!= material impact

material impact
!= code change required

code change required
!= authorized

verification needed
!= semantic conclusion predetermined
```

Use the smallest set of affected surfaces that can change implementation,
verification, closure, authority, or higher-scope decisions.

## Cross-repository impact

When explicitly selected repositories are affected, identify them by caller-
provided repository aliases/identities. Do not silently expand repository scope.

```text
cross-repository impact identified
!= transaction coordinator
!= target scope expanded automatically
```

## Follow-up responsibilities

The analysis may nominate bounded candidate responsibilities such as:

- update an affected contract;
- reconcile stale documentation;
- add finding-specific verification;
- re-run a release/currentness gate;
- revisit a strategic assumption;
- request an owner decision;
- prepare thesis review.

These are semantic recommendations, not automatic work items or authorization.

## Relationship to existing surfaces

- Semantic Architecture probes/reference audits supply mechanically bounded evidence.
- Strategic Repository Sensemaking owns repository-evolution path decisions.
- Strategic Reconciliation owns interpretation of returned Level-3 evidence.
- Campaign reconciliation owns durable Level-2 continuation/closure state.
- Change-Impact Sensemaking owns the **affected-surface decision space around a bounded change**.

## Non-goals

No:

- universal causal graph;
- automatic impact truth oracle;
- numeric severity/risk scoring;
- automatic issue/backlog generation;
- automatic code modification;
- automatic repository discovery;
- cross-repository transaction coordinator;
- automatic owner/thesis decisions;
- automatic merge/release/deploy/publication.
