# Repository Sensemaking Brief

<!-- artifact_id: repository_sensemaking_brief | schema_version: 1 -->
<!-- runtime-generated skeleton created_at: 2026-07-27T15:43:38.956070Z -->

## 1. Repository goal

<!-- MODEL_SECTION:repository_goal:BEGIN -->

Auteur is an opinionated narrative-engineering toolkit for long-form fiction (`README.md:1-3`). It turns a raw premise into a validated `StoryIdentity`, compiles it into a `StoryBlueprint`, runs deterministic structural diagnostics, and optionally drives chapter outlining (Cartographer), TDD-style prose drafting with LLM critics, chapter/book reconciliation, and HTML/EPUB publishing (`README.md:5-23`). The canonical semantic architecture is Ontology -> Identity -> Structure -> Realization -> Expression (`README.md:296-310`, `AGENTS.md:59-77`), with three built-in interactive genre pipelines (netorare, mystery, gentlefemdom) sharing one runtime (`CONTEXT.md:1-60`). Beyond that original engine, the codebase has been extended release-by-release with a project-level narrative-planning layer -- impact analysis, decisions, review sessions, milestones, counterfactual simulation, and multi-decision portfolio comparison (`CHANGELOG.md:1-120`). The repository is evidently developed and maintained largely through autonomous/agentic subagent workflows (`CLAUDE.md:70-99`, `HANDOFF.md`, leftover temp-scratchpad files at repo root), which makes the fidelity of its own status documentation an operational concern, not just a cosmetic one.

<!-- MODEL_SECTION:repository_goal:END -->

## 2. Current shape

<!-- MODEL_SECTION:current_shape:BEGIN -->

`src/auteur/` contains roughly 55 subpackages (`structure`, `expression`, `reasoning`, `critic`, `provenance`, `pipeline`, `genre_pipeline`, `narrative_ontology`, `narrative_blueprint`, `narrative_realization`, `narrative_orchestration`, `universe`, `series`, `character`, `relations`, `editing`, `roundtrip`, plus the newer `decision`, `commitment`, `convergence`, `planning`, `review`, `impact`, `lifecycle`, `notify`, `simulation`, `portfolio`). `scripts/` holds 25+ `validate-*.py` checkers plus `check.py` (the documented local/CI verification entrypoint, `README.md:334-340`). `tests/` and `docs/` are both large: `docs/adr/`, `docs/architecture/` (per-release design + acceptance docs), `docs/acceptance/`, `docs/audits/`, `docs/design/`, `docs/handoffs/`, `docs/archived/superpowers/`. The top-level status documents are `README.md`, `CHANGELOG.md`, `CLAUDE.md`, `AGENTS.md`, `HANDOFF.md`, and `docs/audits/auteur-implementation-completeness-audit.md` (self-described as "the current implementation snapshot -- corrected after each release," `docs/audits/auteur-implementation-completeness-audit.md:653`). The shipped code version is `src/auteur/__init__.py:1` -> `__version__ = "0.35.0"`. The repository also carries a full parallel `skills/`/`artifacts/`/`docs/agents/` sensemaking-skills scaffold (the same machinery producing this very brief), which is a separate concern from the `src/auteur` narrative engine itself.

<!-- MODEL_SECTION:current_shape:END -->

## 3. Strong signals

<!-- MODEL_SECTION:strong_signals:BEGIN -->

- The layered architecture is substantively real, not scaffolding: `structure/analyzer.py`, `expression/book_reconciliation.py`, `bible.py`, `cartographer_compiler.py`, etc. exist and match what the docs describe.
- A genuine per-release documentation habit exists: `docs/architecture/v<version>-<name>-design.md` and matching `*-acceptance.md` files were produced for most releases from v0.8.0 through v0.22.0, and resumed at v0.33.0/v0.34.0.
- The completeness audit's own prior recommendation was actually acted on: it flagged `ReasoningRuntime` as "fully implemented and tested but never called from production code" (`docs/audits/auteur-implementation-completeness-audit.md:591`) and recommended wiring it in v0.3.0. Independent inspection of current code confirms this is no longer true -- `src/auteur/pipeline/runner.py:24-26,37-46,194-204` shows `PipelineRunner` now routes critic execution through `ReasoningRuntime` / `RuntimeRequest` instead of raw `run_critics()`. This is a positive signal: the team does close gaps it identifies, at least for code (not documentation).
- `CHANGELOG.md`'s own entries (through v0.12.0) report disciplined per-release test accounting, e.g. "Zero regressions: 3376 collected, 3348 passed, 27 xfailed, 0 failed" (`CHANGELOG.md:112`), suggesting the underlying engineering process is test-driven and typically well-tracked -- when the tracking step is actually performed.

