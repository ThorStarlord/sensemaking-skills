# Repository Sensemaking Brief

Target: `ThorStarlord/sensemaking-skills` @ `aa13f40115b52f9e7687d742cbc8430d5a9a4a25`
(clean worktree). Invocation: conversational, `MANUAL_EXPLICIT_LOAD` of
`skills/repo-sensemaker/SKILL.md` at the same SHA. Probe backend: local Probe
Engine; same-episode report at `artifacts/history/2026-10-23-probe-report-observation.yaml`.

## 1. Repository goal

Documented (policy, not independently verified as achieved): an agent-native
repository decision-support and control layer for software-engineering agents
(`docs/adr/0029-current-product-boundary.md:18`), whose owner-selected long-term
destination is persistent, typed, source-grounded semantic stewardship
(`STATUS.md:59`, ADR 0031). `STATUS.md:6` projects the current phase as
CONSTRUCTION, with self-repository use of `repository-semantic-steward` as the
next bounded responsibility.

## 2. Current shape

Observed at the pinned SHA (probe `git_state`: 4722 tracked files, 0 untracked,
0 dirty):

- `skills/`: 52 Skill directories, each a `SKILL.md` plus references.
- `scripts/`: 41 `validate-*.py` validators, the Probe Engine
  (`probe-repo.py`, `repo_probes.py`, `probe_relationships.py`), the legacy
  `workflow-runtime.py`, and CI gates such as `gate_relationship_findings.py`.
- `src/sensemaking_skills/`: the installable package (CLI incl. `semantic`
  knowledge commands, Campaign semantics, and the legacy
  `runner.SkillsOrchestrator` compatibility wrapper).
- `docs/adr/`: 32 ADRs; `.sensemaking/knowledge/`: 2 reviewed knowledge files.
- `tests/`: 258 test files; `artifacts/`: tracked framework artifacts and
  dogfood records (including `artifacts/repository_sensemaking_brief.md`).
- `skills/workflow-planner/references/workflow-registry.yaml`: 23 workflows.

## 3. Strong signals

- **The brief contract is enforced, not just documented.** `scripts/validate-brief.py`
  rejected a non-conforming brief with four blocking errors when run in this
  episode (see Section 6).
- **Mechanical and semantic findings are deliberately separated.**
  `scripts/gate_relationship_findings.py:1-28` blocks only mechanically
  decidable ADR findings and routes `status_claim_mismatch` to semantic review.
  That is why this brief, not CI, interprets the probe's 28 ADR findings.
- **Unmeasured stays unmeasured.** The probe reports `test_case_count: null`
  because 42 lab modules need `rfc8785` (`requirements-lab.txt`), rather than
  reporting a partial count.
- **Steward invariants hold in code and tests.** The 46 semantic-knowledge tests
  run in this episode passed (one needed `PYTHONPATH=src` because the package
  is not installed here, an environment caveat rather than a defect).
- **State projection is current.** HEAD `aa13f40` merges PR #562
  ("reconcile PR #560/#561 as integrated"); vendored-Skill drift is 0.

## 4. Missing pieces

- **No test or caller covers the legacy `RepoSensemakerSkill` path.** A search of
  `tests/`, `src/` and `scripts/` found no caller of
  `SkillsOrchestrator.run_repo_sensemaker_skill`. That search scope is complete
  for in-repository callers; external API users are NOT ASSESSED.
- **The README declares no `scripts/*.py` verification entrypoints**, so the
  probe's verification gap is vacuous (`vg: 0.0` with note "no declared
  verification entrypoints found in README") even though CI runs 12 checks.
- **The reviewed knowledge has no `tested_by` link** for
  `inv:index-snapshot-vs-working-overlay`, although it cites two test files.

## 5. Improvement opportunities

- **Operating-map authority pointer is stale.** `docs/agent-native-operating-workflow.md:549`
  cites "REAL (ratified, ADR 0014)", and `:258` cites ADR 0014 for the routing
  deferral, but `docs/adr/0014-product-boundary.md:3` is SUPERSEDED by ADR 0029.
  The rule itself still holds (`docs/adr/0029-current-product-boundary.md:85`).
  The same pointer appears in `docs/semantic-control-map.md:52` and
  `docs/workflow-system-disposition.md:29,133`.
- **Steward reference wording lags `SKILL.md`.**
  `skills/repository-semantic-steward/references/knowledge-contract.md:49` and
  `references/bootstrap.md:9` predate PR #559. Their scope only partly overlaps
  `SKILL.md:31`, so this is a currency gap rather than a contradiction. The doc
  guard `tests/test_repository_semantic_steward.py:66-86` reads `SKILL.md` and
  `references/recall.md` only.
