# Decision record v1 - highest-value next action after repository-sensemaking-skill-hardening-v1

```
schema: post-hardening-decision-probe-v1/decision-record-v1
experiment: post-hardening-decision-probe-v1 (prospective decision probe, Task C)
predecessor: repository-sensemaking-skill-hardening-v1 (CLOSED - REVISE, human disposition 2026-08-07)
status: DECISION RECORDED - PROBE DESIGNED - NOT EXECUTED, NOT IMPLEMENTED
date: 2026-08-07
branch: experiments/post-hardening-decision-probe-v1 (based on origin/main @ 1f9efcf, PR #149 merged)
inputs_read:
  - experiments/product-discovery-v0/** (six-block worksheet, evidence-boundary findings, learning report)
  - origin/hardening/repository-sensemaking-v1 evidence (read-only): final-disposition-v1.yaml,
    phase15-comparison-v1.yaml, phase18-regression-analysis-v1.yaml, phase19-evaluation-report-v1.yaml,
    baseline-report.yaml, candidate-freeze-v1/v2, weakness-taxonomy-inventory-v1/v2,
    interaction-probe/*, tools/* (scorer, comparator, corpus generator), corpus/ground-truth.yaml,
    baseline/ + candidate/ briefs
constraints: no canonical skill/validator/runtime/workflow/scorer/corpus changes; no candidate
  skill merge or copy; no implementation of the chosen solution; stop after the decision/probe package
```

## Owner pre-probe inclination (preserved exactly)

> Do not start another repo-sensemaker implementation yet. Preserve the current baseline and the
> supported lessons from hardening-v1, and first run a cheap probe to determine whether the
> weakest-boundary regression represents genuinely worse repository decisions or mainly disagreement
> with the frozen taxonomy/rubric. Confidence: low-to-medium. Why: hardening-v1 clearly failed its
> frozen gate, but the experiment also showed useful improvements in exploration, evidence authority,
> routing safety, and inference labeling. I do not yet know whether the right response is to simplify
> boundary reasoning, change its evaluation, salvage parts independently, or stop working on it.

---

## 1. Decision and materially different alternatives

**Decision.** Given that repository-sensemaking-skill-hardening-v1 failed its frozen improvement gate
after exhausting 3/3 repair cycles, what is the highest-value next action for repo-sensemaker?

**Answer.** Run a manual, human-adjudicated, blinded comparative probe on the contested corpus
repositories **before any further skill change**: a single independent reviewer reads each frozen
fixture plus the baseline and candidate briefs (blinded, order-randomized) and judges (a) which
weakness-type label is most defensible, and (b) which brief is more useful. The probe's purpose is to
determine whether the measured boundary-type regression (0.640 -> 0.440 under the frozen scorer) is
genuinely worse repository decision-making or mainly disagreement with the generator-authored frozen
taxonomy/rubric. No implementation follows from this package; the probe outcome maps to a
precommitted next action (see probe-design-v1.md section 6).

**Materially different alternatives considered:**

| # | Alternative | Assessment | Status |
|---|---|---|---|
| A | Stop hardening; retain the current baseline as-is | Correct fallback **if** the probe shows the regression is real. Premature now: the regression's meaning is unresolved, and five measured improvements (evidence authority, exploration protocol, routing/validation stability, fog corrections, selection structure) would be discarded on an interpretation, not a measurement. | Deferred pending probe |
| B | Salvage only individually supported ideas from hardening-v1 | Likely post-probe action **if** rubric disagreement dominates. The improvements are separable at the commit level (see evidence-map-v1.md section 7). Premature before adjudication because boundary/fog sections are entangled with salvageable sections at the margin; salvage scope depends on which labels are adjudicated correct. | Deferred pending probe |
| C | Simplify weakest-boundary reasoning rather than adding more guidance | Right response **if** adjudication shows the guidance over-complicates defensible choices (round-2 over-correction supports this for some repos). Also cheaply testable later on the frozen corpus (guidance size vs label match). | Deferred pending probe |
| D | Test a deterministic boundary decision procedure (disposition H1: checklist with binary gates) | Promising mechanism hypothesis. But building a decision procedure before knowing whether the boundary labels matter (vs. rubric disagreement) risks machinery on an unmeasured foundation. The probe precedes it. | Deferred pending probe |
| E | Redesign how weakest-boundary quality is evaluated (human adjudication / claim-level ground truth; H3, H6) | **This probe is the first step of E.** Its outcome decides whether evaluation redesign becomes a workstream. | Selected (as probe) |
| F | Runtime-path or blinded comparative evaluation before changing the skill (H5, H6) | The blinded comparative half (phase 17) was never executed because the mechanical gate failed first; this probe executes exactly that half. The runtime-path half (H5) tests the runtime, not the regression's meaning; orthogonal and deferrable. | Partially selected (comparative half) |
| G | Expand the corpus (H2, 50+ fixtures) before drawing another conclusion | Useful later for variance, but it would re-run the same un-adjudicated label-match measurement on more generator-authored fixtures. It cannot adjudicate the current 25 labels. | Deferred pending probe |
| H | Do nothing for now; focus elsewhere in Sensemaking Skills | Rejected for now: the probe costs a few hours of human time, all artifacts already exist frozen, and the gate failure leaves genuine uncertainty about the quality signal of a shipped skill. A decision, not silence, is the deliverable. | Rejected |

