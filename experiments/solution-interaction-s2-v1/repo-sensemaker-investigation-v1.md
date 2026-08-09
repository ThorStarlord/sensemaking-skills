# Repository Sensemaking Brief — superhero-netorare-parody @ 4f0b2a7c

Frozen owner question (S2): "Understand this repository and tell me what
engineering/product work would create the most value next."

## 1. Repository goal

A dark-themed adult Ren'Py visual novel ("Evil Get Fucked!", v0.1.0-prologue-demo)
with two routes — True MC (HW) and False MC (Marcus) — built on a dual-reading
narrative: every major scene must support both a liberation reading and a horror
reading (AGENTS.md "Dual Reading"). Part 1 is in Implementation/Production phase:
canon is frozen, consistency is treated as technical debt (AGENTS.md "Project
Phase"), and the owner's own documentation defines the first public-facing
milestone as a **polished standalone prologue demo** (CONTEXT.md L92-L94) whose
purpose is opening-hook validation — "test public response to the story's opening
promise at high quality" (CONTEXT.md L94-L96). The repository is simultaneously a
content project (Canon/ -> game/ pipeline with extensive agent governance:
Canon/Sandbox/Reference buckets, source precedence, trackers, ADRs) and a
production-tooling project (a ~50-script Python expression/asset pipeline with
ComfyUI generation, review packages, a runtime expression registry, and ADR-002
through ADR-005 governance).

## 2. Current shape

- **Ren'Py game** (`game/`): 127 `.rpy` files. Narrative in `game/scripts/`:
  `prologue/` (ch1-ch6), `arc1/` (54 files), `arc2/` (20), `arc3/` (50),
  `interlude1/`, `interlude2/`, `epilogue/`, `operative_gen/` (48),
  `false_mc/` (parent_gen 96 KB, daughter_gen 327 KB, heir_families 52 KB,
  special_campaigns 12 KB, big_reveal 11 KB), `core/` (backgrounds,
  characters, effects, variables, persistent_vars, expression_runtime),
  `dev/` (ADR-005 review galleries). Orchestration in `game/script.rpy`
  (route call chain + `mark_chapter`); UI in `game/screens.rpy` (47 KB: main
  menu, chapter select, gallery, roster, credits, end_of_demo); config in
  `game/options.rpy`.
- **Assets**: 97 backgrounds in `game/images/bg/`, 11 OGG tracks in
  `game/audio/` (all present, accepted in-game), 1 SFX, title/icon,
  `game/images/cg/cg_vesper_voss_acquisition.png` (the only CG), sprite trees
  under `game/images/sprites/` (bust/icon/master sets for iris, mirielle,
  adrien; vesper + harlan portraits; `archive/` with ADR-002/003/004 historical
  versions; nested duplicate trees `v2_integration/` and `v2_integration_fixed/`
  that recursively contain `game/images/sprites/...`).
- **Production pipeline** (`scripts/`): ~50 Python tools + `scripts/lib/`
  (comfy_client, expression_production, reference_guidance,
  visual_prompt_contract, schema_validation), including
  `build_runtime_expression_registry.py`, `promote_expression_batch.py`,
  `record_expression_review.py`, `semantic_alpha_validator.py`,
  `sprite_postprocess.py`, `regression_test.py`, `validate_expression_*.py`,
  and a growing family of `repair_*.py` scripts (5 tracked + 3 untracked in the
  working tree).
- **Runtime expression system (ADR-005)**: `game/scripts/core/expression_runtime.rpy`
  loads `state/runtime_expression_registry.json` (schema 1.0, adr_source
  ADR-004) at init -15, resolves character/expression/role via canonical IDs
  with fail-closed SHA-256 verification, exposes `show_expr()`
  (expression_runtime.rpy L27-L53). Registry contains `iris` (3 expressions,
  ACTIVE), `mirielle` (3), `adrien` (2). Dev-only gallery labels in
  `game/scripts/dev/` exercise the registry; the engine QA harness
  (`adr005_full_32_role_runtime_review.rpy`) covers 32 roles.
- **Governance layer**: `CONTEXT.md` (domain language, demo doctrine, music
  palette), `AGENTS.md` (source precedence, behavioral rules, visual prompt
  workflow), `CLAUDE.md`, `AUDIT-MATRIX.md` / `AUDIT-VALIDATION.md` /
  `AUDIT-IMPLEMENTATION-REPORT.md` / `AUDIT-CONFLICTS.md` (canon audit,
  2026-03), `docs/adr/` (0001, 0002, 0003, 0006, ADR-005), `Canon/`,
  `Reference/`, `Sandbox/`, `10_Human_Docs/`, `20_LLM_Docs/`, and a large
  `trackers/` suite (completion-tracker, audio-tracker, part1_asset_tracker,
  part1_missing_asset_matrix, dual-reading matrices d1-d23, distinctness
  audits, review packages under `review_packages/`).
- **Git state**: HEAD `4f0b2a7` on `feat/pilot-vesper-asset-production` (6
  commits ahead of origin/main; the "reusable expression production pipeline"
  merge b5d309c landed on origin/main 2026-08-08 — the same day as this probe).
  Working tree dirty with the owner's uncommitted local work.

## 3. Strong signals

1. **The demo navigation contract is already implemented.** `game/script.rpy`
   L2-L3: `if DEMO_BUILD: jump prologue_demo_start`; L20-L30 chains
   `false_mc_fpa` -> `false_mc_fpb` -> `end_of_demo`. `game/screens.rpy` L237
   shows only "START DEMO" in demo builds and hides CHAPTERS/GALLERY/CAST
   (L242-L246); the `end_of_demo` screen exists (L534) with deliberate
   copy. The structural skeleton the demo doctrine demands is in place.
2. **The rough build is functionally complete.** Completion tracker
   (trackers/completion-tracker.md L205-L207): Phase 1 backgrounds (96 PNGs),
   Phase 2 UI, Phase 2b gallery map, Phase 3 audio (11/11 OGGs placed and
   accepted in-game), Phase 4 credits, Phase 5 developer mode disabled,
   Phase 6 Windows distribution built and smoke test passed. All True MC and
   False MC chapters have `scene bg` calls, audio cues, and unlock wiring;
   D16-D23 campaigns are "Wired" (L129-L147).
3. **A real expression-production pipeline exists and is registry-governed.**
   ADR-005 (docs/adr/ADR-005-runtime-expression-integration.md, 2026-07-22,
   active) defines canonical character/expression/role IDs, explicit aliases,
   and fail-closed resolution with SHA-256 checks (expression_runtime.rpy
   L27-L53). The pilot vertical slice Vesper Rhodes / Harlan Voss is complete
   through QA and "Integrated" per trackers/part1_asset_tracker.md L19, with a
   rendering pipeline locked 2026-07-15 (L3-L6).
4. **Content discipline is institutionalized.** Source precedence hierarchy,
   Sandbox-to-Canon extraction protocol, dual-reading framework, genre
   validation rule (AGENTS.md), and a completed canon/reference/sandbox audit
   with PASS results (AUDIT-VALIDATION.md).
5. **Known runtime defect fixed.** The stale `errors.txt` (2026-07-25) compile
   error in `game/scripts/dev/adr005_expression_gallery.rpy` L43 (`xmaximum`
   invalid for `add`) is fixed in the current tree — the line now reads
   `add _adr005_resource_path(_role["path"]) maxsize (700, 520) fit "contain"`;
   the 2026-08-04 `log.txt` shows a clean load.

## 4. Missing pieces

1. **No character sprite is used anywhere in the story.** Grep over
   `game/scripts/` (excluding `core/` and `dev/`) finds zero `show_expr`
   calls and zero `show <character>` sprite statements. All narrative is
   text/NVL over backgrounds. The ADR-005 runtime is activated at HEAD but has
   no consumer in the actual game; the produced/approved expression assets
   (iris, mirielle, adrien in the registry; vesper/harlan per the part1
   tracker) appear nowhere in the story.
2. **The demo's minimum asset scope is entirely unproduced.** CONTEXT.md
   L120-L125 requires Marcus bust/sprite set, Elena bust/sprite set, HW
   bust/sprite set, and 2 CGs (breach hero spectacle; domestic HW scene).
   No marcus/elena/hw sprite files exist under `game/images/` (only
   backgrounds named after them); the only CG is `cg_vesper_voss_acquisition.png`
   (a True MC campaign character). Gallery screens show "Art Coming Soon"
   placeholders (screens.rpy L1284).
3. **The product has never been human-playtested end-to-end.** The "Tested"
   column is unchecked for every chapter row of the completion tracker, and
   the sole remaining release-checklist item is open:
   `- [ ] Fresh-persistent playthrough complete (both routes) - needs human
   testing` (trackers/completion-tracker.md L208).
4. **Demo-facing polish TODOs remain.** The `end_of_demo` screen states
   "Feedback form: to be added before public launch." (screens.rpy L569).
5. **The ADR-005 activation is unmerged, and the Vesper pilot is
   PENDING_INTERACTIVE_QA.** HEAD is 6 commits ahead of origin/main
   (feat/pilot-vesper-asset-production: Vesper C1 integration, QA packages,
   ADR-005 activation 2026-08-04); the pilot status was set to
   PENDING_INTERACTIVE_QA before human review (commit bad703d). The pipeline
   merge to main happened 2026-08-08 but not the pilot activation.
6. **Repair-script pattern signals pipeline friction.** Bespoke alpha/recrop
   repair scripts keep appearing: 5 tracked (`repair_adr004_iris_adrien_alpha.py`,
   `repair_mirielle_bust_icon_alpha.py`, `repair_remaining_adr005_roles.py`,
   etc.) plus 3 NEW untracked ones in the working tree
   (`repair_adr004_portrait_alpha.py`, `repair_adrien_bust_recrop_alpha.py`,
   `repair_iris_controlled_master_alpha.py`, and
   `create_mirielle_concerned_portrait_recrop.py`) — recurring defects in
   alpha/recrop output that are patched per-batch instead of at the source.
7. **Nested duplicate asset trees.** `game/images/sprites/v2_integration/...`
   and `v2_integration_fixed/...` recursively contain
   `game/images/sprites/...` copies (a zip-extracted-into-itself pattern),
   alongside `archive/` versions for ADR-002/003/004.
8. **Release hazard in the local tree.** `game/zz_local_developer.rpy`
   (excluded only via `.git/info/exclude` L50, i.e., NOT tracked) forces
   `config.developer = True` and `config.console = True` at `init 999`,
   overriding `options.rpy` L59 (`define config.developer = False`). Any Ren'Py
   build made from this working directory ships developer mode + console,
   because builds read the working tree, not git.
9. **Doc drift.** README.md's Release Checklist still marks Phases 3/4/6
   unchecked while the completion tracker records them done; README Quick
   Start references a Ren'Py 8.3.3 SDK path while the project runs 8.5.2;
   part1_asset_tracker.md L3 says `RENDERING_LOCKED_ASSET_GENERATION_STANDBY`
   and shows Mirielle/Adrien sprites unstarted, contradicting the ADR-004
   deployments present in the runtime registry.

## 5. Improvement opportunities

- Delete/archive the nested `v2_integration*` duplicate trees and prune
  `archive/` to ADR-final versions (small, safe hygiene; removes consumer
  confusion in the sprite namespace).
- Fold the recurring alpha/recrop fixes into `sprite_postprocess.py` /
  `semantic_alpha_validator.py` so repair becomes pipeline behavior, not
  per-batch patches.
- Add a release-gate check (script or pre-build checklist) that fails if
  `zz_local_developer.rpy` exists or `config.developer` is not False in the
  effective runtime.
- Reconcile README release checklist, completion tracker, and
  part1_asset_tracker statuses into one current state.
- Sync the runtime registry's character/expression set with the part1 tracker
  rows so "produced" means one thing across documents.

## 6. Weakest boundary

The weakest boundary is **Zero Validation at the product level**: the core
artifact — the playable story — has never been validated by a human end-to-end
(no fresh-persistent playthrough has ever been recorded; the Tested column is
empty for every chapter, and the release checklist's only open item is exactly
that playthrough), and the recently-built expression layer has never been
exercised by a real narrative scene (the runtime and its approved assets are
activated but story scripts contain zero sprite usage). The project's automated
validation machinery (sha256 fail-closed registry resolution, regression
harness, review packages) validates assets in isolation; nothing validates the
game as played.

**Weakness type:** Zero Validation

This matches the registered definition — "Core logic or structure that has no
automated check" (weakness-types.md L10) — extended to its product form: the
core logic (route flow, scene composition, sprite integration) has no
end-to-end validation, automated or human. The Ghost Features flavor (assets
and a runtime with no story consumer) is present, but the root cause is the
absence of validation of the integrated product, not the absence of
implementation.

## 6.5. Problem classification (fog type)

**primary_fog_type: product_fog.** The codebase's dominant uncertainty is
product-direction and product-sequencing, not structure: the owner's own
documentation (CONTEXT.md L92-L169) defines the next milestone (polished
prologue demo) and its production sequence (prose first, then Marcus/Elena/HW
assets), while the implemented trajectory since 2026-07-22 (ADR-004/005
pipeline, Vesper pilot, D16-D23 campaign wiring, pipeline merge to main on
2026-08-08) funds full-game production capacity instead. The demo exists to
validate an unvalidated opening promise (an empirical user-need question), and
the asset pipeline's mapping to product value is unproven in any scene. The
user's open question ("what creates the most value next") implies product
direction, and the codebase agrees — no ui_fog (no frontend framework; the
ui-fog registry's Tier 1 check fails at "no frontend code" — Ren'Py screens
are engine UI, not a design-system problem), no docs_fog (documentation is
extensive), and the architecture signals are real but subordinate: they are
consequences of product sequencing, not independent decision boundaries.

## 7. Evidence

**E1 — The demo milestone and its production sequence are documented and current.**
CONTEXT.md L92-L94: "The first public-facing target is a **polished prologue
demo** for Part 1, not a rough public playtest and not the full Part 1 release."
L120-L125 list the minimum asset scope: "Marcus bust/sprite set", "Elena
bust/sprite set", "HW bust/sprite set", two CGs. L137-L139: "Production
sequence for the polished prologue demo: lock prose/script quality before
final visual asset production. The public test depends first on whether the
opening promise lands in writing". The section was introduced 2026-06-30
(commit 731710e "Update release and demo planning docs") and is unchanged at
HEAD and on origin/main.
Logic trace: the owner's documentation establishes both WHAT the next product
milestone is and the ORDER its work must follow (prose -> assets -> public
test). Any recommendation that skips or reorders this sequence contradicts the
owner's recorded intent; any recommendation that funds other work as the
primary milestone does too, unless the owner has deliberately reprioritized.

**E2 — The implemented work trajectory diverges from the documented milestone.**
`docs/adr/ADR-005-runtime-expression-integration.md` L1-L4 (2026-07-22, active)
formalizes the expression runtime; the Vesper C1 pilot (Vesper Rhodes / Harlan
Voss) is complete per `trackers/part1_asset_tracker.md` L19 and L100-L104
(pilot vertical slice 2026-07-25, PENDING_INTERACTIVE_QA); HEAD
(`feat/pilot-vesper-asset-production`) is 6 commits ahead of origin/main with
the ADR-005 activation (2026-08-04), and the pipeline merge landed on
origin/main 2026-08-08. None of these produce the demo's required assets
(Marcus/Elena/HW) or its prerequisite (polished prologue prose).
Logic trace: the same repository contains a documented product priority (demo)
and a revealed engineering trajectory (pipeline + campaign production). Both
are current — the docs are unmodified since June 30 and the pipeline was
merged to main the same day as this probe. Repository evidence therefore
cannot by itself say which the owner intends to be the operative priority; that
is precisely the decision-changing owner-intent uncertainty Phase 4 of the
probe must surface — and it was surfaced via one neutral clarification (the
owner chose the demo milestone).

**E3 — The demo's binding constraint (per doctrine) is prose, and the demo
skeleton is implemented.**
`game/script.rpy` L2-L3 routes DEMO_BUILD to `prologue_demo_start` (L20),
which calls `false_mc_fpa` (L29-L30); `game/screens.rpy` L237 shows only
"START DEMO" in demo builds; `end_of_demo` (L534) exists with "Feedback form:
to be added before public launch." (L569). The False MC prologue prose is
written (game/scripts/false_mc/parent_gen/parent_gen.rpy L9 `label
false_mc_fpa`, L17 opening narrator line) but CONTEXT.md L112-L113 itself
labels the current build a "rough draft technical validation build".
Logic trace: the demo's structural skeleton is done, its writing is draft, and
its required assets do not exist. The documented sequence therefore points to
the prose-refinement pass as the next critical-path work, with the demo asset
set (Marcus/Elena/HW) produced against the refined beats afterward.

**E4 — The product has never been validated by a human playthrough.**
`trackers/completion-tracker.md` L208: "- [ ] Fresh-persistent playthrough
complete (both routes) - needs human testing" is the only unchecked release
item; the "Tested" column is unchecked for every chapter row (L10 header, rows
through L127). The 2026-08-04 `log.txt` records engine launches only.
Logic trace: every other release gate (backgrounds, audio, credits, build +
smoke test) is recorded complete, yet no human has played the game through.
The demo cannot be released against its own purpose (opening-hook validation)
without this step, and the expression layer's integration cannot be validated
any other way either — a first real playthrough is the cheapest probe that
converts the tracker's open item from risk into evidence.

**E5 — The expression layer is produced but unintegrated into the story.**
`game/scripts/core/expression_runtime.rpy` L27-L53 implements fail-closed
resolution (UNKNOWN_CHARACTER/UNKNOWN_EXPRESSION/MISSING_ROLE/HASH_MISMATCH
exceptions) and `show_expr()`; `state/runtime_expression_registry.json` L2-L13
(schema 1.0, adr_source ADR-004, characters iris/mirielle/adrien with
ACTIVE status). A recursive grep of `game/scripts/` finds zero `show_expr`
calls and zero character-sprite `show` statements outside `core/` and `dev/`
(gallery/QA labels only); the only CG is `cg_vesper_voss_acquisition.png`.
Logic trace: the pipeline has produced and approved assets and a runtime
contract, but no scene consumes them. The integration step — wiring approved
expressions into real scenes — is the missing link between pipeline investment
and product value; until it exists, "the pipeline works" is a claim validated
only in isolation, not in the product.

**E6 — Pipeline friction and tree hygiene are visible but secondary.**
Recurring bespoke repair scripts (5 tracked under scripts/, plus 3 new
untracked: `scripts/repair_adr004_portrait_alpha.py`,
`scripts/repair_adrien_bust_recrop_alpha.py`,
`scripts/repair_iris_controlled_master_alpha.py` in the working tree);
nested duplicate sprite trees `game/images/sprites/v2_integration/...` and
`v2_integration_fixed/...`; and a local-only `game/zz_local_developer.rpy`
(excluded via `.git/info/exclude` L50) that forces `config.developer = True` +
`config.console = True` at `init 999`, overriding `game/options.rpy` L59.
Logic trace: these are real but bounded issues. The repair-script pattern
raises the cost of producing the demo's three character sets (it will recur),
and the zz_local_developer file is a release hazard specifically at the moment
the demo build is made — both argue for a release-gate and pipeline hardening
as part of the demo work, not as a competing workstream.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: CONTEXT.md
    lines: L92-L94
    quote: "see file/lines"
    supports_claim: The polished prologue demo is the documented first public-facing milestone.
  - file: CONTEXT.md
    lines: L120-L125
    quote: "see file/lines"
    supports_claim: The demo's minimum asset scope is Marcus/Elena/HW bust/sprite sets plus two CGs; none of these exist.
  - file: CONTEXT.md
    lines: L137-L145
    quote: "see file/lines"
    supports_claim: The demo production sequence locks prose quality before visual asset production.
  - file: trackers/completion-tracker.md
    lines: L205-L208
    quote: "see file/lines"
    supports_claim: All release phases are complete except a fresh-persistent human playthrough of both routes.
  - file: trackers/part1_asset_tracker.md
    lines: L3-L19
    quote: "see file/lines"
    supports_claim: Asset production is at RENDERING_LOCKED_ASSET_GENERATION_STANDBY; Vesper Rhodes is the only fully complete character row.
  - file: game/script.rpy
    lines: L2-L3
    quote: "see file/lines"
    supports_claim: Demo builds jump to the prologue demo entrypoint, hiding the full route flow.
  - file: game/script.rpy
    lines: L20-L30
    quote: "see file/lines"
    supports_claim: The demo chains false_mc_fpa -> false_mc_fpb -> end_of_demo.
  - file: game/screens.rpy
    lines: L237-L246
    quote: "see file/lines"
    supports_claim: Demo build exposes only START DEMO and hides chapters/gallery/cast.
  - file: game/screens.rpy
    lines: L534-L569
    quote: "see file/lines"
    supports_claim: end_of_demo screen exists but the feedback form is still a TODO.
  - file: game/screens.rpy
    lines: L1284
    quote: "see file/lines"
    supports_claim: Gallery shows "Art Coming Soon" placeholder; no CG art exists for gallery entries.
  - file: game/options.rpy
    lines: L59
    quote: "see file/lines"
    supports_claim: Release config declares config.developer = False.
  - file: game/scripts/core/expression_runtime.rpy
    lines: L27-L53
    quote: "see file/lines"
    supports_claim: ADR-005 runtime resolves expressions fail-closed with SHA-256 and exposes show_expr.
  - file: game/scripts/dev/adr005_expression_gallery.rpy
    lines: L2-L43
    quote: "see file/lines"
    supports_claim: The dev gallery is registry-backed, developer-only, and its former compile error is fixed (maxsize).
  - file: game/scripts/false_mc/parent_gen/parent_gen.rpy
    lines: L9-L21
    quote: "see file/lines"
    supports_claim: The False MC prologue (demo slice) prose is written in draft form; no sprites are shown.
  - file: docs/adr/ADR-005-runtime-expression-integration.md
    lines: L1-L4
    quote: "see file/lines"
    supports_claim: ADR-005 (2026-07-22, active) formalizes the runtime expression integration.
  - file: state/runtime_expression_registry.json
    lines: L2-L13
    quote: "see file/lines"
    supports_claim: The runtime registry is ADR-004-derived and activates iris/mirielle/adrien expressions.
  - file: .git/info/exclude
    lines: L50
    quote: "see file/lines"
    supports_claim: zz_local_developer.rpy is excluded only locally, not tracked; it forces developer mode at init 999.
```

## 9. Why this boundary matters

1. **The demo's release gate is unvalidated product.** Every engineering gate
   is closed (builds, audio, backgrounds) but the one gate that determines
   whether the demo works as a product — a human playing it — has never been
   run. Releasing without it means the first public feedback loop is also the
   first time anyone discovers routing, pacing, or asset-integration failures.
2. **The expression pipeline's value is unproven where it matters.** Assets and
   a runtime contract exist with zero narrative consumers. If the pipeline is
   scaled to the demo trio (Marcus/Elena/HW) before any scene has exercised the
   runtime, the same class of integration defect that the repair scripts keep
   patching will compound inside the demo itself.
3. **The docs/behavior divergence silently changes project direction.** The
   documented milestone (demo) and the funded trajectory (full-game production
   capacity) have coexisted since July. Without surfacing it, "what creates the
   most value next" gets answered by momentum instead of intent — which is
   exactly the failure mode this probe exists to prevent.

## 10. Candidate next steps

1. **Prose-refinement pass on the demo slice** (false_mc_fpa/fpb) against the
   Canon practical outlines, per CONTEXT.md L137-L145's documented sequence.
   Cheapest critical-path work; unlocks asset production against stable beats.
2. **First fresh-persistent human playthrough of the demo slice** (owner
   action, ~1-2 hours): converts the tracker's only open release item into
   evidence and validates routing/demo navigation before public release.
3. **Produce the demo asset scope via the ADR-005 pipeline** (Marcus, Elena,
   HW bust/sprite sets + the two CGs) once prose beats are locked — reusing
   the Vesper/Harlan pilot pattern; includes a release-gate check that fails
   while `zz_local_developer.rpy` exists and a decision to fold repair-script
   patterns back into `sprite_postprocess.py`.
4. **Finish and merge the pilot work** (Vesper C1 interactive QA by the owner,
   then merge the ADR-005 activation from feat/pilot-vesper-asset-production)
   as enabling infrastructure — explicitly not the milestone.
5. **Continue full-game campaign production** (Calista Fenwick P0 per
   part1_missing_asset_matrix) — deferred unless the owner reprioritizes the
   full build-out ahead of the demo.

## 11. Recommended next step

With the owner's clarified intent (polished public prologue demo is the
milestone; pipeline work is enabling infrastructure), execute CONTEXT.md's own
production sequence: **(1) run the prose-refinement pass on the False MC
prologue demo slice (false_mc_fpa/fpb) against the Canon practical outlines,
and in parallel (2) run the first fresh-persistent playthrough of the demo
slice** — the two cheapest moves, both on the demo's critical path, both
required regardless of asset-pipeline outcomes, and together they convert the
two open risks (draft prose, zero playtest) into evidence. Only after prose is
locked, produce the Marcus/Elena/HW bust/sprite sets and the two demo CGs via
the existing ADR-005 pipeline (with the release-gate and repair-at-source
cleanup folded in), then ship the demo build with the feedback form wired and
zz_local_developer.rpy absent.

## 12. Recommended workflow

`product-implementation-workflow` (skills/workflow-planner/references/workflow-registry.yaml L644-L701; purpose: "For product/feature problems. Aligns domain, researches user needs, synthesizes opportunities, creates spec, and implements") — the closest structural vehicle for executing a documented product milestone, run in `plan_only` mode because the demo's spec already exists (CONTEXT.md + completion tracker) and the execution is content production (prose, assets, QA), which the registry's step chain (docs-aligner -> discovery -> opportunity-tree -> to-prd -> to-issues -> triage -> tdd -> handoff) only approximates. If the owner instead wants the milestone formally risk-reviewed before committing, `architectural-review-planning-workflow` (registry L942) is the fallback; the pipeline-hardening subset could also route through `autonomous-sprint-preflight` (L160), but that is not the milestone.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: "S2 owner-originated question: understand this repository and tell me what engineering/product work would create the most value next (frozen owner question, no PRE)"
user_implied_fog_type: product_fog
primary_fog_type: product_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "CONTEXT.md (L92-L94, L120-L125, L137-L145): polished prologue demo is the documented first public milestone; minimum asset scope is Marcus/Elena/HW sprites + 2 CGs; production sequence locks prose before assets"
  - "trackers/completion-tracker.md (L205-L208): all release phases done except fresh-persistent human playthrough of both routes"
  - "trackers/part1_asset_tracker.md (L3, L19, L100-L104): asset production at RENDERING_LOCKED_ASSET_GENERATION_STANDBY; Vesper/Harlan pilot slice complete; demo characters not in production"
  - "game/script.rpy (L2-L3, L20-L30) and game/screens.rpy (L237-L246, L534, L569): demo navigation contract implemented; feedback form TODO remains"
  - "game/scripts/core/expression_runtime.rpy (L27-L53) + state/runtime_expression_registry.json (L2-L13): ADR-005 fail-closed runtime activated with iris/mirielle/adrien; zero story usage of show_expr anywhere in game/scripts"
  - "game/screens.rpy (L1284): gallery shows 'Art Coming Soon' placeholder; only CG is cg_vesper_voss_acquisition.png"
  - "game/options.rpy (L59) vs .git/info/exclude (L50): config.developer=False in options, but local zz_local_developer.rpy forces developer mode+console at init 999"
  - "docs/adr/ADR-005-runtime-expression-integration.md (L1-L4): 2026-07-22 active; HEAD 6 commits ahead of origin/main with ADR-005 activation unmerged"
  - "game/scripts/false_mc/parent_gen/parent_gen.rpy (L9-L21): demo prologue prose is written draft; no sprites shown"
recommended_workflow_id: product-implementation-workflow
recommended_execution_mode: plan_only
weakest_boundary: "Zero Validation: the playable product has never been validated end-to-end by a human (Tested column empty for every chapter; the only open release item is the fresh-persistent playthrough), and the ADR-005 expression layer is activated but consumed by no narrative scene, so its integration is unvalidated too."
weakness_type: Zero Validation
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-08T23:50:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

For `workflow-planner` (plan_only) after this brief, against
`superhero-netorare-parody` @ 4f0b2a7c:

> Consume `experiments/solution-interaction-s2-v1/repo-sensemaker-investigation-v1.md`.
> Plan `product-implementation-workflow` in plan_only mode for the polished
> prologue demo milestone. Owner intent (recorded S2 clarification): the
> polished public prologue demo is the immediate milestone; the expression/
> asset pipeline is enabling infrastructure, not the milestone. Scope:
> (1) prose-refinement pass on `game/scripts/false_mc/parent_gen/parent_gen.rpy`
> labels `false_mc_fpa`/`false_mc_fpb` against the Canon practical outlines
> (CONTEXT.md L137-L145 sequence: prose first); (2) first fresh-persistent
> playthrough of the demo slice as an owner action; (3) after prose lock,
> produce Marcus/Elena/HW bust/sprite sets + 2 demo CGs via the ADR-005
> pipeline pattern (Vesper/Harlan pilot); (4) demo polish: feedback form on
> `end_of_demo` (screens.rpy L569), release-gate check that fails while
> `game/zz_local_developer.rpy` exists, fold repair-script patterns into
> `sprite_postprocess.py`, delete nested `v2_integration*` sprite trees;
> (5) rebuild + smoke test demo, then public release. Explicitly deferred:
> Vesper C1 interactive QA (owner action), ADR-005 activation merge, Calista
> P0 campaign production. Do not implement; produce the plan.
