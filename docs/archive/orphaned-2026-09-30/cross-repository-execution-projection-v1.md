# Cross-Repository Execution Projection v1

**Status:** post-RC2 development contract  
**Input authority:** explicit multi-target set and caller-authored relations only  
**Output:** deterministic read-only projection

## Purpose

Multi-repository Campaigns already preserve explicit target identities and
caller-authored relationships. This surface converts only the mechanically
ordering relation types into a readable prerequisite projection.

```text
explicit target set
+ explicit relations
-> deterministic precedence projection
!= execution plan
```

## Ordering semantics

Only two existing relation types create precedence:

```text
A depends_on B
=> B precedes A

A release_after B
=> B precedes A
```

The following remain descriptive and do not create ordering:

```text
provides_interface_to
consumes_interface_from
must_change_with
```

Sensemaking does not infer additional relationships.

## Precedence layers

The projection performs a deterministic topological layering over the declared
ordering edges.

For example:

```text
frontend depends_on backend
backend release_after shared

=> layer 0: shared
=> layer 1: backend
=> layer 2: frontend
```

A layer means only that no recorded ordering relation constrains members
relative to one another.

```text
same precedence layer != safe parallel execution
same precedence layer != work authorized
precedence projection != execution schedule
```

## Command

JSON:

```bash
sensemaking-skills campaign multi-target execution-view \
  --workspace /path/to/CMP-1 \
  --format json
```

Mermaid:

```bash
sensemaking-skills campaign multi-target execution-view \
  --workspace /path/to/CMP-1 \
  --format mermaid
```

The JSON payload explicitly reports:

- exact target identities and authority metadata;
- original explicit relations;
- derived prerequisite edges;
- deterministic precedence layers;
- descriptive non-ordering relations;
- `execution_plan_selected: false`;
- `parallel_execution_authorized: false`;
- `semantic_recommendation_included: false`.

Invalid target/relation companions fail closed rather than producing a partial
execution projection.

## Boundary

This feature is a view over explicit state. It does not schedule workers,
recommend an order, infer missing dependencies, coordinate commits/deployments,
or authorize cross-repository activation.