<!-- MODEL_SECTION:strong_signals:END -->

## 4. Missing pieces

<!-- MODEL_SECTION:missing_pieces:BEGIN -->

- `CHANGELOG.md`'s newest entry is `## v0.12.0 (2026-07-22) — Narrative Decision Portfolio` (`CHANGELOG.md:5`). There is no entry for any of v0.13.0 through the current v0.35.0 -- 23 releases with zero changelog record.
- `docs/audits/auteur-implementation-completeness-audit.md`, the document explicitly designated as the doc that should be "corrected after each release," declares itself current as of v0.10.0 (`docs/audits/auteur-implementation-completeness-audit.md:5`, `**Version:** 0.10.0`) while its own concluding "Final Product Status Statement" section states `Auteur v0.6.0 is a **functional, release-quality narrative engineering platform**` (`docs/audits/auteur-implementation-completeness-audit.md:633`) and a different test-collection count (3,059 vs. the header's 3,286, lines 6 and 636) -- the file contradicts itself on version and test count before even being compared to the 0.35.0 codebase.
- `README.md`'s newest version-tagged CLI section is `### Compare counterfactual scenarios (v0.11.0+)` (`README.md:119`); v0.12.0's `portfolio` CLI subsystem (`auteur portfolio create/generate/project/compare/frontier/promote/status/inspect/list/history`, `CHANGELOG.md:29-40`) has no README section at all, nor does anything from v0.13.0 onward.
- `docs/architecture/` has a per-release design doc for v0.22.0 (`v0.22.0-chapter-structure-propose-design.md`) and then jumps straight to v0.33.0 (`v0.33.0-author-golden-path-design.md`) -- confirmed by directory listing: there is no `v0.23.0` through `v0.32.0` design or acceptance doc anywhere, a 10-consecutive-release documentation gap with no design doc, no changelog entry, and no audit update for any of them. There is also no v0.35.0 doc yet for the current release.
- No automated check anywhere in the repository enforces that `CHANGELOG.md`, `README.md`, or the completeness audit stay in sync with `src/auteur/__init__.py.__version__`. `scripts/check.py:10-14` runs exactly three commands (`test-validators.py`, `validate-repo.py`, `pytest`), none of which reads `__version__` or diffs it against `CHANGELOG.md`/`README.md`/the audit. `.github/workflows/validation.yml` runs `pytest` and a wheel smoke test only. `scripts/validate-repo.py:11-52` does perform file-existence/YAML checks, but its `core_files` list is entirely the `skills/`, `docs/agents/`, and `docs/mode-coverage.yaml` sensemaking-skills scaffold -- not `CHANGELOG.md` content, not the completeness audit, not `README.md`'s CLI section coverage.

<!-- MODEL_SECTION:missing_pieces:END -->

## 5. Improvement opportunities

<!-- MODEL_SECTION:improvement_opportunities:BEGIN -->

- Add a small `scripts/validate-release-docs.py` (or extend `validate-repo.py`) that fails CI whenever `src/auteur/__init__.py.__version__` has advanced past the highest version heading present in `CHANGELOG.md`, and/or whenever there is no matching `docs/architecture/v<version>-*-design.md` for the current version. This converts the invariant from "someone remembers to update three documents" into an enforced check, matching the pattern the repo already uses for every other artifact type (`scripts/validate-*.py`).
- Run a single reconciliation pass -- ideally via the `docs-contract-reconciliation` workflow -- to backfill `CHANGELOG.md` entries for v0.13.0 through v0.35.0 (using `docs/architecture/v*-*.md` where they exist as source material, and calling out the v0.23.0-v0.32.0 doc gap explicitly rather than inventing retroactive design docs for it), refresh `README.md`'s CLI reference to cover `portfolio`, `commitment`, and any commands added since v0.11.0, and correct `docs/audits/auteur-implementation-completeness-audit.md` so it no longer contradicts itself on version/test count.
- Once reconciled, fix the audit doc's internal self-contradiction (header "v0.10.0" vs. body "v0.6.0", line 5 vs. line 633) as part of the same pass, so a single document is never simultaneously current-as-of two different versions.
- Decide the scope boundary for `scripts/validate-repo.py` explicitly: either extend it to also validate Auteur's own release-doc invariants, or introduce a second, clearly-named validator so the name "validate-repo.py" does not imply repo-wide coverage it does not actually provide.

<!-- MODEL_SECTION:improvement_opportunities:END -->

## 6. Weakest boundary

<!-- MODEL_SECTION:weakest_boundary_prose:BEGIN -->

**Weakness type:** Zero Validation

The weakest boundary is the absence of any automated check tying Auteur's release-status documentation (`CHANGELOG.md`, `README.md`'s CLI reference, and `docs/audits/auteur-implementation-completeness-audit.md`) to the actual shipped code version (`src/auteur/__init__.py.__version__`). This is a **Zero Validation** gap specifically: the repository has a rich validation culture for almost everything else (25+ `scripts/validate-*.py` files covering plans, workflows, artifacts, run logs, prompt handoffs, and more), but none of that machinery, nor `scripts/check.py`, nor `.github/workflows/validation.yml`, ever compares `__version__` against the highest version referenced in the three status documents. Because the check does not exist, the drift accumulated silently and is now large: code is at v0.35.0; `CHANGELOG.md`'s newest entry is v0.12.0 (23 releases undocumented); the completeness audit -- the document explicitly designated to be "corrected after each release" -- is stamped v0.10.0 in its own header and contradicts even that by saying "v0.6.0" in its closing section; and `docs/architecture/` has a completely undocumented 10-release span (v0.23.0-v0.32.0) sandwiched between otherwise-present per-release design docs.

