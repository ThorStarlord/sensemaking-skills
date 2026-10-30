# Architectural Synthesis: Re-entering Discovery-Memory Reasoning

## 1. Governing Intent and Scope

At `ThorStarlord/sensemaking-skills@9f26bb4f2cc86c3e4f55265425ac3fd239f8a0f5`,
the bounded question is how an editor of the portable discovery guidance can
recover its earlier architectural alternatives and distinguish them from the
guidance actually built. ADR 0031 values reusable, source-grounded knowledge;
ADR 0034 keeps the agent as controller and implementation separately authorized.
This is not a reopening of Level 3 or a claim about another repository.

## 2. Target Possibilities

`poss:target-repository-discovery-memory` is recorded as a selected guidance
baseline with explicit prior history, not proven independent-session benefit.
The present comparison serves the narrower re-entry need identified in the
owner's October 30 prospective-reasoning request.

## 3. Current Architecture

At the stated clean revision, `context-for` on
`skills/using-sensemaking/references/portable-construction-loop-v1.md` returned
no owner, decision or alternatives; those categories were `NOT_ASSESSED`, not
absent in the product. The one-hop `explain` of
`arch:git-reviewed-local-memory` returned four options and six consequences.
Its recorded history and the original
`2026-10-28-discovery-memory-prospective-synthesis.md` show that authority
narrowed the preference, while the current portable loop classifies candidates
before retention. The proposed all-`poss:` structure is not the as-built rule.
ADR 0032 is still proposed. The separate funnel path also lacked an owner and
decision in the bounded query; this change addresses the actual discovery
implementation path only.

## 4. Architecture Options

- **A — source-linked history:** anchor the portable reference to its actual
  `using-sensemaking` component and add a reviewed, revision-scoped observation
  linking the component to the earlier synthesis and option IDs. The existing
  `context-for` history category and `explain` remain the consumers.
- **B — context consumer expansion:** add explicit owner-to-option traversal
  to `context-for` and author direct links. This would surface alternatives
  directly, but changes a shared query contract and its caveats.
- **C — preserve the existing search-only route:** make no model or consumer
  change and rely on the editor knowing terms or identifiers. It has no added
  maintenance but leaves this observed file-first entry unassisted.

## 5. Option Comparison

The agent provisionally prefers A: it supplies an attributable path from the
file to the history while preserving the provisional status of the options.
B may be useful if a real consumer needs options directly in the category, but
the existing history and subsequent `explain` answer this case without changing
the shared consumer. C is viable for an agent that knows the identifiers; this
episode began from the file, where the query did not supply them. All three
still require source inspection and agent judgment.

## 6. Consequence Exploration

If editors follow the history reference, A may reduce rediscovery and prevent
the original all-`poss:` proposal being mistaken for the as-built guidance;
this depends on the editor consulting the returned context and source. It also
adds a record that can drift, so it pins the observed revision and sources.
It does not prove later use or causal improvement. B could save a subsequent
query but could also present hypothetical options more prominently and creates
consumer-maintenance cost. Further causal depth would not change the choice
without evidence that the bounded history route is inadequate.

## 7. Provisional Preference and Feedback

`REAFFIRM` A for this bounded decision. The original discovery-memory
preference remains an attributed historical preference, not a new decision.
Its authority restriction and the classification correction affect what the
history must say; neither establishes that a later agent benefits.

## 8. Unresolved Questions

Whether a future independent agent uses the returned history, whether it needs
direct option traversal, and whether maintaining the observation creates
meaningful drift cost are unassessed. Reconsider B upon a real consumer's
documented need; reconsider the original receipt option if ADR 0032 is accepted
with a candidate field. No cross-repository write is authorized here.

## 9. Authority and Claim Boundaries

Provisional preference is not selection or authorization; a conditional
consequence is not an observed outcome; a proposed option is not implemented
architecture. A mechanically valid synthesis does not prove semantic truth.

## 10. Evidence

Original sources: ADRs 0029, 0031, 0032 and 0034; the prior synthesis;
`skills/using-sensemaking/references/portable-construction-loop-v1.md`;
`.sensemaking/knowledge/prospective-reasoning.json` and
`.sensemaking/knowledge/possibilities.json`; and the existing
`knowledge_architecture.py` context consumer. The pre-change `context-for`
and `explain` queries used the exact indexed revision above with a clean
matching workspace. Both path results were untruncated.

