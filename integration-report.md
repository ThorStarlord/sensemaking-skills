# Integration experiment report: cross-artifact relationship probing in the Probe Engine

- **Date**: 2026-08-12
- **Branch**: `feat/probe-engine-relationship-integration` (worktree
  `.claude/worktrees/probe-engine-integration`), based on `main` @ `90780f5`.
  The spike branch (`feat/spike-semantic-drift`) was used as evidence only.
- **Status**: experiment complete. NOT merged. No ADR filed.

## 1. Integration architecture chosen

A new canonical module `scripts/probe_relationships.py` (pure functions:
filesystem reads only, no network, no writes, YAML-safe dicts) exporting
one entry point `relationships(repo_root)`, wired into
`repo_probes.probe_all()` as one additive top-level report key:

    relationships:
      doc_surface: {total, live, by_class}
      version:     {declarations, subpackage_declarations, claims,
                    distinct_values, findings[]}
      adr:         {files, catalog[], references, findings[]}

Contract changes are strictly additive and deliberately small:

- `probe-repo.py` CLI: unchanged flags/exit codes; summary gains one
  line (`relationships: version findings=N adr findings=N ...`).
- `validate-probe-report.py`: REQUIRED_KEYS unchanged (unknown keys
  allowed — older reports without `relationships` still validate); new
  optional shape check `PROBE_REPORT_RELATIONSHIPS_SHAPE` (relationships
  must be a mapping with doc_surface/version/adr; findings lists with
  concept/finding_type/observations).
- Fixtures: `valid/sample.md` extended with the section;
  `invalid/relationships_malformed.md` added (harness: 73/73 pass).
- `skills/repo-sensemaker/SKILL.md`: Probe Engine step 5 — relationship
  findings are evidence candidates requiring semantic review; zero
  findings is a valid correct negative; cite like any measured value.
- Tests: `tests/test_probe_relationships.py` (14 tests), plus CLI-level
  coverage in the existing probe suite (58 passed total).

Full rationale (responsibility boundaries, alternatives, smallest-coherent
argument) is in `integration-design.md`.

## 2. What code from the spike survived conceptually

- Live-document surface discovery (bounded os.walk; ordered path-signal
  classifier historical/vendor/fixture/example/generated/candidate/live;
  live-only claim scanning; source_class provenance; surface counts).
- Version detector: declaration role (top-level package only, sub-package
  role), claim classification (current/historical/unknown), semver family
  filter anchored on product declarations, conflicting-values finding.
- ADR detector: 2-4 digit ids, `**Status**:` / `**Status:**` / `## Status`
  block forms, trailing-period tolerance, per-reference status window,
  duplicate-id per-entry findings, missing/unrecognized status findings.
- The evidence-candidate contract (concept / finding_type / observations
  with file:line provenance / confidence / requires_semantic_review /
  notes) and the invariant: probe → candidate, model → meaning.

## 3. What spike machinery was deliberately NOT carried over

- The network-capability detector (NOT READY per experiments 2-3).
- The probe's standalone CLI and drift-findings.yaml output format.
- The ~700-line spike file structure and its repo-specific scan lists.
- No graph/node/edge abstraction (none earned).

## 4. Probe-report contract changes

One additive top-level key (`relationships`, always present, possibly with
empty findings). Validator: optional-but-validated-when-present (older
reports and no-findings repos still validate). No REQUIRED_KEYS change.
No new ADR: the additive key fits within the schema's existing tolerance
(unknown keys allowed); no normative decision was forced.

## 5. sensemaking-skills results

```
version: declarations=4 claims=56 distinct=[0.2.0,0.2.1,0.2.2,4.1.0]
         findings=1 (conflicting_values, 18 observations)
adr:     files=24 references=202 findings=3 (status_claim_mismatch:
         docs/adr/0018:6, 0019:6, 0020:6)
doc_surface: total=839 live=141
```

Equivalent to the spike's final results, verified programmatically:
version declarations/claims/distinct identical and the observation
(source,value,kind) set is **identical**; ADR files/references/mismatches
**identical**; surface 839/141 **identical**. The spike's network finding
is absent by design.

## 6. auteur results

```
version: declarations=2 subpackage=2 claims=114 distinct=[0.37.1]
         findings=0 (correct negative)
adr:     files=18 references=15 findings=0 (catalog incl. duplicate 013)
doc_surface: total=511 live=143
```

