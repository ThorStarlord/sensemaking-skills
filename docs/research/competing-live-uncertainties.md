# Research: Selecting Among Competing Live Uncertainties

**Status:** amended research protocol / bounded synthetic stress study  
**Authority:** not an ADR, not a product contract, not a Workflow-v0 change  
**Tracker:** Issue #204  
**Original baseline:** `main@65c2be1b430e7bc8d1400ca99d80c6ff6256a051`  
**Synthetic-amendment baseline:** `main@cf959f0f5a262d78366f4dedb50cfb99f555e071`  
**Parent research:** `docs/research/uncertainty-selection.md`  
**Related control study:** `docs/research/warrant-as-control-primitive.md`

## 1. Amendment summary

The original Path 01b protocol required 5–8 qualifying normal-use engineering episodes before synthesis. This amendment deliberately weakens that completion claim.

The immediate study may now use **deliberately constructed synthetic stress scenarios executed by a coding agent** to test whether the qualitative selection procedure is coherent, prospectively usable, invariant to irrelevant presentation changes, capable of admitting ambiguity, and resistant to obvious failure modes.

Synthetic evidence may close this dedicated research cycle under a bounded synthetic disposition. It may **not** establish that:

- competing-live uncertainty cases are common in ordinary engineering work;
- the policy improves outcomes in real repositories;
- humans and coding agents would agree on the same choice;
- a selected uncertainty is objectively optimal;
- the policy is production-ready;
- any numeric scoring, ranking, schema, Skill, workflow, or runtime mechanism is warranted.

Real-world prevalence and effectiveness remain explicitly untested unless later normal-use evidence is collected.

## 2. Research question

> **Under deliberately constructed cases where multiple uncertainties are simultaneously plausible and decision-changing, can a coding agent prospectively choose what to resolve first using qualitative pairwise reasoning without collapsing into brittle numeric ranking or unstable framing effects?**

This study extends Research Path 1. It does not replace the current operating rule:

> **Resolve the nearest currently-live unresolved decision-changing dependency before committing to the consequential action.**

The PR #164 falsification established that an unresolved historical question is not necessarily a currently-live decision dependency. Path 01b targets the harder case where two or more uncertainties are all relevant to the same consequential decision.

Research Path 2 supplies a control frame rather than new machinery:

> **What do current evidence and required authority warrant for this specific target now?**

## 3. Claim boundary

The strongest claim this study is allowed to support is:

> **Under bounded synthetic competing-live-uncertainty scenarios, a coding agent can prospectively use qualitative pairwise reasoning to make explainable selections, survive defined invariance tests, expose genuine ambiguity and failure modes, and avoid collapsing the decision into a numeric ranking scheme.**

A successful synthetic study is evidence of **conceptual coherence and stress resistance**, not ecological validity.

The final synthesis must include this sentence or an equivalent explicit limitation:

> **Real-world prevalence and effectiveness were not tested.**

## 4. Working hypotheses

### H1 — dependency proximity usually dominates when a real dependency order exists

If a credible contrary answer to uncertainty A would invalidate the entire responsibility in which uncertainty B matters, A should normally be resolved first.

A scenario fully explained by this rule is a useful control case but is not a strong parallel-uncertainty stress case.

### H2 — genuinely parallel cases require qualitative comparison

When neither uncertainty clearly invalidates the other's decision surface, compare them using:

- **dependency proximity** — how early the uncertainty sits in the warrant for the contemplated decision;
- **decision branching** — which consequential decisions could change if the answer differs;
- **alternative plausibility** — whether contrary answers have credible support in the supplied evidence;
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

### H4 — decision value should beat raw information gain

A broad uncertainty that would yield much more information should still lose to a narrower uncertainty when the narrower answer has materially greater effect on the consequential decision.

### H5 — the procedure must permit `act_now`

The coding agent must be able to conclude that neither uncertainty warrants further investigation before action. A framework that always selects something to investigate is over-controlling the workflow.

### H6 — genuine ambiguity should remain visible

When two choices are defensible from the same evidence, the coding agent should identify the unresolved tradeoff rather than manufacture false precision.

## 5. Synthetic scenario requirements

Prefer **8–12 frozen scenarios**. The number is a bounded stress target, not a quota that justifies redundant cases.

Every scenario must be written and frozen before the evaluated coding-agent pass sees it.

Each scenario must provide:

1. a goal;
2. an authorized scope and authority boundary;
3. one contemplated consequential decision;
4. at least two candidate live uncertainties;
5. credible alternative answers for each uncertainty;
6. enough evidence to reason prospectively, while withholding the scenario's intended evaluation outcome;
7. a plausible reason why a competent agent might select either A, B, or `act_now`.

Synthetic scenarios are deliberately constructed and therefore do **not** count as evidence that the same case shape occurs frequently in ordinary engineering work.

## 6. Required scenario families

The suite should include conflicts where different qualitative dimensions pull in different directions.

At minimum include:

