# Consequence Depth and Systems Reasoning v0

**Status:** guidance / research clarification  
**Date:** 2026-10-03  
**Authority:** subordinate to current product strategy, ADR 0029, Policy Hierarchy v0, using-sensemaking, and existing authority contracts  
**Runtime status:** semantic guidance only; no new policy layer, planner, score, state machine, or Skill

## 1. Purpose

Coding agents can reason systemically, but ordinary task structure strongly
rewards **local completion**: the smallest visible change that makes the immediate
symptom and its tests go green.

This document names that pressure **Local Completion Bias** and defines a bounded
way to increase reasoning scope when downstream consequences can change the
correct interpretation, responsibility, implementation, verification, or
strategic decision.

~~~text
local mechanical success
!= systemic correctness

think harder inside the same boundary
!= inspect whether the boundary itself is wrong

more reasoning depth
!= better automatically
~~~

The goal is not to force architecture analysis for every edit. The goal is to
reason at the **smallest system scale that preserves correctness**.

## 2. Local Completion Bias

A bounded task often presents an easy-to-observe local objective:

~~~text
observed symptom
-> edit nearby code/state
-> focused test passes
-> task appears complete
~~~

This is valuable when the affected behavior is genuinely local. It becomes risky
when the changed concept or state is consumed elsewhere, propagates through time,
changes another workflow's assumptions, or repeatedly requires neighboring
patches.

Local Completion Bias is therefore a control/environment effect, not an
assertion that an agent lacks the intelligence to reason globally.

~~~text
local success is easy to observe
+ global semantic coherence is harder to observe
-> stopping pressure favors the local boundary
~~~

## 3. Consequence-depth model

Use consequence depth as a descriptive reasoning ladder. These are not mandatory
runtime levels and should not be persisted as a new state machine.

### First order — direct effect

Ask:

> What does the contemplated change directly fix or alter?

~~~text
symptom
-> direct change
-> immediate observable result
~~~

Example:

~~~text
state disappears after refresh
-> persist state
-> refresh now preserves it
~~~

First-order reasoning is sufficient when no decision-relevant downstream
assumption changes.

### Second order — consumers and dependencies

Ask:

> What consumes, depends on, or interprets the changed thing?

~~~text
changed state
-> downstream consumer
-> changed assumption / interpretation
~~~

Inspect explicit contracts, readers, projections, later workflow stages, or
other systems whose behavior depends on the changed concept.

### Third order — propagation through later behavior

Ask:

> How do those downstream changes alter future behavior, later decisions, or
> user expectations?

~~~text
changed assumption
-> later behavior
-> further dependent behavior
-> delayed contradiction / drift / user-model mismatch
~~~

This is especially relevant for long-running workflows where a local state
change influences later chapters, stages, migrations, reconciliations,
deployments, or continuation contexts.

### Fourth order — invariant or missing abstraction

Ask:

> Do several downstream consequences point to one shared invariant, missing
> concept, or missing distinction?

A patch family may indicate that the system lacks the right model.

~~~text
patch A
patch B
patch C
all compensate for the same hidden distinction
        |
        v
candidate missing abstraction / invariant
~~~

Example shape:

~~~text
value present / value absent
~~~

may be insufficient if the product actually needs to distinguish states such as:

~~~text
unknown
deferred
provisional
committed
contradicted
~~~

The specific vocabulary is domain-owned; this document does not impose those
states on repositories generally.

### Fifth order — architectural embodiment

Ask:

> Does the current architecture make the discovered invariant easy to preserve,
> or does every subsystem reproduce it independently?

~~~text
shared invariant
-> one coherent ownership/contract boundary?

or

shared invariant
-> duplicated local representations / compensating patches?
~~~

Architectural change is warranted only when the invariant is real and the
current architecture materially obstructs it.

### Sixth order — product/strategic implication

Ask:

> Does this reveal that the repository is solving the wrong capability boundary,
> or that a higher-level product commitment should be reconsidered?

This is a Level-3 or potentially Level-4 question only when the evidence is
actually decision-changing.

~~~text
local surprise
!= strategy reopened automatically

missing abstraction
!= product thesis changed automatically
~~~

## 4. Zoom-out trigger

Increase reasoning scope when at least one of these is materially plausible:

- the changed state/concept has downstream consumers whose interpretation could
  alter correctness;
