# Metric assessment v1 - does weakest_boundary_accuracy track decision quality?

```
schema: evaluation-design-e1-v1/metric-assessment-v1
status: MANUAL ASSESSMENT over the 16 Task-D packet pairs. Agent-based; not human
  adjudication. All Task-D contamination limits apply.
```

## 1. What the metric counts vs what it misses

`weakest_boundary_accuracy` compares one field (`weakness_type`) against the frozen
generator-authored ground truth. In this 16-case sample it produced:
8 regressions (backend-service, full-stack, multi-language, poorly-documented,
multi-executable, hidden-coupling, strong-ui-fog, generated-heavy), 3 improvements
(tiny-lib, unusual-layout, adv-unused-dep), 4 unchanged-correct (adv-misleading-
readme, docs-heavy-code-light, monorepo, stale-readme), 1 both-wrong (web-frontend).

The decision-quality view over the same 16 pairs: 9 cosmetic (same engineering
work), 7 material (different first task or workflow), with routing (workflow and/or
execution mode) differing in 7 packets.

## 2. False-positive rate among regressions (metric over-penalizes)

Of the 8 metric regressions, 5 are false positives: full-stack, multi-language,
hidden-coupling, strong-ui-fog, generated-heavy. In all five, both labels are
defensible (or partially defensible) AND the two briefs converge on the same
engineering work (add Dockerfiles; resolve the TODO stub; the same refactor; the
same wiring fix; write api.proto). The metric converts a harmless taxonomy choice
into a "regression" of the whole skill. That is the primary failure mode the
hardening verdict was built on: 0.640 -> 0.440 was driven substantially by label
choices that do not change what an engineer would do next.

## 3. False-negative cases (metric misses consequential differences)

Four cases where the metric sees equality (or the wrong equality):

- adv-misleading-readme and docs-heavy-code-light: IDENTICAL weakness labels (both
  Ghost Features, both match gt) - the metric reports no regression - yet fog/routing
  differs (product-implementation guided vs docs-implementation guided) and the two
  briefs would drive materially different work (implement-vs-demote decision vs
  docs-only rewrite). The metric cannot see the most consequential difference.
- web-frontend: metric reports "both wrong" (neither brief matches gt Implicit
  Dependencies) and no regression; the consequential difference is again routing
  (ui-diagnostic plan_only vs architecture guided repair). The metric sees nothing.
- unusual-layout: metric counts an IMPROVEMENT (candidate Vocabulary Drift == gt),
  but the improvement routes to a docs-only workflow while the baseline routes to
  code work, and the blind agent preferred the baseline. The improvement flag may be
  inverted.

The second failure class from the E1 memo is real: same (or both-wrong) weakness
labels with different fog routing produce materially different engineering work,
and the metric is blind to it.

## 4. Ground-truth ambiguity

The frozen gt is contested in roughly half the sample. Sharpest: web-frontend
(gt Implicit Dependencies; both briefs and the blind agent independently identify
the module-loading Contract Mismatch - the app cannot boot), tiny-lib (gt Zero
Validation; the fixture HAS a test, so "nothing checks it" is overstated for the
functionality), unusual-layout (gt Vocabulary Drift; no history supports "drift"
over "phantom promise"), adv-unused-dep (blind agent argues Contract Mismatch).
A metric whose reference standard is itself in dispute cannot be a primary quality
gate without adjudication underneath it.

## 5. Where exact label agreement DOES matter (the metric is not useless)

- backend-service: label choice changes the first task (state-location fix vs
  test-suite first) AND the execution mode (plan_only vs guided).
- multi-executable: label choice changes the first task (CLI contract vs db work).
- poorly-documented: the label links to fog/routing (architecture vs docs).

In these 3 cases the metric has real signal - but it still cannot express direction
(the blind agent preferred the candidate in backend-service and multi-executable,
i.e. the "regressed" brief may be the better one), and it is redundant with the
routing signal in poorly-documented.

## 6. Summary counts

- Regressions flagged: 8. Decision-quality-supported: 3 (label-matters cases).
  False positives: 5. Direction of the 3 "real" ones: unsupported by this evidence
  (blind preference split 2 candidate / 1 baseline).
- Improvements flagged: 3. Benign: 1 (adv-unused-dep). Cosmetic/contested: 2
  (tiny-lib, unusual-layout; blind preference went against both).
- Differences the metric cannot see: 7 packets differ in routing (WF or MODE);
  4 are false-negative class.

## 7. What this means

The metric conflates taxonomy-label agreement with decision quality in both
directions: it punishes harmless label disagreement (5/8 regressions) and it misses
consequential routing differences (4 false negatives). Its reference standard (frozen
gt) is contested in roughly half the sample. Its only genuinely useful signal - the
3 label-matters cases - is mostly redundant with, or weaker than, the routing
consequence signal, and it cannot express direction.

The metric is therefore NOT a reliable primary quality gate. It retains diagnostic
value as a submetric (label drift, taxonomy hygiene, first-task sensitivity) - which
is the DEMOTE position. The routing-consequence dimension (workflow id + execution
mode + first-action category) shows stronger decision-relevant signal and is the
candidate replacement hypothesis to test next - not yet a replacement.

## 8. Limitations (inherited from Task D, preserved)

- The 16 cases are synthetic fixtures; n is small; no real user outcomes.
- The decision-quality judgments are agent-based (Task-D blind subagents + analyst
  reads), not human adjudication. Agent preference is not human ground truth.
- The blind agents were identity-ignorant but were also LLMs; their material/cosmetic
  and usefulness judgments are a weak proxy for a maintainer's.
- The original precommitted human-adjudication thresholds from the Task-C probe
  design were not satisfied by any run to date.