1. **evidence economy vs wrong-action exposure** — A is cheap to resolve; B is more consequential if assumed incorrectly;
2. **dependency proximity vs authority effect** — A is earlier in the warrant chain; B could change who is authorized to act;
3. **option preservation vs decision branching** — A preserves options; B may redirect more downstream work;
4. **balanced ambiguity** — neither A nor B clearly dominates;
5. **resolve-both control** — the metareasoning cost of ordering A/B approaches or exceeds resolving both;
6. **act-now control** — neither uncertainty has enough expected decision effect to justify more investigation;
7. **information-gain trap** — A yields more information but B has greater decision effect;
8. **irreversibility control** — a relatively cheap uncertainty sits before an expensive or externally visible action.

Additional scenarios may cover technical vs authority, scope vs correctness, reconciliation vs repair, finding-specific verification vs more implementation, repository inspection vs empirical probe, or closure vs further validation.

## 7. Controlled transformations and invariance tests

The strongest synthetic evidence should come from paired variants rather than isolated answers.

### T1 — A/B label swap

Create an otherwise identical variant in which A and B labels are exchanged.

Expected property:

- the substantive choice should exchange labels while the reasoning relation remains equivalent.

A failure suggests label/position bias.

### T2 — paraphrase

Rewrite the same scenario without changing decision-relevant facts.

Expected property:

- the selected responsibility and core rationale should remain materially stable;
- wording may differ.

Large unexplained changes indicate framing sensitivity.

### T3 — irrelevant decoy

Add an interesting unresolved question that is not a live dependency of the contemplated consequential decision.

Expected property:

- the decoy should not attract selection merely because it is salient or information-rich.

### T4 — information-gain trap

Make one uncertainty broad and informative while another is narrower but more decision-changing.

Expected property:

- decision effect should dominate information quantity when the evidence supports that distinction.

### T5 — act-now control

Construct a case where both uncertainties are real but neither needs resolution before a cheap, reversible, warranted action.

Expected property:

- the agent should be able to choose `act_now / investigate neither`.

### T6 — ambiguity preservation

Construct a balanced case with defensible arguments for both A and B.

Expected property:

- the agent should identify the genuine tradeoff and explain why the evidence does not warrant fake certainty.

## 8. Coding-agent execution protocol

Run each frozen scenario in an independent pass with no prior answer from another pass supplied as context.

Each pass must return exactly one top-level selection:

```text
A first
B first
act now / investigate neither
```

and must also provide:

- the contemplated consequential decision;
- why each candidate uncertainty is live in the supplied scenario;
- credible alternatives for A and B;
- pairwise reasoning across the qualitative dimensions;
- prospective selection rationale;
- plausible competing selection and why a competent agent might choose it;
- first evidence-producing responsibility it would take;
- expected decision effect of resolving the selected uncertainty;
- whether ambiguity remains;
- explicit statement that no numeric score, weight, or pseudo-point system was used.

Do not reveal the intended stress property, transformation relationship, or evaluator expectation to the coding agent before its answer.

## 9. Synthetic observation record

Assign scenario-family IDs such as `SCLU-001`, with variant IDs such as `SCLU-001-base`, `SCLU-001-swap`, and `SCLU-001-paraphrase`.

Use this research record:

```yaml
scenario_id: "SCLU-XXX-variant"
scenario_family: "SCLU-XXX"
scenario_kind: "base|swap|paraphrase|decoy|information_trap|act_now|ambiguity|other"
synthetic: true

contemplated_target: "<consequential decision>"
authorized_scope: "<scope and authority boundary>"

live_uncertainties:
  - id: "A"
    question: "<question>"
    credible_alternatives:
      - "<answer 1>"
      - "<answer 2>"
  - id: "B"
    question: "<question>"
    credible_alternatives:
      - "<answer 1>"
      - "<answer 2>"

agent_selection: "A first|B first|act now / investigate neither"
agent_rationale: "<prospective rationale>"
plausible_competing_selection: "<alternative and rationale>"
first_evidence_responsibility: "<inspect|probe|ask_owner|other>"
ambiguity_acknowledged: "yes|no|not_applicable"
numeric_scoring_used: false

evaluation:
  expected_stress_property: "<property tested>"
  property_satisfied: "yes|no|unclear"
  invariant_with_pair: "yes|no|not_applicable|unclear"
  framing_sensitivity_observed: "yes|no|unclear"
  information_gain_substitution_observed: "yes|no|unclear"
  false_precision_observed: "yes|no|unclear"
  framework_failure_signal: "<none or failure>"
```

This YAML is a **research observation format only**. It is not a repository schema, runtime contract, validation profile, or proposed persisted product artifact.

## 10. Evaluation principles

Do not judge success by agreement with a hidden preferred answer alone.

Evaluate whether the agent's reasoning satisfies the intended relation across paired scenarios.

Important signals include:

- **selection coherence** — the choice follows from the stated warrant dependencies;
- **transformation invariance** — irrelevant label/wording changes do not alter the substantive decision;
- **decision-value discipline** — decision effect is not replaced by generic information gain;
- **option discipline** — reversibility and option preservation affect reasoning without becoming a score;
- **authority discipline** — authority-changing uncertainty is treated as consequential when relevant;
- **stopping discipline** — `act_now` remains available;
- **ambiguity honesty** — genuine ties or underspecification remain visible;
- **non-numeric reasoning** — qualitative prompts do not collapse into pseudo-math.

