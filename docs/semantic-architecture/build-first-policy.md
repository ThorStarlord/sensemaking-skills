# Build-First Semantic Development Policy

**Status:** Active post-Phase-10 development policy  
**Scope:** Semantic Architecture construction after the qualified Phase 10 Outcome A  
**Further empirical validation:** Intentionally deferred until the Construction Diminishing-Returns Gate is reached or a consequential architecture choice becomes evidence-dependent

## Decision

Phase 10 already ran three real-repository episodes and selected **Outcome A**: keep `semantic_reasoning_profile` as an optional companion audit/reconstruction artifact. That result remains valid and is not reopened by this policy.

After that experiment, Sensemaking resumes bounded Semantic Architecture construction while the next missing capability can be justified from existing product contracts, known integrity gaps, and mechanically testable behavior.

The policy distinguishes:

```text
verification
= does the implementation satisfy its declared mechanical contract?

empirical validation
= does the architecture improve real agent work enough to justify its cost?
```

Verification remains continuous. **Additional** empirical validation may be deferred.

## Continuous verification remains mandatory

Every construction package still requires, where applicable:

- positive contract tests;
- negative/rejection tests;
- exact-head CI;
- package/install proof;
- integrity/provenance checks;
- fail-closed handling of malformed or ambiguous mechanical input;
- explicit semantic-authority limits.

Deferring new empirical episodes is not permission to weaken mechanical qualification or reinterpret Phase 10 beyond its evidence.

## Build authorization rule

A new construction package may proceed without a new empirical episode when most of the following are true:

1. a concrete missing capability or integrity boundary is already visible;
2. the proposed behavior composes with existing canonical concepts;
3. mechanical correctness can be stated independently of semantic judgment;
4. useful negative/rejection cases are identifiable before implementation;
5. the package unlocks a new operator/agent capability or removes a known reconstruction burden;
6. implementation can remain backward-compatible or explicitly versioned;
7. no unresolved product-choice question must be answered by pretending to have empirical evidence.

This policy deliberately permits construction beyond the stricter pre-Phase-11 gate that existed immediately after Phase 10. That change is an owner-authorized development strategy, not a retroactive claim that Phase 10 empirically validated later architecture.

## Construction Diminishing-Returns Gate

Construction pauses for empirical validation when one or more signals become decision-critical and repeated construction no longer resolves them.

### Gate signals

**Competing architectures** — two or more plausible designs remain and repository reasoning alone cannot determine which produces better agent work.

**Abstraction without capability** — most proposed changes add vocabulary, wrappers, metadata, schemas, or layers without unlocking a concrete capability.

**Speculative fields** — new durable fields are justified primarily by “might be useful later.”

**Formalization outpaces consumption** — executable concepts accumulate faster than real Skills/operators consume them.

**Maintenance dominates value** — schema migrations, synchronization, adapters, and documentation churn become the main work while capability growth slows.

**Behavioral question becomes primary** — the decisive question becomes “will agents actually use or benefit from this?” rather than “can this mechanical capability be correctly provided?”

**Persistent placement ambiguity** — repeated work cannot resolve whether semantic state belongs in Skill methodology, a companion artifact, a canonical artifact, or Campaign state.

**Semantic-authority pressure** — useful automation appears to require deterministic machinery to rank uncertainty, select the warranted responsibility/Skill, judge architecture, or decide semantic success.

## Decision rule

```text
Can the next architecture be justified primarily
from existing contracts + a known missing capability?

YES -> build and mechanically qualify
NO  -> invoke empirical validation
```

## What Phase 10 already established

Do not repeat Phase 10 merely because new construction exists. Its current qualified conclusions are:

```text
semantic_reasoning_profile = optional companion artifact
mandatory universal embedding = not warranted
Campaign admission/promotion = not warranted by Phase 10
semantic truth remains agent/human judgment
```

Later construction can add new mechanical capabilities without claiming those capabilities were empirically validated by the Phase 10 episodes.

## Future empirical validation

When the diminishing-returns gate is eventually triggered, future studies may examine:

- whether mechanical probes reduce repeated repository inspection;
- whether Repository Semantic Map reuse reduces cross-Skill reconstruction;
- whether optional semantic companion state improves fresh-context continuation;
- whether Resume Capsules and bundles materially improve portability;
- whether Skill Contract Manifests/Domain Packs reduce integration drift;
- token/coordination overhead and schema-gravity effects;
- native-harness behavior where relevant.

Possible results include retention, narrowing, redistribution, or retirement of newly built layers. Construction is reversible; architecture is not declared successful merely because it exists.

## Permanent boundary

The build-first policy does not authorize a central reasoning engine, automatic semantic routing, automatic uncertainty ranking, automatic Skill selection, semantic truth scoring, or ontology-driven mutation authority.

The governing principle is:

> **Build while architecture remains informative. Validate empirically when architecture stops being informative.**
