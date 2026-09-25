# Strategic Sensemaking Loop v1

**Status:** canonical internal orchestration guidance  
**Skill:** `strategic-sensemaking-loop`  
**Scope:** one-prompt start/resume across Levels 3 → 2 → 1 → evidence return  
**Authority:** semantic-agent guidance; no runtime planner or authority expansion

## Purpose

The repository already had specialized Skills for strategic analysis,
responsibility selection, handoff, returned-evidence reconciliation, and
owner-reserved decisions.

Normal use showed that requiring the operator to manually prompt each transition
created unnecessary ceremony and made it easier to restart an already-completed
stage.

Strategic Sensemaking Loop v1 adds one front door:

```text
ONE USER PROMPT
      |
      v
reconstruct current durable boundary
      |
      +--> strategic-repository-analysis        when Level 3 is open/reopened
      |
      +--> using-sensemaking                    when responsibility is unresolved
      |
      +--> handoff                              only for a real Skill-to-Skill transfer
      |
      +--> active execution / Campaign handoff  for already-selected work
      |
      +--> strategic-repository-reconciliation  when returned evidence changes Level 3
      |
      +--> owner-decision-capsule               when owner preference is genuinely decisive
      |
      +--> stop / continue / reopen
```

This is orchestration guidance, not a new control level.

## Architecture

The specialized Skills keep their existing responsibilities:

| Surface | Responsibility |
| --- | --- |
| `strategic-repository-analysis` | model the Level-3 decision space |
| `using-sensemaking` | select/adjudicate the bounded responsibility and control move |
| `handoff` | preserve context across a real Skill transition |
| active agent / Campaign execution interface | perform already-selected work |
| `organization inspect|role|skill-profile` | optionally expose role/capability/evidence topology when that topology is decision-relevant; never select actors/Skills or grant authority |
| `strategic-repository-reconciliation` | interpret consequential returned evidence against prior Level 3 |
| `owner-decision-capsule` | package a genuinely owner-reserved decision without selecting it |
| `thesis-review-packet` | carry a Level-4 review boundary when warranted |

The loop Skill owns only composition and resume.

It also applies the cross-cutting **Value-Producing Action Preference** and
delegation envelope when those affect how far the episode should continue.

```text
one front door
!= one giant Skill

composition
!= responsibility collapse

highest-value warranted action
!= lowest-risk action automatically
```

See
`skills/strategic-sensemaking-loop/references/value-action-and-delegation-v1.md`.

## Artifact-aware resume

The front door should first reconstruct the current episode from repository
state and durable artifacts.

Typical inputs include:

```text
current owner request / authority
current repository source identity
STATUS.md / strategy / ADRs

strategic_repository_analysis
strategic_reconciliation
sensemaking_decision or current Campaign responsibility
execution handoff / returned evidence
owner_decision_capsule
explicit owner selection after a capsule
```

The agent resumes from the latest **semantically valid** boundary rather than the
latest timestamp.

```text
newest file
!= current decision automatically

prior SRA
+ later reconciliation
-> reconciliation governs continuation
-> prior SRA remains immutable provenance
```

## Conditional routing

Use the following as semantic guidance only:

```text
ANALYZE
-> strategy absent or explicitly reopened
-> run Strategic Exploration Funnel:
   system map → breadth exploration → frontier candidates → depth drill → paths

RESPONSIBILITY
-> strategy current, bounded responsibility unresolved

EXECUTE
-> responsibility + prerequisites + authority established
-> optionally inspect Organization topology when it materially improves delegation / verification / evidence-flow / authority legibility

RECONCILE
-> consequential evidence returned

OWNER_DECISION
-> repository evidence exhausted; owner premise remains

THESIS_REVIEW
-> Level-4 commitment requires reserved review

STOP
-> no further warranted/authorized action
```

These labels are not persisted state and are not deterministic routing enums.

When action-mode choice is material, compare descriptive shapes such as:

```text
BUILD
REVERSIBLE BUILD
VERIFY / QUALIFY
PROBE / INQUIRE
SPIKE / PROTOTYPE
EXPERIMENT
STOP / ESCALATE
```

A reversible build is especially attractive when it creates useful retained
product value and normal use provides evidence strong enough for the current
decision at no greater total cost/downside than a separate experiment followed
by duplicate implementation.

## Autonomous terminal missions

When the owner explicitly delegates a terminal repository outcome with FULL
AUTONOMY / FULL DELEGATION, the loop may continue across multiple bounded
responsibilities without returning control merely because one responsibility
finished.

This is a continuation profile over the existing control model:

```text
terminal mission
-> current semantic boundary
-> bounded responsibility
-> execute
-> verify
-> reconcile
-> terminal-gap check
-> next warranted responsibility when needed
-> continue
```

The mission profile is defined in
`skills/strategic-sensemaking-loop/references/autonomous-terminal-mission-v1.md`.

Its defining laws are:

```text
responsibility completed
!= mission completed

mission incomplete
!= execute backlog blindly

full repository delegation
!= protected-transition authority
```

If Level 3 is genuinely open/reopened, the existing Strategic Exploration Funnel
still owns breadth -> frontier candidates -> proportional depth -> construction
paths -> selection. Full autonomy does not force exactly three approaches and
does not rerun strategic breadth during settled responsibility/execution/
reconciliation.

For implementation, "complete the vertical stack" means every
**decision-relevant** layer required by the selected capability, not maximal
architecture. Domain, integration, persistence, user/operator, observability,
content/progression, compatibility, documentation, and qualification surfaces
are included only when they materially belong to the target.

