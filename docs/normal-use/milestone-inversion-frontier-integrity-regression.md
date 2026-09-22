# Normal-Use Regression Case — Milestone Inversion and Frontier Integrity

**Date:** 2026-09-21  
**Source mode:** normal-use repository work, not a synthetic experiment  
**Target:** a playable narrative-game repository with an explicit release-candidate milestone  
**Purpose:** preserve a regression case for Level-3 goal fitness and path-set completeness

## Case

The owner wanted to finish a player-facing Part 1 experience and had previously
introduced a release-candidate / exact-SHA qualification goal as an operational
milestone.

A strategic analysis treated exact-candidate qualification as the immediate
Level-3 path and represented empirical opening validation as the main
alternative. Downstream Sensemaking correctly selected a bounded qualification
responsibility, preserved authority, executed the exact candidate, classified
repeated zero-step CI as infrastructure evidence rather than repository failure,
and later reconciled the path to an owner decision.

The control loop was disciplined **inside the represented path set**.

The strategic failure occurred earlier: the path set omitted the credible
trajectory of finishing material player-facing Part 1 content/presentation before
returning to release qualification.

## Failure pattern

```text
terminal product intent
-> release-candidate milestone
-> qualification evidence

became

qualification evidence
-> active frontier
```

This is **milestone inversion**: an instrumental milestone became the optimized
objective even though satisfying it did not establish the governing product
outcome.

A related **legibility bias** was present: exact SHAs, CI, validators, packages,
and claim ceilings were mechanically easy to inspect, while player-facing
completion required semantic inspection of content/presentation quality.

## Required regression behavior

A conforming Level-3 analysis should now:

1. preserve the explicit owner objective;
2. classify its role when material:
   `terminal | milestone | proxy | constraint | evidence_state | unclear`;
3. ground governing intent rather than inventing a hidden goal;
4. test whether the stated objective could be satisfied while a material
   governing outcome remains unsatisfied;
5. check decision-relevant completion layers before treating downstream
   qualification/release work as the Strategic Frontier;
6. surface a `GOAL_FIT_WARNING` when mismatch is material;
7. run an orthogonality challenge before converging on a path set;
8. avoid manufacturing a third path when no grounded orthogonal trajectory exists.

Downstream `using-sensemaking` should treat an inherited responsibility as
defeasible when a decision-critical prerequisite is materially unestablished.

An `owner-decision-capsule` should not force an owner to choose inside a path
set already shown to be incomplete. It should return
`OPTION_SET_INCOMPLETE` upstream rather than inventing a new option.

## Non-goals

This regression case does not require:

- a new artifact schema;
- a product-completion database;
- numeric goal-fit scoring;
- automatic strategy reopening;
- mandatory three-option path generation;
- a generic execution Skill;
- an experiment to prove the case.

## Canonical invariants

```text
goal obedience
!= goal diagnosis

stated milestone
!= terminal product intent automatically

milestone completion
!= prerequisite product completion

easy to verify
!= strategically important

two credible paths
!= option set necessarily complete

upstream selected responsibility
!= dependency-free responsibility

owner decision packet
!= owner decision made
```

## Expected control flow

```text
governing intent + stated objective
-> goal fitness
-> completion-layer check
-> Strategic Frontier
-> Strategic Hypothesis Admission
-> path generation
-> orthogonality challenge
-> path comparison
-> disposition
-> bounded responsibility
-> prerequisite backstop
-> execution / evidence
-> reconciliation
```

This is retained as normal-use evidence for future Skill iteration. It is not
treated as proof that every release-oriented objective is a bad proxy or that
every repository requires experiential/product-completion analysis.
