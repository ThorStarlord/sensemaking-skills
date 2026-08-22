# Research: Selecting Among Competing Live Uncertainties

**Status:** amended research protocol / evaluator-aware synthetic coherence study  
**Authority:** not an ADR, not a product contract, not a Workflow-v0 change  
**Tracker:** Issue #204  
**Original baseline:** `main@65c2be1b430e7bc8d1400ca99d80c6ff6256a051`  
**Synthetic-amendment baseline:** `main@cf959f0f5a262d78366f4dedb50cfb99f555e071`  
**Single-context-amendment baseline:** `main@35b5f3126d95529290ae8d9ebb0dad82e9b07548`  
**Parent research:** `docs/research/uncertainty-selection.md`  
**Related control study:** `docs/research/warrant-as-control-primitive.md`

## 1. Amendment summary

Path 01b originally required normal-use engineering episodes, then was weakened to a bounded synthetic stress study with isolated independent coding-agent passes. This amendment deliberately weakens the claim again because the currently available connected execution surface does not provide an isolated general coding-agent executor.

The immediate study may therefore use the already-frozen synthetic scenarios as an **evaluator-aware, single-context synthetic coherence exercise**. The same coding-agent context may apply the qualitative procedure to all scenarios even though it has seen the research protocol, evaluator relationships, and prior answers.

That change removes any claim of independent replication, blind invariance, framing robustness, or cross-agent reproducibility. The exercise is useful only for asking whether the proposed qualitative reasoning procedure can be applied coherently to adversarial worked examples without obvious contradiction, investigation compulsion, information-gain substitution, false precision, or numeric scoring.

The frozen scenario inputs themselves must not be rewritten merely to make later reasoning look better. Any scenario correction must be separately recorded as a protocol/input change before evaluation continues.

## 2. Research question

> **Given frozen synthetic competing-live-uncertainty scenarios and an explicit qualitative reasoning rubric, can a coding agent apply the procedure to produce coherent, auditable worked decisions without obvious contradiction, forced investigation, information-gain substitution, false precision, or numeric ranking?**

This study extends Research Path 1. It does not replace the current operating rule:

> **Resolve the nearest currently-live unresolved decision-changing dependency before committing to the consequential action.**

The PR #164 falsification established that an unresolved historical question is not necessarily a currently-live decision dependency. Path 01b remains focused on the harder case where two or more uncertainties are relevant to the same consequential decision.

Research Path 2 supplies a control frame rather than machinery:

> **What do current evidence and required authority warrant for this specific target now?**

## 3. Strongest permitted claim

The strongest claim this study is allowed to support is:

> **Within a bounded evaluator-aware single-context synthetic exercise, the qualitative Path 01b procedure can be applied to the frozen adversarial scenarios in an internally coherent and auditable way, while preserving `act_now`, exposing genuine ambiguity, preferring decision effect over generic information gain where warranted, and avoiding numeric scoring.**

A positive result is evidence of **internal conceptual coherence only**.

It does **not** establish:

- independent replication;
- blind invariance under A/B swaps or paraphrase;
- robustness to framing effects;
- reproducibility across coding agents, models, sessions, or contexts;
- that competing-live cases are common in ordinary engineering work;
- that the procedure improves real-world engineering outcomes;
- human-agent agreement;
- objective optimality of a selected uncertainty;
- production readiness;
- warrant for a score, ranking engine, schema, Skill, workflow, runtime mechanism, or EXP-0006.

The final synthesis must explicitly state:

> **This was an evaluator-aware, single-context synthetic coherence exercise. Independent execution, framing robustness, reproducibility across coding agents, real-world prevalence, and real-world effectiveness were not tested.**

## 4. Working hypotheses

### H1 — dependency proximity remains useful when a real dependency order exists

If a credible contrary answer to uncertainty A would invalidate the responsibility in which uncertainty B matters, resolving A first should remain a coherent qualitative choice.

### H2 — genuinely parallel cases can be discussed without numeric aggregation

When neither uncertainty clearly invalidates the other, compare qualitatively:

