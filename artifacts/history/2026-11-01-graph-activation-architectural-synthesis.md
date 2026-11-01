# Architectural Synthesis: Graph Activation Across Agent, Installation and Runtime

**Status:** source-grounded, provisional architecture comparison; not an independent host-use trial
**Date:** 2026-11-01
**Target:** `ThorStarlord/sensemaking-skills`, `main@7319af1a52ad3a77b17ae04d6de26b28beae45a9`
**Program:** `docs/superpowers/plans/2026-10-30-graph-mediated-reasoning-evolution.md` WP-4/WP-5/WP-6
**Method:** source/graph record inspection through GitHub; no native host invocation or semantic index query in this episode

## 1. Governing Intent and Scope

The real architecture question is **how a coding agent should gain useful, applicable reviewed graph context when different hosts and workflows have different installation and execution surfaces**. Does the new workflow installation-availability support justify runtime-enforced graph consultation, or should graph activation remain agent-native with optional bounded context attachment?

The product outcome is better source-grounded understanding and decisions across sessions (ADR 0031, ADR 0034). Compare the *mechanisms* for bringing knowledge into a consequential decision against this outcome, rather than ranking the outcome itself against its means. ADR 0029 keeps semantic control with the active agent. The October 30 graph-reasoning plan requires observed need before retrieval or runtime expansion. This synthesis concerns Sensemaking-Skills only, not modification of a target repository, publication or a product-thesis change.

## 2. Target Possibilities

`poss:persistent-semantic-stewardship` is the long-term selected destination. The present synthesis is a mechanism comparison within that destination, not a new strategic frontier or a new possibility selected by this artifact.

## 3. Current Architecture and Relational Evidence

| Surface | Source-verified behavior | Claim boundary |
| --- | --- | --- |
| Agent-native control | `skills/using-sensemaking/SKILL.md` says installed Skill parity is not the loaded host revision; the active agent selects relevant reasoning | Written guidance does not prove active adherence |
| Steward RECALL | `skills/repository-semantic-steward/references/recall.md` supports selective indexed queries, original-source verification and direct authored-record fallback | No mandatory graph stage; misses do not imply product absence |
| Installation availability | `src/sensemaking_skills/workflow_availability.py` separates installation from liveness and authority, and returns `execution_authorized: false` | Presence of Skill files does not show a Skill was invoked |
| Workflow runtime | `scripts/workflow-runtime.py` accepts an explicit installed root, exposes installation and step-invocation evidence, and refuses an unavailable Skill in a relevant invocation path | Not a semantic controller, graph query consumer, or proof of an active coding agent's internal use |
| Campaign context | `src/sensemaking_skills/campaign_knowledge_context.py` attaches optional source-pinned `context-for` results to an explicitly bound Campaign target | Knowledge view neither selects the next responsibility nor authorizes action |
| Current graph | `.sensemaking/knowledge/stewardship.json` records `lesson:installed-skill-currency-includes-references`; the reviewed graph supports source-verified continuity | This lesson concerns installed copy parity, not demonstrated reasoning from graph data |
| Recent context repair | Merged PR #691 records the strategic comparison rule and its governing rationale as file-reachable authored knowledge | Source-checked link construction only; later native retrieval not assessed |

**RELATIONAL_VERDICT.** Claim: *An installation-available Skill or an available workflow establishes that the active coding agent consulted and reasoned with retained graph knowledge.* Positive direction, scoped to the availability module, workflow runtime and documented agent interfaces at the stated revision.

- **Declared:** the sources explicitly limit installation availability to file presence and distinguish liveness, permission, invocation and semantic selection.
- **Implemented:** the inspected availability code calculates installed-set status; the runtime records invocation separately; the Campaign adapter provides optional contextual retrieval; no inspected availability method performs graph-based semantic decision selection.
- **Exercised:** source inspection here; **no fresh host invocation or decision-use trial**. Actual installed, loaded and applied status for a participant is NOT_ASSESSED.
- **Graph:** the existing installed-Skill currency lesson covers file parity and reference drift. The explicit installation-versus-graph-use boundary was not represented as a reviewed observation in the authored packs before this work.
- **Assessment: OVERSTATED**. Presence and availability are not evidence of graph-mediated reasoning. This is neither a runtime implementation gap against a declared graph-use promise nor a reason to make knowledge injection mandatory.

This assessment does not claim that no host ever uses the graph, that runtime invocation is impossible, or that the current controller is consistently obeyed.

