# Repository Sensemaking Brief

## 1. Repository goal

sensemaking-skills is an agent-native framework for repository diagnosis and
workflow orchestration. It aims to turn repository uncertainty ("fog") into
actionable problem frames, research paths, and specific skill recommendations.
README.md:6 states the product promise: "An agent-native framework for
repository diagnosis and workflow orchestration. Turns repository uncertainty
into clear problem frames, research paths, and actionable next-step prompts."
The framework is delivered as (a) SKILL.md files consumed by agent harnesses
and (b) a local-first Python package (CLI + validators) that reads local files,
validates artifacts, and writes Markdown/JSON outputs without any external API
calls (CONTEXT.md:19-30).

The user question for this run: "Understand this repository and tell me what
engineering work would create the most value next."

## 2. Current shape

- **Skills** (`skills/`): `repo-sensemaker` (diagnostic), `workflow-planner`
  (procedural), `docs-aligner`, `problem-framer`, `unknowns-mapper`, `handoff`,
  `to-prd`, `to-issues`, `architectural-review`, `setup-sensemaking-skills`,
  `skill-maintainer`, `usage-researcher`, `using-sensemaking` (bootstrap), and
  others. Each has `SKILL.md` plus `references/` (registries, templates,
  evidence rules).
- **Package** (`src/sensemaking_skills/`, v0.2.1): `cli.py` (Click CLI:
  `analyze`, `validate`, `test`, `setup-skills`), `setup_skills.py`,
  `config.py`, `paths.py`, `campaign_accounting/`, `campaign_validation/`,
  `execution_infra/` (campaign runners, GitHub approval capture).
- **Scripts** (`scripts/`): ~40 validators/runners — `validate-brief.py`,
  `validate-plan.py`, `validate-artifact.py`, `validate-repo.py`,
  `workflow-runtime.py`, `workflow-planner.py`, `run-ledger.py`,
  `shadow-mode-runner.py`, `brief_skeleton.py`, `evidence_quote_extractor.py`,
  `weakness_type_safeguard.py`, etc.
- **Registries**: `skills/workflow-planner/references/workflow-registry.yaml`
  (~21 workflow IDs incl. `architecture-implementation-workflow`,
  `full-local-sensemaking`, `fast-local-diagnostic`),
  `artifact-contracts.yaml` (machine field contracts),
  `docs/canonical-vocabulary.yaml`.
- **Tests** (`tests/`): `campaign_accounting/`, `campaign_validation/`,
  `execution_infra_tests/`, fixtures including `tests/fixtures/brief-valid.md`.
- **Experiments** (merged on `origin/main`): `post-hardening-decision-probe-v1`,
  `post-hardening-adjudication-probe-v1`, `evaluation-design-e1-v1`,
  `evaluation-design-e2-v1` — each an evidence package with a final decision,
  no implementation.
- **Distribution artifacts**: `dist/sensemaking_skills-0.2.1-py3-none-any.whl`
  and sdist built and committed.
- Root contains ~90 status/handoff documents (PHASE-*, DEPLOYMENT-*, FINAL-*,
  SESSION-*), a documentation layer that has outgrown its usefulness as a
  current-state source.

## 3. Strong signals

