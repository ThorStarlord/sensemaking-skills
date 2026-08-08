# Repository Sensemaking Brief — auteur (Task P3)

experiment_type: product_interaction
record: repo-sensemaker-investigation-v1
produced_by: canonical repo-sensemaker SKILL.md (sensemaking-skills @ d980bcdb, blob a5cb5dd7)
target_repository: auteur @ 374abb48fb1f39d1ddb140df9b43b34cf53f4beb
owner_question: "What engineering work would create the most value next?"
mode: agent-native, one-shot, read-only
created_at: 2026-08-08

---

## 1. Repository goal

Auteur is an opinionated narrative-engine toolkit for long-form fiction
(README.md:3). It coordinates high-level narrative-engine recommendation with
deterministic execution rails under a unified "narrative compilation
lifecycle": raw idea → opinionated interpretation → `story_identity.yaml` →
`blueprint.yaml` → structure diagnostics → optional cartographer outline →
optional chapter contracts → optional draft/critique/accept. The product
positions itself as "a literary compiler for long-form fiction"
(pyproject.toml:8) with deterministic code owning schemas, validation, and
retry flow, and LLM calls providing creative planning, prose generation, and
critic judgment (README.md:25-29).

## 2. Current shape

- **Version/identity**: `pyproject.toml:7` declares version 0.37.1. Release
  notes exist only for v0.37.0 and v0.37.1 (`docs/releases/`).
- **Source** (`src/auteur/`, 376 tracked files): large subsystem surface —
  `data` (26 files), `structure` (22), `genres` (19), `schema` (19),
  `narrative_orchestration` (16), `narrative_ontology` (15),
  `narrative_realization` (15), `narrative_blueprint` (15), `validator` (14),
  `portfolio` (13), `series` (13), `genre_pipeline` (12), `planning` (12),
  `decision` (11), `reasoning` (11), plus `book`, `character`, `commitment`,
  `convergence`, `lifecycle` areas and a large CLI layer
  (`cli.py`, `cli_dispatch.py`, `cli_parser.py`, `cli_handlers.py`).
- **Skills**: 67 tracked files under `skills/` including product skills
  (`audit`, `blueprint-to-cartographer`, `chapter-acceptance-testing`,
  `identity-validate`, `project-classifier`, `prose-critic-redline`) and a
  vendored copy of the Sensemaking Skills suite (`repo-sensemaker`,
  `docs-aligner`, `setup-sensemaking-skills`, `skill-maintainer`,
  `sensemaking-docs-reconciler`).
- **Docs**: `docs/architecture/` (31 files), `docs/superpowers/` (specs, 31),
  `docs/adr/` (18 ADR files), `docs/reviews/` (15 review/verification files),
  `docs/engineering/` (release qualification), `docs/releases/` (2).
- **Tests**: 290 tracked test files; v0.37.1 verification measured 3,729
  collected tests (3,701 passed, 1 skipped, 27 xfailed, 0 failed).
- **CLI surface**: identity/blueprint/structure commands, project init,
  cartographer compile/validate, draft/accept/retry, `plan` (project-level
  narrative planning), `simulate` (counterfactual scenarios), `portfolio`
  (multi-decision portfolio), `state`, `reasoning`, and three browser-based
  interactive genre pipelines (`netorare`, `mystery`, `gentlefemdom`).
- **Runtime residue**: 9,221 untracked root-level JSON reasoning reports
  (gitignored via `/*.json`), written by `ReasoningRuntime` when invoked with
  `report_dir=Path()` (src/auteur/pipeline/runner.py:45).

## 3. Strong signals

- **Deterministic-first engineering culture.** Pydantic contracts everywhere,
  20+ deterministic structure diagnostics, a full diagnose → propose → select
  → apply proposal lifecycle, and a 3,729-test suite with zero failures at
  v0.37.1. Release verification reports reconcile test inventories exactly
  (docs/reviews/v0.37-post-release-hardening-verification.md:102-112).
- **Authority discipline.** `StoryIdentity` is the canonical Layer 1 authority;
  recommendations are advisory until explicit author acceptance; the v0.37.1
  hardening made `--confirm` mandatory for every Layer-1-mutating command
  (docs/reviews/v0.37-post-release-hardening-verification.md:56-62). This is
  an unusually strong human-gate posture for an agentic product.