- **dependency proximity** — how early the uncertainty sits in the warrant for the contemplated decision;
- **decision branching** — which consequential decisions could change;
- **alternative plausibility** — whether contrary answers have credible support in the supplied evidence;
- **wrong-action exposure** — cost, propagation, external visibility, reversibility, and false-closure risk if wrong;
- **evidence economy** — cost and reliability of obtaining authoritative evidence;
- **option preservation** — whether acting or investigating preserves alternatives;
- **authority effect** — whether the answer changes who may decide, act, publish, merge, or close.

These are reasoning prompts, **not scores**. Do not assign numbers, weights, pseudo-points, or a composite ranking.

### H3 — pairwise explanation should remain intelligible

A useful worked decision should be explainable prospectively as:

```text
resolve A before B because ...
```

or, where warranted:

```text
act now / investigate neither because ...
```

The study is limited or incoherent if the reasoning repeatedly depends on hidden arithmetic, arbitrary preference, or conclusions that cannot be reconciled with the supplied facts.

### H4 — decision value should beat raw information gain

A broad uncertainty that would yield more information should not automatically outrank a narrower uncertainty whose answer more directly changes the consequential decision.

### H5 — the procedure must permit `act_now`

The coding agent must be able to conclude that neither uncertainty needs resolution before a cheap, reversible, warranted action.

### H6 — genuine ambiguity should remain visible

When the supplied evidence supports multiple defensible choices, the coding agent should preserve the tradeoff rather than manufacture false precision.

## 5. Frozen synthetic scenario suite

Use the frozen 12-scenario suite prepared under Issue #204. The suite covers:

1. evidence economy vs wrong-action exposure;
2. dependency proximity vs authority effect;
3. option preservation vs decision branching;
4. balanced ambiguity;
5. resolve-both / metareasoning-cost control;
6. `act_now` control;
7. information-gain trap;
8. irreversibility control;
9. A/B-label swap;
10. semantic paraphrase;
11. irrelevant-decoy insertion;
12. a second information-gain paraphrase.

Scenario construction and evaluator metadata remain separate research artifacts. Their purpose is to preserve what was frozen before the worked evaluation, not to create a blind test.

Synthetic scenarios do not count as evidence that the same case shapes are common in normal engineering work.

## 6. Transformation pairs are consistency checks, not blind invariance tests

A/B swaps, paraphrases, and decoy variants remain useful, but their interpretation is weakened.

### A/B swap

Ask whether the written reasoning can be translated consistently when candidate labels exchange. A contradiction is evidence against coherence.

Do **not** claim that success proves absence of label or position bias, because the evaluator-aware context knows the relationship.

### Paraphrase

Ask whether semantically equivalent formulations receive mutually compatible explanations.

Do **not** claim that success proves framing robustness or blind paraphrase invariance.

### Irrelevant decoy

Ask whether the reasoning correctly identifies a supplied non-gating uncertainty as non-gating.

Do **not** claim that success proves resistance to salience under blind conditions.

### Information-gain trap

Ask whether the worked reasoning can distinguish decision effect from generic information quantity without inventing a score.

### `act_now` control

Ask whether the procedure can explicitly stop investigating when a reversible warranted action does not depend on resolving the remaining uncertainties.

### Ambiguity control

Ask whether the explanation can preserve an evidence-supported tradeoff without forcing a winner.

## 7. Single-context execution protocol

The same coding-agent context may evaluate all frozen scenarios sequentially.

Independence, context isolation, blindness to evaluator relationships, and absence of previous answers are **not requirements** and must not be implied in the synthesis.

For each scenario, produce exactly one top-level action label:

```text
A first
B first
act now / investigate neither
```

The top-level label is a compact execution record, not a claim that a unique objectively correct answer exists.

Each worked evaluation must also provide:

- the contemplated consequential decision;
- why each candidate uncertainty is live in the supplied scenario;
- credible alternatives for A and B;
- qualitative reasoning across the relevant prompts;
- prospective selection rationale;
- a plausible competing selection and why a competent agent might choose it;
- first evidence-producing responsibility it would take;
- expected decision effect of resolving the selected uncertainty, when applicable;
- whether ambiguity remains;
- whether the worked answer is influenced by an explicitly known transformation/control relationship;
- an explicit statement that no numeric score, weight, or pseudo-point system was used.

