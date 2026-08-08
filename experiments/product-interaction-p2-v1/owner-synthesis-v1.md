# Task P2 — Owner Synthesis v1

experiment_type: product_interaction
record: owner-synthesis-v1
recorded_at: 2026-08-08 (after the single repo-sensemaker interaction)
status: presented to owner for lightweight POST judgment

---

## Recommended action

**Do not make the standalone repo-sensemaker validation failure the next
engineering task. There is higher-value product work first.**

The failure is real and still current, but "fix the validator" is the wrong
framing: the validator is correct (the canonical fixture passes; the runtime
path passes by design). The defect is that the skill's own instructions are
mode-blind — the template tells standalone producers to write placeholder
quotes that only a runtime can overwrite. Recommended sequence:

1. This P2 run's own PHASE 5 validation serves as the one-shot reproduction
   at the current SHA (cheapest credible probe).
2. Then prioritize product/interaction work — the owner-facing synthesis
   step P1 already identified as missing — and decide separately on
   publishing 0.2.2 (the distribution repair currently reaches no user;
   PyPI still serves the broken 0.2.1).
3. Bundle a small, testable hygiene fix into that work: mode-aware quote
   guidance in the template, make `sensemaking-skills validate` honest
   (today it is a stub that prints instructions), optionally reuse
   `evidence_quote_extractor.py` as a standalone reconcile step.

## Strongest supporting evidence

- The validator is not the defect: `tests/fixtures/repo-sensemaker-template-canonical.md`
  passes `validate-brief.py` cleanly (verified this run), and issue #89 was
  closed via the runtime reconciliation design (`brief_skeleton.reconcile` +
  `evidence_quote_extractor`), which runs only in the runtime path.
- The contradiction ships: the template's placeholder instruction
  (`repo-analysis-template.md` L75-L82) is unconditioned on mode, and the
  0.2.2 wheel ships those skill files byte-identical.
- Impact is bounded today: PyPI has no working release (0.2.1 broken, 0.2.2
  unpublished), so there are no external users; the failure does not block
  the machine handoff (Section 13 routing fields are consumed by
  workflow-planner independently of excerpt quotes); and P1's decision value
  survived the same failure.

## Strongest credible alternative

Make the standalone validation failure the next engineering task — framed
correctly as mode-aware guidance + CLI-honesty repair rather than validator
repair. This is defensible because every future agent-native run (P2, P3,
and the owner's own probes) will hit the red gate until it is fixed, and the
fix is small. It loses only because the owner's own post-P1 plan puts
interaction work next and the failure has not been shown to block any real
decision value.

## Most important remaining uncertainty

Whether the red gate actually degrades the owner's (or any future user's)
decisions in practice — P1 suggests it does not (decision value survived),
but that is one observation. Also unresolved: whether 0.2.2 publication is
imminent, which would turn "no external users" into "external users hitting
the shipped contradiction".

## Cheapest credible next action

The PHASE 5 one-shot standalone validation of this run. If it reproduces the
failure at the current SHA (expected), the boundary is confirmed current and
the small mode-aware guidance fix is validated as the minimal credible
engineering item — to be bundled, not made into a standalone task.

## Confidence and why it is bounded

Medium-high. High on the mechanism (template/validator/runtime wiring is
directly evidenced at the frozen SHA); medium on the sequencing because the
impact ranking ("product work beats validator repair") rests on the owner's
own documented P1 plan and on one observation that the failure does not
block decision value. The recommendation would flip if the owner judges the
red gate to be blocking their upcoming product probes.
