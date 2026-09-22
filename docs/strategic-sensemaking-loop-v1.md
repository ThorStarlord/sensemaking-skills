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
| `strategic-repository-reconciliation` | interpret consequential returned evidence against prior Level 3 |
| `owner-decision-capsule` | package a genuinely owner-reserved decision without selecting it |
| `thesis-review-packet` | carry a Level-4 review boundary when warranted |

The loop Skill owns only composition and resume.

```text
one front door
!= one giant Skill

composition
!= responsibility collapse
```

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

RESPONSIBILITY
-> strategy current, bounded responsibility unresolved

EXECUTE
-> responsibility + prerequisites + authority established

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
- automatic owner decisions;
- automatic Level-4 thesis revision;
- automatic merge/release/publication authority;
- mandatory execution through `handoff`;
- mandatory five-Skill choreography.

The active semantic agent remains the controller.