Matches the spike's auteur results exactly (spike's lone network finding
absent by design). Correct negative: no product-version or ADR drift
exists on auteur's live surface; subpackage versions and the duplicate
ADR id remain visible in the section.

## 7. repo-sensemaker consumption evidence (A/B)

Two isolated bounded repo-sensemaker diagnoses of sensemaking-skills:
A without the relationships section, B with it.

- **Interpreted, not blindly adopted.** B accepted the version finding
  (pure measured fact; `requires_semantic_review: false` is correct for a
  literal value disagreement) and ACCEPTED the ADR findings WITH nuance:
  B established that 0018/0019/0020 (dated 2026-07-25) predate ADR 0014's
  2026-07-26 ratification — a date-ordered stale reference, not a
  substantive contradiction of routing policy. That interpretation is the
  probe's job to enable, not to make.
- **Sharpened the diagnosis.** B's weakest boundary became Vocabulary
  Drift (elevated "from suspicion to measured fact"), ruling out
  competing boundaries; A's boundary was Zero Validation (fixture
  coverage). Both are real; B did not lose A's finding (its next steps
  still include the 14/19 fixture gap). B additionally surfaced things A
  missed: `tests/test_cli.py:20` is stale AND never executed by
  `validation.yml`; `package.json:3` 4.1.0 vs pyproject 0.2.2 with no
  cross-checking validator; `docs/adr/README.md:3-4` "no script validates
  the **Status** line" — now mechanistically addressed by the ADR probe.
- **No noise introduced.** B rejected no finding; no false-positive class
  appeared solely because of integration.
- **No finding behaved as authoritative diagnosis.** B explicitly: "No
  finding is over-presented as authoritative. The version finding is
  stated confidently but is pure measured fact. Nothing is presented as a
  diagnosis requiring owner action beyond the evidence itself."
- **The durable Repository Sensemaking Brief remained the downstream
  boundary.** B's output is a brief; B confirmed workflow-planner consumes
  `primary_fog_type`/`recommended_workflow_id`, and relationship findings
  concern repo identity metadata, not brief field contracts.

## 8. False positives / noise

None in either evaluation repo. One carried-over, documented behavior
(the spike's conscious decision): when a repo has NO product-version
declaration at all (empty family anchor), current-state doc claims are
still compared against each other (docs-vs-docs drift), with
`summary.version_declarations`/`declarations: 0` signalling the missing
anchor. Kept for semantic equivalence with the spike; a future iteration
may lower confidence in that case.

## 9. Regressions

- Probe-neighborhood pytest: 58 passed (44 pre-existing + 14 new).
- Validator harness: 73/73 passed, 0 coverage failures (incl. the new
  negative fixture and the extended valid exemplar).
- Existing probe behavior for a repo with no relationship findings is
  unchanged: the section is always present with empty findings lists and
  the validator still accepts it (verified by the fixtures).
- Full-suite collection from a worktree remains blocked by the
  pre-existing Gate A path-containment environment property (unrelated to
  this change); scoped regression covers every touched surface
  (repo_probes, probe CLI, prompt injection, skill-distribution, validator
  fixtures, new module).

## 10. Newly exposed architectural boundary

- The Probe Engine now produces a second class of evidence: relationship
  findings with an explicit confidence/review contract, alongside the
  metric probes. Both are consumed identically (probe-report.yaml →
  repo-sensemaker semantic review).
- `docs/adr/README.md:3-4` ("no script validates the **Status** line")
  is now mechanistically false — a docs/state-currency drift the probe
  itself would flag on its own repository if run from a checkout whose
  docs claimed otherwise. Not repaired (discovery finding != repair
  authorization).

## 11. Recommendation

| Capability | Verdict |
|---|---|
| Version detector integration | **READY_TO_ADOPT** |
| ADR detector integration | **READY_TO_ADOPT** |
| Automatic document-surface discovery | **READY_TO_ADOPT** |

Basis: additive contract, byte-equivalent results on both evaluation
repos, 58 + 73 tests passing, no new false-positive class, and the
product-path A/B showing repo-sensemaker interprets the evidence, sharpens
the diagnosis, and keeps the brief as the boundary.

**Did integration produce evidence that a generalized semantic graph is
now needed? NO.** Every consumer operates on plain findings with
provenance; the A/B analysis needed no traversal or entity resolution.
The default answer remains NO.

---

Stop point reached. No merge to main was performed; no ADR was filed
(no normative architecture decision emerged — the contract extension is
additive within the schema's existing tolerance).
