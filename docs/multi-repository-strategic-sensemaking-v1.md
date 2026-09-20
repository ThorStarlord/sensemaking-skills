# Multi-Repository Strategic Sensemaking v1

**Status:** canonical Level-3 companion contract  
**Authority:** caller-selected repository set + semantic-agent judgment  
**Relationship to Campaigns:** may reuse explicit multi-target identities/relations as evidence; does not mutate Campaign target state

## Purpose

Analyze a deliberately selected set of repositories as one strategic product/system boundary.

```text
caller-selected repositories
+ governing intent
+ repository evidence
+ explicit cross-repository relations when available
        ↓
current multi-repository system model
        ↓
capability ownership / overlap map
        ↓
boundary tensions
        ↓
0–5 coherent multi-repository construction/allocation paths
        ↓
qualitative comparison
        ↓
decision-changing uncertainty
        ↓
BUILD / INVESTIGATE / DEFER / NO_CHANGE / OWNER_DECISION / THESIS_REVIEW
```

This answers questions such as:

- Which repository should own a capability?
- Is apparent duplication actually harmful or a valid separation?
- Should two repos remain independent, share a protocol, use an adapter boundary,
  move one capability, or consolidate?
- Which dependencies constrain the sequence of a multi-repository evolution?
- Which boundary decision is owner preference versus repository-answerable fact?

## Scope selection

Every target must be supplied explicitly. The artifact records stable aliases,
repository identities, source identities, roles, and evidence references.

```text
repository mentioned in evidence
!= repository automatically in scope

related repository exists
!= Sensemaking may discover/add it automatically
```

If another repository becomes decision-changing, return `OWNER_DECISION` or
bounded scope clarification rather than silently expanding scope.

## Relationship evidence

Reuse explicit Campaign relation classes when they exist:

```text
depends_on
provides_interface_to
consumes_interface_from
must_change_with
release_after
```

A Strategic Analysis may also record bounded cross-repository observations, but
these are semantic claims, not mutations to `multi-target-relations.jsonl`.

```text
relationship observed
!= Campaign relation persisted
Campaign relation valid
!= architectural truth
```

## Capability ownership map

For decision-relevant capabilities record:

- stable capability ID;
- current owner repository aliases;
- current state;
- evidence references;
- material overlap/duplication when present;
- boundary consequence.

Do not reduce ownership to a score or infer that duplication is automatically bad.

## Boundary/allocation paths

A path is a coherent future allocation of capabilities and interfaces across the
selected repository set.

Each path records:

- future system state;
- capability allocations;
- major boundary/interface changes;
- coarse cross-repository sequence;
- dependencies;
- what the path unlocks;
- material risks/tradeoffs;
- reversibility;
- evidence gaps.

Useful boundary patterns include, when genuinely supported:

- keep repositories independent;
- move a capability to a clearer owner;
- define a shared protocol/contract;
- introduce an adapter boundary;
- consolidate repositories;
- deliberately retain duplicated implementations.

These are search prompts, not required categories.

```text
boundary alternative
!= required path
construction path
!= backlog
allocation proposed
!= migration authorized
```

## Comparison

Use the existing Level-3 qualitative lenses:

1. mission relevance;
2. decision value;
3. blocking power;
4. evidence sufficiency / resolvability;
5. consequence of error;
6. deferral cost;
7. reversibility;
8. authority availability;
9. dependency;
10. smallest warranted intervention.

No numeric score, rank, or automatic winner.

## Transition to work

Only `BUILD` may nominate one bounded repository responsibility. It must also
state which target aliases it affects.

```text
selected path
!= repositories authorized for mutation
candidate multi-repo responsibility
!= cross-repo transaction plan
same dependency layer
!= parallel execution authorized
```

Execution uses existing Level-2/multi-target/executor surfaces only after
authority is established independently.

## Non-goals

No:

- automatic repository discovery;
- automatic target-set expansion;
- repository crawling outside explicit scope;
- deterministic best-boundary selection;
- numeric ownership/priority scores;
- automatic capability movement;
- cross-repository transaction/deployment/rollback coordinator;
- automatic worker scheduling;
- automatic merge/release/deploy;
- Campaign schema v3.