This is distinct from the fog-type classification in Section 13 (`primary_fog_type`): the underlying engine code is not broken or unclear (structure, expression, and reasoning wiring all check out on inspection) -- the boundary that is weak is the process boundary between "a release happens" and "the documents that claim to describe the release's state are updated," and no gate exists to catch a violation of that boundary.

<!-- MODEL_SECTION:weakest_boundary_prose:END -->

## 6.5. Problem classification (fog type)

Fog type is recorded in the machine-readable handoff block (Section 13), not here.

## 7. Evidence

<!-- MODEL_SECTION:evidence_prose:BEGIN -->

Ground truth for "what version is this repository actually at" is `src/auteur/__init__.py:1`, `__version__ = "0.35.0"`. Three separate status documents disagree with that ground truth in three separate ways. `CHANGELOG.md:5` shows the newest entry is `## v0.12.0 (2026-07-22) — Narrative Decision Portfolio`, and a targeted search for any heading matching versions 0.13 through 0.35 (`^## v0\.(1[3-9]|2[0-9]|3[0-9])\.`) returned zero matches anywhere in the file -- the gap is total, not partial. `docs/audits/auteur-implementation-completeness-audit.md:5` declares `**Version:** 0.10.0 (v0.10.0 update appended)`, yet the same file's closing section at `docs/audits/auteur-implementation-completeness-audit.md:633` states `Auteur v0.6.0 is a **functional, release-quality narrative engineering platform**`, and the two sections also disagree on collected-test counts (3,286 at line 6 vs. 3,059 at line 636) -- the audit is not merely stale, it is internally inconsistent even at whatever point it was last touched. `README.md:104-127` documents CLI usage through `v0.11.0+` (`auteur simulate ...`) with no section for v0.12.0's `auteur portfolio ...` commands (whose CLI surface is listed in `CHANGELOG.md:29-40`) or anything after. Finally, `docs/architecture/v0.22.0-chapter-structure-propose-design.md:1` and `docs/architecture/v0.33.0-author-golden-path-design.md:1` are the two design docs immediately bracketing a directory-listing-confirmed gap: no `v0.23.0` through `v0.32.0` design or acceptance file exists in `docs/architecture/`.

