# Sensemaking Skills v0.3 Productization and Release Plan

**Status:** COMPLETE — P11 merged; post-P11 feature queue complete  
**Effective:** 2026-09-09  
**Release version:** `0.3.0`  
**P11 release merge:** `main@eab146b1b97adf5a106a4dae6c5602370b430f9c`  
**Current product-code milestone:** `main@24a88bf6311122dae1257999f5a7379cb0b095d5`  
**Current frontier:** post-milestone qualification and operational dogfood  
**Canonical product model:** [`sensemaking-campaign.md`](sensemaking-campaign.md)

This document records the completed v0.3 delivery/release baseline and its historical qualification boundaries. The durable definition of a Sensemaking Campaign remains in `sensemaking-campaign.md`. Later documentation-only commits may move `main`; they require their own exact-head validation and do not retroactively change which product-code trees were qualified.

## 1. Product direction

Sensemaking Skills is implementation/productization-first:

```text
identify user-visible capability
→ implement smallest complete vertical slice
→ validate mechanically decidable contracts
→ dogfood in ordinary engineering use
→ repair observed friction
→ ship the bounded slice
```

Formal experiments remain appropriate for consequential uncertainties that implementation and ordinary dogfood cannot resolve. Historical research keeps its actual claim ceilings.

## 2. Product boundary

The active coding agent owns semantic control. Deterministic machinery owns persistence, representation, validation, provenance, authority checks, structural reconstruction, and mechanically decidable integrity.

```text
warranted responsibility != available capability != execution authority
validator passed != semantic truth
provenance != semantic warrant
reconciliation evidence != Campaign decision
handoff != semantic recommendation
Skill copied to discovery root != Skill selected or authorized
external verifier PASS != semantic truth
```

No v0.3 release mechanism may become a centralized semantic router.

## 3. v0.3 north-star lifecycle

```text
start Campaign
→ repository diagnosis through agent-native Skill path
→ preserve/admit validated artifacts
→ record agent-authored responsibility and authority
→ inspect available capabilities
→ perform bounded work
→ preserve durable evidence
→ reconcile / repair-verify result
→ explicitly disposition evidence
→ record durable transition
→ inspect exact evidence lineage
→ hand off Campaign
→ resume in fresh context
→ continue or terminate honestly
```

The fresh agent reconstructs from durable Campaign state and canonical referenced evidence rather than prior conversation memory.

## 4. Integrated milestones

| Milestone | Status | Outcome |
|---|---|---|
| P0 — Productization pivot | MERGED | Implementation-first direction and preserved research claim ceilings. |
| P1 — Durable Campaign workspace | MERGED | File-backed typed state, append-only history, path containment, atomic replacement. |
| P2 — Campaign service | MERGED | Recoverable lifecycle commits, validation/reconstruction, handoff/resume primitives. |
| P3 — Campaign CLI foundation | MERGED | `init/status/validate/history`. |
| P4 — Validated artifact ingestion | MERGED | Canonical validation, content-addressed artifacts, append-only admission receipts. |
| P5 — Agent-authored decisions | MERGED | `advance/defer/close` persist explicit semantic judgment. |
| P6 — Capability registry | MERGED | Deterministic unranked capability/availability inspection. |
| P7 — Durable handoff/resume | MERGED | Fresh-context reconstruction with integrity binding. |
| P8 — Artifact/evidence lineage | MERGED | Exact identity/provenance and explicit transition-consumption reconstruction. |
| P9 — Reconciliation lifecycle | MERGED | Mechanical report-disposition visibility without semantic auto-routing. |
| P10 — Harness adapters | MERGED | Explicit deterministic setup roots for generic, Claude, Codex, and OpenCode environments. |
| P11 — v0.3 release baseline | MERGED | Current-main release hardening, self-contained installed validator runtime, release-contract reconciliation, and exact-head distribution qualification. |
| Post-P11 Feature Queue | COMPLETE | CI authority reconciliation, v0.3 baseline rebuild, and durable target snapshot binding all merged. |

## 5. Why the prior P11 candidate was superseded

PR #294 qualified a candidate rooted at:

```text
main@d833095ab9b37bd9a93d39d286b358061eb913e5
```

After that candidate was created, `main` gained four release-significant boundaries:

1. PR #295 — deterministic real-harness golden-path evidence verifier;
2. PR #296 — Campaign schema-v2 evolution/compatibility;
3. PR #297 — shipped product / retained research-lab packaging split;
4. PR #298 — CI authority reconciliation after that split.

Therefore the old candidate was not the release authority. v0.3 was rebuilt from the newer main line rather than merging or mechanically rebasing #294.

## 6. P11 — v0.3 release baseline

P11 carried forward only the still-valid release mechanics from the old candidate and requalified them against the current architecture of that release milestone.

### 6.1 Installed validator portability

Normal installed use of:

```text
sensemaking-skills campaign ingest
```

must not require a second Sensemaking Skills source checkout.