- consequences appear only after several workflow stages or over time;
- the local fix changes assumptions in another subsystem;
- the user-facing mental model and internal semantic model may diverge;
- several nearby bugs/patches repeatedly compensate for the same distinction;
- the implementation adds more flags/exceptions because the underlying concept
  is unclear;
- a local repair could violate the owning product capability or invariant;
- closure depends on behavior outside the directly edited files.

A useful prompt is:

> **What remaining downstream consequence could make this locally correct fix
> the wrong responsibility?**

## 5. Stop rule

Do not climb consequence depth indefinitely.

Stop increasing scope when the next layer cannot materially change:

- problem interpretation;
- responsibility selection;
- implementation shape;
- required verification/reconciliation;
- ownership or authority;
- system invariant/architecture;
- Level-3 or Level-4 decision.

~~~text
additional zoom
!= decision-relevant change
-> stop and execute the bounded responsibility
~~~

This prevents the opposite failure mode: turning every typo, rename, or local
mechanical defect into architecture work.

## 6. Relationship to change-impact analysis

change-impact-analysis answers:

> What consequential surfaces does this bounded contemplated/completed change
> materially affect?

Consequence-depth reasoning adds:

> How far do those effects propagate, and do they reveal a shared invariant or
> missing abstraction that changes the correct responsibility?

~~~text
affected surface
!= second-order consequence automatically

several affected surfaces
!= missing abstraction automatically

missing abstraction candidate
!= architecture change authorized
~~~

Use the existing change_impact_analysis artifact when a durable affected-surface
decision space is warranted. Do not add a second systems-reasoning artifact
merely to record consequence depth.

## 7. Relationship to responsibility selection

The important control transition is:

~~~text
"What field/file should I change?"
        |
        v
"What concept/state is actually changing?"
        |
        v
"What depends on that concept?"
        |
        v
"What responsibility preserves the relevant invariant?"
~~~

A locally obvious implementation may therefore be premature even when the
implementation itself is technically straightforward.

~~~text
easy patch
!= correct responsibility established
~~~

## 8. Relationship to validation and closure

Focused tests establish focused claims.

~~~text
refresh test PASS
-> persistence behavior established

refresh test PASS
!= all downstream semantic consumers remain coherent
~~~

When the consequence chain is material, closure may require broader
verification, reconciliation, or a change-impact analysis. Do not expand
verification when the broader consequence cannot change the closure claim.

## 9. Relationship to capability learning

Repeated normal-use episodes may reveal a higher-order capability lesson, for
example:

~~~text
episode A -> agent stops at local patch
episode B -> agent stops at local patch
episode C -> agent stops at local patch
        |
        v
recurring capability pattern:
reasoning boundary repeatedly too narrow
~~~

That pattern may justify improving reusable Sensemaking guidance through the
ordinary evidence, review, qualification, and authority path.

~~~text
one locally narrow episode
!= capability doctrine

recurring cross-episode pattern
-> possible capability-learning candidate
~~~

This document itself does not introduce a capability-learning runtime or
automatic Skill modification.

## 10. Anti-patterns

### Local green means globally done

Do not infer system closure from a focused PASS when the actual closure claim
depends on downstream consumers.

### Architecture by imagination

Do not turn a small bug into speculative redesign. Reason outward only while
evidence can change the decision.

### Patch accumulation without abstraction review

Repeated flags, exceptions, special cases, and local workarounds around the same
concept should trigger a bounded question:

> Is the repository missing a shared distinction or invariant?

It does not prove that one exists.

### Universalizing a domain-specific ontology

A useful state model in one product does not become a generic Sensemaking schema.

### Strategy escalation by depth count

Reaching fourth/fifth-order reasoning does not automatically reopen Level 3.
The evidence must actually change a strategic claim, path, boundary, or decision.

## 11. Compact use

For a locally obvious but potentially consequential change, ask:

~~~text
1. What does this directly change?
2. Who/what consumes the changed thing?
3. What later behavior follows from those consumers?
4. Do repeated effects reveal one missing invariant/abstraction?
5. Does architecture materially obstruct that invariant?
6. Does any of this change Level 3 / Level 4?

At each step:
Would going one level deeper change the decision?

no -> stop
yes -> continue one level
~~~

## 12. Governing rule

> **Reason at the smallest system scale that preserves correctness. Increase
> consequence depth only while the next layer can materially change the
> problem, responsibility, solution, verification, or governing invariant.**
