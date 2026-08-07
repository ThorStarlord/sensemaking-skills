# Evidence map v1 - what hardening-v1 actually established

```
schema: post-hardening-decision-probe-v1/evidence-map-v1
purpose: separate OBSERVED evidence from interpretations and hypotheses for the
  post-hardening decision; declare what the 25-repo corpus cannot provide.
sources (all read-only, from origin/hardening/repository-sensemaking-v1 @ a259bce):
  final-disposition-v1.yaml, phase15-comparison-v1.yaml, phase18-regression-analysis-v1.yaml,
  phase19-evaluation-report-v1.yaml, baseline-report.yaml, baseline-scored.yaml,
  candidate-freeze-v1.yaml, weakness-taxonomy-inventory-v1/v2.yaml, interaction-probe/*,
  tools/phase15_compare.py, tools/scorer_semantic_v1.py, tools/corpus_generator.py,
  corpus/ground-truth.yaml, baseline/*.md, candidate/*.md
```

## 1. Evidence ladder placement

Using the product-discovery-v0 ladder (evidence-boundaries-v1.md):

1. Repository assertion / proposed ADR
2. Implemented mechanism + deterministic test
3. Executed artifact under frozen conditions
4. Substantive independent review
5. Matched comparative result
6. External maintainer action/usefulness
7. Repeated outcome across contexts

Hardening-v1 evidence sits at rung 3 (executed artifacts under frozen conditions), with a small
rung-4 fragment (the interaction probe reviewed 5 baseline briefs as a user). It never reached
rung 4 for the candidate briefs (phase-17 blinded A/B was never executed), rung 5 (baseline vs
candidate were never compared blind), rung 6 (no maintainer/usefulness data), or rung 7. The gate
metrics are rung-3 measurements; the decision under review asks whether they may be promoted.

## 2. Observations (frozen measurements)

Every item below is directly verifiable from the committed artifacts; none requires judgment.

O1. Frozen gate results (charter.yaml, phase15-comparison-v1.yaml, phase19-evaluation-report-v1.yaml;
    scorer CF4D03F5, validator F53B637D, template A013FF8B, ground truth v2, 25-repo corpus):
    - unsupported_claim_rate:      0.632 -> 0.633   (gate '< baseline'  FAIL, flat)
    - evidence_precision:          0.844 -> 0.835   (gate '> baseline'  FAIL, flat, -0.009)
    - weakest_boundary_accuracy:   0.640 -> 0.440   (gate '> baseline'  FAIL, real decline)
    - routing_validity:            1.000 -> 1.000   (PASS)
    - validation_pass_rate:        1.000 -> 1.000   (PASS, after REPAIR-3)
    - observed_claim_accuracy:     0.818 -> 0.812   (PASS, no material regression)
    - inference_labeling_rate:     0.022 -> 0.040   (PASS, improved ~2x)
    - fog_classification_accuracy: 0.800 -> 0.760   (tracked, not gated; net -1 repo)

O2. Boundary-type label match vs generator ground truth: 16/25 -> 11/25. Per-repo delta:
    7 boundary regressions (backend-service, full-stack, multi-language, poorly-documented,
    multi-executable, hidden-coupling, strong-ui-fog), 3 boundary improvements (tiny-lib,
    unusual-layout, adv-unused-dep). (phase15-comparison-v1.yaml; corrected accounting in
    section 8 - the published "IMPROVED 11 / REGRESSED 4" is not reliable.)

O3. Fog flips: 3 corrected (docs-heavy-code-light, adv-misleading-readme, adv-partial-impl:
    docs_fog -> product_fog, matching ground truth), 4 flipped off (web-frontend ui_fog ->
    architecture_fog; poorly-documented docs_fog -> architecture_fog; generated-heavy
    architecture_fog -> product_fog; unusual-layout architecture_fog -> docs_fog).

O4. Conflicting-evidence detection rate 0.68 -> 0.92 (round 1 measurement, semantic scorer).

