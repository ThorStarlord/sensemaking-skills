# Delta matrix v1 - routing/action deltas vs Task-D materiality

```
schema: evaluation-design-e2-v1/delta-matrix-v1
basis: mechanical extraction from the 16 frozen packet pairs:
  recommended_workflow_id + recommended_execution_mode (Section 13 handoff),
  first engineering action (Section 11 recommended next step).
Task-D material/cosmetic column is blind-subagent judgment, NON-HUMAN evidence.
```

## First-action categories (normalized; fixed set)

BOOT-FIX (make the thing run: entry point / module loading / launch path),
CONTRACT-IMPLEMENT (define or implement a documented contract/feature/schema),
CONTRACT-DOC (write the contract/spec definition),
DECIDE (owner-intent decision gate first),
STATE-FIX (data/state/DB contract fix),
DEP-FIX (dependency removal/declaration),
PACKAGING (manifest/build-system completion),
TESTS (add tests/CI/smoke check),
DIAGNOSTIC (analysis/inventory pass, no implementation),
DOCS (documentation correction).

Normalization judgment calls (recorded, not hidden):
- multi-language: brief A = CONTRACT-DOC, brief B = CONTRACT-IMPLEMENT (stub). Both
  resolve the same helper contract; Task-D judged cosmetic; counted same-cluster.
- strong-ui-fog: brief A = TESTS (smoke test), brief B = DIAGNOSTIC (UI inventory).
  First step differs but converges on the same action set (wiring + smoke test +
  docs); Task-D judged cosmetic; counted same-cluster (see assessment caveat).

## Matrix

Legend: routing = routing_delta; action = action_delta; decision = decision_delta;
T-D mat = Task-D materiality (NON-HUMAN); label = weakness labels same/different;
metric = weakest_boundary_accuracy verdict (R regressed / C improved / U unchanged-
correct / W both-wrong).

| # | packet | A wf/mode | B wf/mode | routing | A first action | B first action | action | decision | T-D mat | label | metric | class |
|---|--------|-----------|-----------|---------|----------------|----------------|--------|----------|---------|-------|--------|-------|
| 1 | backend-service | arch / plan_only | arch / guided | 1 (MODE) | TESTS | STATE-FIX | 1 | 1 | material | diff | R | caught |
| 2 | full-stack | arch / guided | arch / guided | 0 | BOOT-FIX | BOOT-FIX | 0 | 0 | cosmetic | diff | R | clean |
| 3 | multi-language | arch / guided | arch / guided | 0 | CONTRACT-DOC | CONTRACT-IMPLEMENT | 0 | 0 | cosmetic | diff | R | clean (judgment) |
| 4 | poorly-documented | arch / guided | docs / plan_only | 1 (WF) | CONTRACT-DOC | TESTS | 1 | 1 | material | diff | R | caught |
| 5 | multi-executable | arch / guided | arch / guided | 0 | CONTRACT-IMPLEMENT | STATE-FIX | 1 | 1 | material | diff | R | caught (action only) |
| 6 | hidden-coupling | arch / guided | arch / guided | 0 | STATE-FIX | STATE-FIX | 0 | 0 | cosmetic | diff | R | clean |
| 7 | strong-ui-fog | ui-diag / plan_only | ui-diag / plan_only | 0 | TESTS | DIAGNOSTIC | 0 | 0 | cosmetic | diff | R | clean (judgment) |
| 8 | unusual-layout | arch / guided | docs / guided | 1 (WF) | CONTRACT-IMPLEMENT | DOCS | 1 | 1 | material | diff | C | caught |
| 9 | adv-unused-dep | arch / guided | arch / guided | 0 | DEP-FIX | DEP-FIX | 0 | 0 | cosmetic | diff | C | clean |
| 10 | web-frontend | ui-diag / plan_only | arch / guided | 1 (WF+MODE) | BOOT-FIX | BOOT-FIX | 0 | 1 | material | same | W | caught (routing only) |
| 11 | generated-heavy | arch / guided | product / guided | 1 (WF) | CONTRACT-IMPLEMENT | CONTRACT-IMPLEMENT | 0 | 1 | cosmetic | diff | R | flagged-cosmetic |
| 12 | adv-misleading-readme | product / guided | docs / guided | 1 (WF) | DECIDE | DOCS | 1 | 1 | material | same | U | caught |
| 13 | docs-heavy-code-light | docs / guided | product / guided | 1 (WF) | DOCS | DECIDE | 1 | 1 | material | same | U | caught |
| 14 | monorepo | arch / guided | arch / guided | 0 | PACKAGING | PACKAGING | 0 | 0 | cosmetic | same | U | clean |
| 15 | stale-readme | docs / guided | docs / guided | 0 | DOCS | DOCS | 0 | 0 | cosmetic | same | U | clean |
| 16 | tiny-lib | arch / guided | arch / guided | 0 | PACKAGING | PACKAGING | 0 | 0 | cosmetic | diff | C | clean |

## Per-case notes

1. backend-service - routing differs only in MODE (plan_only vs guided_execution);
   actions differ (test suite vs DB-path fix). Both deltas fire; Task-D material.
5. multi-executable - routing identical; caught ONLY via action_delta (CLI contract
   vs db contract). Shows action_delta is not redundant with routing_delta.
8. unusual-layout - the metric counts an IMPROVEMENT here while decision_delta=1
   (code work vs docs-only): the metric's improvement flag sits on a consequential
   disagreement.
10. web-frontend - first action IDENTICAL in both briefs (add type="module"); caught
   only via routing_delta (ui plan_only vs arch guided). Shows routing_delta is not
   redundant with action_delta. The "material" reading is the mode/workflow, not
   the action.
11. generated-heavy - the single unnecessary flag: workflow ids differ (arch vs
   product) but the first action is identical (author api.proto) and Task-D judged
   cosmetic. Refinement candidate: a workflow-id-only delta with matching first
   action should not fire.
12/13. adv-misleading-readme, docs-heavy-code-light - identical weakness labels
   (both Ghost Features, both match gt; metric U) yet decision_delta=1: the
   metric's false-negative class is exactly what decision_delta catches.
16. tiny-lib - metric counts improvement; decision_delta=0 (cosmetic): the
   metric's improvement flag is on a harmless label change.