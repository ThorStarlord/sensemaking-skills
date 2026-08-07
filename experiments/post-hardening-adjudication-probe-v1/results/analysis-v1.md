# Analysis v1 - agent analysis of all 16 packets

```
schema: post-hardening-adjudication-probe-v1/analysis-v1
status: AGENT ANALYSIS ONLY - NOT human adjudication (see protocol-deviation-v1.md)
evidence_class: non-independent, known treatment identities, prior exposure to
  hardening evidence + ground truth. Blind subagent reads for per-packet merits.
usage: decide whether an independent human review is worth the cost + cheapest next
  action. Original precommitted thresholds are NOT satisfied by this run.
```

## 0. Identity mapping (sealed key, opened per deviation)

| Packet | Brief A | Brief B | Ground truth (weakness type / fog) |
|---|---|---|---|
| backend-service | baseline (Zero Validation / architecture) | candidate (Implicit Dependencies / architecture) | Zero Validation / architecture |
| full-stack | candidate (Ghost Features / architecture) | baseline (Contract Mismatch / architecture) | Contract Mismatch / architecture |
| multi-language | candidate (Implicit Dependencies / architecture) | baseline (Ghost Features / architecture) | Ghost Features / architecture |
| poorly-documented | candidate (Implicit Dependencies / architecture) | baseline (Zero Validation / docs) | Zero Validation / docs |
| multi-executable | candidate (Ghost Features / architecture) | baseline (Implicit Dependencies / architecture) | Implicit Dependencies / architecture |
| hidden-coupling | baseline (Implicit Dependencies / architecture) | candidate (Vocabulary Drift / architecture) | Implicit Dependencies / architecture |
| strong-ui-fog | baseline (Zero Validation / ui) | candidate (Implicit Dependencies / ui) | Zero Validation / ui |
| unusual-layout | baseline (Ghost Features / architecture) | candidate (Vocabulary Drift / docs) | Vocabulary Drift / architecture |
| adv-unused-dep | baseline (Ghost Features / architecture) | candidate (Implicit Dependencies / architecture) | Implicit Dependencies / architecture |
| web-frontend | baseline (Contract Mismatch / ui) | candidate (Contract Mismatch / architecture) | Implicit Dependencies / ui |
| generated-heavy | baseline (Contract Mismatch / architecture) | candidate (Ghost Features / product) | Contract Mismatch / architecture |
| adv-misleading-readme | candidate (Ghost Features / product) | baseline (Ghost Features / docs) | Ghost Features / product |
| docs-heavy-code-light | baseline (Ghost Features / docs) | candidate (Ghost Features / product) | Ghost Features / product |
| monorepo | candidate (Implicit Dependencies / architecture) | baseline (Implicit Dependencies / architecture) | Implicit Dependencies / architecture |
| stale-readme | baseline (Vocabulary Drift / docs) | candidate (Vocabulary Drift / docs) | Vocabulary Drift / docs |
| tiny-lib | baseline (Implicit Dependencies / architecture) | candidate (Zero Validation / architecture) | Zero Validation / architecture |

Boundary-regressed repos per the frozen metric (7): backend-service, full-stack,
multi-language, poorly-documented, multi-executable, hidden-coupling, strong-ui-fog.
Boundary-improved (3): tiny-lib, unusual-layout, adv-unused-dep. Fog flips (4):
web-frontend, poorly-documented, generated-heavy, unusual-layout. Fog corrections (3):
docs-heavy-code-light, adv-misleading-readme, adv-partial-impl (adv-partial-impl not in
this 16-packet sample).

## 1. Per-packet analysis (blind agent reads; identity mapping by analyst)

Legend: Q1 = blind independent weakest-boundary type; Def-A / Def-B = defensibility of
each brief's chosen type; Useful = blind preference; Mat = materiality (does the A/B
difference change engineering work).