- **Spec-first governance.** 18 ADRs, approved design docs before
  implementation (AGENTS.md process rules), release qualification policy
  (docs/engineering/release-qualification.md), verification reports for each
  release, and preregistered evaluation protocols (pilot v2 H1-H6).
- **Provenance machinery.** Reasoning runtime with dependency layering,
  freshness/staleness tracking, revision snapshots, and author-facing review
  commands — the reasoning path itself was exercised in a bounded pilot
  (docs/pilot-report.md).
- **Working product surface.** The CLI works end to end for the deterministic
  path (identity → blueprint → structure diagnostics → cartographer outline
  compilation → chapter contracts), with real genre packs and interactive
  browser pipelines.

## 4. Missing pieces

- **Behavioral evidence for the creative core.** The full end-to-end authored
  path (accepted Scene Realizations, accepted prose, external edit,
  reconciliation) has never been traversed (docs/pilot-report.md:114-117), and
  the Cartographer pilot v1 "did not establish behavioral usefulness"
  (docs/superpowers/specs/2026-07-30-cartographer-agent-native-pilot-v2.md:20).
  The v2 evaluation is designed but blocked: "no provider or `compile_outline()`
  call" per execution (pilot v2 spec:41-42), and the latest review records that
  no capture exists because no API key was present — "Behavioral usefulness
  remains unproven" (docs/reviews/2026-07-28-cartographer-profile-emotional-target-evaluation.md:160).
- **Version/changelog accounting.** `CHANGELOG.md`'s newest entry is
  v0.12.0 (2026-07-22); versions 0.13.0 through 0.36.x (24 minor versions,
  released within roughly 6 days per the v0.37.1 review date) have no changelog
  entries. `docs/releases/` covers only 0.37.0/0.37.1.
- **README coverage of shipped features.** README documents the CLI through
  `simulate` (v0.11.0+); the `portfolio` subsystem (v0.12.0, 13 modules,
  `src/auteur/portfolio/cli.py`) is absent from README (0 matches for
  "portfolio") and from the "Status" feature list.
- **ADR numbering consistency.** Two files both titled "ADR 013":
  `docs/adr/013-series-graph-semantics.md` and
  `docs/adr/ADR-013-Universe-to-Series-Propagation.md`.
- **Vendored validator harness health.** `scripts/check.py` runs a vendored
  sensemaking-skills validator test suite where 21/30 cases fail; accepted as
  pre-existing fixture/environment issues under release policy
  (docs/reviews/v0.37-post-release-hardening-verification.md:116-140).

## 5. Improvement opportunities

- **Scope reasoning-report output.** `ReasoningRuntime` defaults
  `report_dir=Path()` (src/auteur/pipeline/runner.py:45), writing reports to
  the process CWD; 9,221 root-level JSON files accumulated since 2026-07-19
  (gitignored at .gitignore:37). A project-scoped or configurable default
  would keep runtime state out of repository roots.
- **Backfill changelog/release accounting** for v0.13-v0.36 and add README
  coverage for portfolio and later subsystems.
- **Rename the duplicate ADR-013** (e.g. `ADR-013-universe-to-series-propagation.md`
  or a new number) to restore the sequential ADR ledger.
- **Document the check.py 21/30 failure baseline** in a tracked file so the
  accepted-but-failing entrypoint does not silently become a release risk.

## 6. Weakest boundary