Do not rewrite a scenario during evaluation. If a scenario is discovered to be malformed or insufficient, record that as a study limitation.

## 8. Synthetic observation record

Use a compact research record such as:

```yaml
scenario_id: "SCLU-XXX"
synthetic: true
execution_mode: "evaluator_aware_single_context"

contemplated_target: "<consequential decision>"
agent_selection: "A first|B first|act now / investigate neither"
agent_rationale: "<prospective qualitative rationale>"
plausible_competing_selection: "<alternative and rationale>"
first_evidence_responsibility: "<inspect|probe|ask_owner|other|none>"
ambiguity_acknowledged: "yes|no|not_applicable"
known_transformation_or_control: "<yes/no + description if known>"
numeric_scoring_used: false

evaluation:
  internally_coherent: "yes|no|unclear"
  compatible_with_related_variant: "yes|no|not_applicable|unclear"
  decision_value_disciplined: "yes|no|unclear"
  investigation_compulsion_observed: "yes|no|unclear"
  false_precision_observed: "yes|no|unclear"
  contradiction_observed: "yes|no|unclear"
  framework_failure_signal: "<none or failure>"
```

This is a **research observation format only**. It is not a schema, runtime contract, validation profile, or proposed persisted product artifact.

## 9. Evaluation principles

The study evaluates the coherence of the worked reasoning, not blind model behavior.

Important signals include:

- **selection coherence** — the explanation follows from stated warrant dependencies and does not contradict itself;
- **cross-variant compatibility** — related worked examples can be reconciled without claiming blind invariance;
- **decision-value discipline** — generic information gain does not substitute for decision effect;
- **option discipline** — reversibility and option preservation matter without becoming scores;
- **authority discipline** — authority-changing uncertainty is treated as consequential when relevant;
- **stopping discipline** — `act_now` remains available;
- **ambiguity honesty** — genuine ties or underspecification remain visible;
- **non-numeric reasoning** — qualitative prompts do not collapse into pseudo-math;
- **evaluator-awareness disclosure** — the analysis does not pretend that known test relationships were hidden.

Agreement with a hidden preferred answer is not the criterion. The evaluator may use frozen relationship metadata to inspect contradictions and intended control properties, but successful alignment with that metadata cannot be presented as an independent behavioral result.

## 10. Limitation / incoherence criteria

Treat the bounded claim as limited or incoherent if repeated worked scenarios show one or more of:

### F1 — arbitrary or unreconcilable selection

Equivalent or closely related scenarios receive incompatible selections without a stable qualitative explanation.

### F2 — circular rationalization

The explanation merely restates the selected label and does not discriminate prospectively among alternatives.

### F3 — information-gain substitution

The procedure repeatedly prefers broader information gathering even when the supplied facts make another uncertainty more directly decision-changing.

### F4 — excessive metareasoning

The qualitative ordering discussion is more complex than simply gathering both cheap evidence items in scenarios designed to expose that possibility.

### F5 — hidden numeric ranking

Numbers, weights, pseudo-points, or composite score language are used to aggregate the qualitative prompts.

### F6 — cross-variant contradiction

A/B swaps, paraphrases, or decoy variants cannot be reconciled even with evaluator-awareness disclosed.

### F7 — investigation compulsion

The procedure cannot choose `act now / investigate neither` where the supplied scenario makes further investigation non-gating before a reversible action.

### F8 — false precision

A deliberately balanced scenario is forced into a decisive winner without acknowledging the supported tradeoff.

### F9 — evaluator leakage makes the result tautological

The exercise becomes little more than reproducing the evaluator notes rather than demonstrating usable reasoning from the scenario facts. If this dominates the suite, the study should be classified `SYNTHETICALLY_LIMITED` or `SYNTHETICALLY_INCOHERENT`, not upgraded by apparent agreement.

## 11. Bounded dispositions

The synthesis must conclude exactly one of:

```text
SYNTHETICALLY_COHERENT
SYNTHETICALLY_LIMITED
SYNTHETICALLY_INCOHERENT
```

### `SYNTHETICALLY_COHERENT`

Use only when the frozen worked examples show that the qualitative procedure can be applied without material self-contradiction, preserves `act_now` and ambiguity where warranted, distinguishes decision effect from generic information gain, and does not require numeric scoring.

This disposition means **the procedure remained internally coherent in this evaluator-aware single-context exercise**. It does not establish independent robustness, reproducibility, or real-world effectiveness.

### `SYNTHETICALLY_LIMITED`

Use when the procedure remains intelligible but meaningful contradictions, underspecification, evaluator dependence, metareasoning cost, or ambiguous application materially limits the claim.

### `SYNTHETICALLY_INCOHERENT`

Use when the worked procedure repeatedly contradicts itself, cannot preserve obvious controls, requires arbitrary or numeric ranking, or cannot distinguish decision-changing uncertainty from distraction even with the rubric visible.

## 12. Role of future evidence

Independent coding-agent passes are no longer required for this bounded cycle. If an isolated execution surface later becomes available, it may provide a stronger follow-up study but must be treated as new evidence rather than retroactively upgrading this result.

Normal-use cases remain future corroboration. If ordinary engineering work later produces genuine competing-live cases, preserve them prospectively. They may strengthen, weaken, or falsify transfer from this synthetic coherence exercise to real work.

Do not reinterpret this evaluator-aware synthetic exercise as normal-use or independent evidence.

## 13. Synthesis artifact

After the worked scenario suite, produce a separate synthesis note containing:

1. research question and twice-weakened claim;
2. scenario construction and freeze method;
3. explicit disclosure that the evaluator relationships were visible to the execution context;
4. worked selections and rationales;
5. cross-variant compatibility findings, explicitly **not** described as blind invariance results;
6. decision-value and information-gain findings;
7. `act_now` and ambiguity-control findings;
8. contradictions, limitations, and evaluator-dependence signals;
9. bounded disposition;
10. remaining uncertainty;
11. the mandatory limitation statement from Section 3;
12. whether the result is coherent enough to move primary research attention to Path 3 or whether Path 01b needs revision.

Synthetic coherence alone does not warrant product machinery.

## 14. Machinery-promotion boundary

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
- EXP-0006 merely to demonstrate experiment infrastructure.

Any later promotion must independently satisfy the repository's existing machinery-promotion rule:

```text
repeated useful responsibility
+ stable enough semantics
+ repeated manual burden/error
+ mechanically expressible boundary
        -> candidate for formalization
```

Interesting theory or synthetic coherence alone is not sufficient.

## 15. Definition of done for the evaluator-aware Path 01b cycle

The bounded research cycle is complete when:

- this twice-weakened claim and protocol are durable and reviewable;
- the frozen 12-scenario suite remains unchanged except through explicit pre-evaluation amendment;
- all frozen scenarios receive evaluator-aware single-context worked evaluations;
- the worked records preserve `act_now`, ambiguity, decision-value discipline, and non-numeric reasoning as observable controls;
- cross-variant compatibility is evaluated without claiming blind invariance or framing robustness;
- evaluator dependence and any contradiction are recorded rather than hidden;
- a synthesis note concludes `SYNTHETICALLY_COHERENT`, `SYNTHETICALLY_LIMITED`, or `SYNTHETICALLY_INCOHERENT`;
- the synthesis includes the mandatory limitation statement;
- no machinery is promoted merely because the synthetic exercise is coherent.

## 16. Handoff to Research Path 3

If the study becomes `SYNTHETICALLY_COHERENT`, that is enough only to justify **moving research attention** to the decision/orchestration boundary under another appropriately bounded claim:

> **Does orchestration faithfully coordinate a responsibility selected through qualitative evidence reasoning, or does available workflow machinery begin selecting the work indirectly?**

A coherent single-context synthetic result is not empirical validation of Path 01b. It is only evidence that the idea is not obviously internally broken under the frozen worked examples.