- **The fixture metric overstates a gap.** `fixtures_coverage.coverage: 0.49`
  lists 20 validators without `tests/fixtures/<name>/{valid,invalid}`, but every
  one has a dedicated test module (e.g. `validate-strategic-repository-analysis`
  -> `tests/test_strategic_repository_analysis_contract.py`). The metric measures
  a convention, not test coverage; not a Zero Validation finding.
- **The root `00-user-intent.md` is stale and unmarked.** It describes Phase 4
  infrastructure fixes and a "3-week rollout plan"; unlike `goal.md`, it has no
  historical marker. No runtime code reads it (runs create their own intent
  files).
- **The generic validator cannot see Section 15.** `scripts/validate-artifact.py:265`
  checks recommended fields as literal keys of the Section 13 block, so the
  dotted contract entries `extended_analysis.*`
  (`skills/workflow-planner/references/artifact-contracts.yaml:170-173`) always
  warn. Observed this episode: four identical warnings both for this brief,
  which has Section 15, and for the tracked `artifacts/repository_sensemaking_brief.md`,
  which has none. The warnings are non-blocking but carry no information. The
  contract's own comment places these fields in Section 15, not Section 13
  (`artifact-contracts.yaml:163-169`).
- **ADR status integrity candidates.** The probe flags ADR 0013 describing ADR
  0012 as superseded while `docs/adr/0012-invocation-paths.md:3` still reads
  Accepted. Documented, not deeply reviewed here.

## 6. Weakest boundary

**The legacy `RepoSensemakerSkill` producer of `repository_sensemaking_brief`.**
`SkillsOrchestrator.run_repo_sensemaker_skill()`
(`src/sensemaking_skills/runner.py:181`) instantiates `RepoSensemakerSkill`,
which writes the contract artifact id `repository_sensemaking_brief`
(`src/sensemaking_skills/skills/repo_sensemaker.py:49-50`) to a path it computes
itself, `<project_root>/artifacts/<id>.md` (`src/sensemaking_skills/paths.py:69`).
That bypasses runtime-owned path resolution, which `CLAUDE.md:87` forbids
("Never recompute `artifacts/<id>.md` independently").

The content does not satisfy the artifact's contract. When executed in this
episode against a disposable clone at the same SHA (never this checkout), it
**overwrote the tracked 229-line `artifacts/repository_sensemaking_brief.md`**
with a file inventory. It returned `success: True` and
`authority: "authorized_autonomously"`
(`src/sensemaking_skills/skills/repo_sensemaker.py:63`).
`validate-brief.py` rejected the result with `NO_LOGIC_TRACE`,
`MISSING_HANDOFF_SECTION`, `MISSING_EVIDENCE_EXCERPTS` and
`MISSING_HANDOFF_BLOCK`.

The capability catalog describes `repo-sensemaker` as non-mutating
(`src/sensemaking_skills/defaults/capability-registry.yaml:16`). This path
mutates the target. It is the same failure class the Skill's Execution Protocol
records (overwriting a tracked framework artifact by recomputing a path;
`skills/repo-sensemaker/SKILL.md:293`).

**Weakness type:** Contract Mismatch

The artifact claims to be a `repository_sensemaking_brief` but is not one in
shape, path or mutation behavior. Likelihood of harm is low: no in-repo caller
exists and the method is not shown in `API.md`. But the class it belongs to
(`API.md:6`) is a documented legacy surface, and nothing guards it.

## 6.5. Problem classification (fog type)

`architecture_fog`: the problem is an implicit producer/consumer and
path-ownership contract broken inside a compatibility surface, not unclear
user needs, UI, or missing documentation. The user's intent was fog-neutral
(`unknown`), so there is no intent-vs-diagnosis conflict.

## 7. Evidence

<!-- mode: investigative -->

The weakest-boundary claim rests on direct reads and one execution.
`src/sensemaking_skills/skills/repo_sensemaker.py:49-50` writes the artifact,
`src/sensemaking_skills/paths.py:69` resolves the flat path, and
`src/sensemaking_skills/runner.py:181` exposes the entrypoint.
`CLAUDE.md:87` and `skills/repo-sensemaker/SKILL.md:293` state the path-ownership
rule and its incident history.
`skills/workflow-planner/references/artifact-contracts.yaml:117-124` declares
the artifact and its four consumers.

