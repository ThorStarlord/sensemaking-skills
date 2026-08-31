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

## Current compressed-control hypothesis

Recent bounded research suggests that several richer control concepts may be
explanatory vocabulary rather than independent operational primitives. The
current compressed research hypothesis is `C6R`:

1. **Target:** What consequential decision are you making?
2. **Evidence requirement:** What is the smallest reliable evidence needed to
   decide what to do next?
3. **Evidence economy:** Obtain that evidence with the least justified cost.
4. **Authority:** Do not exceed your authority.
5. **Claim scope:** Verify the specific claim before closure.
6. **Orchestration boundary:** Orchestration may coordinate the selected
   responsibility, but may not silently replace it with a materially different
   responsibility.

This is a **research hypothesis, not a product contract or runtime design**.
Concepts such as `act_now`, bounded joint evidence, live versus stale
uncertainty, stopping, and ambiguity may often be derivable from this smaller
loop, but that compression should be retained only while prospective,
independent, and normal-use evidence continues to support it.

### Evidence status

The control-model program has progressed through bounded synthetic coherence,
component ablation, compression, prospective testing, blind fresh-session
replication, and cross-model blind replication. Issues #223 through #225 record
key compression and replication steps. Issue #226 records the current
prospective gate-separation study motivated by the remaining tendency for models
to blur evidence needed to select responsibility, authority needed to act, and
verification needed before closure.

The strongest current positive claim remains deliberately limited: the compact
verbal policy has produced substantively compatible control behavior across a
bounded synthetic suite and multiple isolated model contexts. This does **not**
establish real-world effectiveness, prevalence, productivity benefit, objective
optimality, human-agent agreement, universal model independence, or production
readiness.

Issue #218 remains the standing normal-use evidence lane. Synthetic cases from
#226 do not count as normal-use episodes.

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

### Transfer evidence

Path 4 has now completed one bounded synthetic transfer exercise in AI-research
semantics; see `docs/research/domain-general-control-transfer.md`,
`docs/research/path-4-ai-research-transfer-cases.md`, and
`docs/research/path-4-domain-transfer-results.md`.

That exercise found the candidate control relationships coherent after replacing
software-engineering-specific responsibility, evidence, verification, and
authority semantics. The result is **limited conceptual-transfer evidence only**.
It does not establish real-world AI-research effectiveness, prevalence,
cross-agent reproducibility, organizational fit, or production readiness.

The transfer result does not warrant a generic framework. Further transfer work
should be driven by materially new uncertainty or real use, not by a desire to
accumulate more synthetic examples of the same relation.

## Candidate research direction: formative critique and independent review

**Status:** candidate / inactive  
**Authority:** research questions only; no execution program is authorized  
**Product effect:** none; no new Skill, responsibility contract, artifact,
workflow, validator, routing rule, or product-scope change is ratified here

The terms **critic** and **reviewer** are provisional shorthand in this section,
not canonical responsibility or Skill names. Their semantics and placement are
part of the research question.

This direction asks whether repository sensemaking would improve if diagnostic
work were challenged before completion and/or independently evaluated after
completion. It does **not** assume that either behavior belongs inside
`repo-sensemaker`.

### C1: formative diagnosis critique

**Question:** can a bounded challenge before a `repository_sensemaking_brief` is
finalized catch decision-changing blind spots without creating false uncertainty,
contrarianism, unnecessary owner questions, or analysis paralysis?

Candidate defects worth observing include:

- a strong competing consequential boundary was ignored;
- contradictory repository evidence was not considered;
- an assumption was presented as established fact;
- implementation or another downstream responsibility was selected before a
  cheap decision-changing uncertainty was resolved;
- a claim is stronger than its evidence;
- a recommendation crosses an authority boundary.

A useful critique changes something decision-relevant -- the consequential
boundary, warranted responsibility, claim scope, evidence requirement, owner
question, or decision to stop. The number of objections generated is not a
success measure. Critique should not exist merely to manufacture alternatives.

### C2: independent Brief review

**Question:** after a Brief is frozen, can a sufficiently independent evaluation
reliably detect consequential diagnostic defects that the producing agent missed,
beyond what current mechanical validation already establishes?

Candidate review dimensions include:

- grounding of repository claims;
- whether interpretations follow from cited evidence;
- separation of observations, interpretations, and hypotheses;
- support for the selected consequential boundary;
- omission of materially plausible alternative responsibilities;
- claim-scope and authority discipline;
- usefulness for deciding what responsibility is warranted next.

Independence is itself an empirical variable. Fresh context, a different agent
instance, a different model, holdout criteria, or independent evidence access may
help, but none is assumed sufficient merely because it is present.

A review result is evidence for the active agent. Consistent with
`docs/decision-orchestration-boundary.md`:

```text
review finding != next responsibility
```

### C3: responsibility placement

**Question:** if C1 or C2 demonstrates recurring value, where should the useful
behavior live?

