# Campaign Usability & Composition v1

**Status:** owner-authorized repository-only/hermetic construction package  
**Empirical experiments:** none required or performed  
**Campaign schema:** unchanged (v2)

## Purpose

Compose existing Campaign primitives into lower-friction deterministic surfaces without giving the product semantic routing authority.

## Delivered surfaces

### Resume Capsule v2

`campaign resume-profile` adds explicit `minimal`, `working`, and `audit` projections. `--max-items` applies deterministic tail-preserving bounds and reports omitted counts. The existing `campaign resume-context` v1 surface remains backward compatible.

```text
progressive disclosure != semantic summarization
bounded output != evidence ranking
```

### Capability Context v1

`campaign capability-context --responsibility-type <explicit-type>` enumerates compatible declared capabilities only after the active agent supplies the responsibility classification.

```text
catalog compatibility != capability selection
availability != authorization
```

### Uncertainty Relationships v1

`campaign uncertainty-relate`, `campaign uncertainty-show`, and `campaign uncertainty-graph` add an append-only relationship companion for explicitly authored `depends_on`, `blocks_decision`, `introduced_by_transition`, `resolved_by_transition`, and `supersedes` relations.

`CampaignState.active_uncertainty` remains current authority. No score, ranking, or automatic next uncertainty is introduced.

### Bundle Inspection v1

`campaign bundle-inspect`, `campaign bundle-resume-context`, and `campaign bundle-graph` verify bundle integrity and project state through an ephemeral internal workspace before any durable import destination is created.

```text
bundle verified != import authorized
bundle projected != durable import performed
```

### Campaign Inventory v1

`campaign inventory --root <campaign-root>` enumerates direct child Campaign workspaces, current state, target identity when present, active responsibility, last transition, and mechanical integrity status.

```text
inventory != prioritization
```

## Boundaries

This package does not add:

- automatic responsibility or capability selection;
- automatic uncertainty ranking;
- semantic summarization;
- hidden reasoning reconstruction;
- Campaign schema v3;
- external/native-harness execution;
- new experiment state.

Repository qualification proves only the declared mechanical contracts.