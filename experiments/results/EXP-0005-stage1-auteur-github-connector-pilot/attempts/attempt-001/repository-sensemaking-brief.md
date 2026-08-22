# Repository Sensemaking Brief

## 1. Repository goal

Auteur is an opinionated narrative-engine toolkit for long-form fiction. At the pinned snapshot it combines an author-facing narrative compilation lifecycle with deterministic schemas, validation models, artifact writing, and optional downstream LLM-assisted creative stages. The repository's own framing makes deterministic execution rails and explicit author authority central to the design.

## 2. Current shape

The Python package lives under `src/auteur/`, with major surfaces for story identity, blueprints, Series/Universe continuity, genre pipelines, planning, outlining, drafting, and validation. Tests live under `tests/`, and `.github/workflows/validation.yml` defines a Python 3.11/3.12/3.13 test matrix plus an installed-wheel smoke test. `README.md`, `AGENTS.md`, `CONTEXT.md`, and architecture/release documentation describe the intended semantic ownership and verification discipline.

The target snapshot is `ThorStarlord/auteur@0653defb05625f2fcde0ac32eac6e59ccf7eeb90`, whose merge commit adds explicit human-review notices for Universe `cross_story_constraints`.

## 3. Strong signals

- The repository clearly separates deterministic validation from optional LLM work. `README.md:1-30` states that deterministic code owns schemas, project files, validation models, artifact writing, and retry flow.
- CI is substantive rather than decorative: `.github/workflows/validation.yml:9-52` runs the full pytest suite on Python 3.11, 3.12, and 3.13 and separately builds/installs the wheel for smoke testing.
- The new cross-story behavior is semantically honest. `src/auteur/series/universe_advisory.py:333-425` explicitly says a single Series cannot prove or disprove a cross-story invariant, emits only `UNIVERSE_CROSS_STORY_CONSTRAINT_NOT_EVALUATED`, and refuses to claim compliance.
- Focused tests protect that honesty. `tests/test_cross_story_constraint_notices.py:205-270` requires the explanation to say human review is needed, requires explicit non-evaluation language, and rejects generated pass/fail or compliance claims.

## 4. Missing pieces

The consequential unresolved boundary is not automated cross-story evaluation itself; the snapshot correctly refuses to fake that. The missing piece is an explicit, durable **review-disposition contract** connecting a configured required cross-story constraint to evidence that a human actually reviewed it.

`CrossStoryConstraint.severity` defaults to `required` (`src/auteur/universe/models.py:18-52`), but `surface_cross_story_constraints` always emits `INFO` and treats the configured severity as explanatory metadata only (`src/auteur/series/universe_advisory.py:333-425`). In the Series Bible compile path, only `ERROR` diagnostics block compilation (`src/auteur/series/handlers.py:211-228`). Therefore a required cross-story rule can be surfaced honestly yet remain unresolved while compilation succeeds. The examined path contains the notice, but not a machine-verifiable record that the requested human review was completed, waived, or still pending.

A secondary hygiene gap is also visible in the immutable root tree: `CUsersAdminAppDataLocalTempclaudeH--GithubRepositories-auteur62865e61-062c-4434-9de4-6f441dc6a9bascratchpadtest_validate_choices.py:1-12` is a committed quick-test scratchpad with a machine-local temp-path-derived filename. `pyproject.toml:31-38` scopes pytest discovery to `tests/` and Ruff to `src/auteur/**/*.py` plus `tests/**/*.py`, so this root-level Python artifact is outside both configured checks.

Under the authorized connector-native probe surface, local-only Probe Engine metrics `verification_gap.vg`, `context_entropy.ce`, `fixtures_coverage.coverage`, and `churn` are **unmeasured**. No values are inferred for them.

## 5. Improvement opportunities

1. Introduce a durable cross-story review-disposition artifact keyed to the exact Universe constraint (for example: pending, reviewed, waived) with reviewer/decision provenance, without pretending the underlying semantic rule was automatically checked.
2. For configured `required` cross-story constraints, make the compile/release boundary require an explicit disposition before treating the review obligation as satisfied; the human may still own the substantive judgment.
3. Add focused regression tests for the review-disposition lifecycle: unresolved required constraint, explicit review, explicit waiver, stale disposition after constraint change, and duplicate/index stability.
4. Remove or relocate the root scratchpad and add a lightweight repository hygiene guard for committed temp/scratch Python artifacts outside the declared test/lint surfaces.

