# Strategic Continuity & Currentness v1

**Status:** canonical companion contract  
**Control level:** Level 3 — Strategic Repository Evolution  
**Authority:** subordinate to `docs/product-strategy.md`, ADR 0029, and Strategic Repository Sensemaking v1  
**Runtime posture:** authored semantic continuity + deterministic projection/currentness checks; no planner runtime

## 1. Purpose

Strategic Repository Sensemaking v1 produces an immutable analysis of a repository at a particular evidence boundary. Strategic Continuity v1 makes later analyses explicitly relate to earlier analyses without mutating the earlier artifact or creating a second strategic truth system.

```text
strategic_repository_analysis N
        ↓
later repository/evidence state
        ↓
strategic_repository_analysis N+1
        ↓
explicit continuity declaration
        ↓
compare / currentness / reassessment
```

The active semantic agent still owns whether a prior analysis remains useful, should be revised, or should be superseded. Mechanical tooling may only project declared differences and currentness facts.

## 2. Additive continuity fields

New analyses SHOULD provide:

```yaml
analysis_ref: "SRA-2026-09-20-001"
continuity:
  prior_analysis_ref: "SRA-2026-09-19-003"
  disposition: REVISE
  prior_selected_path_id: PATH-2
  reason: "A previously unresolved dependency is now established."
decision_assumptions:
  - assumption_id: ASSUMPTION-1
    statement: "The current executor boundary remains stable."
    evidence_refs:
      - docs/campaign-execution-interface-v1.md
    reassessment_triggers:
      - "Executor contract changes materially."
      - "Returned worker evidence can no longer be bound to exact targets."
```

Existing qualified analyses remain valid without these fields.

## 3. Continuity dispositions

The semantic author may declare exactly one of:

- `NEW` — no prior strategic analysis is being continued;
- `REAFFIRM` — the prior strategic judgment remains materially intact;
- `CONTINUE` — the selected path remains active and a later capability transition is being considered;
- `REVISE` — material strategic content changed while remaining in the same broad trajectory;
- `SUPERSEDE` — the prior analysis is no longer the current strategic basis;
- `CLOSE` — the prior construction trajectory reached a justified stopping state.

```text
continuity disposition
!= mechanical verdict
!= owner ratification
!= implementation authorization
```

## 4. Construction-path continuation

Each construction path MAY declare:

```yaml
assumptions:
  - "The current public API remains the integration boundary."
reassessment_triggers:
  - "A concrete consumer requires a different boundary."
```

A later analysis uses `continuity.prior_selected_path_id` plus its own `selected_path_id` to make path continuation or change reconstructible.

```text
path continued
!= backlog committed
path closed
!= product thesis retired
```

### 4A. Lightweight path-transition identity

When a selected construction path spans several conceptual capability changes,
the path MAY declare stable transition references:

```yaml
path_id: PATH-2
path_transitions:
  - transition_ref: PATH-2/T1
    transition: "isolated analyses -> explicit strategic lineage"
  - transition_ref: PATH-2/T2
    transition: "lineage -> typed mechanical currentness"
```

A strategic analysis may optionally identify
`candidate_path_transition_ref` for the conceptual transition its candidate
bounded responsibility is intended to advance. Strategic reconciliation may
later record an authored transition effect:

`ESTABLISHED | PARTIAL | NOT_ESTABLISHED | SUPERSEDED | NO_CONCLUSION`.

```text
path transition != roadmap item
path transition != backlog item
path transition != authorized responsibility
transition effect != project status
transition established != next transition selected
```

Scheduling/project-management fields are intentionally rejected.

## 5. Decision assumptions

Decision assumptions are the smallest premises worth remembering because their failure could materially change the strategic judgment.

They are not probabilities, hidden beliefs, confidence scores, or a generic knowledge database.

Each assumption carries:

- stable `assumption_id`;
- semantic statement;
- evidence references;
- one or more reassessment triggers.

A trigger states **when the decision should be reconsidered**, not what the reconsidered decision must be.

## 6. Deterministic strategy projections

The root CLI exposes:

```text
sensemaking-skills strategy inspect
sensemaking-skills strategy paths
sensemaking-skills strategy uncertainty
sensemaking-skills strategy assumptions
sensemaking-skills strategy compare
sensemaking-skills strategy drift
sensemaking-skills strategy history
sensemaking-skills strategy graph
```

