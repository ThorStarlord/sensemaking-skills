# Strategic Repository Sensemaking v1

**Status:** canonical product contract  
**Control level:** Level 3 — Strategic Repository Evolution  
**Authority:** subordinate to `docs/product-strategy.md`, ADR 0029, and the Four-Level Control Model  
**Owner direction:** Issue #401, refined by Issues #446 and #449  
**Runtime posture:** semantic-agent reasoning + mechanically validated artifact; no strategic planner runtime

## 1. Purpose

Strategic Repository Sensemaking v1 turns repository evidence, governing intent,
and strategically relevant opportunity into an explicit, reconstructible
strategic decision space.

It answers:

> Given this repository, its governing intent, current capabilities, evidence
> ceilings, material constraints, and credible opportunities, what coherent ways
> could the repository evolve from here, what distinguishes those paths, and
> what direction or inquiry is warranted now?

This surface sits between repository diagnosis and bounded implementation:

```text
repository + owner intent
        |
goal fitness / objective-role check
        |
current system + completion-layer model
        |
major-system map
        |
breadth opportunity exploration
        |
frontier candidate synthesis
        |
depth drill on material candidates
        |
strategic frontier
        |
generative strategic-hypothesis pass
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

The generative pass does not replace evidence discipline. It separates the
evidentiary burden of describing the present from the strategic burden of
representing a plausible future:

```text
present-state claim
-> evidence or explicit owner-intent source

future-state possibility
-> strategic grounding + explicit assumptions

future success claim
-> returned evidence after action
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
goal obedience != goal diagnosis
stated milestone != terminal product intent automatically
milestone completion != prerequisite product completion
verification legibility != strategic importance
strategic grounding != prior validation
speculative path != manufactured path
```

The active semantic agent owns:

- interpretation of repository evidence;
- generation of plausible construction paths;
- admission of strategically grounded hypotheses about unbuilt futures;
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
- which futures respond to current tensions?
- which futures exploit current capability, architectural leverage, or adjacent opportunity?
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

### 4A. Goal fitness and completion-layer integrity

Before treating the stated objective as the Strategic Frontier, classify its
role when that distinction could change the decision:

```text
terminal | milestone | proxy | constraint | evidence_state | unclear
```

The stated objective remains authoritative owner input. The analysis does not
invent a hidden “real goal.” It compares the stated objective against explicitly
grounded governing intent and asks whether satisfying the objective could still
leave a material governing outcome unsatisfied.

When the objective is release-, qualification-, package-, integration-, or
verification-oriented, establish any decision-relevant prerequisite completion
layers first:

```text
implementation exists
!= integration/reachability complete
!= content/behavior complete
!= intended user/product experience complete
!= release/qualification complete
```

If a concrete counterexample shows that the milestone can be completed while the
governing product objective remains materially incomplete, record a goal-fit
warning and represent the upstream completion gap in the Strategic Frontier.

Use
`skills/strategic-repository-analysis/references/goal-fitness-and-completion-v1.md`
for the detailed contract.

### 4B. Strategic Exploration Funnel

At a genuine Level-3 `ANALYZE` or `REOPEN_ANALYSIS` boundary, run a
repository-wide Strategic Exploration Funnel before converging on the Strategic
Frontier:

```text
SYSTEM MAP
-> BREADTH EXPLORATION
-> FRONTIER CANDIDATE SYNTHESIS
-> DEPTH DRILL
-> CONSTRUCTION PATH SYNTHESIS
-> COMPARATIVE SELECTION
```

The system map identifies major product/control systems and their important
relationships. The breadth pass searches both **within** those systems and
**across** their boundaries for deficiencies, unrealized leverage, semantic or
authority loss, compositional gaps, simplification, autonomy opportunities, and
adjacent product value.

The breadth pass produces an opportunity landscape, not a backlog. The agent then
compresses material observations into grounded **frontier candidates** and
advances only the strongest/material candidates to deeper analysis.

Preserve:

```text
frontier candidate
!= construction path

system map
!= file inventory

breadth exploration
!= exhaustive repository enumeration

