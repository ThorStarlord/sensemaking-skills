# Agent Workflow Golden Paths v1

These are **composition examples, not a router**. The active coding agent owns whether a path applies, the decision-changing uncertainty, responsibility selection, capability selection, authority decisions, and terminal judgment.

Use the CLI projection when useful:

```bash
sensemaking-skills campaign workflow list
sensemaking-skills campaign workflow show single-repository
sensemaking-skills campaign workflow show fresh-context
sensemaking-skills campaign workflow show transferred-campaign
sensemaking-skills campaign workflow show multi-repository
```

## Single-repository consequential work

```text
strategy inspect
-> AGENT: select warranted responsibility
-> strategy handoff
-> preflight
-> capability-context using explicit responsibility type
-> AGENT: select/perform bounded work
-> repository-native validation + evidence admission
-> AGENT: advance / defer / close
-> closeout after terminal close
-> AGENT: archive if useful
```

## Fresh-context continuation

```text
resume-profile --profile working
-> preflight
-> doctor when a mechanical check fails
-> AGENT: decide whether the current responsibility remains warranted
-> continue bounded work or author an explicit Campaign decision
```

## Transferred Campaign

```text
bundle-inspect
-> bundle-resume-context
-> AGENT: authorize durable import
-> bundle-import
-> AGENT: provide exact target path(s)
-> target rebind / multi-target rebind
-> preflight
-> AGENT: interpret and continue
```

Rebinding never searches for repositories or blesses drift.

## Multi-repository work

```text
AGENT: select responsibility
-> strategy handoff
-> AGENT: explicitly add repository targets
-> AGENT: explicitly declare cross-repository relations
-> multi-target verify
-> multi-target dependency-check
-> preflight
-> AGENT: execute bounded work
-> AGENT: explicitly refresh changed target snapshots
-> AGENT: advance / defer / close
-> closeout after terminal close
```

## Non-identities

```text
golden path != workflow engine
golden path != responsibility selection
flow shown != flow recommended
step listed != step authorized
preflight PASS != should proceed
capability compatible != capability selected
archive != success
```

These paths are intentionally static and readable. If the repository later changes a command contract, reconcile this reference and the `campaign workflow` projection rather than adding a semantic router to keep them in sync automatically.
