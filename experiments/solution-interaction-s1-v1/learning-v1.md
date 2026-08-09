# S1 — Learning record (investigation-first, clarify-if-needed)

record: learning-v1
experiment_type: solution_interaction
target: sensemaking-skills @ 27aa2442e5395f8793023882d5ed5e94861755e4
owner_question (agent-selected, frozen): "Should the next engineering work focus
on interaction design or on standalone-contract cleanup (the four infrastructure gaps)?"
owner answers: Q1 Clearly useful | Q2 Narrowed/sequenced my action | Q3
done-but-mis-wired discovery (+ critique: clarification options were somewhat
leading) | Q4 Very low burden / high value | Q5 Necessary and high-value, but
somewhat leading presentation | Q6 Well grounded and intent-preserving |
Q7 Maybe — with neutral clarification wording

## S1 disposition

**PROMISING** — with one specific refinement required before construction:
the clarification question must be presented neutrally, without embedding the
agent's preferred recommendation in the option labels.

## Disposition vocabulary

- CLARIFICATION_BEHAVIOR: **ONE_QUESTION_HELPFUL** (owner: "Necessary and
  high-value"; the agent correctly classified the residual uncertainty as
  owner priority, not evidence. Caveat: option (a) was labeled
  "what the repository evidence supports", which the owner flagged as
  leading; the counterfactual test is therefore not as clean as it could be.)
- OWNER_BURDEN: **LOW** (Q4: "Very low burden / high value"; the owner's total
  involvement was one multiple-choice question before the synthesis.)
- INTENT_PRESERVATION: **GOOD** (Q6: well grounded and intent-preserving.)
- GROUNDING: **STRONG** (Q6; the mis-wiring diagnosis is directly observed;
  direction rested on owner judgment, which was solicited.)

## The seven most important learning questions

1. **Did autonomous investigation do enough work before involving the owner?
   YES.** The investigation collapsed two apparent workstreams into one
   direction plus a bounded repair ("done-but-mis-wired"). The owner's only
   pre-synthesis involvement was one multiple-choice question. No PRE
   questionnaire, no intake form.
2. **Did the agent correctly distinguish missing evidence from missing owner
   intent? YES.** Evidence-resolvable uncertainties (validator skip behavior,
   canonical-vs-legacy identity, version drift) were classified
   EVIDENCE_RESOLVABLE and NOT asked; the single asked uncertainty was
   OWNER_INTENT (strategic priority). The protocol's CASE A vs CASE B
   distinction worked as designed.
3. **Did different answers genuinely lead to different recommendations? YES
   — but the test was weakened by leading presentation.** Counterfactual:
   branch (b) makes reconciliation the focus and defers interaction design —
   materially different work. However, option (a) was labeled as the
   evidence-supported recommendation, biasing the answer. Highest-information
   question? Yes — direction + sequencing resolved in one answer, only the
   owner could supply it. The wording, not the selection, is the defect.
4. **If no question was asked — n/a.** (One question was asked.)
5. **Did the interaction reduce owner cognitive burden relative to the
   PRE-heavy P-series protocols? YES.** Q4 "Very low burden / high value";
   compare P-series assisted-baseline records. The single-question design is
   the main burden reduction.
6. **Did the owner actually prefer this interaction shape? Qualified.**
   Q7: "Maybe — with neutral clarification wording." Not an unqualified
   preference; the shape is promising but the question-presentation defect
   must be fixed before the owner would reuse it confidently.
7. **What must change before implementation in repo-sensemaker?**
   (a) Neutral clarification-question presentation — no embedded
   recommendation in answer options; ask intent, then recommend. (b) The
   probe's brief failed canonical validation (16 EVIDENCE_QUOTE_NOT_FOUND:
   excerpt quotes authored as placeholders) — production execution must
   produce verbatim-quoted excerpts; validation is part of the interaction.
   (c) Decide product behavior when validation fails (record-and-continue vs
   block) rather than the probe's repair-free recording. (d) Productize the
   "one question only, counterfactual-gated" rule explicitly.

## Other learning

- **AGENT_SELECTED_TARGET limitation honored:** the result evaluates the
  interaction shape on an agent-selected plausible decision. It does NOT
  measure owner demand or test an owner-originated decision. Owner Q1 answer
  explicitly restates this limit. The proportional claim: "Given an
  agent-selected plausible repository decision, the investigation-first /
  clarify-if-needed interaction was tested for usefulness, grounding, owner
  burden, and intent handling."
- **Canonical validation (Phase 5) ran once and failed** (valid: false, 16
  quote-verification errors, recorded verbatim in validation-result-v1.json).
  No repair, no rerun, per protocol. The result is preserved as execution
  evidence and is not used to determine the S1 interaction disposition; this
  experiment does not establish a definitive root cause.
- **Substantive product finding (recorded, NOT implemented):** the four INFRA
  gaps (00-user-intent.md) are committed but mis-wired — deliverables in
  legacy root copies, canonical skills/ trees never updated,
  validate-skill-hygiene.py silently skips checks 2-3, two divergent
  artifact-contracts.yaml. Bounded reconciliation (~1 day) is the weakest
  boundary; interaction design is the owner-confirmed direction.
- **Validation as a quality signal:** the validator's quote-verification
  flagged non-conforming excerpts in this probe's brief — support for keeping
  validation in the canonical interaction, without this experiment asserting
  a definitive root cause.

## Hypothesis assessment

S1 **strengthens** the interaction hypothesis ("investigate first; ask the
smallest high-information question only when decision-changing and
owner-intent; then recommend") with a boundary condition: question wording
must be neutral. Autonomous investigation + one counterfactual-gated owner
question produced a decision the owner rated clearly useful, well grounded,
low-burden, and intent-preserving.

## Exact file scope

experiments/solution-interaction-s1-v1/: charter-v1.md,
assisted-context-v1.md, repo-sensemaker-investigation-v1.md,
clarification-v1.md, owner-synthesis-v1.md, owner-post-v1.md (pending owner
answer record), learning-v1.md, validation-result-v1.json.

No implementation was performed. repo-sensemaker was not modified. No S2
started.
