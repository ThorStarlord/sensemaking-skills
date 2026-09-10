# Chess Mentor Engine — PM Problem Discovery Preflight

## Problem framing

Chess Mentor Engine has a technically qualified evidence chain through M19, but the next product-learning investment is still uncertain. The immediate question is not whether the repository can compute and provenance-bind analysis; it is which unresolved user-facing boundary most constrains a useful mentor experience after M17-M19.

This artifact is a **repository-evidence preflight**, not customer validation. It uses current product documentation as evidence of implemented capabilities, acknowledged claim ceilings, and explicitly deferred product questions.

## Existing evidence

- The repository documents a complete technical path from PGN/canonical position through engine evidence, diagnostic selection, grounded mentor feedback, and provenance-bound model language.
- The milestone handoff explicitly leaves end-user UX quality, model-language semantic/pedagogical quality, empirical tutoring efficacy, and production provider selection unproven.
- The handoff recommends, in order, a model-output evaluation harness, a diagnostic-candidate-to-tutor-session bridge, and only then a production provider adapter.
- Current documentation states that software qualification is not empirical tutoring efficacy and that M19 provenance binding does not establish semantic correctness or pedagogical effectiveness.

Evidence references used below:

- `github:ThorStarlord/Chess-Mentor-Engine@4139e4dda567feeadb5684f51c4a265dfae07330:README.md`
- `github:ThorStarlord/Chess-Mentor-Engine@4139e4dda567feeadb5684f51c4a265dfae07330:STATUS.md`
- `github:ThorStarlord/Chess-Mentor-Engine@4139e4dda567feeadb5684f51c4a265dfae07330:docs/product/repository-build-status.md`

## Hypotheses and uncertainties

### H-1 — Candidate-to-session orchestration may be the clearest near-term workflow bottleneck

**Status:** untested.

Repository evidence shows that diagnostic candidate selection and tutor-session machinery both exist, while the handoff still calls out the bridge between them as a major remaining integration gap. What is not established is whether closing this bridge would materially improve the user's learning workflow relative to other gaps.

### H-2 — Model-output quality may become the dominant trust bottleneck once model coaching is used in practice

**Status:** untested.

M19 binds model prose to exact grounding and provenance, but the repository explicitly does not certify semantic correctness, uncertainty handling, safety, or pedagogical quality of arbitrary model prose. The current plan therefore proposes an evaluator-facing harness before a production provider.

### H-3 — Choosing a production model/provider now would be premature

**Status:** evidence-backed as a product sequencing constraint, not as customer preference.

The milestone handoff explicitly recommends provider adoption only after evaluation criteria exist. This supports a sequencing decision but does not establish what users value in provider quality, latency, privacy, or cost.

## Learning plan

1. **Repository-backed workflow walkthrough:** take representative existing diagnostic evidence through the current M18 and M8/M16/M19 boundaries and record where a user or operator must manually translate state. This is an internal product-flow observation, not customer evidence.
2. **Bounded mentor-output evaluation design:** define observable checks for faithfulness to M16 grounding, overclaiming, uncertainty language, actionability, and pedagogical consistency. Do not select a provider yet.
3. **Real user/task evidence before prioritization:** observe at least a small set of real learners or operators performing the candidate-review-to-tutor task and receiving mentor feedback. Record task friction, confusion, trust breaks, and whether the output changes the next training action.
4. **Compare the two leading uncertainties:** candidate-to-session workflow friction versus mentor-output trust/quality. Use observed user/task evidence rather than implementation complexity alone to decide which deserves the next product milestone.

## Decision criteria

- Prefer **candidate-to-session orchestration** if users/operators can understand and trust current mentor output but consistently fail or require manual intervention to move from a selected diagnostic candidate into the tutoring loop.
- Prefer **model-output evaluation/quality work** if users can reach the tutoring loop reliably but model-language quality, overclaiming, uncertainty handling, or inconsistency materially reduces trust or changes decisions incorrectly.
- Do **not** prioritize a production provider merely because integration is technically available; provider work becomes warranted only after explicit evaluation criteria and a bounded quality/operational target exist.
- If neither uncertainty is supported by direct user/task evidence, keep both unresolved and gather evidence rather than converting repository roadmap language into customer truth.

## Unresolved questions

- Which learner segment is the first intended design customer for the mentor loop: self-directed improvers, coached club players, beginners, or another group?
- How often do users currently reach a diagnostic candidate but fail to turn it into a tutoring/training action?
- What mentor-output failures most damage trust: chess inconsistency, overclaiming learner traits, poor explanation, weak actionability, or something else?
- Which outcome should the next product milestone optimize: task completion, explanation trust, training selection quality, repeated use, or learning transfer?
- Is there any existing interview/usability evidence outside the repository that should supersede this repository-only preflight?

## Machine-readable handoff

```yaml
artifact_id: discovery_findings
schema_version: "1"
problem_statement: "Which unresolved user-facing boundary should guide the next Chess Mentor Engine product-learning investment after M17-M19?"
hypotheses:
  - id: H-1
    statement: "The diagnostic-candidate-to-tutor-session bridge is a material near-term workflow bottleneck for users or operators."
    status: untested
    evidence_refs:
      - "github:ThorStarlord/Chess-Mentor-Engine@4139e4dda567feeadb5684f51c4a265dfae07330:STATUS.md"
      - "github:ThorStarlord/Chess-Mentor-Engine@4139e4dda567feeadb5684f51c4a265dfae07330:README.md"
    learning_method: "Observe representative users/operators moving from selected diagnostic candidates into the tutor loop and record manual handoffs, confusion, and failure points."
    decision_criterion: "Prioritize orchestration if repeated task evidence shows the bridge blocks or materially degrades completion of the learning workflow."
  - id: H-2
    statement: "Model-authored mentor output quality and trust are a material bottleneck once users receive M19 coaching."
    status: untested
    evidence_refs:
      - "github:ThorStarlord/Chess-Mentor-Engine@4139e4dda567feeadb5684f51c4a265dfae07330:STATUS.md"
      - "github:ThorStarlord/Chess-Mentor-Engine@4139e4dda567feeadb5684f51c4a265dfae07330:docs/product/repository-build-status.md"
    learning_method: "Evaluate grounded mentor outputs against explicit faithfulness, overclaiming, uncertainty, actionability, and pedagogical-consistency criteria, then observe user trust and comprehension."
    decision_criterion: "Prioritize model-output evaluation/quality if material trust or decision errors occur despite a usable candidate-to-session flow."
  - id: H-3
    statement: "Production provider selection should remain deferred until model-output evaluation criteria exist."
    status: evidence_backed
    evidence_refs:
      - "github:ThorStarlord/Chess-Mentor-Engine@4139e4dda567feeadb5684f51c4a265dfae07330:STATUS.md"
    learning_method: "Define provider-neutral evaluation criteria and operational targets before comparing production providers."
    decision_criterion: "Provider selection becomes eligible only when quality and operational criteria can distinguish acceptable from unacceptable provider behavior."
unresolved_questions:
  - "Which learner segment is the first intended design customer for the mentor loop?"
  - "Which observed user task currently breaks most often: candidate selection, transition into tutoring, mentor explanation, or training selection?"
  - "What direct user or operator evidence already exists outside the repository?"
```