Plausible outcomes include:

1. a lightweight conditional pass inside `repo-sensemaker`;
2. a separate reusable formative-critique responsibility;
3. a separate independent-review responsibility over a frozen Brief;
4. coverage by existing capabilities such as `architectural-review`, mechanical
   validators, `output-reconciler`, or finding-specific verification;
5. no dedicated responsibility because the incremental value does not justify
   additional machinery.

Evidence that critique or review is useful does **not** by itself establish
placement. Responsibility value should be demonstrated before architecture is
chosen.

### Evidence that would activate this direction

Do not start a synthetic critic/reviewer campaign merely because these questions
are now recorded. Activation should be driven by recurring decision-relevant
pressure, such as:

- normal-use episodes where a completed diagnosis later proves to have missed a
  strong competing boundary, contradictory evidence, or an authority problem;
- post-freeze evaluations that repeatedly identify consequential errors that the
  producer missed and mechanical validation could not detect;
- repeated cases where an independent finding changes the warranted
  responsibility rather than only improving prose;
- repeated manual burden around checking the same class of diagnostic defect.

Two existing evidence sources are especially relevant:

- **Goal A:** its frozen-Brief procedure already separates production from
  substantive evidence audit, semantic-quality review, and independent
  usefulness evaluation. Findings from those evaluations may reveal recurring
  defects worth studying, but Goal A does not by itself ratify a reviewer role.
- **Issue #218:** normal-use engineering episodes may reveal whether formative
  critique or independent review would have changed consequential decisions in
  ordinary work.

Neither source automatically activates a new research program. If recurring
findings appear, first characterize the defect class and ask whether a bounded
critique or review would have prevented or detected it. Only then consider a
prospective test.

### Promotion discipline

Use the repository's existing machinery-promotion rule. This candidate direction
becomes a formal responsibility only if evidence demonstrates:

```text
recurring consequential defect
+ bounded critique/review materially improves the decision
+ semantics are stable enough to describe
+ repeated burden/error justifies another responsibility
+ the boundary is mechanically or operationally expressible
        -> candidate for formalization
```

Not:

```text
critic/reviewer sounds useful
        -> evolve repo-sensemaker / create a Skill
```

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

### Autonomous-cycle stopping discipline

An autonomous research or engineering cycle should not continue merely because a
plausible next refinement can be invented.

Before beginning another cycle, state:

1. the **materially new consequential uncertainty** the cycle is intended to
   resolve;
2. why the existing evidence cannot already resolve it;
3. what observation could materially change the model, predicted behavior, or
   warranted action;
4. which evidence class is appropriate for that uncertainty.

If repeated cycles within the same evidence class no longer materially change
the model, predicted behavior, or warranted action, **change evidence class or
stop**. Useful evidence classes may include:

```text
thought experiment
  -> bounded synthetic adversarial case
  -> prospective frozen test
  -> independent fresh-context replication
  -> cross-model replication
  -> normal-use observation
  -> field intervention
```

This is a research-discipline rule, not a proposal for an automatic runtime loop
or stopping engine. The purpose is to prevent locally sensible continuation from
becoming an infinite refinement process.

## Current priority

The current priority is no longer to expand the control vocabulary. It is to
**test whether the compressed hypothesis survives the next stronger evidence
classes without adding machinery prematurely**.

Near-term priorities are:

1. complete Issue #226's blind evidence-authority-verification gate-separation
   study without modifying `C6R` before its preregistered result;
2. continue Issue #218's normal-use evidence lane and give genuine engineering
   episodes more weight than additional same-class synthetic refinements;
3. treat further synthetic work as warranted only when it targets a materially
   new behavioral failure or unresolved decision;
4. keep runtime, schema, scoring, routing, and generic-core formalization behind
   the existing repeated-use and mechanically-expressible-boundary gate.

The most important next question is therefore not whether another refinement can
be imagined, but whether the next consequential uncertainty requires a stronger
class of evidence.

## Meta-finding 2026-08-30: sensemaking loops saturated (Product Hypothesis B hardening)

Further sensemaking loops saturated; next evidence requires constructive spikes, not briefs. Dozens of `repo-sensemaker` runs and a full `experiments/product-hypothesis-b/` artifact sprawl (296 docs/109 historical in `auteur`) no longer changed the warranted responsibility. Three throwaway FULL spikes on `auteur` (`author_decisions` 42 lines/18 min, `structure` 38 lines/15 min, `genre_pipeline` 35 lines/14 min — total 115 lines/47 min) each yielded **0/3 decision change** vs PARTIAL (all `architecture_fog → docs-aligner`, only narrowed scope), meeting `CONTEXT.md:321` hardening for "conditional as default, FULL deferred." Future agents should not re-run sensemaking diagnosis to test this claim; replicate or falsify with a constructive FULL spike that shows a decision change, or stop.