## 6. Weakest boundary

**Weakness type:** Implicit Dependencies

The weakest boundary is the handoff from an explicit `required` cross-story constraint to an out-of-band human review. The code is admirably clear that it did **not** evaluate the rule, but the examined compile path has no equally explicit durable state proving that the required human responsibility was discharged. Correctness therefore depends on a human process outside the deterministic state machine.

## 6.5. Problem classification (fog type)

`architecture_fog`. The uncertainty sits at a system boundary: how a semantic constraint that cannot be mechanically decided should participate in deterministic compilation, provenance, and state transitions without turning human judgment into a false automated compliance claim.

## 7. Evidence

<!-- mode: investigative -->

State-currency backend: `github_connector_exact_sha_v1 @ 0653defb05625f2fcde0ac32eac6e59ccf7eeb90`. The exact target commit was resolved before synthesis, and every repository-content observation below was read with that exact ref. GitHub blob identities are preserved here:

- `README.md:1-30` — blob `52babadc6422f5d491d27dd5927c192b6417605b` — establishes the narrative-engine goal and deterministic/LLM ownership split.
- `.github/workflows/validation.yml:9-52` — blob `156561e860c38c5d9ffb6ec8613ecfd04093eddd` — defines the 3-version pytest matrix and wheel smoke test.
- `src/auteur/universe/models.py:18-52` — blob `9292b7da08484916772a2069e0129b1fb898b3a6` — defines `required|warning|info` and defaults `CrossStoryConstraint.severity` to `required`.
- `src/auteur/series/universe_advisory.py:333-425` — blob `14d11929448bcbd406fbed6cec0eaa0ddd289701` — deliberately performs no cross-story compliance evaluation and always emits non-blocking `INFO` notices whose configured severity is metadata only.
- `src/auteur/series/handlers.py:148-228` — blob `d44f0d5034a04d31ff670650447595c0598a0f84` — appends those notices to Universe diagnostics and blocks Series Bible compilation only when diagnostics have `ERROR` severity.
- `tests/test_cross_story_constraint_notices.py:205-270` — blob `43ee358feba8aeaba7305e5ec819eb093189bf15` — asserts human-review wording, explicit non-evaluation, no outcome claim, and `INFO` severity.
- `pyproject.toml:31-38` — blob `c6dcf42f259aae4c912a4f9e0528f6ee0f2ecc59` — limits pytest to `tests/` and Ruff to `src/auteur/**` plus `tests/**`.
- `CUsersAdminAppDataLocalTempclaudeH--GithubRepositories-auteur62865e61-062c-4434-9de4-6f441dc6a9bascratchpadtest_validate_choices.py:1-12` — blob `7a786becd30233afc01ffb7430518e9b8843e3b5` — confirms the committed root-level scratchpad is real in the pinned tree.

The exact target commit is immutable snapshot evidence. A query for Actions workflow runs/statuses attached directly to this merge SHA returned no records through the connector, so this brief does **not** claim that the merge commit itself passed CI; it only verifies the checked-in CI contract. No mutable default-branch repository content is used as evidence.

Logic trace: the model permits a cross-story constraint to declare `severity: required`; the advisory implementation explicitly refuses automated semantic evaluation and normalizes every such obligation to a non-blocking `INFO`; the Series Bible handler blocks only `ERROR`; therefore the deterministic compile boundary can proceed while a required human-review obligation remains unresolved. The tests prove this is intentional semantic honesty, not an accidental missing branch. That makes the weakest boundary the **implicit external review process**, not the absence of an automated cross-story classifier. The root scratchpad is a real validation/hygiene gap, but it is less consequential because package build configuration includes `src/auteur` rather than the root scratchpad.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: src/auteur/universe/models.py
    lines: L18-L52
    quote: "see exact-SHA source lines"
    supports_claim: "CrossStoryConstraint supports required/warning/info severity and defaults to required."
  - file: src/auteur/series/universe_advisory.py
    lines: L333-L425
    quote: "see exact-SHA source lines"
    supports_claim: "Cross-story constraints are deliberately not evaluated automatically; every notice is INFO and configured severity remains metadata only."
  - file: src/auteur/series/handlers.py
    lines: L148-L228
    quote: "see exact-SHA source lines"
    supports_claim: "Cross-story notices feed Series diagnostics, while Series Bible compilation blocks only ERROR diagnostics."
  - file: tests/test_cross_story_constraint_notices.py
    lines: L205-L270
    quote: "see exact-SHA source lines"
    supports_claim: "Tests enforce semantic honesty: human-review wording, explicit non-evaluation, no pass/fail claim, and INFO behavior."
  - file: pyproject.toml
    lines: L31-L38
    quote: "see exact-SHA source lines"
    supports_claim: "Configured pytest and Ruff scopes exclude root-level scratch Python files."