| # | Packet | Q1 (blind) | Def-A | Def-B | Useful | Mat | Blind confidence / key ambiguity |
|---|---|---|---|---|---|---|---|
| 1 | backend-service | Implicit Deps or Zero Validation (close) | def | def | candidate | material | high / which unenforced boundary is "weakest" |
| 2 | full-stack | Ghost Features (close: Contract Mismatch) | partially | def | candidate | cosmetic | high / GF vs CM framing of missing Dockerfiles |
| 3 | multi-language | Implicit Deps (close: Ghost Features) | partially | def | candidate | cosmetic | medium / reachable TODO stub: GF or wiring gap |
| 4 | poorly-documented | Zero Validation or Implicit Deps (close) | def | def | baseline | material | high / pipeline contract vs missing checks |
| 5 | multi-executable | Ghost Features (close: Implicit Deps) | partially | def | candidate | material | high / empty CLI: documented surface or stub |
| 6 | hidden-coupling | Implicit Deps (close: Contract Mismatch) | def | partially | baseline | cosmetic | high / false README: drift vs symptom |
| 7 | strong-ui-fog | Implicit Deps (close: Ghost Features) | partially | def | candidate | cosmetic | high / unwired routes vs missing docs |
| 8 | unusual-layout | Ghost Features (close: Vocabulary Drift) | def | partially | baseline | material | medium / phantom promise vs stale docs |
| 9 | adv-unused-dep | Contract Mismatch (close: Implicit Deps) | partially | partially | candidate | cosmetic | high / declared-but-unused dep is contested |
| 10 | web-frontend | Contract Mismatch (strong) | def | def | candidate | material | high / fog axis ui vs architecture only |
| 11 | generated-heavy | Ghost Features or Contract Mismatch (close) | partially | def | candidate | cosmetic | medium / GF vs CM + arch vs product underdetermined |
| 12 | adv-misleading-readme | Ghost Features (strong) | def | def | candidate | material | high / implement-vs-demote intent unknowable |
| 13 | docs-heavy-code-light | Ghost Features | def | def | candidate | material | high / none material |
| 14 | monorepo | Implicit Deps (close: Contract Mismatch) | def | def | none | cosmetic | high / only install-resolution is derived |
| 15 | stale-readme | Vocabulary Drift | def | def | none | cosmetic | high / none material |
| 16 | tiny-lib | Implicit Deps (close: Zero Validation) | def | partially | baseline | cosmetic | medium / bare pytest failure is derived, not run |

Per-packet notes (only where the table needs context):

- backend-service (1): the blind agent preferred the candidate because it names a
  specific high-severity defect the baseline never mentions (relative DB path ->
  silent divergent state across launches) and its first step (configurable, validated DB
  path + restart-persistence test) directly removes it; the baseline's test-first plan
  omits the state contract. Both labels defensible. Material: different first commit.
- poorly-documented (4): the blind agent preferred the baseline's first step (a failing
  round-trip test that empirically surfaces the run/save newline break) but flagged that
  the baseline's docs_fog conflicts with its own Zero Validation boundary; candidate
  routes architecture-implementation, baseline routes docs-implementation.
- multi-executable (5): candidate (Ghost Features: documented CLI with no commands)
  judged more useful and material, because it routes to CLI-contract implementation
  while the baseline routes to db-contract work; ground truth (Implicit Dependencies)
  matches the baseline, and the blind agent judged the candidate's reading better
  supported.
- unusual-layout (8): baseline (Ghost Features) judged more useful and material: it
  routes to real code work (implement-or-correct the engine) while the candidate's
  Vocabulary Drift routes to a docs-only rewrite; ground truth (Vocabulary Drift)
  matches the candidate. Blind agent: "with no history, the phantom-promise reading is
  better supported; the drift reading rests on the code having changed."
- web-frontend (10): both briefs chose Contract Mismatch (module-loading boot failure);
  the divergence is fog only. The blind agent judged the candidate's architecture_fog
  correct and material: it routes to architecture-implementation-workflow (repair)
  while the baseline's ui_fog routes to a plan-only UI diagnostic. Ground truth says
  Implicit Dependencies (api base URL) - neither brief chose it.
