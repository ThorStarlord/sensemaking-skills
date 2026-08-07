# Task P1 — Owner disposition (additive record; does not rewrite any observed evidence)

```
schema: product-interaction-p1-v1/disposition-v1
status: DISPOSITION RECORDED - evidence package only. No push, no PR, no
  implementation, no repo-sensemaker change. Publication of P1 and
  authorization of the reproduction probe are separate explicit decisions.
```

## Task P1 result

**"Useful interaction with a serious execution-surface defect"** — not simply
"P1 passed."

Both conclusions are preserved together:

> Task P1 result: the interaction materially sharpened the owner's engineering
> decision, despite the canonical standalone execution path failing validation.
> The next priority remains provisional until the clean-install distribution
> hypothesis is reproduced.

## Decision sharpening (PRE -> POST, as observed)

```
PRE
broad product/interaction improvement
        ↓
P1 investigation
        ↓
POST
verify one specific distribution hypothesis first
```

Genuine decision sharpening: scope narrowed, sequencing changed, confidence
changed for evidence-backed reasons, and premature implementation was avoided.

## Corrected framing of the investigation claim

The agent's brief stated: "The weakest boundary is the execution/distribution
surface."

Owner-corrected claim (keeps the POST faithful to the evidence):

> **The execution/distribution surface is now the leading candidate for the
> highest-value next engineering work, conditional on clean-environment
> reproduction.**

The investigation strongly suggests the defect, but the synthesis itself
identified the clean-environment test as the decision-changing observation.

## Next two explicit decisions (not taken here)

1. **Publication of P1** — whether/when to push the branch or open a PR.
2. **Authorization of the minimal clean-environment reproduction probe** with
   the single question:

   > Does a fresh user following the documented install/setup path receive and
   > invoke the current canonical `repo-sensemaker`?

   Probe shape: fresh environment -> install the actual distributable package
   -> run the documented `setup-skills` path -> inspect what skill gets
   installed/invoked. No new evaluation framework, no corpus, no scorer, no
   skill modification while testing.

   Decision fork:
   - **confirmed distribution defect** -> authorize focused distribution
     repair;
   - **not reproduced** -> deprioritize distribution, return to
     product/interaction learning.

## Non-authorizations (explicit)

- No push of P1 in this task.
- No P2 interaction run.
- No packaging fix, skill fix, or validator fix.
- No hardening-branch salvage/merge.
- No change to the evaluation system.

## Conceptual takeaway (owner)

The thing P1 was testing was not "can repo-sensemaker generate a valid
artifact?" It was "can it help an owner decide what to do?" On this one real
decision, yes — it appears to have done that, while simultaneously exposing a
concrete defect in how the product reaches users. That is exactly the kind of
product learning the earlier evaluation chain was missing.
