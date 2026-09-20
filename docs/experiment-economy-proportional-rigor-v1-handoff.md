# Experiment Economy & Proportional Rigor v1 — Handoff

**Issue:** #438  
**Feature PR:** #439  
**Disposition:** COMPLETE / INTEGRATED / NORMAL_USE_HANDOFF  
**Qualified feature head:** `1c134966901b9be7726b4e07bd23e411baa1d55f`  
**Feature merge:** `9237320910cd696344482a51fafbe140c3cfcb8f`

## Objective

Correct two observed normal-use failure modes without making Sensemaking anti-experiment:

1. experiment-selection bias — uncertainty / `INVESTIGATE` could make experimentation too salient;
2. experimental-rigor inflation — once selected, experiments could accumulate isolation, fresh-agent, contamination-control, evaluator, and evidence-packaging overhead beyond what the decision/claim warranted.

The refinement also addresses evidence-grade escalation, where reversible product
questions could be treated as if they required research-grade causal evidence.

The governing control law is:

```text
decision-changing uncertainty
-> is more evidence actually required?
-> lowest-cost sufficient evidence source
-> could cheap reversible construction answer it?
-> if experiment still warranted:
     minimum sufficient experimental rigor
-> control only decision-relevant confounders
-> stop when evidence is sufficient
```

## Integrated changes

### Experiment Warrant Gate

Experimentation is now a narrower decision inside inquiry.

```text
uncertainty
!= experiment

INVESTIGATE
!= EXPERIMENT

experiment possible
!= experiment warranted

better evidence possible
!= better evidence worth obtaining
```

An experiment should be selected only when its plausible outcomes can materially
change what becomes warranted and cheaper evidence sources are insufficient.

### Evidence-source economy

The guidance now explicitly considers:

```text
existing evidence
-> READ
-> INSPECT
-> VERIFY
-> PROBE
-> REVERSIBLE BUILD / NORMAL USE
-> SPIKE
-> SMALL EXPERIMENT
-> CONTROLLED EXPERIMENT
-> RESEARCH-GRADE ISOLATION
```

This is not a mandatory sequence. The agent starts with the cheapest source capable of
supporting the current decision/claim.

### Reversible construction as evidence

When construction is cheap, reversible, authorized, sufficiently safe, and
information-producing, it may dominate a separate experiment.

```text
cheap reversible construction
can be the cheapest sufficient inquiry

build-as-inquiry
!= irreversible architecture commitment
```

### Total experiment cost

Experiment cost now explicitly includes design, setup, implementation, isolation,
execution, evaluator effort, interpretation, documentation/evidence packaging, delay,
and opportunity cost.

A small amount of experiment code does not by itself make the experiment cheap.

### Minimum Sufficient Experimental Rigor

When an experiment remains warranted, rigor scales qualitatively with consequence,
reversibility, implementation cost, experiment cost, causal-attribution importance,
claim durability/publicity, and the likelihood that an uncontrolled factor could
reverse the inference.

```text
maximum rigor
!= correct rigor

minimum sufficient rigor
= enough control for the current decision and claim
```

### Confounder Warrant

Possible contamination does not automatically justify control overhead.

```text
possible confounder
!= required control

control cost
requires decision-relevant warrant
```

Coding-agent competence, normal repository context, and normal tool use are not
contamination by default when they are part of the intended operating environment.

### Evidence modes

The guidance distinguishes:

- normal-use product evidence;
- bounded diagnostic evidence;
- causal / research-grade evidence.

A usefulness/retain-revise-remove decision does not inherit the evidentiary burden of
a causal superiority claim.

## Integration surfaces

The refinement is integrated through:

- `skills/using-sensemaking/SKILL.md`;
- `skills/using-sensemaking/references/inquiry-policy-v0.md`;
- `skills/using-sensemaking/references/metareasoning-policy-v0.md`;
- `skills/using-sensemaking/references/experiment-economy-v1.md`;
- `skills/strategic-repository-analysis/SKILL.md`;
- `docs/policy-hierarchy-v0.md`;
- `docs/strategic-repository-sensemaking-v1.md`;
- `tests/test_experiment_economy_v1.py`.

No new durable experiment artifact or schema was introduced.

## Qualification

Exact qualified feature head:

`1c134966901b9be7726b4e07bd23e411baa1d55f`

- Product Validation run `35539356624`: PASS
- Release Candidate Distribution run `35539356616`: PASS

Feature merge:

`9237320910cd696344482a51fafbe140c3cfcb8f`

GitHub compare from the qualified feature head to the merge commit reports one merge
commit and **zero file differences**. The integrated feature bytes are therefore
content-identical to the qualified candidate bytes.

Earlier candidate attempts exposed test-contract encoding defects in the newly added
conformance assertions; those assertions were repaired before the final qualified head.
No experiment program or semantic-policy expansion was added in response.

## Product boundaries preserved

No package introduced:

- ExperimentEngine or experiment router;
- numeric expected-value / evidence-grade / rigor scoring;
- automatic experiment selection;
- automatic evidence-grade selection;
- experiment database or new Campaign schema;
- mandatory fresh-agent isolation;
- mandatory isolated worktree;
- mandatory control group;
- mandatory blind evaluator;
- automatic contamination handling;
- synthetic experiment program;
- planner/runtime authority;
- protected merge/release/deploy/publication authority.

## Claim ceiling

Repository qualification establishes that the guidance, contracts, references,
conformance tests, and integration boundaries are coherent for the exact qualified
bytes.

It does **not** establish:

- that Sensemaking previously had a scientifically demonstrated systematic experiment bias;
- that the refinement eliminates every future over-investigation episode;
- that one evidence mode is empirically superior across repositories;
- that the agent will always choose optimal experiment rigor;
- causal product-value improvement.

The motivating observations remain **preliminary normal-use evidence** that warranted a
small reversible guidance correction.

## Terminal state

```text
ISSUE_438_EXPERIMENT_ECONOMY_PROPORTIONAL_RIGOR_V1
= COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF

CURRENT CONSTRUCTION RESPONSIBILITY = NONE
PRIMARY CONSTRUCTION PROGRAM = NONE
OPERATING MODE = NORMAL_USE_VALIDATION
EXPERIMENT_PREREQUISITE = NONE
```

Do not open a validation experiment merely to prove this refinement. Use the guidance
during ordinary consequential work and preserve concrete future friction if it recurs.