- **Deterministic evidence grounding**: `scripts/validate-brief.py` enforces
  verbatim evidence-quote grounding against the target repository
  (EVIDENCE_QUOTE_NOT_FOUND, ±3-line window, issue #80) and hallucinated-file
  rejection — the validator is a real consumer of the evidence contract.
- **Single source of truth for machine fields**: `artifact-contracts.yaml`
  declares field names, and `tests/test_field_contract_agreement.py` enforces
  producer/consumer agreement (CONTEXT.md:150-165).
- **Runtime-owned artifact paths**: ADR 0010 / issue #40 made
  `expected_output_path` the sole path authority; `brief_skeleton.py` (issue
  #55) guarantees deterministic brief grammar.
- **Evaluation discipline**: E1 DEMOTE and E2 USE_AS_TRIAGE_SIGNAL are
  evidence packages that deliberately made NO scorer/skill/registry change —
  the project consistently separates "evidence" from "implementation" and
  refuses to let evaluation machinery quietly become product development.
- **Documented two-mode contract**: the canonical SKILL.md distinguishes
  runtime invocation (skeleton + quote overwrite) from standalone invocation
  (complete artifact, verbatim quotes), so both pipelines are validatable.

## 4. Missing pieces

- **Skills are not shipped in the wheel**: the built wheel
  `dist/sensemaking_skills-0.2.1-py3-none-any.whl` contains 25 entries — only
  Python modules and `defaults/` YAMLs; there are NO `SKILL.md` files in it.
  `pyproject.toml:49` declares package-data `sensemaking_skills =
  ["skills/**/*", ...]`, but that glob covers `src/sensemaking_skills/skills/`
  (Python modules `base.py`, `repo_sensemaker.py`, `workflow_planner.py`), not
  the repo-root `skills/` directory where the actual SKILL.md trees live.
- **The documented install path cannot deliver skills**: GETTING_STARTED.md:22-27
  tells users to run `pip install sensemaking-skills` then
  `sensemaking-skills setup-skills`, promising "This installs skill files to
  `~/.agents/skills`". But `setup_skills.py:29-30` resolves the source skills
  directory as `Path(__file__).parent.parent.parent / "skills"` — a layout that
  exists only in a source checkout; from an installed site-packages wheel the
  path is `site-packages/../..` (no `skills/` there), so the command fails with
  "Skills directory not found ... This may indicate an incomplete installation."
- **Installed copies silently go stale**: `copy_skill` refuses to overwrite an
  existing destination without `--force` (setup_skills.py:100-101), and there is
  no version/checksum reconciliation between the installed skill and the
  canonical repo skill. The observed installed copy at
  `~/.agents/skills/repo-sensemaker/SKILL.md` is the 119-line variant matching
  commit 178d5f0 (2026-05-22) — four months stale — and still teaches the
  pre-ADR-0010 behavior "Call `scripts/create-artifact.py` to resolve the output
  path", which the canonical SKILL.md:114 explicitly forbids as the cause of a
  tracked-framework-artifact overwrite (ADR 0010, issue #40).
- **No compact owner-facing synthesis**: the canonical skill's output is the
  14-section machine brief; there is no human-facing compact synthesis step
  (recommended next work + alternatives + uncertainty) in the skill or
  template. Section 11 ("Recommended next step") is the closest, but it is
  embedded in a machine-contract artifact.
- **No value-production run exists**: CONTEXT.md:322 records "No
  value-production runs exist (blocked — see preconditions): All runs to date
  are system-proving." The system has never been used by an external
  stakeholder to make a real decision.

## 5. Improvement opportunities

- Resolve the documented install path (`pip install` + `setup-skills`) so the
  shipped artifact can actually deliver SKILL.md trees (ship `skills/` in the
  wheel, or resolve the source dir via `importlib.resources`).
- Add an installed-vs-canonical drift check (version pin or checksum) to
  `setup-skills` and/or a `--check` command so stale installed copies are
  detectable instead of silent.
- Add an owner-facing compact synthesis to repo-sensemaker (recommended next
  work, strongest evidence, alternatives, uncertainty) — the P1 experiment
  hypothesis.
- Consolidate the ~90 root-level status documents; the README maturity claim
  ("Production-ready for agent-based use", README.md:10) conflicts with
  CURRENT-PROJECT-STATUS.md:4 ("Overall Progress: 60%") and CONTEXT.md:266
  ("No value-production run exists yet").
- The hardening branch (`hardening/repository-sensemaking-v1`, 452-line
  SKILL.md) is a closed REVISE candidate with substantial unmerged content
  (deterministic exploration passes, GAP-5..GAP-9); the disposition of that
  work is a standing open decision.

## 6. Weakest boundary

**Boundary:** the execution/distribution surface — the skill implementation a
user actually invokes is not guaranteed to be the canonical skill in the
repository.

**Observed contract:** GETTING_STARTED.md:22-27 and README.md:96-118 promise
that `pip install sensemaking-skills` + `sensemaking-skills setup-skills`
installs the current SKILL.md files to `~/.agents/skills`, and README.md:10
declares the product "Production-ready for agent-based use".

**Observed violation or uncertainty:** the wheel contains no SKILL.md files at
all; `setup_skills.py:29-30` can only find the repo-root `skills/` directory in
a source checkout, so the documented flow fails for a pip install; and where a
copy exists (this machine's `~/.agents/skills`), it is a 4-month-old variant
that teaches the exact path-recomputation behavior the canonical skill forbids.
No check detects the divergence.

**Evidence:** see Section 7 (file:line citations) and Section 8 (verbatim
excerpts).

**Weakness type:** Implicit Dependencies

**Logic trace:** The documented install flow (GETTING_STARTED.md:23-27) depends
on a skills directory that the shipped wheel does not contain
(pyproject.toml:49 globs only `src/sensemaking_skills/skills/**`, confirmed by
wheel inspection: no SKILL.md among 25 entries) and on a source-checkout-only
path resolution (`setup_skills.py:29-30` computes `Path(__file__).parent.parent.parent
/ "skills"`). Because `copy_skill` refuses to overwrite without `--force`
(setup_skills.py:100-101), any previously installed copy silently persists — the
observed installed copy matches commit 178d5f0 (2026-05-22) and still instructs
"Call `scripts/create-artifact.py` to resolve the output path", while the
canonical SKILL.md:114 prohibits exactly that call as the cause of a tracked
artifact overwrite (ADR 0010, issue #40). The boundary therefore has three
layers: unshipped files, an implicit layout dependency, and no drift detection —
the installed surface is not the canonical product, and nothing validates it.

**Failure consequence:** a user following the documented install path either
cannot install skills at all (pip install) or runs an outdated skill that
instructs an unsafe path-recomputation workflow; every product improvement made
to the canonical skill is invisible to anyone using an installed copy; and
diagnostics produced through the stale surface are untrustworthy for routing
decisions.

**Confidence:** high — every claim above is directly observed (wheel contents,
source code, git history match, installed file), not inferred. What would raise
it further: a fresh-environment `pip install` + `setup-skills` reproduction
(not performed; the probe is read-only).

**Alternatives considered:**
- *Owner-facing synthesis gap* (product/interaction): real and aligned with the
  user's stated priority, but it is a product-design gap, not a currently
  broken contract; the distribution boundary blocks delivery of ANY improved
  interaction, so it ranks second.
- *Docs maturity drift* (README "production-ready" vs CONTEXT "no
  value-production run"): real but low consequence; a documentation cleanup,
  not a decision blocker.
- *Closed hardening candidate disposition*: consequential but a governance
  decision, not a repository defect; it does not block the distribution fix.

## 6.5. Problem classification (fog type)

The weakest boundary is structural: packaging and install-path machinery that
cannot deliver the canonical skill to users. That is **architecture_fog** —
module/structure problems (unsafe coupling between repo layout, wheel contents,
and install resolution) rather than unclear user needs.

The user's stated priority (improve the owner-facing interaction of
repo-sensemaker) implies **product_fog** — the value contract of the product
experience.

These differ: the codebase's most defensible current weakness is structural
(execution surface), while the user's hypothesis is product-facing (interaction
design). The conflict is genuine but not irreconcilable — the execution-surface
fix is a precondition for any interaction improvement to reach users.

## 7. Evidence

- `src/sensemaking_skills/setup_skills.py:29-30` — skills source resolved as
  `Path(__file__).parent.parent.parent / "skills"`: only valid in a source
  checkout (`# Go up from src/sensemaking_skills/`); an installed wheel would
  resolve outside site-packages to a nonexistent `skills/` directory.
- `src/sensemaking_skills/setup_skills.py:100-101` — `copy_skill` returns
  "Destination already exists: ... (use --force to overwrite)" without
  overwriting; installed copies are never reconciled with the repo.
- `pyproject.toml:49` — `sensemaking_skills = ["skills/**/*", "examples/**/*",
  "docs/**/*"]`; the wheel's `skills/**` covers only `src/sensemaking_skills/
  skills/` Python modules (verified: wheel has 25 entries, zero SKILL.md).
- `GETTING_STARTED.md:23-27` — documented flow: `pip install
  sensemaking-skills`; `sensemaking-skills setup-skills`; "This installs skill
  files to `~/.agents/skills`".
- `skills/repo-sensemaker/SKILL.md:114` — canonical prohibition: "Never call
  `scripts/create-artifact.py` ... that path-recomputation is what caused a
  prior run to overwrite a tracked framework artifact (see ADR 0010, issue
  #40)."
- Installed copy `~/.agents/skills/repo-sensemaker/SKILL.md` (119 lines) hashes
  to the variant at commit 178d5f0 (2026-05-22) and still says "Call
  `scripts/create-artifact.py` to resolve the output path" — observed drift,
  4 months stale vs the canonical 164-line copy.
- `README.md:8-10` — "Status: Beta (Scenario 5 tested and proven)" /
  "Maturity: Production-ready for agent-based use, CLI beta-ready" vs
  `CURRENT-PROJECT-STATUS.md:4` "Overall Progress: 60%" and `CONTEXT.md:322`
  "All runs to date are system-proving."
- `experiments/evaluation-design-e1-v1/final-decision-v1.md:11` — "DEMOTE"
  (weakest_boundary_accuracy is not a reliable primary gate).
- `experiments/evaluation-design-e2-v1/final-decision-v1.md:11` —
  "USE_AS_TRIAGE_SIGNAL" (decision_delta over label accuracy).

Logic trace: The chain from evidence to the weakest-boundary conclusion runs:
documented install promise (GETTING_STARTED.md:23-27) -> source resolution
assumes checkout layout (setup_skills.py:29-30) -> wheel ships no SKILL.md
(pyproject.toml:49 + wheel inspection) -> stale installed copies persist
(setup_skills.py:100-101) -> the copy this machine's agents actually invoke is
the 178d5f0 variant teaching the forbidden create-artifact.py path computation
(canonical SKILL.md:114, ADR 0010) -> therefore the execution surface is not
the canonical product and nothing detects it. That is a structural
(architecture_fog) boundary: an implicit dependency on files and paths that
are neither shipped nor validated.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: src/sensemaking_skills/setup_skills.py
    lines: L29-L30
    quote: 'package_dir = Path(__file__).parent.parent.parent  # Go up from src/sensemaking_skills/
    skills_dir = package_dir / "skills"'
    supports_claim: "setup-skills resolves its skills source via a source-checkout-only relative path, so an installed wheel cannot find it"
  - file: src/sensemaking_skills/setup_skills.py
    lines: L100-L101
    quote: 'if dest_skill.exists() and not force:
        return False, f"Destination already exists: {dest_skill} (use --force to overwrite)"'
    supports_claim: "existing installed skills are never overwritten or reconciled, so installed copies go stale silently"
  - file: GETTING_STARTED.md
    lines: L23-L24
    quote: 'pip install sensemaking-skills
sensemaking-skills setup-skills'
    supports_claim: "the documented install flow is pip install followed by setup-skills"
  - file: GETTING_STARTED.md
    lines: L27
    quote: 'This installs skill files to `~/.agents/skills` (or `C:\Users\*\.agents\skills` on Windows).'
    supports_claim: "the documented promise is that setup-skills installs SKILL.md files for agent invocation"
  - file: pyproject.toml
    lines: L49
    quote: 'sensemaking_skills = ["skills/**/*", "examples/**/*", "docs/**/*"]'
    supports_claim: "package-data globs skills/**/* only under the package (Python modules), not the repo-root SKILL.md trees"
  - file: skills/repo-sensemaker/SKILL.md
    lines: L114
    quote: 'Never call `scripts/create-artifact.py` (or otherwise recompute a path) during a runtime-invoked run; that path-recomputation is what caused a prior run to overwrite a tracked framework artifact (see ADR 0010, issue #40).'
    supports_claim: "the canonical skill forbids the create-artifact.py path recomputation that the stale installed copy still teaches"
  - file: README.md
    lines: L10
    quote: '**Maturity**: Production-ready for agent-based use, CLI beta-ready'
    supports_claim: "README maturity claim conflicts with documented 60% progress and no value-production run"
  - file: CONTEXT.md
    lines: L322
    quote: 'All runs to date are system-proving.'
    supports_claim: "no value-production run exists yet; the framework has never been used for a real external decision"
  - file: experiments/evaluation-design-e2-v1/final-decision-v1.md
    lines: L11
    quote: '**USE_AS_TRIAGE_SIGNAL.**'
    supports_claim: "E2 verdict: decision_delta is a triage signal; label accuracy is not the primary gate"
  - file: experiments/evaluation-design-e1-v1/final-decision-v1.md
    lines: L11
    quote: '**DEMOTE.**'
    supports_claim: "E1 verdict: weakest_boundary_accuracy demoted as primary quality gate"
```

## 9. Why this boundary matters

If the execution surface stays broken, every other investment in
repo-sensemaker is diluted: a user who installs via the documented path either
fails to get skills or runs a stale skill that teaches the exact
path-recomputation behavior ADR 0010 was written to eliminate. Diagnostics
produced through that stale surface can drive downstream routing decisions
(workflow-planner consumes the brief) on the basis of an outdated contract.
The boundary also blocks the user's stated priority: interaction improvements
to the owner-facing experience cannot reach anyone who invokes the installed
copy. Fixing it is small, concrete, and a precondition for everything else.

## 10. Candidate next steps

1. Make the documented install path deliver the canonical skills: ship the
   repo-root `skills/` trees in the wheel (fix package-data/MANIFEST) and
   resolve the setup source via `importlib.resources` or a packaged path,
   then verify with a fresh-environment `pip install` + `setup-skills`.
2. Add drift detection: record a version/checksum of the canonical skill in
   installed copies and add `setup-skills --check` (or make `copy_skill`
   reconcile by default) so stale installs are surfaced instead of silent.
3. Add an owner-facing compact synthesis to repo-sensemaker (recommended next
   work, strongest evidence, alternatives including do nothing, uncertainty,
   decision-changing evidence) — the Task P1 product hypothesis.
4. Resolve the disposition of the closed hardening branch content (452-line
   SKILL.md, deterministic exploration protocol, GAP-5..GAP-9) — merge
   decision, archive, or explicit rejection record.
5. Consolidate root-level status documents and align README maturity claims
   with the actual run evidence (no value-production run yet).

## 11. Recommended next step

Fix the execution/distribution surface first (candidate 1 + 2 together):
ship the canonical SKILL.md trees in the wheel, make `setup-skills` resolve its
source from the installed package, and add a drift check so installed copies
cannot silently diverge. This is the smallest concrete change with the highest
leverage: it is a precondition for the user's product/interaction priority and
for trustworthy diagnostics generally. Verify it end-to-end in a clean venv
(`pip install dist/*.whl && sensemaking-skills setup-skills && diff` against
the canonical skills), because "done" for this boundary requires the real
install path to work, not just structure.

## 12. Recommended workflow

`architecture-implementation-workflow` from the official
`skills/workflow-planner/references/workflow-registry.yaml` — this is
architecture/refactoring work (packaging + install machinery), not a product,
docs, or UI problem. Allowed execution modes include `guided_execution`.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: experiments/product-interaction-p1-v1/charter-v1.md
user_implied_fog_type: product_fog
primary_fog_type: architecture_fog
diagnosis_conflict: true
escalation_recommended: true
evidence:
  - "src/sensemaking_skills/setup_skills.py (lines 29-30): source-checkout-only skills path resolution breaks pip installs"
  - "src/sensemaking_skills/setup_skills.py (lines 100-101): installed skills never overwritten without --force; silent staleness"
  - "pyproject.toml (line 49): package-data glob ships only src/sensemaking_skills/skills Python modules; wheel has no SKILL.md"
  - "GETTING_STARTED.md (lines 23-27): documented pip install + setup-skills flow cannot deliver skills from a wheel"
  - "skills/repo-sensemaker/SKILL.md (line 114): canonical skill forbids create-artifact.py path recomputation (ADR 0010, issue #40)"
  - "README.md (line 10): production-ready maturity claim conflicts with 60% progress and no value-production run (CONTEXT.md:322)"
  - "experiments/evaluation-design-e1-v1/final-decision-v1.md (line 11): DEMOTE label accuracy as primary gate"
  - "experiments/evaluation-design-e2-v1/final-decision-v1.md (line 11): USE_AS_TRIAGE_SIGNAL for decision_delta"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: execution-surface drift - installed skill surface != canonical repo skill; documented install path cannot deliver skills
weakness_type: Implicit Dependencies
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T18:58:25Z"
immutable: true
```

## 14. Ready-to-copy prompt

For `workflow-planner` (or an implementation agent):

> Fix the repo-sensemaker execution/distribution surface. The wheel at
> `dist/sensemaking_skills-0.2.1-py3-none-any.whl` contains no SKILL.md files
> (`pyproject.toml:49` globs only `src/sensemaking_skills/skills/**`), and
> `src/sensemaking_skills/setup_skills.py:29-30` resolves its source skills dir
> via a source-checkout-only relative path, so the documented
> `pip install sensemaking-skills && sensemaking-skills setup-skills` flow
> (GETTING_STARTED.md:23-27) cannot deliver canonical skills to a pip user;
> installed copies are never reconciled (setup_skills.py:100-101) and silently
> go stale (observed copy matches commit 178d5f0, 2026-05-22, and still teaches
> the create-artifact.py path recomputation forbidden by SKILL.md:114 / ADR
> 0010). Ship the canonical `skills/` trees in the wheel, resolve the setup
> source from the installed package (e.g. importlib.resources), and add a
> version/checksum drift check. Prove it with a clean-venv
> `pip install dist/*.whl && sensemaking-skills setup-skills` end-to-end run,
> then `diff` the installed skills against the canonical ones. Do not change
> the repo-sensemaker diagnostic contract itself in this step.
