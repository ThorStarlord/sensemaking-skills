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

### Capability Outcome Binding v1

`campaign capability-outcome bind` records one agent-selected opportunity as
the Campaign's governing capability outcome. The record joins the selected
claim, desired behavior, observable completion condition, source references,
assumptions, counterevidence, required capability claims and remaining
realization conditions.

The binding is stored under the existing Campaign state
`extensions.capability_outcome` key and committed as a lifecycle transition
that preserves the active responsibility. `campaign working-context` and
`resume-profile` project it, so a fresh agent can recover why the work exists
and what would count as realization without repeating opportunity discovery.
One Campaign holds one binding; changing the governing outcome requires a new
Campaign.

```text
agent-authored binding != opportunity verified
bound outcome != realized capability
source reference != admitted Campaign evidence
projection of assumptions != assumptions established
```

### Capability Outcome Bridge v1

`campaign capability-outcome bridge` joins the bound outcome to the selected
possibility's explicitly declared required-capability routes at one committed
revision. It exposes the possibility focus and realization, each capability's
reviewed components and relation evidence, mechanical Campaign/knowledge
capability-set alignment, documentary source-reference overlap, and a
`binding_source_evidence` presence check for each authored binding source
reference at the indexed revision.

```text
declared route != implemented capability
route alignment != readiness
bridge projection != next-action recommendation
```

The command is read-only. It does not rank routes, select an increment, inspect
component code or establish that any declared component satisfies its
capability.

### Capability Outcome Realization v1

`campaign capability-outcome assess` appends an evidence-linked assessment of
the binding's original realization conditions. It preserves the immutable
binding and the active responsibility, validates `file:` and `commit:`
evidence at the exact source revision, and requires exactly one status per
original condition. The binding continues to report
`realization: not_established`; the assessment reports evidence state, not
completion.

`working-context`, `resume-profile` and `capability-outcome bridge` project the
latest assessment. The bridge compares the assessment's source revision with
the indexed revision and flags `REALIZATION_ASSESSMENT_STALE`; it also flags
`KNOWLEDGE_REALIZATION_STALE` when the possibility's authored realization basis
was assessed at a different revision. The bridge projects the knowledge
graph's existing `claim_ceiling` and `scope`, so guidance-only and code-backed
components are not flattened into one implementation flag.

```text
assessment != completion
EVIDENCE_PRESENT != condition satisfied
condition status count != score
latest assessment != readiness verdict
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