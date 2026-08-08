# Task P1 — Learning Record (PRE vs POST comparison)

experiment_type: product_interaction
record: learning-v1
recorded_at: 2026-08-07
status: COMPLETE — interaction preserved, no implementation, no repo-sensemaker change

---

## What ran

- Repository investigated: `sensemaking-skills` at `origin/main` @
  `b58038984f54fa13305aa951a7cbb6767e7ddcc9` (experiment branch
  `experiments/product-interaction-p1-v1`, created from `origin/main` after
  the hardening-branch correction).
- Product under test: canonical in-repo `skills/repo-sensemaker/SKILL.md`
  (164-line variant, standalone agent-native invocation, exactly once).
- User question: "Understand this repository and tell me what engineering work
  would create the most value next."
- Artifacts: `charter-v1.md`, `owner-pre-v1.md`,
  `repo-sensemaker-investigation-v1.md`, `owner-synthesis-v1.md`,
  `owner-post-v1.md`, `validation-result-v1.json` (raw validator output).

## Observed product behavior (ordinary invocation)

- The skill produced a full 14-section Repository Sensemaking Brief with
  evidence excerpts and a machine handoff.
- The brief **failed its own standalone validation** (3 blocking
  `EVIDENCE_QUOTE_NOT_FOUND` on the multiline excerpts; single-line quotes
  grounded fine). Root cause is provisional: the canonical template's Section
  8 guidance ("write a placeholder quote; the runtime overwrites it", issue
  #89) assumes runtime invocation — under standalone invocation (the
  documented GETTING_STARTED path) placeholders/transcription cannot satisfy
  the validator's verbatim grounding. The owner flagged this as a product
  concern and kept the root cause provisional.
- Per protocol: no repair, no rerun, no ensemble — the failure is preserved as
  observed (`validation-result-v1.json`).

## PRE -> POST comparison

| Possible effect | Did it happen? | Evidence |
|---|---|---|
| Action changed | PARTIAL — direction (product/interaction) retained, but the concrete next action changed from "improve the interaction" to "run the clean-env install reproduction first, then fix distribution if confirmed" | owner-post: intended next action |
| Sequence changed | YES — a distribution/execution prerequisite now precedes interaction work | owner-post: "verify distribution defect → fix execution/distribution if confirmed → then return to owner-facing interaction work" |
| Scope narrowed | YES — from a broad product-improvement direction to a concrete, testable next decision (clean-env reproduction) | owner-post: "narrowed the problem ... to a concrete, testable next decision" |
| Confidence increased (evidence-backed) | YES — Medium -> Medium-high, because the mechanism of the drift was surfaced, not because of persuasion | owner-post: confidence section |
| Confidence decreased appropriately | No | — |
| Alternative surfaced | YES — the execution-surface-fix as a material alternative to direct interaction work; "do nothing" seriously considered and rejected with reasoning | owner-synthesis alternatives; owner-post why |
| Evidence need surfaced | YES — the owner now knows the decisive next probe: clean-env `pip install` + `setup-skills` reproduction | owner-post: "the decisive clean-environment reproduction has not been run" |
| Work avoided | YES — owner explicitly says it prevented prematurely starting an interaction redesign before users can receive the canonical skill | owner-post: "prevented me from prematurely starting an interaction redesign" |
| Nothing useful happened | No | — |

## What the owner reported repo-sensemaker surfaced that was missed

The drift itself was known before PRE. What was NEW: the apparent **mechanism
and consequence** — wheel packaging omits skill trees, setup-skills depends on
a source-checkout layout, the documented install path may fail to deliver the
canonical skill, stale copies persist, and the standalone validation path has
its own usability gap. This changed the issue from "a stale local copy" into a
plausible product-distribution problem blocking future improvements.

## Verdict on the interaction

**Useful enough to repeat: YES.** The probe passed the product test: the
owner's decision after the interaction is better informed than before it
(sequencing sharpened, scope narrowed, confidence raised for evidence-backed
reasons, an evidence need was identified, premature work was avoided). This
occurred even though the underlying brief failed its own validator — i.e., the
decision-sharpening value came from the investigation substance, not from a
validated artifact.

## What this single interaction teaches about the desired product

1. The owner-facing synthesis format worked: five questions (recommended work,
   strongest evidence, alternatives incl. do nothing, uncertainty,
   decision-changing evidence) produced a decision change in one interaction.
2. The product's machine artifact is NOT the owner-facing surface: the
   14-section brief needed translation into the compact synthesis; the skill
   itself has no such step. This is a real interaction gap (as the owner
   suspected), but it is secondary to the execution-surface problem.
3. The standalone validation failure is a genuine usability defect in the
   product as documented (GETTING_STARTED recommends exactly the standalone
   path). Its root cause (runtime-only quote-overwrite assumption in the
   template, issue #89) needs isolation before it can be fixed.
4. Distribution/execution surface is a precondition for any interaction
   improvement to have value — confirmed by both the wheel/path evidence and
   this run's own encounter with the stale installed copy.

## Non-authorizations (explicit)

- No implementation of the recommended distribution fix.
- No repo-sensemaker modification.
- No salvage/merge of the hardening branch.
- No change to the evaluation system.
- No P2 designed or run. Whether a P2 (e.g. clean-env reproduction, or a
  second real interaction after the distribution fix) is justified is a
  separate decision for the owner.

## Stop condition reached

Learning record complete. STOP per charter — nothing further is implemented or
changed in this task.
