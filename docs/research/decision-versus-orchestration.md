# Path 3 — Decision Versus Orchestration

**Status:** research protocol / bounded repository-grounded boundary study  
**Authority:** research only; not an ADR, product contract, runtime specification, Skill, schema, or routing rule  
**Tracker:** Issue #210  
**Protocol baseline:** `main@56ae3c323f1717615cfb2c9036f4b83404582eeb`

## 1. Research question

> **Across concrete repository-grounded episodes, can the current decision/orchestration boundary distinguish responsibility-selection decisions from execution-control decisions without either orchestration swallowing decision or Sensemaking swallowing orchestration?**

The current architectural sentence is:

> **Decision selects the work. Orchestration coordinates the work. Evidence determines what becomes warranted next.**

This study asks whether that sentence actually constrains design reasoning across repository evidence rather than functioning only as attractive prose.

## 2. Bounded claim

The strongest positive claim this cycle may support is:

> **Across the bounded repository-grounded episodes studied, the current decision/orchestration distinction provides a coherent explanatory boundary: evidence-grounded responsibility selection remains agent-owned, while deterministic coordination may proceed after responsibility selection without acquiring authority to change the engineering responsibility.**

A positive result does **not** establish:

- universal architectural adequacy;
- optimal workflow design;
- runtime completeness;
- real-world prevalence of either failure mode;
- that every future transition has a unique classification;
- that decision and orchestration can never interact;
- warrant for automatic routing or generic runtime machinery.

## 3. Boundary definitions

### 3.1 Decision

Decision answers:

> **Given current goal, evidence, uncertainty, and authority, what responsibility is warranted next?**

Decision may select:

- another evidence-producing responsibility;
- implementation;
- verification;
- reconciliation;
- stopping;
- escalation;
- a human decision;
- `act now` without resolving adjacent non-gating uncertainties.

Decision remains defeasible. New evidence may change the warranted responsibility.

### 3.2 Orchestration

Orchestration answers:

> **How should an already-selected responsibility be coordinated and performed?**

Legitimate orchestration may include:

- invoking a selected Skill/tool/script/subflow;
- sequencing mechanically stable steps;
- passing declared inputs and artifact paths;
- collecting output and validator evidence;
- applying bounded retry/wait/timeout/failure policy;
- returning evidence to the active agent for reassessment.

An execution-control decision is not automatically a product-level decision. Retrying an already-selected deterministic step does not authorize selecting a new engineering responsibility.

## 4. Two failure modes

### F1 — orchestration swallows decision

A predetermined route, workflow node, compatibility table, retry/fallback path, or automation implicitly chooses a materially different engineering responsibility before evidence and authority warrant it.

Canonical suspicious shapes include:

- routing directly from diagnostic metadata to an engineering workflow;
- continuing `inspect -> repair -> test` after evidence redirects the responsibility to retirement/reconciliation;
- treating a failed execution attempt as authority to choose a different responsibility;
- using fallback machinery to cross an authority or product boundary silently.

### F2 — decision swallows orchestration

Sensemaking begins owning generic execution infrastructure that does not improve responsibility selection, evidence interpretation, authority reasoning, or claim verification.

Canonical suspicious shapes include:

- generic worker scheduling;
- queues and generic DAG execution;
- generic persistence for runtime continuity;
- generic retry/backoff/timeout policy;
- broad job orchestration with no decision semantics.

## 5. Episode eligibility

An episode qualifies when repository evidence can establish enough of the following to classify the boundary prospectively rather than by slogan:

1. a contemplated consequential decision or selected responsibility;
2. evidence/uncertainty/authority relevant to that responsibility;
3. an execution/orchestration mechanism that exists or was seriously proposed;
4. a plausible alternative placement of the behavior across the boundary;
5. a decision effect if the behavior is placed incorrectly.

Do not include an episode merely because it contains a workflow or a human judgment. The episode must illuminate control ownership.

Prefer 6–8 episodes with coverage of both F1 and F2, including at least:

- one historical unsafe routing shape;
- one responsibility-redirection case;
- one legitimate deterministic execution subflow;
- one execution failure/stop boundary;
- one authority boundary;
- one generic-runtime non-goal;
- one ambiguous edge case if the repository provides one.

## 6. Initial repository-grounded candidate families

These are **candidate episodes, not findings**. Each must be inspected before use.

### E1 — superseded ADR 0018 deterministic fog routing

Historical proposal: `primary_fog_type` deterministically selected a downstream workflow.

Research use: likely F1 control. Determine whether the routing table selected an engineering responsibility too early or merely coordinated an already-selected one.

### E2 — PR #164 / Path 1 stale-uncertainty falsification

Historical shape: a remembered unresolved question was no longer a live decision dependency.

Research use: test whether a fixed path would have continued work that current evidence no longer warranted.

### E3 — bounded campaign lifecycle coordination

Possible evidence: reservation, invocation boundary, output capture, exact-head validation, terminalization.

Research use: identify execution-control transitions that can be deterministic because the campaign responsibility and authorization envelope were already selected.

### E4 — EXP-0004 approval-audit failure

Historical shape: execution stopped before invocation when the active surface could not truthfully satisfy the approval-reference contract.

Research use: test whether orchestration correctly failed closed rather than selecting a replacement authorization interpretation or alternative responsibility.

### E5 — EXP-0005 exact-head validation

Historical shape: deterministic validation checked already-produced evidence; later research disposition remained a decision-layer interpretation.

