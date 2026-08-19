# Path 01b Synthetic Coherence Suite — Evaluator Map

**Status:** reconciled evaluator metadata / single-context consistency interpretation  
**Tracker:** Issue #204  
**Scenario inputs:** `docs/research/path-01b-synthetic-scenarios.md`  
**Canonical protocol:** `main@96e01abd9dfb4c0303b6462a1acd5579d92770a0`  
**Frozen scenario-input blob:** `48ce762d5e81fc9f06c4927c2c6258828c80797e`

## Evidence interpretation

This evaluator map is used in an **evaluator-aware, single-context synthetic coherence exercise**. The evaluating coding-agent context may know this map, transformation relationships, prior answers, and the canonical qualitative rubric.

Therefore paired scenarios are **internal consistency checks only**. Agreement across a swap, paraphrase, or decoy variant does not establish blind invariance, framing robustness, absence of salience bias, independent replication, or cross-agent reproducibility.

The frozen scenario-input file must remain unchanged during this cycle unless a separately recorded input correction is required before evaluation continues.

## Frozen evaluator relationships

| Scenario | Relationship / control | Coherence property |
|---|---|---|
| `SCLU-001` | base | evidence economy conflicts with wrong-action exposure; reasoning should acknowledge both without pseudo-scoring |
| `SCLU-002` | base | dependency proximity conflicts with authority effect; authority remains a genuine possible blocker |
| `SCLU-003` | base | option preservation conflicts with larger decision branching |
| `SCLU-004` | balanced ambiguity control | evidence intentionally does not warrant false certainty; ambiguity should remain visible |
| `SCLU-005` | resolve-both / metareasoning-cost control | reasoning should notice when strict ordering costs as much as immediately gathering both cheap evidence items |
| `SCLU-006` | `act_now` control | neither uncertainty gates the cheap reversible correction; `act now / investigate neither` must remain available |
| `SCLU-007` | information-gain trap | broad information quantity must not substitute for finding-specific decision effect |
| `SCLU-008` | irreversibility control | cheap release provenance sits immediately before an externally irreversible publication boundary |
| `SCLU-009` | A/B label swap of `SCLU-001` | reasoning should translate consistently when A/B labels exchange |
| `SCLU-010` | paraphrase of `SCLU-002` | explanation should remain compatible with the same dependency/authority facts |
| `SCLU-011` | irrelevant-decoy variant of `SCLU-003` | known non-gating metric-naming uncertainty should remain non-gating |
| `SCLU-012` | paraphrase of `SCLU-007` | decision-value discipline should remain compatible with the base information-gain case |

## Pair consistency checks

### P1 — `SCLU-001` / `SCLU-009`

- transformation: same substantive scenario with A/B candidate labels exchanged;
- coherence check: the written rationale should translate to the exchanged labels, or both analyses should preserve the same genuine ambiguity;
- contradiction signal: materially incompatible reasoning that cannot be explained by any changed decision-relevant fact;
- prohibited inference: success does **not** prove absence of label or position bias.

### P2 — `SCLU-002` / `SCLU-010`

- transformation: semantic paraphrase with decision-relevant facts preserved;
- coherence check: responsibility/authority reasoning should be mutually compatible;
- contradiction signal: materially incompatible dependency or authority interpretation with no factual basis;
- prohibited inference: success does **not** prove framing robustness.

### P3 — `SCLU-003` / `SCLU-011`

- transformation: addition of a genuine but decision-irrelevant metric-naming question;
- coherence check: the added question should be identified as non-gating and should not require changing the A/B warrant relation;
- contradiction signal: treating the known non-gating decoy as a decision dependency;
- prohibited inference: success does **not** prove blind resistance to salience.

### P4 — `SCLU-007` / `SCLU-012`

- transformation: semantic paraphrase of the information-gain trap;
- coherence check: finding-specific decision effect should remain central despite the broader information opportunity;
- contradiction signal: generic information quantity becomes the decisive reason without a changed decision dependency;
- prohibited inference: success does **not** prove paraphrase invariance.

## Cross-suite evaluation signals

Record for every worked scenario:

- top-level selection: `A first`, `B first`, or `act now / investigate neither`;
- whether each supplied uncertainty is live or non-gating for the contemplated consequential decision;
- qualitative reasoning using dependency proximity, decision branching, alternative plausibility, wrong-action exposure, evidence economy, option preservation, and authority effect as prompts rather than scores;
- first evidence-producing responsibility;
- expected decision effect;
- plausible competing selection;
- whether genuine ambiguity remains;
- whether a numeric score, weight, pseudo-point system, covert arithmetic, or aggregate ranking appears;
- internal consistency with any paired transformed scenario;
- any contradiction, investigation compulsion, information-gain substitution, false precision, or excessive metareasoning signal.

## Bounded dispositions

The synthesis must conclude exactly one of:

- `SYNTHETICALLY_COHERENT`
- `SYNTHETICALLY_LIMITED`
- `SYNTHETICALLY_INCOHERENT`

`SYNTHETICALLY_COHERENT` means only that the qualitative Path 01b procedure remained internally coherent and auditable across this evaluator-aware worked suite. It is not evidence of independent robustness or empirical effectiveness in ordinary engineering work.

The final synthesis must explicitly state:

> **This was an evaluator-aware, single-context synthetic coherence exercise. Independent execution, framing robustness, reproducibility across coding agents, real-world prevalence, and real-world effectiveness were not tested.**

No result from this map or suite alone warrants numeric scoring, ranking machinery, a schema, a new Skill, automatic routing, workflow/runtime changes, a WarrantEngine, or EXP-0006.