Before concluding this is a real, current gap rather than a stale observation of my own, I checked for evidence that would falsify it. First, I checked whether the specific "ReasoningRuntime not wired" finding the audit itself highlights (`docs/audits/auteur-implementation-completeness-audit.md:591`, "never called from any production code path") was still true, since if the audit's technical claims were still accurate that would weaken the "drift" framing -- inspection of `src/auteur/pipeline/runner.py:24-26,37-46,194-204` shows it is *not* still true: `PipelineRunner` now calls `_run_critics_via_runtime`, which builds a `RuntimeRequest` and calls `ReasoningRuntime.run(...)`, confirming the underlying code changed after the audit was written (which is expected and fine) but the audit was never updated to reflect it (which is the actual problem). Second, I searched for a possible alternate location for changelog-style entries (a `docs/changelog/` directory, per-version `NEWS.md`, etc.) and for a differently-named completeness-audit successor document, using broad filename globs across `docs/`; none turned up a document covering v0.13.0-v0.35.0 in aggregate the way `CHANGELOG.md` covers earlier releases -- the closest artifacts are the scattered per-version `docs/architecture/v*-design.md`/`*-acceptance.md` files, which are real but were never rolled up. Third, I checked whether CI or `scripts/check.py` might perform this reconciliation as a side effect of some other check rather than an explicit one; `scripts/check.py:10-14`'s three commands and `.github/workflows/validation.yml`'s two jobs (test matrix, wheel smoke) were read in full and contain no reference to `CHANGELOG.md`, `README.md`, or the audit file at all. This is a bounded, completed search (small, enumerable set of CI/verification entrypoints), not an exhaustive claim about every script in the repository, so I am treating the absence-of-check claim as well-supported rather than merely probable.

Logic trace: `src/auteur/__init__.py:1` establishes the actual current version as 0.35.0. `CHANGELOG.md:5` and a full-file regex search show the changelog stops at v0.12.0, which means every reader of `CHANGELOG.md` is missing 23 releases of history. `docs/audits/auteur-implementation-completeness-audit.md:5` and `:633` show the one document meant to be the reconciled, current snapshot is itself two-versions-inconsistent internally, which means even its own authors were not treating it as a single source of truth at the moment it was last edited. `docs/architecture/`'s v0.22.0 -> v0.33.0 jump shows the per-release design-doc habit itself lapsed for ten releases before resuming, meaning the drift is not a single missed step but a repeating pattern. Tracing why none of this was caught leads to `scripts/check.py:10-14` and `.github/workflows/validation.yml`, which is the repository's actual enforcement surface -- and neither one reads `__version__` or diffs it against any status document. Therefore the specific, actionable failure is: there is no automated gate between "a version bump ships" and "the documents claiming to describe the shipped state are updated," and that missing gate is why the drift was able to reach 23 releases without anyone (human or agent) being forced to notice it.

<!-- MODEL_SECTION:evidence_prose:END -->

<!-- REQUIRED: this section's prose must include a paragraph giving the diagnostic reasoning chain that connects the cited evidence to the weakest-boundary conclusion, starting with the exact two-word marker phrase specified in your execution instructions followed by a colon. validate-brief.py fails the whole artifact (error code NO_LOGIC_TRACE) if that reasoning paragraph is absent. -->

## 8. Evidence excerpts

<!-- MODEL_SECTION:evidence_excerpts:BEGIN -->