Logic trace: Observed O1, the legacy stub writes the contract artifact id at a
self-computed flat path (`repo_sensemaker.py:49-50`, `paths.py:69`). Observed O2,
repository instructions forbid exactly that (`CLAUDE.md:87`). Observed O3,
executing the stub in a disposable clone overwrote the tracked brief and
reported success with autonomous authority. Observed O4, the canonical validator
rejects the output with four blocking errors. Observed O5, no in-repo caller or
test exercises the path. Derived R1 (from O1+O3+O4): a reachable producer of
`repository_sensemaking_brief` violates the artifact's shape contract, its path
contract and the declared non-mutation of its capability. Inferred C1 (from R1+O5):
nothing currently prevents a legacy API user from silently replacing a tracked
brief with a contract-invalid one while being told it succeeded; the four
consumers listed in `artifact-contracts.yaml:120-124` would then read invalid
input. Limit L1: no evidence that anyone calls the method today; external usage
is NOT ASSESSED, so harm is latent, not demonstrated. Open question U1 (owner
intent): should this legacy method be retired or made fail-closed? That changes
the fix, not the diagnosis. Bounded conclusion: the weakest consequential
boundary is this unguarded legacy producer, classified Contract Mismatch, with
low likelihood and high integrity cost if exercised.

State currency and provenance:

- **Verified current (measured/observed this episode):** worktree state and HEAD
  (probe `git_state`); stub behavior (direct execution in a disposable clone);
  validator verdict; caller absence (grep over `tests/`, `src/`, `scripts/`);
  semantic test results (local pytest run).
- **Documented but not independently verified:** `STATUS.md` claims about hosted
  CI runs (Product Validation / Release Candidate Distribution) were not
  re-queried; ADR authority statements are document observations, not verified
  policy outcomes.
- **Inference:** the integrity consequence for downstream consumers (C1).
- **Owner-supplied context:** none beyond the observation request.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: src/sensemaking_skills/skills/repo_sensemaker.py
    lines: L49-L50
    quote: |
                  artifact_id = "repository_sensemaking_brief"
                  self.write_artifact(artifact_id, brief_content)
    supports_claim: "The legacy stub writes the contract artifact id."
  - file: src/sensemaking_skills/paths.py
    lines: L69
    quote: 'return (self.artifacts_dir() / f"{artifact_id}.md").resolve()'
    supports_claim: "Its path is recomputed as a flat artifacts/<id>.md, not runtime-resolved."
  - file: CLAUDE.md
    lines: L87
    quote: '`context["expected_output_path"]` — and write exactly there. Never recompute'
    supports_claim: "Repository instructions forbid independent path recomputation."
  - file: src/sensemaking_skills/runner.py
    lines: L181
    quote: "def run_repo_sensemaker_skill(self) -> Dict[str, Any]:"
    supports_claim: "The path is reachable through the legacy SkillsOrchestrator API."
  - file: src/sensemaking_skills/skills/repo_sensemaker.py
    lines: L63
    quote: '"authority": "authorized_autonomously",'
    supports_claim: "The stub self-reports autonomous authority on success."
  - file: src/sensemaking_skills/defaults/capability-registry.yaml
    lines: L16
    quote: "mutates_repository: false"
    supports_claim: "The repo-sensemaker capability is declared non-mutating."
  - file: skills/workflow-planner/references/artifact-contracts.yaml
    lines: L117
    quote: "- id: repository_sensemaking_brief"
    supports_claim: "The artifact the stub claims to produce has a declared contract."
  - file: docs/adr/0014-product-boundary.md
    lines: L3
    quote: "**Status**: SUPERSEDED — 2026-09-11 by ADR 0029"
    supports_claim: "Operating-map citations of ADR 0014 as ratified point at a superseded ADR."
  - file: skills/repository-semantic-steward/references/bootstrap.md
    lines: L9
    quote: "Current worktree may be dirty; use a separate clean worktree for index commands."
    supports_claim: "Steward reference wording predates the PR #559 'not a development gate' guidance."
  - file: probe-report.yaml
    lines: L31
    quote: "vg: 0.0"
    supports_claim: "Verification gap is vacuous: README declares no scripts/*.py checks."
  - file: probe-report.yaml
    lines: L68
    quote: "coverage: 0.49"
    supports_claim: "Fixture-convention coverage, which overstates untested validators."
  - file: probe-report.yaml
    lines: L41
    quote: "test_case_count: null"
    supports_claim: "Test case count is unmeasured, not zero."
