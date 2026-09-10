# Product Management evidence model

## Purpose

PM methodologies often mix observations, assumptions, recommendations, and decisions in one document. The Sensemaking PM domain must keep those epistemic roles distinguishable so automation cannot manufacture confidence merely by completing a template.

## Source classes

PM artifacts may classify supplied source evidence with the following domain tags where useful:

- `repository_evidence` — product/repository documents, code, current configuration, durable project artifacts.
- `owner_intent` — explicit product/business preference or decision from the authorized owner.
- `customer_evidence` — interviews, surveys, observed customer behavior, support evidence, or other customer-originated data.
- `market_evidence` — competitors, public market material, benchmarks, market research.
- `operational_evidence` — analytics, usage, financial, sales, support, runtime, or business-operation observations.
- `experiment_evidence` — observations/results produced by an experiment with enough provenance to analyze.

These tags are PM-domain descriptive vocabulary. They do not replace Campaign `ClaimEvidence` or artifact-admission identities.

## Claim states

A PM artifact should use language consistent with what its source supports:

- **hypothesis/assumption** — proposition not established by supplied evidence;
- **evidence-backed finding** — interpretation that cites supplied evidence but remains an agent-authored interpretation;
- **measured observation** — value copied/derived from supplied empirical observation with provenance;
- **owner decision** — explicit owner intent/authorization, not inferred preference;
- **recommendation** — agent-authored next-action judgment.

Deterministic validation may reject a representation that claims a required empirical state without the required evidence references. It must not determine whether the interpretation is substantively true.

## Capability-specific minimums for the pilot

### `persona`

A persona may be produced with low evidence, but it must be labeled provisional/hypothetical rather than validated. Any `evidence_backed` persona claim needs at least one source reference.

### `discovery`

Discovery may frame problems and propose tests from partial evidence. It may not mark a hypothesis as validated merely because a validation plan exists.

### `interview-synthesis`

Material patterns and direct quotes must reference supplied interview sources. A synthesized pattern is agent interpretation; the evidence binding proves provenance, not truth.

### `opportunity-tree`

Every opportunity is either evidence-backed or explicitly an assumption. Scoring inputs that are invented rather than measured/owner-supplied must be labeled estimates.

### `hypothesis`

A hypothesis must be falsifiable. Its validation plan is not evidence that validation occurred. Success/kill thresholds may be proposed, but actual outcome claims require experiment/operational evidence.

## Missing evidence

Missing empirical evidence is not automatically a failure to produce a useful artifact. It changes the artifact's claim strength and may create an unresolved question or stop condition.

```text
missing evidence
!= evidence of absence
!= permission to invent evidence
```