O5. Execution integrity: 75/75 standalone runs completed (one clean session per corpus repo,
    baseline protocol); zero missed/skipped repos; validation 25/25 after REPAIR-3; routing
    validity 1.000 across all rounds; zero hallucinated workflow IDs; entry-point coverage 33/33
    (baseline). (baseline-report.yaml, phase19 report, final-disposition section 3.)

O6. REPAIR accounting: 3/3 cycles used. REPAIR-1 restored the pre-existing HEAD test failure set
    (25 pre-existing failures, 0 new - full suite 2563 passed / 25 failed / 21 skipped at freeze).
    REPAIR-2 (constrained GAP-6 mapping + UI-fog tie-break + entry-point qualification) moved
    boundary accuracy 0.52 (round 1) -> 0.44 (round 2) - i.e., the constrained guidance still
    declined. REPAIR-3 fixed 3 YAML authoring defects (unquoted colons) without touching diagnosis
    content; validation returned to 25/25. (candidate-freeze-v1.yaml, phase18, phase19.)

O7. The semantic claim metrics are regex/structural proxies (tools/scorer_semantic_v1.py):
    a sentence is OBSERVED if it has a resolvable file:line citation, DERIVED if citation plus a
    reasoning marker, INFERRED if hedged without citation, UNSUPPORTED otherwise. The scorer cannot
    judge whether a claim is substantively true or useful. Evidence precision and unsupported-claim
    rate therefore measure citation discipline and sentence shape, not semantic quality.

O8. Interaction probe (review-findings-v1.md): a human review of the five frozen BASELINE briefs
    found the machine contract strong (grounded evidence, valid routing, defensible boundaries) and
    the human-facing experience poor (143-258 lines; punchline buried in section 6; internal fog
    vocabulary; no confidence statement; no alternatives section). All five baseline boundary
    selections were judged defensible/useful. The probe never reviewed candidate briefs.

O9. Human-authored ideal-response prototypes (interaction-probe/ideal-response-examples/): for
    tiny-lib the ideal weakness is "repository cannot be built or tested reproducibly" - aligning
    with the baseline's label (Implicit Dependencies), NOT with ground truth (Zero Validation).
    For strong-ui-fog the ideal response emphasizes "the app is structurally unstartable (no route
    registered)" - an architecture/wiring reading, not a UI-fog reading.

O10. Baseline report internal inconsistency: baseline-report.yaml lists 9 weakest-boundary
     mismatches but claims 17/25 = 0.68 accuracy; the frozen scorer counts 16/25 = 0.64 from the
     same data. The gate numbers (0.64) are canonical; the inconsistency shows the manual counts
     were themselves unstable.

O11. Corpus construction (tools/corpus_generator.py, ground-truth.yaml): all 25 repositories are
     small synthetic fixtures (17 repository classes + 8 adversarial variants) generated with
     deterministic commits; ground truth (expected fog candidates, known weak boundaries) was
     authored by the generator, frozen before candidate outputs. The fixtures are NOT real
     repositories and ground truth is NOT independently adjudicated.

## 3. Interpretations (claims beyond the measurements)

I1. "The candidate makes worse repository decisions." Rests on O2/O3. NOT established: label
    mismatch against an un-adjudicated synthetic rubric is not demonstrated degraded usefulness;
    the experiment itself calls the 4 fog flips "defensible diagnoses" (final-disposition 4.2) and
    the web-frontend flip "genuinely structural" (phase18 regression_2).

I2. "Prose guidance overfits at n=25." Rests on O6 (two rounds swung in opposite directions:
    GAP-6 over-generalized Ghost Features round 1; over-corrected into Implicit Dependencies /
    Vocabulary Drift round 2) plus the swing band 0.44-0.64 overlapping baseline. Plausible
    mechanism inference; it is about WHY the metric moved, not a measurement.

