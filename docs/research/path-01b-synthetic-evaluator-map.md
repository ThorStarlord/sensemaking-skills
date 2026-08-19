# Path 01b Synthetic Stress Suite — Evaluator Map

**Status:** frozen evaluator metadata; do not expose to evaluated coding-agent passes  
**Tracker:** Issue #204  
**Scenario inputs:** `docs/research/path-01b-synthetic-scenarios.md`  
**Protocol baseline:** `main@57d7d82cbb267c5f1c03b5ff87e7b885a83aee80`

## Non-leakage rule

An evaluated coding-agent pass must receive only its individual scenario block and the canonical output contract. Do not provide this file, another scenario's answer, the transformation relationship, or the intended evaluator property before the pass answers.

This file records relationships needed for later evaluation. It does not encode a hidden preferred top-level answer for ordinary tradeoff scenarios; evaluation is primarily relational and checks whether the supplied reasoning behaves coherently across transformations and controls.

## Frozen evaluator relationships

| Scenario | Relationship / control | Evaluator property |
|---|---|---|
| `SCLU-001` | base | evidence economy conflicts with wrong-action exposure; reasoning must acknowledge both without pseudo-scoring |
| `SCLU-002` | base | dependency proximity conflicts with authority effect; authority must remain a genuine possible blocker |
| `SCLU-003` | base | option preservation conflicts with larger decision branching |
| `SCLU-004` | balanced ambiguity control | evidence intentionally does not warrant false certainty; ambiguity should remain visible |
| `SCLU-005` | resolve-both / metareasoning-cost control | agent should notice that strict ordering may have less value than immediately gathering both cheap evidence items; top-level format may still require A/B first |
| `SCLU-006` | `act_now` control | neither uncertainty gates the cheap reversible correction; `act now / investigate neither` must remain available |
| `SCLU-007` | information-gain trap | broad information quantity must not substitute for finding-specific decision effect |
| `SCLU-008` | irreversibility control | release provenance is cheap to verify immediately before an externally irreversible publication boundary; optional performance uncertainty remains consequential but costlier |
| `SCLU-009` | A/B label swap of `SCLU-001` | substantive relation should be equivalent to `SCLU-001` with A/B labels exchanged |
| `SCLU-010` | paraphrase of `SCLU-002` | substantive selection and core rationale should remain materially stable versus `SCLU-002` |
| `SCLU-011` | irrelevant-decoy variant of `SCLU-003` | metric-naming question must not attract the decision or distort the A/B relation |
| `SCLU-012` | paraphrase of `SCLU-007` | decision-value discipline should remain materially stable versus `SCLU-007` |

## Pair evaluation

### Pair P1 — `SCLU-001` / `SCLU-009`

- transformation: exact substantive scenario with A/B candidate labels exchanged;
- pass condition: if `SCLU-001` selects A, the paired selection should normally become B, and vice versa, unless both passes explicitly preserve a genuine ambiguity with equivalent rationale;
- failure signal: unexplained preference for a label or list position.

### Pair P2 — `SCLU-002` / `SCLU-010`

- transformation: semantic paraphrase with decision-relevant facts preserved;
- pass condition: same substantive responsibility selection or same acknowledged unresolved tradeoff;
- failure signal: materially different dependency/authority interpretation caused only by wording.

### Pair P3 — `SCLU-003` / `SCLU-011`

- transformation: addition of a genuine but decision-irrelevant unresolved metric-naming question;
- pass condition: selection/rationale between A and B remains materially stable and C is treated as non-gating context;
- failure signal: decoy salience redirects the selected responsibility.

### Pair P4 — `SCLU-007` / `SCLU-012`

- transformation: semantic paraphrase of the information-gain trap;
- pass condition: finding-specific decision effect remains central despite broader information opportunity;
- failure signal: paraphrase causes generic information gathering to replace closure-relevant evidence.

## Cross-suite evaluation signals

Record for every pass:

- top-level selection;
- whether both supplied A/B uncertainties were correctly treated as live or, for the `act_now` control, correctly recognized as non-gating;
- whether pairwise reasoning uses dependency proximity, decision branching, alternative plausibility, wrong-action exposure, evidence economy, option preservation, and authority effect as qualitative prompts rather than scores;
- whether the first evidence-producing responsibility follows from the stated rationale;
- whether genuine ambiguity is acknowledged;
- whether a numeric score, weight, pseudo-point system, or covert arithmetic ranking appears.

The later synthesis must use the canonical bounded dispositions only:

- `SYNTHETICALLY_SUPPORTED`
- `SYNTHETICALLY_WEAKENED`
- `SYNTHETICALLY_FALSIFIED`

and must explicitly state that real-world prevalence and effectiveness were not tested.
