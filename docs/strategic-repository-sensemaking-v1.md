# Strategic Repository Sensemaking v1

**Status:** canonical product contract  
**Control level:** Level 3 — Strategic Repository Evolution  
**Authority:** subordinate to `docs/product-strategy.md`, ADR 0029, and the Four-Level Control Model  
**Owner direction:** Issue #401  
**Runtime posture:** semantic-agent reasoning + mechanically validated artifact; no strategic planner runtime

## 1. Purpose

Strategic Repository Sensemaking v1 turns repository evidence into an explicit,
reconstructible strategic decision space.

It answers:

> Given this repository, its governing intent, current capabilities, evidence
> ceilings, and material constraints, what coherent ways could the repository
> evolve from here, what distinguishes those paths, and what direction or
> inquiry is warranted now?

This surface sits between repository diagnosis and bounded implementation:

```text
repository + owner intent
        |
current system model
        |
capability / limitation map
        |
strategic frontier
        |
candidate construction paths
        |
qualitative path comparison
        |
decision-changing uncertainty
        |
strategic synthesis
        |
warranted direction / inquiry / no change
        |
candidate repository responsibility
        |
existing Level-2 / execution surfaces when separately authorized
```

## 2. Core boundary

Strategic Repository Sensemaking is **not** a deterministic planner.

```text
strategic analysis != implementation authorization
construction path != backlog
path comparison != numeric ranking
semantic recommendation != deterministic planner output
mechanically valid artifact != strategy correct
repository evidence != owner intent
```

The active semantic agent owns:

- interpretation of repository evidence;
- generation of plausible construction paths;
- qualitative comparison;
- identification of decision-changing uncertainty;
- strategic synthesis;
- the semantic disposition.

Deterministic machinery may validate only mechanically decidable representation
facts such as required fields, identifiers, enums, references, path integrity,
and explicit anti-scoring constraints.

## 3. Relationship to repo-sensemaker

`repo-sensemaker` remains the diagnostic repository-understanding capability.

It asks primarily:

- what is this repository?
- what is strong or weak?
- what is missing or contradictory?
- what is the weakest consequential boundary?
- what evidence supports that diagnosis?

`strategic-repository-analysis` asks a different Level-3 question:

- what coherent futures are now plausible?
- how would each future be constructed?
- what does each path build on and require?
- what does each path unlock?
- what could make the current strategic judgment wrong?
- what strategic direction, inquiry, deferral, or no-change disposition follows?

A repository analysis may consume a fresh `repository_sensemaking_brief`, but it
may also inspect the repository directly when the brief would merely duplicate
already-current evidence.

```text
diagnosis available != strategic analysis required
strategic analysis requested != weakest-boundary brief sufficient
```

## 4. Current-system model

The analysis first reconstructs the repository as a product/system rather than
as a list of files.

The model should distinguish:

- governing product purpose / owner intent;
- major user-facing and agent-facing capabilities;
- architectural/control surfaces;
- qualification and evidence surfaces;
- relevant dependencies and constraints;
- current release/development posture when material;
- claim ceilings.

The current-system model is descriptive evidence synthesis. It must distinguish
verified repository state from owner-supplied intent and inference.

## 5. Capability / limitation map

Capabilities use the following bounded semantic states:

| State | Meaning |
| --- | --- |
| `ESTABLISHED` | Repository evidence shows the capability is implemented and currently supported at the stated claim level. |
| `PARTIAL` | A meaningful subset exists but material scope is absent or incomplete. |
| `MISSING` | The capability is materially absent and relevant to at least one plausible path. |
| `DEFERRED` | The capability/direction is explicitly postponed or requires evidence/authority before promotion. |
| `BLOCKED` | Progress depends on an unavailable external, authority, dependency, or environment condition. |
| `CLAIMED_UNVERIFIED` | Documentation/claims exist but current evidence is insufficient to treat the capability as established. |
| `OUT_OF_SCOPE` | The capability is deliberately outside the governing product boundary or selected analysis scope. |

The map is not a maturity score. Multiple capabilities with different states may
coexist without implying a single scalar level.

## 6. Strategic frontier

The Strategic Frontier is the set of current repository/product boundaries that
could materially change progress toward the governing mission.

Before admitting a tension, apply the Strategicity Gate: resolving the boundary
must be capable of materially changing a future capability state, product
boundary, major architecture/control boundary, major dependency structure,
authority/thesis commitment, or materially different future development that
becomes possible.

A local repair, stale status projection, routine maintenance action, or
already-selected implementation task may warrant work without becoming Level 3.

```text
idea exists != frontier item
repository issue exists != strategic frontier
bounded repair != construction path
frontier item != implementation commitment
frontier item != priority score
```

For new `schema_version: 2` analyses, each frontier entry declares
`evidence_refs`, `affected_capability_ids`, and `strategic_consequence`.
The validator checks these declarations mechanically; the active semantic agent
still decides whether the consequence is genuinely strategic.

## 7. Candidate construction paths

A **construction path** is a coherent repository-evolution trajectory: a future
state plus the major capability sequence and dependencies needed to reach it.

A path is not a feature list or roadmap.

Each material path should state:

- stable path identifier and name;
- future state;
- why this path is plausible from current evidence;
- Strategic Frontier entries it responds to;
- capabilities it builds on;
- new capabilities or changes it requires;
- coarse construction sequence;
- dependencies / prerequisites;
- what the path unlocks;
- material risks or tradeoffs;
- reversibility characteristics;
- evidence gaps / assumptions that matter.

Prefer **2–5 paths** when multiple futures are genuinely plausible. A single path
is valid when only one coherent construction trajectory is materially represented.