I3. "The remaining 4 fog flips are all defensible." The experiment's judgment (final-disposition
    4.2). Untested by any second human; the probe adjudicates it.

I4. "The improvements (evidence authority, exploration, routing safety) are genuine gains."
    Rests on O4, O5, O1 (inference labeling). The metrics moved and stayed stable across three
    rounds, but they are proxy/stability metrics; no user-outcome evidence exists (rung 6-7 absent).

I5. "The frozen ground-truth labels are correct." An assumption. Contradicted in places by the
    experiment's own records (tiny-lib "ground-truth product_fog is weak for this fixture",
    cli-app "brief choice is defensible", plugin-architecture "taxonomy gap", baseline-report
    weakest_boundary_mismatches notes) and by O9 (tiny-lib ideal response matches the baseline
    label, not ground truth).

I6. "0.640 -> 0.440 is a skill-quality regression." Only the label-match half is measured; the
    skill-quality half is an interpretation (I1).

I7. "Boundary-type accuracy can/cannot be improved at n=25 under any guidance regime." Unresolved
    by the experiment's own admission (final-disposition 5.1: the observed swing band overlaps
    baseline). Neither direction is established.

## 4. Hypotheses (follow-up ideas - NOT selected, NOT authorized)

From final-disposition-v1.yaml section 6 (explicitly listed "WITHOUT selection"):
- H1: deterministic boundary-type decision procedure (binary-gate checklist) instead of prose.
- H2: larger corpus (50+ fixtures) to reduce variance + enable per-repo adjudication.
- H3: claim-level ground truth (human-annotated claim labels) for semantic metrics.
- H4: taxonomy redesign (e.g., application-code-native types instead of agent-oriented seven).
- H5: runtime-path end-to-end evaluation (skeleton + reconciliation + validate-and-record).
- H6: human-perceived quality A/B (blinded review of baseline vs hardened briefs).

From this task's alternative list: A (stop/retain baseline), B (salvage individually supported
ideas), C (simplify weakest-boundary reasoning), D (= H1), E (= H3/H6-shaped evaluation redesign),
F (= H5 + H6), G (= H2), H (do nothing, focus elsewhere).

All are hypotheses: each requires separate evaluation and authorization before any implementation.
This package selects ONE probe (adjudicated comparative review = the H6/E component) as the next
action; it does not select any implementation.

## 5. What the 25-repo corpus cannot provide

1. **Ground-truth correctness.** Labels are generator-authored intent (O11); no second human has
   adjudicated any of the 25 fixtures. The corpus cannot tell us which label is "right" - it can
   only tell us which brief matched the authoring intent.
2. **Real repository diversity.** All fixtures are synthetic and tiny (5-12 files); real-world
   frameworks, ecosystems, legacy history, team conventions, and scale are absent.
3. **User/consumer outcomes.** Nothing observed a real decision-maker or downstream agent acting on
   a brief; usefulness, actionability, and whether the boundary choice changes action are unmeasured
   (rungs 6-7).
4. **Blinded human preference.** Phase-17 A/B (baseline vs candidate, blind) was never executed
   (final-disposition 5.6). Only baseline briefs were human-reviewed (O8).
5. **Runtime-path behavior.** All 75 runs were standalone; the runtime reconciliation path
   (brief_skeleton) was exercised only by unit tests (final-disposition 5.4).
6. **Claim-level semantic truth.** The scorer is structural (O7); the flat evidence metrics
   (O1) cannot distinguish guidance quality from authoring style - the experiment says so itself
   (final-disposition 4.4).
7. **Model variance separation.** Each repo ran once per condition; no repeated runs under the same
   condition, so treatment effect and model variance are confounded (the 0.44-0.64 swing band
   overlaps baseline - final-disposition 5.1).
8. **Justified thresholds.** No base rates exist; the experiment avoided inventing formal success
   thresholds for this reason (product-discovery-v0 unnecessary-ceremony-v1.md makes the same point).

## 6. The boundary-regression question: real degradation or rubric/taxonomy disagreement?

