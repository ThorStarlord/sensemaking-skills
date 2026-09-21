# Experiment Responsibility Boundary v1

**Status:** current cross-Skill composition contract  
**Issue:** #441  
**Authority:** subordinate to Inquiry Policy v0, Metareasoning Policy v0, and Experiment Economy & Proportional Rigor v1  
**Runtime posture:** guidance + artifact-contract boundaries; no experiment router or automatic responsibility selector

## 1. Problem

Experiment Economy & Proportional Rigor v1 establishes when experimentation is
warranted and how much rigor is sufficient. Individual Skills can still bypass that
control layer if they translate an empirical uncertainty directly into an experiment
or if `experiment-design` silently manufactures the warrant it consumes.

The responsibility boundary is:

```text
diagnostic / domain Skill
-> identify observation
-> identify uncertainty
-> name decision affected
-> name missing evidence
-> do not manufacture experimentation responsibility

Inquiry Policy / Experiment Economy
-> decide whether more evidence is needed
-> choose the lowest-cost sufficient evidence source
-> establish experiment warrant only when experiment dominates alternatives

experiment-design
-> consume established experiment warrant
-> design the smallest sufficiently rigorous, decision-discriminating experiment
-> return experiment_plan

execution
-> separately authorized

ab-test-analysis / evidence-return analysis
-> interpret supplied observations
-> recommendation only
-> continuation / another experiment requires fresh warrant

Learning / Reconciliation
-> interpret what the returned evidence changes
```

## 2. Universal vs conditional responsibilities

Every Skill has **epistemic responsibility**:

- distinguish evidence, inference, assumption, and unknown;
- preserve claim ceilings;
- do not claim that unobserved evidence exists.

Only decision-support Skills need **inquiry responsibility**:

- identify whether an unknown is decision-changing;
- avoid treating missing evidence as an automatic command to gather more evidence.

Only an already-warranted experimentation responsibility activates
**experimental responsibility**:

- design an efficient experiment;
- choose sufficient—not maximal—rigor;
- capture decision discrimination and claim ceiling.

```text
epistemic responsibility
!= inquiry responsibility
!= experimental responsibility
```

## 3. Corpus audit

Current Skill surfaces were inspected for `experiment`, `validation approach`,
`bounded probe`, `test/observation`, `validation evidence`, and research language.

Classification:

| Skill / surface | Class | Current role | Disposition |
| --- | --- | --- | --- |
| `strategic-repository-analysis` | B/C | identifies decision-changing uncertainty and can nominate empirical inquiry | already compliant through Experiment Economy; preserve |
| `repo-sensemaker` | B/C | diagnostic Skill whose conversational empirical branch directly says to formulate a bounded probe | change: emit evidence need / probe candidate only after Experiment Economy; no direct promotion |
| `discovery` | B/C | identifies missing evidence and bounded tests/observations | change: prefer evidence source; experiment only with established warrant |
| `hypothesis` | B/C | defines a validation approach for a proposed hypothesis | change: validation approach is evidence-source-neutral; experiment requires separate warrant |
| `lean-canvas` | B/C | proposes validation approaches for critical assumptions | change: do not default validation to experiments; preserve conditional evidence-source choice |
| `pricing` | C | explicitly says to define experiments for highest-risk pricing assumptions | change: identify evidence needs/options first; populate experiment proposals only when warrant exists |
| `experiment-design` | D | designs experiment plans | change: may not create its own warrant; consume warrant and optimize experiment efficiency |
| `ab-test-analysis` | E | analyzes supplied controlled-experiment evidence | keep analysis role; clarify that `extend` / `investigate` does not itself authorize another experiment |
| `usage-researcher` | D/E specialized | executes/observes already-selected Skill usage research | clarify activation boundary; it does not decide that usage research is warranted |
| `repair-verifier` / `output-reconciler` | verification | bounded probes verify already-made repair/completion claims | no change: verification responsibility is not product experimentation |
| Skills that merely cite prior experiment/research evidence | A | evidence consumption | no change |

Classes:

- **A** — consume or cite existing experiment/research evidence;
- **B** — identify empirical uncertainty;
- **C** — recommend an evidence-producing action that could become an experiment;
- **D** — design/run already-selected experimentation/research;
- **E** — analyze returned experiment evidence.

The audit is static contract reconciliation. It is not an experiment and does not
claim that every possible natural-language synonym was mechanically enumerated.

## 4. Diagnostic-Skill invariant

A diagnostic/domain Skill may identify:

```text
OBSERVATION
UNCERTAINTY
DECISION AFFECTED
EVIDENCE ALREADY AVAILABLE
MISSING EVIDENCE
CANDIDATE EVIDENCE SOURCE
```

It must not infer:

```text
empirical uncertainty
-> experimentation responsibility
```

without Experiment Economy.

Canonical boundary:

```text
uncertainty
!= experiment

missing evidence
!= experiment required

diagnostic recommendation
!= experimentation responsibility
```

When empirical evidence is material, prefer language such as "evidence need",
"candidate evidence source", or "bounded probe candidate" until warrant is established.

## 5. Experiment-design activation contract

`experiment-design` is downstream of experiment warrant.

Required decision context:

- decision to support;
- decision-changing uncertainty;
- explicit statement that experimentation is warranted;
- cheaper evidence sources considered;
- why those sources are insufficient;
- target population/context;
- testable hypothesis.

If the warrant context is absent or merely asserted without enough reconstructible
reasoning to distinguish experiment from cheaper alternatives:

```text
do not manufacture warrant
-> return control
-> name missing experiment-warrant context
```

The Skill can challenge an internally contradictory warrant, but it does not replace
Inquiry Policy / Experiment Economy.

## 6. Experimental quality vs experimental efficiency

These are separate questions.

### Experimental quality

> If this experiment is run, can its evidence support the intended inference?

Includes intervention/exposure, population, metric integrity, sample/duration plan,
analysis, guardrails, and necessary validity controls.

### Experimental efficiency

> Is this the smallest sufficiently rigorous experiment that discriminates the
> decision for acceptable total cost?

Includes:

- cheaper evidence alternatives already ruled insufficient;
- decision branches for material outcomes;
- total setup/isolation/evaluation/interpretation/documentation/delay/opportunity cost;
- minimum sufficient rigor;
- only decision-relevant confounder controls;
- early stop/kill conditions;
- claim ceiling.

```text
methodologically strong
!= decision-efficient

maximum rigor
!= maximum decision value
```

No numeric cost-benefit ratio is required.

## 7. Decision discrimination

Every canonical v2 experiment plan declares how material result classes would change
the supported decision.

Example:

```text
result class A -> BUILD remains warranted
result class B -> DEFER / gather different evidence
result class C -> NO_GO / reconsider hypothesis
```

If every plausible result leads to the same action, the experiment has no useful
decision discrimination and its warrant should be returned for reassessment rather
than silently designed.

## 8. experiment_plan compatibility

Historical `experiment_plan schema_version: "1"` remains valid.

Canonical new plans use `schema_version: "2"` and add:

- `decision_to_support`;
- `decision_changing_uncertainty`;
- `experiment_warrant`;
- `decision_branches`;
- `total_experiment_cost`;
- `minimum_required_controls`;
- `controls_rejected_as_unnecessary`;
- `claim_ceiling`.

Mechanical validation establishes only representation integrity:

```text
v2 experiment plan valid
!= experiment warranted in reality
!= experiment method semantically optimal
!= experiment execution authorized
```

## 9. Non-goals

Do not add:

- automatic experiment routing;
- ExperimentEngine;
- numeric Value-of-Information or cost-benefit scoring;
- automatic evidence-source ranking;
- automatic responsibility selection;
- experiment database;
- new Campaign schema;
- mandatory experiment recommendation from diagnostic Skills;
- mandatory controlled experiment when a probe or normal-use observation is sufficient.

## 10. Completion condition

The boundary is integrated when relevant direct-invocation Skills cannot legitimately
promote empirical uncertainty into experimentation without the warrant boundary,
`experiment-design` consumes rather than creates experiment warrant, canonical new
experiment plans represent efficiency/decision-discrimination context, historical v1
plans remain valid, and ordinary repository qualification passes.