**Zero paths is also valid** when current evidence/authority does not support a
meaningful construction trajectory yet, or when the strategic disposition is reached
without selecting a construction direction (for example `NO_CHANGE`,
`OWNER_DECISION`, `THESIS_REVIEW`, or an investigation that must precede path
formation).

```text
construction_paths: []
!= analysis failure

zero real paths
> one manufactured path

BUILD
-> at least one real path
-> selected_path_id references that path
```

Do not manufacture alternatives merely to fill a template.

New `schema_version: 2` paths make grounding explicit through
`frontier_refs`, `why_plausible`, `builds_on_capability_ids`, and
`required_capability_ids`. Referential integrity is mechanically checkable;
strategic quality is not.

## 8. Qualitative comparison

Compare new v2 construction paths through nine strategic lenses:

1. mission relevance;
2. decision value;
3. blocking power;
4. evidence sufficiency / resolvability;
5. consequence of error;
6. deferral cost;
7. reversibility;
8. authority availability;
9. dependency.

Historical v1 analyses may retain the legacy tenth comparison lens,
`smallest_warranted_intervention`. For v2, derive the smallest warranted
intervention only after the strategic disposition/path judgment.

```text
strategic warrant
-> path/disposition selection
-> smallest warranted intervention

small intervention
!= strategically preferable future
```

Comparison values are semantic prose, not numeric scores.

```text
qualitative comparison != deterministic ranking
agent judgment != unexplained intuition
```

A comparison may conclude that no path is sufficiently warranted.

## 9. Decision-changing uncertainty

The analysis should ask:

> What unresolved premise could materially change the current strategic
> disposition or path judgment?

A decision-changing uncertainty should record:

- the uncertainty;
- what strategic judgment it could change;
- the smallest sufficient evidence, if inquiry is warranted;
- the appropriate evidence source;
- whether the answer is available from repository evidence, empirical reality,
  owner intent, or an external environment.

Inquiry Policy v0 governs whether the uncertainty should actually be
investigated. Experiment Economy & Proportional Rigor v1 governs the narrower
question of whether experimentation is warranted and how much experimental
control the current decision/claim requires.

```text
uncertainty exists != inquiry required
INVESTIGATE != EXPERIMENT
experiment possible != experiment warranted
strategic uncertainty != implementation blocker by default
research-grade evidence != default product-development evidence
```

Prefer the lowest-cost evidence strong enough for the strategic decision.
Cheap reversible construction may be the evidence-producing action when it is
within authority, safe enough, and less costly than a separate experiment.
When an experiment remains warranted, count total setup/isolation/evaluation
overhead and control only confounders that could invalidate the
decision-relevant inference.

## 10. Strategic disposition

The semantic agent emits one of:

- `BUILD` — one construction direction is sufficiently warranted to select a
  bounded repository responsibility;
- `INVESTIGATE` — a specific decision-changing uncertainty should be resolved
  before selecting/building; this does not imply an experiment, and the
  evidence-producing responsibility should use the cheapest sufficient source;
- `DEFER` — action is plausible but not warranted now;
- `NO_CHANGE` — current evidence does not warrant repository construction;
- `OWNER_DECISION` — the material missing premise is owner preference,
  authority, or policy;
- `THESIS_REVIEW` — the decision cannot be resolved inside Level 3 because a
  governing Level-4 commitment is materially challenged.

This disposition is a semantic conclusion produced by the active agent. The
artifact validator checks only that a declared disposition is represented
consistently.

## 11. Bounded responsibility

When disposition is `BUILD`, the analysis may nominate one candidate
repository-level responsibility and the smallest warranted intervention.

That nomination is **not** implementation authority.

The analysis artifact must explicitly preserve:

```text
candidate responsibility recorded
!= responsibility authorized for execution
```

Execution requires authority from the user/owner or an already-valid standing
authority surface.

## 12. Evidence discipline

Decision-changing claims must be grounded in durable evidence.

Evidence entries should identify:

- relative file/path or repository reference;
- line/range or stable identifier where available;
- the claim supported;
- currentness / source status when material.

Owner intent should be identified as owner-supplied context rather than
fabricated repository evidence.

## 13. Policy Hierarchy composition

Strategic Repository Sensemaking v1 is a Level-3 product surface. Policy
Hierarchy v0 supplies reusable semantic-control questions used during the
analysis:

```text
Strategic Policy
  -> what repository-level decision matters?

Inquiry Policy
  -> what should be learned next, if anything?

Metareasoning / Exploration
  -> how should reasoning/search be allocated and what alternatives are missing?

Warrant / Choice
  -> what commitment is justified now?

Learning / Reconciliation
  -> what does returned evidence change?
```

Policy layers do not become runtime services merely because this analysis uses
them.

## 14. Artifact

New canonical analyses use:

```yaml
schema_version: 2
artifact_id: strategic_repository_analysis
```

Historical analyses with no `schema_version` are legacy v1. They remain valid
without mutation so qualified strategic history does not become invalid merely
because the current authoring contract became more precise.

The durable artifact id is:

```text
strategic_repository_analysis
```

Canonical path:

```text
artifacts/strategic_repository_analysis.md
```

The contract is declared in
`skills/workflow-planner/references/artifact-contracts.yaml` and mechanically
checked by `scripts/validate-strategic-repository-analysis.py`.

## 15. Claim ceiling

Repository qualification of this capability establishes only that:

- the Skill and artifact contracts are coherent;
- required representation is mechanically checkable;
- the product surface preserves documented authority boundaries.

It does not establish:

- that generated paths are strategically optimal;
- comparative superiority over unaided reasoning;
- product-market value;
- that a selected path will succeed;
- that mechanical validation establishes semantic truth.
