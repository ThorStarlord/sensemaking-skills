# Repository Sensemaking Brief — attempt-002

## 1. Repository goal

Auteur presents itself as a long-form fiction narrative-engine toolkit that converts creative intent into an accepted story engine and then applies deterministic validation before optional outlining/drafting stages. At the pinned target, explicit author authority and deterministic validation are architectural themes rather than incidental implementation details.

## 2. Current shape

The examined exact snapshot is `ThorStarlord/auteur@0653defb05625f2fcde0ac32eac6e59ccf7eeb90`. This merge introduces human-review notices for Universe `cross_story_constraints`. The relevant path spans `UniverseIdentity` models, Series advisory diagnostics, the Series Bible handler, and focused semantic-honesty tests. The repository also has a configured pytest/Ruff boundary and a stray root scratchpad outside it.

## 3. Strong signals

- `README.md:1-30` preserves a crisp ownership split: deterministic code owns schemas/validation/artifacts while LLM work is downstream creative assistance.
- `src/auteur/series/universe_advisory.py:333-425` refuses to pretend cross-story compliance can be derived from one Series artifact.
- `tests/test_cross_story_constraint_notices.py:205-270` specifically asserts human-review wording, non-evaluation, INFO severity, and absence of generated pass/fail claims.
- The target commit itself is exactly the cross-story-review-notices merge, so the behavior under analysis is the change introduced at the pinned SHA, not an inference from later code.

## 4. Missing pieces

A `CrossStoryConstraint` can declare `severity: required`, and that is the default (`src/auteur/universe/models.py:18-52`). Yet the cross-story advisory deliberately emits `INFO` for every rule and treats the configured severity only as text metadata (`src/auteur/series/universe_advisory.py:333-425`). The Series Bible handler converts the notice to INFO and blocks compilation only on ERROR diagnostics (`src/auteur/series/handlers.py:148-228`).

That makes the human review **semantically explicit but operationally external**: in this examined path there is no durable state that distinguishes “required rule reviewed” from “required rule merely surfaced.” This is more important than trying to automate semantic compliance, because the current code is correct to avoid a false automated verdict.

Secondary finding: `CUsersAdminAppDataLocalTempclaudeH--GithubRepositories-auteur62865e61-062c-4434-9de4-6f441dc6a9bascratchpadtest_validate_choices.py:1-12` is a committed quick-test script at repository root. `pyproject.toml:31-38` limits pytest discovery to `tests/` and Ruff to `src/auteur/**/*.py` and `tests/**/*.py`, leaving this artifact outside both configured checks.

Connector-only local metrics `verification_gap.vg`, `context_entropy.ce`, `fixtures_coverage.coverage`, and `churn` remain unmeasured.

## 5. Improvement opportunities

- Add a first-class review disposition for each cross-story constraint: at minimum pending, reviewed, or waived, with source/provenance.
- Make required cross-story obligations require a current disposition at an appropriate deterministic qualification boundary without claiming that the machine evaluated the prose rule.
- Regression-test stale dispositions after rule edits, duplicate constraints, waivers, and missing review state.
- Remove/relocate the root scratchpad and add a narrow hygiene check for temp-derived root Python artifacts.

## 6. Weakest boundary

**Weakness type:** Implicit Dependencies

The weakest boundary is the dependency on an out-of-band human review to discharge a rule that the model can label `required`. The notice is explicit, but completion of that human responsibility is not represented in the deterministic Series compile path examined here.

## 6.5. Problem classification (fog type)

`architecture_fog` — the unresolved question is how human semantic judgment becomes explicit, durable state at a deterministic compilation/qualification boundary.

## 7. Evidence

<!-- mode: investigative -->

State-currency backend: `github_connector_exact_sha_v1 @ 0653defb05625f2fcde0ac32eac6e59ccf7eeb90`.

Fresh attempt-002 reads resolved the exact target commit and these exact-SHA blobs:

- `README.md:1-30` — blob `52babadc6422f5d491d27dd5927c192b6417605b`.
- `src/auteur/universe/models.py:18-52` — blob `9292b7da08484916772a2069e0129b1fb898b3a6`.
- `src/auteur/series/universe_advisory.py:333-425` — blob `14d11929448bcbd406fbed6cec0eaa0ddd289701`.
- `src/auteur/series/handlers.py:148-228` — blob `d44f0d5034a04d31ff670650447595c0598a0f84`.
- `tests/test_cross_story_constraint_notices.py:205-270` — blob `43ee358feba8aeaba7305e5ec819eb093189bf15`.
- `pyproject.toml:31-38` — blob `c6dcf42f259aae4c912a4f9e0528f6ee0f2ecc59`.
- `CUsersAdminAppDataLocalTempclaudeH--GithubRepositories-auteur62865e61-062c-4434-9de4-6f441dc6a9bascratchpadtest_validate_choices.py:1-12` — blob `7a786becd30233afc01ffb7430518e9b8843e3b5`.

Logic trace: the model expresses required severity; the advisory intentionally converts the unresolved semantic check into an INFO human-review notice; the compile boundary rejects only ERROR; therefore a required review obligation can remain unresolved while compilation succeeds. Tests prove the non-evaluation behavior is deliberate. The next leverage is to make review completion explicit without making compliance automated.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: src/auteur/universe/models.py
    lines: L18-L52
    quote: "see exact-SHA source lines"
    supports_claim: "CrossStoryConstraint defaults to required severity."
  - file: src/auteur/series/universe_advisory.py
    lines: L333-L425
    quote: "see exact-SHA source lines"
    supports_claim: "All cross-story notices are non-blocking INFO and configured severity is metadata only."
  - file: src/auteur/series/handlers.py
    lines: L148-L228
    quote: "see exact-SHA source lines"
    supports_claim: "Series Bible compilation blocks ERROR diagnostics while cross-story notices remain INFO."
  - file: tests/test_cross_story_constraint_notices.py
    lines: L205-L270
    quote: "see exact-SHA source lines"
    supports_claim: "Human-review/non-evaluation semantics are explicitly tested."
```

## 9. Why this boundary matters

Auteur otherwise invests heavily in explicit authority and provenance. For required cross-story obligations, the deterministic state should be able to tell whether the human review responsibility is pending or discharged even when the substantive judgment cannot be automated. Without that state, review completion depends on process memory outside the compile artifact.

## 10. Candidate next steps

1. Specify constraint identity plus review-disposition schema.
2. Add explicit reviewed/waived transitions with provenance.
3. Require a current disposition for required constraints at a deterministic qualification boundary.
4. Add TDD cases for stale, missing, reviewed, waived, and duplicate constraints.
5. Clean and guard the root scratchpad boundary separately.

## 11. Recommended next step

Define the minimum durable cross-story review-disposition contract and gate only on **presence/currentness of human review state**, not on machine-generated semantic compliance.

## 12. Recommended workflow

`implementation-workflow` in `guided_execution` mode. The frozen registry identifies it as the default architecture/code implementation workflow, and human-owned review semantics justify keeping explicit review gates.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: experiments/campaigns/EXP-0005-stage1-auteur-github-connector-pilot/scientific-questions.md
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "src/auteur/universe/models.py (L18-L52, blob 9292b7da08484916772a2069e0129b1fb898b3a6): required severity is modeled and defaulted"
  - "src/auteur/series/universe_advisory.py (L333-L425, blob 14d11929448bcbd406fbed6cec0eaa0ddd289701): unresolved cross-story semantics always surface as INFO human-review notices"
  - "src/auteur/series/handlers.py (L148-L228, blob d44f0d5034a04d31ff670650447595c0598a0f84): Series Bible blocks ERROR only"
  - "tests/test_cross_story_constraint_notices.py (L205-L270, blob 43ee358feba8aeaba7305e5ec819eb093189bf15): semantic honesty is regression-tested"
recommended_workflow_id: implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: "Required cross-story constraints depend on human review whose completion state is external to the examined deterministic Series compile path."
weakness_type: Implicit Dependencies
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-18T19:20:43Z"
immutable: true
```

## 14. Ready-to-copy prompt

Implement a minimal, auditable cross-story review-disposition contract without automating semantic compliance. Preserve current non-evaluation honesty, identify each cross-story rule stably, record `pending|reviewed|waived` with provenance, require a current disposition for `severity: required` at the appropriate deterministic qualification boundary, and cover stale/missing/reviewed/waived/duplicate cases with TDD. Separately remove or relocate the committed root scratchpad and prevent temp-derived root Python artifacts from bypassing repository test/lint policy.
