# Build-First Semantic Development Policy

**Status:** Active development policy  
**Scope:** Semantic Architecture construction after the first Reasoning Model operationalization  
**Empirical validation:** Deliberately deferred until the Construction Diminishing-Returns Gate is reached or an architecture choice becomes evidence-dependent

## Decision

Sensemaking continues bounded Semantic Architecture construction while the next missing capability can be justified from existing product contracts, known integrity gaps, and mechanically testable behavior.

The existing common-envelope experiment is preserved as a future empirical-validation protocol. It is **not** the current implementation gate.

The policy distinguishes:

```text
verification
= does the implementation satisfy its declared mechanical contract?

empirical validation
= does the architecture improve real agent work enough to justify its cost?
```

Verification remains continuous. Empirical validation may be deferred.

## Continuous verification remains mandatory

Every construction package still requires, where applicable:

- positive contract tests;
- negative/rejection tests;
- exact-head CI;
- package/install proof;
- integrity/provenance checks;
- fail-closed handling of malformed or ambiguous mechanical input;
- explicit semantic-authority limits.

Deferring empirical episodes is **not** permission to weaken mechanical qualification.

## Build authorization rule

A new construction package may proceed without a new empirical episode when most of the following are true:

1. a concrete missing capability or integrity boundary is already visible;
2. the proposed behavior composes with existing canonical concepts;
3. its mechanical correctness can be stated independently of semantic judgment;
4. useful negative/rejection cases are identifiable before implementation;
5. the package unlocks a new operator/agent capability or removes a known reconstruction burden;
6. implementation can remain backward-compatible or explicitly versioned;
7. no unresolved product-choice question must be answered by pretending to have empirical evidence.

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

**Semantic-authority pressure** — useful automation seems to require deterministic machinery to rank uncertainty, select the warranted responsibility/Skill, judge architecture, or decide semantic success.

## Decision rule

```text
Can the next architecture be justified primarily
from existing contracts + known missing capability?

YES -> build and mechanically qualify
NO  -> invoke empirical validation
```

## Deferred empirical protocol

The preserved common-envelope protocol should later compare normal artifacts with artifacts plus `semantic_reasoning_profile`, including fresh-context continuation, semantic reconstruction, unsupported-inference prevention, currentness preservation, duplication, validator friction, and coordination/token overhead.

Possible outcomes remain:

```text
A. retain the full companion profile;
B. retain it only at Skill/session boundaries;
C. extract a smaller shared envelope;
D. keep Reasoning Model methodology but retire the Level-3 profile;
E. split useful fields across Campaign, artifacts, and Skill methodology.
```

No construction package may silently assume one of these outcomes has already been empirically established.

## Permanent boundary

The build-first policy does not authorize a central reasoning engine, automatic semantic routing, automatic uncertainty ranking, automatic Skill selection, or semantic truth scoring.

The governing principle is:

> Build while architecture remains informative. Validate empirically when architecture stops being informative.