Research use: test clean handoff from execution evidence back to decision/research judgment.

### E6 — Path 01b `act_now`

Synthetic control: unresolved adjacent questions remained non-gating for a cheap reversible action.

Research use: clarify that decision can stop investigation and authorize execution without turning orchestration into uncertainty selection.

### E7 — registered bounded workflow/subflow

Repository candidate: mechanically stable sequencing inside an already-selected responsibility.

Research use: positive orchestration control.

### E8 — generic scheduler/queue/runtime proposal boundary

Repository candidate: any proposal or adjacent mechanism that adds execution capability without improving responsibility selection.

Research use: F2 control.

## 7. Episode record

For each included episode record:

```text
Episode:
Repository evidence:
Contemplated decision:
Responsibility selected / under consideration:
Decision-changing evidence or uncertainty:
Authority boundary:
Orchestration mechanism:
Decision owner:
Orchestration owner:
Why the behavior belongs on that side:
Counterfactual if orchestration owned the decision:
Counterfactual if decision owned the orchestration:
Ambiguity / caveat:
Failure-mode signal: none | F1 | F2 | mixed
``` 

The counterfactuals are required. A classification is weak if it cannot explain what would go wrong when the behavior moves to the other side.

## 8. Evaluation criteria

### Evidence for a coherent boundary

The boundary is supported when the episode set repeatedly shows that:

- decision determines **what responsibility should become the next node at all**;
- orchestration determines **which already-defined step runs next** within selected work;
- deterministic retry/wait/failure does not silently authorize a materially different engineering responsibility;
- execution returns evidence to the active agent rather than interpreting that evidence into a new responsibility automatically;
- mutation/publication/merge authority remains separate from mere technical capability;
- generic runtime mechanics can stay outside the product thesis unless they solve a recurring decision-boundary problem;
- equivalent transition shapes can be classified consistently without hidden numeric or routing machinery.

### Evidence against or limiting the boundary

Weaken or falsify the boundary if the episode set repeatedly shows that:

- domain judgment must be embedded in orchestration for the system to choose correctly;
- deterministic execution policy must routinely choose between materially different engineering responsibilities;
- the decision layer requires generic scheduling/persistence/worker-management semantics to remain correct;
- equivalent transitions receive contradictory ownership classifications;
- the distinction cannot explain a consequential edge case without ad hoc exceptions;
- the boundary fails to constrain actual design decisions and only restates them after the fact.

## 9. Ambiguity discipline

Do not force every transition into a perfectly pure category.

A transition may involve both layers sequentially:

```text
decision: select verification responsibility
orchestration: run deterministic verification steps
observation: collect result
reassessment: decide whether closure is now warranted
```

The relevant question is not whether both layers participate. It is **which layer owns which semantic transition**.

If an episode remains genuinely ambiguous after inspection, preserve that ambiguity and treat it as evidence for `BOUNDARY_LIMITED` if material.

## 10. Bounded dispositions

The synthesis must conclude exactly one:

### `BOUNDARY_COHERENT`

The distinction explains the bounded repository-grounded episode set without material contradiction, and the counterfactual misplacement analysis shows why the ownership boundary matters.

### `BOUNDARY_LIMITED`

The distinction remains useful, but one or more consequential episode shapes require a refined rule, explicit exception, or stronger semantic boundary.

### `BOUNDARY_INCOHERENT`

The distinction repeatedly fails to classify consequential transitions without arbitrary placement or contradictory reasoning.

None of these dispositions establishes universal architectural adequacy.

## 11. Research sequence

1. Integrate this protocol before episode synthesis.
2. Inspect 6–8 durable repository episodes.
3. Freeze the chosen episode set and citations/identifiers before writing the final disposition.
4. Record each episode using the template above.
5. Compare F1 and F2 behavior across the set.
6. Write a bounded synthesis and disposition.
7. Keep results unmerged until owner integration authorization.

A governed experiment campaign is not required merely to perform retrospective repository-grounded analysis.

## 12. Machinery-promotion boundary

This study does **not** authorize or propose:

- automatic responsibility routing;
- revival of ADR 0018's fog-to-workflow policy;
- a decision score;
- a decision/orchestration schema;
- a runtime state machine;
- Workflow-v0 changes;
- workflow-registry changes;
- a new Skill;
- new retry/fallback behavior;
- a generic scheduler, queue, worker manager, persistence service, or DAG runtime.

Use the existing promotion rule only if later evidence earns it:

```text
repeated useful responsibility
+ stable semantics
+ repeated manual burden/error
+ mechanically expressible boundary
        -> candidate formalization
```

A coherent retrospective boundary study alone is insufficient.

## 13. Definition of done

This Path 3 cycle is complete when:

- this protocol is durable and reviewed on canonical `main`;
- 6–8 repository-grounded episodes are inspected with both F1 and F2 coverage;
- each included episode records decision owner, orchestration owner, evidence/authority boundary, and counterfactual misplacement risk;
- the chosen episode set is frozen before synthesis;
- ambiguous cases are preserved rather than forced into false precision;
- the synthesis concludes exactly one bounded disposition;
- the synthesis explicitly states that the bounded episode set does not establish universal architectural adequacy;
- no machinery is promoted merely because the boundary appears coherent.

## 14. Handoff

If the bounded result is coherent enough, the next research candidate is Path 4 — domain-general control versus domain-specific semantics.

If the result is limited or incoherent, the synthesis should identify the smallest boundary correction before transfer research proceeds.