```

## 9. Why this boundary matters

The repository's founding rule is that artifacts are the API between Skills,
with one owner for artifact paths (`CLAUDE.md`). The brief is the most-consumed
diagnostic artifact (`workflow-planner`, `prompt-handoff`,
`sensemaking-docs-reconciler`, `output-reconciler`). A producer that silently
replaces it with invalid content while reporting success and autonomous
authority defeats the validator only if nobody validates. And it destroys the
previous tracked artifact either way. This failure class has already happened
once (ADR 0010 / issue #40 history cited at `skills/repo-sensemaker/SKILL.md:293`).

## 10. Candidate next steps

1. Retire `SkillsOrchestrator.run_repo_sensemaker_skill` and
   `RepoSensemakerSkill` (removes the only non-conforming producer; changes a
   documented legacy API class).
2. Keep the method but make it fail closed (raise a deprecation error pointing
   at the agent-native Skill), with a regression test asserting it never writes
   under `artifacts/`.
3. Reconcile the operating-map, semantic-control-map and disposition
   citations from ADR 0014 to ADR 0029.
4. Reconcile `bootstrap.md:9` / `knowledge-contract.md:49` wording with
   `SKILL.md:31`, and extend the steward doc guard to the references.
5. Add `tested_by` links for `inv:index-snapshot-vs-working-overlay` in the
   reviewed knowledge (steward RECONCILE, ADD).

## 11. Recommended next step

Choose between steps 1 and 2 for the legacy producer, then implement the chosen
option together with a regression test that runs it against a disposable target
and asserts no tracked file under `artifacts/` changes. The current-state claims
this rests on are verified by direct execution in this episode, not merely
documented. The choice is a public-surface decision (`API.md:6` documents the
class), so it is presented for owner ratification, not as decided.

Separately, steps 3-5 are repository-evidence-resolved guidance and knowledge
fixes within `STATUS.md`'s current responsibility ("focused Skill/currentness
reconciliation"). They are ready regardless of the owner's answer above.

## 12. Recommended workflow

None. `architecture-implementation-workflow` exists in the registry and is
available from this target, since the repository vendors `workflow-planner`
itself. But it chains domain alignment, a refactor spec, issue decomposition
and TDD, which is disproportionate for a one-method change. This is ordinary
coding work. Truthful no-match: `recommended_workflow_id: null` with
`escalation_recommended: true`. The escalation carries the owner decision in
Section 11.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: .sensemaking/receipts/2026-10-23-observe-skills.session.yaml
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: true
evidence:
  - "src/sensemaking_skills/skills/repo_sensemaker.py (lines L49-L50): legacy stub writes repository_sensemaking_brief"
  - "src/sensemaking_skills/paths.py (lines L69): flat artifacts/<id>.md path recomputed outside the runtime"
  - "CLAUDE.md (lines L87): repository forbids independent artifact path recomputation"
  - "src/sensemaking_skills/runner.py (lines L181): reachable via legacy SkillsOrchestrator"
  - "disposable-clone execution at aa13f40: tracked artifacts/repository_sensemaking_brief.md overwritten; validate-brief.py 4 blocking errors"
  - "probe-report.yaml (lines L31, L41, L68): vg vacuous, test_case_count unmeasured, fixture metric is convention-only"
recommended_workflow_id: null
recommended_execution_mode: plan_only
weakest_boundary: "Legacy RepoSensemakerSkill writes a contract-invalid repository_sensemaking_brief to a self-computed path, overwriting tracked artifacts"
weakness_type: Contract Mismatch
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-10-23T05:53:38Z"
immutable: true
representation_sufficiency:
  status: sufficient
  rationale: >-
    The stub's behavior was observed directly by execution and validation; no
    further representation is needed to support the diagnosis. The open
    question (retire vs fail-closed) is owner intent, not missing evidence.
  needed_representation: null
```

## 14. Ready-to-copy prompt

> In `ThorStarlord/sensemaking-skills`, the legacy
> `SkillsOrchestrator.run_repo_sensemaker_skill()` writes a contract-invalid
> `repository_sensemaking_brief` to `artifacts/repository_sensemaking_brief.md`
> and overwrites the tracked file (observed at `aa13f40`). The owner has chosen
> [retire | fail-closed]. Implement that choice in `src/sensemaking_skills/runner.py`
> and `src/sensemaking_skills/skills/repo_sensemaker.py`. Add a regression test
> that runs against a disposable git clone and asserts that no tracked file under
> `artifacts/` changes. Update `API.md` if the method's behavior changes. Do not
> touch the agent-native `skills/repo-sensemaker/SKILL.md`.

## 15. Extended analysis

```yaml
extended_analysis:
  schema_version: 1
  domain:
    - architecture
    - docs
  consequential_boundary:
    description: >
      Whether the legacy SkillsOrchestrator brief producer remains callable in
      a form that can replace tracked artifacts, given that SkillsOrchestrator
      is a documented legacy API class.
    rationale: >
      The fix shape (retire vs fail-closed) depends on public-surface intent;
      the rest of the brief's recommendations do not.
    is_demonstrated_weakness: true
  uncertainty:
    source: owner_intent
    question: >
      Should the legacy run_repo_sensemaker_skill path be removed from the
      public legacy API, or kept and made to fail closed?
  owner_intent_state:
    known: >
      The owner asked only to observe the Skills. STATUS.md (an owner-reconciled
      projection) authorizes self-repository steward use and focused
      Skill/currentness reconciliation, and says deletion of compatibility
      machinery is evidence-gated. No owner statement covers this method.
    status: thin
```
