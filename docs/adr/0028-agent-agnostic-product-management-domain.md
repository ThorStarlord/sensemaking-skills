# ADR 0028: Product Management is an agent-agnostic Campaign domain

**Status:** Accepted  
**Date:** 2026-09-10

## Context

Sensemaking contains historical/deprecated Product Management command identities and artifact relationships, while the current product has evolved toward a Campaign model in which the active agent owns semantic judgment and deterministic machinery owns representation, validation, provenance, integrity, authority checks, and reconstruction.

A separate MIT-licensed repository, `lucasgaravelli/pm-skills-claude-code`, provides a useful 27-command PM methodology library, but its runtime representation is Claude Code slash commands rather than current agent-native Sensemaking capabilities.

The product needs a decision about whether PM adaptation should revive the historical router, target a particular coding agent, or become a portable Campaign domain.

## Decision

Product Management will become a **first-class, coding-agent-agnostic Sensemaking Campaign domain**.

### Canonical semantic ownership

Canonical PM capabilities define responsibility, methodology, evidence requirements, output artifact, semantic limitations, authority requirements, and stop conditions without depending on a specific harness.

The active agent continues to own:

- consequential uncertainty;
- warranted responsibility;
- capability selection;
- evidence interpretation;
- semantic recommendation;
- advance/defer/close decisions.

Deterministic machinery continues to own only mechanically decidable contracts.

### Harness boundary

Harness-specific installation, discovery, invocation representation, vendor metadata, availability reporting, and native invocation evidence belong to adapters. Claude Code, Codex, OpenCode, generic Agent Skills, and future harnesses are not semantic authorities.

### Capability selection

PM capabilities are added to the current Campaign capability catalog as declared candidates. Catalog lookup may filter by an **agent-supplied responsibility type**. It must not infer responsibility from prose, rank candidates, or execute a candidate merely because it is registered.

### Upstream methodology

`lucasgaravelli/pm-skills-claude-code@21cbb2903d740d10fc65c667aea97d3ee8657349` is pinned as methodological provenance. Adapted capabilities evolve independently after import. The upstream list of 27 is a candidate inventory, not a required permanent taxonomy.

### Pilot

The first implementation slice is:

`persona -> discovery -> interview-synthesis -> opportunity-tree -> hypothesis`

expressed canonically as responsibilities:

`customer_understanding -> problem_discovery -> research_synthesis -> opportunity_mapping -> product_hypothesis`.

Expansion is gated by empirical dogfood.

## Invariants

```text
responsibility != capability
available capability != selected capability
selected capability != execution authority
artifact valid != conclusion true
artifact admitted != claim warranted
methodology applied != empirical validation
workflow authorized != external mutation authorized
canonical capability != harness representation
```

## Consequences

Positive:

- one PM semantic source can be exposed through multiple supported harnesses;
- Campaign evidence, lineage, handoff, and authority semantics remain reusable;
- the project avoids rebuilding the old Wayfinder semantic router;
- PM methodology can evolve independently from its Claude-specific source representation.

Costs:

- adapters and real-harness qualification remain necessary;
- some upstream prompts must be decomposed rather than copied verbatim;
- capability migration is deliberately slower than bulk prompt import.

## Rejected alternatives

### Restore the deprecated PM workflow router

Rejected because it would conflate historical catalog data with current semantic authority and conflict with the agent-owned Campaign control loop.

### Target Codex as the new canonical runtime

Rejected because replacing Claude coupling with Codex coupling does not create portability.

### Copy all 27 commands directly into `skills/`

Rejected because command text alone does not provide evidence semantics, artifact integrity, Campaign admission, or empirically tested portability.

## Follow-up authority

`docs/product-management/` owns PM-domain explanatory contracts. Existing Campaign, capability, harness-adapter, artifact-admission, and authority documents remain authoritative for shared infrastructure.