Both components are present; their proportions are unknown. That unknown is the decision-changing
uncertainty.

**Measured (O2, O3):** the candidate's labels matched the frozen ground truth on 11/25 vs the
baseline's 16/25 - a real, frozen-scorer decline of 5 repos (7 boundary regressions vs 3
improvements; fog net -1). This is not in dispute.

**Evidence that the decline may be substantially rubric/taxonomy disagreement, not worse decisions:**
- The experiment's own analysis labels the 4 fog flips "DEFENSIBLE diagnoses under the new rules"
  (final-disposition 4.2) and the web-frontend flip "genuinely structural" (phase18 regression_2).
- Ground truth is un-adjudicated generator intent (O11); the experiment's own notes dispute several
  labels (I5); the tiny-lib human ideal response aligns with the baseline label, not ground truth
  (O9); the baseline human review found the baseline's (ground-truth-mismatched) boundary choices
  defensible (O8).
- 7 of 25 repos were mismatched under BOTH baseline and candidate (cli-app, web-frontend,
  generated-heavy, plugin-architecture, adv-duplicated-packages, adv-removed-feature-docs,
  adv-multi-registry) - i.e., the rubric and both briefs disagree; the rubric itself is not a
  settled arbiter.
- Boundary choices in the briefs are often richer than a single label: e.g., both baseline and
  candidate web-frontend briefs identify the same module-loading Contract Mismatch (the app cannot
  render) while ground truth says Implicit Dependencies (api base URL) - the label metric collapses
  materially better reasoning into "wrong".

**Evidence that the decline may be real degradation:**
- The decline reproduced in two rounds in different directions (O6) - the guidance changes moved
  labels off the rubric repeatedly, and REPAIR-2's corrections did not recover accuracy.
- The candidate over-applied Ghost Features in round 1 and over-corrected in round 2
  (phase18 regression_1, phase19 item 1) - a pattern consistent with guidance that genuinely
  misleads at the margin, not merely a rubric that disagrees.
- 6 of the 7 boundary regressions moved AWAY from the rubric while fog stayed correct
  (section 8) - more systematic than the 4 published regressions suggest.

**Verdict for the decision:** "partly rubric/taxonomy disagreement" is supported but the fraction
is unknown; "actual degraded usefulness" is neither established nor refuted. Only human
adjudication of the shifted labels + blinded usefulness comparison can split the two - which is
exactly the probe (probe-design-v1.md). The 25-repo corpus, by itself, can never answer this
question (section 5.1, 5.4).

## 7. Separability of the evidence-authority/exploration improvements

Yes - separable enough to test independently, with a caveat.

**Commit-level separation** (hardening branch history, e188f43..bcd7c21):
- Commit 1 (1ae8a84): deterministic exploration + evidence authority + GAP-1/GAP-3 (quote modes,
  citation extensions).
- Commit 2 (05460cb): architecture reconstruction.
- Commit 3 (f4cc0d1): GAP-6 weakest-boundary mapping guidance - the boundary-regression driver
  (phase18 regression_1).
- Commit 4 (8383a9e): fog classification rules + ghost-feature 3-way rule - the fog-flip driver
  (phase18 regression_2/3).
- Commit 5 (63b3a05): workflow routing.
- Commit 6 (b0a504e): artifact contract + semantic validator hardening.
- Commit 7 (bcd7c21): regression suite.

**Metric-level separation:** the measured improvements move with the non-boundary commits -
inference_labeling 0.022 -> 0.040 and conflict detection 0.68 -> 0.92 (Commit 1 evidence
authority); routing validity 1.000 and validation 1.000 across all rounds (Commits 5-6);
the declines move with Commits 3-4 (boundary 0.64 -> 0.52 -> 0.44; fog 0.80 -> 0.76). REPAIR-2
operated on Commits 3-4 alone, and the phase18 analysis attributes the regressions to them.