These commands operate only on already-authored `strategic_repository_analysis` artifacts.

### `strategy compare`

Reports declared representation changes such as:

- capability-state changes;
- path additions/removals/material representation changes;
- selected-path changes;
- disposition changes;
- decision-changing uncertainty changes;
- continuity metadata on the newer analysis.

It does not decide which analysis is better.

### `strategy drift`

May mechanically compare:

- the recorded source identity with current Git HEAD when the identity is mechanically comparable;
- relative repository evidence references with their recorded Git version when
  the source identity is a resolvable commit;
- explicitly declared `governing_authority_refs` with their recorded Git version;
- current filesystem presence for addressable local references.

The bounded typed observation vocabulary is:

```text
SOURCE_IDENTITY_CHANGED
EVIDENCE_REF_MISSING
EVIDENCE_REF_CHANGED
GOVERNING_AUTHORITY_REF_CHANGED
```

These are observations, not semantic dispositions. In particular, a changed
governing-authority file does not mechanically establish that the governing
commitment changed in a decision-relevant way.

It deliberately reports:

```text
currentness_observations = [...]
semantic_consequence_inferred_by_command = false
strategy_invalidated_by_command = false
reanalysis_required_by_command = false
```

Because:

```text
currentness observation
!= semantic consequence

repository changed
!= prior strategy wrong

evidence path missing
!= semantic claim false

drift detected
!= reanalysis automatically warranted
```

### `strategy history` and `strategy graph`

These commands accept explicitly supplied strategic-analysis and reconciliation
artifacts. They preserve caller order and project only authored relationships.

`strategy history` renders a textual sequence of declared analyses,
continuity, selected paths, assumptions, path transitions, and reconciliation
effects.

`strategy graph` renders the same declared relationships as Mermaid.

```text
history order != strategic superiority
graph edge != causal truth
graph projection != recommendation
projection != strategy mutation
```

The commands do not discover strategic artifacts automatically, infer missing
chronology, rank strategies, or connect reconciliation to a later analysis
unless the underlying authored artifacts provide the relationship.

## 7. Relationship to strategic reconciliation

Strategic Continuity records **what changed between strategic analyses**.

A later Strategic Reconciliation artifact may explain **what returned evidence means for a prior decision**.

```text
continuity
= relationship between authored strategic states

reconciliation
= semantic interpretation of returned evidence
```

Neither replaces the other.

## 8. Strategic reassessment bridge

Strategic Continuity provides reconstructible lineage, assumptions, triggers, compare,
and drift/currentness facts. Learning / Reconciliation owns the semantic interpretation
of consequential returned evidence.

```text
assumption / reassessment trigger
-> observation, result, or currentness evidence
-> is it decision-changing?
   -> no: NO_MODEL_CHANGE / continue
   -> yes: Learning / Reconciliation
            -> confirm / revise / open uncertainty / change responsibility
            -> REOPEN_STRATEGY only when Level-3 state is materially changed
```

When durability is warranted, `strategic_reconciliation` records the interpretation;
it does not mutate the earlier strategic analysis.

```text
drift detected
!= strategy invalid

drift detected
!= semantic reassessment automatically required

reassessment trigger observed
!= strategic assumption falsified

reassessment trigger observed
!= strategy automatically changed

REOPEN_STRATEGY
!= BUILD

THESIS_REVIEW_REQUIRED
!= thesis ratified
```

The broader ownership crosswalk is
`docs/adaptive-semantic-control-architecture-v0.md`.

## 9. Boundaries

Strategic Continuity v1 does not add:

- StrategicPlanner or `OuterLoopEngine`;
- numeric strategy/path/warrant scoring;
- roadmap/project-management status from path transitions;
- automatic chronology or causal inference from strategic history;
- automatic path selection;
- automatic Campaign creation;
- automatic repository discovery;
- generic belief/state database;
- Campaign schema v3;
- automatic Level-4 thesis revision;
- merge/release/deploy/publication authority.

The governing invariant remains:

> **The semantic agent owns strategic judgment; deterministic machinery owns only mechanically decidable projection, identity, and currentness facts.**