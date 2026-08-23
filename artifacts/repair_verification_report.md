# Repair Verification Report

Post-repair verification of the docs-contract-reconciliation run. The original
`repository_sensemaking_brief` (2026-08-22) is the acceptance criteria; each
original finding is re-checked against a fresh probe report.

**Verdict:** PARTIAL CLOSURE — most canonical/current-facing product-drift is
repaired; two sub-findings remain and are recorded as separate follow-ups
(F4 skill semantics; workflow-registry auto-invoke annotation), per owner
closure rule (do not weaken the criterion or manufacture a full PASS).

## probe_summary

Fresh measured state (`artifacts/probe-report-reconciliation-2026-08-22.yaml`,
generated 2026-08-23T00:46:47Z, validated `scripts/validate-probe-report.py` exit 0):

- git: `main @ 1171b19`; tracked=3889, untracked=69, dirty=14 (the applied patch).
- `verification_gap.vg = 0.67` — declared-but-unenforced checks exist (Contract
  Mismatch signal, pre-existing, not caused by this patch).
- `context_entropy.ce = 0.03` — no artifact-sprawl hygiene warning.
- `fixtures_coverage.coverage = 1.0`, `missing_fixtures = []` — no validator orphans.
- `vendored_skills`: 17 checked, 0 drift findings — skill-tree distribution in sync.

## findings_closed

