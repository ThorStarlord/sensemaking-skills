# Final decision update v1 - block 6 and PRE vs POST comparison

```
schema: post-hardening-decision-probe-v1/final-decision-update-v1
block: six-block block 6 (update: what changed, confidence, disposition, next probe)
plus the mandated PRE-PROBE ACTION vs POST-PROBE ACTION comparison
status: PROSPECTIVE - records the decision state and precommitted update BEFORE the probe runs;
  the probe itself is not executed and nothing is implemented
```

## Block 6. Update

**What changed (from reading the inputs, before any probe runs):**
1. The owner's pre-probe inclination is confirmed as the right action class: probe first, no
   implementation. The reading sharpened it into a specific, precommitted design (probe-design-v1.md).
2. New observation-level finding: the published per-repo summary "IMPROVED 11 / UNCHANGED 10 /
   REGRESSED 4" is distorted by a classification-rule artifact in tools/phase15_compare.py
   (default-IMPROVED fallthrough); corrected accounting is IMPROVED 5 / UNCHANGED 10 / REGRESSED 10
   (evidence-map-v1.md section 8). The candidate's boundary regression is broader than published
   (7 boundary regressions vs 3 improvements), so the probe's contested set covers all 10
   boundary-changed repos, not the 4 published regressions.
3. The decisive uncertainty is now precisely identified: whether the boundary regression is
   genuinely worse decision-making or mainly disagreement with the generator-authored rubric
   (decision-record-v1.md section 3). All eight alternatives (A-H) fork on it; the other unresolved
   uncertainties (runtime mode H5, corpus size H2, claim-level metrics H3) are downstream or
   orthogonal.
4. The regression is now known to be "partly rubric/taxonomy disagreement" in the weak sense -
   the experiment's own records dispute several frozen labels and the human ideal-response
   prototypes align with non-ground-truth labels - but the fraction is unknown and no second human
   ever adjudicated any label or compared the briefs blind (evidence-map-v1.md section 6).
5. The evidence-authority/exploration improvements are separable at the commit level from the
   regressing boundary/fog sections and moved their own metrics (evidence-map-v1.md section 7);
   a salvage path (B) is viable after the probe, with scope set by adjudication.

**Confidence:**
- In the chosen action (run the adjudicated comparative probe; do not implement): raised from
  low-to-medium to HIGH. The probe reuses frozen artifacts, costs 3-5 h, fills the exact
  phase-17 gap, and its outcome maps to a precommitted next action either way; no cheaper probe
  can split the regression question.
- In the outcome of the probe (which branch will trigger): remains LOW. The direction of the
  verdict is genuinely unknown; that is precisely why the probe is precommitted and not predicted.

**Disposition:**
- CONTINUE - manual, human-adjudicated, blinded comparative probe (probe-design-v1.md);
  no implementation, no skill change, no corpus/scorer/gate change.
- The hardening-v1 workstream stays CLOSED - REVISE. The candidate skill is not merged, not
  copied, and not modified. The current baseline remains the shipped repo-sensemaker.
- Supported lessons from hardening-v1 (evidence authority model, deterministic exploration
  protocol, registry authority + execution-mode rule, invocation-mode contract, citation
  extensions, ghost-feature fog corrections, selection structure) remain RECORDED AS HYPOTHESES
  with measured proxy support - not production changes - exactly as final-disposition-v1.yaml
  section 3 states. They become salvage candidates only if the probe outcome supports it.

**Next probe (after this one, conditional):**
- If H_rubric confirmed -> E (evaluation redesign: adjudicated/claim-level labels) then B/D.
- If regression real -> A (retain baseline) with optional C (simplification experiment).
- If ambiguous -> E with a second reviewer + claim-level rubric on the extended 25-repo sample.
- Whichever branch: any subsequent workstream requires its own charter and authorization; this
  package authorizes none of them.

## PRE-PROBE ACTION vs POST-PROBE ACTION

**PRE-PROBE ACTION (owner's pre-probe decision, preserved verbatim in decision-record-v1.md):**
"Do not start another repo-sensemaker implementation yet. Preserve the current baseline and the
supported lessons from hardening-v1, and first run a cheap probe to determine whether the
weakest-boundary regression represents genuinely worse repository decisions or mainly disagreement
with the frozen taxonomy/rubric. Confidence: low-to-medium."

**POST-PROBE ACTION (this package's decision):**
Run a manual, human-adjudicated, blinded comparative review of the 12 contested corpus repos
(10 boundary-changed + 2 fog-only flips) plus 4 calibration repos, in which an independent human
reviewer (the owner) judges, per repo, the most defensible weakness-type label and the more useful
brief, with precommitted thresholds mapping each outcome to a next action (E/B/D, or A/C, or
E-extended). No implementation. Baseline and supported lessons preserved. The hardening workstream
remains closed.

**Are they identical?** In action class, YES: both say "probe first, no implementation, preserve
baseline + supported lessons." The post-probe decision did not change the owner's inclination - it
was validated by the evidence rather than overturned.

**What changed between them (and the evidence/reasoning that caused it):**
1. The probe is now concretely specified (blinded adjudicated comparative review with per-repo
   questions, sealed A/B identities, precommitted thresholds) instead of an unspecified "cheap
   probe". Caused by: evidence-map section 6 - the regression question can only be split by human
   adjudication + blinded comparison, and phase-17 was never executed
   (final-disposition-v1.yaml 5.6).
2. The probe's scope grew from "the regression" (implicitly the 4 published regressed repos) to
   all 10 boundary-changed repos. Caused by: the corrected per-repo accounting (evidence-map
   section 8) showing the published 11/10/4 summary mislabels 6 boundary regressions as
   IMPROVED, plus the baseline report's own internal count inconsistency (O10).
3. The post-probe decision is precommitted (each outcome maps to a specific next action), so the
   probe cannot be rationalized after the fact. Caused by: the product-discovery-v0 discipline of
   predeclaring observations, disconfirming evidence, stop conditions, and ambiguity
   (evidence-boundaries-v1.md, unnecessary-ceremony-v1.md), and by the observation that
   hardening-v1's own disposition already lists six unselected hypotheses - this package must not
   add a seventh.
4. Confidence in the ACTION rose from low-to-medium to high, while outcome confidence stays low.
   Caused by: the probe being the cheapest credible route to the evidence-ladder rungs the
   regression question requires (rungs 4-5), with zero new tooling and frozen artifacts.

**Statement of identity:** the pre- and post-probe decisions are identical in action class
(probe first; no implementation; preserve baseline and supported lessons). The differences are in
probe specification, scope, precommitment, and confidence - all driven by evidence read during
this probe-preparation package, not by a change of inclination. That the owner's original
inclination survived a full evidence pass is itself evidence that "probe first" is robust.

## Package closure

- This is a decision/probe package only. The probe is NOT executed, and no implementation begins
  automatically (per task instruction).
- Deliverables: decision-record-v1.md, evidence-map-v1.md, probe-design-v1.md,
  final-decision-update-v1.md (this file).
- Nothing in experiments/product-discovery-v0/**, the hardening-v1 evidence, canonical skills,
  validators, runtime, workflows, scorer, or corpus was modified; the candidate skill was not
  merged or copied.