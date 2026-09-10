# Product-Change Taxonomy

**Status:** Canonical descriptive taxonomy, Level 1/2 only  
**Important:** These labels do not authorize prioritization, implementation, routing, or promotion.

## Purpose

Product work is often described too loosely as "adding features." This taxonomy gives Sensemaking a more precise vocabulary for describing **what kind of product change is proposed, how it creates value, and what existing product surface it acts upon**.

The taxonomy is intentionally multi-axis. One change may legitimately receive one label from several axes.

## Axis 1 — Structural change type

### Net-new capability

Enables a user outcome the product could not previously support.

Example: exporting a Campaign as a portable bundle when no export mechanism existed.

### Feature extension

Broadens the scope, inputs, targets, contexts, or cases supported by an existing capability.

Example: extending single-repository Campaigns to support multiple repositories.

### Feature enhancement

Makes an existing feature/capability more useful without fundamentally changing its identity.

Example: richer Campaign handoff context.

### Integration

Connects the product to another system, environment, or workflow boundary.

Example: surfacing Campaign provenance in GitHub pull requests.

### Enabler / platform capability

Creates infrastructure or semantic foundation that unlocks later product changes rather than delivering the final user outcome alone.

Example: a stable Skill contract manifest supporting future domain packs.

### Quality improvement

Improves a quality attribute of an existing capability.

Examples: reliability hardening, performance improvement, portability hardening, better integrity checking.

### UX improvement

Reduces user/agent friction in accessing existing capability.

Example: one-command Campaign preflight.

### Automation

Removes or reduces manual work while preserving the same semantic authority boundary.

Example: mechanically packaging qualification evidence that previously required repetitive operator steps.

### Scale capability

Lets existing semantics survive larger workload, volume, duration, or topology.

Example: Campaign history inspection that remains usable across hundreds of transitions.

### Simplification / removal

Removes obsolete, duplicated, misleading, or costly product surface while preserving or improving user value.

Example: consolidating competing Skills that represent one canonical responsibility.

## Axis 2 — Value mechanism

### Add

Creates a new source of value.

### Deepen

Makes an existing capability more powerful, useful, trustworthy, or complete.

### Broaden

Extends value to more users, contexts, domains, repositories, or workflows.

### Connect

Creates value by composing previously separate capabilities or systems.

### Simplify

Reduces cognitive, operational, interaction, or setup cost.

### Harden

Makes existing value more reliable, safe, auditable, deterministic, or resilient.

### Accelerate

Reduces time, latency, or effort required to obtain the same value.

### Scale

Preserves useful behavior at larger size, duration, concurrency, or organizational scope.

### Enable

Creates prerequisite value that makes later changes feasible or less costly.

### Differentiate

Makes the product meaningfully harder to substitute because the combined experience or trust model becomes distinctive.

## Axis 3 — Target of change

A ProductChange may primarily affect:

```text
UserWorkflow
ProductCapability
Feature
SoftwareCapability
QualityAttribute
Platform/Foundation
Ecosystem/IntegrationBoundary
DeveloperWorkflow
OperationalWorkflow
FutureDevelopment
```

This axis prevents statements such as "we improved Campaigns" from hiding what actually changed.

## Axis 4 — Relationship to existing value

### Independent value

The change is useful largely on its own.

### Complementary value

The change makes another capability more valuable.

Example: Resume Capsule complements durable Campaign persistence.

### Multiplicative value

The combination of changes is substantially more useful than the sum of isolated parts.

Example:

```text
persistence
+ fresh-context handoff
+ portable evidence bundle
```

may create a much stronger continuity capability than any one feature alone.

### Foundational value

The change primarily enables future capabilities or reduces future implementation complexity.

### Defensive value

The change protects existing product value against failure, drift, misuse, inconsistency, or degraded trust.

Example: target snapshot integrity checks.

## Axis 5 — Product level

This axis distinguishes concepts that are often incorrectly treated as synonyms.

### Product need / outcome

The user problem or desired result.

### ProductCapability

What the product enables the user to accomplish.

### Feature

A product mechanism/surface realizing or exposing a capability.

### ProductChange

A modification to product behavior, quality, scope, or infrastructure.

### Initiative

A coordinated effort containing one or more ProductChanges in service of an outcome.

### Implementation

The technical mechanism used to realize a ProductChange.

Canonical direction:

```text
Need / outcome
    -> ProductCapability
    -> Feature(s)
    -> ProductChange(s)
    -> Implementation
```

The exact order can vary during discovery, but the concepts should not collapse into one label.

## Classification examples

| Change | Structural type | Value mechanism | Target | Value relation |
|---|---|---|---|---|
| Resume Capsule | enhancement / UX improvement | deepen + simplify | Campaign handoff workflow | complementary |
| Campaign inspect/diff | enhancement / observability | simplify + deepen | Campaign workflow | complementary |
| Harness qualification kit | automation / productization | simplify + harden | qualification workflow | complementary / defensive |
| Domain Pack foundation | enabler | broaden + enable | platform/future development | foundational |
| PM Wave 2 | feature extension | broaden | PM capability surface | independent + complementary |
| Portable Campaign bundle | net-new capability / extension | broaden + connect | Campaign continuity | multiplicative |
| Preflight | quality improvement | harden | Campaign transition workflow | defensive |
| Multi-repository Campaign | extension / scale capability | broaden + scale | Campaign target model | independent |
| Semantic Architecture | enabler / quality improvement | deepen + harden + enable | reasoning platform | foundational / defensive |

## Classification rules

1. Do not force a change into exactly one category if multiple axes genuinely apply.
2. Prefer one **primary structural type** plus secondary labels when communicating roadmap scope.
3. Keep value mechanism separate from implementation mechanism.
4. Keep maturity state separate from change type. `REPOSITORY_QUALIFIED` is not a feature category.
5. Keep product impact separate from engineering effort. A small implementation can create a new capability; a large refactor can create no net-new user capability.
6. An enabler should name which future capability or burden it enables/reduces. "Platform work" without a downstream value hypothesis is too vague.
7. A defensive change should name the product value or trust property it protects.
8. A reinforcing/complementary relation should identify the existing capability being strengthened.

## Relationship to prioritization

This taxonomy describes a proposal; it does not prioritize it.

A later prioritization model may consider evidence such as:

- severity of user problem;
- strategic fit;
- reach;
- confidence;
- implementation cost;
- risk;
- dependency leverage;
- qualification debt;
- trust impact.

But those are separate semantic dimensions and must not be inferred from labels such as `enabler` or `enhancement`.

## Promotion rule

This taxonomy remains descriptive until repeated workflows demonstrate that a particular relation needs durable machine-readable representation.

For example:

```text
"Resume Capsule reinforces Campaign persistence"
```

may remain prose until Skills repeatedly need to query, validate, or reason over `reinforces` as a structured relation.

Only then should the relation be considered for executable promotion.