# Construction Path Synthesis v1

**Status:** canonical reference for `strategic-repository-analysis`  
**Scope:** Level-3 path generation and comparison  
**Authority:** semantic guidance; does not select or authorize implementation

## 1. Purpose

A construction path is a coherent repository-evolution trajectory from current
evidence to a materially different future capability state.

```text
construction path
= future state
+ why plausible from current evidence/intent
+ Strategic Frontier grounding
+ capabilities built on
+ required capabilities
+ coarse sequence
+ dependencies
+ what becomes possible
+ risks / tradeoffs
+ reversibility
+ evidence gaps
+ decision-relevant assumptions when useful
+ reassessment triggers when useful
```

A path is not a feature list, issue backlog, roadmap commitment, or numeric
option score.

## 2. Generate paths from repository tensions, not categories

Start with the current-system model, capability map, Strategic Frontier, and
governing mission.

Generate another path only when it represents a materially different answer to
the repository-evolution decision.

Common *shapes* can help the agent notice alternatives:

- deepen the current product around its existing core;
- broaden into an adjacent capability or user problem;
- consolidate/simplify duplicated or overgrown surfaces;
- productize an internal capability that has become strategically central;
- shift an architectural/control boundary to unlock future development;
- deliberately defer construction while resolving a decision-changing premise.

These are search prompts, not required categories. Do not force one path per
shape.

```text
path diversity
!= category coverage
```

### 2A. Apply the Strategicity Gate before path generation

Do not turn every useful repository action into a Level-3 future.

Before a tension can generate a construction path, ask whether resolving it
could materially change at least one of:

- repository/product future capability state;
- product boundary;
- major architecture/control boundary;
- major dependency structure;
- authority or thesis commitment;
- materially different future development that becomes possible.

If none changes, keep the finding at the appropriate lower control level.

```text
repository-relevant work
!= strategic repository evolution

maintenance repair
!= construction path

bounded work can be warranted
without Level-3 BUILD
```

For new `schema_version: 2` analyses, every Strategic Frontier entry records
evidence references, affected capability identifiers, and a semantic
`strategic_consequence`; every construction path names its `frontier_refs`
and capability identifiers. Mechanical tools validate only the declared
relationships.

## 3. Minimum path distinctness

Two paths are materially distinct when choosing one would change at least one of:

- the future product/capability state;
- major dependencies;
- the order in which foundational capabilities must be built;
- the authority or thesis commitment required;
- the main risk accepted;
- what later work becomes possible.

Renaming the same sequence is not a second path.

## 4. Path count

Prefer 2–5 paths when the repository genuinely admits multiple futures.

Use one path when:

- the governing commitment already constrains the future strongly;
- alternative paths are outside current scope;
- alternatives differ only in implementation detail;
- generating more would be performative.

Use zero paths when current evidence/authority does not support even one coherent
construction trajectory yet, or when the semantic disposition is reached before a
construction choice is meaningful.

Examples include:

- `NO_CHANGE` with no warranted construction;
- `OWNER_DECISION` where owner preference defines the future;
- `THESIS_REVIEW` where Level 4 must resolve the product boundary first;
- `INVESTIGATE` where a decision-changing premise must be resolved before coherent
  paths can be formed.

```text
0–5 construction paths
= valid strategic-alternative cardinality

BUILD
-> at least one path
-> selected real path

zero paths
!= missing required ceremony
```

Do not create an artificial “do nothing” path. `NO_CHANGE` and `DEFER` are
strategic dispositions, not filler alternatives.

## 5. Capability-state grounding

Every path must connect to the capability map.

- `ESTABLISHED` capabilities may be foundations.
- `PARTIAL` capabilities may be completed or deliberately left partial.
- `MISSING` capabilities matter only when a path actually requires them.
- `DEFERRED` capabilities need a reason for promotion before becoming path work.
- `BLOCKED` capabilities expose an external/authority/dependency condition.
- `CLAIMED_UNVERIFIED` capabilities cannot be assumed as foundations until the
  claim is resolved when decision-changing.
