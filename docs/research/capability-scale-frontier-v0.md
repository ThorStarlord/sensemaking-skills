# Capability Scale Frontier v0

**Status:** descriptive research / roadmap-selection model  
**Date:** 2026-10-04  
**Authority:** non-authoritative; subordinate to product strategy, ADR 0029, current Level-3 state, Skill contracts, authority policy, and repository evidence  
**Runtime effect:** none; this document introduces no Skill, score, maturity level, planner, router, state machine, schema, benchmark suite, or implementation authority

## 1. Purpose

Sensemaking Skills already has strong machinery for strategic analysis, bounded
responsibility selection, authority, evidence return, reconciliation, and
normal-use observation. What it lacks is one explicit map for answering:

> **At what scale has a capability actually been demonstrated, and which
> adjacent scale should be stressed before the repository builds more?**

This document defines the **Capability Scale Frontier**.

It is not a feature roadmap and not a maturity score. It is a qualitative map
of demonstrated capability boundaries.

~~~text
capability exists
!= capability demonstrated at every scale

one high-scale episode
!= support for every lower or adjacent combination

higher axis value
!= better automatically

scale coordinate
!= score

stress case
!= implementation responsibility automatically
~~~

The intended control loop is:

~~~text
current evidence
-> current qualified envelope
-> nearest consequential adjacent frontier
-> smallest discriminating stress / normal-use case
-> PASS: expand evidence claim, build nothing
-> FAIL: identify smallest missing capability
-> build only if warranted
-> re-test failed boundary
-> reconcile
-> stop
~~~

## 2. Why a multidimensional model is required

Sensemaking can be mature on one dimension and weakly evidenced on another.

For example, a system may be:

- strong at repository-wide semantic analysis;
- weakly evidenced at fresh-context continuation;
- strong at authority boundaries;
- unproven at autonomous target selection;
- able to reason across repositories while intentionally not owning a
  multi-repository execution runtime.

A single maturity level would collapse these distinctions.

~~~text
"advanced"
!= precise capability claim

"Level 4"
!= tested under every relevant pressure
~~~

Use independent descriptive axes instead.

## 3. Axis A — Decision Scope

Question:

> **How large is the decision object Sensemaking must reason about?**

| Position | Description |
| --- | --- |
| A0 | Local implementation detail |
| A1 | Bounded engineering responsibility |
| A2 | Subsystem / workflow |
| A3 | Whole repository / product repository |
| A4 | Explicit caller-selected multi-repository set |
| A5 | Product-thesis / Level-4 boundary |

Examples:

~~~text
A0  rename a field
A1  repair a validator
A2  repair a cross-workflow continuity defect
A3  determine what the repository should build next
A4  determine capability ownership across Sensemaking and Dark Factory
A5  decide whether the product thesis itself should change
~~~

A5 is often a reserved decision boundary. Correct behavior may be escalation,
not independent action.

## 4. Axis B — Consequence Depth

Question:

> **How far must reasoning follow effects before the correct responsibility is
> stable?**

| Position | Description |
| --- | --- |
| B1 | Direct effect |
| B2 | Downstream consumer/dependency |
| B3 | Effects of downstream effects / delayed propagation |
| B4 | Shared invariant or missing abstraction |
| B5 | Architectural embodiment |
| B6 | Strategic/product implication |

This axis is descriptive. The correct depth is the **shallowest depth that
preserves correctness**.

~~~text
higher B
!= stronger answer automatically

next consequence layer cannot change the decision
-> stop
~~~

See `consequence-depth-and-systems-reasoning-v0.md` when that document is
integrated.

## 5. Axis C — Epistemic Messiness

Question:

> **How difficult is current repository reality to know correctly?**

| Position | Description |
| --- | --- |
| C0 | Explicit, current, internally consistent |
| C1 | Incomplete but straightforward |
| C2 | Ambiguous / several plausible interpretations |
| C3 | Stale or partially superseded evidence |
| C4 | Conflicting authoritative-looking sources |
| C5 | Misleading local evidence / false closure pressure |
| C6 | Genuine external or owner-reserved unknown |

Examples:

~~~text
C0  issue matches current code and tests
C3  STATUS describes pre-merge reality
C4  docs say X, tests imply Y, implementation does Z
C5  focused green test suggests closure while product claim remains false
C6  only owner intent / external provider reality can resolve the question
~~~

This axis directly exercises Sensemaking's core value: determining what evidence
should govern the next responsibility.

## 6. Axis D — Temporal / Continuation Horizon