```

## 9. Why this boundary matters

The repository correctly avoids making a false claim that one Series proves a cross-story invariant. But if a constraint is marked `required`, an INFO-only notice without durable review disposition leaves two materially different states indistinguishable at the compile boundary: “a human reviewed this and accepted/waived it” versus “nobody reviewed it.” That weakens auditability exactly where Auteur otherwise emphasizes explicit authority, provenance, and deterministic state transitions.

## 10. Candidate next steps

1. Specify a cross-story review-disposition schema tied to the exact Universe constraint identity and source revision.
2. Add an explicit acknowledgement/review transition for `required` cross-story notices, preserving the rule text and review provenance.
3. Gate the Series Bible or a later qualification boundary on disposition presence rather than on automated semantic compliance.
4. Add TDD coverage for stale/missing/waived/reviewed dispositions and constraint edits.
5. Separately clean the root scratchpad and add a repository hygiene assertion for stray temp-derived Python paths.

## 11. Recommended next step

Define the smallest durable cross-story **review-disposition contract** first: identify each constraint stably, record `pending|reviewed|waived` plus provenance, and require an explicit disposition for `severity: required` before the relevant deterministic qualification boundary passes. Keep substantive compliance judgment human-owned; the machine should validate only that the required review state exists and matches the current constraint revision.

This recommendation is based on the exact-SHA model/advisory/handler path above, not on a mutable tracker claim.

## 12. Recommended workflow

`implementation-workflow` — verified in the frozen framework workflow registry as the default architecture/code implementation workflow. Use `guided_execution` so the human-owned semantics of review/waiver remain explicit while the schema, state transition, and tests are implemented deterministically.

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
  - "src/auteur/universe/models.py (lines L18-L52, blob 9292b7da08484916772a2069e0129b1fb898b3a6): cross-story severity supports required/warning/info and defaults to required"
  - "src/auteur/series/universe_advisory.py (lines L333-L425, blob 14d11929448bcbd406fbed6cec0eaa0ddd289701): cross-story constraints are deliberately non-evaluated and always surfaced as INFO"
  - "src/auteur/series/handlers.py (lines L148-L228, blob d44f0d5034a04d31ff670650447595c0598a0f84): Series Bible compilation blocks ERROR diagnostics, not INFO human-review notices"
  - "tests/test_cross_story_constraint_notices.py (lines L205-L270, blob 43ee358feba8aeaba7305e5ec819eb093189bf15): semantic-honesty behavior is explicitly regression-tested"
  - "pyproject.toml (lines L31-L38, blob c6dcf42f259aae4c912a4f9e0528f6ee0f2ecc59): configured test/lint scopes exclude root-level scratch Python artifacts"
recommended_workflow_id: implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: "Required cross-story constraints depend on an out-of-band human review whose disposition is not represented in the examined deterministic Series compile path."
weakness_type: Implicit Dependencies
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-18T19:10:15Z"
immutable: true
```

## 14. Ready-to-copy prompt

Design and implement the smallest auditable cross-story review-disposition contract for Auteur. Preserve the existing rule that cross-story semantic compliance is **not** automatically evaluated. Give each current Universe cross-story constraint a stable review identity, record an explicit `pending|reviewed|waived` disposition with provenance, make `severity: required` require a current disposition at the appropriate deterministic qualification boundary, and add TDD coverage for missing, reviewed, waived, stale-after-edit, and duplicate/index cases. Do not convert human judgment into an automated pass/fail claim. Separately remove or relocate the committed root scratchpad and add a narrow hygiene guard preventing temp-derived root Python artifacts from bypassing the declared test/lint surfaces.
