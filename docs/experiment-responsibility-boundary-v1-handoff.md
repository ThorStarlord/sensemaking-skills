# Experiment Responsibility Boundary v1 — Handoff

**Issue:** #441  
**Feature PR:** #442  
**Disposition:** COMPLETE / INTEGRATED / NORMAL_USE_HANDOFF  
**Qualified feature head:** `005aa2d41e7dd89d1af186473c8cc3e18845385f`  
**Feature merge:** `7d15024226022bdd47a82da99241c7989a8e3f4d`

## Objective

Close the composition gap left after Experiment Economy & Proportional Rigor v1:

```text
diagnostic Skill finds empirical uncertainty
-> diagnostic Skill recommends experiment
-> experiment-design designs it
```

could still bypass the intended control path:

```text
Inquiry Policy
-> Experiment Economy
-> experiment warrant
-> experiment-design
```

The package makes experiment responsibility explicit without adding an experiment
router, runtime, score, or new Campaign state.

## Integrated responsibility boundary

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
-> establish experiment warrant only when experimentation dominates alternatives

experiment-design
-> consume experiment warrant
-> design the smallest sufficiently rigorous, decision-discriminating experiment
-> account for total experiment cost and necessary controls
-> preserve claim ceiling
-> return experiment_plan

execution
-> separately authorized

experiment-result analysis
-> interpret supplied observations
-> continuation recommendation only
-> another experiment requires fresh warrant
```

## Corpus reconciliation

The static Skill-corpus audit classified empirical/experiment-facing surfaces as:

- evidence consumption only;
- empirical-uncertainty identification;
- evidence-producing recommendation;
- experiment/research design or execution;
- returned-evidence analysis.

Targeted current-Skill changes were made only where a direct promotion path existed or
where a specialized Skill could otherwise self-select its own research responsibility.

### Changed diagnostic/domain Skills

- `repo-sensemaker` — empirical uncertainty now yields an evidence need / candidate
  source and must pass Experiment Economy before a probe/experiment recommendation;
  the repository-brief template was reconciled too.
- `discovery` — learning methods are evidence-source-neutral; experiments require
  separate warrant.
- `hypothesis` — validation approach no longer implies experiment warrant.
- `lean-canvas` — critical assumptions no longer imply experimentation.
- `pricing` — highest-risk assumptions no longer automatically generate experiment
  proposals; the `experiments` surface stays empty without warrant.

### Specialized downstream roles

- `experiment-design` — may not manufacture its own warrant; it now consumes an
  already-warranted experimentation responsibility and owns experiment quality +
  experiment efficiency.
- `ab-test-analysis` — `extend` / `investigate` are analysis recommendations,
  not fresh experiment warrant.
- `usage-researcher` — can execute/observe already-selected usage research but does
  not decide that new usage research or fresh-context isolation is warranted.

Verification-only probes in `repair-verifier` / `output-reconciler` remain
verification responsibilities rather than product experimentation.

## Experiment design efficiency

After experiment warrant exists, experiment-design now optimizes:

> decision-relevant information per total experiment cost, subject to sufficient
> evidentiary rigor.

It distinguishes:

```text
experimental quality
!= experimental efficiency
```

and requires attention to:

- decision discrimination;
- total design/setup/implementation/isolation/execution/evaluation/interpretation/
  documentation/delay/opportunity cost;
- Minimum Sufficient Experimental Rigor;
- decision-relevant confounder controls only;
- kill/early-stop criteria;
- claim ceiling.

If material result classes would all produce the same decision effect, the experiment
warrant should be reassessed rather than silently designed.

## experiment_plan v2

Historical `experiment_plan schema_version: "1"` remains valid.

Canonical new `schema_version: "2"` plans add:

- `decision_to_support`;
- `decision_changing_uncertainty`;
- `experiment_warrant`;
- `decision_branches`;
- `total_experiment_cost`;
- `minimum_required_controls`;
- `controls_rejected_as_unnecessary`;
- `claim_ceiling`.

The deterministic PM validator now accepts v1/v2 experiment plans. For v2 it checks
representation such as explicit warrant context, cheaper-evidence review, at least two
decision branches, direct duplicate decision effects, cost-component coverage, controls
list shape, and claim ceiling.

```text
validator PASS
!= experiment warrant semantically proven
!= experimental method optimal
!= execution authorized
```

## Qualification coverage repair

Before this package, `tests/campaign_validation/test_pm_measurement.py` was not
explicitly exercised by the Product Validation campaign glob or the Release Candidate
baseline list.

The package adds that existing suite explicitly to both Product Validation and Release
Candidate Distribution, so experiment-plan v1/v2 compatibility and v2 warrant/
efficiency representation are release-qualified.

## Exact feature qualification

Exact qualified feature head:

`005aa2d41e7dd89d1af186473c8cc3e18845385f`

- Product Validation run `35548589418`: PASS
- Release Candidate Distribution run `35548589414`: PASS
- Lab Validation run `35548589416`: PASS

Feature merge:

`7d15024226022bdd47a82da99241c7989a8e3f4d`

GitHub compare from the exact qualified feature head to the merge commit reports one
merge commit and **zero file differences**.

## Product boundaries preserved

No package introduced:

- ExperimentEngine or experiment router;
- numeric cost-benefit ratio;
- numeric Value-of-Information score;
- automatic evidence-source ranking;
- automatic experiment-warrant selection;
- experiment database;
- new Campaign schema;
- mandatory experiment recommendation from every Skill;
- mandatory controlled experiment;
- automatic experiment continuation from result analysis;
- external experiment execution authority.

## Claim ceiling

Repository qualification establishes that the responsibility boundary, Skill guidance,
experiment-plan compatibility, deterministic representation checks, and repository
integration are coherent for the exact qualified bytes.

It does **not** establish:

- that every diagnostic agent will always identify the cheapest evidence source;
- that every warranted experiment will be optimal;
- that v2 mechanical checks prove semantic experiment warrant;
- that decision branches are genuinely exhaustive;
- that stated total-cost descriptions are quantitatively accurate;
- that the repository has empirically eliminated all future experiment-selection or
  experiment-efficiency failures.

The package is a bounded contract correction derived from observed normal-use friction
and corpus reconciliation, not a validation experiment.

## Terminal state

```text
ISSUE_441_EXPERIMENT_RESPONSIBILITY_BOUNDARY_V1
= COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF

CURRENT CONSTRUCTION RESPONSIBILITY = NONE
PRIMARY CONSTRUCTION PROGRAM = NONE
OPERATING MODE = NORMAL_USE_VALIDATION
EXPERIMENT PREREQUISITE = NONE
```

Use the boundary during ordinary work. Reopen only from concrete recurring friction or
new owner direction; do not run an experiment merely to prove this package.