```yaml
<!-- REQUIRED: every item below must include file, lines, supports_claim (exact key names -- `citation` or similar does NOT satisfy this). Give the SMALLEST sufficient line range that contains the cited text -- do not invent paths. A `quote` key is also required by the schema, but its text does not matter: the runtime OVERWRITES it with the exact verbatim text read from file/lines before validation (issue #89) -- write a short placeholder like 'see file/lines' rather than trying to retype the source text yourself. validate-brief.py raises EVIDENCE_EXCERPT_FIELD per missing/misnamed key, per excerpt. -->

```yaml
evidence_excerpts:
  - file: src/auteur/__init__.py
    lines: L1
    quote: "__version__ = \"0.35.0\""
    supports_claim: "Establishes the actual current shipped code version as 0.35.0, the ground truth all other status documents are compared against."
  - file: CHANGELOG.md
    lines: L5
    quote: "## v0.12.0 (2026-07-22) — Narrative Decision Portfolio"
    supports_claim: "Shows the newest CHANGELOG entry is v0.12.0, 23 versions behind the actual __version__ 0.35.0, confirming the changelog has not been updated for any release since v0.12.0."
  - file: docs/audits/auteur-implementation-completeness-audit.md
    lines: L5
    quote: "**Version:** 0.10.0 (v0.10.0 update appended)"
    supports_claim: "The audit designated as 'corrected after each release' declares itself current as of v0.10.0, 25 releases behind actual code."
  - file: docs/audits/auteur-implementation-completeness-audit.md
    lines: L633
    quote: "Auteur v0.6.0 is a **functional, release-quality narrative engineering platform** with:"
    supports_claim: "The same audit document contradicts its own header (v0.10.0) by stating v0.6.0 in its closing 'Final Product Status Statement,' showing the doc was internally inconsistent even before comparing it to current code."
  - file: README.md
    lines: L119
    quote: "### Compare counterfactual scenarios (v0.11.0+)"
    supports_claim: "README's newest version-tagged CLI section is v0.11.0 (simulate); it documents nothing for v0.12.0's portfolio subsystem or any release after it."
  - file: docs/architecture/v0.22.0-chapter-structure-propose-design.md
    lines: L1
    quote: "# Auteur v0.22.0 — Chapter Structure Propose"
    supports_claim: "Confirms per-release design docs existed through v0.22.0, establishing one edge of the undocumented v0.23.0-v0.32.0 gap."
  - file: docs/architecture/v0.33.0-author-golden-path-design.md
    lines: L1
    quote: "# v0.33.0 — Author Golden Path Qualification"
    supports_claim: "Confirms the next per-release design doc after v0.22.0 jumps to v0.33.0, evidencing a completely undocumented 10-release gap (v0.23.0-v0.32.0) with no design docs, changelog entries, or audit updates for any of those releases."
  - file: scripts/check.py
    lines: L10-L14
    quote: "CHECK_COMMANDS = (\n    (sys.executable, \"scripts/test-validators.py\"),\n    (sys.executable, \"scripts/validate-repo.py\"),\n    (sys.executable, \"-m\", \"pytest\", \"tests\", \"-q\", \"--tb=no\"),\n)"
    supports_claim: "Shows the repository's local/CI verification entrypoint runs exactly three checks, none of which reads __version__ or diffs it against CHANGELOG.md, README.md, or the completeness audit -- confirming the Zero Validation gap."
  - file: scripts/validate-repo.py
    lines: L11-L17
    quote: "core_files = [\n        \"README.md\",\n        \"CONTEXT.md\",\n        \"LICENSE\",\n        \"CONTRIBUTING.md\",\n        \"docs/PRD-V1-Sensemaking.md\",\n        \"skills/repo-sensemaker/SKILL.md\","
    supports_claim: "Shows validate-repo.py's core_files check is existence-only (not content/version-sync) and is scoped to the sensemaking-skills scaffold rather than Auteur's own release-documentation invariants."
```
```

<!-- MODEL_SECTION:evidence_excerpts:END -->

## 9. Why this boundary matters

<!-- MODEL_SECTION:why_boundary_matters:BEGIN -->

