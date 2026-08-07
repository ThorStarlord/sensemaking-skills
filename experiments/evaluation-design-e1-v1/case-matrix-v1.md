# Case matrix v1 - 16 Task-D packet pairs

```
schema: evaluation-design-e1-v1/case-matrix-v1
basis: Task-D packets (identity known) + Task-D analysis-v1.md (blind subagent
  verdicts) + workflow/mode extraction from Section-13 handoffs + analyst reads.
non-human evidence: the Task-D blind preference column is agent preference only,
  never treated as human ground truth.
```

## Column keys

- gt = frozen ground-truth weakness type; base/cand = brief labels; metric verdict =
  does `weakest_boundary_accuracy` count the candidate as correct (C), regressed (R),
  unchanged-correct (U), unchanged-both-wrong (W).
- evid = evidence defensibility; bound = boundary defensibility (candidate/baseline);
  material = decision materiality; routing = routing consequence (SAME/WF/MODE);
  action = action quality; uncert = uncertainty quality. Values per rubric.
- blind = Task-D blind-agent usefulness preference (SECONDARY, non-human).

| # | packet | gt | base label | cand label | metric | evid | bound (cand/base) | material | routing | action | uncert | blind | class |
|---|--------|----|-----------|-----------|--------|------|-------------------|----------|---------|--------|--------|-------|-------|
| 1 | backend-service | Zero Validation | Zero Validation | Implicit Dependencies | R | both-strong | defensible / defensible | material | MODE (arch, plan_only vs guided) | cand-better | cand-better | candidate | label-matters |
| 2 | full-stack | Contract Mismatch | Contract Mismatch | Ghost Features | R | both-strong | defensible / partially | cosmetic | SAME | cand-better | both-adequate | candidate | FP |
| 3 | multi-language | Ghost Features | Ghost Features | Implicit Dependencies | R | both-strong | defensible / partially | cosmetic | SAME | cand-better | both-adequate | candidate | FP |
| 4 | poorly-documented | Zero Validation | Zero Validation | Implicit Dependencies | R | both-strong | defensible / defensible | material | WF (arch guided vs docs plan_only) | base-better | both-adequate | baseline | label-matters (routing) |
| 5 | multi-executable | Implicit Dependencies | Implicit Dependencies | Ghost Features | R | both-strong | defensible / partially | material | SAME | cand-better | both-adequate | candidate | label-matters (direction unsupported) |
| 6 | hidden-coupling | Implicit Dependencies | Implicit Dependencies | Vocabulary Drift | R | both-strong | partially / defensible | cosmetic | SAME | base-better | both-adequate | baseline | FP |
| 7 | strong-ui-fog | Zero Validation | Zero Validation | Implicit Dependencies | R | both-strong | defensible / partially | cosmetic | SAME (ui-diagnostic plan_only) | cand-better | both-adequate | candidate | FP |
| 8 | unusual-layout | Vocabulary Drift | Ghost Features | Vocabulary Drift | C | both-strong | partially / defensible | material | WF (arch guided vs docs guided) | base-better | both-adequate | baseline | FN (improvement may be inverted) |
| 9 | adv-unused-dep | Implicit Dependencies | Ghost Features | Implicit Dependencies | C | both-strong | partially / partially | cosmetic | SAME | cand-better | both-adequate | candidate | clean (benign improvement) |
| 10 | web-frontend | Implicit Dependencies | Contract Mismatch | Contract Mismatch | W | both-strong | defensible / defensible | material | WF (ui plan_only vs arch guided) | cand-better | both-adequate | candidate | FN + GT-ambiguous |
| 11 | generated-heavy | Contract Mismatch | Contract Mismatch | Ghost Features | R | both-strong | defensible / partially | cosmetic | WF (arch vs product; same first action) | cand-better | both-adequate | candidate | FP |
| 12 | adv-misleading-readme | Ghost Features | Ghost Features | Ghost Features | U | both-strong | defensible / defensible | material | WF (product guided vs docs guided) | cand-better | both-adequate | candidate | FN |
| 13 | docs-heavy-code-light | Ghost Features | Ghost Features | Ghost Features | U | both-strong | defensible / defensible | material | WF (docs guided vs product guided) | cand-better | both-adequate | candidate | FN |
| 14 | monorepo | Implicit Dependencies | Implicit Dependencies | Implicit Dependencies | U | both-strong | defensible / defensible | cosmetic | SAME | equal | both-adequate | none | clean |
| 15 | stale-readme | Vocabulary Drift | Vocabulary Drift | Vocabulary Drift | U | both-strong | defensible / defensible | cosmetic | SAME | equal | both-adequate | none | clean |
| 16 | tiny-lib | Zero Validation | Implicit Dependencies | Zero Validation | C | both-strong | partially / defensible | cosmetic | SAME | base-better | cand-better (labels inference) | baseline | GT-ambiguous (cosmetic improvement) |

## Per-case notes

1. **backend-service** - both labels defensible; material because the first task
   differs (candidate: configurable/validated DB path + restart-persistence test;
   baseline: test-suite first) AND the execution mode differs (baseline plan_only
   vs candidate guided_execution). The metric flags a real difference, but its
   implied direction ("candidate regressed") is unsupported - the blind agent
   preferred the candidate. Label agreement matters here.