Question:

> **How long must coherent decision state survive?**

| Position | Description |
| --- | --- |
| D0 | One isolated decision |
| D1 | One responsibility |
| D2 | Several responsibilities in one bounded episode |
| D3 | Long mission in one context |
| D4 | Fresh-context resume from durable repository state |
| D5 | Multi-session / long-running durable continuation |
| D6 | Cross-episode institutional/capability learning |

The repository may support the semantics of a higher position while durable
runtime ownership belongs elsewhere. In particular, mature D5 execution/runtime
continuation belongs to Dark Factory where the factory-runtime boundary applies.

## 7. Axis E — Responsibility Breadth

Question:

> **How many qualitatively distinct responsibilities must compose correctly?**

| Position | Description |
| --- | --- |
| E0 | One known task |
| E1 | Diagnose -> fix |
| E2 | Analyze -> select responsibility -> execute |
| E3 | Execute -> verify -> reconcile -> continue |
| E4 | Repeated responsibility cycles |
| E5 | Strategy -> multiple responsibilities -> terminal outcome |

This is an autonomy-depth axis, not a task-count axis.

~~~text
ten mechanical subtasks
!= E5

two semantically distinct responsibility cycles
may be more demanding than ten edits
~~~

## 8. Axis F — Authority Complexity

Question:

> **What authority boundary must be interpreted and respected?**

| Position | Description |
| --- | --- |
| F0 | Read-only reasoning |
| F1 | Local reversible work |
| F2 | Repository mutation |
| F3 | Branch / commit / PR creation |
| F4 | Merge authorized under repository policy |
| F5 | Release / deploy / external protected transition |
| F6 | Owner-reserved / Level-4 decision |

This axis is not an autonomy score.

~~~text
higher F
!= "agent should do more"

correct F6 result
may be STOP / OWNER_DECISION
~~~

Capability means using exactly the authority granted and refusing to infer
additional protected-transition authority.

## 9. Axis G — Repository / Environment Heterogeneity

Question:

> **How much does the operating environment vary?**

| Position | Description |
| --- | --- |
| G0 | Same repository shape repeatedly |
| G1 | Different subsystem/workflow in same repository |
| G2 | Different repository, similar engineering shape |
| G3 | Different repository and product/domain shape |
| G4 | Explicit multi-repository semantic problem |
| G5 | Different agent/harness/tool surface |
| G6 | Non-software domain transfer |

~~~text
works repeatedly on sensemaking-skills
!= general repository capability
~~~

Heterogeneity strengthens transfer claims only when attribution and evidence
remain clear.

## 10. Axis H — Learning Depth

Question:

> **How far does returned evidence change future reasoning capability?**

| Position | Description |
| --- | --- |
| H0 | No durable learning required |
| H1 | Evidence changes current action |
| H2 | Evidence changes current responsibility |
| H3 | Evidence changes repository strategy |
| H4 | Consequential lesson survives context handoff/resume |
| H5 | Several episodes support a reusable lesson candidate |
| H6 | Qualified reusable doctrine changes |
| H7 | Later normal use retains, revises, or retires doctrine |

~~~text
H6
!= model training

H6
= repository-governed reusable doctrine changed
~~~

See the Capability Learning Loop documentation when integrated.

## 11. A capability episode as a coordinate

A scale coordinate summarizes pressure exercised by an episode. It is not a
machine-readable schema and should not be required in ordinary work.

Example:

~~~text
clear local validator repair
A1 B1 C1 D1 E1 F2 G0 H1
~~~

A more demanding terminal mission might exercise:

~~~text
whole-repository product target
+ stale/conflicting evidence
+ systems consequences
+ several responsibilities
+ fresh-context resume
+ PR authority but no merge

A3 B4 C4 D4 E5 F3 G3 H3
~~~

A future cross-repository capability-learning episode could involve:

~~~text
A4 B5 C4 D6 E5 F3 G4 H6
~~~

Do not infer rectangular coverage from one coordinate.

~~~text
episode exercised A3 B4 C4 D4
!= every A0..A3 x B1..B4 x C0..C4 x D0..D4 combination is supported
~~~

Evidence claims remain episode-specific until heterogeneous corroboration
supports a broader claim.

## 12. Qualified envelope

The **qualified envelope** is the set of capability combinations supported by
current evidence at an appropriate claim ceiling.

It may contain:

- mechanically qualified behavior;
- bounded normal-use support;
- cross-repository corroboration;
- fresh-context evidence;
- explicit limitations and excluded claims.