coverage before convergence
!= analysis ceremony
```

A frontier candidate names **where** strategic value/tension may be concentrated.
Construction paths describe **how** the repository could evolve after a candidate
survives enough depth analysis.

The funnel runs only when Level 3 is actually open/reopened. Mid-episode
`RESPONSIBILITY / EXECUTE / VERIFY / RECONCILE` continuation reuses the current
strategic model unless returned evidence genuinely reopens it.

Use
`skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md`
for the detailed contract.

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

Current-state entries require evidence or an explicit owner-intent source.
Future paths may require capabilities currently marked `MISSING`; the fact that
a future capability is absent is normal construction, not a reason to suppress
a strategically grounded path.

```text
missing capability
!= strategic priority

missing capability
!= inadmissible strategic hypothesis
```

## 6. Strategic frontier

When the Strategic Exploration Funnel ran, the Strategic Frontier is formed from
the depth-qualified frontier candidates rather than directly from the first
visible repository problem.

The Strategic Frontier is the set of current repository/product boundaries **and
unexploited opportunities** that could materially change progress toward the
governing mission.

Before admitting a tension or opportunity, apply the Strategicity Gate:
resolving or pursuing it must be capable of materially changing a future
capability state, product boundary, major architecture/control boundary, major
dependency structure, authority/thesis commitment, or materially different
future development that becomes possible.

A local repair, stale status projection, routine maintenance action, or
already-selected implementation task may warrant work without becoming Level 3.

An opportunity may be Level-3 material even when its future capability does not
exist yet. It must be grounded in a present strategic basis such as:

- current repository capability or architectural leverage;
- governing owner/product intent;
- a represented adjacent user/problem;
- an existing contract that makes the extension mechanistically plausible;
- another explicit source that explains why this future belongs in the current
  decision space.

The source grounds the **present basis** of the opportunity. It does not need to
prove the future outcome.

```text
idea exists != frontier item
repository issue exists != strategic frontier
bounded repair != construction path
frontier item != implementation commitment
frontier item != priority score
opportunity not yet built != opportunity not strategically representable
```

For new `schema_version: 2` analyses, each frontier entry declares
`evidence_refs`, `affected_capability_ids`, and `strategic_consequence`.
The validator checks these declarations mechanically; the active semantic agent
still decides whether the consequence is genuinely strategic.

## 7. Candidate construction paths

When breadth/depth exploration ran, synthesize construction paths only after the
relevant frontier candidate has survived proportional depth analysis. Do not
generate detailed paths for every breadth observation.

A **construction path** is a coherent repository-evolution trajectory: a future
state plus the major capability sequence and dependencies needed to reach it.

A path is not a feature list or roadmap.

### Strategic Hypothesis Admission

Before converging on evidence sufficiency, perform a generative pass. Strategy
may represent disciplined hypotheses about futures that do not yet exist.

A **real strategic path** is:

```text
coherent with governing intent
+ compatible with known repository reality
+ materially distinct future capability state
+ plausible mechanism from present capability/opportunity to that future
+ explicit decision-relevant assumptions
+ no known material contradiction
```

A path is **manufactured** when it exists mainly to fill path-count symmetry, is
materially indistinguishable from another path, contradicts governing
intent/current repository reality, solves no strategically represented
problem/opportunity, or relies on hidden/invented premises.

```text
real strategic path
!= empirically validated future

speculative path
!= manufactured path

ambitious
!= ungrounded

absence of evidence for future success
!= evidence that the future is strategically unwarranted
```

Each material path should state:

- stable path identifier and name;
- future state;
- why this path is plausible from current evidence, intent, leverage, or opportunity;
- Strategic Frontier entries it responds to;
- capabilities it builds on;
- new capabilities or changes it requires;
- coarse construction sequence;
- dependencies / prerequisites;
- what the path unlocks;
- material risks or tradeoffs;
- reversibility characteristics;
- evidence gaps / assumptions that matter;
- reassessment triggers when assumption failure could change the path.

Prefer **2–5 paths** when multiple futures are genuinely plausible. A single path
is valid when only one coherent construction trajectory is materially represented.

**Zero paths is also valid** when, after Strategic Hypothesis Admission,
current evidence/intent/authority does not support a meaningful real strategic
trajectory, or when the strategic disposition is reached without selecting a
construction direction (for example `NO_CHANGE`, `OWNER_DECISION`,
`THESIS_REVIEW`, or a genuinely gating investigation that must precede path
formation).

```text
construction_paths: []
!= analysis failure