A mission may explicitly defer field validation until construction completeness.
That allows first-principles heuristics and synthetic personas to guide
construction-stage decisions, while preserving:

```text
synthetic persona
!= empirical user evidence

construction complete
!= externally validated
```

Status/capability authority may be updated after applicable verification and
reconciliation supports promotion. Implementation alone does not make
provisional/draft state canonical.

Merge, release/deploy, external publication, credentials/billing, destructive
external mutation, cross-repository expansion, Level-4 thesis revision, and
genuine owner-preference decisions remain separately governed unless explicitly
granted and permitted by repository policy.

## No mandatory choreography

A fresh episode may traverse several surfaces:

```text
strategic analysis
-> responsibility selection
-> execution
-> reconciliation
-> stop
```

A resumed episode may legitimately begin in the middle:

```text
existing strategic analysis
+ existing selected responsibility
-> execution
-> reconciliation
```

or:

```text
existing owner capsule
+ explicit owner selection
-> responsibility selection
-> execution
```

The loop must not rerun completed stages merely to reproduce a canonical
sequence.

In particular, the repository-wide Strategic Exploration Funnel belongs only to
a genuine `ANALYZE / REOPEN_ANALYSIS` boundary. A resumed
`RESPONSIBILITY / EXECUTE / VERIFY / RECONCILE` episode must not remap every
system or repeat breadth exploration unless returned evidence actually reopens
Level 3.

## Handoff boundary

`handoff` is not mandatory between every stage.

Use it only when preserving a prompt for another **registered Skill** is useful.

Do not fabricate Skill identities for execution mechanisms:

```text
repository-qualification.yml
!= repository-qualification Skill

GitHub Actions
!= GitHub-Actions Skill

active coding agent
!= coding-agent Skill automatically
```

When the active agent can execute directly, execute directly.

When explicit role/capability topology is decision-relevant, the loop may inspect
the shipped Organization surface before or during execution-boundary choice:

```text
organization inspect / organization role / organization skill-profile
-> read-only topology evidence
-> not a new loop state
-> not Skill selection
-> not actor allocation
-> not execution authority
```

Do not make Organization inspection mandatory for obvious bounded work.

When durable cross-context delegation is useful, use the Campaign Execution
Interface:

```text
selected responsibility
-> execution handoff
-> worker
-> returned evidence
-> parent reassessment
```

## Owner boundary

An owner-decision capsule terminates autonomous continuation unless the owner has
already supplied a new explicit selection.

```text
owner capsule exists
+ no selection
-> STOP

owner capsule exists
+ owner explicitly selects OPTION-X
-> treat selection as new intent/authority input
-> using-sensemaking
-> derive bounded responsibility
```

The option statement itself is not automatically a Level-2 work package.

## High-delegation repository envelope

When the owner explicitly delegates continued repository work without approval
pauses, the loop may proceed through ordinary repository-answerable analysis,
construction, reversible builds, repair/refactor/docs, existing qualification,
warranted probes/experiments, branch/commit/draft-PR work, evidence
reconciliation, and the next independently warranted responsibility.

This broad delegation does not silently authorize protected merge, release,
production deployment, credentials/billing, Level-4 thesis choice,
preference-sensitive owner decision, or unrelated external mutation.

```text
high delegation
!= unlimited authority
```

A blocked verification/qualification gate blocks the responsibility that depends
on it. It does not automatically prove that no other independently warranted
repository work exists; such work may continue only when it does not bypass,
depend on, or weaken the blocked gate.

## Evidence return

Returned execution evidence first answers:

1. what exact target/source was acted on;
2. whether the intended action/gate actually executed;
3. what claim the evidence establishes;
4. what it does not establish;
5. whether the consequence is local or strategic.

Use strategic reconciliation only when Level-3 claims, assumptions, path
continuation, frontier, or strategic effect can materially change.

```text
returned evidence
!= strategic reconciliation always required
```

## Final output

The front door may emit a concise run summary containing:

- reconstructed resume point;
- Skills invoked;
- artifacts consumed and produced;
- non-Skill execution surfaces;
- returned evidence;
- current strategic and responsibility state;
- stop reason.

For consequential Level-3 selections, it should also expose a compact **Decision
Trace** with the material alternatives actually considered, the product/capability
value each would create, the selected action shape, and brief reasons a materially
more conservative or aggressive move was less warranted.

When `ANALYZE / REOPEN_ANALYSIS` actually ran, precede that Decision Trace with
a compact **Strategic Exploration Summary** showing the major systems examined,
breadth opportunity themes, synthesized frontier candidates, candidates advanced
to depth, selected Strategic Frontier, and selected construction path (if any).
This is owner-visible proof of coverage-before-convergence, not an exhaustive
idea dump or private chain-of-thought.

This is owner-visible decision observability, not private scratch reasoning and
not a new artifact.

This summary is convenience output only.

```text
loop summary
!= master artifact
```

## Non-goals

Strategic Sensemaking Loop v1 does not add:

- a deterministic planner/router;
- a fifth control level;
- a new master artifact;
- a new Campaign schema;
- automatic Skill selection from scores;
- automatic Campaign creation;
- a mandatory Organization stage;
- automatic role allocation, dynamic Organization generation, or Skill routing;
- automatic owner decisions;
- automatic Level-4 thesis revision;
- automatic merge/release/publication authority;
- numeric expected-value/action scoring or automatic action routing;
- mandatory reversible builds, prototypes, qualification, or experiments;
- mandatory execution through `handoff`;
- mandatory five-Skill choreography;
- mandatory breadth/depth reanalysis during settled execution or verification;
- a persisted search tree, frontier score, or deterministic exploration router.

The active semantic agent remains the controller.