It is not necessarily convex, monotonic, or rectangular.

~~~text
qualified at one hard combination
!= all easier-looking combinations qualified

mechanically qualified
!= semantically useful in normal use

normal-use supported
!= universal transfer claim
~~~

## 13. Adjacent frontier

The **adjacent frontier** is a materially useful, insufficiently demonstrated
scale increase near the current envelope.

An adjacent frontier is worth attention only when:

1. it matters to the current product thesis or a current claim;
2. the missing evidence can change a repository/product decision;
3. the case can be bounded without manufacturing unrelated complexity;
4. success/failure has a clear interpretation;
5. the proposed stress does not violate product ownership boundaries.

Examples:

- D3 -> D4: same mission, fresh-context resume;
- E4 -> E5: move from repeated bounded responsibilities to a complete terminal
  outcome;
- F3 -> F4: exercise explicitly granted merge authority while preserving branch
  protection and exact-head qualification;
- G2 -> G3: apply the same semantic capability to a materially different
  repository shape;
- H4 -> H5: compare several preserved episodes for a reusable lesson candidate.

## 14. Stress-target rule

Do not test every combination.

Select the **smallest discriminating case** at the adjacent frontier.

~~~text
current supported envelope
        |
        v
one consequential adjacent uncertainty
        |
        v
smallest stress case that can distinguish:
SUPPORTED vs MISSING CAPABILITY
~~~

A useful stress case should vary as few material axes as possible.

The Autonomous Terminal Mission corroboration ladder is a good precedent:

~~~text
baseline
-> change repository shape
-> change context boundary
-> change target-selection responsibility
-> change merge authority
~~~

Each step adds one major variable.

## 15. Stress versus normal use

The standing normal-use evidence rule remains authoritative:

~~~text
real normal-use case already available
-> prefer normal-use evidence

cheap bounded synthetic stress
can answer a concrete decision now
-> synthetic stress may be warranted

no decision-changing uncertainty
-> do nothing
~~~

The Capability Scale Frontier must not become a benchmark factory.

Do not create:

- an exhaustive matrix;
- a synthetic fixture for every axis value;
- a numeric benchmark leaderboard;
- a target number of stress cases;
- a requirement to record coordinates for every task.

~~~text
scale model
!= benchmark suite

frontier exists
!= synthetic experiment warranted
~~~

## 16. PASS behavior

If an adjacent-scale stress passes:

1. preserve the exact evidence and claim ceiling;
2. expand the supported envelope only as far as the evidence warrants;
3. do not build a feature merely because a test completed;
4. identify whether another adjacent frontier is actually decision-relevant;
5. otherwise stop.

~~~text
PASS
-> evidence claim may expand

PASS
!= new feature needed
~~~

## 17. FAIL behavior

If a stress fails:

1. identify the smallest common failure mechanism;
2. determine whether the issue is guidance, contract, implementation,
   verification, authority interpretation, or external/runtime ownership;
3. prefer an existing surface when it can absorb the fix;
4. build the smallest missing capability only when failure evidence warrants it;
5. rerun the failed boundary;
6. test one nearby case when needed to detect overfitting;
7. reconcile and stop.

~~~text
FAIL
!= build the originally imagined feature

FAIL
-> learn what capability is actually missing
~~~

## 18. Construction roadmap from scale

The roadmap is generated from evidence rather than maintained as a fixed feature
sequence.

~~~text
roadmap
=
current qualified envelope
+ product-relevant adjacent frontier
+ decision-changing evidence
~~~

A provisional current sequence is:

### Wave 1 — integrate current doctrine

- Capability Learning documentation;
- Consequence-Depth / systems-reasoning documentation;
- reconcile relationships without new runtime.

### Wave 2 — continuation scale

Primary axes: D + E.

Stress:

~~~text
multi-responsibility mission
-> complete/reconcile one responsibility
-> context break
-> fresh session / clean workspace
-> reconstruct terminal goal and current responsibility
-> continue correctly
~~~

### Wave 3 — selection scale

Primary axes: A + C + E.

Remove the pinned next responsibility and test whether the agent identifies the
highest-leverage warranted bottleneck rather than the easiest local work.

### Wave 4 — authority scale

Primary axis: F.

With explicit merge authority on a bounded mission, test:

~~~text
implement
-> exact-head qualification
-> base-drift check
-> branch/review policy
-> merge only when authorized and permitted
-> post-merge reconciliation
-> continue / stop correctly
~~~

### Wave 5 — learning scale

Primary axis: H.