**Caveat (why adjudication comes first):** the commits interact at the margin - the ghost-feature
3-way fog rule (Commit 4) also changed some weakness-type mappings, and the UI-fog tie-break
feeds boundary selection. A salvage candidate ("baseline + Commits 1,2,5,6,7") is therefore
buildable and re-measurable on the frozen corpus with the frozen scorer, but its isolation is not
perfect, and the salvage decision depends on which labels adjudication says were right in the
first place (if the candidate's Ghost Features choices are right, Commits 3-4 are partly salvageable;
if not, they are not). The probe determines salvage scope.

## 8. Corrected per-repository accounting (new finding)

The published summary "IMPROVED 11 / UNCHANGED 10 / REGRESSED 4" (phase15-comparison-v1.yaml,
repeated in final-disposition and phase19) is distorted by a classification-rule artifact in
tools/phase15_compare.py:150-158:

```
state = "IMPROVED"                                   # default
if (fog_b, boundary_b) == (fog_c, boundary_c): UNCHANGED
if (not fog_b and not fog_c) and (boundary_b and not boundary_c): REGRESSED
if fog_b and not fog_c: REGRESSED
if fog_b == fog_c and (not boundary_b and boundary_c): IMPROVED
```

The default-IMPROVED fallthrough never downgrades a repo whose boundary regressed while fog stayed
correct. Verifying each of the 11 "IMPROVED" rows against the phase15 per-repo data:

- Genuine improvements (5): tiny-lib (boundary +), docs-heavy-code-light (fog +),
  adv-misleading-readme (fog +), adv-unused-dep (boundary +), adv-partial-impl (fog +).
- Mislabeled (6, boundary regression misreported as IMPROVED): backend-service (Zero Validation ->
  Implicit Dependencies, gt Zero Validation), full-stack (Contract Mismatch -> Ghost Features,
  gt Contract Mismatch), multi-language (Ghost Features -> Implicit Dependencies, gt Ghost
  Features), multi-executable (Implicit Dependencies -> Ghost Features, gt Implicit Dependencies),
  hidden-coupling (Implicit Dependencies -> Vocabulary Drift, gt Implicit Dependencies),
  strong-ui-fog (Zero Validation -> Implicit Dependencies, gt Zero Validation).

Corrected summary: **IMPROVED 5 / UNCHANGED 10 / REGRESSED 10.** (Note also: the disposition's
"supported directions" item 6 claims multi-language "landed correctly" - contradicted by the
phase15 per-repo data, which shows multi-language moved AWAY from its ground-truth type.)

Consequences:
1. The candidate's boundary regression is broader than published: 7 boundary regressions vs
   3 boundary improvements, not "4 regressed repos" (the 4 published are fog flips; 3 of them -
   poorly-documented, generated-heavy, unusual-layout - carry boundary changes too, and 6 pure
   boundary regressions were hidden).
2. The gate verdict (FAIL) is unaffected - it is computed directly from label matches, not from
   this classification - but every narrative claim built on "11 improved" must be discarded.
3. The probe's contested set must therefore cover all 10 boundary-changed repos (see
   probe-design-v1.md section 2), not just the 4 published regressions.

## 9. What this map means for the decision

- The gate failure is observed; its meaning is interpretation (I1/I2/I3) and the decisive question
  (section 6) is answerable only by human adjudication.
- The candidate's measurable good news (O4, O5, inference labeling) is real but proxy-level; the
  good news is separable from the regressing sections (section 7), so a salvage path exists and is
  cheaper than a redesign - but its scope depends on the probe.
- The experiment's own summary numbers are not fully trustworthy (O10, section 8); the frozen
  gate numbers are. Any future workstream should re-derive per-repo classification from the frozen
  data before quoting it.
- Pre-probe confidence in "probe first" was low-to-medium; this map raises confidence in the
  ACTION (probe) while leaving outcome confidence low - the probe is specifically designed so that
  either outcome changes what happens next.