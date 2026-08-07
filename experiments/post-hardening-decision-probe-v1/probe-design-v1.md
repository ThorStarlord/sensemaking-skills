# Probe design v1 - adjudicated comparative review of the contested repos

```
schema: post-hardening-decision-probe-v1/probe-design-v1
status: DESIGNED AND PRECOMMITTED - NOT EXECUTED (execution requires separate go-ahead)
block: six-block blocks 4 (cheapest credible probe) and 5 (precommitment)
cost_estimate: one reviewer x 12-16 small repos x 10-15 min + ~1 h analysis = 3-5 h total;
  zero new tooling; all artifacts already exist frozen
```

## 1. Probe question

Does the candidate's measured boundary-type regression (0.640 -> 0.440) represent genuinely worse
repository decision-making, or mainly disagreement with the generator-authored frozen
taxonomy/rubric? Equivalently: when a second human reads the fixtures and both briefs blind, which
labels and which briefs come out on top?

This is the phase-17 blinded A/B that hardening-v1 never executed because the mechanical gate
failed first (final-disposition-v1.yaml section 5.6), plus the per-repo label adjudication that the
experiment explicitly lists as never performed (section 5.2). It is the cheapest probe that reaches
evidence-ladder rungs 4-5 (substantive independent review + matched comparative result) for this
question: no implementation, no corpus changes, no new runs - only human reading of frozen
artifacts.

## 2. Sample (frozen artifacts only)

Primary set - all repos where baseline and candidate disagree on weakness_type or fog
(12 repos; the full contested space per evidence-map-v1.md sections 2 and 8):

1.  backend-service      (boundary regressed: Zero Validation -> Implicit Dependencies)
2.  full-stack           (boundary regressed: Contract Mismatch -> Ghost Features)
3.  multi-language       (boundary regressed: Ghost Features -> Implicit Dependencies)
4.  poorly-documented    (boundary regressed + fog flipped)
5.  multi-executable     (boundary regressed: Implicit Dependencies -> Ghost Features)
6.  hidden-coupling      (boundary regressed: Implicit Dependencies -> Vocabulary Drift)
7.  strong-ui-fog        (boundary regressed: Zero Validation -> Implicit Dependencies)
8.  tiny-lib             (boundary improved: Implicit Dependencies -> Zero Validation)
9.  unusual-layout       (boundary improved + fog flipped)
10. adv-unused-dep       (boundary improved: Ghost Features -> Implicit Dependencies)
11. web-frontend         (fog flipped: ui_fog -> architecture_fog; both briefs pick Contract Mismatch)
12. generated-heavy      (fog flipped: architecture_fog -> product_fog)

Calibration set (4 repos): adv-misleading-readme + docs-heavy-code-light (fog corrections both
briefs agree on the ground truth - checks that the adjudicator can find the "obviously right"
cases), monorepo + stale-readme (stable repos, both briefs agree with ground truth - checks
baseline calibration).

Optional extension: the remaining 9 repos (full 25-repo pass) if the primary pass is ambiguous
(see stop conditions) or if cost allows; not required for the decision.

## 3. Method (manual, comparative, human-adjudicated)

1. **Reviewer:** the decision owner (per product-discovery-v0: the owner, not the agent, rates
   usefulness). A second reviewer is added only if the ambiguity condition (section 5) triggers.
2. **Blinding:** reviewer sees the fixture (read-only), then the two briefs labeled A and B with
   per-repo randomized order; reviewer does NOT see ground-truth.yaml, phase15-comparison,
   phase18/19 reports, or the disposition, and is not told which brief is baseline vs candidate.
   After each repo, note whether the reviewer could tell which brief was which (template/style
   differences may leak; record as a confounder, not a failure).
3. **Per-repo questions** (reusing the frozen interaction-probe question set where applicable,
   review-findings-v1.md):
   - Q1 (adjudicated label): "Reading the fixture yourself, which single weakness type is the most
     defensible weakest boundary? (choose from the seven canonical types, or Other / undecidable)."
   - Q2 (usefulness): "Which brief (A/B) gives the more useful and substantively accurate diagnosis
     for a human or downstream agent? (A / B / no material difference)."
   - Q3 (defensibility): "For the weakness type each brief chose, is that choice defensible given
     the fixture? (defensible / partially / not defensible) - one answer per brief."
   - Q4 (materiality): "Is the A/B difference material to the decision a user would make next, or
     cosmetic? (material / cosmetic / cannot tell)."
   - Q5 (fog label, only for the 4 fog flips + calibration): "Is the fog label in each brief
     defensible and useful, or is the fog axis itself the wrong question here?"
   - Record per-repo time and reviewer confidence (high/medium/low).
4. **Analysis (mechanical, no re-scoring):** produce a per-repo table; compute (a) adjudicator
   label vs ground-truth agreement rate, (b) adjudicator label vs candidate-label agreement rate,
   (c) adjudicator label vs baseline-label agreement rate, (d) Q2 usefulness tally, (e) Q3
   defensibility tally, (f) Q4 material/cosmetic tally, (g) fog verdicts, (h) time cost.
   No corpus/scorer/gate re-run; the frozen gate numbers stay as they are.