## 11. Falsification and weakening criteria

Treat the bounded synthetic hypothesis as weakened or falsified if repeated scenarios show one or more of:

### F1 — arbitrary selection

Independent passes repeatedly choose different uncertainties in equivalent cases without a stable qualitative explanation.

### F2 — retrospective-looking rationalization

The reasoning appears to justify whichever option was selected rather than prospectively discriminating among alternatives.

### F3 — information-gain substitution

The agent repeatedly chooses the uncertainty that promises more information even when another uncertainty has clearly stronger decision effect.

### F4 — excessive metareasoning

The reasoning needed to order A/B is more complex than resolving both in scenarios designed to make that comparison visible.

### F5 — hidden numeric ranking

The agent introduces numbers, weights, pseudo-points, or consistent implicit scoring language to aggregate the qualitative dimensions.

### F6 — dependency instability

Equivalent scenario transformations produce materially different interpretations of the warrant dependency structure.

### F7 — framing sensitivity

A/B swaps or paraphrases cause unexplained substantive selection changes.

### F8 — investigation compulsion

The agent cannot select `act_now` in control scenarios where neither uncertainty needs resolution before a warranted reversible action.

### F9 — false precision

The agent reports a decisive winner in deliberately balanced scenarios without acknowledging the evidence-supported tradeoff.

## 12. Bounded dispositions

The synthesis must conclude exactly one of:

```text
SYNTHETICALLY_SUPPORTED
SYNTHETICALLY_WEAKENED
SYNTHETICALLY_FALSIFIED
```

### `SYNTHETICALLY_SUPPORTED`

Use only when the scenario suite shows that:

- the coding agent can identify the supplied live uncertainties;
- pairwise qualitative reasoning produces prospective explanations;
- label swapping preserves the substantive relation;
- paraphrase sensitivity is acceptably bounded;
- irrelevant decoys do not attract selection;
- decision value beats raw information gain in trap cases;
- `act_now` remains available;
- genuine ambiguity is acknowledged;
- the process does not require numeric scoring.

This disposition means **the qualitative procedure survived the bounded synthetic stress suite**. It does not mean the procedure is validated in ordinary engineering work.

### `SYNTHETICALLY_WEAKENED`

Use when the procedure remains partly useful but repeated stress cases expose instability, underspecification, framing dependence, or metareasoning cost that materially limits the claim.

### `SYNTHETICALLY_FALSIFIED`

Use when the core qualitative selection idea repeatedly fails its intended invariance or decision-value tests, requires covert ranking machinery, or cannot distinguish decision-changing uncertainty from information-rich distraction.

## 13. Role of future normal-use evidence

Normal-use cases are now **future corroboration**, not a completion prerequisite for this bounded research cycle.

If ordinary engineering work later produces genuine competing-live cases, preserve them using the prospective discipline from the original protocol. They can strengthen, weaken, or falsify transfer from synthetic scenarios to real work.

Do not reinterpret synthetic scenarios as normal-use observations, and do not use lack of normal-use cases to claim prevalence.

## 14. Synthesis artifact

After the bounded scenario suite, produce a separate synthesis note containing:

1. research question and weakened claim;
2. scenario construction method;
3. scenario families and controlled transformations;
4. coding-agent execution protocol;
5. selection results;
6. invariance-test results;
7. decision-value and information-trap findings;
8. `act_now` and ambiguity-control findings;
9. falsifications/refinements;
10. bounded disposition;
11. remaining uncertainty;
12. explicit statement that real-world prevalence and effectiveness were not tested;
13. whether the synthetic result is coherent enough to hand research attention to Path 3 or instead requires Path-01b revision.

Synthetic success alone does not warrant product machinery.

## 15. Machinery-promotion boundary

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

Interesting theory or synthetic success alone is not sufficient.

## 16. Definition of done for the weakened Path 01b cycle

The bounded synthetic research cycle is complete when:

- this amended claim and protocol are durable and reviewable;
- 8–12 frozen synthetic scenario families/variants provide meaningful coverage without padding;
- controlled A/B swap, paraphrase, decoy, information-gain, `act_now`, and ambiguity tests are represented;
- coding-agent passes are independent and do not receive previous answers;
- scenario evaluations record invariance/failure signals rather than only preferred-answer agreement;
- a synthesis note concludes `SYNTHETICALLY_SUPPORTED`, `SYNTHETICALLY_WEAKENED`, or `SYNTHETICALLY_FALSIFIED`;
- the synthesis explicitly states that real-world prevalence and effectiveness were not tested;
- no machinery is promoted merely because the synthetic study succeeds.

## 17. Handoff to Research Path 3

If the study becomes `SYNTHETICALLY_SUPPORTED`, the next research priority may move to the decision/orchestration boundary under an equivalently bounded claim:

> **Does orchestration faithfully coordinate a responsibility selected through qualitative evidence reasoning, or does available workflow machinery begin selecting the work indirectly?**

Synthetic support is sufficient to justify asking that next research question. It is not sufficient to claim that Path 01b is empirically validated in ordinary engineering work.