- `OUT_OF_SCOPE` capabilities cannot silently become path requirements.

```text
missing capability
!= strategic priority

path requires capability
+ path is warranted
!= capability implementation automatically authorized
```

## 6. Coarse construction sequence

The sequence should describe capability-level dependencies, not implementation
tickets.

Good:

```text
make narrative identity explicit
-> expose stable architecture contract
-> add guided beginner flow
-> qualify end-to-end continuity
```

Too low-level:

```text
edit file A
add class B
rename function C
write test D
```

Detailed task decomposition belongs after strategic selection.

## 7. Qualitative comparison

Compare every material path through the canonical Level-3 lenses:

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

For new `schema_version: 2` artifacts, compare through these nine strategic
lenses. The legacy v1 tenth lens `smallest_warranted_intervention` remains
valid only for backward compatibility; v2 derives the smallest warranted
intervention after strategic disposition/path selection.

For each lens, explain what matters and why. Do not use numbers, stars, weighted
totals, tiers, or pseudo-quantitative labels as substitutes for reasoning.

```text
strategic comparison
-> disposition/path judgment
-> smallest warranted intervention

small intervention
!= strategically preferable path
```

A comparison may reveal:

- one path is sufficiently warranted;
- a specific uncertainty must be resolved first;
- multiple paths remain viable but the choice is owner preference;
- all paths should be deferred;
- current state is sufficient and no change is warranted;
- the real conflict is Level-4 thesis scope.

## 8. Decision-changing uncertainty

After comparison, ask:

> Which unresolved premise could make the current disposition materially
> different?

Do not list every unknown.

Use Inquiry Policy v0 to decide whether that premise deserves additional
evidence now.

Examples:

```text
repository evidence can resolve it
-> bounded repository inquiry

real-user/runtime behavior is required
-> empirical source, if authorized

the distinction is preference / risk appetite / product commitment
-> owner intent

the fact lives outside repository authority
-> external environment
```

```text
uncertainty identified
!= investigation automatically warranted
```

## 9. Strategic synthesis

The synthesis should explain the relationship between evidence and disposition,
not merely repeat path descriptions.

A good synthesis answers:

- Which differences between paths are decision-relevant?
- Which assumptions are already well grounded?
- Which gaps matter enough to change commitment?
- Why is the selected disposition proportional to current evidence?
- Why would a more ambitious intervention be premature?

## 9A. Path assumptions and continuation

A path may name the premises it depends on and observable conditions that should
cause its warrant to be reconsidered.

```text
assumption
= premise material to this path judgment

reassessment trigger
= condition that should cause a fresh semantic review

trigger observed
!= automatic path reversal
```

A later strategic analysis may explicitly `REAFFIRM`, `CONTINUE`, `REVISE`,
`SUPERSEDE`, or `CLOSE` the prior analysis/path relationship. Do not convert
this into progress percentages or a roadmap state machine.

## 10. Transition to bounded work

Only `BUILD` selects a candidate repository-level responsibility.

That transition is:

```text
strategic path selected semantically
-> smallest warranted repository responsibility nominated
-> authority checked independently
-> Level 2 / execution only if authorized
```

`INVESTIGATE` nominates a bounded evidence-producing responsibility.

`OWNER_DECISION` names the owner decision.

`THESIS_REVIEW` escalates the affected Level-4 commitment.

`DEFER` and `NO_CHANGE` create no implementation task by default.

## 11. Anti-patterns

Do not:

- convert maintenance, currentness repair, or every useful repository action into a strategic path;
- convert every gap into a path;
- make path names disguise one shared implementation sequence;
- generate a backlog and call it strategy;
- equate more missing capability with higher priority;
- rank paths numerically;
- treat repository facts as owner preferences;
- assume a path recommendation authorizes implementation;
- continue decomposing after `OWNER_DECISION` or `THESIS_REVIEW` merely to
  maintain momentum.
