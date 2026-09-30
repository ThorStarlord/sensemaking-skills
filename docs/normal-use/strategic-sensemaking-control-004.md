# Control arm 004 — AION Workflow Core (no skill, read-only)

Clean control for `strategic-sensemaking-trial-004.md`. Fresh agent context;
the prompt explicitly forbade reading or using any skill/SKILL.md/sensemaking
material. Same objective, same read-only authority. Recorded for artifact-level
comparison, not self-report.

```text
Repository / domain: aion-workflow-core (small Python control-layer library, v0.1.0)
Date: 2026-09-29
Loaded Skill identity: NONE (control arm — skill deliberately excluded)
Chosen responsibility / next action: Implement the repository's own documented v0.2 step — deterministic artifact schema validation in the run loop (validators.py checks only artifact presence, never content).
First concrete step: define the interface domain's five artifact contracts as data; add validate_artifact_content(context, contract); call it from InterfaceAdapter.validate(); add a unit test that injects an artifact missing a required section and asserts an error.
Scope avoided / refused: LLM/generation logic; premature revise/retry loop or shared base-adapter abstraction (README explicitly defers extraction until repetition is proven); unrelated changes; new third-party deps; any file writes (read-only).
Alternatives rejected: build the full revise/accept lifecycle (unbounded for a one-commit scaffold); make the error path testable via a failing adapter (subsumed); add linting/type-checking to CI (low leverage); fill the auteur placeholder adapter (domain, not core).
Confidence: medium-high (schema validation is owner-documented, core-layer, bounded); medium on exact form.
Blocking question: should artifacts become structured (front-matter/JSON) or remain free-form Markdown with section-presence checks — an owner design decision.
```

## Comparison (skill arm vs control arm)

- Responsibility chosen: skill = CHALLENGE the visible roadmap, verify by
  inspection, surface the unwired validation/retry gap, and flag it as premature
  to build schemas; control = implement the visible documented milestone (v0.2
  schema validation), which also addresses content validation.
- Scope avoided: both refuse unrelated work and deps; the skill arm additionally
  refuses to build on an unverified premise.
- Verdict on this task: **skill-favorable.** The skill redirected from the
  visible milestone to the presupposed gap (validation collected but never
  enforced) — the specific "milestone capture" failure the doctrine targets. The
  control followed the milestone. The control's choice is defensible, but the
  skill's challenge surfaced the presupposition explicitly.