The probe is deliberately a **manual, comparative, human-adjudicated** probe (per the task
constraint: prefer that over another implementation workstream) and it is the cheapest credible way
to resolve the decision-changing uncertainty: every artifact it needs (25 fixtures, 25 baseline
briefs, 25 candidate briefs, ground truth) already exists and is frozen.

## 2. Observed evidence vs interpretations

Full inventory in evidence-map-v1.md. The condensed picture that drives this decision:

**Observations (frozen measurements, verifiable from the committed artifacts):**
- Frozen gate results (scorer CF4D03F5, validator F53B637D, template A013FF8B, ground truth v2):
  unsupported_claim_rate 0.632 -> 0.633 (flat); evidence_precision 0.844 -> 0.835 (flat);
  weakest_boundary_accuracy 0.640 -> 0.440 (decline); routing_validity 1.000 -> 1.000;
  validation_pass_rate 1.000 -> 1.000; observed_claim_accuracy 0.818 -> 0.812;
  inference_labeling_rate 0.022 -> 0.040 (improved).
- Fog classification: 20/25 -> 19/25 (3 corrected: docs-heavy-code-light, adv-misleading-readme,
  adv-partial-impl; 4 flipped off: web-frontend, poorly-documented, generated-heavy, unusual-layout).
- Boundary-type label match vs generator ground truth: 16/25 -> 11/25; 7 boundary regressions and
  3 boundary improvements per-repo (corrected accounting, see evidence-map-v1.md section 8 - the
  published "IMPROVED 11 / REGRESSED 4" is distorted by a classification-rule artifact).
- Conflicting-evidence detection 0.68 -> 0.92 (round 1); 75/75 standalone runs completed; zero
  missed/skipped repos; validation 25/25 after REPAIR-3; routing 1.000 across all rounds.
- Interaction probe (human review of 5 baseline briefs): machine contract strong; human-facing
  experience poor (too long, punchline buried, internal fog vocabulary, no confidence statement,
  no alternatives section).
- Baseline report internal inconsistency: 9 boundary mismatches listed but 17/25 = 0.68 claimed;
  the frozen scorer counts 16/25 = 0.64. The gate numbers are the canonical ones.

**Interpretations (claims that go beyond measurement - each is contested or untested):**
- "The candidate makes worse repository decisions" - NOT established. A label mismatch against a
  generator-authored rubric is not demonstrated degraded usefulness. No second human has adjudicated
  any of the shifted labels; the experiment's own records call several flips "defensible".
- "Prose guidance overfits at n=25" - supported by the two-round swing pattern (0.52 round 1,
  0.44 round 2 in opposite directions), but it is an inference about mechanism, not a measurement.
- "The 4 fog flips are defensible diagnoses" - the experiment's judgment; plausible (e.g.,
  web-frontend's app-cannot-boot argument is genuinely structural), untested by a second human.
- "The evidence-authority/exploration improvements are real gains" - the metrics moved and stayed
  stable, but they are structural proxies; no user-outcome evidence exists.
- "The frozen ground-truth labels are correct" - an assumption, contradicted in places by the
  experiment's own notes (tiny-lib product_fog "weak for this fixture"; cli-app "brief choice is
  defensible"; plugin-architecture "taxonomy gap") and by the human-authored ideal-response
  prototypes (tiny-lib's ideal weakness matches the baseline's non-ground-truth label).
- "0.640 -> 0.440 means the skill got worse" - true only for label-match; the jump from metric to
  skill quality is an interpretation.

## 3. Decision-changing uncertainty and reality boundary

**Single uncertainty most likely to reverse the next decision:**

> Is the candidate's (and the prose-guidance direction's) boundary-type regression genuinely worse
> repository decision-making, or mainly disagreement with the generator-authored frozen
> taxonomy/rubric?

Why this one: every alternative in section 1 forks on it.
- If the regression is real -> A (retain baseline) or C (simplify reasoning) or a narrowed repair.
- If it is mainly rubric/taxonomy disagreement -> E (redesign evaluation: adjudicated / claim-level
  labels), then possibly B (salvage the separable improvements) and D (deterministic procedure).
- Other uncertainties are less decision-reversing: runtime-path behavior (H5) tests the runtime, not
  the regression's meaning; corpus size (H2) re-measures the same contested labels; claim-level
  semantic metrics (H3) would tell us whether the flat evidence metrics mean anything, but those
  metrics did not fail the gate's decisive dimension (boundary accuracy did).

**Reality boundary.** Correctness of a weakness-type label for a repository is not fully observable
from the repository itself, and it is certainly not observable from a generator's intent file: it is
a substantive human judgment about which defect is most decision-relevant. The same applies to
"which brief is more useful" - that is a consumer judgment (human or downstream agent). The
25-repo corpus can provide neither: its ground truth is an un-adjudicated authoring artifact, its
fixtures are synthetic, and no user or downstream consumer was ever observed (see evidence-map-v1.md
section 5). The product-discovery-v0 evidence-boundary rules (evidence-boundaries-v1.md) say the
same thing: do not promote repository assertion into substantive correctness; human-required
decisions stay human. The probe below moves this question to evidence-ladder rung 4-5 (substantive
independent review + matched comparative result) - the highest rung reachable without real users.

## 4-6. Cheapest credible probe, precommitment, update

Blocks 4 and 5 (probe design and precommitment) are fully specified in probe-design-v1.md.
Block 6 (update: what changed, confidence, disposition, next probe) and the mandated
PRE-PROBE vs POST-PROBE comparison are in final-decision-update-v1.md.