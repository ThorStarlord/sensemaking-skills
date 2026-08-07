# Assessment v1 - does decision_delta track materiality?

```
schema: evaluation-design-e2-v1/assessment-v1
status: MANUAL, agent-based. Task-D material/cosmetic is the reference and is
  NON-HUMAN evidence. E2 does not judge which brief is better.
```

## 1. Measured performance (16 pairs)

Reference: Task-D materiality = 7 material, 9 cosmetic (blind subagent, non-human).

decision_delta = routing_delta OR action_delta fired in 8 pairs:
backend-service, poorly-documented, multi-executable, unusual-layout, web-frontend,
adv-misleading-readme, docs-heavy-code-light (the 7 material) + generated-heavy
(the 1 cosmetic).

- Material cases caught: 7 / 7 (100%).
- Cosmetic cases unnecessarily flagged: 1 / 9 (generated-heavy, 11%) - a
  workflow-id-only difference (architecture vs product) with an identical first
  action (author api.proto). Refinement: do not fire on workflow-name-only deltas
  when the normalized first-action category matches.
- Material misses: 0.
- Complementarity: multi-executable is caught ONLY by action_delta (routing
  identical); web-frontend is caught ONLY by routing_delta (first action
  identical). Neither delta alone is sufficient; the OR combination is required
  and sufficient on this sample.

## 2. Does weakness-label disagreement add useful information beyond decision_delta?

No. All 6 label-disagreement cases with decision_delta=0 are Task-D cosmetic
(full-stack, multi-language, hidden-coupling, strong-ui-fog, adv-unused-dep,
tiny-lib): label disagreement re-flags exactly the cases decision_delta correctly
leaves alone - i.e., the over-penalization mode of the old metric. Conversely, the
2 cases where labels AGREE but work materially differs (adv-misleading-readme,
docs-heavy-code-light, both Ghost Features == gt, metric "unchanged") are exactly
the cases decision_delta catches and the label metric misses. Label agreement is
therefore neither necessary nor sufficient for materiality; decision_delta
dominates it on this sample.

## 3. Contrast with the frozen metric on the same 16 pairs

- 4 of the 8 metric regressions (full-stack, multi-language, hidden-coupling,
  strong-ui-fog) have decision_delta=0: the metric's false positives are exactly
  the decision-cosmetic cases.
- 2 metric "unchanged" cases (adv-misleading-readme, docs-heavy-code-light) have
  decision_delta=1: the metric's false negatives.
- 1 metric "improvement" (unusual-layout) has decision_delta=1: the improvement
  flag sits on a consequential disagreement; 1 (tiny-lib) has decision_delta=0:
  the improvement flag sits on a harmless label change.
- web-frontend (metric "both wrong") has decision_delta=1 via routing.

So decision_delta and the label metric disagree exactly where the label metric is
known to mislead (E1: 5 false positives, 4 false negatives), and agree where the
difference is genuinely consequential (backend-service, poorly-documented,
multi-executable via action; the routing cases).

## 4. Normalization judgment calls (transparency)

- multi-language (CONTRACT-DOC vs CONTRACT-IMPLEMENT counted same-cluster): both
  briefs resolve the same helper contract; Task-D cosmetic; if counted as a delta,
  it becomes a second cosmetic false flag. Recorded, not hidden.
- strong-ui-fog (TESTS vs DIAGNOSTIC counted same-cluster): first step differs but
  converges on the same action set; Task-D cosmetic. A stricter reader would flag
  it (second false flag). The two judgment calls bracket the false-flag rate at
  1-3 of 9 cosmetic cases, not 0.
- web-frontend first-action is identical (BOOT-FIX/BOOT-FIX): the materiality is
  genuinely the routing/mode, which routing_delta captures.

## 5. Caveats (preserved from Task D/E1)

- The reference (Task-D material/cosmetic) is blind-subagent judgment, not human
  ground truth; it is correlated with the same briefs the deltas are extracted
  from, so the 7/7 catch rate is partly circular. The mechanical deltas are NOT
  circular (they read Section 13/11 fields), but the reference is.
- n=16 synthetic fixtures; no real users; no outcome data.
- Action-category coding was done by the analyst with the two recorded judgment
  calls; a human coding pass would harden it.
- E2 does not score which brief is better. A material delta means "different work",
  never "worse work".

## 6. Bottom line

decision_delta (routing OR first-action delta) is a reliable materiality detector
on this sample: 7/7 material caught, 0 material misses, 1-3/9 cosmetic false
flags (exactly 1 under the recorded normalization), and it strictly dominates
weakness-label disagreement as a source of decision-relevant signal. That is the
USE_AS_TRIAGE_SIGNAL result - as a trigger for targeted adjudication, not as a
quality metric (direction/quality still needs adjudication, exactly as the memo
framed it).