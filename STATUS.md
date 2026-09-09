# Status

**Version:** 0.3.0  
**Last updated:** 2026-09-09  
**Current phase:** post-milestone qualification and operational dogfood  
**Primary program:** Sensemaking Campaign productization  
**Current frontier:** three-feature queue complete; no next product feature selected

Sensemaking Skills is an **agent-native engineering sensemaking and control layer**. The active coding agent owns semantic judgment; deterministic machinery owns representation, persistence, validation, provenance, integrity, authority checks, target identity, and reconstructible history.

## Current milestone baseline

The three-feature milestone is complete through the Feature-3 merge:

```text
Feature-3 merge commit
24a88bf6311122dae1257999f5a7379cb0b095d5

Feature-3 qualified tree
2bc8d7519656cd0fa1088825fbf2a8dbdf743a1e
```

That commit is the product-code milestone boundary. Documentation-only consolidation may move `main` without changing the qualified Feature-3 product tree.

### Completed Feature Queue

| Feature | Status | PR | Outcome |
|---|---|---:|---|
| CI Authority Reconciliation | MERGED | #298 | Product/lab validation authority reconciled; `pyproject.toml` remains sole literal version authority; installed-wheel tests belong to Product Validation; local `.claude/worktrees/` is ignored and stray gitlinks are rejected. |
| v0.3 Release Baseline Rebuild | MERGED | #299 | Current-main v0.3.0 release baseline rebuilt with installed validator runtime, wheel/sdist qualification, `twine check`, fresh-install proofs, schema-v2 compatibility, and current product/lab boundaries. Stale PR #294 was superseded instead of reused as release authority. |
| Durable Target Snapshot Binding | MERGED | #300 | Campaigns can bind exact target repository identity/worktree state, transitions bind source/destination target digests, drift fails closed, and lineage + handoff/resume preserve target provenance without semantic routing. |

All three approved Feature Queue items are complete. No fourth feature is implied or authorized by this status document.

## v0.3 product claim

v0.3.0 now provides a local, installable Campaign control layer with:

```text
campaign init/status/validate/history
campaign ingest
campaign advance/defer/close
campaign capabilities
campaign lineage
campaign reconciliation
campaign handoff/resume
durable target repository snapshot binding
setup-skills harness adapters
schema-v2 representation compatibility
installed canonical validator runtime
external real-harness evidence verification
```

The installed distribution carries build-derived canonical Skill trees and validator runtime so normal `campaign ingest` does not require a second Sensemaking source checkout.

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