- **Finding:** `integration_fog` defined as a fifth canonical fog type in the
  active enum.
  **Evidence:** removed from both `docs/canonical-vocabulary.yaml` and
  `src/sensemaking_skills/defaults/canonical-vocabulary.yaml` (fog_types,
  fog_type_decision_tree, `primary_fog_type.values`,
  `secondary_fog_types.values`). Verified live:
  `CanonicalVocabulary(Path('.')).get_enum_values('primary_fog_type')` →
  `['product_fog','ui_fog','architecture_fog','docs_fog']`; same for secondary.
  `rg integration_fog src/ scripts/` → 0 hits.
  `scripts/validate-fog-type-normalization.py` → PASS ("All fog types are in
  canonical form").

- **Finding:** stale behavioral assertion and docstring preserved `integration_fog`.
  **Evidence:** `tests/test_validation.py:40` assert removed (test now asserts the
  four ratified types); `tests/test_path_drift.py:143` docstring corrected.
  `python -m pytest tests/test_validation.py -q` → **20 passed**.

- **Finding:** positive fixture accepted a brief with `primary_fog_type:
  integration_fog`.
  **Evidence:** fixture moved to
  `tests/fixtures/validate-brief/invalid/integration-fog-brief.md` with
  `validator_case: negative` and `expected_error_contains: "value
  'integration_fog'"`. `scripts/test-validators.py` (exit 0) → this fixture
  `validate-brief.py integration-fog-brief.md negative ✅ PASS`; validator rejects
  it with `ERROR [unknown_value] primary_fog_type: ...'.

- **Finding:** `yolo_execution` presented as current product behavior.
  **Evidence:** `docs/canonical-vocabulary.yaml` `yolo_execution` annotated
  `compatibility_only: true` + status_note (legacy, ADR 0013);
  `skills/workflow-planner/references/execution-modes.md` row →
  `Compatibility/legacy` with the "not ratified product behavior" note. Still
  mechanically supported (runtime consumers unchanged).

- **Finding:** 30 registered skill IDs documented as real but unimplemented.
  **Evidence:** `skills/workflow-planner/references/skill-registry.yaml` now
  classifies all ghost ids: `triage` → `status: proposed` (still-proposed,
  current-doc consumer refs), 29 → `status: deprecated` (`tdd`, `ui-brief`,
  `ui-flow`, `ui-screen-spec`, `persona`, `discovery`, `interview-synthesis`,
  `competitive-analysis`, `opportunity-tree`, `hypothesis`, `customer-journey`,
  `prd`, `user-stories`, `acceptance-criteria`, `prioritize`, `roadmap`, `okr`,
  `lean-canvas`, `pricing`, `north-star`, `experiment-design`, `measure-pmf`,
  `ab-test-analysis`, `pre-mortem`, `launch-checklist`, `release-notes`,
  `stakeholder-update`, `gtm`, `battlecard`). 14 implemented ids untouched.
  YAML parses (44 ids); `scripts/validate-repo.py` → "Validation passed!".

- **Finding:** current-facing docs taught the wayfinder/orchestrator product and
  claimed production-readiness.
  **Evidence:** `README.md` maturity → "externally exercised / targeting
  externally validated"; stale "Roadmap to User-Ready" replaced with readiness
  statement; `docs/FAQ.md` production-ready + maintainer answers corrected;
  `docs/CUSTOMER_ONBOARDING.md` → HISTORICAL banner + re-scoped "What It Does";
  `GETTING_STARTED.md` ghost-skill (`triage`/`tdd`) references removed and the
  implementation example re-scoped to the ratified `docs-contract-reconciliation`
  subgraph.

## findings_remaining

- **Finding:** `skills/workflow-planner/SKILL.md` lines 87-100 still encode
  five-fog-type routing semantics, automatic fog-to-implementation mapping, and
  auto-invoke language.
  **Evidence:** file unmodified (was intentionally out of scope). `rg
  integration_fog skills/workflow-planner/SKILL.md` still matches; the skill
  contradicts the ratified four-type / recommendation-not-authority boundary.
  **Disposition:** deferred — F4. Requires an independently authorized
  skill-maintenance / owner-authorized skill-repair responsibility, not
  `sensemaking-docs-reconciler` (No-Side-Effects rule).

- **Finding:** `skills/workflow-planner/references/workflow-registry.yaml`
  `auto_invoke_next_workflow: true` entries present automatic downstream routing.
  **Evidence:** file intentionally not mutated in this patch (was outside the
  approved P1-P12 scope). Runtime reads these fields; they present the
  non-ratified automatic-routing it-language.
  **Disposition:** deferred — separate bounded follow-up (registry-compat
  annotation), recorded in this campaign's follow-ups.

## 13. Machine-readable handoff

```yaml
artifact_id: repair_verification_report
schema_version: 1
verified_brief_ref: artifacts/repository_sensemaking_brief.md
findings_closed:
  - finding: "integration_fog as a fifth canonical fog type in the active enum"
    evidence: "CanonicalVocabulary returns exactly four fog types; rg integration_fog src/ scripts/ -> 0; validate-fog-type-normalization PASS"
  - finding: "stale tests asserting integration_fog"
    evidence: "test_validation.py:40 assert removed; pytest tests/test_validation.py -> 20 passed"
  - finding: "positive fixture accepting integration_fog brief"
    evidence: "moved to invalid/ with validator_case: negative; test-validators PASS (negative)"
  - finding: "yolo_execution presented as current product behavior"
    evidence: "compatibility_only: true annotation in both vocab + execution-modes.md; runtime unchanged"
  - finding: "30 ghost skill ids documented as real"
    evidence: "skill-registry.yaml classified (1 proposed, 29 deprecated); 14 implemented untouched; validate-repo PASS"
  - finding: "current-facing docs taught wayfinder product / production-ready"
    evidence: "README, FAQ, CUSTOMER_ONBOARDING, GETTING_STARTED corrected/re-scoped"
findings_remaining:
  - finding: "workflow-planner SKILL.md encodes 5-fog routing + auto-invoke semantics"
    evidence: "file unmodified; rg integration_fog skills/workflow-planner/SKILL.md still matches"
    disposition: deferred
    reason: "F4 (issue #229) - skill semantics outside sensemaking-docs-reconciler authority; requires separate skill-maintenance/owner-authorized repair"
  - finding: "workflow-registry auto_invoke_next_workflow entries present automatic routing"
    evidence: "workflow-registry.yaml not mutated in this patch (outside approved P1-P12 scope)"
    disposition: deferred
    reason: "separate bounded follow-up (issue #230); annotated compatibility in a dedicated registry pass"
created_at: "2026-08-23T00:50:00Z"
immutable: true
```

## Closure interpretation

**PARTIAL CLOSURE.** The canonical/current-facing product-definition conflict
(the fifth fog type, ghost-skill documentation, yolo-as-ratified, production-ready
claims) is repaired and mechanically verified. Two sub-findings — the
`workflow-planner` SKILL routing semantics (F4, explicitly out of `sensemaking-
docs-reconciler` authority) and the `workflow-registry` auto-invoke annotation
(out of the approved P1-P12 scope) — remain as separate, independently-warranted
follow-ups. These do **not** indicate repair failure; they truthfully expose that
the original Ghost Features finding crosses two authority domains (documentation/
registry vs. Skill semantics), exactly as the owner anticipated. The closure
criterion is not weakened.
