# Repository Sensemaking Brief

<!-- artifact_id: repository_sensemaking_brief | schema_version: 1 -->
<!-- runtime-generated skeleton created_at: 2026-07-27T00:38:53.857944Z -->

## 1. Repository goal

<!-- MODEL_SECTION:repository_goal:BEGIN -->

Auteur is a narrative engineering toolkit -- a "literary compiler" for long-form
fiction -- that has grown into a full layered story-production system. Per
`CLAUDE.md` (root), it implements a complete 7-layer hierarchy (Universe ->
Series -> Book/Story Identity -> Blueprint -> Outline -> Draft -> Editing),
each layer producing durable YAML/JSON/Markdown artifacts and deterministic
diagnostics. It also ships three built-in interactive "genre pipelines"
(netorare, mystery, gentlefemdom) that turn author choices into a validated
`StoryIdentity` (see root `CONTEXT.md`). The stated intent behind this
sensemaking run (`artifacts/01-orchestration-run/00-user-intent.md`) is to
run Full Fog Path diagnostics on the current state of the codebase to
understand its boundaries and recommend a next development workflow.

<!-- MODEL_SECTION:repository_goal:END -->

## 2. Current shape

<!-- MODEL_SECTION:current_shape:BEGIN -->

- `src/auteur/` contains 20+ subpackages: `structure/` (whole-story diagnostics
  -- `state.py`, `analyzer.py`, `bible_audit.py`, `outline_audit.py`,
  `genres.py`, revision/proposal machinery), `narrative_blueprint/`,
  `narrative_ontology/`, `narrative_orchestration/`, `narrative_realization/`
  (the newer Layer-0..3 schema/validator/loader stack), `genre_pipeline/`
  (shared runtime for the three built-in genre pipelines), `netorare/`,
  `mystery/`, `gentlefemdom/` (genre-specific templates/validation), `series/`,
  `decision/`, `commitment/`, `convergence/`, `critic/`, `editing/`,
  `expression/`, `character/`, `cartographer*`, `book/`, plus root modules
  (`cli.py`, `cli_parser.py`, `cli_dispatch.py`, `blueprint.py`, `bible.py`,
  `identity.py`).
- `tests/` mirrors this with 200+ `test_*.py` files plus package-scoped
  directories (`tests/netorare/`, `tests/mystery/`, `tests/gentlefemdom/`,
  `tests/convergence/`, `tests/impact/`, `tests/auteur/narrative_*`, etc.).
- `docs/` holds root `CONTEXT.md`, `docs/narrative-architecture.md`, 17
  numbered ADRs plus one non-numbered ADR file, versioned `architecture/`,
  `design/`, and `acceptance/` docs (v0.3 through v0.34), and a
  `docs/superpowers/{specs,plans}/` pair of dated design/implementation
  documents.
- `CHANGELOG.md` documents dated, versioned releases from v0.3.x through
  v0.10.0 (2026-07-22), each adding a named subsystem (Realization
  Convergence v0.6.0, Author Decision Workspace v0.7.0, Project-Level
  Narrative Planning v0.10.0, etc.).
- `scripts/` contains the CLI-adjacent validator scripts (`validate-repo.py`,
  `validate-brief.py`, `check.py`, `orchestration-runner.py`, and ~20 other
  `validate-*.py` scripts) plus `deploy.sh`.
- Two prior sensemaking briefs already exist in this repo
  (`artifacts/repository_sensemaking_brief.md` and
  `artifacts/full-local-sensemaking/04-repository-sensemaking-brief.md`) but
  both describe a materially older codebase state (see Section 6 logic
  trace) and are superseded by this brief.

<!-- MODEL_SECTION:current_shape:END -->

## 3. Strong signals

<!-- MODEL_SECTION:strong_signals:BEGIN -->

- The two structural gaps flagged by the two prior sensemaking briefs have
  since been fixed in the live code: `state_check` now loads and passes
  `outline` into diagnostics (`src/auteur/structure/state.py:159`, with an
  `outline: Optional parsed outline dict` parameter documented at line
  133-134), and `scripts/validate-repo.py` now calls `sys.exit(1)` (line 380)
  rather than the unconditional `sys.exit(0)` the older brief cited -- both
  are evidence the team actively closes gaps that sensemaking surfaces.
