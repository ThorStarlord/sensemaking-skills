# Repository Sensemaking Brief — attempt-003

## 1. Repository goal

Auteur is an opinionated long-form fiction narrative-engine toolkit. At the exact pinned snapshot, it combines deterministic narrative validation and artifact handling with optional downstream LLM-assisted creative stages, while preserving explicit author authority over semantic decisions.

## 2. Current shape

The exact snapshot is `ThorStarlord/auteur@0653defb05625f2fcde0ac32eac6e59ccf7eeb90`, the merge that surfaces Universe `cross_story_constraints` as human-review notices. The decision-bearing path spans the Universe constraint model, the Series advisory function, the Series Bible compile handler, and focused tests. Repository validation scopes are declared in `pyproject.toml`; a root scratchpad sits outside those declared scopes.

## 3. Strong signals

- `README.md:1-30` makes deterministic schemas/validation/artifact writing a first-class ownership boundary and keeps creative LLM work downstream.
- `src/auteur/series/universe_advisory.py:333-425` explicitly refuses to infer cross-story compliance from one Series artifact and emits a human-review notice instead.
- `tests/test_cross_story_constraint_notices.py:205-270` protects semantic honesty by requiring human-review/non-evaluation wording and prohibiting generated compliance claims.
- The exact target merge itself is the cross-story review-notice change, so the analysis is attached to the intended immutable implementation revision.

## 4. Missing pieces

`CrossStoryConstraint.severity` supports `required`, `warning`, and `info`, with `required` as the default (`src/auteur/universe/models.py:18-52`). Nevertheless, `surface_cross_story_constraints` deliberately emits every unresolved cross-story rule as `INFO`; configured severity is explanatory metadata and never becomes a blocking diagnostic (`src/auteur/series/universe_advisory.py:333-425`). The Series Bible path then blocks only `ERROR` diagnostics (`src/auteur/series/handlers.py:148-228`).

That leaves a required semantic obligation dependent on an external human process whose **completion state is not represented in the examined deterministic compile path**. The implementation is correct not to fake compliance; the missing control is a durable review disposition that says whether the requested human responsibility is still pending, completed, or explicitly waived.

Secondary hygiene evidence remains the committed root quick-test file `CUsersAdminAppDataLocalTempclaudeH--GithubRepositories-auteur62865e61-062c-4434-9de4-6f441dc6a9bascratchpadtest_validate_choices.py`. `pyproject.toml:31-38` restricts pytest to `tests/` and Ruff to `src/auteur/**/*.py` plus `tests/**/*.py`, so the scratchpad is outside both configured checks.

Local-only connector-unavailable Probe Engine metrics `verification_gap.vg`, `context_entropy.ce`, `fixtures_coverage.coverage`, and `churn` remain explicitly unmeasured.

## 5. Improvement opportunities

1. Add a durable review-disposition record for each cross-story constraint, tied to the exact rule identity/revision and carrying provenance.
2. Preserve human ownership of semantic compliance while requiring a current disposition for `severity: required` at an appropriate deterministic qualification boundary.
3. Add tests for pending, reviewed, waived, stale-after-edit, and duplicate/index cases.
4. Remove or relocate the root scratchpad and guard against temp-derived Python files that bypass the declared lint/test surfaces.

## 6. Weakest boundary

**Weakness type:** Implicit Dependencies

The weakest boundary is the handoff from a machine-readable `required` cross-story obligation to an out-of-band human review. The repository truthfully marks the semantic check as not evaluated, but the examined deterministic state cannot prove whether the required human review was actually discharged.

## 6.5. Problem classification (fog type)

`architecture_fog`. The unresolved design question is how to represent human semantic judgment as durable, auditable state without converting that judgment into a false machine-generated compliance verdict.

## 7. Evidence

<!-- mode: investigative -->

State-currency backend: `github_connector_exact_sha_v1 @ 0653defb05625f2fcde0ac32eac6e59ccf7eeb90`.

Attempt-003 independently resolved the target commit after its durable `INVOKED` transition and re-read the decision-changing files at that exact SHA:

- `README.md:1-30` — blob `52babadc6422f5d491d27dd5927c192b6417605b` — deterministic ownership and narrative-engine purpose.
- `src/auteur/universe/models.py:18-52` — blob `9292b7da08484916772a2069e0129b1fb898b3a6` — required/warning/info severity model; required default.
- `src/auteur/series/universe_advisory.py:333-425` — blob `14d11929448bcbd406fbed6cec0eaa0ddd289701` — no semantic evaluation, always INFO/non-blocking, human review required.
- `src/auteur/series/handlers.py:148-228` — blob `d44f0d5034a04d31ff670650447595c0598a0f84` — notices flow into Series diagnostics; Series Bible blocks only ERROR.
- `tests/test_cross_story_constraint_notices.py:205-270` — blob `43ee358feba8aeaba7305e5ec819eb093189bf15` — human-review and non-compliance-claim behavior is regression-tested.
- `pyproject.toml:31-38` — blob `c6dcf42f259aae4c912a4f9e0528f6ee0f2ecc59` — configured pytest/Ruff scopes.
- `CUsersAdminAppDataLocalTempclaudeH--GithubRepositories-auteur62865e61-062c-4434-9de4-6f441dc6a9bascratchpadtest_validate_choices.py:1-12` — blob `7a786becd30233afc01ffb7430518e9b8843e3b5` — committed root quick-test scratchpad.

Logic trace: the model can declare a cross-story rule `required`; the advisory intentionally converts unresolved semantic checking into a non-blocking INFO human-review obligation; Series Bible compilation rejects only ERROR; therefore the deterministic compile boundary can succeed without encoding whether the required human review has been completed. The tests show this is deliberate semantic honesty, making the remaining weakness the external review-disposition dependency rather than an accidentally missing evaluator.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: src/auteur/universe/models.py
    lines: L18-L52
    quote: "see exact-SHA source lines"
    supports_claim: "Required severity is modeled and is the CrossStoryConstraint default."
  - file: src/auteur/series/universe_advisory.py
    lines: L333-L425
    quote: "see exact-SHA source lines"
    supports_claim: "Cross-story rules are deliberately not evaluated and always surface as INFO human-review notices."
  - file: src/auteur/series/handlers.py
    lines: L148-L228
    quote: "see exact-SHA source lines"
    supports_claim: "Series Bible compilation blocks ERROR diagnostics while cross-story notices remain INFO."
  - file: tests/test_cross_story_constraint_notices.py
    lines: L205-L270
    quote: "see exact-SHA source lines"
    supports_claim: "The repository explicitly tests non-evaluation and human-review semantics."
```

## 9. Why this boundary matters

Auteur's deterministic rails can distinguish schema failures and other blocking diagnostics, but they cannot currently distinguish two materially different human-process states for a required cross-story rule: reviewed versus merely surfaced. That weakens provenance at exactly the boundary where the system chooses, correctly, not to automate semantic judgment.

## 10. Candidate next steps

1. Define stable identity/currentness for cross-story review obligations.
2. Persist `pending|reviewed|waived` with actor/timestamp/source provenance.
3. Gate required obligations on the existence/currentness of a disposition, not on machine semantic compliance.
4. Add TDD coverage for missing/stale/reviewed/waived/duplicate constraints.
5. Clean and guard the root scratchpad boundary separately.

## 11. Recommended next step

Implement the smallest auditable cross-story review-disposition contract. Preserve `NOT_EVALUATED` semantics, keep substantive compliance human-owned, and make only the **review state** deterministic and machine-verifiable.

## 12. Recommended workflow

`implementation-workflow` in `guided_execution` mode, as verified in the frozen framework registry. The architecture/code work is deterministic, while the meaning of review/waiver should retain explicit human gates.

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
  - "src/auteur/series/universe_advisory.py (L333-L425, blob 14d11929448bcbd406fbed6cec0eaa0ddd289701): cross-story semantics remain intentionally unevaluated and INFO"
  - "src/auteur/series/handlers.py (L148-L228, blob d44f0d5034a04d31ff670650447595c0598a0f84): Series Bible compilation blocks ERROR only"
  - "tests/test_cross_story_constraint_notices.py (L205-L270, blob 43ee358feba8aeaba7305e5ec819eb093189bf15): semantic honesty is explicitly tested"
recommended_workflow_id: implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: "Required cross-story constraints depend on a human review whose completion/disposition is external to the examined deterministic compile path."
weakness_type: Implicit Dependencies
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-18T19:26:03Z"
immutable: true
```

## 14. Ready-to-copy prompt

Design and implement a minimal cross-story review-disposition contract for Auteur without automating semantic compliance. Preserve the existing `NOT_EVALUATED` honesty; identify each current rule stably; record `pending|reviewed|waived` with provenance; make `severity: required` require a current disposition at the appropriate deterministic qualification boundary; and add TDD coverage for missing, reviewed, waived, stale-after-edit, and duplicate/index cases. Separately remove or relocate the committed root scratchpad and add a narrow repository hygiene guard so temp-derived root Python artifacts cannot sit outside the declared test/lint policy unnoticed.