## 4. Architecture Options (same comparison level: graph activation mechanisms)

### A — `arch:agent-native-selective-recall` (provisionally preferred)

Retain `using-sensemaking` as the one semantic controller. When historical decisions or product knowledge could change a consequential decision, the agent calls Steward RECALL/RELATE, verifies current original sources and reconciles meaningful learning. Keep the indexed and direct-authored-record fallback. If actual host observations expose a repeatable failure, narrow the *existing* source guidance or context access accordingly.

**Reuses:** current controller, RECALL/RELATE, revision-aware queries, graph records and receipts. **Transition:** none required by current source evidence; future targeted guidance is conditional on a demonstrated failure. **Assumption:** the active host can expose or manually load its intended instructions and available sources. **Tradeoff:** agent behavior varies by host; the guidance alone cannot guarantee use.

### B — `arch:opt-in-campaign-knowledge-context` (retained complementary mechanism)

For an already selected multi-context Campaign responsibility, let the agent explicitly attach one to eight source-pinned file contexts through the existing `campaign working-context` knowledge options. Make no automatic task routing or mandatory graph lookup. A future consumer integration would be justified only by an actual Campaign task that cannot use the existing opt-in view.

**Reuses:** `campaign_knowledge_context.py`, `context-for`, Campaign identity and revision checks. **Transition:** possible incremental exposure/documentation at an actual consumer, not an immediate runtime change. **Tradeoff:** bounded file-oriented context may not cover alternative history; it still requires agent interpretation.

### C — `arch:runtime-forced-graph-context` (declined counterfactual)

Make the workflow runtime automatically build or attach graph context whenever a Skill step runs, treating consultation as an execution prerequisite. It could improve mechanical availability of context but would impose graph overhead on routine work, conflate workflow orchestration with semantic selection, and be brittle when index access or host loading is unavailable.

**Reuses:** current workflow runtime and knowledge index. **Transition:** new runtime wiring and failure semantics, plus authority-boundary review. **Tradeoff:** additional runtime coupling and maintenance; no source evidence establishes that it would make later decisions better. This is a comparison option, **not** authorized construction.

## 5. Option Comparison

The applicable lenses are decision relevance, portability across hosts, source provenance, authority separation, additional runtime cost, maintenance and recovery when an index is unavailable.

A is the default preference because it directly matches ADR 0034's agent-native semantics and the existing normal-use lessons. B is a useful *conditional complement* in durable Campaign work, not a substitute for the active agent's judgment. C may deliver context mechanically, but the cited installed-availability implementations do not demonstrate a requirement for such injection; a runtime-installed Skill is not proof of agent reasoning.

This is a comparison of mechanisms serving the same product outcome, not a comparison of a product outcome with an experiment or implementation intervention.

## 6. Conditional Consequences and Stopping

- **If** fresh hosts fail to load the correct Skill or the agent fails to consult useful retained knowledge, A can still produce missed context despite accurate source instructions. A host-revision/currentness observation would make this failure visible but would not guarantee corrected reasoning.
- **If** B supplies concise context for an already authorized Campaign task, it can reduce navigation overhead, but the returned `NOT_ASSESSED` categories must remain visible. A Campaign context is never action authority.
- **If** C forces graph context for every step, routine work may incur avoidable construction or lookup overhead, and unrelated incomplete coverage may be interpreted as a workflow blocker. This is hypothetical; no independent measured cost supports a magnitude claim.

Further consequence depth cannot overturn the preference without evidence that current agent-native consumption fails for a real consequential decision or that current opt-in context is inadequate. Preserve those as evidence hinges rather than manufacturing runtime work.

## 7. Provisional Preference and Feedback

**Preference:** A, with B available when Campaign continuation actually warrants it. The installation evidence confirms why availability must not be mistaken for application. The previous PR #691 reachability repair supports reusing the existing query consumer rather than adding a second one, but it is not independent proof of later agent benefit.

**Feedback: REAFFIRM** the agent-native mechanism for this bounded question. The source inspection changes what future reports must claim about installation and graph use; it does not revise ADR 0034, select a new frontier or authorize automated runtime graph injection.

## 8. Unresolved Questions and Reconsideration

The materially unresolved question is whether genuinely separate coding-agent sessions reliably use applicable reviewed knowledge when its source/host version is accessible. Host parity, actual invocation and later decision benefit require separate evidence. Where safe independent execution is unavailable, retain the boundary and continue source-backed engineering work.