zero real paths
> one manufactured path

zero paths
!= default response to unvalidated futures

BUILD
-> at least one real path
-> selected_path_id references that path
```

Do not manufacture alternatives merely to fill a template. Do not use the
zero-path option merely because a coherent path is unvalidated; first ask
whether it is a strategically grounded hypothesis under the rules above.

Before comparison, run an **orthogonality challenge**: if all represented paths
solve the same downstream/proxy-framed problem, ask whether another grounded
Strategic Frontier precedes that frame. This is a search challenge, not a
requirement to manufacture a third option.

New `schema_version: 2` paths make grounding explicit through
`frontier_refs`, `why_plausible`, `builds_on_capability_ids`, and
`required_capability_ids`. The core strategic hypothesis/mechanism belongs in
`why_plausible`; material premises belong in assumptions/reassessment
triggers. Referential integrity is mechanically checkable; strategic quality is
not.

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

### Commission / omission symmetry

Comparison must consider both forms of strategic exposure:

- **commission risk** — the downside of pursuing a path whose assumptions turn
  out to be wrong;
- **omission risk** — mission progress, leverage, learning rate, strategic
  optionality, or adjacent opportunity lost by preserving the current state or
  delaying unnecessarily.

Use the existing lenses, especially consequence of error, deferral cost,
decision value, and reversibility. Do not add numeric expected-value scoring or
a new required schema field.

```text
risk of building wrong
!= only strategic risk

risk of not building
= strategically relevant when omission changes mission progress or optionality
```

A comparison may conclude that no path is sufficiently warranted, but that
conclusion should follow the generative/admission pass rather than replace it.

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
residual uncertainty != BUILD prohibited
```

Prefer the lowest-cost evidence strong enough for the strategic decision.
Cheap reversible construction may be the evidence-producing action when it is
within authority, safe enough, and less costly than a separate experiment.
When an experiment remains warranted, count total setup/isolation/evaluation
overhead and control only confounders that could invalidate the
decision-relevant inference.

Residual uncertainty about whether a strategically grounded future will
succeed does not by itself require `INVESTIGATE`. A bounded, reversible,
authorized, sufficiently safe, information-producing build may be the cheapest
way to resolve that uncertainty while creating product value.

## 10. Strategic disposition

The semantic agent emits one of:

- `BUILD` — one construction direction is sufficiently warranted to select a
  bounded repository responsibility; prior empirical proof of future success is
  not required when the strategic hypothesis is coherently grounded and the
  bounded next responsibility has acceptable downside/reversibility;
- `INVESTIGATE` — a specific decision-changing uncertainty should be resolved
  before selecting/building; this does not imply an experiment, and the
  evidence-producing responsibility should use the cheapest sufficient source;
- `DEFER` — action is plausible but not warranted now;
- `NO_CHANGE` — current evidence and strategically grounded opportunity do not
  warrant repository construction;
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

`BUILD` requires sufficient strategic warrant for the bounded next
responsibility: coherent grounding, acceptable downside, appropriate
reversibility, explicit material assumptions, and independent implementation
authority. It does not require prior proof that the whole future path will
succeed.

That nomination is **not** implementation authority.

The analysis artifact must explicitly preserve:

```text
candidate responsibility recorded
!= responsibility authorized for execution
```

Execution requires authority from the user/owner or an already-valid standing
authority surface.

## 12. Evidence discipline

Decision-changing **present-state claims** must be grounded in durable evidence.

Evidence entries should identify:

- relative file/path or repository reference;
- line/range or stable identifier where available;
- the claim supported;
- currentness / source status when material.

Owner intent should be identified as owner-supplied context rather than
fabricated repository evidence.

Future-state strategic hypotheses must not masquerade as established evidence.
They should declare:

- the present evidence/intent/leverage that makes the future plausible;
- the mechanism connecting the present to the proposed future;
- material assumptions;
- evidence gaps;
- reassessment triggers.

```text
hypothesis explicitly grounded
!= future outcome claimed true

future not yet evidenced
!= future excluded from strategy
```

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
- that the stated milestone is a sufficient proxy for governing product intent;
- that a compared option set is strategically complete merely because its members are credible;
- that mechanical validation establishes semantic truth.
