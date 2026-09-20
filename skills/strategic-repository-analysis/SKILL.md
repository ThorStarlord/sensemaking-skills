---
name: strategic-repository-analysis
description: analyze a repository at level 3 to model its current capability state, generate coherent construction paths, compare them qualitatively, identify decision-changing uncertainty, and produce a strategic repository analysis without selecting work mechanically.
---

# strategic-repository-analysis

Produce a first-class **Strategic Repository Analysis** for a repository whose
future construction direction is materially open.

Use this Skill when the user asks questions such as:

- How could this repository be developed from here?
- What are the plausible strategic directions for this product/repository?
- What could this repository become?
- Compare the main ways we could construct or evolve this repository.
- What should we build next at the repository/product level when no task has
  already been selected?
- Analyze the repository strategically rather than merely diagnosing one weak
  boundary.

Do **not** use this Skill for an already-localized implementation task whose
repository-level direction is already settled.

## Responsibility

This Skill owns one responsibility:

> Turn current repository evidence + governing intent into a reconstructible
> Level-3 strategic decision space.

It produces:

`artifacts/strategic_repository_analysis.md`

The active semantic agent owns the analysis. No deterministic tool selects the
best path.

## Inputs

Use the smallest sufficient input set:

1. target repository;
2. owner/user intent or governing product strategy when available;
3. current repository evidence;
4. an existing `repository_sensemaking_brief` when it is current and
   decision-relevant;
5. current strategic state / ADRs / release state when they materially constrain
   the analysis.

Do not require a Campaign merely to run this analysis.

## Procedure

### 1. Establish governing intent and authority

Distinguish:

- owner-supplied intent;
- repository-owned product strategy / ADR authority;
- inferred purpose;
- implementation authority.

A strategic request grants authority to analyze. It does not automatically
grant authority to implement the resulting direction.

### 2. Verify current repository state

Use the authorized repository-access surface.

Prefer measured/current evidence over stale roadmap or status claims. Treat
documented state as documented until independently verified when the distinction
could change the strategic analysis.

Reuse `repo-sensemaker` evidence when it is current. Run repository diagnosis
first only when doing so would materially improve the strategic model.

### 2A. Establish strategic continuity when relevant

If a prior `strategic_repository_analysis` materially governs the current
decision, do not silently overwrite it. Give the new analysis a stable
`analysis_ref` and declare a continuity relationship:

```text
NEW | REAFFIRM | CONTINUE | REVISE | SUPERSEDE | CLOSE
```

Record the prior analysis reference, prior selected path when applicable, and a
short semantic reason. Continuity is authored judgment; deterministic tools may
project it but may not infer it.

When mechanically addressable repository authority files materially condition
the analysis, declare them in `governing_authority_refs`. This lets later
currentness inspection identify that an authority reference changed; the
mechanical observation does not decide that the governing commitment changed
semantically or that strategy must reopen.

### 3. Build the current-system model

Describe the repository as a system/product:

- purpose and primary use;
- major capabilities;
- important architecture/control boundaries;
- qualification/release posture where relevant;
- major constraints and claim ceilings.

Do not reduce the repository to a file inventory.

### 4. Build the capability / limitation map

Classify decision-relevant capabilities using only:

```text
ESTABLISHED
PARTIAL
MISSING
DEFERRED
BLOCKED
CLAIMED_UNVERIFIED
OUT_OF_SCOPE
```

Each entry needs evidence or an explicit owner-intent source.

Do not turn the states into maturity numbers.

### 5. Form the Strategic Frontier

Before admitting a repository tension into the Strategic Frontier, apply the
**Strategicity Gate**:

> Would resolving this boundary materially change at least one of the
> repository/product future capability state, product boundary, major
> architecture/control boundary, dependency structure, authority/thesis
> commitment, or the materially different future development that becomes
> possible?

Only boundaries that pass that semantic test belong on the Strategic Frontier.
A useful maintenance action, local defect, stale status projection, routine
dependency update, or already-selected bounded implementation task may still
warrant lower-level work without becoming a Level-3 construction path.

```text
repository issue exists != strategic frontier
useful maintenance exists != construction trajectory
bounded repair warranted != Level-3 BUILD warranted
repository-relevant work != strategic repository evolution
```

Identify the small set of unresolved boundaries that could materially change
progress toward the governing mission.

For new canonical `schema_version: 2` artifacts, each frontier entry records
decision-changing evidence references, affected capability identifiers, and a
short `strategic_consequence` explaining why the boundary is Level-3 material.
The semantic agent judges that consequence; the validator checks only shape and
references.

Exclude attractive but non-decision-relevant ideas.

### 6. Generate coherent construction paths

Generate 2–5 paths when multiple futures are materially plausible.

Use one path when only one coherent construction trajectory is materially represented.
Use zero paths when no construction trajectory is currently warranted/representable and
the strategic conclusion is reached before construction selection.

```text
zero real paths
> manufactured alternative

BUILD
-> requires a selected real path
```

Each path must describe:

- future state;
- why it is plausible;
- Strategic Frontier boundary or boundaries it responds to;
- capabilities it builds on;
- required capabilities/changes;
- coarse construction sequence;
- dependencies;
- what it unlocks;
- material risks/tradeoffs;
- reversibility;
- evidence gaps;
- decision-relevant assumptions when useful;
- reassessment triggers for assumptions whose failure could change the path;
- optional lightweight `path_transitions` with stable references such as
  `PATH-2/T1` when later work would otherwise be difficult to place inside the
  trajectory.

A path transition names a conceptual capability-state transition. It is not a
task, milestone, schedule entry, status percentage, or automatic next action.
A path is a coherent future trajectory, not a backlog.

For new canonical `schema_version: 2` artifacts, path grounding is explicit:
`frontier_refs`, `why_plausible`, `builds_on_capability_ids`, and
`required_capability_ids` must connect the path to declared frontier and
capability-map identifiers. Mechanical reference integrity does not establish
that the path is strategically good.

One path is valid when additional alternatives would be artificial. Zero paths is valid when even one construction path would be artificial or premature.

For path distinctness, capability-state grounding, coarse construction
sequencing, comparison discipline, and anti-backlog rules, read
`references/construction-path-synthesis-v1.md`.

Do not generate a path merely because a generic category exists. Two paths are
materially distinct only when they imply a different future capability state,
dependency structure, authority/thesis requirement, major risk, or set of
later possibilities.

### 7. Compare paths qualitatively

Use the canonical strategic-comparison lenses:

1. mission relevance;
2. decision value;
3. blocking power;
4. evidence sufficiency / resolvability;
5. consequence of error;
6. deferral cost;
7. reversibility;
8. authority availability;
9. dependency.

For legacy v1 artifacts, the historical tenth
`smallest_warranted_intervention` comparison lens remains valid for backward
compatibility. New `schema_version: 2` artifacts derive the smallest warranted
intervention only **after** the strategic disposition/path judgment.

```text
strategic warrant
-> path/disposition selection
-> smallest warranted intervention

cheap or local intervention
!= strategically preferable future
```

Do not assign numeric scores, weighted totals, tiers, or a deterministic winner.

Explain the judgment.

### 8. Identify decision-changing uncertainty

Ask what unresolved premise could actually change the strategic conclusion.

Then apply Inquiry Policy v0:

```text
uncertainty exists
!= inquiry required
```

If inquiry is warranted, name the smallest sufficient evidence and correct
source:

- repository_evidence
- empirical
- owner_intent
- external_environment

If no inquiry is warranted, say so.

### 8A. Record decision assumptions when they matter

Record only premises whose failure could materially change the strategic
judgment. Give each a stable identifier, evidence references, and explicit
reassessment triggers.

```text
assumption recorded
!= confidence score
!= generic belief database

trigger observed
!= strategy automatically changed
```

### 9. Synthesize one strategic disposition

Choose semantically:

```text
BUILD
INVESTIGATE
DEFER
NO_CHANGE
OWNER_DECISION
THESIS_REVIEW
```

For `BUILD`, nominate one candidate bounded repository responsibility and the
smallest warranted intervention.

For `INVESTIGATE`, nominate the bounded evidence-producing responsibility, not
a broad research program.

For `OWNER_DECISION`, state the exact owner decision rather than disguising it
as repository investigation. When a durable owner-facing decision surface is
useful, produce an `owner_decision_capsule`; the capsule does not select for the
owner.

For `THESIS_REVIEW`, identify the governing commitment that Level 3 cannot
silently rewrite. When the review must be carried across contexts, produce a
`thesis_review_packet`; the packet does not ratify a Level-4 disposition.

When decision-changing evidence comes from outside repository authority and must
remain reconstructible, use an `external_evidence_packet` to preserve bounded
source/currentness provenance.

### 10. Write and validate the artifact

Use:

`references/strategic-repository-analysis-template.md`

New canonical analyses emit `schema_version: 2`. Historical artifacts without a
`schema_version` remain legacy v1 and must continue to validate without
mutation.

Then validate:

```bash
python scripts/validate-artifact.py strategic_repository_analysis artifacts/strategic_repository_analysis.md
python scripts/validate-strategic-repository-analysis.py artifacts/strategic_repository_analysis.md
```

Mechanical PASS does not establish strategy correctness.

## Required boundary statements

Preserve these distinctions in the artifact:

```text
strategic analysis != implementation authorization
repository-relevant work != strategic repository evolution
bounded repair != construction path
construction path != backlog
path transition != roadmap item
path transition != authorized responsibility
transition established != next transition selected
path comparison != numeric ranking
mechanically valid != semantically correct
candidate responsibility != authorized execution
strategic warrant precedes intervention minimization
```

## Output behavior

The artifact should be useful to a fresh owner or coding agent without hidden
conversation context. When it continues a prior analysis, the lineage and
reassessment assumptions should be reconstructible from the artifact itself.

Do not append an implementation plan unless the strategic disposition and
authority independently warrant one.

When later evidence returns against this analysis, use
`strategic-repository-reconciliation` if the claim/assumption/path/strategic
effect itself must become a durable artifact.

Do not automatically create a Campaign, issue, PR, execution handoff, or code
change from this Skill.