After several meaningful episodes:

~~~text
episode A
episode B
episode C
        |
        v
recurring capability pattern?
        |
      no/yes
        |
        +-> local/historical knowledge
        +-> bounded reusable lesson candidate
~~~

Only repeated operational need should warrant a specialized capability-learning
Skill or stable lesson-candidate artifact.

### Later — heterogeneity and multi-repository semantic scale

Primary axis: G.

Scale semantic ownership/boundary reasoning across explicit repository sets
without turning Sensemaking into a durable scheduler/worker runtime.

## 19. Current rough frontier

This table is descriptive and intentionally qualitative.

| Axis | Current rough evidence posture | Next meaningful frontier |
| --- | --- | --- |
| A — Decision Scope | strong repository-wide and explicit multi-repository analysis | more heterogeneous real strategic decisions |
| B — Consequence Depth | explicit doctrine being added | normal-use evidence that zoom-out/stop triggers are well calibrated |
| C — Epistemic Messiness | strong semantic/evidence machinery | harder real stale/conflicting/false-closure cases |
| D — Continuation Horizon | multi-responsibility support; fresh-context claim limited | fresh-context autonomous resume |
| E — Responsibility Breadth | terminal-mission semantics and one bounded trial | autonomous highest-leverage target/responsibility selection |
| F — Authority Complexity | explicit protected-transition semantics | merge-authorized continuation under real repository policy |
| G — Heterogeneity | multiple repository shapes conceptually/partially exercised | cross-repository corroboration with clean attribution |
| H — Learning Depth | episode/repository learning strong; capability-learning model candidate | repeated cross-episode synthesis and doctrine evidence |

This table does not override `STATUS.md` or establish current work by itself.

## 20. Relationship to the Strategic Frontier

The two concepts answer different questions.

~~~text
Strategic Frontier
= which repository futures are materially decision-relevant?

Capability Scale Frontier
= at what complexity has the current capability been demonstrated,
  and what adjacent scale is worth testing?
~~~

A scale frontier may inform Level-3 analysis, but does not itself select a
construction path.

~~~text
unsupported scale
!= Strategic Frontier item automatically
~~~

## 21. Relationship to System Capability Atlas

~~~text
System Capability Atlas
= what major systems exist and what they own

Capability Scale Frontier
= how far their composed capability has been demonstrated
  and which adjacent pressure is worth evidence
~~~

The atlas remains the product/system ownership map. This document remains the
capability-envelope and roadmap-selection lens.

## 22. Relationship to Capability Learning

Capability Learning operates after episodes produce consequential learning.

~~~text
scale stress / normal use
-> evidence
-> reconciliation
-> several comparable episodes
-> possible reusable lesson
-> qualified doctrine change
~~~

The scale model helps select useful evidence boundaries. It does not itself
perform learning or generalization.

## 23. Anti-patterns

### Maturity score

Do not collapse the axes into:

~~~text
Sensemaking maturity = 73/100
~~~

### Max-scale optimization

The product does not need to maximize every axis. Some boundaries should remain
reserved or downstream-owned.

### Benchmark theater

Do not create fixtures merely to populate the model.

### Frontier-by-feature imagination

Do not assume a new feature is required because an adjacent scale is untested.

### Claim inflation

One difficult PASS does not establish universal support.

### Runtime ownership leakage

Do not use D5/G4 pressure as justification to recreate Dark Factory scheduling,
queueing, retry, workers, or durable software-factory runtime inside
Sensemaking.

## 24. Current disposition

~~~text
CAPABILITY_SCALE_FRONTIER_V0
= DOCUMENTATION_MODEL

EIGHT_SCALE_AXES
= DESCRIPTIVE / ACCEPTED FOR ROADMAP REASONING

SCALE_SCORE
= REJECTED

FIXED FEATURE ROADMAP
= NOT PRIMARY MODEL

ADJACENT_FRONTIER ROADMAP
= PREFERRED

SYNTHETIC STRESS
= ONLY WHEN DECISION-DISCRIMINATING

NORMAL_USE EVIDENCE
= PREFERRED WHEN AVAILABLE

NEW SKILL
= NOT WARRANTED

NEW RUNTIME / SCHEMA
= NOT WARRANTED

STATUS / STRATEGIC FRONTIER REOPENING
= NOT IMPLIED
~~~

## 25. Governing rule

> **Expand one evidence-supported capability frontier at a time. Stress the
> nearest consequential unsupported scale, and build only when the failure
> teaches what capability is actually missing.**