2. **full-stack** - Ghost Features vs Contract Mismatch over the same missing-
   Dockerfile evidence; both lead to "add Dockerfiles" first. Metric regression is
   cosmetic. FP.
3. **multi-language** - Implicit Dependencies vs Ghost Features over a reachable
   TODO stub; same fixes either way. FP.
4. **poorly-documented** - both defensible; material because routing differs
   (architecture guided vs docs plan_only). Blind preferred the baseline's failing
   round-trip test but flagged the baseline's docs_fog/workflow mismatch. The
   metric flags a real difference; direction partially supported.
5. **multi-executable** - Ghost Features (documented CLI, empty cli.py) vs Implicit
   Dependencies (db contract); first task differs (CLI contract vs db work), same
   workflow. Blind preferred the candidate, so the metric's regression flag may be
   inverted. Label agreement matters; direction unknown.
6. **hidden-coupling** - Implicit Dependencies vs Vocabulary Drift over the same
   false-README evidence; same refactor either way. FP.
7. **strong-ui-fog** - Zero Validation vs Implicit Dependencies; same ui-diagnostic
   plan_only routing; blind preferred the candidate's sharper diagnosis. FP.
8. **unusual-layout** - metric counts the candidate as an IMPROVEMENT (Vocabulary
   Drift == gt), but routing differs (baseline architecture->code work vs candidate
   docs-only) and the blind agent preferred the baseline. The improvement flag may
   be inverted. FN/partial.
9. **adv-unused-dep** - metric counts improvement (Implicit Dependencies == gt);
   cosmetic; blind preferred the candidate (better label + UNKNOWN-intent caveat).
   Benign improvement.
10. **web-frontend** - both briefs chose Contract Mismatch; gt says Implicit
    Dependencies (both briefs + blind agent disagree with gt - the app cannot boot
    is more consequential than the api base URL). Metric sees "both wrong", no
    regression; but routing differs materially (ui plan_only diagnosis vs
    architecture guided repair). FN + GT-ambiguous.
11. **generated-heavy** - Contract Mismatch vs Ghost Features over fabricated
    generated-code provenance; same first action (write api.proto). Metric
    regression is cosmetic. FP (workflow ids differ but practice converges).
12. **adv-misleading-readme** - IDENTICAL labels (both Ghost Features, both match
    gt): metric sees no regression. But fog/routing differs (product guided:
    decide implement-vs-demote; docs guided: docs-only demote) -> materially
    different engineering work. Strong FN.
13. **docs-heavy-code-light** - IDENTICAL labels (both Ghost Features): metric sees
    no regression. But routing differs (docs rewrite vs product decide-then-
    implement). Strong FN.
14. **monorepo** - both correct, same work, same routing. clean.
15. **stale-readme** - both correct, same work, same routing. clean.
16. **tiny-lib** - metric counts improvement (Zero Validation == gt); cosmetic (same
    work); blind preferred the baseline (Implicit Dependencies) because the fixture
    HAS a test, so "nothing checks it" is overstated for the functionality. The
    improvement flag is cosmetic and gt is contested. GT-ambiguous.

## Identification lists

### False-positive regression candidates (metric says worse; work is the same)
full-stack (2), multi-language (3), hidden-coupling (6), strong-ui-fog (7),
generated-heavy (11) - 5 of the 8 metric regressions in this sample.

### False-negative candidates (metric sees equal/correct; work materially differs)
adv-misleading-readme (12), docs-heavy-code-light (13) - identical labels, routing
differs; web-frontend (10) - metric sees "both wrong", routing differs; unusual-
layout (8) - metric improvement possibly inverted. 4 cases.

### Frozen ground truth appears ambiguous
web-frontend (10) - gt Implicit Dependencies, both briefs + blind agent say
Contract Mismatch; tiny-lib (16) - gt Zero Validation, blind agent says Implicit
Dependencies; unusual-layout (8) - gt Vocabulary Drift, blind agent says Ghost
Features (no history supports "drift"); adv-unused-dep (9) - blind agent says
Contract Mismatch; multi-executable (5) / strong-ui-fog (7) / multi-language (3) /
full-stack (2) - blind agent leans the non-gt label. Approximately 9 of 16 cases
have some gt contestation.

### Cases where exact label agreement genuinely matters
backend-service (1) - label changes first task + execution mode; multi-executable
(5) - label changes first task; poorly-documented (4) - label links to fog/routing.
3 cases. In these the metric has real signal, though it cannot capture direction.

## Bookkeeping correction discovered during E1

The Task C/D artifacts (evidence-map-v1.md section 8, erratum, probe-design)
state "7 boundary regressions vs 3 boundary improvements" and describe the primary
packet set as "10 boundary-changed repos + 2 fog-only flips". Re-tallying from the
frozen phase15 data shows generated-heavy is ALSO a boundary regression (baseline
Contract Mismatch == gt; candidate Ghost Features != gt), making it 8 regressions /
3 improvements / 6 both-wrong / 8 both-right in the full 25-repo corpus, and 11
boundary-changed repos in this 16-packet sample (the 12-packet primary set itself
was unaffected and complete). This does not change the gate verdict, the
dispositions, or any Task D conclusion; prior Task C/D artifacts are NOT edited
(per constraint) and this correction is recorded here for the record.