target snapshot bound != repository correct
repository changed != repair succeeded
target identity != warranted responsibility
target drift != automatic transition
target provenance != capability selection or execution authority
```

The Campaign Controller is not a semantic router.

## Durable target snapshot binding

A Campaign initialized with `--target-repo` mechanically captures the target repository identity, Git HEAD/tree, deterministic worktree digest, dirty state, and a sanitized locator/identity source.

Repository mutation between decisions is legitimate. Each target-bound lifecycle transition records:

```text
from_target_snapshot_sha256
to_target_snapshot_sha256
```

Ordinary target-aware reconstruction detects unrecorded drift instead of silently accepting different repository bytes. Handoff/resume verifies the current target as part of fresh-context reconstruction, and lineage exposes current and transition target digests.

Historical Campaigns with no target fields remain honestly target-unbound. The additive schema-v2 contract does not invent past provenance or rewrite historical transition bytes.

See `docs/campaign-target-snapshot.md`.

## Campaign schema v2

Current Campaign artifacts emit schema version `2`.

Historical v1 representations are handled by deterministic one-way migration into the current in-memory representation. Migration can normalize already-sanctioned representation differences, but it cannot infer semantic meaning, select work, reinterpret evidence, or grant authority.

Append-only historical transition bytes are not rewritten merely to modernize representation. Migration qualification uses append-only receipts binding exact source bytes to the deterministic migrated payload.

See `docs/campaign-schema-evolution.md`.

## Shipped product / retained lab boundary — product/lab split

The v0.3 product/lab split keeps the shipped Campaign runtime distinct from retained source-only research machinery.

The core wheel contains the product/runtime surface and only its runtime dependencies (`click`, `PyYAML`). These research/lab packages remain source-only and are intentionally excluded from wheel discovery:

```text
sensemaking_skills.campaign_validation*
sensemaking_skills.campaign_accounting*
sensemaking_skills.exploratory_authorization*
sensemaking_skills.exploratory_execution*
```

Retained lab dependencies live in `requirements-lab.txt`.

The authority split is intentional:

- **Product Validation** owns shipped-product, installed-wheel, repository-contract, and filesystem-security claims.
- **Lab Validation** owns retained source-only research/lab claims.
- **Release Candidate Distribution** owns exact-head wheel/sdist release-candidate qualification.

See `docs/product-lab-boundary.md` and `docs/milestone-runbook.md`.

## CI and release authority

### Product Validation

`.github/workflows/validation.yml` runs for PRs/pushes to `main` and owns:

- Campaign product tests on Python 3.11 and 3.12;
- product/lab boundary validation;
- installed-core-wheel regressions;
- repository/Skill contracts and Probe Engine gate;
- Linux and Windows filesystem-security contracts.

### Lab Validation

`.github/workflows/lab-validation.yml` is path-filtered and manually dispatchable. It owns retained research/lab qualification and deliberately excludes `test_installed_wheel_*.py` from its broad Campaign selector.

If a release/milestone claim explicitly depends on retained-lab qualification and path filters did not trigger the workflow, a human operator must dispatch Lab Validation for the intended ref before making that claim.

### Release Candidate Distribution

`.github/workflows/release-candidate.yml` qualifies the exact PR head by:

1. asserting exact-head checkout;
2. validating release contracts, schema evolution, product/lab separation, and external qualification verifier behavior;
3. building wheel and sdist;
4. running `twine check`;
5. asserting exact `0.3.0` artifact names;
6. recording SHA-256 distribution digests;
7. clean-installing wheel and sdist;
8. proving CLI version/Campaign surface, schema v2, core/lab exclusions, packaged Skill trees, and packaged validator runtime;
9. uploading candidate artifacts.

A green run belongs only to the exact head it tested. If the candidate head moves, qualification must run again.

Tagged publication is a separate owner action. `.github/workflows/publish.yml` independently runs `twine check` before upload but does not decide whether publication is warranted.

## Release-version authority

`pyproject.toml` `[project].version` is the sole literal release-version authority.

`sensemaking_skills.__version__` derives from installed distribution metadata. `setup.py` contains only the build hook. `package.json` is private repository tooling metadata and does not declare the Python product version.

## Worktree boundary

`.claude/worktrees/` is local-only and ignored. Nested worktrees/mode-160000 gitlinks are not repository content.

Run:

```bash
python scripts/validate-product-boundary.py
```

before qualification to enforce the product/lab/version/worktree boundary.

## Real-harness qualification verifier

The release includes the real-harness qualification verifier implemented by `sensemaking_skills.external_qualification`. It verifies frozen evidence from a real coding-agent harness attempt. It checks:

- exact candidate, target, and runtime identities;
- SHA-256-bound evidence files;
- distinct Skill installation and native invocation evidence;
- canonical Campaign lifecycle checkpoints;
- no-manual-repair and no-prior-chat boundaries;
- fresh-context handoff/resume integrity;
- explicit PASS / FAIL / INVALID disposition.

Synthetic fixtures prove the verifier contract. They are not a real empirical harness run.

```text
fixture verifier PASS != real harness PASS
```

A real-harness PASS claim requires a real frozen external attempt.

See `docs/external-golden-path-verifier.md`.

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
| P11 — v0.3 release baseline | MERGED | Installed validator portability, current-main release contracts, exact-head distribution qualification, and release-doc reconciliation. |
| Post-P11 Feature Queue | COMPLETE | CI authority reconciliation, v0.3 baseline rebuild, and durable target snapshot binding all merged. |

## Definition of done — achieved for this Feature Queue

The three-feature queue is mechanically closed:

```text
Feature 1 merged
→ Feature 2 merged and exact-head release-qualified
→ Feature 3 merged and exact-head product/lab/distribution-qualified
→ post-milestone operational documentation consolidated
```

The supported product lifecycle is:

```text
start target-bound Campaign
→ repository diagnosis through agent-native Skills
→ validated artifact admission
→ agent-authored responsibility/authority decision
→ capability inspection
→ bounded work
→ deterministic destination target snapshot capture at explicit transition
→ durable evidence
→ reconciliation / repair verification
→ explicit disposition
→ transition
→ lineage inspection
→ handoff
→ fresh-context resume with target verification
→ continue or stop honestly
```

No next semantic responsibility or product feature is inferred by completing this sequence.

## Operator runbook

`docs/milestone-runbook.md` is the consolidated operator reference for:

- target-bound Campaign usage;
- exact local Product Validation commands;
- retained Lab Validation commands;
- release-candidate build/qualification commands;
- exact-head protocol;
- human-only merge/release/real-harness gates;
- harness setup and `--force` policy;
- worktree policy;
- failure interpretation.

When documentation and a checked-in workflow disagree on exact commands, the workflow is executable authority and the documentation should be reconciled.

## Canonical sources

- `README.md` — product entry point and quick start.
- `docs/milestone-runbook.md` — post-milestone operations and qualification runbook.
- `docs/sensemaking-campaign.md` — product model.
- `docs/campaign-target-snapshot.md` — target identity, drift, transition provenance, and fresh-context contract.
- `docs/productization-v0.3.md` — v0.3 delivery and release plan.
- `docs/campaign-schema-evolution.md` — schema compatibility.
- `docs/product-lab-boundary.md` — shipped/lab boundary.
- `docs/external-golden-path-verifier.md` — real-harness evidence verification.
- `docs/artifact-ingestion.md` — artifact admission and installed validator runtime.
- `.github/workflows/validation.yml` — Product Validation authority.
- `.github/workflows/lab-validation.yml` — retained Lab Validation authority.
- `.github/workflows/release-candidate.yml` — release distribution authority.
- `.github/workflows/publish.yml` — tagged publication mechanics.