The weakest boundary is the **unproven behavioral value of the LLM-mediated
creative core** — the Cartographer/profile layer that the product's "literary
compiler" promise depends on. What is deterministic and schema-shaped is
extensively validated (3,729 tests, deterministic artifact validity 8/8);
what makes the product matter — whether the agent-native creative layer
produces structurally useful, repeatable differences for a real author — has
no automated check and no completed evaluation. The repository's own records
say so in three places: the 07-15 pilot ("full end-to-end authoring pilot is
not complete", docs/pilot-report.md:114-115), the v2 pilot spec ("It did not
establish behavioral usefulness", pilot v2 spec:20), and the latest
evaluation review ("Behavioral usefulness remains unproven", review:160).

**Weakness type:** Zero Validation

(Scoped meaning: the core value-creating logic — LLM-mediated outline/profile
behavior — has no automated check of its behavioral usefulness. Structural
validity is checked; behavioral value is not, and the evaluation designed to
check it is currently blocked on provider access, review:158-160.)

## 6.5. Problem classification (fog type)

**primary_fog_type: product_fog** — the dominant uncertainty is user value:
does the engine actually help authors produce better stories, and which
engineering work increases that value next? The architecture layer is
strongly governed (deterministic code, authority gates, ADRs); the docs layer
has real but secondary debt; the decision that matters is product-directional
(evidence-first vs. feature-velocity), which is product_fog.

---

## 7. Evidence

Observed evidence first, inference separately. Files actually read: README.md,
pyproject.toml, CHANGELOG.md, CONTEXT.md, AGENTS.md, .gitignore,
docs/pilot-report.md, docs/superpowers/specs/2026-07-30-cartographer-agent-native-pilot-v2.md,
docs/reviews/2026-07-28-cartographer-profile-emotional-target-evaluation.md,
docs/reviews/v0.37-post-release-hardening-verification.md,
docs/adr/013-series-graph-semantics.md, docs/adr/ADR-013-Universe-to-Series-Propagation.md,
src/auteur/pipeline/runner.py, src/auteur/reasoning/runtime.py, plus
`git ls-files`/`git log` surveys.

**Observed:**

1. `pyproject.toml:7` — `version = "0.37.1"`.
2. `CHANGELOG.md:5` — newest entry is `## v0.12.0 (2026-07-22) — Narrative
   Decision Portfolio`; no v0.13+ entries. `docs/releases/` contains only
   v0.37.0.md and v0.37.1.md.
3. `README.md:120-129` — the newest feature section is "Compare counterfactual
   scenarios (v0.11.0+)"; README contains zero occurrences of "portfolio"
   while `src/auteur/portfolio/cli.py` exists (v0.12.0 changelog documents a
   12-module portfolio subsystem).
4. `docs/pilot-report.md:114-117` — "The bounded reasoning pilot is complete.
   The full end-to-end authoring pilot is not complete; its next prerequisite
   is a genuinely authored bounded project with 3–5 Scene Realizations,
   accepted prose, one external edit, and a reconciliation cycle."
5. `docs/superpowers/specs/2026-07-30-cartographer-agent-native-pilot-v2.md:18-21` —
   pilot v1 "did not establish behavioral usefulness: treatment and control
   each won 2/4 pairs, only one reviewer participated, and run variance was
   not measured"; spec lines 39-42 — every v2 execution uses "no provider or
   `compile_outline()` call".
6. `docs/reviews/2026-07-28-cartographer-profile-emotional-target-evaluation.md:152`
   — "Is another implementation slice warranted? No; evaluation
   infrastructure or safe provider access is needed first."; line 158 — at
   pinned SHA `4598db6` neither `ANTHROPIC_API_KEY` nor `OPENAI_API_KEY` was
   present, "No provider was called", "no prompt/response capture was created";
   line 160 — "The next operator action is to provide one fixed
   provider/model through the normal secure path ... then generate at most
   eight calls and construct/validate captures before review. Behavioral
   usefulness remains unproven." (these lines are uncommitted worktree
   additions at freeze time, i.e. the owner's live record).
7. `src/auteur/pipeline/runner.py:45` — `_REASONING_RUNTIME =
   ReasoningRuntime(_REASONING_REGISTRY, report_dir=Path())`; 9,221 root-level
   JSON reasoning reports exist in the worktree (gitignored, .gitignore:37
   `/*.json`), spanning 2026-07-19 to 2026-08-07.
8. `docs/reviews/v0.37-post-release-hardening-verification.md:102-112` —
   3,729 collected, 3,701 passed, 1 skipped, 27 xfailed, 0 failed; lines
   116-140 — `scripts/check.py` validator suite: 21/30 cases fail, accepted as
   pre-existing third-party fixture issues.
9. Two ADR-013 files exist: `docs/adr/013-series-graph-semantics.md` and
   `docs/adr/ADR-013-Universe-to-Series-Propagation.md` (both titled "ADR 013").

**Inferred (clearly separated):** (a) the release cadence from v0.12.0
(2026-07-22) to v0.37.1 (verified 2026-07-28) implies roughly 24 minor
versions in about 6 days — inference from the changelog date and verification
report dates, not a measured claim; (b) feature velocity has outpaced
behavioral evidence — inference from 4-6 combined with the version delta;
(c) the report-dir default explains the root JSON accumulation — inference
from runner.py:45 plus observed files.

Logic trace: The deterministic surface is heavily validated (8), so the
weakness is not in the schema/rule layer. The version ledger is inconsistent
with the code (1, 2) and README lags shipped subsystems (3), which is real
but explanatory, not blocking. The product's differentiating layer is the
LLM-mediated creative core, and the repository's own records state its
behavioral value was not established in pilot v1 (5), the full end-to-end
path was never run (4), and the designed v2 evaluation is blocked on provider
access with "Behavioral usefulness remains unproven" (6). Therefore the
weakest boundary is the unproven behavioral layer, whose check is the
prerequisite the owner's own review ranks first (6, line 152) — and it is the
boundary whose failure would make the other 24 versions of work moot.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: README.md
    lines: L3
    quote: "Auteur is an opinionated narrative-engine toolkit for long-form fiction. It helps beginner-to-intermediate writers turn raw creative input into a recommended story engine, validates that engine deterministically, and treats chapter outlining and prose generation as optional downstream stages."
    supports_claim: "Repository goal: narrative-engine toolkit with deterministic validation and optional downstream creative stages."
  - file: CHANGELOG.md
    lines: L5
    quote: "## v0.12.0 (2026-07-22) — Narrative Decision Portfolio"
    supports_claim: "Changelog's newest entry is v0.12.0 while the package is at 0.37.1; 24 minor versions undocumented."
  - file: pyproject.toml
    lines: L7
    quote: "version = \"0.37.1\""
    supports_claim: "Current declared version, used to quantify the changelog gap."
  - file: docs/pilot-report.md
    lines: L114
    quote: "The bounded reasoning pilot is complete. The full end-to-end authoring pilot is"
    supports_claim: "End-to-end authored path (Realization, Expression, reconciliation) has never been exercised."
  - file: docs/superpowers/specs/2026-07-30-cartographer-agent-native-pilot-v2.md
    lines: L20
    quote: "It did not establish behavioral usefulness: treatment and control each won 2/4"
    supports_claim: "Cartographer pilot v1 failed to establish behavioral usefulness; v2 exists to measure it."
  - file: docs/reviews/2026-07-28-cartographer-profile-emotional-target-evaluation.md
    lines: L160
    quote: "The next operator action is to provide one fixed provider/model through the normal secure path, confirm local-only retention is acceptable, then generate at most eight calls and construct/validate captures before review. Behavioral usefulness remains unproven."
    supports_claim: "The designed evaluation is blocked on provider access; behavioral value remains unproven per the owner's own live record."
  - file: src/auteur/pipeline/runner.py
    lines: L45
    quote: "        _REASONING_RUNTIME = ReasoningRuntime(_REASONING_REGISTRY, report_dir=Path())"
    supports_claim: "Reasoning runtime defaults reports to the process CWD, explaining 9,221 root-level report files."
  - file: .gitignore
    lines: L37
    quote: "/*.json"
    supports_claim: "Root-level report accumulation is accommodated by gitignore rather than prevented."
```

## 9. Why this boundary matters

If the creative core's behavioral value is never demonstrated, the product's
differentiating promise ("a literary compiler") rests on deterministic
machinery that produces structurally valid artifacts of unknown usefulness.
That makes every future feature slice — including the 24-version backlog of
undocumented work — priority-risky: effort continues on an unvalidated value
assumption. Conversely, if the ≤8-call capture and two-reviewer blinded
review complete, the owner either gets evidence the layer helps (justifying
continued product work and productization) or evidence it does not (redirecting
work toward the deterministic surface, documentation, or a different
interaction design). The boundary is also time-sensitive: the evaluation kit
is designed, frozen at a pinned SHA, and waiting only on a provider decision —
the marginal cost of completing it is at its lowest now.

## 10. Candidate next steps

1. **Complete the Cartographer pilot v2 evaluation captures** — provide one
   fixed provider/model through the normal secure path, generate the designed
   ≤8 calls, construct and validate the captures, then run the preregistered
   two-reviewer blinded review (H1-H6). Smallest action that resolves the
   behavioral-value question.
2. **Defer/do-nothing** — if no provider access or reviewer bandwidth is
   available, explicitly park the evaluation and instead do (3). Credible only
   as a bounded deferral, because the kit is already frozen and the cost of
   stale kits rises.
3. **Backfill the version ledger** — changelog entries for v0.13-v0.36 (or a
   release-notes index), README coverage of `portfolio` and later subsystems,
   ADR-013 rename. Cheap, real, but does not resolve the value question.
4. **Scope reasoning-report output** — change the `report_dir=Path()` default
   to a project-scoped location and stop root-level report accumulation.
   Hygiene, low decision value.
5. **Dogfood the end-to-end path** — build the genuinely authored bounded
   project the 07-15 pilot named as its next prerequisite (3-5 Scene
   Realizations, accepted prose, one external edit, reconciliation). Heavier
   than (1); complementary, not a substitute.

## 11. Recommended next step

**Complete the Cartographer pilot v2 evaluation (candidate 1): provide one
fixed provider/model through the secure path, generate the ≤8 designed calls,
construct and validate the captures, and run the preregistered two-reviewer
blinded review.** This is the smallest action justified by the evidence: it
executes a design that already exists, is frozen at a pinned SHA, and was
explicitly ranked by the owner's own review as the next step ("evaluation
infrastructure or safe provider access is needed first", review:152). It does
not require new features, new schemas, or new evaluation machinery — only the
provider decision and execution. Do not begin a new feature slice until the
behavioral evidence exists; the observed 24-version gap between changelog and
code is a symptom of velocity outrunning evidence, not a reason to continue
it.

## 12. Recommended workflow

`product-implementation-workflow` (from workflow-registry.yaml), executed in
`plan_only` mode. The primary fog is product_fog; the immediate step is an
evaluation/evidence action, not implementation, so planning-only is the honest
execution mode. No workflow ID was invented; the id is verified against
skills/workflow-planner/references/workflow-registry.yaml.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: experiments/product-interaction-p3-v1/charter-v1.md
user_implied_fog_type: unknown
primary_fog_type: product_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "pyproject.toml (line 7): version 0.37.1 vs changelog newest entry v0.12.0 (CHANGELOG.md:5)"
  - "CHANGELOG.md (line 5): newest changelog entry is v0.12.0; 24 minor versions undocumented"
  - "README.md (line 120-129): newest documented feature is v0.11 simulate; portfolio subsystem (src/auteur/portfolio/cli.py) absent from README"
  - "docs/pilot-report.md (lines 114-117): full end-to-end authoring pilot not complete; never traversed"
  - "docs/superpowers/specs/2026-07-30-cartographer-agent-native-pilot-v2.md (line 20): pilot v1 did not establish behavioral usefulness"
  - "docs/reviews/2026-07-28-cartographer-profile-emotional-target-evaluation.md (lines 152-160): evaluation blocked on provider access; behavioral usefulness remains unproven"
  - "src/auteur/pipeline/runner.py (line 45): reasoning reports default to CWD (report_dir=Path()); 9,221 root JSON reports"
  - ".gitignore (line 37): root-level report JSON accumulation accommodated by ignore rule"
recommended_workflow_id: product-implementation-workflow
recommended_execution_mode: plan_only
weakest_boundary: unproven behavioral value of the LLM-mediated creative core; designed evaluation blocked on provider access
weakness_type: Zero Validation
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-08T03:50:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

For `workflow-planner` (or an implementation agent), plan_only:

> In `auteur` (frozen SHA 374abb4), the highest-value next engineering work is
> completing the behavioral evidence path for the LLM-mediated creative core,
> not another feature slice. The Cartographer pilot v2 kit is designed,
> preregistered (H1-H6), and frozen at a pinned SHA, but every execution is
> provider-free and no capture exists — the owner's own review
> (docs/reviews/2026-07-28-cartographer-profile-emotional-target-evaluation.md:152-160)
> ranks "evaluation infrastructure or safe provider access" first and states
> "Behavioral usefulness remains unproven". Plan the smallest credible path:
> one fixed provider/model via the normal secure path, at most eight designed
> calls, capture construction and validation, then the two-reviewer blinded
> review against H1-H6. Do not plan new features, schemas, or evaluation
> machinery; do not modify the target repository as part of planning.
> Secondary (only if the provider path is unavailable): backfill the version
> ledger (CHANGELOG v0.13-v0.36, README portfolio coverage, ADR-013 rename)
> as a bounded deferral. Plan_only — no implementation is authorized by P3.
