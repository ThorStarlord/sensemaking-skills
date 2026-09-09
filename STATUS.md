# Status

**Version:** 0.3.0  
**Last updated:** 2026-09-09  
**Current phase:** v0.3 release qualification  
**Primary program:** Sensemaking Campaign productization  
**Current frontier:** P11 — v0.3 release baseline

Sensemaking Skills is an **agent-native engineering sensemaking and control layer**. The active coding agent owns semantic judgment; deterministic machinery owns representation, persistence, validation, provenance, integrity, authority checks, and reconstructible history.

## Current release baseline

The v0.3 release-baseline branch is built from:

```text
main@36e9ea0e8e5bf0a56f5466113090978317bc0190
```

That baseline already includes:

- P0–P10 Campaign productization milestones;
- the **real-harness qualification verifier** merged by PR #295;
- **Campaign schema v2** and deterministic v1 -> v2 compatibility merged by PR #296;
- the shipped-core / retained-research **product/lab split** merged by PR #297;
- CI authority reconciliation merged by PR #298.

The earlier release candidate PR #294 was qualified against `main@d833095ab9b37bd9a93d39d286b358061eb913e5`. It predates all four changes above and is therefore superseded by the current-main release baseline rather than being merged or rebased as release authority.

## v0.3 release claim

v0.3.0 ships a local, installable Campaign control layer with:

```text
campaign init/status/validate/history
campaign ingest
campaign advance/defer/close
campaign capabilities
campaign lineage
campaign reconciliation
campaign handoff/resume
setup-skills harness adapters
schema-v2 representation compatibility
external real-harness evidence verification
```

The installed distribution also carries a build-derived canonical validator runtime so normal `campaign ingest` does not require a second Sensemaking source checkout.

## Semantic-control invariant

```text
warranted responsibility != available capability != authorized capability
validator passed != semantic conclusion is true
admitted evidence != warranted conclusion
lineage != semantic warrant
reconciliation evidence != Campaign decision
handoff != semantic recommendation
Skill copied to discovery root != harness observed/invoked Skill
external verifier PASS != semantic truth
```

The Campaign Controller is not a semantic router.

## Campaign schema v2

Current Campaign artifacts emit schema version `2`.

Historical v1 representations are handled by deterministic one-way migration into the current in-memory representation. Migration can normalize already-sanctioned representation differences, but it cannot infer semantic meaning, select work, reinterpret evidence, or grant authority.

Append-only historical transition bytes are not rewritten merely to modernize representation. Migration qualification uses append-only receipts binding the exact source bytes to the deterministic migrated payload.

See `docs/campaign-schema-evolution.md`.

## Shipped product / retained lab boundary

The core wheel contains the product/runtime surface and only its runtime dependencies (`click`, `PyYAML`). The following research/lab packages remain source-only and are intentionally excluded from wheel discovery:

```text
sensemaking_skills.campaign_validation*
sensemaking_skills.campaign_accounting*
sensemaking_skills.exploratory_authorization*
sensemaking_skills.exploratory_execution*
```

Retained lab dependencies live in `requirements-lab.txt`. Product Validation and Lab Validation are separate authority lanes.

See `docs/product-lab-boundary.md`.

## Real-harness qualification verifier

`sensemaking_skills.external_qualification` verifies frozen evidence from a real coding-agent harness attempt. It checks:

- exact candidate, target, and runtime identities;
- SHA-256-bound evidence files;
- distinct Skill installation and native invocation evidence;
- canonical Campaign lifecycle checkpoints;
- no-manual-repair and no-prior-chat boundaries;
- fresh-context handoff/resume integrity;
- explicit PASS / FAIL / INVALID disposition.

The repository includes synthetic fixtures and integration tests that prove the verifier contract. Those fixtures are not represented as a real empirical harness run. A real-harness PASS result remains empirical evidence from a frozen external attempt.

See `docs/external-golden-path-verifier.md`.

