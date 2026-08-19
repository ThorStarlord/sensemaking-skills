# Research: Selecting Among Competing Live Uncertainties

**Status:** research protocol / product-design study  
**Authority:** not an ADR, not a product contract, not a Workflow-v0 change  
**Tracker:** Issue #204  
**Baseline when opened:** `main@65c2be1b430e7bc8d1400ca99d80c6ff6256a051`  
**Parent research:** `docs/research/uncertainty-selection.md`  
**Related control study:** `docs/research/warrant-as-control-primitive.md`

## 1. Research question

> **When several currently-live unresolved dependencies could each materially change the next consequential decision, how should the agent choose which one to resolve first without introducing a brittle numeric scoring system?**

This study extends Research Path 1. It does not replace the current operating rule:

> **Resolve the nearest currently-live unresolved decision-changing dependency before committing to the consequential action.**

The PR #164 falsification established that an unresolved historical question is not necessarily a currently-live decision dependency. This study intentionally targets the harder case where two or more uncertainties are genuinely live at the same decision point.

Research Path 2 supplies a control frame rather than new machinery:

> **What do current evidence and required authority warrant for this specific target now?**

## 2. Working hypotheses

### H1 — dependency proximity usually dominates when a real dependency order exists

If a credible contrary answer to uncertainty A would invalidate the entire responsibility in which uncertainty B matters, A should normally be resolved first.

A case that is fully explained by this rule is useful normal-use evidence but is not a strong Path-01b stress case.

### H2 — genuinely parallel cases require qualitative comparison

When neither uncertainty clearly invalidates the other's decision surface, compare them using:

- **dependency proximity** — how early the uncertainty sits in the warrant for the contemplated decision;
- **decision branching** — which consequential decisions could change if the answer differs;
- **alternative plausibility** — whether contrary answers have credible support in current evidence;
- **wrong-action exposure** — cost, propagation, external visibility, reversibility, and false-closure risk if the assumption is wrong;
- **evidence economy** — cost and reliability of obtaining authoritative evidence;
- **option preservation** — whether acting or investigating preserves future alternatives;
- **authority effect** — whether the answer changes who may decide, act, publish, merge, or close.

These are reasoning prompts, **not scores**. Do not assign numbers, weights, rankings, pseudo-points, or a composite value.

### H3 — pairwise explanation should be sufficient

A useful selection should be explainable prospectively as:

```text
resolve A before B because ...
```

The study is weakened if reliable choices require a hidden or explicit numeric ranking mechanism.

### H4 — selection quality is observable through decision effect

Resolving the selected uncertainty first should change or materially confirm a consequential decision more usefully than the plausible alternative would have, considering evidence cost and wrong-action exposure.

Relevant consequential decisions include:

- responsibility;
- scope;
- authority;
- continue / stop / escalate;
- closure or claim boundary.

Reducing uncertainty without changing or materially confirming one of those decisions is not sufficient evidence of good selection.

## 3. Case eligibility

A normal-use episode qualifies as a **strong Path-01b case** only when at least two uncertainties are simultaneously:

1. currently live in canonical evidence;
2. unresolved;
3. dependencies of the same contemplated consequential decision;
4. supported by credible alternative answers;
5. capable of materially changing responsibility, scope, authority, continuation, or closure;
6. resolvable through evidence available to the authorized surface; and
7. not trivially ordered by an obvious upstream/downstream dependency.

### Exclude already-solved case shapes

Do not count the following as strong Path-01b evidence:

```text
currently-live uncertainty
vs
stale historical question
```

PR #164 already supplied the liveness refinement.

Also do not count:

```text
ownership / responsibility uncertainty
vs
minor implementation-detail curiosity
```

when the former plainly invalidates the latter's decision surface. Existing Path-1 evidence already covers that pattern.

### Scarcity is evidence

Do not manufacture a qualifying case. If normal engineering work rarely produces genuinely competing live uncertainties, preserve that observation. Scarcity may itself support stopping this research without product changes.

## 4. Prospective observation protocol