- adv-misleading-readme (12) and docs-heavy-code-light (13): both chose Ghost Features;
  the divergence is fog (product vs docs). The blind agent judged the candidate's
  product_fog more useful and material in both: product-implementation-workflow forces
  the implement-vs-demote decision instead of pre-committing to a docs-only rewrite.
- tiny-lib (16): blind agent preferred the baseline (Implicit Dependencies: the test
  import breaks depending on invocation environment) and judged the candidate's Zero
  Validation only partially defensible ("the fixture's own test for the core function
  undercuts 'nothing checks it'"). Note: the analyst's own earlier contaminated lean
  matched the ground truth (Zero Validation); the blind agent leaned the opposite way.
  This divergence is itself the contamination illustration (see V2).

## 2. Aggregate

### 2.1 Conclusions robust even under contamination (blind-agent data)

- R1. No brief is indefensible: in all 16 packets both briefs' chosen weakness types are
  defensible or partially defensible; zero "not defensible"; no packet needed "Other".
  The seven-type taxonomy fits these fixtures; the taxonomy itself is not the failure.
- R2. In 9/16 packets the A/B difference is cosmetic (same engineering work):
  full-stack, multi-language, hidden-coupling, strong-ui-fog, adv-unused-dep,
  generated-heavy, monorepo, stale-readme, tiny-lib. In 7/16 it is material:
  backend-service, poorly-documented, multi-executable, unusual-layout, web-frontend,
  adv-misleading-readme, docs-heavy-code-light.
- R3. The material set is driven mostly by FOG routing (architecture vs docs vs product
  vs ui workflow choice), not by the weakness-type label: 5 of the 7 material packets
  (poorly-documented, unusual-layout, web-frontend, adv-misleading-readme,
  docs-heavy-code-light) diverge primarily on fog; only backend-service and
  multi-executable diverge primarily on the type label's implied first task.
- R4. Blind independent labels disagree with frozen ground truth in a substantial
  minority: clear agreement in 5 (hidden-coupling, adv-misleading-readme,
  docs-heavy-code-light, monorepo, stale-readme), clear lean-away in 8 (full-stack,
  multi-language, multi-executable, strong-ui-fog, unusual-layout, web-frontend,
  tiny-lib, adv-unused-dep), close/tie in 3 (backend-service, poorly-documented,
  generated-heavy). The web-frontend case is the sharpest: both briefs AND the blind
  agent independently identify Contract Mismatch (the app cannot boot), while ground
  truth says Implicit Dependencies (api base URL) - the ground truth label is
  questionable there.
- R5. On usefulness, the blind pass prefers the candidate in 10/16, the baseline in
  4/16 (poorly-documented, hidden-coupling, unusual-layout, tiny-lib), no material
  difference in 2/16 (monorepo, stale-readme). On the 7 boundary-regressed repos
  specifically: candidate 5 (backend-service, full-stack, multi-language,
  multi-executable, strong-ui-fog), baseline 2 (poorly-documented, hidden-coupling).
  The blind pass does NOT support "the candidate's diagnoses are worse"; it weakly
  favors the candidate. (Caveat: agent preference, not human - see V1.)
- R6. The frozen weakest_boundary_accuracy metric counted every label mismatch as a
  regression, but 9/16 packets are cosmetic (same work). The metric conflates label
  choice with decision quality. Four of the seven "boundary regressions" (full-stack,
  multi-language, hidden-coupling, strong-ui-fog) are in the cosmetic set - blind
  review found their A/B difference does not change engineering work.

### 2.2 Conclusions vulnerable to prior knowledge (analyst contamination)

- V1. The candidate's 10/16 usefulness preference is LLM preference, not maintainer
  judgment. It is a weak prior for "the candidate is more useful", not evidence. The
  original precommitted human thresholds are explicitly NOT satisfied.
- V2. tiny-lib demonstrates contamination in both directions: the blind agent leaned
  Implicit Dependencies (= baseline label); the analyst's own earlier analysis leaned
  Zero Validation (= ground truth label). Prior knowledge can manufacture agreement
  with the rubric. Discount any aggregate statement that happens to align with ground
  truth.
- V3. All identity mapping, fog interpretation, and the material/cosmetic classification
  in this report are analyst judgments over blind raw verdicts. The blind verdicts
  themselves are the reliable layer.

### 2.3 Cases differing only taxonomically (same engineering work) - 9

full-stack, multi-language, hidden-coupling, strong-ui-fog, adv-unused-dep,
generated-heavy, monorepo, stale-readme, tiny-lib. For these, the label disagreement
(and any label-match metric delta) is decision-irrelevant; only the label differs.

### 2.4 Cases with materially different engineering work - 7

| Packet | Baseline path | Candidate path | Who routes "better" per blind agent |
|---|---|---|---|
| backend-service | test suite first | DB-path/state fix first | candidate |
| poorly-documented | docs-implementation (failing round-trip test) | architecture-implementation | baseline (first step) |
| multi-executable | db-contract/ownership work | CLI-contract implementation | candidate |
| unusual-layout | architecture: implement-or-correct engine | docs-only rewrite | baseline |
| web-frontend | ui-diagnostic plan_only (no repair) | architecture: repair boot | candidate |
| adv-misleading-readme | docs-only demote | product: decide implement-vs-demote | candidate |
| docs-heavy-code-light | docs rewrite | product: decide-then-implement | candidate |

4 of these 7 are also the frozen metric's regressions/flips (backend-service,
poorly-documented, multi-executable, unusual-layout, plus web-frontend as fog flip).
These are exactly the packets where a human adjudicator's routing judgment matters.

