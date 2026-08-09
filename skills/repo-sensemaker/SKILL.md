---
name: repo-sensemaker
description: "PROTOTYPE (prototype/repo-sensemaker-vnext branch, not canonical): owner-facing interaction layer. Investigates via repository-diagnostician, then asks at most one neutral clarifying question only if owner intent is both missing and decision-changing, then recommends. On canonical main this skill is diagnostic-only -- see the note below."
---

# repo-sensemaker (PROTOTYPE: EXPERIMENTAL interaction-layer role)

> **This file is different on `prototype/repo-sensemaker-vnext` than on
> `main`.** On `main`, `repo-sensemaker` is diagnostic-only (Stage 1
> intent-comparison + evidence-gathering + brief production, all in one
> skill). On this branch, it has been restructured to test Option A from
> [the assumption ledger](../../docs/prototypes/repo-sensemaker-vnext.md):
> `repo-sensemaker` becomes the **owner-interaction layer**; repository
> investigation is delegated to the new
> [`repository-diagnostician`](../repository-diagnostician/SKILL.md) skill.
> This is a candidate answer, not a ratified one. If this prototype is
> discarded, `main`'s version is untouched and remains authoritative.

This skill's job, in this prototype: given real (or agent-selected) owner
uncertainty, produce a useful recommendation with the least owner burden
possible, while never inventing an owner preference it doesn't have.

## EXPERIMENTAL interaction workflow

```text
recover known owner intent (conversation/prior context)
        |
        v
invoke repository-diagnostician
        |  (repository_state, known_intent)
        v
read the returned Repository Sensemaking Brief (vNext)
        |
        v
inspect analysis_vnext.owner_intent_state.status
        |
   +----+----+---------------------+
   |         |                     |
sufficient  thin              blocking_unknown
   |         |                     |
   |         v                     v
   |   inspect uncertainty.source   ask owner what's needed
   |         |                     to proceed at all (this is
   |         |                     not the "one neutral question"
   |         |                     step below -- it's a hard stop,
   |         |                     not a refinement)
   |         v
   |   repository_evidence -> re-invoke repository-diagnostician with
   |                          a narrower investigation focus (not a new
   |                          owner question)
   |   empirical            -> propose a bounded probe in the
   |                          recommendation; do not ask the owner to
   |                          approve investigation, ask them to approve
   |                          (or just run) the probe
   |   owner_intent         -> would a different answer materially change
   |                          the recommendation?
   |                             no  -> proceed, note the residual
   |                                    uncertainty as non-decision-changing
   |                             yes -> ask ONE neutral, high-information
   |                                    question (see below), then proceed
   |   external_environment -> note what would need inspecting outside
   |                          this repository; do not guess at it
   v
synthesize and recommend
```

**"One question" is a working constraint from S1, not a hard-coded rule
in this prototype.** If investigation genuinely produces two independent
decision-changing owner-intent uncertainties, that is itself a finding
worth reporting plainly rather than silently forcing both into one
question or silently dropping the second — but the default, and the only
case S1 actually tested, is one question.

## Neutral clarification (S1's one concrete finding)

S1's strongest negative learning: a clarification question that labels one
option as "what the repository evidence supports" is leading, even when
unintentional. Concretely, when constructing the question:

- Do not name a preferred option in the option labels.
- Do not use language that implies one answer is more evidenced than
  another when the uncertainty is genuinely about *owner preference*, not
  evidence — if it were an evidence question, it wouldn't have reached this
  step (`uncertainty.source` would have been `repository_evidence` or
  `empirical`, handled above without asking).
- State the decision each option leads to, not just the option's label —
  the owner is choosing a consequence, not a taxonomy term.

## Recover known intent

Before invoking `repository-diagnostician`, extract whatever the owner has
already established from the conversation or prior context (matching
canonical `repo-sensemaker`'s existing Stage 1 intent-extraction, applied
here as the interaction layer's first step rather than folded into
diagnosis). Pass this as `known_intent`. **Do not pad thin intent to look
more complete than it is** — `repository-diagnostician` needs to see
genuinely thin intent as thin, not a paraphrase that hides the gap.

## What this layer does not do

- Does not re-diagnose the repository itself. If you find yourself reading
  source files to form your own weakest-boundary opinion, you are doing
  `repository-diagnostician`'s job in the wrong skill.
- Does not ask more than one clarifying question without explicitly noting
  why the default was insufficient.
- Does not represent `analysis_vnext` fields, the two-skill split, or this
  interaction policy as settled architecture in the final output. The
  recommendation should read as a recommendation, not a proof that this
  packaging is correct.

## Boundary rules (unchanged from canonical)

1. **No implementation.** Output is a diagnostic/recommendation artifact.
2. **Registry grounding.** Any `recommended_workflow_id` must be verified
   against the real `workflow-registry.yaml`. This prototype introduces no
   new routes.

## References

- [repository-diagnostician](../repository-diagnostician/SKILL.md) — the delegated diagnostic core
- [Repository Sensemaking Brief vNext template](../repository-diagnostician/references/brief-vnext-template.md)
- [Prototype assumption ledger](../../docs/prototypes/repo-sensemaker-vnext.md)
- [Canonical Vocabulary Registry](../../docs/canonical-vocabulary.yaml) (canonical, unchanged)

## Execution protocol note

This prototype is invoked directly during evaluation (by name), not through
`workflow-runtime.py` — neither this restructured role nor
`repository-diagnostician` is registered in
`skills/workflow-planner/references/skill-registry.yaml` or any workflow.
The canonical runtime-owned-skeleton protocol (`scripts/brief_skeleton.py`,
`expected_output_path`, `scripts/run-ledger.py`) that governs real runtime
invocations is unchanged on `main` and unaffected by this branch; it simply
doesn't apply to how this prototype is being run.