Assign qualifying cases sequential IDs such as `CLU-001`, `CLU-002`, and so on.

The **pre-evidence section must be written before gathering the evidence selected to resolve A or B**. Repository orientation needed to establish that both uncertainties are live is allowed; the observation must not be backfilled only after the outcome is known.

Use this template.

```yaml
case_id: "CLU-XXX"
observed_at: "<timestamp>"
canonical_baseline: "<repository>@<exact-sha>"

goal: "<goal>"
authorized_scope: "<scope and authority boundary>"
contemplated_target: "<consequential decision currently under consideration>"

warrant_dependencies:
  - "<premise required for contemplated target>"
  - "<premise required for contemplated target>"

live_uncertainties:
  - id: "A"
    question: "<question>"
    evidence_of_liveness: "<why this is still live now>"
    credible_alternatives:
      - "<answer 1>"
      - "<answer 2>"
    decisions_it_could_change:
      - "responsibility|scope|authority|continuation|closure"

  - id: "B"
    question: "<question>"
    evidence_of_liveness: "<why this is still live now>"
    credible_alternatives:
      - "<answer 1>"
      - "<answer 2>"
    decisions_it_could_change:
      - "responsibility|scope|authority|continuation|closure"

pairwise_comparison:
  dependency_proximity: "<A vs B reasoning>"
  decision_branching: "<A vs B reasoning>"
  alternative_plausibility: "<A vs B reasoning>"
  wrong_action_exposure: "<A vs B reasoning>"
  evidence_economy: "<A vs B reasoning>"
  option_preservation: "<A vs B reasoning>"
  authority_effect: "<A vs B reasoning>"

selected_first: "A|B|act_now"
selection_rationale: "<prospective explanation>"
plausible_alternative_selection: "<what a competent alternative choice would be and why>"

# Fill the following only after the selected evidence-producing responsibility.
selected_evidence_responsibility: "inspect|probe|ask_owner|other"
evidence_obtained: "<authoritative evidence>"
decision_before: "<contemplated decision before evidence>"
decision_after: "<decision after evidence>"
decision_effect: "<what changed or was materially confirmed>"
new_live_uncertainty_exposed: "<none or question>"
stop_continue_reason: "<why act, continue investigating, escalate, or stop>"

counterfactual:
  would_alternative_have_been_better: "yes|no|unclear"
  likely_alternative_cost_or_effect: "<reasoned comparison based on available evidence>"
  rationale: "<why>"

research_assessment:
  strong_path01b_case: true
  selection_was_useful: "yes|no|unclear"
  framework_failure_observed: "<none or falsification/weakening signal>"
```

The YAML above is a **research observation template only**. It is not a repository schema, validation profile, runtime contract, or proposed persisted product artifact.

## 5. Evidence-program targets

Prefer **5–8 normal engineering episodes** before attempting synthesis. The number is a research target, not a quota that justifies inventing marginal cases.

Seek diversity where ordinary work provides it:

1. technical correctness vs authority/ownership;
2. scope identification vs implementation correctness;
3. reconciliation direction vs local repair;
4. finding-specific verification vs further implementation;
5. repository/history inspection vs empirical probe;
6. option-preserving evidence work vs irreversible state change.

Preserve non-qualifying episodes when they reveal that the hard case is rare, but do not count them toward the 5–8 target.

## 6. Counterfactual discipline

Every strong case must record a plausible alternative selection **before** resolving the chosen uncertainty.

After evidence arrives, ask:

- would resolving the alternative first have led to the same decision?
- would it have produced useful evidence anyway?
- would it have cost materially more or less?
- would it have delayed discovery of the decisive premise?
- would it have caused unnecessary irreversible work or false closure?
- could the alternative actually have been better?

The purpose is to make the policy falsifiable. Do not treat the path actually taken as correct merely because it produced an answer.

## 7. Independent-review stress test

When 2–3 sufficiently ambiguous strong cases exist, preserve the **pre-decision evidence only** and ask independent competent reviewers to choose:

```text
A first
B first
act now / investigate neither
```

Each reviewer must provide rationale without seeing the eventual outcome.

Interpret outcomes as research evidence:

```text
same selection + same rationale
-> candidate qualitative rule may be robust

same selection + different rationale
-> selection may be stable while theory remains underspecified

different selection + both reasonable
-> genuine unresolved control ambiguity

different selection because case framing differs
-> observation representation may be unstable

both reject investigation
-> eligibility criteria may have overstated decision value
```

Do not force consensus.

## 8. Falsification and weakening criteria

Treat the Path-01b hypothesis as weakened or falsified if repeated evidence shows one or more of:

### F1 — arbitrary selection

Competent reviewers repeatedly choose different uncertainties and the disagreement cannot be explained by stable qualitative principles.

### F2 — retrospective rationalization

The framework can justify whichever path happened to be taken after the outcome is known but does not improve prospective selection.

### F3 — information-gain substitution

Agents repeatedly prefer the uncertainty that yields more information rather than evidence with greater effect on the consequential decision.

### F4 — excessive metareasoning overhead

Choosing which uncertainty to resolve costs roughly as much as resolving both, making the control policy economically pointless.

### F5 — hidden numeric ranking

The qualitative prompts become an unofficial point system or require stable weights to produce decisions.

### F6 — dependency-graph instability

Competent agents cannot reliably identify the warrant dependencies or which ones are current enough for `nearest` to have useful meaning.

### F7 — case scarcity

Genuinely competing-live cases are too rare in ordinary software-engineering work to justify dedicated product machinery or continued focused research.

## 9. Stopping rule

Stop dedicated Path-01b research under either outcome.

### Supported enough

Several independent normal-use cases show that:

- current liveness can be established;
- pairwise qualitative reasoning materially improves or clarifies selection;
- counterfactual review identifies avoided cost, risk, or wasted investigation;
- reviewer disagreement is explainable rather than arbitrary;
- no numeric machinery is needed.

### Weakened or falsified

Cases show that:

- the problem is too rare;
- pairwise reasoning adds little practical value;
- selection remains arbitrary;
- resolving both is usually cheaper;
- the qualitative dimensions do not help prospectively; or
- another abstraction explains the cases better.

Do not continue merely to accumulate a preferred conclusion.

## 10. Synthesis artifact

If sufficient evidence accumulates, produce a separate synthesis note that contains:

1. research question and baseline rule;
2. qualifying and rejected case counts;
3. empirical episodes;
4. pairwise-selection findings;
5. counterfactual analysis;
6. independent-review results;
7. falsifications and refinements;
8. supported qualitative rule, if any;
9. stopping conclusion;
10. remaining uncertainty;
11. whether research attention should move to Path 3.

The synthesis must conclude one of:

```text
SUPPORTED_ENOUGH
WEAKENED
FALSIFIED
```

Those are research dispositions, not runtime states.

## 11. Machinery-promotion boundary

Success of this research does **not** itself warrant:

- an uncertainty score;
- a ranking engine;
- a `decision_value` field;
- a `warrant_dependency` schema or product artifact;
- a new Skill;
- automatic routing;
- a new workflow lifecycle;
- runtime/orchestrator changes;
- a WarrantEngine or warrant schema;
- EXP-0006 merely to demonstrate the experiment infrastructure.

Any later promotion must independently satisfy the repository's existing machinery-promotion rule:

```text
repeated useful responsibility
+ stable enough semantics
+ repeated manual burden/error
+ mechanically expressible boundary
        -> candidate for formalization
```

Interesting theory alone is not sufficient.

## 12. Handoff to Research Path 3

If this study becomes `SUPPORTED_ENOUGH`, the next research priority should be the decision/orchestration boundary:

> **Does orchestration faithfully coordinate the responsibility selected from evidence, or does available workflow machinery begin selecting the work indirectly?**

Path 01b should provide the contested decision cases needed to stress that boundary. No Path-3 implementation or experiment is authorized by this document.