Reconsider a narrow host integration only after observing repeatable, decision-changing missed retrieval or inaccurate revision reporting. Reconsider a runtime consumer only if a specific selected execution responsibility needs read-only context and existing opt-in Campaign retrieval cannot provide it.

## 9. Authority and Claim Boundaries

`installed != loaded != invoked != applied`. An observation about source behavior is not a measurement of participant behavior. A provisional preference does not select or authorize construction. A consequence hypothesis is not an observed effect. ADR 0029, ADR 0031 and ADR 0034 remain controlling; ADRs 0032 and 0033 remain proposed.

## 10. Evidence

- `docs/adr/0029-current-product-boundary.md`; `docs/adr/0031-persistent-semantic-stewardship.md`; `docs/adr/0034-ontology-first-adaptive-sensemaking.md`
- `docs/superpowers/plans/2026-10-30-graph-mediated-reasoning-evolution.md`
- `skills/using-sensemaking/SKILL.md`; `skills/repository-semantic-steward/references/recall.md`
- `src/sensemaking_skills/workflow_availability.py`; `scripts/workflow-runtime.py`; `src/sensemaking_skills/campaign_knowledge_context.py`
- `docs/product-management/distribution-profile-contract.md`
- `.sensemaking/knowledge/architecture.json`; `.sensemaking/knowledge/stewardship.json`
- [PR #691](https://github.com/ThorStarlord/sensemaking-skills/pull/691); [PR #687](https://github.com/ThorStarlord/sensemaking-skills/pull/687)
- `docs/normal-use/operational-qualification-001.md` (narrow, unreplicated evidence; not generalized proof)

No local Semantic CLI index, fresh host invocation, semantic proposal validator or independent comparison was run in this GitHub connector-only episode. The comparison is source-grounded analysis, not qualification.

## 11. Machine-Readable Summary

```yaml
artifact_id: architectural_synthesis
schema_version: 1
analysis_ref: artifacts/history/2026-11-01-graph-activation-architectural-synthesis.md
target_repository: ThorStarlord/sensemaking-skills
target_source_identity: "main@7319af1a52ad3a77b17ae04d6de26b28beae45a9"
governing_intent_refs:
  - docs/adr/0029-current-product-boundary.md
  - docs/adr/0031-persistent-semantic-stewardship.md
  - docs/adr/0034-ontology-first-adaptive-sensemaking.md
target_possibility_refs:
  - poss:persistent-semantic-stewardship
current_architecture_refs:
  - skills/using-sensemaking/SKILL.md
  - src/sensemaking_skills/workflow_availability.py
  - scripts/workflow-runtime.py
  - src/sensemaking_skills/campaign_knowledge_context.py
  - .sensemaking/knowledge/stewardship.json
local_assumptions:
  - assumption_id: hyp:host-applies-loaded-recall
    statement: "An active coding-agent host that loads current Sensemaking instructions can and will apply selective RECALL when it matters; this is not guaranteed by installation or guidance."
    epistemic_status: hypothetical
architecture_options:
  - option_id: arch:agent-native-selective-recall
    title: "Agent-native selective RECALL"
    proposed_structure: "Keep the current semantic controller and use narrow, source-verified graph retrieval only for decision-relevant context; refine guidance only on demonstrated failure."
    reuses_refs:
      - skills/using-sensemaking/SKILL.md
      - skills/repository-semantic-steward/references/recall.md
    proposed_transitions: []
    assumption_refs:
      - hyp:host-applies-loaded-recall
    conditional_consequence_refs:
      - conseq:host-recall-application-miss
    comparison_outcome: PROVISIONALLY_PREFERRED
    comparison_reason: "Preserves one controller, supports the index-free fallback and imposes no mandatory runtime overhead; later actual use remains unqualified."
  - option_id: arch:opt-in-campaign-knowledge-context
    title: "Opt-in Campaign context"
    proposed_structure: "Continue binding source-pinned context-for to an already selected Campaign task only on explicit request; add consumer integration only when a real task warrants it."
    reuses_refs:
      - src/sensemaking_skills/campaign_knowledge_context.py
    proposed_transitions: []
    assumption_refs: []
    conditional_consequence_refs:
      - conseq:campaign-context-limited-coverage
    comparison_outcome: RETAINED_ALTERNATIVE
    comparison_reason: "Useful for durable multi-context tasks but does not solve semantic selection outside Campaign work or establish knowledge completeness."
  - option_id: arch:runtime-forced-graph-context
    title: "Mandatory runtime injection"
    proposed_structure: "Automatically build or attach semantic context for every workflow Skill step."
    reuses_refs:
      - scripts/workflow-runtime.py
      - src/sensemaking_skills/semantic_architecture/knowledge_store.py
    proposed_transitions:
      - target_ref: scripts/workflow-runtime.py
        change: "Make graph-context injection a runtime prerequisite to Skill-step invocation; requires separate architectural and authority review."
    assumption_refs: []
    conditional_consequence_refs:
      - conseq:forced-context-overhead
    comparison_outcome: DECLINED
    comparison_reason: "No demonstrated consumer need, additional complexity, and tension with selective agent-owned semantic control."
option_comparison:
  attribution: "active agent, 2026-11-01; no owner-level choice or authorization"
  lenses:
    - decision relevance
    - source and revision fidelity
    - portability across hosts
    - authority separation
    - runtime and maintenance cost
  summary: "Prefer selective agent-native recall. Keep opt-in Campaign context as a complement; decline mandatory runtime injection without observed necessity."
provisional_preference:
  option_id: arch:agent-native-selective-recall
  status: PROVISIONAL
  attribution: "active agent, 2026-11-01; no authority to change the product thesis"
  rationale: "Matches ADR 0034 and existing retrieval while preserving correct installed-versus-applied evidence boundaries."
  scope: "Applies until a genuine consequential agent session demonstrates inadequate retrieval/consumption that current source grounding cannot repair."
preference_feedback:
  - consequence_ref: conseq:host-recall-application-miss
    outcome: REAFFIRM
    effect: "The hypothetical risk of agent non-use remains open and belongs in honest host qualification; it does not warrant forced runtime injection now."
conditional_consequences:
  - consequence_id: conseq:host-recall-application-miss
    effect: "A future agent may miss applicable retained knowledge despite correct installed files."
    category: risk
    mechanism: "Host loading and agent consumption are independent of installation availability."
    assumption_refs:
      - hyp:host-applies-loaded-recall
    observed_premise_refs:
      - skills/using-sensemaking/SKILL.md
      - src/sensemaking_skills/workflow_availability.py
    counterevidence: "The completed cloud pair observed some direct knowledge use, but that single narrow episode does not establish reliable host behavior."
    would_change_decision_if: "Repeated independent use shows a preventable source-grounding miss that a narrowly scoped host integration could remedy."
  - consequence_id: conseq:campaign-context-limited-coverage
    effect: "Explicit Campaign context may reduce navigation but can omit material decisions or alternatives outside its bounded paths."
    category: mixed
    mechanism: "The existing adapter attaches bounded context-for results with NOT_ASSESSED caveats rather than proving complete task context."
    assumption_refs: []
    observed_premise_refs:
      - src/sensemaking_skills/campaign_knowledge_context.py
    counterevidence: "The adapter's read-only, explicitly requested design already avoids compulsory lookups and identity confusion."
    would_change_decision_if: "A specific selected Campaign responsibility cannot reconstruct necessary context through the existing read-only view."
  - consequence_id: conseq:forced-context-overhead
    effect: "Mandatory graph context may increase task overhead and encourage false confidence in a partial graph."
    category: risk
    mechanism: "A runtime prerequisite adds source/index availability and more output to every Skill step regardless of decision relevance."
    assumption_refs: []
    observed_premise_refs:
      - skills/repository-semantic-steward/references/recall.md
      - scripts/workflow-runtime.py
    counterevidence: "No measured cost or benefit of this unbuilt mechanism exists; a future bounded consumer could be useful in a different scope."
    would_change_decision_if: "Independent evidence demonstrates that narrow automatic context delivery improves actual consequential decisions enough to justify the contract and control costs."
consequence_stop_reason: "Additional hypothetical causal depth will not change the preference without distinct host-use or consumer-limitation evidence."
derived_possibility_refs: []
candidate_responsibility: null
reconsideration_conditions:
  - "A fresh agent with correct loaded Skill version repeatedly misses source-backed decision knowledge in consequential work."
  - "An authorized Campaign task reveals a limitation that the existing opt-in context consumer cannot answer."
unresolved_questions:
  - "Will genuinely independent hosts reuse retained knowledge when the expected Skill instructions are loaded?"
  - "Which, if any, concrete consumer needs additional retrieval mechanics rather than better source anchoring?"
implementation_authority_established_by_artifact: false
semantic_truth_established: false
created_at: "2026-11-01"
immutable: true
```