### 2.5 What remains unresolved without an independent reviewer

1. Whether the candidate's label/usefulness edge holds for real maintainers (LLM
   preference is not human preference; routing quality and actionability are human
   judgments).
2. The 7 material packets: which fog routing is correct. Both fog choices are
   "defensible" in most, but they send engineers to different workflows. This is a
   human decision (the fog label decides what work happens next).
3. Whether ground truth should be revised: blind agents disagreed with it in a
   substantial minority, and the experiment's own records already flag several
   contested labels (tiny-lib, cli-app, plugin-architecture) and the classification-tool
   erratum. Ground truth is not a settled arbiter.
4. The original probe question ("is the boundary regression real degradation or rubric
   disagreement?") in its precommitted, human-threshold form: NOT answered by this run.

## 3. Recommendation (cheapest next action)

1. An independent human review IS still worth the cost, but only over a reduced set:
   the 7 material packets (backend-service, poorly-documented, multi-executable,
   unusual-layout, web-frontend, adv-misleading-readme, docs-heavy-code-light) plus the
   remaining fog flip generated-heavy and the strong-ui-fog type divergence = 9 packets,
   ~1-2 h of reviewer time instead of 3-5 h. The 9 cosmetic packets add no
   decision-relevant information (taxonomic only); adjudicating them would not change
   the next action. A fresh sealed key should be generated for a human run.
2. If no independent reviewer is available, the evidence already justifies treating
   weakest_boundary_accuracy as conflated (it cannot distinguish guidance quality from
   label choice at n=25: cosmetic-vs-material mix, blind preference for the candidate,
   swing band 0.44-0.64 overlapping baseline). That makes evaluation redesign (path E:
   adjudicated/claim-level labels, or fog-routing as the measured output instead of
   weakness-type label-match) the cheapest defensible next workstream regardless of the
   regression question - because the current metric cannot answer it.
3. Do NOT treat this run as authorizing salvage (B) or any implementation: the
   candidate's usefulness edge is agent-level only and the original thresholds were not
   met. Any successor workstream still requires its own charter and authorization.
4. No repo-sensemaker skill, validator, runtime, workflow, scorer, or corpus was
   modified by this run.