This repository is developed largely through autonomous and subagent-driven workflows (`CLAUDE.md:70-99`'s "Continuous Execution Mode," `HANDOFF.md`'s self-reported "production-ready" status claims, and leftover per-session scratchpad files at the repo root). Agents and contributors who need to decide what to build next are explicitly pointed at `docs/audits/auteur-implementation-completeness-audit.md` as the canonical snapshot (it says so about itself) and at `CHANGELOG.md`/`README.md` for what already shipped. Right now, following that guidance is actively misleading: an agent that trusted the audit's "Recommended Next Implementation Phase" (wire `ReasoningRuntime` into production, `docs/audits/auteur-implementation-completeness-audit.md:587-627`) would spend a work session re-doing something already done in the current code, and could easily introduce a conflicting second wiring path or revert working behavior while "fixing" a gap that no longer exists. More broadly, 23 releases' worth of design intent (`portfolio`, `commitment`, `convergence`, `simulation` internals, and whatever shipped in the undocumented v0.23.0-v0.32.0 span) exists only in source code and tests, with no reconciled narrative anywhere -- meaning the next person or agent to touch those subsystems has to reverse-engineer intent from code alone, which is exactly the kind of silent-drift risk a narrative-engineering tool whose entire purpose is preventing "drift" (its own stated goal for authors' stories, `README.md:3`, `CONTEXT.md`) should be least tolerant of in its own process.

<!-- MODEL_SECTION:why_boundary_matters:END -->

## 10. Candidate next steps

<!-- MODEL_SECTION:candidate_next_steps:BEGIN -->

1. Reconcile documentation: backfill `CHANGELOG.md` entries for v0.13.0-v0.35.0 from `docs/architecture/v*-*.md` where available, explicitly flag the v0.23.0-v0.32.0 gap as unrecoverable-from-docs rather than inventing retroactive detail, update `README.md`'s CLI reference through the current command surface, and fix the audit doc's internal version/test-count contradiction.
2. Add an automated release-doc-sync check (new script or extension of `validate-repo.py`) that fails when `__version__` outruns the highest version referenced in `CHANGELOG.md` and/or when no `docs/architecture/v<version>-*-design.md` exists for the current version, and wire it into `scripts/check.py`'s `CHECK_COMMANDS`.
3. Decide and document the intended scope of `scripts/validate-repo.py` (Auteur's own contract vs. the embedded sensemaking-skills scaffold), so future contributors don't assume its passing means Auteur's release documentation is verified.
4. As a smaller, independent cleanup: correct the audit's self-contradicting version/test-count claims (line 5 vs. 633; line 6 vs. 636) even if the full backfill (step 1) is deferred, since an internally-inconsistent "canonical snapshot" is actively worse than an honestly-stale one.

<!-- MODEL_SECTION:candidate_next_steps:END -->

## 11. Recommended next step

<!-- MODEL_SECTION:recommended_next_step:BEGIN -->

Run a documentation-contract reconciliation pass across `CHANGELOG.md`, `README.md`, and `docs/audits/auteur-implementation-completeness-audit.md` against the current `__version__` (0.35.0) and the real command/module surface, explicitly enumerating the v0.13.0-v0.35.0 gap (including calling out the unrecoverable v0.23.0-v0.32.0 design-doc span as such rather than backfilling invented detail), and then add the missing automated version/changelog-sync check so the gap cannot silently reopen. Given the scope (23 undocumented releases across three documents), first produce a concrete plan enumerating exactly what changed release-by-release before writing any doc content, rather than editing directly.

<!-- MODEL_SECTION:recommended_next_step:END -->

## 14. Ready-to-copy prompt

<!-- MODEL_SECTION:ready_to_copy_prompt:BEGIN -->

```
We need to close the weakest boundary identified in the repository sensemaking brief: the
release-status documentation trail has fallen 23 releases behind the shipped code, with no
automated check preventing it. Concretely: src/auteur/__init__.py reports __version__ =
"0.35.0", but CHANGELOG.md's newest entry is v0.12.0, docs/audits/auteur-implementation-
completeness-audit.md is stamped v0.10.0 in its header (and self-contradicts with "v0.6.0"
in its own closing section), README.md's newest documented CLI section is v0.11.0
(auteur simulate), and docs/architecture/ has no per-release design/acceptance doc for
v0.23.0 through v0.32.0 (10 releases) despite having them for surrounding versions.

Please: (1) produce a plan enumerating, release by release from v0.13.0 to v0.35.0, what
actually shipped (using docs/architecture/v*-*.md where they exist, source diffs/tests
otherwise, and explicitly marking v0.23.0-v0.32.0 as undocumented-in-source rather than
inventing detail); (2) backfill CHANGELOG.md and update README.md's CLI reference and
docs/audits/auteur-implementation-completeness-audit.md accordingly, fixing the audit's
internal version/test-count self-contradiction as part of the same pass; (3) add an
automated check (new script or an addition to scripts/validate-repo.py, wired into
scripts/check.py) that fails when __version__ advances without a matching CHANGELOG.md
heading, so this gap cannot silently reopen. Do not modify src/auteur runtime behavior --
this is a documentation-and-verification task only.
```

<!-- MODEL_SECTION:ready_to_copy_prompt:END -->

## 12. Recommended workflow

See `recommended_workflow_id` in Section 13. Must match an id in workflow-registry.yaml. Do not invent workflow ids.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: architecture_fog
primary_fog_type: docs_fog
diagnosis_conflict: True
escalation_recommended: False
evidence:
  - "src/auteur/__init__.py (L1): __version__ = "0.35.0" -- ground-truth current version"
  - "CHANGELOG.md (L5): newest entry is v0.12.0, 23 versions behind __version__"
  - "docs/audits/auteur-implementation-completeness-audit.md (L5): declares itself v0.10.0"
  - "docs/audits/auteur-implementation-completeness-audit.md (L633): self-contradicts as v0.6.0"
  - "README.md (L119): newest documented CLI section is v0.11.0 (simulate); no portfolio (v0.12.0+) section"
  - "docs/architecture/v0.22.0-chapter-structure-propose-design.md (L1): last design doc before the gap"
  - "docs/architecture/v0.33.0-author-golden-path-design.md (L1): first design doc after the gap"
  - "scripts/check.py (L10-L14): CHECK_COMMANDS has no version/changelog-sync check"
  - "scripts/validate-repo.py (L11-L17): core_files check covers the sensemaking-skills scaffold, not release-doc sync"
recommended_workflow_id: docs-contract-reconciliation
recommended_execution_mode: plan_only
weakest_boundary: release-docs-version-drift
weakness_type: Zero Validation
weakness_type_explanation: None
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-07-27T15:43:38.956070Z"
immutable: true
```