Builds derive a canonical validator runtime from the same repository sources used during development:

```text
scripts/                         → sensemaking_skills/validator_runtime/scripts/
skills/                          → sensemaking_skills/validator_runtime/skills/
docs/canonical-vocabulary.yaml   → sensemaking_skills/validator_runtime/docs/
```

This is build-derived duplication, not a second manually maintained implementation.

`--framework-root` remains an explicit development/compatibility override. Once explicitly supplied, an invalid override fails closed rather than falling back silently.

### 6.2 Release-version authority

The single literal release version is:

```text
pyproject.toml [project].version = 0.3.0
```

`setup.py` contains only the build hook. `package.json` remains private repository tooling metadata and must not declare the Python product version. Runtime `sensemaking_skills.__version__` comes from installed distribution metadata.

### 6.3 Campaign schema v2

The release baseline includes Campaign schema v2.

Historical v1 artifacts can undergo deterministic **v1 -> v2** representation migration. The migration layer may normalize sanctioned representation differences but may not:

- reinterpret evidence;
- choose work;
- infer responsibility;
- grant authority;
- rewrite append-only historical bytes merely to modernize serialization.

Append-only migration receipts bind exact legacy bytes to exact current representations.

### 6.4 Product/lab split

The wheel ships only the core Campaign product/runtime surface. Retained research packages remain source-only:

```text
campaign_validation
campaign_accounting
exploratory_authorization
exploratory_execution
```

Product CI owns installed-wheel claims. Lab CI owns retained research claims and must not accidentally rerun installed-wheel product suites in a source-only environment.

### 6.5 Real-harness qualification

The release includes `sensemaking_skills.external_qualification` and protocol `v0.3-external-golden-path-dogfood-v1`.

The verifier can qualify a frozen real external attempt by checking exact candidate/target/runtime identities, SHA-256-bound evidence, Skill setup and native invocation evidence, Campaign lifecycle checkpoints, no-manual-repair/no-prior-chat boundaries, and fresh-context handoff/resume integrity.

The integration fixture proves the verifier contract. **real-harness PASS evidence is empirical** and must come from a real frozen harness attempt; release CI does not manufacture that empirical event from a synthetic fixture.

## 7. Exact-head release qualification

A v0.3 candidate is mechanically qualified only when the same exact candidate head is green in all lanes required for the claim being made. A green result from an older head is historical evidence only and cannot be borrowed by later documentation or code changes.

### Product Validation

- Python 3.11 and 3.12 Campaign product suites;
- schema-evolution and external-verifier integration contracts;
- product/lab boundary validator;
- installed wheel smoke and P9/P10/P11 regressions;
- repository/Skill contract validator and Probe Engine gate;
- Linux/Windows filesystem-security suites.

### Lab Validation

- retained source-only research/lab suites on Python 3.11/3.12;
- Windows path-confinement proofs;
- installed-wheel product tests excluded from the broad campaign-validation selector.

### Release Candidate Distribution

The exact-head release lane must:

1. assert exact-head checkout;
2. run release-baseline contracts;
3. prove Campaign schema-v2 and external-verifier contracts;
4. prove product/lab boundary validity;
5. build wheel and sdist;
6. run `twine check`;
7. assert exact `0.3.0` artifact names;
8. record SHA-256 distribution digests;
9. clean-install wheel and sdist;
10. verify CLI version and Campaign surface;
11. verify schema version 2 in installed distributions;
12. verify source-only lab modules are absent from the wheel;
13. verify packaged Skill trees and canonical validator runtime;
14. upload the exact candidate artifacts.

## 8. Publication boundary

Qualification authorizes the code/release baseline, not automatic PyPI publication. Tagged publication remains a separate explicit owner action.

The tag workflow must build from the tag, run `twine check`, and only then upload with the configured PyPI token.

## 9. External empirical evidence after release-baseline qualification

The deterministic verifier is part of v0.3. A real external harness attempt may be frozen and qualified before or after publication depending on owner release policy.

Regardless of timing:

```text
fixture PASS != real harness PASS
real harness PASS != semantic truth
real harness PASS != universal harness compatibility
```

A real PASS supports only the bounded claim encoded by its frozen evidence package.

## 10. Explicit non-goals for v0.3

Do not add by default:

- centralized semantic routing;
- generic HTN planning;
- Skill ranking/automatic selection;
- critic/voting swarms;
- self-modifying Skills;
- autonomous Skill optimization;
- Campaign server/database/cloud backend;
- universal semantic truth validation;
- automatic external mutation authority;
- full multi-repository Campaign control.

## 11. v0.3 done condition

The P11 release baseline was completed when its exact candidate head passed Product Validation, Lab Validation, and Release Candidate Distribution with no manually repaired Campaign or distribution state and was merged.

Post-P11 changes do not inherit that qualification automatically. Any later candidate that is used to make a current release or milestone qualification claim must independently pass the relevant exact-head validation lanes.

Tag/publication remains an explicit owner-gated release action.