## 4. Precommitment: observations to record

- The full per-repo table (Q1-Q5, A/B identities kept sealed until the table is complete).
- Agreement rates (a)-(f) above, computed AFTER the table is complete.
- Any repo where the reviewer could not decide Q1 or Q2 ("undecidable").
- Blinding-leak notes per repo.
- Total reviewer time and per-repo time.
- Reviewer's own confidence per repo and overall.

## 5. Precommitment: disconfirming evidence, stop condition, ambiguity

**Hypothesis under test (H_rubric):** the regression is predominantly rubric/taxonomy disagreement;
the candidate's shifted labels and briefs are at least as defensible as the baseline's.

**Disconfirming evidence for H_rubric (i.e., evidence that the regression is real):**
- Adjudicator's independent label agrees with GROUND TRUTH on >= 5 of the 7 boundary-regressed
  repos, AND
- Baseline brief judged more useful than candidate (Q2) on >= 7 of the 10 boundary-changed repos,
  AND
- Fewer than 2 of the 4 fog flips adjudicated "defensible" (Q3/Q5).

**Confirming evidence for H_rubric (i.e., evidence the regression is mostly rubric disagreement):**
- Adjudicator's independent label agrees with the CANDIDATE label on >= 5 of the 7 boundary-
  regressed repos, AND
- Candidate brief judged at least as useful as baseline (Q2: candidate or no-material-difference)
  on >= 6 of the 10 boundary-changed repos, AND
- >= 3 of the 4 fog flips adjudicated "defensible".

**Stop condition:** the probe stops when the per-repo table for the 12 primary repos is complete.
No implementation may start from any intermediate result; the sealed A/B identities are opened
only after the table is complete. If total time exceeds 2x the estimate (10 h), halt and report
partial results restricted to the 7 boundary-regressed repos. The probe's product is a decision,
never a patch.

**Ambiguity (neither branch triggers):**
- Mixed verdicts (e.g., 3-4 of 7 on the label discriminator and a near-tie on Q2), or
- "Undecidable" on >= 3 primary repos, or
- The fog-axis answers are consistently "the fog label is the wrong question" (Q5).

Under ambiguity, the correct conclusion is: the regression's meaning is unresolvable at this
sample with a single reviewer - NOT support for either direction and NOT a license to implement.
The next probe would be a second reviewer plus a claim-level, per-label rubric (disposition H3/E),
optionally extended to all 25 repos, before any skill change.

## 6. Precommitted decision rules (probe outcome -> next action)

| Probe outcome | Verdict on the uncertainty | Next action (no implementation in this package) |
|---|---|---|
| H_rubric confirmed | Regression is mainly rubric/taxonomy disagreement; candidate labels/briefs at least as defensible | E first: redesign weakest-boundary evaluation (adjudicated/claim-level labels) as the next workstream, then B: salvage the separable improvements (evidence-map section 7) and D: deterministic procedure - evaluated on the frozen corpus with the frozen scorer, under a new mini-charter with narrowed gates |
| Regression real | Candidate guidance genuinely misleads at the margin | A: retain the current baseline; optionally C: a simplification experiment (smaller boundary guidance, measured on the frozen corpus) before any further hardening |
| Ambiguous | Unresolvable at this sample | E: second reviewer + claim-level rubric, extended sample; no skill change; no salvage claims |
| (invariant) | - | The closed hardening experiment stays closed; the candidate skill is not merged or copied; baseline remains the shipped skill; supported lessons stay recorded as hypotheses until a new workstream is authorized |

The thresholds (5/7, 6-7/10, 3-4/4) are precommitted majorities, chosen before execution so the
result cannot be rationalized after the fact; the "undecidable" accounting prevents a forced call.
Calibration-set expectations: the reviewer should pick the corrected labels (product_fog) for
adv-misleading-readme and docs-heavy-code-light and the stable labels for monorepo/stale-readme;
if the reviewer disagrees with all four, the reviewer's rubric differs fundamentally from the
frozen one and the probe reads as "rubric disagreement, all the way down" - that outcome itself
is informative and maps to E.

## 7. Cost and alternatives rejected as more expensive

- Probe cost: ~3-5 h of one reviewer; artifacts already frozen; no code, no model runs, no corpus
  changes.
- Rejected as more expensive / less decision-relevant for THIS question: runtime-path evaluation
  (H5; tests the runtime, not the regression's meaning), corpus expansion (H2; re-measures the
  same un-adjudicated labels), claim-level semantic re-scoring (H3; tells us about the flat
  evidence metrics, not the boundary question), deterministic-procedure implementation (H1;
  implementation before adjudication risks building on the wrong foundation).
- The probe is also the exact "cheapest credible probe" pattern from product-discovery-v0:
  question -> observed evidence -> decision-changing uncertainty -> cheapest probe -> predeclared
  evidence -> update, with the owner (not the agent) making the usefulness judgment.