# Sensemaking Control-Model Research Agenda

**Status:** research hypotheses only  
**Authority:** not an ADR, not a product contract, not a roadmap commitment  
**Current application domain:** agentic software engineering / repository-centered engineering  
**Purpose:** preserve promising questions without prematurely turning them into
Skills, schemas, workflows, validators, or runtime machinery.

## Current product baseline

The current product does not depend on the hypotheses in this document.
Sensemaking Skills is presently an agent-native engineering sensemaking and
control layer for software-engineering agents. The active coding agent owns the
top-level loop; bounded Skills perform responsibilities; durable evidence,
validation, reconciliation, verification, and authority constrain what may be
claimed or done.

The current operating rule is:

> **Resolve the nearest unresolved decision-changing uncertainty before
> committing to the eventual solution.**

Research should improve or falsify that rule through normal use. It should not
replace the current operating model merely because a more general theory is
possible.

## Research path 1: responsibility selection under uncertainty

### Question

How should a Sensemaking agent determine which unresolved uncertainty is worth
resolving before acting?

### Why this matters

A repository may contain many unknowns. Investigating all of them is wasteful,
while ignoring a cheap uncertainty that could invalidate the planned action can
produce confident work on the wrong problem.

The current heuristic is **nearest unresolved decision-changing uncertainty**.
Useful research questions include:

- What makes an uncertainty genuinely decision-changing rather than merely
  interesting?
- What does "nearest" mean operationally?
- How should the risk of acting while uncertain affect selection?
- How should the cost of obtaining evidence affect selection?
- When does an uncertainty block action, and when can it remain open?
- When is available evidence sufficient to act rather than continue
  investigating?

### Concepts worth studying

Decision-making under uncertainty and value-of-information reasoning may offer
useful vocabulary. A qualitative decision frame to test is:

```text
potential decision impact
+ likelihood that new evidence changes the decision
+ risk/cost of acting while unresolved
- cost of resolving the uncertainty
```

This is **not** a proposal for a numeric scoring system. Any formalization should
be earned by repeated cases where the existing qualitative heuristic fails.

### Evidence that would justify deeper formalization

- repeated normal-use cases where agents investigate irrelevant uncertainties;
- repeated cases where agents act before resolving a cheap, consequential
  uncertainty;
- repeated disagreement between competent reviewers about which uncertainty
  should govern the next responsibility;
- repeated inability to explain why one unresolved uncertainty was selected
  over another.

## Research path 2: warrant as a control primitive

### Question

Is **warrant** a useful common abstraction connecting evidence to responsibility,
action, continuation, claims, and authority?

Observed pattern:

```text
evidence
  -> unresolved uncertainty
  -> updated warrant
  -> responsibility / action / stop

performed responsibility
  -> new evidence
  -> updated warrant
```

Related questions:

- What evidence warrants selecting a responsibility?
- What evidence warrants implementation rather than further investigation?
- What evidence warrants a work claim?
- What evidence warrants closure of an original finding?
- What authority warrants acting or publishing even when the technical evidence
  is sufficient?

This may be more fundamental than the current word `workflow`, but it is not yet
an encoded artifact or state machine. Do not introduce a warrant schema until
normal-use evidence demonstrates that explicit representation solves a recurring
problem.

## Research path 3: decision versus orchestration

### Question

Which decisions belong to evidence-grounded responsibility selection, and which
belong to execution coordination?

The current architectural boundary is documented in
`docs/decision-orchestration-boundary.md`:

> **Decision selects the work; orchestration coordinates the work.**

Research should watch for two opposite failure modes:

1. **orchestration swallows decision** -- fixed/automatic routing selects an
   implementation path before the relevant uncertainty is resolved;
2. **decision swallows orchestration** -- Sensemaking grows into generic
   scheduling, retry, DAG, queue, persistence, or worker-management machinery
   that does not improve responsibility selection.

A boundary should be revisited only when real use repeatedly cannot express a
needed transition cleanly with the current agent-owned loop and bounded
subflows.

## Research path 4: domain-general control versus domain-specific semantics

### Question

Which parts of the Sensemaking control model are intrinsic to software
engineering, and which remain valid when the domain ontology,
responsibilities, evidence, and authority model are replaced?

### Current position

Sensemaking Skills is a **domain-specific software-engineering product built
around a potentially domain-general control principle**.

The following are candidate domain-general concepts:

- goal and current state;
- decision-changing uncertainty;
- warranted responsibility selection;
- evidence-bounded claims;
- distinction between knowing, deciding, acting, and publishing;
- continuation, stopping, and escalation;
- outcome-specific verification.

The following are clearly software-engineering-specific examples:

- repositories, source files, tests, CI, issues, pull requests;
- repair, refactor, component retirement, vendoring reconciliation;
- canonical branch state and merge/publication evidence.

### Transfer test

Do not build a generic framework first. Instead, use a materially different
problem domain as a transfer experiment and ask whether the same control policy
still behaves naturally while only domain semantics change.

AI research is a plausible future test domain because it overlaps with software
engineering while introducing different responsibilities and evidence:

```text
software engineering:
  usage research -> repair / retire / reconcile -> tests / CI -> repair verification

AI research:
  literature review -> hypothesis -> baseline reproduction -> experiment
  -> replication / ablation -> research-claim verification
```

If the core decision logic survives while the responsibility/evidence model is
replaced, that is evidence for domain generality. If the core must be rewritten,
that is evidence that software semantics are doing essential work.

## Deferred architecture hypothesis: domain specializations

A future architecture might separate a reusable control model from
problem-domain-specific responsibility/evidence semantics. "Domain pack" is
useful shorthand for that possibility, but **no domain-pack feature is currently
ratified or warranted**.

If ever earned, a domain specialization would likely contain more than Skills:

- responsibility taxonomy;
- evidence types and contracts;
- verification semantics;
- authority semantics;
- domain vocabulary/objects;
- capability/Skill registry.

Do not create plugin infrastructure, a Sensemaking Core package, or AI-research
specialization until transfer evidence demonstrates a real need.

## Research discipline

Use the same machinery-promotion rule as the agent-native operating workflow:

```text
repeated useful responsibility
+ stable enough semantics
+ repeated manual burden/error
+ mechanically expressible boundary
        -> candidate for formalization
```

Not:

```text
interesting theory
        -> new abstraction / schema / Skill / runtime
```

For each research path, prefer preserving concrete episodes from normal
engineering work:

1. goal and authorized scope;
2. evidence available at the decision point;
3. unresolved uncertainties considered;
4. responsibility actually selected;
5. alternative responsibility that seemed plausible;
6. what new evidence changed or confirmed the decision;
7. whether the chosen investigation/action was useful;
8. whether a recurring failure boundary emerged.

## Current priority

The highest-value research thread is:

> **How should a Sensemaking agent determine which unresolved uncertainty is
> worth resolving before acting?**

Explore decision-making-under-uncertainty concepts only insofar as they sharpen
that product problem. Cross-domain transfer and domain-specialization
architecture remain secondary until the software-engineering control loop has
more normal-use evidence.
