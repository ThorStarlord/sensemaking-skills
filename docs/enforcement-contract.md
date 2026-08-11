# Enforcement contract: the canonical gate

- **Date**: 2026-08-12
- **Branch**: `feat/enforcement-gate` (based on `main` @ `08f091b`)
- **Status**: accepted engineering direction (owner), implementation on
  this branch; merge awaiting separate authorization.

## 1. The problem this addresses

Diagnosis (owner-level Sensemaking question, 2026-08-12): the repository
has substantial verification machinery, but too little of it participates
in the actual merge/CI gate. Evidence: the CI `validate` job explicitly
runs validation *scripts* and "does not execute a single pytest test"
(workflow comment); only a small handful of the repository's test files
run anywhere in CI; six README-declared verification entrypoints are in
no CI run step (`declared_in_ci` was empty); drift that existing tests
already detect (canonical-vocabulary coverage, gate-name canonicality,
fog-type consistency in `tests/test_path_drift.py`) is invisible because
those tests never run in CI.

## 2. What CI ran before this change (map)

`.github/workflows/validation.yml` (push/PR to main):

- `gate-a-tests-linux` / `gate-a-tests-windows`: a curated set of Gate A
  security suites (7 pytest files).
- `phase2-campaign-validation`: `tests/campaign_validation` +
  two-lane schema + path-containment characterization.
- `phase2-wheel-smoke`: installed-wheel smoke + distribution regression.
- `phase3-exploratory-authorization`, `phase4-campaign-ledger`,
  `phase4-windows-path-confinement`, `phase5-exp0001-preparation`,
  `phase6-execution-boundary`: the campaign/execution framework suites.
- `validate`: `scripts/validate-repo.py`, `scripts/test-validators.py`
  (the 73-fixture validator harness), run-log validation, failure
  analysis, mode-coverage self-validation. **No pytest.**

`.github/workflows/publish.yml`: tag-triggered PyPI publish (out of scope
for enforcement).

Canonical verification machinery NOT running anywhere in CI (as of the
map): the Probe Engine (`scripts/probe-repo.py`,
`scripts/validate-probe-report.py`), the relationship probes
(`scripts/probe_relationships.py`), and a large class of pytest suites
including `tests/test_cli.py`, `tests/test_repo_probes.py`,
`tests/test_probe_report_cli.py`, `tests/test_probe_relationships.py`,
`tests/test_skill_distribution_probe.py`, `tests/test_path_drift.py`,
`tests/test_field_contract_agreement.py`.

## 3. The canonical gate (this branch)

Two jobs added to `validation.yml`:

1. **`probe-gate`** — executes the canonical Probe Engine on the
   checkout: `probe-repo.py --output $RUNNER_TEMP/probe-report.yaml` ->
   `validate-probe-report.py` (shape) -> `gate_relationship_findings.py`
   (blocking policy). The report is written to the runner temp dir so the
   tree is never mutated.
2. **`core-assertions`** — the smallest stable pytest gate, currently:
   `test_repo_probes.py`, `test_probe_report_cli.py`,
   `test_probe_relationships.py`, `test_skill_distribution_probe.py`,
   `test_gate_relationship_findings.py`, `test_path_drift.py`,
   `test_cli.py`.

Not included deliberately: `tests/test_field_contract_agreement.py`
(needs the full SDK dependency set in this job — a future promotion), and
"run every pytest file" (an unstable everything-suite would get bypassed
and make enforcement worse). Expansion is incremental, and only suites
that are deterministically green-or-red in CI-equivalent conditions earn
inclusion.

## 4. Blocking policy for relationship findings

`scripts/gate_relationship_findings.py` is the ONLY place that decides
which finding types block. Promotion rule: a finding type may block only
if it is **mechanically decidable** AND the probe classifies it as **not
requiring semantic review** (`requires_semantic_review: False`).

Current blocking set (both earned under that rule):

| finding type | why it may block |
|---|---|
| `missing_reference` | a doc references an ADR id that does not exist; pure lookup, zero interpretation |
| `missing_status_line` | an ADR file has no `**Status**` line; breaks the convention every consumer relies on; pure shape |

Explicitly **evidence-only** (never block, even though mechanically
detected):

- `conflicting_values` (product version) — which declaration is
  authoritative (package.json vs pyproject vs `__init__`) is a policy
  decision not yet made.
- `status_claim_mismatch`, `unrecognized_status` — the probe itself flags
  these as requiring semantic review (which side is stale is
  interpretation); review-required findings never block.
- Anything the probe marks `requires_semantic_review: True`.

Semantic interpretation stays where the architecture put it:
repo-sensemaker. The gate blocks on mechanical contradictions; it never
decides what to fix.

## 5. Dogfood: expected red on current main

A gate that runs existing drift-detecting tests on the current committed
state is expected to fail on main until SEPARATE authorized repair
decisions are made. As mapped at branch creation (deterministic, not
flaky):

- `tests/test_cli.py::test_cli_version` — asserts the old CLI version
  string; the CLI prints the current one. Known-wrong assertion with
  known expected value (demonstrated-defect class), but repairing it is a
  separate decision (knowing how to fix it is not authorization to fix
  it).
- `tests/test_path_drift.py` (5 failures) — canonical-vocabulary coverage
  gaps (workflows, artifacts), non-canonical gate names in the workflow
  registry (`review_findings`, `review_recommendation`), fog-type
  naming inconsistency in docs. These are the registry/vocabulary
  disagreements the relationship probes surface independently.

These failures are evidence for separate repair decisions — not automatic
scope expansion. The gate being deterministically red is the point: the
next commits that touch these areas cannot silently ship green.

## 6. Promotion path for future invariants

Each future blocking invariant earns promotion independently:

- **Version declaration policy** — first decide the declaration
  hierarchy (which files are authoritative); then a `conflicting_values`
  policy can be added, or the probe's declaration-role logic extended.
- **Registry equality** — first establish which representation is
  canonical and which are mirrors/derived subsets (and whether the
  recommendable set must equal the registered set); then a deterministic
  equality/subset check can be promoted. Until the contract says what
  equality means, CI cannot decide it.
- **Status claims** — if the owner decides a status disagreement is
  always a blocker, the probe's `requires_semantic_review` flag for
  `status_claim_mismatch` must be revisited first; the gate must not
  contradict the probe's classification.
- **More pytest coverage** — promote suites incrementally; each must be
  deterministically green (or deterministically red with a registered
  repair decision) in CI-equivalent conditions before inclusion.

## 7. Non-goals

- No repairs of the findings the gate surfaces (separate decisions).
- No "all high-confidence findings block" rule.
- No "run every pytest file" rule.
- No routing/deployment changes (out of product scope per ADR 0014).
