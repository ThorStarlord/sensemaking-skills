# Repository Sensemaking Brief — Auteur (fresh repeated-use run 2026-08-14)

## 1. Repository goal

Auteur is an opinionated narrative-engineering toolkit for long-form fiction:
deterministic code owns schemas, validation models, artifact writing, and
retry flow; LLM calls provide creative planning, prose generation, and
critic judgment, inside a repeatable plan -> draft -> critique -> iterate
loop (README.md:3-29). The repository has a strong deterministic-authority
culture: explicit author confirmation before canonical mutation, atomic
persistence, provenance, and a six-state release-qualification policy
(docs/engineering/release-qualification.md:10-49).

## 2. Current shape

HEAD: `414435b9` (main). Package version 0.37.1 (pyproject.toml:7). Active
feature development continues (thematic contribution, canonical referents,
author-decision review passes; git log: 30529b9 + edb45f7/bd80d62/c996f84).
The release-evidence producer (`scripts/release_evidence.py`, candidate-
addressed evidence in docs/qualification-evidence/) is now committed
history (27c5282, 309a473). No new release since v0.37.1 (docs/releases/
contains only v0.37.0.md, v0.37.1.md).

## 3. Strong signals

- Release-qualification policy is current and prescriptive
  (release-qualification.md:61-107: exact release invariant, test
  accounting that must reconcile, baseline-failure classes, timeout
  semantics).
- Canonical suite evidence now exists mechanically: candidate 309a473
  artifact (docs/qualification-evidence/309a473...json) records 4252
  collected = 4224 passed + 1 skipped + 27 xfailed + 0 + 0 + 0,
  reconciles true, wheel PASS (mechanical, not hand-transcribed).
- Product code review culture is rigorous (named review passes F2/F3 in
  commit history; "complete-suite audit" fixes in earlier history).

## 4. Missing pieces

- No vendor/provenance contract found for the copied Sensemaking Skills
  machinery in this tree (see weakest boundary).
- docs/releases/ records v0.37.0 and v0.37.1 only; the release-evidence
  production path has not yet been exercised by a real release (the
  recorded next step: use `check.py --qualify` at the next release).

## 5. Improvement opportunities

- Decide the vendored-framework posture (document/de-vendor/sync).
- Adopt the release-evidence path in the next real release record.

## 6. Weakest boundary

**Weakness type:** Contract Mismatch

Auteur's committed tree contains a partial, diverging vendored copy of
Sensemaking Skills: 25 skill directories including vendored
`repo-sensemaker`, `problem-framer`, `sensemaking-docs-reconciler`,
`skill-maintainer`, `to-issues`, `to-prd`, `triage` (skills/ listing), plus
the vendored validator/registry scripts (scripts/validate-*.py,
scripts/workflow-execution-engine.py, scripts/orchestration-runner.py,
scripts/router.py). The copy is partial (no
skills/workflow-planner/references/artifact-contracts.yaml found) and has
drifted from the current framework (scripts/validate-repo.py differs from
the current sensemaking-skills version in import structure and content).
Most importantly, the vendored validator stack's own validation warns
about inconsistencies inside this tree: `python scripts/check.py
--skip-pytest` output reports "Workflow 'fast-path-workflow' contains a
recursive call to 'workflow-orchestrator'", "Workflow
'full-fog-workflow' contains a recursive call to 'workflow-orchestrator'",
and unregistered artifacts (ui_flows, screen_specs) in
'ui-implementation-workflow' — while still printing "Validation passed".

Logic trace: the repo's release-qualification promise is deterministic
correctness of its own product, and its check stack invokes this vendored
validator; the vendored validator itself flags registry inconsistencies in
the same tree it validates, and no vendor manifest or provenance record
was found to explain or bound the copy. Therefore the consequential
boundary is not the release-evidence producer (now closed, see Section 13)
but the undocumented, diverging framework copy whose own tooling reports
inconsistent state.

## 7. Why it matters

The next meaningful Auteur decisions are the next release and continued
feature work. The vendored snapshot means Auteur silently runs a second,
diverged verification vocabulary; framework improvements (including the
new release-evidence machinery, which lives in the same scripts/ tree)
interact with a stale copy whose own validation warns about itself.

## 8. Evidence

- skills/ listing: 25 directories incl. repo-sensemaker, problem-framer,
  sensemaking-docs-reconciler, skill-maintainer, to-issues, to-prd, triage
  (no workflow-planner; no skills/workflow-planner/references/
  artifact-contracts.yaml at the expected vendored path).
- scripts/ listing: validate-*.py stack, workflow-execution-engine.py,
  orchestration-runner.py, router.py, skill-execution-agent.py (vendored).
- scripts/validate-repo.py: import block differs from current
  sensemaking-skills scripts/validate-repo.py.
- `python scripts/check.py --skip-pytest` (2026-08-14): validate-repo.py
  warnings — recursive workflow-orchestrator calls in fast-path-workflow
  and full-fog-workflow; unregistered artifacts ui_flows, screen_specs in
  ui-implementation-workflow — followed by "Validation passed!".
- pyproject.toml:7 (0.37.1); docs/releases/ = v0.37.0.md, v0.37.1.md.
- docs/qualification-evidence/309a473...json: suite reconciles, wheel PASS.

## 9. Recommended next step

Owner decision on the vendored-framework posture (document the vendoring
contract and version boundary, or de-vendor/align), taken with the
repository owner; not implementation by the campaign.

## 10. Ready-to-copy prompt

Ask the Auteur owner: is the vendored Sensemaking Skills copy intentional
and where is its provenance/version contract recorded?

## 11. Candidate next steps

- Document the vendoring contract + pinned version (owner).
- Decide whether the vendored validator stack should remain in check.py.
- Continue the recorded next-release adoption of check.py --qualify.

## 12. Evidence rules

- State-currency: all measured claims from 2026-08-14 direct reads or
  command output; probe re-run not performed this run.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
primary_fog_type: architecture_fog
weakness_type: Contract Mismatch
weakness_type_explanation: partial, diverging vendored Sensemaking copy whose own validator warns about inconsistencies
recommended_workflow_id: fast-path-workflow
recommended_execution_mode: plan_only
escalation_recommended: true
escalation_reason: boundary is an owner decision about vendoring posture; fast-path-workflow is the closest diagnostic workflow match, plan_only for decision support only
evidence:
  - skills/ directory listing (25 dirs, partial vendored set)
  - scripts/ listing (vendored validator stack)
  - scripts/validate-repo.py divergence vs sensemaking-skills
  - check.py --skip-pytest validate-repo warnings (recursive workflows, unregistered artifacts)
  - docs/qualification-evidence/309a473...json (suite reconciles, wheel PASS)
  - docs/releases/ (v0.37.0, v0.37.1 only)
created_at: 2026-08-14T00:00:00Z
immutable: true
```

## 15. Extended analysis

- uncertainty: source repository_evidence, detail "vendor provenance contract not found; owner_intent whether the divergence is acceptable"
- owner_intent_state: status thin, known "owner runs a rigorous release culture; vendoring intent undocumented in scanned files"