## CI and release authority

### Product Validation

Owns claims about the shipped product:

- Campaign product tests on Python 3.11 and 3.12;
- product/lab boundary validation;
- installed-core-wheel regression tests through P11;
- repository/Skill contracts and Probe Engine gate;
- Linux and Windows filesystem-security contracts.

### Lab Validation

Owns retained source-only research/lab claims. Installed-wheel product tests are excluded from its broad campaign-validation selector.

### Release Candidate Distribution

The release candidate workflow qualifies the exact PR head by:

1. asserting exact-head checkout;
2. validating release contracts, Campaign schema evolution, product/lab separation, and the external qualification verifier;
3. building wheel and sdist;
4. running `twine check`;
5. asserting exact `0.3.0` artifact names;
6. recording SHA-256 distribution digests;
7. clean-installing wheel and sdist;
8. proving CLI version/Campaign surface, schema v2, core/lab exclusions, packaged Skill trees, and packaged validator runtime;
9. uploading the candidate artifacts.

Tagged publishing independently runs `twine check` before PyPI upload.

## Release-version authority

`pyproject.toml` `[project].version` is the sole literal release-version authority. `sensemaking_skills.__version__` derives from installed distribution metadata. `setup.py` contains only the build hook; `package.json` is private repository tooling metadata and does not declare the Python product version.

## Milestone status

| Milestone | Status | Outcome |
|---|---|---|
| P0 — Productization pivot | MERGED | Implementation-first Campaign direction. |
| P1 — Durable Campaign workspace | MERGED | Typed file-backed persistence and integrity. |
| P2 — Campaign service | MERGED | Recoverable lifecycle operations and reconstruction. |
| P3 — Campaign CLI | MERGED | Init/status/validate/history. |
| P4 — Validated artifact ingestion | MERGED | Canonically validated content-addressed evidence admission. |
| P5 — Agent-authored decisions | MERGED | Explicit advance/defer/close. |
| P6 — Capability registry | MERGED | Deterministic unranked capability inspection. |
| P7 — Handoff/resume | MERGED | Integrity-bound fresh-context reconstruction. |
| P8 — Evidence lineage | MERGED | Exact provenance and transition-consumption reconstruction. |
| P9 — Reconciliation lifecycle | MERGED | Mechanical reconciliation disposition visibility. |
| P10 — Harness adapters | MERGED | Explicit deterministic Skill discovery-root installation. |
| P11 — v0.3 release baseline | CURRENT | Installed validator portability, current-main release contracts, exact-head distribution qualification, and release-doc reconciliation. |

## v0.3 definition of done

The release baseline is mechanically qualified when the exact candidate head passes Product Validation, Lab Validation, and Release Candidate Distribution.

The product lifecycle it supports is:

```text
start Campaign
→ repository diagnosis through agent-native Skills
→ validated artifact admission
→ agent-authored responsibility/authority decision
→ capability inspection
→ bounded work
→ durable evidence
→ reconciliation / repair verification
→ explicit disposition
→ transition
→ lineage inspection
→ handoff
→ fresh-context resume
→ continue or stop honestly
```

A real external harness run can additionally be frozen and verified by the real-harness qualification verifier. That empirical event strengthens dogfood evidence but is not fabricated by release CI.

## Canonical sources

- `docs/sensemaking-campaign.md` — product model.
- `docs/productization-v0.3.md` — v0.3 delivery and release plan.
- `docs/campaign-schema-evolution.md` — schema compatibility.
- `docs/product-lab-boundary.md` — shipped/lab boundary.
- `docs/external-golden-path-verifier.md` — real-harness evidence verification.
- `docs/artifact-ingestion.md` — artifact admission and installed validator runtime.
- `.github/workflows/validation.yml` — product validation authority.
- `.github/workflows/lab-validation.yml` — retained lab authority.
- `.github/workflows/release-candidate.yml` — release distribution authority.
