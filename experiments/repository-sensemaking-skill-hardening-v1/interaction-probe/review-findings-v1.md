# Interaction probe — review findings v1

Reviewed as a user: the five frozen baseline briefs (tiny-lib, backend-service,
strong-ui-fog, hidden-coupling, adv-misleading-readme) against the 5A.2 questions.

## Per-question verdict

| # | Question | Verdict | Evidence |
|---|----------|---------|----------|
| 1 | Quickly explain what the repository does? | YES (mostly) | Section 1 of all five briefs states purpose in 2-5 sentences with citations. strong-ui-fog's goal paragraph is long (7 sentences) but accurate. |
| 2 | Identify the most important thing to understand? | PARTIAL | All five identify the weak boundary, but it arrives in Section 6 (line ~110-160 of 150-260). A user must read ~60% of a long document to reach the punchline. |
| 3 | Distinguish fact from inference? | YES | Evidence excerpts are verbatim-quoted with file/line; Section 7 grounds each claim. Inference is usually flagged ("appears", "no proof of"). |
| 4 | Expose contradictions? | YES | hidden-coupling (README says independent, code couples via global STATE), adv-misleading-readme (README advertises sync/export/webhooks, code only ingests), strong-ui-fog (router registered nowhere). |
| 5 | Identify a useful weak boundary? | YES | All five select a defensible boundary with a Logic trace (e.g., backend-service: unvalidated body into SQLite; hidden-coupling: implicit init-order dependency). |
| 6 | Does the boundary actually matter? | YES for 4/5 | tiny-lib's "Implicit Dependencies" (missing build-system/pythonpath) matters for a library; backend-service's Zero Validation matters; strong-ui-fog's Zero Validation is real but the deeper issue is "app cannot render at all"; hidden-coupling's implicit dependency matters. Debated: adv-misleading-readme boundary (Ghost Features) is right but classified docs_fog when product_fog fits better. |
| 7 | Explain alternatives? | NO | No brief has an explicit "alternatives considered" section. Candidate steps exist but competing interpretations are not articulated. |
| 8 | Communicate uncertainty? | PARTIAL | escalation_recommended + diagnosis_conflict flags exist; prose sometimes hedges. No explicit confidence number/level for the boundary or recommendation. |
| 9 | Recommended next step useful? | YES | Section 14 ready-to-copy prompt is concrete and actionable in all five (e.g., backend-service: "add validation + tests; do not alter the API"). |
| 10 | Fog terminology helping or distracting? | DISTRACTING for users | "architecture_fog/docs_fog/product_fog" is internal vocabulary. For adv-misleading-readme the docs-vs-product debate consumes the classification; a user cares that "the README promises features that don't exist", not the fog label. Terminology should stay in the machine handoff, not the user-facing summary. |
| 11 | 13/14-section structure helping or ceremony? | CEREMONY for users, VALUE for machines | The structure guarantees validator-able handoff (Section 13) and grounded evidence (Section 7/8). For a human, file-by-file inventories (Section 2) dominate the length without adding insight. |
| 12 | Too long? | YES | 143-258 lines. A user summary of 15-30 lines would carry the same message. |
| 13 | Important info buried? | YES | The weakest boundary (Section 6), fog classification (6.5), evidence (7-8) and recommendation (14) are spread across the document. The single most useful fact - "the app cannot render because no route is registered" - is in Section 2 of strong-ui-fog, not the top. |
| 14 | Actionable by a coding agent without another round? | YES | Section 13 handoff + Section 14 prompt are machine-usable; workflow IDs are registry-valid; evidence excerpts are grounded. |

## Headline findings

1. **The machine brief is good; the human experience is not.** The 14-section
   artifact is a strong machine contract (validated 25/25, grounded evidence,
   valid routing). As a user-facing response it is too long, buries the
   punchline, uses internal vocabulary, and never states confidence or
   alternatives explicitly.
2. **Punchline placement**: purpose (S1) -> inventory (S2) -> boundary (S6) ->
   evidence (S7-8) -> recommendation (S14). A user wants: purpose -> how it
   works -> the one important weakness + why -> what to do next.
3. **No confidence statement.** escalation flags are boolean; nothing states
   "confidence: high/medium/low" for the boundary choice or the recommendation.
4. **No alternatives section.** Competing interpretations exist (e.g.,
   adv-misleading-readme: docs stale vs product broken) but are never
   articulated; the plan's 8.3 "Alternatives considered" is absent from the
   template.
5. **Fog vocabulary should be machine-only.** It carries real routing value
   (workflow choice) but zero user value; it must never be the headline of a
   user-facing summary.

## Recommendation (5A.4)

Keep the current brief as the **machine artifact** (it satisfies the
validator, the handoff, and downstream routing). Add a compact **human
synthesis** as the user-facing layer:

```text
human synthesis (~15-30 lines):
  What this repository is
  How it actually works (3-6 sentences, flow not inventory)
  The most important weakness + why it matters
  Evidence basis (2-4 citations)
  Alternatives considered (1-3, when material)
  Confidence (high/medium/low + what would raise it)
  Recommended next step (concrete, actionable)
  Ask before consequential action
```

The synthesis is a derivative of the machine brief (same evidence, same
boundary, same routing), never a second diagnosis. See
ideal-response-examples/ for the five prototypes.
