# Product Management qualification levels

## Purpose

Product Management capability implementation may continue before native-harness dogfood is complete, provided the product claim remains explicit about what has and has not been proven.

This document separates **implementation maturity** from **empirical promotion**. It does not weaken artifact validation, Campaign integrity, repository CI, authority boundaries, or evidence-shape contracts.

## Maturity states

### CANDIDATE

A PM methodology has been selected for adaptation and has a canonical Sensemaking capability design, but repository integration may still be incomplete.

A candidate may not be presented as repository-qualified or empirically qualified.

### REPOSITORY_QUALIFIED

A capability is repository-qualified when, where applicable:

- its canonical agent-agnostic Skill implementation exists;
- its required artifact contract is defined or reconciled;
- positive and rejection validation pass;
- Campaign capability registration is current and unranked;
- artifact admission / lineage / handoff behavior is covered where applicable;
- supported adapter representations derive from the canonical source without semantic forks;
- product packaging/install checks pass;
- required repository CI passes on the exact candidate head.

Repository qualification proves implementation and deterministic integration properties. It does **not** prove native harness discovery/invocation, cross-harness empirical portability, customer truth, strategic correctness, or real-world effectiveness.

### NATIVE_HARNESS_QUALIFIED

A repository-qualified capability becomes native-harness-qualified only after at least one supported real coding-agent harness:

1. discovers the canonical capability through its native mechanism;
2. invokes it on a real bounded task;
3. preserves the expected responsibility, evidence, artifact, authority, and stop semantics;
4. produces preserved attempt evidence without manual repair being hidden as success.

### PORTABILITY_QUALIFIED

A native-harness-qualified capability becomes portability-qualified only after an equivalent bounded responsibility is exercised through a second supported harness and material semantic invariants remain equivalent.

Natural-language prose may differ. Responsibility, evidence rules, artifact identity, validator identity, authority boundary, Campaign representation, and stop semantics must not materially diverge.

### PROMOTED

Promotion is an explicit product/release decision made only after the evidence required for the intended claim exists.

Promotion may be scoped. A capability can be promoted for one supported harness while portability remains pending if product documentation states that narrower support claim explicitly.

## Policy

The PM program uses the following rule:

```text
repository qualification gates continued implementation
native-harness qualification gates native-harness support claims
portability qualification gates cross-harness portability claims
promotion gates stable/support positioning
```

Therefore:

```text
dogfood before promotion
!=
dogfood before expansion
```

New PM capabilities may move from `DEFER` to implementation when they are separately authorized and repository architecture can support them without speculative infrastructure expansion. They must remain clearly marked as unpromoted until the relevant empirical gates are completed.

## Claims that remain forbidden without empirical evidence

Repository qualification alone may not establish:

- that Claude Code, Codex, OpenCode, or another native harness actually discovered/invoked the Skill;
- that a fresh native coding-agent context reconstructed the Campaign correctly;
- that equivalent semantics survived a second native harness;
- that a persona represents the market;
- that a problem is validated by customers;
- that a strategy is correct;
- that product-market fit was measured without actual PMF evidence;
- that an A/B test succeeded without observations;
- that pricing, GTM, or launch recommendations are effective.

## Qualification debt

Deferred empirical validation is tracked as **qualification debt**, not implementation failure.

Each repository-qualified but unpromoted capability should retain:

- current maturity state;
- native-harness qualification status;
- portability qualification status;
- empirical evidence gaps;
- any product claim ceiling;
- dogfood references when attempts eventually exist.

Qualification debt must remain visible in PM status/handoff documentation and must not be silently converted into PASS.