- `AGENTS.md` enforces a disciplined verification protocol before declaring
  code defects ("Verify claims with evidence... Don't cite line numbers
  without inspecting them... Distinguish between 'tests pass' ... and
  'implementation exists in git'"), matching this brief's own evidence
  discipline.
- Newer subsystems are dated and test-backed in the same commit family as
  their `CHANGELOG.md` entry: e.g. `CHANGELOG.md:349-362` documents v0.7.0's
  Decision Workspace CLI surface, and `src/auteur/cli_parser.py:419-420`
  shows `register_decision_subcommands(sub)` actually wiring
  `auteur.decision.cli` into the live dispatcher -- this is a real, reachable
  feature, not a stub.
- `docs/agents/domain.md` establishes a clear, enforceable doctrine ("single-
  context repo," read `CONTEXT.md` for domain vocabulary) that, if followed,
  would prevent exactly the drift this brief identifies as the weakest
  boundary -- the doctrine is sound, only its upkeep has lagged.

<!-- MODEL_SECTION:strong_signals:END -->

## 4. Missing pieces

<!-- MODEL_SECTION:missing_pieces:BEGIN -->

- `CONTEXT.md` (root) is exclusively about the Genre Pipeline subsystem
  (netorare/mystery/gentlefemdom) and a short Series/Universe continuity
  section. It contains zero mentions of `decision`, `commitment`, `critic`,
  `editing`, or `expression` -- six real, tested, CLI-wired packages under
  `src/auteur/` (see Sections 6 and 7 for the full trace).
- No pointer inside `CONTEXT.md` to the scattered docs that do cover these
  subsystems (e.g. `docs/critic-registry.md`, `docs/critic-integration-
  contract.md`, `docs/book-expression.md`, `docs/expression-boundary.md`,
  `docs/design/v0.7.0-author-decision-workspace.md`), so an agent following
  `docs/agents/domain.md`'s instruction to consult `CONTEXT.md` for domain
  vocabulary has no path from the canonical doc to that material.
- `docs/architecture.md` (the other repo-root architecture doc) also has zero
  mentions of `decision`, `commitment`, `convergence`, `critic`, `editing`,
  or `expression` -- so the gap is not compensated for by the second
  architecture document either.

<!-- MODEL_SECTION:missing_pieces:END -->

## 5. Improvement opportunities

<!-- MODEL_SECTION:improvement_opportunities:BEGIN -->

- Extend `CONTEXT.md` with short glossary entries for `decision`,
  `commitment`, `convergence`, `critic`, `editing`, and `expression` (even a
  one-paragraph summary plus a pointer to the fuller docs for each would
  satisfy `docs/agents/domain.md`'s doctrine).
- Add a per-subsystem doc index near the top of `CONTEXT.md` or
  `docs/architecture.md` so future CHANGELOG-worthy subsystems are linked
  from the canonical entry point at the moment they ship, rather than
  requiring a separate reconciliation pass later.
- Since `CHANGELOG.md` already carries dated per-version subsystem
  descriptions (e.g. v0.6.0, v0.7.0, v0.10.0), a lightweight process check
  (e.g. a CI grep) could flag when a new top-level `src/auteur/<package>/`
  directory has no corresponding term in `CONTEXT.md`, preventing this drift
  from recurring.

<!-- MODEL_SECTION:improvement_opportunities:END -->

## 6. Weakest boundary

<!-- MODEL_SECTION:weakest_boundary_prose:BEGIN -->

**Weakness type:** Vocabulary Drift

The weakest boundary is between the code's real domain vocabulary and the
repo's single canonical domain-vocabulary document. `docs/agents/domain.md`
states this is a "single-context repo" and instructs agents to "use the term
as defined in `CONTEXT.md`" for any domain concept, treating an absent
concept as "a signal to ... note a documentation gap." Root `CONTEXT.md`
titles itself "Genre Pipeline Architecture Context" and its entire ~169
lines describe only the Genre Pipeline subsystem plus a short Series/Universe
continuity section (`CONTEXT.md:105-165`). It never mentions `decision`,
`commitment`, `convergence` (outside that Series/Universe section), `critic`,
`editing`, or `expression` -- six packages that exist under `src/auteur/`
with real implementations, dedicated test suites, and (for at least
`decision` and `convergence`) dated `CHANGELOG.md` release entries. This
means an agent that dutifully follows `docs/agents/domain.md`'s own
instructions will treat `decision`, `commitment`, `convergence`, `critic`,
`editing`, and `expression` as undefined domain terms, even though each is a
first-class, shipped, user-facing subsystem (`auteur decision status`,
`auteur decision list`, etc. per `CHANGELOG.md:353-362`, wired at
`src/auteur/cli_parser.py:419-420`).

Both prior sensemaking briefs in this repo targeted a narrower and now-
resolved gap (missing `outline.yaml` validation in `state_check`, and a
decorative `validate-repo.py` exit code); both of those specific findings no
longer hold against the current code (see Section 7's logic trace), which is
itself informative: the repo evolves fast enough that a sensemaking brief
tied to file-level behavior goes stale within weeks, while a brief tied to
the canonical-vocabulary contract (`CONTEXT.md` vs. `src/auteur/*`) targets a
structural gap that has persisted and widened across multiple releases.

<!-- MODEL_SECTION:weakest_boundary_prose:END -->

## 6.5. Problem classification (fog type)

Fog type is recorded in the machine-readable handoff block (Section 13), not here.

## 7. Evidence

<!-- MODEL_SECTION:evidence_prose:BEGIN -->

`CONTEXT.md:1-3` opens with "# Genre Pipeline Architecture Context" and "This
document defines the domain language and runtime ownership for Auteur's
built-in interactive genre pipelines" -- the document's own framing is scoped
to genre pipelines only, not to the whole `src/auteur/` domain.
`docs/agents/domain.md:19-26` is the instruction that makes this scoping a
problem: "When output names a domain concept ... use the term as defined in
`CONTEXT.md`. If the needed concept is not in the glossary yet, treat that as
a signal ... note a documentation gap." `src/auteur/decision/service.py:1`
carries the docstring `"""Decision workspace service -- compose real project
state from subsystems."""`, and `src/auteur/cli_parser.py:419-420` shows
`from auteur.decision.cli import register_decision_subcommands` followed by
`register_decision_subcommands(sub)`, proving the decision subsystem is
registered in the live CLI dispatcher, not dead code. `CHANGELOG.md:349-362`
dates the Decision Workspace's shipped CLI surface to v0.7.0 (2026-07-21) --
ten days after `CONTEXT.md`'s own `CONTEXT.md:168` ("Last updated:
2026-07-11") -- confirming the vocabulary gap is not merely "not yet
written," but persisted through at least one full release cycle after the
document's last touch.

Logic trace: `docs/agents/domain.md:19-26` directs any agent working in this
repo to resolve domain terms exclusively through `CONTEXT.md` and treat a
missing term as a documentation-gap signal. Reading `CONTEXT.md` in full
(all 169 lines) shows it covers only the Genre Pipeline subsystem and a
short Series/Universe section, with zero occurrences of `decision`,
`commitment`, `critic`, `editing`, or `expression` (confirmed by a literal
grep across the file). Cross-checking those terms against `src/auteur/`
shows each is a real subpackage with source (`decision/service.py`,
`commitment/service.py`, `critic/base.py`, `editing/runner.py`,
`expression/composition.py`), dedicated tests (`tests/test_decision.py`,
`tests/test_commitment.py`, `tests/test_critic_base.py` and 7 sibling
`test_critic_*.py` files, `tests/test_editing_*.py` x5,
`tests/test_expression_*.py` x3), and for `decision` specifically a CLI
registration path reachable from `main()` via `cli.py -> cli_parser.py:419-
420 -> auteur.decision.cli.register_decision_subcommands`. Before concluding
these were simply undocumented, I checked for disconfirming evidence: are
they dead/ghost code that a doc author would rightly have skipped? The test
suites and the live CLI wiring rule that out -- these are shipped, reachable
features, which is what makes their total absence from the one document the
repo's own process (`docs/agents/domain.md`) designates as canonical a
genuine Vocabulary Drift rather than a non-issue. `docs/architecture.md` was
also checked as a second possible source of coverage and likewise has zero
matches for any of the six terms, so the gap is not compensated for
elsewhere in the two root architecture docs.

<!-- MODEL_SECTION:evidence_prose:END -->

<!-- REQUIRED: this section's prose must include a paragraph giving the diagnostic reasoning chain that connects the cited evidence to the weakest-boundary conclusion, starting with the exact two-word marker phrase specified in your execution instructions followed by a colon. validate-brief.py fails the whole artifact (error code NO_LOGIC_TRACE) if that reasoning paragraph is absent. -->

## 8. Evidence excerpts

<!-- MODEL_SECTION:evidence_excerpts:BEGIN -->

```yaml
<!-- REQUIRED: every item below must include all four fields file, lines, quote, supports_claim (exact key names -- `citation` or similar does NOT satisfy this). validate-brief.py raises EVIDENCE_EXCERPT_FIELD per missing/misnamed key, per excerpt. -->

```yaml
evidence_excerpts:
  - file: CONTEXT.md
    lines: L1-L3
    quote: "# Genre Pipeline Architecture Context\n\n> Canonical architecture: [Narrative Architecture](docs/narrative-architecture.md)."
    supports_claim: "CONTEXT.md frames itself as scoped to Genre Pipeline Architecture, not the whole src/auteur domain, supporting the claim that six other subsystems are out of its stated scope."
  - file: docs/agents/domain.md
    lines: L19-L26
    quote: "## Vocabulary\n\nWhen output names a domain concept in an issue title, refactor proposal,\nhypothesis, or test name, use the term as defined in `CONTEXT.md`.\n\nIf the needed concept is not in the glossary yet, treat that as a signal to\neither reconsider the wording or note a documentation gap for a future\nconceptual pass."
    supports_claim: "This is the explicit repo doctrine that makes CONTEXT.md's silence on decision/commitment/convergence/critic/editing/expression an active drift problem rather than a harmless omission."
  - file: src/auteur/decision/service.py
    lines: L1
    quote: "\"\"\"Decision workspace service -- compose real project state from subsystems.\"\"\""
    supports_claim: "Proves the decision subsystem is a real, implemented service (not a stub), yet decision is never mentioned in CONTEXT.md."
  - file: src/auteur/cli_parser.py
    lines: L419-L420
    quote: "from auteur.decision.cli import register_decision_subcommands\n    register_decision_subcommands(sub)"
    supports_claim: "Confirms the decision subsystem's CLI is actually wired into the live dispatcher (reachable, not dead code), strengthening the drift claim over a 'ghost feature' explanation."
  - file: CHANGELOG.md
    lines: L349-L362
    quote: "## v0.7.0 (2026-07-21) -- Author Decision Workspace\n\n### New decision workspace subsystem\n\n- auteur decision status: Shows project-level decision status including\n  open impact findings, decisions by readiness, and highest-priority blocker."
    supports_claim: "Dates the Decision Workspace's shipped CLI surface to 2026-07-21, after CONTEXT.md's own 2026-07-11 last-updated date, showing the vocabulary gap persisted through a full release cycle."
  - file: src/auteur/structure/state.py
    lines: L159
    quote: "raw_diagnostics = run_all_diagnostics(blueprint, bible, outline=outline)"
    supports_claim: "Shows the outline.yaml validation gap identified by the older flat-path brief (artifacts/repository_sensemaking_brief.md) has since been fixed, so that brief's weakest-boundary finding is stale."
  - file: scripts/validate-repo.py
    lines: L380
    quote: "sys.exit(1)"
    supports_claim: "Shows the decorative-exit-code gap identified by the full-local-sensemaking brief has since been fixed, so that brief's weakest-boundary finding is also stale."
```
```

<!-- MODEL_SECTION:evidence_excerpts:END -->

## 9. Why this boundary matters

<!-- MODEL_SECTION:why_boundary_matters:BEGIN -->

`docs/agents/domain.md` is not aspirational -- it is the literal instruction
set agents in this repo are told to follow when naming domain concepts. As
long as `CONTEXT.md` stays silent on `decision`, `commitment`, `convergence`,
`critic`, `editing`, and `expression`, any agent (human or automated)
generating an issue title, refactor proposal, or test name for those
subsystems has no canonical vocabulary to draw from, and `docs/agents/
domain.md` explicitly tells them to treat that as "a signal to ... reconsider
the wording" -- i.e. the doctrine itself predicts inconsistent, ad hoc naming
across future work touching these six subsystems. Because new subsystems
have shipped roughly every few days in this repo recently (`CHANGELOG.md`'s
v0.5.0 through v0.10.0 span 2026-07-19 to 2026-07-22), the gap between "last
CONTEXT.md update" and "current subsystem count" will keep widening unless
closing it becomes part of the release process, not a one-off catch-up edit.

<!-- MODEL_SECTION:why_boundary_matters:END -->

## 10. Candidate next steps

<!-- MODEL_SECTION:candidate_next_steps:BEGIN -->

1. Add a glossary section to `CONTEXT.md` covering `decision`, `commitment`,
   `convergence`, `critic`, `editing`, and `expression`, each with a short
   definition plus a pointer to the fuller existing docs (`docs/critic-
   registry.md`, `docs/book-expression.md`, `docs/design/v0.7.0-author-
   decision-workspace.md`, etc.).
2. Add a short "See also" index near `CONTEXT.md`'s top linking to the other
   docs that already cover these subsystems in depth, so the single-context
   doctrine in `docs/agents/domain.md` has a real path to that material.
3. Introduce a lightweight CI or pre-release check that flags any top-level
   `src/auteur/<package>/` directory absent from `CONTEXT.md`'s vocabulary,
   to prevent this drift from re-accumulating after each release.
4. Re-run this sensemaking pass again after the `CONTEXT.md` update lands, to
   confirm the vocabulary gap identified here has actually closed (the same
   check this brief itself performed against the two prior, now-stale
   briefs).

<!-- MODEL_SECTION:candidate_next_steps:END -->

## 11. Recommended next step

<!-- MODEL_SECTION:recommended_next_step:BEGIN -->

Update `CONTEXT.md` to add glossary coverage for `decision`, `commitment`,
`convergence`, `critic`, `editing`, and `expression`, each with a one-
paragraph definition and a pointer to the existing deeper docs for that
subsystem. This is the smallest concrete action that directly closes the gap
`docs/agents/domain.md`'s own doctrine identifies as a documentation-gap
signal, and it does not require any code change.

<!-- MODEL_SECTION:recommended_next_step:END -->

## 14. Ready-to-copy prompt

<!-- MODEL_SECTION:ready_to_copy_prompt:BEGIN -->

```
/docs-architecture
The repo-sensemaker found the weakest boundary is Vocabulary Drift between
root CONTEXT.md (the repo's single canonical domain-vocabulary source per
docs/agents/domain.md) and the actual src/auteur/ domain. CONTEXT.md is
scoped entirely to the Genre Pipeline subsystem plus a short Series/Universe
section, and never mentions the decision, commitment, convergence, critic,
editing, or expression subsystems -- all six are real, tested, CLI-wired
packages (e.g. auteur.decision.cli is registered at
src/auteur/cli_parser.py:419-420; CHANGELOG.md:349-362 dates the Decision
Workspace's v0.7.0 release to 2026-07-21, after CONTEXT.md's own 2026-07-11
last-updated date). Align CONTEXT.md's domain language with the current
src/auteur/ package set: add glossary entries for the six missing
subsystems, each with a pointer to its existing deeper docs (docs/critic-
registry.md, docs/book-expression.md, docs/design/v0.7.0-author-decision-
workspace.md, etc.), and generate copy-paste prompts for the doc edit.
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
  - "CONTEXT.md (lines L1-L3): document frames itself as scoped to Genre Pipeline Architecture only"
  - "docs/agents/domain.md (lines L19-L26): repo doctrine mandates CONTEXT.md as sole domain vocabulary source"
  - "src/auteur/decision/service.py (line L1): Decision Workspace service is real, implemented code absent from CONTEXT.md"
  - "src/auteur/cli_parser.py (lines L419-L420): decision CLI is registered in the live dispatcher, ruling out dead-code explanation"
  - "CHANGELOG.md (lines L349-L362): Decision Workspace shipped 2026-07-21, after CONTEXT.md's 2026-07-11 last-updated date"
  - "src/auteur/structure/state.py (line L159): outline.yaml gap from the older flat-path brief is already fixed, confirming that brief is stale"
  - "scripts/validate-repo.py (line L380): decorative-exit-code gap from the full-local-sensemaking brief is already fixed, confirming that brief is stale"
recommended_workflow_id: docs-architecture
recommended_execution_mode: guided_execution
weakest_boundary: context_md_domain_vocabulary_gap
weakness_type: Vocabulary Drift
weakness_type_explanation: None
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-07-27T00:38:53.857944Z"
immutable: true
```
