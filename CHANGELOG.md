# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0-rc.3] - UNRELEASED

### Changed
- **Decision Journey Productization v1 (Issue #432)** — adds read-only `journey inspect`, caller-selected strategic/responsibility/execution/reassessment context packs, authored `strategic_decision_delta` reference checking, change-impact-to-observed-closure comparison, static beginner guidance, and canonical end-to-end playbooks. Preserves `reconstruction != causal truth`, `context pack != router`, `decision delta != mechanical verdict`, `impact difference != failure`, and `guide suggestion != automatic selection`.
- **Strategic Continuity Refinement v1 (Issue #430)** — deepens the completed Strategic Continuity baseline with typed mechanical currentness observations (`SOURCE_IDENTITY_CHANGED`, `EVIDENCE_REF_MISSING`, `EVIDENCE_REF_CHANGED`, `GOVERNING_AUTHORITY_REF_CHANGED`), deterministic `strategy history` / `strategy graph` projections over explicitly supplied analyses/reconciliations, and optional lightweight path-transition identity/reconciliation effects; preserves `observation != semantic consequence`, `graph edge != causal truth`, `path transition != roadmap item`, and adds no planner, scheduler, numeric score, automatic strategic reopening, Campaign schema change, or authority transfer.
- **Policy Hierarchy Interface Clarification v1 (Issue #426)** — adds the non-authoritative Adaptive Semantic Control Architecture crosswalk, canonical policy-responsibility matrix, adjacent-policy ownership distinctions, and explicit Strategic Continuity -> Learning/Reconciliation -> strategic-reassessment bridge; preserves Policy Hierarchy v0 and Issue #416 as completed baselines and adds no policy layer, runtime, schema, score, automatic strategic reopening, or authority transfer.
- **Issue #416 terminal closeout** — records the qualified/integrated Strategic Continuity, Reconciliation/Reserved-Decision, Multi-Repository Strategic Sensemaking, and Change-Impact packages; returns Level 3 to `NO_CHANGE / NORMAL_USE_HANDOFF` with no active construction program.
- **Change-Impact Sensemaking v1 (Issue #416 Package D)** — adds `change-impact-analysis` / `change_impact_analysis` for evidence-grounded affected-surface, verification/reconciliation, authority, closure, and bounded follow-up analysis around contemplated/completed changes; reference occurrence does not become impact truth, follow-up does not become backlog/authorization, and cross-repository impact does not expand scope automatically.
- **Multi-Repository Strategic Sensemaking v1 (Issue #416 Package C)** — adds `multi-repository-strategic-analysis` / `multi_repository_strategic_analysis` for explicitly selected repository sets, capability ownership/overlap maps, boundary tensions, coherent allocation/construction paths, and qualitative comparison while forbidding automatic repository discovery, target-scope expansion, numeric ranking, and cross-repository transaction/orchestration authority.
- **Strategic Reconciliation & Reserved-Decision Surfaces (Issue #416 Package B)** — adds `strategic-repository-reconciliation`, `owner-decision-capsule`, `thesis-review-packet`, and `external-evidence-packet` Skills/artifacts with mechanical boundary validation; returned evidence does not mutate strategy automatically, owner packets do not make owner decisions, thesis packets do not ratify Level-4 changes, and external evidence does not become repository truth.
- **Strategic Continuity & Currentness v1 (Issue #416 Package A)** — extends `strategic_repository_analysis` with optional explicit analysis lineage, decision assumptions, path assumptions, and reassessment triggers; adds deterministic root `strategy inspect|paths|uncertainty|assumptions|compare|drift` projections that never rank, select, authorize, invalidate, or automatically reopen strategy.
- **Strategic Repository Sensemaking v1** — adds the supported `strategic-repository-analysis` Skill and `strategic_repository_analysis` artifact for current-system modeling, capability/limitation mapping, 0–5 materially real construction paths, qualitative comparison, decision-changing uncertainty, and strategic synthesis without deterministic path ranking or execution authority.
- **Repository evolution routing** — keeps `repo-sensemaker` diagnostic while routing high-level “what could this repository become / how could it be constructed?” questions to strategic repository analysis; construction paths are capability-level trajectories rather than backlogs.
- **Policy Hierarchy Completion v0 begins** — explicit owner direction closes synthetic StrategicPlanner testing as the active mode and starts construction of the missing middle semantic-control layers without adding a generic runtime.
- **Inquiry Policy v0** — adds a canonical agent-facing contract for deciding what to learn next, including `NO_INQUIRY_NEEDED`, smallest-sufficient-evidence selection, owner-intent/external-evidence boundaries, and explicit inquiry stopping rules.
- **Metareasoning Policy v0** — adds the qualitative control-move layer (`ACT / INQUIRE / CHALLENGE / EXPLORE / VERIFY / ESCALATE / STOP`) without a runtime controller, score, or automatic routing.
- **Exploration Policy v0** — adds qualitative iterative-search allocation (`EXPLOIT / EXPLORE / CHALLENGE / DIAGNOSE / RECOMBINE / RESTART / VERIFY / EXIT_SEARCH`) over existing evidence/provenance without a SearchState schema, search-tree service, branch score, or automatic routing.
- **Warrant / Choice Policy v0** — adds target-specific, defeasible adjudication for claims, responsibilities, actions, continuation, closure, protected transitions, and strategic directions; preserves `warrant != authority`, supports `NO_SELECTION`, and introduces no WarrantEngine, scalar score, or automatic chooser.
- **Learning / Reconciliation Policy v0** — adds explicit evidence-return reconciliation across claims, uncertainty, responsibility, continuation/closure, and strategic/thesis state with `NO_MODEL_CHANGE`; reuses existing durable surfaces and adds no belief database, LearningEngine, or automatic semantic state mutation.
- **Stable Strategic Alternatives consolidation** — reuses Strategic Repository Sensemaking v1 rather than adding a planner; `construction_paths` now supports 0–5 materially real alternatives, with zero valid for non-`BUILD` dispositions and `BUILD` still requiring a selected real path.
- **Adaptive Policy Coordinator v0** — completes Policy Hierarchy v0 with progressive policy composition: expose only decision-relevant policy questions, permit zero explicit policy layers for obvious bounded work, and collapse ceremony when decision value disappears; no router, score, state machine, automatic Skill/workflow selection, or coordinator state store is added.
- **Post-RC2 development reopened** — current source advances to `1.0.0rc3.dev0` while preserving the exact qualified RC2 source/tree/artifacts as immutable historical provenance.
- **Next development program** — owner direction authorizes bounded product construction around execution handoff/result evidence, release-authority auditing, external-executor interoperability, provenance publication, and deterministic execution projections without creating a semantic planner or scheduler.
- **Release Authority Auditor** — adds local source/target/Git/document/workflow reconciliation without manufacturing CI, publication, semantic-truth, or owner-authorization claims.
- **Execution Interface v1** — adds append-only execution handoff and worker-result companions plus `campaign working-context`; worker return remains evidence for parent reassessment rather than global closure.
- **External executor interchange** — adds integrity-bound generic handoff/result envelopes and an AI Software Factory GitHub-Issue/command projection with caller-selected workflow.
- **Explicit GitHub provenance publication** — adds preview-by-default Issue/PR comment publication with explicit `--publish`, environment-token isolation, deterministic markers, and duplicate suppression.
- **Cross-repository execution projection** — adds read-only prerequisite edges/layers from explicit `depends_on` / `release_after` relations without selecting an execution plan or authorizing parallel work.
- **Execution Interface & Agent-Factorization v1 closeout** — all planned capability packages integrated and feature-integrated `main` passed Product, Lab, and Release Candidate Distribution validation; the program returns to normal-use validation after closeout qualification.

### Release status
- RC3 is development only; no RC3 candidate has been frozen or qualified.

## [1.0.0-rc.2] - 2026-09-18

### Changed
- **Release identity repair** — current repository development moves to `1.0.0rc2.dev0` while the next frozen candidate target is `1.0.0rc2`.
- **Relational release validation** — validators and distribution CI derive source/target identity from `pyproject.toml` and `release-v1.0.yaml` instead of hardcoding historical RC1.
- **Candidate immutability rule** — a qualified candidate version applies only to its exact source and artifact evidence; continued development must leave the frozen identity.

### Release status
- RC2 source identity is frozen as `1.0.0rc2`; qualification is exact-source evidence-bound and publication remains a separate owner-controlled transition.

## [1.0.0-rc.1] - 2026-09-13

### Added
- Reduced-scope `1.0.0-rc.1` release candidate with Campaign schema v2,
  deterministic migration, provenance, bundles, and package-boundary checks.
- Explicit generic Skill-format support with native harness and portability
  claims excluded pending real external evidence.

### Release status
- Exact source `70542d47412d98ee6dfae5de6df29bf271304568` was mechanically qualified as RC1.
- RC1 was not published to PyPI and was never final `1.0.0`.
- Continued development superseded RC1 as the identity of `main`; the historical qualification remains valid provenance for that exact source.
- Native-harness compatibility, portability, and semantic usefulness remained excluded/deferred under the reduced-scope support promise.

## [0.3.0] - 2026-09-09

### Added
- **Sensemaking Campaign control layer** — durable typed Campaign state, append-only transitions/trace, validated artifact admission, explicit agent-authored decisions, capability inspection, handoff/resume, evidence lineage, reconciliation reconstruction, and harness setup adapters.
- **Self-contained installed validation runtime** — wheel/sdist builds derive the canonical validator runtime from repository `scripts/`, `skills/`, and `docs/canonical-vocabulary.yaml`, so normal `campaign ingest` no longer requires a second Sensemaking source checkout.
- **Campaign schema v2 compatibility** — current artifacts emit schema v2; historical v1 Campaign artifacts can be deterministically migrated in memory and qualified through append-only migration receipts without rewriting historical bytes.
- **Durable target snapshot binding** — target-bound Campaigns persist sanitized repository identity, Git HEAD/tree, deterministic tracked/untracked worktree state, and transition source/destination snapshot digests; status/validation, lineage, and fresh-context handoff/resume fail closed on unrecorded target drift without turning provenance into semantic routing.
- **Real-harness qualification verifier** — `sensemaking_skills.external_qualification` verifies frozen real-harness evidence packages with exact candidate/target/runtime identity, SHA-256 binding, lifecycle checkpoints, fresh-context handoff/resume integrity, and explicit PASS/FAIL/INVALID dispositions.
- **Release-candidate distribution gate** — exact-head CI builds wheel and sdist, runs `twine check`, verifies exact artifact identities, clean-installs both distributions, checks schema-v2/core-lab boundaries, and uploads SHA-256-bound candidate artifacts.

### Changed
- **Product/lab split** — the shipped wheel contains only the Campaign product/runtime surface; retained research/experiment packages and their dependencies remain source-only lab infrastructure.
- **Release-version authority** — `[project].version` in `pyproject.toml` is the single literal release authority; runtime `sensemaking_skills.__version__` derives from installed distribution metadata.
- **CI authority** — Product Validation owns shipped-package, installed-wheel, repository-contract, and filesystem-security claims; Lab Validation owns retained source-only research claims.
- **Publishing workflow** — tagged builds use current GitHub Actions and run `twine check` before PyPI upload.
- **Version** — release authority advances from `0.2.2` to `0.3.0`.

### Claim ceiling
- `validator passed != semantic truth`
- `admitted evidence != warranted responsibility`
- `available capability != selected or authorized capability`
- `reconciliation evidence != semantic disposition`
- `lineage != semantic warrant`
- `handoff != semantic recommendation`
- `target snapshot bound != repository correct`
- `repository changed != repair succeeded`
- `target drift != automatic transition`
- `Skill copied to discovery root != harness observed/invoked Skill`
- `external qualification verifier PASS != semantic truth`

The repository contains the deterministic real-harness evidence verifier and its contract tests. A real-harness PASS result remains empirical evidence from a frozen external attempt; synthetic fixtures prove the verifier contract, not that such an empirical run has occurred.

## [0.2.2] - 2026-08-07

### Added
- **Skill trees shipped in the wheel** — the built wheel contains canonical `SKILL.md` trees under `sensemaking_skills/skill_trees/`, derived at build time from the authoritative repository-root `skills/` directory.
- **Drift detection in `setup-skills`** — installed skills are classified as `current`, `missing`, or `different`; divergent installed bytes are not overwritten without explicit `--force`.
- **Packaged-resource resolution** — `setup-skills` resolves source trees from installed package resources with a repository-root fallback for editable/source installs.
- **Installed-wheel distribution regression test** — fresh-wheel tests verify setup surface, packaged Skill bytes, and fail-closed drift behavior.

### Changed
- **Version bumped** from 0.2.1 to 0.2.2.

## [0.2.1] - 2026-05-25

### Added
- **CLI interface** with Click
  - `sensemaking-skills analyze`
  - `sensemaking-skills validate`
  - `sensemaking-skills test`
- **Source layout** under `src/sensemaking_skills/`.
- **CLI tests and documentation**.

### Changed
- Documentation was corrected to emphasize agent-native architecture and honest CLI boundaries.
- Packaging was reorganized for PyPI publication readiness.
- Version advanced from 0.2.0 to 0.2.1.

## [0.2.0] - 2026-05-25

### Added
- Honest documentation and packaging files.
- `setup.py`, `pyproject.toml`, `INSTALLATION.md`, and `GETTING_STARTED.md`.

### Changed
- Documentation was aligned with the actually implemented agent-native system.

## [0.1.0] - 2026-05-20

### Initial Release
- Agent-native diagnostic framework.
- Scenario 5 budget-exhaustion testing.
- Week 1 shadow-mode execution across 10 repositories.
- Repository sensemaking brief and workflow orchestration artifacts.
- Validation, bounded retry, and escalation behavior.

---

## Release posture

- **0.3.0** — first Campaign-based release baseline: shipped Campaign control layer, schema-v2 compatibility, durable target snapshot provenance, product/lab packaging separation, deterministic harness setup, installed validator runtime, and exact-head release qualification.
- **0.2.2** — wheel Skill-tree distribution repair.
- **0.2.1** — CLI/src-layout packaging.
- **0.2.0** — packaging/documentation foundation.
- **0.1.0** — initial agent-native framework.
- **Future 1.0.0** — stable release after broader runtime dogfood and compatibility evidence warrant stronger stability claims.