## 11. Machine-Readable Summary

```yaml
artifact_id: architectural_synthesis
schema_version: 1
analysis_ref: artifacts/history/2026-10-30-discovery-memory-reentry-synthesis.md
target_repository: ThorStarlord/sensemaking-skills
target_source_identity: "main@9f26bb4f2cc86c3e4f55265425ac3fd239f8a0f5"
governing_intent_refs:
  - docs/adr/0029-current-product-boundary.md
  - docs/adr/0031-persistent-semantic-stewardship.md
  - docs/adr/0034-ontology-first-adaptive-sensemaking.md
target_possibility_refs:
  - poss:target-repository-discovery-memory
current_architecture_refs:
  - skills/using-sensemaking/references/portable-construction-loop-v1.md
  - artifacts/history/2026-10-28-discovery-memory-prospective-synthesis.md
  - src/sensemaking_skills/semantic_architecture/knowledge_architecture.py
architecture_options:
  - option_id: arch:reentry-source-linked-history
    title: Source-linked history
    proposed_structure: "Anchor the discovery reference to its owner and an observed history record that identifies the prior synthesis and option IDs."
    reuses_refs:
      - src/sensemaking_skills/semantic_architecture/knowledge_architecture.py
    proposed_transitions:
      - target_ref: .sensemaking/knowledge/architecture.json
        change: "Add the path anchor, historical observation and explicit owner reference."
    assumption_refs:
      - hyp:target-sessions-consult-retained-candidates
    conditional_consequence_refs: []
    comparison_outcome: PROVISIONALLY_PREFERRED
    comparison_reason: "Reuses the existing history consumer and exposes the source without converting a preference into a decision."
  - option_id: arch:reentry-context-expansion
    title: Direct context consumer expansion
    proposed_structure: "Extend context-for to return explicitly linked owner-to-option records directly."
    proposed_transitions:
      - target_ref: src/sensemaking_skills/semantic_architecture/knowledge_architecture.py
        change: "Extend the alternative selection and its documented coverage semantics."
    assumption_refs: []
    conditional_consequence_refs: []
    comparison_outcome: RETAINED_ALTERNATIVE
    comparison_reason: "A more direct view, but a shared consumer change is not needed for the observed case."
  - option_id: arch:reentry-search-only
    title: Existing search only
    proposed_structure: "Keep existing path coverage and rely on search or known option IDs."
    proposed_transitions:
      - target_ref: skills/repository-semantic-steward/references/architecture-exploration.md
        change: "No change; keep the existing search and explain guidance."
    assumption_refs: []
    conditional_consequence_refs: []
    comparison_outcome: RETAINED_ALTERNATIVE
    comparison_reason: "Low maintenance, but does not help a file-first editor discover the earlier reasoning."
option_comparison:
  attribution: "agent, 2026-10-30"
  lenses:
    - "decision usefulness and source fidelity"
    - "consumer complexity and maintenance"
    - "authority and epistemic boundaries"
  summary: "Source-linked history meets the observed file-first need with the existing consumer; direct traversal is deferred until needed."
provisional_preference:
  option_id: arch:reentry-source-linked-history
  status: PROVISIONAL
  attribution: "agent, 2026-10-30, no authority"
  rationale: "Connects the actual file to the reviewed historical reasoning without adding a query feature."
  scope: "The current repository and this observed discovery-memory decision."
preference_feedback: []
consequence_stop_reason: "Additional conditional layers would not change this choice without a demonstrated consumer need."
derived_possibility_refs: []
candidate_responsibility: "Anchor the portable discovery file to its owner and source-linked historical observation."
reconsideration_conditions:
  - "A real consumer cannot use the history reference to recover the options."
  - "ADR 0032 is accepted with a candidate field."
unresolved_questions:
  - "Whether later independent agents consult and benefit from the returned history."
implementation_authority_established_by_artifact: false
semantic_truth_established: false
created_at: "2026-10-30T20:05:16Z"
immutable: true
```
