# ADR 0029: Current Product Boundary of Sensemaking Skills

**Status**: ACCEPTED — owner-ratified 2026-09-11  
**Date**: 2026-09-11  
**Supersedes**: ADR 0014 — Product Boundary of Sensemaking Skills  
**Level**: Level 4 — Product Thesis / Strategy Revision

## Context

ADR 0014 correctly recorded the owner-ratified July 2026 boundary around repository diagnosis and a validated, human-reviewed `repository_sensemaking_brief`. Since then, Sensemaking has evolved into a broader shipped repository decision-support and control product with optional Campaign durability, continuation/reconstruction surfaces, explicit multi-repository target mechanics, bounded workflow-composition guidance, and higher-scope strategic-control contracts.

Keeping ADR 0014 as the current boundary would require treating product-facing shipped capabilities as merely internal support even though they are intentionally exposed and documented for users. Rewriting ADR 0014 in place would erase useful historical decision context.

The Level-4 review in `docs/product-boundary-reconciliation-v1.md` therefore selected `SUPERSEDE`.

## Decision

Sensemaking Skills is an **agent-native repository decision-support and control layer for software-engineering agents**.

### In current product scope

- repository sensemaking and evidence-grounded diagnosis;
- validated repository sensemaking artifacts, including `repository_sensemaking_brief`;
- responsibility-first reasoning support and explicit uncertainty/authority discipline;
- bounded capability discovery/inspection while the active agent owns semantic selection;
- optional durable Campaign state when continuation complexity warrants it;
- Campaign preflight, observability, Doctor, resume, handoff, transfer, rebinding, provenance, reconciliation support, and reconstructible completion;
- explicit multi-repository target identity and relationship representation without automatic repository discovery or transaction orchestration;
- static workflow-composition/golden-path guidance that does not select or execute a workflow;
- bounded mechanical semantic substrate, validation, conformance, and reference-integrity support;
- Level-3 Strategic Repository Evolution and Level-4 Product Thesis control contracts as product governance/support surfaces.

### Supporting but not independent semantic authority

The following support the product but do not become semantic controllers:

- deterministic validators, hashes, schemas, probes, manifests, and conformance checks;
- Campaign persistence and companion records;
- strategic-state representation validation;
- repository qualification and release-candidate checks.

### Outside current product scope

- a custom coding model or general coding-agent runtime;
- a deterministic semantic planner, `StrategicPlanner`, or `OuterLoopEngine`;
- automatic Strategic Frontier ranking;
- automatic responsibility, capability, Skill, workflow, repository, or product-thesis selection;
- general-purpose multi-repository commit/deploy/rollback transaction coordination;
- default direct third-party tracker mutation;
- autonomous merge, release, deployment, publication, or production operations;
- semantic truth claims derived from mechanical validation alone.

## Boundary law

The active coding agent remains the semantic controller. Deterministic machinery may expose, validate, preserve, and reconstruct explicit state but may not silently convert available information into strategic selection or authority.

```text
product surface available != surface warranted
capability available != capability selected
mechanically valid != semantically correct
same Campaign != atomic deployment unit
workflow shown != workflow recommended
```

## Relationship to ADR 0014

ADR 0014 is now `SUPERSEDED`, not rejected. It remains authoritative historical evidence for the product boundary that governed the July 2026 decision and related historical validation work.

Historical research/protocols may continue citing ADR 0014 when reconstructing the product boundary under which that evidence was produced. Current product-scope decisions should cite ADR 0029.

## Evidence ceilings

This ADR ratifies current scope; it does not strengthen empirical support claims.

Repository-qualified capabilities remain repository-qualified. Native-harness usefulness, portability in genuinely independent harnesses, comparative superiority, and general autonomous software-development capability remain unestablished where current evidence does not support them.

```text
ratified product boundary != product-value proof
```

## Consequences

- `docs/product-strategy.md` and current operating documentation use ADR 0029 as the product-boundary authority.
- ADR 0014 remains intact as historical decision evidence apart from its supersession marker.
- Existing non-goals against automatic semantic planning/routing and autonomous external authority remain in force.
- The broader product boundary does not create a standing roadmap; Level 3 still selects or declines repository responsibilities from current evidence.
- No runtime, API, Campaign schema, or empirical protocol change follows automatically from this ADR.

## Owner ratification

The owner explicitly approved the Strategic Outer Loop Precision v1 implementation plan on 2026-09-11, including the recommendation that ADR 0014 be superseded rather than retroactively rewritten. This ADR records the resulting operative Level-4 product-boundary decision.